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
    
    #create schema arkt0197;
    # table BTRE211 is used in testA00, testA02, testA04 & testB05
    
    stmt = """CREATE TABLE BTRE211 (
Y_to_D DATE,
Y_to_S TIMESTAMP,
Y_to_F TIMESTAMP(6),
H_to_S TIME,
H_to_F TIME(6)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # the view pvA41 is used in testA04
    
    stmt = """CREATE VIEW pvA41 (a,b,c,d,e) AS
SELECT * FROM BTRE211;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO BTRE211 VALUES (
date  '1988-01-01' ,
timestamp  '1988-01-01:12:35:30' ,
timestamp  '1988-01-01:12:35:30.333' ,
time  '10:15:30' ,
time  '10:15:30.555'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE211 VALUES (
date '1977-03-02' ,
timestamp '1979-06-05:14:40:45' ,
timestamp '1980-07-06:15:45:50.678' ,
time '03:53:56' ,
time '04:54:57.345'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE211 VALUES (
date '0802-09-07' ,
timestamp '0805-12-10:07:59:03' ,
timestamp  '0806-01-11:08:01:04.789' ,
time '18:08:09' ,
time '19:09:10.234'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE211 VALUES (
date  '0001-01-01' ,
timestamp '0001-01-01:00:00:00' ,
timestamp '0001-01-01:00:00:00.00' ,
time '00:00:00' ,
time '00:00:00.00'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # table BTRE213 is used in testA01b
    
    stmt = """CREATE TABLE BTRE213 (
DATE1 DATE,
TIME1 TIME
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view pvre213a as
select date1 from BTRE213 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view pvre213b (d, c) as
select date1, extract(year from current_date)
from BTRE213 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table a1table0 (
char_1     char(1),
y_to_m     timestamp,
var_char_3 varchar(3),
y_to_d     date
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # table A3TABLE0 is used in testA03
    
    stmt = """CREATE TABLE A3TABLE0 (
D_of_W  INTEGER,
Y_to_D DATE
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # table a5table0 is used in testA05
    
    stmt = """create table a5table0 (
t_stamp   largeint,
the_date  timestamp(6),
animal    pic x(11),
vegetable varchar(09) UPSHIFT,
number1    pic 9(01)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # table a5table0 is used in testA05
    
    # create table a5table1 (		XXXXX can't do DEFAULT
    #     keydate    TIMESTAMP (6) default current_timestamp not null,
    #     nonkeydate TIMESTAMP (6) default current_timestamp,
    #     i          integer,
    #     primary key (keydate)
    #     );
    
    stmt = """create table a5table1 (
keydate    TIMESTAMP (6) not null,
nonkeydate TIMESTAMP (6),
i          integer,
primary key (keydate)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # table a6table0 is used in testA06
    
    stmt = """create table a6table0 (
j_bdate     largeint,
name1        pic x(11) UPSHIFT,
birthdate   timestamp(6),
hobbies     varchar(39)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # table t921204 is used in testB07
    
    stmt = """CREATE TABLE t921204 (
c1 char(1),
c2 timestamp(6)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT into t921204 values
( '1', current_timestamp(6));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT into t921204 values
( '2', current_timestamp(6));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """UPDATE STATISTICS for table t921204;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test002(desc="""a01"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0197 : testA00
    #  Description:        Datetime function CURRENT - basic.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """delete from BTRE211;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    stmt = """insert into BTRE211 values(
current_date,
current_timestamp,
current_timestamp(6),
current_time,
current_time(6)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from BTRE211;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    # expect 1 row with values varying according to the current date & time
    
    stmt = """update BTRE211 
set y_to_s = timestamp '1999-01-01:01:01:01',
y_to_d     = current_date
where h_to_s  = current_time;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    stmt = """delete from BTRE211 
where y_to_d  = current_date;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select * from BTRE211;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    # expect 0 rows
    
    stmt = """select y_to_f from BTRE211 
where y_to_d  = current_date
order by y_to_d asc, y_to_f desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    _testmgr.testcase_end(desc)

def test003(desc="""a01b"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0197 : testA01
    #  Description:        Datetime function CURRENT.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the 'Title'
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """select date1 , CURRENT_date from BTRE213 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select 'a' from BTRE213 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select CURRENT_date, current_time from BTRE213 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select 'a' from BTRE213 
union
select 'a' from BTRE213 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select CURRENT_date from BTRE213 
union
select CURRENT_date from BTRE213 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # header for select from view with current.
    stmt = """select 'a' from pvre213a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select CURRENT_date, * from pvre213a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select min(d), c from pvre213b group by c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # CURRENT function with an 'OR'
    stmt = """insert into a1table0 
values ('1', CURRENT_timestamp, 'dlh', current_date);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into a1table0 
values ('2', timestamp '1990-07-28:23:45:01.01' ,' *',
CURRENT_date);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into a1table0 
values ('3', timestamp '1990-01-01:04:45:01.01' , 'c ',
date '2020-11-28' );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into a1table0 (char_1, y_to_m, var_char_3, y_to_d)
values ('4', timestamp '1990-05-14:11:59:01.01',' 4 ',
CURRENT_date);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from a1table0 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    #  expect 4 rows with varying values according to the current date & time
    
    ##1
    stmt = """select * from a1table0 where y_to_m IN
(select y_to_m from a1table0 
where y_to_m <> CURRENT_timestamp OR char_1 > '0' );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    ##2
    stmt = """select * from a1table0 where y_to_m IN
(select y_to_m from a1table0 
where y_to_m <> CURRENT_timestamp OR var_char_3 LIKE
'%dlh%');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    ##3
    stmt = """select * from a1table0 where y_to_d >
(select y_to_d from a1table0 
where var_char_3 = '4' OR y_to_d < CURRENT_date);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # #4
    stmt = """select y_to_m, DATEFORMAT(y_to_m,usa), y_to_d from a1table0 
where y_to_d <
(select y_to_d from a1table0 
where y_to_d > CURRENT_date OR char_1 = '0');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    ##5
    stmt = """select char_1, DATEFORMAT(y_to_d,european), y_to_d from a1table0 
where y_to_d = ALL
(select y_to_d from a1table0 
where y_to_d = CURRENT_date OR char_1 is NOT NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # #6
    stmt = """select * from a1table0 where y_to_m < ANY
(select y_to_m from a1table0 
where y_to_m = CURRENT_timestamp OR char_1 is NOT NULL)
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    _testmgr.testcase_end(desc)

def test004(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0197 : testA02
    #  Description:        Datetime function DATEFORMAT.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the 'Title'
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """INSERT INTO BTRE211 VALUES (
date  '1988-01-01' ,
timestamp  '1988-01-01:12:35:30' ,
timestamp  '1988-01-01:12:35:30.333' ,
time  '10:15:30' ,
time  '10:15:30.555'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE211 VALUES (
date '1977-03-02' ,
timestamp '1979-06-05:14:40:45' ,
timestamp '1980-07-06:15:45:50.678' ,
time '03:53:56' ,
time '04:54:57.345'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE211 VALUES (
date '0802-09-07' ,
timestamp '0805-12-10:07:59:03' ,
timestamp  '0806-01-11:08:01:04.789' ,
time '18:08:09' ,
time '19:09:10.234'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE211 VALUES (
date  '0001-01-01' ,
timestamp '0001-01-01:00:00:00' ,
timestamp '0001-01-01:00:00:00.00' ,
time '00:00:00' ,
time '00:00:00.00'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select Y_to_D, Y_to_S, Y_to_F from BTRE211;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    #  expect 4 rows with the following values in any order:
    #  1988-01-01  1988-01-01 12:35:30.000000  1988-01-01 12:35:30.333
    #  1977-03-02  1979-06-05 14:40:45.000000  1980-07-06 15:45:50.678
    #  0802-09-07  0805-12-10 07:59:03.000000  0806-01-11 08:01:04.789
    #  0001-01-01  0001-01-01 00:00:00.000000  0001-01-01 00:00:00.000
    
    stmt = """select H_to_S, H_to_F from BTRE211;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    #  expect 4 rows with the following values in any order:
    #  10:15:30  10:15:30.555000
    #  03:53:56  04:54:57.345000
    #  18:08:09  19:09:10.234000
    #  00:00:00  00:00:00.000000
    
    stmt = """select y_to_s ,dateformat (y_to_s,default ) from BTRE211 
where y_to_s >
timestamp '01/01/0001 11:00:00 am' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    #  expect 3 rows
    
    stmt = """select y_to_s ,dateformat (y_to_s,usa ) from BTRE211 
where y_to_s >
timestamp '01/01/0001 11:00:00 am' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    #  expect 3 rows
    
    stmt = """select y_to_s ,dateformat (y_to_s,european) from BTRE211 
where y_to_s >
timestamp '01/01/0001 11:00:00 am';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s4')
    #  expect 3 rows
    
    stmt = """select y_to_d,
dateformat (y_to_d, usa),
h_to_s,
dateformat (h_to_s, default)
from BTRE211;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')
    
    _testmgr.testcase_end(desc)

def test005(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0197 : testA03
    #  Description:        Datetime function DAYOFWEEK.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:    (provide a high-level description)
    #
    #  Notes:
    #  The DAYOFWEEK function returns integers from 1..7 with 1 = Sunday
    #
    # =================== End Test Case Header  ===================
    
    stmt = """delete from A3TABLE0;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO A3TABLE0 VALUES (
DAYOFWEEK  (date '1989-02-04'),
date '1989-02-04'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # a Saturday = 7
    
    stmt = """INSERT INTO A3TABLE0 VALUES (
DAYOFWEEK  (date '1989-02-05'),
date '1989-02-05'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # a Sunday = 1
    
    stmt = """INSERT INTO A3TABLE0 VALUES (
DAYOFWEEK  (date '1989-02-06'),
date '1989-02-06'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # a Monday = 2
    
    stmt = """INSERT INTO A3TABLE0 VALUES (
DAYOFWEEK  (date '1989-02-07'),
date '1989-02-07'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # a Tuesday = 3
    
    stmt = """INSERT INTO A3TABLE0 VALUES (
DAYOFWEEK  (date '1989-02-08'),
date '1989-02-08'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # a Wednesday = 4
    
    stmt = """INSERT INTO A3TABLE0 VALUES (
DAYOFWEEK  (date '1989-02-09'),
date '1989-02-09'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # a Thursday = 5
    
    stmt = """INSERT INTO A3TABLE0 VALUES (
DAYOFWEEK  (date '1989-02-10'),
date '1989-02-10'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # a Friday = 6
    
    stmt = """INSERT INTO A3TABLE0 VALUES (
DAYOFWEEK  (date '1990-02-28'),
date '1990-02-28'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # a Wednesday = 4
    
    stmt = """INSERT INTO A3TABLE0 VALUES (
DAYOFWEEK  (date '1990-03-01'),
date '1990-03-01'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  a Thursday = 5
    
    stmt = """SELECT * FROM A3TABLE0 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s0')
    # expect 9 rows with the following values in any order
    #        7  1989-02-04
    #        1  1989-02-05
    #        2  1989-02-06
    #        3  1989-02-07
    #        4  1989-02-08
    #        5  1989-02-09
    #        6  1989-02-10
    #        4  1990-02-28
    #        5  1990-03-01
    
    stmt = """UPDATE A3TABLE0 
SET d_of_w = DAYOFWEEK  (date '1990-09-06')
WHERE y_to_d = date '1990-03-01'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    # should change the 5 (Thursday) to a 5 (Thursday) (!)
    
    stmt = """UPDATE A3TABLE0 
SET d_of_w = DAYOFWEEK  (date '1990-09-06'),
y_to_d = date '1990-09-06'
WHERE d_of_w = DAYOFWEEK (date '1990-10-27')
or d_of_w = 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    # 1990-10-27 was a Saturday (7)
    # should change the values for the Saturday (7) and the Tuesday (3)
    # to Thursday (5)
    
    stmt = """UPDATE A3TABLE0 
SET d_of_w = DAYOFWEEK  (date '1990-10-25'),
y_to_d = date '1990-10-25'
WHERE d_of_w IN  (7,2)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    #  only 1 change: the Monday (2) and it's date change to a Thursday (5)
    #  the 7 (Saturday) was already changed in the previous query
    # 04/13/09 added order by
    stmt = """SELECT * FROM A3TABLE0 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    # expect 9 rows with the following values in any order
    # 	5  1990-09-06
    # 	1  1989-02-05
    # 	5  1990-10-25
    # 	5  1990-09-06
    # 	4  1989-02-08
    # 	5  1989-02-09
    # 	6  1989-02-10
    # 	4  1990-02-28
    # 	5  1990-03-01
    
    stmt = """DELETE FROM A3TABLE0 
WHERE d_of_w IN  (1,3)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    # removes 1 row
    
    stmt = """DELETE FROM A3TABLE0 
WHERE d_of_w = DAYOFWEEK  (date '1990-09-06')
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 5)
    #  removes the 5 Thursdays
    
    stmt = """SELECT * FROM A3TABLE0 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    #  expect 3 rows with the following values in any order
    #            4  1989-02-08
    #            6  1989-02-10
    #            4  1990-02-28
    
    stmt = """SELECT DAYOFWEEK  (y_to_d),
d_of_w,
y_to_d
from A3TABLE0 
where extract (year from y_to_d) = 1989
order by d_of_w desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s3')
    #  expect 2 rows with the following values in this order
    #            4  1989-02-08
    #            6  1989-02-10
    
    stmt = """SELECT DAYOFWEEK  (y_to_d),
d_of_w,
y_to_d
from A3TABLE0 
where y_to_d in
(select y_to_d from A3TABLE0 
where y_to_d > date '1989-12-30')
order by d_of_w desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s4')
    #  expect 1 row with the following values
    #  	4  1990-02-28
    
    stmt = """SELECT DAYOFWEEK (y_to_d),
d_of_w,
y_to_d,
DAYOFWEEK (y_to_d + interval '1' day),
DAYOFWEEK (y_to_d + interval '7' day)
from A3TABLE0 
where y_to_d in
(select y_to_d from A3TABLE0 
where y_to_d < date '1990-10-25')
order by y_to_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s5')
    #  expect 3 rows with the following values in any order:
    #  (EXPR)  D_OF_W       Y_TO_D      (EXPR)  (EXPR)
    #  ------  -----------  ----------  ------  ------
    #
    #       4            4  1989-02-08       5       4
    #       6            6  1989-02-10       7       6
    #       4            4  1990-02-28       5       4
    
    stmt = """SELECT DAYOFWEEK (y_to_d),
d_of_w,
y_to_d,
DAYOFWEEK (y_to_d - interval '1' day),
DAYOFWEEK (y_to_d + interval '0' day) from A3TABLE0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s6')
    #  expect 3 rows
    #  	(EXPR)  D_of_W       Y_to_D      (EXPR)  (EXPR)
    #  	------  -----------  ----------  ------  ------
    #
    #  	     4            4  1989-02-08       3       4
    #  	     6            6  1989-02-10       5       6
    #  	     4            4  1990-02-28       3       4
    
    stmt = """SELECT DAYOFWEEK (y_to_d),
d_of_w,
y_to_d
from A3TABLE0 
where extract  (year from y_to_d) > 1900
or d_of_w = 6 or d_of_w = 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s7')
    #  expect 3 rows with the following values in any order
    #            4  1989-02-08
    #            6  1989-02-10
    #            4  1990-02-28
    
    stmt = """SELECT DAYOFWEEK (y_to_d),
d_of_w,
y_to_d
from A3TABLE0 
where d_of_w = 6 or d_of_w = 4
or extract (year from y_to_d) > 1900;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s8')
    #  expect 3 rows with the following values in any order
    #            4  1989-02-08
    #            6  1989-02-10
    #            4  1990-02-28
    
    stmt = """SELECT DAYOFWEEK (y_to_d),
d_of_w,
y_to_d
from A3TABLE0 
where extract (year from y_to_d) > 1900
and d_of_w = 6 and d_of_w is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s9')
    #  expect 1 row with the following values
    #            6  1989-02-10
    
    stmt = """SELECT DAYOFWEEK (y_to_d),
d_of_w,
y_to_d
from A3TABLE0 
where d_of_w = 6 and d_of_w is not null
and  extract (year from y_to_d) > 1900;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s10')
    
    _testmgr.testcase_end(desc)

def test006(desc="""a04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0197 : testA04
    #  Description:        Datetime function EXTEND.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the 'Title'
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """INSERT INTO BTRE211 VALUES
(  date '1988-01-01',
EXTEND ( date '1988-01-01', timestamp),
EXTEND ( date '1988-01-01', timestamp(6)),
EXTEND ( time '15:01:01' hour,timestamp),
EXTEND ( time '15:01:01', timestamp(6)),
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """INSERT INTO BTRE211 VALUES
( EXTEND ( timestamp(3) '1988-05-24:22:22:22.222'
, date),
EXTEND ( timestamp(3) '1988-05-24:22:22:22.222'
, timestamp),
EXTEND ( timestamp(3) '1988-05-24:22:22:22.222'
, timestamp(6)),
EXTEND ( time(3) '17:57:57.777'
, time),
EXTEND ( time(3) '17:57:57.777'
, time(6)),
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """INSERT INTO BTRE211 VALUES
( date '99-01-25',
timestamp '99-01-01:01:01:55',
timestamp(6) '1996-01-01:01:01:01.99',
time '12:01:01',
time(6) '01:01:01.12',
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3045')
    
    stmt = """SELECT * from BTRE211;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s3')
    
    #    Tests added 2 April 1990 in checking 900116-1521:
    stmt = """select * from pvA41 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s4')
    
    stmt = """SELECT extend(BTRE211.Y_to_d , timestamp(6)) -
extend(BTRE211.y_to_s , timestamp(6))
FROM BTRE211 
WHERE BTRE211.Y_to_d = date '1988-01-01'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """SELECT extend(BTRE213.DATE1,timestamp(6)) -
extend(BTRE213.TIME1, timestamp(6))
FROM BTRE213 
WHERE BTRE213.DATE1 = date '1988-10-25'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """SELECT extend (DATE1,timestamp(6)) -
extend (TIME1, timestamp(6))
FROM pvA41 
WHERE DATE1 = date '1988-10-25'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    _testmgr.testcase_end(desc)

def test007(desc="""a05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0197 : testA05
    #  Description:        Datetime function JULIANTIMESTAMP.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the 'Title'
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """insert into a5table0 values
(JULIANTIMESTAMP (timestamp '1989-02-09:06:30' ),
extend (timestamp '1989-10-17:17:04:01',timestamp (6)),
'dog', 'eggplant', 9 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3047')
    #  The Julian number for 09/02/1989 is 2447566
    
    stmt = """insert into a5table0 values
(JULIANTIMESTAMP (date '0019-02-28'),
timestamp (6) '1922-03-08:12:03:59.123498',
'horse', 'radish', 0 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #  The Julian number for 28/02/0019 is 1728055
    
    stmt = """insert into a5table0 values
(JULIANTIMESTAMP (timestamp (6) '1942-01-21:09:42:36.300206'),
extend ('1975-05-18:23:24',timestamp (6)),
'cow', 'onion', null );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #  The Julian number for 21/01/1942 is 2430380
    
    stmt = """insert into a5table0 values
(null, extend (timestamp '1959-09-16:14:30:01',timestamp (6)) ,
'lamb ', 'carrot ', 7 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """insert into a5table0 values
(null, null, 'lamb ', 'carrot ', 7 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into a5table0 values
(JULIANTIMESTAMP (date '3062-12-31' ),
extend (timestamp '1990-10-22:14:30:01',timestamp (6)),
'fox', 'null', 3 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #  The Julian number for 31/12/3062 is 2839796
    
    stmt = """select * from a5table0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s5')
    #  expect 6 rows
    
    stmt = """select DISTINCT t_stamp, CONVERTTIMESTAMP (t_stamp) from a5table0 
where t_stamp = JULIANTIMESTAMP (extend (date '3062-12-31',timestamp (6)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select t_stamp, CONVERTTIMESTAMP (t_stamp), the_date from a5table0 
where CONVERTTIMESTAMP (t_stamp) > timestamp (6) '1900-12-31:06:35:56.120001'
order by the_date desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select t_stamp, CONVERTTIMESTAMP (t_stamp), the_date, animal from a5table0 
where CONVERTTIMESTAMP (t_stamp) is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s8')
    
    stmt = """select * from a5table0 
where t_stamp in (select t_stamp from a5table0 
where the_date  >
date '1922-02-01'
and animal like '%c%')
order by t_stamp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4041')
    
    stmt = """select DAYOFWEEK (CONVERTTIMESTAMP (t_stamp)),
CONVERTTIMESTAMP (t_stamp), t_stamp,
DAYOFWEEK (CONVERTTIMESTAMP (t_stamp - 1)),
CONVERTTIMESTAMP (t_stamp -1), (t_stamp - 1)
from a5table0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s10')
    
    stmt = """select t_stamp, CONVERTTIMESTAMP (t_stamp), (t_stamp + 2),
CONVERTTIMESTAMP (t_stamp + 2) from a5table0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s11')
    
    _testmgr.testcase_end(desc)

def test008(desc="""a05b"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0197 : testA05b
    #  Description:        Datetime function JULIANTIMESTAMP.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the 'Title'
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """insert into a5table1 (i) values (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4024')
    
    stmt = """insert into a5table1 (nonkeydate,i)
values (
extend (timestamp (3) '1996-12-22:22:22:22.222',timestamp (6))
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """insert into a5table1 
values (converttimestamp (
JULIANTIMESTAMP (timestamp (6) '1996-01-05:05:55:55.555555')),
converttimestamp (
JULIANTIMESTAMP (timestamp (6) '1996-11-11:11:11:11.000000')),
3
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select * from a5table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    _testmgr.testcase_end(desc)

def test009(desc="""a06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0197 : testA06.sql
    #  Description:        Datetime function CONVERTTIMESTAMP.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the 'Title'
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """delete from a6table0;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into a6table0 values
( JULIANTIMESTAMP ( date '1989-02-09'),
'Harry', cast(date '1989-02-09' as timestamp),
'hang gliding, croquet, poker'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into a6table0 values
( JULIANTIMESTAMP ( timestamp '0019-02-28:09:54:01'),
'Moses', timestamp '0019-02-28:09:54:01',
'burning bushes, 10 Commandments'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into a6table0 values
( JULIANTIMESTAMP ( timestamp '3062-12-31:13:13:13.131313'),
'Spock III',
timestamp '3062-12-31:13:13:13.131313',
'mental Nintendo'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from a6table0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s0')
    
    stmt = """select converttimestamp(j_bdate), birthdate from a6table0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s1')
    #  Expect the following 3 rows
    # (EXPR)                      BIRTHDATE
    # --------------------------  --------------------------
    #
    # 1989-02-09 00:00:00.000000  1989-02-09 00:00:00.000000
    # 0019-02-28 09:54:01.000000  0019-02-28 09:54:01.000000
    # 3062-12-31 13:13:13.131313  3062-12-31 13:13:13.131313
    
    stmt = """select birthdate, name1, hobbies, j_bdate,
dateformat(converttimestamp(j_bdate),european)
from a6table0 
where birthdate <> cast(date '1990-10-01' as timestamp)
and name1 <> 'Moses'
and hobbies not like '%poker%'
order by j_bdate desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s2')
    
    #  Expect 2 Rows where NAME1=MOSES and SPOCK III
    
    stmt = """select birthdate, dateformat(converttimestamp(j_bdate),european)
from a6table0 
order by birthdate asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s3')
    
    #  Expect 3 rows in this order
    # BIRTHDATE                   (EXPR)
    # --------------------------  --------------------------
    #
    # 0019-02-28 09:54:01.000000  28.02.0019 09.54.01.000000
    # 1989-02-09 00:00:00.000000  09.02.1989 00.00.00.000000
    # 3062-12-31 13:13:13.131313  31.12.3062 13.13.13.131313
    
    stmt = """select dayofweek(converttimestamp(j_bdate)), dayofweek(birthdate),
birthdate from a6table0 
order by name1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s4')
    
    stmt = """select name1,birthdate,hobbies from a6table0 
where converttimestamp(j_bdate) = birthdate
and name1 like '%o%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select name1, j_bdate, converttimestamp(j_bdate)
from a6table0 
where birthdate in (select converttimestamp(j_bdate) from a6table0 
where converttimestamp(j_bdate)
< timestamp '1990-10-25:12:55:41.1');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s5')
    
    _testmgr.testcase_end(desc)

def test010(desc="""b03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0197 : testB03
    #  Description:        DATEFORMAT function with 1st argument of NULL value.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """select y_to_d from BTRE211;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b03exp""", 'b03s0')
    
    stmt = """select dateformat (y_to_d, usa) from BTRE211;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b03exp""", 'b03s1')
    
    _testmgr.testcase_end(desc)

def test011(desc="""b05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0197 : testB05
    #  Description:        Compiler traps on datetime qualifier mismatch in
    #                      a subquery.  Negative test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """select * from BTRE211;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b05exp""", 'b05s0')
    
    # #1
    #    select * from btre211
    #          where y_to_mi in
    #            ( select y_to_mi from btre211
    #                 where y_to_mi < current OR y <> current year
    #            )
    #    ;
    #
    #
    #  --#2
    #    select * from btre211 where y_to_mi in
    #       (select y_to_mi from btre211
    #          where y_to_mi <> current year to month
    #                  OR mo >= datetime '01' month
    #       )
    #    ;
    #
    #
    # #3
    stmt = """select * from BTRE211 where y_to_s in
(select y_to_s from BTRE211 
where y_to_s <> current_date
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4041')
    
    # #4
    stmt = """select * from BTRE211 
where y_to_d > ( select y_to_d from BTRE211 
where y_to_s is not null
OR y_to_s < y_to_d
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4041')
    
    ##5   w/ current function
    stmt = """select * from BTRE211 
where y_to_f > ( select y_to_f from BTRE211 
where y_to_d  = current_date
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # #6
    stmt = """select y_to_s, y_to_d from BTRE211 
where y_to_s
= all ( select y_to_s from BTRE211 
where y_to_s = current_date
OR h_to_f is not null
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4041')
    
    # #7
    stmt = """select * from BTRE211 
where y_to_d
< any ( select y_to_d from BTRE211 
where y_to_d = current_date
OR h_to_f is not null
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b05exp""", 'b05s4')
    
    # #8
    stmt = """select * from BTRE211 
where y_to_s
>= some ( select y_to_s from BTRE211 
where y_to_s  <> current_date
OR h_to_f is not null
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4041')
    
    _testmgr.testcase_end(desc)

def test012(desc="""d00"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """drop view pvA41;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view pvre213a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view pvre213b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table BTRE211;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table BTRE213;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table a1table0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table A3TABLE0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table a5table0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table a5table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table a6table0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table t921204;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

