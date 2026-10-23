![](./doc/screenshot.png)

# NextUI OTA Updater PAK

This fork updates devices from [pvaibhav/NextUI](https://github.com/pvaibhav/NextUI) releases tagged `v<version>-pvaibhav.<revision>`. It gets updater self-updates from [pvaibhav/nextui-updater-pak](https://github.com/pvaibhav/nextui-updater-pak). Wi-Fi is required.

Based on the [official NextUI updater by LanderN](https://github.com/LoveRetro/nextui-updater-pak).

## Installation

The pvaibhav firmware includes this updater. To install it separately, extract `nextui.updater.pakz` (a ZIP archive) to the root of your SD card and merge the contents.

## Controls

- **D-pad Up/Down**: Navigate between buttons
- **Button A**: Select
- **Button B**: Go Back/Exit
- **Button X**: Version Select

## Building for tg5040/tg5050/my355/h700 using [cross-rs](https://github.com/cross-rs/cross)

```bash
cross build --release --target=aarch64-unknown-linux-gnu
```

The compiled binary will be in `target/aarch64-unknown-linux-gnu/release/nextui-updater-rs`.

## Building release zip

```bash
scripts/create_pak.sh
```

The package will be in `./nextui.updater.pakz`, with separate ZIPs for each platform.

## License

This project is open source and available under the MIT License.

## Contributing

Many improvements are possible and contributions are welcome! Please feel free to submit a Pull Request.
