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
    
def test001(desc="""test027"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test027
    # JClear
    # 1999-06-03
    # CJDate tests (5th ed. p174): Join subquery with IN & NOT IN.
    # Exercise 6.22
    # "Get colours of parts supplied by supplier S1."
    #  added "not supplied" too
    #
    stmt = """select distinct color
from p 
where pnum in
(select pnum
from spj 
where snum = 's1')
order by color;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test027.exp""", 's1')
    # expect 1 row with color = red
    
    stmt = """select distinct color
from p 
where not pnum in
(select pnum
from spj 
where snum = 's1')
order by color desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test027.exp""", 's2')
    # expect 3 ordered rows with values: red green blue
    
    stmt = """select distinct color
from hpp 
where pnum in
(select pnum
from hpspj 
where snum = 's1')
order by color;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test027.exp""", 's3')
    # expect 1 row with color = red
    
    stmt = """select distinct color
from hpp 
where not pnum in
(select pnum
from hpspj 
where snum = 's1')
order by color desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test027.exp""", 's5')
    # expect 3 ordered rows with values: red green blue
    
    #- select distinct color
    #-   from vpp
    #-     where pnum in
    #-       (select pnum
    #-          from vpspj
    #- 	   where snum = 's1')
    #- 	     order by color;
    # expect 1 row with color = red
    
    #- select distinct color
    #-   from vpp
    #-     where not pnum in
    #-       (select pnum
    #-          from vpspj
    #- 	   where snum = 's1')
    #- 	     order by color desc;
    # expect 3 ordered rows with values: red green blue
    
    _testmgr.testcase_end(desc)

