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
    
def test001(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0309 : A05
    #  Description:        This test verifies the SQL/K <specify>
    #                      feature.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    # File: JOINTST                     Formerly .jhvc30.qnn
    # Component: NonStop SQL Compiler Regression Test Suite
    # Description:  Outer Join Test file, and this file is used
    #               by following tests files:
    #                      SQLC3010
    #                      SQLC3011
    #
    
    # Insert data
    stmt = """insert into tab1 values (3,3,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab1 values (1,1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab1 values (5,5,5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab1 values (2,2,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab1 values (6,6,null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab1 values (4,4,4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into tab2 values (4,4,4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab2 values (3,3,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab2 values (6,6,null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab2 values (5,5,5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into tab3 values (6, 6, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab3 values (5,5,5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab3 values (7,7,7);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into oj1 values (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into oj1 values (2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into oj2 values (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update statistics for table tab1 on every column;"""
    output = _dci.cmdexec(stmt)
    stmt = """update statistics for table tab2 on every column;"""
    output = _dci.cmdexec(stmt)
    stmt = """update statistics for table tab3 on every column;"""
    output = _dci.cmdexec(stmt)
    stmt = """update statistics for table oj1 on every column;"""
    output = _dci.cmdexec(stmt)
    stmt = """update statistics for table oj2 on every column;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')
    stmt = """select * from tab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s6')
    stmt = """select * from tab3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s7')
    
    #  No join predicates, only truth valued orphans
    stmt = """select * from tab2 left join tab3 on 1 = 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s8')
    stmt = """select * from tab2 left join tab3 on 0 = 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s9')
    
    #  No join predicates, only single table predicates
    
    #  Predicate on primary key column
    stmt = """select * from tab2 left join tab3 on tab2_pk =  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s10')
    stmt = """select * from tab2 left join tab3 on tab2_pk <  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s11')
    stmt = """select * from tab2 left join tab3 on tab2_pk <= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s12')
    stmt = """select * from tab2 left join tab3 on tab2_pk >  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s13')
    stmt = """select * from tab2 left join tab3 on tab2_pk >= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s14')
    stmt = """select * from tab2 left join tab3 on tab3_pk =  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s15')
    stmt = """select * from tab2 left join tab3 on tab3_pk <  6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s16')
    stmt = """select * from tab2 left join tab3 on tab3_pk <= 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s17')
    stmt = """select * from tab2 left join tab3 on tab3_pk >  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s18')
    stmt = """select * from tab2 left join tab3 on tab3_pk >= 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s19')
    
    #  Predicate on a column null not allowed
    stmt = """select * from tab2 left join tab3 on tab2_nn =  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s20')
    stmt = """select * from tab2 left join tab3 on tab2_nn <  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s21')
    stmt = """select * from tab2 left join tab3 on tab2_nn <= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s22')
    stmt = """select * from tab2 left join tab3 on tab2_nn >  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s23')
    stmt = """select * from tab2 left join tab3 on tab2_nn >= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s24')
    stmt = """select * from tab2 left join tab3 on tab3_nn =  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s25')
    stmt = """select * from tab2 left join tab3 on tab3_nn <  6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s26')
    stmt = """select * from tab2 left join tab3 on tab3_nn <= 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s27')
    stmt = """select * from tab2 left join tab3 on tab3_nn >  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s28')
    stmt = """select * from tab2 left join tab3 on tab3_nn >= 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s29')
    
    #  Predicate on a nullable column
    stmt = """select * from tab2 left join tab3 on tab2_na =  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s30')
    stmt = """select * from tab2 left join tab3 on tab2_na <  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s31')
    stmt = """select * from tab2 left join tab3 on tab2_na <= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s32')
    stmt = """select * from tab2 left join tab3 on tab2_na >  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s33')
    stmt = """select * from tab2 left join tab3 on tab2_na >= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s34')
    stmt = """select * from tab2 left join tab3 on tab3_na =  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s35')
    stmt = """select * from tab2 left join tab3 on tab3_na <  6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s36')
    stmt = """select * from tab2 left join tab3 on tab3_na <= 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s37')
    stmt = """select * from tab2 left join tab3 on tab3_na >  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s38')
    stmt = """select * from tab2 left join tab3 on tab3_na >= 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s39')
    
    #  SECTION
    #  Simple join predicates
    
    #  Equijoin predicates
    stmt = """select * from tab2 left join tab3 on tab2_pk =  tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s40')
    stmt = """select * from tab2 left join tab3 on tab2_pk =  tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s41')
    stmt = """select * from tab2 left join tab3 on tab2_pk =  tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s42')
    stmt = """select * from tab2 left join tab3 on tab2_nn =  tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s43')
    stmt = """select * from tab2 left join tab3 on tab2_nn =  tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s44')
    stmt = """select * from tab2 left join tab3 on tab2_nn =  tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s45')
    stmt = """select * from tab2 left join tab3 on tab2_na =  tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s46')
    stmt = """select * from tab2 left join tab3 on tab2_na =  tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s47')
    stmt = """select * from tab2 left join tab3 on tab2_na =  tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s48')
    
    #  < predicates
    stmt = """select * from tab2 left join tab3 on tab2_pk <  tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s49')
    stmt = """select * from tab2 left join tab3 on tab2_pk <  tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s50')
    stmt = """select * from tab2 left join tab3 on tab2_pk <  tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s51')
    stmt = """select * from tab2 left join tab3 on tab2_nn <  tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s52')
    stmt = """select * from tab2 left join tab3 on tab2_nn <  tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s53')
    stmt = """select * from tab2 left join tab3 on tab2_nn <  tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s54')
    stmt = """select * from tab2 left join tab3 on tab2_na <  tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s55')
    stmt = """select * from tab2 left join tab3 on tab2_na <  tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s56')
    stmt = """select * from tab2 left join tab3 on tab2_na <  tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s57')
    
    #  <= predicates
    stmt = """select * from tab2 left join tab3 on tab2_pk <= tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s58')
    stmt = """select * from tab2 left join tab3 on tab2_pk <= tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s59')
    stmt = """select * from tab2 left join tab3 on tab2_pk <= tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s60')
    stmt = """select * from tab2 left join tab3 on tab2_nn <= tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s61')
    stmt = """select * from tab2 left join tab3 on tab2_nn <= tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s62')
    stmt = """select * from tab2 left join tab3 on tab2_nn <= tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s63')
    stmt = """select * from tab2 left join tab3 on tab2_na <= tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s64')
    stmt = """select * from tab2 left join tab3 on tab2_na <= tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s65')
    stmt = """select * from tab2 left join tab3 on tab2_na <= tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s66')
    
    #  >= predicates
    stmt = """select * from tab2 left join tab3 on tab2_pk >= tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s67')
    stmt = """select * from tab2 left join tab3 on tab2_pk >= tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s68')
    stmt = """select * from tab2 left join tab3 on tab2_pk >= tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s69')
    stmt = """select * from tab2 left join tab3 on tab2_nn >= tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s70')
    stmt = """select * from tab2 left join tab3 on tab2_nn >= tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s71')
    stmt = """select * from tab2 left join tab3 on tab2_nn >= tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s72')
    stmt = """select * from tab2 left join tab3 on tab2_na >= tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s73')
    stmt = """select * from tab2 left join tab3 on tab2_na >= tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s74')
    stmt = """select * from tab2 left join tab3 on tab2_na >= tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s75')
    
    #  > predicates
    stmt = """select * from tab2 left join tab3 on tab2_pk >  tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s76')
    stmt = """select * from tab2 left join tab3 on tab2_pk >  tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s77')
    stmt = """select * from tab2 left join tab3 on tab2_pk >  tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s78')
    stmt = """select * from tab2 left join tab3 on tab2_nn >  tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s79')
    stmt = """select * from tab2 left join tab3 on tab2_nn >  tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s80')
    stmt = """select * from tab2 left join tab3 on tab2_nn >  tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s81')
    stmt = """select * from tab2 left join tab3 on tab2_na >  tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s82')
    stmt = """select * from tab2 left join tab3 on tab2_na >  tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s83')
    stmt = """select * from tab2 left join tab3 on tab2_na >  tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s84')
    
    #  <> predicates
    stmt = """select * from tab2 left join tab3 on tab2_pk <> tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s85')
    stmt = """select * from tab2 left join tab3 on tab2_pk <> tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s86')
    stmt = """select * from tab2 left join tab3 on tab2_pk <> tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s87')
    stmt = """select * from tab2 left join tab3 on tab2_nn <> tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s88')
    stmt = """select * from tab2 left join tab3 on tab2_nn <> tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s89')
    stmt = """select * from tab2 left join tab3 on tab2_nn <> tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s90')
    stmt = """select * from tab2 left join tab3 on tab2_na <> tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s91')
    stmt = """select * from tab2 left join tab3 on tab2_na <> tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s92')
    stmt = """select * from tab2 left join tab3 on tab2_na <> tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s93')
    
    #  SECTION
    #  D combinations of join and single-table predicates (no ORs)
    
    #  Join on primary key columns
    stmt = """select tab2_pk, tab3_pk from tab2 left join tab3 on tab2_pk =  tab3_pk
and       1 =  1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s94')
    stmt = """select tab2_pk, tab3_pk from tab2 left join tab3 on tab2_pk =  tab3_pk
and       0 =  1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s95')
    stmt = """select tab2_pk, tab3_pk from tab2 left join tab3 on tab2_pk =  tab3_pk
and tab2_pk =  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s96')
    stmt = """select tab2_pk, tab3_pk from tab2 left join tab3 on tab2_pk =  tab3_pk
and tab2_pk >  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s97')
    stmt = """select tab2_pk, tab3_pk from tab2 left join tab3 on tab2_pk =  tab3_pk
and tab2_pk >= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s98')
    stmt = """select tab2_pk, tab3_pk from tab2 left join tab3 on tab2_pk =  tab3_pk
and tab2_pk <  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s99')
    stmt = """select tab2_pk, tab3_pk from tab2 left join tab3 on tab2_pk =  tab3_pk
and tab2_pk <= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s100')
    stmt = """select tab2_pk, tab3_pk from tab2 left join tab3 on tab2_pk =  tab3_pk
and tab2_pk <> 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s101')
    stmt = """select tab2_pk, tab3_pk from tab2 left join tab3 on tab2_pk =  tab3_pk
and tab3_pk =  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s102')
    stmt = """select tab2_pk, tab3_pk from tab2 left join tab3 on tab2_pk =  tab3_pk
and tab3_pk <  6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s103')
    stmt = """select tab2_pk, tab3_pk from tab2 left join tab3 on tab2_pk =  tab3_pk
and tab3_pk <= 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s104')
    stmt = """select tab2_pk, tab3_pk from tab2 left join tab3 on tab2_pk =  tab3_pk
and tab3_pk >  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s105')
    stmt = """select tab2_pk, tab3_pk from tab2 left join tab3 on tab2_pk =  tab3_pk
and tab3_pk >= 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s106')
    stmt = """select tab2_pk, tab3_pk from tab2 left join tab3 on tab2_pk =  tab3_pk
and tab3_pk <> 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s107')
    stmt = """select tab2_pk, tab3_pk from tab2 left join tab3 on tab2_pk =  tab3_pk
and tab2_pk is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s108')
    stmt = """select tab2_pk, tab3_pk from tab2 left join tab3 on tab2_pk =  tab3_pk
and tab2_pk is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s109')
    stmt = """select tab2_pk, tab3_pk from tab2 left join tab3 on tab2_pk =  tab3_pk
and tab3_pk is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s110')
    stmt = """select tab2_pk, tab3_pk from tab2 left join tab3 on tab2_pk =  tab3_pk
and tab3_pk is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s111')
    
    #  Join on primary key column, non-key non null column
    stmt = """select tab2_pk, tab3_nn from tab2 left join tab3 on tab2_pk =  tab3_nn
and       1 =  1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s112')
    stmt = """select tab2_pk, tab3_nn from tab2 left join tab3 on tab2_pk =  tab3_nn
and       0 =  1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s113')
    stmt = """select tab2_pk, tab3_nn from tab2 left join tab3 on tab2_pk =  tab3_nn
and tab2_pk =  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s114')
    stmt = """select tab2_pk, tab3_nn from tab2 left join tab3 on tab2_pk =  tab3_nn
and tab2_pk >  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s115')
    stmt = """select tab2_pk, tab3_nn from tab2 left join tab3 on tab2_pk =  tab3_nn
and tab2_pk >= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s116')
    stmt = """select tab2_pk, tab3_nn from tab2 left join tab3 on tab2_pk =  tab3_nn
and tab2_pk <  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s117')
    stmt = """select tab2_pk, tab3_nn from tab2 left join tab3 on tab2_pk =  tab3_nn
and tab2_pk <= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s118')
    stmt = """select tab2_pk, tab3_nn from tab2 left join tab3 on tab2_pk =  tab3_nn
and tab2_pk <> 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s119')
    stmt = """select tab2_pk, tab3_nn from tab2 left join tab3 on tab2_pk =  tab3_nn
and tab3_nn =  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s120')
    stmt = """select tab2_pk, tab3_nn from tab2 left join tab3 on tab2_pk =  tab3_nn
and tab3_nn <  6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s121')
    stmt = """select tab2_pk, tab3_nn from tab2 left join tab3 on tab2_pk =  tab3_nn
and tab3_nn <= 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s122')
    stmt = """select tab2_pk, tab3_nn from tab2 left join tab3 on tab2_pk =  tab3_nn
and tab3_nn >  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s123')
    stmt = """select tab2_pk, tab3_nn from tab2 left join tab3 on tab2_pk =  tab3_nn
and tab3_nn >= 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s124')
    stmt = """select tab2_pk, tab3_nn from tab2 left join tab3 on tab2_pk =  tab3_nn
and tab3_nn <> 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s125')
    stmt = """select tab2_pk, tab3_nn from tab2 left join tab3 on tab2_pk =  tab3_nn
and tab2_pk is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s126')
    stmt = """select tab2_pk, tab3_nn from tab2 left join tab3 on tab2_pk =  tab3_nn
and tab2_pk is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s127')
    stmt = """select tab2_pk, tab3_nn from tab2 left join tab3 on tab2_pk =  tab3_nn
and tab3_nn is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s128')
    stmt = """select tab2_pk, tab3_nn from tab2 left join tab3 on tab2_pk =  tab3_nn
and tab3_nn is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s129')
    
    #  Join on primary key column, non-key nullable column
    stmt = """select tab2_pk, tab3_na from tab2 left join tab3 on tab2_pk =  tab3_na
and       1 =  1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s130')
    stmt = """select tab2_pk, tab3_na from tab2 left join tab3 on tab2_pk =  tab3_na
and       0 =  1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s131')
    stmt = """select tab2_pk, tab3_na from tab2 left join tab3 on tab2_pk =  tab3_na
and tab2_pk =  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s132')
    stmt = """select tab2_pk, tab3_na from tab2 left join tab3 on tab2_pk =  tab3_na
and tab2_pk >  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s133')
    stmt = """select tab2_pk, tab3_na from tab2 left join tab3 on tab2_pk =  tab3_na
and tab2_pk >= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s134')
    stmt = """select tab2_pk, tab3_na from tab2 left join tab3 on tab2_pk =  tab3_na
and tab2_pk <  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s135')
    stmt = """select tab2_pk, tab3_na from tab2 left join tab3 on tab2_pk =  tab3_na
and tab2_pk <= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s136')
    stmt = """select tab2_pk, tab3_na from tab2 left join tab3 on tab2_pk =  tab3_na
and tab2_pk <> 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s137')
    stmt = """select tab2_pk, tab3_na from tab2 left join tab3 on tab2_pk =  tab3_na
and tab3_na =  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s138')
    stmt = """select tab2_pk, tab3_na from tab2 left join tab3 on tab2_pk =  tab3_na
and tab3_na <  6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s139')
    stmt = """select tab2_pk, tab3_na from tab2 left join tab3 on tab2_pk =  tab3_na
and tab3_na <= 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s140')
    stmt = """select tab2_pk, tab3_na from tab2 left join tab3 on tab2_pk =  tab3_na
and tab3_na >  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s141')
    stmt = """select tab2_pk, tab3_na from tab2 left join tab3 on tab2_pk =  tab3_na
and tab3_na >= 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s142')
    stmt = """select tab2_pk, tab3_na from tab2 left join tab3 on tab2_pk =  tab3_na
and tab3_na <> 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s143')
    stmt = """select tab2_pk, tab3_na from tab2 left join tab3 on tab2_pk =  tab3_na
and tab2_pk is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s144')
    stmt = """select tab2_pk, tab3_na from tab2 left join tab3 on tab2_pk =  tab3_na
and tab2_pk is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s145')
    stmt = """select tab2_pk, tab3_na from tab2 left join tab3 on tab2_pk =  tab3_na
and tab3_na is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s146')
    stmt = """select tab2_pk, tab3_na from tab2 left join tab3 on tab2_pk =  tab3_na
and tab3_na is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s147')
    
    #  Join on non-key not null column, primary key column
    stmt = """select tab2_nn, tab3_pk from tab2 left join tab3 on tab2_nn =  tab3_pk
and       1 =  1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s148')
    stmt = """select tab2_nn, tab3_pk from tab2 left join tab3 on tab2_nn =  tab3_pk
and       0 =  1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s149')
    stmt = """select tab2_nn, tab3_pk from tab2 left join tab3 on tab2_nn =  tab3_pk
and tab2_nn =  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s150')
    stmt = """select tab2_nn, tab3_pk from tab2 left join tab3 on tab2_nn =  tab3_pk
and tab2_nn >  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s151')
    stmt = """select tab2_nn, tab3_pk from tab2 left join tab3 on tab2_nn =  tab3_pk
and tab2_nn >= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s152')
    stmt = """select tab2_nn, tab3_pk from tab2 left join tab3 on tab2_nn =  tab3_pk
and tab2_nn <  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s153')
    stmt = """select tab2_nn, tab3_pk from tab2 left join tab3 on tab2_nn =  tab3_pk
and tab2_nn <= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s154')
    stmt = """select tab2_nn, tab3_pk from tab2 left join tab3 on tab2_nn =  tab3_pk
and tab2_nn <> 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s155')
    stmt = """select tab2_nn, tab3_pk from tab2 left join tab3 on tab2_nn =  tab3_pk
and tab3_pk =  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s156')
    stmt = """select tab2_nn, tab3_pk from tab2 left join tab3 on tab2_nn =  tab3_pk
and tab3_pk <  6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s157')
    stmt = """select tab2_nn, tab3_pk from tab2 left join tab3 on tab2_nn =  tab3_pk
and tab3_pk <= 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s158')
    stmt = """select tab2_nn, tab3_pk from tab2 left join tab3 on tab2_nn =  tab3_pk
and tab3_pk >  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s159')
    stmt = """select tab2_nn, tab3_pk from tab2 left join tab3 on tab2_nn =  tab3_pk
and tab3_pk >= 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s160')
    stmt = """select tab2_nn, tab3_pk from tab2 left join tab3 on tab2_nn =  tab3_pk
and tab3_pk <> 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s161')
    stmt = """select tab2_nn, tab3_pk from tab2 left join tab3 on tab2_nn =  tab3_pk
and tab2_nn is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s162')
    stmt = """select tab2_nn, tab3_pk from tab2 left join tab3 on tab2_nn =  tab3_pk
and tab2_nn is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s163')
    stmt = """select tab2_nn, tab3_pk from tab2 left join tab3 on tab2_nn =  tab3_pk
and tab3_pk is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s164')
    stmt = """select tab2_nn, tab3_pk from tab2 left join tab3 on tab2_nn =  tab3_pk
and tab3_pk is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s165')
    
    #  Join on non-key not null columns
    stmt = """select tab2_nn, tab3_nn from tab2 left join tab3 on tab2_nn =  tab3_nn
and       1 =  1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s166')
    stmt = """select tab2_nn, tab3_nn from tab2 left join tab3 on tab2_nn =  tab3_nn
and       0 =  1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s167')
    stmt = """select tab2_nn, tab3_nn from tab2 left join tab3 on tab2_nn =  tab3_nn
and tab2_nn =  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s168')
    stmt = """select tab2_nn, tab3_nn from tab2 left join tab3 on tab2_nn =  tab3_nn
and tab2_nn >  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s169')
    stmt = """select tab2_nn, tab3_nn from tab2 left join tab3 on tab2_nn =  tab3_nn
and tab2_nn >= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s170')
    stmt = """select tab2_nn, tab3_nn from tab2 left join tab3 on tab2_nn =  tab3_nn
and tab2_nn <  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s171')
    stmt = """select tab2_nn, tab3_nn from tab2 left join tab3 on tab2_nn =  tab3_nn
and tab2_nn <= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s172')
    stmt = """select tab2_nn, tab3_nn from tab2 left join tab3 on tab2_nn =  tab3_nn
and tab2_nn <> 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s173')
    stmt = """select tab2_nn, tab3_nn from tab2 left join tab3 on tab2_nn =  tab3_nn
and tab3_nn =  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s174')
    stmt = """select tab2_nn, tab3_nn from tab2 left join tab3 on tab2_nn =  tab3_nn
and tab3_nn <  6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s175')
    stmt = """select tab2_nn, tab3_nn from tab2 left join tab3 on tab2_nn =  tab3_nn
and tab3_nn <= 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s176')
    stmt = """select tab2_nn, tab3_nn from tab2 left join tab3 on tab2_nn =  tab3_nn
and tab3_nn >  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s177')
    stmt = """select tab2_nn, tab3_nn from tab2 left join tab3 on tab2_nn =  tab3_nn
and tab3_nn >= 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s178')
    stmt = """select tab2_nn, tab3_nn from tab2 left join tab3 on tab2_nn =  tab3_nn
and tab3_nn <> 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s179')
    stmt = """select tab2_nn, tab3_nn from tab2 left join tab3 on tab2_nn =  tab3_nn
and tab2_nn is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s180')
    stmt = """select tab2_nn, tab3_nn from tab2 left join tab3 on tab2_nn =  tab3_nn
and tab2_nn is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s181')
    stmt = """select tab2_nn, tab3_nn from tab2 left join tab3 on tab2_nn =  tab3_nn
and tab3_nn is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s182')
    stmt = """select tab2_nn, tab3_nn from tab2 left join tab3 on tab2_nn =  tab3_nn
and tab3_nn is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s183')
    
    #  Join on not null column, nullable column, both non-key
    stmt = """select tab2_nn, tab3_na from tab2 left join tab3 on tab2_nn =  tab3_na
and       1 =  1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s184')
    stmt = """select tab2_nn, tab3_na from tab2 left join tab3 on tab2_nn =  tab3_na
and       0 =  1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s185')
    stmt = """select tab2_nn, tab3_na from tab2 left join tab3 on tab2_nn =  tab3_na
and tab2_nn =  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s186')
    stmt = """select tab2_nn, tab3_na from tab2 left join tab3 on tab2_nn =  tab3_na
and tab2_nn >  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s187')
    stmt = """select tab2_nn, tab3_na from tab2 left join tab3 on tab2_nn =  tab3_na
and tab2_nn >= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s188')
    stmt = """select tab2_nn, tab3_na from tab2 left join tab3 on tab2_nn =  tab3_na
and tab2_nn <  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s189')
    stmt = """select tab2_nn, tab3_na from tab2 left join tab3 on tab2_nn =  tab3_na
and tab2_nn <= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s190')
    stmt = """select tab2_nn, tab3_na from tab2 left join tab3 on tab2_nn =  tab3_na
and tab2_nn <> 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s191')
    stmt = """select tab2_nn, tab3_na from tab2 left join tab3 on tab2_nn =  tab3_na
and tab3_na =  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s192')
    stmt = """select tab2_nn, tab3_na from tab2 left join tab3 on tab2_nn =  tab3_na
and tab3_na <  6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s193')
    stmt = """select tab2_nn, tab3_na from tab2 left join tab3 on tab2_nn =  tab3_na
and tab3_na <= 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s194')
    stmt = """select tab2_nn, tab3_na from tab2 left join tab3 on tab2_nn =  tab3_na
and tab3_na >  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s195')
    stmt = """select tab2_nn, tab3_na from tab2 left join tab3 on tab2_nn =  tab3_na
and tab3_na >= 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s196')
    stmt = """select tab2_nn, tab3_na from tab2 left join tab3 on tab2_nn =  tab3_na
and tab3_na <> 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s197')
    stmt = """select tab2_nn, tab3_na from tab2 left join tab3 on tab2_nn =  tab3_na
and tab2_nn is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s198')
    stmt = """select tab2_nn, tab3_na from tab2 left join tab3 on tab2_nn =  tab3_na
and tab2_nn is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s199')
    stmt = """select tab2_nn, tab3_na from tab2 left join tab3 on tab2_nn =  tab3_na
and tab3_na is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s200')
    stmt = """select tab2_nn, tab3_na from tab2 left join tab3 on tab2_nn =  tab3_na
and tab3_na is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s201')
    
    #  Join on non-key nullable column, primary key column
    stmt = """select tab2_na, tab3_pk from tab2 left join tab3 on tab2_na =  tab3_pk
and       1 =  1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s202')
    stmt = """select tab2_na, tab3_pk from tab2 left join tab3 on tab2_na =  tab3_pk
and       0 =  1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s203')
    stmt = """select tab2_na, tab3_pk from tab2 left join tab3 on tab2_na =  tab3_pk
and tab2_na =  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s204')
    stmt = """select tab2_na, tab3_pk from tab2 left join tab3 on tab2_na =  tab3_pk
and tab2_na >  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s205')
    stmt = """select tab2_na, tab3_pk from tab2 left join tab3 on tab2_na =  tab3_pk
and tab2_na >= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s206')
    stmt = """select tab2_na, tab3_pk from tab2 left join tab3 on tab2_na =  tab3_pk
and tab2_na <  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s207')
    stmt = """select tab2_na, tab3_pk from tab2 left join tab3 on tab2_na =  tab3_pk
and tab2_na <= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s208')
    stmt = """select tab2_na, tab3_pk from tab2 left join tab3 on tab2_na =  tab3_pk
and tab2_na <> 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s209')
    stmt = """select tab2_na, tab3_pk from tab2 left join tab3 on tab2_na =  tab3_pk
and tab3_pk =  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s210')
    stmt = """select tab2_na, tab3_pk from tab2 left join tab3 on tab2_na =  tab3_pk
and tab3_pk <  6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s211')
    stmt = """select tab2_na, tab3_pk from tab2 left join tab3 on tab2_na =  tab3_pk
and tab3_pk <= 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s212')
    stmt = """select tab2_na, tab3_pk from tab2 left join tab3 on tab2_na =  tab3_pk
and tab3_pk >  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s213')
    stmt = """select tab2_na, tab3_pk from tab2 left join tab3 on tab2_na =  tab3_pk
and tab3_pk >= 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s214')
    stmt = """select tab2_na, tab3_pk from tab2 left join tab3 on tab2_na =  tab3_pk
and tab3_pk <> 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s215')
    stmt = """select tab2_na, tab3_pk from tab2 left join tab3 on tab2_na =  tab3_pk
and tab2_na is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s216')
    stmt = """select tab2_na, tab3_pk from tab2 left join tab3 on tab2_na =  tab3_pk
and tab2_na is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s217')
    stmt = """select tab2_na, tab3_pk from tab2 left join tab3 on tab2_na =  tab3_pk
and tab3_pk is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s218')
    stmt = """select tab2_na, tab3_pk from tab2 left join tab3 on tab2_na =  tab3_pk
and tab3_pk is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s219')
    
    #  Join on nullable column, not null column, both non-key
    stmt = """select tab2_na, tab3_nn from tab2 left join tab3 on tab2_na =  tab3_nn
and       1 =  1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s220')
    stmt = """select tab2_na, tab3_nn from tab2 left join tab3 on tab2_na =  tab3_nn
and       0 =  1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s221')
    stmt = """select tab2_na, tab3_nn from tab2 left join tab3 on tab2_na =  tab3_nn
and tab2_na =  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s222')
    stmt = """select tab2_na, tab3_nn from tab2 left join tab3 on tab2_na =  tab3_nn
and tab2_na >  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s223')
    stmt = """select tab2_na, tab3_nn from tab2 left join tab3 on tab2_na =  tab3_nn
and tab2_na >= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s224')
    stmt = """select tab2_na, tab3_nn from tab2 left join tab3 on tab2_na =  tab3_nn
and tab2_na <  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s225')
    stmt = """select tab2_na, tab3_nn from tab2 left join tab3 on tab2_na =  tab3_nn
and tab2_na <= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s226')
    stmt = """select tab2_na, tab3_nn from tab2 left join tab3 on tab2_na =  tab3_nn
and tab2_na <> 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s227')
    stmt = """select tab2_na, tab3_nn from tab2 left join tab3 on tab2_na =  tab3_nn
and tab3_nn =  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s228')
    stmt = """select tab2_na, tab3_nn from tab2 left join tab3 on tab2_na =  tab3_nn
and tab3_nn <  6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s229')
    stmt = """select tab2_na, tab3_nn from tab2 left join tab3 on tab2_na =  tab3_nn
and tab3_nn <= 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s230')
    stmt = """select tab2_na, tab3_nn from tab2 left join tab3 on tab2_na =  tab3_nn
and tab3_nn >  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s231')
    stmt = """select tab2_na, tab3_nn from tab2 left join tab3 on tab2_na =  tab3_nn
and tab3_nn >= 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s232')
    stmt = """select tab2_na, tab3_nn from tab2 left join tab3 on tab2_na =  tab3_nn
and tab3_nn <> 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s233')
    stmt = """select tab2_na, tab3_nn from tab2 left join tab3 on tab2_na =  tab3_nn
and tab2_na is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s234')
    stmt = """select tab2_na, tab3_nn from tab2 left join tab3 on tab2_na =  tab3_nn
and tab2_na is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s235')
    stmt = """select tab2_na, tab3_nn from tab2 left join tab3 on tab2_na =  tab3_nn
and tab3_nn is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s236')
    stmt = """select tab2_na, tab3_nn from tab2 left join tab3 on tab2_na =  tab3_nn
and tab3_nn is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s237')
    
    #  Join on non-key columns which do not allow nulls
    stmt = """select tab2_na, tab3_na from tab2 left join tab3 on tab2_na =  tab3_na
and       1 =  1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s238')
    stmt = """select tab2_na, tab3_na from tab2 left join tab3 on tab2_na =  tab3_na
and       0 =  1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s239')
    stmt = """select tab2_na, tab3_na from tab2 left join tab3 on tab2_na =  tab3_na
and tab2_na =  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s240')
    stmt = """select tab2_na, tab3_na from tab2 left join tab3 on tab2_na =  tab3_na
and tab2_na >  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s241')
    stmt = """select tab2_na, tab3_na from tab2 left join tab3 on tab2_na =  tab3_na
and tab2_na >= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s242')
    stmt = """select tab2_na, tab3_na from tab2 left join tab3 on tab2_na =  tab3_na
and tab2_na <  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s243')
    stmt = """select tab2_na, tab3_na from tab2 left join tab3 on tab2_na =  tab3_na
and tab2_na <= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s244')
    stmt = """select tab2_na, tab3_na from tab2 left join tab3 on tab2_na =  tab3_na
and tab2_na <> 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s245')
    stmt = """select tab2_na, tab3_na from tab2 left join tab3 on tab2_na =  tab3_na
and tab3_na =  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s246')
    stmt = """select tab2_na, tab3_na from tab2 left join tab3 on tab2_na =  tab3_na
and tab3_na <  6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s247')
    stmt = """select tab2_na, tab3_na from tab2 left join tab3 on tab2_na =  tab3_na
and tab3_na <= 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s248')
    stmt = """select tab2_na, tab3_na from tab2 left join tab3 on tab2_na =  tab3_na
and tab3_na >  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s249')
    stmt = """select tab2_na, tab3_na from tab2 left join tab3 on tab2_na =  tab3_na
and tab3_na >= 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s250')
    stmt = """select tab2_na, tab3_na from tab2 left join tab3 on tab2_na =  tab3_na
and tab3_na <> 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s251')
    stmt = """select tab2_na, tab3_na from tab2 left join tab3 on tab2_na =  tab3_na
and tab2_na is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s252')
    stmt = """select tab2_na, tab3_na from tab2 left join tab3 on tab2_na =  tab3_na
and tab2_na is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s253')
    stmt = """select tab2_na, tab3_na from tab2 left join tab3 on tab2_na =  tab3_na
and tab3_na is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s254')
    stmt = """select tab2_na, tab3_na from tab2 left join tab3 on tab2_na =  tab3_na
and tab3_na is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s255')
    
    #  SECTION : WHERE CLSE
    
    #  Join on primary key columns
    
    stmt = """select tab2_pk, tab3_pk from tab2 left join tab3 on tab2_pk =  tab3_pk
where       1 =  1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s256')
    stmt = """select tab2_pk, tab3_pk from tab2 left join tab3 on tab2_pk =  tab3_pk
where       0 =  1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select tab2_pk, tab3_pk from tab2 left join tab3 on tab2_pk =  tab3_pk
where tab2_pk =  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s257')
    stmt = """select tab2_pk, tab3_pk from tab2 left join tab3 on tab2_pk =  tab3_pk
where tab2_pk >  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s258')
    stmt = """select tab2_pk, tab3_pk from tab2 left join tab3 on tab2_pk =  tab3_pk
where tab2_pk >= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s259')
    stmt = """select tab2_pk, tab3_pk from tab2 left join tab3 on tab2_pk =  tab3_pk
where tab2_pk <  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s260')
    stmt = """select tab2_pk, tab3_pk from tab2 left join tab3 on tab2_pk =  tab3_pk
where tab2_pk <= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s261')
    stmt = """select tab2_pk, tab3_pk from tab2 left join tab3 on tab2_pk =  tab3_pk
where tab2_pk <> 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s262')
    stmt = """select tab2_pk, tab3_pk from tab2 left join tab3 on tab2_pk =  tab3_pk
where tab3_pk =  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s263')
    stmt = """select tab2_pk, tab3_pk from tab2 left join tab3 on tab2_pk =  tab3_pk
where tab3_pk <  6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s264')
    stmt = """select tab2_pk, tab3_pk from tab2 left join tab3 on tab2_pk =  tab3_pk
where tab3_pk <= 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s265')
    stmt = """select tab2_pk, tab3_pk from tab2 left join tab3 on tab2_pk =  tab3_pk
where tab3_pk >  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s266')
    stmt = """select tab2_pk, tab3_pk from tab2 left join tab3 on tab2_pk =  tab3_pk
where tab3_pk >= 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s267')
    stmt = """select tab2_pk, tab3_pk from tab2 left join tab3 on tab2_pk =  tab3_pk
where tab3_pk <> 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s268')
    stmt = """select tab2_pk, tab3_pk from tab2 left join tab3 on tab2_pk =  tab3_pk
where tab2_pk is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s269')
    stmt = """select tab2_pk, tab3_pk from tab2 left join tab3 on tab2_pk =  tab3_pk
where tab2_pk is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select tab2_pk, tab3_pk from tab2 left join tab3 on tab2_pk =  tab3_pk
where tab3_pk is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s270')
    stmt = """select tab2_pk, tab3_pk from tab2 left join tab3 on tab2_pk =  tab3_pk
where tab3_pk is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s271')
    
    #  Join on primary key column, non-key non null column
    stmt = """select tab2_pk, tab3_nn from tab2 left join tab3 on tab2_pk =  tab3_nn
where       1 =  1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s272')
    stmt = """select tab2_pk, tab3_nn from tab2 left join tab3 on tab2_pk =  tab3_nn
where       0 =  1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select tab2_pk, tab3_nn from tab2 left join tab3 on tab2_pk =  tab3_nn
where tab2_pk =  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s273')
    stmt = """select tab2_pk, tab3_nn from tab2 left join tab3 on tab2_pk =  tab3_nn
where tab2_pk >  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s274')
    stmt = """select tab2_pk, tab3_nn from tab2 left join tab3 on tab2_pk =  tab3_nn
where tab2_pk >= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s275')
    stmt = """select tab2_pk, tab3_nn from tab2 left join tab3 on tab2_pk =  tab3_nn
where tab2_pk <  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s276')
    stmt = """select tab2_pk, tab3_nn from tab2 left join tab3 on tab2_pk =  tab3_nn
where tab2_pk <= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s277')
    stmt = """select tab2_pk, tab3_nn from tab2 left join tab3 on tab2_pk =  tab3_nn
where tab2_pk <> 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s278')
    stmt = """select tab2_pk, tab3_nn from tab2 left join tab3 on tab2_pk =  tab3_nn
where tab3_nn =  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s279')
    stmt = """select tab2_pk, tab3_nn from tab2 left join tab3 on tab2_pk =  tab3_nn
where tab3_nn <  6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s280')
    stmt = """select tab2_pk, tab3_nn from tab2 left join tab3 on tab2_pk =  tab3_nn
where tab3_nn <= 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s281')
    stmt = """select tab2_pk, tab3_nn from tab2 left join tab3 on tab2_pk =  tab3_nn
where tab3_nn >  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s282')
    stmt = """select tab2_pk, tab3_nn from tab2 left join tab3 on tab2_pk =  tab3_nn
where tab3_nn >= 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s283')
    stmt = """select tab2_pk, tab3_nn from tab2 left join tab3 on tab2_pk =  tab3_nn
where tab3_nn <> 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s284')
    stmt = """select tab2_pk, tab3_nn from tab2 left join tab3 on tab2_pk =  tab3_nn
where tab2_pk is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s285')
    stmt = """select tab2_pk, tab3_nn from tab2 left join tab3 on tab2_pk =  tab3_nn
where tab2_pk is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select tab2_pk, tab3_nn from tab2 left join tab3 on tab2_pk =  tab3_nn
where tab3_nn is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s286')
    stmt = """select tab2_pk, tab3_nn from tab2 left join tab3 on tab2_pk =  tab3_nn
where tab3_nn is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s287')
    
    #  Join on primary key column, non-key nullable column
    stmt = """select tab2_pk, tab3_na from tab2 left join tab3 on tab2_pk =  tab3_na
where       1 =  1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s288')
    stmt = """select tab2_pk, tab3_na from tab2 left join tab3 on tab2_pk =  tab3_na
where       0 =  1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select tab2_pk, tab3_na from tab2 left join tab3 on tab2_pk =  tab3_na
where tab2_pk =  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s289')
    stmt = """select tab2_pk, tab3_na from tab2 left join tab3 on tab2_pk =  tab3_na
where tab2_pk >  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s290')
    stmt = """select tab2_pk, tab3_na from tab2 left join tab3 on tab2_pk =  tab3_na
where tab2_pk >= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s291')
    stmt = """select tab2_pk, tab3_na from tab2 left join tab3 on tab2_pk =  tab3_na
where tab2_pk <  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s292')
    stmt = """select tab2_pk, tab3_na from tab2 left join tab3 on tab2_pk =  tab3_na
where tab2_pk <= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s293')
    stmt = """select tab2_pk, tab3_na from tab2 left join tab3 on tab2_pk =  tab3_na
where tab2_pk <> 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s294')
    stmt = """select tab2_pk, tab3_na from tab2 left join tab3 on tab2_pk =  tab3_na
where tab3_na =  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s295')
    stmt = """select tab2_pk, tab3_na from tab2 left join tab3 on tab2_pk =  tab3_na
where tab3_na <  6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s296')
    stmt = """select tab2_pk, tab3_na from tab2 left join tab3 on tab2_pk =  tab3_na
where tab3_na <= 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s297')
    stmt = """select tab2_pk, tab3_na from tab2 left join tab3 on tab2_pk =  tab3_na
where tab3_na >  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select tab2_pk, tab3_na from tab2 left join tab3 on tab2_pk =  tab3_na
where tab3_na >= 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s298')
    stmt = """select tab2_pk, tab3_na from tab2 left join tab3 on tab2_pk =  tab3_na
where tab3_na <> 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select tab2_pk, tab3_na from tab2 left join tab3 on tab2_pk =  tab3_na
where tab2_pk is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s299')
    stmt = """select tab2_pk, tab3_na from tab2 left join tab3 on tab2_pk =  tab3_na
where tab2_pk is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select tab2_pk, tab3_na from tab2 left join tab3 on tab2_pk =  tab3_na
where tab3_na is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s300')
    stmt = """select tab2_pk, tab3_na from tab2 left join tab3 on tab2_pk =  tab3_na
where tab3_na is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s301')
    
    #  Join on non-key not null column, primary key column
    stmt = """select tab2_nn, tab3_pk from tab2 left join tab3 on tab2_nn =  tab3_pk
where       1 =  1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s302')
    stmt = """select tab2_nn, tab3_pk from tab2 left join tab3 on tab2_nn =  tab3_pk
where       0 =  1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select tab2_nn, tab3_pk from tab2 left join tab3 on tab2_nn =  tab3_pk
where tab2_nn =  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s303')
    stmt = """select tab2_nn, tab3_pk from tab2 left join tab3 on tab2_nn =  tab3_pk
where tab2_nn >  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s304')
    stmt = """select tab2_nn, tab3_pk from tab2 left join tab3 on tab2_nn =  tab3_pk
where tab2_nn >= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s305')
    stmt = """select tab2_nn, tab3_pk from tab2 left join tab3 on tab2_nn =  tab3_pk
where tab2_nn <  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s306')
    stmt = """select tab2_nn, tab3_pk from tab2 left join tab3 on tab2_nn =  tab3_pk
where tab2_nn <= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s307')
    stmt = """select tab2_nn, tab3_pk from tab2 left join tab3 on tab2_nn =  tab3_pk
where tab2_nn <> 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s308')
    stmt = """select tab2_nn, tab3_pk from tab2 left join tab3 on tab2_nn =  tab3_pk
where tab3_pk =  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s309')
    stmt = """select tab2_nn, tab3_pk from tab2 left join tab3 on tab2_nn =  tab3_pk
where tab3_pk <  6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s310')
    stmt = """select tab2_nn, tab3_pk from tab2 left join tab3 on tab2_nn =  tab3_pk
where tab3_pk <= 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s311')
    stmt = """select tab2_nn, tab3_pk from tab2 left join tab3 on tab2_nn =  tab3_pk
where tab3_pk >  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s312')
    stmt = """select tab2_nn, tab3_pk from tab2 left join tab3 on tab2_nn =  tab3_pk
where tab3_pk >= 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s313')
    stmt = """select tab2_nn, tab3_pk from tab2 left join tab3 on tab2_nn =  tab3_pk
where tab3_pk <> 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s314')
    stmt = """select tab2_nn, tab3_pk from tab2 left join tab3 on tab2_nn =  tab3_pk
where tab2_nn is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s315')
    stmt = """select tab2_nn, tab3_pk from tab2 left join tab3 on tab2_nn =  tab3_pk
where tab2_nn is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select tab2_nn, tab3_pk from tab2 left join tab3 on tab2_nn =  tab3_pk
where tab3_pk is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s316')
    stmt = """select tab2_nn, tab3_pk from tab2 left join tab3 on tab2_nn =  tab3_pk
where tab3_pk is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s317')
    
    #  Join on non-key not null columns
    stmt = """select tab2_nn, tab3_nn from tab2 left join tab3 on tab2_nn =  tab3_nn
where       1 =  1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s318')
    stmt = """select tab2_nn, tab3_nn from tab2 left join tab3 on tab2_nn =  tab3_nn
where       0 =  1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select tab2_nn, tab3_nn from tab2 left join tab3 on tab2_nn =  tab3_nn
where tab2_nn =  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s319')
    stmt = """select tab2_nn, tab3_nn from tab2 left join tab3 on tab2_nn =  tab3_nn
where tab2_nn >  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s320')
    stmt = """select tab2_nn, tab3_nn from tab2 left join tab3 on tab2_nn =  tab3_nn
where tab2_nn >= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s321')
    stmt = """select tab2_nn, tab3_nn from tab2 left join tab3 on tab2_nn =  tab3_nn
where tab2_nn <  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s322')
    stmt = """select tab2_nn, tab3_nn from tab2 left join tab3 on tab2_nn =  tab3_nn
where tab2_nn <= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s323')
    stmt = """select tab2_nn, tab3_nn from tab2 left join tab3 on tab2_nn =  tab3_nn
where tab2_nn <> 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s324')
    stmt = """select tab2_nn, tab3_nn from tab2 left join tab3 on tab2_nn =  tab3_nn
where tab3_nn =  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s325')
    stmt = """select tab2_nn, tab3_nn from tab2 left join tab3 on tab2_nn =  tab3_nn
where tab3_nn <  6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s326')
    stmt = """select tab2_nn, tab3_nn from tab2 left join tab3 on tab2_nn =  tab3_nn
where tab3_nn <= 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s327')
    stmt = """select tab2_nn, tab3_nn from tab2 left join tab3 on tab2_nn =  tab3_nn
where tab3_nn >  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s328')
    stmt = """select tab2_nn, tab3_nn from tab2 left join tab3 on tab2_nn =  tab3_nn
where tab3_nn >= 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s329')
    stmt = """select tab2_nn, tab3_nn from tab2 left join tab3 on tab2_nn =  tab3_nn
where tab3_nn <> 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s330')
    stmt = """select tab2_nn, tab3_nn from tab2 left join tab3 on tab2_nn =  tab3_nn
where tab2_nn is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s331')
    stmt = """select tab2_nn, tab3_nn from tab2 left join tab3 on tab2_nn =  tab3_nn
where tab2_nn is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select tab2_nn, tab3_nn from tab2 left join tab3 on tab2_nn =  tab3_nn
where tab3_nn is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s332')
    stmt = """select tab2_nn, tab3_nn from tab2 left join tab3 on tab2_nn =  tab3_nn
where tab3_nn is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s333')
    
    #  Join on not null column, nullable column, both non-key
    stmt = """select tab2_nn, tab3_na from tab2 left join tab3 on tab2_nn =  tab3_na
where       1 =  1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s334')
    stmt = """select tab2_nn, tab3_na from tab2 left join tab3 on tab2_nn =  tab3_na
where       0 =  1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select tab2_nn, tab3_na from tab2 left join tab3 on tab2_nn =  tab3_na
where tab2_nn =  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s335')
    stmt = """select tab2_nn, tab3_na from tab2 left join tab3 on tab2_nn =  tab3_na
where tab2_nn >  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s336')
    stmt = """select tab2_nn, tab3_na from tab2 left join tab3 on tab2_nn =  tab3_na
where tab2_nn >= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s337')
    stmt = """select tab2_nn, tab3_na from tab2 left join tab3 on tab2_nn =  tab3_na
where tab2_nn <  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s338')
    stmt = """select tab2_nn, tab3_na from tab2 left join tab3 on tab2_nn =  tab3_na
where tab2_nn <= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s339')
    stmt = """select tab2_nn, tab3_na from tab2 left join tab3 on tab2_nn =  tab3_na
where tab2_nn <> 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s340')
    stmt = """select tab2_nn, tab3_na from tab2 left join tab3 on tab2_nn =  tab3_na
where tab3_na =  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s341')
    stmt = """select tab2_nn, tab3_na from tab2 left join tab3 on tab2_nn =  tab3_na
where tab3_na <  6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s342')
    stmt = """select tab2_nn, tab3_na from tab2 left join tab3 on tab2_nn =  tab3_na
where tab3_na <= 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s343')
    stmt = """select tab2_nn, tab3_na from tab2 left join tab3 on tab2_nn =  tab3_na
where tab3_na >  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select tab2_nn, tab3_na from tab2 left join tab3 on tab2_nn =  tab3_na
where tab3_na >= 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s344')
    stmt = """select tab2_nn, tab3_na from tab2 left join tab3 on tab2_nn =  tab3_na
where tab3_na <> 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select tab2_nn, tab3_na from tab2 left join tab3 on tab2_nn =  tab3_na
where tab2_nn is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s345')
    stmt = """select tab2_nn, tab3_na from tab2 left join tab3 on tab2_nn =  tab3_na
where tab2_nn is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select tab2_nn, tab3_na from tab2 left join tab3 on tab2_nn =  tab3_na
where tab3_na is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s346')
    stmt = """select tab2_nn, tab3_na from tab2 left join tab3 on tab2_nn =  tab3_na
where tab3_na is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s347')
    
    #  Join on non-key nullable column, primary key column
    stmt = """select tab2_na, tab3_pk from tab2 left join tab3 on tab2_na =  tab3_pk
where       1 =  1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s348')
    stmt = """select tab2_na, tab3_pk from tab2 left join tab3 on tab2_na =  tab3_pk
where       0 =  1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select tab2_na, tab3_pk from tab2 left join tab3 on tab2_na =  tab3_pk
where tab2_na =  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s349')
    stmt = """select tab2_na, tab3_pk from tab2 left join tab3 on tab2_na =  tab3_pk
where tab2_na >  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s350')
    stmt = """select tab2_na, tab3_pk from tab2 left join tab3 on tab2_na =  tab3_pk
where tab2_na >= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s351')
    stmt = """select tab2_na, tab3_pk from tab2 left join tab3 on tab2_na =  tab3_pk
where tab2_na <  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s352')
    stmt = """select tab2_na, tab3_pk from tab2 left join tab3 on tab2_na =  tab3_pk
where tab2_na <= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s353')
    stmt = """select tab2_na, tab3_pk from tab2 left join tab3 on tab2_na =  tab3_pk
where tab2_na <> 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s354')
    stmt = """select tab2_na, tab3_pk from tab2 left join tab3 on tab2_na =  tab3_pk
where tab3_pk =  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s355')
    stmt = """select tab2_na, tab3_pk from tab2 left join tab3 on tab2_na =  tab3_pk
where tab3_pk <  6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s356')
    stmt = """select tab2_na, tab3_pk from tab2 left join tab3 on tab2_na =  tab3_pk
where tab3_pk <= 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s357')
    stmt = """select tab2_na, tab3_pk from tab2 left join tab3 on tab2_na =  tab3_pk
where tab3_pk >  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select tab2_na, tab3_pk from tab2 left join tab3 on tab2_na =  tab3_pk
where tab3_pk >= 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s358')
    stmt = """select tab2_na, tab3_pk from tab2 left join tab3 on tab2_na =  tab3_pk
where tab3_pk <> 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select tab2_na, tab3_pk from tab2 left join tab3 on tab2_na =  tab3_pk
where tab2_na is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s359')
    stmt = """select tab2_na, tab3_pk from tab2 left join tab3 on tab2_na =  tab3_pk
where tab2_na is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s360')
    stmt = """select tab2_na, tab3_pk from tab2 left join tab3 on tab2_na =  tab3_pk
where tab3_pk is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s361')
    stmt = """select tab2_na, tab3_pk from tab2 left join tab3 on tab2_na =  tab3_pk
where tab3_pk is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s362')
    
    #  Join on nullable column, not null column, both non-key
    stmt = """select tab2_na, tab3_nn from tab2 left join tab3 on tab2_na =  tab3_nn
where       1 =  1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s363')
    stmt = """select tab2_na, tab3_nn from tab2 left join tab3 on tab2_na =  tab3_nn
where       0 =  1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select tab2_na, tab3_nn from tab2 left join tab3 on tab2_na =  tab3_nn
where tab2_na =  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s364')
    stmt = """select tab2_na, tab3_nn from tab2 left join tab3 on tab2_na =  tab3_nn
where tab2_na >  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s365')
    stmt = """select tab2_na, tab3_nn from tab2 left join tab3 on tab2_na =  tab3_nn
where tab2_na >= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s366')
    stmt = """select tab2_na, tab3_nn from tab2 left join tab3 on tab2_na =  tab3_nn
where tab2_na <  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s367')
    stmt = """select tab2_na, tab3_nn from tab2 left join tab3 on tab2_na =  tab3_nn
where tab2_na <= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s368')
    stmt = """select tab2_na, tab3_nn from tab2 left join tab3 on tab2_na =  tab3_nn
where tab2_na <> 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s369')
    stmt = """select tab2_na, tab3_nn from tab2 left join tab3 on tab2_na =  tab3_nn
where tab3_nn =  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s370')
    stmt = """select tab2_na, tab3_nn from tab2 left join tab3 on tab2_na =  tab3_nn
where tab3_nn <  6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s371')
    stmt = """select tab2_na, tab3_nn from tab2 left join tab3 on tab2_na =  tab3_nn
where tab3_nn <= 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s372')
    stmt = """select tab2_na, tab3_nn from tab2 left join tab3 on tab2_na =  tab3_nn
where tab3_nn >  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select tab2_na, tab3_nn from tab2 left join tab3 on tab2_na =  tab3_nn
where tab3_nn >= 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s373')
    stmt = """select tab2_na, tab3_nn from tab2 left join tab3 on tab2_na =  tab3_nn
where tab3_nn <> 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select tab2_na, tab3_nn from tab2 left join tab3 on tab2_na =  tab3_nn
where tab2_na is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s374')
    stmt = """select tab2_na, tab3_nn from tab2 left join tab3 on tab2_na =  tab3_nn
where tab2_na is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s375')
    stmt = """select tab2_na, tab3_nn from tab2 left join tab3 on tab2_na =  tab3_nn
where tab3_nn is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s376')
    stmt = """select tab2_na, tab3_nn from tab2 left join tab3 on tab2_na =  tab3_nn
where tab3_nn is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s377')
    
    #  Join on non-key columns which do not allow nulls
    stmt = """select tab2_na, tab3_na from tab2 left join tab3 on tab2_na =  tab3_na
where       1 =  1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s378')
    stmt = """select tab2_na, tab3_na from tab2 left join tab3 on tab2_na =  tab3_na
where       0 =  1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select tab2_na, tab3_na from tab2 left join tab3 on tab2_na =  tab3_na
where tab2_na =  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s379')
    stmt = """select tab2_na, tab3_na from tab2 left join tab3 on tab2_na =  tab3_na
where tab2_na >  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s380')
    stmt = """select tab2_na, tab3_na from tab2 left join tab3 on tab2_na =  tab3_na
where tab2_na >= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s381')
    stmt = """select tab2_na, tab3_na from tab2 left join tab3 on tab2_na =  tab3_na
where tab2_na <  4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s382')
    stmt = """select tab2_na, tab3_na from tab2 left join tab3 on tab2_na =  tab3_na
where tab2_na <= 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s383')
    stmt = """select tab2_na, tab3_na from tab2 left join tab3 on tab2_na =  tab3_na
where tab2_na <> 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s384')
    stmt = """select tab2_na, tab3_na from tab2 left join tab3 on tab2_na =  tab3_na
where tab3_na =  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s385')
    stmt = """select tab2_na, tab3_na from tab2 left join tab3 on tab2_na =  tab3_na
where tab3_na <  6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s386')
    stmt = """select tab2_na, tab3_na from tab2 left join tab3 on tab2_na =  tab3_na
where tab3_na <= 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s387')
    stmt = """select tab2_na, tab3_na from tab2 left join tab3 on tab2_na =  tab3_na
where tab3_na >  5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select tab2_na, tab3_na from tab2 left join tab3 on tab2_na =  tab3_na
where tab3_na >= 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s388')
    stmt = """select tab2_na, tab3_na from tab2 left join tab3 on tab2_na =  tab3_na
where tab3_na <> 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select tab2_na, tab3_na from tab2 left join tab3 on tab2_na =  tab3_na
where tab2_na is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s389')
    stmt = """select tab2_na, tab3_na from tab2 left join tab3 on tab2_na =  tab3_na
where tab2_na is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s390')
    stmt = """select tab2_na, tab3_na from tab2 left join tab3 on tab2_na =  tab3_na
where tab3_na is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s391')
    stmt = """select tab2_na, tab3_na from tab2 left join tab3 on tab2_na =  tab3_na
where tab3_na is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s392')
    
    #  SECTION : ORDER BY
    
    #  Primary Key Columns (both not null, of course)
    stmt = """select tab2_pk, tab3_pk
from tab2 left join tab3 on tab2_pk =  tab3_pk
order by tab2_pk asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s393')
    stmt = """select tab2_pk, tab3_pk
from tab2 left join tab3 on tab2_pk =  tab3_pk
order by tab2_pk desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s394')
    stmt = """select tab2_pk, tab3_pk
from tab2 left join tab3 on tab2_pk =  tab3_pk
order by tab3_pk asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s395')
    stmt = """select tab2_pk, tab3_pk
from tab2 left join tab3 on tab2_pk =  tab3_pk
order by tab3_pk desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s396')
    stmt = """select tab2_pk, tab3_pk
from tab2 left join tab3 on tab2_pk =  tab3_pk
order by tab2_pk, tab3_pk asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s397')
    stmt = """select tab2_pk, tab3_pk
from tab2 left join tab3 on tab2_pk =  tab3_pk
order by tab2_pk, tab3_pk desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s398')
    stmt = """select tab2_pk, tab3_pk
from tab2 left join tab3 on tab2_pk =  tab3_pk
order by tab3_pk, tab2_pk asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s399')
    stmt = """select tab2_pk, tab3_pk
from tab2 left join tab3 on tab2_pk =  tab3_pk
order by tab3_pk, tab2_pk desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s400')
    
    #  repeat using an index
    stmt = """select tab2_pk, tab3_pk
from tab2 left join tab3 on tab2_pk =  tab3_pk
order by 1 asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s401')
    stmt = """select tab2_pk, tab3_pk
from tab2 left join tab3 on tab2_pk =  tab3_pk
order by 1 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s402')
    stmt = """select tab2_pk, tab3_pk
from tab2 left join tab3 on tab2_pk =  tab3_pk
order by 2 asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s403')
    stmt = """select tab2_pk, tab3_pk
from tab2 left join tab3 on tab2_pk =  tab3_pk
order by 2 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s404')
    stmt = """select tab2_pk, tab3_pk
from tab2 left join tab3 on tab2_pk =  tab3_pk
order by 1, 2 asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s405')
    stmt = """select tab2_pk, tab3_pk
from tab2 left join tab3 on tab2_pk =  tab3_pk
order by 1, 2 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s406')
    stmt = """select tab2_pk, tab3_pk
from tab2 left join tab3 on tab2_pk =  tab3_pk
order by 2, 1 asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s407')
    stmt = """select tab2_pk, tab3_pk
from tab2 left join tab3 on tab2_pk =  tab3_pk
order by 2, 1 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s408')
    
    #  Primary Key Column, non-key non null column
    stmt = """select tab2_pk, tab3_nn
from tab2 left join tab3 on tab2_pk =  tab3_nn
order by tab2_pk asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s409')
    stmt = """select tab2_pk, tab3_nn
from tab2 left join tab3 on tab2_pk =  tab3_nn
order by tab2_pk desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s410')
    stmt = """select tab2_pk, tab3_nn
from tab2 left join tab3 on tab2_pk =  tab3_nn
order by tab3_nn asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s411')
    stmt = """select tab2_pk, tab3_nn
from tab2 left join tab3 on tab2_pk =  tab3_nn
order by tab3_nn desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s412')
    stmt = """select tab2_pk, tab3_nn
from tab2 left join tab3 on tab2_pk =  tab3_nn
order by tab2_pk, tab3_nn asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s413')
    stmt = """select tab2_pk, tab3_nn
from tab2 left join tab3 on tab2_pk =  tab3_nn
order by tab2_pk, tab3_nn desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s414')
    stmt = """select tab2_pk, tab3_nn
from tab2 left join tab3 on tab2_pk =  tab3_nn
order by tab3_nn, tab2_pk asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s415')
    stmt = """select tab2_pk, tab3_nn
from tab2 left join tab3 on tab2_pk =  tab3_nn
order by tab3_nn, tab2_pk desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s416')
    
    #  repeat using an index
    stmt = """select tab2_pk, tab3_nn
from tab2 left join tab3 on tab2_pk =  tab3_nn
order by 1 asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s417')
    stmt = """select tab2_pk, tab3_nn
from tab2 left join tab3 on tab2_pk =  tab3_nn
order by 1 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s418')
    stmt = """select tab2_pk, tab3_nn
from tab2 left join tab3 on tab2_pk =  tab3_nn
order by 2 asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s419')
    stmt = """select tab2_pk, tab3_nn
from tab2 left join tab3 on tab2_pk =  tab3_nn
order by 2 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s420')
    stmt = """select tab2_pk, tab3_nn
from tab2 left join tab3 on tab2_pk =  tab3_nn
order by 1, 2 asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s421')
    stmt = """select tab2_pk, tab3_nn
from tab2 left join tab3 on tab2_pk =  tab3_nn
order by 1, 2 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s422')
    stmt = """select tab2_pk, tab3_nn
from tab2 left join tab3 on tab2_pk =  tab3_nn
order by 2, 1 asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s423')
    stmt = """select tab2_pk, tab3_nn
from tab2 left join tab3 on tab2_pk =  tab3_nn
order by 2, 1 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s424')
    
    #  Primary Key Column, non-key nullable column
    stmt = """select tab2_pk, tab3_na
from tab2 left join tab3 on tab2_pk =  tab3_na
order by tab2_pk asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s425')
    stmt = """select tab2_pk, tab3_na
from tab2 left join tab3 on tab2_pk =  tab3_na
order by tab2_pk desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s426')
    stmt = """select tab2_pk, tab3_na
from tab2 left join tab3 on tab2_pk =  tab3_na
order by tab3_na asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s427')
    stmt = """select tab2_pk, tab3_na
from tab2 left join tab3 on tab2_pk =  tab3_na
order by tab3_na desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s428')
    stmt = """select tab2_pk, tab3_na
from tab2 left join tab3 on tab2_pk =  tab3_na
order by tab2_pk, tab3_na asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s429')
    stmt = """select tab2_pk, tab3_na
from tab2 left join tab3 on tab2_pk =  tab3_na
order by tab2_pk, tab3_na desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s430')
    stmt = """select tab2_pk, tab3_na
from tab2 left join tab3 on tab2_pk =  tab3_na
order by tab3_na, tab2_pk asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s431')
    stmt = """select tab2_pk, tab3_na
from tab2 left join tab3 on tab2_pk =  tab3_na
order by tab3_na, tab2_pk desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s432')
    
    #  repeat using an index
    stmt = """select tab2_pk, tab3_na
from tab2 left join tab3 on tab2_pk =  tab3_na
order by 1 asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s433')
    stmt = """select tab2_pk, tab3_na
from tab2 left join tab3 on tab2_pk =  tab3_na
order by 1 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s434')
    stmt = """select tab2_pk, tab3_na
from tab2 left join tab3 on tab2_pk =  tab3_na
order by 2 asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s435')
    stmt = """select tab2_pk, tab3_na
from tab2 left join tab3 on tab2_pk =  tab3_na
order by 2 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s436')
    stmt = """select tab2_pk, tab3_na
from tab2 left join tab3 on tab2_pk =  tab3_na
order by 1, 2 asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s437')
    stmt = """select tab2_pk, tab3_na
from tab2 left join tab3 on tab2_pk =  tab3_na
order by 1, 2 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s438')
    stmt = """select tab2_pk, tab3_na
from tab2 left join tab3 on tab2_pk =  tab3_na
order by 2, 1 asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s439')
    stmt = """select tab2_pk, tab3_na
from tab2 left join tab3 on tab2_pk =  tab3_na
order by 2, 1 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s440')
    
    #  Non key not null column, Primary Key Columns
    stmt = """select tab2_nn, tab3_pk
from tab2 left join tab3 on tab2_nn =  tab3_pk
order by tab2_nn asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s441')
    stmt = """select tab2_nn, tab3_pk
from tab2 left join tab3 on tab2_nn =  tab3_pk
order by tab2_nn desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s442')
    stmt = """select tab2_nn, tab3_pk
from tab2 left join tab3 on tab2_nn =  tab3_pk
order by tab3_pk asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s443')
    stmt = """select tab2_nn, tab3_pk
from tab2 left join tab3 on tab2_nn =  tab3_pk
order by tab3_pk desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s444')
    stmt = """select tab2_nn, tab3_pk
from tab2 left join tab3 on tab2_nn =  tab3_pk
order by tab2_nn, tab3_pk asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s445')
    stmt = """select tab2_nn, tab3_pk
from tab2 left join tab3 on tab2_nn =  tab3_pk
order by tab2_nn, tab3_pk desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s446')
    stmt = """select tab2_nn, tab3_pk
from tab2 left join tab3 on tab2_nn =  tab3_pk
order by tab3_pk, tab2_nn asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s447')
    stmt = """select tab2_nn, tab3_pk
from tab2 left join tab3 on tab2_nn =  tab3_pk
order by tab3_pk, tab2_nn desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s448')
    
    stmt = """select tab2_nn, tab3_pk
from tab2 left join tab3 on tab2_nn =  tab3_pk
order by 1 asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s449')
    stmt = """select tab2_nn, tab3_pk
from tab2 left join tab3 on tab2_nn =  tab3_pk
order by 1 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s450')
    stmt = """select tab2_nn, tab3_pk
from tab2 left join tab3 on tab2_nn =  tab3_pk
order by 2 asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s451')
    stmt = """select tab2_nn, tab3_pk
from tab2 left join tab3 on tab2_nn =  tab3_pk
order by 2 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s452')
    stmt = """select tab2_nn, tab3_pk
from tab2 left join tab3 on tab2_nn =  tab3_pk
order by 1, 2 asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s453')
    stmt = """select tab2_nn, tab3_pk
from tab2 left join tab3 on tab2_nn =  tab3_pk
order by 1, 2 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s454')
    stmt = """select tab2_nn, tab3_pk
from tab2 left join tab3 on tab2_nn =  tab3_pk
order by 2, 1 asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s455')
    stmt = """select tab2_nn, tab3_pk
from tab2 left join tab3 on tab2_nn =  tab3_pk
order by 2, 1 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s456')
    
    #  Non key nullable column, Primary Key Columns
    stmt = """select tab2_na, tab3_pk
from tab2 left join tab3 on tab2_na =  tab3_pk
order by tab2_na asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s457')
    stmt = """select tab2_na, tab3_pk
from tab2 left join tab3 on tab2_na =  tab3_pk
order by tab2_na desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s458')
    stmt = """select tab2_na, tab3_pk
from tab2 left join tab3 on tab2_na =  tab3_pk
order by tab3_pk asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s459')
    stmt = """select tab2_na, tab3_pk
from tab2 left join tab3 on tab2_na =  tab3_pk
order by tab3_pk desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s460')
    stmt = """select tab2_na, tab3_pk
from tab2 left join tab3 on tab2_na =  tab3_pk
order by tab2_na, tab3_pk asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s461')
    stmt = """select tab2_na, tab3_pk
from tab2 left join tab3 on tab2_na =  tab3_pk
order by tab2_na, tab3_pk desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s462')
    stmt = """select tab2_na, tab3_pk
from tab2 left join tab3 on tab2_na =  tab3_pk
order by tab3_pk, tab2_na asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s463')
    stmt = """select tab2_na, tab3_pk
from tab2 left join tab3 on tab2_na =  tab3_pk
order by tab3_pk, tab2_na desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s464')
    
    #  repeat using an index
    stmt = """select tab2_na, tab3_pk
from tab2 left join tab3 on tab2_na =  tab3_pk
order by 1 asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s465')
    stmt = """select tab2_na, tab3_pk
from tab2 left join tab3 on tab2_na =  tab3_pk
order by 1 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s466')
    stmt = """select tab2_na, tab3_pk
from tab2 left join tab3 on tab2_na =  tab3_pk
order by 2 asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s467')
    stmt = """select tab2_na, tab3_pk
from tab2 left join tab3 on tab2_na =  tab3_pk
order by 2 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s468')
    stmt = """select tab2_na, tab3_pk
from tab2 left join tab3 on tab2_na =  tab3_pk
order by 1, 2 asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s469')
    stmt = """select tab2_na, tab3_pk
from tab2 left join tab3 on tab2_na =  tab3_pk
order by 1, 2 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s470')
    stmt = """select tab2_na, tab3_pk
from tab2 left join tab3 on tab2_na =  tab3_pk
order by 2, 1 asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s471')
    stmt = """select tab2_na, tab3_pk
from tab2 left join tab3 on tab2_na =  tab3_pk
order by 2, 1 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s472')
    
    #  SECTION : GROUP BY
    
    stmt = """select tab2_pk
from tab2 left join tab3 on tab2_pk =  tab3_pk
group by tab2_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s473')
    stmt = """select tab3_pk
from tab2 left join tab3 on tab2_pk =  tab3_pk
group by tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s474')
    stmt = """select tab2_pk
from tab2 left join tab3 on tab2_pk =  tab3_nn
group by tab2_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s475')
    stmt = """select tab3_nn
from tab2 left join tab3 on tab2_pk =  tab3_nn
group by tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s476')
    stmt = """select tab2_pk
from tab2 left join tab3 on tab2_pk =  tab3_na
group by tab2_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s477')
    stmt = """select tab3_na
from tab2 left join tab3 on tab2_pk =  tab3_na
group by tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s478')
    
    stmt = """select tab2_nn
from tab2 left join tab3 on tab2_nn =  tab3_pk
group by tab2_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s479')
    stmt = """select tab3_pk
from tab2 left join tab3 on tab2_nn =  tab3_pk
group by tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s480')
    stmt = """select tab2_nn
from tab2 left join tab3 on tab2_nn =  tab3_nn
group by tab2_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s481')
    stmt = """select tab3_nn
from tab2 left join tab3 on tab2_nn =  tab3_nn
group by tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s482')
    stmt = """select tab2_nn
from tab2 left join tab3 on tab2_nn =  tab3_na
group by tab2_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s483')
    stmt = """select tab3_na
from tab2 left join tab3 on tab2_nn =  tab3_na
group by tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s484')
    
    stmt = """select tab2_na
from tab2 left join tab3 on tab2_na =  tab3_pk
group by tab2_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s485')
    stmt = """select tab3_pk
from tab2 left join tab3 on tab2_na =  tab3_pk
group by tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s486')
    stmt = """select tab2_na
from tab2 left join tab3 on tab2_na =  tab3_nn
group by tab2_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s487')
    stmt = """select tab3_nn
from tab2 left join tab3 on tab2_na =  tab3_nn
group by tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s488')
    stmt = """select tab2_na
from tab2 left join tab3 on tab2_na =  tab3_na
group by tab2_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s489')
    stmt = """select tab3_na
from tab2 left join tab3 on tab2_na =  tab3_na
group by tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s490')
    
    #  SECTION : GREGATION FUNCTIONS
    
    #  COUNT
    
    #  JOIN on primary jey columns
    stmt = """select count(*) from tab2 left join tab3 on tab2_pk = tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s491')
    stmt = """select count(distinct tab2_pk) from tab2 left join tab3 on tab2_pk = tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s492')
    stmt = """select count(distinct tab3_pk) from tab2 left join tab3 on tab2_pk = tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s493')
    
    #  JOIN on primary key column, non-key non null column
    stmt = """select count(*) from tab2 left join tab3 on tab2_pk = tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s494')
    stmt = """select count(distinct tab2_pk) from tab2 left join tab3 on tab2_pk = tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s495')
    stmt = """select count(distinct tab3_nn) from tab2 left join tab3 on tab2_pk = tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s496')
    
    #  JOIN on primary key column, non-key nullable column
    stmt = """select count(*) from tab2 left join tab3 on tab2_pk = tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s497')
    stmt = """select count(distinct tab2_pk) from tab2 left join tab3 on tab2_pk = tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s498')
    stmt = """select count(distinct tab3_na) from tab2 left join tab3 on tab2_pk = tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s499')
    
    #  JOIN on non-key non null column, primary key column
    stmt = """select count(*) from tab2 left join tab3 on tab2_nn = tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s500')
    stmt = """select count(distinct tab2_nn) from tab2 left join tab3 on tab2_nn = tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s501')
    stmt = """select count(distinct tab3_pk) from tab2 left join tab3 on tab2_nn = tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s502')
    
    #  JOIN on non-key non null columns
    stmt = """select count(*) from tab2 left join tab3 on tab2_nn = tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s503')
    stmt = """select count(distinct tab2_nn) from tab2 left join tab3 on tab2_nn = tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s504')
    stmt = """select count(distinct tab3_nn) from tab2 left join tab3 on tab2_nn = tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s505')
    
    #  JOIN on non null, nullable columns, both non-key
    stmt = """select count(*) from tab2 left join tab3 on tab2_nn = tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s506')
    stmt = """select count(distinct tab2_nn) from tab2 left join tab3 on tab2_nn = tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s507')
    stmt = """select count(distinct tab3_na) from tab2 left join tab3 on tab2_nn = tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s508')
    
    #  JOIN on non-key nullable column, primary key column
    stmt = """select count(*) from tab2 left join tab3 on tab2_na = tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s509')
    stmt = """select count(distinct tab2_na) from tab2 left join tab3 on tab2_na = tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s510')
    stmt = """select count(distinct tab3_pk) from tab2 left join tab3 on tab2_na = tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s511')
    
    #  JOIN on nullable, non null columns, both non-key
    stmt = """select count(*) from tab2 left join tab3 on tab2_na = tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s512')
    stmt = """select count(distinct tab2_na) from tab2 left join tab3 on tab2_na = tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s513')
    stmt = """select count(distinct tab3_nn) from tab2 left join tab3 on tab2_na = tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s514')
    
    #  JOIN on non-key nullable columns
    stmt = """select count(*) from tab2 left join tab3 on tab2_na = tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s515')
    stmt = """select count(distinct tab2_na) from tab2 left join tab3 on tab2_na = tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s516')
    stmt = """select count(distinct tab3_na) from tab2 left join tab3 on tab2_na = tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s517')
    
    #  M, MIN
    
    #  JOIN on primary key columns
    stmt = """select max(tab2_pk), min(tab2_pk)
from tab2 left join tab3 on tab2_pk = tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s518')
    stmt = """select max(tab3_pk), min(tab3_pk)
from tab2 left join tab3 on tab2_pk = tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s519')
    
    #  JOIN on primary key column, non-key non null column
    stmt = """select max(tab2_pk), min(tab2_pk)
from tab2 left join tab3 on tab2_pk = tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s520')
    stmt = """select max(tab3_nn), min(tab3_nn)
from tab2 left join tab3 on tab2_pk = tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s521')
    
    #  JOIN on primary key column, non-key nullable column
    stmt = """select max(tab2_pk), min(tab2_pk)
from tab2 left join tab3 on tab2_pk = tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s522')
    stmt = """select max(tab3_na), min(tab3_na)
from tab2 left join tab3 on tab2_pk = tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s523')
    
    #  JOIN on non-key non null column, primary key column
    stmt = """select max(tab2_nn), min(tab2_nn)
from tab2 left join tab3 on tab2_nn = tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s524')
    stmt = """select max(tab3_pk), min(tab3_pk)
from tab2 left join tab3 on tab2_nn = tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s525')
    
    #  JOIN on non-key non null columns
    stmt = """select max(tab2_nn), min(tab2_nn)
from tab2 left join tab3 on tab2_nn = tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s526')
    stmt = """select max(tab3_nn), min(tab3_nn)
from tab2 left join tab3 on tab2_nn = tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s527')
    
    #  JOIN on non null, nullable columns, both non-key
    stmt = """select max(tab2_nn), min(tab2_nn)
from tab2 left join tab3 on tab2_nn = tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s528')
    stmt = """select max(tab3_na), min(tab3_na)
from tab2 left join tab3 on tab2_nn = tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s529')
    
    #  JOIN on non-key nullable column, primary key column
    stmt = """select max(tab2_na), min(tab2_na)
from tab2 left join tab3 on tab2_na = tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s530')
    stmt = """select max(tab3_pk), min(tab3_pk)
from tab2 left join tab3 on tab2_na = tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s531')
    
    #  JOIN on nullable, non null columns, both non-key
    stmt = """select max(tab2_na), min(tab2_na)
from tab2 left join tab3 on tab2_na = tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s532')
    stmt = """select max(tab3_nn), min(tab3_nn)
from tab2 left join tab3 on tab2_na = tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s533')
    
    #  JOIN on non-key nullable columns
    stmt = """select max(tab2_na), min(tab2_na)
from tab2 left join tab3 on tab2_na = tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s534')
    stmt = """select max(tab3_na), min(tab3_na)
from tab2 left join tab3 on tab2_na = tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s535')
    
    #  SUM, G
    
    #  JOIN on primary key columns
    stmt = """select sum(tab2_pk), avg(tab2_pk)
from tab2 left join tab3 on tab2_pk = tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s536')
    stmt = """select sum(tab3_pk), avg(tab3_pk)
from tab2 left join tab3 on tab2_pk = tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s537')
    
    #  JOIN on primary key column, non-key non null column
    stmt = """select sum(tab2_pk), avg(tab2_pk)
from tab2 left join tab3 on tab2_pk = tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s538')
    stmt = """select sum(tab3_nn), avg(tab3_nn)
from tab2 left join tab3 on tab2_pk = tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s539')
    
    #  JOIN on primary key column, non-key nullable column
    stmt = """select sum(tab2_pk), avg(tab2_pk)
from tab2 left join tab3 on tab2_pk = tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s540')
    stmt = """select sum(tab3_na), avg(tab3_na)
from tab2 left join tab3 on tab2_pk = tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s541')
    
    #  JOIN on non-key non null column, primary key column
    stmt = """select sum(tab2_nn), avg(tab2_nn)
from tab2 left join tab3 on tab2_nn = tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s542')
    stmt = """select sum(tab3_pk), avg(tab3_pk)
from tab2 left join tab3 on tab2_nn = tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s543')
    
    #  JOIN on non-key non null columns
    stmt = """select sum(tab2_nn), avg(tab2_nn)
from tab2 left join tab3 on tab2_nn = tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s544')
    stmt = """select sum(tab3_nn), avg(tab3_nn)
from tab2 left join tab3 on tab2_nn = tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s545')
    
    #  JOIN on non null, nullable columns, both non-key
    stmt = """select sum(tab2_nn), avg(tab2_nn)
from tab2 left join tab3 on tab2_nn = tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s546')
    stmt = """select sum(tab3_na), avg(tab3_na)
from tab2 left join tab3 on tab2_nn = tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s547')
    
    #  JOIN on non-key nullable column, primary key column
    stmt = """select sum(tab2_na), avg(tab2_na)
from tab2 left join tab3 on tab2_na = tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s548')
    stmt = """select sum(tab3_pk), avg(tab3_pk)
from tab2 left join tab3 on tab2_na = tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s549')
    
    #  JOIN on nullable, non null columns, both non-key
    stmt = """select sum(tab2_na), avg(tab2_na)
from tab2 left join tab3 on tab2_na = tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s550')
    stmt = """select sum(tab3_nn), avg(tab3_nn)
from tab2 left join tab3 on tab2_na = tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s551')
    
    #  JOIN on non-key nullable columns
    stmt = """select sum(tab2_na), avg(tab2_na)
from tab2 left join tab3 on tab2_na = tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s552')
    stmt = """select sum(tab3_na), avg(tab3_na)
from tab2 left join tab3 on tab2_na = tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s553')
    
    #  SECTION : 3 TLE JOINS
    
    #  pk, pk, pk
    stmt = """select tab1_pk, tab2_pk, tab3_pk
from tab1 left join tab2 on tab1_pk =  tab2_pk
left join tab3 on tab2_pk =  tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s554')
    #  pk, pk, nn
    stmt = """select tab1_pk, tab2_pk, tab3_nn
from tab1 left join tab2 on tab1_pk =  tab2_pk
left join tab3 on tab2_pk =  tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s555')
    
    #  pk, pk, na
    stmt = """select tab1_pk, tab2_pk, tab3_na
from tab1 left join tab2 on tab1_pk =  tab2_pk
left join tab3 on tab2_pk =  tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s556')
    
    #  pk, nn, pk
    stmt = """select tab1_pk, tab2_nn, tab3_pk
from tab1 left join tab2 on tab1_pk =  tab2_nn
left join tab3 on tab2_nn =  tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s557')
    
    #  pk, nn, nn
    stmt = """select tab1_pk, tab2_nn, tab3_nn
from tab1 left join tab2 on tab1_pk =  tab2_nn
left join tab3 on tab2_nn =  tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s558')
    
    #  pk, nn, na
    stmt = """select tab1_pk, tab2_nn, tab3_na
from tab1 left join tab2 on tab1_pk =  tab2_nn
left join tab3 on tab2_nn =  tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s559')
    
    #  pk, na, pk
    stmt = """select tab1_pk, tab2_na, tab3_pk
from tab1 left join tab2 on tab1_pk =  tab2_na
left join tab3 on tab2_na =  tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s560')
    
    #  pk, na, nn
    stmt = """select tab1_pk, tab2_na, tab3_nn
from tab1 left join tab2 on tab1_pk =  tab2_na
left join tab3 on tab2_na =  tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s561')
    
    #  pk, na, na
    stmt = """select tab1_pk, tab2_na, tab3_na
from tab1 left join tab2 on tab1_pk =  tab2_na
left join tab3 on tab2_na =  tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s562')
    
    #  nn, pk, pk
    stmt = """select tab1_nn, tab2_pk, tab3_pk
from tab1 left join tab2 on tab1_nn =  tab2_pk
left join tab3 on tab2_pk =  tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s563')
    
    #  nn, pk, nn
    stmt = """select tab1_nn, tab2_pk, tab3_nn
from tab1 left join tab2 on tab1_nn =  tab2_pk
left join tab3 on tab2_pk =  tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s564')
    
    #  nn, pk, na
    stmt = """select tab1_nn, tab2_pk, tab3_na
from tab1 left join tab2 on tab1_nn =  tab2_pk
left join tab3 on tab2_pk =  tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s565')
    
    #  nn, nn, pk
    stmt = """select tab1_nn, tab2_nn, tab3_pk
from tab1 left join tab2 on tab1_nn =  tab2_nn
left join tab3 on tab2_nn =  tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s566')
    
    #  nn, nn, nn
    stmt = """select tab1_nn, tab2_nn, tab3_nn
from tab1 left join tab2 on tab1_nn =  tab2_nn
left join tab3 on tab2_nn =  tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s567')
    
    #  nn, nn, na
    stmt = """select tab1_nn, tab2_nn, tab3_na
from tab1 left join tab2 on tab1_nn =  tab2_nn
left join tab3 on tab2_nn =  tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s568')
    
    #  nn, na, pk
    stmt = """select tab1_nn, tab2_na, tab3_pk
from tab1 left join tab2 on tab1_nn =  tab2_na
left join tab3 on tab2_na =  tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s569')
    
    #  nn, na, nn
    stmt = """select tab1_nn, tab2_na, tab3_nn
from tab1 left join tab2 on tab1_nn =  tab2_na
left join tab3 on tab2_na =  tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s570')
    
    #  nn, na, na
    stmt = """select tab1_nn, tab2_na, tab3_na
from tab1 left join tab2 on tab1_nn =  tab2_na
left join tab3 on tab2_na =  tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s571')
    
    #  na, pk, pk
    stmt = """select tab1_na, tab2_pk, tab3_pk
from tab1 left join tab2 on tab1_na =  tab2_pk
left join tab3 on tab2_pk =  tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s572')
    
    #  na, pk, nn
    stmt = """select tab1_na, tab2_pk, tab3_nn
from tab1 left join tab2 on tab1_na =  tab2_pk
left join tab3 on tab2_pk =  tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s573')
    
    #  na, pk, na
    stmt = """select tab1_na, tab2_pk, tab3_na
from tab1 left join tab2 on tab1_na =  tab2_pk
left join tab3 on tab2_pk =  tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s574')
    
    #  na, nn, pk
    stmt = """select tab1_na, tab2_nn, tab3_pk
from tab1 left join tab2 on tab1_na =  tab2_nn
left join tab3 on tab2_nn =  tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s575')
    
    #  na, nn, nn
    stmt = """select tab1_na, tab2_nn, tab3_nn
from tab1 left join tab2 on tab1_na =  tab2_nn
left join tab3 on tab2_nn =  tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s576')
    
    #  na, nn, na
    stmt = """select tab1_na, tab2_nn, tab3_na
from tab1 left join tab2 on tab1_na =  tab2_nn
left join tab3 on tab2_nn =  tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s577')
    
    #  na, na, pk
    stmt = """select tab1_na, tab2_na, tab3_pk
from tab1 left join tab2 on tab1_na =  tab2_na
left join tab3 on tab2_na =  tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s578')
    
    #  na, na, nn
    stmt = """select tab1_na, tab2_na, tab3_nn
from tab1 left join tab2 on tab1_na =  tab2_na
left join tab3 on tab2_na =  tab3_nn;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s579')
    
    #  na, na, na
    stmt = """select tab1_na, tab2_na, tab3_na
from tab1 left join tab2 on tab1_na =  tab2_na
left join tab3 on tab2_na =  tab3_na;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s580')
    
    #  Set 1
    stmt = """select tab1_pk, tab2_pk, tab3_pk
from tab1 left join tab2 on tab1_pk =  tab2_pk
left join tab3 on tab2_pk <  tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s581')
    stmt = """select tab1_pk, tab2_pk, tab3_pk
from tab1 left join tab2 on tab1_pk =  tab2_pk
left join tab3 on tab2_pk >  tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s582')
    stmt = """select tab1_pk, tab2_pk, tab3_pk
from tab1 left join tab2 on tab1_pk =  tab2_pk
left join tab3 on tab2_pk <> tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s583')
    
    #  Set 2
    stmt = """select tab1_pk, tab2_pk, tab3_pk
from tab1 left join tab2 on tab1_pk <  tab2_pk
left join tab3 on tab2_pk =  tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s584')
    stmt = """select tab1_pk, tab2_pk, tab3_pk
from tab1 left join tab2 on tab1_pk <  tab2_pk
left join tab3 on tab2_pk <  tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s585')
    stmt = """select tab1_pk, tab2_pk, tab3_pk
from tab1 left join tab2 on tab1_pk <  tab2_pk
left join tab3 on tab2_pk >  tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s586')
    stmt = """select tab1_pk, tab2_pk, tab3_pk
from tab1 left join tab2 on tab1_pk <  tab2_pk
left join tab3 on tab2_pk <> tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s587')
    
    #  Set 3
    stmt = """select tab1_pk, tab2_pk, tab3_pk
from tab1 left join tab2 on tab1_pk >  tab2_pk
left join tab3 on tab2_pk =  tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s588')
    stmt = """select tab1_pk, tab2_pk, tab3_pk
from tab1 left join tab2 on tab1_pk >  tab2_pk
left join tab3 on tab2_pk <  tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s589')
    stmt = """select tab1_pk, tab2_pk, tab3_pk
from tab1 left join tab2 on tab1_pk >  tab2_pk
left join tab3 on tab2_pk >  tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s590')
    stmt = """select tab1_pk, tab2_pk, tab3_pk
from tab1 left join tab2 on tab1_pk >  tab2_pk
left join tab3 on tab2_pk <> tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s591')
    #  Set 4
    stmt = """select tab1_pk, tab2_pk, tab3_pk
from tab1 left join tab2 on tab1_pk <> tab2_pk
left join tab3 on tab2_pk =  tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s592')
    stmt = """select tab1_pk, tab2_pk, tab3_pk
from tab1 left join tab2 on tab1_pk <> tab2_pk
left join tab3 on tab2_pk <  tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s593')
    stmt = """select tab1_pk, tab2_pk, tab3_pk
from tab1 left join tab2 on tab1_pk <> tab2_pk
left join tab3 on tab2_pk >  tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s594')
    stmt = """select tab1_pk, tab2_pk, tab3_pk
from tab1 left join tab2 on tab1_pk <> tab2_pk
left join tab3 on tab2_pk <> tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s595')
    
    #  Union all of outer joins
    
    #  nn,nn Ua nn,nn
    stmt = """select tab2_nn, tab3_nn
from tab2 left join tab3 on tab2_nn = tab3_nn
union all
select tab2_nn, tab3_nn
from tab3 left join tab2 on tab2_nn = tab3_nn
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s596')
    
    #  nn,nn Ua nn,na
    stmt = """select tab2_nn, tab3_nn
from tab2 left join tab3 on tab2_nn = tab3_nn
union all
select tab2_nn, tab3_na
from tab3 left join tab2 on tab2_nn = tab3_na
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s597')
    
    #  nn,nn Ua na,nn
    stmt = """select tab2_nn, tab3_nn
from tab2 left join tab3 on tab2_nn = tab3_nn
union all
select tab2_na, tab3_nn
from tab3 left join tab2 on tab2_na = tab3_nn
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s598')
    
    #  nn,nn Ua na,na
    stmt = """select tab2_nn, tab3_nn
from tab2 left join tab3 on tab2_nn = tab3_nn
union all
select tab2_na, tab3_na
from tab3 left join tab2 on tab2_na = tab3_na
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s599')
    
    #  nn,na Ua nn,nn
    stmt = """select tab2_nn, tab3_na
from tab2 left join tab3 on tab2_nn = tab3_na
union all
select tab2_nn, tab3_nn
from tab3 left join tab2 on tab2_nn = tab3_nn
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s600')
    
    #  nn,na Ua nn,na
    stmt = """select tab2_nn, tab3_na
from tab2 left join tab3 on tab2_nn = tab3_na
union all
select tab2_nn, tab3_na
from tab3 left join tab2 on tab2_nn = tab3_na
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s601')
    
    #  nn,na Ua na,nn
    stmt = """select tab2_nn, tab3_na
from tab2 left join tab3 on tab2_nn = tab3_na
union all
select tab2_na, tab3_nn
from tab3 left join tab2 on tab2_na = tab3_nn
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s602')
    
    #  nn,na Ua na,na
    stmt = """select tab2_nn, tab3_na
from tab2 left join tab3 on tab2_nn = tab3_na
union all
select tab2_na, tab3_na
from tab3 left join tab2 on tab2_na = tab3_na
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s603')
    
    #  na,nn Ua nn,nn
    stmt = """select tab2_na, tab3_nn
from tab2 left join tab3 on tab2_na = tab3_nn
union all
select tab2_nn, tab3_nn
from tab3 left join tab2 on tab2_nn = tab3_nn
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s604')
    
    #  na,nn Ua nn,na
    stmt = """select tab2_na, tab3_nn
from tab2 left join tab3 on tab2_na = tab3_nn
union all
select tab2_nn, tab3_na
from tab3 left join tab2 on tab2_nn = tab3_na
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s605')
    
    #  na,nn Ua na,nn
    stmt = """select tab2_na, tab3_nn
from tab2 left join tab3 on tab2_na = tab3_nn
union all
select tab2_na, tab3_nn
from tab3 left join tab2 on tab2_na = tab3_nn
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s606')
    
    #  na,nn Ua na,na
    stmt = """select tab2_na, tab3_nn
from tab2 left join tab3 on tab2_na = tab3_nn
union all
select tab2_na, tab3_na
from tab3 left join tab2 on tab2_na = tab3_na
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s607')
    
    #  na,na Ua nn,nn
    stmt = """select tab2_na, tab3_na
from tab2 left join tab3 on tab2_na = tab3_na
union all
select tab2_nn, tab3_nn
from tab3 left join tab2 on tab2_nn = tab3_nn
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s608')
    
    #  na,na Ua nn,na
    stmt = """select tab2_na, tab3_na
from tab2 left join tab3 on tab2_na = tab3_na
union all
select tab2_nn, tab3_na
from tab3 left join tab2 on tab2_nn = tab3_na
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s609')
    
    #  na,na Ua na,nn
    stmt = """select tab2_na, tab3_na
from tab2 left join tab3 on tab2_na = tab3_na
union all
select tab2_na, tab3_nn
from tab3 left join tab2 on tab2_na = tab3_nn
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s610')
    
    #  na,na Ua na,na
    stmt = """select tab2_na, tab3_na
from tab2 left join tab3 on tab2_na = tab3_na
union all
select tab2_na, tab3_na
from tab3 left join tab2 on tab2_na = tab3_na
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s611')
    
    #  Union  of outer joins
    
    #  nn,nn U nn,nn
    stmt = """select tab2_nn, tab3_nn
from tab2 left join tab3 on tab2_nn = tab3_nn
union
select tab2_nn, tab3_nn
from tab3 left join tab2 on tab2_nn = tab3_nn
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s612')
    
    #  nn,nn U nn,na
    stmt = """select tab2_nn, tab3_nn
from tab2 left join tab3 on tab2_nn = tab3_nn
union
select tab2_nn, tab3_na
from tab3 left join tab2 on tab2_nn = tab3_na
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s613')
    
    #  nn,nn U na,nn
    stmt = """select tab2_nn, tab3_nn
from tab2 left join tab3 on tab2_nn = tab3_nn
union
select tab2_na, tab3_nn
from tab3 left join tab2 on tab2_na = tab3_nn
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s614')
    
    #  nn,nn U na,na
    stmt = """select tab2_nn, tab3_nn
from tab2 left join tab3 on tab2_nn = tab3_nn
union
select tab2_na, tab3_na
from tab3 left join tab2 on tab2_na = tab3_na
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s615')
    
    #  nn,na U nn,nn
    stmt = """select tab2_nn, tab3_na
from tab2 left join tab3 on tab2_nn = tab3_na
union
select tab2_nn, tab3_nn
from tab3 left join tab2 on tab2_nn = tab3_nn
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s616')
    
    #  nn,na U nn,na
    stmt = """select tab2_nn, tab3_na
from tab2 left join tab3 on tab2_nn = tab3_na
union
select tab2_nn, tab3_na
from tab3 left join tab2 on tab2_nn = tab3_na
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s617')
    
    #  nn,na U na,nn
    stmt = """select tab2_nn, tab3_na
from tab2 left join tab3 on tab2_nn = tab3_na
union
select tab2_na, tab3_nn
from tab3 left join tab2 on tab2_na = tab3_nn
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s618')
    
    #  nn,na U na,na
    stmt = """select tab2_nn, tab3_na
from tab2 left join tab3 on tab2_nn = tab3_na
union
select tab2_na, tab3_na
from tab3 left join tab2 on tab2_na = tab3_na
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s619')
    
    #  na,nn U nn,nn
    stmt = """select tab2_na, tab3_nn
from tab2 left join tab3 on tab2_na = tab3_nn
union
select tab2_nn, tab3_nn
from tab3 left join tab2 on tab2_nn = tab3_nn
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s620')
    
    #  na,nn U nn,na
    stmt = """select tab2_na, tab3_nn
from tab2 left join tab3 on tab2_na = tab3_nn
union
select tab2_nn, tab3_na
from tab3 left join tab2 on tab2_nn = tab3_na
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s621')
    
    #  na,nn U na,nn
    stmt = """select tab2_na, tab3_nn
from tab2 left join tab3 on tab2_na = tab3_nn
union
select tab2_na, tab3_nn
from tab3 left join tab2 on tab2_na = tab3_nn
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s622')
    
    #  na,nn U na,na
    stmt = """select tab2_na, tab3_nn
from tab2 left join tab3 on tab2_na = tab3_nn
union
select tab2_na, tab3_na
from tab3 left join tab2 on tab2_na = tab3_na
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s623')
    
    #  na,na U nn,nn
    stmt = """select tab2_na, tab3_na
from tab2 left join tab3 on tab2_na = tab3_na
union
select tab2_nn, tab3_nn
from tab3 left join tab2 on tab2_nn = tab3_nn
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s624')
    
    #  na,na U nn,na
    stmt = """select tab2_na, tab3_na
from tab2 left join tab3 on tab2_na = tab3_na
union
select tab2_nn, tab3_na
from tab3 left join tab2 on tab2_nn = tab3_na
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s625')
    
    #  na,na U na,nn
    stmt = """select tab2_na, tab3_na
from tab2 left join tab3 on tab2_na = tab3_na
union
select tab2_na, tab3_nn
from tab3 left join tab2 on tab2_na = tab3_nn
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s626')
    
    #  na,na U na,na
    stmt = """select tab2_na, tab3_na
from tab2 left join tab3 on tab2_na = tab3_na
union
select tab2_na, tab3_na
from tab3 left join tab2 on tab2_na = tab3_na
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s627')
    
    # Insert Selects using Outer Joins and Unions
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    
    #  Error case should be rejected by the Binder
    stmt = """insert into zztemp 
select tab3_nn, tab3_na                -- nullable column should be rejected
from tab3 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8421')
    
    #  Error case should be rejected by the Binder
    stmt = """insert into zztemp 
select tab3_nn, sum(tab3_na)           -- expression containing nullable col
from tab3 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4021')
    
    #  Error case should be rejected by the Binder
    stmt = """insert into zztemp 
select tab3_nn, -tab3_na               -- unary arith op
from tab3 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8421')
    
    #  Error case should be rejected by the Binder
    stmt = """insert into zztemp 
select tab3_nn, tab3_na + 5            -- bi arith op
from tab3 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8421')
    
    #  Error case should be rejected by the Binder
    stmt = """insert into zztemp 
select tab2_nn, tab3_nn                -- tab2_nn col from inner table
from tab3 left join tab2 on tab2_nn = tab3_nn
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8421')
    
    #  Error case should be rejected by the Binder
    stmt = """insert into zztemp 
select -tab2_nn, tab3_nn                    -- un arith op
from tab3 left join tab2 on tab2_nn = tab3_nn
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8421')
    
    #  Error case should be rejected by the Binder
    stmt = """insert into zztemp 
select tab2_nn + 5, tab3_nn                 -- bi arith op
from tab3 left join tab2 on tab2_nn = tab3_nn
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8421')
    
    #  Error case should be rejected by the Binder
    stmt = """insert into zztemp 
select sum (tab2_nn), tab3_nn               -- aggregate function
from tab3 left join tab2 on tab2_nn = tab3_nn
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4021')
    
    #  Error case should be rejected by the Binder
    stmt = """insert into zztemp 
select tab2_nn, tab3_nn
from tab2 left join tab3 on tab2_nn = tab3_nn
union all
select tab2_nn, tab3_nn
from tab3 left join tab2 on tab2_nn = tab3_nn
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8421')
    
    #  Error case should be rejected by the Binder
    stmt = """insert into zztemp 
select tab2_nn, tab3_nn
from tab2 left join tab3 on tab2_nn = tab3_nn
union
select tab2_nn, tab3_nn
from tab3 left join tab2 on tab2_nn = tab3_nn
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8421')
    
    stmt = """insert into zztemp2 
select tab2_nn, tab3_nn
from tab3 left join tab2 on tab2_nn = tab3_nn
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)
    
    stmt = """insert into zztemp2 
select tab2_nn, tab3_nn
from tab2 left join tab3 on tab2_nn = tab3_nn
union all
select tab2_nn, tab3_nn
from tab3 left join tab2 on tab2_nn = tab3_nn
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 7)
    
    stmt = """insert into zztemp2 
