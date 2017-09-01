##############################################################################
# Author: Seda Cavdaroglu                                                    #
# Date: 07/27/2017                                                           #
# This views.py file contains functions needed to read in singer/band name   #
# and phone number of the user and send an sms message the most popular songo#
# of the singer/band.                                                        #
##############################################################################

from django.shortcuts import render
import spotipy
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import spotipy.util as util
import json
from django.contrib import messages
from django.http import JsonResponse
from django.template import Context, Template

def search(request):
    #this function performs all the heavy work :
    # 1) read the singer & phone information user entered
    # 2) do the searching of most popular track in spotify API
    # 3) send an sms message with the song name
    
    #Authentication to be able to use spotify API
    CLIENT_ID="28d9eff5d0aa4471b7f4a9e8278c1043"
    CLIENT_SECRET="839540f0cdd74690b71beaa9bef9fb0b"
    token = util.oauth2.SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    cache_token = token.get_access_token()
    spotify = spotipy.Spotify(cache_token)
    

    #Authentication for sending sms messages through twilio
    from twilio.rest import Client
    account_sid = "ACbb8840b48cc93d4b05e987d82f7a281a"
    auth_token = "0f065f163e588424cf645b07e3dbc0cb"
    client = Client(account_sid, auth_token)
    
    
    if request.method == 'POST':
        #read in what user entered in text fields
        singer = str(request.POST['artistName'])
        phoneNo = str(request.POST['phoneNo'])
        
        #find the url of the singer the user searched
        results = spotify.search(q='artist:' + singer, type='artist')
        artist = results['artists']['items'][0]
        spotify_url= artist['uri']
        
        
        #find the most popular track for that artist
        top_track= spotify.artist_top_tracks(spotify_url)
        track_name = top_track['tracks'][0]['name'] #get the name of the 1st one in the list
        track_link = top_track['tracks'][0]['preview_url']
        
    #send message to the user 
    message = client.api.account.messages.create(to=phoneNo,
            	                                     from_="+18574454093",
                    	                             body=track_name)
   
    return render(request,'results.html',{"artistName" :singer,"track_url" :track_link,"track_name" :track_name})

def back(request):
	#this function takes the user from the results page to the main search page
	return render(request,'index.html',context=None)

# Create your views here.
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)


# Add this view
class ResultsPageView(TemplateView):
    template_name = "results.html"
