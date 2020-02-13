import gpx_parser as parser
import boto3
import datetime

def ParseGPX(path):
    with open(path, "r") as gpx_file:
        gpx = parser.parse(gpx_file)

    return gpx

def GetDistance(parsedGPX):

    distance = parsedGPX.length_2d()

    return distance

def GetTime(parsedGPX):

    for track in parsedGPX:
        time = track.get_duration()
    
    return time
    
def RecordValidation(distance, time):

    speed = distance/time

    if speed > 1.94 and speed < 5.56:
        valChk = True
        return valChk
    else:
        valChk = False
        return valChk

def AddRecord(username, distance):

    client = boto3.client('dynamodb')
    timestmp = str(datetime.datetime.now())
    print(timestmp)
    intDist = str(distance)
    addRecord = client.put_item(TableName='SpringRunningChallenge', Item={'Timestamp':{'S': timestmp},'SlackName-index':{'S': username },'DistStr-index':{'S': intDist }})




def Main():
    path = "/Users/Kacper/Documents/Repos/RunningCoach/20191203_165608.gpx"
    usrNm = "Kacper"

    gpx = ParseGPX(path)

    dist = GetDistance(gpx)
    time = GetTime(gpx)

    if RecordValidation(dist, time) == True:
        AddRecord(usrNm, dist)
        print("Record added")
    else:
        print("Validation failed")


Main()

    