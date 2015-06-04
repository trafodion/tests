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

import rename21_ddl
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
    
    stmt = """set nametype ansi;"""
    output = _dci.cmdexec(stmt)
    
    rename21_ddl._init(_testmgr)
    
    stmt = """insert into tab_ten_original_03 values (1,'ABCDEFGH',1001,1001,11,'IJKLMNOPQRSTUVWX','YZABCDEF',1001,11,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab_ten_original_03 values (2,'ABCDEFGH',1002,1002,12,'IJKLMNOPQRSTUVWX','YZABCDEF',1002,12,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab_ten_original_03 values (3,'ABCDEFGH',1003,1003,13,'IJKLMNOPQRSTUVWX','YZABCDEF',1003,13,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab_ten_original_03 values (4,'ABCDEFGH',1004,1004,14,'IJKLMNOPQRSTUVWX','YZABCDEF',1004,14,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab_ten_original_03 values (5,'ABCDEFGH',1005,1005,15,'IJKLMNOPQRSTUVWX','YZABCDEF',1005,15,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab_ten_original_03 values (6,'ABCDEFGH',1006,1006,16,'IJKLMNOPQRSTUVWX','YZABCDEF',1006,16,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab_ten_original_03 values (7,'ABCDEFGH',1007,1007,17,'IJKLMNOPQRSTUVWX','YZABCDEF',1007,17,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab_ten_original_03 values (8,'ABCDEFGH',1008,1008,18,'IJKLMNOPQRSTUVWX','YZABCDEF',1008,18,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab_ten_original_03 values (9,'ABCDEFGH',1009,1009,19,'IJKLMNOPQRSTUVWX','YZABCDEF',1009,19,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab_ten_original_03 values (10,'ABCDEFGH',1010,1010,20,'IJKLMNOPQRSTUVWX','YZABCDEF',1010,20,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into tab_ten_original_04 values (1,'ABCDEFGH',1001,1001,11,'IJKLMNOPQRSTUVWX','YZABCDEF',1001,11,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab_ten_original_04 values (2,'ABCDEFGH',1002,1002,12,'IJKLMNOPQRSTUVWX','YZABCDEF',1002,12,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab_ten_original_04 values (3,'ABCDEFGH',1003,1003,13,'IJKLMNOPQRSTUVWX','YZABCDEF',1003,13,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab_ten_original_04 values (4,'ABCDEFGH',1004,1004,14,'IJKLMNOPQRSTUVWX','YZABCDEF',1004,14,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab_ten_original_04 values (5,'ABCDEFGH',1005,1005,15,'IJKLMNOPQRSTUVWX','YZABCDEF',1005,15,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab_ten_original_04 values (6,'ABCDEFGH',1006,1006,16,'IJKLMNOPQRSTUVWX','YZABCDEF',1006,16,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab_ten_original_04 values (7,'ABCDEFGH',1007,1007,17,'IJKLMNOPQRSTUVWX','YZABCDEF',1007,17,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab_ten_original_04 values (8,'ABCDEFGH',1008,1008,18,'IJKLMNOPQRSTUVWX','YZABCDEF',1008,18,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab_ten_original_04 values (9,'ABCDEFGH',1009,1009,19,'IJKLMNOPQRSTUVWX','YZABCDEF',1009,19,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab_ten_original_04 values (10,'ABCDEFGH',1010,1010,20,'IJKLMNOPQRSTUVWX','YZABCDEF',1010,20,'GHIJKLMN');"""
    output = _dci.cmdexec(stmt)
    
    ##sh import $my_schema.tab_lrg_original_05 -I ${test_dir}/btpnl17a.dat
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.tab_lrg_original_05 select * from """ + gvars.g_schema_cmureg + """.btpnl17a;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)

    stmt = """select count(*) from tab_lrg_original_05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '2000')

    stmt = """update statistics for table tab_lrg_original_05 on every column;"""
    output = _dci.cmdexec(stmt)
    
    ##sh import $my_schema.tab_lrg_original_06 -I ${test_dir}/btpnl17a.dat
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.tab_lrg_original_06 select * from """ + gvars.g_schema_cmureg + """.btpnl17a;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)

    stmt = """select count(*) from tab_lrg_original_06;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '2000')
    
    stmt = """update statistics for table tab_lrg_original_06 on every column;"""
    output = _dci.cmdexec(stmt)
