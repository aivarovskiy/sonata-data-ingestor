import os
from utils.utils import create_file_if_not_exists


def _load_offset(file_path: str) -> int:
    with open(file_path, "r") as f:
        offset = f.read().strip()
        if offset:
            return int(offset)
        return 0


class OffsetManager:
    def __init__(self, file_path: str = ".offset"):
        self._file_path = create_file_if_not_exists(file_path)
        self.offset = _load_offset(self._file_path)
        self.deleted = False
        
    def delete_file(self) -> None:
        if self.deleted:
            print(f"File {self._file_path} has already been deleted. Deletion aborted")
            return
        try:
            os.remove(self._file_path)
            self.deleted = True
        except KeyboardInterrupt as e:
            print(f"Deleting {self._file_path}...")
            raise e
        finally:
            if os.path.exists(self._file_path):
                os.remove(self._file_path)
            self.deleted = True


    def save_to_file(self) -> None:
        if self.deleted:
            print(f"File {self._file_path} has already been deleted. The offset is not saved")
            return
        try:
            with open(self._file_path, 'w') as f:
                f.write(str(self.offset))
        except KeyboardInterrupt as e:
            print(f"Saving offset value: {self.offset} to {self._file_path}...")
            raise e
        finally:
            with open(self._file_path, 'w') as f:
                f.write(str(self.offset))