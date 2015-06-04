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

# setup.je17

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
    
    stmt = """drop table t8 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table t7 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table t6 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table t5 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table t4 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table t3 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table t2 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table t1 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table m4 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table m3 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table m2 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table m1 cascade;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table t8
(
pk8 int not null not droppable primary key,
a8 int,
b8 int,
c8 int
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table t7
(
pk7 int not null not droppable primary key,
fk78 int references t8,
fknn78 int references t8 not null,
a7 int,
b7 int,
c7 int
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table t6
(
pk6 int not null not droppable primary key,
fk67 int references t7,
fknn67 int references t7 not null,
a6 int,
b6 int,
c6 int
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table t5
(
pk5 int not null not droppable primary key,
fk56 int references t6,
fknn56 int references t6 not null,
a5 int,
b5 int,
c5 int
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table t4
(
pk4 int not null not droppable primary key,
fk45 int references t5,
fknn45 int references t5 not null,
a4 int,
b4 int,
c4 int
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table t3
(
pk3 int not null not droppable primary key,
fk34 int references t4,
fknn34 int references t4 not null,
a3 int,
b3 int,
c3 int
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table t2
(
pk2 int not null not droppable primary key,
fk23 int references t3,
fknn23 int references t3 not null,
a2 int,
b2 int,
c2 int
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table t1
(
pk1 int not null not droppable primary key,
fk12 int references t2,
fknn12 int references t2 not null,
a1 int,
b1 int,
c1 int
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table m4
(
pk4a int unique not null not droppable,
pk4b int not null not droppable,
pk4c int not null not droppable,
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
primary key(pk3a,pk3b,pk3c),
foreign key(fk34a,fk34b,fk34c) references m4
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table m2
(
pk2a int unique not null not droppable,
pk2b int not null not droppable,
pk2c int not null not droppable,
fk23a int,
fk23b int,
fk23c int,
primary key(pk2a,pk2b,pk2c),
foreign key(fk23a,fk23b,fk23c) references m3
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table m1
(
pk1a int unique not null not droppable,
pk1b int not null not droppable,
pk1c int not null not droppable,
fk12a int,
fk12b int,
fk12c int,
primary key(pk1a,pk1b,pk1c),
foreign key(fk12a,fk12b,fk12c) references m2
);"""
    output = _dci.cmdexec(stmt)
