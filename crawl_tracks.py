import pickle
import utils
import settings
import time


token = utils.get_token(settings.CLIENT_ID, settings.CLIENT_SECRET)
albums = pickle.load(open("data/album_full.pkl", "rb"))
discovered_songs = {}

buffer = []
it = 0
start = time.time()
end = time.time()
for album_id in albums.keys():
    if end - start > 600:
        token = utils.get_token(settings.CLIENT_ID, settings.CLIENT_SECRET)
        start = end
        end = time.time()
    else:
        end = time.time()
    it += 1
    for track_id in albums[album_id]["tracks"]:
        if len(buffer) < 49:
            buffer.append(track_id)
        else:
            buffer.append(track_id)
            track_info = utils.get_track(buffer, token)
            if track_info is None:
                print("Track buffer none.")
                for k in buffer:
                    discovered_songs[k] = {}
            else:
                for k, info in zip(buffer, track_info):
                    discovered_songs[k] = info
            buffer = []
    print("Tracks: %d, %d/%d" % (len(discovered_songs), it, len(albums)))
    if it % 100 == 0:
        print("Cooldown...")
        time.sleep(9)

if len(buffer) > 0:
    track_info = utils.get_track(buffer, token)
    for k, info in zip(buffer, track_info):
        discovered_songs[k] = info

print("Tracks: %d" % len(discovered_songs))

file = open("data/tracks_explicit.pkl", "wb")
pickle.dump(discovered_songs, file)
file.close()
