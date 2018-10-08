from prettytable import PrettyTable
import os


class KbCx:
    def __init__(self, ses):
        self.url = 'http://jwgl.cug.edu.cn/jwglxt/kbcx/xskbcx_cxXsKb.html?gnmkdm=N2151'
        self.ses = ses

    def get_grkbxx(self):
        if os.path.exists('./学生个人课表'):
            pass
        else:
            os.mkdir('./学生个人课表')
        xnm = input('请输入要查询的学年(格式:2017-2018):')
        xqm = input('请输入要查询的学期(格式:2):')
        data = self.get_cxdata(xnm, xqm)
        html = self.ses.post(self.url, data=data).json()
        kblists = html['kbList']  # 课程列表
        sjlists = html['sjkList']  # 实践课列表
        xsxm = html['xsxx']['XM']

        pt1 = PrettyTable(['星期', '节次', '周次', '课程名称', '任课老师', '上课地点'])
        for i in range(len(kblists)):
            pt1.add_row([kblists[i]['xqjmc'], kblists[i]['jc'], kblists[i]['zcd'], kblists[i]['kcmc'], kblists[i]['xm'],
                         kblists[i]['cdmc']])
        with open('./学生个人课表/{}学年第{}学期学生个人课表.txt'.format(xnm, xqm), 'a', encoding='utf-8') as f:
            f.write('平时课程表')
            f.write('\n' + str(pt1))

        pt2 = PrettyTable(['实习时间', '实习课名称', '指导老师'])
        for n in range(len(sjlists)):
            pt2.add_row([sjlists[n]['qsz'] + '-' + sjlists[n]['zzz'] + '周', sjlists[n]['kcmc'], sjlists[n]['xm']])
        with open('./学生个人课表/{}学年第{}学期学生个人课表.txt'.format(xnm, xqm), 'a', encoding='utf-8') as f:
            f.write('\n' * 2 + '实习课程表')
            f.write('\n' + str(pt2))
        print('查询成功')

    def get_cxdata(self, xnm, xqm):

        xq = {
            '1': 3,
            '2': 12,
            '3': 16
        }
        data = {
            'xnm': xnm[0:4],
            'xqm': xq[xqm]
        }
        return data

