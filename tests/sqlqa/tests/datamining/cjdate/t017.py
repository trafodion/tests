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
    
def test001(desc="""test017"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test017
    # JClear
    # 1999-06-02
    # CJDate tests (5th ed. p162): query with UNION (and the evil UNION ALL)
    # "Get part numbers for parts that either weigh more than 16 pounds or
    #  are supplied by supplier S2 (or both)"
    #
    stmt = """select pnum
from p 
where weight > 16    

union    

select pnum
from spj 
where snum = 's2'
order by pnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test017.exp""", 's1')
    # expect 4 ordered rows with values p2 p3 p5 p6
    
    stmt = """select pnum
from p 
where weight > 16    

union all    

select pnum
from spj 
where snum = 's2'
order by pnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test017.exp""", 's2')
    # expect 11 ordered rows with values p2 p3 p3 p3 p3 p3 p3 p3 p3 p5 p6
    
    #- select pnum
    #-   from vpp
    #-     where weight > 16
    
    #-  union
    
    #- select pnum
    #-   from vpspj
    #-     where snum = 's2'
    #-       order by pnum;
    # expect 4 ordered rows with values p2 p3 p5 p6
    
    #- select pnum
    #-   from vpp
    #-     where weight > 16
    
    #-  union all
    
    #- select pnum
    #-   from vpspj
    #-     where snum = 's2'
    #-       order by pnum;
    # expect 11 ordered rows with values p2 p3 p3 p3 p3 p3 p3 p3 p3 p5 p6
    
    stmt = """select pnum
from hpp 
where weight > 16    

union    

select pnum
from hpspj 
where snum = 's2'
order by pnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test017.exp""", 's3')
    # expect 4 ordered rows with values p2 p3 p5 p6
    
    stmt = """select pnum
from hpp 
where weight > 16    

union all    

select pnum
from hpspj 
where snum = 's2'
order by pnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test017.exp""", 's4')
    # expect 11 ordered rows with values p2 p3 p3 p3 p3 p3 p3 p3 p3 p5 p6
    
    _testmgr.testcase_end(desc)

