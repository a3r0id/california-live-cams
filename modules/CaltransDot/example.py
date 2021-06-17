
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
