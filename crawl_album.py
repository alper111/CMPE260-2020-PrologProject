import pickle
import utils
import settings


token = utils.get_token(settings.CLIENT_ID, settings.CLIENT_SECRET)
artists = pickle.load(open("artists.pkl", "rb"))
discovered_albums = {}

buffer = []
it = 0
N = len(artists)
for artist_id in artists.keys():
    it += 1
    if len(artists[artist_id]["albums"]) > 0:
        for album_id in artists[artist_id]["albums"]:
            if len(buffer) < 19:
                buffer.append(album_id)
            else:
                buffer.append(album_id)
                album_info = utils.get_album_info(buffer, token)
                for k, info in zip(buffer, album_info):
                    discovered_albums[k] = info
                buffer = []
        print("Albums: %d" % len(discovered_albums))

if len(buffer) > 0:
    album_info = utils.get_album_info(buffer, token)
    for k, info in zip(buffer, album_info):
        discovered_albums[k] = info

print("Albums: %d" % len(discovered_albums))

file = open("albums.pkl", "wb")
pickle.dump(discovered_albums, file)
file.close()
