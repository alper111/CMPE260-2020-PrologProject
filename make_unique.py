import pickle

artists = pickle.load(open("data/artist_full.pkl", "rb"))
albums = pickle.load(open("data/album_full.pkl", "rb"))
tracks = pickle.load(open("data/track_full.pkl", "rb"))

artist_names = []
banned_artist_ids = []
banned_album_ids = []
banned_track_ids = []

for artist_id in artists:
    if artists[artist_id]["name"] not in artist_names:
        artist_names.append(artists[artist_id]["name"])
    else:
        print(artists[artist_id]["name"])
        banned_artist_ids.append(artist_id)
        for album_id in artists[artist_id]["albums"]:
            banned_album_ids.append(album_id)
            for track_id in albums[album_id]["tracks"]:
                banned_track_ids.append(track_id)

print("banned artists: %d, albums: %d, tracks: %d" % (len(banned_artist_ids), len(banned_album_ids), len(banned_track_ids)))

for id in banned_artist_ids:
    del artists[id]

for id in banned_album_ids:
    del albums[id]

for id in banned_track_ids:
    del tracks[id]

file = open("data/artist_full_rev.pkl", "wb")
pickle.dump(artists, file)
file.close()

file = open("data/album_full_rev.pkl", "wb")
pickle.dump(albums, file)
file.close()

file = open("data/track_full_rev.pkl", "wb")
pickle.dump(tracks, file)
file.close()
