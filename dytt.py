import requests
import re
from bs4 import BeautifulSoup

'''
获取电影天堂最新的电影下载链接
'''

class Dytt():

    def __init__(self,url,page_num):
        self.url = url
        self.url_list = [url+"/html/gndy/dyzz/list_23_"+str(i)+".html" for i in range (1,page_num+1)]


    def get_ftp(self,sub_url):
        #主要界面获取ftp链接的
        sub_page = requests.get(sub_url)
        sub_html = sub_page.content.decode("gbk")
        res = re.compile(r'(ftp://.*?\.(rmvb|avi|mp4|mkv))')
        ftp_link = res.findall(sub_html)[0][0]
        return ftp_link
    
    
    def new_movie(self):
        movie_list={}
        for u in self.url_list:
            base_page = requests.get(u)
            html = base_page.content.decode("gbk")
            soup = BeautifulSoup(html)
            for link in  soup.find_all("a",class_="ulink"):
                #每个link实际是一个tag类
                sub_link = self.url +link['href']
                ftp = self.get_ftp(sub_link)
                #以名字为key,链接为value返回字典
                movie_list[link.get_text()] = ftp
        return movie_list

if __name__ == "__main__":
    url = "https://www.dytt8.net"
    page_num=1
    for k,v in Dytt(url,page_num).new_movie().items():
        print (k,"----",v)