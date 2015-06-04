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
    
def test001(desc="""Set up file for the arkt0140 datetime tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # testA00
    # johncl
    #
    #  While converting from fraction to second the precision is
    #  taken as 3 instead of 6, because values inserted are having
    #  only 3 digits at max.
    
    # the table BTRE211 is used in testA01, testA07 and testB02b
    
    stmt = """CREATE TABLE BTRE211 (
Y_to_D      DATE,
Y_to_S      TIMESTAMP,
Y_to_F      TIMESTAMP(3),
H_to_S      TIME,
H_to_F      TIME(3)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # the table BTRE212 is used in testA02, testA08 and B02b
    
    stmt = """CREATE TABLE BTRE212 (
Y           INTERVAL    YEAR(4),
Y_to_MO     INTERVAL    YEAR(4) TO MONTH,
MO          INTERVAL    MONTH,
D           INTERVAL    DAY,
D_to_H      INTERVAL    DAY TO HOUR,
D_to_MI     INTERVAL    DAY TO MINUTE,
D_to_S      INTERVAL    DAY TO SECOND(0),
D_to_F      INTERVAL    DAY TO SECOND(3),
H           INTERVAL    HOUR,
H_to_MI     INTERVAL    HOUR TO MINUTE,
H_to_S      INTERVAL    HOUR TO SECOND(0),
H_to_F      INTERVAL    HOUR TO SECOND(3),
MI          INTERVAL    MINUTE,
MI_to_S     INTERVAL    MINUTE TO SECOND(0),
MI_to_F     INTERVAL    MINUTE TO SECOND(3),
S           INTERVAL    SECOND(2,0),
S_to_F      INTERVAL    SECOND(2,3)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # the table BTRE213 is used in testA03 and testB02b
    
    stmt = """CREATE TABLE BTRE213 (
DATE1       DATE,
TIME1       TIME
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # the table BTRE217 is used in testA06 and testB02b
    
    # XXXXXX can't use DEFAULT
    
    # CREATE TABLE BTRE217 (
    #     DT1       DATE   DEFAULT date '1987-06-15',
    #     TM1       TIME   DEFAULT CURRENT_TIME,
    #     DT2       DATE   DEFAULT NULL,
    #     TM2       TIME   DEFAULT time '18:35:35'  not null,
    #     DT3       DATE   DEFAULT CURRENT_DATE NOT NULL,
    #     TM3       TIME   NO DEFAULT,
    #     DT4       DATE   NO DEFAULT NOT NULL,
    #     TM4       TIME   NOT NULL
    #     );
    
    stmt = """CREATE TABLE BTRE217 (
DT1       DATE,
TM1       TIME,
DT2       DATE,
TM2       TIME,
DT3       DATE,
TM3       TIME,
DT4       DATE NOT NULL,
TM4       TIME NOT NULL
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # the table BTRE218 is used in testA05 and testB02b
    
    # XXXXXX can't use DEFAULT
    
    # CREATE TABLE BTRE218 (
    #     Y         INTERVAL YEAR(2) DEFAULT interval '1' year,
    #     Y_to_MO   INTERVAL YEAR TO MONTH DEFAULT INTERVAL '00.00' YEAR TO MONTH,
    #     MO        INTERVAL MONTH DEFAULT NULL,
    #     D         INTERVAL DAY DEFAULT interval '15' day NOT NULL,
    #     D_to_H    INTERVAL DAY TO HOUR DEFAULT SYSTEM NOT NULL,
    #     D_to_MI   INTERVAL DAY TO MINUTE NO DEFAULT,
    #     D_to_S    INTERVAL DAY TO SECOND NO DEFAULT NOT NULL,
    #     H_to_MI   INTERVAL HOUR TO MINUTE NOT NULL
    #     );
    
    stmt = """CREATE TABLE BTRE218 (
Y         INTERVAL YEAR(2),
Y_to_MO   INTERVAL YEAR TO MONTH,
MO        INTERVAL MONTH,
D         INTERVAL DAY NOT NULL,
D_to_H    INTERVAL DAY TO HOUR NOT NULL,
D_to_MI   INTERVAL DAY TO MINUTE,
D_to_S    INTERVAL DAY TO SECOND NOT NULL,
H_to_MI   INTERVAL HOUR TO MINUTE NOT NULL
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # the table BTRE219 is used in testA04 and testB02b
    
    stmt = """CREATE TABLE BTRE219 (
Y_to_D    DATE	-- XXXXXX DEFAULT NULL
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # the table TEMP1 is used in testB01
    
    # XXXXXX can't use DEFAULT
    
    # CREATE TABLE TEMP1 (
    #     pnum     decimal (5,0) unsigned 	no default not null,
    #     pname    char (15) 		default null,
    #     birthday DATE 			default current_date not null,
    #     age      interval year(2) to month default interval '0' year(2) not null,
    #     vacation interval hour(3) 	default interval '0' hour(3) not null
    # ) ;
    
    stmt = """CREATE TABLE TEMP1 (
pnum     decimal (5,0) unsigned not null,
pname    char (15),
birthday DATE not null,
age      interval year(2) to month not null,
vacation interval hour(3) not null
)  no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # the table DATEKEY is used in testB02
    
    stmt = """CREATE TABLE datekey (
dat   date,
tim   time,
inter interval hour to second not null
) no partition
-- store by date
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index datekey0 
on datekey (tim, inter);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # the table TEMPB3 is is used in testB03
    
    # XXXXXX can't do DEFAULT
    # CREATE  TABLE TEMPB3 (
    #     COL1                           NUMERIC(4,0)    NO DEFAULT NOT NULL,
    #     DATECOLUMNIS30CHARACTERSLONGGG DATE            NO DEFAULT NOT NULL,
    #     INTERVALCOLIS30CHARACTERSLONGG INTERVAL DAY(2) NO DEFAULT NOT NULL
    # );
    
    stmt = """CREATE TABLE TEMPB3 (
COL1                           NUMERIC(4,0)    NOT NULL,
DATECOLUMNIS30CHARACTERSLONGGG DATE            NOT NULL,
INTERVALCOLIS30CHARACTERSLONGG INTERVAL DAY(2) NOT NULL
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # the tables TEMPB4a & TEMPB4 are used in testB04
    
    # XXXXXX can't do DEFAULT
    # create table tempb4a
    #    (col1 interval day(4) default interval '0' day not null);
    
    stmt = """create table tempb4a 
(col1 interval day(4) not null) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table tempb4 
(col1 pic x) no partition;  -- pic x = char (1)"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # the table b6table1 is used in testB06
    
    stmt = """CREATE TABLE b6table1 (
F3   TIME(3) NOT NULL,
D8_4 DECIMAL (8,4) NOT NULL
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # the views b6view1 & b6view2 are used in testB06
    
    stmt = """CREATE VIEW b6view1 AS
SELECT F3
FROM b6table1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE VIEW b6view2 AS
SELECT D8_4
FROM b6table1;"""
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
    
    stmt = """INSERT INTO BTRE212 VALUES
( interval '10' year(2),
interval '10-01' year(2) TO MONTH,
interval '01' month,
interval '15' day,
interval '15:12' day TO HOUR,
interval '16:13:15' day TO MINUTE,
interval '17:14:16:01' DAY TO SECOND(0),
interval '18:15:17:02.123' DAY TO SECOND(3),
interval '16' hour,
interval '17:18' hour TO MINUTE,
interval '18:19:03' HOUR TO SECOND(0),
interval '19:20:04.345' HOUR TO SECOND(3),
interval '21' minute,
interval '21:05' MINUTE TO SECOND(0),
interval '22:06.444' MINUTE TO SECOND(3),
interval '07' SECOND(2,0),
interval '08.555' SECOND(2,3)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE212 VALUES
( interval '9999' year(4),
interval '9999-11' year(4) TO MONTH,
interval '11' month,
interval '31' day,
interval '30:01' day TO HOUR,
interval '29:02:59' day TO MINUTE,
interval '28:03:58:59' DAY TO SECOND(0),
interval '27:04:57:58.999' DAY TO SECOND(3),
interval '23' hour,
interval '22:56' hour TO MINUTE,
interval '21:55:57' HOUR TO SECOND(0),
interval '20:54:56.888' HOUR TO SECOND(3),
interval '59' minute,
interval '58:59' MINUTE TO SECOND(0),
interval '57:58.777' MINUTE TO SECOND(3),
interval '59' SECOND(2,0),
interval '58.666' SECOND(2,3)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE212 VALUES
( interval '1' year(4),
interval '1-1' year(4)  TO MONTH,
interval '1' month,
interval '1' day,
interval '1:1' day TO HOUR,
interval '1:1:1' day TO MINUTE,
interval '1:1:1:1' DAY TO SECOND(0),
interval '1:1:1:1.1' DAY TO SECOND(3),
interval '1' hour,
interval '1:1' hour TO MINUTE,
interval '1:1:1' HOUR TO SECOND(0),
interval '1:1:1.1' HOUR TO SECOND(3),
interval '1' minute,
interval '1:1' MINUTE TO SECOND(0),
interval '1:1.1' MINUTE TO SECOND(3),
interval '1' SECOND(2,0),
interval '1.1' SECOND(2,3)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE212 VALUES
( interval '1' year(2),
interval '1-1' year(2) TO MONTH,
interval '1' month,
interval '1' day,
interval '0:0' day TO HOUR,
interval '0:0:0' day TO MINUTE,
interval '0:0:0:0' DAY TO SECOND(0),
interval '0:0:0:0.0' DAY TO SECOND(3),
interval '0' hour,
interval '0:0' hour TO MINUTE,
interval '0:0:0' HOUR TO SECOND(0),
interval '0:0:0.0' HOUR TO SECOND(3),
interval '0' minute,
interval '0:0' MINUTE TO SECOND(0),
interval '0:0.0' MINUTE TO SECOND(3),
interval '0' SECOND(2,0),
interval '0.0' SECOND(2,3)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE213 VALUES (
date '1988-10-25',
time '10:10:10'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE213 VALUES (
date '0100-01-01',
time '00:00:00'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE213 VALUES (
date '0100-01-01',
time '23:59:59'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE213 VALUES (
date '1954-05-06',
time '22:23:24'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE219 
VALUES
(
date '1774-09-24'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE218 
(D, D_to_H, D_to_MI, D_to_S, H_to_MI)
VALUES
(interval '23' day,
interval '22:13' day to hour,
interval '23:12:55' day TO MINUTE,
interval '25:14:55:55' DAY TO SECOND(0),
interval '12:15' hour TO MINUTE);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """prepare prepBTRE218 from
INSERT INTO BTRE218 
VALUES
(interval '55' year,
interval '11' month,
interval '10' month,
interval '23' day,
interval '22:13' day TO HOUR,
interval '23' minute,
interval '45' SECOND(2,0),
interval '30' minute);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute prepBTRE218;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE217 
(TM3, DT4, TM4)
VALUES
(time '23:12:45',
date '1985-10-15',
time '12:35:45'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE217 
(DT1, TM2, TM3, DT4, TM4)
VALUES
(date '1948-06-15',
time '23:45:45',
time '15:18:24',
date '1920-05-06',
time '01:10:25'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO TEMP1 VALUES (
1,
'frank',
date '1952-04-19',
interval '05-05' year(2) to month,
interval '41' hour(3)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO TEMP1 VALUES (
1,
'frank',
date '1952-04-19',
interval '05-05' year(2) to month,
interval '41' hour(3)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into datekey values (date '1989-01-01', time '16:23:22',
interval '08:08:08' HOUR TO SECOND(0));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into datekey values (date '1989-01-01' ,time '16:23:22',
interval '00:00:00' HOUR TO SECOND(0));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into datekey values (date '1989-01-01' ,time '16:23:22',
interval '00:00:01' HOUR TO SECOND(0));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into datekey values (date '1989-01-01' ,time '16:23:22',
interval '00:01:01' HOUR TO SECOND(0));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into datekey values (date '1989-01-01' ,time '16:23:22',
interval '01:00:00' HOUR TO SECOND(0));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into datekey values (date '1989-01-01' ,time '00:00:00',
interval '00:00:00' HOUR TO SECOND(0));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into datekey values (date '1989-01-01' ,time '00:00:00',
interval '00:01:00' HOUR TO SECOND(0));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into datekey values (date '1989-01-01' ,time '00:02:00',
interval '00:01:00' HOUR TO SECOND(0));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into datekey values (date '1989-01-04' ,time '03:20:00',
interval '03:03:03' HOUR TO SECOND(0));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into datekey values (date '1990-01-02' ,time '16:23:22',
interval '00:01:01' HOUR TO SECOND(0));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO TEMPB3 VALUES (
2455,
date '1988-05-01',
interval '23' day
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO TEMPB3 VALUES (
43,
date '1967-09-12',
interval '6' day
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into tempb4a values (interval '15' day);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into tempb4 values ('X');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    _testmgr.testcase_end(desc)

def test002(desc="""Select from BTRE211"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0140 : testA01
    #  Description:        Create and load data into the table BTRE211 of
    #                      Data type DATETIME.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """select Y_to_D, Y_to_S, Y_to_F from BTRE211;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    
    #  expect 4 rows with the following values:
    #  Y_TO_D      Y_TO_S                      Y_TO_F
    #  ----------  --------------------------  -----------------------
    #
    #  1988-01-01  1988-01-01 12:35:30.000000  1988-01-01 12:35:30.333
    #  1977-03-02  1979-06-05 14:40:45.000000  1980-07-06 15:45:50.678
    #  0802-09-07  0805-12-10 07:59:03.000000  0806-01-11 08:01:04.789
    #  0001-01-01  0001-01-01 00:00:00.000000  0001-01-01 00:00:00.000
    
    stmt = """select H_to_S, H_to_F from BTRE211;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    
    _testmgr.testcase_end(desc)

def test003(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0140 : testA02.sql
    #  Description:        Create and load data into the table
    #			BTRE212 of Data type INTERVAL.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  While converting from fraction to second the precision is
    #  taken as 3 instead of 6, because values inserted are having
    #  only 3 digits at max.
    #  This test case incorporates features detailed in the 'Title'
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """select Y, Y_to_MO, MO from BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    #  expect 4 rows with the following values:
    # 	   10     10-01    1
    # 	 9999   9999-11   11
    # 	    1      1-01    1
    # 	    1      1-01    1
    
    stmt = """select D, D_to_H, D_to_MI from BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    #  expect 4 rows with the following values:
    #      15   15 12   16 13:15
    #      31   30 01   29 02:59
    #       1    1 01    1 01:01
    #       1    0 00    0 00:00
    
    stmt = """select D_to_S, D_to_F from BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    #  expect 4 rows with the following values:
    #      17 14:16:01   18 15:17:02.123
    #      28 03:58:59   27 04:57:58.999
    #       1 01:01:01    1 01:01:01.100
    #       0 00:00:00    0 00:00:00.000
    
    stmt = """select H, H_to_MI from BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    #  expect 4 rows with the following values:
    #      16    17:18
    #      23    22:56
    #       1     1:01
    #       0     0:00
    
    stmt = """select H_to_S, H_to_F from BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s4')
    #  expect 4 rows with the following values:
    #      18:19:03   19:20:04.345
    #      21:55:57   20:54:56.888
    #       1:01:01    1:01:01.100
    #       0:00:00    0:00:00.000
    
    stmt = """select MI, MI_to_S, MI_to_F from BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')
    #  expect 4 rows with the following values:
    #      21    21:05   22:06.444
    #      59    58:59   57:58.777
    #       1     1:01    1:01.100
    #       0     0:00    0:00.000
    
    stmt = """select S, S_to_F from BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s6')
    
    _testmgr.testcase_end(desc)

def test004(desc="""Select from BTRE213"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0140 : testA03.sql
    #  Description:        Create and load data into the table
    #			BTRE213 of Data type DATE and TIME.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the 'Title'
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """select * from BTRE213;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s0')
    
    _testmgr.testcase_end(desc)

def test005(desc="""Select from BTRE219"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0140 : testA04
    #  Description:        Create and load data into the table
    #			$global_catalog.BTRE219 of
    #                      Data type DATETIME with DEFAULT, SYSTEM, NULL and
    #                      literal.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """select * from BTRE219;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s0')
    
    _testmgr.testcase_end(desc)

def test006(desc="""Select from BTRE218"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0140 : testA05.sql
    #  Description:        Create and load data into the table
    #			$global_catalog.BTRE218 of Data type INTERVAL.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the 'Title'
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """select * from BTRE218;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    
    _testmgr.testcase_end(desc)

def test007(desc="""Select from BTRE217"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0140 : testA06.sql
    #  Description:        Create and load data into the table BTRE217 of
    #                      Data type DATE and TIME with DAEFAULT, SYSTEM,
    #                      NULL and literal columns.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the 'Title'
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """select DT1, TM1, DT2, TM2 from BTRE217;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s0')
    #  expect 2 rows with the following values:
    #     DT1         TM1       DT2         TM2
    #     ----------  --------  ----------  --------
    #
    #     	 ?         ?           ?         ?
    #     1948-06-15         ?           ?  23:45:45
    
    stmt = """select DT3, TM3, DT4, TM4 from BTRE217;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s1')
    
    _testmgr.testcase_end(desc)

def test008(desc="""Update and Select on table with data type DATETIME."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0140 : testA07.sql
    #  Description:        This testcase tests the addition of a column to
    #                      the table, Dropping a table, Insertion, Deletion,
    #                      Update and Select on table with data type DATETIME.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the 'Title'
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    #  uses btre211 which has values inserted already in testA00
    
    stmt = """SELECT Y_to_D, Y_to_S, Y_to_F
FROM BTRE211;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s0')
    #  expect 4 rows with the following values:
    #     1988-01-01  1988-01-01 12:35:30.000000  1988-01-01 12:35:30.333
    #     1977-03-02  1979-06-05 14:40:45.000000  1980-07-06 15:45:50.678
    #     0802-09-07  0805-12-10 07:59:03.000000  0806-01-11 08:01:04.789
    #     0001-01-01  0001-01-01 00:00:00.000000  0001-01-01 00:00:00.000
    
    stmt = """SELECT H_to_S, H_to_F
FROM BTRE211;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s1')
    # expect 4 rows with the following values:
    # 	10:15:30  10:15:30.555
    # 	03:53:56  04:54:57.345
    # 	18:08:09  19:09:10.234
    # 	00:00:00  00:00:00.000
    
    stmt = """INSERT INTO BTRE211 VALUES (
date '1957-10-24',
timestamp '1960-01-01:16:15:54' ,
timestamp '1961-02-05:18:18:18.888',
time '22:22:22',
time '22:22:22.222'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """DELETE FROM BTRE211 
WHERE h_to_s = time '22:22:22';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """UPDATE BTRE211 
SET Y_to_d = date '1999-01-01'
WHERE Y_to_S = timestamp  '1979-06-05:14:40:45';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """SELECT * FROM BTRE211 
WHERE Y_to_S = timestamp '1979-06-05:14:40:45';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s2')
    #  expect 0 rows
    
    stmt = """SELECT Y_to_D, Y_to_S, Y_to_F
FROM BTRE211;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s3')
    #  expect 4 rows with the following values:
    #     1988-01-01  1988-01-01 12:35:30.000000  1988-01-01 12:35:30.333
    #     1999-01-01  1979-06-05 14:40:45.000000  1980-07-06 15:45:50.678
    #     0802-09-07  0805-12-10 07:59:03.000000  0806-01-11 08:01:04.789
    #     0001-01-01  0001-01-01 00:00:00.000000  0001-01-01 00:00:00.000
    
    stmt = """SELECT H_to_S, H_to_F
FROM BTRE211;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s4')
    
    _testmgr.testcase_end(desc)

def test009(desc="""Deletion, Update and Select on table with data type INTERVAL."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0140 : testA08.mp
    #  Description:        This testcase tests the addition od a column
    #                      to the table, Dropping a table, Insertion,
    #                      Deletion, Update and Select on table with data
    #                      type INTERVAL.
    #
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the 'Title'
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    #  Note : The DDL's are the part of the main test and hence not taken
    #         out in the pre part of the test.
    #  uses table BTRE212 which already has values inserted in testA01
    
    stmt = """select Y, Y_to_MO, MO from BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s0')
    
    #  expect 4 rows with the following values:
    # 	   10     10-01    1
    # 	 9999   9999-11   11
    # 	    1      1-01    1
    # 	    1      1-01    1
    
    stmt = """select D, D_to_H, D_to_MI from BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s1')
    #  expect 4 rows with the following values:
    #      15   15 12   16 13:15
    #      31   30 01   29 02:59
    #       1    1 01    1 01:01
    #       1    0 00    0 00:00
    
    stmt = """select D_to_S, D_to_F from BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s2')
    #  expect 4 rows with the following values:
    #      17 14:16:01   18 15:17:02.123
    #      28 03:58:59   27 04:57:58.999
    #       1 01:01:01    1 01:01:01.100
    #       0 00:00:00    0 00:00:00.000
    
    stmt = """select H, H_to_MI from BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s3')
    #  expect 4 rows with the following values:
    #      16    17:18
    #      23    22:56
    #       1     1:01
    #       0     0:00
    
    stmt = """select H_to_S, H_to_F from BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s4')
    #  expect 4 rows with the following values:
    #      18:19:03   19:20:04.345
    #      21:55:57   20:54:56.888
    #       1:01:01    1:01:01.100
    #       0:00:00    0:00:00.000
    
    stmt = """select MI, MI_to_S, MI_to_F from BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s5')
    #  expect 4 rows with the following values:
    #      21    21:05   22:06.444
    #      59    58:59   57:58.777
    #       1     1:01    1:01.100
    #       0     0:00    0:00.000
    
    stmt = """select S, S_to_F from BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s6')
    # expect 4 rows with the following values:
    #      7    8.555
    #     59   58.666
    #      1    1.100
    #      0    0.000
    
    # test begins
    
    stmt = """INSERT INTO BTRE212 VALUES
( interval '1444' year(4),
interval '1445-09' year(4) TO MONTH,
interval '8' month,
interval '22' day,
interval '23:10' day TO HOUR,
interval '24:10:10' day TO MINUTE,
interval '25:10:10:10' DAY TO SECOND(0),
interval '26:9:09:09.009' DAY TO SECOND(3),
interval '11' hour,
interval '11:12' hour TO MINUTE,
interval '11:12:13' HOUR TO SECOND(0),
interval '11:12:13.444' HOUR TO SECOND(3),
interval '14' minute,
interval '14:14' MINUTE TO SECOND(0),
interval '14:14.444' MINUTE TO SECOND(3),
interval '35' SECOND(2,0),
interval '35.333' SECOND(2,3)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """DELETE FROM BTRE212 
WHERE D_to_MI = interval '24:10:10' day TO MINUTE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """UPDATE BTRE212 
SET Y = interval '1000' year(4),
Y_to_MO = interval '100-01' year(4) TO MONTH
WHERE Y = interval '10' year(2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """SELECT * FROM BTRE212 
WHERE Y =interval '0' year(2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #  expect 0 rows
    
    stmt = """select Y, Y_to_MO, MO from BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s7')
    #  expect 4 rows with the following new values:
    # 	 1000    100-01    1
    # 	 9999   9999-11   11
    # 	    1      1-01    1
    # 	    1      1-01    1
    
    stmt = """select D, D_to_H, D_to_MI from BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s8')
    #  expect 4 rows with the same values as at the beginning:
    #      15   15 12   16 13:15
    #      31   30 01   29 02:59
    #       1    1 01    1 01:01
    #       1    0 00    0 00:00
    stmt = """select D_to_S, D_to_F from BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s9')
    #  expect 4 rows with the same values as at the beginning:
    #      17 14:16:01   18 15:17:02.123
    #      28 03:58:59   27 04:57:58.999
    #       1 01:01:01    1 01:01:01.100
    #       0 00:00:00    0 00:00:00.000
    stmt = """select H, H_to_MI from BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s10')
    #  expect 4 rows with the same values as at the beginning:
    #      16    17:18
    #      23    22:56
    #       1     1:01
    #       0     0:00
    stmt = """select H_to_S, H_to_F from BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s11')
    #  expect 4 rows with the same values as at the beginning:
    #      18:19:03   19:20:04.345
    #      21:55:57   20:54:56.888
    #       1:01:01    1:01:01.100
    #       0:00:00    0:00:00.000
    stmt = """select MI, MI_to_S, MI_to_F from BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s12')
    #  expect 4 rows with the same values as at the beginning:
    #      21    21:05   22:06.444
    #      59    58:59   57:58.777
    #       1     1:01    1:01.100
    #       0     0:00    0:00.000
    stmt = """select S, S_to_F from BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s13')
    
    _testmgr.testcase_end(desc)

def test010(desc="""ORDER BY on DATE and INTERVAL."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0140 : testB01.sql
    #  Description:        ORDER BY on DATE and INTERVAL.
    #  Test case inputs:
    #  Test case outputs:  
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the 'Title'
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """select * from TEMP1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b01exp""", 'b01s0')
    
    stmt = """select * from TEMP1 order by age      ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b01exp""", 'b01s1')
    
    stmt = """select * from TEMP1 order by vacation ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b01exp""", 'b01s2')
    
    _testmgr.testcase_end(desc)

def test011(desc="""Use of index, particularly where GMT has rolled a day but local day has not."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0140 : testB02.sql
    #  Description:        Use of index, particularly where GMT has
    #                      rolled a day but local day has not.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes: This test case contains intermix of DDL and DML.
    #  According to Bhavesh structure will be kept like this only.
    #  This test case incorporates features detailed in the 'Title'
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """select * from datekey ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s00')
    #  expect 10 rows
    
    #   TIME
    #   The found bug was to get incorrect results here:
    
    stmt = """select * from datekey where tim = time '16:23:22';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s01')
    #  expect 5 rows with these values:
    #       1989-01-01  16:23:22    8:08:08
    #       1989-01-01  16:23:22    0:00:00
    #       1989-01-01  16:23:22    0:00:01
    #       1989-01-01  16:23:22    0:01:01
    #       1989-01-01  16:23:22    1:00:00
    
    stmt = """select * from datekey where tim = time '00:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s02')
    # expect 2 rows with these values:
    #      1989-01-01  00:00:00    0:00:00
    #      1989-01-01  00:00:00    0:01:00
    
    stmt = """select * from datekey where tim = time '03:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #  expect 0 rows
    
    #   INTERVAL
    stmt = """select * from datekey 
where inter = interval '0:1:1' HOUR TO SECOND(0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s03')
    #  expect 2 rows with these values:
    #       1989-01-01  16:23:22    0:01:01
    #       1990-01-02  16:23:22    0:01:01
    
    stmt = """select * from datekey 
where inter = interval '0:1:1' HOUR TO SECOND(0)
and   tim   = time '16:23:22' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s04')
    
    # testB02b
    # This was originally part of testB02.
    # It has no logical connection so I've separated it here to make it easier
    # to assess any failures.
    # The test adds an indexe to each column in turn of each table.
    #
    # TABLE BTRE211;
    
    stmt = """create index ix1 on BTRE211 (y_to_d);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select y_to_d from BTRE211 order by y_to_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s0')
    
    stmt = """create index ix2 on BTRE211 (y_to_s);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select y_to_s from BTRE211 order by y_to_s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s1')
    
    stmt = """create index ix3 on BTRE211 (y_to_f);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select y_to_f from BTRE211 order by y_to_f;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s2')
    
    stmt = """create index ix4 on BTRE211 (h_to_s);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select h_to_s from BTRE211 order by h_to_s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s3')
    
    stmt = """create index ix5 on BTRE211 (h_to_f);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select h_to_f from BTRE211 order by h_to_f;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s4')
    
    # TABLE BTRE212;
    stmt = """create index ix6 on BTRE212 (y);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select y from BTRE212 order by y;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s5')
    
    stmt = """create index ix7 on BTRE212 (y_to_mo);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select y_to_mo from BTRE212 order by y_to_mo;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s6')
    
    stmt = """create index ix8 on BTRE212 (mo);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select mo from BTRE212 order by mo;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s7')
    
    stmt = """create index ix9 on BTRE212 (d);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select d from BTRE212 order by d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s8')
    
    stmt = """create index ix10 on BTRE212 (d_to_h);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select d_to_h from BTRE212 order by d_to_h;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s9')
    
    stmt = """create index ix11 on BTRE212 (d_to_mi);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select d_to_mi from BTRE212 order by d_to_mi;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s10')
    
    stmt = """create index ix12 on BTRE212 (d_to_s);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select d_to_s from BTRE212 order by d_to_s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s11')
    
    stmt = """create index ix13 on BTRE212 (d_to_f);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select d_to_f from BTRE212 order by d_to_f;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s12')
    
    stmt = """create index ix14 on BTRE212 (h);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select h from BTRE212 order by h;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s13')
    
    stmt = """create index ix15 on BTRE212 (h_to_mi);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select h_to_mi from BTRE212 order by h_to_mi;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s14')
    
    stmt = """create index ix16 on BTRE212 (h_to_s);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select h_to_s from BTRE212 order by h_to_s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s15')
    
    stmt = """create index ix17 on BTRE212 (h_to_f);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select h_to_f from BTRE212 order by h_to_f;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s16')
    
    stmt = """create index ix18 on BTRE212 (mi);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select mi from BTRE212 order by mi;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s17')
    
    stmt = """create index ix19 on BTRE212 (mi_to_s);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select mi_to_s from BTRE212 order by mi_to_s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s18')
    
    stmt = """create index ix20 on BTRE212 (mi_to_f);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select mi_to_f from BTRE212 order by mi_to_f;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s19')
    
    stmt = """create index ix21 on BTRE212 (s);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select s from BTRE212 order by s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s20')
    
    stmt = """create index ix22 on BTRE212 (s_to_f);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select s_to_f from BTRE212 order by s_to_f;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s21')
    
    # TABLE BTRE213;
    stmt = """create index ix23 on BTRE213 (date1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select date1 from BTRE213 order by date1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s22')
    
    stmt = """create index ix24 on BTRE213 (time1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select time1 from BTRE213 order by time1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s23')
    
    # TABLE BTRE217;
    stmt = """create index ix25 on BTRE217 (dt1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select dt1 from BTRE217 order by dt1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s24')
    
    stmt = """create index ix26 on BTRE217 (tm1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select tm1 from BTRE217 order by tm1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s25')
    
    stmt = """create index ix27 on BTRE217 (dt2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select dt2 from BTRE217 order by dt2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s26')
    
    stmt = """create index ix28 on BTRE217 (tm2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select tm2 from BTRE217 order by tm2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s27')
    
    stmt = """create index ix29 on BTRE217 (dt3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select dt3 from BTRE217 order by dt3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s28')
    
    stmt = """create index ix30 on BTRE217 (tm3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select tm3 from BTRE217 order by tm3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s29')
    
    stmt = """create index ix31 on BTRE217 (dt4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select dt4 from BTRE217 order by dt4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s30')
    
    stmt = """create index ix32 on BTRE217 (tm4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select tm4 from BTRE217 order by tm4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s31')
    
    # TABLE BTRE218;
    stmt = """create index ix33 on BTRE218 (y);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select y from BTRE218 order by y;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s32')
    
    stmt = """create index ix34 on BTRE218 (y_to_mo);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select y_to_mo from BTRE218 order by y_to_mo;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s33')
    
    stmt = """create index ix35 on BTRE218 (mo);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select mo from BTRE218 order by mo;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s34')
    
    stmt = """create index ix36 on BTRE218 (d);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select d from BTRE218 order by d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s35')
    
    stmt = """create index ix37 on BTRE218 (d_to_h);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select d_to_h from BTRE218 order by d_to_h;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s36')
    
    stmt = """create index ix38 on BTRE218 (d_to_mi);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select d_to_mi from BTRE218 order by d_to_mi;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s37')
    
    stmt = """create index ix39 on BTRE218 (d_to_s);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select d_to_s from BTRE218 order by d_to_s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s38')
    
    stmt = """create index ix40 on BTRE218 (h_to_mi);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select h_to_mi from BTRE218 order by h_to_mi;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s39')
    
    # TABLE BTRE219;
    stmt = """create index ix41 on BTRE219 (y_to_d);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select y_to_d from BTRE219 order by y_to_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s40')
    
    _testmgr.testcase_end(desc)

def test012(desc="""SQL downshifts 24th character of a date or an interval column name."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0140 : testB03.sql
    #  Description:        SQL downshifts 24th character of a date or an
    #                      interval column name.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the 'Title'
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT * FROM TEMPB3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b03exp""", 'b03s0')
    
    #  expect 2 rows with the following values:
    #       2455            1988-05-01                    23
    #         43            1967-09-12                     6
    
    stmt = """SELECT INTERVALCOLIS30CHARACTERSLONGG,
DATECOLUMNIS30CHARACTERSLONGGG
FROM TEMPB3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b03exp""", 'b03s1')
    # expect 2 rows with the following values:
    #        23                      1988-05-01
    #         6                      1967-09-12
    #
    
    stmt = """delete from TEMPB3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    
    _testmgr.testcase_end(desc)

def test013(desc="""Adding an interval data type column default requires"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #  default value specified to be equal to that of the column definition.
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0140 : testB04.sql
    #  Description:        Adding an interval data type column default
    #                      requires default value specified to be equal
    #                      to that of the column definition.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    #  can't do DEFAULT
    #  can't do ALTER TABLE
    #  alter table tempb4 add column
    #     col2        interval day(4) default interval '0' day not null;
    #     col2 interval day(4) not null;
    
    #  alter table tempb4 add column
    #     col3        interval day(4) default interval '0' day(1) not null;
    #     col3 interval day(4) not null;
    
    #  alter table tempb4 add column
    #     col4        interval day(4) default interval '0' day(5) not null;
    #     col4 interval day(4) not null;
    
    #  alter table tempb4 add column
    #     col5        interval day(4) default interval '0' day(4) not null;
    #     col5 interval day(4) not null;
    
    #  do something for the time being
    # insert into tempb4a values (interval '15' day);
    # insert into tempb4 values ('X');
    
    stmt = """select col1 as "no alter table yet" from tempb4a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b04exp""", 'b04s0')
    
    stmt = """select col1 as "no alter table yet" from tempb4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b04exp""", 'b04s1')
    
    _testmgr.testcase_end(desc)

def test014(desc="""DATE, TIME column definitions no longer require 'AT GMT' syntax."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0140 : testB05.sql
    #  Description:        DATE, TIME column definitions no longer
    #                      require 'AT GMT' syntax.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the 'Title'
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """create table tempb5 (
col1 int,
col2 time                         -- XXXXX default time '6:0:0'
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # XXXXX can't do alter table
    #     alter table tempb5
    #         add column col3 time default time '3:0:0';
    
    #     alter table tempb5
    #         add column col4 time default time '4:0:0';
    
    # just do something
    stmt = """insert into tempb5 values (99, time '15:50:30');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from tempb5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b05exp""", 'b05s0')
    # end just do
    
    stmt = """drop table tempb5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test015(desc="""Create table with indexes on DATETIME FRACTION column"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0140 : testB06.sql
    #  Description:        Create table with indexes on DATETIME FRACTION column
    #                      and store and fetch data.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the 'Title'
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    # Create non-UNIQUE INDEX on DECIMAL column.
    #
    
    stmt = """CREATE INDEX B6index3 
ON b6table1 (D8_4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Insert 4 rows of data into the table.
    
    stmt = """INSERT INTO b6table1 values
(time '10:15:30.555', 8.4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO b6table1 values
(time '04:54:57.345', 8.4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO b6table1 values
(time '19:09:10.234', 8.4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO b6table1 values
(time '00:00:00.00', 8.4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # Set the DATETIME columns to max. This puts in the 5th row.
    
    stmt = """INSERT INTO b6table1 VALUES
( time '23:59:59.999',
123.456
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  Create view to see if same results through view.
    #  CREATE VIEW statements moved to the PREUNT
    #
    #       CREATE VIEW b6view1 AS
    #          SELECT F3
    #             FROM b6table1 ;
    
    #
    #  Create view to see if same results through view.
    #
    #       CREATE VIEW b6view2 AS
    #          SELECT D8_4
    #             FROM b6table1;
    
    #
    #  Try to force optimizer to use primary key path.
    #  The original problem was the return of only one row.
    #
    
    stmt = """SELECT F3
FROM b6table1 
ORDER BY F3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b06exp""", 'b06s0')
    
    #  expect 5 rows with the following values:
    #  	00:00:00.000
    #  	04:54:57.345
    #  	10:15:30.555
    #  	19:09:10.234
    #  	23:59:59.999
    
    #
    #  Now check through view.
    #
    
    stmt = """SELECT *
FROM b6view1 
ORDER BY F3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b06exp""", 'b06s1')
    
    #  expect the same 5 rows as above
    
    #
    #  Try to force optimizer to use alternate key path.
    #  The original problem was the return of only 4 out of the 5 rows.
    #
    
    stmt = """SELECT D8_4
FROM b6table1 
ORDER BY D8_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b06exp""", 'b06s2')
    
    #  expect 5 rows with the following values:
    #  	8.4000
    #  	8.4000
    #  	8.4000
    #  	8.4000
    #  	123.4560
    
    #  Now check through view.
    
    stmt = """SELECT *
FROM b6view2 
ORDER BY D8_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b06exp""", 'b06s3')
    
    #  expect the same 5 rows as above
    
    #  Try to force optimizer to use alternate key path.
    #  The original problem was the return of only 4 out of the 5 rows.
    
    stmt = """SELECT d8_4
FROM b6table1 
ORDER BY d8_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b06exp""", 'b06s4')
    
    #  Try to force optimizer to use alternate key path.
    
    stmt = """SELECT F3, D8_4
FROM b6table1 
ORDER BY D8_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b06exp""", 'b06s5')
    
    # expect 5 rows with the following values:
    # 	10:15:30.555      8.4000
    # 	04:54:57.345      8.4000
    # 	19:09:10.234      8.4000
    # 	00:00:00.000      8.4000
    # 	23:59:59.999    123.4560
    
    #
    # Select was not the only one with a problem.  This update
    # should update all rows.
    #
    
    stmt = """UPDATE b6table1 
SET D8_4 = 0.0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    
    #
    #  Check results of update.
    #
    
    stmt = """SELECT F3, D8_4
FROM b6table1 
ORDER BY D8_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b06exp""", 'b06s6')
    
    _testmgr.testcase_end(desc)

def test016(desc="""clean up file for the arkt0140 datetime tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # PSTUNT
    # johncl
    # 1997-02-14
    # clean up file for the arkt0140 datetime tests
    #----------------------------------------------
    
    stmt = """drop view b6view1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view b6view2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table b6table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # drop table BTRE211;
    stmt = """drop table BTRE211;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table BTRE213;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table BTRE217;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table BTRE218;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table BTRE219;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table TEMP1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table datekey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table TEMPB3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table tempb4a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table tempb4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

