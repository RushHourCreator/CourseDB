CLS
ECHO OFF
CHCP 1251
SCHTASKS /Create /RU SYSTEM /SC DAILY /TN "Резервная копия" /TR "C:\Users\sasha\PycharmProjects\courseDB\course\backup.bat" /ST 00:00:00
IF NOT %ERRORLEVEL%==0 MSG * "Ошибка при создании задачи резервного копирования! %ERRORLEVEL%"
