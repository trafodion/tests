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

#opt/hcube4/testcase
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc='Star Join with 4 dimensions'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # fact table key completely covered, no local predicates on dimension
    # ordering of dimension table by clustering key of fact table
    
    stmt = """showshape
select fact.a, fact.b, fact.c, fact.d, fact.txt
from
 """ + gvars.g_schema_hcubedb + """.CUBE3 fact,  -- key: a,b,c,d  10,000,000 rows
 """ + gvars.g_schema_hcubedb + """.T0 dim0,  -- key: a                10 rows
 """ + gvars.g_schema_hcubedb + """.T1 dim1,  -- key: a                10 rows
 """ + gvars.g_schema_hcubedb + """.T2 dim2,  -- key: a                10 rows
 """ + gvars.g_schema_hcubedb + """.T3 dim3  -- key: a                10 rows
where
fact.a = dim0.a  and
fact.b = dim1.a  and
fact.c = dim2.a  and
fact.d = dim3.a;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
select fact.a, fact.b, fact.c, fact.d, fact.txt
from
 """ + gvars.g_schema_hcubedb + """.CUBE3 fact,  -- key: a,b,c,d  10,000,000 rows
 """ + gvars.g_schema_hcubedb + """.T0 dim0,  -- key: a                10 rows
 """ + gvars.g_schema_hcubedb + """.T1 dim1,  -- key: a                10 rows
 """ + gvars.g_schema_hcubedb + """.T2 dim2,  -- key: a                10 rows
 """ + gvars.g_schema_hcubedb + """.T3 dim3  -- key: a                10 rows
where
fact.a = dim0.a  and
fact.b = dim1.a  and
fact.c = dim2.a  and
fact.d = dim3.a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A01exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A01exp P2
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    # NCI set envvar NO_SCREEN_OUTPUT;
    # #expectfile $test_dir/A01exp P3
    # NCI #expect any *row(s) selected*
    # NCI execute xx;
    # NCI reset envvar NO_SCREEN_OUTPUT;
    
    ##expectstat $test_dir/A01exp P4
    # NCI display statistics;
    
    _testmgr.testcase_end(desc)

def test002(desc='Star Join with 4 dimensions'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # fact table completely covered, local predicates on dimension tables
    # fact table should be last, innermost table
    
    stmt = """showshape
select fact.a, fact.b, fact.c, fact.d, fact.txt
from
 """ + gvars.g_schema_hcubedb + """.CUBE3 fact,
 """ + gvars.g_schema_hcubedb + """.T0 dim0,
 """ + gvars.g_schema_hcubedb + """.T1 dim1,
 """ + gvars.g_schema_hcubedb + """.T2 dim2,
 """ + gvars.g_schema_hcubedb + """.T3 dim3
where
fact.a = dim0.a  and
fact.b = dim1.a  and
fact.c = dim2.a  and
fact.d = dim3.a  and
dim0.b = 1       and
dim1.b = 2       and
dim2.b = 3       and
dim3.b = 4;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
select fact.a, fact.b, fact.c, fact.d, fact.txt
from
 """ + gvars.g_schema_hcubedb + """.CUBE3 fact,
 """ + gvars.g_schema_hcubedb + """.T0 dim0,
 """ + gvars.g_schema_hcubedb + """.T1 dim1,
 """ + gvars.g_schema_hcubedb + """.T2 dim2,
 """ + gvars.g_schema_hcubedb + """.T3 dim3