select tab2_nn, tab3_nn
from tab2 left join tab3 on tab2_nn = tab3_nn
union
select tab2_nn, tab3_nn
from tab3 left join tab2 on tab2_nn = tab3_nn
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    
    # OBJECTIVE : To verify that upto 16 tables may participate in an outer join
    # =========   (and that 17 tables cannot)
    # NW02) 1 outer join, 2 tables
    # Join order should be (T1,T2)
    
    stmt = """prepare p1 from
select  *
from oj1 T1 left join oj2 T2  on T1.a = T2.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (NULL, 'P1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select  *
from oj1 T1 left join oj2 T2  on T1.a = T2.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s639')
    
    # NW03) 2 outer joins, 3 tables
    # Join order should be (T1,T2,T3)
    
    stmt = """prepare p2 from
select  *
from oj1 T1 left join oj2 T2  on T1.a = T2.b
left join oj2 T3  on T2.b = T3.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (NULL, 'P2'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select  *
from oj1 T1 left join oj2 T2  on T1.a = T2.b
left join oj2 T3  on T2.b = T3.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s641')
    
    # NW04) 3 outer joins, 4 tables
    # Join order should be (T1,T2,T3,T4)
    
    stmt = """prepare p3 from
select *  from oj1 T1 left join oj2 T2  on T1.a = T2.b
left join oj2 T3  on T2.b = T3.b
left join oj2 T4  on T3.b = T4.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (NULL, 'P3'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select  *
from oj1 T1 left join oj2 T2  on T1.a = T2.b
left join oj2 T3  on T2.b = T3.b
left join oj2 T4  on T3.b = T4.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s643')
    
    # NW05) 4 outer joins, 5 tables
    # Join order should be (T1,T2,T3,T4,T5)
    
    stmt = """prepare p4 from
select * from oj1 T1 left join oj2 T2  on T1.a = T2.b
left join oj2 T3  on T2.b = T3.b
left join oj2 T4  on T3.b = T4.b
left join oj2 T5  on T4.b = T5.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (NULL, 'P4'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select  *
from oj1 T1 left join oj2 T2  on T1.a = T2.b
left join oj2 T3  on T2.b = T3.b
left join oj2 T4  on T3.b = T4.b
left join oj2 T5  on T4.b = T5.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s645')
    
    # NW06) 5 outer joins, 6 tables
    # Join order should be (T1,T2,T3,T4,T5,T6)
    
    stmt = """prepare p5 from
select * from oj1 T1 left join oj2 T2  on T1.a = T2.b
left join oj2 T3  on T2.b = T3.b
left join oj2 T4  on T3.b = T4.b
left join oj2 T5  on T4.b = T5.b
left join oj2 T6  on T5.b = T6.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (NULL, 'P5'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select  *
from oj1 T1 left join oj2 T2  on T1.a = T2.b
left join oj2 T3  on T2.b = T3.b
left join oj2 T4  on T3.b = T4.b
left join oj2 T5  on T4.b = T5.b
left join oj2 T6  on T5.b = T6.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s647')
    
    # NW07) 6 outer joins, 7 tables
    # Join order should be (T1,T2,T3,T4,T5,T6,T7)
    
    stmt = """prepare p6 from
select * from oj1 T1 left join oj2 T2  on T1.a = T2.b
left join oj2 T3  on T2.b = T3.b
left join oj2 T4  on T3.b = T4.b
left join oj2 T5  on T4.b = T5.b
left join oj2 T6  on T5.b = T6.b
left join oj2 T7  on T6.b = T7.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (NULL, 'P6'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select  *
from oj1 T1 left join oj2 T2  on T1.a = T2.b
left join oj2 T3  on T2.b = T3.b
left join oj2 T4  on T3.b = T4.b
left join oj2 T5  on T4.b = T5.b
left join oj2 T6  on T5.b = T6.b
left join oj2 T7  on T6.b = T7.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s649')
    
    # NW08) 7 outer joins, 8 tables
    # Join order should be (T1,T2,T3,T4,T5,T6,T7,T8)
    stmt = """prepare p7 from
select  *
from oj1 T1 left join oj2 T2  on T1.a = T2.b
left join oj2 T3  on T2.b = T3.b
left join oj2 T4  on T3.b = T4.b
left join oj2 T5  on T4.b = T5.b
left join oj2 T6  on T5.b = T6.b
left join oj2 T7  on T6.b = T7.b
left join oj2 T8  on T7.b = T8.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (NULL, 'P7'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select  *
from oj1 T1 left join oj2 T2  on T1.a = T2.b
left join oj2 T3  on T2.b = T3.b
left join oj2 T4  on T3.b = T4.b
left join oj2 T5  on T4.b = T5.b
left join oj2 T6  on T5.b = T6.b
left join oj2 T7  on T6.b = T7.b
left join oj2 T8  on T7.b = T8.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s651')
    
    # NW09) 8 outer joins, 9 tables
    # Join order should be (T1,T2,T3,T4,T5,T6,T7,T8,T9)
    stmt = """prepare p8 from
select * from oj1 T1 left join oj2 T2  on T1.a = T2.b
left join oj2 T3  on T2.b = T3.b
left join oj2 T4  on T3.b = T4.b
left join oj2 T5  on T4.b = T5.b
left join oj2 T6  on T5.b = T6.b
left join oj2 T7  on T6.b = T7.b
left join oj2 T8  on T7.b = T8.b
left join oj2 T9  on T8.b = T9.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (NULL, 'P8'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select  *
from oj1 T1 left join oj2 T2  on T1.a = T2.b
left join oj2 T3  on T2.b = T3.b
left join oj2 T4  on T3.b = T4.b
left join oj2 T5  on T4.b = T5.b
left join oj2 T6  on T5.b = T6.b
left join oj2 T7  on T6.b = T7.b
left join oj2 T8  on T7.b = T8.b
left join oj2 T9  on T8.b = T9.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s653')
    
    # NW10) 9 outer joins, 10 tables
    # Join order should be (T1,T2,T3,T4,T5,T6,T7,T8,T9,T10)
    stmt = """prepare p9 from
select * from oj1 T1 left join oj2 T2  on T1.a = T2.b
left join oj2 T3  on T2.b = T3.b
left join oj2 T4  on T3.b = T4.b
left join oj2 T5  on T4.b = T5.b
left join oj2 T6  on T5.b = T6.b
left join oj2 T7  on T6.b = T7.b
left join oj2 T8  on T7.b = T8.b
left join oj2 T9  on T8.b = T9.b
left join oj2 T10 on T10.b = T9.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (NULL, 'P9'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select  *
from oj1 T1 left join oj2 T2  on T1.a = T2.b
left join oj2 T3  on T2.b = T3.b
left join oj2 T4  on T3.b = T4.b
left join oj2 T5  on T4.b = T5.b
left join oj2 T6  on T5.b = T6.b
left join oj2 T7  on T6.b = T7.b
left join oj2 T8  on T7.b = T8.b
left join oj2 T9  on T8.b = T9.b
left join oj2 T10 on T10.b = T9.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s655')
    
    # NW11) 10 outer joins, 11 tables
    # Join order should be (T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11)
    stmt = """prepare p10 from
select * from oj1 T1 left join oj2 T2  on T1.a = T2.b
left join oj2 T3  on T2.b = T3.b
left join oj2 T4  on T3.b = T4.b
left join oj2 T5  on T4.b = T5.b
left join oj2 T6  on T5.b = T6.b
left join oj2 T7  on T6.b = T7.b
left join oj2 T8  on T7.b = T8.b
left join oj2 T9  on T8.b = T9.b
left join oj2 T10 on T10.b = T9.b
left join oj2 T11 on T11.b = T10.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (NULL, 'P10'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select  *
from oj1 T1 left join oj2 T2  on T1.a = T2.b
left join oj2 T3  on T2.b = T3.b
left join oj2 T4  on T3.b = T4.b
left join oj2 T5  on T4.b = T5.b
left join oj2 T6  on T5.b = T6.b
left join oj2 T7  on T6.b = T7.b
left join oj2 T8  on T7.b = T8.b
left join oj2 T9  on T8.b = T9.b
left join oj2 T10 on T10.b = T9.b
left join oj2 T11 on T11.b = T10.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s657')
    
    # NW12) 11 outer joins 12 tables
    # Join order should be (T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12)
    stmt = """prepare p11 from
select * from oj1 T1 left join oj2 T2  on T1.a = T2.b
left join oj2 T3  on T2.b = T3.b
left join oj2 T4  on T3.b = T4.b
left join oj2 T5  on T4.b = T5.b
left join oj2 T6  on T5.b = T6.b
left join oj2 T7  on T6.b = T7.b
left join oj2 T8  on T7.b = T8.b
left join oj2 T9  on T8.b = T9.b
left join oj2 T10 on T10.b = T9.b
left join oj2 T11 on T11.b = T10.b
left join oj2 T12 on T12.b = T11.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (NULL, 'P11'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select  *
from oj1 T1 left join oj2 T2  on T1.a = T2.b
left join oj2 T3  on T2.b = T3.b
left join oj2 T4  on T3.b = T4.b
left join oj2 T5  on T4.b = T5.b
left join oj2 T6  on T5.b = T6.b
left join oj2 T7  on T6.b = T7.b
left join oj2 T8  on T7.b = T8.b
left join oj2 T9  on T8.b = T9.b
left join oj2 T10 on T10.b = T9.b
left join oj2 T11 on T11.b = T10.b
left join oj2 T12 on T12.b = T11.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s659')
    
    # NW13) 12 outer joins, 13 tables
    # Join order should be (T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13)
    stmt = """prepare p12 from
select * from oj1 T1 left join oj2 T2  on T1.a = T2.b
left join oj2 T3  on T2.b = T3.b
left join oj2 T4  on T3.b = T4.b
left join oj2 T5  on T4.b = T5.b
left join oj2 T6  on T5.b = T6.b
left join oj2 T7  on T6.b = T7.b
left join oj2 T8  on T7.b = T8.b
left join oj2 T9  on T8.b = T9.b
left join oj2 T10 on T10.b = T9.b
left join oj2 T11 on T11.b = T10.b
left join oj2 T12 on T12.b = T11.b
left join oj2 T13 on T13.b = T12.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (NULL, 'P12'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select  *
from oj1 T1 left join oj2 T2  on T1.a = T2.b
left join oj2 T3  on T2.b = T3.b
left join oj2 T4  on T3.b = T4.b
left join oj2 T5  on T4.b = T5.b
left join oj2 T6  on T5.b = T6.b
left join oj2 T7  on T6.b = T7.b
left join oj2 T8  on T7.b = T8.b
left join oj2 T9  on T8.b = T9.b
left join oj2 T10 on T10.b = T9.b
left join oj2 T11 on T11.b = T10.b
left join oj2 T12 on T12.b = T11.b
left join oj2 T13 on T13.b = T12.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s661')
    
    # NW14) 13 outer joins, 14 tables
    # Join order should be (T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14)
    stmt = """prepare p13 from
select * from oj1 T1 left join oj2 T2  on T1.a = T2.b
left join oj2 T3  on T2.b = T3.b
left join oj2 T4  on T3.b = T4.b
left join oj2 T5  on T4.b = T5.b
left join oj2 T6  on T5.b = T6.b
left join oj2 T7  on T6.b = T7.b
left join oj2 T8  on T7.b = T8.b
left join oj2 T9  on T8.b = T9.b
left join oj2 T10 on T10.b = T9.b
left join oj2 T11 on T11.b = T10.b
left join oj2 T12 on T12.b = T11.b
left join oj2 T13 on T13.b = T12.b
left join oj2 T14 on T14.b = T13.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (NULL, 'P13'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select  *
from oj1 T1 left join oj2 T2  on T1.a = T2.b
left join oj2 T3  on T2.b = T3.b
left join oj2 T4  on T3.b = T4.b
left join oj2 T5  on T4.b = T5.b
left join oj2 T6  on T5.b = T6.b
left join oj2 T7  on T6.b = T7.b
left join oj2 T8  on T7.b = T8.b
left join oj2 T9  on T8.b = T9.b
left join oj2 T10 on T10.b = T9.b
left join oj2 T11 on T11.b = T10.b
left join oj2 T12 on T12.b = T11.b
left join oj2 T13 on T13.b = T12.b
left join oj2 T14 on T14.b = T13.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s663')
    
    # NW15) 14 outer joins, 15 tables
    # Join order should be (T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15)
    stmt = """prepare p14 from
select * from oj1 T1 left join oj2 T2  on T1.a = T2.b
left join oj2 T3  on T2.b = T3.b
left join oj2 T4  on T3.b = T4.b
left join oj2 T5  on T4.b = T5.b
left join oj2 T6  on T5.b = T6.b
left join oj2 T7  on T6.b = T7.b
left join oj2 T8  on T7.b = T8.b
left join oj2 T9  on T8.b = T9.b
left join oj2 T10 on T10.b = T9.b
left join oj2 T11 on T11.b = T10.b
left join oj2 T12 on T12.b = T11.b
left join oj2 T13 on T13.b = T12.b
left join oj2 T14 on T14.b = T13.b
left join oj2 T15 on T15.b = T14.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (NULL, 'P14'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select  *
from oj1 T1 left join oj2 T2  on T1.a = T2.b
left join oj2 T3  on T2.b = T3.b
left join oj2 T4  on T3.b = T4.b
left join oj2 T5  on T4.b = T5.b
left join oj2 T6  on T5.b = T6.b
left join oj2 T7  on T6.b = T7.b
left join oj2 T8  on T7.b = T8.b
left join oj2 T9  on T8.b = T9.b
left join oj2 T10 on T10.b = T9.b
left join oj2 T11 on T11.b = T10.b
left join oj2 T12 on T12.b = T11.b
left join oj2 T13 on T13.b = T12.b
left join oj2 T14 on T14.b = T13.b
left join oj2 T15 on T15.b = T14.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s665')
    
    # NW16) 15 outer joins, 16 tables
    # Join order should be (T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16
    stmt = """prepare p15 from
select * from oj1 T1 left join oj2 T2  on T1.a = T2.b
left join oj2 T3  on T2.b = T3.b
left join oj2 T4  on T3.b = T4.b
left join oj2 T5  on T4.b = T5.b
left join oj2 T6  on T5.b = T6.b
left join oj2 T7  on T6.b = T7.b
left join oj2 T8  on T7.b = T8.b
left join oj2 T9  on T8.b = T9.b
left join oj2 T10 on T10.b = T9.b
left join oj2 T11 on T11.b = T10.b
left join oj2 T12 on T12.b = T11.b
left join oj2 T13 on T13.b = T12.b
left join oj2 T14 on T14.b = T13.b
left join oj2 T15 on T15.b = T14.b
left join oj2 T16 on T16.b = T15.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (NULL, 'P15'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select  *
from oj1 T1 left join oj2 T2  on T1.a = T2.b
left join oj2 T3  on T2.b = T3.b
left join oj2 T4  on T3.b = T4.b
left join oj2 T5  on T4.b = T5.b
left join oj2 T6  on T5.b = T6.b
left join oj2 T7  on T6.b = T7.b
left join oj2 T8  on T7.b = T8.b
left join oj2 T9  on T8.b = T9.b
left join oj2 T10 on T10.b = T9.b
left join oj2 T11 on T11.b = T10.b
left join oj2 T12 on T12.b = T11.b
left join oj2 T13 on T13.b = T12.b
left join oj2 T14 on T14.b = T13.b
left join oj2 T15 on T15.b = T14.b
left join oj2 T16 on T16.b = T15.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s667')
    
    #  NW17) Error Case : 17 tables
    stmt = """select  *
from oj1 T1 left join oj2 T2  on T1.a = T2.b
left join oj2 T3  on T2.b = T3.b
left join oj2 T4  on T3.b = T4.b
left join oj2 T5  on T4.b = T5.b
left join oj2 T6  on T5.b = T6.b
left join oj2 T7  on T6.b = T7.b
left join oj2 T8  on T7.b = T8.b
left join oj2 T9  on T8.b = T9.b
left join oj2 T10 on T10.b = T9.b
left join oj2 T11 on T11.b = T10.b
left join oj2 T12 on T12.b = T11.b
left join oj2 T13 on T13.b = T12.b
left join oj2 T14 on T14.b = T13.b
left join oj2 T15 on T15.b = T14.b
left join oj2 T16 on T16.b = T15.b
left join oj2 T17 on T17.b = T16.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s668')
    
    # OBJECTIVE : To verify that the outer join order is not influenced
    # =========   by an extraneous inner join
    # OJIJ01) Inner join of (outer join, inner join)
    stmt = """prepare p16 from
select *
from oj1 T1 left join oj2 T2 on T1.a = T2.b, oj1 T3
where T3.a = T1.a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (NULL, 'P16'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select *
from oj1 T1 left join oj2 T2 on T1.a = T2.b, oj1 T3
where T3.a = T1.a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s670')
    
    # OJIJ02) Inner join of (outer join, inner join)
    stmt = """prepare p17 from
select *
from oj1 T1 left join oj2 T2 on T1.a = T2.b, oj1 T3
where T3.a = T2.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (NULL, 'P17'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select *
from oj1 T1 left join oj2 T2 on T1.a = T2.b, oj1 T3
where T3.a = T2.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s672')
    
    # OJIJ03) Inner join of (outer join, inner join)
    stmt = """prepare p18 from
select *
from oj1 T1, oj1 T2 left join oj2 T3 on T2.a = T3.b
where T1.a = T2.a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (NULL, 'P18'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select *
from oj1 T1, oj1 T2 left join oj2 T3 on T2.a = T3.b
where T1.a = T2.a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s674')
    
    # OJIJ04) Inner join of (outer join, inner join)
    stmt = """prepare p19 from
select *
from oj1 T1, oj1 T2 left join oj2 T3 on T2.a = T3.b
where T1.a = T3.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (NULL, 'P19'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select *
from oj1 T1, oj1 T2 left join oj2 T3 on T2.a = T3.b
where T1.a = T3.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s676')
    
    # OBJECTIVE : To verify that an inner join of outer joins is performed
    # =========   without disrupting any particpant outer join order
    # OJOJ01) X prod
    stmt = """prepare p20 from
select * from oj1 T1 left join oj2 T2 on T1.a = T2.b
, oj2 T3 left join oj1 T4 on T3.b = T4.a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (NULL, 'P20'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select *
from oj1 T1 left join oj2 T2 on T1.a = T2.b
, oj2 T3 left join oj1 T4 on T3.b = T4.a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s678')
    
    # OJOJ02) Inner join on T1, T2
    stmt = """prepare p21 from
select * from oj1 T1 left join oj2 T2 on T1.a = T2.b
, oj2 T3 left join oj1 T4 on T3.b = T4.a
where T1.a = T2.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select *
from oj1 T1 left join oj2 T2 on T1.a = T2.b
, oj2 T3 left join oj1 T4 on T3.b = T4.a
where T1.a = T2.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s679')
    
    # OJOJ03) Inner join on T1, T3
    stmt = """prepare p22 from
select * from oj1 T1 left join oj2 T2 on T1.a = T2.b
, oj2 T3 left join oj1 T4 on T3.b = T4.a
where T1.a = T3.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select *
from oj1 T1 left join oj2 T2 on T1.a = T2.b
, oj2 T3 left join oj1 T4 on T3.b = T4.a
where T1.a = T3.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s680')
    
    # OJOJ04) Inner join on T1, T4
    stmt = """prepare p23 from
select * from oj1 T1 left join oj2 T2 on T1.a = T2.b
, oj2 T3 left join oj1 T4 on T3.b = T4.a
where T1.a = T4.a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (NULL, 'P23'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select *
from oj1 T1 left join oj2 T2 on T1.a = T2.b
, oj2 T3 left join oj1 T4 on T3.b = T4.a
where T1.a = T4.a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s682')
    
    # OJOJ05) Inner join on T2, T3
    stmt = """prepare p24 from
select * from oj1 T1 left join oj2 T2 on T1.a = T2.b
, oj2 T3 left join oj1 T4 on T3.b = T4.a
where T2.b = T3.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select *
from oj1 T1 left join oj2 T2 on T1.a = T2.b
, oj2 T3 left join oj1 T4 on T3.b = T4.a
where T2.b = T3.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s683')
    
    # OJOJ06) Inner join on T2, T4
    stmt = """prepare p25 from
select * from oj1 T1 left join oj2 T2 on T1.a = T2.b
, oj2 T3 left join oj1 T4 on T3.b = T4.a
where T2.b = T4.a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (NULL, 'P25'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select *
from oj1 T1 left join oj2 T2 on T1.a = T2.b
, oj2 T3 left join oj1 T4 on T3.b = T4.a
where T2.b = T4.a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s685')
    
    # OBJECTIVE : To verify that a view containing inner or outer joins
    # =========   can only appear on the left side of a left join but
    #             never in any right subtree of a left join.
    
    #OJVU01) V1 LJ T1
    stmt = """prepare p26 from
select *
from v1 left join tab1 
on a = tab1_pk
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (NULL, 'P25'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select *
from v1 left join tab1 
on a = tab1_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s687')
    
    # OJVU02) T1 LJ V1 - Error case
    
    stmt = """select *
from tab1 left join v1 
on a = tab1_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s688')
    
    #OJVU03) V2 LJ T1
    stmt = """prepare p26 from
select *
from v2 left join tab1 
on a = tab1_pk
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (NULL, 'P26'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select *
from v2 left join tab1 
on a = tab1_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s690')
    
    # OJVU04) T1 LJ V2 - Error case
    
    stmt = """select *
from tab1 left join v2 
on a = tab1_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s691')
    
    #OJVU05) V3 LJ T1
    stmt = """prepare p27 from
select *
from v3 left join tab1 
on a = tab1_pk
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (NULL, 'P27'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select *
from v3 left join tab1 
on a = tab1_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s693')
    
    # OJVU06) T1 LJ V3 - Error case
    
    stmt = """select *
from tab1 left join v3 
on a = tab1_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s694')
    
    # OJVU07) V1 IJ V2
    
    stmt = """select *
from v1 inner join v2 
on v1.a = v2.a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s695')
    
    # OJVU08) V1 LJ V2 - Error Case
    
    stmt = """select *
from v1 left join v2 
on v1.a = v2.a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s696')
    
    # OJVU09) V2 LJ V1 - Error Case
    
    stmt = """select *
from v2 left join v1 
on v1.a = v2.a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s697')
    
    # OJVU10) V3 LJ V1 - Error Case
    
    stmt = """select *
from v3 left join v1 
on v1.a = v3.a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s698')
    
    # OJVU11) V1 LJ V3 - Error Case
    
    stmt = """select *
from v1 left join v3 
on v1.a = v3.a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s699')
    
    # OJVU12) V3 LJ V2 - Error Case
    
    stmt = """select *
from v3 left join v2 
on v2.a = v3.a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s700')
    
    # OJVU13) V2 LJ V3 - Error Case
    
    stmt = """select *
from v2 left join v3 
on v2.a = v3.a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s701')
    
    #OJVU14) V3 IJ V1
    stmt = """prepare p28 from
select *
from v3 inner join v1 
on v1.a = v3.a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (NULL, 'P28'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select *
from v3 inner join v1 
on v1.a = v3.a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s703')
    
    #OJVU5) V2 IJ V3
    stmt = """prepare p29 from
select *
from v1 inner join v3 
on v1.a = v3.a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (NULL, 'P29'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select *
from v1 inner join v3 
on v1.a = v3.a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s705')
    
    stmt = """select seq_num, operator, total_cost
from table (explain ('BLUE01.MXD1000.TESTA13M', 'P29'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (BLUE01.MXD1000.TESTA13M, 'P29'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (,'P29'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select seq_num, operator, total_cost
from table (explain ('P29'));"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

