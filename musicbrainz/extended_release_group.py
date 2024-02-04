from musicbrainz.release_group import ReleaseGroup
from utils.utils import get_formatted_string, get_user_input

class ExtendedReleaseGroup(ReleaseGroup):
    """
    An extension of the ReleaseGroup class with added functionality.
    
    Attributes:
        release_group (ReleaseGroup): The original release group object.
        
    Methods:
        get_genre: Finds the genre with max count that contains any string from the given genre list.
        get_data: Extracts relevant data from a music release and returns it as a dictionary.
        get_cover_path: Returns the formatted path for a release's cover art.
    """
    def __init__(self, release_group: ReleaseGroup):
        """
        Initializes an ExtendedReleaseGroup object with the given release group data.
        
        Args:
            release_group (ReleaseGroup): The release group object to extend.
        """
        super().__init__(release_group._release_data)
    
    def get_genre(self, genre_list: list[str]) -> str:
        """
        Finds the genre with max count that contains any string from the given genre list.

        Args:
            rg (ReleaseGroup): The release group object to extract data from.
            genre_list (list[str]): The list of genres to search for.

        Returns:
            str: The genre with max count that contains any string from the given genre list.
        """
        max_count = 0
        max_count_genre = ""
        for genre in self.get_genres():
            for string in genre_list:
                if string.lower() in str(genre["name"]).lower():
                    if genre["count"] > max_count:
                        max_count = genre["count"]
                        max_count_genre = string
        return max_count_genre

    def get_data(self, genre: str) -> dict:
        """
        Extracts relevant data from a music release and returns it as a dictionary.

        Args:
            release (Release): The music release object to extract data from.
            genre (str): The genre of the music release.

        Returns:
            dict: A dictionary containing the extracted data, with the following keys:
                - "artist": The name of the artist.
                - "title": The title of the release.
                - "year": The year of the first release date (in YYYY format).
                - "genre": The genre of the music release.
        """
        r = {}
        r["artist"] = self.get_artist_name()
        r["title"] = self.get_title()
        r["year"] = self.get_first_release_date()[:4]
        r["genre"] = genre
        return r

    def get_cover_path(self, dir_path: str) -> str:
        """
        Returns the formatted path for a release's cover art.

        Args:
            release (ReleaseGroup): The release group containing the artist and title information.
            dir_path (str): The directory path where the cover art should be saved.

        Returns:
            str: The formatted path for the release's cover art.

        Notes:
            If the artist or title cannot be formatted, the function will prompt the user for input.
        """
        artist = self.get_artist_name()
        artist_alt = self.get_artist_name_disambiguation()
        title = self.get_title()
        title_alt = self.get_title_disambiguation()
        
        formatted_artist = get_formatted_string(artist, artist_alt)
        if not formatted_artist:
            formatted_artist = get_user_input("artist's name", artist)

        formatted_title = get_formatted_string(title, title_alt)
        if not formatted_title:
            formatted_title = get_user_input("release title", title)

        if dir_path[-1] == "/":
            dir_path = dir_path[:-1]

        cover_path = f"{dir_path}/{formatted_artist}/{formatted_title}.jpg"
        return cover_path