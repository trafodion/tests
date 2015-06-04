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

# setup.je12

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
    
    stmt = """drop table m4 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table m3 cascade;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table m4
(
pk4a int unique not null not droppable,
pk4b int not null not droppable,
pk4c int not null not droppable,
v4 varchar(20),
primary key(pk4a,pk4b,pk4c)
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table m3
(
pk3a int unique not null not droppable,
pk3b int not null not droppable,
pk3c int not null not droppable,
fk34a int,
fk34b int,
fk34c int,
v3 varchar(20),
primary key(pk3a,pk3b,pk3c),
foreign key(fk34a,fk34b,fk34c) references m4
);"""
    output = _dci.cmdexec(stmt)
