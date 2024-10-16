import json
import os
import base64
from requests import post, get
from request_spotify import SpotifyRequest
from dotenv import load_dotenv


load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')


class Spotify_Data:

    def __init__(self):
        self.token = SpotifyRequest(client_id, client_secret).get_token()
        self.headers = self.get_auth_token()

    def get_auth_token(self):
        return {"Authorization": "Bearer " + self.token}

    def search_for_artist_by_name(self, artist_name):
        url = "https://api.spotify.com/v1/search"

        query = f'?q={self.spaces_to_plus(artist_name)}&type=artist&limit=1'
        query_url = url + query
        result = get(query_url, headers=self.headers)
        json_results = json.loads(result.content)["artists"]["items"]
        if len(json_results) == 0:
            print("No artist with this name was found...")
        return json_results[0]

    def search_for_artist_by_id(self, artist_id):
        url = f"https://api.spotify.com/v1/artists/{artist_id}"

        result = get(url, headers=self.headers)
        json_results = json.loads(result.content)
        return json_results

    def get_songs_by_artist(self, artist_id):
        url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=BR"

        result = get(url, headers=self.headers)
        json_results = json.loads(result.content)["tracks"]
        return json_results

    def get_album_per_artist(self, artist_id):
        # máximo de 20 álbums
        url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"

        result = get(url, headers=self.headers)
        json_results = json.loads(result.content)["items"]
        return json_results

    def get_market(self):
        url = f"https://api.spotify.com/v1/markets"

        result = get(url, headers=self.headers)
        json_result = json.loads(result.content)
        return json_result

    def get_songs_by_album(self, album_id):
        url = f"https://api.spotify.com/v1/albums/{album_id}/tracks?limit=50"

        result = get(url, headers=self.headers)
        json_results = json.loads(result.content)["items"]
        track_list = []
        for i in json_results:
            track_list.append(i["id"])
        return track_list

    def get_tracks_by_id(self, track):
        url = f"https://api.spotify.com/v1/tracks/{track}"

        result = get(url, headers=self.headers)
        json_result = json.loads(result.content)['name']
        return json_result

    def get_artist_top_tracks(self, artist_id):
        url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"

        result = get(url, headers=self.headers)
        json_results = json.loads(result.content)['tracks']
        return json_results

    def get_available_genre_seeds(self):
        url = f"https://api.spotify.com/v1/recommendations/available-genre-seeds"

        result = get(url, headers=self.headers)
        json_results = json.loads(result.content)
        return json_results

    def spaces_to_plus(self, word):
        string_list = word.split()
        string = ''
        for i in range(0, len(string_list) - 1):
            string = string_list[i] + "+"
        string = string + string_list[-1]
        return string

    def search_for_track_by_name(self, track_name, limit=10):
        # limit max = 50
        url = "https://api.spotify.com/v1/search"

        query = f'?q={self.spaces_to_plus(track_name)}&type=track&limit={limit}'
        print(query)
        query_url = url + query
        result = get(query_url, headers=self.headers)
        json_results = json.loads(result.content)["tracks"]["items"]
        if len(json_results) == 0:
            print("No tracks with this name was found...")
        return json_results

    def search_for_album_by_name(self, album_name, limit=10):
        url = "https://api.spotify.com/v1/search"

        query = f'?q={self.spaces_to_plus(album_name)}&type=album&limit={limit}'
        query_url = url + query
        result = get(query_url, headers=self.headers)
        json_results = json.loads(result.content)["albums"]["items"]
        if len(json_results) == 0:
            print("No albums with this name was found...")
        return json_results

    def search_for_playlist_by_name(self, playlist_name, limit=10):
        url = "https://api.spotify.com/v1/search"

        query = f'?q={self.spaces_to_plus(playlist_name)}&type=playlist&limit={limit}'
        query_url = url + query
        result = get(query_url, headers=self.headers)
        json_results = json.loads(result.content)["playlists"]["items"]
        if len(json_results) == 0:
            print("No playlists with this name was found...")
        return json_results

    def search_for_shows_by_id(self, show_id):
        # shows = podcast
        url = f"https://api.spotify.com/v1/shows/{show_id}"

        result = get(url, headers=self.headers)
        json_results = json.loads(result.content)
        return json_results

    def search_for_episodes_by_id(self, episode_id):
        # podcast episode
        # shows = podcast
        url = f"https://api.spotify.com/v1/episodes/{episode_id}"

        result = get(url, headers=self.headers)
        json_results = json.loads(result.content)
        return json_results

    def get_recommendations_by_track_and_artist(self, seed_artist_id, seed_genres, seed_track_id):
        # in the api docs theres a lot of other features to increase the accuracy
        url = f"https://api.spotify.com/v1/recommendations?seed_artists={seed_artist_id}&seed_genres={seed_genres}&seed_tracks={seed_track_id}"

        result = get(url, headers=self.headers)
        json_results = json.loads(result.content)
        return json_results

    def search_for_audiobooks_by_id(self, audio_books_id):
        url = f"https://api.spotify.com/v1/audiobooks/{audio_books_id}"
        result = get(url, headers=self.headers)
        json_results = json.loads(result.content)
        return json_results

    def get_audio_analysis(self,song_id):
        url = f"https://api.spotify.com/v1/audio-analysis/{song_id}"
        result = get(url, headers=self.headers)
        json_results = json.loads(result.content)
        return json_results




if __name__ == '__main__':
    Spotify_Data()