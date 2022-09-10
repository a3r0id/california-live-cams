# california-live-cams
 A collection of modules to programmatically search for/download imagery from all publicly available live cam feeds across the state of California. In no way am I affiliated with any of these organizations and these modules/methods of gathering imagery are completely unofficial.
 
 Initially, I wanted to create a fire-detection engine using Haar-Cascade classifiers but due to each image containing a logo, the project requires further problem-solving. I hope these modules help someone else in the meantime!

## Alertwildfire.org
This is a very robust module as it contains search features and a querying system that returns results in a JSON object.
Aside from California, AWF also has cams in Oregon, Washington, Idaho, Nevada & Utah.

Note: Each image consistently contains a black footer that contains data. Tesseract-OCR engine flawlessly detects the text in the black bar each time which might be very useful to someone.

[Source: alertwildfire.org](http://www.alertwildfire.org/)

### Usage: 
```python

from awf import *
from PIL import Image

if __name__ == '__main__':

    # Initialize an API-session
    api = AWF()

    # This will keep images after the script has stopped if set to False.
    AWF_GLOBALS.BURN_AFTER_READING = True

    # Note: Downloads are saved to the location "__main__/downloads" by default.

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

```

## Preview:

![](https://raw.githubusercontent.com/hostinfodev/california-live-cams/main/modules/AlertWildfireOrg/preview.png)


------------------------------------------------
------------------------------------------------

## Caltrans & DOT
This is a collection of ALL of the Department Of Transportation's highway cams located in the state of California, in cooperation with Caltrans.
While there is also live-video feeds selectively available, I have not added a streaming capability to the module yet but plan to in the near future.
I did not add a search/query feature to this module as my main focus is around Wildfire detection. 

[Source: cwwp2.dot.ca.gov](https://cwwp2.dot.ca.gov)

```python

from cdt import *
from PIL import Image
from os import remove

# Iterate over entire set of cams
while True:
    
    # Get current cams from Caltrans/DOT
    # This will create a file, data.json
    cams = getCams(file=True)

    # Iterate cam results
    for cam in cams:

        # Print the cam info
        print()
        print("City:    %s" % cam['city'])   
        print("County:  %s" % cam['county'])     
        print("Highway: %s" % cam['county'])    
        print("Cam ID:  %s" % cam['cam']['id'])   
        print()

        # Get the latest feed image url
        imageLocation = getCamFromPoster(cam['cam']['poster'])

        # Download the image
        filename = getImage(imageLocation, "test.jpg")

        # Show the image
        im = Image.open(filename)
        im.show()

        _ = input("Hit [enter] to continue...")

        remove(filename)

```

## Preview:

![](https://raw.githubusercontent.com/hostinfodev/california-live-cams/main/modules/CaltransDot/preview.png)



------------------------------------------------
------------------------------------------------


## Notes

- I plan to merge both modules into one centralized module with universal search features.

- Again, in no way am I affiliated with the above organizations.

- Rate-limiting has not been an issue with either organization but this doesn't mean we can make a rediculous amount of requests... please be respectful!

- I'm am open to accepting contribution to these modules and future iterations, just DM me on [Twitter](https://twitter.com/hostinfodev).

- Enjoy!!
