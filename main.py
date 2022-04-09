# @ Joonery
# 뉴스레터 프로그램입니다.

# 커뮤니티 크롤링해 링크를 포함한 제목과 링크를 모아 메일로 전송하는 프로그램.


# 메일 STTP 서버 활용
# https://velog.io/@myway00/Python-%EB%B3%B5%EC%8A%B5-004-%ED%8C%8C%EC%9D%B4%EC%8D%AC%EC%9C%BC%EB%A1%9C-%EC%9D%B4%EB%A9%94%EC%9D%BC-%EB%B0%9C%EC%86%A1

# 이벤트크롤러
# https://github.com/doorBW/event_crawl/blob/master/event_crawler.py

# 뉴스레터 프로그램
# https://wooiljeong.github.io/python/newsletter/


# 아카라이브 알리미
# https://github.com/aldlfkahs/DCinsideAlarm/tree/arcalive

# 디시알리미
# https://github.com/aldlfkahs/DCinsideAlarm

# 뉴스레터 알리미
# https://wooiljeong.github.io/python/newsletter/

# html.parser 구문 분석기 : 개유용함
# https://docs.python.org/ko/3/library/html.parser.html

# 파싱 예제
# https://library.gabia.com/contents/9239/



# 개념글 뉴스레터 프로그램
# 기본 로직

# 1) 해당 갤러리의 코드를 알아내서, 접속한다.
# 2) 받아온 html 코드를 분석하여, 해당 날짜에 올라온 개념글의 정보를 parcing.
                                                # (제목, 시간, 추천/비추)
# 3-1) 모든 pacing된 정보를 f.open()으로 txt파일 또는 excel 파일에 정리하여 export.


# 발전 1 : 내용을 html을 이용해 예쁘게 정리한다.
# 발전 2 : 내용을 메일로 전송한다.
# 발전 3 : GUI로 동작이 가능하다.
# 발전 4 : Build to exe file.


from bs4 import BeautifulSoup as bs
import requests

user_agent = {'User-agent': 'Mozilla/5.0'}

class KgallAlimi() :

    # 생성자
    def __init__(self, url, path, list_keywords) :
        self.url = url
        self.path = path
        self.list_keywords = list_keywords

    # 파싱 함수
    def parser(self, html, list) : 
        
        tempinfo = []

        # html. ~~~ 어느 부분을 찾아서
        #

        # 개념글 리스트에 추가
        list.append(tempinfo) 

    # 해당 url에 접속한다. 
    def connect(self, url) :

        if 1 :
            return 1
        else :
            return 0

    # URL에서 html을 받아온다.
    def get_html(self, url):
        _html = ""
        suc = False
        while(suc == False):
            try:
                resp = requests.get(url,headers=user_agent)
            except requests.exceptions.RequestException as e:
                time.sleep(3)
                continue

            if resp.status_code == 200:
                suc = True
                _html = resp.text
            else:
                suc = True
                _html = "<tbody><td>잘못된 주소 입니다.</td></tbody>"
        return _html

    # text의 내용을 file로 
    def exporttofile(self, text) :
        pass

    # 관심있는 갤러리에서
    def get_mylist(self) :
        global flag
        flag = True

        html = get_html(self.addr.text())
        soup = BeautifulSoup(html, 'html.parser')

        # 말머리 리스트 가져오기
        subject_list = []
        try:
            center_box = soup.find('div', attrs={'class': 'center_box'})
            for t in center_box.select('li'):
                subject_list.append(t.text)
        except AttributeError:
            print("말머리 없음")
        # 받아온 html에서 글 번호만 파싱
        try:
            init_check = soup.find("tbody").find_all("tr", class_="ub-content us-post")
        except AttributeError:
            QMessageBox.about(self, "오류", "갤러리 주소가 잘못되었습니다.")
            return
        # recent 변수에 현재 최신 글 번호를 저장
        global recent
        self._lock.acquire()
        recent = 1
        for idx in init_check:
            init_num = idx.select_one('td.gall_num').text
            if (not init_num.isdecimal()):
                continue
            if (recent < int(init_num)):
                recent = int(init_num)


if __name__ == "__main__" :
    
    # 주소를 입력하세요.
    url = '디시 갤러리 코드'    
    
    # 파일을 내보낼 경로를 입력하세요.
    path = '내보낼 경로'        
    
    # 검색할 키워드를 입력하세요.
    list_keywords = []          
    
    
    alimi = KgallAlimi(url, path, list_keywords)
    alimi.get_mylist()