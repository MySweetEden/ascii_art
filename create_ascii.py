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

    Args:
        image (cv2.Mat): Grayscale image loaded via OpenCV.
        char_width (int): Width of an ASCII character in pixels.
        char_height (int): Height of an ASCII character in pixels.

    Returns:
        Tuple[cv2.Mat, int, int]: Resized image, new width, and new height.
    """
    original_height, original_width = image.shape
    new_width = original_width // char_width
    new_height = original_height // char_height
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
    ascii_art: List[str], output_path: str, original_width: int, original_height: int
):
    """
    Render ASCII art to an image and save it.

    Args:
        ascii_art (List[str]): ASCII art as a list of strings.
        output_path (str): Path to save the output image.
        original_width (int): Width of the output image.
        original_height (int): Height of the output image.
    """
    char_width = original_width / len(ascii_art[0])
    char_height = original_height / len(ascii_art)

    image = Image.new("RGB", (original_width, original_height), "white")
    draw = ImageDraw.Draw(image)

    font_path = get_default_font()
    font_size = int(min(char_width, char_height) * 1.5)
    font = ImageFont.truetype(font_path, font_size)

    for i, line in enumerate(ascii_art):
        for j, char in enumerate(line):
            x = int(j * char_width)
            y = int(i * char_height)
            draw.text((x, y), char, fill="black", font=font)

    image.save(output_path)
    print(f"ASCII art saved to {output_path}")


def convert_image_to_ascii_art(image_path: str) -> Tuple[List[str], Tuple[int, int]]:
    """
    Convert an image to ASCII art.

    Args:
        image_path (str): Path to the input image.

    Returns:
        Tuple[List[str], Tuple[int, int]]: ASCII art as a list of strings and original image dimensions.
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Image not found at {image_path}")

    downsized_image, ascii_width, ascii_height = resize_image_for_ascii(image)
    ascii_art = image_to_ascii(downsized_image)

    return ascii_art, image.shape


def save_ascii_art_to_image(
    ascii_art: List[str], output_path: str, original_shape: Tuple[int, int]
):
    """
    Save ASCII art as an image.

    Args:
        ascii_art (List[str]): ASCII art as a list of strings.
        output_path (str): Path to save the output ASCII art image.
        original_shape (Tuple[int, int]): Original image dimensions (height, width).
    """
    original_height, original_width = original_shape
    ascii_to_image(ascii_art, output_path, original_width, original_height)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert an image to ASCII art and save it as an image."
    )
    parser.add_argument("-i", "--input", required=True, help="Path to the input image")
    parser.add_argument(
        "-o", "--output", required=True, help="Path to save the output ASCII art image"
    )

    args = parser.parse_args()

    ascii_art, original_shape = convert_image_to_ascii_art(args.input)
    save_ascii_art_to_image(ascii_art, args.output, original_shape)
