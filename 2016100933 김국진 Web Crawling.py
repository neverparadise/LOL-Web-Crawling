#201610933 김국진 Web/Python Term Project
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time
import random
import datetime


#해결해야할 사항 : 텍스트 전처리를 통해 분과 시간만 나오게 하기, 4개월간의 게임 통계를 계속해서 로딩할 수 있도록 버튼 클릭 구현
#프로젝트 순서 1.페이지 더불러오는 문제 해결해야함 데이터 수집 2. 데이터 전처리, 분, 초 나누어주기(연산을 위해)  2.5 엑셀로 저장 3. 데이터 분석 4. 결론 도출 5. 에러처리
#게임 날짜와 게임 시간을 어떻게 같이 가져올 수 있을까? -> 리스트와 딕셔너리, 집합활용


#   3. 인터넷을 통한 데이터의 획득 과정 부분
print("-" * 40)
nickname = input("Enter the your League Of Legend Nickname : ")                 #리그오브레전드 닉네임 입력
filename1 = nickname + ".txt" #메모장 저장을 위한 파일이름 변수 설정
filename2 = "./data/" + nickname + ".csv" #pandas를 통한 파일저장을 위해 파일이름 변수 설정
path = "C:/Users/Administrator/Desktop/chromedriver"                            #selenium을 사용하기 위한 경로변수설정
driver = webdriver.Chrome(path)
driver.implicitly_wait(3)
print("Opening your records of League of Legend")
driver.get("https://www.op.gg/summoner/userName=" + nickname)
req = driver.page_source
bs = BeautifulSoup(req, 'lxml')


#예외처리
Not_Find_Message = bs.findAll('h2', "Title")
#print(Not_Find_Message)
print(bool(Not_Find_Message))
if (bool(Not_Find_Message) == True):
    print("등록되지 않은 사용자입니다. 프로그램을 종료 후 다시 실행해주세요!")
    exit(100)

#데이터를 더 수집하기 위해서 웹사이트의 버튼을 자동으로 클릭해주는 함수를 반복구현.
for n in range(4, 33): #op.gg의 게임데이터는 최근 6개월 간의 게임 데이터를 불러올 수 있다..
    req = driver.page_source
    bs = BeautifulSoup(req, 'lxml')
    Error_Message = bs.findAll('div', 'Message')
    # print(Error_Message)
    # print((Error_Message[len(Error_Message)-1]))
    # print(type((Error_Message[len(Error_Message) - 1])))
    str_Error = str((Error_Message[len(Error_Message) - 1]))
    print(str_Error)
    #기록된 전적이 없으면 break
    a = '<div class="Message"> 기록된 전적이 없습니다.</div>'
    if (a in str_Error):
        print("The record not exists...")
        break
    else:
        ButtonAddress = ('//*[@id="SummonerLayoutContent"]/div[2]/div[2]/div/div[2]/div[%d]/a' % n)
        # find_element함수의 인수는 한가지 뿐이므로 문자열 포맷팅과 같이 사용하기 위해 변수로 만들어준다.

        driver.find_element_by_xpath(ButtonAddress).click()

        #크롬의 매크로 방지기능을 우회하기 위한 랜덤변수 30초에서 60초 사이의 무작위 시간 동안 쉬어준다.
        rand_value = random.randint(40, 60)
        time.sleep(rand_value)
        print(rand_value)

#모든 버튼을 클릭한 후 데이터 전처리
#4.분석을 위한 데이터 가공, 전처리 부분
req = driver.page_source
bs = BeautifulSoup(req, 'lxml')
f = open(filename1, 'a', encoding='utf-8')
f.write(req)
f.close()

#게임 date를 추출한다..
GameDate_list = bs.findAll('div', 'TimeStamp')
print(GameDate_list)
Date_list = []
# 데이터 전처리
for index in range(len(GameDate_list)):
    temp = GameDate_list[index]
    print(temp)
    string_data1 = str(temp)
    if " tpd-delegation-uid-1" in string_data1:
       string_data1 = string_data1.replace (' tpd-delegation-uid-1', "")

    string_data1 = string_data1.replace(string_data1[0:135], "")
    string_data1 = string_data1.replace("</span></div>", "")
    for hour in range(1,25):
        junk = (">%d시간 전" %hour)
        string_data1 = string_data1.replace(junk, "")

    string_data1 = string_data1.replace("하루 전", "")

    for day in range(2, 31):
        junk = (">%s일 전" %day)
        string_data1 = string_data1.replace(junk, "")

    string_data1 = string_data1.replace("한달 전", "")

    for month in range(0, 6):
        junk = (">%s달 전" %month)
        string_data1 = string_data1.replace(junk, "")

    splited_data = string_data1.split()
    splited_data[3:] = []
    temp_data = splited_data[0] + splited_data[1] + splited_data[2]
    temp_data = temp_data.replace("년", '-')
    temp_data = temp_data.replace("월", '-')
    temp_data = temp_data.replace('일', '')
    processed_data = temp_data
    print(processed_data)
    Date_list.append(processed_data)
