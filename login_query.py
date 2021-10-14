import pyodbc


class connection:

    def login_connection(self, username, password):
        try:
            server = 'diaspeiraia2010.hopto.org'
            database = 'Axion'
            username="axion"
            password="h6945441201"
            cnxn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password,
                timeout=10)
            cursor = cnxn.cursor()
            msg = "Connection established"
        except Exception as e:
            msg = "Connection failed"

        print(str(msg))
        return msg
