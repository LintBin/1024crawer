import urllib.request
import os
import re
import time
import socket
from bs4 import BeautifulSoup
def crawerEach(url,urldir):
    resp=urllib.request.urlopen(url)
    html=resp.read().decode('gbk')
    soup = BeautifulSoup(html)
    items=soup.find('body').find('div',id='main').find(name='div',attrs={"class":"t","style":"margin:3px auto"}
                                                       ).find('table',id='ajaxtable'
                                                              ).find("tbody").findAll(name="tr",attrs={"class":"tr3 t_one"})
    for item in items:
        target=item.find(name='td',attrs={"style":"text-align:left;padding-left:8px"}).find('h3').find('a')
        if target.u ==  None and target.b == None and target.font == None:
            urldir[target.text] = "http://wo.yao.cl/"+target.get('href')
    return urldir
#爬下所有文章的标题的URL地址    
def crawer():
    urldir={}
    for i in range(39):
        url="http://wo.yao.cl/thread0806.php?fid=20&page="+str(i+1)
        print("=====================正在爬取第"+str(i+1)+"页=========")
        urldir=crawerEach(url,urldir)
    f=open("all.xml",'w',encoding="utf-8")
    for key,url in urldir.items() :
        firstColumn="<article title="+"\""+key+"\">"
        secondColumn="   "+"<url>"+url+"</url>"
        thirdColumn="</article>"
        f.write(firstColumn+'\n'+secondColumn+'\n'+thirdColumn+'\n')
    f.close()
    
    
#以文章的标题模糊搜索
def search():
    keyword = input("请输入关键字：")
    file=open("all.xml",'r',encoding='utf-8')
    content=file.read()
    soup=BeautifulSoup(content)
    items=soup.findAll(name="article",attrs={"title":re.compile(keyword)})
    for item in items:
        print(item.get('title') + item.text)

#获得文章内容
def getContent(soup , author ,url, pageAccount):
    contents = soup.body.find(name='div',attrs={'id':'main'}).findAll(name='div',attrs={'class':'t t2'})
    tid = url[-12:]
    print (tid)
    #获得首页的文章内容
    for item in contents:
        if(item.find('table').find(name='tr',attrs={'class':'tr3 tr1'}).find('font').b.text == author):
            content = item.table.find(name='tr',attrs={'class':'tr3 tr1'}).find(name='th',attrs={'class':'r_one'}
                                                                            ).table.tr.td.find(name='div',attrs={'class':'tpc_content'}).text
            writeContent(content)
            print(content)
            print("")
    pageInt = int(pageAccount)
    i = 2
    while i<=pageInt:
        pageUrl = "http://wo.yao.cl/read.php?tid=" + tid + "&page=" + str(i)
        print(pageUrl)
        getAuthorFloorContent(pageUrl,author)
        i=i+1
    print(pageUrl)

#把内容写入文件
def writeContent(content):
    f=open('content1.txt','a',encoding='utf-8')
    f.write(content)
    f.write('\n')
    f.write('\n')
    f.write('\n')
    f.write('\n')
    f.close()



'''以下为获得内容所做的准备'''
#获得第2页以后的页面的作者的楼层中的内容
def getAuthorFloorContent(pageUrl,author):
    resp=urllib.request.urlopen(pageUrl)
    html=resp.read().decode('gbk')
    soup = BeautifulSoup(html)
    #获得所有楼层
    contents = soup.body.find(name='div',attrs={'id':'main'}).findAll(name='div',attrs={'class':'t t2'})
    
    for item in contents:
        #在所有楼层中选出作者的楼层
        if(item.find('table').find(name='tr',attrs={'class':'tr1'}).find(name='th',attrs={'class':'r_two'}).b.text == author):
            content = item.table.find(name='tr',attrs={'class':'tr1'}).find(name='th',attrs={'class':'r_one'}
                                                                            ).find(name='div',attrs={'class':'tpc_content'}).text
            writeContent(content)
            print(content)
            print("")
    

    
#获得帖子中共有多少页
def getContentPage(soup):
    divItems = soup.body.find('div',id='main').findAll(name='div',attrs={'class':'t3'})
    #获得页数的节点
    pageAccounts = divItems[2].table.tr.td.find(name='div',attrs={'class':'pages'}).findAll(name='a',attrs={'style':None})
    pageAccount = pageAccounts[len(pageAccounts)-1].text
    print("页数为：" + pageAccount)
    return pageAccount



#获得作者名字
def getAuthor(soup):
    author = soup.body.find('div',id='main').find(name='div',attrs={'class':'t t2'}
                                                  ).find('table').find(name='tr',attrs={'class':'tr3 tr1'}).find('font').b.text
    print("作者为：" + author)
    return author


#获得文章
def getArtilcle(url):
    resp=urllib.request.urlopen(url)
    html=resp.read().decode('gbk')
    soup = BeautifulSoup(html)

    #取得帖子的页数
    account = getContentPage(soup)
    #取得文章的作者
    author = getAuthor(soup)
    #取得内容，并将内容存入txt
    content = getContent(soup , author ,url ,account)
    

#获得图片
def getPicture(url):
    #url="http://wo.yao.cl/htm_data/8/1412/1313643.html"
    resp=urllib.request.urlopen(url)
    soup = BeautifulSoup(resp)
    contents = soup.body.find(name='div',attrs={'id':'main'}).findAll(name='div',attrs={'class':'t t2'})
    #获得网页内容
    for item in contents:
        pictures = item.table.find(name='tr',attrs={'class':'tr3 tr1'}).find(name='th',attrs={'class':'r_one'}
                                                                            ).table.tr.td.find(name='div',attrs={'class':'tpc_content'}).findAll(name='input')
        i = 0
        for tag in pictures:
            print(tag['src'])
            conn = urllib.request.urlopen(tag['src'])
            f=open(str(i)+".jpg",'wb')
            i=i+1
            f.write(conn.read())
            f.close()
    resp.close();

    
    


if __name__ == "__main__":
    print("1--更新")
    print("2--查询")
    print("3--取得文章")
    print("4--取得图片")
    choose=input("请输入结果：")
    if choose=="1":
        crawer()
    else :
        if choose=="3":
            url = input("请输入文章的网址:")
            getArtilcle(url)
        else:
            if choose=="4":
                url = input("请出入图片的网址:")
                getPicture(url)
            else:
                search()
    print("The End")

    
