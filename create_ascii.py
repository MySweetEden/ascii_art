import argparse
import platform
from typing import List, Tuple

import cv2
from PIL import Image, ImageDraw, ImageFont

# Define ASCII characters based on intensity
ASCII_CHARS = "@%#*+=-:. "


def resize_image_for_ascii(
    image: cv2.Mat, char_width: int = 6, char_height: int = 12
) -> Tuple[cv2.Mat, int, int]:
    """
    Resize the image for ASCII conversion by downsizing based on character dimensions.
    Each ASCII character corresponds to char_width x char_height pixels.

    Args:
        image (cv2.Mat): Grayscale image loaded via OpenCV.
        char_width (int): Width of an ASCII character in pixels.
        char_height (int): Height of an ASCII character in pixels.

    Returns:
        Tuple[cv2.Mat, int, int]: Resized image, new width, and new height.
    """
    original_height, original_width = image.shape

    # Calculate the new dimensions for downsizing
    new_width = original_width // char_width
    new_height = original_height // char_height

    # Resize the image
    resized_image = cv2.resize(image, (new_width, new_height))

    return resized_image, new_width, new_height


def image_to_ascii(image: cv2.Mat, ascii_chars: str = ASCII_CHARS) -> List[str]:
    """
    Convert a grayscale image to ASCII characters.

    Args:
        image (cv2.Mat): Grayscale image.
        ascii_chars (str): Characters to represent intensity levels.

    Returns:
        List[str]: ASCII art as a list of strings.
    """
    scale = 256 // len(ascii_chars)
    return [
        "".join(ascii_chars[min(len(ascii_chars) - 1, pixel // scale)] for pixel in row)
        for row in image
    ]


def get_default_font() -> str:
    """
    Return a default monospaced font path based on the operating system.

    Returns:
        str: Path to a monospaced font.
    """
    system = platform.system()
    if system == "Darwin":  # macOS
        return "/System/Library/Fonts/Supplemental/Menlo.ttc"
    elif system == "Windows":  # Windows
        return "C:\\Windows\\Fonts\\consola.ttf"  # Consolas
    elif system == "Linux":  # Linux
        return "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
    else:
        raise RuntimeError("Unsupported OS. Please specify a font manually.")


def ascii_to_image(
    ascii_art: List[str],
    output_path: str = "output.png",
    font_path: str = None,
    original_width: int = 960,
    original_height: int = 1280,
):
    """
    Render ASCII art to an image and save it.

    Args:
        ascii_art (List[str]): ASCII art as a list of strings.
        output_path (str): Path to save the output image.
        font_path (str): Path to the font file.
        original_width (int): Width of the output image.
        original_height (int): Height of the output image.
    """
    # Calculate character dimensions
    char_width = original_width / len(ascii_art[0])  # Width per character
    char_height = original_height / len(ascii_art)  # Height per character

    # Create a blank white canvas
    image = Image.new("RGB", (original_width, original_height), "white")
    draw = ImageDraw.Draw(image)

    # Load the font
    font_path = font_path or get_default_font()
    font_size = int(min(char_width, char_height) * 1.5)
    font = ImageFont.truetype(font_path, font_size)

    # Draw each character onto the canvas
    for i, line in enumerate(ascii_art):
        for j, char in enumerate(line):
            x = int(j * char_width)
            y = int(i * char_height)
            draw.text((x, y), char, fill="black", font=font)

    # Save the image
    image.save(output_path)
    print(f"ASCII art saved to {output_path}")


def convert_image_to_ascii(image_path: str, output_path: str):
    """
    Convert an image to ASCII art and save the output as an image.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the output ASCII art image.
    """
    # Load the image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Image not found at {image_path}")

    # Downsize the image for ASCII conversion
    downsized_image, ascii_width, ascii_height = resize_image_for_ascii(image)

    # Convert the downsized image to ASCII
    ascii_art = image_to_ascii(downsized_image)

    # Render the ASCII art to an image with the original dimensions
    ascii_to_image(
        ascii_art,
        output_path=output_path,
        original_width=image.shape[1],
        original_height=image.shape[0],
    )


if __name__ == "__main__":
    # Set up the argument parser
    parser = argparse.ArgumentParser(
        description="Convert an image to ASCII art and save it as an image."
    )
    parser.add_argument("-i", "--input", required=True, help="Path to the input image")
    parser.add_argument(
        "-o", "--output", required=True, help="Path to save the output ASCII art image"
    )

    # Parse the arguments
    args = parser.parse_args()

    # Call the function with the provided arguments
    convert_image_to_ascii(args.input, args.output)
