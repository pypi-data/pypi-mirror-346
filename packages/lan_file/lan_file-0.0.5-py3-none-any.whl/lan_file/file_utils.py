"""
file utils
"""

import os
import time


def is_file_exist(filename: str, directory: str) -> bool:
    """
    judge file whether exist
    :param filename: file will be uploaded
    :param directory: path to save files
    :return: bool
    """
    exist_files: list = os.listdir(directory)
    if filename in exist_files:
        return True
    return False


def rename_file(filename: str) -> str:
    """
    if file exist, add timestamp
    :param filename: file will be uploaded
    :return: new filename with timestamp
    """
    timestamp: int = int(time.time())
    dot: str = "."
    if dot in filename:
        prefix, suffix = filename.rsplit(dot, maxsplit=1)
        new_filename: str = f"{prefix}{timestamp}{dot}{suffix}"
        return new_filename

    return f"{filename}{timestamp}"


def get_files_sorted_by_time(directory: str) -> list:
    """
    sort files by time
    :param directory: path to save files
    :return: sorted files by time
    """
    file_time: list = []
    for file in os.listdir(directory):
        file_path: str = os.path.join(directory, file)
        if os.path.isfile(file_path):
            create_time: float = os.path.getmtime(file_path)
            file_time.append([file, create_time])

    if not file_time:
        return []

    file_modify_time_sorted_list: list = sorted(
        file_time, key=lambda x: x[1], reverse=True
    )
    file_sorted_list: list = [i[0] for i in file_modify_time_sorted_list]
    return file_sorted_list
