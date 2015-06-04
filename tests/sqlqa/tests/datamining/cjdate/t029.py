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
    
def test001(desc="""test029"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test029
    # JClear
    # 1999-06-03
    # CJDate tests (5th ed. p175): Nested subquery with GROUP BY & HAVING
    # Exercise 6.28
    # "Get project numbers for projects supplied with part P1 in an average
    #  quantity greater than the greatest quantity in which any part is
    #  supplied to project J1."
    #
    stmt = """select jnum
from spj 
where pnum = 'p1'
group by jnum
having avg (qty) >
(select max (qty)
from spj 
where jnum = 'j1');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    # expect 0 rows
    
    #- select jnum
    #-   from vpspj
    #-     where pnum = 'p1'
    #-       group by jnum
    #-         having avg (qty) >
    #-           (select max (qty)
    #-              from vpspj
    #-                where jnum = 'j1');
    # expect 0 rows
    
    stmt = """select jnum
from hpspj 
where pnum = 'p1'
group by jnum
having avg (qty) >
(select max (qty)
from hpspj 
where jnum = 'j1');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    # expect 0 rows
    
    _testmgr.testcase_end(desc)

