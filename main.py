import os
import sys
from PIL import Image
from requests import Session
from dotenv import load_dotenv
from supabase import create_client
from sentence_transformers import SentenceTransformer
from utils.utils import load_lines, save_cover
from managers.csv_manager import CSVManager
from managers.offset_manager import OffsetManager
from musicbrainz.musicbrainz_api import MusicBrainzAPI
from musicbrainz.extended_release_group import ExtendedReleaseGroup


ARTISTS_FILE_PATH = "data/artists.txt"
CSV_FILE_PATH = "data/db.csv"
COVER_ART_DIR_PATH = "data/covers"

MODEL_NAME = "clip-ViT-B-32"

GENRE_LIST = ["rock", "pop", "r&b", "hip hop"]


def main() -> None:
    try:
        load_dotenv()
        SUPABASE_URL = os.environ.get("SUPABASE_URL")
        SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
        SUPABASE_TABLE = os.environ.get("SUPABASE_TABLE")
        SUPABASE_BUCKET = os.environ.get("SUPABASE_BUCKET")
        
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        model = SentenceTransformer(MODEL_NAME)
        cm = CSVManager(CSV_FILE_PATH)
        om = OffsetManager()
        artists = load_lines(ARTISTS_FILE_PATH)
        
        for i in range(om.offset,len(artists)):
            print(f"{i+1}/{len(artists)} Processing artist: {artists[i]}")
            
            mb = MusicBrainzAPI(Session())
            
            artist_id = mb.fetch_artist_id(artists[i])
            release_groups_ids = mb.fetch_release_groups_ids(artist_id)
            
            for release_group_id in release_groups_ids:
                release_group = ExtendedReleaseGroup(mb.fetch_release_group(release_group_id))
                if not release_group.is_album() or not release_group.is_solo() or not release_group.is_released("2023-12-31"):
                    continue
                
                release_genre = release_group.get_genre(GENRE_LIST)
                if not release_genre:
                    continue
                if release_genre == "hip hop":
                    release_genre = "hip-hop"
                release_data = release_group.get_data(release_genre)
                
                cover_path = release_group.get_cover_path(COVER_ART_DIR_PATH)
                cover = mb.fetch_cover(release_group_id)
                save_cover(cover_path, cover)
                
                db_cover_path = "/".join(cover_path.split("/")[-2:])
                cover_in_storage = supabase.rpc("file_exists", {"bucket_id": SUPABASE_BUCKET, "file_path": db_cover_path}).execute().data
                if not cover_in_storage:
                    with open(cover_path, 'rb') as f:
                        supabase.storage.from_(SUPABASE_BUCKET).upload(file=f,path=db_cover_path,file_options={"content-type":"image/jpeg"})
                release_data["src"] = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(db_cover_path)[:-1]
                
                cover_emb = model.encode(Image.open(cover_path))
                cover_emb = "[" + ','.join(map(str, cover_emb)) + "]"
                release_data["embedding"] = cover_emb
                
                table_col_names = supabase.rpc("get_column_names", {"tablename": SUPABASE_TABLE}).execute().data
                for key in release_data.keys():
                    if key not in table_col_names:
                        raise ValueError(f"Column \"{key}\" does not exist in \"{SUPABASE_TABLE}\" table")
                
                row_in_table = supabase.from_(SUPABASE_TABLE).select("src").eq("src", release_data["src"]).execute().data
                if not row_in_table:
                    supabase.from_(SUPABASE_TABLE).insert(release_data).execute()
                
                if not cm.csv_data_exists(release_data):
                    cm.save(release_data)
                
                print(f'Ending proccessing {release_data["artist"]} - {release_data["title"]}')
            
            om.offset += 1
            om.save_to_file()
      
        om.delete_file()
        print("Done!")
    except KeyboardInterrupt:
        print("Exiting early...")
        sys.exit(0)


if __name__ == "__main__":
    main()