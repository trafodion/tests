# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2014-2015 Hewlett-Packard Development Company, L.P.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# @@@ END COPYRIGHT @@@

from ...lib import hpdci
from ...lib import gvars
import defs

_testmgr = None
_testlist = []
_dci = None

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""Datetime function DDL"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =====================  Begin Test Case Header  ===================
    # Test case name	: Arkt1422:  testa000
    # Description		: Datetime function DDL
    # Test case inputs	:
    # Test case outputs	:
    # Expected Results	: (provided a high-level description)
    #
    # Notes:
    # DAYNAME(<date-exp>)  : returns name of the day of week ( Sunday, Monday)
    # MONTHNAME(<date-exp>): returns month name ( January, February,..)
    # DAYOFYEAR(<date-exp>): returns day of year in <date> in range 1 to 366
    # WEEK(<date-exp>)     : returns week of year in <date> in range 1 to 53
    # QUARTER(<date-exp>)  : returns quarter in <date> in range 1 to 4
    # <datetime-field>(<date-exp>)
    #			: extracts the <datetime-field> from <date>.
    #		          Field should be YEAR, MONTH, DAY,... SECOND
    
    stmt = """drop table DAYTAB;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE DAYTAB(
d_t_m_e	TIMESTAMP  	NO DEFAULT NOT NULL,
d_n 		CHAR(10)	NO DEFAULT NOT NULL,
m_n		VARCHAR(10)	NO DEFAULT NOT NULL,
d_of_y   	INTEGER      	NO DEFAULT NOT NULL,
w_k 		SMALLINT 	NO DEFAULT NOT NULL,
q_r 		SMALLINT 	NO DEFAULT NOT NULL,
year_d		INT		NO DEFAULT NOT NULL,
month_d	SMALLINT	NO DEFAULT NOT NULL,
day_d		SMALLINT 	NO DEFAULT NOT NULL,
hour_d		SMALLINT	NO DEFAULT NOT NULL,
minute_d	SMALLINT	NO DEFAULT NOT NULL,
second_d	INT		NO DEFAULT NOT NULL
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Default format
    stmt = """INSERT INTO DAYTAB VALUES(
TIMESTAMP  '1901-10-10 23:15:00.300000',
DAYNAME   (date '1989-01-11'),
MONTHNAME (date '1976-10-31'),
DAYOFYEAR (date '1920-01-01'),
WEEK      (date '2040-12-31'),
QUARTER   (date '2000-01-01'),
YEAR	  (date '1945-05-06'),
MONTH     (date '1936-08-10'),
DAY	  (date '2000-12-31'),
HOUR	  (timestamp '1718-01-10 12:50:59.400000'),
MINUTE    (timestamp '0001-01-01 01:59:50.400000'),
SECOND    (timestamp '1210-11-11 11:01:00.999999')
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # US format
    stmt = """INSERT INTO DAYTAB VALUES(
TIMESTAMP  '12/31/1999 23:59:59.999999',
DAYNAME   (date '05/01/1989'),
MONTHNAME (date '01/31/1956'),
DAYOFYEAR (date '12/31/2001'),
WEEK      (date '01/01/1998'),
QUARTER   (date '06/30/1900'),
YEAR	  (date '05/06/0001'),
MONTH     (date '07/10/1936'),
DAY	  (date '02/28/1951'),
HOUR	  (timestamp '01/10/0718 12:50:59.999 pm'),
MINUTE    (timestamp '01/01/0001 01:59:50.000001 am'),
SECOND    (timestamp '11/11/1210 11:01:59.999910')
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # European format
    stmt = """INSERT INTO DAYTAB VALUES(
TIMESTAMP '13.12.0001 00.00.00.000000',
DAYNAME   (date '11.01.1989'),
MONTHNAME (date '31.10.1976'),
DAYOFYEAR (date '01.01.1920'),
WEEK      (date '21.09.2000'),
QUARTER   (date '01.10.2000'),
YEAR	  (date '13.05.1945'),
MONTH     (date '10.10.1946'),
DAY	  (date '29.02.1996'), -- leap year
HOUR      (timestamp '10.01.1718 00.50.58.400000'),
MINUTE    (timestamp '01.01.0001 01.00.50.400000'),
SECOND    (timestamp '11.11.1210 11.01.40.590000')
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # Use timestamp as date-expression
    stmt = """INSERT INTO DAYTAB VALUES(
TIMESTAMP  '1901-05-10 15:19:59.300000',
DAYNAME   (timestamp '1918-10-11 10:00:09.999930'),
MONTHNAME (timestamp '1876-01-31 07:59:05.000000'),
DAYOFYEAR (timestamp '0001-01-01 23:59:59.999999'),
WEEK      (timestamp '1999-04-03 23:59:59.999999'),
QUARTER   (timestamp '1191-09-30 23:59:59.999999'),
YEAR	  (timestamp '2106-01-01 00:00:00.000001'),
MONTH     (timestamp '1433-04-10 22:22:22.222222'),
DAY	  (timestamp '1945-03-31 12:50:59.400000'),
HOUR	  (time '12:50:59.400000'),
MINUTE    (time '23:59:59.999999'),
SECOND    (time '00:00:01.000000')
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    _testmgr.testcase_end(desc)

def test002(desc="""DAYNANE function positive tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =====================  Begin Test Case Header  ======================
    # Test case name: 	Arkt1422:  testa001
    # Description:		DAYNANE function positive tests
    # Test case inputs:
    # Test case outputs:
    # Expected Results:	(provided a high-level description)
    #
    # Notes:
    # The DAYNAME function returns name of the day of week(Sunday, Monday...)
    #
    
    stmt = """SELECT *  from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", 'a001s0')
    
    #  SELECT, WHERE tests
    stmt = """SELECT DAYNAME(d_t_m_e)
from DAYTAB 
where DAYNAME(d_t_m_e) = 'Friday';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", 'a001s1')
    
    #  08/15/00 EL  Took out the comment and add GROUP BY for testing HAVING.
    #  HAVING, LIKE tests
    stmt = """SELECT DAYNAME(d_t_m_e)
from DAYTAB 
group by d_t_m_e
having dayname(d_t_m_e) = 'Monday'
or
dayname(d_t_m_e) like '%day%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", 'a001s2')
    
    #  Subqueries tests
    stmt = """SELECT DAYNAME(d_t_m_e)
from DAYTAB 
where year_d > 100
order by
d_n
READ COMMITTED ACCESS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", 'a001s3')
    
    # Create view vday for join, union all
    
    stmt = """CREATE VIEW vday AS SELECT *
FROM DAYTAB 
WITH CHECK OPTION;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Within/Upon the VIEW tests
    stmt = """INSERT INTO vday VALUES(
TIMESTAMP  '1990-10-05 15:19:59.900000',
DAYNAME   (timestamp '1918-05-11 10:00:09.999930'),
MONTHNAME (timestamp '1876-01-31 07:59:05.000000'),
DAYOFYEAR (timestamp '2000-01-01 00:00:00.000001'),
WEEK      (timestamp '1999-12-31 23:59:59.999999'),
QUARTER   (timestamp '1191-09-30 23:59:59.999999'),
YEAR      (timestamp '2106-07-01 00:00:00.000001'),
MONTH     (timestamp '1433-08-10 22:22:22.222222'),
DAY       (timestamp '1945-03-31 12:50:59.400000'),
HOUR      (time '12:50:59.400000'),
MINUTE    (time '23:59:59.999999'),
SECOND    (time '00:00:01.000000')
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  UNION ALL, CAST tests
    stmt = """SELECT MONTHNAME(d_t_m_e)
from DAYTAB 
UNION ALL
SELECT MONTHNAME(CAST(d_t_m_e AS DATE))
from vday 
group by
w_k, d_t_m_e
having  w_k <= 53;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", 'a001s4')
    
    #  String concatenation test
    stmt = """SELECT d_n || ' CONCAT ' || DAYNAME (d_t_m_e)
from vday;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", 'a001s5')
    
    #  JOIN tests
    stmt = """SELECT DAYTAB.d_n, vday.d_n
from 	    DAYTAB 
INNER JOIN    vday 
ON  DAYTAB.d_n =  vday.d_n;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", 'a001s6')
    
    stmt = """SELECT DAYTAB.d_n, vday.d_n
from 	   DAYTAB 
LEFT JOIN    vday 
ON  DAYTAB.d_n =  vday.d_n;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", 'a001s7')
    
    stmt = """SELECT DAYTAB.d_n, vday.d_n
from 	    DAYTAB 
RIGHT JOIN    vday 
ON  DAYTAB.d_n =  vday.d_n;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", 'a001s8')
    
    #  INDEX keys tests
    stmt = """CREATE INDEX idx1 on vday(d_n);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1127')
    
    stmt = """SELECT 	d_n
from  DAYTAB 
order by	d_n;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", 'a001s10')
    
    #  CASE test
    stmt = """SELECT d_n, m_n, w_k, q_r, DAYNAME(d_t_m_e),
CASE DAYNAME(d_t_m_e)
WHEN 'Sunday' 	THEN 'It is Sunday!'
WHEN 'Monday' 	THEN 'It is Monday!'
WHEN 'Tuesday' 	THEN 'It is Tuesday!'
WHEN 'Wendnesday' 	THEN 'It is Wendnesday!'
WHEN 'Thursday' 	THEN 'It is Thursday!'
WHEN 'Friday' 	THEN 'It is Friday!'
WHEN 'Saturday' 	THEN 'It is Saturday!'
ELSE NULL
END
FROM DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", 'a001s11')
    
    # UPDATE test
    stmt = """UPDATE vday 
set d_t_m_e = CURRENT_TIMESTAMP
where DAYNAME(d_t_m_e) = 'October';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 0)
    
    # DELETE test
    stmt = """DELETE from vday 
where d_t_m_e = CURRENT_TIMESTAMP;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    _testmgr.testcase_end(desc)

def test003(desc="""MONTHNANE function positive tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =====================  Begin Test Case Header  ====================
    # Test case name:      Arkt1422: testa002
    # Description:		MONTHNANE function positive tests
    # Test case inputs:
    # Test case outputs:
    # Expected Results:	(provided a high-level description)
    #
    # Notes:
    # The MONTHNAME function returns name of the month of year(Janurary, Feburary...)
    #
    
    stmt = """SELECT *  from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002exp""", 'a002s0')
    
    #  SELECT, WHERE tests
    stmt = """SELECT MONTHNAME(d_t_m_e)
from DAYTAB 
where MONTHNAME(d_t_m_e) = 'December';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002exp""", 'a002s1')
    
    #  08/15/00 EL  Took out the comment and add GROUP BY for testing HAVING.
    # HAVING, LIKE tests
    stmt = """SELECT MONTHNAME(d_t_m_e), m_n
from DAYTAB 
group by d_t_m_e, m_n
having m_n = 'January'
and
monthname(d_t_m_e) like '%mber';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    #  Subqueries, EXTRACT tests
    stmt = """SELECT MONTHNAME(d_t_m_e)
from DAYTAB 
where q_r > 1
order by
q_r
Read Uncommitted Access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002exp""", 'a002s2')
    
    # Create view vmonth for join, union all
    
    stmt = """CREATE VIEW vMONTH AS SELECT *
from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Within/Upon the VIEW tests
    stmt = """INSERT INTO vMONTH VALUES(
TIMESTAMP  '1990-10-05 15:19:59.300000',
DAYNAME   (timestamp '1918-05-11 10:00:09.999930'),
MONTHNAME (timestamp '1876-01-31 07:59:05.000000'),
DAYOFYEAR (timestamp '2000-01-01 00:00:00.000001'),
WEEK      (timestamp '1999-12-31 23:59:59.999999'),
QUARTER   (timestamp '1191-09-30 23:59:59.999999'),
YEAR	  (timestamp '2106-07-01 00:00:00.000001'),
MONTH     (timestamp '1433-08-10 22:22:22.222222'),
DAY	  (timestamp '1945-03-31 12:50:59.400000'),
HOUR	  (time '12:50:59.400000'),
MINUTE    (time '23:59:59.999999'),
SECOND    (time '00:00:01.0000')
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  Juliantimestamp, Converttimestamp tests
    stmt = """SELECT d_t_m_e, MONTHNAME(CONVERTTIMESTAMP(JULIANTIMESTAMP(d_t_m_e)))
from vMONTH;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002exp""", 'a002s3')
    
    #  UNION ALL, CAST, GROUP BY, HAVING tests
    stmt = """SELECT MONTHNAME(d_t_m_e)
from DAYTAB 
UNION ALL
SELECT MONTHNAME(CAST( d_t_m_e AS date))
from vMONTH 
group by
q_r, d_t_m_e
having  q_r >= 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002exp""", 'a002s4')
    
    #  String concat test
    # #expectfile ${test_dir}/a002exp a002s5
    stmt = """SELECT m_n || ' CONCAT ' || MONTHNAME(d_t_m_e)
from vMONTH;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 6)
    
    #  JOIN tests
    stmt = """SELECT DAYTAB.m_n, vMONTH.m_n
from 	    DAYTAB 
INNER JOIN    vMONTH 
ON  DAYTAB.m_n =  vMONTH.m_n;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002exp""", 'a002s6')
    
    stmt = """SELECT DAYTAB.m_n, vMONTH.m_n
from 	   DAYTAB 
LEFT JOIN    vMONTH 
ON  DAYTAB.m_n =  vMONTH.m_n;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002exp""", 'a002s7')
    
    stmt = """SELECT DAYTAB.m_n, vMONTH.m_n
from 	    DAYTAB 
RIGHT JOIN    vMONTH 
ON  DAYTAB.m_n =  vMONTH.m_n;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002exp""", 'a002s8')
    
    #  INDEX keys tests
    stmt = """CREATE INDEX idx1 on vMONTH(m_n);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1127')
    
    stmt = """SELECT 	m_n
from  DAYTAB 
order by	m_n;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002exp""", 'a002s10')
    
    #  CASE test
    stmt = """SELECT d_n, m_n, w_k, q_r,
CASE
WHEN  MONTHNAME(d_t_m_e) = 'January'  THEN 'First month.'
WHEN  MONTHNAME(d_t_m_e) = 'December' THEN 'Last month.'
ELSE ' With the year.'
END
FROM DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002exp""", 'a002s11')
    
    # UPDATE test
    stmt = """UPDATE vMONTH 
set d_t_m_e = cast(CURRENT_DATE as Timestamp)
where MONTHNAME(d_t_m_e) = 'January';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 0)
    
    # DELETE test
    stmt = """DELETE from vMONTH 
