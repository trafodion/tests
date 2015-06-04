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
    _dci.setup_schema(defs.my_schema)

    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table t1 (a int, b int, c int, d int, e int) no partitions attribute extent (128);"""
    output = _dci.cmdexec(stmt)
    stmt = """create table t2 (a int, b int, c int, d int, e int) no partitions attribute extent (128);"""
    output = _dci.cmdexec(stmt)
    stmt = """create table t3 (a int, b int, c int, d int, e int) no partitions attribute extent (128);"""
    output = _dci.cmdexec(stmt)
    stmt = """create table t4 (a int, b int, c int, d int, e int) no partitions attribute extent (128);"""
    output = _dci.cmdexec(stmt)
    stmt = """create table t5 (a int, b int, c int, d int, e int) no partitions attribute extent (128);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into t1
select x1 + 10*x2,
2*(x1 + 10*x2),
3*(x1 + 10*x2),
4*(x1 + 10*x2),
5*(x1 + 10*x2)
from (values(0)) T
transpose 0,1,2,3,4,5,6,7,8,9 as x2
transpose 0,1,2,3,4,5,6,7,8,9 as x1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into t2 select * from t1;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into t3 select * from t1;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into t4 select * from t1;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into t5 select * from t1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table p1 (a int no default not null, b int, c int, d int, e int, primary key(a)) number of partitions 2 attributes extent(128);"""
    output = _dci.cmdexec(stmt)
    stmt = """create table p2 (a int no default not null, b int, c int, d int, e int, primary key(a)) number of partitions 2 attributes extent(128);"""
    output = _dci.cmdexec(stmt)
    stmt = """create table p3 (a int no default not null, b int, c int, d int, e int, primary key(a)) number of partitions 2 attributes extent(128);"""
    output = _dci.cmdexec(stmt)
    stmt = """create table p4 (a int no default not null, b int, c int, d int, e int, primary key(a)) number of partitions 2 attributes extent(128);"""
    output = _dci.cmdexec(stmt)
    stmt = """create table p5 (a int no default not null, b int, c int, d int, e int, primary key(a)) number of partitions 2 attributes extent(128);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into p1
select x1 + 10*x2,
2*(x1 + 10*x2),
3*(x1 + 10*x2),
4*(x1 + 10*x2),
5*(x1 + 10*x2)
from (values(0)) T
transpose 0 as x2
transpose 0,1,2,3,4,5,6,7,8,9 as x1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into p2 select * from p1;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into p3 select * from p1;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into p4 select * from p1;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into p5 select * from p1;"""
    output = _dci.cmdexec(stmt)
    
