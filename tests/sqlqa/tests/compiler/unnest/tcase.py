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

import unnest3_ins
import unnest2_sql
import unnest5_ins
import unnest8_sql
import unnest6_sql
import unnest5_sql
import unnest3_sql
import unnest1_ins
import unnest4_sql
import unnest9_sql
import unnest7_ins
import unnest2_ins
import unnest1_sql
import unnest4_ins
import unnest6_ins
import unnest8_ins
import unnest7_sql
import unnest9_ins
from ...lib import hpdci
from ...lib import gvars
import defs

_testmgr = None
_testlist = []
_dci = None

# PURPOSE: This test validates COMPARISON  PREDICATES WITH  BOOLEAN OPERATORS
# & AGGREGATE
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""unnest1"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """Create table T1(A int, B  smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T2(C int, D smallint,  E largeint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T3(F int,  G  smallint, H largeint , I numeric(9,3));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T4(J int,  K smallint, L largeint ,  M numeric(9,3),  N decimal(18,9));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T5(O int,  P smallint, Q  largeint, R numeric(9,3),  S decimal(18,9), T char(20), U float(52), V real, W double precision, X timestamp,Y interval year to month ,Z char (12), AA time);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    defs.test_id='1'
    unnest1_ins._init(_testmgr)
    unnest1_sql._init(_testmgr)
    
    stmt = """Create table  T1(A int  not null not droppable primary key,
B smallint default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T2(C int default null,
D smallint not null not droppable primary key,
E largeint default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T3(F int default null,
G smallint default null,
H largeint not null not droppable primary key,
I numeric(9,3) default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create table T4(J int default null,
K smallint default null,
L largeint default  null ,
M numeric(9,3) not null not droppable primary key,
N decimal(18,9) default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create table T5(O int default null,
P smallint default null,
Q largeint default null,
R numeric(9,3) not null not droppable primary key,
S decimal(18,9) default null,
T char(20) default null,
U float(52) default null,
V real default null,
W double precision default null,
X timestamp default null,
Y interval year to month default null ,
Z char (12) default null,
AA time default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index smint_idx on T1(B) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idx  on T2(E) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idx on T2(C) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index num_idx on T3(I) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idxT3 on T3(G) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT3  on T3(F) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dem_idxT4  on T4(N) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT4  on T4(J) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index sint_idxT4  on T4(K) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idxT4  on T4(L) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dat_idxT5   on  T5(T) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT5   on T5(O) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index smint_idxT5 on T5(P) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idxT5 on T5(Q) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dem_idxT5  on T5(S) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index flo_idxT5  on T5(U) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index rel_idxT5  on T5(V) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dou_idxT5  on T5(W) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index tms_idxT5  on T5(X) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index intv_idxT5 on T5(Y) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index char_idxT5 on T5(Z) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index tim_idxT5  on T5(AA) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    defs.test_id='2'
    unnest1_ins._init(_testmgr)
    unnest1_sql._init(_testmgr)
    stmt = """Create table  T1(A int  not null not droppable primary key,
B smallint default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T2(C int default null,
D smallint not null not droppable primary key,
E largeint default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T3(F int not null not droppable ,
G smallint not null not droppable ,
H largeint not null not droppable ,
I numeric(9,3) default null,
primary key (F,G,H) )
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T4          (J int default null,
K smallint not null not droppable,
L largeint not null not droppable,
M numeric(9,3) not null not droppable,
N decimal(18,9) default null,
primary key (K,L,M) )
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create table T5       (O int default null,
P smallint default null,
Q largeint default null,
R numeric(9,3) not null not droppable primary key,
S decimal(18,9) default null,
T char(20) default null,
U float(52) default null,
V real default null,
W double precision default null,
X timestamp default null,
Y interval year to month default null ,
Z char (12) default null,
AA time default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index smint_idx on T1(B) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idx on T2(E) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idx on T2(C) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index num_idx on T3(I) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dem_idxT4 on T4(N) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT4 on T4(J) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dat_idxT5 on  T5(T) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT5 on T5(O) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index smint_idxT5 on T5(P) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idxT5 on T5(Q) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dem_idxT5 on T5(S) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index flo_idxT5 on T5(U) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index rel_idxT5 on T5(V) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dou_idxT5 on T5(W) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index tms_idxT5 on T5(X) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index intv_idxT5 on T5(Y) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index char_idxT5 on T5(Z) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index tim_idxT5 on T5(AA) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    defs.test_id='3'
    unnest1_ins._init(_testmgr)
    unnest1_sql._init(_testmgr)
    
    _testmgr.testcase_end(desc)

def test002(desc="""unnest2"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """Create table  T1(A int, B  smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T2(C int, D smallint,  E largeint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T3(F int,  G  smallint, H largeint , I numeric(9,3));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T4(J int,  K smallint, L largeint ,  M numeric(9,3),  N decimal(18,9));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T5(O int,  P smallint, Q  largeint, R numeric(9,3),  S decimal(18,9), T char(20), U float(52), V real, W double precision, X timestamp,Y interval year to month ,Z char (12), AA time);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    defs.test_id='1'
    unnest2_ins._init(_testmgr)
    unnest2_sql._init(_testmgr)
    
    stmt = """Create table  T1(A int  not null not droppable primary key,
B  smallint default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T2(C int default null,
D smallint not null not droppable primary key,
E largeint default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T3(F int default null,
G smallint default null,
H largeint not null not droppable primary key,
I numeric(9,3) default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create table T4(J int default null,
K smallint default null,
L largeint default  null ,
M numeric(9,3) not null not droppable primary key,
N decimal(18,9) default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create table T5(O int default null,
P smallint default null,
Q largeint default null,
R numeric(9,3) not null not droppable primary key,
S decimal(18,9) default null,
T char(20) default null,
U float(52) default null,
V real default null,
W double precision default null,
X timestamp default null,
Y interval year to month default null ,
Z char (12) default null,
AA time default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index smint_idx   on T1(B) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idx    on T2(E) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idx     on T2(C) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index num_idx     on T3(I) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idxT3  on T3(G) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT3   on T3(F) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dem_idxT4   on T4(N) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT4   on T4(J) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index sint_idxT4  on T4(K) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idxT4  on T4(L) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dat_idxT5   on T5(T) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT5   on T5(O) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index smint_idxT5 on T5(P) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idxT5  on T5(Q) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dem_idxT5   on T5(S) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index flo_idxT5   on T5(U) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index rel_idxT5   on T5(V) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dou_idxT5   on T5(W) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index tms_idxT5   on T5(X) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index intv_idxT5  on T5(Y) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index char_idxT5  on T5(Z) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index tim_idxT5   on T5(AA) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    defs.test_id='2'
    unnest2_ins._init(_testmgr)
    unnest2_sql._init(_testmgr)
    
    stmt = """Create table  T1(A int  not null not droppable primary key,
B smallint default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T2(C int default null,
D smallint not null not droppable primary key,
E largeint default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T3(F int not null not droppable ,
G smallint not null not droppable ,
H largeint not null not droppable ,
I numeric(9,3) default null,
primary key (F,G,H) )
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create table T4           (J int default null,
K smallint not null not droppable,
L largeint not null not droppable,
M numeric(9,3) not null not droppable,
N decimal(18,9) default null,
primary key (K,L,M) )
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create table T5        (O int default null,
P smallint default null,
Q largeint default null,
R numeric(9,3) not null not droppable primary key,
S decimal(18,9) default null,
T char(20) default null,
U float(52) default null,
V real default null,
W double precision default null,
X timestamp default null,
Y interval year to month default null ,
Z char (12) default null,
AA time default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index smint_idx   on T1(B) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idx    on T2(E) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idx     on T2(C) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index num_idx     on T3(I) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dem_idxT4   on T4(N) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT4   on T4(J) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dat_idxT5   on  T5(T) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT5   on T5(O) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index smint_idxT5 on T5(P) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idxT5  on T5(Q) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dem_idxT5   on T5(S) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index flo_idxT5   on T5(U) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index rel_idxT5   on T5(V) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dou_idxT5   on T5(W) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index tms_idxT5   on T5(X) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index intv_idxT5  on T5(Y) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index char_idxT5  on T5(Z) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index tim_idxT5   on T5(AA) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    defs.test_id='3'
    unnest2_ins._init(_testmgr)
    unnest2_sql._init(_testmgr)
    
    _testmgr.testcase_end(desc)

def test003(desc="""unnest3"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """Create table T1(A int, B smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T2(C int, D smallint, E largeint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T3(F int, G smallint, H largeint , I numeric(9,3));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T4(J int, K smallint, L largeint ,  M numeric(9,3),  N decimal(18,9));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T5(O int, P smallint, Q  largeint, R numeric(9,3),  S decimal(18,9), T char(20), U float(52), V real, W double precision, X timestamp,Y interval year to month ,Z char (12), AA time);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    defs.test_id='1'
    unnest3_ins._init(_testmgr)
    unnest3_sql._init(_testmgr)
    
    stmt = """Create table T1(A int  not null not droppable primary key,
B  smallint default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T2(C int default null,
D smallint not null not droppable primary key,
E largeint default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T3(F int default null,
G  smallint default null,
H largeint not null not droppable primary key,
I numeric(9,3) default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create table T4(J int default null,
K smallint default null,
L largeint default  null ,
M numeric(9,3) not null not droppable primary key,
N decimal(18,9) default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create table T5(O int default null,
P smallint default null,
Q largeint default null,
R numeric(9,3) not null not droppable primary key,
S decimal(18,9) default null,
T char(20) default null,
U float(52) default null,
V real default null,
W double precision default null,
X timestamp default null,
Y interval year to month default null ,
Z char (12) default null,
AA time default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index smint_idx on T1(B) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idx on T2(E) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idx on T2(C) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index num_idx on T3(I) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idxT3 on T3(G) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT3 on T3(F) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dem_idxT4 on T4(N) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT4 on T4(J) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index sint_idxT4 on T4(K) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idxT4 on T4(L) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dat_idxT5 on T5(T) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT5 on T5(O) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index smint_idxT5 on T5(P) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idxT5 on T5(Q) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dem_idxT5 on T5(S) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index flo_idxT5 on T5(U) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index rel_idxT5 on T5(V) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dou_idxT5 on T5(W) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index tms_idxT5 on T5(X) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index intv_idxT5 on T5(Y) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index char_idxT5 on T5(Z) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index tim_idxT5 on T5(AA) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    defs.test_id='2'
    unnest3_ins._init(_testmgr)
    unnest3_sql._init(_testmgr)
    
    stmt = """Create table T1(A int  not null not droppable primary key,
B  smallint default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T2(C int default null,
D smallint not null not droppable primary key,
E largeint default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T3(F int not null not droppable ,
G  smallint not null not droppable ,
H largeint not null not droppable ,
I numeric(9,3) default null,
primary key (F,G,H) )
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create table T4          (J int default null,
K smallint not null not droppable,
L largeint not null not droppable,
M numeric(9,3) not null not droppable,
N decimal(18,9) default null,
primary key (K,L,M) )
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create table T5        (O int default null,
P smallint default null,
Q largeint default null,
R numeric(9,3) not null not droppable primary key,
S decimal(18,9) default null,
T char(20) default null,
U float(52) default null,
V real default null,
W double precision default null,
X timestamp default null,
Y interval year to month default null ,
Z char (12) default null,
AA time default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index smint_idx on T1(B) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idx on T2(E) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idx on T2(C) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index num_idx on T3(I) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dem_idxT4 on T4(N) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT4 on T4(J) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dat_idxT5 on  T5(T) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT5 on T5(O) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index smint_idxT5 on T5(P) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idxT5 on T5(Q) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dem_idxT5 on T5(S) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index flo_idxT5 on T5(U) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index rel_idxT5 on T5(V) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dou_idxT5 on T5(W) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index tms_idxT5 on T5(X) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index intv_idxT5 on T5(Y) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index char_idxT5 on T5(Z) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index tim_idxT5 on T5(AA) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    defs.test_id='3'
    unnest3_ins._init(_testmgr)
    unnest3_sql._init(_testmgr)
    
    _testmgr.testcase_end(desc)

def test004(desc="""unnest4"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """Create table T1(A int, B  smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T2(C int, D smallint,  E largeint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T3(F int, G  smallint, H largeint , I numeric(9,3));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T4(J int, K smallint, L largeint ,  M numeric(9,3),  N decimal(18,9));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T5(O int,  P smallint, Q  largeint, R numeric(9,3),  S decimal(18,9), T char(20), U float(52), V real, W double precision, X timestamp,Y interval year to month ,Z char (12), AA time);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    defs.test_id='1'
    unnest4_ins._init(_testmgr)
    unnest4_sql._init(_testmgr)
    
    stmt = """Create table T1(A int  not null not droppable primary key,
B  smallint default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T2(C int default null,
D smallint not null not droppable primary key,
E largeint default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T3(F int default null,
G smallint default null,
H largeint not null not droppable primary key,
I numeric(9,3) default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create table T4(J int default null,
K smallint default null,
L largeint default  null ,
M numeric(9,3) not null not droppable primary key,
N decimal(18,9) default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create table T5(O int default null,
P smallint default null,
Q largeint default null,
R numeric(9,3) not null not droppable primary key,
S decimal(18,9) default null,
T char(20) default null,
U float(52) default null,
V real default null,
W double precision default null,
X timestamp default null,
Y interval year to month default null ,
Z char (12) default null,
AA time default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index smint_idx on T1(B) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idx on T2(E) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idx on T2(C) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index num_idx on T3(I) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idxT3 on T3(G) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT3 on T3(F) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dem_idxT4 on T4(N) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT4 on T4(J) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index sint_idxT4 on T4(K) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idxT4 on T4(L) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dat_idxT5 on  T5(T) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT5 on T5(O) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index smint_idxT5 on T5(P) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idxT5 on T5(Q) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dem_idxT5 on T5(S) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index flo_idxT5 on T5(U) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index rel_idxT5 on T5(V) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dou_idxT5 on T5(W) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index tms_idxT5 on T5(X) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index intv_idxT5 on T5(Y) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index char_idxT5 on T5(Z) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index tim_idxT5 on T5(AA) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    defs.test_id='2'
    unnest4_ins._init(_testmgr)
    unnest4_sql._init(_testmgr)
    
    stmt = """Create table T1(A int  not null not droppable primary key,
B smallint default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T2(C int default null,
D smallint not null not droppable primary key,
E largeint default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T3(F int not null not droppable ,
G smallint not null not droppable ,
H largeint not null not droppable ,
I numeric(9,3) default null,
primary key (F,G,H) )
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T4          (J int default null,
K smallint not null not droppable,
L largeint not null not droppable,
M numeric(9,3) not null not droppable,
N decimal(18,9) default null,
primary key (K,L,M) )
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create table T5        (O int default null,
P smallint default null,
Q largeint default null,
R numeric(9,3) not null not droppable primary key,
S decimal(18,9) default null,
T char(20) default null,
U float(52) default null,
V real default null,
W double precision default null,
X timestamp default null,
Y interval year to month default null ,
Z char (12) default null,
AA time default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index smint_idx on T1(B) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idx on T2(E) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idx on T2(C) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index num_idx on T3(I) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dem_idxT4 on T4(N) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT4 on T4(J) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dat_idxT5 on  T5(T) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT5 on T5(O) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index smint_idxT5 on T5(P) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idxT5 on T5(Q) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dem_idxT5 on T5(S) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index flo_idxT5 on T5(U) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index rel_idxT5 on T5(V) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dou_idxT5 on T5(W) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index tms_idxT5 on T5(X) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index intv_idxT5 on T5(Y) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index char_idxT5 on T5(Z) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index tim_idxT5 on T5(AA) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    defs.test_id='3'
    unnest4_ins._init(_testmgr)
    unnest4_sql._init(_testmgr)
    
    _testmgr.testcase_end(desc)

def test005(desc="""unnest5"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """Create table T1(A int, B  smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T2(C int, D smallint,  E largeint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T3(F int,  G  smallint, H largeint , I numeric(9,3));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T4(J int,  K smallint, L largeint ,  M numeric(9,3),  N decimal(18,9));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T5(O int,  P smallint, Q  largeint, R numeric(9,3),  S decimal(18,9), T char(20), U float(52), V real, W double precision, X timestamp,Y interval year to month ,Z char (12), AA time);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    defs.test_id='1'
    unnest5_ins._init(_testmgr)
    unnest5_sql._init(_testmgr)
    
    stmt = """Create table T1(A int  not null not droppable primary key,
B  smallint default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T2(C int default null,
D smallint not null not droppable primary key,
E largeint default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T3(F int default null,
G  smallint default null,
H largeint not null not droppable primary key,
I numeric(9,3) default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T4(J int default null,
K smallint default null,
L largeint default  null ,
M numeric(9,3) not null not droppable primary key,
N decimal(18,9) default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T5(O int default null,
P smallint default null,
Q largeint default null,
R numeric(9,3) not null not droppable primary key,
S decimal(18,9) default null,
T char(20) default null,
U float(52) default null,
V real default null,
W double precision default null,
X timestamp default null,
Y interval year to month default null ,
Z char (12) default null,
AA time default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index smint_idx on T1(B) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idx on T2(E) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idx on T2(C) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index num_idx on T3(I) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idxT3 on T3(G) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT3 on T3(F) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dem_idxT4 on T4(N) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT4 on T4(J) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index sint_idxT4 on T4(K) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idxT4 on T4(L) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dat_idxT5 on  T5(T) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT5 on T5(O) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index smint_idxT5 on T5(P) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idxT5 on T5(Q) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dem_idxT5 on T5(S) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index flo_idxT5 on T5(U) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index rel_idxT5 on T5(V) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dou_idxT5 on T5(W) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index tms_idxT5 on T5(X) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index intv_idxT5 on T5(Y) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index char_idxT5 on T5(Z) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index tim_idxT5 on T5(AA) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    defs.test_id='2'
    unnest5_ins._init(_testmgr)
    unnest5_sql._init(_testmgr)
    
    stmt = """Create table T1(A int  not null not droppable primary key,
B  smallint default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T2(C int default null,
D smallint not null not droppable primary key,
E largeint default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T3(F int not null not droppable ,
G smallint not null not droppable ,
H largeint not null not droppable ,
I numeric(9,3) default null,
primary key (F,G,H) )
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create table T4          (J int default null,
K smallint not null not droppable,
L largeint not null not droppable,
M numeric(9,3) not null not droppable,
N decimal(18,9) default null,
primary key (K,L,M) )
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create table T5 (O int default null,
P smallint default null,
Q  largeint default null,
R numeric(9,3) not null not droppable primary key,
S decimal(18,9) default null,
T char(20) default null,
U float(52) default null,
V real default null,
W double precision default null,
X timestamp default null,
Y interval year to month default null ,
Z char (12) default null,
AA time default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index smint_idx on T1(B) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idx on T2(E) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idx on T2(C) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index num_idx on T3(I) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dem_idxT4 on T4(N) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT4 on T4(J) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dat_idxT5 on  T5(T) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT5 on T5(O) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index smint_idxT5 on T5(P) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idxT5 on T5(Q) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dem_idxT5 on T5(S) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index flo_idxT5 on T5(U) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index rel_idxT5 on T5(V) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dou_idxT5 on T5(W) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index tms_idxT5 on T5(X) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index intv_idxT5 on T5(Y) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index char_idxT5 on T5(Z) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index tim_idxT5 on T5(AA) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    defs.test_id='3'
    unnest5_ins._init(_testmgr)
    unnest5_sql._init(_testmgr)
    
    _testmgr.testcase_end(desc)

def test006(desc="""unnest6"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """Create table T1(A int, B  smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T2(C int, D smallint,  E largeint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T3(F int, G  smallint, H largeint , I numeric(9,3));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T4(J int, K smallint, L largeint ,  M numeric(9,3),  N decimal(18,9));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T5(O int, P smallint, Q  largeint, R numeric(9,3),  S decimal(18,9), T char(20), U float(52), V real, W double precision, X timestamp,Y interval year to month ,Z char (12), AA time);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    defs.test_id='1'
    unnest6_ins._init(_testmgr)
    unnest6_sql._init(_testmgr)
    
    stmt = """Create table T1(A int  not null not droppable primary key,
B  smallint default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T2(C int default null,
D smallint not null not droppable primary key,
E largeint default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T3(F int default null,
G smallint default null,
H largeint not null not droppable primary key,
I numeric(9,3) default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T4(J int default null,
K smallint default null,
L largeint default  null ,
M numeric(9,3) not null not droppable primary key,
N decimal(18,9) default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T5(O int default null,
P smallint default null,
Q largeint default null,
R numeric(9,3) not null not droppable primary key,
S decimal(18,9) default null,
T char(20) default null,
U float(52) default null,
V real default null,
W double precision default null,
X timestamp default null,
Y interval year to month default null ,
Z char (12) default null,
AA time default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index smint_idx on T1(B) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idx on T2(E) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idx on T2(C) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index num_idx on T3(I) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idxT3 on T3(G) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT3 on T3(F) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dem_idxT4 on T4(N) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT4 on T4(J) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index sint_idxT4 on T4(K) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idxT4 on T4(L) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dat_idxT5 on  T5(T) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT5 on T5(O) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index smint_idxT5 on T5(P) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idxT5 on T5(Q) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dem_idxT5 on T5(S) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index flo_idxT5 on T5(U) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index rel_idxT5 on T5(V) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dou_idxT5 on T5(W) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index tms_idxT5 on T5(X) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index intv_idxT5 on T5(Y) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index char_idxT5 on T5(Z) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index tim_idxT5 on T5(AA) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    defs.test_id='2'
    unnest6_ins._init(_testmgr)
    unnest6_sql._init(_testmgr)
    
    stmt = """Create table T1(A int  not null not droppable primary key,
B  smallint default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T2(C int default null,
D smallint not null not droppable primary key,
E largeint default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T3(F int not null not droppable ,
G smallint not null not droppable ,
H largeint not null not droppable ,
I numeric(9,3) default null,
primary key (F,G,H) )
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T4           (J int default null,
K smallint not null not droppable,
L largeint not null not droppable,
M numeric(9,3) not null not droppable,
N decimal(18,9) default null,
primary key (K,L,M) )
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T5        (O int default null,
P smallint default null,
Q largeint default null,
R numeric(9,3) not null not droppable primary key,
S decimal(18,9) default null,
T char(20) default null,
U float(52) default null,
V real default null,
W double precision default null,
X timestamp default null,
Y interval year to month default null ,
Z char (12) default null,
AA time default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index smint_idx on T1(B) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idx on T2(E) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idx on T2(C) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index num_idx on T3(I) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dem_idxT4 on T4(N) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT4 on T4(J) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dat_idxT5 on  T5(T) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT5 on T5(O) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index smint_idxT5 on T5(P) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idxT5 on T5(Q) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dem_idxT5 on T5(S) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index flo_idxT5 on T5(U) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index rel_idxT5 on T5(V) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dou_idxT5 on T5(W) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index tms_idxT5 on T5(X) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index intv_idxT5 on T5(Y) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index char_idxT5 on T5(Z) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index tim_idxT5 on T5(AA) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    defs.test_id='3'
    unnest6_ins._init(_testmgr)
    unnest6_sql._init(_testmgr)
    
    _testmgr.testcase_end(desc)

def test007(desc="""unnest7"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Create table T1(A int, B  smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T2(C int, D smallint,  E largeint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T3(F int, G  smallint, H largeint , I numeric(9,3));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T4(J int, K smallint, L largeint ,  M numeric(9,3),  N decimal(18,9));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T5(O int, P smallint, Q  largeint, R numeric(9,3),  S decimal(18,9), T char(20), U float(52), V real, W double precision, X timestamp,Y interval year to month ,Z char (12), AA time);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    defs.test_id='1'
    unnest7_ins._init(_testmgr)
    unnest7_sql._init(_testmgr)
    
    stmt = """Create table T1(A int  not null not droppable primary key,
B  smallint default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T2(C int default null,
D smallint not null not droppable primary key,
E largeint default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T3(F int default null,
G  smallint default null,
H largeint not null not droppable primary key,
I numeric(9,3) default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create table T4(J int default null,
K smallint default null,
L largeint default  null ,
M numeric(9,3) not null not droppable primary key,
N decimal(18,9) default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create table T5(O int default null,
P smallint default null,
Q largeint default null,
R numeric(9,3) not null not droppable primary key,
S decimal(18,9) default null,
T char(20) default null,
U float(52) default null,
V real default null,
W double precision default null,
X timestamp default null,
Y interval year to month default null ,
Z char (12) default null,
AA time default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index smint_idx on T1(B) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idx on T2(E) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idx on T2(C) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index num_idx on T3(I) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idxT3 on T3(G) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT3 on T3(F) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dem_idxT4 on T4(N) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT4 on T4(J) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index sint_idxT4 on T4(K) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idxT4 on T4(L) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dat_idxT5 on  T5(T) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT5 on T5(O) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index smint_idxT5 on T5(P) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idxT5 on T5(Q) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dem_idxT5 on T5(S) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index flo_idxT5 on T5(U) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index rel_idxT5 on T5(V) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dou_idxT5 on T5(W) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index tms_idxT5 on T5(X) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index intv_idxT5 on T5(Y) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index char_idxT5 on T5(Z) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index tim_idxT5 on T5(AA) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    defs.test_id='2'
    unnest7_ins._init(_testmgr)
    unnest7_sql._init(_testmgr)
    
    stmt = """Create table T1(A int  not null not droppable primary key,
B  smallint default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T2(C int default null,
D smallint not null not droppable primary key,
E largeint default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T3(F int not null not droppable ,
G smallint not null not droppable ,
H largeint not null not droppable ,
I numeric(9,3) default null,
primary key (F,G,H) )
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T4          (J int default null,
K smallint not null not droppable,
L largeint not null not droppable,
M numeric(9,3) not null not droppable,
N decimal(18,9) default null,
primary key (K,L,M) )
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T5        (O int default null,
P smallint default null,
Q  largeint default null,
R numeric(9,3) not null not droppable primary key,
S decimal(18,9) default null,
T char(20) default null,
U float(52) default null,
V real default null,
W double precision default null,
X timestamp default null,
Y interval year to month default null ,
Z char (12) default null,
AA time default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index smint_idx on T1(B) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idx on T2(E) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idx on T2(C) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index num_idx on T3(I) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dem_idxT4 on T4(N) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT4 on T4(J) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dat_idxT5 on  T5(T) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT5 on T5(O) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index smint_idxT5 on T5(P) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idxT5 on T5(Q) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dem_idxT5 on T5(S) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index flo_idxT5 on T5(U) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index rel_idxT5 on T5(V) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dou_idxT5 on T5(W) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index tms_idxT5 on T5(X) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index intv_idxT5 on T5(Y) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index char_idxT5 on T5(Z) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index tim_idxT5 on T5(AA) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    defs.test_id='3'
    unnest7_ins._init(_testmgr)
    unnest7_sql._init(_testmgr)
    
    # Semi join queries
    _testmgr.testcase_end(desc)

def test008(desc="""unnest8"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """Create table T1(A int, B  smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T2(C int, D smallint,  E largeint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T3(F int, G  smallint, H largeint , I numeric(9,3));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T4(J int, K smallint, L largeint ,  M numeric(9,3),  N decimal(18,9));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T5(O int, P smallint, Q  largeint, R numeric(9,3),  S decimal(18,9), T char(20), U float(52), V real, W double precision, X timestamp,Y interval year to month ,Z char (12), AA time);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    defs.test_id='1'
    unnest8_ins._init(_testmgr)
    unnest8_sql._init(_testmgr)
    
    stmt = """Create table T1(A int  not null not droppable primary key,
B  smallint default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T2(C int default null,
D smallint not null not droppable primary key,
E largeint default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T3(F int default null,
G smallint default null,
H largeint not null not droppable primary key,
I numeric(9,3) default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T4(J int default null,
K smallint default null,
L largeint default  null ,
M numeric(9,3) not null not droppable primary key,
N decimal(18,9) default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create table T5(O int default null,
P smallint default null,
Q largeint default null,
R numeric(9,3) not null not droppable primary key,
S decimal(18,9) default null,
T char(20) default null,
U float(52) default null,
V real default null,
W double precision default null,
X timestamp default null,
Y interval year to month default null ,
Z char (12) default null,
AA time default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index smint_idx on T1(B) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idx on T2(E) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idx on T2(C) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index num_idx on T3(I) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idxT3 on T3(G) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT3 on T3(F) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dem_idxT4 on T4(N) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT4 on T4(J) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index sint_idxT4 on T4(K) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idxT4 on T4(L) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dat_idxT5 on  T5(T) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT5 on T5(O) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index smint_idxT5 on T5(P) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idxT5 on T5(Q) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dem_idxT5 on T5(S) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index flo_idxT5 on T5(U) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index rel_idxT5 on T5(V) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dou_idxT5 on T5(W) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index tms_idxT5 on T5(X) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index intv_idxT5 on T5(Y) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index char_idxT5 on T5(Z) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index tim_idxT5 on T5(AA) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    defs.test_id='2'
    unnest8_ins._init(_testmgr)
    unnest8_sql._init(_testmgr)
    
    stmt = """Create table T1(A int  not null not droppable primary key,
B  smallint default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T2(C int default null,
D smallint not null not droppable primary key,
E largeint default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T3(F int not null not droppable ,
G smallint not null not droppable ,
H largeint not null not droppable ,
I numeric(9,3) default null,
primary key (F,G,H) )
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T4          (J int default null,
K smallint not null not droppable,
L largeint not null not droppable,
M numeric(9,3) not null not droppable,
N decimal(18,9) default null,
primary key (K,L,M) )
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T5       (O int default null,
P smallint default null,
Q largeint default null,
R numeric(9,3) not null not droppable primary key,
S decimal(18,9) default null,
T char(20) default null,
U float(52) default null,
V real default null,
W double precision default null,
X timestamp default null,
Y interval year to month default null ,
Z char (12) default null,
AA time default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index smint_idx on T1(B) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idx on T2(E) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idx on T2(C) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index num_idx on T3(I) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dem_idxT4 on T4(N) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT4 on T4(J) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dat_idxT5 on  T5(T) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT5 on T5(O) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index smint_idxT5 on T5(P) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idxT5 on T5(Q) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dem_idxT5 on T5(S) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index flo_idxT5 on T5(U) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index rel_idxT5 on T5(V) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dou_idxT5 on T5(W) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index tms_idxT5 on T5(X) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index intv_idxT5 on T5(Y) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index char_idxT5 on T5(Z) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index tim_idxT5 on T5(AA) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    defs.test_id='3'
    unnest8_ins._init(_testmgr)
    unnest8_sql._init(_testmgr)
    
    # Semi join queries
    _testmgr.testcase_end(desc)

def test009(desc="""unnest9"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """Create table T1(A int, B  smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T2(C int, D smallint,  E largeint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T3(F int, G  smallint, H largeint , I numeric(9,3));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T4(J int, K smallint, L largeint ,  M numeric(9,3),  N decimal(18,9));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T5(O int, P smallint, Q  largeint, R numeric(9,3),  S decimal(18,9), T char(20), U float(52), V real, W double precision, X timestamp,Y interval year to month ,Z char (12), AA time);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    defs.test_id='1'
    unnest9_ins._init(_testmgr)
    unnest9_sql._init(_testmgr)
    
    stmt = """Create table T1(A int  not null not droppable primary key,
B  smallint default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T2(C int default null,
D smallint not null not droppable primary key,
E largeint default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T3(F int default null,
G smallint default null,
H largeint not null not droppable primary key,
I numeric(9,3) default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T4(J int default null,
K smallint default null,
L largeint default  null ,
M numeric(9,3) not null not droppable primary key,
N decimal(18,9) default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T5(O int default null,
P smallint default null,
Q largeint default null,
R numeric(9,3) not null not droppable primary key,
S decimal(18,9) default null,
T char(20) default null,
U float(52) default null,
V real default null,
W double precision default null,
X timestamp default null,
Y interval year to month default null ,
Z char (12) default null,
AA time default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index smint_idx on T1(B) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idx on T2(E) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idx on T2(C) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index num_idx on T3(I) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idxT3 on T3(G) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT3 on T3(F) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dem_idxT4 on T4(N) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT4 on T4(J) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index sint_idxT4 on T4(K) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idxT4 on T4(L) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dat_idxT5 on  T5(T) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT5 on T5(O) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index smint_idxT5 on T5(P) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idxT5 on T5(Q) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dem_idxT5 on T5(S) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index flo_idxT5 on T5(U) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index rel_idxT5 on T5(V) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dou_idxT5 on T5(W) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index tms_idxT5 on T5(X) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index intv_idxT5 on T5(Y) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index char_idxT5 on T5(Z) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index tim_idxT5 on T5(AA) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    defs.test_id='2'
    unnest9_ins._init(_testmgr)
    unnest9_sql._init(_testmgr)
    
    stmt = """Create table T1(A int  not null not droppable primary key,
B  smallint default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T2(C int default null,
D smallint not null not droppable primary key,
E largeint default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T3(F int not null not droppable ,
G smallint not null not droppable ,
H largeint not null not droppable ,
I numeric(9,3) default null,
primary key (F,G,H) )
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T4          (J int default null,
K smallint not null not droppable,
L largeint not null not droppable,
M numeric(9,3) not null not droppable,
N decimal(18,9) default null,
primary key (K,L,M) )
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Create table T5(O int default null,
P smallint default null,
Q largeint default null,
R numeric(9,3) not null not droppable primary key,
S decimal(18,9) default null,
T char(20) default null,
U float(52) default null,
V real default null,
W double precision default null,
X timestamp default null,
Y interval year to month default null ,
Z char (12) default null,
AA time default null)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index smint_idx on T1(B) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idx on T2(E) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idx on T2(C) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index num_idx on T3(I) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dem_idxT4 on T4(N) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT4 on T4(J) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dat_idxT5 on  T5(T) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index int_idxT5 on T5(O) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index smint_idxT5 on T5(P) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index lint_idxT5 on T5(Q) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dem_idxT5 on T5(S) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index flo_idxT5 on T5(U) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index rel_idxT5 on T5(V) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index dou_idxT5 on T5(W) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index tms_idxT5 on T5(X) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index intv_idxT5 on T5(Y) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index char_idxT5 on T5(Z) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index tim_idxT5 on T5(AA) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    defs.test_id='3'
    unnest9_ins._init(_testmgr)
    unnest9_sql._init(_testmgr)
    
    #             End of Unneset
    _testmgr.testcase_end(desc)

