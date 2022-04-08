from typing import List
from aiohttp import ClientSession
from bs4 import BeautifulSoup
import re
from dataclasses import dataclass

@dataclass
class Slide:
    index:int
    url:str
regex = "^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]slideshare+)\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$"

async def valid_link(link: str) -> bool:
    compiled_regex = re.compile(regex)
    if re.search(compiled_regex, link):
        return True
    return False

@dataclass
class Slides:
    author:str
    title:str
    slides:List[Slide]
    @property
    def count(self):
        return len(self.slides)

class SlideShare:
    def __init__(self):
        self.__main_domain = 'https://www.slideshare.net/'
        self.session =ClientSession(raise_for_status=True)

    async def __soup(self,url:str)-> BeautifulSoup:
        async with self.session.get(url) as resp:
            assert resp.ok
        soup = BeautifulSoup(await resp.text('utf-8'),'html.parser')
        return soup
    

    async def slides(self, url: str):
        soup =await self.__soup(url)  # type: ignore
        title = str(soup.title.text)
        author = soup.find('div', class_='author-name').find('span',{'itemprop': 'name'}).text.strip()  # type: ignore
        slides_mcp = soup.find('div', {'id': 'slide-container'}).find_all('img')  # type: ignore
        slides_list = []
        for slide_img in slides_mcp:
            print('fuck')
            src = slide_img.get('src')
            if len(src) <= 0:
                src = slide_img.get('data-original')
            index = int(slide_img.get('data-index'))
            slides_list.append(Slide(index=index,url=src))
        print('fuckkkkkkkkkkk')
        return Slides(author=author,title=title,slides=slides_list)
