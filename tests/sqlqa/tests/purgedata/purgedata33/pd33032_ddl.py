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
   
    if hpdci.tgtSQ(): 
        stmt = """control query default POS 'LOCAL_NODE';"""
        output = _dci.cmdexec(stmt)
        stmt = """control query default POS_NUM_OF_PARTNS '32';"""
        output = _dci.cmdexec(stmt)
    
    stmt = """create table pd33032
(
unique1         int            not null not droppable,
unique2         int            not null not droppable
primary key not droppable,
two             int            not null not droppable,
four            int            not null not droppable,
ten             int            not null not droppable,
twenty          int            not null not droppable,
onePercent      int            not null not droppable,
tenPercent      int            not null not droppable,
twentyPercent   int            not null not droppable,
fiftyPercent    int            not null not droppable,
unique3         int            not null not droppable,
evenOnePercent  int             not null not droppable,
oddOnePercent   int             not null not droppable,
stringu1        char(52)        not null not droppable,
stringu2        char(52)        not null not droppable,
string4         char(52)        not null not droppable
);"""
    output = _dci.cmdexec(stmt)
   
    if hpdci.tgtSQ(): 
        stmt = """control query default POS 'DISK_POOL';"""
        output = _dci.cmdexec(stmt)
        stmt = """control query default POS_NUM_OF_PARTNS 'SYSTEM';"""
        output = _dci.cmdexec(stmt)
    
    stmt = """create view pd33032v1 (v_unique3, v_ten) as
select unique3, ten from pd33032;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index pd33032a1 on pd33032 (two , four);"""
    output = _dci.cmdexec(stmt)
