import pickle

# artists = pickle.load(open("data/artist_small.pkl", "rb"))
artists = pickle.load(open("data/artist_full2.pkl", "rb"))
it = 0
for key in artists.keys():
    artist_str = ""
    artist_name = artists[key]["name"].replace("\\", "/").replace("\"", "\\\"")
    artist_str += "artist(\"" + artist_name + "\", ["

    if len(artists[key]["genres"]) > 0:
        for genre in artists[key]["genres"]:
            artist_str += "\"" + genre + "\", "
        artist_str = artist_str[:-2] + "], ["
    else:
        artist_str += "], ["

    if len(artists[key]["albums"]) > 0:
        for album in artists[key]["albums"]:
            artist_str += "\"" + album + "\", "
        artist_str = artist_str[:-2] + "])."
    else:
        print("girmemeli aslında")
        artist_str += "])."
    # artist_str += str(artists[key]["popularity"]) + ")."
    print(artist_str, file=open("data/artist_full_predicates.pl", "a"))
    it += 1
    if it % 100 == 0:
        print("%d/%d" % (it, len(artists)))
