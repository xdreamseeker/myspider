from SSpider import url_manager
from helper.logger import logger
import time,chardet,traceback,re

from bs4 import BeautifulSoup
import urllib.request,urllib,urllib.parse

class SSpider():
    def __init__(self):
        self.urlmgr = url_manager.UrlManger()
        self.filter = '^http://[^\s]*.smzdm.com[^\s]*'
        self.number = 1
        print(self.filter)

    def __filterUrl(self,url):
        """
        检查url是否有效
        :param url:
        :return:0 无效，1有效
        """
        return 1


    def __analyzeUrl(self,url):
        """
        检查本url中的有用信息，包括new url，及本url信息
        :param url:
        :return:分析出的new url，本页面有效信息写入db
        """
        logger.debug("number:%s"%self.number)
        self.number +=1
        logger.info("begin analysis url:%s"%url)
        result_urls=[]
        try:
            req = urllib.request.Request(url)
            req.add_header('User-Agent','Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0')

            response = urllib.request.urlopen(req)

            pagedata = response.read()
            chardit = chardet.detect(pagedata)['encoding']
            pagedata=pagedata.decode(chardit)
            #logger.debug("%s coding is %s"%(url,chardit))

            soup=BeautifulSoup(pagedata,"html.parser")

            for link in soup.find_all('a',attrs={"href":re.compile(r'^http://[^\s]*.smzdm.com[^\s]*')}):
                #print(link.get('href'))
                if self.__filterUrl(link.get('href')):
                    result_urls.append(link.get('href'))

            rc = re.compile(r'^http://[^\s]*.smzdm.com/p/\d+/')
            dataurl=rc.findall(url)
            #print(dataurl)
            if dataurl:
                #http://www.smzdm.com/p/6275447/
                my=soup.find('h1',attrs={"class":"article_title"})

                #post like http://post.smzdm.com/p/469942/
                if my is None:
                    my=soup.find('h1',attrs={"class":"item-name"})
                print(my.text)
                print("dataurl:"+dataurl[0])


        except Exception  as err:
            logger.error("url data error %s"%url)
            traceback.print_exc()
        return result_urls


    def craw(self):
        while True:
            if self.urlmgr.has_new_url() == 0:
                logger.debug("has no url in set,wait for 10 second")
                time.sleep(10)
                pass
            else:
                url = self.urlmgr.get_new_url()
                return_urls = self.__analyzeUrl(url)
                for return_url in return_urls:
                    self.urlmgr.add_new_url(return_url)
                pass

    def add_root_url(self,root_url):
        """
        增加第一个url
        :param root_url:
        :return:
        """
        self.urlmgr.add_new_url(root_url)