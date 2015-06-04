# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2015 Hewlett-Packard Development Company, L.P.
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

# Additional tables needed for this test unit.

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """create table t1y
(
pk1y int not null not droppable primary key,
fk1y2 int references t2,
a1y int
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table t1x
(
pk1x int not null not droppable primary key,
fk1x2 int references t2,
fk1x1y int references t1y,
a1x int
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table m1x
(
pk1xa int unique not null not droppable,
pk1xb int not null not droppable,
pk1xc int not null not droppable,
fk1x2a int,
fk1x2b int,
fk1x2c int,
v1x varchar(20),
primary key(pk1xa,pk1xb,pk1xc),
foreign key(fk1x2a,fk1x2b,fk1x2c) references m2
);"""
    output = _dci.cmdexec(stmt)
    
