import redis
import configparser
from helper.logger import logger

class UrlManger():
    def __init__(self):
        self.__cf=configparser.ConfigParser()
        self.__cf.read("SSpider.conf")
        confret=self.__cf.sections()
        if len(confret) <1:
            logger.error("read config file error")
            exit(-1)
        self.__rdisconn=redis.Redis(host=self.__cf.get("Redis","host"),port=self.__cf.get("Redis","port"),db=self.__cf.get("Redis","db"))


    def __del__(self):
        pass


    def has_new_url(self):
        return  self.__rdisconn.scard("new_urls")

    def add_new_url(self,url):
        if url is None:
            return
        if  not self.__rdisconn.sismember("new_urls",url) and not self.__rdisconn.sismember("old_urls",url):
            #self.new_urls.add(url)
            self.__rdisconn.sadd("new_urls",url)

    def get_new_url(self):
        bnew_url = self.__rdisconn.spop("new_urls")
        if bnew_url is None:
            return
        new_url = bnew_url.decode()
        self.__rdisconn.sadd("old_urls",new_url)
        return new_url



if __name__=='__main__':
    urlmgr = UrlManger()
    print(urlmgr.has_new_url())
    urlmgr.add_new_url("www.baidu2.com")
    m_url = urlmgr.get_new_url()
    print(m_url)
    print(urlmgr.has_new_url())