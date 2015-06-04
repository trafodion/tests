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

# A01 ALTER TABLE RENAME SYNTAX (invalid rename to same table - 1R)
# A02 ALTER TABLE RENAME SYNTAX (invalid rename to same table - 2R)
# A03 ALTER TABLE RENAME SYNTAX (invalid rename to same table - 3R)
# A04 ALTER TABLE RENAME SYNTAX (invalid rename to existing table - 1R)
# A05 ALTER TABLE RENAME SYNTAX (invalid rename to existing table - 2R)
# A06 ALTER TABLE RENAME SYNTAX (invalid rename to existing table - 3R)
# A07 ALTER TABLE RENAME SYNTAX (invalid rename to new table - 1R)
# A08 ALTER TABLE RENAME SYNTAX (invalid rename to new table - 2R)
# A09 ALTER TABLE RENAME SYNTAX (invalid rename to new table - 3R)

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""ALTER TABLE RENAME SYNTAX (invalid rename to same table - 1R)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Negative testing: Alter table rename to same table
    # Check that operation failed and did not cause side-effects
    # Table: local and remote partitions, empty
    # Rename statement: old-name use format tablename only, new-name use various combinations
    
    stmt = """select * from tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """alter table tab_rem_emp_original rename to tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """insert into tab_rem_emp_original values (0,'zzzzzzzzzzzzzzzz','yyyyyyyy',99999,10,9.99,1,'xxxxxxxx',999,'wwww');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from tab_rem_emp_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a01s02""")
    stmt = """update tab_rem_emp_original set char1_10 = 'vvvv' where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a01s03""")
    stmt = """delete from tab_rem_emp_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """select * from tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """alter table tab_rem_emp_original rename to """ + defs.my_schema + """.tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table tab_rem_emp_original rename to """ + defs.my_schema3 + """.tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table tab_rem_emp_original rename to """ + defs.my_schema2 + """.tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table tab_rem_emp_original rename to """ + defs.my_schema + """.tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table tab_rem_emp_original rename to """ + defs.my_schema3 + """.tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table tab_rem_emp_original rename to """ + defs.my_schema2 + """.tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table tab_rem_emp_original rename to """ + defs.my_schema7 + """.tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table tab_rem_emp_original rename to """ + defs.my_schema9 + """.tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table tab_rem_emp_original rename to """ + defs.my_schema8 + """.tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table tab_rem_emp_original rename to """ + defs.my_schema4 + """.tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table tab_rem_emp_original rename to """ + defs.my_schema6 + """.tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table tab_rem_emp_original rename to """ + defs.my_schema5 + """.tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """insert into tab_rem_emp_original values (0,'zzzzzzzzzzzzzzzz','yyyyyyyy',99999,10,9.99,1,'xxxxxxxx',999,'wwww');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from tab_rem_emp_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a01s02""")
    stmt = """update tab_rem_emp_original set char1_10 = 'vvvv' where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a01s03""")
    stmt = """delete from tab_rem_emp_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """select * from tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    _testmgr.testcase_end(desc)

def test002(desc="""ALTER TABLE RENAME SYNTAX (invalid rename to same table - 2R)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Negative testing: Alter table rename to same table
    # Check that operation failed and did not cause side-effects
    # Table: local and remote partitions, non-empty
    # Rename statement: old-name use format schema.tablename, new-name use various combinations
    
    stmt = """select * from tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a02s11""")
    
    stmt = """alter table tab_rem_ten_original rename to tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """insert into tab_rem_ten_original values (0,'zzzzzzzzzzzzzzzz','yyyyyyyy',99999,10,9.99,1,'xxxxxxxx',999,'wwww');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from tab_rem_ten_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a02s12""")
    stmt = """update tab_rem_ten_original set char1_10 = 'vvvv' where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a02s13""")
    stmt = """delete from tab_rem_ten_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """select * from tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a02s11""")
    
    stmt = """alter table """ + defs.my_schema + """.tab_rem_ten_original rename to tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    stmt = """alter table """ + defs.my_schema + """.tab_rem_ten_original rename to """ + defs.my_schema + """.tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_ten_original rename to """ + defs.my_schema3 + """.tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_ten_original rename to """ + defs.my_schema2 + """.tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_ten_original rename to """ + defs.my_schema + """.tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_ten_original rename to """ + defs.my_schema3 + """.tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_ten_original rename to """ + defs.my_schema2 + """.tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_ten_original rename to """ + defs.my_schema7 + """.tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_ten_original rename to """ + defs.my_schema9 + """.tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_ten_original rename to """ + defs.my_schema8 + """.tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_ten_original rename to """ + defs.my_schema4 + """.tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_ten_original rename to """ + defs.my_schema6 + """.tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_ten_original rename to """ + defs.my_schema5 + """.tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """insert into tab_rem_ten_original values (0,'zzzzzzzzzzzzzzzz','yyyyyyyy',99999,10,9.99,1,'xxxxxxxx',999,'wwww');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from tab_rem_ten_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a02s12""")
    stmt = """update tab_rem_ten_original set char1_10 = 'vvvv' where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a02s13""")
    stmt = """delete from tab_rem_ten_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """select * from tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a02s11""")
    
    _testmgr.testcase_end(desc)

def test003(desc="""ALTER TABLE RENAME SYNTAX (invalid rename to same table - 3R)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Negative testing: Alter table rename to same table
    # Check that operation failed and did not cause side-effects
    # Table: local and remote partitions, large
    # Rename statement: old-name use format catalog.schema.tablename, new-name use various combinations
    
    stmt = """select count(*) from tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a03s21""")
    
    stmt = """alter table tab_rem_lrg_original rename to tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """insert into tab_rem_lrg_original values (0,'zzzzzzzzzzzzzzzz','yyyyyyyy',99999,10,9.99,1,'xxxxxxxx',999,'wwww');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select count(*) from tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update statistics for table """ + defs.my_schema + """.tab_rem_lrg_original
