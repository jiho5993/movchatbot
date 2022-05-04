import requests
from bs4 import BeautifulSoup as bs
from decouple import config

class BoxOffice:
    def __init__(self):
        self.KOFIC_KEY = config('KOFIC_KEY')
        self.base_url = "https://search.naver.com/search.naver?where=nexearch&query=박스오피스순위"

    def __getBoxOfficeInfo(self):
        html = requests.get(self.base_url)
        soup = bs(html.text, 'html.parser')
        
        res = soup.select("div._panel_popular > div.list_image_info > div.list_image_box > ul._panel")
        return res[0] # index 0 is popular panel
    
    def createBoxOfficeList(self):
        result = []
        data = self.__getBoxOfficeInfo()

        is_li = data.select("li")

        for i in range(10):
            img = is_li[i].select("img")[0]

            title = img["alt"]
            thumb = img["src"]
            
            result.append(
                dict(
                    title=title,
                    thumb=thumb
                )
            )
        
        return result