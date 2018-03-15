from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from 空教室查询 import KxCdCx
from 课表查询 import KbCx
from 考试信息查询 import Ksxxcx
import time
import re
'''
此文件为登录并获取cookie用于后续网站访问
'''

class Login:
    def __init__(self):
        pass

    def login_cug(self):
        username = input('请输入你的账号:')
        password = input('请输入你的密码:')
        print('登陆中，请稍等。。。')
        brower = webdriver.Firefox()
        try:
            brower.get('http://sfrz.cug.edu.cn/tpass/login?service=http%3A%2F%2Fxyfw.cug.edu.cn%2Ftp_up%2Fview%3Fm%3Dup')
            inputun = brower.find_element_by_id('un')
            inputun.send_keys(username)
            time.sleep(2)
            inputun = brower.find_element_by_id('pd')
            inputun.send_keys(password)
            inputun.send_keys(Keys.ENTER)
            wait = WebDriverWait(brower, 10)
            wait.until(EC.element_to_be_clickable((By.ID, 'app_a')))
            html = brower.page_source
            appurl = re.findall('appurl="(.*?)"', html, re.S)
            appurl = appurl[0]
            brower.get(appurl)
            cookie = brower.get_cookies()

        finally:
            brower.close()
        cookie = cookie[0]['name'] + '=' + cookie[0]['value']
        return cookie


if __name__ == '__main__':
    Me = Login()
    print('欢迎使用本产品，输入0退出。')
    zong_code = 1
    while input() != '0' and zong_code != 0:
        cookie = Me.login_cug()
        print('登录成功，请开始你的表演！')
        headers = {
            'Cookie': cookie,
            'Host': 'jwgl.cug.edu.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
        }
        ClassScdSearch = KbCx()  # 课表查询
        ClassRoomSearch = KxCdCx()  # 空闲教室查询
        ExamMsgSearch = Ksxxcx()  # 考试信息查询
        quit_code = 1
        while quit_code != 0:
            print('\n'+'*******************************')
            print('1.查询个人课表', '2.查询空闲教室', '3.查询考试信息', '4.退出', sep='\n')
            print('*******************************'+'\n')
            user_input = int(input('请输入:'))
            print('\n')
            if user_input == 1:
                ClassScdSearch.get_grkbxx(headers)
            elif user_input == 2:
                ClassRoomSearch.get_cdxx(headers)
            elif user_input == 3:
                ExamMsgSearch.ksxxcx(headers)
            elif user_input == 4:
                print('欢迎下次使用，再见(*╹▽╹*)')
                quit_code = 0
                zong_code = 0

