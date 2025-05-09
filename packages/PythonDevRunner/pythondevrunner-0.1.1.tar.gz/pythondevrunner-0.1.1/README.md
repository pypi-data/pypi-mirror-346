
# PythonDevRunner

Auto-reload your Python app when source files change. Useful for development of web servers, CLI tools, or any script-driven workflow.

## 🚀 Features

- Watches for changes in `.py` files
- Automatically restarts your app
- Configurable via CLI or JSON file
- Cross-platform support

## 🛠 Installation

```bash
pip install .
```

## 💡 Usage

### CLI

```bash
devrunner --entry main.py --watch-ext .py --exclude venv __pycache__ --debounce 0.5
```

### Config file

```bash
devrunner --config examples/config.json
```

## 🔧 Configuration Options

| Option       | CLI Flag       | Config Key   | Default    |
|--------------|----------------|--------------|------------|
| Entry script | `--entry`      | `entry`      | `main.py`  |
| Extensions   | `--watch-ext`  | `watch_ext`  | `[".py"]`  |
| Exclude      | `--exclude`    | `exclude`    | `[]`       |
| Debounce     | `--debounce`   | `debounce`   | `0.5`      |
| Verbose      | `--quiet`      | `quiet`      | `false`    |

## 📦 Packaging

Supports installation via `pip install .` and CLI via `devrunner`.

---

## License

MIT
