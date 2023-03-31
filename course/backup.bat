CLS
ECHO OFF
CHCP 1251

SET PGBIN=C:\Program Files\PostgreSQL\15\bin
SET PGDATABASE=course_db
SET PGHOST=localhost
SET PGPORT=5432
SET PGUSER=course_db_user
SET PGPASSWORD=qwerty

%~d0 
CD %~dp0

SET DATETIME=%DATE:~6,4%-%DATE:~3,2%-%DATE:~0,2% %TIME:~0,2%-%TIME:~3,2%-%TIME:~6,2%
SET DUMPFILE=%PGDATABASE% %DATETIME%.sql
SET LOGFILE=%PGDATABASE% %DATETIME%.log
SET DUMPPATH="backup\daily\%DUMPFILE%"
SET LOGPATH="backup\%LOGFILE%"

IF NOT EXIST backup\daily\Daily MD backup\daily
IF NOT EXIST Daily\%DATETIME% MD Daily\%DATETIME%
CALL "%PGBIN%\pg_dump.exe" --format=plain --verbose --file=%DUMPPATH% 2>%LOGPATH%

IF NOT %ERRORLEVEL%==0 GOTO Error
GOTO Successfull

:Error
DEL %DUMPPATH%
MSG * "Ошибка при создании резервной копии базы данных. Смотрите backup.log."
ECHO %DATETIME% Ошибки при создании резервной копии базы данных %DUMPFILE%. Смотрите отчет %LOGFILE%. >> backup.log
GOTO End

:Successfull
ECHO %DATETIME% Успешное создание резервной копии %DUMPFILE% >> backup.log
GOTO End

:End
