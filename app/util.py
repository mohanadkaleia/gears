"""
This module contains helper functions
"""

import random
import string
from pathlib import Path
from werkzeug.utils import secure_filename


def random_id(initial="i", size=8, chars=string.ascii_uppercase + string.digits):
    """
    Generate a random string with an initial to be used for ids

    Args:
        initial (str, optional): first letter of the generated id. Defaults to 'i'.
        size (int, optional): Defaults to 8.
        chars ([type], optional): characters set to be used in generating the id.
        Defaults to string.ascii_uppercase+string.digits.

    Returns:
        [str]: the generated id
    """
    return initial + "".join(random.choice(chars) for _ in range(size))


def upload_files(files, target_dir):
    uploaded_files = []
    for image in files:
        filename = secure_filename(image.filename)
        filepath = Path(target_dir) / Path(filename)
        image.save(filepath)
        uploaded_files.append(filename)
    return uploaded_files


def remove_files(files: list, target_dir):
    for filepath in files:
        filename = filepath.split("/").pop()
        file = Path(target_dir) / Path(filename)
        file.unlink()
