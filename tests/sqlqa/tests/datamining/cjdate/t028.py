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
    
def test001(desc="""test028"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test028
    # JClear
    # 1999-06-03
    # CJDate tests (5th ed. p175): Nested subqueries with IN
    # Exercise 6.25
    # "Get supplier numbers for suppliers supplying at least one part
    #  supplied by at least one supplier who supplies at least one red part."
    #
    stmt = """select distinct snum
from spj 
where pnum in
(select pnum
from spj 
where snum in
(select snum
from spj 
where pnum in
(select pnum
from p 
where color = 'red')))
order by snum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test028.exp""", 's1')
    # expect 5 rows with values in order: s1 s2 s3 s4 s5
    
    #- select distinct snum
    #-   from vpspj
    #-     where pnum in
    #-       (select pnum
    #-          from vpspj
    #-            where snum in
    #-   	     (select snum
    #-   	        from vpspj
    #-   	          where pnum in
    #-   	            (select pnum
    #-                        from vpp
    #-                          where color = 'red')))
    #- 			   order by snum;
    # expect 5 rows with values in order: s1 s2 s3 s4 s5
    
    stmt = """select distinct snum
from hpspj 
where pnum in
(select pnum
from hpspj 
where snum in
(select snum
from hpspj 
where pnum in
(select pnum
from hpp 
where color = 'red')))
order by snum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test028.exp""", 's2')
    # expect 5 rows with values in order: s1 s2 s3 s4 s5
    
    _testmgr.testcase_end(desc)

