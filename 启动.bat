@echo off
chcp 65001 >nul
cd /d D:\smart-ai-agent

echo ========================================
echo   Smart AI Agent 启动中...
echo ========================================

echo [1/2] 启动后端API服务...
start "AI Agent 后端" cmd /k "cd /d D:\smart-ai-agent && python src/run_service.py"

timeout /t 3 /nobreak >nul

echo [2/2] 启动Web界面...
start "AI Agent 前端" cmd /k "cd /d D:\smart-ai-agent && streamlit run src/streamlit_app.py --server.port 8501"

timeout /t 5 /nobreak >nul

echo.
echo ========================================
echo   启动完成！
echo   浏览器打开: http://localhost:8501
echo ========================================
start http://localhost:8501
pause