on every column;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from tab_rem_lrg_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a03s22""")
    stmt = """update tab_rem_lrg_original set char1_10 = 'vvvv' where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select count(*) from tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a03s23""")
    stmt = """delete from tab_rem_lrg_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """select count(*) from tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a03s21""")
    
    stmt = """alter table """ + defs.my_schema + """.tab_rem_lrg_original rename to tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    stmt = """alter table """ + defs.my_schema + """.tab_rem_lrg_original rename to """ + defs.my_schema + """.tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_lrg_original rename to """ + defs.my_schema3 + """.tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_lrg_original rename to """ + defs.my_schema2 + """.tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_lrg_original rename to """ + defs.my_schema + """.tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_lrg_original rename to """ + defs.my_schema3 + """.tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_lrg_original rename to """ + defs.my_schema2 + """.tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_lrg_original rename to """ + defs.my_schema7 + """.tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_lrg_original rename to """ + defs.my_schema9 + """.tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_lrg_original rename to """ + defs.my_schema8 + """.tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_lrg_original rename to """ + defs.my_schema4 + """.tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_lrg_original rename to """ + defs.my_schema6 + """.tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_lrg_original rename to """ + defs.my_schema5 + """.tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """insert into tab_rem_lrg_original values (0,'zzzzzzzzzzzzzzzz','yyyyyyyy',99999,10,9.99,1,'xxxxxxxx',999,'wwww');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update statistics for table """ + defs.my_schema + """.tab_rem_lrg_original
on every column;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from tab_rem_lrg_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a03s22""")
    
    stmt = """update tab_rem_lrg_original set char1_10 = 'vvvv' where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select count(*) from tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a03s23""")
    
    stmt = """delete from tab_rem_lrg_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select count(*) from tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a03s21""")
    
    _testmgr.testcase_end(desc)

