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
    
def test001(desc='Create tables'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # create tables
    
    # stmt = """control query default pos_num_of_partns '1';"""
    # output = _dci.cmdexec(stmt)
    stmt = """create table t0 (a int not null not droppable, b int, c int, primary key (a))"""
    if hpdci.tgtTR():
        stmt += """ salt using """ + defs.num_salt_partitions + """ partitions;"""
    else:
        stmt += """ attributes extent (16,64) maxextents 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table t1 (a int not null not droppable, b int, c int, primary key (a))"""
    if hpdci.tgtTR():
        stmt += """ salt using """ + defs.num_salt_partitions + """ partitions;"""
    else:
        stmt += """ attributes extent (16,64) maxextents 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table t2 (a int not null not droppable, b int, c int, primary key (a))"""
    if hpdci.tgtTR():
        stmt += """ salt using """ + defs.num_salt_partitions + """ partitions;"""
    else:
        stmt += """ attributes extent (16,64) maxextents 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table t3 (a int not null not droppable, b int, c int, primary key (a))"""
    if hpdci.tgtTR():
        stmt += """ salt using """ + defs.num_salt_partitions + """ partitions;"""
    else:
        stmt += """ attributes extent (16,64) maxextents 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table t4 (a int not null not droppable, b int, c int, primary key (a))"""
    if hpdci.tgtTR():
        stmt += """ salt using """ + defs.num_salt_partitions + """ partitions;"""
    else:
        stmt += """ attributes extent (16,64) maxextents 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table t5 (a int not null not droppable, b int, c int, primary key (a))"""
    if hpdci.tgtTR():
        stmt += """ salt using """ + defs.num_salt_partitions + """ partitions;"""
    else:
        stmt += """ attributes extent (16,64) maxextents 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table t6 (a int not null not droppable, b int, c int, primary key (a))"""
    if hpdci.tgtTR():
        stmt += """ salt using """ + defs.num_salt_partitions + """ partitions;"""
    else:
        stmt += """ attributes extent (16,64) maxextents 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table t66 (a int not null not droppable, b int, c int, primary key (a))"""
    if hpdci.tgtTR():
        stmt += """ salt using """ + defs.num_salt_partitions + """ partitions;"""
    else:
        stmt += """ attributes extent (16,64) maxextents 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table t7 (a int not null not droppable, b int, c int, primary key (a))"""
    if hpdci.tgtTR():
        stmt += """ salt using """ + defs.num_salt_partitions + """ partitions;"""
    else:
        stmt += """ attributes extent (16,64) maxextents 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table t8 (a int not null not droppable, b int, c int, primary key (a))"""
    if hpdci.tgtTR():
        stmt += """ salt using """ + defs.num_salt_partitions + """ partitions;"""
    else:
        stmt += """ attributes extent (16,64) maxextents 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table t9 (a int not null not droppable, b int, c int, primary key (a))"""
    if hpdci.tgtTR():
        stmt += """ salt using """ + defs.num_salt_partitions + """ partitions;"""
    else:
        stmt += """ attributes extent (16,64) maxextents 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table t10 (a int not null not droppable, b int, c int, primary key (a))"""
    if hpdci.tgtTR():
        stmt += """ salt using """ + defs.num_salt_partitions + """ partitions;"""
    else:
        stmt += """ attributes extent (16,64) maxextents 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table t11 (a int not null not droppable, b int, c int, primary key (a))"""
    if hpdci.tgtTR():
        stmt += """ salt using """ + defs.num_salt_partitions + """ partitions;"""
    else:
        stmt += """ attributes extent (16,64) maxextents 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table t12 (a int not null not droppable, b int, c int, primary key (a))"""
    if hpdci.tgtTR():
        stmt += """ salt using """ + defs.num_salt_partitions + """ partitions;"""
    else:
        stmt += """ attributes extent (16,64) maxextents 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # stmt = """control query default pos_num_of_partns 'SYSTEM';"""
    # output = _dci.cmdexec(stmt)
    stmt = """create table cube1
(a int not null not droppable,
b int not null not droppable,
c int not null not droppable,
d int, e int, f int, txt char(100),
primary key (a,b,c))
store by primary key"""
    if hpdci.tgtTR():
        stmt += """ salt using """ + defs.num_salt_partitions + """ partitions;"""
    else:
        stmt += """ attribute extent (100, 100) maxextents 700 hash partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table cube2
(a int not null not droppable,
b int not null not droppable,
c int not null not droppable,
d int, e int, f int, txt char(100),
primary key (a,b,c))
store by primary key"""
    if hpdci.tgtTR():
        stmt += """ salt using """ + defs.num_salt_partitions + """ partitions;"""
    else:
        stmt += """ attribute extent (1024,1024) maxextents 700 hash partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table cube3
(a int not null not droppable,
b int not null not droppable,
c int not null not droppable,
d int not null not droppable,
e int, f int,txt char(100),
primary key (a,b,c,d))
store by primary key"""
    if hpdci.tgtTR():
        stmt += """ salt using """ + defs.num_salt_partitions + """ partitions;"""
    else:
        stmt += """ attribute extent (4096, 4096) maxextents 700 hash partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # 100M row table
    stmt = """create table cube4
(a int not null not droppable,
b int not null not droppable,
c int not null not droppable,
d int not null not droppable,
e int, f int,
primary key (a,b,c,d))
store by primary key"""
    if hpdci.tgtTR():
        stmt += """ salt using """ + defs.num_salt_partitions + """ partitions;"""
    else:
        stmt += """ attribute extent (4096, 4096) maxextents 700 hash partition;"""
    output = _dci.cmdexec(stmt)
    # table cube5 pretty big, and not used at present
    # create only when necessary
    # 1 Billion row tablei
    #create table cube5
    #(a largeint not null not droppable,
    #b largeint not null not droppable,
    #c largeint not null not droppable,
    #d largeint not null not droppable,
    #e largeint, f largeint,
    #primary key (a,b,c,d))
    # store by primary key
    #attribute extent (4096, 4096) maxextents 700
    #hash partition
    #;
    
    _testmgr.testcase_end(desc)

