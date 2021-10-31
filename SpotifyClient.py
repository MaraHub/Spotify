class SpotifyClient:
    """SpotifyClient performs operations using the Spotify API."""

    def __init__(self, token):
        """
        :param client_id (str): Spotify client_id
        :param client_secret (str): Spotify secret_id
        """
        self._token = token
        self._auth_headers = {'Authorization': 'Bearer ' + token}

    def get_albums_from_artist(self, artist_id):

        endpointURL = 'https://api.spotify.com/v1/artists/{id_}/albums'

        response = requests.get(url=endpointURL.format(id_=artist_id),
                                headers=self._auth_headers)
        # print(response)
        albums = []

        for item in response.json()['items']:
            albums.append(
                (item['name'], item['release_date'], item['total_tracks'], item['images'][0]['url'], item['uri']))
        albums_df = pd.DataFrame(albums, columns=['Name', 'Release_Date', 'Total_Tracks', 'Image_URL', 'URI'])

        return albums_df

    def get_related_artists(self, artist_id):

        endpointURL = "https://api.spotify.com/v1/artists/{id_}/related-artists"
        response = requests.get(url=endpointURL.format(id_=artist_id),
                                headers=self._auth_headers)
        return pd.DataFrame([(item['name'], item['id']) for item in response.json()['artists']],
                            columns=['ArtistName', 'ArtistID'])

    def get_tracks_from_album(self, album_id):

        endpointURL = 'https://api.spotify.com/v1/albums/{id_}/tracks'

        response = requests.get(url=endpointURL.format(id_=album_id),
                                headers=self._auth_headers)

        return pd.DataFrame([(item['name'], item['id']) for item in response.json()['items']],
                            columns=['Track', 'Track_ID'])

    def search(self, type_, name):

        endpointURL = "https://api.spotify.com/v1/search?query={name}&type={type_}&limit=50"

        prepare = name.replace(" ", "%20")

        searchURL = endpointURL.format(name=prepare, type_=type_)
        print(searchURL)
        response = requests.get(url=searchURL,
                                headers=self._auth_headers)

        try:

            if type_ == 'album':
                return (response.json()['albums']['items'][0]['name'],
                        response.json()['albums']['items'][0]['artists'][0]['name'],
                        response.json()['albums']['items'][0]['id'])
            elif type_ == 'artist':
                return (response.json()['artists']['items'][0]['name']
                        , response.json()['artists']['items'][0]['id'])
        except IndexError:
            return response.json()

    def get_track_popularity(self, track_id):

        endpointURL = 'https://api.spotify.com/v1/tracks/{id_}'
        response = requests.get(url=endpointURL.format(id_=track_id),
                                headers=self._auth_headers)

        # print(response)
        return response.json()['popularity']
