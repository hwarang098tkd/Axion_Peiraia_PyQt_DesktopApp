Declare @yearss int
Declare @tkd int
Declare @fencing int
Declare @oplo int
Declare @outcomes int
Declare @axion_income int

DECLARE MY_CURSOR CURSOR
  LOCAL STATIC READ_ONLY FORWARD_ONLY
FOR
SELECT DISTINCT DATEPART(yyyy,DATENEW) FROM economics order by YEAR(datenew) desc

--SELECT DISTINCT DATEPART(yyyy,DATENEW) as 'Year' FROM economics order by YEAR(datenew)

OPEN MY_CURSOR
FETCH NEXT FROM MY_CURSOR INTO @yearss
WHILE @@FETCH_STATUS = 0
BEGIN
		Declare @months int
		DECLARE MY_CURSOR1 CURSOR
		  LOCAL STATIC READ_ONLY FORWARD_ONLY
		FOR
		SELECT DISTINCT DATEPART(MM,DATENEW) as 'Month Name' FROM economics  where YEAR(datenew)=@yearss order by MONTH(datenew) desc
			OPEN MY_CURSOR1
			FETCH NEXT FROM MY_CURSOR1 INTO @months
			WHILE @@FETCH_STATUS = 0
			BEGIN

				set @tkd = (Select SUM([AMOUNT]) from economics where MONTH(datenew)=@months AND YEAR(DATENEW)=@yearss and (SELECT SPORT FROM Data WHERE ID=ID_DATA)='TAEKWON-DO')
				if @tkd is NUll
					Set @tkd = 0
				set @fencing = (Select SUM([AMOUNT]) from economics where MONTH(datenew)=@months AND YEAR(DATENEW)=@yearss and (SELECT SPORT FROM Data WHERE ID=ID_DATA)='FENCING')
				if @fencing is NUll
					Set @fencing = 0
				set @oplo = (Select SUM([AMOUNT]) from economics where MONTH(datenew)=@months AND YEAR(DATENEW)=@yearss and (SELECT SPORT FROM Data WHERE ID=ID_DATA)='OPLOMAXIA')
				if @oplo is NUll
					Set @oplo = 0
				set @outcomes = (Select SUM([AMOUNT]) from economics where MONTH(datenew)=@months AND YEAR(DATENEW)=@yearss and IN_OUT='OUTCOME')
				if @outcomes is NUll
					Set @outcomes = 0
				set @axion_income = (Select SUM([AMOUNT]) from economics where MONTH(datenew)=@months AND YEAR(DATENEW)=@yearss and IN_OUT='INCOME' and (SELECT ID FROM Data WHERE ID=ID_DATA)=130)
				if @axion_income is NUll
					Set @axion_income = 0
				select @yearss as 'YEAR', @months as 'MONTH',@tkd as 'TKD',@fencing as 'FENCING',@oplo as 'OPLOMAXIA',@outcomes as 'SPENDS', SUM(@tkd+@fencing+@oplo-@outcomes+@axion_income) as 'Total'
			FETCH NEXT FROM MY_CURSOR1 INTO @months
			END
			CLOSE MY_CURSOR1
			DEALLOCATE MY_CURSOR1


    FETCH NEXT FROM MY_CURSOR INTO @yearss
END
CLOSE MY_CURSOR
DEALLOCATE MY_CURSOR