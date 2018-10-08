import xlwt
from prettytable import PrettyTable
import requests
import time
import re
import os


class StuScore:
    def __init__(self, ses):
        self.url = 'http://jwgl.cug.edu.cn/jwglxt/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005'
        self.ses = ses

    def stu_score(self):
        # 判断程序所在文件下有无以查询结果命名的文件，没有就创建
        if os.path.exists('./个人成绩查询结果'):
            pass
        else:
            os.mkdir('./个人成绩查询结果')
        # 用来构建学期xqm_id:1-3 2-12 3-16
        xqmlist = [3, 12, 16]
        xnm = input('请输入要查询的学年:')
        # 获取要查询的学年
        xqm = int(input('请输入要查询的学期:'))
        # 要post的数据构建
        data = {
            'xnm': xnm[:4],
            'xqm': xqmlist[xqm - 1],
            'nd': time.time(),
            'queryModel.showCount': 100,
            'queryModel.sortOrder': 'asc'

        }
        html = self.ses.post(self.url, data=data).json()
        score_datas = html['items']  # 获取成绩列表
        totalcount = html['totalResult']  # 总共的数量
        # 构建表头，然后写入excel
        bt1 = ['学年', '学期', '课程名称', '课程性质', '学分', '成绩', '绩点', '成绩性质', '是否成绩作废', '是否学位课程', '开课部门', '课程类别',
               '任课教师', '学号', '姓名', '性别', '学生类别', '学院', '专业', '年级', '班级']
        # 打开一个工作簿
        excel = xlwt.Workbook()
        sheet = excel.add_sheet('sheet1', cell_overwrite_ok=True)
        self.save2excel(bt1, -1, sheet)
        score_path = './个人成绩查询结果/{}学年第{}学期成绩'.format(xnm, xqm)  # 成绩文件保存地址
        if os.path.exists(score_path):
            pass
        else:
            os.mkdir(score_path)
        # 构建详细成绩的描述
        with open(score_path + '/{}学年第{}学期成绩详细.txt'.format(xnm, xqm), 'a', encoding='utf-8')as f:
            f.write('\n' + str(xnm) + '学年' + '第' + str(xqm) + '学期成绩')
        for i in range(totalcount):
            # 开始保存成绩
            a = score_datas[i]
            score_data = [a['xnm'], a['xqmmc'], a['kcmc'], a['kcxzmc'], a['xf'], a['cj'], a['jd'], a['ksxz'],
                          a['cjsfzf'], a['sfxwkc'], a['kkbmmc'], a['kclbmc'], a['jsxm'], a['xh'], a['xm'],
                          a['xb'], a['xslb'], a['jgmc'], a['zymc'], a['njmc'], a['bj']]
            self.save2excel(score_data, i, sheet)
            # 获取每一门课程的详细分数
            juti = self.get_specific_score(a['xh_id'], a['jxb_id'], a['xnm'], a['xqm'], a['kcmc'])
            pt = PrettyTable(['成绩分项', '成绩分项比例', '分数'])
            for n in range(0, len(juti), 3):
                # 清洗数据并用PrettyTable格式化
                bbdata = [juti[n].strip('【】'), juti[n + 1].strip('&nbsp;'), juti[n + 2].strip('&nbsp;')]
                pt.add_row(bbdata)
            # 将格式化的数据保存到txt文件中
            with open(score_path + '/{}学年第{}学期成绩详细.txt'.format(xnm, xqm), 'a', encoding='utf-8') as f:
                f.write('\n' + a['kcmc'] + '\n' + str(pt))

        print('查询成功')
        # 上面打开的工作簿保存，并用学年加学期命名
        excel.save(score_path + '/{}学年第{}学期成绩信息查询结果.xls'.format(xnm, xqm))

    # 该函数用来获取课程的详细分数，接受参数为 学号，教学班id，学年，学期，课程名称
    def get_specific_score(self, xh_id, jxb_id, xnm, xqm, kcmc):
        data = {
            'xh_id': xh_id,
            'jxb_id': jxb_id,
            'xnm': xnm,
            'xqm': xqm,
            'kcmc': kcmc

        }
        url = 'http://jwgl.cug.edu.cn/jwglxt/cjcx/cjcx_cxCjxq.html?time={}&gnmkdm=N305005'.format(int(time.time()))
        new_html = requests.post(url, data=data, headers=self.ses)
        # 用于匹配成绩文本，每3个结果为一组
        b = re.findall('<td valign="middle">(.*?)</td>', new_html.text, re.S)
        return b

    # 该函数用于将数据保存到excel中，接受参数为 数据，起始行，控制写入的对象名
    def save2excel(self, data, row, sheet):
        for i in range(0, len(data)):
            sheet.write(row + 1, i, data[i])

