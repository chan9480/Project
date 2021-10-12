import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import re
import time


test_url_1 = 'https://steamdb.info/sales/'

#number = 한번에 불러올수 있는 최대 갯수. {0(권장) : 100, 1:250, 2: 1k, 3: 5k}
number_1 = 3

def get_sales_data(url, number):
    # 크롬 드라이버를 실행하는 명령어를 dr로 지정 dr.get('~url~') 
    # 드라이버를 통해 url의 웹 페이지를 오픈
    dr = webdriver.Chrome()
    act = ActionChains(dr)
    dr.get(url)
    
    #한페이지에 100개 이상 표시하기 위해 동적입력()
    for i in range(number):
        element_1 = dr.find_element_by_name('DataTables_Table_0_length').send_keys(Keys.ARROW_DOWN)
    #Rating 높은 순으로 정렬 (top100)
    elems_rating = dr.find_elements_by_class_name('sorting.sorting_desc')
    for i in range(2):
        elems_rating[2].click()

    dr.implicitly_wait(5)
    #게임 이름, 할인율, 가격, 평가 등을 담은 정보를 가져옴. 
    elements_ = dr.find_elements_by_tag_name("tr")

    #p1 이름, p2 할인율, p3 가격, p4 평가 를 뽑아내기위한 정규표현식.
    p1=re.compile('.+\n')
    p2=re.compile('-\d+%')
    p3=re.compile('₩ \d+')
    p4=re.compile('\d+[.]\d+%')
    #print(len(element_names)-1) #전체 길이
    
    result = []
    for element in elements_[1:]:
        #이름 : 여러 글자합중 첫번째꺼 + \n제거
        temp_name=p1.findall(element.text)
        name = temp_name[0].rstrip()
        #할인율 : 00%로 끝나는 여러개중 첫번째꺼, %제거
        temp_discount_rate=p2.findall(element.text)
        discount_rate=int(temp_discount_rate[0][0:-1])
        #가격 ₩ 000 모양으로 된것.
        temp_price=p3.findall(element.text)
        price=int(temp_price[0][2:])
        #rating 00.00%로 된 것. 근데 없을수도 있음. 그러면 0
        try :
            temp_rating=p4.findall(element.text)
            rating = float(temp_rating[0][0:-1])
        except:
            rating = 0
        result.append({'name': name, 'discount_rate': discount_rate, 'price' : price, 'rating':rating})
    dr.quit()
    return result


def get_play_time(game_name):
    # 옵션 생성
    options = webdriver.ChromeOptions()
    # 창 숨기는 옵션 추가
    options.add_argument("headless")
    dr = webdriver.Chrome(options=options)
    #불러오고 게임네임 검색.엔터
    act = ActionChains(dr)
    dr.get('https://howlongtobeat.com/#search')
    dr.find_element_by_xpath('//form/div/div/div/div/div/div/input').send_keys(game_name)
    dr.find_element_by_xpath('//form/div/div/div/div/div/div/input').send_keys(Keys.RETURN)
    time.sleep(2)

    #element 수집
    result=''
    for i in range(10,110,10):
        try : 
            elems_1=dr.find_element_by_class_name('search_list_tidbit.center.time_'+str(i))
        except:
            pass
        if result =='':
            try:
                result=elems_1.text
            except:
                pass
    if result=='':
        result=None
    #elems_2=dr.find_elements_by_class_name("VwiC3b.yXK7lf.MUxGbd.yDYNvb.lyLwlc.lEBKkf")
    # ~~hours 나 Hours모양의 text 추출
    #p5=re.compile('\d+ .ours')

    print(result)
    #result=p5.findall(elems_1[0].text + elems_2[0].text)
    return result

#print(get_play_time('it takes two'))
#print(get_sales_data(test_url_1,0))