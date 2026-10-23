#!/usr/bin/env python3
"""Check package identity, stock-updater isolation, and launcher restarts."""

import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile


source = Path(__file__).resolve().parent.parent
name = "Updater (pvaibhav)"
platforms = ("tg5040", "tg5050", "my355", "h700")

with tempfile.TemporaryDirectory(prefix="nextui-updater-package-") as temporary:
    root = Path(temporary)
    shutil.copy(source / "pak.json", root / "pak.json")
    binary = root / "target/aarch64-unknown-linux-gnu/release/nextui-updater-rs"
    binary.parent.mkdir(parents=True)
    binary.write_text('''#!/bin/sh
attempt=0
[ ! -f attempts.txt ] || attempt=$(cat attempts.txt)
attempt=$((attempt + 1))
echo "$attempt" > attempts.txt
echo "attempt $attempt"
echo "stderr $attempt" >&2
[ "$attempt" -ne 1 ] || exit 5
exit 0
''')
    binary.chmod(0o755)
    subprocess.run(["bash", str(source / "scripts/create_pak.sh")], cwd=root,
                   check=True, stdout=subprocess.DEVNULL)

    with zipfile.ZipFile(root / "nextui.updater.pakz") as package:
        assert package.testzip() is None
        for platform in platforms:
            prefix = f"Tools/{platform}/{name}.pak/"
            metadata = json.loads(package.read(prefix + "pak.json"))
            assert metadata["name"] == name
            assert metadata["repo_url"] == "https://github.com/pvaibhav/nextui-updater-pak"
            assert not any(path.startswith(f"Tools/{platform}/Updater.pak/")
                           for path in package.namelist())

        sdcard = root / "sdcard"
        package.extractall(sdcard)
        before = {path: (sdcard / path).read_bytes() for path in package.namelist()
                  if not path.endswith("/")}

        # Pak Store's official entry installs into Updater.pak.
        stock = root / "stock-updater.pakz"
        with zipfile.ZipFile(stock, "w") as archive:
            for platform in platforms:
                archive.writestr(f"Tools/{platform}/Updater.pak/nextui-updater", "stock updater")
        with zipfile.ZipFile(stock) as archive:
            archive.extractall(sdcard)
        assert all((sdcard / path).read_bytes() == data for path, data in before.items())

        tool = sdcard / f"Tools/tg5040/{name}.pak"
        (tool / "nextui-updater").chmod(0o755)
        subprocess.run(["sh", str(tool / "launch.sh")], cwd=root, check=True)
        assert (tool / "attempts.txt").read_text().strip() == "2"
        assert (tool / "logs.txt").read_text().splitlines() == [
            "attempt 1", "stderr 1", "attempt 2", "stderr 2"]

print("Package identity, stock-updater isolation, and launcher restart checks passed.")
