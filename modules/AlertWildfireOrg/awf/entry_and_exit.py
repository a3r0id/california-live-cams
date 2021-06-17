from awf.awf_globals import AWF_GLOBALS
from awf.updater_thread import start_updater_thread

import atexit
from os.path import isdir
from os import mkdir, remove
import logging


# EXIT HANDLER
def exit_handler():

    AWF_GLOBALS.logger = logging.getLogger(__name__)
    AWF_GLOBALS.logger.setLevel(0)
    
    # CLEANUP DOWNLOADS
    if AWF_GLOBALS.BURN_AFTER_READING:
        for session in AWF_GLOBALS.sessions:
            for download in AWF_GLOBALS.sessions[session]['download_cache']:
                remove(download['filename'])
                
        print("[CLEANUP FINISHED]")
    
    # CLEANUP THREADS
    AWF_GLOBALS.exit_thread = True

# ENTRY (REQUIRED)
def entryAndExit():
    # ENSURE REQUIRED DIRECTORIES EXIST
    REQUIRED_DIRECTORIES = ["downloads"]
    for dir_ in REQUIRED_DIRECTORIES:
        if not isdir(dir_):
            mkdir(dir_)

    # REGISTER THE EXIT HANDLER
    atexit.register(exit_handler)

    # START THE UPDATER THREAD
    start_updater_thread()

    logging.debug("[SETUP]: Ready")


