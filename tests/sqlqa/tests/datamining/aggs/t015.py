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
    
def test001(desc="""test015"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test015
    # empty.sql
    # jclear
    # 22 Apr 1997
    # Test for the new aggreate functions.
    # Tests all the aggregates, as well as Variance and StdDev, on an
    # integer column of an empty table.
    stmt = """delete from ints500;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 500)
    
    stmt = """select count (*) from ints500;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test015exp""", 'test015b')
    # expect count of 0
    
    stmt = """select
Count (*) as "Count",
Avg (int500) as "Average",
Sum (int500) as "Sum",
Variance (int500) as "PVar",
Min (int500) as "Min",
StdDev (int500) as "PStDev",
Max (int500) as "Max"
from ints500;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test015exp""", 'test015c')
    # expect 1 row with 0 for the count and nulls for the rest
    
    # restore the table
    stmt = """insert into ints500 
select * from in500bak;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 500)
    
    stmt = """select count (*) from ints500;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test015exp""", 'test015e')
    # expect count = 500
    
    _testmgr.testcase_end(desc)

