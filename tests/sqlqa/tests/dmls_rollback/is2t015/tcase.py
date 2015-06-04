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
    
def test001(desc="""t01"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # no rollback when AUTOCOMMIT OFF
    
    stmt = """create table t15tab (
a int not null, b int, c int
)
attribute extent (1024, 1024), maxextents 512
store by (a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into t15tab values (1,10,100),(2,20,200),(3,30,300);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)
    
    stmt = """drop table t15tabA;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table t15tabA (
a int not null, b int, c int,
v1 int not null,
v2 int not null
)
attribute extent (1024, 1024), maxextents 512
store by (a, v1, v2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl t15tabA;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert with no rollback
into t15tabA (
select * from t15tab
transpose 1,2,3,4,5 as v1
transpose 10,20,30,40,50 as v2)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 75)
    
    stmt = """select count(*) from t15tabA;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, """75""")
    
    _dci = _testmgr.get_dci_proc('mymxci')
    stmt = """env;"""
    output = _dci.cmdexec(stmt)
    
    # t01.1: start a new MXCI. SET AUTOCOMMIT OFF
    stmt = """SET TRANSACTION AUTOCOMMIT OFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.2: update with no rollback
    # #expect any *3231*
    stmt = """update with no rollback
t15tabA
set b = 1,
c = 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3231')
    
    # t01.3: delete with no rollback
    stmt = """delete with no rollback
from t15tabA where a = v1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3231')
    
    stmt = """select count(*) from t15tabA;"""
    output = _dci.cmdexec(stmt)
    
    # t01.4: insert with no rollback
    stmt = """insert with no rollback into t15tabA (a,v1,v2)
values (101,102,103);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3231')
    
    # t01.5: insert with no rollback
    stmt = """insert with no rollback into t15tabA values
(102,103,104,105,106),(103,104,105,106,107);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3231')
    
    # t01.6: insert with no rollback
    stmt = """update with no rollback t15tabA set b = v1 + v2 where a < 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3231')
    
    # t01.7: delete with no rollback
    stmt = """delete with no rollback from t15tabA
where a in (select a from t15tab where a = 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3231')
    
    # this should work
    stmt = """delete from t15tabA
where a in (select a from t15tab where a = 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 25)
    
    # t01.8: without no rollback should work
    stmt = """delete from t15tabA where b = v2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 10)
    
    # t01.9:
    stmt = """select with no rollback [first 2] * from t15tabA
order by a,v1,v2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t01.10:
    stmt = """select [first 2] * from t15tabA order by a,v1,v2;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 2)
    
    # t01.11:
    stmt = """select * from t15tabA order by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t01exp""", 't01s11')
    
    stmt = """commit;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _dci = _testmgr.get_default_dci_proc()
    
    # t01.12:
    # default is AUTOCOMMIT ON
    stmt = """insert with no rollback into t15tabA values
(102,103,104,105,106),(103,104,105,106,107);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    # t01.13:
    stmt = """update with no rollback t15tabA set c = b * v1
