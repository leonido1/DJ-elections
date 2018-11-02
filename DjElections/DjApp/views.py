from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.db import transaction
from .models import *
from datetime import datetime,timezone,timedelta
from .utils import *

# Create your views here.
def login(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render({},request))


def logInConformation(request):

    dj = authenticate(username=request.POST["DJ"], password=request.POST['password'])
    template1 = loader.get_template("DjPage.html")

    if dj is not None:

        songs = Song.objects.filter(dj = dj.id).order_by('name')
        request.session['DJ_ID'] = dj.id

        return HttpResponse(template1.render({"Songs": songs, }, request))
    else:
        return HttpResponse("No such DJ ")


def backToDJPage(request):

    template1 = loader.get_template("DjPage.html")
    songs = Song.objects.filter(dj=request.session['DJ_ID'] ).order_by('name')

    return HttpResponse(template1.render({"Songs": songs, }, request))


def addSong (request):

    song = Song(artist=request.POST["artist"], name= request.POST["song"])
    dj = DJ.objects.filter(id = request.session['DJ_ID'] )

    song.save()
    song.dj.set(dj)
    song.save()

    return backToDJPage(request)


def mainAction(request):

    if "Election" in request.POST :


        dj = DJ.objects.filter(id = request.session['DJ_ID'] ).first()
        stopTime = datetime.now() + timedelta(minutes = 1)

        songs = Song.objects.filter (id__in=request.POST.getlist('my-select[]'))
        election = Elections(dj=dj, startTime=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                             , endTime=stopTime.strftime("%Y-%m-%d %H:%M:%S"))
        election.save()

        for song in songs:
            SongsInElections(elections = election, song = song , votes = 0).save()

        template1 = loader.get_template("DjWaiting.html")
        return HttpResponse(template1.render({"time": election.endTime, }, request))


    if "Delete" in request.POST:
        print("Implement Delete")

    if "Log-out" in request.POST:
        print("Implement Log-out")


    return HttpResponse()

def checkUpDate (request,djName=""):

    present = datetime.now(timezone.utc)+timedelta(hours=2)
    dj = DJ.objects.filter(username=djName).first()
    elections = Elections.objects.filter(dj=dj).order_by('-endTime').first()

    if not elections:
        JsonResponse({'value': 'no'})

    if present < elections.endTime:
            return JsonResponse({'value': 'yes' , 'id': elections.id})

    return JsonResponse({'value':'no'})


def userPage(request,djName=""):

    dj = DJ.objects.filter(username = djName)

    if not dj:
        return HttpResponse ("no dj")

    template1 = loader.get_template("UserWaiting.html")


    return HttpResponse(template1.render({"DjName":djName }, request))

def electionInAction(request , elections_id =""):

    elections = Elections.objects.filter(id = elections_id).first()
    songsInElect = SongsInElections.objects.filter (elections=elections)
    songs = []

    template1 = loader.get_template("UserPage.html")
    request.session["Elections"] = elections_id

    for song in songsInElect:
        songs.append(song.song)

    return HttpResponse(template1.render({"songs":songs ,"time":str(elections.endTime)[:-6] }, request))



def vote(request):
    election_id = request.session['Elections']
    elections = Elections.objects.filter(id = election_id).first()
    song = Song.objects.filter(id = request.POST["song"]).first()
    songInElection = SongsInElections.objects.filter(elections=elections,song=song).first()

    with transaction.atomic():
        songInElection.vote()
        songInElection.save()

    return HttpResponse("Thank you for you'r vote")


def finishElectionDj(request):

    dj_id = request.session['DJ_ID']
    dj = DJ.objects.filter(id = dj_id).first()
    lastElections = Elections.objects.filter(dj=dj).order_by('-startTime').first()
    songs = SongsInElections.objects.filter(elections = lastElections)

    wininigSong = findTheWinner(songs)
    song = Song.objects.filter(id = wininigSong.song.id).first()

    return HttpResponse("the wining song is "+ song.name)



