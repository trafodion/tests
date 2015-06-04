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
    
def test001(desc="""cr8cjdate"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # cr8cjdate
    # create the cjdate tables
    # jclear
    # 1999-06-01
    # C.J.Date DB from An Intro. to Database Systems, Vol I, 5th ed., pp.143 ff.
    #
    #
    # original tables
    #
    stmt = """create table stb (                -- Suppliers
snum      char (5)  not null,
sname     char (20) not null,
status    smallint  not null,
city      char (15) not null,
primary key (snum)
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view s as select * from stb;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table ptb (                -- Parts
pnum      char (6)  not null,
pname     char (20) not null,
color     char (6)  not null,
weight    smallint  not null,
city      char (15) not null,
primary key (pnum)
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view p as select * from ptb;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table jtb (                -- proJects
jnum      char (4)  not null,
jname     char (10) not null,
city      char (15) not null,
primary key (jnum)
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view j as select * from jtb;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table spjtb (
snum  char (5) not null,
pnum  char (6) not null,
jnum  char (4) not null,
qty   int,
primary key (snum, pnum, jnum)
-- , foreign key (snum) references stb,
-- foreign key (pnum) references ptb,
-- foreign key (jnum) references jtb 
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view spj as select * from spjtb;"""
    output = _dci.cmdexec(stmt)
    
    # hash partitioned tables
    #
    stmt = """create table hpstb (                -- Suppliers
snum      char (5)  not null,
sname     char (20) not null,
status    smallint  not null,
city      char (15) not null,
primary key (snum))
STORE BY (snum);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view hps as select * from hpstb;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table hpptb (                -- Parts
pnum      char (6)  not null,
pname     char (20) not null,
color     char (6)  not null,
weight    smallint  not null,
city      char (15) not null,
primary key (pnum))
STORE BY (pnum);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view hpp as select * from hpptb;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table hpjtb (                -- proJects
jnum      char (4)  not null,
jname     char (10) not null,
city      char (15) not null,
primary key (jnum))
STORE BY (jnum);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view hpj as select * from hpjtb;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table hpspjtb (
snum  char (5) not null,
pnum  char (6) not null,
jnum  char (4) not null,
qty   int,
primary key (snum, pnum, jnum))
STORE BY (snum, pnum, jnum);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view hpspj as select * from hpspjtb;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

