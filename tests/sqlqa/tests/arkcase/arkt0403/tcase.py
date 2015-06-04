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
    
    # create schema arkt0403;
    # table DTTAB is used in testA01 and testA06
    
    stmt = """CREATE    TABLE DTTAB (
Y           INTERVAL    YEAR (4),
Y_to_MO     INTERVAL    YEAR (4) TO MONTH,
MO          INTERVAL    MONTH,
D           INTERVAL    DAY,
D_to_H      INTERVAL    DAY TO HOUR,
D_to_MI     INTERVAL    DAY TO MINUTE,
D_to_S      INTERVAL    DAY TO SECOND,
H           INTERVAL    HOUR,
H_to_MI     INTERVAL    HOUR TO MINUTE,
H_to_S      INTERVAL    HOUR TO SECOND,
MI          INTERVAL    MINUTE,
MI_to_S     INTERVAL    MINUTE TO SECOND,
S           INTERVAL    SECOND,
S_to_F      INTERVAL    SECOND (2, 6)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # view VDTTAB is used in testA01 and testA06
    
    stmt = """CREATE VIEW VDTTAB ( Y_TO_MO, MI_TO_S ) AS
SELECT Y_TO_MO + INTERVAL '10' YEAR,
MI_TO_S - INTERVAL '3:20' MINUTE TO SECOND
FROM DTTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # create an index on dttab
    stmt = """CREATE INDEX IDTTAB 
ON DTTAB( Y, H_TO_S);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # table DTMTAB is used in testA02, testA03 & testA06
    
    # CREATE TABLE DTMTAB (                XXXXX can't do defaults
    #     DATE1 DATE DEFAULT NULL,
    #     TIME1 TIME DEFAULT TIME '12:00:00' AT GMT
    #     );
    
    stmt = """CREATE TABLE DTMTAB (
DATE1 DATE,
TIME1 TIME,
YEAR1 INTERVAL YEAR(4)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # table INTTAB is used in testA04, testA05 and testA06
    stmt = """CREATE TABLE INTTAB (
Y       INTERVAL YEAR,
Y_to_MO INTERVAL YEAR TO MONTH,
MO      INTERVAL MONTH not null,
D       INTERVAL DAY,
D_to_H  INTERVAL DAY TO HOUR,
D_to_MI INTERVAL DAY TO MINUTE,
D_to_S  INTERVAL DAY TO SECOND,
H       INTERVAL HOUR,
H_to_MI INTERVAL HOUR TO MINUTE,
H_to_S  INTERVAL HOUR TO SECOND,
MI      INTERVAL MINUTE,
MI_to_S INTERVAL MINUTE TO SECOND,
S       INTERVAL SECOND,
S_to_F  INTERVAL SECOND (2, 6),
PRIMARY KEY  (mo)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create index inttabi 
on INTTAB (y_to_mo asc, mI_to_s asc);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # table TEMPTS is used in testA06
    
    stmt = """CREATE TABLE TEMPTS (
id2m interval day to minute
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # CREATE TABLE TEMPINT (			XXXXX can't do DEFAULT
    #     Y_to_mo INTERVAL YEAR TO MONTH
    #                      DEFAULT INTERVAL '0-0'YEAR TO MONTH,
    #     D_to_F  INTERVAL DAY TO FRACTION DEFAULT NULL
    #     );
    
    stmt = """CREATE TABLE TEMPINT (
Y_to_mo INTERVAL YEAR TO MONTH,
D_to_S  INTERVAL DAY TO SECOND(6)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # the following tables are used in testA07
    
    stmt = """create table dt1 (a timestamp) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table dt2 (b timestamp) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table dt1k (
c timestamp NOT NULL,
primary key (c)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table dt2k (
d timestamp NOT NULL,
primary key (d)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table dtup (a timestamp, b timestamp) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table dt1d (a timestamp) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # the following tables are used in testA07
    
    stmt = """create table dtyf3 (a timestamp) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table itym  (a interval year to month) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ity4m (a interval year to month) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table itdf3 (a interval day to second (3)) no partition;"""
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
    #  Test case name:     arkt0303 : testA01
    #  Description:        This test verifies the SQL <specify>
    #                      feature.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    stmt = """INSERT INTO DTTAB VALUES (
INTERVAL'1988' YEAR (4),
INTERVAL'1988-01' YEAR (4) TO MONTH,
INTERVAL'11' MONTH,
INTERVAL'25' DAY,
INTERVAL'25:07' DAY TO HOUR,
INTERVAL'25:07:08' DAY TO MINUTE,
INTERVAL'25:07:08:10' DAY TO SECOND,
INTERVAL'10' HOUR,
INTERVAL'10:15' HOUR TO MINUTE,
INTERVAL'10:15:30' HOUR TO SECOND,
INTERVAL'55' MINUTE,
INTERVAL'55:59' MINUTE TO SECOND,
INTERVAL'59' SECOND,
INTERVAL'59.555' SECOND (2, 6)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO DTTAB VALUES (
INTERVAL'1975' YEAR (4),
INTERVAL'1974-02' YEAR (4) TO MONTH,
INTERVAL'01' MONTH,
INTERVAL'12' DAY,
INTERVAL'13:20' DAY TO HOUR,
INTERVAL'14:21:49' DAY TO MINUTE,
INTERVAL'15:22:50:54' DAY TO SECOND,
INTERVAL'01' HOUR,
INTERVAL'02:52' HOUR TO MINUTE,
INTERVAL'03:53:56' HOUR TO SECOND,
INTERVAL'55' MINUTE,
INTERVAL'56:58' MINUTE TO SECOND,
INTERVAL'01' SECOND,
INTERVAL'02.567' SECOND (2, 6)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO DTTAB VALUES (
INTERVAL'1975' YEAR (4),
INTERVAL'1975-03' YEAR (4) TO MONTH,
INTERVAL'01' MONTH,
INTERVAL'12' DAY,
INTERVAL'13:20' DAY TO HOUR,
INTERVAL'14:21:49' DAY TO MINUTE,
INTERVAL'15:22:50:54' DAY TO SECOND,
INTERVAL'01' HOUR,
INTERVAL'02:52' HOUR TO MINUTE,
INTERVAL'03:53:56' HOUR TO SECOND,
INTERVAL'55' MINUTE,
INTERVAL'56:58' MINUTE TO SECOND,
INTERVAL'01' SECOND,
INTERVAL'02.567' SECOND (2, 6)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO DTTAB VALUES (
INTERVAL'800' YEAR (4),
INTERVAL'801-08' YEAR (4) TO MONTH,
INTERVAL'02' MONTH,
INTERVAL'17' DAY,
INTERVAL'18:13' DAY TO HOUR,
INTERVAL'19:14:05' DAY TO MINUTE,
INTERVAL'20:15:05:07' DAY TO SECOND,
INTERVAL'17' HOUR,
INTERVAL'17:07' HOUR TO MINUTE,
INTERVAL'18:08:09' HOUR TO SECOND,
INTERVAL'10' MINUTE,
INTERVAL'11:11' MINUTE TO SECOND,
INTERVAL'13' SECOND,
INTERVAL'14.678' SECOND (2, 6)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO DTTAB VALUES (
INTERVAL'1' YEAR (4),
INTERVAL'1-01' YEAR (4) TO MONTH,
INTERVAL'01' MONTH,
INTERVAL'01' DAY,
INTERVAL'01:0' DAY TO HOUR,
INTERVAL'01:0:0' DAY TO MINUTE,
INTERVAL'01:0:0:0' DAY TO SECOND,
INTERVAL'0' HOUR,
INTERVAL'0:0' HOUR TO MINUTE,
INTERVAL'0:0:0' HOUR TO SECOND,
INTERVAL'0' MINUTE,
INTERVAL'0:0' MINUTE TO SECOND,
INTERVAL'0' SECOND,
INTERVAL'0.0' SECOND (2, 6)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO DTTAB VALUES (
INTERVAL'1984' YEAR (4),
INTERVAL'1984-01' YEAR (4) TO MONTH,
INTERVAL'01' MONTH,
INTERVAL'01' DAY,
INTERVAL'01:23' DAY TO HOUR,
INTERVAL'01:0:0' DAY TO MINUTE,
INTERVAL'01:23:40:50' DAY TO SECOND,
INTERVAL'0' HOUR,
INTERVAL'0:30' HOUR TO MINUTE,
INTERVAL'0:0:0' HOUR TO SECOND,
INTERVAL'30' MINUTE,
INTERVAL'0:0' MINUTE TO SECOND,
INTERVAL'55' SECOND,
INTERVAL'10.330' SECOND (2, 6)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO DTTAB VALUES (
INTERVAL'1989' YEAR (4),
INTERVAL'1989-10' YEAR (4) TO MONTH,
INTERVAL'10' MONTH,
INTERVAL'31' DAY,
INTERVAL'31:23' DAY TO HOUR,
INTERVAL'31:0:0' DAY TO MINUTE,
INTERVAL'31:23:40:50' DAY TO SECOND,
INTERVAL'0' HOUR,
INTERVAL'0:30' HOUR TO MINUTE,
INTERVAL'0:0:0' HOUR TO SECOND,
INTERVAL'30' MINUTE,
INTERVAL'0:0' MINUTE TO SECOND,
INTERVAL'55' SECOND,
INTERVAL'10.330' SECOND (2, 6)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  select from a view with datetime fields
    #  SELECT * FROM VDTTAB;	XXXXX gets errors
    stmt = """SELECT Y, Y_TO_MO, MO, D, D_TO_H, D_TO_MI, D_TO_S
--      FROM VDTTAB;	XXXXX gets errors
FROM DTTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    #  expect 7 rows with the following values in any order:
    #  Y      Y_TO_MO   MO   D    D_TO_H  D_TO_MI    D_TO_S
    #  -----  --------  ---  ---  ------  ---------  -------------------
    #
    #   1988   1988-01   11   25   25 07   25 07:08   25 07:08:10.000000
    #   1975   1974-02    1   12   13 20   14 21:49   15 22:50:54.000000
    #   1975   1975-03    1   12   13 20   14 21:49   15 22:50:54.000000
    #    800    801-08    2   17   18 13   19 14:05   20 15:05:07.000000
    #      1      1-01    1    1    1 00    1 00:00    1 00:00:00.000000
    #   1984   1984-01    1    1    1 23    1 00:00    1 23:40:50.000000
    #   1989   1989-10   10   31   31 23   31 00:00   31 23:40:50.000000
    
    stmt = """SELECT H, H_TO_MI, H_TO_S, MI, MI_TO_S, S, S_TO_F
--      FROM VDTTAB;	XXXXX gets errors
FROM DTTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    # expect 7 rows with the following values in any order:
    # H    H_TO_MI  H_TO_S            MI   MI_TO_S        S           S_TO_F
    # ---  -------  ----------------  ---  -------------  ----------  ----------
    #
    #  10    10:15   10:15:30.000000   55   55:59.000000   59.000000   59.555000
    #   1     2:52    3:53:56.000000   55   56:58.000000    1.000000    2.567000
    #   1     2:52    3:53:56.000000   55   56:58.000000    1.000000    2.567000
    #  17    17:07   18:08:09.000000   10   11:11.000000   13.000000   14.678000
    #   0     0:00    0:00:00.000000    0    0:00.000000    0.000000    0.000000
    #   0     0:30    0:00:00.000000   30    0:00.000000   55.000000   10.330000
    #   0     0:30    0:00:00.000000   30    0:00.000000   55.000000   10.330000
    
    #  Test insert, update, delete
    
    stmt = """INSERT INTO  DTTAB VALUES (
INTERVAL'1955' YEAR (4),
INTERVAL'1955-11' YEAR (4) TO MONTH,
INTERVAL'10' MONTH,
INTERVAL'5' DAY,
INTERVAL'5:15' DAY TO HOUR,
INTERVAL'5:15:15' DAY TO MINUTE,
INTERVAL'5:15:15:15' DAY TO SECOND,
INTERVAL'22' HOUR,
INTERVAL'22:22' HOUR TO MINUTE,
INTERVAL'22:22:22' HOUR TO SECOND,
INTERVAL'33' MINUTE,
INTERVAL'33:33' MINUTE TO SECOND,
INTERVAL'44' SECOND,
INTERVAL'44.444' SECOND (2, 6)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  Select the row to verify insert
    stmt = """SELECT Y, Y_to_mo from DTTAB 
where d_to_s = INTERVAL '05:15:15:15' day to second;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    # expect 1 row with the following values:
    # 	 1955   1955-11
    
    # Update the row
    stmt = """UPDATE  DTTAB 
SET  y = INTERVAL '3000' year (4),
y_to_mo = INTERVAL '3000-11' year (4) to month
where d_to_s = INTERVAL '05:15:15:15' day to second;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    #  select the row again to verify the update
    stmt = """SELECT Y, Y_to_mo from DTTAB 
where d_to_s = INTERVAL '05:15:15:15' day to second;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    # expect 1 row with the following values:
    # 	 3000   3000-11
    
    # delete the row
    stmt = """DELETE FROM DTTAB 
WHERE y = INTERVAL '3000' year (4) AND
y_to_mo = INTERVAL '3000-11' year (4) to month;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #  select the row again to verify the delete
    stmt = """SELECT Y, Y_to_mo from DTTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    #  expect 7 rows with the following values in any order:
    #  	 1988   1988-01
    #  	 1975   1974-02
    #  	 1975   1975-03
    #  	  800    801-08
    #  	    1      1-01
    #  	 1984   1984-01
    #  	 1989   1989-10
    #
    
    _testmgr.testcase_end(desc)

def test003(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0303 : testA02
    #  Description:        This test verifies the SQL <specify>
    #                      feature.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    stmt = """INSERT INTO DTMTAB VALUES (
DATE '1988-10-25',
TIME '10:10:10',
INTERVAL '1988' YEAR (4)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO DTMTAB VALUES (
DATE '0100-01-01',
TIME '00:00:00',
INTERVAL '0100' YEAR (4)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO DTMTAB VALUES (
DATE '0100-01-01',
TIME '23:59:59',
INTERVAL '0100' YEAR (4)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO DTMTAB VALUES (
DATE '9999-01-01',
TIME '10:20:30',
INTERVAL '9999' YEAR (4)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO DTMTAB VALUES (
DATE '0001-01-01',
TIME '00:00:00',
INTERVAL '0001' YEAR (4)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # -- Create a view  by joining the dttab and dtmtab
    stmt = """CREATE VIEW vdtab AS
SELECT * FROM DTTAB 
left join DTMTAB ON
YEAR1 = Y;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INVOKE vdtab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SELECT * FROM vdtab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    
    stmt = """SELECT * FROM DTTAB 
LEFT JOIN DTMTAB ON
YEAR1 = Y;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    
    _testmgr.testcase_end(desc)

def test004(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0303 : testA03
    #  Description:        This test verifies the SQL <specify>
    #                      feature.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    stmt = """SET PARAM ?P '2010-10-01';"""
    output = _dci.cmdexec(stmt)
    stmt = """SET PARAM ?P2 '1756-11-25';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO DTMTAB VALUES (
CAST (?P2 AS DATE),
TIME '23:55:35',
INTERVAL '1756' YEAR (4)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  display the record just inserted.
    stmt = """SELECT * FROM DTMTAB where DATE1 = CAST (?P2 AS DATE);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s0')
    
    # Update using parameters
    stmt = """UPDATE DTMTAB set date1 = CAST (?P AS DATE) WHERE
date1 = CAST (?P2 AS DATE);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    #  verify the update.
    stmt = """SELECT * FROM DTMTAB where DATE1 = CAST (?P AS DATE);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    
    #  Display in different formats.
    stmt = """SELECT DATEFORMAT( DATE1, USA ), DATEFORMAT( TIME1, USA)
FROM DTMTAB 
where DATE1 = CAST (?P AS DATE);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    
    stmt = """SELECT DATEFORMAT( DATE1, European ), DATEFORMAT( TIME1, European )
FROM DTMTAB 
where DATE1 = CAST (?P AS DATE);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s3')
    
    stmt = """SELECT DATEFORMAT( DATE1, default ), DATEFORMAT( TIME1, default )
FROM DTMTAB 
where DATE1 = CAST (?P AS DATE);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s4')
    
    # delete the record
    stmt = """DELETE FROM DTMTAB 
WHERE DATE1 = CAST (?P AS DATE);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    # verify the delete.
    stmt = """SELECT * FROM DTMTAB where DATE1 = CAST (?P AS DATE);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    _testmgr.testcase_end(desc)

def test005(desc="""a04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0303 : testA04
    #  Description:        This test verifies the SQL <specify>
    #                      feature.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    stmt = """INSERT INTO INTTAB  VALUES (
INTERVAL'10' YEAR,
INTERVAL'10-01' YEAR TO MONTH,
INTERVAL'01' MONTH,
INTERVAL'15' DAY,
INTERVAL'15:12' DAY TO HOUR,
INTERVAL'16:13:15' DAY TO MINUTE,
INTERVAL'17:14:16:01' DAY TO SECOND,
INTERVAL'16' HOUR,
INTERVAL'17:18' HOUR TO MINUTE,
INTERVAL'18:19:03' HOUR TO SECOND,
INTERVAL'21' MINUTE,
INTERVAL'21:05' MINUTE TO SECOND,
INTERVAL'07' SECOND,
INTERVAL'08.555' SECOND (2, 6)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO INTTAB VALUES (
INTERVAL'99' YEAR,
INTERVAL'99-11' YEAR TO MONTH,
INTERVAL'11' MONTH,
INTERVAL'31' DAY,
INTERVAL'30:01' DAY TO HOUR,
INTERVAL'29:02:59' DAY TO MINUTE,
INTERVAL'28:03:58:59' DAY TO SECOND,
INTERVAL'23' HOUR,
INTERVAL'22:56' HOUR TO MINUTE,
INTERVAL'21:55:57' HOUR TO SECOND,
INTERVAL'59' MINUTE,
INTERVAL'58:59' MINUTE TO SECOND,
INTERVAL'59' SECOND,
INTERVAL'58.666' SECOND (2, 6)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO INTTAB VALUES (
INTERVAL'1' YEAR,
INTERVAL'1-1' YEAR TO MONTH,
INTERVAL'5' MONTH,
INTERVAL'1' DAY,
INTERVAL'1:1' DAY TO HOUR,
INTERVAL'1:1:1' DAY TO MINUTE,
INTERVAL'1:1:1:1' DAY TO SECOND,
INTERVAL'1' HOUR,
INTERVAL'1:1' HOUR TO MINUTE,
INTERVAL'1:1:1' HOUR TO SECOND,
INTERVAL'1' MINUTE,
INTERVAL'1:1' MINUTE TO SECOND,
INTERVAL'1' SECOND,
INTERVAL'1.1' SECOND (2, 6)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO INTTAB VALUES (
INTERVAL'10' YEAR,
INTERVAL'0-0' YEAR TO MONTH,
INTERVAL'0' MONTH,
INTERVAL'0' DAY,
INTERVAL'0:10' DAY TO HOUR,
INTERVAL'0:12:10' DAY TO MINUTE,
INTERVAL'0:23:22:30' DAY TO SECOND,
INTERVAL'0' HOUR,
INTERVAL'0:10' HOUR TO MINUTE,
INTERVAL'0:24:35' HOUR TO SECOND,
INTERVAL'0' MINUTE,
INTERVAL'0:40' MINUTE TO SECOND,
INTERVAL'0' SECOND,
INTERVAL'0.000' SECOND (2, 6)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  insert negative values
    
    stmt = """INSERT INTO INTTAB VALUES (
INTERVAL'-10' YEAR,
INTERVAL'-0-0' YEAR TO MONTH,
INTERVAL'-10' MONTH,
INTERVAL'-20' DAY,
INTERVAL'-10:10' DAY TO HOUR,
INTERVAL'-20:12:10' DAY TO MINUTE,
INTERVAL'-10:23:22:30' DAY TO SECOND,
INTERVAL'-10' HOUR,
INTERVAL'-21:10' HOUR TO MINUTE,
INTERVAL'-10:24:35' HOUR TO SECOND,
INTERVAL'-80' MINUTE,
INTERVAL'-30:40' MINUTE TO SECOND,
INTERVAL'-60' SECOND,
INTERVAL'-81.000' SECOND (2, 6)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3044')
    
    #  a simple select
    # 04/14/09 added order by
    stmt = """SELECT MO FROM INTTAB GROUP BY MO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s1')
    
    #  select with multi value predicates in the where clause.
    stmt = """SELECT Y, Y_TO_MO  FROM INTTAB WHERE
MO, Y_TO_MO > INTERVAL '01' month, interval '01-01' YEAR TO MONTH
ORDER BY s_TO_F;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s2')
    
    _testmgr.testcase_end(desc)

def test006(desc="""a05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0303 : testA05
    #  Description:        This test verifies the SQL <specify>
    #                      feature.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    stmt = """INSERT INTO INTTAB VALUES (
INTERVAL'14' YEAR,
INTERVAL'15-09' YEAR TO MONTH,
INTERVAL'8' MONTH,
INTERVAL'22' DAY,
INTERVAL'23:10' DAY TO HOUR,
INTERVAL'24:10:10' DAY TO MINUTE,
INTERVAL'25:10:10:10' DAY TO SECOND,
INTERVAL'11' HOUR,
INTERVAL'11:12' HOUR TO MINUTE,
INTERVAL'11:12:13' HOUR TO SECOND,
INTERVAL'14' MINUTE,
INTERVAL'14:14' MINUTE to SECOND,
INTERVAL'35' SECOND,
INTERVAL'35.333' SECOND (2, 6)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """set param ?P '14:14';"""
    output = _dci.cmdexec(stmt)
    
    #  verify INSERT
    stmt = """SELECT * FROM INTTAB 
WHERE h_to_mi = INTERVAL '11:12' HOUR TO MINUTE
AND mi_to_s = CAST (?P AS INTERVAL MINUTE TO SECOND);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    
    # expect 1 row with values as inserted above
    
    # UPDATE
    stmt = """UPDATE INTTAB 
set y = INTERVAL '10' YEAR WHERE
h_to_mi = INTERVAL '11:12' HOUR TO MINUTE
AND mi_to_s = CAST (?P AS INTERVAL MINUTE TO SECOND);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    #  verify UPDATE
    stmt = """SELECT * FROM INTTAB 
WHERE h_to_mi = INTERVAL '11:12' HOUR TO MINUTE
AND mi_to_s = CAST (?P AS INTERVAL MINUTE TO SECOND);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
    # expect 1 row with values modified as above
    
    # DELETE
    stmt = """DELETE FROM INTTAB 
WHERE h_to_mi = INTERVAL '11:12' HOUR TO MINUTE
AND mi_to_s = CAST (?P AS INTERVAL MINUTE TO SECOND);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    # verify delete
    stmt = """SELECT * FROM INTTAB 
WHERE h_to_mi = INTERVAL '11:12' HOUR TO MINUTE
AND mi_to_s = CAST (?P AS INTERVAL MINUTE TO SECOND);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    _testmgr.testcase_end(desc)

def test007(desc="""a06a"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0303 : testA06
    #  Description:        This test verifies the SQL <specify>
    #                      feature.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #  display fields
    stmt = """SELECT DTTAB.Y, DTTAB.y_to_mo FROM DTTAB 
WHERE DTTAB.y = INTERVAL '1975' YEAR(4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06aexp""", 'a06as0')
    #  expect 2 rows with the following values in any order:
    #  	 1975   1974-02
    #  	 1975   1975-03
    
    stmt = """SELECT INTTAB.Y_to_mo FROM INTTAB 
WHERE INTTAB.y = INTERVAL '10' YEAR(2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06aexp""", 'a06as1')
    #  expect 2 rows with the following values in any order:
    #  	   0-00
    #  	  10-01
    
    stmt = """INSERT INTO TEMPINT (Y_to_mo) (
SELECT DTTAB.Y_to_mo - INTTAB.Y_to_mo
FROM DTTAB, INTTAB 
WHERE DTTAB.Y = INTERVAL '1975' YEAR (4)
AND INTTAB.Y = INTERVAL '10' YEAR (2)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    # verify results
    stmt = """SELECT * FROM TEMPINT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    # expect 4 rows with the following values in any order:
    # 	1974-02  	?
    # 	1964-01  	?
    # 	1975-03 	?
    # 	1965-02		?
    
    stmt = """delete FROM TEMPINT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    _testmgr.testcase_end(desc)

def test008(desc="""a06b"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0303 : testA06b
    #  Description:        This test verifies the SQL <specify>
    #                      feature.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT d_to_s, y_to_mo FROM DTTAB 
WHERE DTTAB.y_to_mo = INTERVAL '1988-01' YEAR (4) TO MONTH;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06bexp""", 'a06bs0')
    #  expect 1 row with the following values:
    #  	 25 07:08:10.000000   1988-01
    
    stmt = """INSERT INTO TEMPINT (
SELECT DTTAB.y_to_mo, DTTAB.d_to_s - INTTAB.d_to_s
FROM DTTAB, INTTAB 
WHERE DTTAB.y_to_mo = INTERVAL '1988-01' YEAR (4) TO MONTH
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    stmt = """SELECT * FROM TEMPINT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    # expect 4 rows with the following values in any order:
    #	1988-01   24 07:45:40.000000
    #	1988-01    7 16:52:09.000000
    #	1988-01   24 06:07:09.000000
    #	1988-01  - 2 20:50:49.000000
    
    stmt = """delete FROM TEMPINT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    _testmgr.testcase_end(desc)

def test009(desc="""a06c"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0303 : testA06c
    #  Description:        This test verifies the SQL <specify>
    #                      feature.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    stmt = """SELECT DTTAB.Y, INTTAB.Y,
 DTTAB.D_to_MI, INTTAB.D_to_MI,
 DTTAB.D_to_MI + INTTAB.D_to_MI
FROM DTTAB, INTTAB 
WHERE DTTAB.Y = INTERVAL '1975' YEAR (4)
AND INTTAB.Y = interval '10' YEAR (2)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06cexp""", 'a06cs0')
    # expect 4 rows with the following values in any order:
    # 	 1975   10   14 21:49    0 12:10    15 09:59
    # 	 1975   10   14 21:49   16 13:15    31 11:04
    # 	 1975   10   14 21:49    0 12:10    15 09:59
    # 	 1975   10   14 21:49   16 13:15    31 11:04
    
    # insert into temp1   (INTERVAL + interval)
    stmt = """INSERT INTO TEMPTS (
SELECT DTTAB.D_to_MI + INTTAB.D_to_MI
FROM DTTAB, INTTAB 
WHERE DTTAB.Y = INTERVAL'1975' YEAR (4)
AND INTTAB.Y = interval'10' YEAR
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 4)
    
    #  verify results
    stmt = """SELECT * FROM TEMPTS order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06cexp""", 'a06cs1')
    # expect 4 rows with the following values in any order:
    # 	 15 09:59
    # 	 31 11:04
    # 	 15 09:59
    # 	 31 11:04
    
    stmt = """delete from TEMPTS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    
    _testmgr.testcase_end(desc)

def test010(desc="""a06d"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0303 : testA06d
    #  Description:        This test verifies the SQL <specify>
    #                      feature.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    stmt = """SELECT DTTAB.D_TO_MI FROM DTTAB 
WHERE DTTAB.Y = INTERVAL'1984' YEAR (4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06dexp""", 'a06ds0')
    #  expect 1 row with the following value
    #  	  1 00:00
    
    #  select from intable the columns involved in (datetime - interval) operation
    stmt = """SELECT INTTAB.D_TO_MI FROM INTTAB 
WHERE INTTAB.Y = interval'10' YEAR (2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06dexp""", 'a06ds1')
    # expect 2 row with the following values
    # 	  0 12:10
    # 	 16 13:15
    
    # insert into tempts    (datetime - interval)
    stmt = """INSERT INTO TEMPTS (
SELECT DTTAB.D_to_MI - INTTAB.D_to_MI
FROM DTTAB, INTTAB 
WHERE DTTAB.Y = INTERVAL'1984' YEAR (4)
AND INTTAB.Y = interval'10' YEAR (2)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    #  verify results
    #  SELECT Y_TO_F FROM TEMPTS 		XXXXX can't do extend
    #      WHERE Y_TO_F IN (
    #  	SELECT EXTEND ((DTTAB.D_to_MI - INTTAB.D_to_MI), YEAR TO FRACTION)
    #              FROM DTTAB, INTTAB
    #                  WHERE DTTAB.Y = INTERVAL'1984' YEAR (4)
    #  		 AND INTTAB.Y = interval'10' YEAR (2)
    #      );
    
    stmt = """select * from TEMPTS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06dexp""", 'a06ds2')
    # expect 2 rows with the following values:
    # 	  0 11:50
    # 	-15 13:15
    
    stmt = """delete from TEMPTS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    
    _testmgr.testcase_end(desc)

def test011(desc="""a06e"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0303 : testA06e
    #  Description:        This test verifies the SQL <specify>
    #                      feature.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #  test datetime in multivalue predicates
    stmt = """SELECT Y, Y_to_MO FROM DTTAB WHERE
Y, Y_to_mo = INTERVAL '800' Year(4), INTERVAL '801-08' year(4) to month;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06eexp""", 'a06es0')
    # expect 1 row with the following values
    # 	  800    801-08
    
    # test interval in mutlivalue predicates
    stmt = """SELECT Y_to_mo, d_to_s
FROM INTTAB WHERE
Y_to_mo, d_to_s = INTERVAL '99-11' Year (2) TO MONTH,
INTERVAL '27:04:57:58.999' DAY TO SECOND;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #  expect 0 rows
    
    stmt = """SELECT Y_to_mo, d_to_s
FROM INTTAB WHERE
Y_to_mo, d_to_s = INTERVAL '99-11' Year (2) TO MONTH,
INTERVAL '28:03:58:59.000' DAY TO SECOND;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06eexp""", 'a06es1')
    
    _testmgr.testcase_end(desc)

def test012(desc="""a06f"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0303 : testA06f
    #  Description:        This test verifies the SQL <specify>
    #                      feature.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #  select columns involved in (interval - interval) operation
    stmt = """SELECT INTTAB.Y_TO_MO, INTTAB.Y FROM INTTAB 
WHERE INTTAB.Y_TO_MO = interval'10-01' YEAR TO MONTH;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06fexp""", 'a06fs0')
    # expect 1 row with the following values:
    # 	  10-01   10
    
    # empty tempint
    stmt = """delete FROM TEMPINT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    # insert into temp2 result of subtracting two interval type columns
    # INSERT INTO TEMPINT (Y_to_Mo) (		XXXXX can't do this yet
    #     SELECT INTTAB.Y_to_MO - INTTAB.Y FROM INTTAB
    
    stmt = """INSERT INTO TEMPINT (
SELECT INTTAB.Y_to_MO - INTTAB.Y, INTTAB.d_to_s FROM INTTAB 
WHERE INTTAB.Y_to_MO = interval'10-01' YEAR TO MONTH
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  verify the results
    stmt = """SELECT * FROM TEMPINT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06fexp""", 'a06fs1')
    
    _testmgr.testcase_end(desc)

def test013(desc="""a06g"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0303 : testA06g
    #  Description:        This test verifies the SQL <specify>
    #                      feature.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT * FROM TEMPINT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06gexp""", 'a06gs0')
    #  expect 1 row with the following values:
    #  	   0-01   17 14:16:01.000000
    
    #  display columns from intable that are involved in multiplication
    stmt = """SELECT INTTAB.Y_to_MO, INTTAB.d_to_s
FROM INTTAB 
WHERE INTTAB.Y_to_MO = interval'10-01' YEAR TO MONTH;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06gexp""", 'a06gs1')
    # expect 1 row with the following values:
    # 	  10-01   17 14:16:01.000000
    
    # insert into temp2  intable.y_to_mo * 2
    stmt = """INSERT INTO TEMPINT (Y_to_MO, d_to_s) (
SELECT INTTAB.Y_to_MO * 2, INTTAB.d_to_s * 5
FROM INTTAB 
WHERE INTTAB.Y_to_MO = interval'10-01' YEAR TO MONTH
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  verify results
    stmt = """SELECT * FROM TEMPINT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06gexp""", 'a06gs2')
    # expect 2 rows with the following values:
    # 	   0-01   17 14:16:01.000000
    # 	  20-02   87 23:20:05.000000
    
    stmt = """delete from TEMPINT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    
    _testmgr.testcase_end(desc)

def test014(desc="""a06h"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0303 : testA06h
    #  Description:        This test verifies the SQL <specify>
    #                      feature.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #  display the selected columns
    stmt = """SELECT INTTAB.Y, INTTAB.D_TO_S FROM INTTAB 
WHERE INTTAB.D = INTERVAL '15' DAY
AND INTTAB.MI = INTERVAL '21' MINUTE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06hexp""", 'a06hs0')
    #  expect 1 row with the following values:
    #  	 10   17 14:16:01.000000
    
    #  interval / scalar
    stmt = """SELECT INTTAB.Y / 4, INTTAB.D_TO_S / 3  FROM INTTAB 
WHERE INTTAB.D = INTERVAL '15' DAY
AND INTTAB.MI = INTERVAL '21' MINUTE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06hexp""", 'a06hs1')
    #  expect 1 row with the following values:
    #  	     2    5 20:45:20.333333
    
    #  interval * scalar
    stmt = """SELECT INTTAB.Y * 20, INTTAB.D_TO_S * 3  FROM INTTAB 
WHERE INTTAB.D = INTERVAL '15' DAY
AND INTTAB.MI = INTERVAL '21' MINUTE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06hexp""", 'a06hs2')
    #  expect 1 row with the following values:
    #  	   200    52 18:48:03.000000
    
    #  scalar * interval
    stmt = """SELECT 20 * INTTAB.Y, 3 * INTTAB.D_TO_S FROM INTTAB 
WHERE INTTAB.D = INTERVAL '15' DAY
AND INTTAB.MI = INTERVAL '21' MINUTE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06hexp""", 'a06hs3')
    # expect 1 row with the following values:
    # 	   200    52 18:48:03.000000
    
    # XXXXX can't do these next two
    # interval / interval
    # SELECT INTTAB.Y / INTERVAL '2' YEAR ,
    #        INTTAB.D_TO_S / INTERVAL '3:10:20:20' DAY TO SECOND
    #             FROM INTTAB
    #             WHERE INTTAB.D = INTERVAL '15' DAY
    #               AND INTTAB.MI = INTERVAL '21' MINUTE;
    
    # interval / ?p cast as interval
    stmt = """set param ?p "2";"""
    output = _dci.cmdexec(stmt)
    
    stmt = """set param ?p1 "3:10:20:20";"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test015(desc="""a06m"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0303 : testA06m
    #  Description:        This test verifies the SQL <specify>
    #                      feature.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT DATE1, DTTAB.y_to_MO
FROM DTMTAB, DTTAB 
WHERE DATE1 = date '1988-10-25'
AND DTTAB.y_TO_MO = INTERVAL '1974-02' YEAR (4) TO MONTH;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06mexp""", 'a06ms0')
    #  expect 1 row with the values 1988-10-25 and 1974-02
    
    #  (date - datetime)  using datetime qualifier on a column
    
    stmt = """SELECT DATE1 - DTTAB.y_to_MO
FROM DTMTAB, DTTAB 
WHERE DATE1 = date '1988-10-25'
AND DTTAB.y_TO_MO = INTERVAL'1974-02' YEAR (4) TO MONTH;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06mexp""", 'a06ms1')
    #  expect 1 row with the value 	0014-08-25
    
    #  display columns
    stmt = """SELECT TIME1, H_TO_S
FROM DTMTAB, DTTAB 
WHERE TIME1 = TIME'10:10:10'
AND DTTAB.H_TO_S = TIME'18:08:09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4041')
    #  expect 1 row with the values 10:10:10 and 18:08:09.000000
    
    #  XXXXX can't do EXTEND yet
    #  (TIME - DATETIME) with extension of time on the right
    #  SELECT EXTEND (TIME1, HOUR TO SECOND) - H_TO_S
    #      FROM DTMTAB, DTTAB
    #          WHERE TIME1 = TIME'10:10:10'
    #            AND DTTAB.H_TO_S = TIME'18:08:09';
    
    #  expect 1 row with the value 	0014-08-25
    
    #  more complicated interval and datetime arithmatic
    
    stmt = """SELECT Y, Y_TO_MO FROM DTTAB 
WHERE DTTAB.Y = INTERVAL ' 1975 ' YEAR (4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06mexp""", 'a06ms3')
    #  expect 2 rows with the following values:
    #  	 1975   1974-02
    #  	 1975   1975-03
    
    #  XXXXX can't do EXTEND yet
    #  SELECT  Y_TO_MO + interval' 10 ' YEAR -
    #      INTERVAL '3' MONTH  -
    #          EXTEND (Y_TO_D, YEAR TO MONTH)
    #              FROM DTTAB
    #                  WHERE Y = INTERVAL '1988' YEAR;
    
    #  Using unit specifiers. Result is numeric.
    #  The follwoing test case gets a binder error and should not.
    #   SELECT
    #            (
    #             (EXTEND (DTTAB.Y_TO_MO -
    #                       EXTEND (INTTAB.Y, YEAR TO MONTH), YEAR TO DAY) -
    #              DTTAB.Y_TO_D
    #            ) DAY + INTTAB.D
    #           ) UNITS HOUR
    #            FROM INTTAB, DTTAB WHERE
    #            DTTAB.Y = INTERVAL '1988' YEAR;
    
    #  Use of the Max and MIN functions
    stmt = """SELECT MAX (Y_to_MO), MIN (D_to_mi)
FROM DTTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06mexp""", 'a06ms4')
    
    _testmgr.testcase_end(desc)

def test016(desc="""a06n"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0303 : testA06n
    #  Description:        This test verifies the SQL <specify>
    #                      feature.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #  test DAYOFWEEK function
    stmt = """select DATE1 from DTMTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06nexp""", 'a06ns0')
    #  expect 6 rows with the following values:
    #  	1988-10-25
    #  	0100-01-01
    #  	0100-01-01
    #  	9999-01-01
    #  	0001-01-01
    #  	2010-10-01
    
    stmt = """select DAYOFWEEK (DATE1) from DTMTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06nexp""", 'a06ns1')
    #  expect 6 rows with the following values:
    #  3 (Tuesday)
    #  4 (Wednesday)
    #  4 (Wednesday)
    #  6 (Friday)
    #  7 (Saturday)
    #  6 (Friday)
    
    stmt = """select DTTAB.y, DTTAB.d from DTTAB 
where DTTAB.y = interval '1' year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06nexp""", 'a06ns2')
    #  expect 1 row with the following values:
    #  	    1    1
    
    stmt = """select DTTAB.d + cast (4 as interval day) from DTTAB 
where DTTAB.y = interval '1' year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06nexp""", 'a06ns3')
    #  expect 1 row with the value 5
    
    stmt = """SELECT DTTAB.D + CAST (DAYOFWEEK (DATE '1989-11-01') AS INTERVAL DAY)
FROM DTTAB 
WHERE DTTAB.Y = INTERVAL '1' YEAR;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06nexp""", 'a06ns4')
    #  expect 1 row with the value 5
    
    # *   datetime arithmetic on a view with datatime columns.
    #  #201
    stmt = """SELECT * FROM VDTTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06nexp""", 'a06ns5')
    #  expect 8 rows with the following values:
    #  	  1998-01    52:39.000000
    #  	  1984-02    53:38.000000
    #  	  1985-03    53:38.000000
    #  	   811-08     7:51.000000
    #  	    11-01  -  3:20.000000
    #  	  1994-01  -  3:20.000000
    #  	  1999-10  -  3:20.000000
    #  	  1965-11    30:13.000000
    
    stmt = """SELECT Y_TO_MO + interval' 10 ' MONTH FROM VDTTAB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06nexp""", 'a06ns6')
    
    _testmgr.testcase_end(desc)

def test017(desc="""a07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0303 : testA07
    #  Description:        This test verifies the SQL <specify>
    #                      feature.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """delete from dt1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    stmt = """delete from dt2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    stmt = """delete from dt1k;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    stmt = """delete from dt2k;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    # -- SET PARAM to be used in ALL the tests
    # reset param *;
    # 04/14/09 NCI doesn't take timestamp with : between date and time
    # changed the set param to remove the ":" between date and time
    #set param ?p '1989-03-17:08:45:58.123';
    stmt = """set param ?p '1989-03-17 08:45:58.123';"""
    output = _dci.cmdexec(stmt)
    # show param *;
    
    # XXXXXX can't do datetime params yet
    # -- INSERT into DATETIME tables
    stmt = """insert into dt1 values  (?p);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into dt2 values  (?p);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into dt1k values (?p);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into dt2k values (?p);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  INSERT into DATETIME tables
    # insert into dt1 values  (timestamp '1989-03-17:08:45:58.123');
    # insert into dt2 values  (timestamp '1989-03-17:08:45:58.123');
    # insert into dt1k values (timestamp '1989-03-17:08:45:58.123');
    # insert into dt2k values (timestamp '1989-03-17:08:45:58.123');
    
    #  Simple SELECTs
    stmt = """select * from dt1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s0')
    stmt = """select * from dt2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s1')
    stmt = """select * from dt1k;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s2')
    stmt = """select * from dt2k;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s3')
    
    stmt = """select a + interval '0' hour from dt1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s4')
    #  expect the same value as the above:
    
    stmt = """select a + interval '2' hour from dt1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s5')
    #  expect 1 row with the following value:
    #  	1989-03-17 10:45:58.123000
    
    stmt = """select * from dt1 where a is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s6')
    #  expect 1 row with the following value:
    #  	1989-03-17 08:45:58.123000
    
    #  XXXXXX can't do datetime params yet
    #  XXXXXX can't do datetime comparisons yet
    #  -- WHERE predicates on DATETIME values
    stmt = """select * from dt1 where a = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s7')
    stmt = """select * from dt1 where a + interval'0'hour = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s8')
    #  select * from dt1 where a = ?p + interval'0'hour;
    #
    stmt = """select * from dt1k where c = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s9')
    stmt = """select * from dt1k where c + interval'0'hour = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s10')
    #  select * from dt1k where c = ?p + interval'0'hour;
    
    #  JOIN tests
    #  expect 1 row from each with the following values:
    #  	1989-03-17 08:45:58.123000  1989-03-17 08:45:58.123000
    stmt = """select * from dt1, dt2 where a = b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s11')
    stmt = """select * from dt1k, dt2k where c = d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s12')
    stmt = """select * from dt1, dt1k where a = c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s13')
    
    stmt = """select * from dt1, dt2  where a + interval'0'hour = b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s14')
    stmt = """select * from dt1k, dt2k where c + interval'0'hour = d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s15')
    
    #  SUBQUERY tests: returning one value
    #  expect 1 row from each with the following value:
    #  	1989-03-17 08:45:58.123000
    stmt = """select * from dt1 where a = (select * from dt1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s16')
    stmt = """select * from dt1 where a = (select * from dt2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s17')
    stmt = """select * from dt1k where c = (select * from dt1k);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s18')
    stmt = """select * from dt1k where c = (select * from dt2k);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s19')
    
    #  SUBQUERY tests: ANY, ALL type
    stmt = """select * from dt1 where a in (select * from dt1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s20')
    stmt = """select * from dt1 where a in (select * from dt2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s21')
    stmt = """select * from dt1 where a = any (select * from dt2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s22')
    stmt = """select * from dt1 where a = all (select * from dt2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s23')
    stmt = """select * from dt1 where a = some (select * from dt2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s24')
    
    # XXXXX can't do datetime params yet
    # -- UPDATE tests
    
    stmt = """delete from dtup;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    stmt = """insert into dtup values (?p, ?p);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from dtup;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s25')
    #
    stmt = """update dtup set a = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from dtup;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s26')
    #
    stmt = """update dtup set a = b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from dtup;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s27')
    #
    # update dtup set a = a + interval'0'hour;
    # select * from dtup;
    #
    # update dtup set a = ?p + interval'0'hour;
    # select * from dtup;
    
    # UPDATE tests
    stmt = """delete from dtup;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """insert into dtup values (
timestamp '1989-03-17:08:45:58.123',
timestamp '1989-03-17:08:45:58.123'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from dtup;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s28')
    
    # XXXXX can't do datetime params yet
    stmt = """update dtup set a = ?p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    #  update dtup set b = timestamp '1989-03-17:10:45:58.123';
    stmt = """select * from dtup;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s29')
    # expect 1 row with the following values:
    # 	1989-03-17 08:45:58.123000  1989-03-17 10:45:58.123000
    
    stmt = """update dtup set a = b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from dtup;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s30')
    # expect 1 row with the following values:
    # 	1989-03-17 10:45:58.123000  1989-03-17 10:45:58.123000
    
    # update dtup set a = a + interval '0' hour;
    # select * from dtup;
    # expect 1 row with the same values as above.
    
    # update dtup set a = a - interval '2' hour;
    # select * from dtup;
    # expect 1 row with the following values:
    #      1989-03-17 08:45:58.123000  1989-03-17 10:45:58.123000
    
    # XXXXX can't do datetime params yet
    # update dtup set a = ?p + interval '0' hour;
    # update dtup set a = b + interval '0' hour;
    # select * from dtup;
    # expect 1 row with the following values:
    #      1989-03-17 10:45:58.123000  1989-03-17 10:45:58.123000
    
    # INSERT from SELECT
    stmt = """delete from dt1d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    stmt = """insert into dt1d select * from dt1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from dt1d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s31')
    
    stmt = """insert into dt1d select a + interval '16' hour from dt1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from dt1d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s32')
    
    _testmgr.testcase_end(desc)

def test018(desc="""a08"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0303 : testA08
    #  Description:        This test verifies the SQL <specify>
    #                      feature.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """delete from dtyf3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    _testmgr.testcase_end(desc)

def test019(desc="""a09"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0303 : testA09
    #  Description:        This test verifies the SQL <specify>
    #                      feature.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #  expect values as in the SELECT statements
    
    stmt = """select INTERVAL '1989' YEAR (4) from vdtab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s0')
    
    stmt = """select INTERVAL '1989-03' YEAR (4) to MONTH from vdtab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s1')
    
    stmt = """select INTERVAL '03' MONTH from vdtab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s2')
    
    stmt = """select INTERVAL '26' DAY from vdtab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s3')
    
    stmt = """select INTERVAL '26:10' DAY to HOUR from vdtab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s4')
    
    stmt = """select INTERVAL '26:10:30' DAY to MINUTE from vdtab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s5')
    
    stmt = """select INTERVAL '26:10:30:59.123456' DAY to SECOND (6) from vdtab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s6')
    
    stmt = """select INTERVAL '10' HOUR from vdtab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s7')
    
    stmt = """select INTERVAL '10:30' HOUR to MINUTE from vdtab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s8')
    
    stmt = """select INTERVAL '10:23:37.123456' HOUR to SECOND (6) from vdtab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s9')
    
    stmt = """select INTERVAL '23' MINUTE from vdtab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s10')
    
    stmt = """select INTERVAL '23:37.123456' MINUTE to SECOND (6) from vdtab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s11')
    
    stmt = """select INTERVAL '37.123456' SECOND (6) from vdtab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s12')
    
    stmt = """select INTERVAL '37.123' SECOND (2, 3) from vdtab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s13')
    
    stmt = """select INTERVAL '0.123456' SECOND (6) from vdtab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s14')
    
    stmt = """select INTERVAL '0.123' SECOND (2, 3) from vdtab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s15')
    
    stmt = """select TIMESTAMP '1989-03-26:10:23:37.123' from vdtab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s16')
    
    stmt = """select DATE '1989-03-26' from vdtab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s17')
    
    stmt = """select TIME '10:23:37' from vdtab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s18')
    
    # - -- USA formatting
    # -
    stmt = """select DATEFORMAT (
TIMESTAMP '03/26/1989 10:23:37.123456' , USA)
from vdtab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s19')
    
    # - DATEFORMAT does not support an INTERVAL expression per ANSI specs
    # -
    # - select DATEFORMAT (INTERVAL '03/26/1989'YEAR to DAY, USA) from vdtab;
    # -
    # - select DATEFORMAT (INTERVAL '1989-03' YEAR (4) to MONTH, USA) from vdtab;
    # -
    # - select DATEFORMAT (INTERVAL '03/26' MONTH to DAY, USA) from vdtab;
    # -
    # - select DATEFORMAT (INTERVAL '1989' YEAR, USA) from vdtab;
    # -
    # - select DATEFORMAT (INTERVAL '03' MONTH to MONTH, USA) from vdtab;
    # -
    # - select DATEFORMAT (INTERVAL '26' DAY, USA) from vdtab;
    # -
    # - select DATEFORMAT (INTERVAL '03/26/1989 10' YEAR to HOUR, USA) from vdtab;
    # -
    # - select DATEFORMAT (INTERVAL '03/26 10' MONTH to HOUR, USA) from vdtab;
    # -
    # - select DATEFORMAT (INTERVAL '26 10' DAY to HOUR, USA) from vdtab;
    # -
    # - select DATEFORMAT (INTERVAL '10:23:37.123456' HOUR to FRACTION(6), USA)
    # - from vdtab;
    # -
    # - select DATEFORMAT (INTERVAL '10' HOUR, USA) from vdtab;
    # -
    # - select DATEFORMAT (INTERVAL '23'MINUTE, USA) from vdtab;
    # -
    # - select DATEFORMAT (INTERVAL '37.123456' SECOND to FRACTION(6), USA) from
    # - vdtab;
    # -
    # - select DATEFORMAT (INTERVAL '37.123' SECOND to FRACTION(3), USA) from vdtab;
    # -
    # - select DATEFORMAT (INTERVAL '123456' FRACTION to FRACTION(6), USA) from
    # - vdtab;
    # -
    # - select DATEFORMAT (INTERVAL '123' FRACTION to FRACTION(3), USA) from
    # - vdtab;
    # -
    stmt = """select DATEFORMAT (TIMESTAMP'03/26/1989 10:23:37.123', USA) from vdtab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s20')
    
    stmt = """select DATEFORMAT (DATE '03/26/1989', USA) from vdtab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s21')
    
    stmt = """select DATEFORMAT (TIME '10:23:37', USA) from vdtab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s22')
    
    stmt = """select DATEFORMAT (TIMESTAMP'03/26/1989 10:23:37.123 AM', USA) from vdtab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s23')
    
    stmt = """select DATEFORMAT (DATE '03/26/1989', USA) from vdtab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s24')
    
    stmt = """select DATEFORMAT (TIME '10:23:37 AM', USA) from vdtab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s25')
    
    stmt = """select DATEFORMAT (TIMESTAMP'03/26/1989 10:23:37.123 PM', USA) from vdtab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s26')
    
    stmt = """select DATEFORMAT (DATE '03/26/1989', USA) from vdtab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s27')
    
    stmt = """select DATEFORMAT (TIME '10:23:37 PM', USA) from vdtab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s28')
    
    stmt = """select DATEFORMAT (TIME '12:00:00 AM', USA) from vdtab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s29')
    
    stmt = """select DATEFORMAT (TIME '12:00:00 PM', USA) from vdtab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s30')
    
    stmt = """select DATEFORMAT (TIME '12:23:37 AM', USA) from vdtab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s31')
    
    stmt = """select DATEFORMAT (TIME '12:23:37 PM', USA) from vdtab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s32')
    
    # - select DATEFORMAT (INTERVAL '26 10 AM'DAY TO HOUR, USA) from vdtab;
    # -
    # - select DATEFORMAT (INTERVAL '10 AM'HOUR, USA) from vdtab;
    # -
    # - select DATEFORMAT (INTERVAL '26 10 PM'DAY TO HOUR, USA) from vdtab;
    # -
    # - select DATEFORMAT (INTERVAL '10 PM'HOUR, USA) from vdtab;
    # -
    # - -- EUROPEAN formatting
    # -
    # - select DATEFORMAT (INTERVAL '26.03.1989 10.23.37.123456' YEAR to
    # -                   FRACTION(6), EUROPEAN) from vdtab;
    # - select DATEFORMAT (INTERVAL '26.03.1989'YEAR to DAY, EUROPEAN) from
    # - vdtab;
    # -
    # - select DATEFORMAT (INTERVAL '03.1989'YEAR to MONTH, EUROPEAN) from vdtab;
    # -
    # - select DATEFORMAT (INTERVAL '26.03' MONTH to DAY, EUROPEAN) from vdtab;
    # -
    # - select DATEFORMAT (INTERVAL '1989' YEAR, EUROPEAN) from vdtab;
    # -
    # - select DATEFORMAT (INTERVAL '03' MONTH to MONTH, EUROPEAN) from vdtab;
    # -
    # - select DATEFORMAT (INTERVAL '26' DAY, EUROPEAN) from vdtab;
    # -
    # - select DATEFORMAT (INTERVAL '26.03.1989 10' YEAR to HOUR, EUROPEAN) from
    # - vdtab;
    # - select DATEFORMAT (INTERVAL '26.03 10' MONTH to HOUR, EUROPEAN) from
    # - vdtab;
    # -
    # - select DATEFORMAT (INTERVAL '26 10' DAY to HOUR, EUROPEAN) from vdtab;
    # -
    # - select DATEFORMAT (INTERVAL '10.23.37.123456' HOUR to FRACTION(6),
    # - EUROPEAN) from vdtab;
    # -
    # - select DATEFORMAT (INTERVAL '10' HOUR, EUROPEAN) from vdtab;
    # -
    # - select DATEFORMAT (INTERVAL '23'MINUTE, EUROPEAN) from vdtab;
    # -
    # - select DATEFORMAT (INTERVAL '37.123456' SECOND to FRACTION(6), EUROPEAN)
    # - from vdtab;
    # -
    # - select DATEFORMAT (INTERVAL '37.123' SECOND to FRACTION(3), EUROPEAN) from vdtab;
    # -
    # - select DATEFORMAT (INTERVAL '123456' FRACTION to FRACTION(6), EUROPEAN)
    # - from vdtab;
    # -
    # - select DATEFORMAT (INTERVAL '123' FRACTION to FRACTION(3), EUROPEAN)
    # - from vdtab;
    # -
    stmt = """select DATEFORMAT (TIMESTAMP '26.03.1989 10.23.37.123', EUROPEAN) from vdtab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s33')
    
    stmt = """select DATEFORMAT (DATE '26.03.1989', EUROPEAN) from vdtab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s34')
    
    stmt = """select DATEFORMAT (TIME '10.23.37', EUROPEAN) from vdtab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s35')
    
    _testmgr.testcase_end(desc)

def test020(desc="""a16a"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0303 : testA16a
    #  Description:        This test verifies the SQL <specify>
    #                      feature.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    # create tables where key access could be chosen and multiple
    # scans are generated
    stmt = """create table tab1 (
a time not null,
primary key (a)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table tab2 (
a time not null,
b int,
primary key (a)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table tab3 (
a time not null,
b int not null,
primary key (a,b)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table tab4 (
a interval minute not null,
primary key (a)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table tab5 (
a interval hour to minute not null,
primary key (a)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table tab6 (
a interval day to minute not null,
primary key (a)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # table created to check ORDERBY clauses
    stmt = """create table otab1 (
a interval day to hour not null,
primary key (a)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table otab2 (
a interval day to hour not null,
b int,
primary key (a)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table otab3 (
a interval day to hour not null,
b int not null,
primary key (a,b)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table otab4 (a interval day to hour) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table otab5 (a interval day to hour, b int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table otab6 (a interval day to hour, b int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index otab4i on otab4 (a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index otab5i on otab5 (a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index otab6i on otab6 (a,b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # create tables where key access could not be chosen
    stmt = """create table ntab1 (
a time not null,
b time not null,
primary key (a,b)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ntab2 (
a int not null,
b time not null,
primary key (a,b)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ntab3 (
a interval day to hour,
b interval minute
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index ntab3i on ntab3(a,b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test021(desc="""a16b"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0303 : testA16b
    #  Description:        This test verifies the SQL <specify>
    #                      feature.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    # populate the tables
    stmt = """insert into tab1 values (time '00:00:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab1 values (time '10:00:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab1 values (time '15:00:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab1 values (time '16:00:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab1 values (time '20:00:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab1 values (time '23:00:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into tab2 values (time '00:00:00', 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab2 values (time '10:00:00', 10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab2 values (time '15:00:00', 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab2 values (time '16:00:00', 20);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab2 values (time '20:00:00', 999);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab2 values (time '23:00:00', 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into tab3 values (time '00:00:00', 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab3 values (time '10:00:00', 10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab3 values (time '15:00:00', 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab3 values (time '16:00:00', 20);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab3 values (time '20:00:00', 999);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab3 values (time '23:00:00', 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # NOTE: to test this case, we need a gmt difference of 30 minutes.
    stmt = """insert into tab4 values (interval '0'  minute);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab4 values (interval '10' minute);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab4 values (interval '30' minute);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab4 values (interval '40' minute);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into tab5 values (interval '0:0' hour to minute);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab5 values (interval '10:00' hour to minute);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab5 values (interval '15:00' hour to minute);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab5 values (interval '16:00' hour to minute);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab5 values (interval '20:00' hour to minute);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab5 values (interval '23:00' hour to minute);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into tab6 values (interval '31:00:00' day to minute);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab6 values (interval '31:10:00' day to minute);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab6 values (interval '31:15:00' day to minute);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab6 values (interval '31:16:00' day to minute);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab6 values (interval '31:20:00' day to minute);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab6 values (interval '31:23:00' day to minute);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into otab1 values (interval '31:00' day to hour);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab1 values (interval '31:10' day to hour);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab1 values (interval '31:15' day to hour);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab1 values (interval '31:16' day to hour);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab1 values (interval '31:20' day to hour);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab1 values (interval '31:23' day to hour);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into otab2 values (interval '31:00' day to hour, 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab2 values (interval '31:10' day to hour, 10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab2 values (interval '31:15' day to hour, 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab2 values (interval '31:16' day to hour, 20);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab2 values (interval '31:20' day to hour, 999);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab2 values (interval '31:23' day to hour, 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into otab3 values (interval '31:00' day to hour, 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab3 values (interval '31:10' day to hour, 10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab3 values (interval '31:10' day to hour, 20);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab3 values (interval '31:15' day to hour, 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab3 values (interval '31:16' day to hour, 20);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab3 values (interval '31:20' day to hour, 999);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab3 values (interval '31:23' day to hour, 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into otab4 values (interval '31:00' day to hour);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab4 values (interval '31:10' day to hour);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab4 values (interval '31:15' day to hour);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab4 values (interval '31:16' day to hour);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab4 values (interval '31:20' day to hour);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab4 values (interval '31:23' day to hour);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab4 values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into otab5 values (interval '31:00' day to hour, 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab5 values (interval '31:00' day to hour, 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab5 values (interval '31:10' day to hour, 10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab5 values (interval '31:15' day to hour, 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab5 values (interval '31:16' day to hour, 20);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab5 values (interval '31:16' day to hour, 20);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab5 values (interval '31:20' day to hour, 999);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab5 values (interval '31:23' day to hour, 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab5 values (null, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into otab6 values (interval '31:00' day to hour, 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab6 values (interval '31:10' day to hour, 10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab6 values (interval '31:15' day to hour, 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab6 values (interval '31:16' day to hour, 20);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab6 values (interval '31:20' day to hour, 999);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab6 values (interval '31:23' day to hour, 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab6 values (null,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into otab6 values (null,null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into ntab1 values (time '10:00:00', time '10:00:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ntab1 values (time '10:00:00', time '20:00:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ntab1 values (time '20:00:00', time '10:00:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ntab1 values (time '20:00:00', time '20:00:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into ntab2 values (0, time '10:00:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ntab2 values (0, time '20:00:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ntab2 values (1, time '10:00:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ntab2 values (1, time '20:00:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into ntab3 values (interval '31:10' day to hour, interval '30' minute);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ntab3 values (interval '31:20' day to hour, interval '50' minute);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    _testmgr.testcase_end(desc)

def test022(desc="""a16c"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0303 : testA16c
    #  Description:        This test verifies the SQL <specify>
    #                      feature.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #  SELECT from tables
    stmt = """select * from tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16cexp""", 'a16cs0')
    #  expect 6 rows with the following values:
    #  	00:00:00
    #  	10:00:00
    #  	15:00:00
    #  	16:00:00
    #  	20:00:00
    #  	23:00:00
    
    stmt = """select * from tab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16cexp""", 'a16cs1')
    #  expect 6 rows with the following values:
    #     00:00:00            0
    #     10:00:00           10
    #     15:00:00            0
    #     16:00:00           20
    #     20:00:00          999
    #     23:00:00            0
    
    stmt = """select * from tab3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16cexp""", 'a16cs2')
    #  expect 6 rows with the following values:
    #  	00:00:00            0
    #  	10:00:00           10
    #  	15:00:00            0
    #  	16:00:00           20
    #  	20:00:00          999
    #  	23:00:00            0
    
    stmt = """select * from tab4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16cexp""", 'a16cs3')
    #  expect 4 rows with the following values:
    #       0
    #      10
    #      30
    #      40
    
    stmt = """select * from tab5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16cexp""", 'a16cs4')
    #  expect 6 rows with the following values:
    #       0:00
    #      10:00
    #      15:00
    #      16:00
    #      20:00
    #      23:00
    
    stmt = """select * from tab6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16cexp""", 'a16cs5')
    #  expect 6 rows with the following values:
    #      31 00:00
    #      31 10:00
    #      31 15:00
    #      31 16:00
    #      31 20:00
    #      31 23:00
    
    stmt = """select * from tab1 where a > time '10:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16cexp""", 'a16cs6')
    #  expect 4 rows with the following values:
    #     15:00:00
    #     16:00:00
    #     20:00:00
    #     23:00:00
    
    stmt = """select * from tab1 where a > time '10:00:00' and a < time '20:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16cexp""", 'a16cs7')
    #  expect 2 rows with the following values:
    #     15:00:00
    #     16:00:00
    
    stmt = """select * from tab1 where a >= time '10:00:00' and a < time '20:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16cexp""", 'a16cs8')
    #  expect 3 rows with the following values:
    #     10:00:00
    #     15:00:00
    #     16:00:00
    
    stmt = """select * from tab1 where a > time '10:00:00' and a <= time '20:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16cexp""", 'a16cs9')
    #  expect 3 rows with the following values:
    #     15:00:00
    #     16:00:00
    #     20:00:00
    
    stmt = """select * from tab1 where a >= time '10:00:00' and a <= time '20:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16cexp""", 'a16cs10')
    #  expect 4 rows with the following values:
    #     15:00:00
    #     16:00:00
    #     20:00:00
    #     23:00:00
    
    stmt = """select * from tab1 where a > time '10:00:00' and a <= time '16:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16cexp""", 'a16cs11')
    #  expect 2 rows with the following values:
    #     15:00:00
    #     16:00:00
    
    stmt = """select * from tab1 where a > time '10:00:00' and a < time '16:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16cexp""", 'a16cs12')
    #  expect 1 row with the following value:
    #  	15:00:00
    
    stmt = """select * from tab1 where a > time '10:00:00' and a < time '16:00:00' OR
a > time '10:00:00' and a < time '16:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16cexp""", 'a16cs13')
    #  expect 1 row with the following value:
    #  	15:00:00
    
    stmt = """select * from tab2 where a > time '10:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16cexp""", 'a16cs14')
    #  expect 4 rows with the following values:
    #     15:00:00            0
    #     16:00:00           20
    #     20:00:00          999
    #     23:00:00            0
    
    stmt = """select * from tab2 where a > time '10:00:00' and a < time '20:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16cexp""", 'a16cs15')
    #  expect 2 rows with the following values:
    #  	15:00:00            0
    #  	16:00:00           20
    
    stmt = """select * from tab2 where a >= time '10:00:00' and a < time '20:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16cexp""", 'a16cs16')
    #  expect 3 rows with the following values:
    #     10:00:00           10
    #     15:00:00            0
    #     16:00:00           20
    
    stmt = """select * from tab2 where a > time '10:00:00' and a <= time '20:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16cexp""", 'a16cs17')
    #  expect 3 rows with the following values:
    #     15:00:00            0
    #     16:00:00           20
    #     20:00:00          999
    
    stmt = """select * from tab2 where a >= time '10:00:00' and a <= time '20:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16cexp""", 'a16cs18')
    #  expect 4 rows with the following values:
    #     10:00:00           10
    #     15:00:00            0
    #     16:00:00           20
    #     20:00:00          999
    
    stmt = """select * from tab2 where a > time '10:00:00' and a <= time '16:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16cexp""", 'a16cs19')
    #  expect 2 rows with the following values:
    #  	15:00:00            0
    #  	16:00:00           20
    
    stmt = """select * from tab2 where a > time '10:00:00' and a < time '16:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16cexp""", 'a16cs20')
    #  expect 1 row with the following value:
    #  	15:00:00            0
    
    stmt = """select * from tab2 where a > time '10:00:00' and a < time '16:00:00' OR
a > time '10:00:00' and a < time '16:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16cexp""", 'a16cs21')
    #  expect 1 row with the following value:
    #  	15:00:00            0
    
    stmt = """select * from tab3 where a > time '10:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16cexp""", 'a16cs22')
    #  expect 4 rows with the following values:
    #     15:00:00            0
    #     16:00:00           20
    #     20:00:00          999
    #     23:00:00            0
    
    stmt = """select * from tab3 where a > time '10:00:00' and a < time '20:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16cexp""", 'a16cs23')
    #  expect 2 rows with the following values:
    #  	15:00:00            0
    #  	16:00:00           20
    
    stmt = """select * from tab3 where a >= time '10:00:00' and a < time '20:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16cexp""", 'a16cs24')
    #  expect 3 rows with the following values:
    #     10:00:00           10
    #     15:00:00            0
    #     16:00:00           20
    
    stmt = """select * from tab3 where a > time '10:00:00' and a <= time '20:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16cexp""", 'a16cs25')
    #  expect 3 rows with the following values:
    #     15:00:00            0
    #     16:00:00           20
    #     20:00:00          999
    
    stmt = """select * from tab3 where a >= time '10:00:00' and a <= time '20:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16cexp""", 'a16cs26')
    #  expect 4 rows with the following values:
    #     10:00:00           10
    #     15:00:00            0
    #     16:00:00           20
    #     20:00:00          999
    
    stmt = """select * from tab3 where a > time '10:00:00' and a <= time '16:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16cexp""", 'a16cs27')
    #  expect 2 rows with the following values:
    #  	15:00:00            0
    #  	16:00:00           20
    
    stmt = """select * from tab3 where a > time '10:00:00' and a < time '16:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16cexp""", 'a16cs28')
    #  expect 1 row with the following value:
    #  	15:00:00            0
    
    stmt = """select * from tab3 where a > time '10:00:00' and a < time '16:00:00' OR
a > time '10:00:00' and a < time '16:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16cexp""", 'a16cs29')
    
    _testmgr.testcase_end(desc)

def test023(desc="""a16d"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0303 : testA16e
    #  Description:        This test verifies the SQL <specify>
    #                      feature.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """select * from ntab1 where a > time '10:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16dexp""", 'a16ds0')
    #  expect 2 rows with the following values:
    #  	20:00:00  10:00:00
    #  	20:00:00  20:00:00
    
    stmt = """select * from ntab1 where a > time '10:00:00' order by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16dexp""", 'a16ds1')
    #  expect 2 rows with the following values:
    #     20:00:00  10:00:00
    #     20:00:00  20:00:00
    
    stmt = """select * from ntab3 where a > interval '31:10' day to hour order by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16dexp""", 'a16ds2')
    #  expect 1 row with the following values:
    #      31 20   50
    
    #  SELECTs where index/key access cannot be chosen
    stmt = """select * from ntab1 where a,b > time '10:00:00', time '10:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16dexp""", 'a16ds3')
    #  expect 3 rows with the following values:
    #     10:00:00  20:00:00
    #     20:00:00  10:00:00
    #     20:00:00  20:00:00
    
    stmt = """select * from ntab2 where a,b > 0, time '10:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16dexp""", 'a16ds4')
    #  expect 3 rows with the following values:
    #               0  20:00:00
    #               1  10:00:00
    #               1  20:00:00
    
    #  KILLER QUERY XXXXXX
    stmt = """select * from ntab3 where a,b >
interval '31:10' day to hour, interval '30' minute;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16dexp""", 'a16ds5')
    #  -- expect 1 row with the following values:
    #  --     31 20   50
    
    #  ORDER BY where ordering cannot be done by inserting in a key seq file
    stmt = """select * from ntab1 order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16dexp""", 'a16ds6')
    #  expect 4 rows with the following values:
    #     10:00:00  10:00:00
    #     10:00:00  20:00:00
    #     20:00:00  10:00:00
    #     20:00:00  20:00:00
    
    stmt = """select * from ntab2 order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16dexp""", 'a16ds7')
    #  expect 4 rows with the following values:
    #               0  10:00:00
    #               0  20:00:00
    #               1  10:00:00
    #               1  20:00:00
    
    stmt = """select * from ntab3 order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16dexp""", 'a16ds8')
    #  expect 2 rows with the following values:
    #      31 10   30
    #      31 20   50
    
    stmt = """select * from ntab1 where a,b > time '10:00:00', time '10:00:00'
order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16dexp""", 'a16ds9')
    #  expect 3 rows with the following values:
    #     10:00:00  20:00:00
    #     20:00:00  10:00:00
    #     20:00:00  20:00:00
    
    stmt = """select * from ntab2 where a,b > 0, time '10:00:00'
order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16dexp""", 'a16ds10')
    #  expect 3 row with the following values:
    #            0  20:00:00
    #            1  10:00:00
    #            1  20:00:00
    
    #  KILLER QUERY XXXXX
    stmt = """select * from ntab3 where a,b >
interval '31:10' day to hour, interval '30' minute
order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16dexp""", 'a16ds11')
    # -- expect 1 rows with the following values:
    # -- 	 31 20   50
    
    # UPDATEs
    #begin work;
    stmt = """update tab2 set b = -1 where a > time '10:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 4)
    
    stmt = """select * from tab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16dexp""", 'a16ds12')
    # expect 6 rows with the following values:
    #    00:00:00            0
    #    10:00:00           10
    #    15:00:00           -1
    #    16:00:00           -1
    #    20:00:00           -1
    #    23:00:00           -1
    
    #rollback work;
    
    #begin work;
    stmt = """update tab2 set b = -1 where a > time '10:00:00' and a < time '16:00:00' OR
a > time '10:00:00' and a < time '16:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from tab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16dexp""", 'a16ds13')
    # expect 6 rows with the following values:
    #    00:00:00            0
    #    10:00:00           10
    #    15:00:00           -1
    #    16:00:00           -1
    #    20:00:00           -1
    #    23:00:00           -1
    
    #rollback work;
    
    # DELETEs
    #begin work;
    stmt = """delete from tab2 where a > time '10:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    
    stmt = """select * from tab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16dexp""", 'a16ds14')
    # expect 62rows with the following values:
    #    00:00:00            0
    #    10:00:00           10
    
    stmt = """insert into tab2 values (time '15:00:00', 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from tab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16dexp""", 'a16ds15')
    # expect 3 rows with the following values:
    #    00:00:00            0
    #    10:00:00           10
    #    15:00:00            0
    
    stmt = """delete from tab2 where a > time '10:00:00' and a < time '16:00:00' OR
a > time '10:00:00' and a < time '16:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    _testmgr.testcase_end(desc)

def test024(desc="""a16e"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0303 : testA16e
    #  Description:        This test verifies the SQL <specify>
    #                      feature.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """select * from ntab1 where a > time '10:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16eexp""", 'a16es0')
    #  expect 2 rows with the following values:
    #     20:00:00  10:00:00
    #     20:00:00  20:00:00
    
    stmt = """select * from ntab1 where a > time '10:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16eexp""", 'a16es1')
    #  expect 2 rows with the following values:
    #     20:00:00  10:00:00
    #     20:00:00  20:00:00
    
    stmt = """select * from ntab3 where a > interval '31:10' day to hour order by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16eexp""", 'a16es2')
    #  expect 1 row with the following values:
    #  	 31 20   50
    
    #  SELECTs where index/key access cannot be chosen
    stmt = """select * from ntab1 where a,b > time '10:00:00', time '10:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16eexp""", 'a16es3')
    #  expect 3 rows with the following values:
    #  	10:00:00  20:00:00
    #  	20:00:00  10:00:00
    #  	20:00:00  20:00:00
    
    stmt = """select * from ntab2 where a,b > 0, time '10:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16eexp""", 'a16es4')
    #  expect 3 rows with the following values:
    #  	          0  20:00:00
    #  	          1  10:00:00
    #  	          1  20:00:00
    
    #  KILLER QUERY XXXXXX
    stmt = """select * from ntab3 where a,b >
interval '31:10' day to hour, interval '30' minute;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16eexp""", 'a16es5')
    #  -- expect 1 row with the following values:
    #  -- 	 31 20   50
    
    #  ORDER BY where ordering cannot be done by inserting in a key seq file
    stmt = """select * from ntab1 order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16eexp""", 'a16es6')
    #  expect 4 rows with the following values:
    #  	10:00:00  10:00:00
    #  	10:00:00  20:00:00
    #  	20:00:00  10:00:00
    #  	20:00:00  20:00:00
    
    stmt = """select * from ntab2 order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16eexp""", 'a16es7')
    #  expect 4 rows with the following values:
    #               0  10:00:00
    #               0  20:00:00
    #               1  10:00:00
    #               1  20:00:00
    
    stmt = """select * from ntab3 order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16eexp""", 'a16es8')
    #  expect 2 rows with the following values:
    #      31 10   30
    #      31 20   50
    
    stmt = """select * from ntab1 where a,b > time '10:00:00', time '10:00:00'
order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16eexp""", 'a16es9')
    #  expect 3 rows with the following values:
    #  	10:00:00  20:00:00
    #  	20:00:00  10:00:00
    #  	20:00:00  20:00:00
    
    stmt = """select * from ntab2 where a,b > 0, time '10:00:00'
order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16eexp""", 'a16es10')
    #  expect 3 rows with the following values:
    #               0  20:00:00
    #               1  10:00:00
    #               1  20:00:00
    
    #  KILLER QUERY XXXXX
    stmt = """select * from ntab3 where a,b >
interval '31:10' day to hour, interval '30' minute
order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16eexp""", 'a16es11')
    # -- expect 1 row with the following values:
    # -- 	 31 20   50
    
    # UPDATEs
    # rebuild tab2
    stmt = """delete from tab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    
    stmt = """insert into tab2 values (time '00:00:00', 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab2 values (time '10:00:00', 10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab2 values (time '15:00:00', 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab2 values (time '16:00:00', 20);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab2 values (time '20:00:00', 999);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab2 values (time '23:00:00', 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #begin work;
    stmt = """update tab2 set b = -1 where a > time '10:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 4)
    
    stmt = """select * from tab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16eexp""", 'a16es12')
    # expect 6 rows with the following values:
    #    00:00:00            0
    #    10:00:00           10
    #    15:00:00           -1
    #    16:00:00           -1
    #    20:00:00           -1
    #    23:00:00           -1
    
    #rollback work;
    
    #begin work;
    # rebuild tab2
    stmt = """delete from tab2 where a > time '10:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    
    stmt = """insert into tab2 values (time '15:00:00', 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab2 values (time '16:00:00', 20);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab2 values (time '20:00:00', 999);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab2 values (time '23:00:00', 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update tab2 set b = -1 where a > time '10:00:00' and a < time '16:00:00' OR
a > time '10:00:00' and a < time '16:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from tab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16eexp""", 'a16es13')
    # expect 6 rows with the following values:
    #    00:00:00            0
    #    10:00:00           10
    #    15:00:00           -1
    #    16:00:00           20
    #    20:00:00          999
    #    23:00:00            0
    
    #rollback work;
    
    # DELETEs
    #begin work;
    stmt = """delete from tab2 where a > time '16:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    
    stmt = """select * from tab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16eexp""", 'a16es14')
    # expect 4 rows with the following values:
    #    00:00:00            0
    #    10:00:00           10
    #    15:00:00           -1
    #    16:00:00           20
    
    stmt = """delete from tab2 where a > time '10:00:00' and a < time '16:00:00' OR
a > time '10:00:00' and a < time '16:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select * from tab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16eexp""", 'a16es15')
    
    _testmgr.testcase_end(desc)

def test025(desc="""a16f"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0303 : testA16d
    #  Description:        This test verifies the SQL <specify>
    #                      feature.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """drop index otab4i;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop index otab5i;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop index otab6i;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop index ntab3i;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table tab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table tab3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table tab4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table tab5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table tab6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table otab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table otab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table otab3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table otab4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table otab5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table otab6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table ntab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table ntab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table ntab3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

