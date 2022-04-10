# @ Joonery
# 개념글 뉴스레터 프로그램



# 기본 로직

# 1) 해당 갤러리의 코드를 알아내서, 접속한다.
# 2) 받아온 html 코드를 분석하여, 해당 날짜에 올라온 개념글의 정보를 parcing.
                                                # (제목, 시간, 추천)
# 3-1) 모든 pacing된 정보를 f.open()으로 txt파일 또는 excel 파일에 정리하여 export.

###### 발전 -3 : keyword가 있는 것만 추출하기.
# 발전 -2 : days를 활용할 수 없을까?
# 발전 -1 : 시간을 더욱 정확하게 표시
# 발전 0 : 마이너 갤러리 말고 일반 갤에서도 작동하도록 대응.
# 발전 1 : 내용을 html을 이용해 예쁘게 정리
# 발전 2 : 내용을 메일로 전송
# 발전 5 : 누구에 관련된 글인지 유형을 알려준다.
# 발전 4 : Build to an exe file.
# 발전 3 : GUI로 동작


from bs4 import BeautifulSoup as bs
import requests as rq
import time
from datetime import datetime, timedelta
import os
from openpyxl import Workbook


class KgallAlimi() :

    # 생성자
    def __init__(self, code, list_keywords, path="", maxpost=100, filename="냠냠") :
        self.code = code                        # 갤러리 코드
        self.list_keywords = list_keywords      # 수집할 키워드
        self.path = path                        # 내보낼 경로
        # self.days = days                        # 며칠 전까지 수집할 것인가 (현재는 사용하지 않음)
        self.maxpost = maxpost                  # 최대 수집할 글의 개수
        self.filename = filename

        self.pagenum = 0
        self.today = datetime.today()                                           # 오늘 날짜
        self.user_agent = {'User-agent': 'Mozilla/5.0'}                         # 접속설정
        self.urlbase = "https://gall.dcinside.com/mgallery/board/lists/?id="    # 접속할 개념글 주소 베이스
        self.urlbase_view = "https://gall.dcinside.com/m/"                      # 내보낼 개념글 주소 베이스

    ### 다음 개념글 페이지의 주소를 리턴한다.
    def get_next_page(self) :
        # 조합 방식 : https://gall.dcinside.com/mgallery/board/lists/?id= + kizunaai + &page= + 1 + &exception_mode=recommend
        self.pagenum += 1
        next_page_url = self.urlbase + self.code + "&page=" + str(self.pagenum) + "&exception_mode=recommend"
        return next_page_url

    ### URL에서 html을 받아온다.
    def get_html(self, url):
        _html = ""
        suc = False
        
        # 성공할 때까지 반복하며 html을 가져옴.
        while(suc == False):
            
            try:
                response = rq.get(url,headers=self.user_agent)
            
            except rq.exceptions.RequestException as e:
                time.sleep(3)
                continue

            if response.status_code == 200:
                suc = True
                _html = response.text

            else:
                suc = True
                _html = "<tbody><td>잘못된 주소 입니다.</td></tbody>"

        return _html

    ### 오늘의 날짜를 04.09 의 string으로 return.
    def get_today(self) :
        return str(self.today.strftime('%m.%d'))

    ### n일 전의 날짜를 04.09 의 string 형태로 return.
    def get_beforeday(self, nday) :
        return str((datetime.today()-timedelta(days=nday)).strftime('%m.%d'))

    ### html에서 얻어온 데이터를 파싱해 집어넣는다.
    def parse_data(self, html, newposts) :
        
        # 해당 페이지의 정보를 html로 읽어서
        soup = bs(html, 'html.parser')

        # 해당 페이지에 있는 모든 글의 정보를 리스트에 저장
        rawposts = soup.find("tbody").find_all("tr", class_="ub-content us-post")

        # 모든 글들의 리스트에서 필요한 정보만 추출.
        for i in rawposts :

            # 만일 공지나 이벤트인 경우는 넘김.
            if (i.find("td", class_="gall_subject").text == "이벤트") or (i.find("td", class_="gall_subject").text == "공지") :
                continue

            # newpost = [4.9 , 6809, 74, 냠냠, ㅇㅇ, 링크]
            newpost = []

            newpost.append(i.find("td", class_="gall_date").text) # 날짜
            newpost.append(i.find("td", class_="gall_count").text) # 조회수
            newpost.append(i.find("td", class_="gall_recommend").text) # 추천수
            newpost.append(i.find("td", class_="gall_tit ub-word").text[:-6][1:]) # 제목
            newpost.append(self.urlbase_view + self.code + "/" + i.find("td", class_="gall_num").text) # 링크 

            # 글 모음에 집어넣음.
            newposts.append(newpost)

            # 만일 최대 개수까지 채웠으면 함수 종료
            if self.is_full(newposts) :
                return

    ### 파싱한 정보가 최대 개수를 넘었는지 판정.
    def is_full(self, newposts) :
        return (len(newposts) >= int(self.maxpost))

    ### 저장할 파일 경로를 반환한다. (디폴트 바탕화면)
    def get_filepath(self, extension) :
        
        # 넘어온 값이 있으면
        if self.path : 
            return self.path + self.filename + extension
        
        # 넘어온 값이 없으면
        else : 
            filename = "\\" + self.filename + extension
            filepath = os.path.join(os.path.expanduser('~'),'Desktop') + filename 
            return filepath

    ### 파싱한 내용을 txt file로 export. 
    def export_txt(self, newposts) :
        
        with open(self.get_filepath(".txt"), "w") as f:
            f.write(newposts) # 링크    
            f.close()

    ### 파싱한 내용을 xlsx file로 export. 
    def export_xlsx(self, newposts) :

        write_wb = Workbook()
        write_ws = write_wb.create_sheet('시트1')

        write_ws = write_wb.active

        for i in range(len(newposts)) :
            for j in range(len(newposts[i])) :
                write_ws.cell(row=i+1, column=j+1).value = newposts[i][j]
                if j==4 :
                    write_ws.cell(row=i+1, column=j+1).style = "Hyperlink"

        write_wb.save(self.get_filepath(".xlsx"))

    ### 파싱한 리스트를 콘솔창에 프린트(확인용)
    def print_list(self, newposts) :
        for post in newposts :
            print(post[0])
            print("조회수 : {} / 추천수 : {}".format(post[1], post[2]))
            print(post[3])
            print(post[4])
            print()

    # 메인 함수.
    def main(self) :       

        # 0) 초기화
        newposts = []

        # 1) 글을 모으기
        while not self.is_full(newposts) :                      # 정해진 개수만큼 수집하기 전까지는
            newurl = self.get_next_page()                       # 다음 페이지의 주소를 구해
            self.parse_data(self.get_html(newurl), newposts)    # 받아온 정보를 newposts에 파싱
        
        # 2) 파일로 내보내기
        self.export_xlsx(newposts)
        # self.print_list(newposts)


