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

import rename02_ddl
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
    
    stmt = """set nametype ansi;"""
    output = _dci.cmdexec(stmt)
    
    rename02_ddl._init(_testmgr)
    
    stmt = """insert into tab_rem_ten_original values (0,'CGAAAAAAAAAAAAAA','CAAAAAAA',1492,96,14.61,6,'ABAAAAAA',492,'ABAA');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab_rem_ten_original values (1,'DCAAAAAAAAAAAAAA','DAAAAAAA',1491,44,1.28,7,'BCAAAAAA',491,'BCAA');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab_rem_ten_original values (1,'BUAAAAAAAAAAAAAA','BAAAAAAA',1490,57,3.97,5,'BAAAAAAA',490,'BAAA');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab_rem_ten_original values (1,'BNAAAAAAAAAAAAAA','BAAAAAAA',1489,2,2.39,13,'BDAAAAAA',489,'BDAA');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab_rem_ten_original values (0,'ABAAAAAAAAAAAAAA','AAAAAAAA',1488,88,0.76,16,'ABAAAAAA',488,'ABAA');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab_rem_ten_original values (1,'DNAAAAAAAAAAAAAA','DAAAAAAA',1487,37,14.69,3,'BDAAAAAA',487,'BDAA');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab_rem_ten_original values (1,'BTAAAAAAAAAAAAAA','BAAAAAAA',1486,8,7.79,9,'BEAAAAAA',486,'BEAA');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab_rem_ten_original values (0,'AFAAAAAAAAAAAAAA','AAAAAAAA',1485,10,5.87,0,'AAAAAAAA',485,'AAAA');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab_rem_ten_original values (1,'BKAAAAAAAAAAAAAA','BAAAAAAA',1484,42,6.84,5,'BAAAAAAA',484,'BAAA');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab_rem_ten_original values (0,'ATAAAAAAAAAAAAAA','AAAAAAAA',1483,29,6.33,4,'AEAAAAAA',483,'AEAA');"""
    output = _dci.cmdexec(stmt)
    
    ##sh import tab_rem_lrg_original -I ${g_sqldpop_data}/btpns05.dat
    stmt = gvars.inscmd + """ tab_rem_lrg_original select * from """ + gvars.g_schema_sqldpop + """.btpns05;"""
    output = _dci.cmdexec(stmt)
    