print(Date_list)

#게임 플레이 시간을 추출한다.
GameLength_list = bs.findAll('div', 'GameLength')
print(GameLength_list)
print(len(GameLength_list))
Length_list = []
Minutes_list = []
Seconds_list = []
Hour_list = []
# 데이터 전처리
for index in range(len(GameLength_list)):
    temp = GameLength_list[index]
    print(temp)
    string_data2 = str(temp)
    string_data2 = string_data2.replace('<div class="GameLength">', "")
    string_data2 = string_data2.replace("초", "")
    string_data2 = string_data2.replace("분", "")
    string_data2 = string_data2.replace("</div>", "")
    print(string_data2)
    time_temp = string_data2.split()
    minutes = int(time_temp[0])
    seconds = int(time_temp[1])
    Hours = float(((60*minutes)+seconds)/3600)

    Length_list.append(string_data2)
    Minutes_list.append(minutes)
    Seconds_list.append(seconds)
    Hour_list.append(Hours)

print(Length_list)

GameDateLength = {}
for index in range(0, len(Length_list) - 1):
    GameDateLength[Date_list[index]] = Length_list[index]

print(GameDateLength)

sum = 0
for i in Hour_list:
   sum += i
GameHourSum = sum
#
# print(frequency_of_day)
# print(len(Date_list))
# print(len(Hour_list))
# print(len(frequency_of_day))


#한 판 단위 게임데이터 저장
frequency_of_day = []
for index in range(0, len(Date_list)):
    a = Date_list[index]
    frequency = Date_list.count(a)
    frequency_of_day.append(frequency)

data = {"GameData":Date_list, "GameLength":Hour_list, "Frequency": frequency_of_day}
db =pd.DataFrame(data, columns=["GameDate", "GameLength", "Frequency"])
db.index.name = nickname + "의 게임기록"
db.to_csv("result.csv", mode = 'a', header=True, index=True, encoding='cp949')



#하루 단위 게임 데이터 저장
temp = set(Date_list)
temp2 = list(temp)
result_Date = sorted(temp2, key=lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'), reverse=True)
#이로써 날짜를 가장 최근의 순서대로 정렬된 리스트가 생성되었다.

index = 0
processed_Hour_list = []
pro_frequency_of_day = []
while(index < len(Date_list)):
    a = Date_list[index]
    frequency = Date_list.count(a)
    pro_frequency_of_day.append(frequency)

    Hour_sum = 0
    for index2 in range(index, index + frequency):
        Hour_sum += Hour_list[index2]

    processed_Hour_list.append(Hour_sum)
    index += frequency
    #print(index)
#print(pro_frequency_of_day)
#print(processed_Hour_list)



data1 = {"GameData":result_Date, "GameLength":processed_Hour_list, "Frequency":pro_frequency_of_day}
db1 = pd.DataFrame(data1, columns=["GameData", "GameLength", "Frequency"])
db1.index.name = "GameRecord"
db1.to_csv(filename2, mode = 'a', header=True, index=True, encoding='cp949')

print("Data Crawling and Processing Finished")
# print("당신이 리그오브레전드를 한 판만 한 날은 최근 4개월간 %d번입니다..." %final_count)
# print("게임 한 판은 단 한 판으로 끝날 가능성이 거의 낮습니다 따라서 시험기간에 게임하는 것을 조심하세요!")
# print("당신이 리그오브레전드를 4개월 간 플레이한 시간은 %f시간입니다...." %GameHourSum)
# print("당신의 시간은 매우 소중합니다. 다시는 돌아오지 않는 시간들 알차게 보내세요!")

#가장 고민이 많았던 부분 날짜와 게임빈도를 어떻게 같이 묶을 것인가?
#해결책 : 파이썬 내장함수 set을 이용
#집합은 순서가 없기 때문에 정렬을 해야한다.
#하지만 파이썬의 내장함수 sort로는 스트링으로 된 날짜를 정렬할 수 없다.
#따라서 datetime이라는 외부 라이브러리를 이용한다.

