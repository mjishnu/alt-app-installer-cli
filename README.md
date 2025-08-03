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
| `-h` | `--help` | Show help information | - | - |
| `-d` | `--download_only` | Download only, don't install | - | `False` |
| `-deps` | `--dependencies` | Dependency handling mode | `all`, `required`, `ignore_ver`, `none` | `required` |
| `-p` | `--progress` | Progress bar type | `full`, `simple`, `none` | `full` |
| `-o` | `--output` | Output directory | Any valid path | `./downloads` |
| `-a` | `--arch` | Target architecture | `x64`, `arm`, `arm64`, `x86`, `auto` | `auto` |

### Dependency Options

- **`all`**: Install all available dependencies
- **`required`**: Install only latest version of dependencies according to your current architecture (default)
- **`ignore_ver`**: Install all version of dependencies for your current architecture
- **`none`**: Skip dependencies entirely

### Progress Bar Options

- **`full`**: Complete progress bar with details (default)
- **`simple`**: Lightweight for legacy terminals
- **`none`**: Text-only output

## 📸 Screenshots
<img alt="Screenshot 2025-08-04 013759" src="https://github.com/user-attachments/assets/2ea32cae-8021-4036-84a1-92f3ccb0c51c" />
<br><br>

<img alt="Screenshot 2025-08-04 014437" src="https://github.com/user-attachments/assets/c3b88b19-b589-4c6c-884c-d3b9768e332f" />

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
