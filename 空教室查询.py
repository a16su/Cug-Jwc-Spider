from xlrd import open_workbook
from xlutils.copy import copy
import requests
import time


class KxCdCx:
    def __init__(self):
        self.url = 'http://jwgl.cug.edu.cn/jwglxt/cdjy/cdjy_cxKxcdlb.html?doType=query&gnmkdm=N2155'

    def get_cdxx(self, headers):

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
            'zcd': sum(list(map((lambda x: 2**(int(x)-1)), list(input('请输入周次（若多周用‘，’分割）:').split(',')[:])))),
            'xqj': input('请输入星期几:'),
            'jcd': sum(list(map((lambda x: 2**(int(x)-1)), list(input('请输入节次（若多节用‘，’分割）:').split(',')[:])))),
            '_search': 'false',
            'nd': time.time(),
            'queryModel.showCount': 100,
            'queryModel.currentPage': 1,
            'queryModel.sortName': 'cdbh',
            'queryModel.sortOrder': 'asc',
            'time': 1

            }
        new_html = requests.post(self.url, data=data, headers=headers)
        a = new_html.json()
        totalPage = a['totalPage']
        totalCount = a['totalCount']
        cd_msg = a['items']
        if totalPage == 1:
            for i in range(0, len(cd_msg)):
                cd_data = self.cl_cdxx(i, cd_msg)
                self.save2excel(cd_data, i)
                print('成功保存第1页第{}条信息'.format(i+1))
            print('查询成功')
        else:
            for i in range(1, totalPage+1):
                data['queryModel.currentPage'] = i
                data['time'] = i
                new_html = requests.post(self.url, data=data, headers=headers).json()
                new_cd_msg = new_html['items']
                if i == totalPage:
                    for n in range(0, totalCount + 100 - i * 100):
                        cd_data = self.cl_cdxx(n, new_cd_msg)
                        self.save2excel(cd_data, (totalPage-1)*100+n)
                        print('成功保存最后一页第{}条信息'.format(n+1))
                    print('查询成功')

                else:
                    for n in range(100):
                        cd_data = self.cl_cdxx(n, cd_msg)
                        self.save2excel(cd_data, n + 100*(i-1))
                        print('成功保存第{}页第{}条'.format(i, n+1))

    def save2excel(self, data, row):
        rb = open_workbook('./空闲教室信息.xls')
        rs = rb.sheet_by_index(0)
        wb = copy(rb)
        ws = wb.get_sheet(0)
        lb = ['场地编号', '场地名称', '校区', '场地类别', '楼号', '楼层号', '座位数', '考试座位数', '场地借用类型']
        for a in range(0, len(lb)):
            ws.write(0, a, lb[a])
        for i in range(0, len(data)):
            ws.write(row+1, i, data[i])
        wb.save('./空闲教室信息.xls')

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

