--cant use print statment in this form of query
Declare @yearss int
Declare @MONTH int
Declare @MONTHname VARCHAR(max)
Declare @tkd int
Declare @fencing int
Declare @oplo int
Declare @outcomes int
set @yearss = {}

DECLARE MY_CURSOR CURSOR
  LOCAL STATIC READ_ONLY FORWARD_ONLY
FOR
SELECT DISTINCT DATEPART(MM,DATENEW) FROM economics where YEAR(datenew)= @yearss order by month(datenew)

SELECT DISTINCT DATEPART(MM,DATENEW) FROM economics where YEAR(datenew)= @yearss order by month(datenew)

OPEN MY_CURSOR
FETCH NEXT FROM MY_CURSOR INTO @MONTH
WHILE @@FETCH_STATUS = 0
BEGIN
	set @MONTHname = DateName( month , DateAdd( month , @MONTH , 0 ) - 1 )
	set @tkd = (Select SUM([AMOUNT]) from economics where MONTH(datenew)=@MONTH AND YEAR(DATENEW)=@yearss and (SELECT SPORT FROM Data WHERE ID=ID_DATA)='TAEKWON-DO')
	set @fencing = (Select SUM([AMOUNT]) from economics where MONTH(datenew)=@MONTH AND YEAR(DATENEW)=@yearss and (SELECT SPORT FROM Data WHERE ID=ID_DATA)='FENCING')
	set @oplo = (Select SUM([AMOUNT]) from economics where MONTH(datenew)=@MONTH AND YEAR(DATENEW)=@yearss and (SELECT SPORT FROM Data WHERE ID=ID_DATA)='OPLOMAXIA')
	set @outcomes = (Select SUM([AMOUNT]) from economics where MONTH(datenew)=@MONTH AND YEAR(DATENEW)=@yearss and IN_OUT='OUTCOME')
	Select TKD= @tkd,FENCING = @fencing,OPLOMAXIA = @oplo,EXODA = @outcomes

    FETCH NEXT FROM MY_CURSOR INTO @MONTH
END
CLOSE MY_CURSOR