from datetime import date
import bs4
import datetime
import pandas as pd
import requests

names = {
    0: 'otherTime',
    1: 'objectName',
    3: 'teacherFirstName',
    4: 'teacherSecondName',
    5: 'cabinetNumber'
}

objectTimes = {
    0: '8:30-10:00',
    1: '10:20-11:50',
    2: '12:25-13:55',
    3: '14:05-15:35',
    4: '15:45-17:00',
}

mnths = {
    1: ['Января', 'Январь'],
    2: ['Февраля', 'Февраль'],
    3: ['Марта', 'Март'],
    4: ['Апреля', 'Апрель'],
    5: ['Мая', 'Май'],
    6: ['Июня', 'Июнь'],
    7: ['Июля', 'Июль'],
    8: ['Августа', 'Август'],
    9: ['Сентября', 'Сентябрь'],
    10: ['Октября', 'Октябрь'],
    11: ['Ноября', 'Ноябрь'],
    12: ['Декабря', 'Декабрь']
}

Response = requests.get('https://tspk.org/studentam/novoe-raspisanie-demo.html')  # Ссылка на сайт
Page = bs4.BeautifulSoup(Response.content, 'html5lib')  # Преобразование страницы в байты
Items = Page.findAll('caption', {'class': 'cal-caption'})  # Поиск по странице месяцев таблиц
ItemTable = Page.findAll('table')  # Поиск всех таблиц

class funcRasp:

    def parsRasp(rasp=None):
        """Парсинг в json файл"""
        if rasp == None:
            return False
        else:
            raspisanie = {}
            for k in range(0, 5):
                if type(rasp[k]) != float:
                    objectName = str()
                    text = rasp[k]
                    ww = text.replace('\n', ' n/ ')
                    words = ww.split()
                    raspisanie[k] = {'time': f'{objectTimes[k]}', 'main': {}}
                    if len(words) == 6:
                        for j in range(0, len(words)):
                            try:
                                float(words[j])
                                raspisanie[k]['main'][f'{names[j]}'] = f'{words[j]}'
                            except:
                                if words[j] != 'n/':
                                    objectName += f'{words[j]} '
                                else:
                                    raspisanie[k]['main'][f'{names[1]}'] = objectName
                                    num = 5
                                    for j in range(1, 4):
                                        raspisanie[k]['main'][f'{names[num]}'] = f'{words[-j]}'  # 1 2 3 // 5 4 3
                                        num = num - 1
                                    break
                    else:
                        for j in range(0, len(words)):
                            try:
                                float(words[j])
                                raspisanie[k]['main'][f'{names[j]}'] = f'{words[j]}'
                            except:
                                if words[j] != 'n/':
                                    objectName += f'{words[j]} '
                                else:
                                    raspisanie[k]['main'][f'{names[1]}'] = objectName
                                    num = 5
                                    for j in range(1, 4):
                                        raspisanie[k]['main'][f'{names[num]}'] = f'{words[-j]}'  # 1 2 3 // 5 4 3
                                        num = num - 1
                                    break
                else:
                    raspisanie[k] = {'time': f'{objectTimes[k]}', 'main': False}
            return raspisanie

    def resRasp(raspUrls=str(), groupName=str(), jOff=False):
        """Получение массива расписания"""
        url = raspUrls.replace('/edit#gid=', '/export?format=csv&gid=')
        df = pd.read_csv(url, on_bad_lines='skip')
        pr = df.to_dict()
        li = list()
        raspLi = list()
        raspLiRes = list()
        for i in pr.keys():
            for j in pr[i]:
                li.append(pr[i][j])
        if groupName in li:
            groupName = groupName
        elif groupName + ' ' in li:
            groupName = groupName + ' '
        elif groupName + ' 2 смена' in li:
            groupName = groupName + ' 2 смена'
        elif groupName + ' 2 смена ' in li:
            groupName = groupName + ' 2 смена '
        else:
            return False
        for line in range(li.index(groupName) + 1, li.index(groupName) + 6):
            raspLi.append(li[line])
        if jOff == False:
            for i in raspLi:
                if type(i) != float:
                    raspLiRes.append(i.split('\n'))
                else:
                    raspLiRes.append(False)
            return raspLiRes
        else:
            return raspLi

    def urlRasp(resdata=date.today()):
        day = int(resdata.strftime('%d'))
        mounth = int(resdata.strftime('%m'))
        year = int(resdata.strftime('%y'))
        now = datetime.datetime.now()
        date_obj = datetime.date(now.year, 6, 30)
        if resdata > date_obj:
            return False
        else:
            pr = {}
            length = 1
            for i in range(0, len(Items) // 2):
                srch = Items[i].get_text()
                if srch.find(str(year)) > -1 & srch.find(mnths[mounth][1]) > -1:
                    aUrls = ItemTable[i].findAll('a')  # Поиск ссылок по айди таблицы
                    for i in aUrls:
                        if i.find('span'):
                            pass
                        else:
                            pr[length] = i.get('href')  # Получение конкретного значения в словарь
                            length += 1
                    if pr[day] == '#norasp':
                        return '#norasp'
                    else:
                        urlId = pr[day].split('/')[-2]
                        return f'https://docs.google.com/spreadsheets/d/{urlId}/edit#gid=0'