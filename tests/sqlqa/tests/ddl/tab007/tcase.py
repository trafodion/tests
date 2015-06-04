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

import t7a008t1_ddl
import t7a009t1_ddl
import t7a004t2_ddl
import t7a007t1_ddl
import t7a008t5_ddl
import t7a005t1_ddl
import t7a009t5_ddl
import t7a002t2_ddl
import t7a005t2_ddl
import t7a001t1_ddl
import t7a008t6_ddl
import t7a007t4_ddl
import t7a009t3_ddl
import t7a008t2_ddl
import t7a003t3_ddl
import t7a002t4_ddl
import t7a009t4_ddl
import t7a009t2_ddl
import t7a002t3_ddl
import t7a006t2_ddl
import t7a008t3_ddl
import t7a001t3_ddl
import t7a005t3_ddl
import t7a008t4_ddl
import t7a002t1_ddl
import t7a006t1_ddl
import t7a004t1_ddl
import t7a003t1_ddl
import t7a003t2_ddl
import t7a009t6_ddl
import t7a001t2_ddl
from ...lib import hpdci
from ...lib import gvars
import defs

_testmgr = None
_testlist = []
_dci = None

#  TAB007 CREATE TABLE STORE BY TESTS
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""Create TABLE with no store by options"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    #A001.1 Create table with no primary key, no store by
    defs.exp_err = None
    t7a001t1_ddl._init(_testmgr)
    
    # R2.5 NCI #expectfile $test_dir/A001 a1s1
    stmt = """showddl t7a001t1;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = """showlabel t7a001t1,detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # R2.5 NCI #expect any *20*
    # R2.5 NCI #sh import $my_schema.t7a001t1 -I $datadir/b2pwl14.dat -C 20
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.t7a001t1
(select * from """ + gvars.g_schema_sqldpop + """.b2pwl14);"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    # R2.5 NCI #expectfile $test_dir/A001 a1s1b
    stmt = """select [last 0] sdec16_uniq, syskey
from t7a001t1;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #A001.2 Create table with PK, droppable, no store by clause
    defs.exp_err = None
    t7a001t2_ddl._init(_testmgr)
    
    # R2.5 NCI #expectfile $test_dir/A001 a1s2
    stmt = """showddl t7a001t2;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = """showlabel t7a001t2,detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # R2.5 NCI #expect any *20*
    # R2.5 NCI #sh import $my_schema.t7a001t2 -I $datadir/b2pwl16.dat -C 20
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.t7a001t2
(select * from """ + gvars.g_schema_sqldpop + """.b2pwl16);"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    # R2.5 NCI #expectfile $test_dir/A001 a1s2b
    # TRAF stmt = """select [last 0] real1_uniq, syskey,ubin16_n10 from t7a001t2;"""
    stmt = """select [last 0] real1_uniq, ubin16_n10 from t7a001t2;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #A001.3 Create partitioned table with PK not droppable, no store by clause
    defs.exp_err = None
    t7a001t3_ddl._init(_testmgr)
    
    # R2.5 NCI #expectfile $test_dir/A001 a1s3
    stmt = """showddl t7a001t3;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_any_substr(output, """STORE BY (SYSKEY ASC, TIME1_1000 ASC, INT1_YTOM_UNIQ ASC)""")
    elif hpdci.tgtTR():
        _dci.expect_any_substr(output, """PRIMARY KEY (SYSKEY ASC, TIME1_1000 ASC, INT1_YTOM_UNIQ ASC)""")
 
    stmt = """showlabel t7a001t3, detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #expect purge
    # R2.5 NCI #expect any *20*
    # R2.5 NCI #sh import $my_schema.t7a001t3 -I $datadir/b2pwl20.dat -C 20
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.t7a001t3
(select * from """ + gvars.g_schema_sqldpop + """.b2pwl20);"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    # R2.5 NCI #expectfile $test_dir/A001 a1s3b
    stmt = """select [last 0] real1_uniq, syskey,ubin16_n10 from t7a001t3;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    _testmgr.testcase_end(desc)

def test002(desc="""Create TABLE store by PK"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    #A002.1 Create TABLE with no PK, store by PK
    # R2.5 NCI #expectfile ${test_dir}/a002.exp sec1
    defs.exp_err = '3188'
    t7a002t1_ddl._init(_testmgr)
    
    #A002.2 Create TABLE using droppable PK, store by PK
    defs.exp_err = '3065'
    t7a002t2_ddl._init(_testmgr)
    
    #A002.3 Create table with desc primary key, store by PK
    defs.exp_err = None
    t7a002t3_ddl._init(_testmgr)
    
    # R2.5 NCI #expectfile $test_dir/A001 a2s3
    stmt = """showddl t7a002t3;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = """showlabel t7a002t3,detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # R2.5 NCI #expect any *20*
    # R2.5 NCI #sh import $my_schema.t7a002t3 -I $datadir/b2pwl16.dat -C 20
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.t7a002t3
(select * from """ + gvars.g_schema_sqldpop + """.b2pwl16);"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    # R2.5 NCI #expectfile $test_dir/A001 a2s3b
    stmt = """select [last 0] real1_uniq, sdec16_uniq
from t7a002t3;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #A002.4 Create table with asc primary key, store by PK
    defs.exp_err = None
    t7a002t4_ddl._init(_testmgr)
    
    # R2.5 NCI #expectfile $test_dir/A001 a2s4
    stmt = """showddl t7a002t4;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = """showlabel t7a002t4,detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # R2.5 NCI #expect any *20*
    # R2.5 NCI #sh import $my_schema.t7a002t4 -I $datadir/b2pwl20.dat -C 20
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.t7a002t4
(select * from """ + gvars.g_schema_sqldpop + """.b2pwl20);"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    # R2.5 NCI #expectfile $test_dir/A001 a2s4b
    stmt = """select [last 0] date0_100, time1_1000, int1_yTOm_uniq,