where
fact.a = dim0.a  and
fact.b = dim1.a  and
fact.c = dim2.a  and
fact.d = dim3.a  and
dim0.b = 1       and
dim1.b = 2       and
dim2.b = 3       and
dim3.b = 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A02exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A02exp P2
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    # NCI set envvar NO_SCREEN_OUTPUT;
    # #expectfile $test_dir/A02exp P3
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    # NCI reset envvar NO_SCREEN_OUTPUT;
    
    ##expectstat $test_dir/A02exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test003(desc='Star Join with 3 dimensions'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # fact table key partially covered
    # local equality predicates
    # fact should be last, innermost table
    
    stmt = """showshape
select fact.a, fact.b, fact.c, fact.d, fact.txt
from
 """ + gvars.g_schema_hcubedb + """.CUBE3 fact,
 """ + gvars.g_schema_hcubedb + """.T0 dim0,
 """ + gvars.g_schema_hcubedb + """.T1 dim1,
 """ + gvars.g_schema_hcubedb + """.T2 dim2
where
fact.a = dim0.a  and
fact.b = dim1.a  and
fact.c = dim2.a  and
dim0.b = 1       and
dim1.b = 2       and
dim2.b = 3;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
select fact.a, fact.b, fact.c, fact.d, fact.txt
from
 """ + gvars.g_schema_hcubedb + """.CUBE3 fact,
 """ + gvars.g_schema_hcubedb + """.T0 dim0,
 """ + gvars.g_schema_hcubedb + """.T1 dim1,
 """ + gvars.g_schema_hcubedb + """.T2 dim2
where
fact.a = dim0.a  and
fact.b = dim1.a  and
fact.c = dim2.a  and
dim0.b = 1       and
dim1.b = 2       and
dim2.b = 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A03exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A03exp P2
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    # NCI set envvar NO_SCREEN_OUTPUT;
    ##expectfile $test_dir/A03exp P3
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    # NCI reset envvar NO_SCREEN_OUTPUT;
    
    ##expectstat $test_dir/A03exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test004(desc='Star Join with 5 dimensions'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # check for key ordering of dimension tables
    # all key previx dimension tables are forced to be below the fact table
    # except for dim4 which is not a key column
    
    stmt = """showshape
select count(*)
from
 """ + gvars.g_schema_hcubedb + """.CUBE3 fact, -- key: a,b,c,d  10,000,000 rows
 """ + gvars.g_schema_hcubedb + """.T66   dim0, -- key: a               100 rows
 """ + gvars.g_schema_hcubedb + """.T1    dim1, -- key: a                10 rows
 """ + gvars.g_schema_hcubedb + """.T2    dim2, -- key: a                10 rows
 """ + gvars.g_schema_hcubedb + """.T3    dim3, -- key: a                10 rows
 """ + gvars.g_schema_hcubedb + """.T4    dim4  -- key: a                10 rows
where
fact.a = dim0.a and
fact.b = dim1.a and
fact.c = dim2.a and
fact.d = dim3.a and
fact.e = dim4.a and
dim0.b < 8      and
dim1.b < 7      and
dim2.b < 6      and
dim3.b < 4      and
dim4.b < 2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
select count(*)
from
 """ + gvars.g_schema_hcubedb + """.CUBE3 fact, -- key: a,b,c,d  10,000,000 rows
 """ + gvars.g_schema_hcubedb + """.T66   dim0, -- key: a               100 rows
 """ + gvars.g_schema_hcubedb + """.T1    dim1, -- key: a                10 rows
 """ + gvars.g_schema_hcubedb + """.T2    dim2, -- key: a                10 rows
 """ + gvars.g_schema_hcubedb + """.T3    dim3, -- key: a                10 rows
 """ + gvars.g_schema_hcubedb + """.T4    dim4  -- key: a                10 rows
