import xlwt
import time
import os


class KxCdCx:
    def __init__(self, ses):
        self.url = 'http://jwgl.cug.edu.cn/jwglxt/cdjy/cdjy_cxKxcdlb.html?doType=query&gnmkdm=N2155'
        self.ses = ses

    def get_cdxx(self):
        if os.path.exists('./空闲教室查询结果'):
            pass
        else:
            os.mkdir('./空闲教室查询结果')
        data = {
            'fwzt': 'cx',  # ,
            'xqh_id': 1,  # 校区id
            'xnm': 2017,  # 学年
            'xqm': 12,  # 学期
            'cdlb_id': '',  # 场地类别
            'cdejlb_id': '',  # 场地二级类别
            'qszws': '',  #
            'jszws': '',  # 教室座位数
            'cdmc': '',  # 场地名称
            'lh': '',  # 楼号
            'qssd': '',
            'jssd': '',
            'qssj': '',
            'jssj': '',
            'jyfs': 0,
            'cdjylx': '',  # 场地借用类型

            '_search': 'false',
            'nd': time.time(),  # 时间戳
            'queryModel.showCount': 100,  # 每页展示的数量
            'queryModel.currentPage': 1,
            'queryModel.sortName': 'cdbh',  # 要查询的数据库名称
            'queryModel.sortOrder': 'asc',  # 排序顺序
            'time': 1

        }
        # 周次的id构建 比如2,3,4周 则post为 2**1+2**2+2**3，节次的构建同理。星期几的构建搞不出来，所以采用只能查询单天的方式
        zcd = [int(x) for x in input('请输入周次（若多周用‘，’分割）:').split(',')]
        zcd_id = sum([2**(x-1) for x in zcd])
        xqj = input('请输入星期几(目前不能同时查询多天):')
        jcd = [int(x) for x in input('请输入周次（若多周用‘，’分割）:').split(',')]
        jcd_id = sum([2**(x-1) for x in jcd])
        data['zcd'] = zcd_id
        data['xqj'] = xqj
        data['jcd'] = jcd_id
        html = self.ses.post(self.url, data=data)
        a = html.json()
        totalPage = a['totalPage']  # 总共的页数
        totalCount = a['totalCount']  # 总共的数量
        cd_msg = a['items']
        # 打开工作簿
        f = xlwt.Workbook()
        sheet = f.add_sheet('sheet1')
        lb = ['场地编号', '场地名称', '校区', '场地类别', '楼号', '楼层号', '座位数', '考试座位数', '场地借用类型']  # 表头
        for m in range(0, len(lb)):
            sheet.write(0, m, lb[m])
        # 判断页数是否大于1，小于1则场地的数目小于100 可以直接写入
        if totalPage == 1:
            for i in range(0, len(cd_msg)):
                # 用来判断数据是否存在，不存在设置为None
                cd_data = self.cl_cdxx(i, cd_msg)
                self.save2excel(cd_data, i, sheet)
                print('成功保存第1页第{}条信息'.format(i + 1))
            print('查询成功')
            f.save('./空闲教室查询结果/{}周—星期{}—{}节空闲教室查询结果.xls'.format(zcd, xqj, jcd))
        # 大于1页则需要分页写入
        else:
            for i in range(1, totalPage + 1):
                # 分页请求数据
                data['queryModel.currentPage'] = i
                data['time'] = i
                new_html = self.ses.post(self.url, data=data).json()
                new_cd_msg = new_html['items']
                if i == totalPage:
                    # 最后一页的数量为totalCount+100减去页数*100
                    for n in range(0, totalCount + 100 - i * 100):
                        cd_data = self.cl_cdxx(n, new_cd_msg)
                        self.save2excel(cd_data, (totalPage - 1) * 100 + n, sheet)
                        print('成功保存最后一页第{}条信息'.format(n + 1))
                    print('查询成功')
                    f.save('./空闲教室查询结果/{}周—星期{}—{}节空闲教室查询结果.xls'.format(zcd, xqj, jcd))

                else:
                    for n in range(100):
                        cd_data = self.cl_cdxx(n, cd_msg)
                        self.save2excel(cd_data, n + 100 * (i - 1), sheet)
                        print('共{}页,正在保存第{}页第{}条'.format(totalPage, i, n + 1))

    # 用于保存数据
    def save2excel(self, data, row, sheet):

        for i in range(0, len(data)):
            sheet.write(row + 1, i, data[i])

    # 用于判断数据是否存在
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

