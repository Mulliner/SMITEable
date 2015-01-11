from urllib2 import Request, urlopen
import datetime
import hashlib

developerID = ''
authKey = ''
url = 'http://api.smitegame.com/smiteapi.svc/'

def askName():
    player = raw_input('Enter a name: ')
    getSessionID(time(), player)
    return player

def time():
    getTime = datetime.datetime.utcnow().strftime('%Y%m%d%I%M%S')
    return getTime

def getSessionID(getTime, player):
    url2 = url + 'createsessionJson/'
    session = 'createsession'
    try:
        signature = hashlib.md5(developerID + session + authKey + getTime)
        signatureHashed = signature.hexdigest()
        time()
        request = Request(url2+developerID + '/' + signatureHashed + '/' + getTime)
        response = urlopen(request)
        data = response.read()
        print data
        dataSplit = data.split('"')
        sessionID = dataSplit[7]
        getPlayerStats(sessionID, player, getTime)
    except:
        pass

def getPlayerStats(sessionID, player, getTime):
    time()
    try:
        session = 'getplayer'
        signature = hashlib.md5(developerID + session + authKey + getTime)
        signatureHashed = signature.hexdigest()
        getplayerURL = url + 'getplayerjson/' + developerID + '/' + signatureHashed + '/' + sessionID + '/' + getTime + '/' + \
                       player
        request = Request(getplayerURL)
        response = urlopen(request)
        data = response.read()
        dataSplit= data.split('"')
        name =  'Name: ' + dataSplit[85]
        masterylevel = 'Mastery Level: ' + dataSplit[82].replace(':', '').replace(',', '')
        wins =  'Wins: ' + dataSplit[102].replace(':', '').replace(',', '')
        losses =  'Losses: ' + dataSplit[80].replace(':', '').replace(',', '')
        leaves =  'Leaves: ' + dataSplit[76].replace(':', '').replace(',', '')
        level =  'Level: ' + dataSplit[78].replace(':', '').replace(',', '')
        lastlogin = 'Last Login: ' + dataSplit[9].replace(',', '').replace('/','').replace('\\', '/')
        creationdate = 'Account Creation Date: ' + dataSplit[3].replace(',', '').replace('/','').replace('\\', '/')
        joustrank = 'Joust Rank: ' + dataSplit[90].replace(':', '').replace(',', '')
        clanname = 'Clan Name: ' + dataSplit[95].replace(':', '').replace(',', '')
        print name
        print clanname
        print creationdate
        print joustrank
        print masterylevel
        print wins
        print losses
        print leaves
        print level
        print lastlogin
        getGodStats(sessionID, player, getTime)
    except:
        print 'Unable to find user!'
        askName()

def getGodStats(sessionID, player, getTime):
    time()
    session = 'getgodranks'
    signature = hashlib.md5(developerID + session + authKey + getTime)
    signatureHashed = signature.hexdigest()
    getplayerURL = url + 'getgodranksjson/' + developerID + '/' + signatureHashed + '/' + sessionID + '/' + getTime + '/' + player
    request = Request(getplayerURL)
    response = urlopen(request)
    data = response.read().replace('"', '').replace('{', '').replace(':', ' = ').replace("('",'').replace('[','')
    dataSplit= data.split(',')
    counter1 = 2
    counter2 = 1
    counter3 = 0
    for i in dataSplit:
        try:
            gods = dataSplit[counter1], dataSplit[counter2], dataSplit[counter3]
            counter1 += 6
            counter2 += 6
            counter3 += 6
            print gods
        except:
            break

    # getMatchHistory(sessionID)
    getFriends(sessionID, player, getTime)

# def getMatchHistory(sessionID):
#     session = 'getmatchhistory'
#     signature = hashlib.md5(developerID + session + authKey + time)
#     signatureHashed = signature.hexdigest()
#     getMatchURL = url + 'getmatchhistoryjson/' + developerID + '/' + signatureHashed + '/' + sessionID + '/' + time + '/' + player
#     request = Request(getMatchURL)
#     response = urlopen(request)
#     data = response.read()
#     dataSplit= data.split(',')
#     print data

def getFriends(sessionID, player,  getTime):
    time()
    session = 'getfriends'
    signature = hashlib.md5(developerID + session + authKey + getTime)
    signatureHashed = signature.hexdigest()
    getplayerURL = url + 'getfriendsjson/' + developerID + '/' + signatureHashed + '/' + sessionID + '/' + getTime + '/' + player
    request = Request(getplayerURL)
    response = urlopen(request)
    data = response.read().replace('{"name":"', '').replace('"', '').replace('ret_msg:null},', '').replace('[','').replace('}]', '').replace(']', '')
    dataSplit = data.split(',')
    friends =  dataSplit
    if 'ret_msg:null' in friends:
        friends.remove('ret_msg:null')
    for i in friends:
        print 'Friend: ' + i + '\n'.strip()

askName()
