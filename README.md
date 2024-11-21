# ASCII Art Generator
This Python program converts images into ASCII art and saves the resulting art as an image. The project leverages OpenCV for image processing and Pillow for rendering the ASCII art into an output image.

## Features
- Resize images for ASCII representation.
- Convert grayscale intensity to ASCII characters.
- Save ASCII art as an image file.
- Cross-platform compatibility with font customization.

## Requirements
- Python 3.12+
- Dependency Management: pyproject.toml and uv.lock


Install the required libraries using uv:
```
uv sync
```

## Usage
### 1. Clone the repository:
```
git clone https://github.com/yourusername/ascii-art-generator.git
cd ascii-art-generator
```

### 2. Install dependencies:
Ensure you have uv installed (or your preferred dependency management tool):
```
pip install pipx
pipx install uv
```

Then, install the dependencies specified in pyproject.toml and uv.lock:
```
uv sync
```

### 3. Run the program:
#### Option 1: Direct execution
Run the main script to process an image and save the ASCII art:

```
python run_ascii.py
```

Update the input_image_path and output_ascii_art_path variables in run_ascii.py to specify the paths for the input and output files.

#### Option 2: Import and use as a library
You can also use the program in other scripts by importing the main function:

```
from create_ascii import convert_image_to_ascii

convert_image_to_ascii("path/to/input.jpg", "path/to/output.png")
```

### 4. Example Input and Output
- Input Image:
    - image.jpg
- Output ASCII Art Image:
    - ascii_art.png

## How It Works
1.	The input image is loaded in grayscale using OpenCV.
2.	The image is resized based on ASCII character dimensions.
3.	Each pixel’s intensity is mapped to an ASCII character.
4.	The ASCII art is rendered onto an image using Pillow and saved to the specified path.

## Customization
### Font Customization

To use a custom font for rendering the ASCII art, update the get_default_font function in create_ascii.py or pass the path to your font file when calling ascii_to_image.

### ASCII Character Set
Modify the ASCII_CHARS constant in create_ascii.py to use a different set of characters.

## License
This project is licensed under the MIT License. See the LICENSE file for details.