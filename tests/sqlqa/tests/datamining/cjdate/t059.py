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
    
def test001(desc="""test059"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test059
    # JClear
    # 2000-10-05
    # UNION of test024 Simple query with between. Exercise 6.4
    #          test025 Simple query with between. Exercise 6.4
    # CJDate tests (5th ed. p173)
    #
    stmt = """select snum, pnum, jnum
from s, p, j 
where s.city = p.city
and p.city = j.city
union
select snum, pnum, jnum
from spj 
where qty between 300 and 750
order by snum desc, pnum desc, jnum asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test059.exp""", 's1')
    
    # expect 26 rows with the following values in order
    #    s5     p6      j4
    #    s5     p5      j4
    #    s5     p5      j5
    #    s4     p6      j3
    #    s4     p6      j5
    #    s4     p6      j7
    #    s4     p4      j5
    #    s4     p4      j7
    #    s4     p1      j5
    #    s4     p1      j7
    #    s3     p5      j1
    #    s3     p4      j2
    #    s3     p2      j1
    #    s2     p5      j1
    #    s2     p3      j1
    #    s2     p3      j4
    #    s2     p3      j5
    #    s2     p3      j6
    #    s2     p2      j1
    #    s1     p6      j5
    #    s1     p6      j7
    #    s1     p4      j5
    #    s1     p4      j7
    #    s1     p1      j4
    #    s1     p1      j5
    #    s1     p1      j7
    
    # VP tables
    #- select snum, pnum, jnum
    #-   from vps s, vpp p, vpj j
    #-     where s.city = p.city
    #-       and p.city = j.city
    #- union
    #- select snum, pnum, jnum
    #-   from vpspj
    #-     where qty between 300 and 750
    #-         order by snum desc, pnum desc, jnum asc;
    
    # HP tables
    stmt = """select snum, pnum, jnum
from hps s, hpp p, hpj j 
where s.city = p.city
and p.city = j.city
union
select snum, pnum, jnum
from hpspj 
where qty between 300 and 750
order by snum desc, pnum desc, jnum asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test059.exp""", 's2')
    
    _testmgr.testcase_end(desc)

