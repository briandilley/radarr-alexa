
import os

import requests

RADAR_BASE_URL = os.environ.get('RADAR_BASE_URL')
RADAR_API_KEY = os.environ.get('RADAR_API_KEY')
RADAR_ROOT_PATH = os.environ.get('RADAR_ROOT_PATH')


def get_history_response(count=5):
    response = requests.get(RADAR_BASE_URL + "/api/history", params={
        'apikey': RADAR_API_KEY,
        'sortKey': 'date',
        'sortDir': 'desc',
        'page': '1',
        'pageSize': str(count),
        'filterKey': 'eventType',
        'filterValue': '3',
        'filterType': 'equal'
    })
    if response.status_code != requests.codes.ok:
        return "There was a problem communicating with your Radar backend: " + response.text

    json = response.json()
    if 'records' not in json.keys():
        return "Your Radar backend isn't returning a valid response for the history endpoint"

    records = json['records']
    if len(records) == 0:
        return "There isn't anything in your Radar history"
    if len(records) > 5:
        records = records[:5]

    return "The following " + str(len(records)) + " movies have downloaded recently: " \
           + ". ".join([r['movie']['title'] + " from " + str(r['movie']['year']) for r in records])


def search_movie_for_download(title, year):
    response = requests.get(RADAR_BASE_URL + "/api/movie/lookup", params={
        'apikey': RADAR_API_KEY,
        'term': title
    })
    if response.status_code != requests.codes.ok:
        return (
            "There was a problem communicating with your Radar backend: " + response.text,
            None)

    records = response.json()
    if len(records) == 0:
        return (
            "Radar couldn't find the movie: " + title,
            None)

    record = None
    for r in records:
        if r.get('isAvailable', False) and (year is None or r.get('year', None) == year):
            record = r
            break

    if not record:
        return (
            "The movie " + title + " was not found"
            if year else "The movie " + title + " from " + str(year) + " was not found",
            None)

    return (
        "Radar found " + record["title"] + " from " + str(record["year"]) + ", is that what you are looking for?",
        record)


def add_movie_to_download(record):
    response = requests.post(RADAR_BASE_URL + "/api/movie", params={
            'apikey': RADAR_API_KEY
        },
        json={
             'title': record['title'],
             'qualityProfileId': 6,
             'titleSlug': record['titleSlug'],
             'images': record['images'],
             'tmdbId': record['tmdbId'],
             'year': record['year'],
             'monitored': True,
             'addOptions': {
                 'searchForMovie': True
             },
             'rootFolderPath': RADAR_ROOT_PATH
         })

    if response.status_code < 200 or response.status_code > 299:
        return "The movie " + record['title'] + " wasn't added, perhaps you already have it?"

    return "The movie " + record['title'] + " was found and added to Radar "
