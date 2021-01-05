from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import time

#검사 받을 텍스트 파일은 연다.
fp = open("1.txt", 'r' , encoding="utf-8")
text = fp.read()
fp.close()

ready_list = []
while (len(text) > 500):
    temp_str = text[:500] # 처음 500글자를 보관
    last_space = temp_str.rfind(' ') # 500번 째 전 가장 가까운 공백을 찾아서 위치 보관
    temp_str = text[0:last_space] # 위 위치로 문자열 범위 재조정
    print(len(temp_str))
    ready_list.append(temp_str) # 재조정된 문자열을 리스트에 추가

    text = text[last_space:] # 최초의 텍스트 중 추가된 문자열 제거

ready_list.append(text) # 500글자 이하 나머지 조각 리스트에 추가가print(len(ready_list))


driver = webdriver.Chrome('C:\\Users\\태정\\Desktop\\chromedriver')
driver.get("http://www.naver.com")

elem = driver.find_element_by_id("query")
elem.send_keys("맞춤법 검사기")
elem.send_keys(Keys.RETURN)

time.sleep(2)
textarea = driver.find_element_by_class_name("txt_gray")

new_str = ''
for ready in ready_list:
    textarea.send_keys(Keys.CONTROL, "a")
    textarea.send_keys(ready)

    elem = driver.find_element_by_class_name("btn_check")
    elem.click()

    time.sleep(1)

    soup = bs(driver.page_source, 'html.parser')
    st = soup.select("p._result_text.stand_txt")[0].text
    new_str += st.replace('. ', '.\n')

fp = open("result.txt", 'w', encoding='utf-8')
fp.write(new_str)
fp.close()

driver.close()
driver.quit()