import streamlit as st
import pandas as pd
import datetime
import os

# ... (이하 생략)

  

  


 


  


Installing collected packages: pyngrok, pydeck, streamlit
Successfully installed pydeck-0.9.1 pyngrok-7.5.0 streamlit-1.52.2
Overwriting app.py
from pyngrok import ngrok

# 1. 여기에 ngrok 사이트에서 복사한 토큰을 따옴표 안에 넣어주세요
ngrok.set_auth_token("35Uxhqdaebm07P1Rl6stsEOSGFU_4YHmrr7rvdvPe2wF9A7Ty")

# 2. 앱 실행 (백그라운드)
!nohup streamlit run app.py --server.port 80 &

# 3. 외부 접속 주소 생성
url = ngrok.connect(80).public_url
print(f"👇 아래 링크를 클릭하면 앱이 열립니다! 👇\n\n{url}\n")
nohup: appending output to 'nohup.out'
👇 아래 링크를 클릭하면 앱이 열립니다! 👇

https://jocularly-unblinding-angele.ngrok-free.dev
