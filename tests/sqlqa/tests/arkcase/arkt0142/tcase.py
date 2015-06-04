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
    # set up file for the arkt0140 datetime tests
    
    #  While converting from fraction to second the precision is
    #  taken as 3 instead of 6, because values inserted are having
    #  only 3 digits at max.
    
    # the table aBTRE211 is used in testA01, testA07 and testB02b
    
    stmt = """CREATE TABLE aBTRE211 (
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
inter interval hour to second(0) not null
) no partition
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
(col1 pic x) no partition; -- pic x = char (1)"""
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
    
    stmt = """INSERT INTO aBTRE211 VALUES (
date  '1988-01-01' ,
timestamp  '1988-01-01:12:35:30' ,
timestamp  '1988-01-01:12:35:30.333' ,
time  '10:15:30' ,
time  '10:15:30.555'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO aBTRE211 VALUES (
date '1977-03-02' ,
timestamp '1979-06-05:14:40:45' ,
timestamp '1980-07-06:15:45:50.678' ,
time '03:53:56' ,
time '04:54:57.345'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO aBTRE211 VALUES (
date '0802-09-07' ,
timestamp '0805-12-10:07:59:03' ,
timestamp  '0806-01-11:08:01:04.789' ,
time '18:08:09' ,
time '19:09:10.234'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO aBTRE211 VALUES (
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

def test002(desc="""a06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0142 : testA06.sql
    #  Description:        This testcase tests following arithmetic
    #                      operation on the column of two table with
    #                      data types INTERVAL.
    #                      1. interval + interval = interval
    #                      2. interval - interval = interval
    #                      3. interval * scalar   = interval
    #                      4. interval / scalar   = interval
    #                      5. scalar   * interval = interval
    #                      6. interval / interval = numeric
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the 'Title'
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT Y_to_MO, Y
FROM BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s0')
    #  expect 4 rows with the following values:
    #  	   10-01     10
    #  	 9999-11   9999
    #  	    1-01      1
    #  	    1-01      1
    
    stmt = """SELECT Y_to_MO + Y
FROM BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s1')
    #  expect 4 rows with the following values:
    #  	    20-01
    #  	 19998-11
    #  	     2-01
    #  	     2-01
    
    #  #2 interval - interval = interval
    stmt = """SELECT D_to_S, D_to_F
FROM BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s2')
    #  expect 4 rows with the following values:
    #      17 14:16:01   18 15:17:02.123
    #      28 03:58:59   27 04:57:58.999
    #       1 01:01:01    1 01:01:01.100
    #       0 00:00:00    0 00:00:00.000
    
    stmt = """SELECT D_to_S - D_to_F
FROM BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s3')
    #  expect 4 rows with the following values:
    #     -  1 01:01:01.123
    #        0 23:01:00.001
    #     -  0 00:00:00.100
    #        0 00:00:00.000
    
    #  #3 interval * scalar   = interval
    stmt = """SELECT Y_to_MO
FROM BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s4')
    #  expect 4 rows with the following values:
    #          10-01
    #        9999-11
    #           1-01
    #           1-01
    
    stmt = """SELECT Y_to_MO * 2
FROM BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s5')
    #  expect 4 rows with the following values:
    #         20-02
    #      19999-10
    #          2-02
    #          2-02
    
    #  #4 interval / scalar   = interval
    stmt = """SELECT D_to_S
FROM BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s6')
    #  expect 4 rows with the following values:
    #  	 17 14:16:01
    #  	 28 03:58:59
    #  	  1 01:01:01
    #  	  0 00:00:00
    
    stmt = """SELECT D_to_S / 5
FROM BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s7')
    #  expect 4 rows with the following values:
    #       3 12:27:12
    #       5 15:11:47
    #       0 05:00:12
    #       0 00:00:00
    
    #  #5 scalar   * interval = interval
    stmt = """SELECT Y_to_MO
