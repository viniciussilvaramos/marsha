import os
from json import loads, dumps
from pprint import pprint as p
from zipfile import ZipFile
from bs4 import BeautifulSoup

class Epub(object):

    def __init__(self, epub_path, cache_folder=".cache"):
        self.epub_path = epub_path
        self.cache_folder = cache_folder
        self.epub_name = os.path.basename(self.epub_path)
        self.cache_path = os.path.join(self.cache_folder, self.epub_name)
        self.all_files = []
        self.text_content = []

    def _extract_all_text(self, pages):
        print("[Epub] Extracting all text...")

        for p_path in pages:
            with open(p_path, 'r') as f:
                page = BeautifulSoup(f.read(), "lxml")
                self.text_content.append(page.text.strip())

    def _serialize(self):
        print("[Epub] Serializing...")
        with open(os.path.join(self.cache_path,"serialized.json"), "w+") as f:
            f.write(dumps({
                "content": self.text_content
            }))


    def _read_contents(self):
        print("[Epub] Reading contents...")
        path = next(filter(lambda x: "content.opf" in x, self.all_files))

        with open(path, 'r') as o:
            opf = BeautifulSoup(o.read(), "lxml")

            print("[Epub] Getting page order...")
            page_order = (i['idref'] for i in opf.findAll('itemref'))

            print("[Epub] Ordering pages...")

            content =  dict(((p['id'],p['href']) for p in opf.find("manifest").findAll("item")))
            partial_pages = (content[po] for po in page_order)

            pages = []

            for pp in partial_pages:
                page = next(filter(lambda x: pp in x, self.all_files))
                pages.append(page)

            self._extract_all_text(pages)


    def _enumerate_files(self):
        print("[Epub] Enumerating files...")
        for rootpath, dirs, files in os.walk(self.cache_path):
            for fi in files:
                self.all_files.append(os.path.join(rootpath, fi))

    def extract(self):
        print("[Epub] Extracting '{}' into folder '{}'".format(self.epub_name, self.cache_path))
        with ZipFile(self.epub_path, 'r') as epub_zip:
            epub_zip.extractall(self.cache_path)
        self._enumerate_files()
        self._read_contents()
        self._serialize()
        
        print("[Epub] Done!")

if __name__ == '__main__':
    e = Epub("/home/vvv/Downloads/O Exterminador do Futuro - James Cameron.epub")
    e.extract()
