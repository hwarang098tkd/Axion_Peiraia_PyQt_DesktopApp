SELECT Sport = (select SPORT from data where [ID_DATA]=id)
       ,[ID_DATA]= TRIM((select Concat(LAST_NAME,  ' ' , FIRST_NAME) from data where id = ID_DATA))
      ,TRIM([DESCRIPTION])
      ,[AMOUNT]
      ,[IN_OUT]
      ,[DATENEW]
      ,[CATEG_ID] = TRIM((Select [econ_categ] from econo_categ where id = CATEG_ID ))
      ,[CATEG_SUB_ID] = TRIM((Select econo_subcateg from econo_subcatego where [CATEG_SUB_ID] = ID_CAT ))
      ,[POS]

  FROM [Axion].[dbo].[economics] where year(datenew)= '{}' and MONTH(datenew)='{}' and ID_DATA<>130
  order by Sport desc,DATENEW
