DELETE FROM [dbo].[active_members]  WHERE [ID_DATA_active]= (SELECT ID FROM DATA where LAST_NAME= '{}' and FIRST_NAME= '{}' and FATHER_NAME= '{}')

DELETE FROM [dbo].[Data] WHERE LAST_NAME= '{}' and FIRST_NAME= '{}' and FATHER_NAME= '{}'

