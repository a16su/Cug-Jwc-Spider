from 空教室查询 import KxCdCx
from 课表查询 import KbCx
from 考试信息查询 import Ksxxcx
from 个人成绩查询 import StuScore
import re
import execjs
import requests


def login(username, passwd):
    url1 = 'http://sfrz.cug.edu.cn/tpass/login?service=http%3A%2F%2Fxyfw.cug.edu.cn%2Ftp_up%2Fview%3Fm%3Dup#act=portal/viewhome'
    url2 = 'http://sfrz.cug.edu.cn/tpass/login?service=http%3A%2F%2Fxyfw.cug.edu.cn%2Ftp_up%2F'
    header1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    }
    header2 = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
        'Referer': 'http://sfrz.cug.edu.cn/tpass/login?service=http%3A%2F%2Fxyfw.cug.edu.cn%2Ftp_up%2Fview%3Fm%3Dup',
        'Origin': 'http://sfrz.cug.edu.cn',
        'Host': 'sfrz.cug.edu.cn',
    }
    ses = requests.session()
    res = ses.get(url=url1, headers=header1)
    res.encoding = 'utf-8'
    text = res.text
    parrtern1 = re.compile(r'<input type="hidden" id="lt" name="lt" value="(.*?)" />')
    parrtern2 = re.compile(r'<input type="hidden" name="execution" value="(.*?)" />')

    lt = re.search(parrtern1, text).group(1)
    execution = re.search(parrtern2, text).group(1)
    with open('dec.js', 'r') as f:
        keys = execjs.compile(f.read()).call('strEnc', username + passwd + lt, '1', '2', '3')
    data = {
        'rsa': keys,
        'ul': str(len(username)),
        'pl': str(len(passwd)),
        'lt': lt,
        'execution': execution,
        '_eventId': 'submit',
    }

    r = ses.post(url2, headers=header2, data=data)
    r = ses.get('http://202.114.207.137:80/ssoserver/login?ywxt=jw')
    return ses


if __name__ == '__main__':
    print('欢迎使用本产品，输入0退出。')
    # 用来控制退出的数字
    zong_code = 1
    while input() != '0' and zong_code != 0:
        username = input('用户名: ')
        passwd = input('密码: ')
        ses = login(username, passwd)
        print('登录成功，请开始你的表演！')
        ClassScdSearch = KbCx(ses)  # 课表查询
        ClassRoomSearch = KxCdCx(ses)  # 空闲教室查询
        ExamMsgSearch = Ksxxcx(ses)  # 考试信息查询
        StuScore = StuScore(ses)  # 个人成绩查询
        quit_code = 1
        while quit_code != 0:
            print('\n' + '*' * 20)
            print('1.查询个人课表', '2.查询空闲教室', '3.查询考试信息', '4.查询个人成绩', '5.退出', sep='\n')
            print('*' * 20 + '\n')
            user_input = int(input('请输入:'))
            print('\n')
            if user_input == 1:
                ClassScdSearch.get_grkbxx()
            elif user_input == 2:
                ClassRoomSearch.get_cdxx()
            elif user_input == 3:
                ExamMsgSearch.ksxxcx()
            elif user_input == 4:
                StuScore.stu_score()
            elif user_input == 5:
                print('欢迎下次使用，再见(*╹▽╹*)')
                quit_code = 0
                zong_code = 0

