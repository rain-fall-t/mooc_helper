from selenium import webdriver
from selenium.webdriver import ChromeOptions
import time
import datetime
from selenium.webdriver import ActionChains
import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget,QMessageBox
import sys

class window(QWidget):
    username = ''
    password = ''
    class_num = ''
    button_name = ''
    def __init__(self):
        super().__init__()
        self.resize(300, 300)
        from PyQt5.uic import loadUi  # 需要导入的模块
        loadUi("window.ui", self)  # 加载UI文件
        #self.pushButton.clicked.connect(self.AA)  # 调用UI文件中的控件
        self.OK_button.clicked.connect(self.create_files)
        self.save_data_box.clicked.connect(self.save_data)
        self.auto_input_box.clicked.connect(self.auto_input)
        self.emailButton.toggled.connect(lambda: self.get_button_name(self.emailButton))
        self.phoneButton.toggled.connect(lambda: self.get_button_name(self.phoneButton))
        self.iclassButton.toggled.connect(lambda: self.get_button_name(self.iclassButton))

    def save_data(self):
        username_text = self.USERNAME.text()
        password_text = self.PASSWORD.text()
        if username_text =='' or password_text =='':
            QMessageBox.warning(self,'ERROR','请输入账号密码',QMessageBox.Ok,QMessageBox.Ok)
            self.save_data_box.setChecked(False)
        else:
            file = open('accounts.txt', 'w')
            file.write(username_text + ' ' + password_text)
            file.close()

    def auto_input(self):
        try:
            file = open('accounts.txt', 'r')
            account = file.readline().split(' ')
            self.USERNAME.setText(account[0])
            self.PASSWORD.setText(account[1])
        except:
            QMessageBox.warning(self,'ERROR','账户信息不存在，请输入账户并保存',QMessageBox.Ok,QMessageBox.Ok)
            self.auto_input_box.setChecked(False)


    def get_file_name(self):
        now_1 = datetime.datetime.now()
        now_1.strftime('%X')
        now_1_str = str(now_1)
        list_1 = now_1_str.split(' ')
        date_1 = list_1[0]
        list_2 = list_1[1].split(':')
        date_2 = list_2[0]
        now = date_1 + '_' + date_2 + '_'
        return now

    def get_file_path(self):
        # 建立文件夹

        if not os.path.exists(root_path):
            os.mkdir(root_path)
        unmanaged_work_path = root_path + '/unmanaged_work'
        if not os.path.exists(unmanaged_work_path):
            os.mkdir(unmanaged_work_path)
        finished_work_path = root_path + '/finished_work'
        if not os.path.exists(finished_work_path):
            os.mkdir(finished_work_path)
        return root_path, unmanaged_work_path, finished_work_path
    def login_page(self):
        # 无头浏览器
        options = ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 避免检测
        driver = webdriver.Chrome(executable_path='chromedriver.exe')
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                      get: () => undefined
                    })
                  """
        })
        driver.get(
            url='https://www.icourse163.org/member/login.htm?returnUrl=aHR0cHM6Ly93d3cuaWNvdXJzZTE2My5vcmcvaW5kZXguaHRt#/webLoginIndex')
        time.sleep(1)
        # driver.maximize_window()
        # 点击“注册/登陆”
        login_post_button = driver.find_element_by_xpath(
            '/html/body/div[4]/div[1]/div/div/div/div[7]/div[2]/div/div/div/a')
        login_post_button.click()
        # 点击“其他登陆方式”
        other_login_button = driver.find_element_by_xpath(
            '/html/body/div[4]/div[2]/div/div/div/div/div/div/div/div/div[2]/span')
        # 需要使用actions方法
        actions = ActionChains(driver)
        actions.move_to_element(other_login_button).perform()
        actions.release()
        time.sleep(2)
        other_login_button.click()
        # 等待响应
        time.sleep(2)
        #跳转框架
        current_window = driver.current_window_handle
        return current_window, driver

    def get_button_name(self,Button):
        if Button.isChecked()==True:
            self.button_name = Button.text()

    def login(self):

        current_window, driver = self.login_page()
        if self.button_name == '邮箱登陆':
            # 跳转到邮箱登陆框架
            switch = driver.find_element_by_xpath(
                '/html/body/div[4]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div/div[1]/div[2]/div[1]/iframe')
            driver.switch_to.frame(switch)
            #键入账号、密码
            phone_num = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/form/div/div[1]/div[2]/input')
            phone_num.send_keys(self.username)  # 输入账号
            phone_password = driver.find_element_by_xpath(
                '/html/body/div[2]/div[2]/div[2]/form/div/div[3]/div[2]/input[2]')
            phone_password.send_keys(self.password)  # 输入密码
            # 点击登陆
            login_button = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/form/div/div[8]/a')
            login_button.click()

        if self.button_name == '手机号登陆':
            # 点击手机号登陆
            phone_button = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div/div[1]/div[1]/ul/li[2]')
            phone_button.click()
            # 跳转到手机号登陆框架
            switch = driver.find_element_by_xpath(
                '/html/body/div[4]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div/div[1]/div[2]/div[2]/div/iframe')
            driver.switch_to.frame(switch)
            # 键入账号、密码
            phone_num = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/form/div/div[2]/div[2]/input')
            phone_num.send_keys(self.username)  # 输入账号
            phone_password = driver.find_element_by_xpath(
                '/html/body/div[2]/div[2]/div[2]/form/div/div[4]/div[2]/input[2]')
            phone_password.send_keys(self.password)  # 输入密码
            # 点击登陆
            login_button = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/form/div/div[6]/a')
            login_button.click()

        if self.button_name == '爱课程账号登陆':
            # 点击爱课程登陆
            phone_button = driver.find_element_by_xpath(
                '/html/body/div[4]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div/div[1]/div[1]/ul/li[3]')
            phone_button.click()
            # 跳转到爱课程登陆框架
            switch = driver.find_element_by_xpath(
                '/html/body/div[4]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div/div[1]/div[2]/div[2]/div/iframe')
            driver.switch_to.frame(switch)
            # 键入账号、密码
            phone_num = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div/div[1]/div[2]/div[3]/div[2]/label/input')
            phone_num.send_keys(self.username)  # 输入账号
            phone_password = driver.find_element_by_xpath(
                '/html/body/div[4]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div/div[1]/div[2]/div[3]/div[3]/label/input')
            phone_password.send_keys(self.password)  # 输入密码
            # 点击登陆
            login_button = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div/div[1]/div[2]/div[3]/div[4]/span')
            login_button.click()


        try:
            test_button = driver.find_element_by_xpath(
                '/html/body/div[4]/div[1]/div/div/div/div/div[7]/div[3]/div/div/a/span')
        except:
            # 遇到滑块验证，手动完成
            # 系统停止
            time.sleep(6)

        login_button = driver.find_element_by_xpath(
            '/html/body/div[4]/div[1]/div/div/div/div/div[7]/div[3]/div/div/a')  # /html/body/div[4]/div[1]/div/div/div/div/div[7]/div[3]/div/div/a
        login_button.click()
        # 进入页面，等待页面响应
        time.sleep(3)
        # 可能遇到广告，关闭广告
        try:
            close_button = driver.find_element_by_xpath('/html/body/div[11]/div/div[1]/a')
            close_button.click()
            time.sleep(2)
        except:
            pass
        # 获得当前页面，用于后期debug
        current_window = driver.current_window_handle
        return current_window, driver

    def get_courses(self, unmanaged_work_path, current_window, driver):
        # 获得参数中指定的课程
        fp_name_list = []
        class_name_list = []
        for course_sort in range(self.class_num):
            path = '/html/body/div[4]/div[2]/div[3]/div/div[1]/div[3]/div/div[2]/div/div/div[2]/div[1]/div[2]/div/div[1]/div[' + str(
                course_sort + 1) + ']/div[1]/a'
            power = driver.find_element_by_xpath(path)
            power.click()
            time.sleep(2)
            # 此处会遇到新页面，进行窗口跳转
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(5)
            # 进入测验与作业
            test_and_homework = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div[4]/div[1]/div/ul/li[4]/a')
            test_and_homework.click()
            time.sleep(5)
            # 获得作业数据
            div_list = driver.find_elements_by_xpath(
                '/html/body/div[4]/div[2]/div[4]/div[2]/div/div[1]/div/div[2]/div[@class="m-chapterQuizHwItem"]')

            class_name = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div[3]/div/div[1]/div/a/h4').text
            fp_name = unmanaged_work_path + '\\' + self.get_file_name() + class_name + '.txt'
            content_name = self.get_file_name() + class_name
            class_name_list.append(class_name)
            fp_name_list.append(fp_name)
            with open(fp_name, 'w', encoding='utf-8') as fp:
                for div in div_list:
                    work = {}
                    try:
                        work['chapter_name'] = div.find_element_by_xpath('./h3').text
                        work['chapter_test'] = div.find_element_by_xpath('./div[1]/div[1]/h4').text
                        work['chapter_deadline'] = div.find_element_by_xpath(
                            './div[1]/div[1]/div[@class="j-submitTime score f-fl"]').text
                        # 检查测验是否完成
                        mark = div.find_element_by_xpath('.//div[@class="j-validScore score f-fr"]').text
                        if mark:
                            work['chapter_process'] = True
                        else:
                            work['chapter_process'] = False

                    except:
                        pass
                    try:
                        work['chapter_homework'] = div.find_element_by_xpath('./div[2]/div[1]/h4').text
                        work['chapter_homework_deadline'] = div.find_element_by_xpath(
                            './div[2]/div[1]/div[@class="j-submitTime score f-fl"]').text

                        fp.write(str(work) + '\n')
                    except:
                        fp.write(str(work) + '\n')
            driver.close()
            driver.switch_to.window(current_window)

        time.sleep(5)
        return fp_name_list, class_name_list, fp_name

    def display(self, work_dict):
        # self.result_text.end(False)
        for key, value in work_dict.items():
            self.result_text.appendPlainText(key + ':' + value)

    def exit(self):
        pass

    def manage_work(self, dead_time, class_name, finished_work_path, unmanaged_work_path):
        now = datetime.datetime.now()
        time_zero = datetime.timedelta(seconds=1)
        fp_finished_name = finished_work_path + '\\' + self.get_file_name() + class_name + '.txt'
        with open(fp_finished_name, 'w', encoding='gbk', errors='ignore') as all:
            with open(unmanaged_work_path, 'r', encoding='utf-8') as fp:
                for fl in fp.readlines():

                    try:
                        deadline_message = eval(fl)
                        print(deadline_message)
                        test_dead = datetime.datetime.strptime(deadline_message['chapter_deadline'][5:],
                                                               '%Y/%m/%d %H:%M')
                        homework_dead = datetime.datetime.strptime(
                            deadline_message['chapter_homework_deadline'][5:],
                            '%Y/%m/%d %H:%M')
                        if ((test_dead - now) < dead_time or (homework_dead - now) < dead_time) and not deadline_message['chapter_process']:
                            try:
                                self.display(deadline_message)
                            except:
                                pass
                            all.write(deadline_message['chapter_test'] + '\n')
                            all.write(deadline_message['chapter_deadline'] + '\n')
                            all.write(deadline_message['chapter_homework'] + '\n')
                            all.write(deadline_message['chapter_homework_deadline'] + '\n')
                    except:
                         pass
        return fp_finished_name

    def create_file(self, class_name, path):
        new_file_path = root_path + self.get_file_name() + '.txt'
        with open(path, 'r') as fq:
            temp = fq.readlines()
        with open(new_file_path, 'a', encoding='utf-8') as fp:
            fp.write(class_name + '\n')
            for _ in temp:
                fp.write(_)

    def create_files(self):
        self.username = self.USERNAME.text()
        self.password = self.PASSWORD.text()
        self.class_num = self.class_num.value()
        #QMessageBox.information(self,'waiting','正在查询，请稍候......',QMessageBox.Yes,QMessageBox.Yes)
        # 设置新文件保存路径
        #print(self.username)
        root_path, unmanaged_work_path, finished_work_path = self.get_file_path()
        # 设置文件检索时间
        deadline = datetime.timedelta(days=self.deadline_text.value())
        # 进行登陆
        current_window, driver = self.login()
        fp_name_list, class_name_list, fp_name = self.get_courses(unmanaged_work_path, current_window, driver)
        for fp_name, class_name in zip(fp_name_list, class_name_list):
            # self.result_text.end(False)

            self.result_text.appendPlainText(class_name + ':\n')
            finished_path = self.manage_work(deadline, class_name, finished_work_path, fp_name)
            self.create_file(class_name, finished_path)
        # print('最终文件保存于:' + root_path)
        self.result_text.appendPlainText("\n仅检测测验是否完成，请将作业和测验一起完成")
        driver.quit()
        QMessageBox.information(self,'Finished', '查询成功！', QMessageBox.Yes)

if __name__=="__main__":
    root_path = os.getcwd()+'\\work_files'
    if not os.path.exists(root_path):
        os.mkdir(root_path)
    app = QtWidgets.QApplication(sys.argv)
    w = window()
    w.show()
    QMessageBox.information(w,'welcome', '欢迎使用！', QMessageBox.Yes)
    sys.exit(app.exec_())