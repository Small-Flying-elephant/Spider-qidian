#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author : linsheng
import os
import urllib2
import urllib
from bs4 import  BeautifulSoup
import time
import lxml
import re
from selenium import  webdriver
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
def After_completing_this(urls):

    file_text=urllib2.urlopen(urls).read()
    readhtml=BeautifulSoup(file_text,'lxml')
    Name_of_the_novel=readhtml.select('body > div.wrap > div.all-pro-wrap.box-center.cf > div.main-content-wrap.fl > div.all-book-list > div > ul > li > div.book-mid-info > h4 > a')
    author = readhtml.select('body > div.wrap > div.all-pro-wrap.box-center.cf > div.main-content-wrap.fl > div.all-book-list > div > ul > li > div.book-mid-info > p.author > a.name')
    novel_type = readhtml.select('body > div.wrap > div.all-pro-wrap.box-center.cf > div.main-content-wrap.fl > div.all-book-list > div > ul > li > div.book-mid-info > p.author > a.go-sub-type')
    The_end_or_not = readhtml.select('body > div.wrap > div.all-pro-wrap.box-center.cf > div.main-content-wrap.fl > div.all-book-list > div > ul > li > div.book-mid-info > p.author > span')
    url_path=readhtml.select('body > div.wrap > div.all-pro-wrap.box-center.cf > div.main-content-wrap.fl > div.all-book-list > div > ul > li > div.book-mid-info > h4 > a')

    for  Name_of_the_novels ,authors,novel_types,The_end_or_nots,url_paths in zip(Name_of_the_novel,author,novel_type,The_end_or_not,url_path):

        data = {
            "Name_of_the_novel_s":Name_of_the_novels.get_text(),
            "author_s":authors.get_text(),
            "novel_type_s":novel_types.get_text(),
            "The_end_or_not_s":The_end_or_nots.get_text(),
            "url_path_s" :url_paths.attrs['href']
        }
        with open('xiao_shuo_info.txt','a') as wrxs:
            wrxs.write(str(data['Name_of_the_novel_s']) +'   ')
            wrxs.write(str(data['author_s'] )+ '   ')
            wrxs.write(str(data['novel_type_s']) + '   ')
            wrxs.write(str(data['The_end_or_not_s']) + '   ')
            wrxs.write('http:'+str(data['url_path_s'])+ '   ')
            wrxs.write('\r\n')
    return Name_of_the_novel

def Get_a_novel_directory(novel_directory):

    for novel_url_item in novel_directory:
        novel_number=str(novel_url_item.attrs['href']).split('/')
        # print 'http://m.qidian.com/book/showbook.aspx?bookid=' + str(novel_number[-1])
        directory_source=urllib2.urlopen('http://m.qidian.com/book/'+str(novel_number[-1])+'/catalog').read()
        dir_content=BeautifulSoup(directory_source,'lxml')
        file_name = dir_content.select('#header > h1')
        chapter_name=dir_content.select('#volumes > li > a > span')
        dir_urlpath = dir_content.select('#volumes > li > a')

        for item in file_name:
            if os.path.exists('item.get_text()')==False:
                os.mkdir(item.get_text())
            else:
                print 'dir exists'

            for  items in range(len(chapter_name)):
                print dir_urlpath[items].attrs['href']
                dir_urlpath_number=dir_urlpath[items].attrs['href'].split('/')
                print dir_urlpath_number[-1]
                content_content=urllib2.urlopen('http://m.qidian.com/book/' + str(novel_number[-1]) + '/'+dir_urlpath_number[-1])
                html_content=BeautifulSoup(content_content,'lxml')
                body_content=html_content.select('#chapterContent > section > p')
                for body_content_item in body_content:
                    with open(item.get_text()+'/'+chapter_name[items].get_text(),'a') as writecontent:
                        writecontent.write(str(body_content_item.get_text()) + '\r\n')
                time.sleep(3)
def spider_qidian(urls):

    #遍历完本小说,并记录信息到TXT文件中
    novel_directory=After_completing_this(urls)

    #获取小说目录 （错在错误）
    Get_a_novel_directory(novel_directory)

if __name__ == '__main__':

    urls = 'http://fin.qidian.com/'
    spider_qidian(urls)