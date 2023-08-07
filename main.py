from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import random
import subprocess
import time
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
import random
import time
from datetime import datetime, timedelta
import pyperclip

def is_within_last_week(date_string):
    # Convert the input date string to a datetime object
    input_date = datetime.strptime(date_string, "%Y-%m-%d")
    # Get the current date
    current_date = datetime.now()
    # Calculate the date one week ago from the current date
    one_week_ago = current_date + timedelta(weeks=4)
    # Check if the input date is within the last week
    return current_date <= input_date <= one_week_ago

def chromeStart():
    try:
        # 크롬드라이버 옵션 설정
        options = Options()
          
        with open("./data/chrome.txt", "r+",encoding='utf-8') as chrome_dir:
          chrome = chrome_dir.readlines()
          
        # with open("./data/number.txt", "r+",encoding='utf-8') as number_dir:
        #   number = number_dir.readlines()
        
        
        # userCookieDir = os.path.abspath(f"./cookie/{number[0]}")
        # if os.path.exists(userCookieDir) == False:
        #     os.mkdir(userCookieDir)    
        userCookieDir = os.path.abspath(f"./cookie")
        if os.path.exists(userCookieDir) == False:
            os.mkdir(userCookieDir)
            
        if(chrome == ''):
          print("./data/chrome.txt 에 크롬의 위치를 입력 해주세요.")
          
        # if(number == ''):
        #   print("./data/number.txt 에 숫자를 입력 해주세요.")
          
        chrome_cmd = '\"'+chrome[0]+'\" --remote-debugging-port=9222 --user-data-dir=\"'+str(userCookieDir)+'\"  --user-agent=\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36\"'
        #chrome_cmd = '\"'+chrome[0]+'\" --user-data-dir="'+str(userCookieDir)+'" --disable-gpu --disable-popup-blocking --disable-dev-shm-usage --disable-plugins --disable-background-networking'
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        #options.add_experimental_option("debuggerAddress", "127.0.0.1:922"+str(number[0]))
        subprocess.Popen(chrome_cmd, shell=True)
        driver = webdriver.Chrome(options=options)
        return driver
    except Exception as e:
        print(e)
        input("아무키나 누르세요... ")
        
def htmlLoadingCheck(driver:webdriver, xpath):
    while 1:
        try:
            driver.execute_script("document.evaluate('"+xpath+"', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();")
            return
        except:
            time.sleep(1)
            try:
                driver.execute_script("document.evaluate('//*[@id=\"lastName\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();")    
                return 1
            except:
                print()
def copyPaste(xpath ,string, driver : webdriver):
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
    try:
        element = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].value = '';", element)
    except:
        print()
    element.click()
    pyperclip.copy(string)
    element.send_keys(Keys.CONTROL, 'v')
    time.sleep(1)
    
