from awf import *
from PIL import Image

if __name__ == '__main__':

    # Initialize an API-session
    api = AWF()

    # This will keep images after the script has stopped if set to False.
    # Downloads are saved to the location "__main__/downloads" by default.
    AWF_GLOBALS.BURN_AFTER_READING = True

    # Get all cams where "county" == "napa", then download the latest image of each result to our cache.
    print("Starting query...")
    query = api.fetchByProp("county", "napa", download=True)

    # If any results from the query:
    if (len(query)):

        print("Found %s matching cams." % len(query))
        
        for cam in query:
            print("Cam ID:   %s" % cam['properties']['id'])
            print("Location: %s, %s" % (cam['properties']['county'], cam['properties']['state'],))
            Image.open(cam['download']['filename']).show()
            _ = input("Hit enter to continue...")

    # Finally, kill our updater thread as it will be hanging.
    AWF_GLOBALS.exit_thread = True
