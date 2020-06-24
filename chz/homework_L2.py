

from bs4 import BeautifulSoup
import pandas as pd
# 请求URL
#url = 'http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-0-0-0-0-0-1.shtml'
# 得到页面的内容


def get_page_content(url):
    headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    html=requests.get(url,headers=headers,timeout=10)
    content = html.text
    
    # 通过content创建BeautifulSoup对象
    soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
    return soup


#分析当前页面投诉
def analysis(soup):
    temp = soup.find('div',class_="tslb_b")
    #创建DataFrame
    df = pd.DataFrame(columns=['id','brand','car_model','type','desc','problem','datetime','status'])
    tr_list = temp.find_all('tr')
    
    for tr in tr_list:
        #提取汽车投诉信息
        temp1 = {}
        td_list = tr.find_all('td')
        if len(td_list) >0:
            #解析各个字段的内容
            id, brand, car_model, type, desc, problem, datetime, status = td_list[0].text, td_list[1].text, td_list[2].text, td_list[3].text, td_list[4].text, td_list[5].text, td_list[6].text, td_list[7].text
            #放到DataFrame中
            temp1['id'], temp1['brand'], temp1['car_model'], temp1['type'], temp1['desc'], temp1['problem'], temp1['datetime'], temp1['status']= id, brand, car_model, type, desc, problem, datetime, status
            df = df.append(temp1,ignore_index=True)
    return df

#df1 = analysis(soup)
#print(df1)
results= pd.DataFrame(columns=['id','brand','car_model','type','desc','problem','datetime','status'])
page_num = 20
base_url ='http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-0-0-0-0-0-'
for i in range(page_num):
    request_url=base_url + str(i+1) +'.shtml'
    soup= get_page_content(request_url)
    df = analysis(soup)
    results=results.append(df)
print(results)
results.to_csv('result.csv')

#输出第一个 title 标签
print(soup.title)
#输出第一个 title 标签的标签名称
print(soup.title.name)
#输出第一个 title 标签的包含内容
print(soup.title.string)