where a = v2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3233')
    
    stmt = """update t15tabA set c = b * v1
where a = v1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 8)
    
    # t01.14:
    stmt = """delete with no rollback from t15tabA where c = b * v1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 8)
    
    # t01.15:
    stmt = """update with no rollback
t15tabA
set b = 100,
c = 100 ** 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 34)
    
    # t01.16:
    stmt = """select * from t15tabA order by 1,2,3,4,5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t01exp""", 't01s16')
    
    _testmgr.testcase_end(desc)

def test002(desc="""t02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # no rollback when AUTOCOMMIT OFF: prepare and execute
    
    stmt = """create table t02tab (
a int not null, b int, c int,
primary key(a)
)
attribute extent (1024, 1024), maxextents 512
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into t02tab values (1,10,100),(2,20,200),(3,30,300);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)
    
    # t02.1:
    stmt = """create table t02tabA (
a int not null, b int, c int,
v1 int not null,
v2 int not null
)
attribute extent (1024, 1024), maxextents 512
store by (a, v1, v2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """showddl t02tabA;"""
    output = _dci.cmdexec(stmt)
    
    # t02.2:
    stmt = """insert with no rollback
into t02tabA (
select * from t02tab
transpose 1,2,3,4,5 as v1
transpose 10,20,30,40,50 as v2)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 75)
    
    stmt = """select count(*) from t02tabA;"""
    output = _dci.cmdexec(stmt)
    
    _dci = _testmgr.get_dci_proc('mymxci')
    
    # t02.4:
    stmt = """SET TRANSACTION AUTOCOMMIT OFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t02.5: update with no rollback
    stmt = """prepare x from
update with no rollback
t02tabA
set b = 1,
c = 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3231')
    
    # t02.6: delete with no rollback
    stmt = """prepare x from
delete with no rollback
from t02tabA where a = v1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3231')
    
    stmt = """select count(*) from t02tabA;"""
    output = _dci.cmdexec(stmt)
    
    # t02.7: insert with no rollback
    stmt = """prepare x from
insert with no rollback into t02tabA (a,v1,v2)
values (101,102,103);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3231')
    
    # t02.8: insert with no rollback
    stmt = """prepare x from
insert with no rollback into t02tabA values
(102,103,104,105,106),(103,104,105,106,107);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3231')
    
    # t02.9: insert with no rollback
    stmt = """prepare x from
update with no rollback t02tabA set b = log(a) where a < 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3231')
    
    # t02.10: delete with no rollback
    stmt = """prepare x from
delete with no rollback from t02tabA
where a in (select v2 from t02tabA where v2 = 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3231')
    
    # t02.11: without no rollback should work
    stmt = """prepare x from
delete from t02tabA where b = v2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t02.12:
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 15)
    
    # t02.13:
    stmt = """prepare x from
select with no rollback [first 2] * from t02tabA
order by a,v1,v2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t02.14:
    stmt = """prepare x from
select [first 2] * from t02tabA order by a,v1,v2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # t02.15:
    stmt = """explain x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t02.16:
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    _dci.expect_selected_msg(output, 2)
    
    # t02.17:
    stmt = """commit;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t02.18:
    stmt = """select * from t02tabA order by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t02exp""", 't02s16')
    
    _dci = _testmgr.get_default_dci_proc()
    
    # default is AUTOCOMMIT ON
    # t02.19:
    stmt = """prepare x from
insert with no rollback into t02tabA values
(102,103,104,105,106),(103,104,105,106,107);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # t02.20:
    stmt = """explain x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t02.21:
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    # t02.22:
    #$SQL_prepared_msg
    stmt = """prepare x from
update with no rollback t02tabA set c = mod(v1,10)
where a = v1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3233')
    
    # t02.25:
    stmt = """prepare x from
delete from t02tabA where c = 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # t02.26:
    stmt = """explain x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t02.27:
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 20)
    
    # t02.28:
    stmt = """select * from t02tabA order by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t02exp""", 't02s3')
    
    _testmgr.testcase_end(desc)

