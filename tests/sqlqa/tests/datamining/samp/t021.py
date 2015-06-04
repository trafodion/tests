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
    
def test001(desc="""test021"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test021
    # JClear
    # 1999-02-01
    # Sampling tests: random sampling (with a param)
    #
    stmt = """set param ?ten 10;"""
    output = _dci.cmdexec(stmt)
    
    # make sure the temp tables are empty
    stmt = """delete from tempt1;"""
    output = _dci.cmdexec(stmt)
    stmt = """delete from tempt2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into tempt1 (intcol)
select count (*) from vwsamptb1 
where a between 0 and 100
sample random 10 percent rows
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # pass if 1 row is inserted
    
    stmt = """select count (*) from tempt1 
where intcol between 0 and 26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test021.exp""", 's2')
    # expect count = 1
    
    stmt = """update tempt1  set intcol =
(select count (*) from vwsamptb1 
where a > -666
sample random 10 percent);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    # pass if 1 row is updated
    
    stmt = """select count (*) from tempt1 
where intcol between 0 and 26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test021.exp""", 's4')
    # expect count = 1
    
    #- params not supported yet XXXXX
    #- update tempt1  set intcol =
    #-   (select count (*) from vwsamptb1
    #-     where a >= 0 and a <= 100
    #-       sample random ?ten percent rows);
    #- -- pass if 1 row is updated
    
    #- select count (*) from tempt1
    #-   where intcol between 3 and 19;
    #- -- expect count = 1
    
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    
    ##expectfile ${test_dir}/test021.exp s5
    stmt = """insert into tempt1 
select a, b, c from vwsamptb1 
sample random 10 percent rows;"""
    output = _dci.cmdexec(stmt)
    # pass if 0-26 rows are inserted
    
    stmt = """insert into tempt2 (intcol)
select count (*) from tempt1 
where intcol between 0 and 26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # pass if 1 row is inserted
    
    stmt = """select count (*) from tempt2;"""
    output = _dci.cmdexec(stmt)
    # _dci.expect_file(output, defs.test_dir + """/test021.exp""", 's7')
    # expect count = 1
    
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

