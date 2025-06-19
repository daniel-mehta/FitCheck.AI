@echo off
CALL "%USERPROFILE%\anaconda3\Scripts\activate.bat" hackathon
streamlit run "fitcheck\Fashion AI Advisor.py"
pause
