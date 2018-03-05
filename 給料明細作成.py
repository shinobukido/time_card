from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as msg
import re


def calc_app():
    root = Tk()
    root.geometry()
    root.title('給料明細作成')
    label = ttk.Label(root)
    label.pack()

    button_1 = ttk.Button(label, width=35, text='今月の牧さんの給料明細', command=maki_san)
    button_1.pack()
    button_2 = ttk.Button(label, width=35, text='今月の山田さんの給料明細', command=yamada_san)
    button_2.pack()
    button_3 = ttk.Button(label, width=35, text='今月の前田さんの給料明細', command=maeda_san)
    button_3.pack()
    button_4 = ttk.Button(label, width=35, text='今月の山村さんの給料明細', command=yamamura_san)
    button_4.pack()
    root.mainloop()


def read_csv(file_name, name):
    today = date.today()
    last_month = today - relativedelta(months=1)
    date_list = []
    yobi = ["月", "火", "水", "木", "金", "土", "日"]
    with open(file_name, encoding='utf-8') as f:
        for row in f:
            columns = row.rstrip().replace('\ufeff', '').split(',')
            workday = datetime.strptime(columns[0], '%Y/%m/%d')
            work_time = datetime.strptime(columns[1], '%H:%M')
            working_day = workday.weekday()
            action = columns[-1]
            data_list = [name, workday, work_time, yobi[working_day], action]
            if name in columns[3] and last_month.month == workday.month:
                    date_list.append(data_list)
    return date_list


def calc_time_saturday(name):
    saturday_time = []
    default_times_7 = '07:00'
    default_time_7 = datetime.strptime(default_times_7, '%H:%M')
    default_times_8 = '08:00'
    default_time_8 = datetime.strptime(default_times_8, '%H:%M')
    default_times_9 = '09:00'
    default_time_9 = datetime.strptime(default_times_9, '%H:%M')
    for row in read_csv('timecard.txt', name):
        action = row[-1]
        week_day = row[3]
        if '出勤' in action and '土' == row[-2]:
            start_time_saturday = row[2]
            if 6 <= start_time_saturday.hour < 7:
                time_delta = default_time_7 - start_time_saturday
            elif 7 <= start_time_saturday.hour < 8:
                time_delta = default_time_8 - start_time_saturday
            elif 8 <= start_time_saturday.hour < 9:
                time_delta = default_time_9 - start_time_saturday
            else:
                time_delta = row[2] - start_time_saturday
        if '退勤' in action and '土' in row:
            end_time_saturday = row[2]

            calc_work_time_saturday = end_time_saturday - start_time_saturday - time_delta
            sat_data = str(row[1])[:10] + ',' + week_day + ',' + start_time_saturday.strftime('%H:%M')\
                            + ',' + end_time_saturday.strftime('%H:%M') + ',' + str(calc_work_time_saturday)\
                           .replace(':00', '')
            saturday_time.append(sat_data)
    return saturday_time


def calc_time_week_day(name):
    week_day_time = []
    default_times_9 = '09:00'
    default_time_9 = datetime.strptime(default_times_9, '%H:%M')
    default_times_13_30 = '13:30'
    default_time_13_30 = datetime.strptime(default_times_13_30, '%H:%M')
    end_times = '12:05'
    end_time_12 = datetime.strptime(end_times, '%H:%M')

    for row in read_csv('timecard.txt', name):
        action = row[-1]
        week_day = row[3]
        end_time = row[2]
        if '出勤' in action and '土' not in week_day:
            start_time = row[2]
            if 8 <= start_time.hour < 9:
                time_delta = default_time_9 - start_time
            elif 13 <= start_time.hour < 14:
                time_delta = default_time_13_30 - start_time
        elif '退勤' in action and '土' not in week_day:
            if 11 <= end_time.hour < 12 and end_time.minute == 0:
                end_time = end_time_12
            else:
                end_time = row[2]

            calc_work_time = end_time - start_time - time_delta
            week_day_data = str(row[1])[:10] + ',' + week_day + ',' + start_time.strftime('%H:%M')\
                            + ',' + end_time.strftime('%H:%M') + ',' + str(calc_work_time).replace(':00', '')
            week_day_time.append(week_day_data)
    return week_day_time


def calc_saturday(name):
    change_time = []
    for row in calc_time_saturday(name):
        data = row.replace(':00', '').split(',')
        time_data = datetime.strptime(data[4], '%H:%M')
        if 0 <= time_data.minute < 15:
            str_time = time_data.strftime('%H:%M')
            str_change_time = str_time[3:5]
            re_change = str_time[1] + '.' + re.sub(r'[0-9]+', '00', str_change_time)
            change_time.append(re_change)
        elif 15 <= time_data.minute < 30:
            str_time = time_data.strftime('%H:%M')
            str_change_time = str_time[3:5]
            re_change = str_time[1] + '.' + re.sub(r'[0-9]+', '25', str_change_time)
            change_time.append(re_change)
        elif 30 <= time_data.minute < 45:
            str_time = time_data.strftime('%H:%M')
            str_change_time = str_time[3:5]
            re_change = str_time[1] + '.' + re.sub(r'[0-9]+', '50', str_change_time)
            change_time.append(re_change)
        elif 45 <= time_data.minute <= 59:
            str_time = time_data.strftime('%H:%M')
            str_change_time = str_time[3:5]
            re_change = str_time[1] + '.' + re.sub(r'[0-9]+', '75', str_change_time)
            change_time.append(re_change)
    return change_time


