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
    
def test001(desc="""a01"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0025 : A01
    #  Description:        This is test for SQL DML
    #                      statements related to INSERT.
    #                      Positive insert for tables and views
    #  Purpose:            Inserts into various table types and
    #                      protection views
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    
    #  insert appending on protection view defined against a
    #  key sequenced table that has a syskey associated with it
    #  (APPEND is only valid against tables containing syskey)
    stmt = """CREATE VIEW pv16 AS SELECT * FROM btsel16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INVOKE pv16;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """delete from btsel16 where data_93 = 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    stmt = """SELECT * FROM pv16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    
    #Insert into the view pv16 created in the pretest
    
    stmt = """INSERT INTO pv16 VALUES (10, 100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """SELECT * FROM pv16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    
    stmt = """DROP VIEW pv16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """DELETE FROM btemprel;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    #  single column relative table; insert constant
    stmt = """SELECT syskey,* FROM btemprel;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """INSERT INTO btemprel (some_data) VALUES (0)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """SELECT syskey,* FROM btemprel;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """DELETE FROM btsel03 where pic_9_7 = 13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    #   insert expressions using expressions are
    #   not supported
    stmt = """SELECT syskey, * FROM btsel03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 8)
    
    #   relative table protection view; SYSKEY omitted in WHERE
    stmt = """SELECT syskey, * FROM btsel04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 8)
    stmt = """SELECT * FROM pvsel04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s8')
    
    stmt = """INSERT INTO pvsel04 
(var_char, medium_int, pic_x_7, pic_comp_1)
VALUES ('xyz', -32, 'abcdefg', 43);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """SELECT * FROM pvsel04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s9')
    stmt = """SELECT syskey, * FROM btsel04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 9)
    
    stmt = """DELETE FROM btsel02 WHERE PIC_X_1 = '1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    #   entry seq table; insert *
    stmt = """SELECT syskey,* FROM btsel02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 8)
    
    stmt = """INSERT INTO btsel02 (*) VALUES ('1');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """SELECT syskey,* FROM btsel02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 9)
    
    stmt = """delete FROM btsel07 where pic_x_a = 'qrs';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    #   key seq table; absent column list; truncating data & padding data
    stmt = """SELECT * FROM btsel07;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s14')
    
    # INSERT INTO btsel07 VALUES ('qrst', 'a', 'x');
    stmt = """INSERT INTO btsel07 VALUES ('qrs', 'a', 'x');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """SELECT * FROM btsel07;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s15')
    
    _testmgr.testcase_end(desc)

def test002(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0025 : A02
    #  Description:        This is test for SQL DML
    #                      statements related to INSERT.
    #                      Second set of inserts.
    #  Purpose:            Inserts into various table types and
    #                      protection views already inserted into
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    
    stmt = """SELECT syskey,* FROM btsel03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 8)
    stmt = """SELECT * FROM pvsel03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    stmt = """SELECT * FROM btsel04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    
    #   protection view on relative table; not specifying syskey value
    stmt = """INSERT INTO pvsel03 VALUES (1954, 20, 'xxxxxxx', 8);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4027')
    
    #  insert record shorter than table def; not using defaults
    stmt = """INSERT INTO btsel04 (var_char, medium_int, pic_x_7)
VALUES ('abc', -1, 'abc123d') read committed access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """INSERT INTO btsel04 
VALUES ('abc', -1, 'abc123d',400) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """SELECT syskey,* FROM btsel03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 8)
    stmt = """SELECT * FROM pvsel03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    stmt = """SELECT * FROM btsel04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s7')
    
    _testmgr.testcase_end(desc)

def test003(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0025 : A03
    #  Description:        This is test for SQL DML
    #                      statements related to INSERT.
    #                      Third set of inserts
    #  Purpose:            Inserts into various table types and
    #                      protection views that have been inserted
    #                      into twice already
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    
    stmt = """SELECT * FROM btsel03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s0')
    
    stmt = """INSERT INTO btsel03 (pic_x_7) VALUES ('1234');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4024')
    
    #        serializable access;
    stmt = """INSERT INTO btsel03 VALUES ('1234',7,'xyz',60,1300) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """SELECT * FROM btsel03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    
    stmt = """DELETE FROM btsel03 where pic_x_7 = '1234';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """SELECT * FROM btsel03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s4')
    
    _testmgr.testcase_end(desc)

def test004(desc="""a04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0025 : A04
    #  Description:        This is test for SQL DML
    #                      statements related to INSERT.
    #                      Testing APPEND and ANYWHERE
    #  Purpose:            Testing appends and anywhere on tables
    #                      and protection views
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    
    #   delete records to test ANYWHERE vs. APPEND
    stmt = """DELETE FROM btsel03 WHERE binary_64_s >= 1000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 7)
    
    #  cannot delete records from an entry sequenced table; NEGATIVE TEST
    stmt = """DELETE FROM btsel02 WHERE pic_x_1 = 'Q';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)
    
    #  insert APPENDing on table
    stmt = """INSERT INTO btsel03 
VALUES ('apptab', 12345.67, 'xyz', 7, 225);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #       VALUES ('apptab', 'xyz', 225) APPEND;
    
    #  insert APPENDing on table without specifying APPEND
    stmt = """INSERT INTO btsel03 
