from helper.logger import logger
from SSpider import SSpider


if __name__ == '__main__':
    #print(soup.prettify())
    #analysisUrl("www.baidu.com")
    myspider = SSpider.SSpider()
    myspider.add_root_url("http://www.smzdm.com/")
    myspider.craw()
