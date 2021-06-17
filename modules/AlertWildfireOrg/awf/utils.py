from awf.awf_globals import AWF_GLOBALS, Essentials

from math import sin, cos, sqrt, asin, radians
from datetime import datetime
from requests import get
from uuid import uuid1
from time import time
from json import dump

def saveJson(dict, name="result.json", mode="w+"):
    with open(name, mode) as f:
        dump(dict, f, indent=4)

# Gets distance in km of Lat/Lon #1 
def haversineFormula(ll1, ll2):
    # convert decimal degrees to radians 
    lat1, long1, lat2, long2 = map(radians, [ll1[0], ll1[1], ll2[0], ll2[1]])
    # haversine formula 
    dlon = long2 - long1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    # Radius of earth in kilometers is 6371
    km = 6371 * c
    return km

# TODO:
# https://pythonprogramming.net/haar-cascade-object-detection-python-opencv-tutorial/
# https://docs.opencv.org/3.4/dc/d88/tutorial_traincascade.html

def nonce():
    return str(uuid1()).replace("-", "")

# GET CAMS JSON
def getCams():
    url = Essentials.base_url + "/all_cameras-v2.json"
    r = get(url, headers=Essentials.headers)
    if r.ok:
        return r.json()
    return None

# GET LATEST IMAGE (IN BYTES) FROM SPECIFIC CAM BY UNIX TIMESTAMP
def getCam(camId, filename=None, timestamp=None):
    if timestamp is None:
        timestamp = str(int(time() * 1e3))
    url = Essentials.base_url + "/" + camId + "/latest_full.jpg?x-request-time=" + timestamp
    r = get(url, headers=Essentials.headers)
    if r.ok:
        if filename is None:
            filename = camId + ".jpg"
        with open(filename, "wb+") as f:
            f.write(r.content)
        return filename
    return None

### TEST NETWORKING ###
def requestTest():
    
    cams = getCams()

    start = datetime.now()
    for feature in cams['features']:
        if feature['properties']['county'].lower() == 'butte':
            props    = feature['properties']
            filename = "test/" + props['id'] + ".jpg"
            t = datetime.now()
            getCam(props['id'], filename=filename)
            seconds = datetime.now() - t
            
            print("[%sms] %s" % (seconds.microseconds / 1000, props['id']) )

    print("Completed in %s seconds!" % ( str((datetime.now() - start).total_seconds()) ))