where d_t_m_e = CURRENT_TIMESTAMP;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    # Cleanup view vmonth
    # DELETE from vmonth;
    stmt = """DROP view vMONTH;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test004(desc="""DAYOFYEAR function positive tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =====================  Begin Test Case Header  ======================
    # Test case name: 	Arkt1422:  testa003
    # Description:		DAYOFYEAR function positive tests
    # Test case inputs:
    # Test case outputs:
    # Expected Results:	(provided a high-level description)
    #
    # Notes:
    # The DAYOFYEAR function returns number of the DAYOFYEAR of year(1,2...,366/365)
    #
    
    stmt = """SELECT *  from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003exp""", 'a003s0')
    
    #  SELECT, WHERE tests
    stmt = """SELECT DAYOFYEAR(d_t_m_e)
from DAYTAB 
where d_of_y > 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003exp""", 'a003s1')
    
    #  08/15/00 EL  Took out the comment and add GROUP BY for testing HAVING.
    #  HAVING, LIKE tests
    stmt = """SELECT DAYOFYEAR(d_t_m_e)
from DAYTAB 
group by d_t_m_e, d_n
having dayofyear(d_t_m_e) in (283, 300, 498, 500, 347)
or
cast(dayofyear(d_t_m_e) as varchar(3)) like 'aaa' or
cast(dayofyear(d_t_m_e) as varchar(3)) like '130' or
cast(dayofyear(d_t_m_e) as varchar(3)) like '365' or
cast(dayofyear(d_t_m_e) as varchar(3)) like 'put';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003exp""", 'a003s1a')
    
    #  Subqueries, EXTRACT tests
    stmt = """SELECT  EXTRACT( DAY from d_t_m_e)
from DAYTAB 
where d_of_y > 100
order by d_of_y;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003exp""", 'a003s2')
    
    # Create view vdofyear for join, union all
    
    stmt = """CREATE VIEW vdofyear AS SELECT *
FROM DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Within/Upon the VIEW tests
    stmt = """INSERT INTO vdofyear VALUES(
TIMESTAMP   '1990-10-05 15:19:59.300000',
DAYNAME   	(timestamp '1918-05-11 10:00:09.999930'),
MONTHNAME 	(timestamp '1876-01-31 07:59:05.000000'),
DAYOFYEAR 	(timestamp '2000-01-01 00:00:00.000001'),
WEEK	        (timestamp '1999-12-31 23:59:59.999999'),
QUARTER   	(timestamp '1191-09-30 23:59:59.999999'),
YEAR	    	(timestamp '2106-07-01 00:00:00.000001'),
MONTH     	(timestamp '1433-08-10 22:22:22.222222'),
DAY	    	(timestamp '1945-03-31 12:50:59.400000'),
HOUR	    	(time '12:50:59.400000'),
MINUTE    	(time '23:59:59.999999'),
SECOND   	(time '00:00:01.000000')
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  UNION ALL, CAST tests
    stmt = """SELECT DAYOFYEAR(d_t_m_e)
from DAYTAB 
UNION ALL
SELECT DAYOFYEAR(CAST(d_t_m_e AS DATE)) + YEAR(d_t_m_e) --AS Newcol
from vdofyear 
group by
q_r, d_t_m_e;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003exp""", 'a003s3')
    
    #  JOIN tests
    stmt = """SELECT DAYTAB.d_of_y, vdofyear.d_of_y
from 	        DAYTAB 
INNER JOIN    vdofyear 
ON  DAYTAB.d_of_y =  vdofyear.d_of_y;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003exp""", 'a003s4')
    
    stmt = """SELECT DAYTAB.d_of_y, vdofyear.d_of_y
from 	   DAYTAB 
LEFT JOIN    vdofyear 
ON  DAYTAB.d_of_y =  vdofyear.d_of_y;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003exp""", 'a003s5')
    
    stmt = """SELECT DAYTAB.d_of_y, vdofyear.d_of_y
from 	    DAYTAB 
RIGHT JOIN    vdofyear 
ON  DAYTAB.d_of_y =  vdofyear.d_of_y;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003exp""", 'a003s6')
    
    #  INDEX keys tests
    stmt = """CREATE INDEX idx1 on vdofyear(d_of_y);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1127')
    
    stmt = """SELECT 		d_of_y
from 	 DAYTAB 
order by	d_of_y;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003exp""", 'a003s8')
    
    #  Cleanup index
    stmt = """DROP index idx1;"""
    output = _dci.cmdexec(stmt)
    
    # 08/15/00 EL  Took out the comment for testing.
    # CASE, Leapyear test
    stmt = """SELECT d_n, m_n, d_of_y, w_k, q_r,
CASE
WHEN  dayofyear(d_t_m_e) <= 30 THEN dayofyear(d_t_m_e) * 100
WHEN  dayofyear(d_t_m_e) > 30  THEN dayofyear(d_t_m_e) + 100
WHEN  dayofyear(d_t_m_e) < 90  THEN dayofyear(d_t_m_e)
ELSE NULL
END
FROM DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003exp""", 'a003s8a')
    
    # UPDATE test
    stmt = """UPDATE vdofyear 
