from awf.awf_globals import AWF_GLOBALS
from awf.utils import nonce, getCams, haversineFormula, getCam

from time import time
import logging
class AWF(object):
    
    # Constructor
    def __init__(self):   
        self.session_id                               = nonce()
        AWF_GLOBALS.sessions[self.session_id]         = {"download_cache": [], "alive": True}

    # Gets current downloads manifest
    def downloads(self):
        return AWF_GLOBALS.sessions[self.session_id]['download_cache']

    # Gets a download object from downloads manifest by download ID.
    def fromDownloads(self, id):
        session = self.get_session()
        for download in session['download_cache']:
            if id == download['id']:
                return download
        return None

    # Gets the session object from manifest
    def getSession(self):
        return AWF_GLOBALS.sessions[self.session_id]
    
    # Searches manifest for cams by ID. Not really useful unless you know exaclty what cam you are looking for.
    # Appends to downloads by default if found.
    def fetchByID(self, id, **kwargs):
        return self.fetchByProp("id", id, kwargs)

    ### NOTE: ###    
    # ALL SEARCHES ARE AGAINST EACH CAM'S "properties" OBJECT.
    # Try iterating over your global "cams" objects then using "print(cam['properties'])" for each cam to give yourself some clarification of whats under the hood. 

    # Fetch by property key/value. Accepts {"key" => string, int or list}
    # download: If True, downloads each found cam's latest image and appends the download info to the downloads object.
    # timestamp: (datetime object) Overrides the current datetime and attempts to search for older imagery. 
    # distance: (Kilometers, int) If searching by "field off view" (example: "fov_center" => ['-122.492152', '39.181985']),
    # you can set an acceptable range so if distance is set to 20km, all results within 20km of ['-122.492152', '39.181985'] will be returned.
    def fetchByProp(self, key, value, download=False, timestamp=None, distance=None):
        
        if not AWF_GLOBALS.cams:
            AWF_GLOBALS.LOCK.acquire()
            AWF_GLOBALS.cams = getCams()
            AWF_GLOBALS.LOCK.release()

        query = []

        for cam in AWF_GLOBALS.cams['features']:

            match = False

            if key.lower() == "fov_rt":
                difference = haversineFormula(cam['properties']['fov_rt'], value)
                if difference <= distance:
                    match = True

            elif key.lower() == "fov_center":
                difference = haversineFormula(cam['properties']['fov_center'], value)
                if difference <= distance:
                    match = True

            elif cam['properties'][key.lower()].lower() == value.lower():
                    match = True

            else:
                continue

            if match:

                if download:
    
                        download_id = nonce()
                        filename = "downloads/" + download_id + ".jpg"

                        if timestamp is None:
                            timestamp = str(int(time() * 1e3))

                        AWF_GLOBALS.LOCK.acquire()
                        if not getCam(cam['properties']['id'], filename=filename):
                            logging.error("HTTP ERROR: Failed to get image.")
                            continue

                        dl_receipt = {
                            "timestamp": timestamp,
                            "filename": filename,
                            "time": str(time()),
                            "id": download_id,
                            "cam": cam
                        }

                        AWF_GLOBALS.sessions[self.session_id]['download_cache'].append(dl_receipt)
                        AWF_GLOBALS.LOCK.release()

                        cam['download'] = dl_receipt
                
                query.append(cam)

        return query