where
fact.a = dim0.a and
fact.b = dim1.a and
fact.c = dim2.a and
fact.d = dim3.a and
fact.e = dim4.a and
dim0.b < 8      and
dim1.b < 7      and
dim2.b < 6      and
dim3.b < 4      and
dim4.b < 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A04exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A04exp P2
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    # NCI set envvar NO_SCREEN_OUTPUT;
    ##expectfile $test_dir/A04exp P3
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    # NCI reset envvar NO_SCREEN_OUTPUT;
    
    ##expectstat $test_dir/A04exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test005(desc='Star Join with 3 dimensions'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # query to check for choice of prime table
    # prime table should be cube3 since it has highest cardinality after
    # application of all local key predicates
    
    
    stmt = """showshape
select count(*)
from
 """ + gvars.g_schema_hcubedb + """.CUBE2 dim1,  -- key: a,b,c    1,000,000 rows
 """ + gvars.g_schema_hcubedb + """.T1    dim2,  -- key: a               10 rows
 """ + gvars.g_schema_hcubedb + """.T2    dim3,  -- key: a               10 rows
 """ + gvars.g_schema_hcubedb + """.CUBE3 fact   -- key: a,b,c,d 10,000,000 rows
where
fact.a = dim1.c and
fact.b = dim1.e and
fact.c = dim2.a and
fact.e = dim3.a and
dim2.c = 1      and
dim3.b = 1      and
dim1.a < 2      and
dim1.b < 2      and
dim1.f < 10     and
fact.d = 1      and
fact.f < 2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
select count(*)
from
 """ + gvars.g_schema_hcubedb + """.CUBE2 dim1,  -- key: a,b,c    1,000,000 rows
 """ + gvars.g_schema_hcubedb + """.T1    dim2,  -- key: a               10 rows
 """ + gvars.g_schema_hcubedb + """.T2    dim3,  -- key: a               10 rows
 """ + gvars.g_schema_hcubedb + """.CUBE3 fact   -- key: a,b,c,d 10,000,000 rows
where
fact.a = dim1.c and
fact.b = dim1.e and
fact.c = dim2.a and
fact.e = dim3.a and
dim2.c = 1      and
dim3.b = 1      and
dim1.a < 2      and
dim1.b < 2      and
dim1.f < 10     and
fact.d = 1      and
fact.f < 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A05exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A05exp P2
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    ##expectfile $test_dir/A05exp P3
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    ##expectstat $test_dir/A05exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test006(desc='Star Join with 3 dimensions'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # query to test prime table selection
    # cube3 should be prime
    
    stmt = """showshape
select count(*)
from
 """ + gvars.g_schema_hcubedb + """.CUBE3 fact, -- key: a,b,c,d 10,000,000 rows
 """ + gvars.g_schema_hcubedb + """.CUBE2 dim1, -- key: a,b,c    1,000,000 rows
 """ + gvars.g_schema_hcubedb + """.T1    dim2, -- key: a               10 rows
 """ + gvars.g_schema_hcubedb + """.T2    dim3  -- key: a               10 rows
where
fact.a = dim2.a and
fact.b = dim3.a and
fact.c = dim1.c and
fact.e = dim1.e and
dim2.c < 5      and
dim3.b < 6      and
dim1.a < 5      and
dim1.b < 2      and
dim1.f < 500    and
fact.d < 100    and
fact.f < 2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
select count(*)
from
 """ + gvars.g_schema_hcubedb + """.CUBE3 fact, -- key: a,b,c,d 10,000,000 rows
 """ + gvars.g_schema_hcubedb + """.CUBE2 dim1, -- key: a,b,c    1,000,000 rows
 """ + gvars.g_schema_hcubedb + """.T1    dim2, -- key: a               10 rows
 """ + gvars.g_schema_hcubedb + """.T2    dim3  -- key: a               10 rows
