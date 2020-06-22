

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




# created a little input function so I can input whatever artists I want to look into
q_name = input("What artist are you looking for? \n Type the name here: ")
search = spotify.search(query = str(q_name), search_type = "album", limit_on = "5")

# just a little for loop to get information in more legible context

for i in range(0,5):
   album_name = search['albums']['items'][i]['name']
   total_tracks =  search['albums']['items'][i]['total_tracks']
   album_year = search['albums']['items'][i]['release_date']

   print(f"{album_name} : {total_tracks}, released {album_year}")

   