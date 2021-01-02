import requests
import os
import urllib
import urllib.request as request
from urllib.parse import urlparse

import wget as wget
from bs4 import *


# get the contents of the specified URL
def get_url_contents(url):
    contents = ""
    try:
        print("Downloading contents from '%s'" % url)
        contents = request.urlopen(url)
    except:
        print("Could not open %s" % url)

    return contents


# process the html page and obtain the tuple (author, link)
def process(contents, root_tag="h2"):
    bs = BeautifulSoup(contents, "html.parser")
    content = bs.find_all(root_tag)

    biblios = []

    for item in content:
        author = item.get_text()

        links = item.findNext("table").find_all("a")
        for link in links:
            if 'href' in dict(link.attrs):
                maybe_link = link['href']
                if not maybe_link.startswith("#") and not author.startswith("Lista"):
                    biblios.append(
                        (author, maybe_link)
                    )

    return biblios


# download and create directory tree inside @parent_directory
def download(author_links_list, parent_dir="Pioneers"):
    for (author, link) in author_links_list:
        print("****> Author: %s" % author)
        path = os.path.join(parent_dir, author)

        try:
            os.makedirs(path, exist_ok=True)
            print("Directory '%s' created successfully" % path)

            try:
                # print(link)
                # wget.download(prepare_url(link), path)
                download_request(link, path)
                print("File %s downloaded successfully" % link)
            except Exception as err:
                print("File %s downloaded failed" % link)
                print(err.message)
                exit(0)

        except OSError:
            print("Directory '%s' can not be created" % path)
        except KeyboardInterrupt:
            exit(0)


def download_request(url, parent_dir):
    r = requests.get(url)
    p = urlparse(url)
    file_path = p.path
    filename = os.path.basename(file_path)
    path = os.path.join(parent_dir, filename)

    with open(path, 'wb') as output_file:
        output_file.write(r.content)


def prepare_url(url):
    base_url = "http://www.centrowhite.org.br"

    p = urlparse(url)
    file_path = p.path
    old_filename = os.path.basename(file_path)
    new_filename = urllib.parse.quote(old_filename)
    file_path = file_path.replace(old_filename, new_filename)
    new_url = base_url + file_path

    print(new_url)

    return new_url


def run_pioneers():
    url = "http://www.centrowhite.org.br/downloads/ebooks-dos-pioneiros-adventistas/"
    response = get_url_contents(url)
    result = process(response, "h2")
    download(result, "Pioneers")


def run_egw():
    url = "http://www.centrowhite.org.br/downloads/ellen-g-white-ebooks-epub-pdf-mobi/"
    response = get_url_contents(url)
    result = process(response, "h3")
    download(result, "EGW")


# run the process to find and download the ebooks
def run():
    run_pioneers()
    run_egw()


# main context
run()
