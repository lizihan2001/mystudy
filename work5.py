from lxml import etree
import requests
import os
import time

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
}
base_url = 'https://desk.zol.com.cn'


# 获取解析后的html
def get_html(url):
    respone = requests.get(url=url, headers=headers)
    # 出现乱码 content.decode() 默认解码是utf-8,如果不行，就尝试中文解码 gbk，gb18030,gb2312
    html_text = respone.content.decode('gb18030')

    # 使用xpath解析页面内容
    html = etree.HTML(html_text)
    return html


# 获取图片专辑的名称和连接
def get_page_imgs(html):
    imgs_list = html.xpath('//ul[@class="pic-list2  clearfix"]/li[position()>1]')
    next_url = base_url + html.xpath('//*[@id="pageNext"]/@href')[0] if len(html.xpath('//*[@id="pageNext"]/@href')) > 0 else None
    imgs_info_list = []
    for i in imgs_list:
        imgs_title = i.xpath('./a/img/@title')[0]
        imgs_href = base_url + i.xpath('./a/@href')[0]
        imgs_info_list.append((imgs_title, imgs_href))
    return imgs_info_list, next_url


# 保存图片
def save_img(img_url,title,name):
    p = './picture/'+name+'/' + str(title).replace(':'or '：','_')
    img_name = img_url.split('/')[-1]
    if not os.path.exists(p):
        os.makedirs(p)
    t = requests.get(img_url, headers=headers)
    with open(p + '/' + img_name, 'wb') as f:
        f.write(t.content)


# 在获取图片集合的连接下，获取该集合下的每张图片的最大分辨率图片的的连接
def get_high_img_href(img_info,name):
    html = get_html(img_info[1])
    imgs_href = [base_url + i for i in html.xpath('//*[@id="showImg"]/li/a/@href')]
    num = 0
    for i in imgs_href:
        num=num+1
        h = get_html(i)
        real_href = get_real_href(base_url + h.xpath('//*[@id="tagfbl"]/a[2]/@href')[0])
        save_img(real_href, img_info[0],name)
        print('爬取中' + '.' * (num % 6))

def get_real_href(img_href):
    html = get_html(img_href)
    real_href = html.xpath('//img[1]/@src')[0]
    return real_href


# 获取该集合下的每张图片的最大分辨率图片实际地址
url='https://desk.zol.com.cn'
html=get_html(url)
res=html.xpath('//*[@id="main"]/dl[1]/dd/a')
dict={}
print('以下为爬取的标题')
for i in res:
    print(i.text,end=' ')
    dict[i.text]=i.attrib['href']
k=0
while 1:
    if k>0:
        n=input('是否继续爬取[是/y,否/n]：')
        if n!='y':
            break
        else:
            pass
    k=k+1
    try:
        name=input('\n请输入想要爬取的内容：')
        next_url=url+dict[name]
    except ValueError:
        print('请输入上表所含的标题')
    except KeyError:
        print('所输入文本不在上表')
    else:
        print('你所爬取的内容所在网址:',next_url)
        print('开始爬取')
        while next_url:
            html = get_html(next_url)  # 发送请求
            imgs_info_list,next_url = get_page_imgs(html)
            for j in imgs_info_list:
                get_high_img_href(j,name)
print('爬取结束')


