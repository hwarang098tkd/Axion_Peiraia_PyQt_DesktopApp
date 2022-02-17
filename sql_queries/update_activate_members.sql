UPDATE [dbo].[active_members]
   SET [Active] = 0
 WHERE ID_DATA_active in ({})

UPDATE [dbo].[active_members]
   SET [Active] =1
 WHERE ID_DATA_active in ({})