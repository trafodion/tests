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
    
    stmt = """create table t12tab (
a int not null, b int, c int,
d char(2), e char(4), f char(8)
)
attribute extent (1024, 1024), maxextents 15
store by (a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into t12tab values
(1,10,100,'d1','e1','f1'),
(2,20,200,'d2','e2','f2'), (3,30,300,'d3','e3','f3'),
(4,40,400,'d4','e4','f4'), (5,50,500,'d5','e5','f5'),
(6,60,600,'d6','e6','f6'), (7,70,700,'d7','e7','f7'),
(8,80,800,'d8','e8','f8'), (9,90,900,'d9','e9','f9'),
(10,100,1000,'da','ea','fa'), (11,110,1100,'db','eb','fb'),
(12,120,1200,'dc','ec','fc'), (13,130,1300,'dd','ed','fd'),
(14,140,1400,'de','ee','fe'), (15,150,1500,'df','ef','ff');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 15)
    
