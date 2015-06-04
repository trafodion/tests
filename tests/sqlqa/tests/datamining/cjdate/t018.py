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
    
def test001(desc="""test018"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test018
    # JClear
    # 1999-06-02
    # CJDate tests (5th ed. p163): UPDATE with a subquery
    # "Set the shipment quantity to zero for all the suppliers in London"
    #
    # check the original values
    stmt = """select distinct qty, city
from s, spj 
where city = 'London'
order by qty;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test018.exp""", 's1')
    # expect 8 rows with qty values 100 200 300 400 500 600 700 800
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update spj 
set qty = 0
where 'London' =
(select city
from s 
where s.snum = spj.snum);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 4)
    
    stmt = """select qty, city
from s, spj 
where qty = 0 and city = 'London';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test018.exp""", 's3')
    # expect 8 rows with qty values = 0
    
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    # (can't update a Vertically partitioned table)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update hpspj 
set qty = 0
where 'London' =
(select city
from hps 
where hps.snum = hpspj.snum);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 4)
    
    stmt = """select qty, city
from hps, hpspj 
where qty = 0 and city = 'London';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test018.exp""", 's5')
    # expect 8 rows with qty values = 0
    
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    # check the values after the rollback
    stmt = """select distinct qty, city
from hps, hpspj 
where city = 'London'
order by qty;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test018.exp""", 's6')
    # expect 8 rows with qty values 100 200 300 400 500 600 700 800
    
    _testmgr.testcase_end(desc)

