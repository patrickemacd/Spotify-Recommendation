import base64
import requests
import datetime
import client_credentials
import json
from time import sleep
from urllib.parse import urlencode

client_id = "351e3f22d6504e4da8a5b81badf7642d"
client_secret = client_credentials.client_secret


#creating Spotify object
class SpotifyAPI(object):
    access_token = None
    #run another request if access token expires
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    #spotifys specific token url
    token_url = "https://accounts.spotify.com/api/token"

  
    #initializing the client_id and client secret to obtain the token
    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def __repr__(self):
        print("gathering credentials")
        
    #receiving client credentials
    def get_client_credentials(self):
        """
        Returns a base64 encoded string
        """
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret == None or client_id == None:
            raise Exception("You must set client_id and client_secret")
        client_creds = f"{client_id}:{client_secret}"
        #encoding client id and secret(required by spotify)
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode() #make sure to decode the bit64 

    def get_token_headers(self):
        client_creds_b64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_creds_b64}"
        }
    
    def get_token_data(self):
        return {
            "grant_type": "client_credentials"
        } 
    
    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200, 299):
            raise Exception("Could not authenticate.")
            #return False
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in'] # seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True
    
    # gathering access token from the specific client and secret id
    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token()
        return token
    
    # getting headers for the API
    def get_resource_header(self):
        access_token = self.get_access_token()
        headers = {
            "Authorization" : f"Bearer {access_token}"
        }
        return headers
    

    #this is for the individual querys that don't necessarily build off of others
        # i.e artists,albums,tracks
    def get_resource(self, lookup_id, resource_type = None, version = "v1"): #version is still v1, idk if subject to change
        base_url = "https://api.spotify.com" #url to use
        endpoint = f"{base_url}/{version}/{resource_type}/{lookup_id}" #using f string to parse in the reuquired url
        headers = self.get_resource_header()#use the access token from the ids and the init fuction we ran before
        r = requests.get(endpoint, headers = headers)
        if r.status_code not in range(200,299):
            return {}
        return r.json()

    
    # searching for more than the bare bones information that just requires the ID
        #we can later just input build the recommendation based off of the parameters of related artists and features
    def get_more(self, lookup_id, resource_type = None, version = "v1", topic = None):
        base_url = "https://api.spotify.com"
        endpoint = f"{base_url}/{version}/{resource_type}/{lookup_id}/{topic}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers = headers)
        if r.status_code not in range(200,299):
            return {}
        return r.json()

    #getting recommendations from seeds, must add this feature for creating recommendations
    def get_recommendations(self, seed_tracks = None, seed_artists = None, seed_genres = None, limit = None, **kwargs):
        query_params = urlencode({"seed_artists": seed_artists, "seed_tracks": seed_tracks, "seed_genres": seed_genres, **kwargs, "limit": limit})
        base_url = "https://api.spotify.com/v1/recommendations"
        endpoint = f"{base_url}?{query_params}"
        print(endpoint)
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers = headers)
        
        if r.status_code not in range(200,299):
            return {}
        return r.json()


    #base search that the main search is built off of 
    def base_search(self, query_params):
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        url = f"{endpoint}?{query_params}"
        r = requests.get(url, headers = headers)
        if r.status_code not in range(200,299):
            return {}
        return r.json()

    #this just acts a very basic serach if you have the api url
    def url_search(self,_url):
        headers = self.get_resource_header()
        url = _url
        r = requests.get(url,headers = headers)
        if r.status_code not in range(200,299):
            return {}
        return r.json()
    
    #create an operator that discludes any lists of artists within the specific playlist
    

    #search query setting track as defauly becuase album create a lot of things
    def search(self, query=None, genre_type = None, operator=None, operator_query=None, search_type = None, limit = None):
        if query == None:
            raise Exception("A search must be done")
        #check to see if the query is a dictionary
        if isinstance(query, dict):
            query = " ".join([f"{k}:{v}" for k,v in query.items()]) #using list comprehension for query 
        query_params = urlencode({"q": query, "type": search_type, "limit": limit})
        #this section is if genre is selected then, songs would be included in the genre
        if isinstance(genre_type,str):
             query_params = urlencode({"q": f"{query} genre: {genre_type}", "type": search_type, "limit": limit})
        if operator != None and operator_query != None:
            if operator.lower() == "or" or operator.lower() == 'not':
                operator = operator.upper
                if isinstance(operator_query, str):
                    query = f"{query} {operator} {operator_query}"

        return self.base_search(query_params)


    """ALL OF THESE ARE METHODS for gathering information from the API, might add more, might not we'll see..."""

    #retrieve an album dependant on the ID
    def get_album(self, _id):
        return self.get_resource(_id,resource_type = 'albums')
    #retrieve an artist's information
    def get_artist(self, _id):
        return self.get_resource(_id,resource_type = 'artists')
    #retrieve related artists, input the OG artist's id
    def get_related_artists(self,_id):
        return self.get_more(_id,resource_type = 'artists', topic = 'related-artists')
    #gather tracks with the id
    def get_track(self, _id):
        return self.get_resource(_id,resource_type = 'tracks')
    #gather fetaures like danceability,tempo and everything according to spotify 
    def get_features(self,_id):
        return self.get_resource(_id,resource_type = 'audio-features')
    #gather the audio analysis, A LOT OF INFORMATION HERE! I will have to figure out how useful the songs are
    def get_analysis(self,_id):
        return self.get_resource(_id,resource_type = 'audio-analysis')
    #Get tracks from within an album
    def get_tracks(self,_id):
        return self.get_more(_id,resource_type = 'albums', topic = 'tracks')


    #retrieve playlist information from the user ID
    def get_user_playlists(self,_id):
        return self.get_more(_id,resource_type = 'users', topic = 'playlists')

    def get_playlist(self,_id):
        return self.get_more(_id, resource_type = 'playlists')

    #retrieve playlist contents from the playlist ID
    def get_playlist_items(self,_id):
        return self.get_more(_id,resource_type = 'playlists', topic = 'tracks')


#running the for spotify api
spotify = SpotifyAPI(client_id,client_secret)

#test output, for some reason the limit function is not working



#output = spotify.search(query = {"track":"blue"}, genre_type = "indie", search_type = "track")
#print(output)