set d_of_y = DAYOFYEAR ( CURRENT_DATE)
where d_of_y = 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 0)
    
    # DELETE test
    stmt = """DELETE from vdofyear 
where d_of_y = DAYOFYEAR (CURRENT_DATE );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    # Cleanup view vdofyear
    # DELETE from vdofyear;
    stmt = """DROP view vdofyear;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test005(desc="""WEEK function positive tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # ===============  Begin Test Case Header  ==================
    # Test case name: 	Arkt1422:  testa004
    # Description:		WEEK function positive tests
    # Test case inputs:
    # Test case outputs:
    # Expected Results:	(provided a high-level description)
    #
    # Notes:
    # The WEEK function returns number of the week of year(1,2...,52)
    #
    
    stmt = """SELECT *  from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a004exp""", 'a004s0')
    
    #  SELECT, WHERE tests
    stmt = """SELECT WEEK(d_t_m_e)
from DAYTAB 
where w_k > 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a004exp""", 'a004s1')
    
    #  08/15/00 EL  Took out the comment and add GROUP BY for testing HAVING.
    # HAVING, LIKE tests
    stmt = """SELECT d_t_m_e, WEEK(d_t_m_e)
from DAYTAB 
group by d_t_m_e, d_n
having week(d_t_m_e) in (1, 3, 5, 7, 9, 11, 13, 15, 17, 19,
21, 23, 25, 27, 29, 31, 33, 35, 37, 39,
41, 43, 45, 47, 49, 50, 51, 52)
or
cast(week(d_t_m_e) as varchar(2)) like '53'
order by d_t_m_e desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a004exp""", 'a004s1a')
    
    # Subqueries, CAST tests
    stmt = """SELECT WEEK( CAST( timestamp'0001-01-01 00:00:01.000001' AS date) )
from DAYTAB 
where w_k in(10,50);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # Create view vweek for join, union all
    
    stmt = """CREATE VIEW vweek AS SELECT *
FROM DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Within/Upon the VIEW tests
    stmt = """INSERT INTO vweek VALUES(
TIMESTAMP  '1990-10-05 15:19:59.300000',
DAYNAME   (timestamp '1918-05-11 10:00:09.999930'),
MONTHNAME (timestamp '1876-01-31 07:59:05.000000'),
DAYOFYEAR (timestamp '2000-01-01 00:00:00.000001'),
WEEK      (timestamp '1999-12-31 23:59:59.999999'),
QUARTER   (timestamp '1191-09-30 23:59:59.999999'),
YEAR	    (timestamp '2106-07-01 00:00:00.000001'),
MONTH     (timestamp '1433-08-10 22:22:22.222222'),
DAY	    (timestamp '1945-03-31 12:50:59.400000'),
HOUR	    (time '12:50:59.400000'),
MINUTE    (time '23:59:59.999999'),
SECOND    (time '00:00:01.000000')
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  UNION ALL, EXTRACT tests
    stmt = """SELECT WEEK(d_t_m_e)
from DAYTAB 
UNION ALL
SELECT EXTRACT(YEAR from d_t_m_e) + YEAR(d_t_m_e)
from vweek 
group by
q_r, d_t_m_e;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a004exp""", 'a004s2')
    
    #  08/15/00 EL  Took out the comment and modified query for testing.
    #  String concat and current_timestamp function test
    #  Depend on the season the result was generated
    #  the test result only correct 1/4 of the time
    # #expectfile ${test_dir}/a004exp a004s2a
    stmt = """SELECT concat(m_n || CAST (CURRENT_TIMESTAMP AS CHAR(21)) || ' ',
cast(week(current_date) as varchar(19))),
d_n
from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 8)
    
    #  JOIN tests
    stmt = """SELECT DAYTAB.w_k, vweek.w_k
from 	    DAYTAB 
INNER JOIN    vweek 
ON  DAYTAB.w_k =  vweek.w_k;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a004exp""", 'a004s3')
    
    stmt = """SELECT DAYTAB.w_k, vweek.w_k
from 	   DAYTAB 
LEFT JOIN    vweek 
ON  DAYTAB.w_k =  vweek.w_k;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a004exp""", 'a004s4')
    
    stmt = """SELECT DAYTAB.w_k, vweek.w_k
from 	    DAYTAB 
RIGHT JOIN    vweek 
ON  DAYTAB.w_k =  vweek.w_k;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a004exp""", 'a004s5')
    
    #  INDEX keys tests
    stmt = """CREATE INDEX idx1 on vweek(w_k);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1127')
    
    stmt = """SELECT 		w_k
from 	 DAYTAB 
order by	w_k;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a004exp""", 'a004s7')
    
    #  Cleanup index
    stmt = """DROP index idx1;"""
    output = _dci.cmdexec(stmt)
    
    #  CASE test
    stmt = """SELECT DAYNAME(d_t_m_e), MONTHNAME(d_t_m_e), DAYOFYEAR(d_t_m_e), QUARTER(d_t_m_e),
CASE QUARTER(d_t_m_e)
WHEN 1 THEN 'FIRST  QUARTER'
WHEN 2 THEN 'SECOND QUARTER'
WHEN 3 THEN 'THIRD  QUARTER'
WHEN 4 THEN 'FORTH  QUARTER'
ELSE NULL
END
FROM DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a004exp""", 'a004s9')

    # TRAFODION
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output);

    # UPDATE test
    stmt = """UPDATE vweek 
set w_k = WEEK ( CURRENT_DATE )
where w_k < 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    
    # DELETE test
    stmt = """DELETE from vweek 
where w_k = WEEK ( CURRENT_DATE );"""
    output = _dci.cmdexec(stmt)
    # TRAFODION: we only know that there are at least 2 rows from the previous
    # update, but we don't know if there are any preexsting rows that have the
    # same week as the CURRENT_DATE.  It really depends on when you run the
    # test. 
    _dci.expect_deleted_msg(output)

    # TRAFODION
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # TRAFODION now delete the 2 rows from the view (and the table) so that
    # the tests after would have the same intended table to work with.
    stmt = """DELETE from vweek where w_k < 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)

    # Cleanup view vweek
    # DELETE from vweek;
    stmt = """DROP view vweek;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test006(desc="""quarter function positive tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # ====================  Begin Test Case Header  ====================
    # Test case name: 	Arkt1422:  testa005
    # Description:		quarter function positive tests
    # Test case inputs:
    # Test case outputs:
    # Expected Results:	(provided a high-level description)
    #
    # Notes:
    # The QUARTER function returns number of the quarter of year(1,2,3,4)
    #
    
    stmt = """SELECT *  from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a005exp""", 'a005s0')
    
    #  SELECT, WHERE tests
    stmt = """SELECT QUARTER(d_t_m_e)
from DAYTAB 
where q_r <= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a005exp""", 'a005s1')
    
    #  08/15/00 EL  Took out the comment and modified query for testing HAVING.
    #  HAVING, LIKE tests
    stmt = """SELECT d_t_m_e, QUARTER(d_t_m_e), max(d_n), min(m_n)
from DAYTAB 
where QUARTER(d_t_m_e) > 2
group by d_t_m_e, d_n, m_n
having Quarter(d_t_m_e) in
(9, 10, 2, 5, 7, 8, 1, 23, 87, 4, 183, 832, 3)
or
cast(Quarter(d_t_m_e) as char(3)) like '%1%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a005exp""", 'a005s1a')
    
    stmt = """INSERT INTO DAYTAB VALUES(
TIMESTAMP  '1901-05-10 15:19:59.300000',
DAYNAME   (timestamp '1918-10-11 10:00:09.999930'),
MONTHNAME (timestamp '1876-01-31 07:59:05.000000'),
DAYOFYEAR (timestamp '0001-01-01 23:59:59.999999'),
WEEK      (timestamp '1999-04-03 23:59:59.999999'),
QUARTER   (timestamp '1191-09-30 23:59:59.999999'),
YEAR      (timestamp '2106-01-01 00:00:00.000001'),
MONTH     (timestamp '1433-04-10 22:22:22.222222'),
DAY       (timestamp '1945-03-31 12:50:59.400000'),
HOUR      (time '12:50:59.400000'),
MINUTE    (time '23:59:59.999999'),
SECOND    (time '00:00:01.000000')
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  08/15/00 EL  Took out the comment for testing.
    #  Subqueries, EXTRACT tests
    stmt = """SELECT  EXTRACT(YEAR from timestamp '0001-01-01 00:00:01.000001')
from DAYTAB 
where d_n Like (select d_n
from DAYTAB 
where Quarter(d_t_m_e) = 2)
order by d_n
READ UNCOMMITTED ACCESS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a005exp""", 'a005s2')
    
    stmt = """delete from DAYTAB 
where cast(d_t_m_e as char(30)) = '1901-05-10 15:19:59.300000';"""
    output = _dci.cmdexec(stmt)
    
    # Create view vQUARTER for join, union all
    
    stmt = """CREATE VIEW vQUARTER AS SELECT *
FROM DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Within/Upon the VIEW tests
    stmt = """INSERT INTO vQUARTER VALUES(
TIMESTAMP  '1990-10-05 15:19:59.300000',
DAYNAME   (timestamp '1918-05-11 10:00:09.999930'),
MONTHNAME (timestamp '1876-01-31 07:59:05.000000'),
DAYOFYEAR (timestamp '2000-01-01 00:00:00.000001'),
WEEK      (timestamp '1999-12-31 23:59:59.999999'),
QUARTER   (timestamp '1191-09-30 23:59:59.999999'),
YEAR	    (timestamp '2106-07-01 00:00:00.000001'),
MONTH     (timestamp '1433-08-10 22:22:22.222222'),
DAY	    (timestamp '1945-03-31 12:50:59.400000'),
HOUR	    (time '12:50:59.400000'),
MINUTE    (time '23:59:59.999999'),
SECOND    (time '00:00:01.000000')
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  UNION ALL, CAST tests
    stmt = """SELECT QUARTER(d_t_m_e)
from DAYTAB 
UNION ALL
SELECT QUARTER(CAST(d_t_m_e AS DATE)) + QUARTER(d_t_m_e)
from vQUARTER 
group by
w_k, d_t_m_e;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a005exp""", 'a005s3')
    
    #  JOIN tests
    stmt = """SELECT DAYTAB.q_r, vQUARTER.q_r
from 	    DAYTAB 
INNER JOIN    vQUARTER 
ON  DAYTAB.q_r =  vQUARTER.q_r;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a005exp""", 'a005s4')
    
    stmt = """SELECT DAYTAB.q_r, vQUARTER.q_r
