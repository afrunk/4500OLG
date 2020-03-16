# 链接 pymongo 数据库
import pymongo
client = pymongo.MongoClient(host='localhost',port=27017)
# 指定数据库 douban
db =client.douban
# 指定集合 doubanbooksML
collection = db.doubanbooksML


import requests
from bs4 import BeautifulSoup
import pandas as pd
# print("导入成功！")

header ={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
}
# 将cookies存储到字典的方法
cookies  = 'bid=P_ZKV9BVHfE; __utmc=30149280; ll="118271"; _vwo_uuid_v2=D5F6301CCA0BA1F403310BBDB612A50A8|a7920ac816b0fa2e758cd41c10b386ce; gr_user_id=c45f1875-a6e0-43d9-aa34-cd019cf81e6b; __utmv=30149280.18622; douban-fav-remind=1; viewed="3165271_4254271"; __utmc=81379588; gr_cs1_b61834d4-dee7-400e-b3ef-ba1189b0456b=user_id%3A0; ap_v=0,6.0; __utma=30149280.696154547.1563276061.1583499887.1583829730.30; __utmz=30149280.1583829730.30.17.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt_douban=1; __utma=81379588.1649039511.1582552835.1582552835.1583829730.2; __utmz=81379588.1583829730.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1583829730%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DuNphXXY-esw0TdBmKkUMe2BS2M-TjiIZi-QBZGAcYwXjmUMfOtxJRMnkop0Bperh%26wd%3D%26eqid%3D94ea1a200002da69000000055e6752aa%22%5D; _pk_ses.100001.3ac3=*; dbcl2="186229531:3ufBftA4bfw"; ck=OeSD; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=e3637341-2cf6-460d-836a-b24b088f6d0d; gr_cs1_e3637341-2cf6-460d-836a-b24b088f6d0d=user_id%3A1; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_e3637341-2cf6-460d-836a-b24b088f6d0d=true; push_noty_num=0; push_doumail_num=0; _pk_id.100001.3ac3=527bb4a0a2a1ee2d.1582552835.2.1583829810.1582552835.; __utmb=30149280.4.10.1583829730; __utmb=81379588.4.10.1583829730'
clst = cookies.split(';')
dic_c={}
for i in clst:
    dic_c[i.split('=')[0]]=i.split('=')[1]

# 拼接链接 返回列表
def get_urls(n):
    """
    分页网页URL采集 函数
    n:页数参数
    结果：得到一个分页网页的list
    """
    lst=[]
    for i in range(n):
        # %% 必须是双引号 否则无法生效
        ui='https://book.douban.com/tag/%%E6%%9C%%BA%%E5%%99%%A8%%E5%%AD%%A6%%E4%%B9%%A0?start=%i&type=T'%(i*20)
        lst.append(ui)
    return lst

# 获取HTML 然后匹配信息
def get_soup(url):
    r= requests.get(url,headers=header,cookies=dic_c)

    # 如果编码不正常添加如下代码即可
    # r.encodng = r.apprent_encoding
    # print(r.text)
    from bs4 import BeautifulSoup
    # 搜索匹配信息 方便进行抓取
    soup = BeautifulSoup(r.text,'lxml')
    ul_class = soup.find('ul',class_='subject-list')
    lis= ul_class.find_all('li',class_='subject-item')
    for i in lis:
        info = i.find('div',class_='info')
        h2 = info.find('h2').text.strip().replace('\n','') # 标题
        chubaninfo = info.find('div',class_='pub').text.strip().split('/') # 出版信息
        # 如果有两个作者 删除第2个作者信息
        if len(chubaninfo)>4:
            del chubaninfo[1]
        # 如果有缺失信息 补足4条信息 
        elif len(chubaninfo)<4:
            for i in range(len(chubaninfo),4):
                chubaninfo.append(' ')
        commits = info.find('span',class_='pl').text.strip()# 评论人数
        try:
            documents = info.find('p').text # 简介
        except:
            documents = '无简介'
#         print(h2)
#         print(chubaninfo)
#         print(commits)
#         print(documents)
        # 拼接数据字典
        data ={
            'title':h2,
            'author':chubaninfo[0],
            'Publishinghouse':chubaninfo[1],
            'publishingTime':chubaninfo[2],
            'price':chubaninfo[3],
            'commits':commits,
            'documents':documents
        }
        print(data)
        result = collection.insert_one(data)

if __name__ == '__main__':
    retun_lst = get_urls(20)
#     print(retun_lst)
    for i in retun_lst:
#         print(i)
        get_soup(i)
#         break
    