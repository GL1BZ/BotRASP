import sqlite3

class BotRaspDB:

    def __init__(self, db_file):
        """Инициализация соединения с БД"""
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        """Проверяем есть ли пользователь в БД"""
        result = self.cursor.execute("SELECT `id` FROM `BOT_usersList` WHERE `idUser` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def add_user(self, groupName, user_id, nameUser):
        """Добавление пользователя в БД"""
        if self.cursor.execute("INSERT INTO `BOT_usersList` (`groupName`, `idUser`, `nameUser`) VALUES (?, ?, ?)", (groupName, user_id, nameUser)):
            self.conn.commit()
            return True
        else:
            return False

    def get_user_group(self, user_id):
        """Получаем группу юзера по ID в телеграмме"""
        result = self.cursor.execute("SELECT `groupName` FROM `BOT_usersList` WHERE `idUser` = ?", (user_id,))
        return result.fetchone()[0]

    def change_user_group(self, groupName, user_id):
        """Обновление группы пользователя"""
        if self.cursor.execute("UPDATE `BOT_usersList` SET `groupName` = ? WHERE `idUser` = ?", (groupName, user_id)):
            self.conn.commit()
            return True
        else:
            return False

    def get_user_alertStatus(self, user_id):
        """Получаем статус рассылки юзера по ID в телеграмме"""
        result = self.cursor.execute("SELECT `alertStatus` FROM `BOT_usersList` WHERE `idUser` = ?", (user_id,))
        return result.fetchone()[0]

    def on_user_alertStatus(self, user_id):
        """Включение статуса рассылки пользователя"""
        if self.cursor.execute("UPDATE `BOT_usersList` SET `alertStatus` = ? WHERE `idUser` = ?", (1, user_id)):
            self.conn.commit()
            return True
        else:
            return False

    def off_user_alertStatus(self, user_id):
        """Отключение статуса рассылки пользователя"""
        if self.cursor.execute("UPDATE `BOT_usersList` SET `alertStatus` = ? WHERE `idUser` = ?", (0, user_id)):
            self.conn.commit()
            return True
        else:
            return False

    def close(self):
        """Закрытие соединения с БД"""
        self.conn.close()