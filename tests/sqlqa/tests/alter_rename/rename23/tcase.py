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

# A01 ALTER TABLE RENAME CASCADE (empty, old before new)
# A02 ALTER TABLE RENAME CASCADE (empty, new before old)
# A03 ALTER TABLE RENAME CASCADE (non-empty, old before new)
# A04 ALTER TABLE RENAME CASCADE (non-empty, new before old)
# A05 ALTER TABLE RENAME CASCADE (large, old before new)
# A06 ALTER TABLE RENAME CASCADE (large, new before old)

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""ALTER TABLE RENAME CASCADE (empty, old before new)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Alter table rename
    # Table: empty, local, no partitions, no constraints, no dependent objects
    # Check for old name before new name
    # Verify new name exist, old name does not exist
    
    # table
    stmt = """select * from tab_emp_original_01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # showddl
    stmt = """showddl tab_emp_original_01;"""
    output = _dci.cmdexec(stmt)
    
    # **********************************
    
    stmt = """alter table tab_emp_original_01 rename to tab_emp_new_01 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from tab_emp_original_01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    stmt = """select * from tab_emp_new_01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # **********************************
    
    # showddl
    stmt = """showddl tab_emp_original_01;"""
    output = _dci.cmdexec(stmt)
    stmt = """showddl tab_emp_new_01;"""
    output = _dci.cmdexec(stmt)
    
    # table
    stmt = """select * from tab_emp_original_01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    stmt = """select * from tab_emp_new_01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # insert
    stmt = """insert into tab_emp_original_01 values (1,'eeeeeeee',999999,999999,11,'test_constraint','YZABCDEF',1001,11,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    stmt = """insert into tab_emp_original_01 values (1,'eeeeeeee',999999,999999,11,'test_constraint','YZABCDEF',1001,11,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    stmt = """insert into tab_emp_original_01 values (1,'eeeeeeee',999999,999999,11,'test_constraint','YZABCDEF',NULL,NULL,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    stmt = """insert into tab_emp_new_01 values (1,'eeeeeeee',999999,999999,11,'test_constraint','YZABCDEF',1001,11,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab_emp_new_01 values (1,'eeeeeeee',999999,999999,11,'test_constraint','YZABCDEF',1001,11,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab_emp_new_01 values (1,'eeeeeeee',999999,999999,11,'test_constraint','YZABCDEF',NULL,NULL,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # table
    stmt = """select * from tab_emp_original_01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    stmt = """select * from tab_emp_new_01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a23exp""", """a01s02""")
    
    _testmgr.testcase_end(desc)

def test002(desc="""ALTER TABLE RENAME CASCADE (empty, new before old)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Alter table rename
    # Table: empty, local, no partitions, no constraints, no dependent objects
    # Check for new name before old name
    # Verify new name exist, old name does not exist
    
    # table
    stmt = """select * from tab_emp_original_02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # showddl
    stmt = """showddl tab_emp_original_02;"""
    output = _dci.cmdexec(stmt)
    
    # **********************************
    
    stmt = """alter table tab_emp_original_02 rename to tab_emp_new_02 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from tab_emp_new_02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select * from tab_emp_original_02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    # **********************************
    
    # table
    stmt = """select * from tab_ten_original_03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a23exp""", """a03s01""")
    
    # showddl
    stmt = """showddl tab_ten_original_03;"""
    output = _dci.cmdexec(stmt)
    
    # **********************************
    
    stmt = """alter table tab_ten_original_03 rename to tab_ten_new_03 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from tab_ten_original_03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    stmt = """select * from tab_ten_new_03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a23exp""", """a03s01""")
    
    # **********************************
    
    # showddl
    stmt = """showddl tab_ten_original_03;"""
    output = _dci.cmdexec(stmt)
    stmt = """showddl tab_ten_new_03;"""
    output = _dci.cmdexec(stmt)
    
    # table
    stmt = """select * from tab_ten_original_03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    stmt = """select * from tab_ten_new_03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a23exp""", """a03s01""")
    
    # insert
    stmt = """insert into tab_ten_original_03 values (1,'eeeeeeee',999999,999999,11,'test_constraint','YZABCDEF',1001,11,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    stmt = """insert into tab_ten_original_03 values (1,'eeeeeeee',999999,999999,11,'test_constraint','YZABCDEF',1001,11,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    stmt = """insert into tab_ten_original_03 values (1,'eeeeeeee',999999,999999,11,'test_constraint','YZABCDEF',NULL,NULL,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    stmt = """insert into tab_ten_new_03 values (1,'eeeeeeee',999999,999999,11,'test_constraint','YZABCDEF',1001,11,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab_ten_new_03 values (1,'eeeeeeee',999999,999999,11,'test_constraint','YZABCDEF',1001,11,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab_ten_new_03 values (1,'eeeeeeee',999999,999999,11,'test_constraint','YZABCDEF',NULL,NULL,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # table
    stmt = """select * from tab_ten_original_03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    stmt = """select * from tab_ten_new_03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a23exp""", """a03s02""")
    
    _testmgr.testcase_end(desc)

def test003(desc="""ALTER TABLE RENAME CASCADE (non-empty, new before old)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Alter table rename
    # Table: non-empty, local, no partitions, no constraints, no dependent objects
    # Check for new name before old name
    # Verify new name exist, old name does not exist
    
    # table
    stmt = """select * from tab_ten_original_04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a23exp""", """a04s01""")
    
    # showddl
    stmt = """showddl tab_ten_original_04;"""
    output = _dci.cmdexec(stmt)
    
    # **********************************
    
    stmt = """alter table tab_ten_original_04 rename to tab_ten_new_04 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from tab_ten_new_04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a23exp""", """a04s01""")
    
    stmt = """select * from tab_ten_original_04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    # **********************************
    
    # showddl
    stmt = """showddl tab_ten_new_04;"""
    output = _dci.cmdexec(stmt)
    stmt = """showddl tab_ten_original_04;"""
    output = _dci.cmdexec(stmt)
    
    # table
    stmt = """select * from tab_ten_new_04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a23exp""", """a04s01""")
    stmt = """select * from tab_ten_original_04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    # insert
    stmt = """insert into tab_ten_new_04 values (1,'eeeeeeee',999999,999999,11,'test_constraint','YZABCDEF',1001,11,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab_ten_new_04 values (1,'eeeeeeee',999999,999999,11,'test_constraint','YZABCDEF',1001,11,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab_ten_new_04 values (1,'eeeeeeee',999999,999999,11,'test_constraint','YZABCDEF',NULL,NULL,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab_ten_original_04 values (1,'eeeeeeee',999999,999999,11,'test_constraint','YZABCDEF',1001,11,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    stmt = """insert into tab_ten_original_04 values (1,'eeeeeeee',999999,999999,11,'test_constraint','YZABCDEF',1001,11,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    stmt = """insert into tab_ten_original_04 values (1,'eeeeeeee',999999,999999,11,'test_constraint','YZABCDEF',NULL,NULL,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    # table
    stmt = """select * from tab_ten_new_04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a23exp""", """a04s02""")
    stmt = """select * from tab_ten_original_04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    _testmgr.testcase_end(desc)

def test004(desc="""ALTER TABLE RENAME CASCADE (large, old before new)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Alter table rename
    # Table: large, local, no partitions, no constraints, no dependent objects
    # Check for old name before new name
    # Verify new name exist, old name does not exist
    
    # table
    stmt = """select count(*) from tab_lrg_original_05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a23exp""", """a05s01""")
    
    # showddl
    stmt = """showddl tab_lrg_original_05;"""
    output = _dci.cmdexec(stmt)
    
    # **********************************
    
    stmt = """alter table tab_lrg_original_05 rename to tab_lrg_new_05 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select count(*) from tab_lrg_original_05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    stmt = """select count(*) from tab_lrg_new_05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a23exp""", """a05s01""")
    
    # **********************************
    
    # showddl
    stmt = """showddl tab_lrg_original_05;"""
    output = _dci.cmdexec(stmt)
    stmt = """showddl tab_lrg_new_05;"""
    output = _dci.cmdexec(stmt)
    
    # table
    stmt = """select count(*) from tab_lrg_original_05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    stmt = """select count(*) from tab_lrg_new_05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a23exp""", """a05s01""")
    
    # insert
    stmt = """insert into tab_lrg_original_05 values (1,'eeeeeeee',999999,999999,11,'test_constraint','YZABCDEF',1001,11,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    stmt = """insert into tab_lrg_original_05 values (1,'eeeeeeee',999999,999999,11,'test_constraint','YZABCDEF',1001,11,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    stmt = """insert into tab_lrg_original_05 values (1,'eeeeeeee',999999,999999,11,'test_constraint','YZABCDEF',NULL,NULL,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    stmt = """insert into tab_lrg_new_05 values (1,'eeeeeeee',999999,999999,11,'test_constraint','YZABCDEF',1001,11,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab_lrg_new_05 values (1,'eeeeeeee',999999,999999,11,'test_constraint','YZABCDEF',1001,11,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab_lrg_new_05 values (1,'eeeeeeee',999999,999999,11,'test_constraint','YZABCDEF',NULL,NULL,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # table
    stmt = """select count(*) from tab_lrg_original_05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    stmt = """select count(*) from tab_lrg_new_05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a23exp""", """a05s02""")
    
    _testmgr.testcase_end(desc)

def test005(desc="""ALTER TABLE RENAME CASCADE (large, new before old)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Alter table rename
    # Table: large, local, no partitions, no constraints, no dependent objects
    # Check for new name before old name
    # Verify new name exist, old name does not exist
    
    # table
    stmt = """select count(*) from tab_lrg_original_06;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a23exp""", """a06s01""")
    
    # showddl
    stmt = """showddl tab_lrg_original_06;"""
    output = _dci.cmdexec(stmt)
    
    # **********************************
    
    stmt = """alter table tab_lrg_original_06 rename to tab_lrg_new_06 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select count(*) from tab_lrg_new_06;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a23exp""", """a06s01""")
    
    stmt = """select count(*) from tab_lrg_original_06;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    # **********************************
    
    # showddl
    stmt = """showddl tab_lrg_new_06;"""
    output = _dci.cmdexec(stmt)
    stmt = """showddl tab_lrg_original_06;"""
    output = _dci.cmdexec(stmt)
    
    # table
    stmt = """select count(*) from tab_lrg_new_06;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a23exp""", """a06s01""")
    stmt = """select count(*) from tab_lrg_original_06;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    # insert
    stmt = """insert into tab_lrg_new_06 values (1,'eeeeeeee',999999,999999,11,'test_constraint','YZABCDEF',1001,11,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab_lrg_new_06 values (1,'eeeeeeee',999999,999999,11,'test_constraint','YZABCDEF',1001,11,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab_lrg_new_06 values (1,'eeeeeeee',999999,999999,11,'test_constraint','YZABCDEF',NULL,NULL,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab_lrg_original_06 values (1,'eeeeeeee',999999,999999,11,'test_constraint','YZABCDEF',1001,11,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    stmt = """insert into tab_lrg_original_06 values (1,'eeeeeeee',999999,999999,11,'test_constraint','YZABCDEF',1001,11,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    stmt = """insert into tab_lrg_original_06 values (1,'eeeeeeee',999999,999999,11,'test_constraint','YZABCDEF',NULL,NULL,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    # table
    stmt = """select count(*) from tab_lrg_new_06;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a23exp""", """a06s02""")
    stmt = """select count(*) from tab_lrg_original_06;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    _testmgr.testcase_end(desc)

