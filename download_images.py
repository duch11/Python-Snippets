import concurrent.futures
from distutils.log import error
from importlib.resources import contents
import requests
from bs4 import BeautifulSoup

url_with_page = "https://www.uahirise.org/catalog/captions/index.php?page="

resolution = "1440"
path = "images/"
image_url = "https://static.uahirise.org/images/wallpaper/"+resolution+"/"

def download_image(image_url, file_name):
    print("download: " +image_url +" -> "+ file_name)
    image_data = requests.get(image_url)
    open(path+file_name, 'wb').write(image_data.content)

#imgs = [{"url":"URL","filename":"FILE"}]
imgs = []
#print(imgs[0]["url"])
#print(imgs[0]["filename"])

for i in range(108):
    print(i+1)
    res = requests.get(url_with_page+str(i+1))

    html = BeautifulSoup(res.content, "html.parser")
    image_cells = html.find_all("td", class_="catalog-cell-images")

    for cell in image_cells:
        a = cell.find("a", contents="")
        image_name = a.get('href').split("/")[2]
        image_file_name = image_name + ".jpg"
        full_img_url = image_url + image_file_name
        #print(full_img_url)
        imgs.append({"url" : full_img_url, "filename" : image_file_name})
        print("Found"+image_file_name)


with concurrent.futures.ThreadPoolExecutor() as executor:
    for img in imgs:
        #print(type(img))
        print(img)
        hello = executor.submit(download_image, str(img["url"]), str(img["filename"]))