def test004(desc="""ALTER TABLE RENAME SYNTAX (invalid rename to existing table - 1R)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Negative testing: Alter table rename to existing table
    # Check that operation failed and did not cause side-effects
    # Table: local and remote partitions, empty
    # Rename statement: old-name use format schema.tablename, new-name use various combinations
    
    stmt = """select * from tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select count(*) from tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a04s32""")
    
    stmt = """alter table tab_rem_emp_original rename to tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """insert into tab_rem_emp_original values (0,'zzzzzzzzzzzzzzzz','yyyyyyyy',99999,10,9.99,1,'xxxxxxxx',999,'wwww');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from tab_rem_emp_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a04s33""")
    stmt = """update tab_rem_emp_original set char1_10 = 'vvvv' where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a04s34""")
    stmt = """delete from tab_rem_emp_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """select * from tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """insert into tab_rem_lrg_original values (0,'zzzzzzzzzzzzzzzz','yyyyyyyy',99999,10,9.99,1,'xxxxxxxx',999,'wwww');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update statistics for table """ + defs.my_schema + """.tab_rem_lrg_original
on every column;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from tab_rem_lrg_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a04s35""")
    stmt = """update tab_rem_lrg_original set char1_10 = 'vvvv' where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select count(*) from tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a04s36""")
    stmt = """delete from tab_rem_lrg_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """select count(*) from tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a04s32""")
    
    stmt = """alter table """ + defs.my_schema + """.tab_rem_emp_original rename to tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    stmt = """alter table """ + defs.my_schema + """.tab_rem_emp_original rename to """ + defs.my_schema + """.tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_emp_original rename to """ + defs.my_schema3 + """.tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_emp_original rename to """ + defs.my_schema2 + """.tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_emp_original rename to """ + defs.my_schema + """.tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_emp_original rename to """ + defs.my_schema3 + """.tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_emp_original rename to """ + defs.my_schema2 + """.tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_emp_original rename to """ + defs.my_schema7 + """.tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_emp_original rename to """ + defs.my_schema9 + """.tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_emp_original rename to """ + defs.my_schema8 + """.tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_emp_original rename to """ + defs.my_schema4 + """.tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_emp_original rename to """ + defs.my_schema6 + """.tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_emp_original rename to """ + defs.my_schema5 + """.tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """insert into tab_rem_emp_original values (0,'zzzzzzzzzzzzzzzz','yyyyyyyy',99999,10,9.99,1,'xxxxxxxx',999,'wwww');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from tab_rem_emp_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a04s33""")
    stmt = """update tab_rem_emp_original set char1_10 = 'vvvv' where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a04s34""")
    stmt = """delete from tab_rem_emp_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """select * from tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """insert into tab_rem_lrg_original values (0,'zzzzzzzzzzzzzzzz','yyyyyyyy',99999,10,9.99,1,'xxxxxxxx',999,'wwww');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update statistics for table """ + defs.my_schema + """.tab_rem_lrg_original
on every column;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from tab_rem_lrg_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a04s35""")
    
    stmt = """update tab_rem_lrg_original set char1_10 = 'vvvv' where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select count(*) from tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a04s36""")
    
    stmt = """delete from tab_rem_lrg_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select count(*) from tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a04s32""")
    
    _testmgr.testcase_end(desc)

def test005(desc="""ALTER TABLE RENAME SYNTAX (invalid rename to existing table - 2R)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Negative testing: Alter table rename to existing table
    # Check that operation failed and did not cause side-effects
    # Table: local and remote partitions, non-empty
    # Rename statement: old-name use format catalog.schema.tablename, new-name use various combinations
    
    stmt = """select * from tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a05s41""")
    stmt = """select * from tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """alter table tab_rem_ten_original rename to tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """insert into tab_rem_ten_original values (0,'zzzzzzzzzzzzzzzz','yyyyyyyy',99999,10,9.99,1,'xxxxxxxx',999,'wwww');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from tab_rem_ten_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a05s43""")
    stmt = """update tab_rem_ten_original set char1_10 = 'vvvv' where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a05s44""")
    stmt = """delete from tab_rem_ten_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """select * from tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a05s41""")
    
    stmt = """insert into tab_rem_emp_original values (0,'zzzzzzzzzzzzzzzz','yyyyyyyy',99999,10,9.99,1,'xxxxxxxx',999,'wwww');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from tab_rem_emp_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a05s45""")
    stmt = """update tab_rem_emp_original set char1_10 = 'vvvv' where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a05s46""")
    stmt = """delete from tab_rem_emp_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """select * from tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """alter table """ + defs.my_schema + """.tab_rem_ten_original rename to tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    stmt = """alter table """ + defs.my_schema + """.tab_rem_ten_original rename to """ + defs.my_schema + """.tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_ten_original rename to """ + defs.my_schema3 + """.tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_ten_original rename to """ + defs.my_schema2 + """.tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_ten_original rename to """ + defs.my_schema + """.tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_ten_original rename to """ + defs.my_schema3 + """.tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_ten_original rename to """ + defs.my_schema2 + """.tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_ten_original rename to """ + defs.my_schema7 + """.tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_ten_original rename to """ + defs.my_schema9 + """.tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_ten_original rename to """ + defs.my_schema8 + """.tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_ten_original rename to """ + defs.my_schema4 + """.tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_ten_original rename to """ + defs.my_schema6 + """.tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_ten_original rename to """ + defs.my_schema5 + """.tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """insert into tab_rem_ten_original values (0,'zzzzzzzzzzzzzzzz','yyyyyyyy',99999,10,9.99,1,'xxxxxxxx',999,'wwww');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from tab_rem_ten_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a05s43""")
    stmt = """update tab_rem_ten_original set char1_10 = 'vvvv' where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a05s44""")
    stmt = """delete from tab_rem_ten_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """select * from tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a05s41""")
    
    stmt = """insert into tab_rem_emp_original values (0,'zzzzzzzzzzzzzzzz','yyyyyyyy',99999,10,9.99,1,'xxxxxxxx',999,'wwww');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from tab_rem_emp_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a05s45""")
    stmt = """update tab_rem_emp_original set char1_10 = 'vvvv' where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a05s46""")
    stmt = """delete from tab_rem_emp_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """select * from tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    _testmgr.testcase_end(desc)

