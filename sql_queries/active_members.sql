SELECT NAME=Concat([LAST_NAME], ' ',[FIRST_NAME]),
		Active= (select Active from active_members where ID=ID_DATA_active)
  FROM [Axion].[dbo].[Data] where sport = '{}'

  order by name asc,active