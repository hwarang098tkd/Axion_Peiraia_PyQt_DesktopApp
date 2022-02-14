SELECT Sport = (select SPORT from data where [ID_DATA]=id)
       ,[ID_DATA]= TRIM((select Concat(LAST_NAME,  ' ' , FIRST_NAME) from data where id = ID_DATA))
      ,[CATEG_ID] = TRIM((Select [econ_categ] from econo_categ where id = CATEG_ID ))
      ,[CATEG_SUB_ID] = TRIM((Select econo_subcateg from econo_subcatego where [CATEG_SUB_ID] = ID_CAT ))
      ,[AMOUNT]
      ,TRIM([DESCRIPTION])
      ,[DATENEW]
      ,[POS]
      ,[ID]
      ,[IN_OUT]






  FROM [Axion].[dbo].[economics] where year(datenew)= '{}' and MONTH(datenew)='{}'
  order by Sport desc,DATENEW
