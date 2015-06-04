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
    
def test001(desc="""test037"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test037
    # JClear
    # 1999-06-03
    # CJDate tests (5th ed. p178): IN .. OR .. IN
    # Exercise 6.46
    # "Get part numbers for parts that are supplied either by a London
    #  supplier or to a London project."
    #
    stmt = """select distinct pnum
from spj 
where snum in
(select snum
from s 
where city = 'London')
or jnum in
(select jnum
from j 
where city = 'London')
order by pnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test037.exp""", 's1')
    # expect 4 rows in order with values p1 p3 p5 p6
    
    #- select distinct pnum
    #-   from vpspj
    #-     where snum in
    #-       (select snum
    #-          from vps
    #- 	   where city = 'London')
    #-     or jnum in
    #-       (select jnum
    #-          from vpj
    #-            where city = 'London')
    #- 	     order by pnum;
    # expect 4 rows in order with values p1 p3 p5 p6
    
    stmt = """select distinct pnum
from hpspj 
where snum in
(select snum
from hps 
where city = 'London')
or jnum in
(select jnum
from hpj 
where city = 'London')
order by pnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test037.exp""", 's2')
    # expect 4 rows in order with values p1 p3 p5 p6
    
    # mixed tables
    stmt = """select distinct pnum
from spj 
where snum in
(select snum
from hps 
where city = 'London')
or jnum in
(select jnum
from hpj 
where city = 'London')
order by pnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test037.exp""", 's3')
    # expect 4 rows in order with values p1 p3 p5 p6
    
    _testmgr.testcase_end(desc)