def test006(desc="""ALTER TABLE RENAME SYNTAX (invalid rename to existing table - 3R)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Negative testing: Alter table rename to existing table
    # Check that operation failed and did not cause side-effects
    # Table: local and remote partitions, large
    # Rename statement: old-name use format tablename only, new-name use various combinations
    
    stmt = """select count(*) from tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a06s51""")
    stmt = """select * from tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a06s52""")
    
    stmt = """alter table tab_rem_lrg_original rename to tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """insert into tab_rem_lrg_original values (0,'zzzzzzzzzzzzzzzz','yyyyyyyy',99999,10,9.99,1,'xxxxxxxx',999,'wwww');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update statistics for table """ + defs.my_schema + """.tab_rem_lrg_original
on every column;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from tab_rem_lrg_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a06s53""")
    
    stmt = """update tab_rem_lrg_original set char1_10 = 'vvvv' where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select count(*) from tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a06s54""")
    
    stmt = """delete from tab_rem_lrg_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select count(*) from tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a06s51""")
    
    stmt = """insert into tab_rem_ten_original values (0,'zzzzzzzzzzzzzzzz','yyyyyyyy',99999,10,9.99,1,'xxxxxxxx',999,'wwww');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from tab_rem_ten_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a06s55""")
    stmt = """update tab_rem_ten_original set char1_10 = 'vvvv' where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a06s56""")
    stmt = """delete from tab_rem_ten_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """select * from tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a06s52""")
    
    stmt = """alter table tab_rem_lrg_original rename to """ + defs.my_schema + """.tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table tab_rem_lrg_original rename to """ + defs.my_schema3 + """.tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table tab_rem_lrg_original rename to """ + defs.my_schema2 + """.tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table tab_rem_lrg_original rename to """ + defs.my_schema + """.tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table tab_rem_lrg_original rename to """ + defs.my_schema3 + """.tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table tab_rem_lrg_original rename to """ + defs.my_schema2 + """.tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table tab_rem_lrg_original rename to """ + defs.my_schema7 + """.tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table tab_rem_lrg_original rename to """ + defs.my_schema9 + """.tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table tab_rem_lrg_original rename to """ + defs.my_schema8 + """.tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table tab_rem_lrg_original rename to """ + defs.my_schema4 + """.tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table tab_rem_lrg_original rename to """ + defs.my_schema6 + """.tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table tab_rem_lrg_original rename to """ + defs.my_schema5 + """.tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """insert into tab_rem_lrg_original values (0,'zzzzzzzzzzzzzzzz','yyyyyyyy',99999,10,9.99,1,'xxxxxxxx',999,'wwww');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update statistics for table """ + defs.my_schema + """.tab_rem_lrg_original
on every column;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from tab_rem_lrg_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a06s53""")
    
    stmt = """update tab_rem_lrg_original set char1_10 = 'vvvv' where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select count(*) from tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a06s54""")
    
    stmt = """delete from tab_rem_lrg_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select count(*) from tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a06s51""")
    
    stmt = """insert into tab_rem_ten_original values (0,'zzzzzzzzzzzzzzzz','yyyyyyyy',99999,10,9.99,1,'xxxxxxxx',999,'wwww');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from tab_rem_ten_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a06s55""")
    stmt = """update tab_rem_ten_original set char1_10 = 'vvvv' where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a06s56""")
    stmt = """delete from tab_rem_ten_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """select * from tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a06s52""")
    
    _testmgr.testcase_end(desc)

def test007(desc="""ALTER TABLE RENAME SYNTAX (invalid rename to new table - 1R)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Negative testing: Alter table rename to new table
    # Check that operation failed and did not cause side-effects
    # Table: local and remote partitions, empty
    # Rename statement: old-name use format catalog.schema.tablename, new-name use various combinations
    
    stmt = """select * from tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """alter table tab_rem_emp_original rename to """ + defs.my_schema + """.tab_rem_new_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """insert into tab_rem_emp_original values (0,'zzzzzzzzzzzzzzzz','yyyyyyyy',99999,10,9.99,1,'xxxxxxxx',999,'wwww');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from tab_rem_emp_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a07s62""")
    stmt = """update tab_rem_emp_original set char1_10 = 'vvvv' where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a07s63""")
    stmt = """delete from tab_rem_emp_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """select * from tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """alter table """ + defs.my_schema + """.tab_rem_emp_original rename to """ + defs.my_schema3 + """.tab_rem_new_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_emp_original rename to """ + defs.my_schema2 + """.tab_rem_new_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_emp_original rename to """ + defs.my_schema + """.tab_rem_new_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_emp_original rename to """ + defs.my_schema3 + """.tab_rem_new_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_emp_original rename to """ + defs.my_schema2 + """.tab_rem_new_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_emp_original rename to """ + defs.my_schema7 + """.tab_rem_new_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_emp_original rename to """ + defs.my_schema9 + """.tab_rem_new_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_emp_original rename to """ + defs.my_schema8 + """.tab_rem_new_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_emp_original rename to """ + defs.my_schema4 + """.tab_rem_new_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_emp_original rename to """ + defs.my_schema6 + """.tab_rem_new_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_emp_original rename to """ + defs.my_schema5 + """.tab_rem_new_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """insert into tab_rem_emp_original values (0,'zzzzzzzzzzzzzzzz','yyyyyyyy',99999,10,9.99,1,'xxxxxxxx',999,'wwww');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from tab_rem_emp_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a07s62""")
    stmt = """update tab_rem_emp_original set char1_10 = 'vvvv' where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a07s63""")
    stmt = """delete from tab_rem_emp_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """select * from tab_rem_emp_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    _testmgr.testcase_end(desc)

def test008(desc="""ALTER TABLE RENAME SYNTAX (invalid rename to new table - 2R)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Negative testing: Alter table rename to new table
    # Check that operation failed and did not cause side-effects
    # Table: local and remote partitions, non-empty
    # Rename statement: old-name use format tablename only, new-name use various combinations
    
    stmt = """select * from tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a08s71""")
    
    stmt = """alter table tab_rem_ten_original rename to """ + defs.my_schema + """.tab_rem_new_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """insert into tab_rem_ten_original values (0,'zzzzzzzzzzzzzzzz','yyyyyyyy',99999,10,9.99,1,'xxxxxxxx',999,'wwww');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from tab_rem_ten_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a08s72""")
    stmt = """update tab_rem_ten_original set char1_10 = 'vvvv' where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a08s73""")
    stmt = """delete from tab_rem_ten_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """select * from tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a08s71""")
    
    stmt = """alter table tab_rem_ten_original rename to """ + defs.my_schema3 + """.tab_rem_new_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table tab_rem_ten_original rename to """ + defs.my_schema2 + """.tab_rem_new_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table tab_rem_ten_original rename to """ + defs.my_schema + """.tab_rem_new_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table tab_rem_ten_original rename to """ + defs.my_schema3 + """.tab_rem_new_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table tab_rem_ten_original rename to """ + defs.my_schema2 + """.tab_rem_new_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table tab_rem_ten_original rename to """ + defs.my_schema7 + """.tab_rem_new_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table tab_rem_ten_original rename to """ + defs.my_schema9 + """.tab_rem_new_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table tab_rem_ten_original rename to """ + defs.my_schema8 + """.tab_rem_new_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table tab_rem_ten_original rename to """ + defs.my_schema4 + """.tab_rem_new_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table tab_rem_ten_original rename to """ + defs.my_schema6 + """.tab_rem_new_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table tab_rem_ten_original rename to """ + defs.my_schema5 + """.tab_rem_new_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """insert into tab_rem_ten_original values (0,'zzzzzzzzzzzzzzzz','yyyyyyyy',99999,10,9.99,1,'xxxxxxxx',999,'wwww');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from tab_rem_ten_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a08s72""")
    stmt = """update tab_rem_ten_original set char1_10 = 'vvvv' where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a08s73""")
    stmt = """delete from tab_rem_ten_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """select * from tab_rem_ten_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a08s71""")
    
    _testmgr.testcase_end(desc)

