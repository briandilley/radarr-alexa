
import requests
import os

RADAR_BASE_URL = os.environ.get('RADAR_BASE_URL')
RADAR_API_KEY = os.environ.get('RADAR_API_KEY')


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
           + ". ".join([r['movie']['title'] for r in records])


def add_movie_to_download(title):
    response = requests.get(RADAR_BASE_URL + "/api/movie/lookup", params={
        'apikey': RADAR_API_KEY,
        'term': title
    })
    if response.status_code != requests.codes.ok:
        return "There was a problem communicating with your Radar backend: " + response.text

    records = response.json()
    if len(records) == 0:
        return "Radar couldn't find the movie: " + title

    record = records[0]
    if not record.get('isAvailable', False):
        return "The movie " + record['title'] + " is not available"

    response = requests.get(RADAR_BASE_URL + "/api/movie", params={
        'apikey': RADAR_API_KEY,
        'pageSize': '-1'
    })

    existing = None
    for r in response.json():
        if r['titleSlug'] == record['titleSlug']:
            existing = r
            break

    if existing:
        return "You have already added the movie " + existing["title"]

    #requests.post(RADAR_BASE_URL + "/api/movie", params={
    #    'apikey': RADAR_API_KEY
    #    },
    #    json={
    #        'title': record['title'],
    #        'qualityProfileId': 6,
    #        'titleSlug': record['titleSlug'],
    #        'images': record['images'],
    #        'tmdbId': record['tmdbId'],
    #        'year': record['year'],
    #        'title': record['title']
    #    })

    #
    #return "The following " + str(len(records)) + " movies have downloaded recently: " \
    #       + ". ".join([r['movie']['title'] for r in records])

    return "The movie " + record['title'] + " was found, but this functionality isn't coded yet... bitch ass mofo"
