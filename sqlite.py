import sqlite3
from datetime import date


class Database:
    def __init__(self, path_to_db="Avtoyordam.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        try:
            if not parameters:
                parameters = ()
            connection = self.connection
            # connection.set_trace_callback(logger)
            cursor = connection.cursor()
            data = None
            cursor.execute(sql, parameters)
            if commit:
                connection.commit()
            if fetchall:
                data = cursor.fetchall()
            if fetchone:
                data = cursor.fetchone()
            connection.close()
            return data

        except Exception as ex:
            print(ex)

    def create_table_users(self):
        sql = """
        CREATE TABLE Users (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            USER_ID int NOT NULL,
            USER_NAME varchar(30) ,
            FIRST_NAME varchar(30),
            LAST_NAME varchar(30),
            PHONE_NUMBER varchar(20),
            USER_LANG varchar(10),
            LAST_STATE varchar(10),
            USER_REG_DATE date,
            USER_INFO varchar(255)
            );
"""
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, user_id: int, user_name: str, first_name: str, last_name: str, last_state: str = "user_lang",
                 user_reg_date: str = date.today()):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO Users(USER_ID, USER_NAME, FIRST_NAME, LAST_NAME, LAST_STATE, USER_REG_DATE) VALUES(?, ?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(user_id, user_name, first_name, last_name, last_state, user_reg_date), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def update_user_lang(self, language, user_id):
        sql = f"""
        UPDATE Users SET last_state="finish", user_lang=? WHERE user_id=?
        """
        return self.execute(sql, parameters=(language, user_id), commit=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)

    def select_all_avtosalon(self, lang):
        sql = f"""
           SELECT name{lang} FROM Avtosalonlar order by id
           """
        return self.execute(sql, fetchall=True)

    def select_one_avtosalon(self, lang, name):
        sql = f"""
           SELECT * FROM Avtosalonlar WHERE name{lang}='{name}'
           """
        return self.execute(sql, fetchone=True)
    #
    def select_all_texosmotr(self, lang):
        sql = f"""
           SELECT name{lang} FROM Texnik_korik order by id
           """
        return self.execute(sql, fetchall=True)

    def select_one_texosmotr(self, lang, name):
        sql = f"""
           SELECT * FROM Texnik_korik WHERE name{lang}='{name}'
           """
        return self.execute(sql, fetchone=True)
    #
    def select_all_straxovka(self, lang):
        sql = f"""
           SELECT name{lang} FROM Avtosugurta order by id
           """
        return self.execute(sql, fetchall=True)

    def select_one_straxovka(self, lang, name):
        sql = f"""
           SELECT * FROM Avtosugurta WHERE name{lang}='{name}'
           """
        return self.execute(sql, fetchone=True)
    # def select_all_gai(self, lang):
    #
    #     sql = f"""
    #        SELECT name{lang} FROM Gaiyhxb order by id
    #        """
    #     print(sql)
    #     return self.execute(sql, fetchall=True)
    #
    def select_all_evakuatr(self, lang):
        sql = f"""
           SELECT name{lang} || ' ' || phone FROM Evokuator order by id
           """
        return self.execute(sql, fetchall=True)

    def select_one_evakuatr(self, lang, name):
        sql = f"""
           SELECT * FROM Evokuator WHERE name{lang}='{name}'
           """
        return self.execute(sql, fetchone=True)

    #
    def select_all_moyka(self, lang):
        sql = f"""
           SELECT * FROM Avtomoyka order by id
           """
        return self.execute(sql, fetchall=True)

    def select_one_moyka(self, lang, name):
        sql = f"""
           SELECT * FROM Avtomoyka name{lang}='{name}'
           """
        return self.execute(sql, fetchone=True)
    #
    def select_all_moysam(self, lang):
        sql = f"""
           SELECT * FROM MoySam order by id
           """
        return self.execute(sql, fetchall=True)

    def select_one_moysam(self, lang, name):
        sql = f"""
           SELECT * FROM MoySam name{lang}='{name}'
           """
        return self.execute(sql, fetchone=True)


    def select_all_servis(self):
        sql = f"""
           SELECT * FROM Avtoservis
           """
        return self.execute(sql, fetchall=True)

    def select_one_servis(self, lang, name):
        sql = f"""
           SELECT * FROM Avtoservis name{lang}='{name}'
           """
        return self.execute(sql, fetchone=True)

    def select_all_tuning(self):
        sql = f"""
           SELECT * FROM tuning
           """
        return self.execute(sql, fetchall=True)

    def select_one_tuning(self, lang, name):
        sql = f"""
           SELECT * FROM tuning name{lang}='{name}'
           """
        return self.execute(sql, fetchone=True)

#
    def select_all_shinomontaj(self):
        sql = f"""
           SELECT * FROM Vulkanizatsiya
           """
        return self.execute(sql, fetchall=True)

    def select_one_shinomontaj(self, lang, name):
        sql = f"""
           SELECT * FROM Vulkanizatsiya name{lang}='{name}'
           """
        return self.execute(sql, fetchone=True)
#
    def select_all_masla(self):
        sql = f"""
           SELECT * FROM Zamenamasla
           """
        return self.execute(sql, fetchall=True)

    def select_one_masla(self, lang, name):
        sql = f"""
           SELECT * FROM Zamenamasla name{lang}='{name}'
           """
        return self.execute(sql, fetchone=True)
    #
    def select_one_gai(self, tumanid):
        sql = f"""
           SELECT * FROM Gaiyhxb WHERE tumanid={tumanid}
           """
        return self.execute(sql, fetchone=True)

    #
    def select_all_tuman(self, lang, hududid):
        sql = f"""
           SELECT name{lang} FROM Tuman WHERE hududid={hududid} order by id
           """
        return self.execute(sql, fetchall=True)

    def select_one_tuman(self, lang, name):

        sql = f"""
           SELECT id FROM Tuman WHERE name{lang}='{name}'
           """
        return self.execute(sql, fetchone=True)


    def select_all_hudud(self, lang):
        sql = f"""
           SELECT name{lang} FROM Hudud order by id
           """
        return self.execute(sql, fetchall=True)

    def select_one_hudud(self, lang, name):

        sql = f"""
           SELECT id FROM Hudud WHERE name{lang}='{name}'
           """
        return self.execute(sql, fetchone=True)

    def select_all_zapravka(self, oil_type):
        sql = f"""
              SELECT * FROM Avtozapravka WHERE oil_type='{oil_type}'
              """
        return self.execute(sql, fetchall=True)

    def select_all_zapravkatuman(self, oil_type, tumanid):
        sql = f"""
              SELECT * FROM Avtozapravka WHERE oil_type='{oil_type}' and tumanid={tumanid}
              """
        return self.execute(sql, fetchall=True)





    def update_user_state(self, state, user_id):
        sql = f"""
        UPDATE Users SET last_state=? WHERE user_id=?
        """
        return self.execute(sql,  parameters=(state, user_id), commit=True)

    def get_user_state(self, user_id):
        sql = f"""
                  SELECT last_state, USER_LANG FROM users WHERE user_id=? 
                  """
        return self.execute(sql, parameters=(user_id,),  fetchone=True)

