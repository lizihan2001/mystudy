import re
import requests
import json
import time
import random
'''
    单位：重庆文理学院20数据科学1
    文件创建者：李子晗
    文件说明：
        用来爬取永川二手房网（https://fc.cqyc.net/resoldhome/esf/list）二手房内容信息（包括：标题；链接；户型；楼层；朝向；建筑年代；地址；详细地址；房主；数据更新时间；面积；价格；单位面积价格）；
        主要功能特色：
        ①可以爬取任意多的页面
        ②在输入爬取页数是，值错误会继续运行重新输入，无需再次开启程序
        ③当每次爬取完页面后：可选择是否罗列当页每个二手房的信息，输入y罗列，输入其他不罗列继续爬取下一页
    创建时间：2021/10/26  20:30
    修改时间：2021/10/27  14:52
        修改内容：
            ①解决了输入页数为负数时候,返回值为空的问题。
    修改时间：2021/11/4   12:50
        修改内容：
            ①新增爬取房屋图片链接功能，无房屋图片返回字符串‘无房屋图片’
            ②新增爬取房源描述功能，无房源描述返回字符串‘无房源描述’
            ③显示爬取进度图形化，代码运行等待时候进度可知化
            ④将两个新功能①②写入功能列表，如果不需要就不爬取，需要的话爬取后会存入一开始的temp字典中方便取用
    注：
        文本内容仅供参考，仅用于交流学习，
        我的GitHub网址："https://github.com/lizihan2001/mystudy"
        我的gitee网址："https://gitee.com/li-zihan-2001"       
'''

def getPageInfo(s):
    reg1 = re.compile('<li class="item clearfix">.+?<div class="content fl">.+?href="(.+?)".+?>(.+?)</a>.+?<p class="detail">(.+?)</p>.+?<a.+?>(.+?)</a>.+?<a.+?>(.+?)</a>.+?<a.+?>(.+?)</a>.+?<span class="maps">(.+?)</span>.+?<a.+?>(.+?)</a>.+?<span>(.+?)</span>.+?<span class="area-detail_big">(.+?)</span>(.+?)</p>.+?<em class="prices">(.+?)</em>(.+?)</p>.+?<p.+?>(.+?)</p>',re.DOTALL)
    reg2 = re.compile('<span>(.+?)</span>')
    reg3 = re.compile('：</span>(.+)')
    index = reg1.findall(s)
    List=[]
    for i in index:
        info_dict = {}
        info_dict["标题"]=i[1]
        info_dict["链接"]='https://fc.cqyc.net'+i[0]
        index1 = reg2.findall(i[2])
        index2 = reg3.findall(i[2])

        index1.append(index2[0])
        if len(index1)==3:
            info_dict["户型"]=index1[0]
            info_dict["楼层"]=index1[1]
            info_dict["建筑年代"]=index1[2].replace(' ','')

        if len(index1)==4:
            info_dict["户型"] = index1[0]
            info_dict["楼层"] = index1[1]
            info_dict["朝向"] = index1[2]
            info_dict["建筑年代"] = index1[3].replace(' ', '')
        info_dict["地址"]=i[3]+i[4]+i[5].replace('\n','').replace(' ','')
        info_dict["详细地址"]=i[6]
        info_dict["房主"]=i[7]
        info_dict["数据更新时间"]=i[8]
        info_dict["面积"]=i[9]+i[10]
        info_dict["价格"]=i[11]+i[12]
        info_dict["单位面积价格"]=i[13]
        List.append(info_dict)
    return List

def getPageInfo1(text):
    description = {}
    reg_info = re.compile('<div class="detailDesc-i.+? detailDesc-i">.+?<div class="detailDesc-label">(.+?)</div>.+?<div class="detailDesc-text">.+?<p>(.+?)</p>',re.DOTALL)
    index_info = reg_info.findall(text)

    for i in range(0, len(index_info)):
        description[index_info[i][0]] = index_info[i][1]
    if len(index_info) != 0:
        return description
    if len(index_info) == 0:
        return '该房屋没有房源描述'

def getPageInfo2(text):
    Listing_pictures = []
    reg_info1 = re.compile('<div class="detailImg">(.+?)<a id="content3"></a>', re.DOTALL)
    reg_info1_1 = re.compile('<div class="detailImg-item">.+?<img src="(.+?)".+?>.+?</div>', re.DOTALL)
    index_info1 = reg_info1.findall(text)
    index_info1_1 = reg_info1_1.findall(index_info1[0])
    for i in index_info1_1:
        Listing_pictures.append(i)
    if len(index_info1_1) != 0:
        return Listing_pictures
    if len(index_info1_1) == 0:
        return '该房屋没有房屋图片'



def getPagestr(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
    }
    respone = requests.get(url, headers=headers)
    #返回响应文本
    return respone.text

def main():
    while 1:
        try :
            n=int(input("请输入爬取页数:"))
            assert n>0
        except ValueError:
            print('输入错误，请输入阿拉伯数字！')
        except AssertionError:
            print('不可爬取负数页！')
        else:
            for i in range(1,n+1):
                url = "https://fc.cqyc.net/resoldhome/esf/list?page={}".format(i)
                temp = getPageInfo(getPagestr(url))
                time.sleep(random.randint(1, 3))
                print("第{}页数据：\n".format(i),temp)
                while 1:
                    m=input("是否进行如下操作（是[请输入操作编号]/否[输入不在表中的任意字符]）\na.罗列爬取到的房屋信息\nb.罗列具体的房源描述\nc.罗列房源图片\n")
                    if m=='a':
                        for j in temp:
                            print(j)
                    elif m=='b':
                        for j in range(len(temp)):
                            temp[j]['房源描述'] = getPageInfo1(getPagestr(temp[j]['链接']))
                            print('爬取中',j*'#',(59-j)*'-')
                        n=input('是否罗列所爬取的房屋描述[是（y）/否（任意字符）]')
                        if n=='y':
                            for k in temp:
                                print(k['房源描述'])
                        else:
                            pass
                    elif m=='c':
                        for j in range(len(temp)):
                            temp[j]['房屋图片'] = getPageInfo2(getPagestr(temp[j]['链接']))
                            print('爬取中',j*'#',(59-j)*'-')
                        n = input('是否罗列所爬取的房屋图片[是（y）/否（任意字符）]')
                        if n == 'y':
                            for k in temp:
                                print(k['房屋图片'])
                        else:
                            pass
                    else:
                        break
                with open('./YongchuanSecondHandHouse.json', 'a+', encoding='utf-8') as f:
                    json.dump(temp, f, ensure_ascii=False)
            else:
                print('已爬取全部所需内容！')
            break
if __name__ == '__main__':
    main()

