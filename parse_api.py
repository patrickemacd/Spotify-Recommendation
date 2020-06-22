

# this just acts as exploration list of what I will use later in a function or loops to get out the informaiton from the API

# this is to be updated as more ways to get information form API is discovered :)

#just using Local Natives as an example for query and album search
search = spotify.search(query = "Local Natives", search_type = "album")
#print(search)

# the name of the first album when searching through API
album_name = search['albums']['items'][0]['name']

# figure out how many tracks to put into range here...iterate over
# we can then loop to get track names for the albums
 for i in range():
   total_tracks =  search['albums']['items'][i]['total_tracks']


#find the album release date
album_year = search['albums']['items'][0]['release_date']

# # gather album id 
album_id = search['albums']['items'][0]['id']

# this was a predefined function within the Spotify object seen in updated better query
album_1 = spotify.get_album(str(album_id))

# getting the track name... can also get duration as well
album_track1 = album_1['tracks']['items'][0]['name']