def calc_week_day(name):
    change_time = []
    for row in calc_time_week_day(name):
        data = row.replace(':00', '').split(',')
        time_data = datetime.strptime(data[4], '%H:%M')
        if 0 <= time_data.minute < 15:
            str_time = time_data.strftime('%H:%M')
            str_change_time = str_time[3:5]
            re_change = str_time[1] + '.' + re.sub(r'[0-9]+', '00', str_change_time)
            change_time.append(re_change)
        elif 15 <= time_data.minute < 30:
            str_time = time_data.strftime('%H:%M')
            str_change_time = str_time[3:5]
            re_change = str_time[1] + '.' + re.sub(r'[0-9]+', '25', str_change_time)
            change_time.append(re_change)
        elif 30 <= time_data.minute < 45:
            str_time = time_data.strftime('%H:%M')
            str_change_time = str_time[3:5]
            re_change = str_time[1] + '.' + re.sub(r'[0-9]+', '50', str_change_time)
            change_time.append(re_change)
        elif 45 <= time_data.minute <= 59:
            str_time = time_data.strftime('%H:%M')
            str_change_time = str_time[3:5]
            re_change = str_time[1] + '.' + re.sub(r'[0-9]+', '75', str_change_time)
            change_time.append(re_change)
    return change_time


def saturday_data(name):
    saturday_data_list = []
    for i, j in zip(calc_time_saturday(name), calc_saturday(name)):
        data = i + ',' + j
        saturday_data_list.append(data)
    return saturday_data_list


def week_day_data(name):
    week_day_data_list = []
    for i, j in zip(calc_time_week_day(name), calc_week_day(name)):
        data = i + ',' + j
        week_day_data_list.append(data)
    return week_day_data_list


def data_set(name):
    data = week_day_data(name) + saturday_data(name)
    return data


def main(name, price, saturday_price, textname):
    today = date.today()
    last_month = today - relativedelta(months=1)
    total_day = 0
    saturday_total = 0
    total_time = 0
    total_week_day = 0
    total_saturday = 0
    columns = ['日付', '曜日', '出勤時間', '退勤時間', '勤務時間', '計算時間']
    with open(textname, 'w', encoding='utf-8') as f:
        f.write(name + 'さんの給料明細' + '\n')
        title = ','.join(columns)
        f.write(title + '\n')
        for row in sorted(data_set(name)):
            columns = row.split(',')
            f.write(row + '\n')
            total_time += float(columns[-1])
            if '土' in row:
                total_saturday += float(columns[-1])
                saturday_total += len(columns)
            else:
                total_week_day += float(columns[-1])
                total_day += len(columns)
        total_data = int(total_day / 6)
        total_saturday_data = int(saturday_total / 6)
        sum_data = total_data + total_saturday_data
        calc_salary = float(total_week_day) * price
        calc_saturday_salary = float(total_saturday) * saturday_price
        f.write('\n')
        f.write('{}月の勤務日数： '.format(last_month.month) + str(sum_data) + '日' + '\n')
        f.write('{}月の勤務時間： '.format(last_month.month) + str(total_time) + '時間' + '\n')
        f.write('----　内訳　----' + '\n')
        f.write('{}月の平日勤務日数： '.format(last_month.month) + str(total_data) + '日' + '\n')
        f.write('{}月の土日勤務日数： '.format(last_month.month) + str(total_saturday_data) + '日' + '\n')
        f.write('{}月の平日勤務時間： '.format(last_month.month) + str(total_week_day) + '時間'+ '　x　880円'
              + ' = ' + '{}円'.format(int(calc_salary)) + '\n')
        f.write('{}月の土日勤務時間： '.format(last_month.month) + str(total_saturday) + '時間' + '　x　930円'
              + ' = ' + '{}円'.format(int(calc_saturday_salary)) + '\n')
        f.write('今月のお給料は{}円です'.format(int(calc_salary) + int(calc_saturday_salary)) + '\n')


def maki_san():
    today = date.today()
    last_month = today - relativedelta(months=1)
    main('牧', 880, 930, '給料明細/maki_san.csv')
    msg.showinfo('給料明細', '牧さんの{}月分の給料明細を作成しました'.format(last_month.month))


def yamada_san():
    today = date.today()
    last_month = today - relativedelta(months=1)
    main('山田', 880, 930, '給料明細/yamada_san.csv')
    msg.showinfo('給料明細', '山田さんの{}月分の給料明細を作成しました'.format(last_month.month))


def maeda_san():
    today = date.today()
    last_month = today - relativedelta(months=1)
    main('前田', 880, 930, '給料明細/maeda_san.csv')
    msg.showinfo('給料明細', '前田さんの{}月分の給料明細を作成しました'.format(last_month.month))


def yamamura_san():
    today = date.today()
    last_month = today - relativedelta(months=1)
    main('山村', 880, 930, '給料明細/yamamura_san.csv')
    msg.showinfo('給料明細', '山村さんの{}月分の給料明細を作成しました'.format(last_month.month))


if __name__ == '__main__':
    calc_app()

