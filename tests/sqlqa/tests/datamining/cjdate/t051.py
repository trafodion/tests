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
    
def test001(desc="""test051"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test051
    # JClear
    # 2000-10-03
    # UNION of test013 subquery with NOT EXISTS
    #          test014 subquery with NOT IN
    #          test015 subquery with EXISTS
    # CJDate tests 5th ed. pp 160, 161 & 175
    #
    stmt = """select sname
from s 
where not exists
(select *
from spj 
where snum = s.snum
and pnum = 'p2')
union
select sname
from s 
where snum not in
(select snum
from spj 
where pnum = 'p2')
union
select sname
from s 
where exists
(select *
from p 
where exists
(select *
from spj 
where snum = s.snum
and pnum = p.pnum))
order by sname desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test051.exp""", 's1')
    
    # VP tables
    #- select sname
    #-   from vps
    #-     where not exists
    #-       (select *
    #-          from vpspj
    #-            where snum = vps.snum
    #-              and pnum = 'p2')
    #- union
    #- select sname
    #-   from vps
    #-     where snum not in
    #-       (select snum
    #-          from vpspj
    #-            where pnum = 'p2')
    #- union
    #- select sname
    #-   from vps
    #-     where exists
    #-       (select *
    #-          from vpp
    #-            where exists
    #-              (select *
    #-                 from vpspj
    #-                   where snum = vps.snum
    #-                     and pnum = vpp.pnum))
    #-         order by sname desc;
    
    # HP tables
    stmt = """select sname
from hps 
where not exists
(select *
from hpspj 
where snum = hps.snum
and pnum = 'p2')
union
select sname
from hps 
where snum not in
(select snum
from hpspj 
where pnum = 'p2')
union
select sname
from hps 
where exists
(select *
from hpp 
where exists
(select *
from hpspj 
where snum = hps.snum
and pnum = hpp.pnum))
order by sname desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test051.exp""", 's2')
    
    _testmgr.testcase_end(desc)

