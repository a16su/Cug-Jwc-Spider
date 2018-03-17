from 课表查询 import KbCx
import xlwt
import requests
import os


class Ksxxcx:

    def __init__(self):
        # url记得改
        #self.username = username
        self.url = 'http://jwgl.cug.edu.cn/jwglxt/kwgl/kscx_cxXsksxxIndex.html?doType=query&gnmkdm=N358105&su='

    def ksxxcx(self, headers):
        if os.path.exists('./考试信息查询结果'):
            pass
        else:
            os.mkdir('./考试信息查询结果')
        print('目前官网只能查看当前学年的考试信息！')
        xnm = input('请输入要查询的学年(格式:2017-2018):')
        xqm = input('请输入要查询的学期(格式:2):')
        data = data1.get_cxdata(xnm, xqm)
        data['queryModel.showCount'] = 30
        html = requests.post(self.url, headers=headers, data=data)
        f = xlwt.Workbook()
        sheet = f.add_sheet('sheet1')
        bt = ['学年', '学期', '学号', '姓名', '性别', '班级', '课程代码', '课程名称', '重修标记', '自修标记', '考试时间', '考试地点', '考试校区', '考试座位号', '学院',
              '专业']
        for a in range(0, len(bt)):
            sheet.write(0, a, bt[a])
        if html.json()['totalCount'] != 0:
            totalcount = html.json()['totalCount']
            ksxx_lists = html.json()['items']
            for i in range(totalcount):
                xymc = ksxx_lists[i]['jgmc']  # 学院名称
                kcmc = ksxx_lists[i]['kcmc']  # 考试名称
                cdxqmc = ksxx_lists[i]['cdxqmc']  # 校区名称
                xh = ksxx_lists[i]['xh']  # 学号
                xm = ksxx_lists[i]['xm']  # 姓名
                xb = ksxx_lists[i]['xb']  # 性别
                bj = ksxx_lists[i]['bj']  # 班级
                kch = ksxx_lists[i]['kch']  # 课程代码
                cxbj = ksxx_lists[i]['cxbj']  # 重修标记
                zxbj = ksxx_lists[i]['zxbj']  # 自修标记
                kssj = ksxx_lists[i]['kssj']  # 考试时间
                cdmc = ksxx_lists[i]['cdmc']  # 考试地点
                zwh = ksxx_lists[i]['zwh']  # 座位号
                zymc = ksxx_lists[i]['zymc']  # 专业名称
                ks_data = [xnm, xqm, xh, xm, xb, bj, kch, kcmc, cxbj, zxbj, kssj, cdmc, cdxqmc, zwh, xymc, zymc]
                self.save2excel(ks_data, i, sheet)
                print('共{}条,成功保存第{}条'.format(totalcount, i))
            f.save('./考试信息查询结果/{}学年第{}学期考试信息查询结果.xls'.format(xnm, xqm))
            print('查询成功')
        else:
            print('没有您所查询的信息')

    def save2excel(self, data, row, sheet):

        for i in range(0, len(data)):
            sheet.write(row + 1, i, data[i])

data1 = KbCx()
if __name__ == '__main__':
    header = {
        'Cookie': 'JSESSIONID = 1AB8DF05C6AC733486B291BD94753C6A',
        'Host': 'jwgl.cug.edu.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
    }

    while True:
        exam_seg = Ksxxcx()
        exam_seg.ksxxcx(header)
