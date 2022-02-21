INSERT INTO [dbo].[active_members]
           ([ID_DATA_active]
           ,[Active])
     VALUES
           ((SELECT ID FROM DATA where LAST_NAME= '{}' and FIRST_NAME= '{}' and FATHER_NAME= '{}')
           ,{})