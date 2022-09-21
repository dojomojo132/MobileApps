import sqlite3
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screenmanager import MDScreenManager


class WindowManager(MDScreenManager):

    def check_init(self, root, user_login, user_password, status_check):

        with sqlite3.connect("server.db") as db:
            cursor = db.cursor()

            query = """
            CREATE TABLE IF NOT EXISTS users(
                login VARCHAR(15),
                password INTEGER(5)    
            )
            """

            cursor.executescript(query)

        global login
        login = user_login.text
        password = user_password.text


        try:
            cursor.execute("SELECT login FROM users WHERE login = ?", [login])
            if cursor.fetchone() is None:
                status_check.text = "Логин не существует"
                status_check.theme_text_color =  "Custom"
                status_check.text_color = 1,0,0,1

                # print("Такой логин не существует!")
            else:
                cursor.execute("SELECT password FROM users WHERE login = ? AND password = ?", [login, password])
                if cursor.fetchone() is None:
                    status_check.text = "Пароль неверный"
                    status_check.theme_text_color = "Custom"
                    status_check.text_color = 1, 0, 0, 1
                    print("Пароль неверный!")
                else:
                    user_login.text = ""
                    user_password.text = ""
                    status_check.text = ""
                    root.current = "menu_window"
                    print("Вы зашли под учетной записью ", login)

        except sqlite3.Error as e:
            print("Error", e)
        finally:
            cursor.close()
            db.close()

    def print_text(self, user):

        user.text = "Текущий пользователь: " + login

    def check_root(self, root, status):

        if login != "admin":
            status.text = "У вас недостаточно прав доступа"
            status.theme_text_color = "Custom"
            status.text_color = 1, 0, 0, 1

        else:
            root.current = "admin_window"


    def registration(self, root, login, password, status):
        add_user_login = login.text
        add_user_password = password.text
        if add_user_login == "":
            status.text = "Заполните логин"
            status.theme_text_color = "Custom"
            status.text_color = 1, 0, 0, 1
        else:
            if add_user_password == "":
                status.text = "Заполните пароль"
                status.theme_text_color = "Custom"
                status.text_color = 1, 0, 0, 1
            else:
                try:
                    db = sqlite3.connect("server.db")
                    cursor = db.cursor()

                    values = [add_user_login, add_user_password]

                    cursor.execute("SELECT login FROM users WHERE login = ?", [add_user_login])
                    if cursor.fetchone() is None:
                        cursor.execute("INSERT INTO users(login, password) VALUES(?, ?)", values)
                        db.commit()
                        status.text = "Пользователь успешно добавлен"
                        status.text_color = 1, 0, 0, 1
                    else:
                        status.text = "Пользователь уже существует"
                        status.theme_text_color = "Custom"
                        status.text_color = 1, 0, 0, 1
                except sqlite3.Error as e:
                    print("Error", e)
                finally:
                    cursor.close()
                    db.close()

    def login_menu(self, root, status):
        status.text = ""
        root.current = "login_window"

    def main_menu(self, root, login, password, status):
        login.text = ""
        password.text = ""
        status.text = ""
        root.current = "menu_window"


class WWPApp(MDApp):

    def build(self):
        Builder.load_file('wwpapp.kv')
        return WindowManager()

if __name__ == '__main__':
    WWPApp().run()