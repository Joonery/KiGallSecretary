# @ Joonery
# 키워드 개념글 뉴스레터 프로그램

### BASIC LOGIC
# 1) 해당 갤러리의 코드를 알아내서, 접속한다.
# 2) 받아온 html 코드를 분석하여, 해당 날짜에 올라온 개념글의 정보를 parcing. (제목, 시간, 추천)
# 3-1) 모든 pacing된 정보를 f.open()으로 txt파일 또는 excel 파일에 정리하여 export.

from kigallalimi import *
from config import *

# ========================================================== 실행
alimi = KgallAlimi(gcode_kig, kw_holoen, maxpost, export_type, mail_addr=addr)
alimi.start()