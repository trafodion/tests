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
    
def test001(desc="""test034"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test034
    # JClear
    # 1999-06-03
    # CJDate tests (5th ed. p176): NOT EXISTS nested
    # Exercise 6.34
    # "Get part numbers for parts supplied to all projects in London."
    #
    stmt = """select distinct pnum
from spj x
where not exists
(select *
from j 
where city = 'London'
and not exists
(select *
from spj y
where y.pnum = x.pnum
and y.jnum = j.jnum))
order by pnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test034.exp""", 's1')
    # expect p3 p5
    
    #- select distinct pnum
    #-   from vpspj x
    #-     where not exists
    #-       (select *
    #-          from vpj
    #- 	   where city = 'London'
    #- 	     and not exists
    #- 	       (select *
    #- 	          from vpspj y
    #- 		    where y.pnum = x.pnum
    #- 		      and y.jnum = vpj.jnum))
    #- 		        order by pnum;
    # expect p3 p5
    
    stmt = """select distinct pnum
from hpspj x
where not exists
(select *
from hpj 
where city = 'London'
and not exists
(select *
from hpspj y
where y.pnum = x.pnum
and y.jnum = hpj.jnum))
order by pnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test034.exp""", 's2')
    # expect p3 p5
    
    # Mixed tables
    stmt = """select distinct pnum
from hpspj x
where not exists
(select *
from j 
where city = 'London'
and not exists
(select *
from hpspj y
where y.pnum = x.pnum
and y.jnum = j.jnum))
order by pnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test034.exp""", 's3')
    # expect p3 p5
    
    _testmgr.testcase_end(desc)

