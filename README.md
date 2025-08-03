# Alt App Installer CLI

A command-line version of [Alt App Installer](https://github.com/mjishnu/alt-app-installer)

## 🚀 Quick Start

- Download the executable from [releases](https://github.com/mjishnu/alt-app-installer-cli/releases)
- Run: 
```bash
./altappinstaller.exe "app url"
```

## 📋 Usage

```bash
python main.py <URL> [OPTIONS]
```

### Basic Examples
```bash
# Simple download and install
python main.py https://example.com/app

# Download only
python main.py https://example.com/app -d

# Custom output directory
python main.py https://example.com/app -o ./my-downloads
```

## 🔧 Command Line Options

| Short | Long | Description | Choices | Default |
|-------|------|-------------|---------|---------|
| `-v` | `--version` | Show version information | - | - |
| `-d` | `--download_only` | Download only, don't install | - | `False` |
| `-deps` | `--dependencies` | Dependency handling mode | `all`, `required`, `ignore_ver`, `none` | `required` |
| `-p` | `--progress` | Progress bar type | `full`, `simple`, `none` | `full` |
| `-o` | `--output` | Output directory | Any valid path | `./downloads` |
| `-a` | `--arch` | Target architecture | `x64`, `arm`, `arm64`, `x86`, `auto` | `auto` |

### Dependency Options

- **`all`**: Install all available dependencies
- **`required`**: Install only latest version of dependencies accrording to your current architecture (default)
- **`ignore_ver`**: Install all version of dependencies for your current architecture
- **`none`**: Skip dependencies entirely

### Progress Bar Options

- **`full`**: Complete progress bar with details (default)
- **`simple`**: Lightweight for legacy terminals
- **`none`**: Text-only output

## 📸 Screenshots

![Screenshot 2024-06-20 134921-min](https://github.com/mjishnu/alt-app-installer-cli/assets/83004520/d47bdc96-ff57-43b0-bd96-c4c77ad18375)

![Screenshot 2024-06-20 135021-min](https://github.com/mjishnu/alt-app-installer-cli/assets/83004520/b9d217d5-8eb9-469c-9d9d-d2d31f3d42f1)

![Screenshot 2024-06-20 135001-min](https://github.com/mjishnu/alt-app-installer-cli/assets/83004520/e9975215-dbd6-4480-a879-7b682ee9abbb)

## 🔥 Advanced Examples

```bash
# Download all dependencies with simple progress bar
python main.py https://example.com/app --dependencies all --progress simple

# Specific architecture, no dependencies
python main.py https://example.com/app --arch x64 --dependencies none

# Custom output with download only
python main.py https://example.com/app -d -o ./custom-folder --progress full
```

## 🛠️ Building from Source

### Prerequisites
- [Git](https://git-scm.com/download/win)
- Python 3.8+
- pip

### Steps
1. **Clone the repository**
   ```bash
   git clone https://github.com/mjishnu/alt-app-installer-cli
   cd alt-app-installer-cli
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   cd app
   python main.py "your-app-url"
   ```

## 🔍 Troubleshooting

| Issue | Solution |
|-------|----------|
| No progress bar visible | Try `--progress simple` or `--progress none` |
| Wrong architecture | Use `--arch x64/x86/arm/arm64` |
| Download fails | Check internet connection and URL validity |

## 📝 Version Information

```bash
./altappinstaller.exe -v
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/mjishnu/alt-app-installer-cli/blob/main/LICENSE) file for details.

## 🆘 Support

- 🐛 [Report Issues](https://github.com/mjishnu/alt-app-installer-cli/issues)
- 🌐 [Discord](https://discord.gg/9eeN2Wve4T)
- 📖 Check the documentation above for common solutions

## ⭐ Show your support

Give a ⭐️ if this project helped you!