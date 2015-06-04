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

# ==================   Begin Test Case Header   ==================
#
#  Test case name:     volt2
#
#	1) Volatile table
#
#  Revision History:
#      01/10/07       Modified wm/wm10 testcase.
#
# =================== End Test Case Header  ===================

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc='a00'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """create volatile table vt_000
(
seqno   integer         not null        not droppable,    

smin1   smallint                default null,    

inte1   integer                 default null,    

lint1   largeint                default null,    

nume1   numeric(9,3)            default null,    

deci1   decimal(18,9)           default null,    

pict1   pic s9(13)v9(5)         default null,    

flot1   float (52)              default null,    

real1   real                    default null,    

dblp1   double precision        default null,    

char1   char (12)               default null,    

vchr1   varchar (12)            default null,    

primary key (seqno)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #) attribute extent 256;
    
    stmt = """insert into vt_000
select * from wm000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 8)
    
    stmt = """create volatile table vt_001
(
seqno   integer         not null        not droppable,    

smin1   smallint                default null,    

inte1   integer                 default null,    

lint1   largeint                default null,    

nume1   numeric(9,3)            default null,    

deci1   decimal(18,9)           default null,    

pict1   pic s9(13)v9(5)         default null,    

flot1   float (52)              default null,    

real1   real                    default null,    

dblp1   double precision        default null,    

char1   char (12)               default null,    

vchr1   varchar (12)            default null,    

primary key (seqno)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #) attribute extent 256;
    
    stmt = """insert into vt_001
