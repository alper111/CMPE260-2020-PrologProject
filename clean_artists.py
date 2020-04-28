import pickle

revised = pickle.load(open("albums_rev.pkl", "rb"))
artists = pickle.load(open("artists.pkl", "rb"))

artists_rev = {}
album_keys = revised.keys()

for artist_id in artists.keys():
    albums = artists[artist_id]["albums"]
    new_albums = []
    for album_id in albums:
        if album_id in album_keys:
            new_albums.append(album_id)
    artists_rev[artist_id] = artists[artist_id]
    artists_rev[artist_id]["albums"] = new_albums

file = open("artists_rev.pkl", "wb")
pickle.dump(artists_rev, file)
file.close()
