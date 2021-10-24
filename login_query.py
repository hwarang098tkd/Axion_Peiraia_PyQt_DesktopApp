import pyodbc
from datetime import date


class connection:
    global server
    global database
    server = 'diaspeiraia2010.hopto.org'
    database = 'Axion'
    ####################################
    global username
    global password
    username = "axion"
    password = "h6945441201"

    ####################################
    def login_connection(self, username, password):
        try:
            username = "axion"
            password = "h6945441201"
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
            username = "axion"
            password = "h6945441201"
            query = '''SELECT Sum_Members = count([ID]) FROM [Data] SELECT Sum_Members_TKD = count([ID]) FROM [Data] 
            where SPORT = 'TAEKWON-DO' SELECT Sum_Members_FENCING = count([ID]) FROM [Data] where SPORT = 'FENCING' 
            SELECT Sum_Members_OPLOMAXIA = count([ID]) FROM [Data] where SPORT = 'OPLOMAXIA' '''
            cnxn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password + ';Trusted_Connection=no', timeout=10)
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

    def login_presents_stats(self, username, password):
        result = []
        try:
            today = date.today()
            d1 = today.strftime("%Y/%m/%d")
            username = "axion"
            password = "h6945441201"
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
            username = "axion"
            password = "h6945441201"
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