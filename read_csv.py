data = []
yobi = ["月", "火", "水", "木", "金", "土", "日"]
with open('timecard.txt', encoding='utf-8') as f:
    for row in f:
        columns = row.rstrip().replace(' : ', '').split(',')
        date = columns[0]
        time = columns[1]
        week_day = columns[2]
        name = columns[3]
        action = columns[-1]
        new_data = str(date) + ',' + str(time) + ',' + week_day + ',' + name + ',' + action
        data.append(new_data)
with open('time_card.txt', 'w', encoding='utf-8') as f:
    for row in data:
        f.write(row + '\n')