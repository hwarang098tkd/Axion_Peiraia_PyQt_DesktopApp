DECLARE @year int
DECLARE @month int
DECLARE @cat_id int
DECLARE @subcat_id int
DECLARE @active int

SET @year = '{}'
SET @month = '{}'
SET @cat_id = {}
SET @subcat_id = {}
SET @active = {}

SELECT case  when (select AMOUNT from economics where dbo.economics.ID_DATA =dbo.Data.ID and year(datenew)=@year and month(datenew)=@month and CATEG_ID=@cat_id and CATEG_SUB_ID=@subcat_id ) >0 then  'PAID'
						when (select AMOUNT from economics where dbo.economics.ID_DATA =dbo.Data.ID and year(datenew)=@year and month(datenew)=@month and CATEG_ID=@cat_id and CATEG_SUB_ID=@subcat_id ) is null  then 'NOT PAID' end as OK
        ,NAME=Concat([LAST_NAME], ' ',[FIRST_NAME])
      ,[PAY_DAY]
	  ,PAID_AMOUNT = (select AMOUNT from economics where dbo.economics.ID_DATA =dbo.Data.ID and year(datenew)=@year and month(datenew)=@month and CATEG_ID=@cat_id and CATEG_SUB_ID=@subcat_id )
	  ,PAID_DATE = (select DATENEW from economics where dbo.economics.ID_DATA =dbo.Data.ID and year(datenew)=@year and month(datenew)=@month and CATEG_ID=@cat_id and CATEG_SUB_ID=@subcat_id )
	  ,ID


	  FROM [Axion].[dbo].[Data]

  where (select Active from active_members where ID=ID_DATA_active)=@active and SPORT='TAEKWON-DO'

  order by PAID_AMOUNT desc, PAY_DAY desc