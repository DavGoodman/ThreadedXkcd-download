# ! python3
# downloadXkcd.py - Downloads every XKCD comic using multiple threads
import requests, os, bs4, threading

os.makedirs("xkcd", exist_ok=True)  # exist_ok=True prevents from throwing exception if folder already exists

def downloadXkcd(startComic, endComic):
    for url_number in range(startComic, endComic):
        print('Downloading page https://xkcd.com/%s...' % (url_number))
        res = requests.get('https://xkcd.com/%s' % (url_number))
        res.raise_for_status()

        soup = bs4.BeautifulSoup(res.text, 'html.parser')

        comic_elem = soup.select('#comic img')
        if comic_elem == []:
            print("could not find image")
        else:
            comic_url = comic_elem[0].get('src')
            print('Downloading image %s...' % (comic_url))
            res = requests.get('https:' + comic_url)
            res.raise_for_status()

            image_file = open(os.path.join('xkcd', os.path.basename(comic_url)), "wb")

            for chunk in res.iter_content(100000):
                image_file.write(chunk)
            image_file.close()

# Create and start the thread objects
download_threads = []
for i in range(0, 140, 10):
    start = i
    end = i + 9
    if start == 0:
        start = 1 # there is no comic 0 so set it to 1
    download_thread = threading.Thread(target=downloadXkcd, args=(start, end))
    download_threads.append(download_thread)
    download_thread.start()

# Wait for all threads to end before continuing main thread
for downloadThread in download_threads:
    downloadThread.join()
print('Done.')
