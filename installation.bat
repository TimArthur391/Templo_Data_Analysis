cd /d %~dp0
cd ..
cd ..

xcopy /s Templo_Data_Analysis-main %userprofile%\Documents

cd C:\

conda create --name Templo-External-Moments python=3.9
call activate Templo-External-Moments

cd %userprofile%\Documents\Templo_Data_Analysis-main
python -m pip install -r requirements.txt

powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%userprofile%\Desktop\Templo External Moments.lnk');$s.TargetPath='%userprofile%\Documents\Templo_Data_Analysis-main\run_app.bat';$s.WorkingDirectory='%userprofile%\Documents\Templo_Data_Analysis-main';$s.IconLocation='%userprofile%\Documents\Templo_Data_Analysis-main\scrpts\walking_icon.ico';$s.Save()"

pause