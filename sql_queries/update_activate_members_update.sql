
UPDATE [dbo].[active_members]
   SET [Active] = {}
 WHERE [ID_DATA_active]= (SELECT ID FROM DATA where LAST_NAME= '{}' and FIRST_NAME= '{}' and FATHER_NAME= '{}')