import pickle

# tracks = pickle.load(open("data/track_small.pkl", "rb"))
# artists = pickle.load(open("data/artist_small.pkl", "rb"))
tracks = pickle.load(open("data/track_full2.pkl", "rb"))
artists = pickle.load(open("data/artist_full2.pkl", "rb"))

it = 0
for key in tracks.keys():
    tracks_str = ""
    track_name = tracks[key]["name"].replace("\\", "/").replace("\"", "\\\"")
    album_name = tracks[key]["album"].replace("\\", "/").replace("\"", "\\\"")
    tracks_str += "track(\"" + key + "\", \"" + track_name + "\", ["
    artist_ok = False 
    for artist in tracks[key]["artists"]:
        if artist in artists:
            tracks_str += "\"" + artists[artist]["name"].replace("\\", "/").replace("\"", "\\\"") + "\", "
            artist_ok = True

    if not artist_ok:
        print(key, ",", tracks[key]["artists"])
        continue

    tracks_str = tracks_str[:-2] + "], "
    tracks_str += "\"" + album_name + "\", ["
    tracks_str += str(int(tracks[key]["explicit"])) + ", "
    full = False
    if "danceability" in tracks[key].keys():
        full = True
        tracks_str += str(tracks[key]["danceability"]).replace("None", "-1") + ", "
        tracks_str += str(tracks[key]["energy"]).replace("None", "-1") + ", "
        tracks_str += str(tracks[key]["key"]).replace("None", "-1") + ", "
        tracks_str += str(tracks[key]["loudness"]).replace("None", "-1") + ", "
        tracks_str += str(tracks[key]["mode"]).replace("None", "-1") + ", "
        tracks_str += str(tracks[key]["speechiness"]).replace("None", "-1") + ", "
        tracks_str += str(tracks[key]["acousticness"]).replace("None", "-1") + ", "
        tracks_str += str(tracks[key]["instrumentalness"]).replace("None", "-1") + ", "
        tracks_str += str(tracks[key]["liveness"]).replace("None", "-1") + ", "
        tracks_str += str(tracks[key]["valence"]).replace("None", "-1") + ", "
        tracks_str += str(tracks[key]["tempo"]).replace("None", "-1") + ", "
        tracks_str += str(tracks[key]["duration_ms"]).replace("None", "-1") + ", "
        tracks_str += str(tracks[key]["time_signature"]).replace("None", "-1")
    tracks_str += "])."
    if full:
        print(tracks_str, file=open("data/track_full_predicates.pl", "a"))
    else:
        print(tracks_str, file=open("data/track_full_predicates-2.pl", "a"))
    it += 1
    if it % 10000 == 0:
        print("%d/%d" % (it, len(tracks)))
