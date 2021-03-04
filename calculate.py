import sys
import json
import glob
import datetime


def getStopId(routeId, stopName, goBack):
    f = open("GetStop.json", "r", encoding="utf-8")
    data = json.load(f)
    busInfos = data["BusInfo"]
    matches = [busInfo for busInfo in busInfos if busInfo["nameZh"]
               == stopName and busInfo["routeId"] == routeId and busInfo["goBack"] == goBack]
    return matches[0]["Id"]


def getRouteId(routeName):
    f = open("GetRoute.json", "r", encoding="utf-8")
    data = json.load(f)
    busInfos = data["BusInfo"]
    matches = [busInfo for busInfo in busInfos if busInfo["nameZh"] == routeName]
    return matches[0]["Id"]


def getArriveTime(filenames, routeId, stopId, goBack):
    times = []
    for filename in filenames:
        f = open(filename, "r", encoding="utf-8")
        data = json.load(f)
        busInfos = data["BusInfo"]
        # TODO 過濾未發車:-1，交管不停靠:-2，末班車已過:-3，今日未營運:-4
        times.append([int(busInfo["EstimateTime"]) for busInfo in busInfos if busInfo["StopID"]
                      == stopId and busInfo["RouteID"] == routeId and busInfo["GoBack"] == goBack][0])
    mean = sum(times)/len(times)
    print('Average EstimateTime = {} seconds'.format(mean))
    start = datetime.datetime.now().replace(
        hour=8, minute=0, second=0, microsecond=0)
    calculateTime = start + datetime.timedelta(seconds=mean)
    return "%s:%s:%s" % (calculateTime.hour, calculateTime.minute, calculateTime.second)


if __name__ == "__main__":
    routeName = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else "1"
    stopName = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] else "捷運龍山寺站"
    goBack = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] else "1"
    routeId = getRouteId(routeName)
    print("routeId = {}".format(routeId))
    stopId = getStopId(routeId, stopName, goBack)
    print("stopId = {}".format(stopId))

    # root_dir = os.path.abspath(os.getcwd())

    filenames = [filename for filename in glob.iglob(
        '**', recursive=False) if filename.startswith("2021") and filename.endswith(".json")]
    arriveTime = getArriveTime(filenames, routeId, stopId, goBack)
    print('Average arrive Time = {}'.format(arriveTime))