where
fact.a = dim2.a and
fact.b = dim3.a and
fact.c = dim1.c and
fact.e = dim1.e and
dim2.c < 5      and
dim3.b < 6      and
dim1.a < 5      and
dim1.b < 2      and
dim1.f < 500    and
fact.d < 100    and
fact.f < 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A06exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A06exp P2
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    ##expectfile $test_dir/A06exp P3
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    ##expectstat $test_dir/A06exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test007(desc='Star Join with 4 dimensions'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #query to test prime table selection
    #join pattern should not match type-1 plan
    
    stmt = """showshape
select fact.a, fact.b, fact.e, fact.txt
from
 """ + gvars.g_schema_hcubedb + """.CUBE3 fact,
 """ + gvars.g_schema_hcubedb + """.CUBE2 dim1,
 """ + gvars.g_schema_hcubedb + """.CUBE1 dim2,
 """ + gvars.g_schema_hcubedb + """.T1    dim3,
 """ + gvars.g_schema_hcubedb + """.T2    dim4,
 """ + gvars.g_schema_hcubedb + """.T3    dim11,
 """ + gvars.g_schema_hcubedb + """.T4    dim21
where
fact.a = dim1.e  and
fact.e = dim1.b  and
fact.b = dim2.d  and
fact.f = dim2.b  and
fact.c = dim3.a  and
fact.d = dim4.a  and
dim1.c = dim11.b and
dim2.c = dim21.b and
fact.e < 2       and
fact.f < 2       and
dim1.a < 10      and
dim1.f < 90      and
dim2.a < 5       and
dim11.a < 5      and
dim21.a < 5      and
dim3.b < 4       and
dim4.b < 5;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
select fact.a, fact.b, fact.e, fact.txt
from
 """ + gvars.g_schema_hcubedb + """.CUBE3 fact,
 """ + gvars.g_schema_hcubedb + """.CUBE2 dim1,
 """ + gvars.g_schema_hcubedb + """.CUBE1 dim2,
 """ + gvars.g_schema_hcubedb + """.T1    dim3,
 """ + gvars.g_schema_hcubedb + """.T2    dim4,
 """ + gvars.g_schema_hcubedb + """.T3    dim11,
 """ + gvars.g_schema_hcubedb + """.T4    dim21
where
fact.a = dim1.e  and
fact.e = dim1.b  and
fact.b = dim2.d  and
fact.f = dim2.b  and
fact.c = dim3.a  and
fact.d = dim4.a  and
dim1.c = dim11.b and
dim2.c = dim21.b and
fact.e < 2       and
fact.f < 2       and
dim1.a < 10      and
dim1.f < 90      and
dim2.a < 5       and
dim11.a < 5      and
dim21.a < 5      and
dim3.b < 4       and
dim4.b < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A07exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A07exp P2
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    # NCI set envvar NO_SCREEN_OUTPUT;
    ##expectfile $test_dir/A07exp P3
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    # NCI reset envvar NO_SCREEN_OUTPUT;
    
    ##expectstat $test_dir/A07exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test008(desc='Star Join with 3 dimensions'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # prime table rule used in pass 1
    # no join predicate on prefix of fact clustering key, so no type-1 star
    
    stmt = """showshape
select count(*)
from
 """ + gvars.g_schema_hcubedb + """.CUBE3 fact, -- key a,b,c,d 10,000,000 rows
 """ + gvars.g_schema_hcubedb + """.T1    dim1, -- key a               10 rows
 """ + gvars.g_schema_hcubedb + """.T2    dim2, -- key a               10 rows
 """ + gvars.g_schema_hcubedb + """.T3    dim3  -- key a               10 rows
where
fact.d = dim1.a and
fact.e = dim2.a and
fact.f = dim3.a and
dim1.b < 1      and
dim2.b < 2      and
dim3.b < 3;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
select count(*)
from
 """ + gvars.g_schema_hcubedb + """.CUBE3 fact, -- key a,b,c,d 10,000,000 rows
 """ + gvars.g_schema_hcubedb + """.T1    dim1, -- key a               10 rows
 """ + gvars.g_schema_hcubedb + """.T2    dim2, -- key a               10 rows
 """ + gvars.g_schema_hcubedb + """.T3    dim3  -- key a               10 rows
where
fact.d = dim1.a and
fact.e = dim2.a and
fact.f = dim3.a and
dim1.b < 1      and
dim2.b < 2      and
dim3.b < 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A08exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A08exp P2
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    # NCI set envvar NO_SCREEN_OUTPUT;
    ##expectfile $test_dir/A08exp P3
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    # NCI reset envvar NO_SCREEN_OUTPUT;
    
    ##expectstat $test_dir/A08exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

