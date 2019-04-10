import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


class AQI:
    """
    获的样本数据
    """

    def __init__(self):
        self.encoding = None
        self.status = None

    def get_encoding(self, ):
        try:
            res = requests.get('http://datacenter.mee.gov.cn/aqiweb2/')
            res.raise_for_status()
            self.status = '200'
            self.encoding = res.apparent_encoding
            print('获得网页编码方式为 %s' % self.encoding)

        except:
            print('连接出现异常！')

    def process_data(self, sleep_time=3600):
        if self.status:
            res = BeautifulSoup(requests.get('http://datacenter.mee.gov.cn/aqiweb2/').text, 'html.parser')
            items = res.find('ul', class_='list_title').find_all('li')
            time_ = res.find('input').get('value').replace('年', '-').replace('月', '-').replace('日', '-').\
                replace('时', ':00:00')
            header = []
            # 获得li标签下的文本内容
            for i in items:
                header.append(i.get_text())
            # 读取html,返回一个列表形式的dataFrame对象
            """
                data_res:class list
                data:class dataFrame
            """
            data_res = pd.read_html('http://datacenter.mee.gov.cn/aqiweb2/', encoding=self.encoding)
            # 保留实时报
            data = data_res[0]
            data.columns = header
            data['time'] = time
            write_header = None
            if not write_header:
                data.to_csv('data.csv', index=False, mode='a', header=True)
                write_header = 'non None'
            else:
                data.to_csv('data.csv', index=False, mode='a', header=False)
            print('Successful collection data of {} and saved it !'.format(time_))
            time.sleep(sleep_time)


if __name__ == '__main__':
    aqi = AQI()
    aqi.get_encoding()
    aqi.process_data()