def test009(desc="""ALTER TABLE RENAME SYNTAX (invalid rename to new table - 3R)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Negative testing: Alter table rename to new table
    # Check that operation failed and did not cause side-effects
    # Table: local and remote partitions, large
    # Rename statement: old-name use format schema.tablename, new-name use various combinations
    
    stmt = """select count(*) from tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a09s81""")
    
    stmt = """alter table tab_rem_lrg_original rename to """ + defs.my_schema + """.tab_rem_new_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """insert into tab_rem_lrg_original values (0,'zzzzzzzzzzzzzzzz','yyyyyyyy',99999,10,9.99,1,'xxxxxxxx',999,'wwww');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update statistics for table """ + defs.my_schema + """.tab_rem_lrg_original
on every column;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from tab_rem_lrg_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a09s82""")
    
    stmt = """update tab_rem_lrg_original set char1_10 = 'vvvv' where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select count(*) from tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a09s83""")
    
    stmt = """delete from tab_rem_lrg_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select count(*) from tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a09s81""")
    
    stmt = """alter table """ + defs.my_schema + """.tab_rem_lrg_original rename to """ + defs.my_schema3 + """.tab_rem_new_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_lrg_original rename to """ + defs.my_schema2 + """.tab_rem_new_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_lrg_original rename to """ + defs.my_schema + """.tab_rem_new_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_lrg_original rename to """ + defs.my_schema3 + """.tab_rem_new_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_lrg_original rename to """ + defs.my_schema2 + """.tab_rem_new_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_lrg_original rename to """ + defs.my_schema7 + """.tab_rem_new_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_lrg_original rename to """ + defs.my_schema9 + """.tab_rem_new_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_lrg_original rename to """ + defs.my_schema8 + """.tab_rem_new_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_lrg_original rename to """ + defs.my_schema4 + """.tab_rem_new_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_lrg_original rename to """ + defs.my_schema6 + """.tab_rem_new_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table """ + defs.my_schema + """.tab_rem_lrg_original rename to """ + defs.my_schema5 + """.tab_rem_new_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """insert into tab_rem_lrg_original values (0,'zzzzzzzzzzzzzzzz','yyyyyyyy',99999,10,9.99,1,'xxxxxxxx',999,'wwww');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update statistics for table """ + defs.my_schema + """.tab_rem_lrg_original
on every column;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from tab_rem_lrg_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a09s82""")
    
    stmt = """update tab_rem_lrg_original set char1_10 = 'vvvv' where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select count(*) from tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a09s83""")
    
    stmt = """delete from tab_rem_lrg_original where sbin0_uniq = 99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select count(*) from tab_rem_lrg_original;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", """a09s81""")
    
    _testmgr.testcase_end(desc)

