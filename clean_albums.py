import pickle
import utils
import settings

token = utils.get_token(settings.CLIENT_ID, settings.CLIENT_SECRET)
albums = pickle.load(open("albums.pkl", "rb"))
albums_revised = {}
white_list = []
ban_list = []
for album_id in albums:
    tup = (albums[album_id]["artists"], albums[album_id]["name"])
    if tup not in white_list:
        white_list.append(tup)
        albums_revised[album_id] = albums[album_id]
    else:
        ban_list.append(album_id)

print(len(ban_list))
print(len(albums_revised))

file = open("albums_rev.pkl", "wb")
pickle.dump(albums_revised, file)
file.close()
