@echo off
echo "Start NSC_Builder Interface"

cd %~dp0

cd ..\ztools\dist\ztools
squirrel.exe -lib_call Interface start -xarg chrome true 800 740 rg8000 localhost