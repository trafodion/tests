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
    
def test001(desc="""test032"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test032
    # JClear
    # 1999-06-03
    # CJDate tests (5th ed. p176): NOT EXISTS with nested IN selects
    # Exercise 6.32
    # "Get project numbers for projects not supplied with any red part
    #  by any London supplier."
    #
    stmt = """select jnum
from j 
where not exists
(select *
from spj 
where jnum =j.jnum
and pnum in
(select pnum
from p 
where color = 'red')
and snum in
(select snum
from s 
where city = 'London'))
order by jnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test032.exp""", 's1')
    # expext 3 ordered rows with values: j2 j5 j6
    
    #- select jnum
    #-   from vpj
    #-     where not exists
    #-       (select *
    #-          from vpspj
    #- 	   where jnum = vpj.jnum
    #- 	     and pnum in
    #- 	       (select pnum
    #- 	          from vpp
    #- 		    where color = 'red')
    #-              and snum in
    #- 	       (select snum
    #- 	          from vps
    #- 		    where city = 'London'))
    #-       order by jnum;
    # expext 3 ordered rows with values: j2 j5 j6
    
    # this query mixes plain, HP tables
    stmt = """select jnum
from j 
where not exists
(select *
from hpspj 
where jnum = j.jnum
and pnum in
(select pnum
from p 
where color = 'red')
and snum in
(select snum
from hps 
where city = 'London'))
order by jnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test032.exp""", 's2')
    # expext 3 ordered rows with values: j2 j5 j6
    
    stmt = """select jnum
from hpj 
where not exists
(select *
from hpspj 
where jnum = hpj.jnum
and pnum in
(select pnum
from hpp 
where color = 'red')
and snum in
(select snum
from hps 
where city = 'London'))
order by jnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test032.exp""", 's3')
    # expext 3 ordered rows with values: j2 j5 j6
    
    _testmgr.testcase_end(desc)