dt16_m_n10,int16_h_20
from t7a002t4;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    _testmgr.testcase_end(desc)

def test003(desc="""Create TABLE store by prefix of PK"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    #A003.1 Create TABLE with 4 column droppable PK, store by first three cols
    defs.exp_err = None
    t7a003t1_ddl._init(_testmgr)
    
    # R2.5 NCI #expectfile $test_dir/A001 a3s1
    stmt = """showddl t7a003t1;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = """showlabel t7a003t1,detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # R2.5 NCI #expect any *20*
    # R2.5 NCI #sh import $my_schema.t7a003t1 -I $datadir/b2pwl04.dat -C 20
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.t7a003t1
(select * from """ + gvars.g_schema_sqldpop + """.b2pwl04);"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    # R2.5 NCI #expectfile $test_dir/A001 a3s1b
    stmt = """select [last 0] sdec9_uniq ,sdec0_100,
sdec1_20, char16_n20
from t7a003t1;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #A003.2 Create TABLE with 4-column non-droppable PK store by first two columns
    defs.exp_err = None
    t7a003t2_ddl._init(_testmgr)
    
    # R2.5 NCI #expectfile $test_dir/A001 a3s2
    stmt = """showddl t7a003t2;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = """showlabel t7a003t2,detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # R2.5 NCI #expect any *20*
    # R2.5 NCI #sh import $my_schema.t7a003t2 -I $datadir/b2pwl26.dat -C 20
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.t7a003t2
(select * from """ + gvars.g_schema_sqldpop + """.b2pwl26);"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    # R2.5 NCI #expectfile $test_dir/A001 a3s2b
    stmt = """select [last 0] int1_yTOm_100,
sbin0_uniq, sdec8_4 from t7a003t2;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #A003.3 Create TABLE with 5-column non-droppable PK store by first column
    defs.exp_err = None
    t7a003t3_ddl._init(_testmgr)
    
    # R2.5 NCI #expectfile $test_dir/A001 a3s3
    stmt = """showddl t7a003t3;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = """showlabel t7a003t3,detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # R2.5 NCI #expect any *20*
    # R2.5 NCI #sh import $my_schema.t7a003t3 -I $datadir/b2pwl28.dat -C 20
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.t7a003t3
(select * from """ + gvars.g_schema_sqldpop + """.b2pwl28);"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    # R2.5 NCI #expectfile $test_dir/A001 a3s3b
    stmt = """select [last 0] time1_uniq, char16_n20 from t7a003t3;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    _testmgr.testcase_end(desc)

def test004(desc="""Create TABLE store by columns in (non-prefix) of PK"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    #A004.1 Create TABLE with 4-column droppable PK, store by PK cols 2 and 3
    defs.exp_err = None
    t7a004t1_ddl._init(_testmgr)
    
    # R2.5 NCI #expectfile $test_dir/A001 a4s1
    stmt = """showddl t7a004t1;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = """showlabel t7a004t1,detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A004.2 Create TABLE with  4-column droppable PK, store by PK col
    defs.exp_err = None
    t7a004t2_ddl._init(_testmgr)
    
    # R2.5 NCI #expectfile $test_dir/A001 a4s2
    stmt = """showddl t7a004t2;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = """showlabel t7a004t2,detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test005(desc="""Create TABLE store by non-PK columns"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    #A005.1 Create table with no PK store by not null, droppable keys
    defs.exp_err = None
    t7a005t1_ddl._init(_testmgr)
    
    # R2.5 NCI #expectfile $test_dir/A001 a5s1
    stmt = """showddl t7a005t1;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = """showlabel t7a005t1,detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A005.2 Create table with droppable PK store by nullable keys
    defs.exp_err = None
    t7a005t2_ddl._init(_testmgr)
    
    # R2.5 NCI #expectfile $test_dir/A001 a5s2
    stmt = """showddl t7a005t2;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = """showlabel t7a005t2,detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A005.3 Create table with PK, store by not null, not droppable keys
    defs.exp_err = None
    t7a005t3_ddl._init(_testmgr)
    
    # R2.5 NCI #expectfile $test_dir/A001 a5s3
    stmt = """showddl t7a005t3;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = """showlabel t7a005t3,detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test006(desc="""Create TABLE store by superset of PK"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    #A006.1 Create TABLE with droppable 4-col PK, store by 4-col + 1 CK
    defs.exp_err = None
    t7a006t1_ddl._init(_testmgr)
    
    # R2.5 NCI #expectfile $test_dir/A001 a6s1
    stmt = """showddl t7a006t1;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = """showlabel t7a006t1,detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #A006.2 Create TABLE with not droppable 3-col PK, store by 3-col + 2 CK
    defs.exp_err = None
    t7a006t2_ddl._init(_testmgr)
    
    # R2.5 NCI #expectfile $test_dir/A001 a6s2
    stmt = """showddl t7a006t2;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = """showlabel t7a006t2,detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test007(desc="""Negative store by tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #N001.last  Create partitions with incompatible data type specification
    #  beware this will cause all subsequent tests to fail!!!  make it last...
    # #unexpect any *ERROR[2006]*
    stmt = """Create Table t7test
(
sbin0_500           Largeint                      no default not null,
time1_uniq          Time                          not null,
char15_100          Character(8)               not null,
dt16_m_n10          Date                     ,
int16_h_20          Interval hour                 no default not null,
ubin16_n10          Numeric(4) unsigned                    no default,
sdec16_uniq         Decimal(18) signed         not null,
char16_n20          Character(5)        ,   -- len = 2,4
real16_10           Real                          no default not null,
primary key  (  time1_uniq, sbin0_500, sdec16_uniq desc, int16_h_20, char15_100) not droppable
)
store by primary key;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '1246')
    elif hpdci.tgtTR():
        _dci.expect_complete_msg(output)
 
    _testmgr.testcase_end(desc)

def test008(desc="""Create TABLE droppable Pk different from store by"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    #A007.1 Create TABLE with droppable  PK, store by
    #primary key (droppable), different from store by
    #clustering key = store by + syskey
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    #a007.1 Primary key - asc ( droppable ) , different from store by
    #single partitioned table
    defs.exp_err = None    
    t7a007t1_ddl._init(_testmgr)
    
    # R2.5 NCI #expectfile $test_dir/a07exp a7s1
    stmt = """showddl t7a007t1;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = """showlabel t7a007t1,detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # R2.5 NCI #expect any *20*
    # R2.5 NCI #sh import $my_schema.t7a007t1 -I $datadir/b2pnl11.dat -C 20
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.t7a007t1
(select * from """ + gvars.g_schema_sqldpop + """.b2pnl11);"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    # R2.5 NCI #expectfile $test_dir/a07exp a7s1b
    # TRAF stmt = """select [last 0] char0_uniq, ubin1_1000, int0_ytom_uniq, syskey
    stmt = """select [last 0] char0_uniq, ubin1_1000, int0_ytom_uniq
from t7a007t1
order by char0_uniq, ubin1_1000, int0_ytom_uniq
;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #a07.4 Primary key - desc ( droppable ) , different from store by
    #single partitioned table
    defs.exp_err = None    
    t7a007t4_ddl._init(_testmgr)
    
    # R2.5 NCI #expectfile $test_dir/a07exp a7s4
    stmt = """showddl t7a007t4;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = """showlabel t7a007t4,detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # R2.5 NCI #expect any *20*
    # R2.5 NCI #sh import $my_schema.t7a007t4 -I $datadir/b2pnl11.dat -C 20
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.t7a007t4
(select * from """ + gvars.g_schema_sqldpop + """.b2pnl11);"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    # R2.5 NCI #expectfile $test_dir/a07exp a7s4b
    # TRAF stmt = """select [last 0] char0_uniq, ubin1_1000, int0_ytom_uniq, syskey
    stmt = """select [last 0] char0_uniq, ubin1_1000, int0_ytom_uniq
from t7a007t4
order by char0_uniq, ubin1_1000, int0_ytom_uniq
;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    _testmgr.testcase_end(desc)

def test009(desc="""Create TABLE Pk same as store by"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    #Primary key (not droppable), same as store by (A002.3)
    #primary key = clustering key
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    #a08.1 Primary key - asc ( not droppable ) , same as store by
    #single partitioned table
    #store by primary key
    defs.exp_err = None    
    t7a008t1_ddl._init(_testmgr)
    
    # R2.5 NCI #expectfile $test_dir/a08exp a8s1
    stmt = """showddl t7a008t1;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = """showlabel t7a008t1,detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # R2.5 NCI #expect any *Exit Status: 0*
    # R2.5 NCI #sh import $my_schema.t7a008t1 -I $datadir/b2pwl16.dat -C 20
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.t7a008t1
(select * from """ + gvars.g_schema_sqldpop + """.b2pwl16);"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    # R2.5 NCI #expectfile $test_dir/a08exp a8s1b
    stmt = """select [last 0] real1_uniq , sdec16_uniq
from t7a008t1
order by real1_uniq , sdec16_uniq
;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #a08.2 Primary key - asc ( not droppable ) , same as store by
    #partitioned table ( single node )
    #store by primary key
    defs.exp_err = None    
    t7a008t2_ddl._init(_testmgr)
    
    # R2.5 NCI #expectfile $test_dir/a08exp a8s2
    stmt = """showddl t7a008t2;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = """showlabel t7a008t2,detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # R2.5 NCI #expect any *Exit Status: 0*
    # R2.5 NCI #sh import $my_schema.t7a008t2 -I $datadir/b2pwl16.dat -C 20
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.t7a008t2
(select * from """ + gvars.g_schema_sqldpop + """.b2pwl16);"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    # R2.5 NCI #expectfile $test_dir/a08exp a8s2b
    stmt = """select [last 0] real1_uniq, sdec16_uniq
from t7a008t2
order by  real1_uniq, sdec16_uniq
;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #a08.3 Primary key - asc ( not droppable ) , same as store by
    #partitioned table ( multi node )
    #store by primary key
    defs.exp_err = None    
    t7a008t3_ddl._init(_testmgr)
    
    # R2.5 NCI #expectfile $test_dir/a08exp a8s3
    stmt = """showddl t7a008t3;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = """showlabel t7a008t3,detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # R2.5 NCI #expect any *Exit Status: 0*
    # R2.5 NCI #sh import $my_schema.t7a008t3 -I $datadir/b2pwl16.dat -C 20
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.t7a008t3
(select * from """ + gvars.g_schema_sqldpop + """.b2pwl16);"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    # R2.5 NCI #expectfile $test_dir/a08exp a8s3b
    stmt = """select [last 0] real1_uniq , sdec16_uniq
from t7a008t3
order by  real1_uniq , sdec16_uniq
;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #a08.4 Primary key - desc ( not droppable ) , same as store by
    #single partitioned table
    #store by ()
    defs.exp_err = None    
    t7a008t4_ddl._init(_testmgr)
    
    # R2.5 NCI #expectfile $test_dir/a08exp a8s4
    stmt = """showddl t7a008t4;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = """showlabel t7a008t4,detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # R2.5 NCI #expect any *Exit Status: 0*
    # R2.5 NCI #sh import $my_schema.t7a008t4 -I $datadir/b2pwl16.dat -C 20
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.t7a008t4
(select * from """ + gvars.g_schema_sqldpop + """.b2pwl16);"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    # R2.5 NCI #expectfile $test_dir/a08exp a8s4b
    stmt = """select [last 0] real1_uniq, sdec16_uniq
from t7a008t4
order by  real1_uniq, sdec16_uniq
;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #a08.5 Primary key - desc ( not droppable ) , same as store by
    #partitioned table ( single node )
    #store by ()
    defs.exp_err = '1160'    
    t7a008t5_ddl._init(_testmgr)
    
    stmt = """showddl t7a008t5;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '4082')
    elif hpdci.tgtTR():
        _dci.expect_complete_msg(output)
 
    stmt = """showlabel t7a008t5,detail;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '1004')
    elif hpdci.tgtTR():
        _dci.expect_complete_msg(output)
 
    ##expect any *Exit Status: 0*
    # R2.5 NCI #expect any *ERROR*
    # R2.5 NCI #sh import $my_schema.t7a008t5 -I $datadir/b2pwl16.dat -C 20
    
    stmt = """select  real1_uniq, sdec16_uniq
from t7a008t5
order by  real1_uniq, sdec16_uniq
;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '4082')
    elif hpdci.tgtTR():
        _dci.expect_selected_msg(output)
    
    #a08.6 Primary key - desc ( not droppable ) , same as store by
    #partitioned table ( multi node )
    #store by ()
    defs.exp_err = '1160'    
    t7a008t6_ddl._init(_testmgr)
    
    stmt = """showddl t7a008t6;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '4082')
    elif hpdci.tgtTR():
        _dci.expect_complete_msg(output)
    
    stmt = """showlabel t7a008t6,detail;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '1004')
    elif hpdci.tgtTR():
        _dci.expect_complete_msg(output)
    
    ##expect any *Exit Status: 0*
    # R2.5 NCI #expect any *ERROR*
    # R2.5 NCI #sh import $my_schema.t7a008t6 -I $datadir/b2pwl16.dat -C 20
    
    stmt = """select  real1_uniq, sdec16_uniq
from t7a008t6
order by  real1_uniq, sdec16_uniq;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '4082')
    elif hpdci.tgtTR():
        _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test010(desc="""Create TABLE PK different from store by"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    #primary key (not droppable) different from store by
    #Error occurs
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    #a09.1 Primary key - asc ( not droppable ) , different from store
    #single partitioned table
    defs.exp_err = '1160'    
    t7a009t1_ddl._init(_testmgr)
    
    #a09.2 Primary key - asc ( not droppable ) , different from store
    #partitioned table ( single node )
    defs.exp_err = '1160'    
    t7a009t2_ddl._init(_testmgr)
    
    #a09.3 Primary key - asc ( not droppable ) , different from store
    #partitioned table ( multi node )
    defs.exp_err = '1160'    
    t7a009t3_ddl._init(_testmgr)
    
    #a09.4 Primary key - desc ( not droppable ) , different from store
    #single partitioned table
    defs.exp_err = '1160'    
    t7a009t4_ddl._init(_testmgr)
    
    #a09.5 Primary key - desc ( not droppable ) , different from store
    #partitioned table ( single node )
    defs.exp_err = '1160'    
    t7a009t5_ddl._init(_testmgr)
    
    #a09.6 Primary key - desc ( not droppable ) , different from store
    #partitioned table ( multi node )
    defs.exp_err = '1160'    
    t7a009t6_ddl._init(_testmgr)
    
    _testmgr.testcase_end(desc)

