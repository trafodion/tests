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

# A01 ALTER RENAME TABLE HAVING INDEX AND MANY PARTITIONS

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""ALTER RENAME TABLE HAVING INDEX AND MANY PARTITIONS"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """control query default POS 'MULTI_NODE';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """control query defaUlt POS_NUM_OF_PARTNS '136';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table table_136p_01
(
sbin0_10            Numeric(18) signed    not null,
char0_2             Character(8)          not null,
udec0_uniq          Decimal(9) unsigned   not null,
ubin0_uniq          PIC 9(9) COMP         not null,
sdec0_500           PIC S9(9)             not null,
varchar0_10         varchar(16)      not null,
varchar1_20         varchar(8)       not null,
sbin1_5000          Numeric(4) signed     not null,
sdec1_4             Decimal(18) signed    not null,
char1_4             Character(8)          not null,
constraint p_key_lrg_01 primary key ( udec0_uniq  ASC ) not droppable,
constraint tlo_con_01 unique (udec0_uniq, sbin1_5000) droppable
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table table_136p_02
(
sbin0_10            Numeric(18) signed    not null,
char0_2             Character(8)          not null,
udec0_uniq          Decimal(9) unsigned   not null,
ubin0_uniq          PIC 9(9) COMP         not null,
sdec0_500           PIC S9(9)             not null,
varchar0_10         varchar(16)      not null,
varchar1_20         varchar(8)       not null,
sbin1_5000          Numeric(4) signed     not null,
sdec1_4             Decimal(18) signed    not null,
char1_4             Character(8)          not null,
constraint p_key_lrg_02 primary key ( udec0_uniq  ASC ) not droppable,
constraint tlo_con_02 unique (udec0_uniq, sbin1_5000) droppable
)
;"""
    output = _dci.cmdexec(stmt)
    stmt = """create unique index idx01_136p_02 on table_136p_02 (udec0_uniq);"""
    output = _dci.cmdexec(stmt)
    stmt = """create unique index idx02_136p_02 on table_136p_02 (ubin0_uniq);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """showlabel table_136p_01, detail;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_any_substr(output, '136 partition[s]')
    stmt = """showlabel table_136p_02, detail;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_any_substr(output, '136 partition[s]')
    
    stmt = """alter table table_136p_01 rename to table_136p_01_new;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """alter table table_136p_02 rename to table_136p_02_new;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from table_136p_01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    stmt = """select * from table_136p_02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    stmt = """select * from table_136p_01_new;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    stmt = """select * from table_136p_02_new;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """alter table table_136p_01_new rename to table_136p_01_new2 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """alter table table_136p_02_new rename to table_136p_02_new2 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from table_136p_01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    stmt = """select * from table_136p_02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    stmt = """select * from table_136p_01_new;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    stmt = """select * from table_136p_02_new;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    stmt = """select * from table_136p_01_new2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    stmt = """select * from table_136p_02_new2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

