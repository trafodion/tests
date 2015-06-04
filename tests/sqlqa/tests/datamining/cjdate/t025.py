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
    
def test001(desc="""test025"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test025
    # JClear
    # 1999-06-02
    # CJDate tests (5th ed. p173): Join. Exercises 6.6 & 6.7
    # "Get all supplier-number/part-number/project-number triples such that
    #  the indicated supplier, part, and project are [all colocated/are not
    #  all colocated]
    #
    stmt = """select snum, pnum, jnum, s.city
from s, p, j 
where s.city = p.city
and p.city = j.city
order by snum, pnum, jnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test025.exp""", 's1')
    # expect 16 rows
    
    stmt = """select snum, pnum, jnum, s.city
from s, p, j 
where not
(s.city = p.city and p.city = j.city)
order by snum, pnum, jnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test025.exp""", 's2')
    # expect 194 rows
    
    #- select snum, pnum, jnum, vps.city
    #-   from vps, vpp, vpj
    #-     where vps.city = vpp.city
    #-       and vpp.city = vpj.city
    #-         order by snum, pnum, jnum;
    # expect 16 rows
    
    #- select snum, pnum, jnum, vps.city
    #-   from vps, vpp, vpj
    #-     where not
    #-       (vps.city = vpp.city and vpp.city = vpj.city)
    #-          order by snum, pnum, jnum;
    # expect 194 rows
    
    stmt = """select snum, pnum, jnum, hps.city
from hps, hpp, hpj 
where hps.city = hpp.city
and hpp.city = hpj.city
order by snum, pnum, jnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test025.exp""", 's3')
    # expect 16 rows
    
    stmt = """select snum, pnum, jnum, hps.city
from hps, hpp, hpj 
where not
(hps.city = hpp.city and hpp.city = hpj.city)
order by snum, pnum, jnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test025.exp""", 's4')
    # expect 194 rows
    
    _testmgr.testcase_end(desc)

