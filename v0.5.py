import re, praw, requests, os, glob, sys
from bs4 import BeautifulSoup
from imgurpython import ImgurClient
import albumDown
from time import sleep

def ShowProgress(counter, image_url, path):
    os.system('cls')
    print('downloading album: {}'.format(post.url))
    print('current image: {}, {}'.format(image_url, counter))
    equals = round((counter/downloader.num_images()*50)-2)
    none = 50 - equals
    print('¦8{}{}¦ {}%'.format(('='*equals+'>'), ' '*none, round(counter/downloader.num_images()*100)))
    sleep(0.1)
    
def GetImage(url, fileName, doujinshi):
    if doujinshi == True:
        pathText = r'../albumsToSort/'
    else:
        pathText = r'../pics/'

    response = requests.get(url)
    if response.status_code == 200:
        print('Downloading {}...'.format(fileName))
        with open(r'{}{}'.format(pathText, fileName), 'wb') as openFile:
            for i in response.iter_content(4096):
                openFile.write(i)

if __name__ == '__main__':
    targetSub = 'hentai'
    imgurPattern = re.compile(r'(http://i.imgur.com/(.*))(\?.*)?')
    r = praw.Reddit(user_agent='windows:SubbreditImgurAlbumDownloader:v0.3 (by /u/YuiYukihira)')

    posts = r.get_subreddit(targetSub).get_new(limit=50)
    for post in posts:
        try:
            print('Checking: {}'.format(str(post)))
            if 'imgur.com/' not in post.url:
                continue
            if len(glob.glob('pics/reddit_{}_{}_*'.format(targetSub, post.id))) > 0:
                continue

            if 'http://imgur.com/a/' in post.url:
                imageId = post.url[len('http://imgur.com/a/') + 1:]
                downloader = albumDown.ImgurAlbumDownloader(post.url)
                downloader.on_image_download(ShowProgress)
                downloader.save_images('../albumsToSort/'+imageId)

            elif 'http://i.imgur.com/' in post.url:
                mo = imgurPattern.search(post.url)

                imgurFileName = mo.group(2)
                if '?' in imgurFileName:
                    imgurFileName = imgurFileName[:imgurFileName.find('?')]

                localFileName = 'reddit_{}_{}_imgur_{}'.format(targetSub, post.id, imgurFileName)
                GetImage(post.url, localFileName, False)

            elif 'http://imgur.com' in post.url:
                try:
                    htmlSource = requests.get(post.url).text
                    soup = BeautifulSoup(htmlSource, 'html.parser')
                    imageUrl = soup.select('link')[10]['href']
                    if imageUrl.startswith('//'):
                        imageUrl = 'http:' + imageUrl
                    imageId = imageUrl[imageUrl.rfind('/') + 1:imageUrl.rfind('.')]

                    if '?' in imageUrl:
                        imageFile = imageUrl[imageUrl.rfind('/') + 1:imageUrl.rfind('?')]
                    else:
                        imageFile = imageUrl[imageUrl.rfind('/') + 1:]

                    localFileName = 'reddit_{}_{}_imgur_{}'.format(targetSub, post.id, imageFile)
                    GetImage(imageUrl, localFileName, False)
                except:
                    pass
        except:
            pass
