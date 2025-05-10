# QChat

QChat is a Python framework for building chat interfaces with QT6, featuring command decorators and automatic type conversion.

![QChat Screenshot](img/qchat_screenshot.png)

## Features

- 🎨 **QT6-based UI**: Modern, customizable chat interface
- ✨ **Command Decorators**: Easily turn functions into chat commands
- 🔄 **Auto Type Conversion**: Automatic argument type conversion
- 📚 **Built-in Help**: Auto-generated help system
- 🚀 **Lightweight**: Minimal dependencies

## A Simple Example

```python
import qchat

@qchat.command("greet")
def greet(name: str):
    """Greet a user"""
    return f"Hello, {name}!"

if __name__ == "__main__":
    qchat.run()

```

## Installation

### Prerequisites

- Python 3.8+
- pip

### Setup

```bash
pip install qchat
```

## Advanced Features
Type Conversion:

```python
@qchat.command("add")
def add_numbers(a: int, b: int):
    """Add two numbers"""
    return f"Result: {a + b}"
```

Variable Arguments:

```python
@qchat.command("echo")
def echo_message(*args):
    """Echo back the input"""
    return " ".join(args)
```

## Hacking on QChat

install pyside6 with the following command:

```bash
pip install pyside6
```

update the ui file and convert it to python code with the following command:

```bash
pyside6-uic.exe .\main_window.ui -o .\main_window.py
```

### License
MIT License. See LICENSE for details.