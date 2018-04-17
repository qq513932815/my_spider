#coding:utf-8
'''
Created on 2018年4月16日

@author: LXT
'''
from bs4 import BeautifulSoup
import re
import urllib2
import urlparse


#url
class UrlManager(object):  

    
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()
    
    
    #向new_urls中添加新的url
    def add_new_url(self, url):
        if url is None:
            return
        #判断当前待添加的url是否存在
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)
#         print self.new_urls
        
    
    #负责前台接受解析出的url列表，解析后传递给add_new_url进行添加
    def add_new_urls(self,urls):
#         print '1',urls
        if urls is None:
            return
        if not isinstance(urls, str):
#             print '2'
            for url in urls:
                self.add_new_url(url)
    #             print "1",url
        else:
            print '3'
            self.str_add(urls)
        
    def str_add(self, urls):
        print '4'
        self.new_urls.add(urls)
        print '5',self.new_urls


    
    #判断是否存在待爬取的url
    def has_new_url(self):
        return len(self.new_urls) != 0
    
    #负责取出新的url返回给main函数
    def get_new_url(self):
        new_url = self.new_urls.pop()
#         print self.new_urls
        self.old_urls.add(new_url)
        return new_url
    
    
class HTMLDownloader(object):
    
    
    def download(self, root_url):
        if root_url is None:
            return 'URL Is None !'
        response = urllib2.urlopen(root_url)
        
        if response.getcode() != 200:
            return 'Response failed !'
        return response.read()

class UrlPaser(object):
    def __init__(self):
        self.UrlManager = UrlManager()
    
    #解析新的url
    def _get_new_urls(self, page_url, soup):
        
        new_urls = set()
        #/item/Guido%20van%20Rossum
        links = soup.find_all('a', href=re.compile(r"\/item\/[^/]*"))
        for link in links:
            new_url = link['href']
            new_full_url = urlparse.urljoin(page_url, new_url)
            new_urls.add(new_full_url)
#         self.UrlManager.new_urls.add(new_urls)
        return new_urls
    
    #解析数据
    def _get_data(self, page_url, soup):
        
        res_data = {}
        res_data['url'] = page_url
        #<dd class="lemmaWgt-lemmaTitle-title">
        #<h1>Python</h1>
        #解析url_text内容中有效数据
        title_node = soup.find('dd', class_='lemmaWgt-lemmaTitle-title').find('h1')
        res_data['title'] = title_node.get_text()
        
        #<div class="lemma-summary" label-module="lemmaSummary">
        #解析出需要的数据
        text_node = soup.find('div', class_='lemma-summary')
        res_data['text'] = text_node.get_text()
        
        return res_data
    
    #解析的总调度方法，分别调用私有方法解析新的url和所需数据
    def parse(self, new_url, url_text):
        if new_url is None or url_text is None:
            return
        
        soup = BeautifulSoup(url_text,'html.parser',from_encoding='utf-8')
        new_urls = self._get_new_urls(new_url, soup)
        new_data = self._get_data(new_url, soup)
        return new_urls, new_data
        
class HTMLOutputer(object):

    def __init__(self):
        self.datas = []
    
    #搜集所有数据
    def collect_data(self,data):
        if data is None:
            return
        self.datas.append(data)
  
    #输出器
    def OutputHTML(self):
        
        fout = open('output.html', 'w')
        
        fout.write('<html>')
        fout.write('<header>')
        fout.write('<title>爬取结果</title>')
        fout.write('<meta charset="utf-8">')
        fout.write('</header>')
        fout.write('<body>')
        fout.write('<table>')
        
        #python默认使用ascii编码，需转换为utf8
        for data in self.datas:
            print '1',data
            fout.write('<tr>')
            fout.write('<td>%s</td>' % data['url'])
            fout.write('<td>%s</td>' % data['title'].encode('utf-8'))
            fout.write('<td>%s</td>' % data['text'].encode('utf-8'))
            fout.write('</tr>')
        
        fout.write('</table>')
        fout.write('</body>')
        fout.write('</html>')
        
        fout.close()

class SpiderMain(object):
    def __init__(self):
        #初始化url管理器
        self.UrlManager = UrlManager()
        self.HTMLDownloader = HTMLDownloader()
        self.UrlPaser = UrlPaser()
        self.HTMLOutputer = HTMLOutputer()

    
    def craw(self, root_url):
        
        count = 1
        
        self.UrlManager.add_new_url(root_url)
        while self.UrlManager.has_new_url():
            try:
                #获取爬取url
                new_url = self.UrlManager.get_new_url()
#                 print new_url
                #将目标url下载为字符文件
                url_text = self.HTMLDownloader.download(new_url)
                print 'Carw %d : %s' % (count, new_url)
                #解析下载的字符串 
                new_urls, new_data = self.UrlPaser.parse(new_url,url_text)
                #将当前解析到的url添加到新的url中
                self.UrlManager.add_new_urls(new_urls)
                print "Craw Data：",new_data,"\n"
                #将解析到的数据进行输出
                self.HTMLOutputer.collect_data(new_data)
#                 print self.HTMLOutputer.datas
                if count == 10:
                    break
                count += 1
            except Exception,e:
                print "Craw Failed",e.message
        self.HTMLOutputer.OutputHTML()

if __name__ == '__main__':
    root_url = 'http://baike.baidu.com/item/Python/407313'
    Spider = SpiderMain()
    Spider.craw(root_url)
    
    