import pickle

# albums = pickle.load(open("data/album_small.pkl", "rb"))
# artists = pickle.load(open("data/artist_small.pkl", "rb"))
albums = pickle.load(open("data/album_full2.pkl", "rb"))
artists = pickle.load(open("data/artist_full2.pkl", "rb"))

it = 0
for key in albums.keys():
    album_str = ""
    album_name = albums[key]["name"].replace("\\", "/").replace("\"", "\\\"")
    album_str += "album(\"" + key + "\", \"" + album_name + "\", ["

    artist_ok = False
    for artist in albums[key]["artists"]:
        if artist in artists:
            album_str += "\"" + artists[artist]["name"].replace("\\", "/").replace("\"", "\\\"") + "\", "
            artist_ok = True
    album_str = album_str[:-2] + "], ["
    if not artist_ok:
        print(key, ",", albums[key]["artists"])
        continue

    for track in albums[key]["tracks"]:
        album_str += "\"" + track + "\", "
    album_str = album_str[:-2] + "])."
    # print(album_str, file=open("data/album_small_predicates.pl", "a"))
    print(album_str, file=open("data/album_full_predicates.pl", "a"))
    it += 1
    if it % 1000 == 0:
        print("%d/%d" % (it, len(albums)))
