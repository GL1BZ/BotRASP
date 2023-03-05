from datetime import date, timedelta
import bs4
import datetime
import numpy as np
import pandas as pd
import requests

mnths = {
    1: 'Январь',
    2: 'Февраль',
    3: 'Март',
    4: 'Апрель',
    5: 'Май',
    6: 'Июнь',
    7: 'Июль',
    8: 'Август',
    9: 'Сентябрь',
    10: 'Октябрь',
    11: 'Ноябрь',
    12: 'Декабрь',
}

time = {
    1: '8:30-10:00',
    2: '10:20-11:50',
    3: '12:25-13:55',
    4: '14:05-15:35',
    5: '15:45-17:00',
}

ThisYear = date.today().year  # Текущий год
ThisMounth = date.today().month  # Текущий месяц
ThisDay = date.today().day  # Текущий день

Response = requests.get('https://tspk.org/studentam/novoe-raspisanie-demo.html')  # Ссылка на сайт
Page = bs4.BeautifulSoup(Response.content, 'html5lib')  # Преобразование страницы в байты
Items = Page.findAll('caption', {'class': 'cal-caption'})  # Поиск по странице месяцев таблиц
ItemTable = Page.findAll('table')  # Поиск всех таблиц

class BotRasp:

    def raspUrl(resdata=date.today()):
        """Получение ссылки на расписание по дате"""
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
                if srch.find(str(year)) > -1 & srch.find(mnths[mounth]) == 2:
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

    def resRasp(raspUrls=str(), groupName=str()):
        """Получение конечного расписания по ссылке и группе"""
        if raspUrls == '#norasp':
            return False
        else:
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
            for line in range(li.index(groupName)+1, li.index(groupName) + 6):
                raspLi.append(li[line])
            for i in raspLi:
                if type(i) != float:
                    raspLiRes.append(i.replace('\n', ' '))
                else:
                    raspLiRes.append(i)
            return raspLiRes

    def srchRasp(raspUrls=str(), srchName=str()):
        """Поиск в раписании"""
        if srchName == None:
            return False
        elif raspUrls=='#norasp':
            return False
        else:
            url = raspUrls.replace('/edit#gid=', '/export?format=csv&gid=')
            df = pd.read_csv(url, on_bad_lines='skip')
            pr = df.to_dict()
            li = list()
            for i in pr.keys():
                for j in pr[i]:
                    li.append(pr[i][j])
            values = np.array(li)
            srchResult = list()
            for i in range(0, len(values)):
                if srchName in values.item(i):
                    srchResult.append(values.item(i))
            return srchResult

class BotResponce:

    def requestError():
        """Нет расписания"""
        text = ("\n"
                f"&#128195 Что то сломалось...\n"
                f"Попробуй ещё раз!\n"
                "        ")
        return text

    def noRasp():
        """Нет расписания"""
        text = ("\n"
                "&#129302 Похоже расписания нет! \n"
                "&#127881 Можно отдохнуть\n"
                "        ")
        return text

    def noGroup():
        """Нет группы"""
        text = ("\n"
                "&#129302 Похоже что ты не установил свою группу.\n"
                "Установите свою группу с помощью - /setgroup или воспользуйтесь поиском\n"
                "Подробнее - /help\n"
                "        ")
        return text

    def bigDate():
        """Большая дата"""
        text = ("\n"
                    "&#129302 Дата слишком большая, чтобы получить на неё раписание.\n"
                    "Или расписание ещё не добавлено\n"
                    "        ")
        return text

    def alertsOn():
        """Включённая рассылка"""
        text = ("\n"
                    f"&#129302 Ты подключен на ежедневную рассылку раписания!\n"
                    f"Если хочешь, чтобы я перестал - напиши мне <i>/stoprasp</i>\n"
                    "        ")
        return text

    def alertsOff():
        """Выключенная рассылка"""
        text = ("\n"
                    f"&#129302 Ты отключен от ежедневной рассылки расписания(\n"
                    f"Если хочешь, чтобы я начал - напиши мне <i>/startrasp</i>\n"
                    "        ")
        return text

    def alertsStatusOn():
        """Включённая рассылка СТАТУС"""
        text = ("\n"
                f"&#129302 Ты уже подключен на ежедневную рассылку раписания!\n"
                f"Если хочешь, чтобы я перестал - напиши мне <i>/stoprasp</i>\n"
                "        ")
        return text

    def alertsStatusOff():
        """Выключенная рассылка СТАТУС"""
        text = ("\n"
                f"&#129302 Ты уже отключен от ежедневной рассылки расписания(\n"
                f"Если хочешь, чтобы я начал - напиши мне <i>/startrasp</i>\n"
                "        ")
        return text