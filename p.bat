@echo off
chcp 65001 > nul

echo ========================================
echo 🚀 Pol-Guard 강제 동기화 및 업로드 시작
echo ========================================

git add .
set /p msg="📝 커밋 메시지를 입력하세요 (미입력 시 'update'): "
if "%msg%"=="" (
    set msg=update
)

git commit -m "%msg%"
:: --force를 붙여서 서버 기록을 내 컴퓨터 기록으로 덮어씌웁니다.
git push origin main 
echo.
echo ========================================
echo ✅ 강제 업로드 완료! 이제 사이트를 확인하세요.
echo ========================================
pause