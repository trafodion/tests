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
    
def test001(desc="""test008"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test008
    # JClear
    # 1999-06-01
    # CJDate tests (5th ed. p153): 3-table join
    # "Get all pairs of city names such that a supplier located
    # in the first city supplies a part stored in the second city"
    #
    stmt = """select distinct s.city, p.city
from s, spj, p 
where s.snum = spj.snum
and spj.pnum = p.pnum
order by s.city, p.city;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test008.exp""", 's1')
    # expect 7 rows with the following values in order:
    #      Athens           London
    #      Athens           Paris
    #      Athens           Rome
    #      London           London
    #      Paris            London
    #      Paris            Paris
    #      Paris            Rome
    
    #- select distinct vps.city, vpp.city
    #-   from vps, vpspj, vpp
    #-     where vps.snum = vpspj.snum
    #-       and vpspj.pnum = vpp.pnum
    #-         order by vps.city, vpp.city;
    # expect the same 7 rows as above
    
    stmt = """select distinct hps.city, hpp.city
from hps, hpspj, hpp 
where hps.snum = hpspj.snum
and hpspj.pnum = hpp.pnum
order by hps.city, hpp.city;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test008.exp""", 's2')
    # expect the same 7 rows as above
    
    _testmgr.testcase_end(desc)

