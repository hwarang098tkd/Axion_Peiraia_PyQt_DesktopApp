--cant use print statment in this form of query
Declare @yearss int
DECLARE MY_CURSOR CURSOR 
  LOCAL STATIC READ_ONLY FORWARD_ONLY
FOR 
SELECT DISTINCT DATEPART(yyyy,DATENEW) FROM economics order by YEAR(datenew)

SELECT DISTINCT DATEPART(yyyy,DATENEW) FROM economics order by YEAR(datenew)

OPEN MY_CURSOR
FETCH NEXT FROM MY_CURSOR INTO @yearss
WHILE @@FETCH_STATUS = 0
BEGIN
	Select 
		SUM(CASE
		when TRIM(IN_OUT)='INCOME' then  [AMOUNT]
		when  TRIM(IN_OUT)='OUTCOME' then [AMOUNT]*(-1)
		END)
	from economics where YEAR(datenew)=@yearss
    FETCH NEXT FROM MY_CURSOR INTO @yearss
END
CLOSE MY_CURSOR
DEALLOCATE MY_CURSOR