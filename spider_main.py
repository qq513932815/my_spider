#coding:utf-8
'''
Created on 2018年4月16日

@author: LXT
'''
from bs4 import BeautifulSoup
import re
import urllib2

#url
class UrlManager(object):  
    
    #向html解析器发送网址进行解析
    def open_url(self, root_url):
        if root_url is None or len(root_url) == 0:
            return
        return root_url
class HTMLDownloader(object):
    
    
    def download(self, root_url):
        if root_url is None:
            return 'URL Is None !'
        response = urllib2.urlopen(root_url)
        
        if response.getcode() != 200:
            return 'Response failed !'
        return response.read()
    

class UrlPaser(object):
    
    def get_data(self, page_url, url_text):
        soup = BeautifulSoup(url_text,'html.parser',from_encoding='utf-8')
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
        

class HTMLOutputer(object):
  
    #输出器
    def OutputHTML(self,data):
        
        fout = open('output.html', 'w')
        
        if data is None or len(data) == 0:
            fout.write('<p>No Data Output !</p>') 
        fout.write('<html>')
        fout.write('<header>')
        fout.write('<title>爬取结果</title>')
        fout.write('<meta charset="utf-8">')
        fout.write('</header>')
        fout.write('<body>')
        fout.write('<table>')
        
        #python默认使用ascii编码，需转换为utf8
#         for data in self.datas:
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
        new_url = self.UrlManager.open_url(root_url)
        url_text = self.HTMLDownloader.download(new_url)
        url_paser = self.UrlPaser.get_data(new_url,url_text)
        html_outputer = self.HTMLOutputer.OutputHTML(url_paser)

if __name__ == '__main__':
    root_url = "http://baike.baidu.com/item/Python/407313"
    Spider = SpiderMain()
    Spider.craw(root_url)
    
    