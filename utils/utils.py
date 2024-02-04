import os
import io
import re
import time
from PIL import Image
from datetime import datetime
from unidecode import unidecode
from requests import Session, Response
from requests.exceptions import HTTPError


SPECIAL_CHARS_DICT = {
            "?": "question mark",
            "!": "exclamation mark",
            "#": "number sign",
            "$": "dollar sign",
            "%": "percent sign",
            "&": "ampersand",
            "'": "apostrophe",
            "(": "left parenthesis",
            ")": "right parenthesis",
            "*": "asterisk",
            "+": "plus sign",
            ",": "comma",
            "-": "hyphen",
            ".": "period",
            "/": "forward slash",
            ":": "colon",
            ";": "semicolon",
            "<": "less than sign",
            "=": "equals sign",
            ">": "greater than sign",
            "?": "question mark",
            "@": "at sign",
            "[": "left square bracket",
            "\\": "backslash",
            "]": "right square bracket",
            "^": "caret",
            "_": "underscore",
            "`": "grave accent",
            "{": "left curly bracket",
            "|": "vertical bar",
            "}": "right curly bracket",
            "~": "tilde",
        }
    

def replace_special_chars(string: str) -> str:
    """
    Replaces special characters in a string with their corresponding replacements.

    Args:
    string(str): The original string.

    Returns:
    str: The string with special characters replaced.
    """
    special_chars = SPECIAL_CHARS_DICT
    for char, replacement in special_chars.items():
        string = string.replace(char, replacement)
    return string


def format_string(string: str) -> str:
    """
    Formats a string by removing non-word characters, converting to lowercase, replacing spaces with hyphens and replacing non-Latin characters with their closest Latin analogs.

    Args:
    string(str): The original string.

    Returns:
    str: The formatted string.
    """
    string = re.sub(r"[^\w\s]", '', string.strip())
    string = re.sub(r"\s+", '-', string.lower())
    string = unidecode(string)
    return string


def get_formatted_string(string: str, alt_string: str) -> str:
    """
    Formats a string so it is suitable as a file path.

    Args:
    string(str): The original string.
    alt_string(str): An alternative string.

    Returns:
    str: The formatted string. If the string is empty then function was unable to format it.
    """
    formatted_string = format_string(string)
    if not formatted_string:
        formatted_string = format_string(alt_string)
        if not formatted_string:
            formatted_string = format_string(replace_special_chars(string))
            if not formatted_string:
                formatted_string = format_string(replace_special_chars(alt_string))
    return formatted_string


def load_lines(file_path: str, separator: str = "\n") -> list:
    """
    Reads a file and splits its content into lines based on a given separator.

    Args:
        file_path (str): Path to the file to read.
        separator (str): Separator to use for splitting the file content.

    Returns:
        list: A list of lines read from the file.
    """
    with open(file_path, 'r') as f:
        content = f.read()
        lines = re.split(separator, content)
        return lines


def save_cover(cover_path: str, cover: bytes, resolution: tuple = (1024, 1024)):
    """
    Saves the cover art to a file.

    Args:
        cover_path (str): The path to save the cover art.
        cover (bytes): The content of the cover art in bytes.
        resolution (tuple): A tuple containing the desired width and height (e.g. (1024, 1024))
    """
    try:
        dir_path = os.path.dirname(cover_path)
        os.makedirs(dir_path, exist_ok=True)
        image = Image.open(io.BytesIO(cover))
        image = image.convert('RGB')
        image = image.resize(resolution)
        image.save(cover_path)
    except KeyboardInterrupt as e:
        print(f"Saving {cover_path}...")
        raise e
    finally:
        dir_path = os.path.dirname(cover_path)
        os.makedirs(dir_path, exist_ok=True)
        image = Image.open(io.BytesIO(cover))
        image = image.convert('RGB')
        image = image.resize(resolution)
        image.save(cover_path)


def get_user_input(prompt, original_value):
    """
    Asks the user for input when a value cannot be formatted.

    Args:
        prompt (str): The prompt to display to the user.
        original_value (str): The original value that could not be formatted.

    Returns:
        str: The user's input, which must be a valid formatted string.

    Notes:
        The function will continue to prompt the user until a valid formatted string is entered.
    """
    while True:
        user_input = input(f"Unable to format {prompt} \"{original_value}\". Enter {prompt} to use: ")
        if get_formatted_string(user_input, ""):
            return user_input
        print(f"Still unable to format {prompt}. Please try again.")
        
        
def create_file_if_not_exists(file_path: str) -> str:
    """
    Creates a file at the specified path if it does not already exist.
    Also creates all directories in the file path if they do not exist.

    Args:
        file_path (str): The path to the file to be created.

    Returns:
        str: The file path, whether the file was created or already existed.
    """
    if os.path.dirname(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
    if not os.path.exists(file_path):
        with open(file_path, "w"):
            pass
    return file_path


def make_api_request(s: Session, url: str) -> Response:
    """
    Makes a GET request to the specified URL using the provided Session object.

    The function will retry the request up to 5 times with exponential backoff if it encounters a 503 status code.
    If all retries fail, it will raise an exception.

    Args:
        s (Session): The Session object to use for the request.
        url (str): The URL to make the request to.

    Returns:
        Response: The response object from the successful request.

    Raises:
        Exception: If all retries fail.
    """
    retries = 0
    max_retries = 5
    backoff_factor = 1
    while retries < max_retries:
        try:
            response = s.get(url)
            response.raise_for_status()
            return response
        except HTTPError as e:
            if e.response.status_code == 503:
                retries += 1
                backoff_factor *= 2
                time.sleep(backoff_factor)
            else:
                raise
    raise Exception(f"Failed to make API request after {max_retries} retries")


def format_date(date: str) -> datetime:
    """
    Attempts to parse a date string into a datetime object.

    The function will try to parse the date string using the following formats:
    - %Y-%m-%d
    - %Y-%m
    - %Y

    If the date string cannot be parsed, it will raise a ValueError.

    Args:
        date (str): The date string to parse.

    Returns:
        datetime: The parsed datetime object.

    Raises:
        ValueError: If the date string cannot be parsed.
    """
    date_formats = ["%Y-%m-%d", "%Y-%m", "%Y"]
    dt = None
    for date_format in date_formats:
        try:
            dt = datetime.strptime(date, date_format)
            break
        except ValueError:
            pass
    else:
        raise ValueError("Date must be in one of the following formats: {}".format(", ".join(date_formats)))
    
    if dt.day == 0:
        dt = dt.replace(day=1)
    if dt.month == 0:
        dt = dt.replace(month=1)
    return dt