FROM BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s8')
    #  expect 4 rows with the following values:
    #          10-01
    #        9999-11
    #           1-01
    #           1-01
    
    stmt = """SELECT 5 * Y_to_MO
FROM BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s9')
    #  expect 4 rows with the following values:
    #         50-05
    #      49999-07
    #          5-05
    #          5-05
    
    #  #6 interval / interval = numeric
    stmt = """SELECT Y_to_MO, Y
FROM BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s10')
    #  expect 4 rows with the following values:
    #        10-01     10
    #      9999-11   9999
    #         1-01      1
    #         1-01      1
    
    stmt = """SELECT Y_to_MO / Y
FROM BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4034')
    #  gets an error
    
    stmt = """SELECT Y / Y_to_MO
FROM BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4034')
    
    _testmgr.testcase_end(desc)

def test003(desc="""a07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0142 : testA07.sql
    #  Description:        This testcase tests the following arithmetic
    #                      operations on the data types DATE and TIME:
    #                    1. date - date = interval
    #                    2. time - time = interval
    #                    3. date - time = interval
    #                    4. time - date = interval
    #                    5. date + interval = datetime
    #                    6. date - interval = datetime
    #                    7. time + interval = datetime
    #                    8. time - interval = datetime
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the 'Title'
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    #  #1. date - date = interval
    stmt = """SELECT DT1, DT4
FROM BTRE217;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s0')
    #  expect 2 rows with the following values:
    #  	         ?  1985-10-15
    #  	1948-06-15  1920-05-06
    
    stmt = """SELECT (DT1 -  DT4) YEAR
FROM BTRE217 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4035')
    #  expect 2 rows with the following values:
    #  	     ?
    #  	    28
    
    stmt = """SELECT (DT1 -  DT4) MONTH
FROM BTRE217 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4035')
    #  expect 2 rows with the following values:
    #  	     ?
    #  	   337
    
    stmt = """SELECT (DT1 -  DT4) DAY
FROM BTRE217 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    #  expect 2 rows with the following values:
    #  	     ?
    #  	 10267
    
    stmt = """SELECT (DATE1 - DATE1) day
FROM BTRE213;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s4')
    #  expect 4 rows with zeros
    
    #     INSERT INTO TEMP13
    #           (SELECT (DATE1 - DATE1) day
    #                  FROM BTRE213
    #           );
    
    #     SELECT * FROM TEMP13;
    #  expect 4 rows with all zeros
    
    #  #2. time - time = interval
    stmt = """SELECT TM3 , TM4
FROM BTRE217 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s5')
    #  expect 2 rows with the following values:
    #  	23:12:45  12:35:45
    #  	15:18:24  01:10:25
    
    #  INSERT INTO TEMP13
    #     (SELECT (TM3 - TM4) hour
    #         FROM BTRE217);
    
    #     SELECT * FROM TEMP13 ;
    #  expect 6 rows, 4 rows all zeros and 2 with the following values:
    #  	  0 11:00:00.000000
    #  	  0 14:00:00.000000
    
    #  #3. date - time = interval
    #  SELECT DATE1, TIME1
    #      FROM BTRE213;
    #
    #  SELECT ( extend(DATE1, year to fraction) -
    #           extend(TIME1, year to fraction) )
    #                       DAY TO FRACTION
    #                    FROM BTRE213
    #                    WHERE DATE1 = date '1988-10-25'
    #             ;
    
    #  #4. time - date = interval
    #              SELECT        TIME1,
    #                            DATE1
    #                    FROM BTRE213
    #             ;
    #              SELECT CAST(  extend(TIME1, year to fraction) -
    #                       extend(DATE1, year to fraction) )
    #                       INTERVAL DAY TO FRACTION)
    #                    FROM BTRE213
    #                    WHERE DATE1 = date '1988-10-25'
    #             ;
    #  gets error
    
    #  #5. date + interval = datetime
    stmt = """SELECT DATE1
FROM BTRE213;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s6')
    #  expect 4 rows with the following values:
    #  	1988-10-25
    #  	0100-01-01
    #  	0100-01-01
    #  	1954-05-06
    
    stmt = """SELECT BTRE212.Y_TO_MO
FROM BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s7')
    #  expect 4 rows with the following values:
    #  	   10-01
    #  	 9999-11
    #  	    1-01
    #  	    1-01
    
    stmt = """SELECT DATE1 + BTRE212.Y_TO_MO
FROM BTRE213, BTRE212 
WHERE DATE1 = date '1988-10-25'
AND
 BTRE212.Y = interval '1' YEAR
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s8')
    
    #  expect 2 rows with the following values:
    #  	1998-11-25
    #  	1989-11-25
    
    #  #6. date - interval = datetime
    #  delete from temp11;
    
    stmt = """SELECT DATE1
FROM BTRE213;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s10')
    #  expect 4 rows with the following values:
    #  	1988-10-25
    #  	0100-01-01
    #  	0100-01-01
    #  	1954-05-06
    
    stmt = """SELECT BTRE212.Y_TO_MO
FROM BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s11')
    #  expect 4 rows with the following values:
    #        10-01
    #      9999-11
    #         1-01
    #         1-01
    
    stmt = """SELECT DATE1 - BTRE212.Y_TO_MO
FROM BTRE213, BTRE212 
WHERE DATE1 = date '1988-10-25'
AND
 BTRE212.Y = interval '1' YEAR
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s12')
    
    #  #7. time + interval = datetime
    stmt = """SELECT TIME1, DATE1
FROM BTRE213;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s14')
    #  expect 4 rows with the following values:
    #  10:10:10  1988-10-25
    #  00:00:00  0100-01-01
    #  23:59:59  0100-01-01
    #  22:23:24  1954-05-06
    
    stmt = """SELECT Y, H, D_to_S
FROM BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s15')
    #  expect 4 rows with the following values:
    #        10   16   17 14:16:01
    #      9999   23   28 03:58:59
    #         1    1    1 01:01:01
    #         1    0    0 00:00:00
    
    stmt = """SELECT TIME1 + BTRE212.H
FROM BTRE213, BTRE212 
--          WHERE DATE1 = date '1988-10-25'
--              AND
--          BTRE212.Y = interval '1' YEAR
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s16')
    #  expect 16 rows with the following values:
    #  	02:10:10
    #  	10:10:10
    #  	11:10:10
    #  	09:10:10
    #  	16:00:00
    #  	00:00:00
    #  	01:00:00
    #  	23:00:00
    #  	15:59:59
    #  	23:59:59
    #  	00:59:59
    #  	22:59:59
    #  	14:23:24
    #  	22:23:24
    #  	23:23:24
    #  	21:23:24
    
    stmt = """SELECT TIME1, CAST (BTRE212.D_to_S as INTERVAL DAY TO SECOND), DATE1
FROM BTRE213, BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s17')
    #SELECT TIME1, CAST (BTRE212.D_to_S as INTERVAL HOUR TO SECOND), DATE1
    #    FROM BTRE213, BTRE212;
    #  expect 16 rows with the following values (expr thous look odd):
    #  	TIME1     (EXPR)            DATE1
    #  	--------  ----------------  ----------
    #
    #  	10:10:10    0:00:01.520161  1988-10-25
    #  	10:10:10    0:00:00.000000  1988-10-25
    #  	10:10:10    0:00:00.090061  1988-10-25
    #  	10:10:10    0:00:02.433539  1988-10-25
    #  	00:00:00    0:00:01.520161  0100-01-01
    #  	00:00:00    0:00:00.000000  0100-01-01
    #  	00:00:00    0:00:00.090061  0100-01-01
    #  	00:00:00    0:00:02.433539  0100-01-01
    #  	23:59:59    0:00:01.520161  0100-01-01
    #  	23:59:59    0:00:00.000000  0100-01-01
    #  	23:59:59    0:00:00.090061  0100-01-01
    #  	23:59:59    0:00:02.433539  0100-01-01
    #  	22:23:24    0:00:01.520161  1954-05-06
    #  	22:23:24    0:00:00.000000  1954-05-06
    #  	22:23:24    0:00:00.090061  1954-05-06
    #  	22:23:24    0:00:02.433539  1954-05-06
    
    stmt = """SELECT TIME1 + CAST (BTRE212.D_to_S as INTERVAL day to second)
FROM BTRE213, BTRE212 
;"""
    output = _dci.cmdexec(stmt)
    #  expect 16 rows with the following values):
    #  	10:10:11
    #  	10:10:10
    #  	10:10:10
    #  	10:10:12
    #  	00:00:01
    #  	00:00:00
    #  	00:00:00
    #  	00:00:02
    #  	00:00:00
    #  	23:59:59
    #  	23:59:59
    #  	00:00:01
    #  	22:23:25
    #  	22:23:24
    #  	22:23:24
    #  	22:23:26
    
    #  (1) This is a negative test and should be moved to T159.
    #  (2) To make this a positive test, use EXTEND.
    stmt = """SELECT TIME1 + cast(BTRE212.Y as INTERVAL hour to second)
FROM BTRE213, BTRE212 
--          WHERE DATE1 = date '1988-10-25'
--              AND
--          BTRE212.Y = interval '1' YEAR
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4035')
    #  gets error: The type, INTERVAL YEAR(4), cannot be cast to the type,
    # 	       INTERVAL HOUR(2) TO SECOND(6).
    
    #  #8. time - interval = datetime
    stmt = """SELECT TIME1, DATE1
FROM BTRE213;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s20')
    #  expect 4 rows with the following values:
    #  10:10:10  1988-10-25
    #  00:00:00  0100-01-01
    #  23:59:59  0100-01-01
    #  22:23:24  1954-05-06
    
    stmt = """SELECT Y, Y_TO_MO, H, D_to_S
FROM BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s21')
    #  expect 4 rows with the following values:
    #  	   10     10-01   16   17 14:16:01
    #  	 9999   9999-11   23   28 03:58:59
    #  	    1      1-01    1    1 01:01:01
    #  	    1      1-01    0    0 00:00:00
    
    stmt = """SELECT TIME1, BTRE212.H, DATE1, BTRE212.Y
FROM BTRE213, BTRE212 
--          WHERE DATE1 = date '1988-10-25'
--              AND
--          BTRE212.Y = interval '1' YEAR
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s22')
    #  expect 16 rows with the following values:
    #  	TIME1     H    DATE1       Y
    #  	--------  ---  ----------  -----
    #
    #  	10:10:10   16  1988-10-25     10
    #  	10:10:10    0  1988-10-25      1
    #  	10:10:10    1  1988-10-25      1
    #  	10:10:10   23  1988-10-25   9999
    #  	00:00:00   16  0100-01-01     10
    #  	00:00:00    0  0100-01-01      1
    #  	00:00:00    1  0100-01-01      1
    #  	00:00:00   23  0100-01-01   9999
    #  	23:59:59   16  0100-01-01     10
    #  	23:59:59    0  0100-01-01      1
    #  	23:59:59    1  0100-01-01      1
    #  	23:59:59   23  0100-01-01   9999
    #  	22:23:24   16  1954-05-06     10
    #  	22:23:24    0  1954-05-06      1
    #  	22:23:24    1  1954-05-06      1
    #  	22:23:24   23  1954-05-06   9999
    
    stmt = """SELECT TIME1, BTRE212.H, TIME1 - BTRE212.H, DATE1, BTRE212.Y
FROM BTRE213, BTRE212 
--          WHERE DATE1 = date '1988-10-25'
--              AND
--          BTRE212.Y = interval '1' YEAR
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s23')
    #  expect 16 rows with the following values:
    #  	TIME1     H    (EXPR)    DATE1       Y
    #  	--------  ---  --------  ----------  -----
    #
    #  	10:10:10   16  18:10:10  1988-10-25     10
    #  	10:10:10    0  10:10:10  1988-10-25      1
    #  	10:10:10    1  09:10:10  1988-10-25      1
    #  	10:10:10   23  11:10:10  1988-10-25   9999
    #  	00:00:00   16  08:00:00  0100-01-01     10
    #  	00:00:00    0  00:00:00  0100-01-01      1
    #  	00:00:00    1  23:00:00  0100-01-01      1
    #  	00:00:00   23  01:00:00  0100-01-01   9999
    #  	23:59:59   16  07:59:59  0100-01-01     10
    #  	23:59:59    0  23:59:59  0100-01-01      1
    #  	23:59:59    1  22:59:59  0100-01-01      1
    #  	23:59:59   23  00:59:59  0100-01-01   9999
    #  	22:23:24   16  06:23:24  1954-05-06     10
    #  	22:23:24    0  22:23:24  1954-05-06      1
    #  	22:23:24    1  21:23:24  1954-05-06      1
    #  	22:23:24   23  23:23:24  1954-05-06   9999
    
    stmt = """SELECT TIME1, cast(BTRE212.D_to_S as interval hour to second),
TIME1 - cast(BTRE212.D_to_S as interval hour to second),
DATE1, BTRE212.Y
FROM BTRE213, BTRE212 
WHERE DATE1 = date '1988-10-25'
AND
 BTRE212.Y = interval '1' YEAR
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s24')
    
    _testmgr.testcase_end(desc)

def test004(desc="""a08"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0142 : testA08.sql
    #  Description:        This test case will test the following
    #                      comparison on a table with data type DATE,timestamp.
    #                      Equal =  (removed from the test)
    #                      Not Equal <>
    #                      Less Than <
    #                      Greater Than > (removed from the test)
    #                      Less Than or Equal <=
    #                      Greater Than or Equal >= (removed from the test)
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the 'Title'
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT Y_TO_D, Y_TO_S, Y_TO_F FROM aBTRE211 
WHERE Y_TO_S <> timestamp '1944-05-10:15:20:25';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s0')
    #  should select 4 rows with the following values:
    #  Y_TO_D      Y_TO_S                      Y_TO_F
    #  ----------  --------------------------  -----------------------
    #
    #  1988-01-01  1988-01-01 12:35:30.000000  1988-01-01 12:35:30.333
    #  1977-03-02  1979-06-05 14:40:45.000000  1980-07-06 15:45:50.678
    #  0802-09-07  0805-12-10 07:59:03.000000  0806-01-11 08:01:04.789
    #  0001-01-01  0001-01-01 00:00:00.000000  0001-01-01 00:00:00.000
    
    stmt = """SELECT Y_TO_D, Y_TO_S, Y_TO_F FROM aBTRE211 
WHERE Y_TO_D < date '1500-10-08';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s1')
    #  should select 2 rows with the following values:
    #  Y_TO_D      Y_TO_S                      Y_TO_F
    #  ----------  --------------------------  -----------------------
    #
    #  0802-09-07  0805-12-10 07:59:03.000000  0806-01-11 08:01:04.789
    #  0001-01-01  0001-01-01 00:00:00.000000  0001-01-01 00:00:00.000
    
    stmt = """SELECT Y_TO_D, Y_TO_S, Y_TO_F FROM aBTRE211 
WHERE Y_TO_D <= date '1988-01-25';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s2')
    
    _testmgr.testcase_end(desc)

def test005(desc="""a09"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0142 : testA09.sql
    #  Description:        This test case will test the following
    #                      comparison on a table with data type INTERVAL.
    #                      Equal =
    #                      Not Equal <>
    #                      Less Than <
    #                      Greater Than >
    #                      Less Than or Equal <=
    #                      Greater Than or Equal >=
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the 'Title'
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT Y, Y_TO_MO, MO FROM BTRE212 
WHERE Y_TO_MO = interval '1' year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #  should select 0 rows
    
    stmt = """SELECT D, D_TO_H, D_TO_MI, D_TO_S, D_TO_F FROM BTRE212 
WHERE D <> interval '10' day;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s0')
    #  should select 4 rows with the following values:
    #  D    D_TO_H  D_TO_MI    D_TO_S        D_TO_F
    #  ---  ------  ---------  ------------  ----------------
    #
    #   15   15 12   16 13:15   17 14:16:01   18 15:17:02.123
    #   31   30 01   29 02:59   28 03:58:59   27 04:57:58.999
    #    1    1 01    1 01:01    1 01:01:01    1 01:01:01.100
    #    1    0 00    0 00:00    0 00:00:00    0 00:00:00.000
    
    stmt = """SELECT D, D_TO_H, D_TO_MI, D_TO_S, D_TO_F FROM BTRE212 
WHERE D_TO_H < interval '15:22' day TO HOUR;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s1')
    #  should select 3 rows with the following values:
    #  D    D_TO_H  D_TO_MI    D_TO_S        D_TO_F
    #  ---  ------  ---------  ------------  ----------------
    #
    #   15   15 12   16 13:15   17 14:16:01   18 15:17:02.123
    #    1    1 01    1 01:01    1 01:01:01    1 01:01:01.100
    #    1    0 00    0 00:00    0 00:00:00    0 00:00:00.000
    
    stmt = """SELECT S, S_TO_F FROM BTRE212 
WHERE S > interval '54' second;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s2')
    #  should select 1 row with the following values:
    #  S    S_TO_F
    #  ---  -------
    #
    #   59   58.666
    
    stmt = """SELECT S, S_TO_F FROM BTRE212 
WHERE S_TO_F <= interval '45.789' second(2,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s3')
    
    _testmgr.testcase_end(desc)

def test006(desc="""b00"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0142 : testB00.sql
    #  Description:        This test case will test the following comparison
    #                      on a table with data type DATE and TIME :
    #                      Equal =
    #                      Not Equal <>
    #                      Less Than <
    #                      Greater Than >
    #                      Less Than or Equal <=
    #                      Greater Than or Equal >=
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the 'Title'
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT * FROM BTRE213 
WHERE DATE1 = date '1988-10-25';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b00exp""", 'b00s0')
    #  should select 1 row with the following values:
    #  	1988-10-25  10:10:10
    
    stmt = """SELECT * FROM BTRE213 
WHERE DATE1 <> date '1988-10-25';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b00exp""", 'b00s1')
    #  should select 3 rows with the following values:
    #  DATE1       TIME1
    #  ----------  --------
    #
    #  0100-01-01  00:00:00
    #  0100-01-01  23:59:59
    #  1954-05-06  22:23:24
    
    stmt = """SELECT * FROM BTRE213 
WHERE not DATE1 = date '1988-10-25';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b00exp""", 'b00s2')
    #  should select the same 3 rows as above
    
    stmt = """SELECT * FROM BTRE213 
WHERE DATE1 < date '1944-05-10';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b00exp""", 'b00s3')
    #  should select 2 rows with the following values:
    #  DATE1       TIME1
    #  ----------  --------
    #
    #  0100-01-01  00:00:00
    #  0100-01-01  23:59:59
    
    stmt = """SELECT * FROM BTRE213 
WHERE DATE1 > date '1140-10-10';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b00exp""", 'b00s4')
    #  should select 2 rows with the following values:
    #  DATE1       TIME1
    #  ----------  --------
    #
    #  1988-10-25  10:10:10
    #  1954-05-06  22:23:24
    
    stmt = """SELECT * FROM BTRE213 
WHERE DATE1 <= date '1988-10-25';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b00exp""", 'b00s5')
    #  should select 4 rows with the following values:
    #  DATE1       TIME1
    #  ----------  --------
    #
    #  1988-10-25  10:10:10
    #  0100-01-01  00:00:00
    #  0100-01-01  23:59:59
    #  1954-05-06  22:23:24
    
    stmt = """SELECT * FROM BTRE213 
WHERE DATE1 >= date '0100-01-01';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b00exp""", 'b00s6')
    #  should select the same 4 rows as above
    
    stmt = """SELECT * FROM BTRE213 
WHERE TIME1 = time '10:10:10';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b00exp""", 'b00s7')
    #  should select 1 row with the following values:
    #  1988-10-25  10:10:10
    
    stmt = """SELECT * FROM BTRE213 
WHERE TIME1 <> time '10:10:10';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b00exp""", 'b00s8')
    #  should select 3 rows with the following values:
    #  DATE1       TIME1
    #  ----------  --------
    #
    #  0100-01-01  00:00:00
    #  0100-01-01  23:59:59
    #  1954-05-06  22:23:24
    
    stmt = """SELECT * FROM BTRE213 
WHERE TIME1 < time '23:23:23';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b00exp""", 'b00s9')
    #  should select 2 rows with the following values:
    #  DATE1       TIME1
    #  ----------  --------
    #
    #  1988-10-25  10:10:10
    #  0100-01-01  00:00:00
    
    stmt = """SELECT * FROM BTRE213 
WHERE TIME1 > time '05:05:05';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b00exp""", 'b00s10')
    #  should select 3 rows with the following values:
    #  DATE1       TIME1
    #  ----------  --------
    #
    #  1988-10-25  10:10:10
    #  0100-01-01  23:59:59
    #  1954-05-06  22:23:24
    
    stmt = """SELECT * FROM BTRE213 
WHERE TIME1 <= time '10:10:10';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b00exp""", 'b00s11')
    #  should select 2 rows with the following values:
    #  DATE1       TIME1
    #  ----------  --------
    #
    #  1988-10-25  10:10:10
    #  0100-01-01  00:00:00
    
    stmt = """SELECT * FROM BTRE213 
WHERE TIME1 >= time '10:10:10';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b00exp""", 'b00s12')
    
    _testmgr.testcase_end(desc)

def test007(desc="""b01"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0142 : testB01.sql
    #  Description:        Perform Division operations on a table with
    #                      INTERVAL datatypes containing FRACTION fields.
    #
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT D_to_F, D_to_F / 1
FROM BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b01exp""", 'b01s0')
    #  should select 4 rows with the following values:
    #  	D_TO_F            (EXPR)
    #  	----------------  ----------------
    #
    #  	 18 15:17:02.123   18 15:17:02.123
    #  	 27 04:57:58.999   27 04:57:58.999
    #  	  1 01:01:01.100    1 01:01:01.100
    #  	  0 00:00:00.000    0 00:00:00.000
    
    stmt = """SELECT D_to_F, D_to_F / 2
FROM BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b01exp""", 'b01s1')
    #  should select 4 rows with the following values:
    #  	D_TO_F            (EXPR)
    #  	----------------  ----------------
    #
    #  	 18 15:17:02.123    9 07:38:31.061
    #  	 27 04:57:58.999   13 14:28:59.499
    #  	  1 01:01:01.100    0 12:30:30.550
    #  	  0 00:00:00.000    0 00:00:00.000
    
    stmt = """SELECT H_to_F,
H_to_F / 10,
MI_to_F,
MI_to_F / 2,
S_to_F,
S_to_F / 60
FROM BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b01exp""", 'b01s2')
    
    _testmgr.testcase_end(desc)

def test008(desc="""c00"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """drop TABLE TEMP1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # drop TABLE TEMP11;
    # drop TABLE TEMP12;
    # drop TABLE TEMP13;
    # drop TABLE TEMP14;
    
    stmt = """drop TABLE aBTRE211;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop TABLE BTRE212;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop TABLE BTRE213;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop TABLE BTRE217;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop TABLE BTRE218;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop TABLE BTRE219;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop index datekey0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop TABLE datekey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view b6view1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view b6view2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop TABLE b6table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table tempb4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table tempb4a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table TEMPB3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

