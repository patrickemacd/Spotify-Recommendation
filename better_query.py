
import base64
import requests
import datetime
from urllib.parse import urlencode

client_id = "351e3f22d6504e4da8a5b81badf7642d"
client_secret = "INSERT YOUR CLIENT SECRET"



# the client that will obtain all of the song information for recommendations 

#creating a Spotify object for the API access
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
    def get_more(self, lookup_id, resource_type = None, topic = None, version = "v1"):
        base_url = "https://api.spotify.com"
        endpoint = f"{base_url}/{version}/{resource_type}/{lookup_id}/{topic}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers = headers)
        if r.status_code not in range(200,299):
            return {}
        return r.json()
    

    #have to work on formatting the json that is output so we only get all the tracks and album name 
    # in an ordered dictionary
    def get_album(self, _id):
        return self.get_resource(_id,resource_type = 'albums')
    
    def get_artist(self, _id):
        return self.get_resource(_id,resource_type = 'artists')
    
    def get_related_artists(self,_id):
        return self.get_more(_id,resource_type = 'artists', topic = 'related-artists')
    
    def get_tracks(self, _id):
        return self.get_resource(_id,resource_type = 'tracks')
    
    def get_features(self,_id):
        return self.get_resource(_id,resource_type = 'audio-features')

    def get_tracks(self,_id):
        return self.get_more(_id,resource_type = 'albums', topic = 'tracks')


    def base_search(self, query_params):
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        url = f"{endpoint}?{query_params}"
        r = requests.get(url, headers = headers)
        
        if r.status_code not in range(200,299):
            return {}
        return r.json()
    
    #create an operator that discludes any lists of artists within the specific playlist
    

    def search(self, query=None, operator=None, operator_query=None, search_type = None):
        if query == None:
            raise Exception("A search must be done")

        if isinstance(query, dict):
            query = " ".join([f"{k}:{v}" for k,v in query.items()]) #creating a list from a dictionary)
        query_params = urlencode({"q": query, "type": search_type.lower()})
        if operator != None and operator_query != None:
            if operator.lower() == "or" or operator.lower() == 'not':
                operator = operator.upper
                if isinstance(operator_query, str):
                    query = f"{query} {operator} {operator_query}"

       
        return self.base_search(query_params)

  # have to create a function that gathers all of the ids to use from the initial search
    # some sort of flip on the search or base search


# q = the specific query where search_type = what it is(artist, track, album, etc.)
#input are you looking for an album, artists or track?
# if artist input(what artist are you looking for)
# if track etc etc

# input(What song, album, artist are you looking for?)
# inputs that into the search type

#connecting to spotify client
spotify = SpotifyAPI(client_id,client_secret)


#search ids and artist id
search = spotify.search(query = "Local Natives", search_type = "album")
#print(search)



# the name of album 
album_name = search['albums']['items'][0]['name']

#gathering the total tracks from albums

 for i in range():
    print(search['albums']['items'][i]['name'])
   total_tracks =  search['albums']['items'][i]['total_tracks']



# search['albums']['items'][0]['total_tracks']

# # find the year of the album release date
# album_year = search['albums']['items'][0]['release_date']

# # gather album id 
album_id = search['albums']['items'][0]['id']

# album_1 = spotify.get_album(str(album_id))

print(spotify.get_tracks(str(album_id)))

# #getting the track name, duration as well
# album_track1 = album_1['tracks']['items'][0]['name']


# # for loop time!

# # for i in len(album_1['tracks']['items']):
# #     print([i]['name'])





######## the actual seraching part 

# finding genre from an artist
# def genre_find(x):
#     search = spotify.search(query = x, search_type = "artist")
#     list_search = search['artists']['items'][0]['genres']
#     return list_search




