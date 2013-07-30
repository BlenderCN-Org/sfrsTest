@set filename=scenefile
@set workdir="E:\Graphics\Works\testbuildsfor253\InstanceCheck"
@set jardir="E:\Graphics\sunflow\sunflow.jar"
@echo %jardir%
@set javadir="E:\Program Files\Java\jdk1.7.0_25"
@set mem=1G
@set val=%javadir%\bin\java -Xmx%mem% -server -jar %jardir%  -o %workdir%\%filename%.png  %workdir%\%filename%.sc %*
%val%
@if %errorlevel% neq 0 pause