select * from wm001;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 7)
    
    ##expectfile ${test_dir}/a00exp a00s0
    #	select	a.seqno,
    #		b.seqno
    #	from	000 a FULL OUTER JOIN 001 b
    #		on a.seqno = b.seqno
    #	order by 1,2;
    
    stmt = """select	a.seqno,
b.seqno
from	wm000 a INNER JOIN vt_001 b
on a.seqno = b.seqno
order by 1,2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a00exp""", 'a00s0')
    
    ##expectfile ${test_dir}/a00exp a00s1
    #	select	a.seqno,
    #		b.seqno,
    #		a.smin1,
    #		b.smin1
    #	from	vt_000 a FULL OUTER JOIN vt_001 b
    #		on a.smin1 = b.smin1
    #	order by 1,2,3,4;
    
    stmt = """select	a.seqno,
b.seqno,
a.smin1,
b.smin1
from	vt_000 a LEFT OUTER JOIN vt_001 b
on a.smin1 = b.smin1
order by 1,2,3,4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a00exp""", 'a00s1')
    
    ##expectfile ${test_dir}/a00exp a00s2
    #	select	a.seqno,
    #		b.seqno,
    #		a.inte1,
    #		b.inte1
    #	from	vt_000 a FULL OUTER JOIN vt_001 b
    #		on a.inte1 = b.inte1
    #	order by 1,2,3,4;
    
    stmt = """select	a.seqno,
b.seqno,
a.inte1,
b.inte1
from	vt_000 a LEFT OUTER JOIN vt_001 b
on a.inte1 = b.inte1
order by 1,2,3,4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a00exp""", 'a00s2')
    
    ##expectfile ${test_dir}/a00exp a00s3
    #	select	a.seqno,
    #		b.seqno,
    #		a.lint1,
    #		b.lint1
    #	from	vt_000 a FULL OUTER JOIN vt_001 b
    #		on a.lint1 = b.lint1
    #	order by 1,2,3,4;
    
    stmt = """select	a.seqno,
b.seqno,
a.lint1,
b.lint1
from	vt_000 a RIGHT OUTER JOIN vt_001 b
on a.lint1 = b.lint1
order by 1,2,3,4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a00exp""", 'a00s3')
    
    ##expectfile ${test_dir}/a00exp a00s4
    #	select	a.seqno,
    #		b.seqno,
    #		a.nume1,
    #		b.nume1
    #	from	vt_000 a FULL OUTER JOIN vt_001 b
    #		on a.nume1 = b.nume1
    #	order by 1,2,3,4;
    
    stmt = """select	a.seqno,
b.seqno,
a.nume1,
b.nume1
from	vt_000 a INNER JOIN vt_001 b
on a.nume1 = b.nume1
order by 1,2,3,4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a00exp""", 'a00s4')
    
    ##expectfile ${test_dir}/a00exp a00s5
    #	select	a.seqno,
    #		b.seqno,
    #		a.deci1,
    #		b.deci1
    #	from	vt_000 a FULL OUTER JOIN vt_001 b
    #		on a.deci1 = b.deci1
    #	order by 1,2,3,4;
    
    stmt = """select	a.seqno,
b.seqno,
a.deci1,
b.deci1
from	vt_000 a INNER JOIN vt_001 b
on a.deci1 = b.deci1
order by 1,2,3,4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a00exp""", 'a00s5')
    
    ##expectfile ${test_dir}/a00exp a00s6
    #	select	a.seqno,
    #		b.seqno,
    #		a.pict1,
    #		b.pict1
    #	from	vt_000 a FULL OUTER JOIN vt_001 b
    #		on a.pict1 = b.pict1
    #	order by 1,2,3,4;
    
    stmt = """select	a.seqno,
b.seqno,
a.flot1,
b.flot1
from	vt_000 a LEFT OUTER JOIN vt_001 b
on a.flot1 = b.flot1
order by 1,2,3,4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a00exp""", 'a00s7')
    
    ##expectfile ${test_dir}/a00exp a00s8
    #	select	a.seqno,
    #		b.seqno,
    #		a.real1,
    #		b.real1
    #	from	vt_000 a FULL OUTER JOIN vt_001 b
    #		on a.real1 = b.real1
    #	order by 1,2,3,4;
    
    stmt = """select	a.seqno,
b.seqno,
a.real1,
b.real1
from	vt_000 a LEFT OUTER JOIN vt_001 b
on a.real1 = b.real1
order by 1,2,3,4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a00exp""", 'a00s8')
    
    ##expectfile ${test_dir}/a00exp a00s9
    #	select	a.seqno,
    #		b.seqno,
    #		a.dblp1,
    #		b.dblp1
    #	from	vt_000 a FULL OUTER JOIN vt_001 b
    #		on a.dblp1 = b.dblp1
    #	order by 1,2,3,4;
    
    stmt = """select	a.seqno,
b.seqno,
a.dblp1,
b.dblp1
from	vt_000 a LEFT OUTER JOIN vt_001 b
on a.dblp1 = b.dblp1
order by 1,2,3,4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a00exp""", 'a00s9')
    
    ##expectfile ${test_dir}/a00exp a00s10
    #	select	a.seqno,
    #		b.seqno,
    #		a.char1,
    #		b.char1
    #	from	vt_000 a FULL OUTER JOIN vt_001 b
    #		on a.char1 = b.char1
    #	order by 1,2,3,4;
    
    stmt = """select	a.seqno,
b.seqno,
a.char1,
b.char1
from	vt_000 a INNER JOIN vt_001 b
on a.char1 = b.char1
order by 1,2,3,4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a00exp""", 'a00s10')
    
    ##expectfile ${test_dir}/a00exp a00s11
    #	select	a.seqno,
    #		b.seqno,
    #		a.vchr1,
    #		b.vchr1
    #	from	vt_000 a FULL OUTER JOIN vt_001 b
    #		on a.vchr1 = b.vchr1
    #	order by 1,2,3,4;
    
    stmt = """select	a.seqno,
b.seqno,
a.vchr1,
b.vchr1
from	vt_000 a LEFT OUTER JOIN vt_001 b
on a.vchr1 = b.vchr1
order by 1,2,3,4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a00exp""", 'a00s11')
    
    _testmgr.testcase_end(desc)