from 	   DAYTAB 
LEFT JOIN    vQUARTER 
ON  DAYTAB.q_r =  vQUARTER.q_r;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a005exp""", 'a005s5')
    
    stmt = """SELECT DAYTAB.q_r, vQUARTER.q_r
from 	    DAYTAB 
RIGHT JOIN    vQUARTER 
ON  DAYTAB.q_r =  vQUARTER.q_r;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a005exp""", 'a005s6')
    
    #  INDEX keys tests
    stmt = """CREATE INDEX idx1 on vQUARTER(q_r);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1127')
    
    stmt = """SELECT 		q_r
from 	 DAYTAB 
order by	q_r;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a005exp""", 'a005s8')
    
    #  Cleanup index
    stmt = """DROP index idx1;"""
    output = _dci.cmdexec(stmt)
    
    #  CASE test
    stmt = """SELECT d_n, m_n, d_of_y, w_k, q_r,
CASE q_r
WHEN 1 THEN 'FIRST  QUARTER'
WHEN 2 THEN 'SECOND QUARTER'
WHEN 3 THEN 'THIRD  QUARTER'
WHEN 4 THEN 'FORTH  QUARTER'
ELSE NULL
END
FROM DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a005exp""", 'a005s10')
    
    # UPDATE test
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """UPDATE vQUARTER 
set q_r = QUARTER ( CURRENT_DATE )
where q_r < 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    # DELETE test
    # The result depend on the CURRENT_DATE !!!
    stmt = """DELETE from vQUARTER 
where q_r = QUARTER ( CURRENT_DATE );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """DELETE from vQUARTER where q_r < 3;"""
    output = _dci.cmdexec(stmt)
    
    # Cleanup view vQUARTER
    # DELETE from vQUARTER;
    stmt = """DROP view vQUARTER;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test007(desc="""YEAR function positive tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # ===================  Begin Test Case Header  ====================
    # Test case name: 	Arkt1422:  testa006
    # Description:		YEAR function positive tests
    # Test case inputs:
    # Test case outputs:
    # Expected Results:	(provided a high-level description)
    #
    # Notes:
    # The YEAR function extracts the year from <date-exp>,
    #					returns year(0001, 9999...)
    #
    
    stmt = """SELECT *  from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a006exp""", 'a006s0')
    
    #  SELECT, WHERE tests
    stmt = """SELECT YEAR(d_t_m_e)
from DAYTAB 
where year_d > 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a006exp""", 'a006s1')
    
    #  08/16/00 EL  Took out the comment and modified query for testing HAVGING.
    #  HAVING, LIKE tests
    stmt = """SELECT YEAR(d_t_m_e)
from DAYTAB 
where YEAR(d_t_m_e) = 1990 or
YEAR(d_t_m_e) = 0001 or
YEAR(d_t_m_e) = 1901
group by d_t_m_e
having max(year(d_t_m_e)) in (2000, 3432, 1001, 1999, 1901, 1990, 0001)
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a006exp""", 'a006s1a')
    
    #  Subqueries, EXTRACT tests
    stmt = """SELECT  EXTRACT(YEAR from d_t_m_e)
from DAYTAB 
where year_d < 2000
order by year_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a006exp""", 'a006s2')
    
    # Create view vyear for join, union all
    
    stmt = """CREATE VIEW vyear AS SELECT *
FROM DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Within/Upon the VIEW tests
    stmt = """INSERT INTO vyear VALUES(
TIMESTAMP  '1990-10-05 15:19:59.300000',
DAYNAME   (timestamp '1918-05-11 10:00:09.999930'),
MONTHNAME (timestamp '1876-01-31 07:59:05.000000'),
DAYOFYEAR (timestamp '2000-01-01 00:00:00.000001'),
WEEK      (timestamp '1999-12-31 23:59:59.999999'),
QUARTER   (timestamp '1191-09-30 23:59:59.999999'),
YEAR	    (timestamp '2106-07-01 00:00:00.000001'),
MONTH     (timestamp '1433-08-10 22:22:22.222222'),
DAY	    (timestamp '1945-03-31 12:50:59.400000'),
HOUR	    (time '12:50:59.400000'),
MINUTE    (time '23:59:59.999999'),
SECOND    (time '00:00:01.000000')
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  UNION ALL, CAST tests
    stmt = """SELECT YEAR(d_t_m_e)
from DAYTAB 
UNION ALL
SELECT YEAR(CAST(d_t_m_e AS DATE)) + YEAR(d_t_m_e)
from vyear 
group by
year_d, d_t_m_e;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a006exp""", 'a006s3')
    
    #  JOIN tests
    stmt = """SELECT DAYTAB.year_d, vyear.year_d
from 	    DAYTAB 
INNER JOIN    vyear 
ON  DAYTAB.year_d  =  vyear.year_d ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a006exp""", 'a006s4')
    
    stmt = """SELECT DAYTAB.year_d , vyear.year_d    

from 	   DAYTAB 
LEFT JOIN    vyear 
ON  DAYTAB.year_d  =  vyear.year_d ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a006exp""", 'a006s5')
    
    stmt = """SELECT DAYTAB.year_d , vyear.year_d
from 	    DAYTAB 
RIGHT JOIN    vyear 
ON  DAYTAB.year_d  =  vyear.year_d ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a006exp""", 'a006s6')
    
    #  INDEX keys tests
    stmt = """CREATE INDEX idx1 on vyear(year_d);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1127')
    
    ##expectfile ${test_dir}/a006exp a006s7
    stmt = """SELECT 		year_d
from 	 DAYTAB 
order by	year_d;"""
    output = _dci.cmdexec(stmt)
    
    #  Cleanup index
    stmt = """DROP index idx1;"""
    output = _dci.cmdexec(stmt)
    
    # 08/16/00 EL  Took out the comment and modified query for testing.
    # CASE test
    stmt = """SELECT d_t_m_e, d_n, m_n, d_of_y, w_k, q_r,year_d,
CASE year(d_t_m_e)
WHEN 1990 THEN year(d_t_m_e)
WHEN 0001 THEN day(d_t_m_e)
WHEN 1956 THEN year(d_t_m_e)
WHEN 1976 THEN day(d_t_m_e)
ELSE NULL
END
FROM DAYTAB 
group by d_t_m_e, d_n, m_n, d_of_y, w_k, q_r, year_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a006exp""", 'a006s8')
    
    # UPDATE test
    stmt = """UPDATE vyear 
set year_d = YEAR (CURRENT_TIMESTAMP)
where year_d  < 100 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 0)
    
    # DELETE test
    stmt = """DELETE from vyear 
where year_d = YEAR( CURRENT_TIMESTAMP );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    # Cleanup view vyear
    # DELETE from vyear;
    stmt = """DROP view vyear;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test008(desc="""MONTH function positive tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # ====================  Begin Test Case Header ===================
    # Test case name:	Arkt1422:  testa007
    # Description:		MONTH function positive tests
    # Test case inputs:
    # Test case outputs:
    # Expected Results:	(provided a high-level description)
    #
    # Notes:
    # The MONTH function extracts the month from <date-exp>,
    #				 returns month(1,2...12)
    #
    
    stmt = """SELECT *  from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a007exp""", 'a007s0')
    
    #  SELECT, WHERE tests
    stmt = """SELECT MONTH(d_t_m_e)
from DAYTAB 
where month_d < 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a007exp""", 'a007s1')
    
    #  08/16/00 EL  Took out the comment and modified query for testing HAVING.
    #  HAVING, LIKE tests
    stmt = """SELECT MONTH(d_t_m_e), upper(dayname(d_t_m_e)), d_n
from DAYTAB 
where MONTH(d_t_m_e) > 5
group by d_t_m_e, d_n
having month(d_t_m_e) = (select month(d_t_m_e)
from DAYTAB 
where month(d_t_m_e) = 5
)
or
upper(dayname(d_t_m_e)) like '%RID%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a007exp""", 'a007s1a')
    
    #  Subqueries,  EXTRRACT tests
    stmt = """SELECT  EXTRACT( month from d_t_m_e )
from DAYTAB 
-- 	where month_d > 10
order by month_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a007exp""", 'a007s2')
    
    # Create view vMONTH for join, union all
    
    stmt = """CREATE VIEW vMONTH AS SELECT *
FROM DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Within/Upon the VIEW tests
    stmt = """INSERT INTO vMONTH VALUES(
TIMESTAMP  '1990-10-05 15:19:59.300000',
DAYNAME   (timestamp '1918-05-11 10:00:09.999930'),
MONTHNAME (timestamp '1876-01-31 07:59:05.000000'),
DAYOFYEAR (timestamp '2000-01-01 00:00:00.000001'),
WEEK      (timestamp '1999-12-31 23:59:59.999999'),
QUARTER   (timestamp '1191-09-30 23:59:59.999999'),
YEAR	    (timestamp '2106-07-01 00:00:00.000001'),
MONTH     (timestamp '1433-08-10 22:22:22.222222'),
DAY	    (timestamp '1945-03-31 12:50:59.400000'),
HOUR	    (time '12:50:59.00000'),
MINUTE    (time '23:59:59.999999'),
SECOND    (time '00:00:01.000000')
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  UNION ALL, CAST, Arithmetic-exp tests
    stmt = """SELECT MONTH(d_t_m_e)
from DAYTAB 
UNION ALL
SELECT MONTH(CAST(d_t_m_e AS DATE)) + MONTH(d_t_m_e)
from vMONTH 
group by
w_k, d_t_m_e;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a007exp""", 'a007s3')
    
    #  JOIN tests
    stmt = """SELECT DAYTAB.month_d, vMONTH.month_d
from 	    DAYTAB 
INNER JOIN    vMONTH 
ON  DAYTAB.month_d =  vMONTH.month_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a007exp""", 'a007s4')
    
    stmt = """SELECT DAYTAB.month_d, vMONTH.month_d
from 	   DAYTAB 
LEFT JOIN    vMONTH 
ON  DAYTAB.month_d =  vMONTH.month_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a007exp""", 'a007s5')
    
    stmt = """SELECT DAYTAB.month_d, vMONTH.month_d
from 	    DAYTAB 
RIGHT JOIN    vMONTH 
ON  DAYTAB.month_d =  vMONTH.month_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a007exp""", 'a007s6')
    
    #  INDEX keys tests
    stmt = """CREATE INDEX idx1 on vMONTH(month_d);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1127')
    
    stmt = """SELECT 		month_d
