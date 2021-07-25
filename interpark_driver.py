from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.alert import Alert
import re
from datetime import datetime
import time

            
class InterparkMacro:
    def __init__(self):
        self.driver = self.selenium_init()

    def selenium_init(self):
        driver = webdriver.Chrome('chromedriver.exe')
        driver.implicitly_wait(5)
        return driver

    def login(self, id, pwd, musical_id):
        interpark_login_url = 'https://ticket.interpark.com/Gate/TPLogin.asp?CPage=B&MN=Y&tid1=main_gnb&tid2=right_top&tid3=login&tid4=login&GPage=https%3A%2F%2Ftickets.interpark.com%2Fgoods%2F' + musical_id
        self.driver.get(interpark_login_url)

        self.driver.switch_to.frame(self.driver.find_element(By.XPATH, "//div[@class='leftLoginBox']/iframe[@title='login']"))
        self.driver.find_element_by_name('userId').send_keys(id)
        self.driver.find_element_by_name('userPwd').send_keys(pwd)
        self.driver.find_element_by_id('btn_login').click()

    # 해당 태그가 있는지 검사
    def check_exists_by_element(self, by, name):
        elements = self.driver.find_elements(by, name)
        if not elements:
            return False
        else:
            return True

    # 예매안내가 팝업이 뜨면 닫기. ( ticketingInfo_check : True, False )
    # 뮤지컬 예약 전 팝업 
    def close_tickting_info_popup(self):
        ticketinginfo_check = self.check_exists_by_element(By.XPATH, "//div[@class='popupWrap']/div[@class='popupFooter']/button[@class='popupCloseBtn is-bottomBtn']")
        if ticketinginfo_check:
            popup_close_btn = self.driver.find_element(By.XPATH, "//button[@class='popupCloseBtn is-bottomBtn']")
            if popup_close_btn.text != "":
                popup_close_btn.click()

    # 예매안내가 팝업이 뜨면 닫기. ( ticketingInfo_check : True, False )
    # 뮤지컬 예약 후 팝업
    def close_ticketing_check_popup(self):
        self.driver.switch_to.default_content()
        ticketingInfo_check = self.check_exists_by_element(By.XPATH, "//div[@class='layerWrap']/div[@class='titleArea']/a[@class='closeBtn']")
        if ticketingInfo_check:
            self.driver.find_element(By.XPATH, "//div[@class='layerWrap']/div[@class='titleArea']/a[@class='closeBtn']").click()
        
    # 예매하기 버튼 클릭
    def click_book_btn(self):
        self.driver.find_element(By.XPATH, "//div[@class='sideBtnWrap']/a[@class='sideBtn is-primary']").click()

    # 예매하기 눌러서 새창이 뜨면 포커스를 새창으로 변경
    def switching_focus(self):
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get_window_position(self.driver.window_handles[1])

    def wait_safety_booking(self):
        self.driver.switch_to.default_content()
        iframe_element = WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='divBookSeat']/iframe[@id='ifrmSeat']")))
        self.driver.switch_to.frame(iframe_element)
        
        recaptcha_input = self.driver.find_elements(By.XPATH, "//div[@class='validationTxt']")
        recaptcha_input[0].click()
        
        video_element = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//div[@id='divRecaptcha' and @style='display: none;']")))
        print("[INFO] 안심예매 RECAPTCHA 완료!")
        
    def click_want_date(self, wantYear, wantMonth, wantDay, wantTime):
        year_month = self.driver.find_element(By.XPATH, "//ul/li[@data-view='month current']").text.split('.')
        year = year_month[0].strip()
        month = year_month[1].strip()
        
        year_diff = wantYear - int(year)
        month_diff = wantMonth - int(month)
        
        total_month_diff = year_diff * 12 + month_diff
        
        # 원하는 월이 될 때까지 이동
        for i in range(abs(total_month_diff)):
            if total_month_diff > 0:
                next_month = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//ul/li[@data-view='month next']")))
                self.driver.execute_script("arguments[0].click();", next_month)
                print(next_month.text)
            else:
                prev_month = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//ul/li[@data-view='month prev']")))
                self.driver.execute_script("arguments[0].click();", prev_month)
        
        # 원하는 일자 클릭
        days = self.driver.find_elements(By.XPATH, "//div[@class='datepicker-panel']/ul[@data-view='days']/li")
        for day in days:
                if int(day.text) == wantDay:	# wantDate : 예매 원하는 일
                    day.click()
                    break

            
        # 원하는 시간 클릭
        show_times = self.driver.find_elements(By.XPATH, "//ul[@class='timeTableList']/li")
        for show_time in show_times:
            if show_time.text.split(' ')[1] == wantTime:
                show_time.click()
                break
        
    

    # 원하는 자리를 빠르게 클릭해주는 함수! (원하는 자리에 맞춰 코드를 수정해주면 된다)
    def click_want_seat(self):
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.driver.find_element(By.XPATH, "//div[@id='divBookSeat']/iframe[@id='ifrmSeat']"))
        self.driver.switch_to.frame(self.driver.find_element(By.XPATH, "//div[@class='seatL']/iframe[@id='ifrmSeatDetail']"))
        stySeats = self.driver.find_elements(By.XPATH, "//img[@class='stySeat']")
        for seat in stySeats:
            seatInfo = seat.get_attribute("onclick").split(',')

            floor = int(re.findall('\d+', seatInfo[2])[0])
            column = int(re.findall('\d+', seatInfo[3])[0])
            row = int(re.findall('\d+', seatInfo[4])[0])

            if floor == 1 and column <= 25 and 9 <= row <= 26:
                print(seat.text)
                seat.click()
                break
        
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.driver.find_element(By.XPATH, "//div[@id='divBookSeat']/iframe[@id='ifrmSeat']"))
        nextBtn = self.driver.find_element(By.XPATH, "//div[@class='btnWrap']/a")
        print(nextBtn.text)
        nextBtn.click()
        
        try:
            WebDriverWait(self.driver, 1).until(EC.alert_is_present(),
                                        'Timed out waiting for PA creation ' +
                                        'confirmation popup to appear.')

            alert = self.driver.switch_to.alert
            if alert.text.strip() == '좌석을 선택하세요.':
                print("[Info] 좌선 미선택! 재시도 합니다")
            alert.accept()
            self.click_want_seat()
        
        except TimeoutException:
            print("no alert")
            

    # 티켓팅 
    def click_ticket_price(self):
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.driver.find_element(By.XPATH, "//div[@class='contL']/iframe[@id='ifrmBookStep']"))
        ticketNums = self.driver.find_elements(By.XPATH, "//tr[@id='PriceRow001']/td[@class='taL']/select/option")
        for ticketNum in ticketNums:
            num = int(re.findall('\d+', ticketNum.text)[0])
            if num == 1:
                ticketNum.click()
                break

        self.driver.switch_to.default_content()
        self.driver.find_element(By.XPATH, "//p[@id='SmallNextBtn']").click()


    def insert_oder_info(self, birthDay, phoneNumber):
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.driver.find_element(By.XPATH, "//div[@class='contL']/iframe[@id='ifrmBookStep']"))
        self.driver.find_element_by_id('YYMMDD').clear()
        self.driver.find_element_by_id('YYMMDD').send_keys(birthDay)
        self.driver.find_element_by_id('HpNo1').clear()
        self.driver.find_element_by_id('HpNo1').send_keys(phoneNumber[0])
        self.driver.find_element_by_id('HpNo2').clear()
        self.driver.find_element_by_id('HpNo2').send_keys(phoneNumber[1])
        self.driver.find_element_by_id('HpNo3').clear()
        self.driver.find_element_by_id('HpNo3').send_keys(phoneNumber[2])

        self.driver.switch_to.default_content()
        self.driver.find_element(By.XPATH, "//p[@id='SmallNextBtn']").click()

    def click_payment_method(self, wantBank):
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.driver.find_element(By.XPATH, "//div[@class='contL']/iframe[@id='ifrmBookStep']"))
        
        # 무통장입금 클릭(매칭 id로 검색)
        # 유연하게 진행하기 위해선 결제방식에 따른 id값을 미리 가지고 있을 필요있음
        self.driver.find_element(By.XPATH, "//tr[@id='Payment_22004']/td/input").click()

        # 입금 은행 - 농협 클릭
        banks = self.driver.find_elements(By.XPATH, "//select[@id='BankCode']/option")
        for bank in banks:
            if bank.text == wantBank:
                bank.click()
                break

        self.driver.switch_to.default_content()
        self.driver.find_element(By.XPATH, "//p[@id='SmallNextBtn']").click()

    def agree_payment(self):
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.driver.find_element(By.XPATH, "//div[@class='contL']/iframe[@id='ifrmBookStep']"))
        self.driver.find_element_by_id('checkAll').click()

        self.driver.switch_to.default_content()
        self.driver.find_element(By.XPATH, "//p[@id='LargeNextBtn']").click()