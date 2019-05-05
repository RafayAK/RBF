# import the necessary packages
from imutils import paths
import argparse
import requests
import cv2
import os

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-u", "--urls", required=True,
                help="Path to file containing image URLs")

ap.add_argument("-o", "--output", required=True,
                help="path to output directory of images")
args = vars(ap.parse_args())


# grab the list of URLs from the input file, then
# initialize the total number of images downloaded so far
rows = open(args["urls"]).read().strip().split("\n")
total = 0


# loop over the urls and attempt to download each image
for url in rows:
    try:
        # try to download the image
        r = requests.get(url, timeout=60) # timeout after 60ms if no response from url

        # save the image to disk
        p = os.path.sep.join([args["output"], "{}.jpg".format(str(total).zfill(8))])
        f = open(p, "wb")
        f.write(r.content)
        f.close()

        # update the counter
        print("[INFO] downloaded: {}".format(p))
        total+=1

    # handel if any exceptions are thrown during the download phase
    except:
        print("[INFO] error downloading {}...skipping".format(p))



# IMPORTANT STEP: loop through downloaded images try to open with OpenCv
#                 if can't open chuck'em out

for imagePath in paths.list_images(args["output"]):
    # initialize if the image should be deleted or not
    delete = False

    # try to load the images
    try:
        image = cv2.imread(imagePath)
        # if the image is 'None' then we could not properly load it
        # from the disk, so delete it
        if image is None:
            delete = True

    except:
        # if openCV could not load the image then the image is
        # likely to be corrupt so we should delete it
        print("Except")
        delete = True

    if delete:
        print('[INFO] deleting {}'.format(imagePath))
        os.remove(imagePath)


