# 🐍 pmoschos_art_gen 🌈

A Simple Colorful Rainbow ASCII Art Generator.

## Installation

```bash
pip install pmoschos_art_gen
```

## Usage

### Command Line

Once installed, you can use the `pmoschos-art` command in your terminal:

```bash
# Provide text directly
pmoschos-art "Hello World"

# Disable horizontal centering
pmoschos-art "Hello World" --no-center

# Disable vertical centering
pmoschos-art "Hello World" --no-vcenter

# Disable both
pmoschos-art "Hello World" --no-center --no-vcenter

# Use interactive mode
pmoschos-art
```

Use double spaces to create new lines:

```bash
pmoschos-art "Hello  World"
```

### Python API

You can also use `pmoschos_art_gen` in your Python scripts:

```python
from pmoschos_art_gen import generate_rainbow_ascii

# Generate rainbow ASCII art
art = generate_rainbow_ascii("Hello World")
print(art)

# No centering
art = generate_rainbow_ascii("Hello World", center=False, vertical_center=False)
print(art)

# Horizontal centering only
art = generate_rainbow_ascii("Hello World", center=True, vertical_center=False)
print(art)

# Vertical centering only
art = generate_rainbow_ascii("Hello World", center=False, vertical_center=True)
print(art)

# Create multi-line text with double spaces
art = generate_rainbow_ascii("Hello  World  !")
print(art)
```

```python
from pmoschos_art_gen import render_ascii_lines, center_ascii_output

# Generate raw ASCII art lines without centering
lines = ["Hello", "World"]
ascii_lines = render_ascii_lines(lines)
print("\n".join(ascii_lines))

# Apply centering to existing lines
centered_lines = center_ascii_output(ascii_lines, vertical=True)
print("\n".join(centered_lines))
```

## Features

- Rainbow colored ASCII art 🌈
- Multiple line support
- Auto-centering in the terminal
- Simple API for integration
- Command-line interface


## License
This project is protected under the [MIT License](https://mit-license.org/).

## Contact
Panagiotis Moschos - www.linkedin.com/in/panagiotis-moschos

<h1 align=center>👨‍💻 Happy Coding 👨‍💻</h1>

<p align="center">
  Made by Panagiotis Moschos
</p>
