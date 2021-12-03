INSERT INTO [dbo].[economics]
           ([ID_DATA],[DESCRIPTION],[AMOUNT],[IN_OUT],[DATENEW],[CATEG_ID],[CATEG_SUB_ID],[POS])
     VALUES
           ((select id from data where Concat(LAST_NAME,  ' ' , FIRST_NAME) = '{}'),
           '{}',{},'{}','{}',
           (select id from econo_categ where trim(econ_categ)='{}'),
           (select ID_CAT from econo_subcatego where trim(econo_subcateg)='{}'),
           '{}')