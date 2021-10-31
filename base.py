import credentials
import oAuth
import SpotifyClient as sc
client_id = credentials.client_id
client_secret = credentials.client_secret

authorization = oAuth.get_token(client_id,client_secret)

explore = sc.SpotifyClient(authorization[0])

print(explore.search('album', 'zeppelin II'))



