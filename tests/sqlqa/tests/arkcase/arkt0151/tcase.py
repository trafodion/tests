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
    
    # BTRE211U is used int testA01
    
    stmt = """CREATE  TABLE  BTRE211U (
Y_to_D date,
Y_to_S timestamp(6),
Y_to_F timestamp(3),
H_to_S interval hour to second(6),
H_to_F interval hour to second(3)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # BTRE211C is used int testA02
    
    stmt = """CREATE  TABLE   BTRE211C (
Y_to_D_1       date  ,
Y_to_S         timestamp(6),
Y_to_F         timestamp(3)  ,
H_to_S         interval hour to second,
H_to_F_1       interval hour to second(3)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # BTRE212U is used int testA04
    
    stmt = """CREATE TABLE       BTRE212U (
Y           INTERVAL    YEAR(4),
Y_to_MO     INTERVAL    YEAR(4) TO MONTH,
MO          INTERVAL    MONTH,
D           INTERVAL    DAY,
D_to_H      INTERVAL    DAY TO HOUR,
D_to_MI     INTERVAL    DAY TO MINUTE,
D_to_S      INTERVAL    DAY TO SECOND,
D_to_F      INTERVAL    DAY TO SECOND(3),
H           INTERVAL    HOUR,
H_to_MI     INTERVAL    HOUR TO MINUTE,
H_to_S      INTERVAL    HOUR TO SECOND,
H_to_F      INTERVAL    HOUR TO SECOND(3),
MI          INTERVAL    MINUTE,
MI_to_S     INTERVAL    MINUTE TO SECOND,
MI_to_F     INTERVAL    MINUTE TO SECOND(3),
S           INTERVAL    SECOND(2),
S_to_F      INTERVAL    SECOND(2,3)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # BTRE212C is used int testA05
    stmt = """CREATE TABLE       BTRE212C (
Y           INTERVAL    YEAR(4),
Y_to_MO     INTERVAL    YEAR(4) TO MONTH,
MO          INTERVAL    MONTH,
D           INTERVAL    DAY,
D_to_H_1    INTERVAL    DAY TO HOUR,
D_to_MI     INTERVAL    DAY TO MINUTE,
D_to_S      INTERVAL    DAY TO SECOND,
D_to_F_1    INTERVAL    DAY TO SECOND(3),
H           INTERVAL    HOUR,
H_to_MI     INTERVAL    HOUR TO MINUTE,
H_to_S      INTERVAL    HOUR TO SECOND,
H_to_F_1    INTERVAL    HOUR TO SECOND(3),
MI          INTERVAL    MINUTE,
MI_to_S_1   INTERVAL    MINUTE TO SECOND,
MI_to_F     INTERVAL    MINUTE TO SECOND(3),
S_1         INTERVAL    SECOND(2),
S_to_F      INTERVAL    SECOND(2,3)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # BTRE213U is used int testA07
    
    stmt = """CREATE TABLE    BTRE213U (
DATE1       DATE,
TIME1       TIME
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # BTRE213C is used int testA08
    
    stmt = """CREATE TABLE    BTRE213C (
DATE1_1     DATE,
TIME1       TIME
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # BTRE217U is used int testB06
    
    stmt = """CREATE  TABLE     BTRE217U (
DT1       DATE   DEFAULT date '1987-06-15',
TM1       TIME   DEFAULT NULL,
DT2       DATE   DEFAULT NULL,
TM2       TIME   DEFAULT time '18:35:35'  not null,
DT3       DATE   DEFAULT NULL,
TM3       TIME   NO DEFAULT,
DT4       DATE   NO DEFAULT NOT NULL,
TM4       TIME   NOT NULL
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # BTRE217C is used int testB07
    
    stmt = """CREATE TABLE    BTRE217C (
DT1_1     DATE   DEFAULT date '1987-06-15',
TM1       TIME   DEFAULT NULL,
DT2       DATE   DEFAULT NULL,
TM2_1     TIME   DEFAULT time '18:35:35'  not null,
DT3       DATE   DEFAULT NULL,
TM3       TIME   NO DEFAULT,
DT4       DATE   NO DEFAULT NOT NULL,
TM4_1     TIME   NOT NULL
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # BTRE218U is used int testB03
    
    stmt = """CREATE TABLE    BTRE218U (
Y         INTERVAL YEAR(2) DEFAULT interval '1' year,
Y_to_MO   INTERVAL YEAR TO MONTH DEFAULT interval '00-00' year to month,
MO        INTERVAL MONTH DEFAULT NULL,
D         INTERVAL DAY DEFAULT interval '15' day NOT NULL,
D_to_H    INTERVAL DAY TO HOUR DEFAULT interval '00:00' day to hour NOT NULL,
D_to_MI   INTERVAL DAY TO MINUTE NO DEFAULT,
D_to_S    INTERVAL DAY TO SECOND NO DEFAULT NOT NULL,
H_to_MI   INTERVAL HOUR TO MINUTE NOT NULL
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # BTRE218C is used int testB04
    
    stmt = """CREATE TABLE    BTRE218C (
Y         INTERVAL YEAR(2) DEFAULT interval '01' year,
Y_to_MO   INTERVAL YEAR TO MONTH DEFAULT interval '00-00' year to month,
MO_1      INTERVAL MONTH DEFAULT NULL,
D         INTERVAL DAY DEFAULT interval '15' day NOT NULL,
D_to_H_1  INTERVAL DAY TO HOUR DEFAULT interval '00:00' day to hour NOT NULL,
D_to_MI   INTERVAL DAY TO MINUTE NO DEFAULT,
D_to_S_1  INTERVAL DAY TO SECOND NO DEFAULT NOT NULL,
H_to_MI   INTERVAL HOUR TO MINUTE NOT NULL
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # BTRE219U is used int testB00
    
    stmt = """CREATE TABLE   BTRE219U (
Y_to_D     date DEFAULT NULL
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # BTRE219C is used int testB01
    
    stmt = """CREATE TABLE    BTRE219C (
Y_to_D_1  DATE DEFAULT NULL
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO BTRE211U VALUES (
date   '1988-01-01' ,
timestamp   '1988-01-01:12:35:30' ,
timestamp   '1988-01-01:12:35:30.333' ,
interval '10:15:30' hour to second(6),
interval '10:15:30.555' hour to second(3)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE211U VALUES (
date  '1900-03-02' ,
timestamp  '1979-06-05:14:40:45' ,
timestamp  '1980-07-06:15:45:50.678' ,
interval  '03:53:56'  hour to second(6),
interval  '04:54:57.345'  hour to second(3)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE211U VALUES (
date  '0902-09-07' ,
timestamp  '0805-12-10:07:59:03' ,
timestamp  '0806-01-11:08:01:04.789' ,
interval  '18:08:09'  hour to second(6),
interval  '19:09:10.234'  hour to second(3)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE211U VALUES (
date  '0009-01-01' ,
timestamp  '0001-01-01:00:00:00' ,
timestamp  '0001-01-01:00:00:00.000' ,
interval  '00:00:00'  hour to second(6),
interval  '00:00:00.000'  hour to second(3)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # ** From TestA02 **
    stmt = """INSERT INTO BTRE211C VALUES (
date   '1988-01-01' ,
timestamp   '1988-01-01:12:35:30' ,
timestamp    '1988-01-01:12:35:30.333' ,
interval   '10:15:30' hour to second,
interval   '10:15:30.555' hour to second(3)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE211C VALUES (
date  '1900-03-02' ,
timestamp  '1979-06-05:14:40:45' ,
timestamp  '1980-07-06:15:45:50.678' ,
interval  '03:53:56'  hour to second,
interval  '04:54:57.345'  hour to second(3)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE211C VALUES (
date   '0902-09-07' ,
timestamp   '0805-12-10:07:59:03' ,
timestamp   '0806-01-11:08:01:04.789' ,
interval  '18:08:09'  hour to second,
interval  '19:09:10.234'  hour to second(3)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE211C VALUES (
date   '0009-01-01' ,
timestamp   '0001-01-01:00:00:00' ,
timestamp   '0001-01-01:00:00:00.000' ,
interval   '00:00:00'  hour to second,
interval   '00:00:00.00'  hour to second(3)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # ** From TestA03 **
    stmt = """INSERT INTO BTRE212U VALUES
( interval '10' year(2),
interval '10-01' year(2) TO MONTH,
interval '01' month,
interval '15' day,
interval '15:12' day TO HOUR,
interval '16:13:15' day TO MINUTE,
interval '17:14:16:01' DAY TO SECOND,
interval '18:15:17:02.123' DAY TO SECOND(3),
interval '16' hour,
interval '17:18' hour TO MINUTE,
interval '18:19:03' HOUR TO SECOND,
interval '19:20:04.345' HOUR TO SECOND(3),
interval '21' minute,
interval '21:05' MINUTE TO SECOND,
interval '22:06.444' MINUTE TO SECOND(3),
interval '07' SECOND(2,0),
interval '08.555' SECOND(2,3)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE212U VALUES
( interval '9999' year(4),
interval '9999-11' year(4) TO MONTH,
interval '11' month,
interval '31' day,
interval '30:01' day TO HOUR,
interval '29:02:59' day TO MINUTE,
interval '28:03:58:59' DAY TO SECOND,
interval '27:04:57:58.999' DAY TO SECOND(3),
interval '23' hour,
interval '22:56' hour TO MINUTE,
interval '21:55:57' HOUR TO SECOND,
interval '20:54:56.888' HOUR TO SECOND(3),
interval '59' minute,
interval '58:59' MINUTE TO SECOND,
interval '57:58.777' MINUTE TO SECOND(3),
interval '59' SECOND(2,0),
interval '58.666' SECOND(2,3)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE212U VALUES
( interval '9' year(4),
interval '9-1' year(4)  TO MONTH,
interval '9' month,
interval '9' day,
interval '1:1' day TO HOUR,
interval '1:1:1' day TO MINUTE,
interval '1:1:1:1' DAY TO SECOND,
interval '1:1:1:1.1' DAY TO SECOND(3),
interval '1' hour,
interval '1:1' hour TO MINUTE,
interval '1:1:1' HOUR TO SECOND,
interval '1:1:1.1' HOUR TO SECOND(3),
interval '1' minute,
interval '1:1' MINUTE TO SECOND,
interval '1:1.1' MINUTE TO SECOND(3),
interval '1' SECOND(2,0),
interval '1.1' SECOND(2,3)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE212U VALUES
( interval '7' year(2),
interval '7-1' year(2) TO MONTH,
interval '7' month,
interval '7' day,
interval '0:0' day TO HOUR,
interval '0:0:0' day TO MINUTE,
interval '0:0:0:0' DAY TO SECOND,
interval '0:0:0:0.0' DAY TO SECOND(3),
interval '0' hour,
interval '0:0' hour TO MINUTE,
interval '0:0:0' HOUR TO SECOND,
interval '0:0:0.0' HOUR TO SECOND(3),
interval '0' minute,
interval '0:0' MINUTE TO SECOND,
interval '0:0.0' MINUTE TO SECOND(3),
interval '0' SECOND(2,0),
interval '0.0' SECOND(2,3)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # ** From TestA05 **
    stmt = """INSERT INTO BTRE212C VALUES
( interval '10' year(2),
interval '10-01' year(2) TO MONTH,
interval '01' month,
interval '15' day,
interval '15:12' day TO HOUR,
interval '16:13:15' day TO MINUTE,
interval '17:14:16:01' DAY TO SECOND,
interval '18:15:17:02.123' DAY TO SECOND(3),
interval '16' hour,
interval '17:18' hour TO MINUTE,
interval '18:19:03' HOUR TO SECOND,
interval '19:20:04.345' HOUR TO SECOND(3),
interval '21' minute,
interval '21:05' MINUTE TO SECOND,
interval '22:06.444' MINUTE TO SECOND(3),
interval '07' SECOND(2,0),
interval '08.555' SECOND(2,3)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE212C VALUES
( interval '9999' year(4),
interval '9999-11' year(4) TO MONTH,
interval '11' month,
interval '31' day,
interval '30:01' day TO HOUR,
interval '29:02:59' day TO MINUTE,
interval '28:03:58:59' DAY TO SECOND,
interval '27:04:57:58.999' DAY TO SECOND(3),
interval '23' hour,
interval '22:56' hour TO MINUTE,
interval '21:55:57' HOUR TO SECOND,
interval '20:54:56.888' HOUR TO SECOND(3),
interval '59' minute,
interval '58:59' MINUTE TO SECOND,
interval '57:58.777' MINUTE TO SECOND(3),
interval '59' SECOND(2,0),
interval '58.666' SECOND(2,3)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE212C VALUES
( interval '9' year(4),
interval '9-1' year(4)  TO MONTH,
interval '9' month,
interval '9' day,
interval '1:1' day TO HOUR,
interval '1:1:1' day TO MINUTE,
interval '1:1:1:1' DAY TO SECOND,
interval '1:1:1:1.1' DAY TO SECOND(3),
interval '1' hour,
interval '1:1' hour TO MINUTE,
interval '1:1:1' HOUR TO SECOND,
interval '1:1:1.1' HOUR TO SECOND(3),
interval '1' minute,
interval '1:1' MINUTE TO SECOND,
interval '1:1.1' MINUTE TO SECOND(3),
interval '1' SECOND(2,0),
interval '1.1' SECOND(2,3)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE212C VALUES
( interval '7' year(2),
interval '7-1' year(2) TO MONTH,
interval '7' month,
interval '7' day,
interval '0:0' day TO HOUR,
interval '0:0:0' day TO MINUTE,
interval '0:0:0:0' DAY TO SECOND,
interval '0:0:0:0.0' DAY TO SECOND(3),
interval '0' hour,
interval '0:0' hour TO MINUTE,
interval '0:0:0' HOUR TO SECOND,
interval '0:0:0.0' HOUR TO SECOND(3),
interval '0' minute,
interval '0:0' MINUTE TO SECOND,
interval '0:0.0' MINUTE TO SECOND(3),
interval '0' SECOND(2,0),
interval '0.0' SECOND(2,3)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # ** From TestA07 **
    stmt = """INSERT INTO BTRE213U VALUES
( date '1988-10-25',
time '10:10:10'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE213U VALUES
( date '0100-01-01',
time '00:00:00'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE213U VALUES
( date '0500-01-01',
time '21:59:59'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE213U VALUES
( date '1800-05-06',
time '12:23:24'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # ** From TestA08 **
    stmt = """INSERT INTO BTRE213C VALUES
( date '1988-10-25',
time '10:10:10'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE213C VALUES
( date '0100-01-01',
time '00:00:00'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE213C VALUES
( date '0500-01-01',
time '21:59:59'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE213C VALUES
( date '1800-05-06',
time '12:23:24'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # ** From TestB03 **
    
    stmt = """INSERT INTO BTRE218U 
(D_to_MI, D_to_S, H_to_MI)
VALUES
(interval '23:12:55' day TO MINUTE,
interval '25:14:55:55' DAY TO SECOND,
interval '12:15' hour TO MINUTE);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE218U 
(Y, D, D_to_MI, D_to_S, H_to_MI)
VALUES
(interval '30' year,
interval '20' day,
interval '20:18:00' day TO minute,
interval '24' SECOND(2,0),
interval '12' minute
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE218U 
VALUES
(interval '99' year,
interval '10' month,
interval '10' month,
interval '23' day,
interval '22:13' day TO HOUR,
interval '23:00:00' day to minute,
interval '45' SECOND(2,0),
interval '30' minute);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # ** From TestB04 **
    stmt = """INSERT INTO BTRE218C (D_to_MI, D_to_S_1, H_to_MI)
VALUES (
interval '23:12:55' day TO MINUTE,
interval '25:14:55:55' DAY TO SECOND,
interval '12:15' hour TO MINUTE);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE218C (Y, D, D_to_MI, D_to_S_1, H_to_MI)
VALUES (
interval '30' year,
interval '20' day,
interval '20:18:00' DAY TO MINUTE,
interval '24' day,
interval '12' minute);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE218C VALUES (
interval '99' year,
interval '10' month,
interval '10' month,
interval '23' day,
interval '22:13' day TO HOUR,
interval '23:00:00' day to minute,
interval '45' SECOND(2,0),
interval '30' minute
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # ** From TestB06 **
    
    stmt = """INSERT INTO BTRE217U 
(TM3, DT4, TM4)
VALUES
(time '23:12:45',
date '1985-10-15',
time '12:35:45'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE217U 
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
    
    # ** From TestB07 **
    
    stmt = """INSERT INTO BTRE217C 
(TM3, DT4, TM4_1)
VALUES
(time '23:12:45',
date '1985-10-15',
time '12:35:45'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO BTRE217C 
(DT1_1, TM2_1, TM3, DT4, TM4_1)
VALUES
(date '1948-06-15',
time '23:45:45',
time '15:18:24',
date '1920-05-06',
time '01:10:25'
);"""
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
    #  Test case name:     arkt0151 : testA01
    #  Description:        Create and load data into the table BTRE211U of
    #                      Data type DATETIME. This test case will create
    #                      a table of data type DATETIME with all possible
    #                      start and and date qualifier. this table have 28
    #                      columns. Insert four rows into this table. The last
    #                      row contains Default value for DATETIME. This table
    #                      is created to be used for UNION.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    # 04/13/09 added order by
    stmt = """SELECT Y_TO_D, Y_TO_S, Y_TO_F FROM BTRE211U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    #  expect 4 rows with the following values in any order:
    #  1988-01-01  1988-01-01 12:35:30.000  1988-01-01 12:35:30.333
    #  1900-03-02  1979-06-05 14:40:45.000  1980-07-06 15:45:50.678
    #  0902-09-07  0805-12-10 07:59:03.000  0806-01-11 08:01:04.789
    #  0009-01-01  0001-01-01 00:00:00.000  0001-01-01 00:00:00.000
    
    stmt = """SELECT H_TO_S, H_TO_F FROM BTRE211U;"""
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
    #  Test case name:     arkt0151 : testA02
    #  Description:        Create and load data into the table BTRE211 of
    #                      Data type DATETIME. This test case will create
    #                      a table of data type DATETIME with all possible
    #                      start and and date qualifier. this table have
    #                      28 columns. Insert four rows into this table.
    #                      The last row contains Default value for DATETIME.
    #                      This table is created to be used for UNION with the
    #                      CORRESPONDING option.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT Y_TO_D_1, Y_TO_S, Y_TO_F FROM BTRE211C;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    #  expect 4 rows with the following values in any order:
    #  1988-01-01  1988-01-01 12:35:30.000  1988-01-01 12:35:30.333
    #  1900-03-02  1979-06-05 14:40:45.000  1980-07-06 15:45:50.678
    #  0902-09-07  0805-12-10 07:59:03.000  0806-01-11 08:01:04.789
    #  0009-01-01  0001-01-01 00:00:00.000  0001-01-01 00:00:00.000
    
    stmt = """SELECT H_TO_S, H_TO_F_1 FROM BTRE211C;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    
    _testmgr.testcase_end(desc)

def test004(desc="""a04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0151 : testA04
    #  Description:        This test case will create a table of data
    #                      type INTERVAL with all possible start and
    #                      and date qualifier. this table have 18 columns.
    #                      Insert four rows into this table. The last row
    #                      contains Default value for DATETIME. This table
    #                      is created to be used for UNION operation.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT Y, Y_TO_MO, MO FROM BTRE212U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s0')
    #  expect 4 rows with the following values:
    #  	   10     10-01    1
    #  	 9999   9999-11   11
    #  	    9      9-01    9
    #  	    7      7-01    7
    
    stmt = """SELECT D, D_TO_H, D_TO_MI, D_TO_S, D_TO_F FROM BTRE212U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s1')
    #  expect 4 rows with the following values in any order:
    #      15   15 12   16 13:15   17 14:16:01   18 15:17:02.123
    #      31   30 01   29 02:59   28 03:58:59   27 04:57:58.999
    #       9    1 01    1 01:01    1 01:01:01    1 01:01:01.100
    #       7    0 00    0 00:00    0 00:00:00    0 00:00:00.000
    
    stmt = """SELECT H, H_TO_MI, H_TO_S, H_TO_F FROM BTRE212U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s2')
    #  expect 4 rows with the following values in any order:
    #      16    17:18   18:19:03   19:20:04.345
    #      23    22:56   21:55:57   20:54:56.888
    #       1     1:01    1:01:01    1:01:01.100
    #       0     0:00    0:00:00    0:00:00.000
    
    stmt = """SELECT MI, MI_TO_S, MI_TO_F, S, S_TO_F FROM BTRE212U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s3')
    
    _testmgr.testcase_end(desc)

def test005(desc="""a05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0151 : testA05
    #  Description:        This test case will create a table of data
    #                      type INTERVAL with all possible start and
    #                      and date qualifier. this table have 18 columns.
    #                      Insert four rows into this table. The last row
    #                      contains Default value for INTERVAL. This table
    #                      is created to be used for UNION operation with
    #                      the CORRESPONDING option.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT Y, Y_TO_MO, MO FROM BTRE212C;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    #  expect 4 rows with the following values in any order:
    #          10     10-01    1
    #        9999   9999-11   11
    #           9      9-01    9
    #           7      7-01    7
    
    stmt = """SELECT D, D_TO_H_1, D_TO_MI, D_TO_S, D_TO_F_1 FROM BTRE212C;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
    #  expect 4 rows with the following values in any order:
    #      15   15 12   16 13:15   17 14:16:01   18 15:17:02.123
    #      31   30 01   29 02:59   28 03:58:59   27 04:57:58.999
    #       9    1 01    1 01:01    1 01:01:01    1 01:01:01.100
    #       7    0 00    0 00:00    0 00:00:00    0 00:00:00.000
    
    stmt = """SELECT H, H_TO_MI, H_TO_S, H_TO_F_1 FROM BTRE212C;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    #  expect 4 rows with the following values in any order:
    #      16    17:18   18:19:03   19:20:04.345
    #      23    22:56   21:55:57   20:54:56.888
    #       1     1:01    1:01:01    1:01:01.100
    #       0     0:00    0:00:00    0:00:00.000
    
    stmt = """SELECT MI, MI_TO_S_1, MI_TO_F, S_1, S_TO_F FROM BTRE212C;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
    
    _testmgr.testcase_end(desc)

def test006(desc="""a07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0151 : testA07
    #  Description:        This test case will create a table of data
    #                      type DATE and TIME. It has two columns the
    #                      first one will tests the DATE and the second
    #                      column will test TIME data type. This table
    #                      will be used for UNION operation.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """select * from BTRE213U 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s0')
    #  expect 4 rows with the following values in this order:
    #  	DATE1       TIME1
    #  	----------  --------
    #
    #  	0100-01-01  00:00:00
    #  	0500-01-01  21:59:59
    #  	1800-05-06  12:23:24
    #  	1988-10-25  10:10:10
    
    stmt = """select * from BTRE213U 
order by 2,1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s1')
    
    _testmgr.testcase_end(desc)

def test007(desc="""a08"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0151 : testA08
    #  Description:        This test case will create a table of data
    #                      type DATE and TIME. It has two columns the
    #                      first one will tests the DATE and the second
    #                      column will test TIME data type. This table
    #                      will be used for UNION operation with the
    #                      CORRESPONDING option.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """select * from BTRE213C 
order by 1,2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s0')
    #  expect 4 rows with the following values in this order:
    #  DATE1_1     TIME1
    #  ----------  --------
    #
    #  0100-01-01  00:00:00
    #  0500-01-01  21:59:59
    #  1800-05-06  12:23:24
    #  1988-10-25  10:10:10
    
    stmt = """select * from BTRE213C 
order by 2,1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s1')
    
    _testmgr.testcase_end(desc)

def test008(desc="""b00"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0151 : testB00
    #  Description:        Create and load data into the table BTRE219U of
    #                      Data type DATETIME with DEFAULT, SYSTEM, NULL
    #                      and literal.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """INSERT INTO BTRE219U VALUES (date  '1700-09-24');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """SELECT * FROM BTRE219U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b00exp""", 'b00s0')
    
    _testmgr.testcase_end(desc)

def test009(desc="""b01"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0151 : testB01
    #  Description:        Create and load data into the table BTRE219C of
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
    
    stmt = """INSERT INTO BTRE219C VALUES ( date '1700-09-24');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """SELECT * FROM BTRE219C;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b01exp""", 'b01s0')
    
    _testmgr.testcase_end(desc)

def test010(desc="""b03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0151 : testB03
    #  Description:        This test case will create a table of data
    #                      type INTERVAL with all possible DEFAULT,
    #                      SYSTEM, NULL and literal column. It will be
    #                      populated with all possible combination of data.
    #                      This table will be used for UNION operation.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT Y, Y_TO_MO, MO, D FROM BTRE218U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b03exp""", 'b03s0')
    #  expect 3 rows with the following values in any order:
    #       Y    Y_TO_MO  MO  D
    #       ---  -------  --  ---
    #
    #         1     0-00   ?   15
    #        30     0-00   ?   20
    #        99     0-10  10   23
    
    stmt = """SELECT D_TO_H, D_TO_MI, D_TO_S, H_TO_MI FROM BTRE218U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b03exp""", 'b03s1')
    
    _testmgr.testcase_end(desc)

def test011(desc="""b04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0151 : testB04
    #  Description:        This test case will create a table of data
    #                      type INTERVAL with all possible DEFAULT,
    #                      SYSTEM, NULL and literal column. It will be
    #                      populated with all possible combination of data.
    #                      This table will be used for UNION operation with
    #                      the CORRESPONDING option.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT Y, Y_TO_MO, MO_1, D FROM BTRE218C;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b04exp""", 'b04s0')
    #  expect 3 rows with the following values in any order:
    #  	Y    Y_TO_MO  MO_1  D
    #  	---  -------  ----  ---
    #
    #  	  1     0-00     ?   15
    #  	 30     0-00     ?   20
    #  	 99     0-10    10   23
    
    stmt = """SELECT D_TO_H_1, D_TO_MI, D_TO_S_1, H_TO_MI FROM BTRE218C;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b04exp""", 'b04s1')
    
    _testmgr.testcase_end(desc)

def test012(desc="""b06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0151 : testB06
    #  Description:        Create and load data into the table BTRE217U of
    #                      Data type DATE and TIME with DEFAULT, SYSTEM,
    #                      NULL and literal columns.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT DT1, TM1, DT2, TM2 FROM BTRE217U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b06exp""", 'b06s0')
    #  expect 2 rows with the following values in any order:
    #  	DT1         TM1       DT2         TM2
    #  	----------  --------  ----------  --------
    #
    #  	1987-05-15         ?           ?  18:35:35
    #  	1948-06-15         ?           ?  23:45:45
    
    stmt = """SELECT DT3, TM3, DT4, TM4 FROM BTRE217U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b06exp""", 'b06s1')
    
    _testmgr.testcase_end(desc)

def test013(desc="""b07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0151 : testB07
    #  Description:        Create and load data into the table BTRE217C of
    #                      Data type DATE and TIME with DEFAULT, SYSTEM,
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
    
    stmt = """SELECT DT1_1, TM1, DT2, TM2_1 FROM BTRE217C;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b07exp""", 'b07s0')
    #  expect 2 rows with the following values in any order:
    #     DT1_1       TM1       DT2         TM2_1
    #     ----------  --------  ----------  --------
    #
    #     1987-06-15         ?           ?  18:35:35
    #     1948-06-15         ?           ?  23:45:45
    
    stmt = """SELECT DT3, TM3, DT4, TM4_1 FROM BTRE217C;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b07exp""", 'b07s1')
    
    _testmgr.testcase_end(desc)

def test014(desc="""b08"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0151 : testB08
    #  Description:        Perform UNION operation on a table with data
    #                      type DATETIME.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test depends on the successful completion of testA01 and testA02
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT * FROM BTRE211C;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b08exp""", 'b08s0')
    #  expect 4 rows with the following values in any order:
    #  Y_TO_D_1    Y_TO_S                   Y_TO_F                   H_TO_S    H_TO_F_1
    #  ----------  -----------------------  -----------------------  --------  ------------
    #
    #  1988-01-01  1988-01-01 12:35:30.000000  1988-01-01 12:35:30.333  10:15:30  10:15:30.555
    #  1900-03-02  1979-06-05 14:40:45.000000  1980-07-06 15:45:50.678  03:53:56  04:54:57.345
    #  0902-09-07  0805-12-10 07:59:03.000000  0806-01-11 08:01:04.789  18:08:09  19:09:10.234
    #  0009-01-01  0001-01-01 00:00:00.000000  0001-01-01 00:00:00.000  00:00:00  00:00:00.000
    
    stmt = """SELECT * FROM BTRE211U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b08exp""", 'b08s1')
    #  expect 4 rows with the same values as above in any order.
    
    #  Note: UNION eliminates duplicate rows, UNION ALL includes duplicates
    
    stmt = """SELECT * FROM BTRE211C 
UNION
SELECT * FROM BTRE211U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b08exp""", 'b08s2')
    #  expect 4 rows with the same values as above in any order.
    
    stmt = """SELECT * FROM BTRE211C 
UNION ALL
SELECT * FROM BTRE211U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b08exp""", 'b08s3')
    #  expect 8 rows with 2x the same values as above in any order.
    
    stmt = """SELECT Y_to_S FROM BTRE211C 
UNION
SELECT Y_to_S FROM BTRE211U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b08exp""", 'b08s4')
    #  expect 4 rows with the following values in any order:
    #  	1988-01-01 12:35:30.000000
    #  	1979-06-05 14:40:45.000000
    #  	0805-12-10 07:59:03.000000
    #  	0001-01-01 00:00:00.000000
    
    stmt = """SELECT Y_to_S FROM BTRE211C 
UNION ALL
SELECT Y_to_S FROM BTRE211U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b08exp""", 'b08s5')
    #  expect 8 rows with 2x the same values as above in any order.
    
    #  DANGER
    #
    #  the ORDER BY in this next query gets into an infinite loop
    stmt = """SELECT y_to_s, Y_to_D_1 FROM BTRE211C 
UNION
SELECT y_to_s, Y_to_D FROM BTRE211U 
--  ORDER BY 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b08exp""", 'b08s6')
    
    #  expect 4 rows with the following values in this order:
    #  	Y_TO_S                   Y_TO_D_1
    #  	-----------------------  ----------
    #
    #  	0001-01-01 00:00:00.000000  0009-01-01
    #  	0805-12-10 07:59:03.000000  0902-09-07
    #  	1979-06-05 14:40:45.000000  1900-03-02
    #  	1988-01-01 12:35:30.000000  1988-01-01
    
    stmt = """SELECT Y_to_F FROM BTRE211C 
UNION ALL
SELECT Y_to_F FROM BTRE211U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b08exp""", 'b08s7')
    #  expect 8 rows with the following values in any order:
    #  	1988-01-01 12:35:30.333
    #  	1980-07-06 15:45:50.678
    #  	0806-01-11 08:01:04.789
    #  	0001-01-01 00:00:00.000
    #  	1988-01-01 12:35:30.333
    #  	1980-07-06 15:45:50.678
    #  	0806-01-11 08:01:04.789
    #  	0001-01-01 00:00:00.000
    
    stmt = """SELECT Y_to_F
FROM BTRE211C 
UNION ALL
SELECT Y_to_F FROM BTRE211U 
ORDER BY 1 DESC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b08exp""", 'b08s8')
    
    _testmgr.testcase_end(desc)

def test015(desc="""b08b"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0151 : testB08b
    #  Description:        Perform UNION operation on a table with data
    #                      type DATETIME.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test depends on the successful completion of testA04 and testA05
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT Y FROM BTRE212C 
UNION
SELECT Y FROM BTRE212U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b08bexp""", 'b08bs0')
    #  expect 4 rows with the following values in any order:
    #  	    7
    #  	    9
    #  	   10
    #  	 9999
    
    stmt = """SELECT Y FROM BTRE212C 
UNION ALL
SELECT Y FROM BTRE212U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b08bexp""", 'b08bs1')
    #  expect 8 rows with 2x the same values as above in any order.
    
    stmt = """SELECT H_to_F_1 FROM BTRE212C 
UNION
SELECT D_to_F FROM BTRE212U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b08bexp""", 'b08bs2')
    #  expect 7 rows with the following values in any order:
    #  	  1 01:01:01.100
    #  	  0 00:00:00.000
    #  	  0 20:54:56.888
    #  	 18 15:17:02.123
    #  	 27 04:57:58.999
    #  	  0 19:20:04.345
    #  	  0 01:01:01.100
    
    stmt = """SELECT H_to_F_1 FROM BTRE212C 
UNION ALL
SELECT D_to_F FROM BTRE212U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b08bexp""", 'b08bs3')
    #  expect 8 rows with the following values in any order:
    #  	  0 19:20:04.345
    #  	  0 20:54:56.888
    #  	  0 01:01:01.100
    #  	  0 00:00:00.000
    #  	 18 15:17:02.123
    #  	 27 04:57:58.999
    #  	  1 01:01:01.100
    #  	  0 00:00:00.000
    
    stmt = """SELECT MI_to_F FROM BTRE212C 
UNION
SELECT D_to_F FROM BTRE212U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b08bexp""", 'b08bs4')
    #  expect 7 rows with the following values in any order:
    #       1 01:01:01.100
    #       0 00:00:00.000
    #       0 00:01:01.100
    #      18 15:17:02.123
    #      27 04:57:58.999
    #       0 00:57:58.777
    #       0 00:22:06.444
    
    stmt = """SELECT MI_to_F FROM BTRE212C 
UNION ALL
SELECT D_to_F FROM BTRE212U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b08bexp""", 'b08bs5')
    #  expect 8 rows with the following values in any order:
    #  	  0 00:22:06.444
    #  	  0 00:57:58.777
    #  	  0 00:01:01.100
    #  	  0 00:00:00.000
    #  	 18 15:17:02.123
    #  	 27 04:57:58.999
    #  	  1 01:01:01.100
    #  	  0 00:00:00.000
    
    stmt = """SELECT D_to_H_1 FROM BTRE212C 
UNION
SELECT H_to_F FROM BTRE212U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b08bexp""", 'b08bs6')
    #  expect 7 rows with the following values in any order:
    #  	  0 00:00:00.000
    #  	  0 20:54:56.888
    #  	  1 01:00:00.000
    #  	  0 19:20:04.345
    #  	  0 01:01:01.100
    #  	 15 12:00:00.000
    #  	 30 01:00:00.000
    
    stmt = """SELECT D_to_H_1 FROM BTRE212C 
UNION ALL
SELECT H_to_F FROM BTRE212U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b08bexp""", 'b08bs7')
    #  expect 8 rows with the following values in any order:
    #  	 15 12:00:00.000
    #  	 30 01:00:00.000
    #  	  1 01:00:00.000
    #  	  0 00:00:00.000
    #  	  0 19:20:04.345
    #  	  0 20:54:56.888
    #  	  0 01:01:01.100
    #  	  0 00:00:00.000
    
    stmt = """SELECT Y, D, H, Mi, S_1 FROM BTRE212C 
UNION ALL
SELECT Y, D, H, Mi, S FROM BTRE212U 
ORDER BY 1, 2, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b08bexp""", 'b08bs8')
    
    _testmgr.testcase_end(desc)

def test016(desc="""b08c"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0151 : testB08c
    #  Description:        Perform UNION operation on a table with data
    #                      type DATETIME.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test depends on the successful completion of testA01 and testA02
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT BTRE211C.Y_to_F, BTRE212C.D_to_F_1, BTRE212C.D_to_H_1
FROM BTRE211C, BTRE212C 
UNION ALL
SELECT BTRE211U.Y_to_F, BTRE212U.D_to_F, BTRE212U.D_to_H
FROM BTRE211U, BTRE212U 
ORDER BY 1, 2 DESC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b08cexp""", 'b08cs0')
    #  expect 32 rows with 8 each of the following values in this order:
    #  	0001-01-01 00:00:00.000
    #  	0806-01-11 08:01:04.789
    #  	1980-07-06 15:45:50.678
    #  	1988-01-01 12:35:30.333
    #  and each group of 8 accompanied by the following values in this order:
    #  	27 04:57:58.999     30 01
    #  	27 04:57:58.999     30 01
    #  	18 15:17:02.123     15 12
    #  	18 15:17:02.123     15 12
    #  	1 01:01:01.100      1 01
    #  	1 01:01:01.100      1 01
    #  	0 00:00:00.000      0 00
    #  	0 00:00:00.000      0 00
    
    stmt = """SELECT BTRE211C.Y_to_F, BTRE212C.D_to_F_1, BTRE212C.D_to_H_1
FROM BTRE211C, BTRE212C 
UNION ALL
SELECT BTRE211U.Y_to_F, BTRE212U.D_to_F, BTRE212U.D_to_H
FROM BTRE211U, BTRE212U 
ORDER BY 1 ASC, 2 DESC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b08cexp""", 'b08cs1')
    #  expect 32 rows with the same values as above but in reversed order:
    
    stmt = """SELECT BTRE211C.Y_to_F, BTRE212C.D_to_F_1
FROM BTRE211C, BTRE212C 
UNION ALL
SELECT BTRE211U.Y_to_F, BTRE212U.D_to_F
FROM BTRE211U, BTRE212U 
ORDER BY BTRE212C.D_to_F_1 ASC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b08cexp""", 'b08cs2')
    #  expect 32 rows with 8 each of the following values in this order
    #  for the column D_TO_F_1:
    #  	 0 00:00:00.000
    #  	 1 01:01:01.100
    #  	18 15:17:02.123
    #  	27 04:57:58.999
    #  each group of 8 should be accompanied by 2 sets of the following:
    #  	1988-01-01 12:35:30.333
    #  	1980-07-06 15:45:50.678
    #  	0806-01-11 08:01:04.789
    #  	0001-01-01 00:00:00.000
    
    stmt = """SELECT Y, MO, D, H, MI, S_1, S_to_F FROM BTRE212C 
UNION ALL
SELECT Y, MO, D, H, MI, S, S_to_F FROM BTRE212U ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b08cexp""", 'b08cs3')
    #  expect 8 rows with the following values in any order:
    #  	Y      MO   D    H    MI   S_1  S_TO_F
    #  	-----  ---  ---  ---  ---  ---  -------
    #
    #  	   10    1   15   16   21    7    8.555
    #  	 9999   11   31   23   59   59   58.666
    #  	    9    9    9    1    1    1    1.100
    #  	    7    7    7    0    0    0    0.000
    #  	   10    1   15   16   21    7    8.555
    #  	 9999   11   31   23   59   59   58.666
    #  	    9    9    9    1    1    1    1.100
    #  	    7    7    7    0    0    0    0.000
    
    stmt = """SELECT Y, MO, D, H, MI, S_1, S_to_F FROM BTRE212C 
UNION ALL
SELECT Y, MO, D, H, MI, S, S_to_F FROM BTRE212U 
ORDER BY Y DESC, D DESC, S_1 DESC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b08cexp""", 'b08cs4')
    
    _testmgr.testcase_end(desc)

def test017(desc="""b09"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0151 : testB09
    #  Description:        Perform UNION operations on a table with the data
    #                      type INTERVAL.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT Y, Y_TO_MO, MO FROM BTRE212C 
UNION
SELECT Y, Y_TO_MO, MO FROM BTRE212U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b09exp""", 'b09s0')
    #  expect 4 rows with the following values in any order:
    #  	    9      9-01    9
    #  	   10     10-01    1
    #  	 9999   9999-11   11
    #  	    7      7-01    7
    
    stmt = """SELECT Y, Y_TO_MO, MO FROM BTRE212C 
UNION ALL
SELECT Y, Y_TO_MO, MO FROM BTRE212U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b09exp""", 'b09s1')
    #  expect 8 rows with 2x the preceding values in any order:
    
    stmt = """SELECT D, D_TO_H_1, D_TO_MI, D_TO_S, D_TO_F_1 FROM BTRE212C 
UNION
SELECT D, D_TO_H, D_TO_MI, D_TO_S, D_TO_F FROM BTRE212U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b09exp""", 'b09s2')
    #  expect 4 rows with the following values in any order:
    #      15     15 12   16 13:15   17 14:16:01   18 15:17:02.123
    #       7      0 00    0 00:00    0 00:00:00    0 00:00:00.000
    #       9      1 01    1 01:01    1 01:01:01    1 01:01:01.100
    #      31     30 01   29 02:59   28 03:58:59   27 04:57:58.999
    
    stmt = """SELECT D, D_TO_H_1, D_TO_MI, D_TO_S, D_TO_F_1 FROM BTRE212C 
UNION ALL
SELECT D, D_TO_H, D_TO_MI, D_TO_S, D_TO_F FROM BTRE212U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b09exp""", 'b09s3')
    #  expect 8 rows with 2x the preceding values in any order:
    
    stmt = """SELECT H, H_TO_MI, H_TO_S, H_TO_F_1 FROM BTRE212C 
UNION
SELECT H, H_TO_MI, H_TO_S, H_TO_F FROM BTRE212U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b09exp""", 'b09s4')
    #  expect 4 rows with the following values in any order:
    #  	  0     0:00    0:00:00    0:00:00.000
    #  	  1     1:01    1:01:01    1:01:01.100
    #  	 23    22:56   21:55:57   20:54:56.888
    #  	 16    17:18   18:19:03   19:20:04.345
    
    stmt = """SELECT H, H_TO_MI, H_TO_S, H_TO_F_1 FROM BTRE212C 
UNION ALL
SELECT H, H_TO_MI, H_TO_S, H_TO_F FROM BTRE212U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b09exp""", 'b09s5')
    #  expect 8 rows with 2x the preceding values in any order:
    
    stmt = """SELECT MI, MI_TO_S_1, MI_TO_F, S_1, S_TO_F FROM BTRE212C 
UNION
SELECT MI, MI_TO_S, MI_TO_F, S, S_TO_F FROM BTRE212U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b09exp""", 'b09s6')
    #  expect 4 rows with the following values in any order:
    #       0       0:00    0:00.000    0    0.000
    #      59      58:59   57:58.777   59   58.666
    #       1       1:01    1:01.100    1    1.100
    #      21      21:05   22:06.444    7    8.555
    
    stmt = """SELECT MI, MI_TO_S_1, MI_TO_F, S_1, S_TO_F FROM BTRE212C 
UNION ALL
SELECT MI, MI_TO_S, MI_TO_F, S, S_TO_F FROM BTRE212U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b09exp""", 'b09s7')
    #  expect 8 rows with 2x the preceding values in any order:
    
    stmt = """SELECT D_to_S FROM BTRE212C 
UNION
SELECT D_to_S FROM BTRE212U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b09exp""", 'b09s8')
    #  expect 4 rows with the following values in any order:
    #       0 00:00:00
    #      17 14:16:01
    #       1 01:01:01
    #      28 03:58:59
    
    stmt = """SELECT Y FROM BTRE212C 
UNION ALL
SELECT Y FROM BTRE212U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b09exp""", 'b09s9')
    #  expect 8 rows with 2x the following values in any order:
    #        10
    #      9999
    #         9
    #         7
    
    stmt = """SELECT D_to_MI FROM BTRE212C 
UNION
SELECT D_to_F FROM BTRE212U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b09exp""", 'b09s10')
    #  expect 7 rows with the following values in any order:
    #       1 01:01:01.100
    #       0 00:00:00.000
    #      29 02:59:00.000
    #       1 01:01:00.000
    #      18 15:17:02.123
    #      27 04:57:58.999
    #      16 13:15:00.000
    
    stmt = """SELECT D_to_MI  FROM BTRE212C 
UNION ALL
SELECT D_to_F FROM BTRE212U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b09exp""", 'b09s11')
    #  expect 8 rows with the following values in any order:
    #      16 13:15:00.000
    #      29 02:59:00.000
    #       1 01:01:00.000
    #       0 00:00:00.000
    #      18 15:17:02.123
    #      27 04:57:58.999
    #       1 01:01:01.100
    #       0 00:00:00.000
    
    #  this one gets a wierd answer		XXXXXXXX
    #  SELECT MI_to_F FROM BTRE212C
    #                 UNION
    #  SELECT D_to_S FROM BTRE212U;
    
    stmt = """SELECT MI_to_F FROM BTRE212C 
UNION
SELECT D_to_F FROM BTRE212U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b09exp""", 'b09s12')
    #  expect 7 rows with the following values in any order:
    #       1 01:01:01.100
    #       0 00:00:00.000
    #       0 00:01:01.100
    #      18 15:17:02.123
    #      27 04:57:58.999
    #       0 00:57:58.777
    #       0 00:22:06.444
    
    stmt = """SELECT MI_to_F FROM BTRE212C 
UNION ALL
SELECT D_to_F FROM BTRE212U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b09exp""", 'b09s13')
    #  expect 8 rows with the following values in any order:
    #       0 00:22:06.444
    #       0 00:57:58.777
    #       0 00:01:01.100
    #       0 00:00:00.000
    #      18 15:17:02.123
    #      27 04:57:58.999
    #       1 01:01:01.100
    #       0 00:00:00.000
    
    stmt = """SELECT MI_to_S_1 FROM BTRE212C 
UNION
SELECT D_to_F FROM BTRE212U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b09exp""", 'b09s14')
    
    _testmgr.testcase_end(desc)

def test018(desc="""b09b"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0151 : testB09b
    #  Description:        Perform UNION operations on a table with the data
    #                      type INTERVAL.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  These tests depend on successful completion of testA01 and testA02
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT Y, Y_to_MO, D_to_MI FROM BTRE212C 
UNION
SELECT Y, Y_to_MO, D_to_MI FROM BTRE212U 
ORDER BY 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b09bexp""", 'b09bs0')
    #  expect 4 rows with the following values in this order:
    #  	    7      7-01    0 00:00
    #  	    9      9-01    1 01:01
    #  	   10     10-01   16 13:15
    #  	 9999   9999-11   29 02:59
    
    stmt = """SELECT Y, D, H, MI FROM BTRE212C 
UNION ALL
SELECT Y, D, H, MI FROM BTRE212U 
ORDER BY 1, 2, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b09bexp""", 'b09bs1')
    #  expect 8 rows with 2 each of the following values in this order:
    #  	    7      7-01    0 00:00
    #  	    9      9-01    1 01:01
    #  	   10     10-01   16 13:15
    #  	 9999   9999-11   29 02:59
    #  	    7    7    0    0
    #  	    9    9    1    1
    #  	   10   15   16   21
    #  	 9999   31   23   59
    
    stmt = """SELECT Y_to_MO, D_to_MI, D_to_S FROM BTRE212C 
UNION ALL
SELECT Y_to_MO, D_to_MI, D_to_S FROM BTRE212U 
ORDER BY 1 ASC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b09bexp""", 'b09bs2')
    #  expect 8 rows with 2 each of the following values in this order:
    #  	    7-01    0 00:00    0 00:00:00
    #  	    9-01    1 01:01    1 01:01:01
    #  	   10-01   16 13:15   17 14:16:01
    #  	 9999-11   29 02:59   28 03:58:59
    
    stmt = """SELECT D_to_F_1, MI_to_F, D_to_S, D_to_H_1 FROM BTRE212C 
UNION ALL
SELECT D_to_F, MI_to_F, D_to_S, D_to_H FROM BTRE212U 
ORDER BY 1, 2 DESC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b09bexp""", 'b09bs3')
    #  expect 8 rows with 2 each of the following values in this order:
    #  	D_TO_F_1          MI_TO_F     D_TO_S        D_TO_H_1
    #  	----------------  ----------  ------------  --------
    #
    #  	  0 00:00:00.000    0:00.000    0 00:00:00      0 00
    #  	  1 01:01:01.100    1:01.100    1 01:01:01      1 01
    #  	 18 15:17:02.123   22:06.444   17 14:16:01     15 12
    #  	 27 04:57:58.999   57:58.777   28 03:58:59     30 01
    
    stmt = """SELECT D_to_F_1, MI_to_F, D_to_F_1 FROM BTRE212C 
UNION ALL
SELECT D_to_F, MI_to_F, D_to_F FROM BTRE212U 
ORDER BY 1 ASC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b09bexp""", 'b09bs4')
    #  expect 8 rows with 2 each of the following values in this order:
    #  	D_TO_F_1          MI_TO_F     D_TO_F_1
    #  	----------------  ----------  ----------------
    #
    #  	  0 00:00:00.000    0:00.000    0 00:00:00.000
    #  	  1 01:01:01.100    1:01.100    1 01:01:01.100
    #  	 18 15:17:02.123   22:06.444   18 15:17:02.123
    #  	 27 04:57:58.999   57:58.777   27 04:57:58.999
    
    #  Added 18 Jan 90 because of C30G Window 1 error, perhaps related
    #  to order by:
    stmt = """SELECT Y, MO, D, H, MI FROM BTRE212C 
UNION ALL
SELECT Y, MO, D, H, MI FROM BTRE212U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b09bexp""", 'b09bs5')
    #  expect 8 rows with 2 each of the following values in any order:
    #  	   10    1   15   16   21
    #  	 9999   11   31   23   59
    #  	    9    9    9    1    1
    #  	    7    7    7    0    0
    
    stmt = """SELECT Y, MO, D, H, MI FROM BTRE212C 
UNION ALL
SELECT Y, MO, D, H, MI FROM BTRE212U 
ORDER BY Y, D DESC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b09bexp""", 'b09bs6')
    
    _testmgr.testcase_end(desc)

def test019(desc="""b09c"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0151 : testB09c
    #  Description:        Perform UNION operations on a table with the data
    #                      type INTERVAL.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  These tests depend on successful completion of testB03 and testB04
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT * FROM BTRE218C 
UNION
SELECT * FROM BTRE218U 
ORDER BY 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b09cexp""", 'b09cs0')
    #  expect 3 rows with the following values in this order;
    #  	Y    Y_TO_MO  MO   D    D_TO_H  D_TO_MI    D_TO_S        H_TO_MI
    #  	---  -------  ---  ---  ------  ---------  ------------  -------
    #
    #  	  1     0-00    ?   15    0 00   23 12:55   25 14:55:55    12:15
    #  	 30     0-00    ?   20    0 00   20 18:00   24 00:00:00     0:12
    #  	 30     0-00    ?   20    0 00   20 18:00    0 00:00:24     0:12
    #  	 99     0-10   10   23   22 13   23 00:00    0 00:00:45     0:30
    
    stmt = """SELECT Y_to_MO FROM BTRE218C 
UNION ALL
SELECT Y_to_MO FROM BTRE218U 
ORDER BY 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b09cexp""", 'b09cs1')
    
    _testmgr.testcase_end(desc)

def test020(desc="""c00"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0151 : testC00
    #  Description:        Perform    UNION operations on a table with the
    #                      data type DATE and TIME.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test relies on successful completion of testA07 and testA08
    #
    # =================== End Test Case Header  ===================
    
    #  the ORDER BY in this query causes an infinite loop XXXXX
    stmt = """SELECT * FROM BTRE213C 
UNION
SELECT * FROM BTRE213U 
ORDER BY 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c00exp""", 'c00s0')
    #  expect 4 rows with the following values in this order:
    #  	0100-01-01  00:00:00
    #  	0500-01-01  21:59:59
    #  	1800-05-06  12:23:24
    #  	1988-10-25  10:10:10
    
    stmt = """SELECT * FROM BTRE213C 
UNION ALL
SELECT * FROM BTRE213U 
ORDER BY 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c00exp""", 'c00s1')
    #  expect 8 rows: the same 4 rows as above, each doubled in that order.
    
    #  the order by in this query causes an infinite loop XXXXX
    stmt = """SELECT DATE1_1  FROM BTRE213C 
UNION
SELECT DATE1  FROM BTRE213U 
ORDER BY 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c00exp""", 'c00s2')
    #  expect 4 rows with the following values in this order:
    #     0100-01-01
    #     0500-01-01
    #     1800-05-06
    #     1988-10-25
    
    #  the order by in this query causes an infinite loop XXXXX
    stmt = """SELECT DATE1_1 FROM BTRE213C 
UNION ALL
SELECT DATE1 FROM BTRE213U 
ORDER BY 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c00exp""", 'c00s3')
    #  expect 8 rows: the same 4 rows as above, each doubled in that order.
    
    #  the order by in this query causes an infinite loop XXXXX
    stmt = """SELECT TIME1 FROM BTRE213C 
UNION
SELECT TIME1 FROM BTRE213U 
ORDER BY 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c00exp""", 'c00s4')
    #  expect 4 rows with the following values in this order:
    #     00:00:00
    #     10:10:10
    #     12:23:24
    #     21:59:59
    
    stmt = """SELECT TIME1 FROM BTRE213C 
UNION ALL
SELECT TIME1 FROM BTRE213U 
ORDER BY 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c00exp""", 'c00s5')
    #  expect 8 rows: the same 4 rows as above, each doubled in that order.
    
    #  the order by in this query causes an infinite loop XXXXX
    stmt = """SELECT DATE1_1, TIME1 FROM BTRE213C 
UNION
SELECT DATE1, TIME1 FROM BTRE213U 
ORDER BY 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c00exp""", 'c00s6')
    #  expect 8 rows with 2 each of the following values in this order:
    #  	0100-01-01  00:00:00
    #  	0500-01-01  21:59:59
    #  	1800-05-06  12:23:24
    #  	1988-10-25  10:10:10
    
    stmt = """SELECT DATE1_1, TIME1 FROM BTRE213C 
UNION ALL
SELECT DATE1, TIME1 FROM BTRE213U 
ORDER BY 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c00exp""", 'c00s7')
    #  expect the same 8 rows as above.
    
    stmt = """SELECT DATE1_1, TIME1 FROM BTRE213C 
UNION ALL
SELECT DATE1, TIME1 FROM BTRE213U 
ORDER BY 1 ASC, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c00exp""", 'c00s8')
    #  expect the same 8 rows as above.
    
    stmt = """SELECT DATE1_1, TIME1 FROM BTRE213C 
UNION ALL
SELECT DATE1, TIME1 FROM BTRE213U 
ORDER BY 1, 2 DESC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c00exp""", 'c00s9')
    #  expect the same 8 rows as above.
    
    stmt = """SELECT DATE1_1, TIME1 FROM BTRE213C 
UNION ALL
SELECT DATE1, TIME1 FROM BTRE213U 
ORDER BY DATE1_1  ASC, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c00exp""", 'c00s10')
    
    _testmgr.testcase_end(desc)

def test021(desc="""c00b"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0151 : testC00b
    #  Description:        Perform    UNION operations on a table with the
    #                      data type DATE and TIME.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test relies on successful completion of testB06 and testB07
    #
    # =================== End Test Case Header  ===================
    
    #  the order by in this query causes an infinite loop XXXXX
    stmt = """SELECT DT1_1, TM1, DT2, TM2_1 FROM BTRE217C 
UNION
SELECT DT1, TM1, DT2, TM2 FROM BTRE217U 
ORDER BY 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c00bexp""", 'c00bs0')
    #  expect 2 rows with the following values in this order:
    #  	DT1_1       TM1       DT2         TM2_1
    #  	----------  --------  ----------  --------
    
    #  	1948-06-15         ?           ?  23:45:45
    #  		 ?         ?           ?         ?
    
    #  the order by in this query causes an infinite loop XXXXX
    stmt = """SELECT DT3, TM3, DT4, TM4_1 FROM BTRE217C 
UNION
SELECT DT3, TM3, DT4, TM4 FROM BTRE217U 
ORDER BY 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c00bexp""", 'c00bs1')
    #  expect 2 rows with the following values in this order:
    # 	DT3         TM3       DT4         TM4
    # 	----------  --------  ----------  --------
    #
    # 	         ?  23:12:45  1985-10-15  12:35:45
    # 	         ?  15:18:24  1920-05-06  01:10:25
    
    stmt = """SELECT DT2    FROM BTRE217C 
UNION ALL
SELECT DT2    FROM BTRE217U 
ORDER BY 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c00bexp""", 'c00bs2')
    
    _testmgr.testcase_end(desc)

def test022(desc="""c01"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0151 : testC01
    #  Description:        Perform JOIN operation on a table with the data
    #                      types DATE and TIME.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  These tests depend on successful completion of testA01, testA02,
    #		testA04, testA05, testB00 and testB01
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT  Y_to_D_1 FROM BTRE211C ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c01exp""", 'c01s0')
    #  expect 4 rows with the following values in any order:
    #  	1988-01-01
    #  	1900-03-02
    #  	0902-09-07
    #  	0009-01-01
    
    stmt = """SELECT  Y_to_D FROM  BTRE211U ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c01exp""", 'c01s1')
    #  expect the same 4 rows as above in any order:
    
    stmt = """SELECT BTRE212C.Y, BTRE212U.Y
FROM         BTRE212C 
INNER JOIN   BTRE212U 
ON BTRE212C.Y = BTRE212U.Y
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c01exp""", 'c01s2')
    #  expect 4 rows with the following values in any order:
    #  	   10     10
    #  	 9999   9999
    #  	    9      9
    #  	    7      7
    
    stmt = """SELECT a.Y_to_MO, b.Y_to_MO
FROM         BTRE212C a
INNER JOIN   BTRE212U b
ON a.Y_to_MO = b.Y_to_MO
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c01exp""", 'c01s3')
    #  expect 4 rows with the following values in any order:
    #  	   10-01     10-01
    #  	 9999-11   9999-11
    #  	    9-01      9-01
    #  	    7-01      7-01
    
    stmt = """SELECT a.Y_to_MO, b.Y_to_MO
FROM         BTRE212C a
LEFT JOIN    BTRE212U b
ON a.Y_to_MO = b.Y_to_MO
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c01exp""", 'c01s4')
    #  expect the same 4 rows as above in any order:
    
    stmt = """SELECT a.Y_to_MO, b.Y_to_MO
FROM         BTRE212C a
RIGHT JOIN  BTRE212U b
ON a.Y_to_MO = b.Y_to_MO
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c01exp""", 'c01s5')
    #  expect the same 4 rows as above in any order:
    
    stmt = """SELECT a.Y_to_D_1, b.Y_to_D
FROM         BTRE219C a
INNER JOIN   BTRE219U b
ON a.Y_to_D_1 = b.Y_to_D
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c01exp""", 'c01s6')
    #  expect 1 row with the following values:
    #  	1700-09-24  1700-09-24
    
    stmt = """SELECT a.Y_to_D_1, b.Y_to_D
FROM         BTRE219C a
LEFT JOIN    BTRE219U b
ON a.Y_to_D_1 = b.Y_to_D
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c01exp""", 'c01s7')
    #  expect 1 row with the following values:
    #  	1700-09-24           ?
    
    stmt = """SELECT a.Y_to_D_1, b.Y_to_D
FROM         BTRE219C a
RIGHT JOIN   BTRE219U b
ON a.Y_to_D_1 = b.Y_to_D
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c01exp""", 'c01s8')
    #  expect 1 row with the following values:
    #           ?  1700-09-24
    
    stmt = """SELECT a.Y, a.Y_TO_MO
, b.Y, b.Y_TO_MO FROM BTRE212C a
INNER JOIN BTRE212U b
ON a.Y = b.Y
ORDER BY 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c01exp""", 'c01s9')
    #  expect 4 rows with the following values in this order:
    #  	    7      7-01      7      7-01
    #  	    9      9-01      9      9-01
    #  	   10     10-01     10     10-01
    #  	 9999   9999-11   9999   9999-11
    
    stmt = """SELECT a.Y, a.Y_TO_MO
, b.Y, b.Y_TO_MO FROM BTRE212C a
LEFT  JOIN BTRE212U b
ON a.Y = b.Y
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c01exp""", 'c01s10')
    #  expect 4 rows with the following values in any order:
    #        10     10-01     10     10-01
    #      9999   9999-11   9999   9999-11
    #         9      9-01      9      9-01
    #         7      7-01      7      7-01
    
    stmt = """SELECT a.Y, a.Y_TO_MO
, b.Y, b.Y_TO_MO FROM BTRE212C a
LEFT  JOIN BTRE212U b
ON a.Y = b.Y
ORDER BY 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c01exp""", 'c01s11')
    #  expect 4 rows with the following values in this order:
    #  	    7      7-01      7      7-01
    #  	    9      9-01      9      9-01
    #  	   10     10-01     10     10-01
    #  	 9999   9999-11   9999   9999-11
    
    stmt = """SELECT a.Y, a.Y_TO_MO
, b.Y, b.Y_TO_MO FROM BTRE212C a
LEFT  JOIN BTRE212U b
ON a.Y = b.Y
ORDER BY 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c01exp""", 'c01s12')
    #  expect the same 4 rows as above in that order:
    
    stmt = """SELECT a.Y, a.Y_TO_MO
, b.Y, b.Y_TO_MO FROM BTRE212C a
RIGHT JOIN BTRE212U b
ON a.Y = b.Y
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c01exp""", 'c01s13')
    
    _testmgr.testcase_end(desc)

def test023(desc="""c02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0151 : testC02
    #  Description:        This testcase tests the JOIN  operation on a
    #                      table with the data type INTERVAL.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  These tests depend on successful completion of testA04 and test A05
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT BTRE212C.Y, BTRE212U.Y
FROM         BTRE212C 
INNER JOIN   BTRE212U 
ON BTRE212C.Y = BTRE212U.Y
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c02exp""", 'c02s0')
    #  expect 4 rows with the following values in any order:
    #  	   10     10
    #  	 9999   9999
    #  	    9      9
    #  	    7      7
    
    stmt = """SELECT a.Y_to_MO, b.Y_to_MO
FROM         BTRE212C a
INNER JOIN   BTRE212U b
ON a.Y_to_MO = b.Y_to_MO
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c02exp""", 'c02s1')
    #  expect 4 rows with the following values in any order:
    #        10-01     10-01
    #      9999-11   9999-11
    #         9-01      9-01
    #         7-01      7-01
    
    stmt = """SELECT a.Y_to_MO, b.Y_to_MO
FROM         BTRE212C a
LEFT JOIN    BTRE212U b
ON a.Y_to_MO = b.Y_to_MO
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c02exp""", 'c02s2')
    #  expect the same 4 rows as above in any order:
    
    stmt = """SELECT a.Y_to_MO, b.Y_to_MO
FROM         BTRE212C a
RIGHT JOIN  BTRE212U b
ON a.Y_to_MO = b.Y_to_MO
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c02exp""", 'c02s3')
    
    _testmgr.testcase_end(desc)

def test024(desc="""c02b"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0151 : testC02b
    #  Description:        This testcase tests the JOIN  operation on a
    #                      table with the data type INTERVAL.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  These tests depend on successful completion of testB03 and testB04
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT a.D_to_H_1, b.D_to_H
FROM         BTRE218C a
INNER JOIN   BTRE218U b
ON a.D_to_H_1 = b.D_to_H
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c02bexp""", 'c02bs0')
    #  expect 3 rows with the following values in any order:
    #  	  342 16  342 16
    #  	    0 00    0 00
    #  	   22 13   22 13
    
    stmt = """SELECT a.D_to_H_1, b.D_to_H
FROM         BTRE218C a
LEFT JOIN    BTRE218U b
ON a.D_to_H_1 = b.D_to_H
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c02bexp""", 'c02bs1')
    #  expect the same 3 rows as above in any order:
    
    stmt = """SELECT a.D_to_H_1, b.D_to_H
FROM         BTRE218C a
RIGHT JOIN   BTRE218U b
ON a.D_to_H_1 = b.D_to_H
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c02bexp""", 'c02bs2')
    
    _testmgr.testcase_end(desc)

def test025(desc="""c02c"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0151 : testC02c
    #  Description:        This testcase tests the JOIN  operation on a
    #                      table with the data type INTERVAL.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  These tests depend on successful completion of testA04 and testA05
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT a.Y, b.Y, a.Y_TO_MO, b.Y_TO_MO, a.MO, b.MO FROM BTRE212C a
INNER JOIN BTRE212U b
ON a.Y = b.Y
ORDER BY 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c02cexp""", 'c02cs0')
    #  expect 4 rows with the following values in this order:
    #  	Y      Y      Y_TO_MO   Y_TO_MO   MO   MO
    #  	-----  -----  --------  --------  ---  ---
    #
    #  	    7      7      7-01      7-01    7    7
    #  	    9      9      9-01      9-01    9    9
    #  	   10     10     10-01     10-01    1    1
    #  	 9999   9999   9999-11   9999-11   11   11
    
    stmt = """SELECT a.D, b.D,
a.D_TO_H_1, b.D_TO_H,
a.D_TO_MI, b.D_TO_MI,
a.D_TO_S, b.D_TO_S
FROM BTRE212C a
LEFT  JOIN BTRE212U b
ON a.D = b.D
ORDER BY 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c02cexp""", 'c02cs1')
    #  expect 4 rows with the following values in this order:
    # D    D    D_TO_H_1  D_TO_H  D_TO_MI    D_TO_MI    D_TO_S        D_TO_S
    # ---  ---  --------  ------  ---------  ---------  ------------  ------------
    #
    #   7    7      0 00    0 00    0 00:00    0 00:00    0 00:00:00    0 00:00:00
    #   9    9      1 01    1 01    1 01:01    1 01:01    1 01:01:01    1 01:01:01
    #  15   15     15 12   15 12   16 13:15   16 13:15   17 14:16:01   17 14:16:01
    #  31   31     30 01   30 01   29 02:59   29 02:59   28 03:58:59   28 03:58:59
    
    stmt = """SELECT a.H, b.H,
a.H_TO_MI, b.H_TO_MI,
a.H_TO_S, b.H_TO_S
FROM BTRE212C a
RIGHT JOIN BTRE212U b
ON a.H = b.H
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c02cexp""", 'c02cs2')
    
    _testmgr.testcase_end(desc)

def test026(desc="""c03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0151 : testC03
    #  Description:        This testcase tests the JOIN  operation on a
    #                      table with the data type DATE and TIME. It
    #                      test the following cases:
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  These tests depends on successful completion of testA07 and testA08
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT BTRE213C.DATE1_1, BTRE213U.DATE1
FROM         BTRE213C 
INNER JOIN   BTRE213U 
ON BTRE213C.DATE1_1 = BTRE213U.DATE1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c03exp""", 'c03s0')
    #  expect 4 rows, each of the following values in any order:
    #  	1988-10-25  1988-10-25
    #  	0100-01-01  0100-01-01
    #  	0500-01-01  0500-01-01
    #  	1800-05-06  1800-05-06
    
    stmt = """SELECT a.TIME1, b.TIME1
FROM         BTRE213C a
INNER JOIN   BTRE213U b
ON a.TIME1 = b.TIME1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c03exp""", 'c03s1')
    #  expect 4 rows, each of the following values in any order:
    #  	10:10:10  10:10:10
    #  	00:00:00  00:00:00
    #  	21:59:59  21:59:59
    #  	12:23:24  12:23:24
    
    stmt = """SELECT a.TIME1, b.TIME1
FROM         BTRE213C a
LEFT JOIN    BTRE213U b
ON a.TIME1 = b.TIME1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c03exp""", 'c03s2')
    #  expect 16 rows, 4 each of the values above in any order:
    
    stmt = """SELECT a.TIME1, b.TIME1
FROM         BTRE213C a
RIGHT JOIN  BTRE213U b
ON a.TIME1 = b.TIME1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c03exp""", 'c03s3')
    
    _testmgr.testcase_end(desc)

def test027(desc="""c03b"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0151 : testC03b
    #  Description:        This testcase tests the JOIN  operation on a
    #                      table with the data type DATE and TIME. It
    #                      test the following cases:
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  These tests depends on successful completion of testB06 and testB07
    #
    # =================== End Test Case Header  ===================
    
    stmt = """selecT a.DT2, b.DT2
FROM         BTRE217C a
INNER JOIN   BTRE217U b
ON a.DT2 = b.DT2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #  expect 4 rows OF NULLs
    
    stmt = """SELECT a.DT2, b.DT2
FROM         BTRE217C a
LEFT JOIN    BTRE217U b
ON a.DT2 = b.DT2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c03bexp""", 'c03bs0')
    #  expect 2 rows of NULLs
    
    stmt = """SELECT a.DT2, b.DT2
FROM         BTRE217C a
RIGHT JOIN   BTRE217U b
ON a.DT2 = b.DT2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c03bexp""", 'c03bs1')
    
    _testmgr.testcase_end(desc)

def test028(desc="""c03c"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0151 : testC03c
    #  Description:        This testcase tests the JOIN  operation on a
    #                      table with the data type DATE and TIME. It
    #                      test the following cases:
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  These tests depends on successful completion of testA07 and testA08
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT * FROM BTRE213C a
INNER JOIN BTRE213U b
ON a.DATE1_1 = b.DATE1
ORDER BY 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c03cexp""", 'c03cs0')
    #  expect 4 rows of 4 columns of the following values in this order:
    #  0100-01-01  00:00:00  0100-01-01  00:00:00
    #  0500-01-01  21:59:59  0500-01-01  21:59:59
    #  1800-05-06  12:23:24  1800-05-06  12:23:24
    #  1988-10-25  10:10:10  1988-10-25  10:10:10
    
    stmt = """SELECT * FROM BTRE213C a
LEFT  JOIN BTRE213U b
ON a.DATE1_1 = b.DATE1
ORDER BY 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c03cexp""", 'c03cs1')
    #  expect 4 rows of the following values in this order:
    #  DATE1_1     TIME1     DATE1       TIME1
    #  ----------  --------  ----------  --------
    #
    #  0100-01-01  00:00:00  0100-01-01  00:00:00
    #  0500-01-01  21:59:59  0500-01-01  21:59:59
    #  1800-05-06  12:23:24  1800-05-06  12:23:24
    #  1988-10-25  10:10:10  1988-10-25  10:10:10
    
    stmt = """SELECT * FROM BTRE213C a
RIGHT JOIN BTRE213U b
ON a.DATE1_1 = b.DATE1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/c03cexp""", 'c03cs2')
    
    _testmgr.testcase_end(desc)

def test029(desc="""d00"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """DROP TABLE BTRE211U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE BTRE211C;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE BTRE212U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE BTRE212C;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE BTRE213U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE BTRE213C;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE BTRE217U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE BTRE217C;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE BTRE218U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE BTRE218C;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE BTRE219U;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE BTRE219C;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

