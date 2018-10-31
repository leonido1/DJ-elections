def findTheWinner(songs):

    winnerNunVotes = 0
    winingSong = None

    for song in songs:

        if song.votes > winnerNunVotes:
            winingSong = song
            winnerNunVotes = song.votes

    return winingSong