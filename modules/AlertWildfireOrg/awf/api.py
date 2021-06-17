from awf.awf_globals import AWF_GLOBALS
from awf.utils import nonce, getCams, haversineFormula, getCam

from time import time
import logging
class AWF(object):
    
    def __init__(self):   
        self.session_id                               = nonce()
        AWF_GLOBALS.sessions[self.session_id]         = {"download_cache": [], "alive": True}

    def downloads(self):
        return AWF_GLOBALS.sessions[self.session_id]['download_cache']

    def fromDownloads(self, id):
        session = self.get_session()
        for download in session['download_cache']:
            if id == download['id']:
                return download
        return None

    def getSession(self):
        return AWF_GLOBALS.sessions[self.session_id]

    def fetchByID(self, id, **kwargs):
        return self.fetchByProp("id", id, kwargs)
    
    def fetchByProp(self, key, value, download=False, timestamp=None, distance=None):
        
        """
        > download: Download image if match found.
        > timestamp: Sets image timestamp if download is enabled.
        > distance: For use only if search value is a lat/long array (possible keys: "").
        Sets search distance (km).
        """
        
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
