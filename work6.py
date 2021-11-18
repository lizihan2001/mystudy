from bs4 import BeautifulSoup
import requests
import json
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
}
url = 'https://www.autohome.com.cn/news/1/#liststart'
base_url = 'https:'
def get_html(url):
    res = requests.get(url,headers=headers)
    return res.text
def get_sum_info(html):
    soup = BeautifulSoup(html,'lxml')
    ul_s = soup.find_all('ul',class_="article")
    next_url = 'https://www.autohome.com.cn'+soup.find('a',class_='page-item-next',target="_self")['href']
    # print(next_url)
    sum_car_info_list = []
    for i in ul_s:
        li_s = i.find_all('li',id='')
        k=0
        for j in li_s:
            dict={}
            if j.find('h3')!=None:
                dict['title'] = j.find('h3').text
            else:
                dict['title'] = '发布者很懒没有设置标题，详情请点击链接查询'
            if j.a['href']!=None:
                title_url = base_url + j.a['href']
                # print(title_url)
                dict['href'] = title_url
            else:
                dict['href'] = '没有链接'
            eyes = j.find_all('em')[0].text
            dict['浏览量'] = eyes
            newurl,s_name,time = get_newurl(get_html(title_url))
            dict['时间'] = time
            if newurl != None:
                name,role,bumen,aihao=get_info(get_html(newurl))
                dict['发布人'] = name
                dict['发布人部门'] = bumen
                dict['发布人爱好'] = aihao
                dict['发布人角色'] = role
            else:
                dict['发布人'] = s_name
                dict['发布人部门'] = '无法查询'
                dict['发布人爱好'] = '无法查询'
                dict['发布人角色'] = '无法查询'
            sum_car_info_list.append(dict)
            k=k+1
            print('爬取中'+'*'*k)
            print(dict)
            print('一条信息完整爬取')
    #     print(sum_car_info_list)
    print('当页数据爬取完成！')
    return sum_car_info_list,next_url



def get_newurl(html):
    soup = BeautifulSoup(html, 'lxml')
    if soup.find('a',class_='name')!=None:
        url = base_url+soup.find('a',class_='name')['href']
        time = soup.find('span',class_='time').text.replace('\r','').replace('\n','').replace(' ','')
        name = None
    elif soup.find('a',class_='name')==None and soup.find('span', class_='time')!=None and soup.find('div',class_='name')!=None:
        url = None
        time = soup.find('span', class_='time').text.replace('\r','').replace('\n','').replace(' ','')
        name = soup.find('div',class_='name').text.replace('\r','').replace('\n','').replace(' ','')
        # print(type(name))
    else:
        url = None
        time = None
        name = None
    return url, name, time


def get_info(html):
    soup = BeautifulSoup(html,'lxml')
    name = soup.find('span',class_='eblog-editor-detail__name').text
    role = soup.find('span',class_='eblog-editor-detail__role').text
    bumen = soup.find_all('p',class_='eblog-editor-detail__item')[0].text.split('：')[1]
    aihao = soup.find_all('p',class_='eblog-editor-detail__item')[1].text.split('：')[1]
    return name,role,bumen,aihao
def save(sum_info):
    with open('./carnews.json', 'a+', encoding='utf-8') as f:
        json.dump(sum_info, f, ensure_ascii=False)
    print('保存完成')
i=1
num = eval(input('爬取几页数据：'))
while url:
    if i<num+1:
        sum_info,url=get_sum_info(get_html(url))
        save(sum_info)
        print('第{}页爬取完成\n\n'.format(i))
        i=i+1
    else:
        break