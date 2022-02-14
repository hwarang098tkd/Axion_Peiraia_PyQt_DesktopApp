UPDATE [dbo].[economics]
   SET [DESCRIPTION] = '{}'
      ,[AMOUNT] = {}
      ,[IN_OUT] = '{}'
      ,[DATENEW] = '{}'
      ,[CATEG_ID] = (select id from econo_categ where trim(econ_categ)='{}')
      ,[CATEG_SUB_ID] = (select ID_CAT from econo_subcatego where trim(econo_subcateg)='{}')
      ,[POS] = '{}'
 WHERE id = {}