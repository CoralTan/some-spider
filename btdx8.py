import requests
import re
from bs4 import BeautifulSoup


class Btdx8():


    def __init__(self,host):
        self.host = host
        self.headers = {'User-Agent':'Chrome/73.0.3683.75'}

    def get_down_page(self,url):
        #详情页面的分析https://www.btdx8.com/torrent/fcrs_2019.html这种
        html = requests.get(url,headers=self.headers).content.decode("utf-8")
        soup = BeautifulSoup(html,"html.parser")
        link = soup.find('div',id="zdownload").find("a")
        movie_name = link.get_text()
        #更新cookie
        post_id = soup.find('div',class_="entry lazyload")["id"].split("-")[1]
        self.headers['cookie']="btpc_%s=%s"%(post_id,post_id)
        return (link["href"],movie_name)

    def get_zhongzi(self,links): 
        r = self.get_down_page(links)
        link = r[0]
        bt_name = r[1]
        #download界面分析
        zhongzi_page = requests.get(link,headers=self.headers).content.decode("utf-8")
        res1 = re.compile(r'file_id:\s\S*"')
        res2 = re.compile(r'fc:\s\S*"')
        file_id = res1.findall(zhongzi_page)[0].split(': ')[1].replace('"','')
        fc = res2.findall(zhongzi_page)[0].split(': ')[1].replace('"','')
        data = {'file_id': file_id, 'fc': fc}
        zhongzi_url = self.host+'/calldown/calldown.php'
        rsp = requests.post(zhongzi_url,data=data)
        bt_url = rsp.json()["down"]
        #下载种子啦
        #这里有防盗链，所以要从主页链接过去
        bt_headers = {'Referer': link}
        try:
            with open(bt_name,"wb") as f:
                f.write(requests.get(bt_url,headers=bt_headers).content)
        except:
            print("%s ----下载失败"%bt_name)
        else:
            print("%s ----下载成功"%bt_name)

    def get_newmovie(self):
        home = requests.get(self.host).content.decode("utf-8")
        soup_home = BeautifulSoup(home)
        new_movie = soup_home.find("div",class_="slider clearfix").find_all("a")
        for i in new_movie:
            self.get_zhongzi(i["href"])



if __name__ == "__main__":

    Btdx8("https://www.btdx8.com").get_newmovie()