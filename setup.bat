@echo off
echo [PASSO 1 de 3] Criando o ambiente virtual (venv)...
python -m venv venv

echo [PASSO 2 de 3] Ativando o ambiente e instalando pacotes...
REM 'call' e usado para executar outro .bat e depois retornar
call venv\Scripts\activate.bat

REM Instala os pacotes do requirements.txt
pip install -r requirements.txt

echo [PASSO 3 de 3] Setup completo!
echo.
echo Voce pode fechar esta janela.
pause