#
import re
import requests
import time
import random
YongChuanInfo = '''
<DIV class=clubs_hd>
  <H2 class=club_name><A href="https://bbs.cqyc.net/forum-2-1.html" 
  target=_blank>聚焦永川</A><SPAN class=count>(今日帖: <EM 
  class=forum_tpost>416</EM>)</SPAN></H2>
  <H3 class="club_logo club21"><A href="https://bbs.cqyc.net/forum-2-1.html" 
  target=_blank>聚焦永川</A></H3></DIV>
  <DIV class="clubs_list cc"><A href="https://bbs.cqyc.net/forum.php?mod=forumdisplay&amp;fid=2&amp;filter=typeid&amp;typeid=1" 
  target=_blank>永川杂谈</A><A href="https://bbs.cqyc.net/forum.php?mod=forumdisplay&amp;fid=2&amp;filter=typeid&amp;typeid=2" 
  target=_blank>永川新闻</A><A href="https://bbs.cqyc.net/forum.php?mod=forumdisplay&amp;fid=2&amp;filter=typeid&amp;typeid=3" 
  target=_blank>网友报料</A><A href="https://bbs.cqyc.net/forum.php?mod=forumdisplay&amp;fid=2&amp;filter=typeid&amp;typeid=4" 
  target=_blank>百姓心声</A><A href="https://bbs.cqyc.net/forum-44-1.html" 
  target=_blank>发展永川</A><A href="https://bbs.cqyc.net/forum.php?mod=forumdisplay&amp;fid=2&amp;filter=typeid&amp;typeid=5" 
  target=_blank>社会热点</A><A href="https://bbs.cqyc.net/forum.php?mod=forumdisplay&amp;fid=2&amp;filter=typeid&amp;typeid=78" 
  target=_blank>回音壁</A><A href="https://bbs.cqyc.net/forum-39-1.html" 
  target=_blank>会员相册</A></DIV></LI>
  <LI 
  style="POSITION: absolute; BORDER-BOTTOM-COLOR: rgb(255,255,255); BORDER-TOP-COLOR: rgb(255,255,255); BORDER-RIGHT-COLOR: rgb(255,255,255); BORDER-LEFT-COLOR: rgb(255,255,255); TOP: 0px; LEFT: 199px" 
  class="club_items w217 cc">

'''

'''
respone2=re.compile('<H2 .+?=club_name><A href="(.+?)".+?>(.+?)</A>.+?<DIV class="clubs_list cc">(.+?)</DIV>',re.I|re.S)
respone3=re.compile('A href="(.+?)".+?>(.+?)</A>',re.I|re.S)
index2=respone2.findall(YongChuanInfo)
str=index2[0][2].replace('amp;','')
print(index2[0])
index=[(index2[0][0],index2[0][1])]
index4=respone3.findall(str)
print(index4)
for i in index4:
    index.append(i)
print(index)
'''


def getPageInfo(s):
    YongChuan_list = []
    #根据html结构可知每个框之下的子标题个数不同，所以可以将div下所有内容先提取出来再做进一步处理
    respone1 = re.compile('<H2 .+?=club_name><A href="(.+?)".+?>(.+?)</A>.+?<DIV class="clubs_list cc">(.+?)</DIV>',re.I | re.S)
    respone2 = re.compile('A href="(.+?)".+?>(.+?)</A>', re.I | re.S)
    #index= respone1.findall(s)将html文本中的每一块中，（大标题的网址）（大标题名称）（包含div中所有的小标题html文本）分别对应下标[0][1][2]
    index = respone1.findall(s)
    #z，通过index中元组的个数，判断有多少个大标题方块
    z = int(len(index))
    List = []
    #对每个方块中进行数据处理
    for i in range(0, z):
        #将第i个元组，即第i个方块中的子标题链接中会造成网址错误的amp;去掉
        str = index[i][2].replace('amp;', '')
        #将第i个方块中的大标题与链接储存按照：（’大标题‘，’链接‘）存入list表
        List.append((index[i][0], index[i][1]))
        #在处理后的小标题html内容str，得到小标题的字与链接：
        index1 = respone2.findall(str)
        for j in index1:
            # 将第i个方块中的小标题与链接储存按照：（’小标题‘，’链接‘）存入list表
            List.append(j)
    info_dict = {}
    #将获取到的信息按照{’标题‘：’链接‘}的格式存入字典info_dict
    for i in List:
        info_dict[i[1]] = i[0]
    #将字典放入列表
    YongChuan_list.append(info_dict)
    return YongChuan_list

#获取html文本
def getPagestr(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
    }
    respone = requests.get(url, headers=headers)
    #返回响应文本
    return respone.text


def main():
    url = "https://www.cqyc.net"
    temp = getPageInfo(getPagestr(url))
    print(temp)


if __name__ == '__main__':
    main()