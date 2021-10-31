import requests
import six
import base64

def _make_authorization_headers(client_id, client_secret):
    auth_header = base64.b64encode(
        six.text_type(client_id + ":" + client_secret).encode("ascii")
    )
    return "Basic %s" % auth_header.decode("ascii")

def get_token(client_id, client_secret):
    Tokenurl = 'https://accounts.spotify.com/api/token'
    my_headers = {'Authorization': _make_authorization_headers(client_id, client_secret)}
    payload = {"grant_type": "client_credentials"}

    response = requests.post(
        Tokenurl,
        data=payload,
        headers=my_headers,
        verify=True
    )

    token = response.json()['access_token']
    return (token, {'Authorization': 'Bearer ' + token})



