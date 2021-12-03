Declare @id int
Set @id = (SELECT id FROM [Axion].[dbo].[economics] where 
			ID_DATA=(select id from data
					where Concat(LAST_NAME,  ' ' , FIRST_NAME) = '{}') and
			CATEG_ID = (select id from econo_categ
					where trim(econ_categ)='{}') and
			CATEG_SUB_ID = (select ID_CAT from econo_subcatego
					where trim(econo_subcateg)='{}') and
			DATENEW = '{}')
if @id is null 
begin
	Select 'not_exist'
end
else
begin
	select @id
end