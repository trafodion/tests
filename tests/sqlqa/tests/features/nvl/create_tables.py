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
    
def test001(desc="""create tables"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """create table OPTABLE 
(  p1  largeint          not null
, u1  smallint          unsigned
, zi1 smallint          not null
, f1  double precision
, n1  numeric (4,2)    unsigned no default not null
, d1  decimal (4,2)    unsigned no default not null
, t1  date             not null
, c1  char
, p2  integer           not null
, u2  integer           unsigned
, zi2 integer           signed no default not null
, f2  real              not null
, n2  numeric (6,3)     unsigned
, d2  decimal (6,3)     signed no default not null
, t2  time
, c2  char(2)
, p3  smallint          signed no default not null
, u3  largeint
, zi3 largeint          signed no default not null
, f3  float             no default not null
, n3  numeric (12,4)    signed no default not null
, d3  decimal (12,4)
, t3  interval hour to second
, c3  char(3)
, z   char (8)
, psv pic s9v9(3)       no default not null
, p9c pic 9v9(2) comp
, ps9 pic s9(5)         no default not null
, psc pic s9(1) comp
, f4  float
, f5  real              no default not null
, b1  double precision  no default not null
, b2  double precision
, vc1 varchar(15)
, primary key (zi3, t1, d2) );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index idxp1 on OPTABLE (b1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create unique index unidx on OPTABLE (p1, p2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view voptbl as
select * from OPTABLE 
where trim(z) < 'Row05' or
vc1 in ('~!#$%^&', '\$vcRNULL~', '\$vcZERO~');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view voptbl1 as
select vv.z, vv.b1, vv.b2, vv.c1, vv.vc1
from voptbl vv left join OPTABLE t1 on
(TANH(vv.f4) = TANH(t1.f4) and
TANH(SIN(vv.f5)) = TANH(SIN(t1.f5))) or
t1.vc1 in ('~!#$%^&', '\$vcRNULL~', '\$vcZERO~');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into OPTABLE values (
0, 0,  -32768,  -.7394723453, 10.79,  10, date '1959-12-31',  'a' ,
-2147484,   9,   9,   0.9,   9,   9, time '23:59:59', 'aa',
9, 200,  -1, 0.10120, 11.9,  null, null, null, null,
-0.1123, 0.99, -99999, -9, .314159260, -1.175E-18,
-1.2250E-28, 0.05, '~!#$%^&');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into OPTABLE values (
9.223e18,  10,  32767,  0.00971, 10,  10, date '1960-11-01', 'a'  ,
10, 10, 214748366, -1.17e-18, 10, 10, time '00:00:00', 'aa', -2418,
5678236,  -4928761,  -0.10859,  10,  -2.222197264,
interval '00:00:00' hour to second, 'aaa', 'Row01',
0.356, 1.99, 99999, 9, -2.225E-8, 3.402E-8,
1.7976E-3, -0.05, '\$vcR1~');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into OPTABLE values (
10, 32766, -32766, -1.79e-2, 1.01, 2.99, date '1974-05-24', 'a',
-3829135, 847201, 23.0008347231, -.123009, 10, 10, time '00:00:15',
'aa', 0, 20, 0, -.00092746, 36.02, 20,
interval '00:00:15' hour to second, 'aab', 'Row02',
0.997, 0.11, 12345, 8, -.3876, -3.402E-3,
-1.7976E-3, -2.225E-38, '\$vcR2~');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into OPTABLE values (
193, 24923, 9992, -0.9999999, 1.1, 22.03, date '1900-12-01', 'a'  ,
-2.14588, 78246, 8, 0.82304903,  3.33,  10, time '00:00:30', 'aa' ,
30, 18234, 3, -0.333330, -0.000392, 12353298.1999,
interval '00:00:30' hour to second, 'aac', 'Row03',
-.019, 0.58, 4598, 7, .9789, -0.58793,
0.045, -0.045, '\$vcR3~');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into OPTABLE values (
9999, 33392, -19234, -0.0003726, 2.1, 1.9, date '1981-08-21', 'a',
2083292, 83652920, -19283745, 0.983720007, 208.3, 2,
time '00:00:45', 'ab' ,
1, 182734, 42, 0.948, 3, 87, interval '00:00:45' hour to second,
'aba', 'Row04', 0.866, .50, 75849, 6, .8345, -.9999999,
-0.71414, -.60, '\$vcR4~');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into OPTABLE values (
10328, 75, 78, 0.8700123, 3.0, 34.29, date '2960-03-22',  'a'  ,
-58339, 38412, -38413, 0.2000974, 444.238, 2.0, time '00:01:00',
'ab', -12390, -9335202, -109, -.853, 12345678.1234, 0,
interval '00:01:00' hour to second, 'abb', 'Row05',
0.037, 1.06, 83936, 5, -.7129, 0.834673734574,
7.9098700456e-23, -7.9098700456e-1, '\$vcR5~');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into OPTABLE values (
3, 201, 1, -1,  10, 25.73, date '1925-09-12',  'a'  ,
836, 2, -2, -.5,  1.3,  20, time '00:01:15', 'ab' ,
11, 28, 322, .111003, -12345678.1234, -1.3,
interval '00:01:15' hour to second, 'abc', 'Row06',
0.298, 1.17, 76546, 4, -0.6958, -0.7986750064688,
-.0976952543975, 0.0976952543975, '\$vcR6~');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into OPTABLE values (
1, 2,  3, -0.1, 0.27, 8.2, date '1963-03-01',  'a'  ,
82, 0, 0, -.10834562, 6.003, 60.006, time '00:01:30', 'ac' ,
0, 1, 1, -1.0, 333.02, 666.09, interval '00:01:30' hour to second,
'aca', 'Row07',
0.309, 0.01, 52076, 3, 0.57308, -0.98633667800,
-0.008754335, 0.008754335, '\$vcR7~');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into OPTABLE values (
25, 83, 19, 0.2787124838, 8.000, 7.23, date '1926-02-17', 'a'  ,
16, 30, 3088, -.300072823,  9.003, 3, time '00:01:45', 'ac' ,
20, 0, 20, -.20008436, 20, 20, interval '00:01:45' hour to second,
'acb', 'Row08', -0.1007, .05, 42770, 2, 4.0876e-5, -1,
0.0008745245, -0.0008745245, '\$vcR8~');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into OPTABLE values (
75, null, 19, null, 8.000, 7.23, date '1986-02-17', null,
16, null, 3088, -.300072823,  null, 313, null, 'LL',
20, null, 20, -.20008436, 212, null, null,
null, 'NULLS', -0.1007, null, 42770, null, null, -1,
0.0008745245, null, '\$vcRNULL~');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into OPTABLE values (
15, 0, 19, null, 8.000, 7.23, date '1926-02-17', '0',
16, 0, 3088, -.300072823,  0, 8, time '00:00:00', '00',
20, 0, 80, -.20008436, 20, 0, interval '00:00:00' hour to second,
'000', 'ZEROS', -0.1007, 0, 42770, 0, 0, -1,
0.0008745245, 0, '\$vcZERO~');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update statistics for table OPTABLE on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expectfile ${test_dir}/a09exp a09s6
    stmt = """select count(*) from voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    ##expectfile ${test_dir}/a09exp a09s7
    stmt = """select * from voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """CREATE TABLE DAYTAB(
d_t_m_e        TIMESTAMP       NO DEFAULT NOT NULL,
d_n            CHAR(10)        NO DEFAULT NOT NULL,
m_n            VARCHAR(10)     NO DEFAULT NOT NULL,
d_of_y         INTEGER         NO DEFAULT NOT NULL,
w_k            SMALLINT        NO DEFAULT NOT NULL,
q_r            SMALLINT        NO DEFAULT NOT NULL,
year_d         INT             NO DEFAULT NOT NULL,
month_d        SMALLINT        NO DEFAULT NOT NULL,
day_d          SMALLINT        NO DEFAULT NOT NULL,
hour_d         SMALLINT        NO DEFAULT NOT NULL,
minute_d       SMALLINT        NO DEFAULT NOT NULL,
second_d       INT             NO DEFAULT NOT NULL
);"""
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
YEAR      (date '1945-05-06'),
MONTH     (date '1936-08-10'),
DAY       (date '2000-12-31'),
HOUR      (timestamp '1718-01-10 12:50:59.400000'),
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
YEAR      (date '05/06/0001'),
MONTH     (date '07/10/1936'),
DAY       (date '02/28/1951'),
HOUR      (timestamp '01/10/0718 12:50:59.999 pm'),
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
YEAR      (date '13.05.1945'),
MONTH     (date '10.10.1946'),
DAY       (date '29.02.1996'), -- leap year
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
YEAR      (timestamp '2106-01-01 00:00:00.000001'),
MONTH     (timestamp '1433-04-10 22:22:22.222222'),
DAY       (timestamp '1945-03-31 12:50:59.400000'),
HOUR      (time '12:50:59.400000'),
MINUTE    (time '23:59:59.999999'),
SECOND    (time '00:00:01.000000')
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expectfile ${test_dir}/a00exp a00s3
    
    stmt = """create table playt3 (
binary_signed          numeric (4) signed     default 0.0  not null
, binary_32_u            numeric (9,2) unsigned default 0.0
, binary_64_s            numeric (18,3) signed  default 0.0
, small_int              smallint               default 0
, medium_int             integer unsigned       default 0
, primary key (binary_signed)
)
attribute
blocksize 4096;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # create non-unique index
    stmt = """create index playt3a on playt3 (binary_32_u);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into playt3 values (-5000,0,1200,90,null);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into playt3 values (50,50,200,90,10000);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into playt3 values (60,80,2000,1000,8000);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into playt3 values (1000,80,1500,80,9000);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into playt3 values (2000,90,1200,2000,0);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into playt3 values (3000,80,2000,9000,1000);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into playt3 values (4000,40,2000,90,5000);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into playt3 values (8000,70,0,90,10000);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into playt3 values (9000,0,null,0,null);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into playt3 values (1800,null,null,null,0);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update statistics for table playt3 on every column;"""
    output = _dci.cmdexec(stmt)
    
    ##expectfile ${test_dir}/a00exp a00s4
    stmt = """select * from playt3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
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
    
    stmt = """INSERT INTO emp 
values ('a123456789', 'b987654321', 0, null, null,
date '09/23/1908', timestamp '09/23/1908 12:34:00.067222');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO emp 
values ('First Name', 'Last NameL', 950, null, null,
date '09/23/1908', timestamp '09/23/1908 12:34:00.067222');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO emp 
values ('FName A', 'LName A', 2006, null, null,
null, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO emp 
values ('FName B', 'LName B', 6006, 0, 0,
null, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO emp 
values ('FName A', 'LName A', 9006, null, null,
null, timestamp '2006-05-12 16:36:01.000006');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expectfile ${test_dir}/a00exp a00s5
    stmt = """select * from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """create table play_tabA (td      date,
tt      timestamp
default timestamp '1111-11-11 11:11:11.000006',
intv_hs interval hour to second,
intv_md interval year to month,
intv_y2 interval year(2),
intv_h2 interval hour(2));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into play_tabA (td, tt, intv_hs, intv_md, intv_y2, intv_h2)
values (null, null, null, null, null, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create table play_likeA (td      date,
tt      timestamp
default timestamp '1111-11-11 11:11:11.000006',
intv_hs interval hour to second,
intv_md interval year to month,
intv_y2 interval year(2),
intv_h2 interval hour(2));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table play_tabB (td      date,
tt      timestamp,
intv_hs interval hour to second,
intv_md interval year to month,
intv_y2 interval year(2),
intv_h2 interval hour(2));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into play_tabB (td, tt, intv_hs, intv_md, intv_y2, intv_h2)
values (date '2006-05-08', timestamp '2006-05-08 15:05:59.400000',
interval '00:00:00.000006' hour to second,
interval '01-01' year to month,
interval '01' year(2), interval '01' hour(2));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    _testmgr.testcase_end(desc)

