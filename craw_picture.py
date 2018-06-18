#coding:utf-8
import requests
from bs4 import BeautifulSoup
import re
import os

def getHTMLText(url):
    """获得原始网页代码"""
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        return ""


def save_picture(picture_url, fpath):
    try:
        picture = requests.get(picture_url)
        picture.raise_for_status()
        with open(fpath, 'wb') as f:
            f.write(picture.content)
    except:
        return ""


def get_picture_name(url):
    """从图片链接中获取图片名称"""
    pic_name = url.split('/')[-1]
    return pic_name


def get_picture(html,start_fpath):
    """从原始网页中获取图片"""
    soup = BeautifulSoup(html, 'html.parser')

    if soup:
        #获取存放改网页所有图片的文件夹名称,并新建该目录
        folder_name = soup.find('title').text.split(' ')[0]
        print("当前处理页面：",folder_name)
        folder_path = start_fpath + '/' + folder_name
        folder_isExists = os.path.exists(folder_path)
        if not folder_isExists:
            os.makedirs(folder_path)

        #查找图片相关的网页源代码段，并将其中网页链接的相关标签存入列表
        pic_info = soup.find('div', attrs={'class': 'pics'})
        pic_list = pic_info.find_all('img')
        
        
        #将图片的链接存入列表
        pic_url_list = []
        for i in range(len(pic_list)):
            pic_url_list.append(pic_list[i].attrs['src'])

        #遍历图片链接的列表，存储图片到本地目录
        for i in range(len(pic_url_list)):
            pic_name = get_picture_name(pic_url_list[i])
            fpath = start_fpath + '/' + folder_name + '/' + pic_name
            picture_isExists = os.path.exists(fpath)
            if not picture_isExists:
                save_picture(pic_url_list[i], fpath)
            print("共%d张照片，已爬取%d张照片，当前进度：%.2f%%" % (len(pic_url_list), (i + 1), float(i + 1) / len(pic_url_list) * 100))
        print("-"*60)
        print("\n")
        


def get_url_list(list_url, start_url):
    """从导航页中得到包含不同组图的网页链接列表"""
    original_html = getHTMLText(list_url)
    #soup = BeautifulSoup(original_html, 'html.parser')
    #url_info=soup.find('li')
    original_list = re.findall(r'href=\"/htm/pic9/.*?htm', original_html)
    url_list=[]
    for i in range(len(original_list)):
        last_url = original_list[i].split('/')[-1]
        url = start_url + last_url
        url_list.append(url)
    return url_list
        


def main():
    #PC用路径
    #start_fpath = 'F:/Craw Picutre/偷拍自拍'
    #NAS用路径
    start_fpath = '/volume1/爬虫相关/Craw Picutre/偷拍自拍'
    start_url = 'http://www.183jj.com/htm/pic9/'
    start_list_url = 'http://www.183jj.com/htm/piclist9/'
    #url = start_url + '120672' + '.htm'
    #html = getHTMLText(url)
    for i in range(1, 50):
        list_url = start_list_url + str(i) + '.htm'
        url_list=get_url_list(list_url, start_url)
        for j in range(len(url_list)):
            html=getHTMLText(url_list[j])
            get_picture(html, start_fpath)
    print("所有爬取已完成")
    os.system("pause")

if __name__=="__main__":
    main()


    