from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import random
import subprocess
import time
import re
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
from selenium.webdriver.support.ui import Select
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
    
def extract_numbers(s):
    return re.findall(r'\d+', s)
  
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
      alert.accept()
      time.sleep(3)
    except Exception as e:
      while 1:
        try : 
          element = driver.find_element(By.XPATH, '//*[@id="ct"]/div[3]/ul/li[1]/a')
          if (element):
          #로그인되어있음
            print(id + " // 정상 접속")
            break
        except Exception:
          print()
        time.sleep(1)
      
  
  
    #컬러
    buy_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="option0"]/a')))
    driver.execute_script("arguments[0].click();", buy_button)
    
    buy_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="op_0_0"]')))
    driver.execute_script("arguments[0].click();", buy_button)
    
    buy_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ct"]/div[4]/a[1]')))
    driver.execute_script("arguments[0].click();", buy_button)
    
    #사이즈
    
    buy_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="option1"]/a')))
    driver.execute_script("arguments[0].click();", buy_button)
    
    
    if(size != ''):
      try:
        label = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//label[contains(text(), "'+size+'")]')))
        driver.execute_script("arguments[0].click();", label)
      except:
        labels = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//label')))
        labels_with_numbers = [label for label in labels if any(num in label.text for num in extract_numbers(label.text))]
        labels_with_numbers.pop()
        if labels_with_numbers:
          # 랜덤하게 라벨 선택
          selected_label = random.choice(labels_with_numbers)  
          driver.execute_script("arguments[0].click();", selected_label)
    else:
      labels = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//label')))
      labels_with_numbers = [label for label in labels if any(num in label.text for num in extract_numbers(label.text))]
      labels_with_numbers.pop()
      if labels_with_numbers:
        # 랜덤하게 라벨 선택
        selected_label = random.choice(labels_with_numbers)  
        driver.execute_script("arguments[0].click();", selected_label)
        
        
        # 라벨 클릭
      # # 텍스트가 없는 경우 랜덤하게 요소 선택 후 클릭
      # elements = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//label')))
      # if elements:
      #   random_element = random.choice(elements)
      #   random_element.click()
    
    #확인
    buy_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ct"]/div[4]/a[1]')))
    driver.execute_script("arguments[0].click();", buy_button)
    
    #확인
    buy_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ct"]/div[3]/ul/li[1]/a')))
    driver.execute_script("arguments[0].click();", buy_button)
    
    while 1:
      try : 
        element = driver.find_element(By.XPATH, '//*[@id="orderForm"]/div/div[7]/button')
        if (element):
          #로그인되어있음
          print(id + " // 결제 창 진입")
          break
      except Exception:
        time.sleep(1)

    #일반결제
    buy_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="chargePointScrollArea"]/div[1]/ul[1]/li[4]/div[1]/span[1]/span')))
    driver.execute_script("arguments[0].click();", buy_button)
    
    #나중에결제
    buy_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="chargePointScrollArea"]/div[1]/ul[1]/li[4]/ul/li[4]/span[1]/span')))
    driver.execute_script("arguments[0].click();", buy_button)
    
    
    
    option_dropdown = driver.find_element(By.XPATH, '//*[@id="skipPaymentMethodSelectBox"]/select')
    # '옵션 선택'을 제외한 옵션들을 찾아서 리스트에 저장
    available_options = option_dropdown.find_elements(By.XPATH, "./option[contains(text(), '나중에 카드')]")
    driver.execute_script("arguments[0].click();", available_options)
      
    # #결제구분
    # buy_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="skipPaymentMethodSelectBox"]/div/div')))
    # driver.execute_script("arguments[0].click();", buy_button)
    
    # #나중에 카드 결제
    # buy_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/ul/li[2]')))
    # driver.execute_script("arguments[0].click();", buy_button)
    
    #주문결제
    buy_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="orderForm"]/div/div[7]/button')))
    driver.execute_script("arguments[0].click();", buy_button)
        
  if(driver.current_url in "https://order.pay.naver.com/orderSheet/result/2023080830498831/integrationCart"):
    print("// 주문 완료")
  else:
    print("// 주문 실패")
  
input_date_string = "2023-08-10"  # Replace this with the date you want to check
result = is_within_last_week(input_date_string)
if(result):
  start()
