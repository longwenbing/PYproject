import time
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import re

from storage_data import storage_infos, connect_db


class Egg_Web_Spider():
    def __init__(self):
        self.cap = {
            "platformName": "Android",
            "platformVersion": "5",
            "deviceName": "127.0.0.1:62001",
            "appPackage": "app.eggworld.cn.android",
            "appActivity": ".MainActivity",
            "noRest": True
        }
        self.beginurl = 'http://localhost:4723/wd/hub'
        # 账号
        self.account_number = '13184840089'
        # 密码
        self.pwd = '970505'
        # 数据
        self.data = []

    def get_logined_driver(self):
        driver = webdriver.Remote(self.beginurl, self.cap)
        # login_button "//android.widget.Button[@text='登录']"
        try:
            if WebDriverWait(driver, 10, 0.2).until(
                    lambda x: x.find_element_by_xpath("//android.widget.Button[@text='登录']")):
                driver.find_element_by_xpath("//android.widget.Button[@text='登录']").click()
                # account_number //android.widget.ListView/android.view.View[1]/android.widget.EditText[1]
                WebDriverWait(driver, 10, 0.2).until(
                    lambda x: x.find_element_by_xpath(
                        '//android.widget.ListView/android.view.View[1]/android.widget.EditText[1]')).send_keys(
                    self.account_number)
                # pwd
                WebDriverWait(driver, 10, 0.2).until(
                    lambda x: x.find_element_by_xpath(
                        "//android.widget.ListView/android.view.View[2]/android.widget.EditText[1]")).send_keys(
                    self.pwd)
                # login_button
                WebDriverWait(driver, 10, 0.2).until(
                    lambda x: x.find_element_by_xpath("//android.widget.Button[@text='登  录']")).click()
                print("登录成功")
                driver.find_element_by_xpath('')
        except:
            print("已经登录")
            pass
        return driver

    # 获取页面的大小
    def get_screen_size(self, driver):
        x = driver.get_window_size()['width']
        y = driver.get_window_size()['height']
        return (x, y)

    # 滑动页面获取更多
    # 滑动操作
    def slide_screen(self, driver):
        size = self.get_screen_size(driver)
        # slide_screen start
        x1 = int(size[0] * 0.5)
        y1 = int(size[1] * 0.90)
        # slide_screen end
        y2 = int(size[1] * 0.10)
        driver.swipe(x1, y1, x1, y2)

    # 小滑动
    def slide_litter_screen(self, driver):
        size = self.get_screen_size(driver)
        # slide_screen start
        x1 = int(size[0] * 0.5)
        y1 = int(size[1] * 0.5)
        # slide_screen end
        y2 = int(size[1] * 0.5 - 180)
        driver.swipe(x1, y1, x1, y2)
        # 对齐

    def slide_alignment(self, driver):
        size = self.get_screen_size(driver)
        # slide_screen start
        x1 = int(size[0] * 0.5)
        y1 = int(size[1] * 0.5)
        # slide_screen end
        y2 = int(size[1] * 0.5 - 45)
        driver.swipe(x1, y1, x1, y2)

    def get_max_enterprise_number(self, driver):
        # 重试三次查找
        for i in range(3):
            try:
                if WebDriverWait(driver, 20, 0.2).until(
                        lambda x: x.find_element_by_xpath(
                            "//android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.webkit.WebView[1]/android.webkit.WebView[1]/android.view.View[1]/android.view.View[1]/android.view.View[4]")):
                    str_numbers = driver.find_element_by_xpath(
                        "//android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.webkit.WebView[1]/android.webkit.WebView[1]/android.view.View[1]/android.view.View[1]/android.view.View[4]").text
                    return int(re.findall(r'([1-9]\d*)', str_numbers)[0])
            except:
                print("没找到企业，重试")
        return None

    def handle_certified_info(self, driver):
        try:
            certified_info = driver.find_element_by_xpath(
                "//android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.webkit.WebView[1]/android.webkit.WebView[1]/android.view.View[1]/android.view.View[2]/android.view.View[1]/android.view.View[1]/android.view.View[3]").text.strip()
            certified_person = driver.find_element_by_xpath(
                "//android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.webkit.WebView[1]/android.webkit.WebView[1]/android.view.View[1]/android.view.View[2]/android.view.View[1]/android.view.View[1]/android.view.View[4]/android.view.View[2]").text.strip()
            certified_time = driver.find_element_by_xpath(
                "//android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.webkit.WebView[1]/android.webkit.WebView[1]/android.view.View[1]/android.view.View[2]/android.view.View[1]/android.view.View[1]/android.view.View[4]/android.view.View[3]").text.strip().split("：")[1]
        except:
            certified_info = ''
            certified_person = ''
            certified_time = ''
        return (certified_info, certified_person, certified_time)

    def check_message(self, mes):
        if mes:
            return mes.text
        else:
            return ''

    def get_base_info(self, driver):
        # 负责人
        leader = self.check_message(WebDriverWait(driver, 10, 0.2).until(lambda x: x.find_element_by_xpath(
            "//android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.webkit.WebView[1]/android.webkit.WebView[1]/android.view.View[1]/android.view.View[2]/android.view.View[1]/android.view.View[1]/android.view.View[6]/android.view.View[2]"))).strip()
        if "未授权" in leader:
            leader=''
        print(leader)
        # 电话
        # 点击达上限
        # 电话
        try:
            WebDriverWait(driver, 10, 0.2).until(lambda x: x.find_element_by_xpath(
                "//android.widget.Button[@text='查看联系电话']")).click()
            phone = self.check_message(driver.find_element_by_xpath(
                "//android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.webkit.WebView[1]/android.webkit.WebView[1]/android.view.View[1]/android.view.View[2]/android.view.View[1]/android.view.View[1]/android.view.View[7]/android.view.View[2]"))
        except:
            phone=''
        time.sleep(0.2)
        print(phone)
        # 养殖鸡种
        try:
            egg_species = self.check_message(
                driver.find_element_by_xpath("//android.view.View/android.view.View[8]/android.view.View[2]"))
        except:
            egg_species=''
        print(egg_species)
        # 地址
        try:
            address = self.check_message(driver.find_element_by_xpath(
                "//android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.webkit.WebView[1]/android.webkit.WebView[1]/android.view.View[1]/android.view.View[2]/android.view.View[1]/android.view.View[1]/android.view.View[9]/android.view.View[2]"))
        except:
            address=''
        print(address)
        # 规模
        try:
            scale_temp = self.check_message(driver.find_element_by_xpath(
                "//android.view.View/android.view.View[2]/android.view.View[1]/android.view.View[1]/android.widget.ListView[1]/android.view.View[1]/android.view.View[1]"))
            scale=re.findall(r'(\d+)',scale_temp)[0]
            if len(scale)>=4:
                scale=int(scale)/10000.0
        except:
            scale=''
        print(scale)
        # 鸡舍数量
        try:
            number_of_chicken_coops_temp = self.check_message(driver.find_element_by_xpath(
                "//android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.webkit.WebView[1]/android.webkit.WebView[1]/android.view.View[1]/android.view.View[2]/android.view.View[1]/android.view.View[1]/android.widget.ListView[1]/android.view.View[2]/android.view.View[1]"))
            number_of_chicken_coops=re.findall(r'(\d+)',number_of_chicken_coops_temp)[0]
        except:
            number_of_chicken_coops=''
        print(number_of_chicken_coops)
        # 经营时间
        try:
            operating_hours = self.check_message(driver.find_element_by_xpath(
                "//android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.webkit.WebView[1]/android.webkit.WebView[1]/android.view.View[1]/android.view.View[2]/android.view.View[1]/android.view.View[1]/android.widget.ListView[1]/android.view.View[3]/android.view.View[1]"))
        except:
            operating_hours=''
        print(operating_hours)
        return (leader, phone, egg_species, address, scale, number_of_chicken_coops, operating_hours)


    #验证信息存在？




    # 用料信息
    def get_forage_info(self, driver):
        # 用料信息
        try:
            WebDriverWait(driver, 10, 0.2).until(lambda x: x.find_element_by_xpath(
                "//android.view.View/android.widget.ListView[2]/android.view.View[2]/android.view.View[2]"))
        except:
            WebDriverWait(driver, 10, 0.2).until(lambda x: x.find_element_by_xpath(
                "//android.view.View/android.widget.ListView[2]/android.view.View[2]/android.view.View[2]")).click()
        time.sleep(0.2)
        try:
            feed_type = self.check_message(driver.find_element_by_xpath(
                "//android.view.View/android.view.View[1]/android.view.View[2]/android.view.View[1]/android.view.View[2]"))
        except:
            feed_type=''
        print(feed_type)
        time.sleep(0.2)
        try:
            feed_brand = self.check_message(driver.find_element_by_xpath(
                "//android.view.View/android.view.View[1]/android.view.View[2]/android.view.View[2]/android.view.View[2]"))
        except:
            feed_brand=''
        print(feed_brand)
        time.sleep(0.2)
        # //android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.webkit.WebView[1]/android.webkit.WebView[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]
        # driver.find_element_by_xpath(
        # "//android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.webkit.WebView[1]/android.webkit.WebView[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]").click()
        time.sleep(0.5)
        return (feed_type, feed_brand)

    # 蛋品渠道
    def get_egg_canal(self, driver):

        # 蛋品渠道
        try:
            WebDriverWait(driver, 10, 0.2).until(lambda x: x.find_element_by_xpath(
                "//android.view.View/android.widget.ListView[2]/android.view.View[3]/android.view.View[2]")).click()
        # except:
        # driver.find_element_by_xpath("//android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.webkit.WebView[1]/android.webkit.WebView[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]").click()
            time.sleep(0.2)
            egg_canal = self.check_message(driver.find_element_by_xpath(
                "//android.view.View/android.widget.ListView[2]/android.view.View[3]/android.view.View[2]"))
        except:
            egg_canal=''
        print(egg_canal)

        return egg_canal

    # 库存
    def get_stock_on_hand(self, driver):
        try:
            WebDriverWait(driver, 10, 0.2).until(lambda x: x.find_element_by_xpath(
                "//android.view.View/android.widget.ListView[2]/android.view.View[1]/android.view.View[2]")).click()
            time.sleep(0.5)
            stock_on_hand = self.check_message(driver.find_element_by_xpath(
                "//android.view.View/android.widget.ListView[2]/android.view.View[1]/android.view.View[2]"))
            hand_ = re.findall('(\d+)', stock_on_hand)[0]
            if len(hand_)>=4:
                stock_on_hand=int(hand_)/10000.0
        except:
            stock_on_hand=''
        print(stock_on_hand)
        return stock_on_hand

    #淘汰鸡
    def get_elimination_info(self,driver):
        try:
            WebDriverWait(driver, 10, 0.2).until(lambda x: x.find_element_by_xpath(
                "//android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.webkit.WebView[1]/android.webkit.WebView[1]/android.view.View[1]/android.view.View[2]/android.view.View[1]/android.view.View[1]/android.widget.ListView[2]/android.view.View[6]/android.view.View[2]")).click()
            time.sleep(0.3)
            elimination = self.check_message(WebDriverWait(driver, 10, 0.2).until(lambda x: x.find_element_by_xpath(
                "//android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.webkit.WebView[1]/android.webkit.WebView[1]/android.view.View[1]/android.view.View[2]/android.view.View[1]/android.view.View[1]/android.widget.ListView[2]/android.view.View[6]/android.view.View[2]")))
        except:
            elimination=''
        print(elimination)
        return elimination

    def get_cultivation_info(self, driver):
        try:
            WebDriverWait(driver, 10, 0.2).until(lambda x: x.find_element_by_xpath(
                "//android.widget.ListView/android.view.View[5]/android.view.View[2]")).click()
            time.sleep(0.2)
            coop = WebDriverWait(driver, 10, 0.2).until(lambda x: x.find_element_by_xpath(
                "//android.view.View/android.view.View[2]/android.view.View[1]/android.view.View[4]/android.view.View[1]/android.view.View[2]")).text
        except:
            coop=''
        print(coop)
        try:
            brand = self.check_message(driver.find_element_by_xpath(
                "//android.view.View/android.view.View[2]/android.view.View[1]/android.view.View[4]/android.view.View[2]/android.view.View[2]"))
            print(brand)
            time.sleep(0.2)
            brand_name = self.check_message(driver.find_element_by_xpath(
                "//android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.webkit.WebView[1]/android.webkit.WebView[1]/android.view.View[1]/android.view.View[2]/android.view.View[1]/android.view.View[4]/android.view.View[3]/android.view.View[2]"))
            print(brand_name)
            time.sleep(0.2)
        except:
            print('没有产品名')
            try:
                brand = self.check_message(driver.find_element_by_xpath(
                    "//android.view.View/android.view.View[2]/android.view.View[1]/android.view.View[4]/android.view.View[2]/android.view.View[2]"))
                print(brand)
                brand_name = ''
            except:
                brand=''
                brand_name=''
        print(brand_name)
        try:
            driver.find_element_by_xpath(
                "//android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.webkit.WebView[1]/android.webkit.WebView[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]").click()
        except:
            pass
        return (coop, brand, brand_name)

    # 滑动至底部
    def roll_base(self, driver):
        self.slide_screen(driver)
        time.sleep(0.1)
        self.slide_screen(driver)
        time.sleep(0.1)
        self.slide_screen(driver)
        time.sleep(0.1)
        self.slide_screen(driver)
        time.sleep(0.1)
        self.slide_screen(driver)
        time.sleep(0.1)
        self.slide_screen(driver)
        time.sleep(0.1)
        self.slide_screen(driver)
        time.sleep(0.1)

    def get_column_info(self, text):
        cn = text.split("供应品种")[0].strip()
        other=text.split("供应品种")[1].strip()
        eggs = other.split("建设规模")[0].replace(" ", '，').strip()
        other2= other.split("建设规模")[1].strip()
        sclae =other2.split("所在地区")[0].strip()
        other3 = other2.split("所在地区")[1].strip()
        province = other3.split(' ')[0].strip()
        try:
            e =other3.split(' ')[1].strip()
        except:
            e=''
        return (cn, eggs, sclae, province, e)

    # 保存数据
    def save_data(self, ):
        storage_infos(self.save_path, self.data)
        self.data.clear()

    # //android.view.View[@resource-id='content']/android.view.View[2]/android.widget.ListView[1]/android.view.View[4]
    # 进入鸡蛋黄页的 操作链
    def enter_egg_yellow_pages_actions(self, driver):
        # 进入黄页
        WebDriverWait(driver, 20, 0.5).until(
            lambda x: x.find_element_by_xpath(
                "//android.view.View[@text='蛋鸡黄页']")).click()
        time.sleep(1.5)
        numbers = self.get_max_enterprise_number(driver)
        print(numbers)
        if numbers != None:
            #保存到第几个就滑动几次
            for i in range(22, numbers + 1):
                for x in range(1, i):
                    self.slide_litter_screen(driver)
                    time.sleep(0.25)
                time.sleep(1)
                try:
                    text = driver.find_element_by_xpath(
                        "//android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.webkit.WebView[1]/android.webkit.WebView[1]/android.view.View[1]/android.view.View[1]/android.view.View[5]/android.view.View[%d]/android.view.View[1]" % i).text
                    WebDriverWait(driver, 5, 0.2).until(lambda x: x.find_element_by_xpath(
                        "//android.view.View[@resource-id='content']/android.view.View[5]/android.view.View[%d]" % i)).click()
                except:
                    self.slide_litter_screen(driver)
                    text = driver.find_element_by_xpath(
                        "//android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.webkit.WebView[1]/android.webkit.WebView[1]/android.view.View[1]/android.view.View[1]/android.view.View[5]/android.view.View[%d]/android.view.View[1]" % i).text
                    WebDriverWait(driver, 5, 0.2).until(lambda x: x.find_element_by_xpath(
                        "//android.view.View[@resource-id='content']/android.view.View[5]/android.view.View[%d]" % i)).click()
                time.sleep(2.5)
                print(text)
                column_info = self.get_column_info(text)
                # 企业名
                cn = column_info[0]
                # 鸡蛋品种
                egg_species = column_info[1]
                # 养殖规模
                scale = column_info[2]
                # 所在地 省份
                province = column_info[3]
                # 蛋E网认证
                e = column_info[4]
                print(column_info)

                # 基本信息
                base_info = self.get_base_info(driver)
                leader = base_info[0]
                phone = base_info[1]
                chicken_species = base_info[2]
                address = base_info[3]
                scale = base_info[4]
                number_of_chicken_coops = base_info[5]
                operating_hours = base_info[6]
                # 关于认证信息
                info = self.handle_certified_info(driver)
                # 认证信息
                certified_info = info[0]
                certified_person = info[1]
                certified_time = info[2]
                print(info)
                WebDriverWait(driver, 10, 0.2).until(
                    lambda x: x.find_element_by_xpath("//android.widget.Button[@text='打电话']"))
                # 划至底部
                self.roll_base(driver)
                # 生产数据
                #  库存
                stock_on_hand = self.get_stock_on_hand(driver)
                # 用料信息
                forage_info = self.get_forage_info(driver)
                feed_type = forage_info[0]
                feed_brand = forage_info[1]
                # 鸡蛋渠道
                egg_canal = self.get_egg_canal(driver)

                # 淘汰鸡渠道
                elimination = self.get_elimination_info(driver)

                # 养殖信息
                cultivation_info = self.get_cultivation_info(driver)
                coop = cultivation_info[0]
                brand = cultivation_info[1]
                brand_name = cultivation_info[2]
                time.sleep(0.3)
                one = (
                    province, cn, leader, phone, address, chicken_species, egg_species, scale, number_of_chicken_coops,operating_hours,
                    certified_info, certified_person, certified_time, stock_on_hand, feed_type, feed_brand, egg_canal,elimination,
                    coop, brand,brand_name, e)
                # self.data.append(one)
                # # 12薯条数据存一次
                # if i % 12 == 0 or i == numbers:
                #     self.save_data()
                connect_db(one)
                while True:
                    try:
                        driver.find_element_by_xpath(
                            "//android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.webkit.WebView[1]/android.webkit.WebView[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]").click()
                        break
                    except:
                        print("找不到返回键")
                        pass
                time.sleep(1)
                # # 点击去掉底端小广告
                while True:
                    try:
                        WebDriverWait(driver, 10, 0.2).until(
                            lambda x: x.find_element_by_xpath("//android.view.View/android.widget.Button[2]")).click()
                        break
                    except:
                        print("找不到广告键")
                time.sleep(1)
                self.slide_alignment(driver)

        else:
            print("没有企业信息！")

    def run(self):
        driver = self.get_logined_driver()
        time.sleep(2)
        self.enter_egg_yellow_pages_actions(driver)


if __name__ == '__main__':
    a = Egg_Web_Spider()
    a.run()
