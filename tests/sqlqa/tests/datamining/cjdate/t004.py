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
    
def test001(desc="""test004"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test004
    # JClear
    # 1999-06-01
    # CJDate tests (5th ed. p150): equijoin
    # "get all combinations of supplier and part information
    #  such that the supplier and part in question are located
    #  in the same city"
    #
    stmt = """select s.*, p.*
from s, p 
where s.city = p.city
order by snum, pnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test004.exp""", 's1')
    # expect 10 rows with the following values in order:
    #    SNUM SNAME STATUS CITY  PNUM  PNAME   COLOR WEIGHT  CITY
    #    ---- ----- ------ ----  ----  -----   ----- ------  ----
    #    s1   Smith   20  London   p1   nut     red     12  London
    #    s1   Smith   20  London   p4   screw   red     14  London
    #    s1   Smith   20  London   p6   cog     red     19  London
    #    s2   Jones   10  Paris    p2   bolt    green   17  Paris
    #    s2   Jones   10  Paris    p5   cam     blue    12  Paris
    #    s3   Blake   30  Paris    p2   bolt    green   17  Paris
    #    s3   Blake   30  Paris    p5   cam     blue    12  Paris
    #    s4   Clark   20  London   p1   nut     red     12  London
    #    s4   Clark   20  London   p4   screw   red     14  London
    #    s4   Clark   20  London   p6   cog     red     19  London
    
    #- select vps.*, vpp.*
    #-   from vps, vpp
    #-     where vps.city = vpp.city
    #-       order by snum, pnum;
    # expect the same 10 rows
    
    stmt = """select hps.*, hpp.*
from hps, hpp 
where hps.city = hpp.city
order by snum, pnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test004.exp""", 's2')
    # expect the same 10 rows
    
    _testmgr.testcase_end(desc)

