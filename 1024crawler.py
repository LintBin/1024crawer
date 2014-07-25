import urllib.request
import os
import re
from bs4 import BeautifulSoup
def crawerEach(url,urldir,i):
    print(len(urldir))
    resp=urllib.request.urlopen(url)
    html=resp.read().decode('gbk')
    soup = BeautifulSoup(html)
    items=soup.find('body').find('div',id='main').find(name='div',attrs={"class":"t","style":"margin:3px auto"}).find('table',id='ajaxtable').find("tbody").findAll(name="tr",attrs={"class":"tr3 t_one"})
    #f=open("title"+str(i)+".xml",'w',encoding="utf-8")
    print("this is befor item loop " + str(len(urldir)))
    for item in items:
        target=item.find(name='td',attrs={"style":"text-align:left;padding-left:8px"}).find('h3').find('a')
        if target.u ==  None and target.b == None and target.font == None:
            urldir[target.text]=target.get('href')
            print(len(urldir))
            item_str=str(target)
            #f.write(item_str+'\n')
    #f.close()
    print("after crawerEach " + str(len(urldir)))
    print("=================================================")
    return urldir
    
def crawer():
    urldir={}
    for i in range(39):
        url="http://wo.yao.cl/thread0806.php?fid=20&page="+str(i+1)
        print("this is befor crawerEach method " + str(len(urldir)))
        urldir=crawerEach(url,urldir,i)
    f=open("all.xml",'w',encoding="utf-8")
    for key,url in urldir.items() :
        firstColumn="<article title="+"\""+key+"\">"
        secondColumn="   "+"<url>"+url+"</url>"
        thirdColumn="</article>"
        f.write(firstColumn+'\n'+secondColumn+'\n'+thirdColumn+'\n')
    f.close()

if __name__=="__main__":
    crawer()
