# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2014 Hewlett-Packard Development Company, L.P.
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
    
def test001(desc="""a00"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA00
    #  Description:        Tests for SQL, this test case only
    #			create the table, and insert data into
    #			the table for the use in the following
    #			test cases.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    # Create LOG file
    
    stmt = """drop table emp;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE emp 
(
FIRST_NAME             CHAR(10) NOT NULL
, LAST_NAME              CHAR(10) DEFAULT NULL
, DEPT_NUM               NUMERIC(4, 0) NOT NULL
, SALARY                 NUMERIC(8, 2) DEFAULT NULL
, MARITAL_STATUS         NUMERIC(3, 0) DEFAULT NULL
, HIRE_DATE              DATE
, START_TIME             TIMESTAMP,
primary key (first_name, dept_num))
store by primary key;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index idx1 on emp (last_name);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create unique index undx on emp (first_name, start_time);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO emp 
values
( 'CLARK' , 'DINAH',9000, 37000.50, 3,
date '05/02/1977', timestamp '05/02/1977 08:12:00.110000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO emp 
values ('CRINAR', 'JESSICA', 3500, 39500.00, 2,
date '08/12/1984', timestamp '08/12/1984 05:00:00.000233');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO emp 
values ('GREEN','ROGER',  9000, 175500.99, 2,
date '09/23/1908', timestamp '09/23/1908 12:34:00.320222');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO emp 
values ('HOWARD', 'JERRY', 1000, 65000.64, 1,
date '11/05/1923', timestamp '11/05/1923 10:30:00.999900');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO emp 
values ('jerry', 'white', 1200, 70000.00, 1,
date '11/05/1923', timestamp '11/05/1923 08:30:00.009999');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO emp 
values ('hans', 'christian', 500, 99000.04, 1,
date '09/23/1908', timestamp '09/23/1908 12:34:00.067222');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    _testmgr.testcase_end(desc)

def test002(desc="""a01"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA01
    #  Description:        Tests for SQL, use of ASCII function
    #                      in the select list.  This is a positive
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # ASCII function syntax:
    # ASCII{(<string-exp>)}
    
    # Create LOG file
    
    # char(ASCII) is not suported in WM, change to use substring
    stmt = """select concat(char(ASCII(first_name)), '.'), last_name,
ASCII(CHAR(ASCII(last_name))), ascii(char(255)),
ascii(char(0)), ASCII(SUBSTRING(last_name, 2, 3)),
hire_date
from emp 
where hire_date = (select hire_date
from emp 
where ASCII(first_name) = 106)
group by hire_date, last_name, first_name
order by 2 asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    stmt = """select first_name, last_name,
concat(first_name,  ' , ' || last_name),
char_length(SPACE(ASCII(LOWER(first_name)))),
char_length(REPEAT(first_name, cast(Ascii(first_name) / 10 as integer)))
from emp 
where ASCII(UPPER(first_name)) > 69 or
ASCII(LOWER(last_name)) = 44 or
first_name in
(select first_name
from emp 
where ASCII(first_name) > 43)
group by first_name, last_name
having ASCII(first_name || last_name) in (43, 50, 67, 104)
order by first_name desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    
    stmt = """insert into emp values
('david', LOWER('tess'), ASCII('*'), 35000, 4,
date '09/01/1999', timestamp '01/09/2000 12:33:22.123456');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    
    stmt = """update emp set marital_status = 10
where ASCII(UPSHIFT(first_name)) in (ASCII(UPPER('david')));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    
    stmt = """delete from emp 
where CHAR(ASCII(last_name)) = 't';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select * from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    
    stmt = """select last_name, CHAR(ASCII(last_name)),
case
when ASCII(last_name) > 40 and ASCII(last_name) < 91
then 40
when ASCII(last_name) > 60 and ASCII(last_name) < 123
then ascii(last_name)
end,
first_name, REPLACE(first_name, 'E',
cast(ASCII('x') as char(3))),
hire_date
from emp 
where ASCII(CAST(first_name as char(15))) > 60
group by first_name, last_name, hire_date
order by first_name, hire_date;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    
    # AR 12/08/06 Changed lpad, rpad stmt according to spec.
    stmt = """select first_name,
min(ASCII(LPAD(first_name, 12, char(ASCII('y'))))),
ASCII(RPAD(last_name, 13, char(ASCII(UPPER(first_name))))),
INSERT('what is your first name', 9, ASCII('our'), 'A'),
CONCAT(' -- ', first_name),
ASCII(INSERT('what is your first name', 1, 1, 'W'))
from emp 
where ASCII(LOWER(last_name)) > 100
group by first_name, last_name;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')
    
    stmt = """create view vemp as
select * from emp where
ASCII(Upper(first_name)) = ASCII(UPSHIFT(first_name));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vemp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s7')
    
    stmt = """create view vemp1 as
select * from emp where
ASCII(UCASE(first_name)) =
ASCII(UPSHIFT(first_name)) and
hire_date = hire_date;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vemp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s8')
    
    stmt = """create view vvemp as
select v1.last_name, t1.hire_date
from vemp v1 left join emp t1 on
ASCII(lcase(v1.first_name)) =
ASCII(lower(t1.first_name)) and
v1.start_time = t1.start_time;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select emp.last_name, emp.start_time
from emp 
union all
select CHAR(ASCII('@')), v1.start_time
from vemp v1
left join vemp v2 on CHAR(ASCII(UPPER(v2.last_name))) = 'D';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s9')
    
    stmt = """select emp.last_name, emp.hire_date, vemp.marital_status
from emp inner join vemp on
CHAR(ASCII(UPPER(vemp.last_name))) = 'D';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s10')
    
    stmt = """select vvemp.last_name, emp.hire_date
from emp join vvemp on
ASCII(emp.last_name) = ASCII(vvemp.last_name);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s11')
    
    # char(ascii) is not supported in WM mode, change to use substring
    stmt = """select min(char(ascii(last_name))),
max(ascii(char(ascii(last_name))))
from vvemp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s12')
    # -------------------------------
    # Cleanup section
    # -------------------------------
    
    stmt = """DROP VIEW  vvemp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """DROP VIEW  vemp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """DROP VIEW  vemp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test003(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA02
    #  Description:        Tests for SQL, use of CHAR function
    #                      in the select list.  This is a positive
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # CHAR function syntax:
    # CHAR{(<ascii-code>)}
    
    # Create LOG file
    
    # CHAR(254) is non-printable ascii, adding converttohex function to show the
    # hex code
    # 7/10/09
    stmt = """select first_name, converttohex(CHAR(ASCII(CHAR(254)))),
CHAR(ASCII(first_name)), char(1),
last_name, CHAR(ASCII(SUBSTRING(last_name, 1, 2))),
char_length(CHAR(19) || CHAR(27) || CHAR(139)),
octet_length(CHAR(3) || CHAR(211)),
CONCAT(' -- ', last_name)
from emp 
where CHAR(ASCII(last_name)) =
(select CHAR(ASCII(last_name))
from emp 
where last_name > 'tiss')
group by first_name, last_name
having cast(ascii(first_name) as varchar(3)) in
('67', '68', '72', '80', '106')
order by 2 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    stmt = """insert into emp values
(UPPER('davii'),  CHAR(64), 570, 63000.34, 3,
date '09/01/1999', timestamp '10/31/2001 17:30:00.000000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    
    stmt = """update emp set marital_status = 999
where ASCII(Ucase(first_name)) = ASCII(upshift('D')) and
CHAR(ASCII(last_name)) = char(64);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    
    stmt = """delete from emp 
where CHAR(Ascii(first_name)) = 'D';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select * from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    
    # AR 12/08/06 Changed lpad, rpad stmt according to spec.
    # added convertohex to CHAR(255) to get the code instead of getting
    # non-printable ascii code
    stmt = """select CHAR(ASCII(LOWER(first_name))), first_name,
converttohex(REPEAT(CHAR(255), 5)),
case
when ASCII(last_name) > 64 and ASCII(last_name) < 91
then CHAR(64)
when ASCII(last_name) > 96 and ASCII(last_name) < 123
then CHAR(96)
else 'done'
end,
LPAD(first_name, 10, CHAR(61)),
RPAD(last_name, 10, CHAR(ASCII(LCASE(first_name)))),
INSERT('what is your first name', 9, 4, CHAR(100)),
REPLACE(first_name, 'E', CHAR(254))
from emp 
where CAST(first_name as char(1)) > CHAR(96)
group by first_name, last_name
order by 1, 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    stmt = """create view vemp as
select * from emp 
where UCASE(CHAR(ascii(first_name))) =
upper(char(ascii(first_name)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vemp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')
    
    stmt = """create view vemp1 as
select * from emp where
char(ascii(UPPER(first_name))) =
char(ascii(UPSHIFT(first_name))) and
hire_date = hire_date;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vemp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s6')
    
    stmt = """create view vvemp as
select vemp.last_name, vemp.first_name, vemp.marital_status,
 vemp.hire_date, vemp.start_time
from vemp left join emp on
CHAR(ascii(lcase(vemp.first_name))) =
CHAR(ascii(lower(emp.first_name))) and
 vemp.start_time = emp.start_time;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """prepare p from
select emp.last_name, emp.start_time
from emp 
union all
select CHAR(ASCII('@')), vemp.start_time
from vemp 
left join vvemp on
CHAR(ASCII(UPPER(vvemp.last_name))) = 'D';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s8')
    
    # -------------------------------
    # Cleanup section
    # -------------------------------
    
    stmt = """DROP VIEW  vvemp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP VIEW  vemp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP VIEW  vemp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test004(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA03
    #  Description:        Tests for SQL, use of INSERT function
    #                      in the select list.  This is a positive
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # INSERT function syntax:
    # INSERT{(<exp1>, <start>, <length>, <exp2>)}
    
    # Create LOG file
    
    stmt = """select concat(INSERT(first_name, 1, 2, 'FF'), '.'), last_name,
INSERT(first_name, 1, 1, '@'), first_name,
INSERT(SUBSTRING(first_name, 3, 2), 1, 2, 'FF')
from emp 
where INSERT(first_name, 1, 5, 'FF') =
(select INSERT(first_name, 1, 5, 'FF')
from emp 
where last_name = 'JESSICA');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s0')
    
    stmt = """select last_name, INSERT(first_name, 2, 2, 'Fg'),
INSERT(first_name, 3+7, 2, 'eF'),
INSERT(first_name, octet_length(first_name), 5,
cast(ascii(first_name) as varchar(3))),
SPACE(2) || '.' || SPACE(3),
INSERT(first_name, 1, char_length(first_name), 'FF'),
INSERT(first_name, 2, 0, 'FF')
from emp 
where INSERT(first_name, 3, 3, 'son') = 'hason'
group by first_name, last_name
having ASCII(INSERT(last_name, 5, 1, 'L')) in (67, 74, 80, 99, 119)
order by last_name;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    
    stmt = """prepare p from
select first_name, last_name,
INSERT(first_name, 1, 2, 'hi, there ') || ',' || last_name
from emp 
where INSERT(Lcase(last_name), 3, 3, 'own') = 'roown' or
INSERT(Ucase(first_name), 1, 1, 'H') = 'HERRY';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s3')
    
    stmt = """insert into emp values
('david', INSERT(Lcase('tess'), 1, 1, '###'), 3, 67000.04, 5,
date '09/02/2000', timestamp '10/31/2001 17:30:00.000000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s4')
    
    stmt = """update emp set marital_status = 45
where INSERT(UPSHIFT(first_name), 1, 1, CHAR(68)) = 'DAVID';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s5')
    # AR Added order by for reliable result
    stmt = """select INSERT(LCASE(first_name), 2, 3, 'xyz'), first_name,
REPEAT(INSERT(first_name, 1, 2, 'FF'), 5),
last_name, ASCII(INSERT(last_name, 1, 1, 'C')),
case
when INSERT(last_name, 2, 1, 'U') > 'jERRY'
then 'not jerry b'
when INSERT(last_name, 2, 1, 'x') > 'chrise'
then 'not hans'
else
INSERT('there is no such person', 10, 2, 'no no')
end
from emp 
where INSERT(last_name, 5, 1, 'Y') > 'CLARK' order by first_name, last_name;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s6')
    
    stmt = """delete from emp 
where INSERT(UPSHIFT(first_name), 1, 1, CHAR(68)) = 'DAVID';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select * from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s7')
    
    stmt = """select first_name,
REPLACE(first_name, 'e', INSERT('x', 1, 1, 'ab')),
last_name,
INSERT(LPAD(first_name, 10, CHAR(ASCII('yy'))), 1, 1, 'I'),
INSERT(RPAD(last_name, 7, 'ho'), 2, 4, 'good'),
ASCII(INSERT(UPPER(first_name), 1, 3, 'Y')),
INSERT(INSERT
('what is your first name', 9, 4, 'our'), 1, 2, 'Ha') ||
' -- ' || first_name
from emp 
where INSERT(CAST(first_name as char(15)), 1, 3, 'ins') > 'insRK'
group by first_name, last_name
order by first_name, last_name,4,5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s8')
    
    stmt = """create view vemp as
select * from emp where
INSERT(UPPER(first_name), 5, 1, 'e') like 'CR%NeR%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vemp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s9')
    
    stmt = """create view vemp1 as
select * from emp where
INSERT(last_name, 1, 2, 'P') > 'Pop';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vemp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s10')
    
    stmt = """create view vvemp as
select v1.first_name, v1.last_name, te.marital_status
from vemp v1 left join emp te on
(INSERT(Ucase(v1.first_name), 3, 2, 'Hi') =
INSERT(UPSHIFT(te.first_name), 3, 2, 'Hi')) and
(v1.start_time = te.start_time);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select emp.last_name, emp.start_time,
INSERT(first_name, 4, 2, ' hello  @ ')
from emp 
union all
select vemp.last_name,
 vemp.start_time,
CHAR(ascii(INSERT(vemp.last_name, 1, 2, '11')))
from vemp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s11')
    
    stmt = """select e.last_name, e.hire_date, v.marital_status
from emp e inner join vemp v on
char(ASCII(INSERT(UPPER(v.last_name), 1, 2, 'D'))) = 'D';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s12')
    
    stmt = """select char_length(INSERT('NewsCenter...', 4, 6, 'Well')),
char_length(INSERT(last_name, 5, 2, ' Is that really you? ')),
octet_length(INSERT('NewsCenter...', 4, 6, 'Well')),
octet_length(INSERT(last_name, 5, 2, ' Is that really you? '))
from emp 
where char_length(INSERT(last_name, 1, 2, 'Long name ')) > 15;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s13')
    
    stmt = """select INSERT('ehi,ens', 99, 5, 'mary'),
INSERT('abcdf', 1, 99, 'bye'),
first_name, marital_status,
insert(first_name, 1, marital_status, '999'),
last_name,
insert(last_name, marital_status, marital_status, last_name)
from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s14')
    
    stmt = """select max(INSERT(last_name, 5, 2, 'max')),
min(INSERT(last_name, 1, 2, 'mm'))
from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s15')
    
    # -------------------------------
    # Cleanup section
    # -------------------------------
    
    stmt = """DROP VIEW  vvemp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP VIEW  vemp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP VIEW  vemp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test005(desc="""a04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA04
    #  Description:        Tests for SQL, use of REPEAT function
    #                      in the select list.  This is a positive
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # REPEAT function syntax:
    # REPEAT{(<exp>, <count>)}
    
    # Create LOG file
    
    stmt = """select REPEAT(SUBSTRING(
last_name, 1 * char_length(last_name) - 2, 1), 5),
last_name, hire_date, REPEAT(first_name,  1 + 0)
from emp 
where last_name in
(select last_name
from emp 
where REPEAT(first_name, 2) like 'HOWARD%OWARD%');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """select max(REPEAT(LOWER(last_name), 3)), last_name,
REPEAT(first_name, 2) || ', ' || REPEAT(last_name, 3),
substring(Concat(first_name, repeat(
last_name, cast(2 + 3 - 2 * 4 / 2 as integer))),  1, 25)
from emp 
where REPEAT(first_name, 2) > 'GREEN'
group by first_name, last_name, marital_status
having REPEAT(first_name || last_name, 2) in
('CLARK     DINAH     CLARK     DINAH',
'CRINAR    JESSICA   CRINAR    JESSICA',
'HOWARD    JERRY     HOWARD    JERRY')
order by last_name desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s1')
    
    stmt = """insert into emp values
('david', REPEAT(LCASE('Tess'), 2), 230, 78000, 2,
date '09/02/1655', timestamp '09/02/1923 10:30:00.9999');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select first_name,
repeat(cast(hire_date as varchar(15)), 0) as "hire_date to varchar",
repeat('REPEAT zero time', 0) as "REPEAT zero time"
from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s2')
    
    stmt = """update emp set last_name = REPEAT('ha', 5)
where REPEAT(UPSHIFT(first_name), 2) = 'DAVID     DAVID';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s3')
    
    stmt = """delete from emp 
where repeat(lcase(last_name), 2) = 'hahahahahahahahahaha';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select * from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s4')
    
    stmt = """select substring(SPACE(cast(ascii(
REPEAT(UPPER(first_name), 5)) / 10 as integer)), 1, 14),
first_name,
last_name, CHAR(ascii(REPEAT(last_name, 10))),
min(REPEAT(REPEAT(first_name, 5), 2)),
case
when REPEAT(UPSHIFT(last_name), 2) = 'JERRYJERRY'
then 'last name is JERRY'
when REPEAT(UCASE(last_name), 3) > 'JERRYJERRY'
then last_name
else 'who are you?'
end
from emp 
group by last_name, first_name;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s5')
    
    stmt = """prepare s from select  REPEAT(first_name,  2-1)   from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select  REPEAT(first_name,  1*1)   from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 6)
    
    stmt = """select  REPEAT(first_name,  1 + 1)   from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 6)
    
    stmt = """select first_name,
REPEAT(LPAD(first_name, 10, Char(ASCII('yy'))), 4),
REPEAT(RPAD(last_name, 11, chAr(ASCII(UPPER(first_name)))), 3),
INSERT('what is your first name', 9, 4, REPEAT('our', 3)),
REPEAT(INSERT('what is your first name', 1, 1, 'W'), 1),
REPLACE(first_name, 'e', REPEAT('x', 10))
from emp 
where REPEAT(CAST(first_name as char(8)), 2) > 'hanshans'
group by first_name, last_name, hire_date
order by 1, 2 desc, 3 asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s6')
    
    stmt = """create view vemp as
select *
from emp where
REPEAT(UPPER(first_name), 2) =
REPEAT(UPSHIFT(first_name), 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vemp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s7')
    
    stmt = """create view vemp1 as
select *
from emp where
REPEAT(UPPER(first_name), 15) =
REPEAT(UPSHIFT(first_name), 15) and
hire_date = hire_date;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vemp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s8')
    
    stmt = """create view vvemp as
select vemp.hire_date, emp.start_time
from vemp left join emp on
REPEAT(ucase(vemp.first_name), 100) =
REPEAT(UPSHIFT(emp.first_name), 100) and
 vemp.start_time = emp.start_time;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select emp.last_name, emp.hire_date
from emp 
union all
select CHAR(Ascii(REPEAT('@', 15))), v.hire_date
from vemp v
left join vvemp vv on
repeat(cast(vv.hire_date as char(10)), 2) =
repeat(cast(v.hire_date as char(10)), 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s9')
    
    stmt = """select emp.last_name, emp.hire_date, vemp.marital_status
from emp inner join vemp on
CHAR(ascii(REPEAT(UPPER(vemp.last_name), 2))) = 'J';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s10')
    
    # AR 12/08/06 Added order by
    stmt = """select char_length(rEPEAT(last_name, 5)),
char_length(REPEAT(first_name, 3)),
octet_length(rEPEAT(last_name, 5)),
octet_length(REPEAT(first_name, 3)),
max(repeat(last_name, 4)),
min(repeat(char(ascii(lpad(first_name, 10, 'b'))), 5))
from emp 
group by last_name, first_name order by 6,5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s11')
    
    # -------------------------------
    # Cleanup section
    # -------------------------------
    
    stmt = """DROP VIEW  vvemp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP VIEW  vemp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP VIEW  vemp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test006(desc="""a05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA05
    #  Description:        Tests for SQL, use of REPLACE function
    #                      in the select list.  This is a positive
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # REPLACE function syntax:
    # REPLACE{(<exp1>, <exp2>, <exp3>)}
    
    # Create LOG file
    
    # AR 12/15/06 Added order by to get consistent result set
    stmt = """select REPLACE(first_name, 'C', SUBSTRING(first_name, 1, 2)),
REPLACE(last_name, SUBSTRING(last_name from 1 for 2), 'GI'),
REPLACE(first_name, 'R', 'r'),
REPLACE(first_name, 'N', 'm')
from emp 
where ASCII(last_name) IN (ASCII(REPLACE(last_name, 'Y', 'y'))) order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    
    stmt = """prepare p from
select first_name, last_name,
REPLACE(first_name, 'h', 'SHiiiiiiiiiii') ||
',' || REPLACE(last_name, 'CA', 'for'),
REPLACE(LOWER(last_name), 'na', 'ER')
from emp 
where REPLACE(first_name, 'C', 'c') > 'cLARK'
group by last_name, first_name
having REPLACE(trim(first_name) || trim(last_name), 'RJE', '@@@') >
'H'
order by 1 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    
    stmt = """insert into emp values
('david',
REPLACE(LOWER('tess'), LCASE('TESS'), ucase('tess')),
230, 78000, 2,
date '09/02/2100', timestamp '08/01/2020 04:30:00.9999');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from emp order by 3,4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
    
    stmt = """update emp set last_name = REPLACE('tess', 'ss', 'SY')
where REPLACE(UPSHIFT(first_name), 'DAVID', ucase(first_name)) =
'DAVID';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s4')
    
    stmt = """select char_length(trim(SPACE(ascii(REPLACE
(first_name, first_name, UPPER(first_name)))))),
first_name,
REPEAT(REPLACE(last_name, last_name, LOWER(last_name)), 3),
last_name, CHAR(ascii(REPLACE(last_name, 'D', 'open'))),
case
when REPLACE(lcase(last_name), 'w', 'WW') = 'WWhite'
then 'last name is WWhite'
when REPLACE(UPSHIFT(last_name), 'JERRY', 'bond') > 'aname'
then 'I am Jerry Louise'
else 'who are you?'
end
from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s5')
    
    stmt = """select first_name,
REPLACE(first_name, 'E', REPLACE('x', 'x', '&')),
last_name, hire_date,
REPLACE(INSERT
('what is your first name', 1, 1, 'W'), 'W', 'w')
from emp 
where REPLACE(CAST(first_name as char(8)), 'e', 'EEE') > 'CNAME'
group by first_name, last_name, hire_date
order by first_name, last_name, hire_date;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s6')
    
    stmt = """select first_name,
REPLACE(LPAD(first_name, 10, lcase('y')), 'yy', 'YY'),
REPLACE(RPAD(last_name, 15, Ucase(first_name)), 'S', 's'),
INSERT('what is your first name', 9, 4,
REPLACE(last_name, last_name, UPPER(last_name)))
from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s7')
    
    stmt = """delete from emp 
where Replace(Lcase(last_name), lcase('SY'), 'sy') = 'tesy';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """create view vemp as
select * from emp where
REPLACE(
UPPER(first_name), Ucase(first_name), LOWER(first_name))
= Lcase(first_name);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vemp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s8')
    
    stmt = """create view vemp1 as
select * from emp where
REPLACE(UPPER(first_name), UPSHIFT(first_name), 'HaHa') =
REPLACE(UPSHIFT(first_name), UPSHIFT(first_name), 'HaHa') and
hire_date = hire_date;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vemp1 order by 3,4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s9')
    
    stmt = """create view vvemp as
select emp.first_name, vemp.hire_date
from vemp left join emp on
(REPLACE(Ucase(vemp.first_name), 'HOWARD', 'HOW') =
REPLACE(UPSHIFT(emp.first_name), 'HOWARD', 'HOW')) and
(vemp.start_time = emp.start_time);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vvemp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s10')
    
    stmt = """select last_name, start_time
from emp 
union all
select
REPLACE(first_name, first_name, first_name || last_name),
 vemp.start_time
from vemp order by last_name,start_time;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s11')
    
    stmt = """select emp.last_name, emp.hire_date, vemp.marital_status
from emp inner join vemp on
REPLACE(UPPER(emp.last_name), vemp.last_name, 'LAST NAME') =
'LAST NAME';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s12')
    
    stmt = """select char_length(rEPlAce
(last_name, last_name, 'Is this his lname?')),
char_length(REPLACE(first_name, first_name, '12/31/2000')),
octet_length(rEplace
(first_name, first_name, 'So, it is you')),
octet_length(REPLACE
(last_name, last_name, '12/31/2000 12:56:56.0000'))
from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s13')
    
    stmt = """select max(replace(lcase(last_name), 'ry', 'sisi')),
min(replace(upshift(first_name), 'R', 'ban'))
from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s14')
    
    # -------------------------------
    # Cleanup section
    # -------------------------------
    
    stmt = """DROP VIEW  vvemp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP VIEW  vemp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP VIEW  vemp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test007(desc="""a06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA06
    #  Description:        Tests for SQL, use of SPACE function
    #                      in the select list.  This is a positive
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # SPACE function syntax:
    # SPACE{(<count>)}
    
    # Create LOG file
    
    stmt = """select first_name, SPACE(3), '.', last_name,
ASCII(SPACE(13)), char_length(SUBSTRING(SPACE(20), 5, 5)),
SPACE(2) || '###########' || SPACE(10)
from emp 
where 'hans' || SPACE(2) || 'christian' in
('GREENGREEN', 'hans  christian', 'HOWARDHOWARD')
group by first_name, last_name;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s0')
    
    stmt = """insert into emp values
('david', SPACE(2), 230, 78000, 2,
date	'09/03/2050', timestamp '12/25/1998 10:30:00.9999');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s1')
    
    stmt = """update emp set last_name = SPACE(7)
where first_name = 'david';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s2')
    
    stmt = """delete from emp 
where last_name = (SPACE(7));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select * from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s3')
    
    stmt = """select last_name, ASCII(SPACE(10)),
REPLACE(first_name, 'E', SPACE(10)),
case
when last_name = 'JERRY'
then 'last name is JERRY'
when last_name > 'JERRY'
then last_name
else SPACE(10)
end,
first_name, LPAD(first_name, 10, SPACE(3)),
RPAD(last_name, 13, SPACE(3)),
INSERT('what is your first name', 9, 4, SPACE(23))
from emp 
group by first_name, last_name
having last_name not in (SPACE(10))
order by 1, 2 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s4')
    
    stmt = """select char_length(SPACE(105)),
char_length(SPACE(453)),
octet_length(SPACE(1005)),
octet_length(SPACE(4090)),
cast(Space(12) as pic x(12)),
cast(last_name as varchar(21)),
cast(hire_date as char(19))
from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s5')
    
    stmt = """create view vemp as
select last_name, first_name, hire_date
from emp where
ASCII(UPPER(first_name)) =
ASCII(UPSHIFT(first_name));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vemp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s6')
    
    stmt = """select octet_length(
SPACE(ASCII(INSERT('what is your first name', 1, 1, 'W')))),
 emp.last_name, emp.hire_date
from emp 
union all
select char_length(SPACE(2)), last_name, vemp.hire_date
from vemp order by last_name,hire_date;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s7')
    
    stmt = """select emp.first_name, SPACE(2), emp.hire_date, vemp.last_name
from emp left join vemp on emp.last_name like '_R';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s8')
    
    # -------------------------------
    # Cleanup section
    # -------------------------------
    
    stmt = """DROP VIEW  vemp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test008(desc="""a07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA07
    #  Description:        Tests for SQL, use of LPAD function
    #                      in the select list.  This is a positive
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # LPAD function syntax:
    # LPAD{(<exp>, <count> [,<padchar>])}
    
    # Create LOG file
    
    stmt = """select LPAD(first_name, 7, space(1)),
LPAD(first_name, 11, SUBSTRING(last_name for 10)),
LPAD(SUBSTRING(first_name, 2, 8), 11, last_name),
last_name, LPAD(first_name, 15, '.'),
case LPAD(first_name, 13, 'z')
when 'zzzs'   then 'Last name is Christian'
when 'zzzNAR' then 'The name is Jessica'
else concat('I am ', last_name)
end,
LPAD(first_name, 12, '@') || '###########' || SPACE(10)
from emp 
where LPAD(last_name, 12, '*') in
(select LPAD(last_name, 12, '*')
from emp)
group by first_name, last_name
having 'hans' || LPAD('hans', 2) || 'christian' in
('GREENGREEN', 'hans  nschristian', 'HOWARDHOWARD')
order by last_name;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """insert into emp values
('david', LPAD('Last Name', 10, '*'), 230, 78000, 2,
date '09/03/1998', timestamp '01/31/2200 04:58:00.9999');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s1')
    
    stmt = """update emp set last_name = LPAD(first_name, 15, '*')
where lcase(first_name) = 'david';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from emp 
where ascii(first_name) > 90;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s2')
    
    stmt = """delete from emp 
where first_name = 'david';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select last_name, ASCII(LPAD(first_name, 15, '@')),
REPLACE(first_name, 'E', LPAD(first_name, 0, '\$')),
marital_status,
case
when LPAD(last_name, 14, '#') = '####Y'
then 'last name is JERRY'
when last_name > 'JERRY'
then 'last name is ' || last_name
else LPAD(first_name, 10, '&')
end
from emp 
where LPAD(last_name, 11, '@') =
'@' || substring(last_name, 2, char_length(last_name) - 2) and
ascii(lcase(last_name)) > 80
group by first_name, last_name, marital_status
order by last_name;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select first_name,
LPAD(first_name, 12, char(ASCII(RPAD(last_name, 3, '%')))),
LPAD(LPAD(last_name, 13, 'G'), 3, 'B'),
RPAD(LPAD(last_name, 13, 'G'), 3, 'B'),
LPAD(char(ASCII(
INSERT('what is your first name', 1, 1, 'W'))), 1, '!'),
INSERT('what is your first name', 9, 4,
LPAD(last_name, 11, 'Q'))
from emp 
group by first_name, last_name, hire_date
having LPAD(first_name, 13, '#') =
'###' || substring(first_name, 4, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """create view vemp as
select * from emp where
LPAD(first_name, 12, '\$') =
insert(first_name, 11, 2, '\$\$');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select e.last_name, e.start_time
from emp e
union all
select CAST(LPAD(first_name, 10, ')') as varchar(10)),
 vemp.start_time
from vemp 
where vemp.marital_status =
(select e1.marital_status
from emp e1
where e1.hire_date = cast('1977-05-02' as date));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s5')
    
    stmt = """select char_length(LPAD(first_name, 12, '-')) as c1,
char_length(LPAD(last_name, 17, '+')) as c2 ,
octet_length(LPAD(last_name, 14, '=')) as c3,
cast(LPAD(last_name, 13, 'A') as char(19)) as c4,
cast(LPAD(first_name, 13, '%') as varchar(21)) as c5
from emp order by c4,c5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s6')
    
    # -------------------------------
    # Cleanup section
    # -------------------------------
    
    stmt = """DROP VIEW  vemp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test009(desc="""a08"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA08
    #  Description:        Tests for SQL, use of RPAD function
    #                      in the select list.  This is a positive
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # RPAD function syntax:
    # RPAD{(<exp>, <count> [,<padchar>])}
    
    # Create LOG file
    
    stmt = """select first_name, RPAD(first_name, 9, '.'),
RPAD(first_name, 7, ''''''),
RPAD(first_name, 1, SUBSTRING(last_name, 1, 10)),
last_name,
RPAD(SUBSTRING(first_name from 2 for 8), 1, last_name),
RPAD(first_name, 7, SPACE(1)),
max(RPAD
(first_name, 2, '@') || '###########' || SPACE(10))
from emp 
where RPAD(last_name, 2, '*') in
(select RPAD(last_name, 2, '*')
from emp)
group by first_name, last_name
having 'hans' || RPAD('hans', 2) || 'christian' in
('GREENGREEN', 'hansha  christian', 'HOWARDHOWARD');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """prepare p from
insert into emp values
('david', RPAD('Last Name', 3, '*'), 2, 69000, 27,
date '09/03/2078', timestamp '12/23/1998 09:17:53.9999');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s2')
    
    stmt = """update emp set last_name = RPAD(trim(first_name), 10, '*')
where RPAD(trim(first_name), 10, '*') = 'david*****';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s3')
    
    stmt = """delete from emp where RPAD(trim(first_name), 10, '*') = 'david*****';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select last_name, ASCII(CHAR(10)),
REPLACE(first_name, 'E', RPAD(first_name, 0, '\$')),
case
when RPAD(last_name, 4, '#') = 'JERRY ####'
then 'last name is JERRY'
when last_name > 'JERRY'
then last_name
else RPAD(first_name, 10, '&')
end,
hire_date
from emp 
group by first_name, last_name, hire_date
order by last_name desc, hire_date asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s4')
    
    stmt = """select first_name,
RPAD(first_name, 2, char(ascii(RPAD(last_name, 3, '%')))),
RPAD(RPAD(last_name, 13, 'G'), 3, 'B'),
RPAD(LPAD(last_name, 13, 'G'), 3, 'B'),
INSERT('what is your first name', 9, 4,
RPAD(last_name, 1, 'Q')),
RPAD(INSERT('what is your first name', 1, 1, 'W'), 1, '!'),
hire_date
from emp 
where RPAD(cast(hire_date as char(10)), 3, '#') = '1977-05###'
group by first_name, last_name, hire_date
order by 1 desc, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """create view vemp (vc1, vc2, vc3) as
select first_name, RPAD(last_name, 3), start_time
from emp 
where RPAD(first_name, 2, '\$') =
insert(first_name, 9, 2, '\$\$');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # AR 1/17/06 Added order by
    stmt = """select emp.last_name, emp.start_time
from emp 
union all
select CAST(RPAD(v.vc1, 2, ')') as varchar(20)),
v.vc3
from vemp v
left join vemp v1 on
RPAD(v1.vc2, 2) = (select rpad(last_name, 2)
from emp 
where cast(hire_date as char(10)) =
'1984-08-12') order by emp.last_name;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s6')
    
    stmt = """select char_length(RPAD(first_name, 10, '-')),
char_length(RPAD(last_name, 7, '+')),
octet_length(RPAD(last_name, 5, '=')),
octet_length(RPAD(first_name, 3, '`')),
cast(RPAD(last_name, 3, 'A') as char(19)),
RPAD(cast(start_time as varchar(25)), 3, '%'),
RPAD(cast(hire_date as char(10)), 6, 't'),
rpad(first_name, marital_status, 'r')
from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 6)
    
    # for debug purpose
    stmt = """select min(last_name) from emp;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select max(RPAD(cast(hire_date as char(10)), 6, 't')),
min(lpad(last_name, 12, '&'))
from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s8')
    
    # -------------------------------
    # Cleanup section
    # -------------------------------
    
    stmt = """DROP VIEW  vemp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test010(desc="""a09"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA09
    #  Description:        Tests for SQL, use of CONCAT, LCASE,
    #			LOCATE, LTRIM, RTRIM, SUBSTRING, UCASE
    #			functions.  This is a positive test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # function syntax:
    # CONCAT {(<string-exp1>, <string-exp2>)}
    # LCASE {(<string-exp>)}
    # LOCATE {(<string1>, <string-exp2>)}
    # LTRIM {(<string-exp>)}
    # RTRIM {(<string-exp>)}
    # SUBSTRING {(<string>, <start>, <length>)}
    # UCASE {(<string>)}
    
    # Create LOG file
    
    stmt = """SET PARAM ?P1 '   Hello ,   ';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT LTRIM(CONCAT(?P1, 'Robert John,  ' ) || ' @@@ ' ||
CONCAT('Robert John', ?P1)),
RTRIM(CONCAT(?P1, 'Robert John,  ' ) || ' @@@ ' ||
CONCAT('Robert John', ?P1))
FROM emp 
WHERE cast(hire_date as char(10)) < '2000-01-01';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s0')
    
    stmt = """SELECT concat(first_name, last_name),
CONCAT(first_name, CONCAT('   ', last_name))
FROM emp 
WHERE CONCAT(first_name, '.') =
(SELECT CONCAT(first_name, '.')
FROM emp 
WHERE first_name < 'CRA');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s1')
    
    #AR 12/15/06 added order by
    stmt = """SELECT case CONCAT(first_name, last_name)
when 'CLARK     DINAH     '
then 'ok, ' || 'lower ' || lower(first_name)
when 'GREEN     ROGER     '
then 'hi, Roger'
when 'jerry     white     '
then 'well, ' || 'upshift ' || upshift(last_name)
else 'Hi, ' || 'rest of you'
end,
case
when ucase(first_name || last_name) =
'CLARK     DINAH     '
then 'successed upper case'
when lcase(first_name || last_name) =
'jerry     white     '
then 'successed lower case'
when concat(first_name, last_name) = 'GREEN     ROGER     '
then concat('Hello! ', 'Mr. ' || 'Green')
end
FROM emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s2')
    
    stmt = """SELECT LCASE(UCASE(first_name)),
UCASE(LCASE(UPSHIFT(LOWER(last_name)))), start_time,
lcase(concat(first_name, last_name)) as c4,
ucase(concat(first_name, last_name)) as c5
FROM emp 
WHERE UPPER(last_name) = UCASE(last_name) and
LOWER(first_name) = LCASE(first_name) order by c4,c5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s3')
    
    stmt = """SELECT UCASE(CONCAT(first_name, last_name))
FROM emp 
GROUP BY first_name, last_name
HAVING UCASE(CONCAT(first_name, last_name)) in
('CLARK     DINAH', 'jerry     white', 'GREEN     ROGER',
'NONONO    JERRY', 'HOWARD    JERRY', 'ENDENDENDENDENDEND')
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s2a')
    
    stmt = """SELECT UCASE(CONCAT(first_name, last_name))
FROM emp 
WHERE LCASE(first_name) like 'j%' or
LCASE(last_name) like 'c%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s2b')
    
    stmt = """SET PARAM ?P1 '0';"""
    output = _dci.cmdexec(stmt)
    
    # AR 12/15/06 added order by
    stmt = """SELECT LTRIM(' Your last name is?     '), last_name,
RTRIM(' Your first name is     ') || ' ' || first_name,
CONCAT(' Init. ',
SUBSTRING(UCASE(last_name), 1, cast(5 * 2 / 10 as int)))
FROM emp order by last_name;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s4')
    
    stmt = """SELECT LTRIM(
TRIM(leading ' ' from ' ltrim nested with trim   ')),
RTRIM(
TRIM(trailing ' ' from '  rtrim nested with trim ')),
LTRIM(RTRIM('  ltrim with rtrim                     ')),
RTRIM(LTRIM(
TRIM(both from ' three trim functions      ')))
FROM emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s5')
    
    # AR added ordery by
    stmt = """SELECT CONCAT(first_name, last_name) || '  ' ||
cast(hire_date as char(15)),
SUBSTRING(
SUBSTRING(CONCAT(first_name, last_name), cast(8 / 4 as int), 8)
FROM 1 FOR 5)
FROM emp order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s6')
    
    stmt = """SELECT LCASE(first_name),
UCASE(first_name),
locate('start', 'negative start position'),
LOCATE('ry', 'ry' || CONCAT(first_name, last_name)),
LOCATE(ucase('ry'), CONCAT(first_name, last_name)),
locate('wh', last_name),
locate('ite', last_name)
FROM emp order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s7')
    
    stmt = """SELECT LOCATE('', 'null')
FROM emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s8')
    
    stmt = """SELECT LOCATE('n', '')
FROM emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s9')
    
    stmt = """SELECT SUBSTRING(first_name, 2, 10)
FROM emp order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s10')
    
    stmt = """SELECT SUBSTRING(last_name, 20, 5)
FROM emp order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s11')
    
    _testmgr.testcase_end(desc)

def test011(desc="""a10"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA10
    #  Description:        Tests for SQL, use of LEFT function
    #                      in the select list.  This is a positive
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # LEFT function syntax:
    # LEFT{(<exp>, <count>)}
    
    # Create LOG file
    
    stmt = """prepare p from
select LEFT(t1.first_name, cast(33 / 10 - 2 as int)),
LPAD(t1.first_name, 18, '.'),
LEFT(SUBSTRING(t1.last_name from 1 for 10), 1),
LEFT(LEFT(t1.last_name, 2), 1),
LEFT(RIGHT(t1.last_name, 2), 1 * 4),
t1.last_name
from emp t1
where LEFT(RPAD(t1.last_name, 2, '*'), 4) =
(select LEFT(RPAD(t2.last_name, 2, '*'), 4)
from emp t2
where LEFT(RPAD(t2.last_name, 2, '*'), 4) >= 'whit')
group by t1.last_name, t1.first_name;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select t1.last_name, LEFT(LCASE(t1.first_name), 3),
SPACE(10), LEFT(UCASE(t1.first_name), 2),
max(LEFT(UPSHIFT(t1.first_name), 4)),
LEFT(LOWER(t1.last_name), 5)
from emp t1
where LEFT(LPAD(t1.last_name, 12, '*'), 4) in
(select LEFT(LPAD(t2.last_name, 12, '*'), 4) from emp t2)
group by t1.last_name, t1.first_name
order by t1.last_name;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s2')
    
    stmt = """select first_name, last_name,
replace(LEFT(first_name, 2), 'R', 'J'),
min(replace(LEFT(last_name, 2), 'R', 'J') ||
CONCAT('###########', SPACE(10)))
from emp 
group by first_name, last_name
having 'hans' || LEFT('hans', 2) || 'christian' in
('GREENGREEN', 'hanshachristian', 'HOWARDHOWARD');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s3')
    
    stmt = """insert into emp values
('david', LEFT('jungle', 24), 9, 45903.05, 7,
date '09/04/2990', timestamp '04/19/2998 12:32:00.1234');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s4')
    
    stmt = """update emp set last_name = LEFT(first_name, 3)
where LEFT(first_name, 3) = 'dav';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s5')
    
    stmt = """delete from emp 
where LEFT(first_name, 3) = 'dav' or
last_name = 'jungle';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select first_name, ASCII(LEFT(first_name, 1)),
REPLACE(first_name, LEFT(first_name, 1), '%'),
hire_date,
case
when LEFT(last_name, 4) = 'JERR'
then 'last name is JERRY'
when last_name > 'JERRY'
then LEFT(last_name, 3)
else LEFT(first_name, 10)
end
from emp 
where LEFT(last_name, 2) = (
select LEFT(last_name, 2)
from emp 
where LEFT(last_name, 2) = lcase('WH'))
group by first_name, last_name, hire_date
order by first_name;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s6')
    
    stmt = """select first_name,
LEFT(first_name, ASCII(RPAD(last_name, 1, '%'))),
LEFT(LPAD(last_name, 13, 'G'), 19),
RPAD(LEFT(last_name, 3), 12, 'G'),
LEFT(INSERT('what is your first name', 1, 1, 'W'), 1),
INSERT('what is your first name', 9, 4, LEFT(last_name, 5))
from emp 
where LEFT(first_name, 1) =
(select LEFT(first_name, 1)
from emp 
where LEFT(first_name, 1) > 'h')
group by first_name, last_name, hire_date
having cast(LEFT(cast(hire_date as char(10)), 10) as varchar(12)) =
'1923-11-05'
order by first_name asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s7')
    
    stmt = """create view vemp as
select * from emp 
where 	LEFT(first_name, 2) > 'AB';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vemp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s8')
    
    stmt = """create view vemp1 (vc1, vc2, vc3) as
select LEFT(UCASE(first_name), 1), LCASE(last_name),
hire_date
from vemp 
where cast(hire_date as char(10)) < '1980-02-28';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vemp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s9')
    
    stmt = """select vemp1.vc1, first_name, last_name, hire_date
from vemp1 left join vemp on
 vemp.hire_date = vemp1.vc3
order by hire_date asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s10')
    
    stmt = """select emp.last_name, emp.hire_date,
LTRIM(CONCAT('   ', 'ltrim with concat  ')),
RTRIM(CONCAT('   ', 'rtrim with concat  '))
from emp 
union all
select CAST(LEFT(first_name, 2) as pic x(9)), vemp.hire_date,
ltrim('    I am left trimed  :' || ')'),
rtrim(concat('     :', ')') || 'I am right trimed .    ')
from vemp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s11')
    
    stmt = """select char_length(LEFT(first_name, 20)),
char_length(LEFT(cast(start_time as pic x(50)), 17)),
octet_length(LEFT(last_name, 34)),
octet_length(LEFT(cast(hire_date as varchar(20)), 384)),
LEFT(RIGHT(last_name, 3), 2)
from emp 
where LEFT(last_name, char_length(last_name)) =
(select LEFT(last_name, character_length(last_name))
from vemp 
where ASCII(first_name) = 104);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s12')
    
    # -------------------------------
    # Cleanup section
    # -------------------------------
    
    stmt = """DROP VIEW  vemp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP VIEW  vemp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test012(desc="""a11"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA11
    #  Description:        Tests for SQL, use of RIGHT function
    #                      in the select list.  This is a positive
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # RIGHT function syntax:
    # RIGHT{(<exp>, <count>)}
    
    # Create LOG file
    
    stmt = """select RIGHT(t1.first_name, 3 * 2 + 3),
LPAD(t1.first_name, 14, '.'),
RIGHT(SUBSTRING(t1.last_name from 1 for 4), 10),
RIGHT(LEFT(t1.last_name, 2), 6),
RIGHT(RIGHT(t1.last_name, 7), 5),
t1.last_name
from emp t1
where RIGHT(RPAD(t1.last_name, 2, '*'), 4) in
(select RIGHT(RPAD(t2.last_name, 2, '*'), 4)
from emp t2
where RIGHT(RPAD(t2.last_name, 2, '*'), 4) = 'A **')
group by t1.last_name, first_name;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select t1.last_name, RIGHT(LCASE(t1.first_name), 7),
RIGHT(UCASE(t1.first_name), 8),
RIGHT(UPPER(t1.last_name), 6),
RIGHT(LOWER(t1.last_name), 5)
from emp t1
where RIGHT(LPAD(t1.last_name, 12, '*'), 4) in
(select RIGHT(LPAD(t2.last_name, 12, '*'), 4) from emp t2)
group by t1.last_name, t1.first_name
order by t1.last_name;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s1')
    
    stmt = """select first_name, last_name,
replace(RIGHT(first_name, 7), 'R', '&') ||
CONCAT('###########', last_name) || SPACE(10)
from emp 
group by first_name, last_name
having first_name || RIGHT('hans', 2) || 'christian' in
('GREENGREEN%',
'hans      nschristian',
'HOWARD    nschristian');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s2')
    
    stmt = """insert into emp values
('david', RIGHT('Last Name', 24), 230, 78000, 2,
date '09/08/1978', timestamp '01/05/2030 08:21:47.9999');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s3')
    
    stmt = """update emp set last_name = RIGHT(first_name, 3)
where right(last_name, 7) = 't Name';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s4')
    
    stmt = """delete from emp 
where right(last_name, 10) = space(10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select first_name, ASCII(RIGHT(first_name, 8)),
REPLACE(first_name, 'R', RIGHT(first_name, 9)),
hire_date, last_name,
case
when RIGHT(last_name, 7) = 'RY'
then 'last name is JERRY'
when last_name > 'JERRY'
then RIGHT(last_name, 8)
else RIGHT(first_name, 10)
end
from emp 
where RIGHT(last_name, 7) > 'JE'
group by first_name, last_name, hire_date
order by first_name asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s5')
    
    stmt = """select first_name,
RIGHT(first_name, ASCII(RPAD(last_name, 1, '%'))),
RIGHT(LPAD(last_name, 19, 'G'), 5),
RPAD(RIGHT(last_name, 10), 4, 'Y'),
RIGHT(Char(ASCII(INSERT(
'what is your first name', 1, 1, 'K'))), 1),
INSERT('what is your first name', 9, 4, RIGHT(last_name, 5))
from emp 
where RIGHT(first_name, 6) =
(select RIGHT(first_name, 6)
from emp 
group by first_name, hire_date
having RIGHT(cast(hire_date as char(15)), 10) =
'05-02');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s6')
    stmt = """create view vemp as
select *
from emp 
where RIGHT(first_name, 7) < 'avg';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vemp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s7')
    
    stmt = """create view vemp1 (vc1, vc2, vc3) as
select LEFT(UCASE(first_name), 1), LCASE(last_name),
hire_date
from vemp 
where hire_date < date '02/28/1983';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vemp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s8')
    
    stmt = """select vemp1.vc1
from vemp1 left join vemp on
left(right(vemp.first_name, 10), 1) = left(vemp1.vc1, 1) and
 vemp.hire_date = vemp1.vc3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s9')
    
    stmt = """select emp.last_name, emp.hire_date,
LTRIM(CONCAT('   ', 'ltrim with concat  ')),
right(RTRIM(CONCAT('   ', 'rtrim with concat  ')), 11)
from emp 
union all
select CAST(RIGHT(first_name, 9) as pic x(9)), vemp.hire_date,
first_name, last_name
from vemp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s10')
    
    stmt = """select first_name, last_name,
char_length(RIGHT(first_name, 20)),
octet_length(RIGHT(last_name, 34)),
cast(RIGHT(last_name, 5) as char(19)),
RIGHT(cast(hire_date as char(10)), 6),
RIGHT(RIGHT(first_name, 7), 2)
from emp 
where RIGHT(last_name, char_length(last_name)) in
(select RIGHT(last_name, character_length(last_name))
from vemp 
where ASCII(first_name) > 61);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s11')
    
    stmt = """select max(left(first_name, 2)),
min(right(last_name, 15))
from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s12')
    
    # -------------------------------
    # Cleanup section
    # -------------------------------
    
    stmt = """DROP VIEW  vemp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP VIEW  vemp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test013(desc="""n01"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN01
    #  Description:        Tests for SQL, use of ASCII function
    #                      in the select list.  This is a negative
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # ASCII function syntax:
    # ASCII{(<string-exp>)}
    
    # Create LOG file
    
    #  string-exp not used
    
    stmt = """select ASCII() from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select ASCII from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select ASCII, ASCII from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select ASCII ASCII from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    #  string-exp used more than once
    
    stmt = """select ASCII(last_name, last_name) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select ASCII(last_name first_name) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select ASCII(last_name, first_name, last_name) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select ASCII(last_name first_name first_name) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Missing the parentheses
    
    stmt = """select asCii(last_name from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select asCii last_name) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Non-existence column name
    
    stmt = """select asCii(name) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    #  Misspelled table name
    
    stmt = """select ascii(first_name) from enp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    #  Misspelled ASCII
    
    # error different in SQ and NSK
    stmt = """select asdii(last_name) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Misplaced ASCII
    
    stmt = """select last_name
from emp 
where last_name > 'AAAAA'
order by ASCII(last_name);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select last_name
from emp 
where last_name > 'AAAAA'
group by ASCII(last_name);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    #  ASCII typed in more than once
    
    stmt = """select ASCII ASCII(last_name) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select ASCII, ASCII(last_name) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select ASCII, ASCII, ASCII(last_name) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select ASCII ASCII ASCII(last_name) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Invalid string-exp
    
    stmt = """select ASCII(dept_num) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    
    stmt = """select ASCII(salary) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    
    stmt = """select ASCII(&*\$) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select ASCII(999) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    
    stmt = """select ASCII(888.90) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    
    stmt = """select ASCII(hire_date) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    
    stmt = """select ASCII(start_time) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    
    stmt = """select ASCII(NULL) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    _testmgr.testcase_end(desc)

def test014(desc="""n02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN02
    #  Description:        Tests for SQL, use of CHAR function
    #                      in the select list.  This is a negative
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # CHAR function syntax:
    # CHAR{(<ascii-code>)}
    
    # Create LOG file
    
    #  ascii-code not used
    
    stmt = """select CHAR() from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select CHAR from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select CHAR, CHAR from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select CHAR CHAR from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  ascii-code used more than once
    
    stmt = """select CHAR(last_name, last_name) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select CHAR(last_name first_name) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select CHAR(last_name, first_name, last_name) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select CHAR(last_name first_name first_name) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Missing the parentheses
    
    stmt = """select char(last_name from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select Char last_name) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Non-existence column name
    
    stmt = """select chAR(name) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    #  Misspelled CHAR
    
    # error different in SQ and NSK
    stmt = """select CHAT(last_name) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Misplaced CHAR
    
    stmt = """select last_name
from emp 
where last_name > 'AAAAA'
order by CHAR(255);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select last_name
from emp 
where last_name > 'AAAAA'
group by CHAR(254);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    #  CHAR typed in more than once
    
    stmt = """select CHAR CHAR(last_name) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select CHAR, CHAR(last_name) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select CHAR, CHAR, CHAR(last_name) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select CHAR CHAR CHAR(last_name) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Invalid ascii-code
    
    stmt = """select CHAR(dept_num) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    stmt = """select CHAR(salary) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4047')
    
    stmt = """select CHAR(last_name) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select CHAR(&*\$) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select CHAR(888.90) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4047')
    
    stmt = """select CHAR(hire_date) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select CHAR(start_time) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select CHAR(null) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    #  Exceeding the valid max and min limits
    
    stmt = """select CHAR(-1) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8432')
    
    stmt = """select CHAR(-99) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8432')
    
    stmt = """select CHAR(-255) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8432')
    
    stmt = """select CHAR(256) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    stmt = """select CHAR(9999) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    _testmgr.testcase_end(desc)

def test015(desc="""n03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN03
    #  Description:        Tests for SQL, use of INSERT function
    #                      in the select list.  This is a negative
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # INSERT function syntax:
    # INSERT {(<exp1>, <start>, <length>, <exp2>)}
    
    # Create LOG file
    
    #  Missing one or more than one of the required elements
    
    stmt = """select INSERT('BBB') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select INSERT(3, 1, 'qaz') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select INSERT('abc', 2) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select INSERT('abc', 1, 'qcv') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select INSERT('BIE', 2, 1) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  More than required elements are used
    
    stmt = """select INSERT('abc', 3, 1, 2, 'ing') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select INSERT('kjn', 2, 2, 'ing', 'abc') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  INSERT typed in more than once
    
    stmt = """select INSERT INSERT('abd', 2, 1, 'bye') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select INSERT INSERT
INSERT ('abd', 2, 1, 'bye') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled table name
    
    stmt = """select INSERT ('abd', 2, 1, 'bye') from enp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    #  Misspelled INSERT
    
    # error different in SQ and NSK
    stmt = """select INSETT('abd', 2, 1, 'bye') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Misplaced INSERT
    
    stmt = """select INSERT(first_name, 1, 2, 'FF'), last_name
from emp 
where hire_date > '01/04/0000'
order by INSERT(first_name, 1, 1, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select INSERT(first_name, 1, 2, 'FF'), last_name
from emp 
where hire_date > '01/04/0000'
group by INSERT(first_name, 1, 1, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    #  Missing all the required elements
    
    stmt = """select INSERT() from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select INSERT(( from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select INSERT)( from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select INSERT from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Invalid exp1 value
    
    stmt = """select INSERT(abc, 2, 1, 'bye') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select INSERT(123, 2, 3, 'bye') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4051')
    
    stmt = """select INSERT(\$*&, 3, 1, 'BYE') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select INSERT(hire_date, 3, 1, 'BYE') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4051')
    
    stmt = """select INSERT(dept_num, 3, 1, 'BYE') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4051')
    
    stmt = """select INSERT(NULL, 3, 1, 'a') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    #  Invalid start value
    
    stmt = """select INSERT(first_name, 0, 2, 'Fg') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8403')
    
    stmt = """select INSERT('abcdf', a, 3, 'bye') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select INSERT('abcdf', \$, 3, 'bye') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select INSERT('abcdf', start_time, 3, 'bye') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4035')
    
    stmt = """select insert('abcdf', null, 3, 'bye') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4098')
    
    #  start value < 0
    
    stmt = """select INSERT('abdge', -3, 4, 'pqnoop') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8432')
    
    #  Invalid length value
    
    stmt = """select INSERT('abcdf', 1, \$, 'bye') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select INSERT('abcdf', 1, a, 'bye') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select INSERT('abcdf', 1, start_time, 'bye') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4053')
    
    stmt = """select INSERT('ehi,ens', 8, 5+null, 'mary') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4098')
    
    stmt = """select INSERT('ehi,ens', 8 * null, 5, 'mary') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4098')
    
    stmt = """select INSERT('abdge', 3, -4, 'pqnoop') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8432')
    
    stmt = """select insert('abdge', 3, null , 'pqnoop') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    stmt = """select insert('abdge', 3, 12.9 , 'pqnoop') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4053')
    
    stmt = """select insert('abdge', 3.4, 12 , 'pqnoop') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4047')
    
    #  Invalid exp2 value
    
    stmt = """select INSERT('abc', 2, 1, bye) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select INSERT('bnie', 2, 3, 123) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4034')
    
    stmt = """select INSERT('BYE', 3, 1, \$%*) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select INSERT('BYE', 3, 1, hire_date) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4034')
    
    stmt = """select INSERT(first_name, 3, 2, null) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    _testmgr.testcase_end(desc)

def test016(desc="""n04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN04
    #  Description:        Tests for SQL, use of REPEAT function
    #                      in the select list.  This is a negative
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # REPEAT function syntax:
    # REPEAT{(<exp>, <count>)}
    
    # Create LOG file
    
    #  Missing required elements
    
    stmt = """select REPEAT() from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select REPEAT(last_name, ) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select REPEAT(first_name) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select REPEAT from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select REPEAT (( from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  REPEAT typed in more than once
    
    stmt = """select REPEAT, REPEAT from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select REPEAT REPEAT from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    #  More than required elements
    
    stmt = """select REPEAT(first_name, 3, 1) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select REPEAT('high', 2, 99) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select REPEAT('HGIT', 1, ab) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Non-existence column name
    
    stmt = """select REPEAT(col_name, 2) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    #  Misspelled table name
    
    stmt = """select REPEAT('high', 2) from enp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    #  Misspelled REPEAT
    
    # error different in SQ and NSK
    stmt = """select REPPTE(last_name, 4) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Misplaced REPEAT
    
    stmt = """select first_name
from emp 
order by REPPTE(first_name, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select last_name
from emp 
group by REPEAT(last_name, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    #  Invalid exp
    
    stmt = """select REPEAT(dept_num, 25) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4051')
    
    stmt = """select REPEAT(salary, 3) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4051')
    
    stmt = """select REPEAT(&*\$, 100) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select REPEAT(999, 999) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4051')
    
    stmt = """select REPEAT(888.90, 10234) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4051')
    
    stmt = """select REPEAT(hire_date, 33) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4051')
    
    stmt = """select REPEAT(start_time, 87) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4051')
    
    stmt = """select REPEAT(order, 3) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select REPEAT(NULL, 2) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    #  Missing exp value
    
    stmt = """select REPEAT(4) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select REPEAT(, 5) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Invalid count value
    
    stmt = """select REPEAT('karyt', abt) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select REPEAT('karyt', %##) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select REPEAT('karyt', hire_date) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4052')
    
    stmt = """select REPEAT(first_name, 9999999999999999999)
from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4116')
    
    stmt = """select REPEAT('negative count', -26) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8432')
    
    stmt = """select REPEAT('negative count', -1) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8432')
    
    stmt = """select REPEAT('NULL value', null) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    stmt = """select REPEAT('negative count', null - 1) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4098')
    
    _testmgr.testcase_end(desc)

def test017(desc="""n05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN05
    #  Description:        Tests for SQL, use of REPLACE function
    #                      in the select list.  This is a negative
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # REPLACE function syntax:
    # REPLACE {(<exp1>, <exp2>, <exp3>)}
    
    # Create LOG file
    
    #  Missing one or more than one of the required elements
    
    stmt = """select REPLACE('BBB') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select REPLACE('qaz', 'a') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select REPLACE() from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select REPLACE from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  More than required elements are used
    
    stmt = """select REPLACE('abc', 'b', 'c', 'a') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select REPLACE('kjn', 'k', 'j', 'c', 'j') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  REPLACE typed in more than once
    
    stmt = """select REPLACE REPLACE('abd', 'd', ';') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select REPLACE REPLACE
REPLACE ('abd', 'b', 'M') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled the table name
    
    stmt = """select REPLACE ('abd', 'b', 'M') from emo;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    #  Non-existence column name
    
    stmt = """select REPLACE (col_name, 'b', 'M') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    #  Misspelled REPLACE
    
    # error different in SQ and NSK
    stmt = """select REOLACE('abd', 2, 1, 'bye') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Misplaced REPLACE
    
    stmt = """select first_name
from emp 
order by REPLACE(last_name, 'D', 'open');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select last_name
from emp 
group by REPLACE(last_name, 'D', 'open');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    #  Missing all the required elements
    
    stmt = """select REPLACE() from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select REPLACE from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Invalid exp1 value
    
    stmt = """select REPLACE(abc, 'abc', 'bye') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select REPLACE(123, '123', 'bye') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4064')
    
    stmt = """select REPLACE(\$*&, '\$*&', 'BYE') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select REPLACE(hire_date, '5', 'BYE') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4064')
    
    stmt = """select REPLACE(col_1, '5', 'BYE') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select REPLACE(NULL, 'a', 'b') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    stmt = """select replace(start_time, '11', last_name) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4064')
    
    #  Invalid exp2 value
    
    stmt = """select REPLACE('abc', abc, 'bye') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select REPLACE('123', 123, 'bye') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4041')
    
    stmt = """select REPLACE('\$*&', \$*&, 'BYE') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select REPLACE('5', hire_date, '3') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4041')
    
    stmt = """select REPLACE(first_name, col_1, 'a') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select REPLACE(first_name, null, 'n') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    stmt = """select replace(first_name, start_time, last_name) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4041')
    
    #  Invalid exp3 value
    
    stmt = """select REPLACE('abc', 'abc', bye) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select REPLACE('123', '123', by) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select REPLACE('\$*&', '\$*&', B) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select REPLACE('2345655', '5', 3) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4064')
    
    stmt = """select REPLACE(first_name, 'e', col_name) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select REPLACE(last_name, 'R', null) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    stmt = """select replace(first_name, first_name, hire_date) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4064')
    
    stmt = """select replace(first_name, first_name, 12345667) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4064')
    
    stmt = """select replace(first_name, 's', start_time) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4064')
    
    _testmgr.testcase_end(desc)

def test018(desc="""n06.temp"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN06
    #  Description:        Tests for SQL, use of SPACE function
    #                      in the select list.  This is a negative
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # SPACE function syntax:
    # SPACE{(<count>)}
    
    # Create LOG file
    
    #  count not used
    
    stmt = """select SPACE() from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select SPACE from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select SPACE, SPACE from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select SPACE SPACE from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    #  count used more than once
    
    stmt = """select SPACE(10, 1) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select SPACE(10, 99, 100) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Missing the parentheses
    
    stmt = """select Space(3 from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select SpAcE 5) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled table name
    
    stmt = """select space(1) from enp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    #  Misspelled SPACE
    
    # error different in SQ and NSK
    stmt = """select SPSCE(34) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Misplaced SPACE
    
    stmt = """select hire_date
from emp 
order by SPACE(10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select start_time
from emp 
group by SPACE(10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    #  SPACE typed in more than once
    
    stmt = """select SPACE SPACE(10) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select SPACE, SPACE(3) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select SPACE, SPACE, SPACE(5) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select SPACE SPACE SPACE(99) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Invalid count
    
    stmt = """select SPACE(salary) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4047')
    
    stmt = """select SPACE(&*\$) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select SPACE(888.90) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4047')
    
    stmt = """select SPACE(hire_date) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4052')
    
    stmt = """select SPACE(start_time) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4052')
    
    stmt = """select SPACE(NULL) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    stmt = """select SPACE(999 * null) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4098')
    
    stmt = """select SPACE(-999) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8432')
    
    # count > possible maximum number
    stmt = """select SPACE(999999999)
from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4129')
    
    _testmgr.testcase_end(desc)

def test019(desc="""n07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN07
    #  Description:        Tests for SQL, use of LPAD function
    #                      in the select list.  This is a negative
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # LPAD function syntax:
    # LPAD{(<exp>, <count>[, <padchar>])}
    
    # Create LOG file
    
    #  Missing required elements
    
    stmt = """select LPAD() from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select LPAD(last_name, ) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select LPAD(first_name) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select LPAD from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select LPAD)( from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  LPAD typed in more than once
    
    stmt = """select LPAD, LPAD(last_name, 5) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select LPAD LPAD(last_name, 5) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select LPAD LPAD LPAD(first_name, 2, 'a') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  More than required elements
    
    stmt = """select LPAD(first_name, 3, 1, last_name) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select LPAD(first_name, last_name, 3, last_name) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Missing the parentheses
    
    stmt = """select lpad(last_name, 4 from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select lpad last_name, 5, 'z') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled table name
    
    stmt = """select lpad(first_name, 1, 'b') from enp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    #  Misspelled LPAD
    # error different in SQ and NSK
    stmt = """select LPAAD(last_name, 4) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Misplaced LPAD
    
    stmt = """select first_name
from emp 
order by LPAD(first_name, 5, 'a');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select last_name
from emp 
group by LPAD(last_name, 5, 'W');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    #  Invalid exp
    
    stmt = """select LPAD(dept_num, 3) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    
    stmt = """select LPAD(salary, 4) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    
    stmt = """select LPAD(\&*$, 2, 'a') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select LPAD(999, 9) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    
    stmt = """select LPAD(888.90, 8 'b') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select LPAD(hire_date, 12, 'y') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    
    stmt = """select LPAD(start_time, 20) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    
    stmt = """select LPAD(no_such_row, 19) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select LPAD(no_such_row, 87, 'b') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select LPAD(null, 9, 'n') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    #  Missing exp value
    
    stmt = """select LPAD(4) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select LPAD(, 5) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select LPAD(4, 'A') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    
    stmt = """select LPAD(, 5, 'B') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Invalid count value
    
    stmt = """select LPAD('karyt', abt) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select LPAD('karyt', %##) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select LPAD('karyt', hire_date) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4041')
    
    stmt = """select LPAD(first_name, null) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4099')
    _dci.expect_error_msg(output, '4062')
    
    stmt = """select LPAD(first_name, 19 / null) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4098')
    
    stmt = """select lpad(first_name, -19) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8403')
    
    stmt = """select lpad(last_name, no_such_col, 'a') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    #  The count value is greater than the length of character string
    
    stmt = """select lpad(last_name, 20, 'x') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n07exp""", 'n07s37')
    
    #  Invalid padchar value
    
    stmt = """select LPAD(last_name, 5, B) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select LPAD(last_name, 5, \$) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select LPAD(first_name, 9, %8) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select LPAD(first_name, 7, null) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    stmt = """select lpad('negative test', 5, hire_date) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4051')
    
    _testmgr.testcase_end(desc)

def test020(desc="""n08"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN08
    #  Description:        Tests for SQL, use of RPAD function
    #                      in the select list.  This is a negative
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # RPAD function syntax:
    # RPAD{(<exp>, <count>[, <padchar>])}
    
    # Create LOG file
    #  Missing required elements
    stmt = """select RPAD() from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select RPAD(last_name, ) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select RPAD(first_name) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select RPAD from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    #  RPAD typed in more than once
    
    stmt = """select RPAD, RPAD(last_name, 5) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select RPAD RPAD(last_name, 5) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select RPAD RPAD RPAD (first_name, 2, last_name) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  More than required elements
    
    stmt = """select RPAD(first_name, 3, 1, 'wrong, wrong, ') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Missing the parentheses
    
    stmt = """select rpad(last_name, 4 from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select rpad last_name, 5, 'z') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled table name
    
    stmt = """select rpad(first_name, 1, 'b') from enp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    #  Misspelled RPAD
    # error different in SQ and NSK
    stmt = """select RPAAD(last_name, 4) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Misplaced RPAD
    
    stmt = """select first_name
from emp 
order by RPAD(first_name, 5, 'a');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select last_name
from emp 
group by RPAD(last_name, 5, 'W');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    #  Invalid exp
    
    stmt = """select RPAD(dept_num, 3) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    
    stmt = """select RPAD(salary, 4) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    
    stmt = """select RPAD(&*\$, 2, 'a') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select RPAD(999, 9) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    
    stmt = """select RPAD(888.90, 8, 'b') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    
    stmt = """select RPAD(hire_date, 12) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    
    stmt = """select RPAD(start_time, 20) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    
    stmt = """select RPAD(no_such_col, 45, 'q') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select RPAD(no_such_col, 94) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select RPAD(null, 8) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    #  Missing exp value
    
    stmt = """select RPAD(4) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select RPAD(, 5) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select RPAD(4, 'A') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    
    stmt = """select RPAD(, 5, 'B') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Invalid count value
    
    stmt = """select RPAD('karyt', abt) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select RPAD('karyt', %##) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select RPAD('karyt', hire_date) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4041')
    _dci.expect_error_msg(output, '4062')
    
    stmt = """select RPAD(last_name, null) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4047')
    
    stmt = """select RPAD(last_name, null + 99) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4098')
    
    stmt = """select Rpad(first_name, -19) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8403')
    
    stmt = """select Rpad(no_such_col, 5, 'a') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select rpad(first_name, 999.9911, 'a') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4047')
    
    #  The count value is greater than the length of character length
    
    stmt = """select rpad(last_name, 78, 'y') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n08exp""", 'n08s35')
    
    #  Invalid padchar value
    
    stmt = """select RPAD(last_name, 5, B) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select RPAD(last_name, 5, \$) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select RPAD(first_name, 9, %8) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select RPAD(first_name, 3, null) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    stmt = """select rpad('wrong', 3, start_time) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4051')
    
    _testmgr.testcase_end(desc)

def test021(desc="""n09"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN09
    #  Description:        Tests for SQL, use of CONCAT, LCASE,
    #			LENGTH, LOCATE, LTRIM, RTRIM, SUBSTRING,
    #			UCASE functions.  This is a negative test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # function syntax:
    # CONCAT {(<string-exp1>, <string-exp2>)}
    # LCASE {(<string-exp>)}
    # LENGTH {(<string-exp>)}
    # LOCATE {(<string1>, <string-exp2>)}
    # LTRIM {(<string-exp>)}
    # RTRIM {(<string-exp>)}
    # SUBSTRING {(<string>, <start>, <length>)}
    # UCASE {(<string>)}
    
    # Create LOG file
    
    #  Concatenate with no string
    stmt = """SELECT CONCAT()
FROM  emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """SELECT CONCAT(( from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """SELECT CONCAT from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    #  Concatenate with an empty string
    stmt = """SELECT CONCAT(first_name, )
FROM emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """SELECT CONCAT(, 'empty string ') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Concatenation with non-string values
    stmt = """SELECT CONCAT('concatenation with numbers ', 12345)
FROM emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4034')
    
    #  Missplaced CONCAT
    stmt = """SELECT first_name
FROM emp 
GROUP BY CONCAT(first_name, last_name);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    stmt = """SELECT first_name
FROM emp 
ORDER BY CONCAT(first_name, last_name);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  SUBSTRING without character string.
    stmt = """SELECT SUBSTRING(), last_name
FROM emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  SUBSTRING typed twice.
    stmt = """SELECT hire_date,
SUBSTRING SUBSTRING('Robert John Smith', 'bad'),
start_time
FROM emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  SUBSTRING string without quotes.
    stmt = """SELECT SUBSTRING('123456789', 4, aabbdc), first_name
FROM emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    #  SUBSTRING string missing the start position.
    stmt = """SELECT SUBSTRING('123456789', 'aabbdc'), first_name
FROM emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4052')
    
    #  Invalid start, length values
    
    stmt = """select SUBSTRING(last_name, 4 / null, 3) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4098')
    
    stmt = """select SUBSTRING(last_name, 2, 3 - null) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4098')
    
    #  Mispalced SUBSTRING
    
    stmt = """SELECT first_name
FROM emp 
GROUP BY SUBSTRING(first_name, 1, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    stmt = """SELECT first_name
FROM emp 
ORDER BY SUBSTRING(last_name, 1, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  LOCATE twice
    stmt = """SELECT LOCATE LOCATE('AAA', first_name)
FROM emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  More than required string expression entered
    stmt = """SELECT LOCATE('re', 'ry', last_name, 1)
FROM emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select locate('re', 'ry', 2) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n09exp""", 'n09s18')
    
    #  Substring is a numeric value
    stmt = """SELECT LOCATE(1234567, 'Hello, and Hello')
FROM emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4063')
    
    stmt = """SELECT LOCATE('Hello, and Hello', 1234567)
FROM emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4063')
    
    #  substring is a null value
    stmt = """SELECT LOCATE(NULL, last_name, 3)
FROM emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    stmt = """SELECT LOCATE('this is null value', null)
FROM emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    stmt = """SELECT LOCATE('null') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """SELECT LOCATE(12345) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misplaced LOCATE
    
    stmt = """SELECT first_name
FROM emp 
GROUP BY LOCATE(first_name, 'ry');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    stmt = """SELECT first_name
FROM emp 
ORDER BY LOCATE(first_name, 'ry');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select LCASE LCASE(first_name)
from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select LCASE(121312)
from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    
    stmt = """select LCASE(-2345)
from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    
    stmt = """select LCASE(null)
from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    stmt = """select first_name, hire_date
from emp 
order by LCASE(first_name);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select last_name, start_time
from emp 
group by LCASE(last_name);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    stmt = """select UCASE
from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """selec UCASE ()
from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select UCASE(first_name, last_name)
from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select UCASE(non_col)
from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select UCASE(121312)
from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    
    stmt = """select UCASE(-999)
from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    
    stmt = """select UCASE(null)
from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    stmt = """select first_name, hire_date
from emp 
order by UCASE(first_name);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select last_name, start_time
from emp 
group by UCASE(last_name);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    stmt = """SELECT rtrim()
from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select ltrim()
from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """SELECT rtrim(non_exist_col)
from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select ltrim(non_exist_col)
from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """SELECT rtrim(first_name, last_name)
from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """select rtrim(trailing 'bb' from last_name)
from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select rtrim(both ' ' from first_name)
from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select ltrim(first_name, last_name)
from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select ltrim(leading 'ab' from first_name)
from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """SELECT rtrim(76543)
from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4133')
    
    stmt = """select rtrim(null)
from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    stmt = """select ltrim(-232425)
from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4133')
    
    stmt = """select ltrim(null)
from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    stmt = """SELECT rtrim(first_name)
from x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    stmt = """select ltrim(last_name)
from x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    stmt = """select first_name, hire_date
from emp 
order by ltrim(first_name);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select last_name, start_time
from emp 
group by rtrim(last_name);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    stmt = """select SUBSTRING() from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select SUBSTRING(first_name, 1) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n09exp""", 'n09s58')
    
    stmt = """select SUBSTRING('Missing ') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select SUBSTRING(invalid_string, 1, 2) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select SUBSTRING(NUll, 1, 3) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    stmt = """select SUBSTRING('invalid start', &, 2) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select SUBSTRING('null value for start', null, 2) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    stmt = """select SUBSTRING('INVALID LENGTH', 1, AB) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select SUBSTRING('NULL VALUE FOR LENGTH', 1, NULL) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    stmt = """select substring('abdee', 3.3, 1) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4047')
    
    stmt = """select substring('abdee', 3, 1.3) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4047')
    
    _testmgr.testcase_end(desc)

def test022(desc="""n10"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN10
    #  Description:        Tests for SQL, use of LEFT function
    #                      in the select list.  This is a negative
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # LEFT function syntax:
    # LEFT{(<exp>, <count>)}
    
    # Create LOG file
    
    #  Missing one or both required elements
    
    stmt = """select LEFT(first_name) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select LEFT(first_name, ) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select LEFT() from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select LEFT from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select LEFT)( from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  More than required elements
    
    stmt = """select LEFT(last_name, first_name, 3) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select LEFT(first_name, last_name, 1, 5) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  LEFT typed more than once
    
    stmt = """select LEFT LEFT(first_name, 3) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Missing the parentheses
    
    stmt = """select left(last_name, 4 from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select left last_name, 5) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select left last_name, 2( from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled table name
    
    stmt = """select Left(first_name, 1) from enp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    #  Misspelled LEFT
    stmt = """select LEFR(last_name, 1) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Misplaced LEFT
    
    stmt = """select first_name, hire_date
from emp t1
order by LEFT(t1.last_name, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select first_name, hire_date
from emp t1
group by LEFT(t1.last_name, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    #  Invalid exp
    
    stmt = """select LEFT(9999, 9999) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4051')
    
    stmt = """select LEFT(###@, 3) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select LEFT(hire_date, 6) from emp order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4051')
    stmt = """select LEFT(null, 10) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    stmt = """select LEFT('missing quote, 22) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15005')
    stmt = """select LEFT(missing_everything, 53) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    stmt = """select LEFT(no_such_col, 199) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    #  Invalid count
    
    stmt = """select LEFT(first_name, ##) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select LEFT('invalid count', ab) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    stmt = """select LEFT('null count', null) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4046')
    stmt = """select LEFT('date count1', hire_date) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4046')
    stmt = """select LEFT('date count2', '07/22/98') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4046')
    stmt = """SElect Left(last_name, -23) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8403')
    stmt = """select LEFT('over largest count', 99999999999999999999999999999)
from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    stmt = """select LEFT('null count', 35 * null + 100) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4098')
    
    stmt = """SElect Left(last_name, 2.3) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4047')
    
    _testmgr.testcase_end(desc)

def test023(desc="""n11"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN11
    #  Description:        Tests for SQL, use of RIGHT function
    #                      in the select list.  This is a negative
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # RIGHT function syntax:
    # RIGHT{(<exp>, <count>)}
    
    # Create LOG file
    
    #  Missing one or both required elements
    
    stmt = """select RIGHT(first_name) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select RIGHT(first_name, ) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select RIGHT() from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select RIGHT from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select RIGHT  )) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  More than required elements
    
    stmt = """select RIGHT(last_name, first_name, 3) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select RIGHT(first_name, last_name, 1, 5) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  RIGHT typed more than once
    
    stmt = """select RIGHT RIGHT(first_name, 3) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Missing the parentheses
    
    stmt = """select right(last_name, 4 from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select right last_name, 5) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select right last_name, 2( from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled table name
    
    stmt = """select Right(first_name, 1) from enp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    #  Misseplled RIGHT
    stmt = """select RIGGTY(last_name, 1) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Misplaced RIGHT
    
    stmt = """select first_name, hire_date
from emp t1
order by RIGHT(t1.last_name, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select first_name, hire_date
from emp t1
group by RIGHT(t1.last_name, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    #  Invalid exp
    
    stmt = """select RIGHT(9999, 9999) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    stmt = """select RIGHT(###@, 3) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select RIGHT(hire_date, 6) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    stmt = """select RIGHT(null, 10) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    stmt = """select RIGHT('missing quote, 22) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15005')
    stmt = """select RIGHT(missing_everything, 53) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    stmt = """select RIGHT(no_such_col, 199) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    #  Invalid count
    
    stmt = """select RIGHT(first_name, ##) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select RIGHT('invalid count', ab) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    stmt = """select RIGHT('null count', null) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4046')
    stmt = """select RIGHT('date count1', hire_date) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4046')
    stmt = """select RIGHT('date count2', '07/22/98') from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4046')
    stmt = """SElect right(last_name, -23) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8432')
    stmt = """select RIGHT('over size count', 9999999999999999999999999999999)
from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    stmt = """select RIGHT('null count', null / 98 + 34) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4098')
    
    stmt = """select right('robert left', -3.3) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4047')
    
    stmt = """select right('robert left', 3.3) from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4047')
    
    # -------------------------------
    # Clean up section
    # -------------------------------
    stmt = """drop table emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

