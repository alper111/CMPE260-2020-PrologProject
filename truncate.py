import pickle
import numpy as np

artists = pickle.load(open("data/artist_full.pkl", "rb"))
albums = pickle.load(open("data/album_full.pkl", "rb"))
tracks = pickle.load(open("data/track_full.pkl", "rb"))

np.random.seed(1)
# R = np.random.permutation(len(artists))
# artist_keys = np.array(list(artists.keys()))[R[:1000]]

artists_truncated = {}
albums_truncated = {}
tracks_truncated = {}

for artist_id in artists.keys():
    print(artists[artist_id]["name"])
    artist = artists[artist_id]
    if len(artist["albums"]) == 0:
        continue
    # artist["albums"] = artist["albums"][:10]
    artists_truncated[artist_id] = artist

    for album_id in artist["albums"]:
        album = albums[album_id]
        # album["tracks"] = album["tracks"][:10]
        if artist_id not in album["artists"]:
            album["artists"].insert(0, artist_id)
        albums_truncated[album_id] = album

        for track_id in album["tracks"]:
            track = tracks[track_id]
            if artist_id not in track["artists"]:
                track["artists"].insert(0, artist_id)
            if "danceability" in track.keys():
                tracks_truncated[track_id] = track
            else:
                idx = albums_truncated[album_id]["tracks"].index(track_id)
                albums_truncated[album_id]["tracks"] = albums_truncated[album_id]["tracks"][:idx]\
                                                       + albums_truncated[album_id]["tracks"][idx+1:]

file = open("data/artist_full2.pkl", "wb")
pickle.dump(artists_truncated, file)
file.close()

file = open("data/album_full2.pkl", "wb")
pickle.dump(albums_truncated, file)
file.close()

file = open("data/track_full2.pkl", "wb")
pickle.dump(tracks_truncated, file)
file.close()
