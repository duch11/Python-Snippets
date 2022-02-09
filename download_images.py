import concurrent.futures
from distutils.log import error
from importlib.resources import contents
import requests
from bs4 import BeautifulSoup

url_with_page = "https://www.uahirise.org/catalog/captions/index.php?page="

resolution = "4500"
path = "images/"
image_url = "https://static.uahirise.org/images/wallpaper/"+resolution+"/"

def download_image(image_url, file_name):
    print("download: " +image_url +" -> "+ file_name)
    image_data = requests.get(image_url)
    open(path+file_name, 'wb').write(image_data.content)

def download_page(page_url):
    page_data = requests.get(page_url)
    return page_data




page_urls = []
pages = []
imgs = []
#imgs = [{"url":"URL","filename":"FILE"}]
#print(imgs[0]["url"])
#print(imgs[0]["filename"])

for i in range(108):
    url_with_page_and_no = url_with_page+str(i+1)
    print(url_with_page_and_no)
    page_urls.append(url_with_page_and_no)


with concurrent.futures.ThreadPoolExecutor() as executor:
    threads = []
    for page_url in page_urls:
        print(page_url)
        threads.append(executor.submit(download_page, page_url))
    for thread in concurrent.futures.as_completed(threads):
        res=thread.result()
        pages.append(res)
        print(res.text[ : 8])

for page in pages:
    html = BeautifulSoup(page.content, "html.parser")
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


