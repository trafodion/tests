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
    
def test001(desc='TPCD -- OR optimization test'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """showshape
select * from """ + gvars.g_schema_tpch2x + """.region r1,""" + gvars.g_schema_tpch2x + """.region r2, """ + gvars.g_schema_tpch2x + """.nation, """ + gvars.g_schema_tpch2x + """.supplier,
 """ + gvars.g_schema_tpch2x + """.customer, """ + gvars.g_schema_tpch2x + """.orders, """ + gvars.g_schema_tpch2x + """.lineitem, """ + gvars.g_schema_tpch2x + """.part, """ + gvars.g_schema_tpch2x + """.partsupp 
where r1.r_name='ASIA' and r1.r_regionkey > r2.r_regionkey
and (r2.r_regionkey = n_regionkey OR r1.r_regionkey = n_regionkey)
and n_nationkey = s_nationkey and n_nationkey = c_nationkey
and c_custkey=o_custkey
and p_name like '%plum%'
and p_partkey=ps_partkey and ps_partkey = l_partkey
and ps_suppkey=l_suppkey
and l_orderkey <> o_orderkey;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
select * from """ + gvars.g_schema_tpch2x + """.region r1,""" + gvars.g_schema_tpch2x + """.region r2, """ + gvars.g_schema_tpch2x + """.nation, """ + gvars.g_schema_tpch2x + """.supplier,
 """ + gvars.g_schema_tpch2x + """.customer, """ + gvars.g_schema_tpch2x + """.orders, """ + gvars.g_schema_tpch2x + """.lineitem, """ + gvars.g_schema_tpch2x + """.part, """ + gvars.g_schema_tpch2x + """.partsupp 
where r1.r_name='ASIA' and r1.r_regionkey > r2.r_regionkey
and (r2.r_regionkey = n_regionkey OR r1.r_regionkey = n_regionkey)
and n_nationkey = s_nationkey and n_nationkey = c_nationkey
and c_custkey=o_custkey
and p_name like '%plum%'
and p_partkey=ps_partkey and ps_partkey = l_partkey
and ps_suppkey=l_suppkey
and l_orderkey <> o_orderkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A01exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A01exp P2
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    ##expectfile $test_dir/A01exp P3
    #execute xx;
    
    ##expectstat $test_dir/A01exp P4
    # NCI display statistics;
    
    _testmgr.testcase_end(desc)

def test002(desc='TPCD -- AND optimization tests'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """showshape
select * from """ + gvars.g_schema_tpch2x + """.part p1, """ + gvars.g_schema_tpch2x + """.supplier s1, """ + gvars.g_schema_tpch2x + """.partsupp, """ + gvars.g_schema_tpch2x + """.part p2, """ + gvars.g_schema_tpch2x + """.supplier s2, """ + gvars.g_schema_tpch2x + """.lineitem 
where p1.p_name=?
and s1.s_name=?
and p1.p_partkey=ps_partkey and ps_partkey=p2.p_partkey and p2.p_partkey=l_partkey
and s1.s_suppkey=ps_suppkey and ps_suppkey=s2.s_suppkey and s2.s_suppkey=l_suppkey;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
select * from """ + gvars.g_schema_tpch2x + """.part p1, """ + gvars.g_schema_tpch2x + """.supplier s1, """ + gvars.g_schema_tpch2x + """.partsupp, """ + gvars.g_schema_tpch2x + """.part p2, """ + gvars.g_schema_tpch2x + """.supplier s2, """ + gvars.g_schema_tpch2x + """.lineitem 
where p1.p_name=?
and s1.s_name=?
and p1.p_partkey=ps_partkey and ps_partkey=p2.p_partkey and p2.p_partkey=l_partkey
and s1.s_suppkey=ps_suppkey and ps_suppkey=s2.s_suppkey and s2.s_suppkey=l_suppkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A02exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A02exp P2
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx using 'azure peach dodger frosted lavender','Supplier#000000123';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    ##expectstat $test_dir/A02exp P4
    # NCI display statistics;
    
    _testmgr.testcase_end(desc)

def test003(desc='TPCD 4-way join'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """showshape
select count(*) from """ + gvars.g_schema_tpch2x + """.lineitem, """ + gvars.g_schema_tpch2x + """.orders, """ + gvars.g_schema_tpch2x + """.customer, """ + gvars.g_schema_tpch2x + """.supplier 
where o_totalprice > 541000 and c_acctbal > 9950
and l_quantity < 3 and l_extendedprice > 104500
and l_orderkey = o_orderkey and o_custkey = c_custkey
and l_suppkey = s_suppkey and s_name = c_name;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
select count(*) from """ + gvars.g_schema_tpch2x + """.lineitem, """ + gvars.g_schema_tpch2x + """.orders, """ + gvars.g_schema_tpch2x + """.customer, """ + gvars.g_schema_tpch2x + """.supplier 
where o_totalprice > 541000 and c_acctbal > 9950
and l_quantity < 3 and l_extendedprice > 104500
and l_orderkey = o_orderkey and o_custkey = c_custkey
and l_suppkey = s_suppkey and s_name = c_name;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A03exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A03exp P2
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A03exp""", 'P3')
    
    ##expectstat $test_dir/A03exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test004(desc='TPCD 4-way join'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """showshape
select count(*) from """ + gvars.g_schema_tpch2x + """.lineitem, """ + gvars.g_schema_tpch2x + """.orders, """ + gvars.g_schema_tpch2x + """.customer, """ + gvars.g_schema_tpch2x + """.supplier 
where o_totalprice > 541000 and c_acctbal > 9950
and l_quantity < 3 and l_extendedprice > 104500
and l_orderkey = o_orderkey and o_custkey = c_custkey
and l_suppkey = s_suppkey;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
select count(*) from """ + gvars.g_schema_tpch2x + """.lineitem, """ + gvars.g_schema_tpch2x + """.orders, """ + gvars.g_schema_tpch2x + """.customer, """ + gvars.g_schema_tpch2x + """.supplier 
where o_totalprice > 541000 and c_acctbal > 9950
and l_quantity < 3 and l_extendedprice > 104500
and l_orderkey = o_orderkey and o_custkey = c_custkey
and l_suppkey = s_suppkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A04exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A04exp P2
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A04exp""", 'P3')
    
    ##expectstat $test_dir/A04exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test005(desc='TPCD fully connected 8-way join'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """showshape
select count(*) from """ + gvars.g_schema_tpch2x + """.part p1, """ + gvars.g_schema_tpch2x + """.partsupp ps1, """ + gvars.g_schema_tpch2x + """.lineitem l1,
 """ + gvars.g_schema_tpch2x + """.part p2, """ + gvars.g_schema_tpch2x + """.partsupp ps2, """ + gvars.g_schema_tpch2x + """.lineitem l2,
 """ + gvars.g_schema_tpch2x + """.part p3, """ + gvars.g_schema_tpch2x + """.partsupp ps3
where p1.p_type like '%BRASS' and p1.p_size = 15
and p1.p_partkey = ps1.ps_partkey and ps1.ps_partkey = l1.l_partkey
and p2.p_partkey = ps2.ps_partkey and ps2.ps_partkey = l2.l_partkey
and p3.p_partkey = ps3.ps_partkey
and p1.p_partkey = p2.p_partkey and p2.p_partkey = p3.p_partkey;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
select count(*) from """ + gvars.g_schema_tpch2x + """.part p1, """ + gvars.g_schema_tpch2x + """.partsupp ps1, """ + gvars.g_schema_tpch2x + """.lineitem l1,
 """ + gvars.g_schema_tpch2x + """.part p2, """ + gvars.g_schema_tpch2x + """.partsupp ps2, """ + gvars.g_schema_tpch2x + """.lineitem l2,
 """ + gvars.g_schema_tpch2x + """.part p3, """ + gvars.g_schema_tpch2x + """.partsupp ps3
where p1.p_type like '%BRASS' and p1.p_size = 15
and p1.p_partkey = ps1.ps_partkey and ps1.ps_partkey = l1.l_partkey
and p2.p_partkey = ps2.ps_partkey and ps2.ps_partkey = l2.l_partkey
and p3.p_partkey = ps3.ps_partkey
and p1.p_partkey = p2.p_partkey and p2.p_partkey = p3.p_partkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A05exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A05exp P2
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A05exp""", 'P3')
    
    ##expectstat $test_dir/A05exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test006(desc='TPCD fully connected 8-way join'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """showshape
select count(*) from """ + gvars.g_schema_tpch2x + """.part p1, """ + gvars.g_schema_tpch2x + """.partsupp ps1, """ + gvars.g_schema_tpch2x + """.lineitem l1,
 """ + gvars.g_schema_tpch2x + """.part p2, """ + gvars.g_schema_tpch2x + """.partsupp ps2, """ + gvars.g_schema_tpch2x + """.lineitem l2,
 """ + gvars.g_schema_tpch2x + """.part p3, """ + gvars.g_schema_tpch2x + """.partsupp ps3
where p1.p_type like '%BRASS' and p1.p_size = 15
and ps1.ps_availqty < 2 and l1.l_quantity<2
and l1.l_extendedprice > 104500
and p1.p_partkey = ps1.ps_partkey and ps1.ps_partkey = l1.l_partkey
and p2.p_partkey = ps2.ps_partkey and ps2.ps_partkey = l2.l_partkey
and p3.p_partkey = ps3.ps_partkey
and p1.p_partkey = p2.p_partkey and p2.p_partkey = p3.p_partkey;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
select count(*) from """ + gvars.g_schema_tpch2x + """.part p1, """ + gvars.g_schema_tpch2x + """.partsupp ps1, """ + gvars.g_schema_tpch2x + """.lineitem l1,
 """ + gvars.g_schema_tpch2x + """.part p2, """ + gvars.g_schema_tpch2x + """.partsupp ps2, """ + gvars.g_schema_tpch2x + """.lineitem l2,
 """ + gvars.g_schema_tpch2x + """.part p3, """ + gvars.g_schema_tpch2x + """.partsupp ps3
where p1.p_type like '%BRASS' and p1.p_size = 15
and ps1.ps_availqty < 2 and l1.l_quantity<2
and l1.l_extendedprice > 104500
and p1.p_partkey = ps1.ps_partkey and ps1.ps_partkey = l1.l_partkey
and p2.p_partkey = ps2.ps_partkey and ps2.ps_partkey = l2.l_partkey
and p3.p_partkey = ps3.ps_partkey
and p1.p_partkey = p2.p_partkey and p2.p_partkey = p3.p_partkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A06exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A06exp P2
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A06exp""", 'P3')
    
    ##expectstat $test_dir/A06exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test007(desc='TPCD 12-way join'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """showshape
select count(*) from """ + gvars.g_schema_tpch2x + """.part p1, """ + gvars.g_schema_tpch2x + """.partsupp ps1, """ + gvars.g_schema_tpch2x + """.lineitem l1,
 """ + gvars.g_schema_tpch2x + """.part p2, """ + gvars.g_schema_tpch2x + """.partsupp ps2, """ + gvars.g_schema_tpch2x + """.lineitem l2,
 """ + gvars.g_schema_tpch2x + """.part p3, """ + gvars.g_schema_tpch2x + """.partsupp ps3, """ + gvars.g_schema_tpch2x + """.lineitem l3,
 """ + gvars.g_schema_tpch2x + """.part p4, """ + gvars.g_schema_tpch2x + """.partsupp ps4, """ + gvars.g_schema_tpch2x + """.lineitem l4
where p1.p_type like '%BRASS' and p1.p_size = 15
and p1.p_partkey = ps1.ps_partkey and ps1.ps_partkey = l1.l_partkey
and p2.p_partkey = ps2.ps_partkey and ps2.ps_partkey = l2.l_partkey
and p3.p_partkey = ps3.ps_partkey and ps3.ps_partkey = l3.l_partkey
and p4.p_partkey = ps4.ps_partkey and ps4.ps_partkey = l4.l_partkey
and p1.p_partkey = p2.p_partkey and p2.p_partkey = p3.p_partkey
and p3.p_partkey = p4.p_partkey;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
select count(*) from """ + gvars.g_schema_tpch2x + """.part p1, """ + gvars.g_schema_tpch2x + """.partsupp ps1, """ + gvars.g_schema_tpch2x + """.lineitem l1,
 """ + gvars.g_schema_tpch2x + """.part p2, """ + gvars.g_schema_tpch2x + """.partsupp ps2, """ + gvars.g_schema_tpch2x + """.lineitem l2,
 """ + gvars.g_schema_tpch2x + """.part p3, """ + gvars.g_schema_tpch2x + """.partsupp ps3, """ + gvars.g_schema_tpch2x + """.lineitem l3,
 """ + gvars.g_schema_tpch2x + """.part p4, """ + gvars.g_schema_tpch2x + """.partsupp ps4, """ + gvars.g_schema_tpch2x + """.lineitem l4
where p1.p_type like '%BRASS' and p1.p_size = 15
and p1.p_partkey = ps1.ps_partkey and ps1.ps_partkey = l1.l_partkey
and p2.p_partkey = ps2.ps_partkey and ps2.ps_partkey = l2.l_partkey
and p3.p_partkey = ps3.ps_partkey and ps3.ps_partkey = l3.l_partkey
and p4.p_partkey = ps4.ps_partkey and ps4.ps_partkey = l4.l_partkey
and p1.p_partkey = p2.p_partkey and p2.p_partkey = p3.p_partkey
and p3.p_partkey = p4.p_partkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A07exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A07exp P2
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    ##expectfile $test_dir/A07exp P3
    #execute xx;
    
    ##expectstat $test_dir/A07exp P4
    # NCI display statistics;
    
    _testmgr.testcase_end(desc)

def test008(desc='TPCD 12-way join with extra predicates'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """showshape
select count(*) from """ + gvars.g_schema_tpch2x + """.part p1, """ + gvars.g_schema_tpch2x + """.partsupp ps1, """ + gvars.g_schema_tpch2x + """.lineitem l1,
 """ + gvars.g_schema_tpch2x + """.part p2, """ + gvars.g_schema_tpch2x + """.partsupp ps2, """ + gvars.g_schema_tpch2x + """.lineitem l2,
 """ + gvars.g_schema_tpch2x + """.part p3, """ + gvars.g_schema_tpch2x + """.partsupp ps3, """ + gvars.g_schema_tpch2x + """.lineitem l3,
 """ + gvars.g_schema_tpch2x + """.part p4, """ + gvars.g_schema_tpch2x + """.partsupp ps4, """ + gvars.g_schema_tpch2x + """.lineitem l4
where p1.p_type like '%BRASS' and p1.p_size = 15
and ps1.ps_availqty < 2 and l1.l_quantity<2
and l1.l_extendedprice > 104500
and p1.p_partkey = ps1.ps_partkey and ps1.ps_partkey = l1.l_partkey
and p2.p_partkey = ps2.ps_partkey and ps2.ps_partkey = l2.l_partkey
and p3.p_partkey = ps3.ps_partkey and ps3.ps_partkey = l3.l_partkey
and p4.p_partkey = ps4.ps_partkey and ps4.ps_partkey = l4.l_partkey
and p1.p_partkey = p2.p_partkey and p2.p_partkey = p3.p_partkey
and p3.p_partkey = p4.p_partkey;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
select count(*) from """ + gvars.g_schema_tpch2x + """.part p1, """ + gvars.g_schema_tpch2x + """.partsupp ps1, """ + gvars.g_schema_tpch2x + """.lineitem l1,
 """ + gvars.g_schema_tpch2x + """.part p2, """ + gvars.g_schema_tpch2x + """.partsupp ps2, """ + gvars.g_schema_tpch2x + """.lineitem l2,
 """ + gvars.g_schema_tpch2x + """.part p3, """ + gvars.g_schema_tpch2x + """.partsupp ps3, """ + gvars.g_schema_tpch2x + """.lineitem l3,
 """ + gvars.g_schema_tpch2x + """.part p4, """ + gvars.g_schema_tpch2x + """.partsupp ps4, """ + gvars.g_schema_tpch2x + """.lineitem l4
where p1.p_type like '%BRASS' and p1.p_size = 15
and ps1.ps_availqty < 2 and l1.l_quantity<2
and l1.l_extendedprice > 104500
and p1.p_partkey = ps1.ps_partkey and ps1.ps_partkey = l1.l_partkey
and p2.p_partkey = ps2.ps_partkey and ps2.ps_partkey = l2.l_partkey
and p3.p_partkey = ps3.ps_partkey and ps3.ps_partkey = l3.l_partkey
and p4.p_partkey = ps4.ps_partkey and ps4.ps_partkey = l4.l_partkey
and p1.p_partkey = p2.p_partkey and p2.p_partkey = p3.p_partkey
and p3.p_partkey = p4.p_partkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A08exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    #Should't not give String over flow error 8402
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A08exp""", 'P3')
    
    ##expectstat $test_dir/A08exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test009(desc='TPCD 16-way join'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """showshape
select count(*) from """ + gvars.g_schema_tpch2x + """.part p1, """ + gvars.g_schema_tpch2x + """.partsupp ps1, """ + gvars.g_schema_tpch2x + """.lineitem l1,
 """ + gvars.g_schema_tpch2x + """.part p2, """ + gvars.g_schema_tpch2x + """.partsupp ps2, """ + gvars.g_schema_tpch2x + """.lineitem l2,
 """ + gvars.g_schema_tpch2x + """.part p3, """ + gvars.g_schema_tpch2x + """.partsupp ps3, """ + gvars.g_schema_tpch2x + """.lineitem l3,
 """ + gvars.g_schema_tpch2x + """.part p4, """ + gvars.g_schema_tpch2x + """.partsupp ps4, """ + gvars.g_schema_tpch2x + """.lineitem l4,
 """ + gvars.g_schema_tpch2x + """.part p5, """ + gvars.g_schema_tpch2x + """.partsupp ps5, """ + gvars.g_schema_tpch2x + """.lineitem l5,
 """ + gvars.g_schema_tpch2x + """.part p6
where p1.p_type like '%BRASS' and p1.p_size = 15
and p1.p_partkey = ps1.ps_partkey and ps1.ps_partkey = l1.l_partkey
and p2.p_partkey = ps2.ps_partkey and ps2.ps_partkey = l2.l_partkey
and p3.p_partkey = ps3.ps_partkey and ps3.ps_partkey = l3.l_partkey
and p4.p_partkey = ps4.ps_partkey and ps4.ps_partkey = l4.l_partkey
and p5.p_partkey = ps5.ps_partkey and ps5.ps_partkey = l5.l_partkey
and p1.p_partkey = p2.p_partkey and p2.p_partkey = p3.p_partkey
and p3.p_partkey = p4.p_partkey and p4.p_partkey = p5.p_partkey
and p5.p_partkey = p6.p_partkey;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
select count(*) from """ + gvars.g_schema_tpch2x + """.part p1, """ + gvars.g_schema_tpch2x + """.partsupp ps1, """ + gvars.g_schema_tpch2x + """.lineitem l1,
 """ + gvars.g_schema_tpch2x + """.part p2, """ + gvars.g_schema_tpch2x + """.partsupp ps2, """ + gvars.g_schema_tpch2x + """.lineitem l2,
 """ + gvars.g_schema_tpch2x + """.part p3, """ + gvars.g_schema_tpch2x + """.partsupp ps3, """ + gvars.g_schema_tpch2x + """.lineitem l3,
 """ + gvars.g_schema_tpch2x + """.part p4, """ + gvars.g_schema_tpch2x + """.partsupp ps4, """ + gvars.g_schema_tpch2x + """.lineitem l4,
 """ + gvars.g_schema_tpch2x + """.part p5, """ + gvars.g_schema_tpch2x + """.partsupp ps5, """ + gvars.g_schema_tpch2x + """.lineitem l5,
 """ + gvars.g_schema_tpch2x + """.part p6
where p1.p_type like '%BRASS' and p1.p_size = 15
and p1.p_partkey = ps1.ps_partkey and ps1.ps_partkey = l1.l_partkey
and p2.p_partkey = ps2.ps_partkey and ps2.ps_partkey = l2.l_partkey
and p3.p_partkey = ps3.ps_partkey and ps3.ps_partkey = l3.l_partkey
and p4.p_partkey = ps4.ps_partkey and ps4.ps_partkey = l4.l_partkey
and p5.p_partkey = ps5.ps_partkey and ps5.ps_partkey = l5.l_partkey
and p1.p_partkey = p2.p_partkey and p2.p_partkey = p3.p_partkey
and p3.p_partkey = p4.p_partkey and p4.p_partkey = p5.p_partkey
and p5.p_partkey = p6.p_partkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A09exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A09exp P2
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    ##expectfile $test_dir/A09exp P3
    #execute xx;
    
    ##expectstat $test_dir/A09exp P4
    # NCI display statistics;
    
    _testmgr.testcase_end(desc)

def test010(desc='TPCD 16-way join with extra predicates'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """showshape
select count(*) from """ + gvars.g_schema_tpch2x + """.part p1, """ + gvars.g_schema_tpch2x + """.partsupp ps1, """ + gvars.g_schema_tpch2x + """.lineitem l1,
 """ + gvars.g_schema_tpch2x + """.part p2, """ + gvars.g_schema_tpch2x + """.partsupp ps2, """ + gvars.g_schema_tpch2x + """.lineitem l2,
 """ + gvars.g_schema_tpch2x + """.part p3, """ + gvars.g_schema_tpch2x + """.partsupp ps3, """ + gvars.g_schema_tpch2x + """.lineitem l3,
 """ + gvars.g_schema_tpch2x + """.part p4, """ + gvars.g_schema_tpch2x + """.partsupp ps4, """ + gvars.g_schema_tpch2x + """.lineitem l4,
 """ + gvars.g_schema_tpch2x + """.part p5, """ + gvars.g_schema_tpch2x + """.partsupp ps5, """ + gvars.g_schema_tpch2x + """.lineitem l5,
 """ + gvars.g_schema_tpch2x + """.part p6
where p1.p_type like '%BRASS' and p1.p_size = 15
and ps1.ps_availqty < 2 and l1.l_quantity<2
and l1.l_extendedprice > 104500
and p1.p_partkey = ps1.ps_partkey and ps1.ps_partkey = l1.l_partkey
and p2.p_partkey = ps2.ps_partkey and ps2.ps_partkey = l2.l_partkey
and p3.p_partkey = ps3.ps_partkey and ps3.ps_partkey = l3.l_partkey
and p4.p_partkey = ps4.ps_partkey and ps4.ps_partkey = l4.l_partkey
and p5.p_partkey = ps5.ps_partkey and ps5.ps_partkey = l5.l_partkey
and p1.p_partkey = p2.p_partkey and p2.p_partkey = p3.p_partkey
and p3.p_partkey = p4.p_partkey and p4.p_partkey = p5.p_partkey
and p5.p_partkey = p6.p_partkey;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
select count(*) from """ + gvars.g_schema_tpch2x + """.part p1, """ + gvars.g_schema_tpch2x + """.partsupp ps1, """ + gvars.g_schema_tpch2x + """.lineitem l1,
 """ + gvars.g_schema_tpch2x + """.part p2, """ + gvars.g_schema_tpch2x + """.partsupp ps2, """ + gvars.g_schema_tpch2x + """.lineitem l2,
 """ + gvars.g_schema_tpch2x + """.part p3, """ + gvars.g_schema_tpch2x + """.partsupp ps3, """ + gvars.g_schema_tpch2x + """.lineitem l3,
 """ + gvars.g_schema_tpch2x + """.part p4, """ + gvars.g_schema_tpch2x + """.partsupp ps4, """ + gvars.g_schema_tpch2x + """.lineitem l4,
 """ + gvars.g_schema_tpch2x + """.part p5, """ + gvars.g_schema_tpch2x + """.partsupp ps5, """ + gvars.g_schema_tpch2x + """.lineitem l5,
 """ + gvars.g_schema_tpch2x + """.part p6
where p1.p_type like '%BRASS' and p1.p_size = 15
and ps1.ps_availqty < 2 and l1.l_quantity<2
and l1.l_extendedprice > 104500
and p1.p_partkey = ps1.ps_partkey and ps1.ps_partkey = l1.l_partkey
and p2.p_partkey = ps2.ps_partkey and ps2.ps_partkey = l2.l_partkey
and p3.p_partkey = ps3.ps_partkey and ps3.ps_partkey = l3.l_partkey
and p4.p_partkey = ps4.ps_partkey and ps4.ps_partkey = l4.l_partkey
and p5.p_partkey = ps5.ps_partkey and ps5.ps_partkey = l5.l_partkey
and p1.p_partkey = p2.p_partkey and p2.p_partkey = p3.p_partkey
and p3.p_partkey = p4.p_partkey and p4.p_partkey = p5.p_partkey
and p5.p_partkey = p6.p_partkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A10exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    #Should't not give String over flow error 8402
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A10exp""", 'P3')
    
    ##expectstat $test_dir/A10exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test011(desc='TPCD prime table'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """showshape
select count(*) from """ + gvars.g_schema_tpch2x + """.lineitem l1, """ + gvars.g_schema_tpch2x + """.lineitem l2, """ + gvars.g_schema_tpch2x + """.lineitem l3, """ + gvars.g_schema_tpch2x + """.orders o1,
 """ + gvars.g_schema_tpch2x + """.orders o2, """ + gvars.g_schema_tpch2x + """.customer, """ + gvars.g_schema_tpch2x + """.nation 
where l1.l_orderkey = l2.l_orderkey and l2.l_orderkey = l3.l_orderkey
and l1.l_orderkey = o1.o_orderkey and o1.o_orderkey = o2.o_orderkey
and c_custkey = o1.o_custkey and c_nationkey = n_nationkey
and n_name = 'CANADA';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
select count(*) from """ + gvars.g_schema_tpch2x + """.lineitem l1, """ + gvars.g_schema_tpch2x + """.lineitem l2, """ + gvars.g_schema_tpch2x + """.lineitem l3, """ + gvars.g_schema_tpch2x + """.orders o1,
 """ + gvars.g_schema_tpch2x + """.orders o2, """ + gvars.g_schema_tpch2x + """.customer, """ + gvars.g_schema_tpch2x + """.nation 
where l1.l_orderkey = l2.l_orderkey and l2.l_orderkey = l3.l_orderkey
and l1.l_orderkey = o1.o_orderkey and o1.o_orderkey = o2.o_orderkey
and c_custkey = o1.o_custkey and c_nationkey = n_nationkey
and n_name = 'CANADA';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A11exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A11exp P2
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A11exp""", 'P3')
    
    ##expectstat $test_dir/A11exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test012(desc='TPCD prime table with extra paths'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """showshape
select count(*) from """ + gvars.g_schema_tpch2x + """.lineitem l1, """ + gvars.g_schema_tpch2x + """.lineitem l2, """ + gvars.g_schema_tpch2x + """.lineitem l3, """ + gvars.g_schema_tpch2x + """.orders o1,
 """ + gvars.g_schema_tpch2x + """.orders o2, """ + gvars.g_schema_tpch2x + """.customer, """ + gvars.g_schema_tpch2x + """.nation 
where l1.l_orderkey = l2.l_orderkey and l2.l_orderkey = l3.l_orderkey
and l1.l_orderkey = o1.o_orderkey and o1.o_orderkey = o2.o_orderkey
and c_custkey = o1.o_custkey and c_nationkey = n_nationkey
and n_name = 'CANADA';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
select count(*) from """ + gvars.g_schema_tpch2x + """.lineitem l1, """ + gvars.g_schema_tpch2x + """.lineitem l2, """ + gvars.g_schema_tpch2x + """.lineitem l3, """ + gvars.g_schema_tpch2x + """.orders o1,
 """ + gvars.g_schema_tpch2x + """.orders o2, """ + gvars.g_schema_tpch2x + """.customer, """ + gvars.g_schema_tpch2x + """.nation 
where l1.l_orderkey = l2.l_orderkey and l2.l_orderkey = l3.l_orderkey
and l1.l_orderkey = o1.o_orderkey and o1.o_orderkey = o2.o_orderkey
and c_custkey = o1.o_custkey and c_nationkey = n_nationkey
and n_name = 'CANADA';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A12exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A12exp P2
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A12exp""", 'P3')
    
    ##expectstat $test_dir/A12exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test013(desc='TPCD query 7'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """showshape
select supp_nation, cust_nation, yr, sum(volume) as revenue
from
( select n1.n_name as supp_nation, n2.n_name as cust_nation,
extract(year from l_shipdate) as yr,
CAST(l_extendedprice*(1-l_discount) AS NUMERIC(18,2)) as volume
from """ + gvars.g_schema_tpch2x + """.supplier,""" + gvars.g_schema_tpch2x + """.lineitem,""" + gvars.g_schema_tpch2x + """.orders,""" + gvars.g_schema_tpch2x + """.customer, """ + gvars.g_schema_tpch2x + """.nation n1, """ + gvars.g_schema_tpch2x + """.nation n2
where s_suppkey = l_suppkey
and o_orderkey = l_orderkey
and c_custkey = o_custkey
and s_nationkey = n1.n_nationkey
and c_nationkey = n2.n_nationkey
and (( n1.n_name  = 'FRANCE' and n2.n_name = 'GERMANY') or
( n1.n_name = 'GERMANY' and n2.n_name = 'FRANCE'))
and l_shipdate between  DATE '1995-01-01' and DATE '1996-12-31'
) as shipping
group by supp_nation, cust_nation, yr
order by supp_nation, cust_nation, yr;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
select supp_nation, cust_nation, yr, sum(volume) as revenue
from
( select n1.n_name as supp_nation, n2.n_name as cust_nation,
extract(year from l_shipdate) as yr,
CAST(l_extendedprice*(1-l_discount) AS NUMERIC(18,2)) as volume
from """ + gvars.g_schema_tpch2x + """.supplier,""" + gvars.g_schema_tpch2x + """.lineitem,""" + gvars.g_schema_tpch2x + """.orders,""" + gvars.g_schema_tpch2x + """.customer, """ + gvars.g_schema_tpch2x + """.nation n1, """ + gvars.g_schema_tpch2x + """.nation n2
where s_suppkey = l_suppkey
and o_orderkey = l_orderkey
and c_custkey = o_custkey
and s_nationkey = n1.n_nationkey
and c_nationkey = n2.n_nationkey
and (( n1.n_name  = 'FRANCE' and n2.n_name = 'GERMANY') or
( n1.n_name = 'GERMANY' and n2.n_name = 'FRANCE'))
and l_shipdate between  DATE '1995-01-01' and DATE '1996-12-31'
) as shipping
group by supp_nation, cust_nation, yr
order by supp_nation, cust_nation, yr;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A13exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A13exp P2
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    ##expectstat $test_dir/A13exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test014(desc='Derivative from TPCD q09'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """showshape
select nation, o_year, sum(amount) as sum_profit
from
( select n_name as nation, extract(year from o_orderdate) as o_year,
l_extendedprice * (1-l_discount) - ps_supplycost *l_quantity as amount
from """ + gvars.g_schema_tpch2x + """.part, """ + gvars.g_schema_tpch2x + """.supplier, """ + gvars.g_schema_tpch2x + """.lineitem, """ + gvars.g_schema_tpch2x + """.partsupp, """ + gvars.g_schema_tpch2x + """.orders, """ + gvars.g_schema_tpch2x + """.nation 
where s_suppkey = l_suppkey	and ps_suppkey = l_suppkey
and ps_partkey = l_partkey	and p_partkey = l_partkey
and o_orderkey = l_orderkey
and s_nationkey = n_nationkey
and p_name like '%green%'
and n_name = 'CANADA'
and p_brand <> 'Brand#45'
and p_type not  like 'MEDIUM POLISHED%'
and p_size in (49, 14, 23, 45, 19, 3, 36, 9)
and s_comment like '%Customer%Complaints%'
and o_orderdate < date '1995-03-15'
and l_shipdate > date '1995-03-15'
) as profit
group by nation, o_year
order by nation, o_year desc;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
select nation, o_year, sum(amount) as sum_profit
from
( select n_name as nation, extract(year from o_orderdate) as o_year,
l_extendedprice * (1-l_discount) - ps_supplycost *l_quantity as amount
from """ + gvars.g_schema_tpch2x + """.part, """ + gvars.g_schema_tpch2x + """.supplier, """ + gvars.g_schema_tpch2x + """.lineitem, """ + gvars.g_schema_tpch2x + """.partsupp, """ + gvars.g_schema_tpch2x + """.orders, """ + gvars.g_schema_tpch2x + """.nation 
where s_suppkey = l_suppkey	and ps_suppkey = l_suppkey
and ps_partkey = l_partkey	and p_partkey = l_partkey
and o_orderkey = l_orderkey
and s_nationkey = n_nationkey
and p_name like '%green%'
and n_name = 'CANADA'
and p_brand <> 'Brand#45'
and p_type not  like 'MEDIUM POLISHED%'
and p_size in (49, 14, 23, 45, 19, 3, 36, 9)
and s_comment like '%Customer%Complaints%'
and o_orderdate < date '1995-03-15'
and l_shipdate > date '1995-03-15'
) as profit
group by nation, o_year
order by nation, o_year desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A14exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A14exp P2
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    ##expectstat $test_dir/A14exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test015(desc='DUTP query 30'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """showshape
select [first 20] *
from """ + gvars.g_schema_tpch2x + """.region, """ + gvars.g_schema_tpch2x + """.nation, """ + gvars.g_schema_tpch2x + """.supplier, """ + gvars.g_schema_tpch2x + """.customer, """ + gvars.g_schema_tpch2x + """.orders, """ + gvars.g_schema_tpch2x + """.lineitem, """ + gvars.g_schema_tpch2x + """.part, """ + gvars.g_schema_tpch2x + """.partsupp 
where r_regionkey = n_regionkey
and n_nationkey = s_nationkey and n_nationkey = c_nationkey
and c_custkey=o_custkey
and o_orderkey=l_orderkey
and p_partkey=ps_partkey and ps_partkey = l_partkey
and ps_suppkey=l_suppkey
and r_name='ASIA'
and p_name like '%plum%'
and p_brand <> 'Brand#45'
and p_type not  like 'MEDIUM POLISHED%'
and c_mktsegment = 'AUTOMOBILE'
and substring(c_phone from 1 for 2) in ('13', '35', '31', '23', '29', '30', '18', '17')
and l_shipinstruct = 'NONE'
and o_orderdate between date '1995-01-01' and date '1996-12-31'
and o_orderpriority = '1-URGENT'
and ps_availqty < 5000;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
select [first 20] *
from """ + gvars.g_schema_tpch2x + """.region, """ + gvars.g_schema_tpch2x + """.nation, """ + gvars.g_schema_tpch2x + """.supplier, """ + gvars.g_schema_tpch2x + """.customer, """ + gvars.g_schema_tpch2x + """.orders, """ + gvars.g_schema_tpch2x + """.lineitem, """ + gvars.g_schema_tpch2x + """.part, """ + gvars.g_schema_tpch2x + """.partsupp 
where r_regionkey = n_regionkey
and n_nationkey = s_nationkey and n_nationkey = c_nationkey
and c_custkey=o_custkey
and o_orderkey=l_orderkey
and p_partkey=ps_partkey and ps_partkey = l_partkey
and ps_suppkey=l_suppkey
and r_name='ASIA'
and p_name like '%plum%'
and p_brand <> 'Brand#45'
and p_type not  like 'MEDIUM POLISHED%'
and c_mktsegment = 'AUTOMOBILE'
and substring(c_phone from 1 for 2) in ('13', '35', '31', '23', '29', '30', '18', '17')
and l_shipinstruct = 'NONE'
and o_orderdate between date '1995-01-01' and date '1996-12-31'
and o_orderpriority = '1-URGENT'
and ps_availqty < 5000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A15exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A15exp P2
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    # NCI set envvar NO_SCREEN_OUTPUT;
    # NCI #expectfile $test_dir/A15exp P3
    # NCI execute xx;
    # NCI reset envvar NO_SCREEN_OUTPUT;
    
    ##expectstat $test_dir/A15exp P4
    # NCI display statistics;
    
    _testmgr.testcase_end(desc)

def test016(desc='DUTP 31'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """showshape
SELECT 	sum(l_extendedprice*(1-l_discount))
FROM  """ + gvars.g_schema_tpch2x + """.region r1, """ + gvars.g_schema_tpch2x + """.region r2, """ + gvars.g_schema_tpch2x + """.nation n1, """ + gvars.g_schema_tpch2x + """.nation n2,
 """ + gvars.g_schema_tpch2x + """.supplier s1 , """ + gvars.g_schema_tpch2x + """.customer c1, """ + gvars.g_schema_tpch2x + """.part, """ + gvars.g_schema_tpch2x + """.partsupp, """ + gvars.g_schema_tpch2x + """.orders, """ + gvars.g_schema_tpch2x + """.lineitem 
WHERE 	r1.r_name = 'ASIA'
AND		n1.n_regionkey = r1.r_regionkey
AND		s1.s_nationkey = n1.n_nationkey
AND		r2.r_name = 'EUROPE'
AND		n2.n_regionkey = r2.r_regionkey
AND		c1.c_nationkey = n2.n_nationkey
AND		o_custkey = c1.c_custkey
AND		l_orderkey = o_orderkey
AND		ps_partkey = l_partkey AND	 p_partkey = ps_partkey
AND		ps_suppkey = l_suppkey AND	 s1.s_suppkey = ps_suppkey
AND		p_type LIKE '%BRASS'
AND 		l_shipdate between date'1996-01-01' and date'1996-12-31';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
SELECT 	sum(l_extendedprice*(1-l_discount))
FROM  """ + gvars.g_schema_tpch2x + """.region r1, """ + gvars.g_schema_tpch2x + """.region r2, """ + gvars.g_schema_tpch2x + """.nation n1, """ + gvars.g_schema_tpch2x + """.nation n2,
 """ + gvars.g_schema_tpch2x + """.supplier s1 , """ + gvars.g_schema_tpch2x + """.customer c1, """ + gvars.g_schema_tpch2x + """.part, """ + gvars.g_schema_tpch2x + """.partsupp, """ + gvars.g_schema_tpch2x + """.orders, """ + gvars.g_schema_tpch2x + """.lineitem 
WHERE 	r1.r_name = 'ASIA'
AND		n1.n_regionkey = r1.r_regionkey
AND		s1.s_nationkey = n1.n_nationkey
AND		r2.r_name = 'EUROPE'
AND		n2.n_regionkey = r2.r_regionkey
AND		c1.c_nationkey = n2.n_nationkey
AND		o_custkey = c1.c_custkey
AND		l_orderkey = o_orderkey
AND		ps_partkey = l_partkey AND	 p_partkey = ps_partkey
AND		ps_suppkey = l_suppkey AND	 s1.s_suppkey = ps_suppkey
AND		p_type LIKE '%BRASS'
AND 		l_shipdate between date'1996-01-01' and date'1996-12-31';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A16exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A16exp P2
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A16exp""", 'P3')
    
    ##expectstat $test_dir/A16exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test017(desc='Derivative from TPCD q09'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """showshape
SELECT 	sum(l_extendedprice * (1-l_discount))
FROM  """ + gvars.g_schema_tpch2x + """.region r1, """ + gvars.g_schema_tpch2x + """.region r2, """ + gvars.g_schema_tpch2x + """.nation n1, """ + gvars.g_schema_tpch2x + """.nation n2, """ + gvars.g_schema_tpch2x + """.part,
 """ + gvars.g_schema_tpch2x + """.supplier s1 , """ + gvars.g_schema_tpch2x + """.customer c1, """ + gvars.g_schema_tpch2x + """.partsupp, """ + gvars.g_schema_tpch2x + """.orders, """ + gvars.g_schema_tpch2x + """.lineitem 
WHERE 	r1.r_name = 'ASIA'
AND		n1.n_regionkey = r1.r_regionkey
AND		s1.s_nationkey = n1.n_nationkey
AND		r2.r_name = 'EUROPE'
AND		n2.n_regionkey = r2.r_regionkey
AND		c1.c_nationkey = n2.n_nationkey
AND		o_custkey = c1.c_custkey
AND		l_orderkey = o_orderkey
AND		ps_partkey = l_partkey AND	 p_partkey = ps_partkey
AND		ps_suppkey = l_suppkey AND	 s1.s_suppkey = ps_suppkey
AND		p_type LIKE '%BRASS'
AND 		l_shipdate between date'1996-01-01' and date'1996-12-31'
AND       	c1.c_acctbal >   ( SELECT avg(c3.c_acctbal)
FROM     """ + gvars.g_schema_tpch2x + """.region r3, """ + gvars.g_schema_tpch2x + """.nation n3, """ + gvars.g_schema_tpch2x + """.customer c3
WHERE	r3.r_name = 'EUROPE'
AND	n3.n_regionkey = r3.r_regionkey
AND	c3.c_nationkey = n3.n_nationkey
AND	c3.c_acctbal > 0);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
SELECT 	sum(l_extendedprice * (1-l_discount))
FROM  """ + gvars.g_schema_tpch2x + """.region r1, """ + gvars.g_schema_tpch2x + """.region r2, """ + gvars.g_schema_tpch2x + """.nation n1, """ + gvars.g_schema_tpch2x + """.nation n2, """ + gvars.g_schema_tpch2x + """.part,
 """ + gvars.g_schema_tpch2x + """.supplier s1 , """ + gvars.g_schema_tpch2x + """.customer c1, """ + gvars.g_schema_tpch2x + """.partsupp, """ + gvars.g_schema_tpch2x + """.orders, """ + gvars.g_schema_tpch2x + """.lineitem 
WHERE 	r1.r_name = 'ASIA'
AND		n1.n_regionkey = r1.r_regionkey
AND		s1.s_nationkey = n1.n_nationkey
AND		r2.r_name = 'EUROPE'
AND		n2.n_regionkey = r2.r_regionkey
AND		c1.c_nationkey = n2.n_nationkey
AND		o_custkey = c1.c_custkey
AND		l_orderkey = o_orderkey
AND		ps_partkey = l_partkey AND	 p_partkey = ps_partkey
AND		ps_suppkey = l_suppkey AND	 s1.s_suppkey = ps_suppkey
AND		p_type LIKE '%BRASS'
AND 		l_shipdate between date'1996-01-01' and date'1996-12-31'
AND       	c1.c_acctbal >   ( SELECT avg(c3.c_acctbal)
FROM     """ + gvars.g_schema_tpch2x + """.region r3, """ + gvars.g_schema_tpch2x + """.nation n3, """ + gvars.g_schema_tpch2x + """.customer c3
WHERE	r3.r_name = 'EUROPE'
AND	n3.n_regionkey = r3.r_regionkey
AND	c3.c_nationkey = n3.n_nationkey
AND	c3.c_acctbal > 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A17exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A17exp P2
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    ##expectfile $test_dir/A17exp P3
    #execute xx;
    
    ##expectstat $test_dir/A17exp P4
    # NCI display statistics;
    
    _testmgr.testcase_end(desc)

def test018(desc='DUTP 33'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """showshape
SELECT 	sum(l_extendedprice * (1-l_discount))
FROM  """ + gvars.g_schema_tpch2x + """.region r1, """ + gvars.g_schema_tpch2x + """.region r2, """ + gvars.g_schema_tpch2x + """.nation n1, """ + gvars.g_schema_tpch2x + """.nation n2, """ + gvars.g_schema_tpch2x + """.part,
 """ + gvars.g_schema_tpch2x + """.supplier s1 , """ + gvars.g_schema_tpch2x + """.customer c1, """ + gvars.g_schema_tpch2x + """.partsupp, """ + gvars.g_schema_tpch2x + """.orders, """ + gvars.g_schema_tpch2x + """.lineitem 
WHERE 	r1.r_name = 'ASIA'
AND	n1.n_regionkey = r1.r_regionkey
AND	s1.s_nationkey = n1.n_nationkey
AND	r2.r_name = 'EUROPE'
AND	n2.n_regionkey = r2.r_regionkey
AND	c1.c_nationkey = n2.n_nationkey
AND	o_custkey = c1.c_custkey
AND	l_orderkey = o_orderkey
AND	ps_partkey = l_partkey AND	 p_partkey = ps_partkey
AND	ps_suppkey = l_suppkey AND s1.s_suppkey = ps_suppkey
AND	p_type LIKE '%BRASS'
AND 	l_shipdate between date'1996-01-01' and date'1996-12-31'
AND c1.c_acctbal>( SELECT avg(c3.c_acctbal)
FROM   """ + gvars.g_schema_tpch2x + """.region r3, """ + gvars.g_schema_tpch2x + """.nation n3, """ + gvars.g_schema_tpch2x + """.customer c3
WHERE	r3.r_name = 'EUROPE'
AND	n3.n_regionkey = r3.r_regionkey
AND	c3.c_nationkey = n3.n_nationkey
AND	c3.c_acctbal > 0)
AND s1.s_acctbal>( SELECT avg(s4.s_acctbal)
FROM   """ + gvars.g_schema_tpch2x + """.region r4, """ + gvars.g_schema_tpch2x + """.nation n4, """ + gvars.g_schema_tpch2x + """.supplier s4
WHERE	r4.r_name = 'ASIA'
AND	n4.n_regionkey = r4.r_regionkey
AND	s4.s_nationkey = n4.n_nationkey
AND	s4.s_acctbal > 0);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
SELECT 	sum(l_extendedprice * (1-l_discount))
FROM  """ + gvars.g_schema_tpch2x + """.region r1, """ + gvars.g_schema_tpch2x + """.region r2, """ + gvars.g_schema_tpch2x + """.nation n1, """ + gvars.g_schema_tpch2x + """.nation n2, """ + gvars.g_schema_tpch2x + """.part,
 """ + gvars.g_schema_tpch2x + """.supplier s1 , """ + gvars.g_schema_tpch2x + """.customer c1, """ + gvars.g_schema_tpch2x + """.partsupp, """ + gvars.g_schema_tpch2x + """.orders, """ + gvars.g_schema_tpch2x + """.lineitem 
WHERE 	r1.r_name = 'ASIA'
AND	n1.n_regionkey = r1.r_regionkey
AND	s1.s_nationkey = n1.n_nationkey
AND	r2.r_name = 'EUROPE'
AND	n2.n_regionkey = r2.r_regionkey
AND	c1.c_nationkey = n2.n_nationkey
AND	o_custkey = c1.c_custkey
AND	l_orderkey = o_orderkey
AND	ps_partkey = l_partkey AND	 p_partkey = ps_partkey
AND	ps_suppkey = l_suppkey AND s1.s_suppkey = ps_suppkey
AND	p_type LIKE '%BRASS'
AND 	l_shipdate between date'1996-01-01' and date'1996-12-31'
AND c1.c_acctbal>( SELECT avg(c3.c_acctbal)
FROM   """ + gvars.g_schema_tpch2x + """.region r3, """ + gvars.g_schema_tpch2x + """.nation n3, """ + gvars.g_schema_tpch2x + """.customer c3
WHERE	r3.r_name = 'EUROPE'
AND	n3.n_regionkey = r3.r_regionkey
AND	c3.c_nationkey = n3.n_nationkey
AND	c3.c_acctbal > 0)
AND s1.s_acctbal>( SELECT avg(s4.s_acctbal)
FROM   """ + gvars.g_schema_tpch2x + """.region r4, """ + gvars.g_schema_tpch2x + """.nation n4, """ + gvars.g_schema_tpch2x + """.supplier s4
WHERE	r4.r_name = 'ASIA'
AND	n4.n_regionkey = r4.r_regionkey
AND	s4.s_nationkey = n4.n_nationkey
AND	s4.s_acctbal > 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A18exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A18exp P2
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A18exp""", 'P3')
    
    ##expectstat $test_dir/A18exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

