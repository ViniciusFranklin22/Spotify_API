from Spotify_Data import Spotify_Data
from requests import get
import json
from dotenv import load_dotenv
import os



obj1 = Spotify_Data()
teste = obj1.search_for_artist_by_name("The Beatles")

#for i, name in enumerate(x):
    #print(i,name["name"])
#print(obj1.get_songs_by_album('1xJHno7SmdVtZAtXbdbDZp'))
#for i,x in enumerate(obj1.get_songs_by_album('1xJHno7SmdVtZAtXbdbDZp')):
#    print(f'{i+1} song -> {obj1.get_song_by_id(x)} ')

print("Nova Aplicação Top Tracks")
for i,x in enumerate(obj1.get_artist_top_tracks(teste["id"])):
    print(f'{i+1} song -> {x["name"]}')

print(obj1.search_for_track_by_name("Something"))
print(obj1.search_for_album_by_name('Garage Inc.',limit=2))
print(obj1.search_for_playlist_by_name('Top 50')[0])
print(obj1.search_for_shows_by_id("1zABd2DqKPrytkVL6yjIax")['name'])
print(obj1.search_for_episodes_by_id('5UYexbZRVQuIWEafaF0RzV')['name'])
print(obj1.get_available_genre_seeds())
print("Recomendação")
print(obj1.get_recommendations_by_track_and_artist('2ye2Wgw4gimLv2eAKyk1NB','rock-n-roll','5sICkBXVmaCQk5aISGR3x1'))

print("Análise de Áudio")
print(obj1.get_audio_analysis('3GfOAdcoc3X5GPiiXmpBjK'))
