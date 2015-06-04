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
    
def test001(desc="""A01"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A01
    #  Description:        DUP indexed table; and access via index.
    #
    #  Purpose:            Sets up data base for case A1, which reports
    #                      on initialization errors.
    #  Test case inputs:    pretstA01
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    #  Revision History:
    #      07/ 1/96       Converted from MP test library sqlt026:TESTS:A0
    # =================== End Test Case Header  ===================
    
    #set mploc ${w_catalog};
    #set nametype NSK;
    
    stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    #  Create table ;
    stmt = """create table btsel123 (
pic_comp_2             pic sv9(2) comp default 0 not null
, data_93                pic 9(3)        default 0 not null
, primary key (data_93)
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  Simple index:
    
    stmt = """create index btseli1 on btsel123 ( pic_comp_2 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # ---------------------------
    # INSERTS to populate table:
    # ---------------------------
    
    stmt = """insert into btsel123 values (0.12,441);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel123 values (-0.25,442);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel123 values (0.13,443);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel123 values (0.14,444);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel123 values (0.15,445);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel123 values (0.16,446);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel123 values (0.17,447);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into btsel123 values (0.18,448);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Select * from btsel123 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a1exp""", 'a1s1')
    
    stmt = """update statistics for table btsel123 on every column;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table tb1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """Create table tb1 (b int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into tb1 values (2), (4), (6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)
    
    stmt = """select * from tb1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    stmt = """select b, runningmax(b), movingmax(b, 100)
from ((values(2), (4), (6))) as T (b) sequence by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a1exp""", 'a1s2')
    
    stmt = """select b, runningmax(b), movingmax(b,-5)
from ((values(2), (4), (6))) as T (b) sequence by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a1exp""", 'a1s3')
    
    stmt = """create table ht (h10s4 interval hour(10) to second(4)) no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into ht values (-interval '1111111111:12:00.1234'hour(10) to second(4));"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into ht values (interval '1111111111:12:00.1234'hour(10) to second(4));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update ht set h10s4 = h10s4  * 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    _testmgr.testcase_end(desc)

def test002(desc="""A02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A02
    #  Description:        access via index.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #  Revision History:
    #      07/ 1/96       Converted from MP test library sqlt026:TESTS:
    # =================== End Test Case Header  ===================
    #set mploc ${w_catalog};
    #set nametype NSK;
    
    #  Create table ;
    
    stmt = """create table bt23c2 (
pic_comp_2             pic sv9(2) comp default 0 not null
, data_93                pic 9(3)        default 0 not null
, primary key (data_93)
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  Simple index:
    
    stmt = """create index bt23c2a on bt23c2 ( pic_comp_2 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # ---------------------------
    # INSERTS to populate table:
    # ---------------------------
    
    stmt = """insert into bt23c2 values (0.12,441);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into bt23c2 values (-0.25,442);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into bt23c2 values (0.13,443);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into bt23c2 values (0.14,444);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into bt23c2 values (0.15,445);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into bt23c2 values (0.16,446);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into bt23c2 values (0.17,447);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into bt23c2 values (0.18,448);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Select * from bt23c2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a2exp""", 'a2s1')
    
    stmt = """update histogram statistics for table bt23c2;"""
    output = _dci.cmdexec(stmt)
    
    # ----------------------------
    # SELECT and Update:
    # ----------------------------
    
    stmt = """select * from bt23c2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a2exp""", 'a2s2')
    
    stmt = """select * from bt23c2 where pic_comp_2 <0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a2exp""", 'a2s3')
    
    stmt = """update bt23c2 set pic_comp_2 = .01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 8)
    
    stmt = """select * from bt23c2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a2exp""", 'a2s4')
    
    stmt = """drop index bt23c2a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop index btseli1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table bt23c2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table btsel123;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

