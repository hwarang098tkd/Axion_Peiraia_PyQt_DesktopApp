import os

import pyodbc
from datetime import date


class connection:
    global server
    global database
    server = 'diaspeiraia2010.hopto.org'
    database = 'Axion'

    # ####################################
    def login_connection(self, username, password):
        try:
            cnxn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server +
                ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password +
                ';Trusted_Connection=no', timeout=10)
            cursor = cnxn.cursor()
            msg = "Connection established"
        except Exception as e:
            msg = "Connection failed"
            print(str(e))

        print("LOGIN: " + str(msg))
        return msg

    def login_members_stats(self, username, password):
        result = []
        try:
            query = '''SELECT Sum_Members = count([ID]) FROM [Data] SELECT Sum_Members_TKD = count([ID]) FROM [Data] 
            where SPORT = 'TAEKWON-DO' SELECT Sum_Members_FENCING = count([ID]) FROM [Data] where SPORT = 'FENCING' 
            SELECT Sum_Members_OPLOMAXIA = count([ID]) FROM [Data] where SPORT = 'OPLOMAXIA' '''
            cnxn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password + ';Trusted_Connection=no',
                timeout=10)
            cursor = cnxn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            result.append(rows[0][0])
            while (cursor.nextset()):
                rows = cursor.fetchall()
                result.append(rows[0][0])
            msg = "Members: Connection established"
        except Exception as e:
            msg = "Members: Connection failed"
            print("Error: Members: " + str(e))
        print(str(msg))
        return result

    def login_members_names(self, username, password, sport):
        result = []
        result.append("Επιλέξτε Μέλος")
        try:
            if sport != "SPORT":
                query = "SELECT Concat(LAST_NAME,  ' ' , FIRST_NAME) FROM [Data] where SPORT = '" + sport + "' order by LAST_NAME "
            else:
                query = "SELECT Concat(LAST_NAME,  ' ' , FIRST_NAME) FROM [Data] where SPORT = " + sport + " order by LAST_NAME "

            cnxn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password + ';Trusted_Connection=no',
                timeout=10)
            cursor = cnxn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            for i in rows:
                result.append(i[0])
            msg = "Members names: Connection established"
        except Exception as e:
            msg = "Members names: Connection failed"
            print("Error: Members names: " + str(e))
        print(str(msg))
        return result

    def member_info(self, username, password, name):
        result = []
        try:
            query = "SELECT * FROM [Data] where '" + name + "' =concat(LAST_NAME, ' ',FIRST_NAME) "
            cnxn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password + ';Trusted_Connection=no',
                timeout=10)
            cursor = cnxn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            msg = "member_info: Connection established"
        except Exception as e:
            msg = "member_info: Connection failed"
            print("Error: member_info: " + str(e))
        print(str(msg))
        return rows

    def login_presents_stats(self, username, password):
        result = []
        try:
            today = date.today()
            d1 = today.strftime("%Y/%m/%d")
            query = '''SELECT SUMPRESE = count([ID])
                FROM [Axion].[dbo].[PRESENTERS]  where DATENEW=' ''' + d1 + ''' '  
                SELECT TAEKWONDO = count([ID])
                FROM [Axion].[dbo].[PRESENTERS]  where DATENEW=' ''' + d1 + ''' ' and SPORT='TAEKWON-DO'
                SELECT FENCING = count([ID])
                FROM [Axion].[dbo].[PRESENTERS]  where DATENEW=' ''' + d1 + ''' ' and SPORT='FENCING'
                SELECT OPLOMAXIA=count([ID])
                FROM [Axion].[dbo].[PRESENTERS]  where DATENEW=' ''' + d1 + ''' ' and SPORT='OPLOMAXIA' '''
            cnxn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password,
                timeout=10)
            cursor = cnxn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            result.append(rows[0][0])
            while (cursor.nextset()):
                rows = cursor.fetchall()
                result.append(rows[0][0])
            msg = "Presents: Connection established"
        except Exception as e:
            msg = "Presents: Connection failed"
            print("Error: Presents: " + str(e))
        print(str(msg))
        return result

    def login_economics_stats(self, username, password):
        result = []
        try:
            today = date.today()
            d1 = today.strftime("%Y/%m/%d")
            query = ''' SELECT  SUM= SUM (CASE WHEN IN_OUT='INCOME' THEN  AMOUNT ELSE AMOUNT*-1 END )
                        FROM [Axion].[dbo].[economics] where month(datenew)=MONTH(getdate()) and year(datenew)=year(getdate()) 
                        SELECT TAEK = SUM (CASE WHEN IN_OUT='INCOME' THEN AMOUNT ELSE 0 END )
                        FROM [Axion].[dbo].[economics] where month(datenew)=MONTH(getdate()) and year(datenew)=year(getdate()) and (SELECT SPORT FROM Data WHERE ID_DATA=ID)='TAEKWON-DO'
                        SELECT FENCING = SUM (CASE WHEN IN_OUT='INCOME' THEN AMOUNT ELSE 0 END )
                        FROM [Axion].[dbo].[economics] where month(datenew)=MONTH(getdate()) and year(datenew)=year(getdate()) and (SELECT SPORT FROM Data WHERE ID_DATA=ID)='FENCING'
                        
                        SELECT OPLOMAXIA = SUM (CASE WHEN IN_OUT='INCOME' THEN  AMOUNT ELSE 0 END )
                        FROM [Axion].[dbo].[economics] where month(datenew)=MONTH(getdate()) and year(datenew)=year(getdate()) and (SELECT SPORT FROM Data WHERE ID_DATA=ID)='OPLOMAXIA'
                        
                        SELECT EXODA = SUM (AMOUNT)
                        FROM [Axion].[dbo].[economics] where month(datenew)=MONTH(getdate()) and year(datenew)=year(getdate()) and  IN_OUT='OUTCOME' '''
            cnxn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password,
                timeout=10)
            cursor = cnxn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            result.append(rows[0][0])
            while (cursor.nextset()):
                rows = cursor.fetchall()
                result.append(rows[0][0])
            msg = "Econ: Connection established"
        except Exception as e:
            msg = "Econ: Connection failed"
            print("Error: Econ: " + str(e))
        print(str(msg))
        return result

    def login_name_ifexists(self, username, password, last_name, first_name, father_name):
        message = ""
        try:
            query = " if exists(SELECT ID FROM [Axion].[dbo].[Data] where LAST_NAME= '" + last_name + "' and FIRST_NAME= '" + first_name + "' and FATHER_NAME='" + father_name + "') select 'exists' else select 'go_to_add' "
            cnxn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username
                + ';PWD=' + password,
                timeout=10)
            cursor = cnxn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            message = rows[0][0]
            msg = "Exists_name: Connection established"
        except Exception as e:
            msg = "Exists_name: Connection failed"
            print("Error: Exists_name: " + str(e))
        print(str(msg))
        return message

    def login_members_add(self, username, password, LAST_NAME, FIRST_NAME, FATHER_NAME,
                          MOTHER_NAME,
                          BIRTHDATE,
                          BIRTH_PLACE,
                          NATIONALITY,
                          PROFESSION,
                          ID_NUMBER,
                          ADDRESS_STREET,
                          ADDRESS_NUMBER,
                          REGION,
                          HOME_PHONE,
                          MOTHER_PHONE,
                          FATHER_PHONE,
                          EMAIL,
                          SPORT,
                          DATE_SUBSCRIBE,
                          EMERG_PHONE,
                          BARCODE,
                          CELL_PHONE,
                          BARCODE_1,
                          SPORT_1,
                          PAY_DAY):
        message = ""
        try:
            query = "INSERT INTO [Axion].[dbo].[Data] ([LAST_NAME],[FIRST_NAME],[FATHER_NAME],[MOTHER_NAME],[BIRTHDATE]" \
                    ",[BIRTH_PLACE],[NATIONALITY],[PROFESSION],[ID_NUMBER],[ADDRESS_STREET],[ADDRESS_NUMBER],[REGION],[HOME_PHONE]" \
                    ",[MOTHER_PHONE],[FATHER_PHONE],[EMAIL],[SPORT],[DATE_SUBSCRIBE],[EMERG_PHONE],[BARCODE],[CELL_PHONE]" \
                    ",[BARCODE_1],[SPORT_1],[PAY_DAY])" \
                    " VALUES ('" + LAST_NAME + "', '" + FIRST_NAME + "','" + FATHER_NAME + "','" + MOTHER_NAME + "','" + BIRTHDATE + "','" + BIRTH_PLACE + "','" + NATIONALITY + "'," \
                                                                                                                                                                                 "'" + PROFESSION + "','" + ID_NUMBER + "','" + ADDRESS_STREET + "','" + ADDRESS_NUMBER + "','" + REGION + "','" + HOME_PHONE + "','" + MOTHER_PHONE + "','" + FATHER_PHONE + "'," \
                                                                                                                                                                                                                                                                                                                                                              "'" + EMAIL + "','" + SPORT + "','" + DATE_SUBSCRIBE + "','" + EMERG_PHONE + "','" + BARCODE + "','" + CELL_PHONE + "','" + BARCODE_1 + "','" + SPORT_1 + "','" + PAY_DAY + "')"

            cnxn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password,
                timeout=10)
            cursor = cnxn.cursor()
            cursor.execute(query)
            cnxn.commit()
            message = "Επιτυχία καταχώρησης !!!"
            msg = "Add_members: Connection established"
        except Exception as e:
            msg = "Add_members: Connection failed"
            print("Error: Add_members: " + str(e))
            message = "Αποτυχία καταχώρησης"
        print(str(msg))
        return message

    def login_name_delete(self, username, password, last_name, first_name):
        message = ""
        try:
            query = "DELETE FROM [dbo].[Data] WHERE LAST_NAME= '" + last_name + "' and FIRST_NAME= '" + first_name + "'"
            cnxn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username
                + ';PWD=' + password,
                timeout=10)
            cursor = cnxn.cursor()
            cursor.execute(query)
            cnxn.commit()
            msg = "Delete_name: Connection established"
            message = "Επιτυχία Διαγραφής"
        except Exception as e:
            msg = "Delete_name: Connection failed"
            message = "Αποτυχία Διαγραφής"
            print("Error: Delete_name: " + str(e))
        print(str(msg))
        return message

    def login_members_updare(self, username, password, original_lastName, original_firstName, LAST_NAME, FIRST_NAME, FATHER_NAME,
                          MOTHER_NAME,
                          BIRTHDATE,
                          BIRTH_PLACE,
                          NATIONALITY,
                          PROFESSION,
                          ID_NUMBER,
                          ADDRESS_STREET,
                          ADDRESS_NUMBER,
                          REGION,
                          HOME_PHONE,
                          MOTHER_PHONE,
                          FATHER_PHONE,
                          EMAIL,
                          SPORT,
                          DATE_SUBSCRIBE,
                          EMERG_PHONE,
                          BARCODE,
                          CELL_PHONE,
                          BARCODE_1,
                          SPORT_1,
                          PAY_DAY):
        message = ""
        try:
            query = "UPDATE [dbo].[Data] SET [LAST_NAME] = '" + LAST_NAME + "',[FIRST_NAME] =  '" + FIRST_NAME + "',[FATHER_NAME] = '" + FATHER_NAME + "',[MOTHER_NAME] = '" + MOTHER_NAME + "'" \
                  ",[BIRTHDATE] = '" + BIRTHDATE + "',[BIRTH_PLACE] = '" + BIRTH_PLACE + "',[NATIONALITY] = '" + NATIONALITY + "',[PROFESSION] = '" + PROFESSION + "',[ID_NUMBER] = '" + ID_NUMBER + "'" \
                  ",[ADDRESS_STREET] = '" + ADDRESS_STREET + "',[ADDRESS_NUMBER] = '" + ADDRESS_NUMBER + "',[REGION] = '" + REGION + "',[HOME_PHONE] = '" + HOME_PHONE + "',[MOTHER_PHONE] = '" + MOTHER_PHONE + "'" \
                  ",[FATHER_PHONE] = '" + FATHER_PHONE + "',[EMAIL] = '" + EMAIL + "',[SPORT] ='" + SPORT + "',[DATE_SUBSCRIBE] = '" + DATE_SUBSCRIBE + "',[EMERG_PHONE] = '" + EMERG_PHONE + "'" \
                  ",[BARCODE] = '" + BARCODE + "',[CELL_PHONE] = '" + CELL_PHONE + "',[BARCODE_1] = '" + BARCODE_1 + "',[SPORT_1] = '" + SPORT_1 + "', [PAY_DAY] ='" + PAY_DAY + "' WHERE LAST_NAME= '" + original_lastName + "' and FIRST_NAME= '" + original_firstName + "'"

            cnxn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password,
                timeout=10)
            cursor = cnxn.cursor()
            cursor.execute(query)
            cnxn.commit()
            message = "Επιτυχία ανανέωσης !!!"
            msg = "Update_members: Connection established"
        except Exception as e:
            msg = "Update_members: Connection failed"
            print("Error: Update_members: " + str(e))
            message = "Αποτυχία ανανέωσης"
        print(str(msg))
        return message

    def login_chart_year_all(self, username, password):
        result_all = []
        result_years = []
        result_eco = []
        home_dir = os.path.abspath('')
        sql_query = os.path.join(home_dir, 'sql_queries/all_years_econ.txt')
        print("Path of query: ", sql_query)
        try:
            with open(sql_query, 'r') as file:
                query = file.read()
            #print(query)
            cnxn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password + ';Trusted_Connection=no',
                timeout=10)
            cursor = cnxn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            for i in rows:
                result_years.append(str(i[0]))
            result_all.append(result_years)
            while (cursor.nextset()):
                rows = cursor.fetchall()
                result_eco.append(rows[0][0])
            result_all.append(result_eco)
            msg = "chart_year_all: Connection established"
        except Exception as e:
            msg = "chart_year_all: Connection failed"
            print("Error: chart_year_all: " + str(e))
        print(str(msg))
        print(result_all)
        return result_all