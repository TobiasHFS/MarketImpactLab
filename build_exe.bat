@echo off
echo Building Market Impact Lab Executable...
pyinstaller --noconfirm --onefile --windowed --name "MarketImpactLab" --add-data "src;src" --hidden-import "sklearn.utils._typedefs" --hidden-import "sklearn.neighbors._partition_nodes" --hidden-import "matplotlib.backends.backend_tkagg" src/gui/app.py
echo Build Complete. Executable is in dist/MarketImpactLab.exe
pause