VALUES ('apprec', 12345.67, 'xyz', 7, 225);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  insert APPENDing on view
    #INSERT INTO pvsel03 (new_name_1, new_name_2, new_name_3)
    #       VALUES (7777777, 9876543.21,'abcdefg');
    #       VALUES (7777777, 9876543.21,'abcdefg') APPEND read committed access;
    
    #  insert ANYWHERE on table
    stmt = """INSERT INTO btsel03 
VALUES ('anytab', 12345.67, 'xyz', 7, 225);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #       VALUES ('anytab', 'xyz', 225) ANYWHERE serializable access;
    
    #  insert ANYWHERE on view
    #INSERT INTO pvsel03 (new_name_1, new_name_2, new_name_3)
    #       VALUES (9876543, 7777777.77,'poiuytr');
    # ANYWHERE;
    
    #  insert APPEND on entry sequenced table
    stmt = """INSERT INTO btsel02 VALUES ('X');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  APPEND;
    
    stmt = """SELECT syskey, * FROM btsel03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    stmt = """SELECT * FROM pvsel03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    stmt = """SELECT syskey, * FROM btsel02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 7)
    
    _testmgr.testcase_end(desc)

def test005(desc="""a05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0025 : A05
    #  Description:        This is test for SQL DML
    #                      statements related to INSERT.
    #                      Searched INSERTS (positive)
    #  Purpose:            Insert into views and tables based on
    #                      SELECTed data
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    
    stmt = """SELECT * FROM btsel03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    #   select many records using a comparison
    
    stmt = """SELECT binary_32_u, char_1, binary_64_s
FROM btsel01 
WHERE binary_signed < 100 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
    
    stmt = """SELECT pic_x_a, pic_x_b, col_1, pic_x_c, col_2, col_10, col_21
FROM btsel06 
WHERE col_1 BETWEEN 800 and 900 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    
    stmt = """SELECT * FROM btsel06;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
    
    #  select many records using BETWEEN
    
    stmt = """INSERT INTO btsel11 
(SELECT pic_x_a, pic_x_b, col_1, pic_x_c, col_2, col_10, col_21
FROM btsel06 
WHERE col_1 BETWEEN 800 and 900);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """SELECT * FROM btsel06;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s4')
    
    stmt = """SELECT * FROM btsel07;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s5')
    
    #  NOTE:  The results of the above query are NOT in a specific
    #         order, so from time to time it changes, make sure all
    #         the elements are returned, then use the new order
    
    stmt = """SELECT pic_x_a, pic_x_b, pic_x_c
FROM btsel06 
WHERE pic_x_a IN ('joe', 'pam') ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s6')
    
    #  select many records using IN
    stmt = """INSERT INTO btsel07 
(SELECT pic_x_a, pic_x_b, pic_x_c
FROM btsel06 
WHERE pic_x_a IN ('joe', 'pam'))
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    #        APPEND serializable access;
    
    stmt = """SELECT * FROM btsel07;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s7')
    
    # NOTE:  The results of the above query are NOT in a specific
    #        order, so from time to time it changes, make sure all
    #        the elements are returned, then use the new order
    
    stmt = """SELECT * FROM btempkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #   select many records using many comparisons
    
    stmt = """SELECT regnum