from 	 DAYTAB 
order by	month_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a007exp""", 'a007s8')
    
    #  Cleanup index
    stmt = """DROP index idx1;"""
    output = _dci.cmdexec(stmt)
    
    #  CASE test
    stmt = """SELECT CURRENT_DATE,
CASE
WHEN MONTH(CURRENT_DATE) <=3 THEN 'FIRST  QUARTER'
WHEN MONTH(CURRENT_DATE) <=6 THEN 'SECOND QUARTER'
WHEN MONTH(CURRENT_DATE) <=9 THEN 'THIRD  QUARTER'
WHEN MONTH(CURRENT_DATE) <=12 THEN 'FORTH  QUARTER'
ELSE NULL
END
FROM DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 8)
    
    #  08/24/00 EL  Added BEGIN WORK and ROLLBACK statements. Depending on the
    #		 current month, there are 7 rows in the month_d = 8, so if
    #		 this test runs in August, then all the rows will be deleted.
    #		 This deletion will effect the following test cases. I added
    #		 one more DELETE statement to make sure only one row is deleted.
    
    stmt = """Begin Work;"""
    output = _dci.cmdexec(stmt)
    
    # UPDATE test
    stmt = """UPDATE vMONTH 
set month_d = MONTH (CURRENT_TIMESTAMP)
where month_d = 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    # DELETE test
    # The number of rows delete depends on what month this test is running.
    stmt = """DELETE from vMONTH 
where month_d = MONTH (CURRENT_TIMESTAMP);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    stmt = """Rollback work;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """DELETE from vMONTH 
where month_d = 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    # Cleanup view vMONTH
    # DELETE from vMONTH;
    stmt = """DROP view vMONTH;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test009(desc="""DAY function positive tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # ====================  Begin Test Case Header  ===================
    # Test case name: 	Arkt1422:  testa008
    # Description:		DAY function positive tests
    # Test case inputs:
    # Test case outputs:
    # Expected Results:	(provided a high-level description)
    #
    # Notes:
    # The DAY function extracts the DAY from <date-exp>, returns DAY(1,2...31)
    #
    
    stmt = """SELECT *  from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 7)
    
    # SELECT, WHERE tests
    stmt = """SELECT DAY(d_t_m_e)
from DAYTAB 
where DAY(d_t_m_e) > 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    #  Subqueries, Arithmetic exp., EXTRRACT tests
    stmt = """SELECT  DAY(CAST(d_t_m_e AS date))
from DAYTAB 
where day_d > 100
order by day_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    #  Create view vDAY for join, union all
    
    stmt = """drop view vday;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW vday AS SELECT * FROM DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Within/Upon the VIEW tests
    stmt = """INSERT INTO vday VALUES(
TIMESTAMP  '1990-10-05 15:19:59.300000',
DAYNAME   (timestamp '1918-05-11 10:00:09.999930'),
MONTHNAME (timestamp '1876-01-31 07:59:05.000000'),
DAYOFYEAR (timestamp '2000-01-01 00:00:00.000001'),
WEEK      (timestamp '1999-12-31 23:59:59.999999'),
QUARTER   (timestamp '1191-09-30 23:59:59.999999'),
YEAR      (timestamp '2106-07-01 00:00:00.000001'),
MONTH     (timestamp '1433-08-10 22:22:22.222222'),
DAY       (timestamp '1945-03-31 12:50:59.400000'),
HOUR      (time '12:50:59.400000'),
MINUTE    (time '23:59:59.999999'),
SECOND    (time '00:00:01.000000')
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  08/16/00 EL  Took out the comment and modified query for testing HAVING.
    #  HAVING, LIKE tests
    stmt = """SELECT DAY(d_t_m_e), upper(dayname(d_t_m_e)), d_t_m_e
from DAYTAB 
where DAY(d_t_m_e) is not null
group by d_t_m_e
having upper(dayname(d_t_m_e)) like '%MON%' or
upper(dayname(d_t_m_e)) like '%UES%' or
upper(dayname(d_t_m_e)) like '%DNS%' or
upper(dayname(d_t_m_e)) like '%RSD%' or
upper(dayname(d_t_m_e)) like '%IDA%' or
upper(dayname(d_t_m_e)) like '%ATU%' or
upper(dayname(d_t_m_e)) like '%UND%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a008exp""", 'a008s1')
    
    #  UNION ALL, Interval tests
    stmt = """SELECT cast(DAY(d_t_m_e) as interval day) from DAYTAB 
UNION ALL
SELECT cast(DAY(d_t_m_e) as interval day) + interval '5' day  from DAYTAB 
group by q_r, d_t_m_e;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a008exp""", 'a008s3')
    
    #  JOIN tests
    stmt = """SELECT DAYTAB.day_d, vday.day_d
from 	    DAYTAB 
INNER JOIN    vday 
ON  DAYTAB.day_d =  vday.day_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a008exp""", 'a008s4')
    
    stmt = """SELECT DAYTAB.day_d, vday.day_d
from 	   DAYTAB 
LEFT JOIN    vday 
ON  DAYTAB.day_d =  vday.day_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a008exp""", 'a008s5')
    
    stmt = """SELECT DAYTAB.day_d, vday.day_d
from 	    DAYTAB 
RIGHT JOIN    vday 
ON  DAYTAB.day_d =  vday.day_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a008exp""", 'a008s6')
    
    #  INDEX keys tests
    stmt = """CREATE INDEX idx1 on vday(day_d);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1127')
    
    stmt = """SELECT 		day_d
from 	 DAYTAB 
order by	day_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a008exp""", 'a008s8')
    
    #  Cleanup index
    stmt = """DROP index idx1;"""
    output = _dci.cmdexec(stmt)
    
    # 08/16/00 EL  Took out the comment and modified query for testing.
    # CASE test
    stmt = """SELECT d_n, m_n, d_of_y, w_k, q_r,
CASE lower(cast(dayname(d_t_m_e) as varchar(10)))
WHEN cast('monday' as varchar(10))    THEN cast(day(d_t_m_e) as char(10))
WHEN cast('tuesday' as varchar(10))   THEN cast(day(d_t_m_e) as char(10))
WHEN cast('wednesday' as varchar(10)) THEN cast(day(d_t_m_e) as char(10))
WHEN cast('thursday' as varchar(10))  THEN cast(day(d_t_m_e) as char(10))
WHEN cast('friday' as varchar(10))    THEN 'Good Friday'
WHEN cast('saturday' as varchar(10))  THEN 'Wow Saturday'
WHEN cast('sunday' as varchar(10))    THEN 'Sunday!!!!!'
ELSE NULL
END
FROM DAYTAB 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a008exp""", 'a008s8a')
    
    # UPDATE test
    stmt = """UPDATE vday 
set day_d = DAY (CURRENT_DATE)
where d_of_y < 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 8)
    
    # DELETE test
    stmt = """DELETE from vday 
where day_D = DAY (CURRENT_DATE);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 8)
    
    # Cleanup view vDAY
    # DELETE from vDAY;
    stmt = """DROP view vday;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test010(desc="""HOUR function positive tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # ==================  Begin Test Case Header  ===================
    # Test case name: 	Arkt1422:  testa009
    # Description:		HOUR function positive tests
    # Test case inputs:
    # Test case outputs:
    # Expected Results:	(provided a high-level description)
    #
    # Notes:
    # The HOUR function extracts the HOUR from <date-exp>,
    #			returns HOUR(0,1...23)
    #
    
    stmt = """SELECT *  from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # SELECT, WHERE tests
    stmt = """SELECT HOUR(d_t_m_e)
from DAYTAB 
where HOUR(d_t_m_e) > 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # 08/16/00 EL  Took out the comment and modified query for testing HAVING.
    # HAVING, LIKE tests
    stmt = """SELECT HOUR(d_t_m_e)
from DAYTAB 
where HOUR(d_t_m_e) in (0, -154, 15, 342.345, 93, 12342523523, 23)
group by d_t_m_e
having hour(d_t_m_e) like (0, -154, 15, 342.345, 93, 12342523523, 23);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # Subqueries, Arithmetic exp., EXTRRACT tests
    stmt = """SELECT  EXTRACT( HOUR from CURRENT_TIME) + HOUR(CURRENT)
from DAYTAB 
where d_of_y > 100
order by d_of_y;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # Create view vhour for join, union all
    
    stmt = """CREATE VIEW vhour AS SELECT *
FROM DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Within/Upon the VIEW tests
    stmt = """INSERT INTO vhour VALUES(
TIMESTAMP  '1990-10-05 15:19:59.300000',
DAYNAME   (timestamp '1918-05-11 10:00:09.999930'),
MONTHNAME (timestamp '1876-01-31 07:59:05.000000'),
DAYOFYEAR (timestamp '2000-01-01 00:00:00.000001'),
WEEK      (timestamp '1999-12-31 23:59:59.999999'),
QUARTER   (timestamp '1191-09-30 23:59:59.999999'),
YEAR	    (timestamp '2106-07-01 00:00:00.000001'),
MONTH     (timestamp '1433-08-10 22:22:22.222222'),
DAY	    (timestamp '1945-03-31 12:50:59.400000'),
HOUR	    (time '12:50:59.400000'),
MINUTE    (time '23:59:59.999999'),
SECOND    (time '00:00:01.000000')
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  UNION ALL, CAST tests
    stmt = """SELECT HOUR(d_t_m_e)
from DAYTAB 
UNION ALL
SELECT HOUR(CAST(d_t_m_e AS TIMESTAMP))
from vhour 
group by
w_k , d_t_m_e;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a009exp""", 'a009s0')
    
    #  String concat and current_timestamp function test
    #  SELECT cast(q_r as char) || cast (CURRENT_DATE AS CHAR)
    
    #  JOIN tests
    stmt = """SELECT DAYTAB.hour_d, vhour.hour_d
from 	    DAYTAB 
INNER JOIN    vhour 
ON  DAYTAB.hour_d =  vhour.hour_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a009exp""", 'a009s1')
    
    stmt = """SELECT DAYTAB.hour_d, vhour.hour_d
from 	   DAYTAB 
LEFT JOIN    vhour 
ON  DAYTAB.hour_d =  vhour.hour_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a009exp""", 'a009s2')
    
    stmt = """SELECT DAYTAB.hour_d, vhour.hour_d
from 	    DAYTAB 
RIGHT JOIN    vhour 
ON  DAYTAB.hour_d =  vhour.hour_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a009exp""", 'a009s3')
    
    #  INDEX keys tests
    stmt = """CREATE INDEX idx1 on vhour(hour_d);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1127')
    
    stmt = """SELECT 		hour_d
from 	 DAYTAB 
order by	hour_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a009exp""", 'a009s5')
    
    #  Cleanup index
    stmt = """DROP index idx1;"""
    output = _dci.cmdexec(stmt)
    
    # 08/16/00 EL  Took out the comment and modified query for testing.
    # CASE test
    stmt = """SELECT d_n, m_n, d_of_y, w_k, q_r,
CASE cast(hour(d_t_m_e) as char(10))
WHEN '23' THEN cast(hour(d_t_m_e) as char(10))
WHEN '0'  THEN 'ZERO......'
WHEN '15' THEN cast(minute(d_t_m_e) as char(10))
WHEN '59' THEN 'NULL......'
ELSE NULL
END
FROM DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a009exp""", 'a009s5a')
   
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
 
    # UPDATE test
    stmt = """UPDATE vhour 
set hour_d = HOUR ( CURRENT_TIME)
where hour_d > 13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 0)
    
    # DELETE test
    stmt = """DELETE from vhour 
