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
    
def test001(desc="""test019"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test019
    # JClear
    # 1999-06-02
    # CJDate tests (5th ed. p168): v. complicated query
    # "For all red and blue parts such that the total quantity supplied
    #  is greater than 350 (excluding from the total all shipments for which
    #  the quantity is less than or equal to 200), get the part number, the
    #  weight in grams, the colour, and the maximum quantity supplied of that
    #  part; and order the result by descending part number within ascending
    #  values of that maximum quantity."
    #
    stmt = """select p.pnum,
 p.weight * 454 as "Weight in grams",
 p.color,
max (spj.qty) as "Max shipped quantity"
from p, spj 
where p.pnum = spj.pnum
and (p.color = 'red' or p.color = 'blue')
and spj.qty > 200
group by p.pnum, p.weight, p.color
having sum (qty) > 350
order by 4, p.pnum desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test019.exp""", 's1')
    # expect 5 rows with these values in this order:
    #    PNUM    "Weight in grams"  COLOR   "Max shipped quantity"
    #    ------  -----------------  ------  ----------------------
    #    p6                   8626  red                        500
    #    p5                   5448  blue                       500
    #    p1                   5448  red                        700
    #    p4                   6356  red                        800
    #    p3                   7718  blue                       800
    
    #- select vpp.pnum,
    #-        vpp.weight * 454 as "Weight in grams",
    #-        vpp.color,
    #-        max (vpspj.qty) as "Max shipped quantity"
    #-   from vpp, vpspj
    #-     where vpp.pnum = vpspj.pnum
    #-       and (vpp.color = 'red' or vpp.color = 'blue')
    #-       and vpspj.qty > 200
    #-         group by vpp.pnum, vpp.weight, vpp.color
    #-               having sum (qty) > 350
    #- 	    order by 4, vpp.pnum desc;
    # expect the same 5 rows with the same values in the same order:
    
    stmt = """select hpp.pnum,
 hpp.weight * 454 as "Weight in grams",
 hpp.color,
max (hpspj.qty) as "Max shipped quantity"
from hpp, hpspj 
where hpp.pnum = hpspj.pnum
and (hpp.color = 'red' or hpp.color = 'blue')
and hpspj.qty > 200
group by hpp.pnum, hpp.weight, hpp.color
having sum (qty) > 350
order by 4, hpp.pnum desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test019.exp""", 's2')
    # expect the same 5 rows with the same values in the same order:
    
    _testmgr.testcase_end(desc)

