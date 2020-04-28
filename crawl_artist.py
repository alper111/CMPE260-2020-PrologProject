import utils
import pickle
import settings

token = utils.get_token(settings.CLIENT_ID, settings.CLIENT_SECRET)
genres = utils.get_genres(token)
discovered_artists = {}

print("Discovering artists...")
for genre in genres:
    res = utils.get_recommendations(seed_tracks=[], seed_artists=[], seed_genres=[genre], token=token)
    for track in res["tracks"]:
        artists = track["artists"]
        for artist in artists:
            if artist["id"] not in discovered_artists.keys():
                discovered_artists[artist["id"]] = {}
    print("genre: %s, total artists: %d" % (genre, len(discovered_artists)))

print("Enough discovered. Now will get info about them.")
artists = {}
buffer = []
it = 0
for key in discovered_artists.keys():
    it += 1
    if len(buffer) < 49:
        buffer.append(key)
    else:
        buffer.append(key)
        artist_info = utils.get_artist_info(buffer, token)
        for i in range(50):
            artists[buffer[i]] = artist_info[i]
        buffer = []
        print("%d/%d" % (it, len(discovered_artists)))

if len(buffer) > 0:
    artist_info = utils.get_artist_info(buffer, token)
    for i in range(len(buffer)):
        artists[buffer[i]] = artist_info[i]
    print("%d/%d" % (it, len(discovered_artists)))

print("Learned all. Saving.")
file = open("artists.pkl", "wb")
pickle.dump(artists, file)
file.close()
