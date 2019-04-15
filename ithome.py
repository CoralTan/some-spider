import requests
from bs4 import BeautifulSoup
import re
import json

class IThome():

    def __init__(self,host):
        self.host = host

    def get_home(self):
        ithome = requests.get(self.host) 
        ithome_home = ithome.content.decode('utf-8')
        return ithome_home

    def get_newlist(self):
        soup = BeautifulSoup(self.get_home())
        new_list = soup.find_all('li',class_='new')
        news = {}
        for new in new_list:
            tmp = new.find('a')
            if 'lapin.ithome' not in tmp["href"]:
                news[tmp.text]=tmp["href"]
        return news

    def get_comment(self,url):
        sub_page = requests.get(url).content.decode('utf-8')
        soup = BeautifulSoup(sub_page)
        comment = soup.find("iframe",id="ifcomment")
        comment_newsid = comment['data']
        #获取hash newsid 来请求https://dyn.ithome.com/ithome/getajaxdata.aspx接口获取评论
        comment_url = 'https://dyn.ithome.com/comment/'+comment_newsid
        #hash在'https://dyn.ithome.com/comment/newsid'接口中，用get
        hash_html = requests.get(comment_url,headers={'Referer': url}).text
        res = re.compile(r"\w{16}")
        hash_id = res.search(hash_html).group()
        hot_coment = requests.post("https://dyn.ithome.com/ithome/getajaxdata.aspx",headers={'Referer': comment_url},data={'newsID': comment_newsid, 'hash': hash_id, 'pid': '1', 'type': 'hotcomment'}).content.decode('utf-8')
        hot_html = json.loads(hot_coment)['html']
        # print(hot_html)
        if hot_html:
            hot_1 = BeautifulSoup(hot_html).find('li',class_="entry").find('p')
            hot_2 = str(hot_1).replace('<br/>',"\n").replace("<p>",'').replace("</p>",'')
            # print(hot_2)
            return hot_2
        else:
            return "没有热门评论"

    def hot(self):
        tmp = {}
        for k,v in self.get_newlist().items():
            tmp[k]=self.get_comment(v)
            print("获取评论：%s"%k)
        with open("news","w",encoding='utf-8') as f:
                for k,v in tmp.items():
                    f.write("-"*80+'\n'*2)
                    f.write(k+'\n'*2)
                    f.write("热门评论"+">"*60+'\n'*2)
                    f.write(v+'\n'*2)
        print("-"*60)


if __name__ == "__main__":
    a = IThome("https://www.ithome.com/")
    # a.get_comment("https://www.ithome.com/0/419/260.htm")
    a.hot()