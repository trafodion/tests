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
    
def test001(desc="""a14"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A14
    #  Description:        Create objects needed for the test unit
    #  Purpose:            To create the objects that will be used
    #                      throughout the test unit
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """DROP TABLE reltaba;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE reltaba (col_1 PIC x(3), col_2 PIC 9(3), col_3 PIC x(3)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #     CATALOG ORGANIZATION R;
    #      CATALOG ORGANIZATION K;
    
    stmt = """CREATE INDEX relinda ON reltaba (col_2 DESC);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #       CATALOG
    
    #   CREATE non-empty key sequenced table with a specified primary key
    
    stmt = """DROP TABLE keytaba;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE keytaba (col_1 PIC x(3), col_2 PIC 9(3), col_3 PIC x(3)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #      CATALOG ORGANIZATION K;
    
    stmt = """INSERT INTO keytaba VALUES ('abc', 123, 'def');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO keytaba VALUES ('ghi', 456, 'jkl');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO keytaba VALUES ('mno', 789, 'pqr');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO keytaba VALUES ('stu', 987, 'vwx');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO keytaba VALUES ('yz', 654, 'zyx');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #   CREATE non-empty entry sequenced table with a partition, a view, and
    #          SYSKEY
    stmt = """DROP   VIEW entviewa;"""
    output = _dci.cmdexec(stmt)
    stmt = """DROP   TABLE enttaba;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE enttaba (col_1 PIC x(3) not null,
col_2 PIC 9(3),
col_3 PIC x(3),
primary key (col_1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """CREATE VIEW entviewa AS SELECT col_2, col_3 FROM enttaba 
WHERE col_2 > 234;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # CATALOG FOR PROTECTION;
    
    stmt = """INSERT INTO enttaba VALUES ('zyx', 987, 'abc');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO enttaba VALUES ('wvu', 654, 'def');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO enttaba VALUES ('tsr', 321, 'ghi');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #   CREATE empty key sequenced table with a SYSKEY
    
    stmt = """DROP   TABLE keytabb;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE keytabb (col_1 PIC 9(3), col_2 PIC x(3), col_3 PIC 9(3)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SELECT * FROM reltaba;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """SELECT * FROM keytaba;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s5')
    stmt = """SELECT * FROM enttaba;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s6')
    stmt = """SELECT * FROM entviewa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s7')
    stmt = """SELECT * FROM keytabb;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """DROP TABLE keytaba;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE TABLE keytaba (col_1 PIC x(3), col_2 PIC 9(3), col_3 PIC x(3)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO keytaba VALUES ('abc', 123, 'def');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO keytaba VALUES ('ghi', 456, 'jkl');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO keytaba VALUES ('mno', 789, 'pqr');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO keytaba VALUES ('stu', 987, 'vwx');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO keytaba VALUES ('yz', 654, 'zyx');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    _testmgr.testcase_end(desc)

def test002(desc="""a15"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """control query default query_cache '0';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """alter table reltaba 
add constraint C1 check (col_2 < 555);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """invoke keytaba;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """alter table keytaba 
add constraint C2 CHECK
(col_1 IN ('abc', 'ghi', 'mno', 'stu', 'yz ') AND
col_3 IN ('def', 'jkl', 'pqr', 'vwx', 'zyx'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #   non-empty key sequenced table with assertion based on contents of
    #   another table  --  THIS IS A NEGATIVE TEST and therefore should
    #   get an error
    stmt = """alter table keytaba 
add constraint C3 CHECK (col_1 NOT IN (SELECT col_1 FROM enttaba));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4089')
    
    #  unique assertion name for the table BUT NOT FOR THE CATALOG
    stmt = """alter table keytabb 
add constraint C4 check (col_3 < 999);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  assertion with an expression in it
    stmt = """alter table keytabb 
add constraint C5 check ((col_1 * 3) > col_3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  create assertion on partitioned entry sequenced table
    stmt = """alter table enttaba 
add constraint C6 check (col_2 > 100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #   create assertion on SYSKEY of relative table
    #   this is a NEGATIVE test; assertions cannot be made against syskeys
    stmt = """alter table reltaba 
add constraint C7 check (syskey >= 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1139')
    
    #   create assertion on SYSKEY of entry sequenced table
    #   this is a NEGATIVE test; assertions cannot be made against
    #   syskeys
    stmt = """alter table enttaba 
add constraint C8 check (syskey >= 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    #   create assertion on SYSKEY of key sequenced table
    #   this is a NEGATIVE test; assertions cannot be made against
    #   syskeys
    stmt = """alter table keytabb 
add constraint C9 check (syskey >= 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1139')
    
    stmt = """control query default query_cache reset;"""
    output = _dci.cmdexec(stmt)
    stmt = """showcontrol query default query_cache;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test003(desc="""a16"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A16
    #  Description:        Insert and Update some objects
    #  Purpose:            Insert and update tables with data that
    #                      meets the assertion criteria
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #   insert record into keytaba
    ##expectfile ${test_dir}/a16exp a16s0
    stmt = """INSERT INTO keytaba VALUES ('abc', 654, 'jlm');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')
    
    #  update record in keytaba
    stmt = """UPDATE keytaba SET col_2 = 777 WHERE col_1 = 'yz';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from keytaba;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s1')
    
    _testmgr.testcase_end(desc)

def test004(desc="""a17"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A17
    #  Description:        This test verifies DROP CONSTRAINTs;
    #                      try inserts and updates on the tables
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """alter table reltaba 
drop constraint c1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table reltaba 
drop constraint c7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1005')
    
    stmt = """alter table keytaba 
drop constraint c2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table keytaba 
drop constraint c3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1005')
    
    stmt = """alter table keytabb 
drop constraint c4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table keytabb 
drop constraint c5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table keytabb 
drop constraint c9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1005')
    
    stmt = """alter table enttaba 
drop constraint c6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table enttaba 
drop constraint c8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1005')
    
    #  insert into reltaba
    stmt = """INSERT INTO reltaba VALUES ('abc', 777, 'xyz');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  update keytaba
    stmt = """UPDATE keytaba SET col_1 = 'hij' WHERE col_1 = 'abc';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    #  insert into keytabb
    stmt = """INSERT INTO keytabb VALUES (123, 'ats', 852);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  update enttaba
    stmt = """UPDATE enttaba SET col_2 = 77;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    
    # ---------------------------------
    # Clean up the tables
    # ---------------------------------
    stmt = """drop view entviewa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table reltaba;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table keytaba;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table keytabb;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table enttaba;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #               End of test cases ARKT0039
    _testmgr.testcase_end(desc)

