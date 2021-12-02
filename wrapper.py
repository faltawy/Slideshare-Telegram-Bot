from requests import Session
from bs4 import BeautifulSoup
import re
from errors import LinkNotValid


regex = "^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]slideshare+)\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$"


class SlideShare:
    def __init__(self):
        self.__main_domain = 'https://www.slideshare.net/'

    def valid_link(self, link: str) -> bool:
        compiled_regex = re.compile(regex)

        if not isinstance(link, str):
            raise LinkNotValid('The Link Must Be str. not int. typo')
        else:
            if re.search(compiled_regex, link):
                return True
            else:
                return False

    def slides(self, link: str):
        session = Session()
        s = session.get(link)
        if s.ok:
            soup = BeautifulSoup(s.content, features='html.parser')
            title = soup.title.text
            try:
                author = soup.find('a', class_='j-author-name').find('span',
                                                                     {'itemprop': 'name'}).text.strip()
                slides_imgs = soup.find(
                    'div', {'id': 'slide_container'}).find_all('img')
            except:
                return None
            slides_list = list()
            for slide_img in slides_imgs:
                src = slide_img.get('src')
                if len(src) <= 0:
                    src = slide_img.get('data-original')
                slides_list.append(src)
            return {'author': author, 'title': title, 'count': len(slides_list), 'slides': slides_list}
        else:
            return None
# SlideShare Search Soon https://www.slideshare.net/search/slideshow?q={Search Term}&page={Pages}
