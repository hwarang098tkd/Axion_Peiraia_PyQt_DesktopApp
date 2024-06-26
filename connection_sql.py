import os
import pyodbc
from datetime import date


class Connection:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        server = 'diaspeiraia2010.hopto.org'
        #server = '192.168.1.100'
        database = 'Axion'
        try:
            self.cnxn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server +
                ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password +
                ';Trusted_Connection=no', timeout=5)

        except Exception as e:
            msg = "Connection failed"
            print(str(e))

    # ####################################
    def login_connection(self):
        try:
            cursor = self.cnxn.cursor()
            msg = "Connection established"
        except Exception as e:
            msg = "Connection failed"
            print(str(e))

        print("LOGIN: " + str(msg))
        return msg

    def login_members_stats(self):
        result = []
        try:
            query = '''SELECT Sum_Members = count([ID]) FROM [Data] SELECT Sum_Members_TKD = count([ID]) FROM [Data] 
            where SPORT = 'TAEKWON-DO' SELECT Sum_Members_FENCING = count([ID]) FROM [Data] where SPORT = 'FENCING' 
            SELECT Sum_Members_OPLOMAXIA = count([ID]) FROM [Data] where SPORT = 'OPLOMAXIA' '''

            cursor = self.cnxn.cursor()
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

    def login_members_names(self, sport):
        result = []
        result.append("Επιλέξτε Μέλος")
        try:
            if sport != "SPORT":
                query = "SELECT Concat(LAST_NAME,  ' ' , FIRST_NAME) FROM [Data] where SPORT = '" + sport + "' order by LAST_NAME "
            else:
                query = "SELECT Concat(LAST_NAME,  ' ' , FIRST_NAME) FROM [Data] where SPORT = " + sport + " order by LAST_NAME "
            cursor = self.cnxn.cursor()
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

    def member_info(self, name):
        result = []
        rows = []
        try:
            query = "SELECT * FROM [Data] where '" + name + "' =concat(LAST_NAME, ' ',FIRST_NAME) "
            cursor = self.cnxn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            msg = "member_info: Connection established"
        except Exception as e:
            msg = "member_info: Connection failed"
            print("Error: member_info: " + str(e))
        print(str(msg))
        return rows

    def login_presents_stats(self):
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
            cursor = self.cnxn.cursor()
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

    def login_economics_stats(self):
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
            cursor = self.cnxn.cursor()
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

    def login_name_ifexists(self, last_name, first_name, father_name):
        message = ""
        try:
            query = " if exists(SELECT ID FROM [Axion].[dbo].[Data] where LAST_NAME= '" + last_name + "' and FIRST_NAME= '" + first_name + "' and FATHER_NAME='" + father_name + "') select 'exists' else select 'go_to_add' "
            cursor = self.cnxn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            message = rows[0][0]
            msg = "Exists_name: Connection established"
        except Exception as e:
            msg = "Exists_name: Connection failed"
            print("Error: Exists_name: " + str(e))
        print(str(msg))
        return message

    def login_members_add(self, LAST_NAME, FIRST_NAME, FATHER_NAME,
                          MOTHER_NAME, BIRTHDATE, BIRTH_PLACE,
                          NATIONALITY, PROFESSION, ID_NUMBER,
                          ADDRESS_STREET, ADDRESS_NUMBER, REGION,
                          HOME_PHONE, MOTHER_PHONE, FATHER_PHONE,
                          EMAIL, SPORT, DATE_SUBSCRIBE,
                          EMERG_PHONE, BARCODE, CELL_PHONE,
                          BARCODE_1, SPORT_1,
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

            cursor = self.cnxn.cursor()
            cursor.execute(query)
            self.cnxn.commit()
            message = "Επιτυχία καταχώρησης !!!"
            msg = "Add_members: Connection established"
        except Exception as e:
            msg = "Add_members: Connection failed"
            print("Error: Add_members: " + str(e))
            message = "Αποτυχία καταχώρησης"
        print(str(msg))
        return message

    def login_name_delete(self, last_name, first_name,father_name):
        message = ""
        try:
            query = self.str_query('delete_member.sql').format(last_name, first_name,father_name,last_name, first_name,father_name)
            cursor = self.cnxn.cursor()
            cursor.execute(query)
            self.cnxn.commit()
            msg = "Delete_name: Connection established"
            message = "Επιτυχία Διαγραφής"
        except Exception as e:
            msg = "Delete_name: Connection failed"
            message = "Αποτυχία Διαγραφής"
            print("Error: Delete_name: " + str(e))
        print(str(msg))
        return message

    def login_members_updare(self, original_lastName, original_firstName, LAST_NAME, FIRST_NAME, FATHER_NAME,
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

            cursor = self.cnxn.cursor()
            cursor.execute(query)
            self.cnxn.commit()
            message = "Επιτυχία ανανέωσης !!!"
            msg = "Update_members: Connection established"
        except Exception as e:
            msg = "Update_members: Connection failed"
            print("Error: Update_members: " + str(e))
            message = "Αποτυχία ανανέωσης"
        print(str(msg))
        return message

    def login_chart_year_all(self):
        result_all = []
        result_years = []
        result_eco = []
        try:
            query = self.str_query('all_years_econ.sql')
            cursor = self.cnxn.cursor()
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
        return result_all

    def login_chart_oneYear(self, year):
        result_all = []
        result_month = []
        result_eco = []
        list_greek_months = ["Ιαν", "Φεβρ", "Μαρτ", "Απρ", "Μαιος", "Ιουν", "Ιουλ", "Αυγ", "Σεπτ", "Οκτ", "Νοε", "Δεκ"]
        try:
            query = self.str_query('one_year.sql').format(year)
            cursor = self.cnxn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            for i in rows:
                result_month.append(list_greek_months[i[0] - 1])

            result_all.append(result_month)

            while (cursor.nextset()):
                rows = cursor.fetchall()
                result_eco.append(rows[0])

            result_all.append(result_eco)
            msg = "chart_oneYear: Connection established"
        except Exception as e:
            msg = "chart_oneYear: Connection failed"
            print("Error: chart_oneYear: " + str(e))
        print(str(msg))
        return result_all

    def login_list_ofYears(self):
        result = []
        try:
            query = self.str_query('list_ofYears.sql')
            cursor = self.cnxn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            for i in rows:
                result.append(str(i[0]))
            msg = "list_ofYears: Connection established"
        except Exception as e:
            msg = "list_ofYears: Connection failed"
            print("Error: list_ofYears: " + str(e))
        print(str(msg))
        return result

    def login_list_ofMonths(self,year):
        result = []
        try:
            query = self.str_query('list_ofMonths.sql').format(year)
            cursor = self.cnxn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            for i in rows:
                result.append(str(i[0]))
            msg = "list_ofMonths: Connection established"
        except Exception as e:
            msg = "list_ofMonths: Connection failed"
            print("Error: list_ofMonths: " + str(e))
        print(str(msg))
        return result

    def login_economics_categ(self):
        result = []
        gen_cat = []
        sub_cat = []
        try:
            query = self.str_query('economics_categ.sql')
            cursor = self.cnxn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            result.append(rows)
            while (cursor.nextset()):
                rows = cursor.fetchall()
                result.append(rows)
            msg = "economics_categ: Connection established"
        except Exception as e:
            msg = "economics_categ: Connection failed"
            print("Error: economics_categ: " + str(e))
        print(str(msg))
        return result

    def login_get_amount(self, name, cat, sub_cat):
        result = 0
        try:
            query = self.str_query('get_amount.sql').format(name, cat, sub_cat)
            cursor = self.cnxn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            result = str(rows[0][0])
            msg = "get_amount: Connection established"
        except Exception as e:
            msg = "get_amount: Connection failed"
            print("Error: get_amount: " + str(e))
        print(str(msg))
        return result

    def login_sports_list(self):
        result = []
        try:
            query = self.str_query('sports_list.sql')
            cursor = self.cnxn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            result.append("Επιλέξτε...")
            for item in rows:
                result.append(item[0])
            msg = "get_amount: Connection established"
        except Exception as e:
            msg = "get_amount: Connection failed"
            print("Error: get_amount: " + str(e))
        print(str(msg))
        return result

    def login_eco_check(self, name, cat_id, catsub_id, datenew):
        result = ''
        try:
            query = self.str_query('eco_check.sql').format(name, cat_id, catsub_id,cat_id, datenew)
            cursor = self.cnxn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            result = rows[0][0]
            msg = "eco_check: Connection established"
        except Exception as e:
            result = 'error'
            msg = "eco_check: Connection failed"
            print("Error: eco_check: " + str(e))
        print(str(msg))
        return result

    def login_eco_INSERT(self, name, descr, amount, in_out, datenew, cat_id, catsub_id, pos):
        result = ''
        try:
            query = self.str_query('eco_insert.sql').format(name, descr, amount, in_out, datenew, cat_id, catsub_id,cat_id,
                                                            pos)
            cursor = self.cnxn.cursor()
            cursor.execute(query)
            self.cnxn.commit()
            result = "Επιτυχία καταχώρησης !!!"
            msg = "eco_INSERT: Connection established"
        except Exception as e:
            msg = "eco_INSERT: Connection failed"
            result = "Αποτυχία καταχώρησης !!!"
            print("Error: eco_INSERT: " + str(e))
        print(str(msg))
        return result

    def login_eco_UPDATE(self, descr, amount, in_out, pos, name, cat_id, catsub_id, datenew):
        result = ''
        try:
            query = self.str_query('eco_update.sql').format(descr, amount, in_out, pos, name, cat_id, catsub_id, cat_id,
                                                            datenew)
            cursor = self.cnxn.cursor()
            cursor.execute(query)
            self.cnxn.commit()
            result = "Επιτυχία ενημέρωσης !!!"
            msg = "eco_UPDATE: Connection established"
        except Exception as e:
            msg = "eco_UPDATE: Connection failed"
            result = "Αποτυχία ενημέρωσης !!!"
            print("Error: eco_UPDATE: " + str(e))
        print(str(msg))
        return result

    def login_eco_UPDATE_fromTreeview(self,id, descr, amount, in_out, pos, cat_id, catsub_id, datenew):
        try:
            query = self.str_query('eco_updade_fromTree.sql').format(descr, amount, in_out, datenew, cat_id, catsub_id, pos, id)
            cursor = self.cnxn.cursor()
            cursor.execute(query)
            self.cnxn.commit()
            result = "Επιτυχία ενημέρωσης !!!"
            msg = "eco_updade_fromTree: Connection established"
        except Exception as e:
            msg = "eco_updade_fromTree: Connection failed"
            result = "Αποτυχία ενημέρωσης !!!"
            print("Error: eco_updade_fromTree: " + str(e))
        print(str(msg))
        return result

    def eco_data_tree(self):
        result_all = []
        try:
            query = self.str_query('eco_data_tree.sql')
            cursor = self.cnxn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            for i in rows:
                result_all.append(i)
            while (cursor.nextset()):
                rows = cursor.fetchall()
                result_all.append(rows[0])
            msg = "eco_data_tree: Connection established"
        except Exception as e:
            msg = "eco_data_tree: Connection failed"
            print("Error: eco_data_tree: " + str(e))
        print(str(msg))
        return result_all

    def eco_analytics(self, year, month):
        result_all = []
        try:
            query = self.str_query('eco_analytics.sql').format(str(year), str(month))
            cursor = self.cnxn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            for i in rows:
                result_all.append(i)
            while (cursor.nextset()):
                rows = cursor.fetchall()
                result_all.append(rows[0])
            msg = "eco_analytics: Connection established"
        except Exception as e:
            msg = "eco_analytics: Connection failed"
            print("Error: eco_analytics: " + str(e))
        print(str(msg))
        return result_all

    def eco_delete(self, member_id):
        try:
            query = self.str_query('eco_delete.sql').format(str(member_id))
            cursor = self.cnxn.cursor()
            cursor.execute(query)

            msg = "eco_delete: Connection established"
            self.cnxn.commit()
        except Exception as e:
            msg = "eco_delete: Connection failed"
            print("Error: eco_delete: " + str(e))
        print(str(msg))
        return msg

    def login_tkd_treeView(self, year, month, cat_id, subcat_id, active):
        result = []
        try:
            query = self.str_query('tkd_treevieww.sql').format(year, month, cat_id, subcat_id, active)
            cursor = self.cnxn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            result = rows
            msg = "tkd_treeView: Connection established"
        except Exception as e:
            msg = "tkd_treeView: Connection failed"
            print("Error: tkd_treeView: " + str(e))
        print(str(msg))
        return result

    def login_members_treeView(self, sport):
        result = []
        result.append("Επιλέξτε Μέλος")
        try:
            if sport != "SPORT":
                query = "SELECT Active= (select Active from active_members where ID=ID_DATA_active), NAME=Concat([LAST_NAME], ' ',[FIRST_NAME]),id  FROM [Axion].[dbo].[Data] where sport = '" + sport+ "' order by active  desc, name "
            else:
                query = "SELECT Active= (select Active from active_members where ID=ID_DATA_active), NAME=Concat([LAST_NAME], ' ',[FIRST_NAME]),id  FROM [Axion].[dbo].[Data] where sport = " + sport+ " order by active  desc, name "

            cursor = self.cnxn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            result = rows
            msg = "login_members_treeView: Connection established"
        except Exception as e:
            msg = "login_members_treeView: Connection failed"
            print("Error: login_members_treeView: " + str(e))
        print(str(msg))
        return result

    def login_members_activate(self, noActi_memb,acti_mebm):
        result=''
        try:
            query = self.str_query('update_activate_members.sql').format(', '.join(noActi_memb),', '.join(acti_mebm))
            cursor = self.cnxn.cursor()
            cursor.execute(query)

            msg = "update_activate_members: Connection established"
            self.cnxn.commit()
            result = 'Επιτυχής ενημέρωση !'
        except Exception as e:
            msg = "update_activate_members: Connection failed"
            print("Error: update_activate_members: " + str(e))
            result = 'Ανεπιτυχής ενημέρωση !!!'
        print(str(msg))
        return result


    def login_viber_msg(self):
        result = []
        try:
            query = self.str_query('viber_messages.sql')
            cursor = self.cnxn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            result = rows
            msg = "login_viber_msg: Connection established"
        except Exception as e:
            msg = "login_viber_msg: Connection failed"
            print("Error: login_viber_msg: " + str(e))
        print(str(msg))
        return result

    def login_bot_info(self, object):
        result = []
        try:
            query = self.str_query('bot_info.sql').format(object)
            cursor = self.cnxn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            result = rows[0]
            msg = "login_bot_info: Connection established"
        except Exception as e:
            msg = "login_bot_info: Connection failed"
            print("Error: login_bot_info: " + str(e))
        print(str(msg))
        return result

    def login_members_activate_add(self,mode, last_name, first_name, father_name, active):
        result=''
        try:
            if mode == 'insert':
                query = self.str_query('update_activate_members_insert.sql').format(last_name, first_name, father_name, active)
            elif mode == 'update':
                query = self.str_query('update_activate_members_update.sql').format(active,last_name, first_name, father_name)

            cursor = self.cnxn.cursor()
            cursor.execute(query)

            msg = "login_members_activate_add: Connection established"
            self.cnxn.commit()
            result = 'Επιτυχής ενημέρωση !'
        except Exception as e:
            msg = "login_members_activate_add: Connection failed"
            print("Error: login_members_activate_add: " + str(e))
            result = 'Ανεπιτυχής ενημέρωση !!!'
        print(str(msg))
        return result

    def login_bot_info_insert(self, object,object_content):
        result=''
        try:
            query = self.str_query('bot_info_send.sql').format(object_content,object)
            cursor = self.cnxn.cursor()
            cursor.execute(query)

            msg = "login_bot_info_insert: Connection established"
            self.cnxn.commit()
            result = 'Επιτυχής ενημέρωση !'
        except Exception as e:
            msg = "login_bot_info_insert: Connection failed"
            print("Error: login_bot_info_insert: " + str(e))
            result = 'Ανεπιτυχής ενημέρωση !!!'
        print(str(msg))
        return result

    def login_viber_ids(self, list_Id_data):
        result = []
        try:
            query = self.str_query('viber_ids.sql').format(', '.join(list_Id_data))
            cursor = self.cnxn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            result = rows
            msg = "login_viber_ids: Connection established"
        except Exception as e:
            msg = "login_viber_ids: Connection failed"
            print("Error: login_viber_ids: " + str(e))
        print(str(msg))
        return result

    def str_query(self, query):
        home_dir = os.path.abspath('.')
        sql_query = os.path.join(home_dir, 'sql_queries//' + query)
        with open(sql_query, 'r') as file:
            return file.read()
