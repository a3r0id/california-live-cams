from threading import Lock

# AMF GLOBALS
class AWF_GLOBALS:

    # SESSIONS
    sessions = {}
    
    # THREAD-LOCK TO ENSURE WE ARENT CORRUPTING OUR CAMS OBJECT WITH OUR PARALLEL, UPDATER THREAD.
    # ONLY SINGULAR INTERACTION IS ALLOWED HERE DUE TO CAMS OBJECT PREVIOUSLY CUT IN HALF. 
    LOCK = Lock()

    # SET TO FALSE TO KEEP AFTER SCRIPT EXIT
    BURN_AFTER_READING = True

    # Cams object
    cams = {}

    # Kills the spinning updater thread if set to True.
    exit_thread = False

    # Amount in seconds between grabbing the latest config file from awf server.
    update_frequency_seconds = 5

    # Updater Thread
    updater_thread = None

    # Redundancy as logging is not setup yet.
    logger = None

# THE ESSENTIALS
class Essentials:
    
    # BASE URL
    base_url = "http://s3-us-west-2.amazonaws.com/alertwildfire-data-public"

    # HEADERS
    headers = {
        "Referer": "http://www.alertwildfire.org/",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Mobile Safari/537.36"
    }