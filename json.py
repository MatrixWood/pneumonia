import json
import re
import requests
import datetime

today = datetime.date.today().strftime('%Y%m%d')

def crawl_dxy_data():
    """
    爬取丁香园实时统计数据，保存到data目录下，以当前日期作为文件名，存JSON文件
    """
    response = requests.get('https://ncov.dxy.cn/ncovh5/view/pneumonia')
    print(response.status_code)


    try:
        url_text = response.content.decode()
        #print(url_text)
        url_content = re.search(r'window.getAreaStat = (.*?)}]}catch',
                                url_text, re.S)
        texts = url_content.group()
        content = texts.replace('window.getAreaStat = ', '').replace('}catch', '')
        json_data = json.loads(content)                                         
        with open('data/' + today + '.json', 'w', encoding='UTF-8') as f:
            json.dump(json_data, f, ensure_ascii=False)
    except:
        print('<Response [%s]>' % response.status_code)


def crawl_statistics_data():
    """
    获取各个省份历史统计数据，保存到data目录下，存JSON文件
    """
    with open('data/'+ today + '.json', 'r', encoding='UTF-8') as file:
        json_array = json.loads(file.read())

    statistics_data = {}
    for province in json_array:
        response = requests.get(province['statisticsData'])
        try:
            statistics_data[province['provinceShortName']] = json.loads(response.content.decode())['data']
        except:
            print('<Response [%s]> for url: [%s]' % (response.status_code, province['statisticsData']))

    with open("data/statistics_data.json", "w", encoding='UTF-8') as f:
        json.dump(statistics_data, f, ensure_ascii=False)


if __name__ == '__main__':
    crawl_dxy_data()
    crawl_statistics_data()
