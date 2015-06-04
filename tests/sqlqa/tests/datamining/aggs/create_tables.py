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
    
def test001(desc="""create_tables"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # cr8aggs.sql
    # jclear
    # 22 Apr 1997
    # Set up for the new aggreate functions tests (Variance and StdDev).
    #
    # create catalog;
    #
    # tests 1-7,10,12 (loaded with insrt500)
    stmt = """create table small500 (
counter   int not null primary key,            -- 1 - 500
smallcol  smallint,       -- random small ints
fivehun21 int,            -- 500 - 1
nulls     int,
zeroes    int,
ones      int,
one0one   int
);"""
    output = _dci.cmdexec(stmt)
    
    # test008 (loaded with inhasnul)
    stmt = """create table hasnulls (
counter   int not null primary key,            -- 1 - 500
nulls  int
);"""
    output = _dci.cmdexec(stmt)
    
    # tests 9-12,15 (loaded with insin500)
    stmt = """create table ints500 (
counter   int not null primary key,            -- 1 - 500
 small500  smallint,
int500    int
);"""
    output = _dci.cmdexec(stmt)
    
    # test015 (loaded with in500bak - after insin500)
    stmt = """create table in500bak (
counter   int not null primary key,            -- 1 - 500
 small500  smallint,
int500    int
);"""
    output = _dci.cmdexec(stmt)
    
    # test 12 (loaded with inswghts)
    stmt = """create table weights (
counter   int not null primary key,            -- 1 - 500
 small500  smallint,
int500    int,
weight    int
);"""
    output = _dci.cmdexec(stmt)
    
    # test 13,14 (loaded with insminmax)
    stmt = """create table minmax (
counter  int not null primary key,
minint   int,
maxint   int,
minsmall smallint,
maxsmall smallint
);"""
    output = _dci.cmdexec(stmt)
    
    # test 16 (loaded with insflt100)
    stmt = """create table float100 (
counter int not null primary key,
flt100  float
);"""
    output = _dci.cmdexec(stmt)
    
    # test 17 (loaded with insrl100 - after insflt100)
    stmt = """create table real100 (
counter int not null primary key,
rl100  real
);"""
    output = _dci.cmdexec(stmt)
    
    # test 18 (loaded with indbl100)
    stmt = """create table dbls100 (
counter int not null primary key,
dbl100  double precision
);"""
    output = _dci.cmdexec(stmt)
    
    # test 19 (loaded with innum100)
    stmt = """create table num100 (
counter int not null primary key,
num     numeric (18, 5)
);"""
    output = _dci.cmdexec(stmt)
    
    # test 20 (loaded with indec100)
    stmt = """create table dec100 (
counter int not null primary key,
num     decimal (18, 5) signed
);"""
    output = _dci.cmdexec(stmt)
    
    # test 21 (loaded with insintrvl)
    stmt = """create table intrval (
iyr  interval year ,
imon interval month,
idy  interval day,
ihr  interval hour,
imin interval minute,
isec interval second,
cnt int not null primary key
);"""
    output = _dci.cmdexec(stmt)
    
    # test 24 (loaded with inlar75)
    stmt = """create table lar75 (
counter int not null primary key,
lar     largeint
);"""
    output = _dci.cmdexec(stmt)
    _testmgr.testcase_end(desc)

