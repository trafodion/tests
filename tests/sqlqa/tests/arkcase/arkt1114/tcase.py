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
    
def test001(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1114:A02
    #  Description:        This test verifies fixes for CAST behavior.
    #
    # =================== End Test Case Header  ===================
    #
    #
    # Force autocommit:
    stmt = """SET transaction Autocommit on;"""
    output = _dci.cmdexec(stmt)

    stmt = """select char0_10, varchar5_10, sbin4_2
from BTA1P001 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    #
    #  Expect errors:
    stmt = """select char0_10
from BTA1P001 
where (char0_10 < NULL) or
(char0_10 > NULL)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4099')
    #
    stmt = """select varchar5_10
from BTA1P001 
where (varchar5_10 <> NULL)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4099')
    #
    stmt = """select sbin4_2
from BTA1P001 
where (sbin4_2 = NULL)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4099')
    #
    #  ---------------------------
    #
    #  Select from primary key (disallows NULL).
    #  Expect all
    
    #  Select from and compare columns that allow NULL.
    #  Expect rows as in global table:
    stmt = """select varchar0_nuniq, ubin1_n2, char2_2
from BTA1P005 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    #
    #  Expect errors:
    stmt = """select varchar0_nuniq
from BTA1P005 
where (varchar0_nuniq < NULL) or
(varchar0_nuniq > NULL)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4099')
    #
    stmt = """select ubin1_n2
from BTA1P005 
where (ubin1_n2 <> NULL)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4099')
    #
    stmt = """select char2_2
from BTA1P005 
where (char2_2 = NULL)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4099')
    #
    
    stmt = """Create table tA02 
(c1 varchar(25) not null primary key, c2 int)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  Should get syntax error.
    stmt = """Create view vA02 as
select 1 from tA02 
where c1 >= NULL and c1 < ('mmmmmm')
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4099')
    stmt = """Drop view vA02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    stmt = """Drop table tA02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test002(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1114:A03
    #  Description:        SQL Bug tests
    #                      Entry-order tables should not alter varchar length.
    #
    # =================== End Test Case Header  ===================
    #
    # Choose local schema.
    #
    # Create Entry sequenced table.
    
    stmt = """Create Table tentry (
c1 Int Not Null,
c2 Varchar (10)
) no partition
--   Store By Entry Order
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Insert Into tentry Values (1, 'avc'), (2, 'sjdkfl');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    #
    #  Attempt to write shorter varchar value -- should be rejected.
    #  Looking for Error 1031: A supplied numeric value exceeds the declared
    #  precision of the column, some of the supplied values for DECIMAL or VARCHAR
    #  columns are invalid, or the supplied row is too long.  Also, the NonStop
    #  Data Access Manager might have encountered a bad column in a stored row
    #  or a value in an update on a row that would change the length of a VARCHAR
    #  column in an entry-sequenced table
    #  Kind of a grab-bag, but at least this avoids data corruption.
    stmt = """Update tentry Set c2 = 'aaa';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    stmt = """Update tentry Set c2 = 'bb' Where c1 = 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    #  Expect 2 rows as entered ( 1 'aaa') (2 'aaa')
    stmt = """Select * From tentry;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    #
    #  Attempt to write longer varchar value -- should be rejected.
    stmt = """Update tentry Set c2 = 'aaaaaaaaa';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    stmt = """Update tentry Set c2 = 'REALLY BIG' Where c1 = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    #  Expect 2 rows as entered ( 1 'aaa') (2 'aaa')
    stmt = """Select * From tentry;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s5')
    #
    # Cleanup.
    stmt = """Drop Table tentry ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Create Entry sequenced table.
    stmt = """Create Table tentry (
c1 int not null,
c2 varchar (10),
c3 varchar (9),
c4 int not null
) no partition
--   Store By Entry Order
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Insert Into tentry Values (1, 'avc', 'a23', 1), (2, 'sjdkfl', 's23456', 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    #
    #  Attempt to write shorter varchar value -- should be rejected.
    stmt = """Update tentry Set c3 = 'aaa';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    stmt = """Update tentry Set c3 = 'bb' Where c1 = 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """Update tentry Set c2 = 'abc', c3='wxyz' Where c1 = 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    #  Expect 2 rows as entered
    stmt = """Select * From tentry;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s9')
    #
    #  Attempt to write longer varchar value -- should be rejected.
    stmt = """Update tentry Set c3 = 'aaaaaaaa';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    stmt = """Update tentry Set c3 = 'REAL LONG' Where c1 = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    #  Expect 2 rows as entered ( 1 'aaa') (2 'aaa')
    stmt = """Select * From tentry;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s12')
    
    # Then write SAME-LENGTH varchar value; should be accepted.
    stmt = """Update tentry Set c2 = 'NEW' Where c1 = 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """Update tentry Set c3 = 'YORKER' Where c1 = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    #  Expect 2 rows (1 'NEW' 'a23' 1) (2 'sjdkfl' 'YORKER' 2)
    stmt = """Select * From tentry;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s13')
    
    # Cleanup.
    stmt = """Drop Table tentry ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

