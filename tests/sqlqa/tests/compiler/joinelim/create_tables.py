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

# setup
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
    
    stmt = """control query default POS_ALLOW_NON_PK_TABLES 'on';"""
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
fknnu78 int references t8 not null unique,
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
a4 int,
b4 int,
c4 int
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table t3
(
pk3 int not null not droppable primary key,
fk34 int references t4,
a3 int,
b3 int,
c3 int
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table t2
(
pk2 int not null not droppable primary key,
fk23 int references t3,
a2 int,
b2 int,
c2 int
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table t1
(
pk1 int not null not droppable primary key,
fk12 int references t2,
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
    
    stmt = """create table m2
(
pk2a int unique not null not droppable,
pk2b int not null not droppable,
pk2c int not null not droppable,
fk23a int,
fk23b int,
fk23c int,
v2 varchar(20),
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
v1 varchar(20),
primary key(pk1a,pk1b,pk1c),
foreign key(fk12a,fk12b,fk12c) references m2
);"""
    output = _dci.cmdexec(stmt)
    
    #drop table t1 cascade;
    #drop table t2 cascade;
    #drop table t3 cascade;
    #drop table t4 cascade;
    #drop table t5 cascade;
    #drop table t6 cascade;
    #drop table t7 cascade;
    #drop table t8 cascade;
    #drop table m1 cascade;
    #drop table m2 cascade;
    #drop table m3 cascade;
    #drop table m4 cascade;
    
    stmt = """insert into t8
(pk8,       a8,  b8,   c8) values
---        ---  ---   ----
(81,        181, 191,  null)
,(82,        182, 191,  null)
,(83,        183, 192,  null)
,(84,        184, null, null)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into t7
(pk7, fk78, fknn78, fknnu78, a7,  b7,   c7) values
---  ----  ------  -------  ---  ---   ----
(71,  81,   81,     81,      171, 181,  null)
,(72,  81,   81,     82,      172, 181,  null)
,(73,  82,   82,     83,      173, 182,  null)
,(74,  null, 82,     84,      174, null, null)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into t6
(pk6, fk67, fknn67, a6,  b6,   c6) values
---  ----  ------  ---  ---   ----
(61,  71,   71,     161, 171,  null)
,(62,  71,   71,     162, 171,  null)
,(63,  72,   72,     163, 172,  null)
,(64,  null, 72,     164, null, null)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into t5
(pk5, fk56, fknn56, a5,  b5,   c5) values
---  ----  ------  ---  ---   ----
(51,  61,   61,     151, 161,  null)
,(52,  61,   61,     152, 161,  null)
,(53,  62,   62,     153, 162,  null)
,(54,  null, 62,     154, null, null)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into t4
(pk4, fk45, a4,  b4,   c4) values
---  ----  ---  ---   ----
(41,  51,   141, 151,  null)
,(42,  51,   142, 151,  null)
,(43,  52,   143, 152,  null)
,(44,  null, 144, null, null)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into t3
(pk3, fk34, a3,  b3,   c3) values
---  ----  ---  ---   ----
(31,  41,   131, 141,  null)
,(32,  41,   132, 141,  null)
,(33,  42,   133, 142,  null)
,(34,  null, 144, null, null)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into t2
(pk2, fk23, a2,  b2,   c2) values
---  ----  ---  ---   ----
(21, 31,    121, 131,  null)
,(22, 31,    122, 131,  null)
,(23, 32,    123, 132,  null)
,(24, null,  124, null, null)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into t1
(pk1, fk12, a1,  b1,   c1) values
---  ----  ---  ---   ----
(11,  21,   111, 121,  null)
,(12,  21,   112, 121,  null)
,(13,  22,   113, 122,  null)
,(14,  null, 114, null, null)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into m4
(pk4a, pk4b, pk4c,                      v4)    values
----  ----  ----                       ------
(411,  412,  413,                       'm4_1')
,(421,  422,  423,                       'm4_2')
,(431,  432,  433,                       'm4_3')
,(441,  442,  443,                       'm4_4')
,(451,  452,  453,                       'm4_5')
,(461,  462,  463,                       'm4_6')
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into m3
(pk3a, pk3b, pk3c, fk34a, fk34b, fk34c, v3)    values
----  ----  ----  -----  -----  -----  ------
(311,  312,  313,  411,   412,   413,   'm3_1')
,(321,  322,  323,  411,   412,   413,   'm3_2')
,(331,  332,  333,  421,   422,   423,   'm3_3')
,(341,  342,  343,  null,  null,  null,  'm3_4')  -- all null fk
,(351,  352,  353,  451,   452,   null,  'm3_5')  -- partially null fk
,(361,  362,  363,  999,   null,  888,   'm3_6')  -- partially null fk, non-nulls don't match
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into m2
(pk2a, pk2b, pk2c, fk23a, fk23b, fk23c, v2)    values
----  ----  ----  -----  -----  -----  ------
(211,  212,  213,  311,   312,   313,   'm2_1')
,(221,  222,  223,  311,   312,   313,   'm2_2')
,(231,  232,  233,  321,   322,   323,   'm2_3')
,(241,  242,  243,  null,  null,  null,  'm2_4')  -- all null fk
,(251,  252,  253,  351,   352,   null,  'm2_5')  -- partially null fk
,(261,  262,  263,  999,   null,  888,   'm2_6')  -- partially null fk, non-nulls don't match
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into m1
(pk1a, pk1b, pk1c, fk12a, fk12b, fk12c, v1)    values
----  ----  ----  -----  -----  -----  ------
(111,  112,  113,  211,   212,   213,   'm1_1')
,(121,  122,  123,  211,   212,   213,   'm1_2')
,(131,  132,  133,  221,   222,   223,   'm1_3')
,(141,  142,  143,  null,  null,  null,  'm1_4')  -- all null fk
,(151,  152,  153,  251,   252,   null,  'm1_5')  -- partially null fk
,(161,  162,  163,  999,   null,  888,   'm1_6')  -- partially null fk, non-nulls don't match
;"""
    output = _dci.cmdexec(stmt)
    
