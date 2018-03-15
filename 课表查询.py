import requests

class KbCx:
    def __init__(self):
        self.url = 'http://jwgl.cug.edu.cn/jwglxt/kbcx/xskbcx_cxXsKb.html?gnmkdm=N2151'

    def get_grkbxx(self, headers):
        xnm = input('请输入要查询的学年(格式:2017-2018):')
        xqm = input('请输入要查询的学期(格式:2):')
        data = self.get_cxdata(xnm, xqm)
        html = requests.post(self.url, headers=headers, data=data).json()
        kblists = html['kbList']  # 课程列表
        sjlists = html['sjkList']  # 实践课列表
        xsxm = html['xsxx']['XM']
        print('\n'+'{}学年第{}学期 {}的个人课表'.format(xnm, xqm, xsxm)+'\n')
        print('课程列表')
        # 课程列表
        for i in range(len(kblists)):
            kbxx = ['上课时间:' + kblists[i]['zcd'] + ' ' + ' 的 '.join((kblists[i]['xqjmc'], kblists[i]['jc'])) + ' 老师:'
                    + kblists[i]['xm']+' 课程名称:' + '《' + kblists[i]['kcmc'] + '》' + ' 上课地点:' + kblists[i]['cdmc']]
            print(kbxx[0])
        # 实践课列表
        print('\n' + '实践课程列表')
        for n in range(len(sjlists)):
            sjkbxx = ['实习时间'+sjlists[n]['qsz']+'-'+sjlists[n]['zzz']+'周' + ' 实习课名称:'+'《'+sjlists[n]['kcmc'] + '》'
                      + ' 指导老师:'+sjlists[n]['xm']]
            print(sjkbxx[0])

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

