# Sonata Data Ingestor

## Overview

The Sonata Data Ingestor retrieves release data from the [MusicBrainz API](https://musicbrainz.org/doc/MusicBrainz_API) for a list of artists, processes the data and saves it to a [Supabase](https://supabase.com) database and on disk.

> [!NOTE]
> This tool is a part of the Sonata project so it retrieves only the data necessary for that project.

## Sonata project

| Repository | Description |
|---|---|
| [Sonata](https://github.com/aivarovsky/sonata-app) | Web application that allows you to search for music releases by describing their cover. |
| [Sonata API](https://github.com/aivarovsky/sonata-api) | API for generating embeddings of user queries for the Sonata project. |
| Sonata Data Ingestor | Data ingestor for the Sonata project. |

## Prerequisites

- A Supabase account and a project set up (or comment out the Supabase-related code in `main.py`).

## Modules

| Module | Description |
|---|---|
| [main.py](https://github.com/aivarovsky/sonata-data-ingestor/blob/main/main.py) | Main script that runs the data ingestor. |
| [musicbrainz/musicbrainz_api.py](https://github.com/aivarovsky/sonata-data-ingestor/blob/main/musicbrainz/musicbrainz_api.py) | `MusicBrainzAPI` class for interacting with the MusicBrainz API. |
| [musicbrainz/release_group.py](https://github.com/aivarovsky/sonata-data-ingestor/blob/main/musicbrainz/release_group.py) | `ReleaseGroup` class for interacting with data returned by the `MusicBrainzAPI` class. |
| [musicbrainz/extended_release_group.py](https://github.com/aivarovsky/sonata-data-ingestor/blob/main/musicbrainz/extended_release_group.py) | `ExtendedReleaseGroup` class that extends the `ReleaseGroup` class with additional methods. |
| [managers/csv_manager.py](https://github.com/aivarovsky/sonata-data-ingestor/blob/main/managers/csv_manager.py) | `CSVManager` class for managing the CSV file. |
| [managers/offset_manager.py](https://github.com/aivarovsky/sonata-data-ingestor/blob/main/managers/offset_manager.py) | `OffsetManager` class for managing the offset of processed artists. |
| [utils/utils.py](https://github.com/aivarovsky/sonata-data-ingestor/blob/main/utils/utils.py) | Utility functions for all the modules above. |

## Setup

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/aivarovsky/sonata-data-ingestor
    ```

2. Navigate to the project directory:

    ```bash
    cd sonata-data-ingestor
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file with these environment variables:

    ```bash
    SUPABASE_URL = "YOUR SUPABASE PROJECT URL"
    SUPABASE_KEY = "YOUR SUPABASE PROJECT API KEY"
    SUPABASE_TABLE = "YOUR SUPABASE TABLE NAME"
    SUPABASE_BUCKET = "YOUR SUPABASE BUCKET NAME"
    ```

5. Set up constants in `main.py`:

    ```python
    ARTISTS_FILE_PATH = "data/artists.txt"
    CSV_FILE_PATH = "data/db.csv"
    COVER_ART_DIR_PATH = "data/covers"

    MODEL_NAME = "clip-ViT-B-32"

    GENRE_LIST = ["rock", "pop", "r&b", "hip hop"] # For filtering release group genres
    ```

6. Run `main.py`:

    ```bash
    python main.py
    ```

## License

This project is licensed under the [**MIT License**](https://github.com/aivarovsky/sonata-data-ingestor/blob/main/LICENSE).
