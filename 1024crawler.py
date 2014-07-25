import urllib.request
import os
import re
from bs4 import BeautifulSoup
def crawerEach(url,urldir):
    resp=urllib.request.urlopen(url)
    html=resp.read().decode('gbk')
    soup = BeautifulSoup(html)
    items=soup.find('body').find('div',id='main').find(name='div',attrs={"class":"t","style":"margin:3px auto"}).find('table',id='ajaxtable').find("tbody").findAll(name="tr",attrs={"class":"tr3 t_one"})
    for item in items:
        target=item.find(name='td',attrs={"style":"text-align:left;padding-left:8px"}).find('h3').find('a')
        if target.u ==  None and target.b == None and target.font == None:
            urldir[target.text] = "http://wo.yao.cl/"+target.get('href')
    return urldir
    
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

def search():
    keyword = input("请输入关键字：")
    file=open("all.xml",'r',encoding='utf-8')
    content=file.read()
    soup=BeautifulSoup(content)
    items=soup.findAll(name="article",attrs={"title":re.compile(keyword)})
    for item in items:
        print(item.get('title') + item.text)
if __name__=="__main__":
    print("1--更新")
    print("2--查询")
    choose=input("请输入结果：")
    if choose=="1":
        crawer()
    else:
        search()
    print("The End")