def test003(desc="""t03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # CREATE [volatile] TABLE AS:
    #   Table will be initially created as unaudited and altered to be
    #     audit after insert
    #   The operation bypasses TMF. No transaction will be generated.
    
    stmt = """set warnings on;"""
    output = _dci.cmdexec(stmt)

    # TRAF does not support DDL in a transaction
    # stmt = """begin work;"""
    # output = _dci.cmdexec(stmt)

    # t03.1: expect no transaction from TMF
    # #sh testlog=$test_dir/t03s1log
    # #runscript $is2tools/getTrans
    
    # t03.2:
    # $SQL_complete_msg
    # #expect any *SQL operation completed*
    stmt = """prepare s from
create table t031tab
attribute extent (2048, 2048), maxextents 512
store by (unique2)
AS (
select * from """ + gvars.g_schema_wisc32 + """.abase
where unique2 < 10000);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select OPERATOR from table (explain(NULL,'S'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    # t03.3:
    # #runscript $is2tools/stopTrans
    # #expectfile $test_dir/t03exp t03s3
    # #sh cat $testlog
    # #sh sleep 120
   
    # TRAF does not support DDL in a transaction 
    # stmt = """commit work;"""
    # output = _dci.cmdexec(stmt)
    
    # t03.4:
    stmt = """select count(*) from t031tab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t03exp""", 't03s4')
    
    # t03.5:
    # If a user trasnaction is in effect, VSBB insert will be used
    # stmt = """begin work;"""
    # output = _dci.cmdexec(stmt)
    # _dci.expect_complete_msg(output)
    
    # t03.6:
    # #sh testlog=$test_dir/t03s6log
    # #runscript $is2tools/getTrans
    
    # t03.7:
    # $SQL_complete_msg
    # #expect any *SQL operation completed*
    stmt = """prepare s from
create volatile table t032tab
(unique2, unique1, two, four, ten, twenty, string4)
store by (unique2, unique1)
attribute extent (2048, 2048), maxextents 512
AS (
select unique2, unique1, two, four, ten, twenty, string4
from """ + gvars.g_schema_wisc32 + """.abase
where unique2 between 0000000 and 0001000)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select OPERATOR from table (explain(NULL,'S'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """showlabel t032tab;"""
    output = _dci.cmdexec(stmt)
    
    # t03.8:
    # #runscript $is2tools/stopTrans
    # #expectfile $test_dir/t03exp t03s8
    # #sh cat $testlog
    # #sh sleep 150
    
    stmt = """showddl t032tab;"""
    output = _dci.cmdexec(stmt)
    stmt = """set warnings off;"""
    output = _dci.cmdexec(stmt)
    
    # t03.9:
    # expected 0 row returned
    stmt = """select count(*) from t032tab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t03exp""", 't03s9')
    
    # stmt = """commit work;"""
    # output = _dci.cmdexec(stmt)
    # _dci.expect_complete_msg(output)
    
    stmt = """select count(*) from t032tab;"""
    output = _dci.cmdexec(stmt)
    stmt = """showcontrol query default IGNORE_DUPLICATE_KEYS, match full;"""
    output = _dci.cmdexec(stmt)
    
    # t03.12:
    stmt = """select unique1, unique2, unique3 from t031tab
where unique2 = 0000000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t03exp""", 't03s12')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into t031tab values (
440    -- unique1
, 0      -- unique2
, 0, 0, 0, 0  -- two,four,ten,twenty
, 0, 0, 0, 0  -- one,ten,twenty,fifty percent
, 440         -- unique3
, 0, 0        -- even, old onepercent
, 'stringu1', 'stringu2', 'string4'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # t03.14:
    # #expectfile $test_dir/t03exp t03s14
    # $SQL_selected_msg 2
    #   select unique1, unique2, unique3 from t031tab
    #     where unique2 = 2500000;
    
    stmt = """select unique1, unique2, unique3 from t031tab
where unique2 = 0000000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    # t03.15:
    # $SQL_updated_msg 15000001
    # #expectfile $test_dir/t03exp t03s15
    #   update with no rollback t031tab
    #     set unique1 = 1,
    #         unique2 = 1,
    #         two    = 2,
    #         four   = 4,
    #         ten    = 10,
    #         twenty = 20
    #      where unique2 < 30000000;
    #   get statistics;
    
    # t03.16:
    # #sh testlog=$test_dir/t03s16log
    # #runscript $is2tools/getTrans
    
    # $SQL_updated_msg 10001
    stmt = """prepare s3 from
update with no rollback t031tab
set two    = 2,
four   = 4,
ten    = 10,
twenty = 20
where unique2 < 30000000;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """explain s3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select OPERATOR from table (explain(NULL,'S3'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 10001)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    # t03.17:
    # #runscript $is2tools/stopTrans
    # #expectfile $test_dir/t03exp t03s17
    # #sh cat $testlog
    
    # t03.18:
    stmt = """prepare s from
delete with no rollback
from t031tab where (two,four,ten,twenty) = (2,4,10,20);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """explain s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select OPERATOR from table (explain(NULL,'S'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 10001)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