FROM region 
WHERE (regnum >= 3) AND ((manager BETWEEN 50 and 90) OR
(location LIKE 'TO%'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s8')
    
    stmt = """INSERT INTO btempkey 
(SELECT regnum
FROM region 
WHERE (regnum >= 3) AND ((manager BETWEEN 50 and 90) OR
(location LIKE 'TO%')));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)
    stmt = """SELECT * FROM btempkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s9')
    
    stmt = """SELECT * FROM btsel11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s10')
    
    #   select all records of one table and insert into another
    stmt = """SELECT * FROM btsel10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s11')
    
    stmt = """INSERT INTO btsel11 (*)
(SELECT * FROM btsel10 
read committed access);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 8)
    
    stmt = """SELECT * FROM btsel11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s12')
    
    stmt = """SELECT * FROM btsel15;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s13')
    
    #   syntactic check for different locking in INSERT and SELECT
    stmt = """SELECT * FROM btsel16 serializable access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s14')
    
    #   This is a negative test
    stmt = """INSERT INTO btsel15 (SELECT * FROM
 btsel16 serializable access)
read committed access;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT * FROM btsel15;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s16')
    
    _testmgr.testcase_end(desc)

def test006(desc="""a06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0025 : A06
    #  Description:        This is test for SQL DML
    #                      statements related to INSERT.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    
    #   -- TESTCASE SUMMARY
    #   Searched INSERTS, second set
    #
    #
    #   |                                                     |
    #   |  Test Case Name:  B2                                |
    #   |                                                     |
    #   |  Purpose:  insert into views and tables based on    |
    #   |            SELECTed data                            |
    #   |                                                     |
    #
    #
    
    #   select many records using LIKE; selects the whole table
    stmt = """INSERT INTO btsel07 
(SELECT pic_x_a, pic_x_b, pic_x_c FROM
 btsel06 WHERE pic_x_c LIKE '%');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    
    #  insert using select which returns zero records
    stmt = """INSERT INTO btsel07 
(SELECT pic_x_a, pic_x_b, pic_x_c FROM
 btsel05 WHERE pic_x_a = 'ted');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 0)
    
    #  insert using select which returns one record
    stmt = """INSERT INTO btsel07 
(SELECT pic_x_a, pic_x_b, pic_x_c FROM
 btsel05 WHERE pic_x_a = 'red' AND
pic_x_b = 'B');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO btempent 
(SELECT data_93 FROM btsel12);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 8)
    
    stmt = """SELECT * FROM btsel07;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s1')
    
    #  NOTE:  The results of the above query are NOT in a specific
    #         order, so from time to time it changes, make sure all
    #         the elements are returned, then use the new order
    
    stmt = """SELECT syskey,* FROM btempent;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 8)
    
    _testmgr.testcase_end(desc)

def test007(desc="""a07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #  have 1 row.  These two tables will be used in the
    #  SELECT portion of the INSERT-SELECT statement.
    stmt = """CREATE TABLE t025b31 
(a int) no partition;"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE TABLE t025b32 
(a int) no partition;"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE TABLE t025b33 
(a int) no partition;"""
    output = _dci.cmdexec(stmt)
    
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0025 : A07
    #  Description:        This is test for SQL DML
    #                      statements related to INSERT.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    
    #  -- TESTCASE SUMMARY
    #  Verification of INSERT using
    #  SELECT with UNION ALL.
    #
    #
    #  |                                                     |
    #  |  Test Case Name:  B3                                |
    #  |                                                     |
    #  |  Purpose:  INSERT INTO using SELECT with UNION ALL. |
    #  |                                                     |
    
    stmt = """INSERT INTO t025b32 VALUES (2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #   First execute the SELECT UNION ALL by itself. It
    #   should return 1 row from the second SELECT. (No
    #   rows in table from first SELECT).
    stmt = """SELECT * FROM t025b31 
UNION ALL
SELECT * FROM t025b32;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s0')
    
    #  INSERT INTO using the SELECT UNION ALL.  Before fix,
    #  this erroneously returned - WARNING from SQL [100].
    #  The expected result is 1 row inserted into T025b33.
    stmt = """INSERT INTO t025b33 
(SELECT * FROM t025b31 
UNION ALL
SELECT * FROM t025b32);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  There was not a problem when the INSERT INTO used
    #  SELECT UNION (not UNION ALL).  The above test will be
    #  repeated to ensure UNION still works as well. 1 more
    #  should be inserted into T025b33.
    stmt = """INSERT INTO t025b33 
(SELECT * FROM t025b31 
UNION
SELECT * FROM t025b32);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #   Verify there are now 2 rows in T025B33.
    stmt = """SELECT * FROM t025b33;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s1')
    
    #ROLLBACK;
    
    _testmgr.testcase_end(desc)

