import xlwt
import requests
import time
import os


class KxCdCx:
    def __init__(self):
        self.url = 'http://jwgl.cug.edu.cn/jwglxt/cdjy/cdjy_cxKxcdlb.html?doType=query&gnmkdm=N2155'

    def get_cdxx(self, headers):
        if os.path.exists('./空闲教室查询结果'):
            pass
        else:
            os.mkdir('./空闲教室查询结果')
        data = {
            'fwzt': 'cx',  # ,
            'xqh_id': 1,  # 校区id
            'xnm': 2017,  # 学年
            'xqm': 12,  # 学期
            'cdlb_id': '',
            'cdejlb_id': '',
            'qszws': '',
            'jszws': '',
            'cdmc': '',
            'lh': '',
            'qssd': '',
            'jssd': '',
            'qssj': '',
            'jssj': '',
            'jyfs': 0,
            'cdjylx': '',

            '_search': 'false',
            'nd': time.time(),
            'queryModel.showCount': 100,
            'queryModel.currentPage': 1,
            'queryModel.sortName': 'cdbh',
            'queryModel.sortOrder': 'asc',
            'time': 1

            }
        zcd = list(map((lambda x: int(x)), (list(input('请输入周次（若多周用‘，’分割）:').split(',')[:]))))
        zcd_id = sum(list(map((lambda x: 2 ** (int(x) - 1)), list(zcd))))
        xqj = input('请输入星期几:')
        jcd = list(map((lambda x: int(x)), (list(input('请输入节次（若多节用‘，’分割）:').split(',')[:]))))
        jcd_id = sum(list(map((lambda x: 2 ** (int(x) - 1)), list(jcd))))
        data['zcd'] = zcd_id
        data['xqj'] = xqj
        data['jcd'] = jcd_id
        new_html = requests.post(self.url, data=data, headers=headers)
        a = new_html.json()
        totalPage = a['totalPage']
        totalCount = a['totalCount']
        cd_msg = a['items']
        f = xlwt.Workbook()
        sheet = f.add_sheet('sheet1')
        lb = ['场地编号', '场地名称', '校区', '场地类别', '楼号', '楼层号', '座位数', '考试座位数', '场地借用类型']
        for a in range(0, len(lb)):
            sheet.write(0, a, lb[a])
        if totalPage == 1:
            for i in range(0, len(cd_msg)):
                cd_data = self.cl_cdxx(i, cd_msg)
                self.save2excel(cd_data, i, sheet)
                print('成功保存第1页第{}条信息'.format(i+1))
            print('查询成功')
            f.save('./空闲教室查询结果/{}周—星期{}—{}节空闲教室查询结果.xls'.format(zcd, xqj, jcd))
        else:
            for i in range(1, totalPage+1):
                data['queryModel.currentPage'] = i
                data['time'] = i
                new_html = requests.post(self.url, data=data, headers=headers).json()
                new_cd_msg = new_html['items']
                if i == totalPage:
                    for n in range(0, totalCount + 100 - i * 100):
                        cd_data = self.cl_cdxx(n, new_cd_msg)
                        self.save2excel(cd_data, (totalPage-1)*100+n, sheet)
                        print('成功保存最后一页第{}条信息'.format(n+1))
                    print('查询成功')
                    f.save('./空闲教室查询结果/{}周—星期{}—{}节空闲教室查询结果.xls'.format(zcd, xqj, jcd))

                else:
                    for n in range(100):
                        cd_data = self.cl_cdxx(n, cd_msg)
                        self.save2excel(cd_data, n + 100*(i-1), sheet)
                        print('共{}页,正在保存第{}页第{}条'.format(totalPage, i, n+1))

    def save2excel(self, data, row, sheet):

        for i in range(0, len(data)):
            sheet.write(row+1, i, data[i])

    def cl_cdxx(self, num, seg):
        cd_data = [seg[num]['cdbh'], seg[num]['cdmc'], seg[num]['xqmc'], seg[num]['cdlbmc'], seg[num]['jxlmc'],
                   seg[num]['zws']]
        for item in ['lch', 'kszws1', 'cdjylx']:
            if item not in seg[num]:
                seg[num][item] = None
        cd_data.insert(5, seg[num]['lch'])
        cd_data.insert(8, seg[num]['kszws1'])
        cd_data.insert(9, seg[num]['cdjylx'])

        return cd_data


if __name__ == '__main__':
    header = {
                'Cookie': 'JSESSIONID = 1AB8DF05C6AC733486B291BD94753C6A',
                'Host': 'jwgl.cug.edu.cn',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
            }
    while True:
        a = KxCdCx()
        a.get_cdxx(header)
