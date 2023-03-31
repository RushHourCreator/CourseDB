import yadisk
import os
import locale
import schedule

y = yadisk.YaDisk(token="y0_AgAAAABCdZvFAAmakwAAAADfzTqucpSqQNwDToe82CdknNv6GO-pTEE")
DAILY_DIR = "/daily-backup-db"
FILE_PATH = r'C:\Users\sasha\PycharmProjects\courseDB\course\Backup\Daily'


def backup_daily():
    for address, dirs, files in os.walk(FILE_PATH):
        for file in files:
            if not y.exists(f'{DAILY_DIR}/{file}'):
                y.upload(f'{address}/{file}', f'{DAILY_DIR}/{file}')
                print(f'Файл {file} загружен')


def main():
    schedule.every().minute.at(':00').do(backup_daily)
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL)
    print(y.check_token())
    main()
