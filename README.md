# CMPE260-2020-PrologProject
This repository contains scripts for transforming Spotify data to Prolog knowledge base for the CMPE260 course project (Principles of Programming Languages).

* `crawl_artists.py`:
For all genres (provided from Spotify), discover playlists. Save artists from discovered playlists to `artists.pkl`. After this step, there will be plenty of artists from different genres.
* `crawl_albums.py`:
For each saved artist in `artists.pkl`, save their album information to `albums.pkl`.
* `crawl_tracks.py`:
For each saved album in `albums.pkl`, save its tracks' information (and features) to `tracks.pkl`.
* `generate_artist_predicates.py`
Converts the information in `artists.pkl` to Prolog facts.
* `generate_album_predicates.py`
Converts the information in `albums.pkl` to Prolog facts.
* `generate_track_predicates.py`
Converts the information in `tracks.pkl` to Prolog facts.
* `utils.py`:
Wrapper functions for HTTPS calls.
* `clean_albums.py` and `clean_artists.py`
Remove duplicate albums (they contain different IDs but basically the same thing for our purpose) and their IDs from their respective artists.

Other scripts are used to filter out some problematic facts. If you want to reproduce the data, run the following:
1. `python crawl_artists.py`
2. `python crawl_albums.py`
3. `python crawl_tracsk.py`
4. `python generate_artist_predicates.py`
5. `python generate_album_predicates.py`
6. `python generate_track_predicates.py`
7. `python clean_albums.py`
8. `python clean_artists.py`

In order to make calls to Spotify API, you will need a token which can be obtained by registering an application to Spotify API. Look for the details [https://developer.spotify.com/documentation/web-api/](https://developer.spotify.com/documentation/web-api/)

You can truncate albums and tracks using `truncate.py` if you want your knowledge base to be small.
