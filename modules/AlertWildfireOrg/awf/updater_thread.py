
from threading import Thread
from awf.awf_globals import AWF_GLOBALS
from awf.utils import getCams

from datetime import datetime

import logging


def updateCams():
    t_start = datetime.now()
    while True:

        if (AWF_GLOBALS.exit_thread):
            break

        if (datetime.now() - t_start).total_seconds() > AWF_GLOBALS.update_frequency_seconds:
            AWF_GLOBALS.LOCK.acquire()
            AWF_GLOBALS.cams=getCams()
            AWF_GLOBALS.LOCK.release()
            t_start = datetime.now()

            logging.debug("[UPDATE THREAD]: Updated cams")
            
    logging.debug("[UPDATE THREAD]: Thread closed")
            
def start_updater_thread():
    logging.debug("[UPDATE THREAD]: Thread started")
    AWF_GLOBALS.updater_thread = Thread(target=updateCams)
    AWF_GLOBALS.updater_thread.start()
    #AWF_GLOBALS.updater_thread.join()

