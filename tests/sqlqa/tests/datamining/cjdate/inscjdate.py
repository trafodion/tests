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
    
def test001(desc="""inscjdate"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # inscjdate
    # load the cjdate tables
    # jclear
    # 1999-06-01
    #
    # original tables
    stmt = """insert into s values
('s1', 'Smith', 20, 'London'),
('s2', 'Jones', 10, 'Paris'),
('s3', 'Blake', 30, 'Paris'),
('s4', 'Clark', 20, 'London'),
('s5', 'Adams', 30, 'Athens');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select count (*) from s;"""
    output = _dci.cmdexec(stmt)
    # expect count = 5
    
    stmt = """insert into p values
('p1', 'nut',   'red',   12, 'London'),
('p2', 'bolt',  'green', 17, 'Paris' ),
('p3', 'screw', 'blue',  17, 'Rome'  ),
('p4', 'screw', 'red',   14, 'London'),
('p5', 'cam',   'blue',  12, 'Paris' ),
('p6', 'cog',   'red',   19, 'London');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select count (*) from p;"""
    output = _dci.cmdexec(stmt)
    # expect count = 6
    
    stmt = """insert into j values
('j1', 'sorter',   'Paris' ),
('j2', 'punch',    'Rome'  ),
('j3', 'reader',   'Athens'),
('j4', 'console',  'Athens'),
('j5', 'collator', 'London'),
('j6', 'terminal', 'Oslo'  ),
('j7', 'tape',     'London');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select count (*) from j;"""
    output = _dci.cmdexec(stmt)
    # expect count = 7
    
    stmt = """insert into spj values
('s1', 'p1', 'j1', 200),
('s1', 'p1', 'j4', 700),
('s2', 'p3', 'j1', 400),
('s2', 'p3', 'j2', 200),
('s2', 'p3', 'j3', 200),
('s2', 'p3', 'j4', 500),
('s2', 'p3', 'j5', 600),
('s2', 'p3', 'j6', 400),
('s2', 'p3', 'j7', 800),
('s2', 'p5', 'j2', 100),
('s3', 'p3', 'j1', 200),
('s3', 'p4', 'j2', 500),
('s4', 'p6', 'j3', 300),
('s4', 'p6', 'j7', 300),
('s5', 'p2', 'j2', 200),
('s5', 'p2', 'j4', 100),
('s5', 'p5', 'j5', 500),
('s5', 'p5', 'j7', 100),
('s5', 'p6', 'j2', 200),
('s5', 'p1', 'j4', 100),
('s5', 'p3', 'j4', 200),
('s5', 'p4', 'j4', 800),
('s5', 'p5', 'j4', 400),
('s5', 'p6', 'j4', 500);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select count (*) from spj;"""
    output = _dci.cmdexec(stmt)
    # expect count = 24
    
    # hash partitioned tables
    stmt = """insert into hps select * from s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into hpp select * from p;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into hpj select * from j;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into hpspj select * from spj;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

