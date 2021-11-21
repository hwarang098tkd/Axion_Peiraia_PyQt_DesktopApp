select max(amount) from economics
where ID_DATA= (select id from data
					where Concat(LAST_NAME,  ' ' , FIRST_NAME) = '{}')
and
CATEG_ID =		(select id from econo_categ
					where trim(econ_categ)='{}')
and
CATEG_SUB_ID =  (select id from econo_subcatego
					where trim(econo_subcateg)='{}')

