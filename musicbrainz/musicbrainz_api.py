from requests import Session
from utils.utils import make_api_request
from musicbrainz.release_group import ReleaseGroup


MUSICBRAINZ_API_URL = "https://musicbrainz.org/ws/2"
COVERARTARTCHIVE_API_URL = "https://coverartarchive.org"
    
    
class MusicBrainzAPI:
    """
    A class for interacting with the MusicBrainz API.

    Attributes:
    _session: A Session object used to make requests to the MusicBrainz API.

    Methods:
    fetch_artist_id(artist): Searches for an artist by name and fetches the ID of the first matching artist.
    fetch_release_groups_ids(artist_id): Fetches the release groups IDs of the artist by artist_id.
    fetch_release_group(release_group_id): Fetches the release group by release_group_id.
    fetch_release_group_cover(release_group_id): Fetches the cover art of the release group by release group ID.
    """
    def __init__(self, session: Session):
        """
        Initializes a MusicBrainzAPI object.

        Args:
        _session(Session): A Session object used to make requests to the MusicBrainz API.
        """
        self._session = session

    def fetch_artist_id(self, artist: str) -> str:
        """
        Searches for an artist by name and fetches the ID of the first matching artist.

        Args:
        artist (str): The name of the artist to search for.

        Returns:
        str: The ID of the first artist that matches the search query.
        """
        response = make_api_request(self._session, f"{MUSICBRAINZ_API_URL}/artist/?query={artist}&fmt=json")
        data = response.json()
        artist_id = data["artists"][0]["id"]
        return artist_id

    def fetch_release_groups_ids(self, artist_id: str) -> list[str]:
        """
        Fetches the release groups IDs of the artist by artist ID.

        Args:
        artist_id(str): The ID of the artist.

        Returns:
        list[str]: A list of release groups IDs of the artist.
        """
        response = make_api_request(self._session, f"{MUSICBRAINZ_API_URL}/artist/{artist_id}?inc=release-groups&fmt=json")
        data = response.json()
        release_groups_data = data["release-groups"]
        release_groups_ids = [release_group["id"] for release_group in release_groups_data]
        return release_groups_ids
    
    def fetch_release_group(self, release_group_id: str) -> ReleaseGroup:
        """
        Fetches the release group data by release group ID.

        Args:
        release_group_id(str): The ID of the release group.

        Returns:
        ReleaseGroup: A ReleaseGroup object representing the release group of the release group ID.
        """
        response = make_api_request(self._session, f"{MUSICBRAINZ_API_URL}/release-group/{release_group_id}?inc=artists+genres&fmt=json")
        data = response.json()
        release_group = ReleaseGroup(data)
        return release_group
    
    def fetch_cover(self, release_group_id: str) -> bytes:
        """
        Fetches the cover art of the release group by release group ID.

        Args:
        release_group_id(str): The ID of the release group.

        Returns:
        bytes: The content of the cover art of the release group in bytes.
        """
        response = make_api_request(self._session, f"{COVERARTARTCHIVE_API_URL}/release-group/{release_group_id}/front")
        cover = response.content
        return cover