if __name__ == "__main__" :
    

    # ========================================================== config
    # 갤 코드를 입력하세요.
    code = 'kizunaai'    
    
    # 파일을 내보낼 경로를 입력하세요.
    path = ""      
    
    # 검색할 키워드를 입력하세요.
    list_keywords = [
        'EN', '2기생',                              # EN
        '모리', '칼리', '데몬다이스', '사신',        # 칼리
        '키아라', '치킨', '불닭', '타카나시',        # 키아라
        '아메', '왓슨', '슨상', '스몰', 'ame',      # 아메
        '타코', '이나', '희주', '무너',             # 이나
        '상어', '구라',                            # 구라
        '아이리스', 'Rys',                         # 아이리스
        '시계','크로니','도토부',                   # 크로니
        '땃쥐', '베이', '벨즈',                     # 베이
        '나나시', '무메이', '우흥', '토리',          # 무메이
        '파우나', '자연', '마망', '비건',            # 파우나
        '사나', '흑인',                             # 사나
    ]          
    

    # ========================================================== 실행
    alimi = KgallAlimi(code, path, 100, list_keywords, "냠냠")
    alimi.main()



##### 조합식 ====================================
# https://gall.dcinside.com/m/kizunaai/5181831
# https://gall.dcinside.com/mgallery/board/lists/?id=kizunaai&page=1&exception_mode=recommend
# https://gall.dcinside.com/mgallery/board/lists/?id=kizunaai&page=3&exception_mode=recommend

# 조합 방식 : https://gall.dcinside.com/mgallery/board/lists/?id= + kizunaai + &page= + 1 + &exception_mode=recommend



##### 결과물 ====================================
# 시간 
# 조회수 / 추천수
# 제목
# 링크

# 17:00
# 조회수 : 12500 / 추천수 : 120
# 무메이 너무 귀여워
# https://ㄴㅇㄹㄴㅇㄹㄴㅇㄹㄴ