def start():
  #
  # 상품 정보 입력
  #
  while True:
    goodUrl = input("구매할 상품 번호 : ")
    if goodUrl:
          print("주소 : ",goodUrl)
          break
  while True:
      size = input("구매할 사이즈(미입력시 랜덤 선택) : ")
      # 입력값이 비어있거나 숫자로 이루어져 있는지 확인
      if size == '' or size.isnumeric():
          break
      else:
          print("Invalid input. Please enter a number or leave it blank.")
  while True:
      option = input("구매할 옵션 숫자 : ")
      # 입력값이 비어있거나 숫자로 이루어져 있는지 확인
      if option == '' or size.isnumeric():
          break
      else:
          print("Invalid input. Please enter a number or leave it blank.")
  
  print(" // 로그인 진행")      
  driver = chromeStart()
  print(" // 로그인 진행")
  #
  # 접속
  #

  with open("./data/account.txt", "r+") as account_file:
      account = account_file.readlines()
      account_file.seek(0)  # 파일 포인터 위치를 파일의 처음으로 이동
  
  id = account[0].split("/pw:")[0]
  pw = account[0].split("/pw:")[1]
  
  print(id + " // 로그인 진행")
  driver.get("https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/")

  copyPaste('//*[@id="id"]',id,driver)
  copyPaste('//*[@id="pw"]',pw,driver)
  # element = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '//*[@id="id"]')))
  # for c in id.strip():
  #   wait_time = random.uniform(0.01, 0.1)
  #   time.sleep(wait_time)
  #   element.send_keys(c)
    
  # element = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '//*[@id="pw"]')))
  # for c in pw.strip():
  #   wait_time = random.uniform(0.01, 0.1)
  #   time.sleep(wait_time)
  #   element.send_keys(c)
  
  element = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="log.login"]')))
  element.click()
  
  time.sleep(3)
  #https://m.pay.naver.com/o/products/510440774/8946855153/purchase?from=https://m.pay.naver.com/
  
  if(driver.current_url == "https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/"):
    print(id + " // 로그인 문제 발생 실행 종료")
    return
  else:
    print(id + " // 로그인 성공")
    
  #
  # 상품 접속 로직
  #
  
  goodUrl = "https://m.pay.naver.com/o/products/510440774/" + goodUrl + "/purchase?from=https://m.pay.naver.com/"
  print(id + " // 상품 페이지 이동")
  while 1:
    try:
      driver.get(goodUrl)
      WebDriverWait(driver, 1).until(EC.alert_is_present())
      alert = driver.switch_to.alert
      print("Alert Text:", alert.text)
      alert.accept()
      time.sleep(3)
    except Exception as e:
      print(id + " // 정상 접속")
  
  
    
    
  try:
    option_element = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="default_top"]/div[3]/button')))
    option_element.click()
  except Exception:
    print("로그인 확인..")


  # 로그인이 되길 기다려줘야하는데....
  #상품 주소일때 로그인 값이 없다면 그때 작동하도록
  while 1:
    if(driver.current_url in goodUrl):
      try : 
          element = driver.find_element(By.XPATH, '//*[@id="default_top"]/div[3]/div[1]/a')
          if (element):
              #로그인되어있음
              break
      except Exception:
          print()
      time.sleep(1)
  print("로그인 확인..")
  print("품절 체크")  
  while 1:
    if(driver.current_url in goodUrl):
      try:
        # 해당 요소의 텍스트 가져오기
        element = driver.find_element(By.XPATH, "//*[contains(text(), '품절 또는 판매가 중지된 상품입니다.')]")
        driver.refresh()
        time.sleep(3)
      except:
        break
  print("판매 예정 체크")  
  while 1:
    if(driver.current_url in goodUrl):
      try:
        # 해당 요소의 텍스트 가져오기
        element = driver.find_element(By.XPATH, "//*[contains(text(), '판매 예정')]")
        #element = driver.find_element(By.XPATH, '//*[@id="buy_option_area"]/div[9]/div[1]/a')
        # '품절' 또는 '판매가 중지' 문구가 포함되어 있는지 확인
        driver.refresh()
        time.sleep(3)
      except:
        break

  try:
    if(size != ''):
      option_value_to_select = size
      option_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//option[@value='{option_value_to_select}']")))
      option_element.click()
    else:
      # 옵션 선택 드롭다운을 찾음
      option_dropdown = driver.find_element(By.XPATH, "//select[@id='option1']")
      # '옵션 선택'을 제외한 옵션들을 찾아서 리스트에 저장
      available_options = option_dropdown.find_elements(By.XPATH, "./option[not(contains(text(), '옵션 선택'))]")
      # 재입고와 관련된 옵션을 제거
      available_options = [option for option in available_options if "재입고" not in option.text]
      # 랜덤으로 옵션 선택
      selected_option = random.choice(available_options)
      selected_option.click()


      # # 옵션 리스트 가져오기
      # options_list = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//select[@id='option1']")))
      # print(options_list)
      # # "재입고 알림 받기"가 없는 옵션들만 필터링
      # available_options = [option for option in options_list if "재입고 알림 받기" not in option.get_attribute("data-txt")]
      # if available_options:
      #   # 랜덤으로 하나의 옵션 선택
      #   selected_option = random.choice(available_options)
      #   option_value = selected_option.get_attribute("value")
      #   selected_option.click()
      # else:
      #   print("모든 옵션이 품절 상태입니다.")
  except Exception as e:
    print("옵션창을 찾을 수 없습니다.")

  try:
      buy_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '바로구매')]")))
      #buy_button.click()
          # Click the element using JavaScript
      driver.execute_script("arguments[0].click();", buy_button)
      try:
        # 얼럿이 표시될 때까지 대기 (10초로 설정)
        WebDriverWait(driver, 0.1).until(EC.alert_is_present())
        # 얼럿 객체 가져오기
        alert = driver.switch_to.alert
        # 얼럿 텍스트 출력 (선택사항)
        print("Alert Text:", alert.text)
        # 얼럿 확인 버튼 클릭 (선택사항)
        alert.accept()
        # 옵션 선택 드롭다운을 찾음
        option_dropdown = driver.find_element(By.XPATH, "//select[@id='option1']")
        # '옵션 선택'을 제외한 옵션들을 찾아서 리스트에 저장
        available_options = option_dropdown.find_elements(By.XPATH, "./option[not(contains(text(), '옵션 선택'))]")
        # 재입고와 관련된 옵션을 제거
        available_options = [option for option in available_options if "재입고" not in option.text]
        # 랜덤으로 옵션 선택
        selected_option = random.choice(available_options)
        selected_option.click()
        buy_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '바로구매')]")))
        driver.execute_script("arguments[0].click();", buy_button)
        #buy_button.click()
      except Exception as e:
          # 얼럿이 표시되지 않은 경우 예외 처리
          print()
  except Exception as e:
      print("바로구매 버튼을 클릭하는데 실패했습니다.")
      buy_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="buy_option_area"]/div[7]/div[1]/a')))
      buy_button.click()
      print(str(e))


  while 1:
    try:
      # html 로딩 대기
      goods = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btn_pay"]')))
      if(goods):
        break
    except:
      time.sleep(1)
  
  radio_button = driver.find_element(By.XPATH,'//*[@id="payment_btn0"]')
    # Click the radio button using JavaScript
  driver.execute_script("arguments[0].click();", radio_button)
    
  
  option_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="cardSwiper"]/div[2]')))
  option_element.click()
  time.sleep(1)
  try:
    option_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="allCheckAgree"]')))
    option_element.click()
  except:
    print()

  option_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btn_pay"]')))
  option_element.click()    

  try:
      # 얼럿이 표시될 때까지 대기 (10초로 설정)
      WebDriverWait(driver, 0.1).until(EC.alert_is_present())
      # 얼럿 객체 가져오기
      alert = driver.switch_to.alert
      # 얼럿 텍스트 출력 (선택사항)
      print("Alert Text:", alert.text)
      # 얼럿 확인 버튼 클릭 (선택사항)
      alert.accept()
      option_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="allCheckAgree"]')))
      option_element.click()
      option_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btn_pay"]')))
      option_element.click()    
  except Exception as e:
      # 얼럿이 표시되지 않은 경우 예외 처리
      print("No alert found.", str(e))


  #새창 대기
  current_window = driver.current_window_handle
  # 새로운 창 핸들 찾기
  new_window = None
  while not new_window:
      for window_handle in driver.window_handles:
          if window_handle != current_window:
              new_window = window_handle
              driver.switch_to.window(window_handle)
              time.sleep(0.5)
              current_url = driver.current_url
              print("새창 찾기 창 주소: " + driver.current_url)
              if "https://pay.musinsa.com/certify/req"  in current_url:
                  print("찾는 주소가 열린 창입니다.")
                  break
              driver.switch_to.window(new_window)
          time.sleep(0.5)

  iFrame = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="__tosspayments_connectpay_iframe__"]')))
  driver.switch_to.frame(iFrame)

  while 1:
    try:
      # html 로딩 대기
      goods = driver.find_elements(By.XPATH, '//*[@id="connectpay-portal-container"]/div/div/a[2]')
      if(goods):
        break
    except:
      time.sleep(0.1)

  def click_number_keypad(driver, number):
      script = f"""
          var keypadElement = document.querySelector("#connectpay-portal-container > div > div");
          var numberButtons = keypadElement.querySelectorAll("a[data-virtual-keypad='{number}']");
          if (numberButtons.length > 0) {{
              var randomNumberButton = numberButtons[Math.floor(Math.random() * numberButtons.length)];
              randomNumberButton.dispatchEvent(new MouseEvent('mouseup', {{
                  bubbles: true,
                  cancelable: true,
                  view: window
              }}));
          }}
      """
      driver.execute_script(script)

  script = f"""
          var keypadElement = document.querySelector("#connectpay-portal-container > div > div");
          return keypadElement.querySelectorAll("a");
      """
  a_elements = driver.execute_script(script)
  #a_elements = driver.find_element(By.XPATH, '//*[@id="connectpay-portal-container"]/div/div/a')
      # a 태그의 텍스트 값 출력

  with open("./data/password.txt", "r", encoding='utf-8') as password_file:
    password_str = password_file.readline().strip()

  for password in password_str:  
    for a_element in a_elements:
      virtual_keypad_value = a_element.get_attribute("data-virtual-keypad")
      if(password == a_element.text):
        click_number_keypad(driver, virtual_keypad_value)
        break

  print("구매 완료...")

  # def click_number_keypad(driver, number):
  #     # 숫자 키패드 엘리먼트를 찾음
  #     keypad_element = driver.find_element(By.CLASS_NAME, "connectpay-1iyjup2")

  #     # 숫자 키패드의 모든 숫자 버튼을 찾아 리스트에 저장
  #     number_buttons = keypad_element.find_elements(By.CLASS_NAME, "connectpay-1wd7y69")

  #     # 주어진 숫자를 찾아서 클릭
  #     for button in number_buttons:
  #         if button.get_attribute("data-virtual-keypad") == str(number):
  #             button.click()
  #             break
  # with open("./data/chrome.txt", "r", encoding='utf-8') as password_file:
  #     password_str = password_file.readline().strip()

  # # 문자열 비밀번호를 숫자 리스트로 변환
  # password = [int(digit) for digit in password_str]

  # for digit in password:
  #     click_number_keypad(driver, digit)
  #     time.sleep(0.5)  # 숫자를 클릭한 후 잠시 대기 (0.5초)

  # click_number_keypad(driver, 1)
  # click_number_keypad(driver, 3)
  # click_number_keypad(driver, 5)
  # click_number_keypad(driver, 6)
  # click_number_keypad(driver, 0)
  # click_number_keypad(driver, 0)



  # driver.execute_script(
  #   "var anchorElement = document.querySelector("+\
  #   "'#connectpay-portal-container > div > div > a:nth-child(1)');"+\
  #   "if (anchorElement) {"+\
  #     "var mouseUpEvent = new MouseEvent('mouseup', {"+\
  #       "bubbles: true,"+\
  #       "cancelable: true,"+\
  #       "view: window,"+\
  #     "});"+\
  #     "anchorElement.dispatchEvent(mouseUpEvent);"+\
  #   "}"
  # )
  time.sleep(60)
  
input_date_string = "2023-08-07"  # Replace this with the date you want to check
result = is_within_last_week(input_date_string)
if(result):
  start()