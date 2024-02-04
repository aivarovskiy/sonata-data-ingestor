import os
import csv
from utils.utils import create_file_if_not_exists

def _validate_csv_file_path(file_path: str) -> None:
    if not file_path:
        raise ValueError(f"File path \"{file_path}\" cannot be empty")
    if not file_path.lower().endswith(".csv"):
        raise ValueError(f"File path \"{file_path}\" must have a .csv extension")


def _validate_csv_data(csv_data: dict) -> None:
    if not csv_data or any(not key or not value for key, value in csv_data.items()):
        raise ValueError(f"Every element of the csv_data must not be empty")
        

def _load_existing_fieldnames(file_path: str) -> list[str]:
    with open(file_path, "r", newline="") as f:
        reader = csv.reader(f)
        return next(reader, None)


def _write_fieldnames(file_path: str, fieldnames: list[str]) -> None:
    with open(file_path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()


def _compare_fieldnames(fieldnames1: list[str], fieldnames2: list[str]) -> None:
    if set(fieldnames1) != set(fieldnames2):
        raise ValueError(f"Existing fieldnames in the csv file are different from the ones in the csv_data list")


def _write_csv_data(file_path: str, csv_data: dict, fieldnames: list[str]) -> None:
    with open(file_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(csv_data)


class CSVManager:
    def __init__(self, file_path: str):
        _validate_csv_file_path(file_path)
        self._file_path = create_file_if_not_exists(file_path)

    def save(self, csv_data: dict) -> None:
        _validate_csv_data(csv_data)
        fieldnames = list(csv_data.keys())
        existing_fieldnames = _load_existing_fieldnames(self._file_path)     
        original_file_length = os.path.getsize(self._file_path)
        try:
            if not existing_fieldnames:
                _write_fieldnames(self._file_path, fieldnames)
            else:
                _compare_fieldnames(existing_fieldnames, fieldnames)
            _write_csv_data(self._file_path, csv_data, fieldnames)
        except KeyboardInterrupt as e:
            with open(self._file_path, 'r+') as f:
                f.truncate(original_file_length)
            print(f"Saving csv_data to {self._file_path} has been cancelled.")
            raise e
        
    def csv_data_exists(self, csv_data: dict) -> bool:
        fieldnames = list(csv_data.keys())
        cells = list(csv_data.values())
        existing_fieldnames = _load_existing_fieldnames(self._file_path)
        if not existing_fieldnames:
            return False
        _compare_fieldnames(existing_fieldnames, fieldnames)
        with open(self._file_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            next(reader, None)
            for row in reader:
                if all(row[fieldname] == cell for fieldname, cell in zip(fieldnames, cells)):
                    return True
        return False