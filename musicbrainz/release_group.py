from datetime import datetime
from utils.utils import format_date

class ReleaseGroup:
    """
    Represents a release group, encapsulating its data and providing methods for accessing and manipulating it.

    Attributes:
        _release_data (dict): The underlying data for the release group.
        
    Methods:
    get_id: Retrieves the ID of the release group.
    get_artist_name: Retrieves the artist name of the release group.
    get_artist_name_disambiguation: Retrieves the disambiguation of the artist name of the release group.
    get_title: Retrieves the title of the release group.
    get_title_disambiguation: Retrieves the disambiguation of the title of the release group.
    get_genres: Retrieves the list of genres associated with the release group.
    is_album: Returns True if the release is an album, False otherwise.
    is_solo: Returns True if the release is a solo release, False otherwise.
    is_released(date): Returns True if the release has been released, False otherwise.
    """
    def __init__(self, release_data: dict):
        """
        Initializes a ReleaseGroup object with the given release data.

        Args:
            _release_data (dict): The data for the release group.
        """
        self._release_data = release_data

    def get_id(self) -> str:
        """
        Retrieves the ID of the release group.

        Returns:
            str: The ID of the release group.
        """
        return self._release_data["id"]

    def get_artist_name(self) -> str:
        """
        Retrieves the artist name of the release group.

        Returns:
            str: The artist name of the release group.
        """
        return self._release_data["artist-credit"][0]["name"]
    
    def get_artist_name_disambiguation(self) -> str:
        """
        Retrieves the disambiguation of the artist name of the release group.

        Returns:
            str: The disambiguation of the artist name of the release group.
        """
        return self._release_data["artist-credit"][0]["artist"]["disambiguation"]
    
    def get_title(self) -> str:
        """
        Retrieves the title of the release group.

        Returns:
            str: The title of the release group.
        """
        return self._release_data["title"]

    def get_title_disambiguation(self) -> str:
        """
        Retrieves the disambiguation of the title of the release group.

        Returns:
            str: The disambiguation of the title of the release group.
        """
        return self._release_data["disambiguation"]

    def get_first_release_date(self) -> str:
        """
        Retrieves the first release date of the release group in the "%Y-%m-%d" format.

        Returns:
            str: The first release date of the release group in the "%Y-%m-%d" format.
        """
        return self._release_data["first-release-date"]
    
    def get_genres(self) -> list[dict]:
        """
        Retrieves the list of genres associated with the release group.

        Returns:
            list[dict]: The list of genres.
        """
        return self._release_data["genres"]
    
    def is_album(self) -> bool:
        """
        Returns True if the release group is an album, False otherwise.

        Returns:
        bool: A boolean indicating whether the release group is an album.
        """
        return str(self._release_data["primary-type"]).lower() == "album" and not self._release_data["secondary-types"]

    def is_solo(self) -> bool:
        """
        Returns True if the release group is a solo release, False otherwise.

        Returns:
        bool: A boolean indicating whether the release group is a solo release.
        """
        return len(self._release_data["artist-credit"]) == 1
    
    def is_released(self, date: str = datetime.now().strftime("%Y-%m-%d")) -> bool:
        """
        Returns True if the release group has been released before the date, False otherwise.
        
        Args:
        date(str, optional): The date to check against in the "%Y-%m-%d" or "%Y-%m" or "%Y" format. Defaults to the current date.

        Returns:
        bool: A boolean indicating whether the release group has been released before the date.
        
        Raises:
        ValueError: If the date argument is not in the "%Y-%m-%d" or "%Y-%m" or "%Y" format.
        """
        dt_date = format_date(date)
        frd = self._release_data["first-release-date"]
        if not frd:
            return False
        dt_frd = format_date(frd)
        return dt_frd <= dt_date