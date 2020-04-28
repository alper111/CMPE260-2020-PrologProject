import requests
import base64
import json
import time


def get_recommendations(seed_tracks, seed_artists, seed_genres, token):
    endpoint = "https://api.spotify.com/v1/recommendations"
    params = {
        "seed_tracks": seed_tracks,
        "seed_artists": seed_artists,
        "seed_genres": seed_genres
    }
    r = requests.get(endpoint, params=params, headers=get_headers(token))
    return json.loads(r.content)


def get_artist_info(artist_id, token):
    endpoint = "https://api.spotify.com/v1/artists"
    params = {"ids": ",".join(artist_id)}
    r = request("GET", endpoint, get_headers(token), params)
    artists = []
    for i in range(len(artist_id)):
        albums = get_album_ids(artist_id[i], token)
        res = {
            "name": r["artists"][i]["name"],
            "genres": r["artists"][i]["genres"],
            "popularity": r["artists"][i]["popularity"],
            "albums": albums
        }
        artists.append(res)
    return artists


def get_album_ids(artist_id, token):
    endpoint = "https://api.spotify.com/v1/artists/" + artist_id + "/albums"
    params = {"include_groups": "album"}
    r = requests.get(endpoint, params=params, headers=get_headers(token))
    r = json.loads(r.content)
    albums = r["items"]
    while r["next"]:
        r = requests.get(r["next"], headers=get_headers(token))
        r = json.loads(r.content)
        albums += r["items"]
    albums = [x["id"] for x in albums]
    return albums


def get_album_info(album_id, token):
    endpoint = "https://api.spotify.com/v1/albums"
    params = {"ids": ",".join(album_id)}
    r = request("GET", endpoint, get_headers(token), params)
    albums = []
    for album in r["albums"]:
        res = {
            "name": album["name"],
            "artists": [x["id"] for x in album["artists"]],
            "genres": album["genres"],
            "tracks": [x["id"] for x in album["tracks"]["items"]]
        }
        next_ptr = album["tracks"]["next"]
        while next_ptr:
            rr = request("GET", next_ptr, headers=get_headers(token))
            res["tracks"] += [x["id"] for x in rr["items"]]
            next_ptr = rr["next"]
        albums.append(res)
    return albums


def get_audio_features(track_id, token):
    endpoint = "https://api.spotify.com/v1/audio-features"
    params = {"ids": ",".join(track_id)}
    r = request("GET", endpoint, get_headers(token), params)
    if r is None:
        print(r)
        print("="*30)
        print(track_id)
        print("None in get_audio_features. Exiting")
        return None
    features = []
    for feature in r["audio_features"]:
        if feature is None:
            features.append({})
        else:
            features.append({
                "danceability": feature["danceability"],
                "energy": feature["energy"],
                "key": feature["key"],
                "loudness": feature["loudness"],
                "mode": feature["mode"],
                "speechiness": feature["speechiness"],
                "acousticness": feature["acousticness"],
                "instrumentalness": feature["instrumentalness"],
                "liveness": feature["liveness"],
                "valence": feature["valence"],
                "tempo": feature["tempo"],
                "duration_ms": feature["duration_ms"],
                "time_signature": feature["time_signature"]
            })
    return features


def get_track(track_id, token):
    endpoint = "https://api.spotify.com/v1/tracks"
    params = {"ids": ",".join(track_id)}

    r = request("GET", endpoint, get_headers(token), params)
    if r is None:
        print(r)
        print("="*30)
        print(track_id)
        print("None in get_track.")
        return None

    feats = get_audio_features(track_id, token)
    if feats is None:
        print(feats)
        print("="*30)
        print(track_id)
        print("None in feats.")
        return None

    tracks = []
    for track, feat in zip(r["tracks"], feats):
        tr_inf = {
            "name": track["name"],
            "artists": [x["id"] for x in track["artists"]],
            "album": track["album"]["name"],
            "explicit": track["explicit"]
        }
        for key in feat.keys():
            tr_inf[key] = feat[key]
        tracks.append(tr_inf)
    return tracks


def get_genres(token):
    endpoint = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
    r = requests.get(endpoint, headers=get_headers(token))
    return json.loads(r.content)["genres"]


def get_token(client_id, client_secret):
    client_id = client_id.encode("UTF-8")
    client_secret = client_secret.encode("UTF-8")
    endpoint = "https://accounts.spotify.com/api/token"
    auth = "Basic " + base64.b64encode(client_id + ":".encode("UTF-8")
                                       + client_secret).decode("UTF-8")
    data = {"grant_type": "client_credentials"}
    headers = {"Authorization": auth}
    r = requests.post(endpoint, data=data, headers=headers)
    return json.loads(r.content)["access_token"]


def print_track(track_id, token):
    features = get_audio_features(track_id, token)
    info = get_track(track_id, token)
    print("Song: %s" % info["name"])
    print("Artist: %s" % info["artists"][0]["name"])
    print("Album: %s" % info["album"]["name"])
    print("Popularity: %d" % info["popularity"])
    print("Explicit: %s" % info["explicit"])
    print("Danceability: %f" % features["danceability"])
    print("Energy: %f" % features["energy"])
    print("Key: %d" % features["key"])
    print("Loudness: %f" % features["loudness"])
    print("Mode: %d" % features["mode"])
    print("Speechiness: %f" % features["speechiness"])
    print("Acousticness: %f" % features["acousticness"])
    print("Instrumentalness: %f" % features["instrumentalness"])
    print("Liveness: %f" % features["liveness"])
    print("Valence: %f" % features["valence"])
    print("Tempo: %f" % features["tempo"])
    print("Duration: %d" % features["duration_ms"])
    print("Time signature: %d" % features["time_signature"])


def get_headers(token):
    auth = "Bearer " + token
    headers = {"Authorization": auth}
    return headers


def print_dic(dic):
    for key in dic.keys():
        print(key)
        print(dic[key])
        print("="*30)


def request(method_type, endpoint, headers, params=None, data=None):
    response = None
    if method_type == "GET":
        response = requests.get(endpoint, headers=headers, params=params)
    else:
        response = requests.post(endpoint, headers=headers, data=data)

    if response.status_code == 200:
        return json.loads(response.content)
    elif response.status_code == 429:
        print(response)
        time.sleep(60)
        return request(method_type, endpoint, headers, params, data)
    else:
        print(response)
