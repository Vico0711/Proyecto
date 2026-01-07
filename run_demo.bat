@echo off
echo ============================================
echo GENERANDO DEMO DEL SISTEMA
echo ============================================
echo.

echo [1/3] Generando dataset sintetico...
python scripts/generate_dataset.py
echo.

echo [2/3] Ejecutando notebook de demo...
jupyter nbconvert --to notebook --execute notebooks/DEMO_PRESENTACION.ipynb
echo.

echo [3/3] Abriendo Jupyter...
jupyter notebook notebooks/DEMO_PRESENTACION.ipynb

echo.
echo ============================================
echo DEMO LISTA PARA PRESENTACION
echo ============================================
pause