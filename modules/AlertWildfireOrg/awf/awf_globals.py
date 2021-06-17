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

    cams = {}

    exit_thread = False

    update_frequency_seconds = 5

    updater_thread = None

    logger = None

    class tesseract:
        # Tesseract OCR timeout
        # A timeout should be considered fatal, this shouldn't happen.
        timeout = 8

# THE ESSENTIALS
class Essentials:
    
    base_url = "http://s3-us-west-2.amazonaws.com/alertwildfire-data-public"

    # HEADERS
    headers = {
        "Referer": "http://www.alertwildfire.org/",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Mobile Safari/537.36"
    }