where hour_d = HOUR ( CURRENT_TIME );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)

    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Cleanup view vhour
    # DELETE from vhour;
    stmt = """DROP view vhour;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test011(desc="""MINUTE function positive tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # ====================  Begin Test Case Header  ===================
    # Test case name: 	Arkt1422:  testa010
    # Description:		MINUTE function positive tests
    # Test case inputs:
    # Test case outputs:
    # Expected Results:	(provided a high-level description)
    #
    # Notes:
    # The MINUTE function extracts the MINUTE from <date-exp>,
    #							returns MINUTE(0,1...59)
    #
    
    stmt = """SELECT *  from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a010exp""", 'a010s0')
    
    #  SELECT, WHERE tests
    stmt = """SELECT MINUTE(d_t_m_e)
from DAYTAB 
where MINUTE(d_t_m_e) > 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a010exp""", 'a010s1')
    
    #  08/16/00 EL  Took out the comments and modified query for testing HAVGING.
    #  HAVING, LIKE tests
    stmt = """SELECT MINUTE(d_t_m_e)
from DAYTAB 
group by d_t_m_e
having cast(minute(d_t_m_e) as char(2)) like '%9' or
cast(minute(d_t_m_e) as char(2)) like '%0%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a010exp""", 'a010s1a')
    
    #  Subqueries, EXTRACT tests
    stmt = """SELECT MINUTE(d_t_m_e)
from DAYTAB 
where MINUTE(d_t_m_e) > 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a010exp""", 'a010s2')
    
    # Create view vMINUTE for join, union all
    
    stmt = """CREATE VIEW vMINUTE AS SELECT *
FROM DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Within/Upon the VIEW tests
    stmt = """INSERT INTO vMINUTE VALUES(
TIMESTAMP  '1990-10-05 15:19:59.300000',
DAYNAME   (timestamp '1918-05-11 10:00:09.999930'),
MONTHNAME (timestamp '1876-01-31 07:59:05.000000'),
DAYOFYEAR (timestamp '2000-01-01 00:00:00.000001'),
WEEK      (timestamp '1999-12-31 23:59:59.999999'),
QUARTER   (timestamp '1191-09-30 23:59:59.999999'),
YEAR	  (timestamp '2106-07-01 00:00:00.000001'),
MONTH     (timestamp '1433-08-10 22:22:22.222222'),
DAY	  (timestamp '1945-03-31 12:50:59.400000'),
HOUR	  (time '12:50:59.400000'),
MINUTE    (time '23:59:59.999999'),
SECOND    (time '00:00:01.000000')
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  UNION ALL, CAST tests
    stmt = """SELECT MINUTE(d_t_m_e)
from DAYTAB 
UNION ALL
SELECT MINUTE(CAST(d_t_m_e AS TIMESTAMP))
from vMINUTE 
group by
w_k, d_t_m_e;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a010exp""", 'a010s3')
    
    #  String concat and current_timestamp function test
    #  SELECT cast(q_r as char) || cast (CURRENT_DATE AS CHAR)
    
    #  JOIN tests
    stmt = """SELECT DAYTAB.minute_d, vMINUTE.minute_d
from 	    DAYTAB 
INNER JOIN    vMINUTE 
ON  DAYTAB.minute_d =  vMINUTE.minute_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a010exp""", 'a010s4')
    
    stmt = """SELECT DAYTAB.minute_d, vMINUTE.minute_d
from 	   DAYTAB 
LEFT JOIN    vMINUTE 
ON  DAYTAB.minute_d =  vMINUTE.minute_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a010exp""", 'a010s5')
    
    stmt = """SELECT DAYTAB.minute_d, vMINUTE.minute_d
from 	    DAYTAB 
RIGHT JOIN    vMINUTE 
ON  DAYTAB.minute_d =  vMINUTE.minute_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a010exp""", 'a010s6')
    
    #  INDEX keys tests
    stmt = """CREATE INDEX idx1 on vMINUTE(minute_d);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1127')
    
    stmt = """SELECT 		minute_d
from 	 DAYTAB 
order by	      minute_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a010exp""", 'a010s8')
    
    #  Cleanup index
    stmt = """DROP index idx1;"""
    output = _dci.cmdexec(stmt)
    
    # 08/16/00 EL  Took out the comments and modified query for testing.
    # CASE test
    stmt = """SELECT d_n, m_n, d_of_y, w_k, q_r,
CASE
WHEN cast(minute(d_t_m_e) as char(2)) = '15'    THEN 'Fifteen 15'
WHEN cast(minute(d_t_m_e) as char(2)) = '59'    THEN 'Fifty-nine'
WHEN cast(minute(d_t_m_e) as char(2)) = '19'    THEN 'Ninteen 19'
WHEN cast(minute(d_t_m_e) as char(2)) like '0%' THEN
cast(minute(d_t_m_e) as char(2))
ELSE NULL
END
FROM DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a010exp""", 'a010s8a')
    
    # UPDATE test
    stmt = """UPDATE vMINUTE 
set minute_d = MINUTE (CURRENT_TIME)
where minute_d > 30;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    
    # DELETE test
    stmt = """DELETE from vMINUTE 
where minute_d  = MINUTE ( CURRENT_TIME);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    
    # Cleanup view vminute
    # DELETE from vminute;
    stmt = """DROP view vMINUTE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test012(desc="""SECOND function positive tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # ==================  Begin Test Case Header  ==================
    # Test case name: 	Arkt1422:  testa011
    # Description:		SECOND function positive tests
    # Test case inputs:
    # Test case outputs:
    # Expected Results:	(provided a high-level description)
    #
    # Notes:
    # The SECOND function extracts the SECOND from <date-exp>,
    #				 returns SECOND(0,1...59)
    #
    
    stmt = """SELECT *  from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # SELECT, WHERE tests
    stmt = """SELECT SECOND(d_t_m_e)
from DAYTAB 
where SECOND(d_t_m_e) > 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # Subqueries, EXTRACT tests
    stmt = """SELECT EXTRACT(SECOND from CURRENT_TIME) + SECOND(CURRENT)
from DAYTAB 
where d_of_y > 100
order by d_of_y;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # Create view vsecond for join, union all
    
    stmt = """CREATE VIEW vsecond AS SELECT *
FROM DAYTAB ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Within/Upon the VIEW tests
    stmt = """INSERT INTO vsecond VALUES(
TIMESTAMP '1990-10-05 15:19:59.300000',
DAYNAME   (timestamp '1918-05-11 10:00:03.999930'),
MONTHNAME (timestamp '1876-01-31 07:59:05.000000'),
DAYOFYEAR (timestamp '2000-01-01 00:00:00.000001'),
WEEK      (timestamp '1999-12-31 23:59:59.999999'),
QUARTER   (timestamp '1191-09-30 23:59:59.999999'),
YEAR	  (timestamp '2106-07-01 00:00:00.000001'),
MONTH     (timestamp '1433-08-10 22:22:22.222222'),
DAY	  (timestamp '1945-03-31 12:50:59.400000'),
HOUR	  (time '12:50:59.400000'),
MINUTE    (time '23:59:59.999999'),
SECOND    (time '00:00:01.000000')
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # 08/16/00 EL  Took out the comment and modified query for testing HAVING.
    # HAVING, LIKE tests
    stmt = """SELECT SECOND(d_t_m_e)
from DAYTAB 
where SECOND(d_t_m_e) > .000000 and
second(d_t_m_e) < 60.300000
group by d_t_m_e
having second(d_t_m_e) in (000000.000000, .299999, .300000, 59.299999,
59.400000, 59.300000, 60.000000, 59.999998)
or
cast(second(d_t_m_e) as char(10)) like '%59.999999%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a011exp""", 'a011s0a')
    
    #  UNION ALL, CAST tests
    stmt = """SELECT SECOND(d_t_m_e)
from DAYTAB 
UNION ALL
SELECT SECOND(CAST(d_t_m_e AS TIMESTAMP))
from vsecond 
group by
w_k, d_t_m_e;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a011exp""", 'a011s0')
    
    #  String concat and current_timestamp function test
    #  SELECT cast(q_r as char) || cast (CURRENT_DATE AS CHAR)
    
    #  JOIN tests
    stmt = """SELECT DAYTAB.second_d , vsecond.second_d
from 	    DAYTAB 
INNER JOIN    vsecond 
ON  DAYTAB.second_d  =  vsecond.second_d ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a011exp""", 'a011s1')
    
    stmt = """SELECT DAYTAB.second_d , vsecond.second_d
from 	   DAYTAB 
LEFT JOIN    vsecond 
ON  DAYTAB.second_d  =  vsecond.second_d ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a011exp""", 'a011s2')
    
    stmt = """SELECT DAYTAB.second_d , vsecond.second_d
from 	    DAYTAB 
RIGHT JOIN    vsecond 
ON  DAYTAB.second_d  =  vsecond.second_d ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a011exp""", 'a011s3')
    
    #  INDEX keys tests
    stmt = """CREATE INDEX idx1 on vsecond(second_d );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1127')
    
    stmt = """SELECT 		second_d
