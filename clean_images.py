from os import listdir, remove
from PIL import Image

folder = "./images/"
filetype = ".jpg"
delete = True

for filename in listdir(folder):
    if filename.endswith(filetype):
        try:
            img = Image.open(folder+filename) # open the image file
            img.verify() # verify that it is, in fact an image
            print(folder+filename +" ok")
        except (IOError, SyntaxError) as e:
            print('Bad file:', folder+filename) # print out the names of corrupt files
            if delete:
                remove(folder+filename)