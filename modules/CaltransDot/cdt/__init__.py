from requests import get
from bs4 import BeautifulSoup as s
from json import dump

def getCams(file=False):
    """
    Returns all data from streamlist and optionally updates static data file.
    """

    r = get("https://cwwp2.dot.ca.gov/vm/streamlist.htm")

    soup = s(r.text, 'lxml')

    tables = soup.find_all("table")

    data = []

    for tr in tables[0].find_all("tr"):

        buf = {}
        i = 0

        for td in tr.find_all("td"):

            if (i == 0):
                buf['highway'] = td.text
                
            elif (i == 1):
                buf['county']  = td.text

            elif (i == 2):
                buf['city']    = td.text
            
            elif (i == 3):
                a = td.find_all("a")

                if len(a):
                    buf['cam']     = {"id": td.text, "poster": a[0].get("href")}

                else:
                    continue

            i += 1
        
        data.append(buf)

    final = []

    for item in data:
        if "cam" in item:
            final.append(item)
    
    if file:
        with open("data.json", "w+") as f:
            dump(final, f, indent=4, sort_keys=True)

    return final

def getCamFromPoster(poster):
    """
    Uses poster url from main object to get latest image url for that cam.
    """
    r = get(poster)
    return r.text.split("posterURL=\"")[1].split("\"")[0]

def getImage(url, filename):
    """
    Gets image from url.
    """
    r = get(url)
    if r.ok:
        with open(filename, "wb+") as f:
            f.write(r.content)
        return filename
    return None



    