from 	 DAYTAB 
order by	      second_d ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a011exp""", 'a011s5')
    
    #  Cleanup index
    stmt = """DROP index idx1;"""
    output = _dci.cmdexec(stmt)
    
    # 08/16/00 EL  Took out the comment and modified the query for testing.
    # CASE test
    stmt = """SELECT d_n, m_n, d_of_y, w_k, q_r,
CASE q_r
WHEN 1 THEN second(d_t_m_e)
WHEN 2 THEN hour(d_t_m_e)
WHEN 3 THEN week(d_t_m_e)
WHEN 4 THEN year(d_t_m_e)
ELSE NULL
END
FROM DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a011exp""", 'a011s5a')
    
    # UPDATE test
    stmt = """UPDATE vsecond 
set second_d  = SECOND (CURRENT_TIMESTAMP)
where second_d > 30;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 0)
    
    # DELETE test
    stmt = """DELETE from vsecond 
where second_d  = SECOND ( CURRENT_TIMESTAMP );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    # Cleanup view vsecond
    # DELETE from vsecond;
    stmt = """DROP view vsecond;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test013(desc="""DAYNANE function negative tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # ====================  Begin Test Case Header  =====================
    # Test case name: 	Arkt1422:  testn001
    # Description:		DAYNANE function negative tests
    # Test case inputs:
    # Test case outputs:
    # Expected Results:	(provided a high-level description)
    #
    # Notes:
    # The DAYNAME function returns name of the day of week(Sunday, Monday...)
    #
    
    #  Negative tests 1: DAYNAME function test.
    stmt = """INSERT INTO DAYTAB VALUES(
TIMESTAMP  '1901-10-10 15:23:00.300000',
DAYNAME   (date '1989-02-29'), -- wrong day given
MONTHNAME (date '1976-10-31'),
DAYOFYEAR (date '1920-01-01'),
WEEK      (date '1999-12-31'),
QUARTER   (date '2000-01-01'),
YEAR	  (date '1945-05-06'),
MONTH     (date '1936-08-10'),
DAY	  (date '1951-02-28'),
HOUR	  (timestamp '1718-01-10 12:50:59.400000'),
MINUTE	  (timestamp '0001-01-01 01:59:50.400000'),
SECOND	  (timestamp '1210-11-11 11:01:40.999999')
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3045')
    
    #  Missing date-expression
    stmt = """SELECT DAYNAME()  from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  More than one function name used
    stmt = """SELECT DAYNAME DAYNAME(d_t_m_e)
from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled the function name
    stmt = """SELECT DATENAME(d_t_m_e)
from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Date-exp out of bound
    stmt = """SELECT DAYNAME(time '23:59:50.0000')
from  DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4072')
    
    _testmgr.testcase_end(desc)

def test014(desc="""MONTHNANE function negative tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # ====================  Begin Test Case Header  =====================
    # Test case name: 	Arkt1422:  testn002
    # Description:		MONTHNANE function negative tests
    # Test case inputs:
    # Test case outputs:
    # Expected Results:	(provided a high-level description)
    #
    # Notes:
    # The MONTHNAME function returns name of the month of year(January, February...)
    #
    
    #  Negative tests 2: MONTHNAME function test.
    stmt = """INSERT INTO DAYTAB VALUES(
TIMESTAMP  '1901-10-10 15:23:00.330000',
DAYNAME   (date '1989-01-11'),
MONTHNAME (date '1976-13-31'), -- wrong month given
DAYOFYEAR (date '1920-01-01'),
WEEK      (date '1999-12-31'),
QUARTER   (date '2000-01-01'),
YEAR	    (date '1945-05-06'),
MONTH     (date '1936-08-10'),
DAY	    (date '1951-02-28'),
HOUR	    (timestamp '1718-01-10 12:50:59.400000'),
MINUTE    (timestamp '0001-01-01 01:59:50.400000'),
SECOND    (timestamp '1210-11-11 11:01:40.999999')
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3045')
    
    #  Missing date-expression
    stmt = """SELECT MONTHNAME()  from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  More than one function name used
    stmt = """SELECT MONTHNAME MONTHNAME(d_t_m_e)
from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled the function name
    stmt = """SELECT MONTHNAM(d_t_m_e)
from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Date-exp out of bound
    stmt = """SELECT MONTHNAME(time '10:10:20')
from  DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4037')
    
    _testmgr.testcase_end(desc)

def test015(desc="""DAYOFYEAR function negative tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ====================
    # Test case name: 	Arkt1422:  testn003
    # Description:		DAYOFYEAR function negative tests
    # Test case inputs:
    # Test case outputs:
    # Expected Results:	(provided a high-level description)
    #
    # Notes:
    # The DAYOFYEAR function returns number of the DAYOFYEAR of year(1,2...,366/365)
    #
    
    #  Negative tests 3: DAYOFYEAR function test.
    stmt = """INSERT INTO DAYTAB VALUES(
TIMESTAMP  '1901-10-10 15:23:00.300000',
DAYNAME   (date '1989-01-11'),
MONTHNAME (date '1976-11-10'),
DAYOFYEAR (date '1001-02-29'), -- wrong year given
WEEK      (date '1999-12-31'),
QUARTER   (date '2000-01-01'),
YEAR	  (date '1945-05-06'),
MONTH     (date '1936-08-10'),
DAY	  (date '1951-02-28'),
HOUR      (timestamp '1718-01-10 12:50:59.400000'),
MINUTE    (timestamp '0001-01-01 01:59:50.400000'),
SECOND    (timestamp '1210-11-11 11:01:40.999999'),
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3045')
    
    #  Missing date-expression
    stmt = """SELECT DAYOFYEAR()  from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  More than one function name used
    stmt = """SELECT DAYOFYEAR DAYOFYEAR(d_t_m_e)
from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled the function name
    stmt = """SELECT DAYOFYEER(d_t_m_e)
from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Date-exp out of bound
    stmt = """SELECT 	DAYOFYEAR(date '12/20/0000')
from  DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3045')
    
    _testmgr.testcase_end(desc)

def test016(desc="""DAYOFYEAR function negative tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # ====================  Begin Test Case Header  ===================
    # Test case name: 	Arkt1422:  testn004
    # Description:		DAYOFYEAR function negative tests
    # Test case inputs:
    # Test case outputs:
    # Expected Results:	(provided a high-level description)
    #
    # Notes:
    # The WEEK function returns number of the week of year(1,2...,52)
    #
    
    #  Negative tests 4: WEEK function test.
    stmt = """INSERT INTO DAYTAB VALUES(
TIMESTAMP '1901-10-10 15:23:00.300000',
DAYNAME   (date '1989-01-11'),
MONTHNAME (date '1976-13-31'),
DAYOFYEAR (date '0000-01-01'),
WEEK      (date '1999-00-31'), -- wrong week given
QUARTER   (date '2000-01-01'),
YEAR	    (date '1945-05-06'),
MONTH     (date '1936-08-10'),
DAY	    (date '1951-02-28'),
HOUR	    (timestamp '1718-01-10 12:50:59.000040'),
MINUTE    (timestamp '0001-01-01 01:59:50.000400'),
SECOND    (timestamp '1210-11-11 11:01:40.599909')
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3045')
    
    #  Missing date-expression
    stmt = """SELECT WEEK()  from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  More than one function name used
    stmt = """SELECT WEEK WEEK(d_t_m_e)
from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled the function name
    stmt = """SELECT WEAK(d_t_m_e)
from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Date-exp out of bound
    stmt = """SELECT WEEK(date '1998-01-01'),  WEEK(date'1998-12-31')
from  DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n004exp""", 'n004s4')
    
    _testmgr.testcase_end(desc)

def test017(desc="""QUARTER function negative tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =====================  Begin Test Case Header  ==================
    # Test case name: 	Arkt1422:  testn005
    # Description:		QUARTER function negative tests
    # Test case inputs:
    # Test case outputs:
    # Expected Results:	(provided a high-level description)
    #
    # Notes:
    # The QUARTER function returns number of the Quarter of year(1,2,3,4)
    #
    
    #  Negative tests 5: QUARTER function test.
    stmt = """INSERT INTO DAYTAB VALUES(
TIMESTAMP '1901-10-10 15:23:00.300000',
DAYNAME   (date '1989-01-11'),
MONTHNAME (date '1976-03-31'),
DAYOFYEAR (date '1000-01-01'),
WEEK      (date '1999-08-01'),
QUARTER   (time '20:01:05'), -- time given
YEAR	    (date '1945-05-06'),
MONTH     (date '1936-08-10'),
DAY	    (date '1951-02-28'),
HOUR	    (timestamp '1718-01-10 12:50:59.400000'),
MINUTE    (timestamp '0001-01-01 01:59:50.400000'),
SECOND    (timestamp '1210-11-11 11:01:40.590000')
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4037')
    
    #  Missing date-expression
    stmt = """SELECT QUARTER()  from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  More than one function name used
    stmt = """SELECT QUARTER QUARTER(d_t_m_e)
from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled the function name
    stmt = """SELECT QUARTAR(d_t_m_e)
from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Date-expression out of bound
    stmt = """SELECT QUARTER(interval '10-3' year to month)
from  DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4071')
    
    #  03/12/01 EL  Added following queries.
    
    stmt = """SELECT QUARTER(123456789) from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4071')
    
    stmt = """SELECT QUARTER(abcdefg) from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    _testmgr.testcase_end(desc)

def test018(desc="""YEAR function negative tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # ====================  Begin Test Case Header  ===================
    # Test case name: 	Arkt1422:  testn006
    # Description:		YEAR function negative tests
    # Test case inputs:
    # Test case outputs:
    # Expected Results:	(provided a high-level description)
    #
    # Notes:
    # The YEAR function extracts the year from <date-exp>,
    # 				 returns year(1990, 1921...)
    #
    
    #  Negative tests 6: YEAR function test.
    stmt = """INSERT INTO DAYTAB VALUES(
TIMESTAMP '1901-10-10 15:23:00.300000',
DAYNAME   (date '1986-01-11'),
MONTHNAME (date '1977-13-31'),
DAYOFYEAR (date '0001-01-01'),
WEEK      (date '1992-00-31'),
QUARTER   (date '2001-01-00'),
YEAR	    (date '0000-05-06'), -- wrong year given
MONTH     (date '1934-08-10'),
DAY 	    (date '1952-02-28'),
HOUR	    (timestamp '1718-01-10 12:50:59.000040'),
MINUTE    (timestamp '0001-01-01 01:59:50.007940'),
SECOND    (timestamp '1210-11-11 11:01:40.009959')
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3045')
    
    #  Missing date-expression
    stmt = """SELECT YEAR()  from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  More than one function name used
    stmt = """SELECT YEAR YEAR(d_t_m_e)
from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled the function name
    stmt = """SELECT YAER(d_t_m_e)
from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Date-exp out of bound
    stmt = """SELECT  YEAR(interval '10-05' year to month )
from  DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n006exp""", 'n006s4')
    
    stmt = """SELECT YEAR(123)
from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4036')
    
    _testmgr.testcase_end(desc)

def test019(desc="""MONTH function negative tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # ===================  Begin Test Case Header  ===================
    # Test case name: 	Arkt1422:  testn007
    # Description:		MONTH function negative tests
    # Test case inputs:
    # Test case outputs:
    # Expected Results:	(provided a high-level description)
    #
    # Notes:
    # The MONTH function extracts the month from <date-exp>,
    #			returns year(1,2...12)
    #
    
    #  Negative tests 7: MONTH function test.
    stmt = """INSERT INTO DAYTAB VALUES(
TIMESTAMP '1901-10-10 15:23:00.300000',
DAYNAME   (date '1986-01-11'),
MONTHNAME (date '1977-11-30'),
DAYOFYEAR (date '0001-01-01'),
WEEK      (date '1992-06-30'),
QUARTER   (date '2001-01-11'),
YEAR	    (date '0001-05-06'),
MONTH     (time ' 20:20:20.200000'), -- wrong month given
DAY	    (date '1998-02-30'),
HOUR	    (timestamp '1718-01-10 12:50:59.400000'),
MINUTE    (timestamp '0001-01-01 01:59:50.400000'),
SECOND    (timestamp '1210-11-11 11:01:40.590000')
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3045')
    
    #  Missing date-expression
    stmt = """SELECT MONTH()  from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  More than one function name used
    stmt = """SELECT MONTH MONTH(d_t_m_e)
from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled the function name
    stmt = """SELECT MONTHE(d_t_m_e)
from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Date-exp out of bound
    stmt = """SELECT MONTH(interval '02-05' year to month)
from  DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n007exp""", 'n007s4')
    
    stmt = """SELECT MONTH(123)
from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4036')
    
    _testmgr.testcase_end(desc)

def test020(desc="""DAY function negative tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # ===================  Begin Test Case Header  =================
    # Test case name: 	Arkt1422:  testn008
    # Description:		DAY function negative tests
    # Test case inputs:
    # Test case outputs:
    # Expected Results:	(provided a high-level description)
    #
    # Notes:
    # The DAY function extracts the DAY from <date-exp>,
    #				returns year(1,2...31)
    #
    
    #  Negative tests 8: DAY function test.
    stmt = """INSERT INTO DAYTAB VALUES(
TIMESTAMP '1901-10-10 15:23:00.300000',
DAYNAME   (date '1986-01-11'),
MONTHNAME (date '1977-04-30'),
DAYOFYEAR (date '0001-01-01'),
WEEK      (date '1992-07-16'),
QUARTER   (date '2001-01-10'),
YEAR	   (date '1303-05-06'),
MONTH     (date '1934-08-10'),
DAY	   (date '1998-03-32'), -- wrong day given
HOUR	   (timestamp '1718-01-10 12:50:59.499990'),
MINUTE	   (timestamp '0001-01-01 01:59:50.499990'),
SECOND	   (timestamp '1210-11-11 11:01:40.599999')
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3045')
    
    #  Missing date-expression
    stmt = """SELECT DAY()  from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  More than one function name used
    stmt = """SELECT DAY DAY(d_t_m_e)
from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled the function name
    stmt = """SELECT DAYE(d_t_m_e)
from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Date-exp arithematic out of bound
    stmt = """SELECT  DAY(interval '5' DAY )
from  DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n008exp""", 'n008s4')
    
    stmt = """SELECT DAY(123)
from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4036')
    
    _testmgr.testcase_end(desc)

def test021(desc="""HOUR function negative tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # ================  Begin Test Case Header  ====================
    # Test case name: 	Arkt1422:  testn009
    # Description:		HOUR function negative tests
    # Test case inputs:
    # Test case outputs:
    # Expected Results:	(provided a high-level description)
    #
    # Notes:
    # The HOUR function extracts the HOUR from <date-exp>,
    #						returns HOUR(0,1...23)
    #
    
    #  Negative tests 9: HOUR function test.
    stmt = """INSERT INTO DAYTAB VALUES(
TIMESTAMP '1901-10-10 15:23:00.300000',
DAYNAME   (date '1989-01-11'),
MONTHNAME (date '1976-10-31'),
DAYOFYEAR (date '1920-01-01'),
WEEK      (date '1999-12-30'),
QUARTER   (date '2000-01-01'),
YEAR	  (date '1945-05-06'),
MONTH     (date '1936-08-10'),
DAY	  (date '1951-02-28'),
HOUR	  (timestamp '1718-01-10 24:50:59.400000'),-- wrong hour given
MINUTE    (timestamp '0001-01-01 01:59:50.400000'),
SECOND    (timestamp '1210-11-11 11:01:40.590000')
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3047')
    
    #  Missing date-expression
    stmt = """SELECT HOUR()  from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  More than one function name used
    stmt = """SELECT HOUR HOUR(d_t_m_e)
from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled the function name
    stmt = """SELECT HOURE(d_t_m_e)
from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Date-exp arithematic out of bound
    stmt = """SELECT HOUR(interval '5:2:15:36.33' DAY to SECOND(2))
from  DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n009exp""", 'n009s4')
    
    stmt = """SELECT HOUR(123)
from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4036')
    
    _testmgr.testcase_end(desc)

def test022(desc="""MINUTE function negative tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    # Test case name: 	Arkt1422:  testn010
    # Description:		MINUTE function negative tests
    # Test case inputs:
    # Test case outputs:
    # Expected Results:	(provided a high-level description)
    #
    # Notes:
    # The MINUTE function extracts the MINUTE from <date-exp>,
    #						returns MINUTE(0,1...59)
    #
    
    #  Negative tests 10: MINUTE function test.
    stmt = """INSERT INTO DAYTAB VALUES(
TIMESTAMP '1901-10-10 15:23:00.300000',
DAYNAME   (date '1989-01-11'),
MONTHNAME (date '1976-10-31'),
DAYOFYEAR (date '1920-01-01'),
WEEK      (date '1999-12-31'),
QUARTER   (date '2000-01-01'),
YEAR	    (date '1945-05-06'),
MONTH     (date '1936-08-10'),
DAY	    (date '1951-02-28'),
HOUR	    (timestamp '1718-01-10 12:50:59.400000'),
MINUTE    (time '01:60:50.123456'), 		-- wrong minute given
SECOND    (timestamp '1210-11-11 11:01:4.999999'),
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3046')
    
    #  Missing date-expression
    stmt = """SELECT MINUTE()  from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  More than one function name used
    stmt = """SELECT MINUTE MINUTE(d_t_m_e)
from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled the function name
    stmt = """SELECT MINUTEE(d_t_m_e)
from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Date-exp arithematic out of bound
    stmt = """SELECT MINUTE( interval '5:13:25:2.12' DAY to SECOND(2))
from  DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n010exp""", 'n010s4')
    
    stmt = """SELECT MINUTE(123)
from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4036')
    
    _testmgr.testcase_end(desc)

def test023(desc="""SECOND function negative tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ===================
    # Test case name: 	Arkt1422:  testn011
    # Description:		SECOND function negative tests
    # Test case inputs:
    # Test case outputs:
    # Expected Results:	(provided a high-level description)
    #
    # Notes:
    # The SECOND function extracts the SECOND from <date-exp>,
    #					 returns SECOND(0,1...59)
    #
    
    #  Negative tests 11: SECOND function test.
    stmt = """INSERT INTO DAYTAB VALUES(
TIMESTAMP '1901-10-10 15:23:00.300000',
DAYNAME   (date '1989-01-11'),
MONTHNAME (date '1976-10-31'),
DAYOFYEAR (date '1920-01-01'),
WEEK      (date '1999-12-31'),
QUARTER   (date '2000-01-01'),
YEAR	    (date '1945-05-06'),
MONTH     (date '1936-08-10'),
DAY	    (date '1951-02-28'),
HOUR	    (timestamp '1718-01-10 12:50:59.400000'),
MINUTE    (timestamp '0001-01-01 01:59:50.000040'),
SECOND    (time '11:01:60.000000'),       -- wrong second given
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3046')
    
    #  Missing date-expression
    stmt = """SELECT SECOND()  from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  More than one function name used
    stmt = """SELECT SECOND SECOND(d_t_m_e)
from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled the function name
    stmt = """SELECT SECONDE(d_t_m_e)
from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Date-exp arithematic out of bound
    stmt = """SELECT 	SECOND(interval '5:13:13:3.10' DAY TO SECOND(2))
from  DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n011exp""", 'n011s4')
    
    stmt = """SELECT SECOND(123)
from DAYTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4036')
    
    _testmgr.testcase_end(desc)

