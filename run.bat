@echo off
echo Ativando o ambiente virtual...
call venv\Scripts\activate.bat

echo.
echo Iniciando o aplicativo Streamlit...
echo O app abrira no seu navegador.
echo (Feche esta janela preta para parar o app).
echo.

streamlit run app.py