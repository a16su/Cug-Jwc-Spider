import xlwt
from prettytable import PrettyTable
import requests
import time
import re
import os


class StuScore:
    def __init__(self, header):
        self.url = 'http://jwgl.cug.edu.cn/jwglxt/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005'
        self.headers = header

    def stu_score(self):
        if os.path.exists('./个人成绩查询结果'):
            pass
        else:
            os.mkdir('./个人成绩查询结果')
        xqmlist = [3, 12, 16]
        xnm = input('请输入要查询的学年:')
        xqm = int(input('请输入要查询的学期:'))
        data = {
            'xnm': xnm[:4],
            'xqm': xqmlist[xqm-1],
            'nd': time.time(),
            'queryModel.showCount': 100,
            'queryModel.sortOrder': 'asc'

        }
        html = requests.post(self.url, data=data, headers=self.headers).json()
        score_datas = html['items']
        totalcount = html['totalResult']
        bt1 = ['学年', '学期', '课程名称', '课程性质', '学分', '成绩', '绩点', '成绩性质', '是否成绩作废', '是否学位课程', '开课部门', '课程类别',
              '任课教师', '学号', '姓名', '性别', '学生类别', '学院', '专业', '年级', '班级']
        excel = xlwt.Workbook()
        sheet = excel.add_sheet('sheet1', cell_overwrite_ok=True)
        self.save2excel(bt1, -1, sheet)
        score_path = './个人成绩查询结果/{}学年第{}学期成绩'.format(xnm, xqm)
        if os.path.exists(score_path):
            pass
        else:
            os.mkdir(score_path)
        with open(score_path+'/{}学年第{}学期成绩详细.txt'.format(xnm, xqm), 'a', encoding='utf-8')as f:
            f.write('\n'+str(xnm) + '学年' + '第'+str(xqm)+'学期成绩')
        for i in range(totalcount):
            a = score_datas[i]
            score_data = [a['xnm'], a['xqmmc'], a['kcmc'], a['kcxzmc'], a['xf'], a['cj'], a['jd'], a['ksxz'],
                          a['cjsfzf'], a['sfxwkc'], a['kkbmmc'], a['kclbmc'], a['jsxm'], a['xh'], a['xm'],
                          a['xb'], a['xslb'], a['jgmc'], a['zymc'], a['njmc'], a['bj']]
            self.save2excel(score_data, i, sheet)

            juti = self.get_specific_score(a['xh_id'], a['jxb_id'], a['xnm'], a['xqm'], a['kcmc'])
            pt = PrettyTable(['成绩分项', '成绩分项比例', '分数'])
            for n in range(0, len(juti), 3):
                bbdata = [juti[n].strip('【】'), juti[n+1].strip('&nbsp;'), juti[n+2].strip('&nbsp;')]
                pt.add_row(bbdata)

            with open(score_path+'./{}学年第{}学期成绩详细.txt'.format(xnm, xqm), 'a', encoding='utf-8') as f:
                f.write('\n'+a['kcmc']+'\n'+str(pt))

        print('查询成功')
        excel.save(score_path+'./{}学年第{}学期成绩信息查询结果.xls'.format(xnm, xqm))

    def get_specific_score(self, xh_id, jxb_id, xnm, xqm, kcmc):
        data = {
            'xh_id': xh_id,
            'jxb_id': jxb_id,
            'xnm': xnm,
            'xqm': xqm,
            'kcmc': kcmc

        }
        url = 'http://jwgl.cug.edu.cn/jwglxt/cjcx/cjcx_cxCjxq.html?time={}&gnmkdm=N305005'.format(int(time.time()))
        new_html = requests.post(url, data=data, headers=self.headers)
        b = re.findall('<td valign="middle">(.*?)</td>', new_html.text, re.S)
        return b

    def save2excel(self, data, row, sheet):
        for i in range(0, len(data)):
            sheet.write(row+1, i, data[i])


if __name__ == '__main__':
    while True:
        header = {
            'Cookie': 'JSESSIONID = 1AB8DF05C6AC733486B291BD94753C6A',
            'Host': 'jwgl.cug.edu.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
        }
        Score = StuScore(header)
        Score.stu_score()



