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
    
def test001(desc="""a01"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:         A01
    #  Description:            Tests key building algo and use of keys
    #  Test case inputs:       This test relies on the existence of
    #                          the files OPTTST, KEYTST
    #                          Only tests unsigned key columns for now.
    #  Test case outputs:
    #  Expected Results:        (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # Description: Tests key building algo and use of keys
    # NOTE:
    # 1) This test relies on the existence of the files OPTTST,
    #    KEYTST (DEFINEs in SQLDEFS in test library subvolume).
    # 2) Only tests unsigned key columns for now.
    
    stmt = """drop table OPTABLE;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table OPTABLE 
( p1  largeint not null
, u1  smallint unsigned
, zi1 smallint not null
, f1  double precision
, n1  numeric (4,2) unsigned
, d1  decimal (4,2)
, t1  date
, c1  char
, p2  integer not null
, u2  integer unsigned
, zi2 integer not null
, f2  real
, n2  numeric (6,3) unsigned
, d2  decimal (6,3)
, t2  time
, c2  char(2)
, p3  smallint not null
, u3  largeint
, zi3 largeint not null
, f3  float
, n3  numeric (12,4)
, d3  decimal (12,4)
, t3  interval hour to second
, c3  char(3)
, z   char (10)
, primary key (p1, p2, p3) )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1959-12-31',  'a' ,
9,   9,   9,   9,   9,   9, time '23:59:59', 'aa',
9,null,  -1,null,null,null, null, null, null
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1960-01-01', 'a'  ,
10,  10,  10,  10,  10,  10, time '00:00:00', 'aa' ,
10,  10,  10,  10,  10,  10, interval '00:00:00' hour to second, 'aaa', 'Row01'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10, 10, date '1960-01-01',  'a'  ,
10,  10,  10,  10,  10, 10, time '00:00:15', 'aa' ,
20,  20,  20,  20,  20, 20, interval '00:00:15' hour to second, 'aab', 'Row02'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
10,  10,  10,  10,  10,  10, time '00:00:30', 'aa' ,
30,  30,  30,  30,  30,  30, interval '00:00:30' hour to second, 'aac', 'Row03'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
20,  20,  20,  20,  20,  20, time '00:00:45', 'ab' ,
10,  10,  10,  10,  10,  10, interval '00:00:45' hour to second, 'aba', 'Row04'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
20,  20,  20,  20,  20,  20, time '00:01:00', 'ab' ,
20,  20,  20,  20,  20,  20, interval '00:01:00' hour to second, 'abb', 'Row05'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
20,  20,  20,  20,  20,  20, time '00:01:15', 'ab' ,
30,  30,  30,  30,  30,  30, interval '00:01:15' hour to second, 'abc', 'Row06'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
30,  30,  30,  30,  30,  30, time '00:01:30', 'ac' ,
10,  10,  10,  10,  10,  10, interval '00:01:30' hour to second, 'aca', 'Row07'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
30,  30,  30,  30,  30,  30, time '00:01:45', 'ac' ,
20,  20,  20,  20,  20,  20, interval '00:01:45' hour to second, 'acb', 'Row08'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
30,  30,  30,  30,  30,  30, time '00:02:00', 'ac' ,
30,  30,  30,  30,  30,  30, null, 'acc', 'Row09'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
10,  10,  10,  10,  10,  10, null,                               'ba' ,
10,  10,  10,  10,  10,  10, interval '00:02:00' hour to second, 'baa', 'Row10'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
10,  10,  10,  10,  10,  10, time '00:59:00', 'ba' ,
20,  20,  20,  20,  20,  20, interval '00:59:00' hour to second, 'bab', 'Row11'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
10,  10,  10,  10,  10,  10, time '00:59:15', 'ba' ,
30,  30,  30,  30,  30,  30, interval '00:59:15' hour to second, 'bac', 'Row12'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
20,  20,  20,  20,  20,  20, time '00:59:30', 'bb' ,
10,  10,  10,  10,  10,  10, interval '00:59:30' hour to second, 'bba', 'Row13'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
20,  20,  20,  20,  20,  20, time '00:59:45', 'bb' ,
20,  20,  20,  20,  20,  20, interval '00:59:45' hour to second, 'bbb', 'Row14'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
20,  20,  20,  20,  20,  20, time '01:00:00', 'bb' ,
30,  30,  30,  30,  30,  30, interval '01:00:00' hour to second, 'bbc', 'Row15'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
30,  30,  30,  30,  30,  30, time '01:00:00', 'bc' ,
10,  10,  10,  10,  10,  10, null,                               'bca', 'Row16'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
30,  30,  30,  30,  30,  30, time '01:00:15', 'bc' ,
20,  20,  20,  20,  20,  20, interval '01:00:15' hour to second, 'bcb', 'Row17'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
30,  30,  30,  30,  30,  30, time '01:00:30', 'bc' ,
30,  30,  30,  30,  30,  30, interval '01:00:30' hour to second, 'bcc', 'Row18'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
10,  10,  10,  10,  10,  10, time '01:00:45', 'ca' ,
10,  10,  10,  10,  10,  10, interval '01:00:45' hour to second, 'caa', 'Row19'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
10,  10,  10,  10,  10,  10, null,                               'ca' ,
20,  20,  20,  20,  20,  20, interval '01:01:00' hour to second, 'cab', 'Row20'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
10,  10,  10,  10,  10,  10, time '01:59:00', 'ca' ,
30,  30,  30,  30,  30,  30, interval '01:59:00' hour to second, 'cac', 'Row21'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
20,  20,  20,  20,  20,  20, time '01:59:15', 'cb' ,
10,  10,  10,  10,  10,  10, interval '01:59:15' hour to second, 'cba', 'Row22'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
20,  20,  20,  20,  20,  20, time '01:59:30', 'cb' ,
20,  20,  20,  20,  20,  20, interval '01:59:30' hour to second, 'cbb', 'Row23'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
20,  20,  20,  20,  20,  20, time '01:59:45', 'cb' ,
30,  30,  30,  30,  30,  30, interval '01:59:45' hour to second, 'cbc', 'Row24'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
30,  30,  30,  30,  30,  30, time '02:00:00', 'cc' ,
10,  10,  10,  10,  10,  10, interval '02:00:00' hour to second, 'cca', 'Row25'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
30,  30,  30,  30,  30,  30, time '11:59:00', 'cc' ,
20,  20,  20,  20,  20,  20, interval '11:59:00' hour to second, 'ccb', 'Row26'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
30,  30,  30,  30,  30,  30, time '11:59:15', 'cc' ,
30,  30,  30,  30,  30,  30, interval '11:59:15' hour to second, 'ccc', 'Row27'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
30,  10,  10,  10,  10,  10, time '11:59:30', 'ac' ,
40,null,  -1,null,null,null, interval '11:59:30' hour to second, 'aca', 'Row28'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
40,null,  -1,null,null,null, time '11:59:45', 'aa' ,
30,  10,  10,  10,  10,  10, interval '11:59:45' hour to second, null,  'Row29'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
40,null,  -1,null,null,null, time '12:00:00', null ,
40,null,  -1,null,null,null, interval '12:00:00' hour to second, 'aaa', 'Row30'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
40,null,  -1,null,null,null, date '1960-01-01',  null ,
30,  10,  10,  10,  10,  10, time '12:00:00', 'aa' ,
30,  10,  10,  10,  10,  10, interval '12:00:00' hour to second, 'aaa', 'Row31'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
40,null,  -2,null,null,null, date '1960-01-01',  'b'  ,
30,  10,  10,  10,  10,  10, time '23:59:15', 'bb' ,
40,  10,  10,  10,  10,  10, interval '23:59:15' hour to second, null , 'Row32'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
40,null,  -1,null,null,null, date '1960-01-01',  'b'  ,
40,  10,  10,  10,  10,  10, time '23:59:30', null ,
30,null,  -1,null,null,null, interval '23:59:30' hour to second, 'bbb', 'Row33'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
40,null,  -1,null,null,null, date '1960-01-01',  null ,
40,null,  -1,null,null,null, time '23:59:45', 'bb' ,
40,  10,  10,  10,  10,  10, interval '23:59:45' hour to second, 'bbb', 'Row34'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
40,null,  -1,null,null,null, date '1960-01-02',  'c'  ,
40,null,  -1,null,null,null, time '00:00:00', 'cc' ,
50,null,  -1,null,null,null, interval '24:00:00' hour to second, null , 'Row35'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  update statistics for table OPTABLE;
    
    stmt = """update statistics for table OPTABLE on every column;"""
    output = _dci.cmdexec(stmt)
    
    #  Case 1) Ascending index on all columns
    
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 > 30,20  ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop index iuaaa;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuaad;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuada;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuadd;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudaa;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudad;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudda;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuddd;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index iuaaa on OPTABLE(U1 asc, u2 asc, u3 asc);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # KETTST
    
    #An unbounded (<) range scan, only the first key column
    
    stmt = """prepare x from
select count(*)
from OPTABLE 
where u1 < 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(25)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s9')
    # COUNT should be 13
    
    #An unbounded (<=) range scan, only the first key column
    stmt = """prepare x from
select count(*)
from OPTABLE 
where u1 <= 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(25)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    # COUNT should be 13
    
    #An unbounded (>=) range scan, only the first key column
    stmt = """prepare x from
select count(*)
from OPTABLE 
where u1 > 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(25)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s11')
    # COUNT should be 9
    
    #An unbounded (<=) range scan, only the first key column
    stmt = """prepare x from
select count(*)
from OPTABLE 
where u1 >= 30;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(25)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s12')
    # COUNT should be 9
    
    #Partial equality prefix, only the first column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)

    #  see whether it works (should not see any null values)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s13')
    
    # should select 13 rows
    
    #Partial equality prefix, expression for key value
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 5 + 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan, should select indexed access
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s14')
    # should select 13 rows
    
    #Partial equality prefix, select null values only
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 is null
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s15')
    # should select 5 rows
    
    #Partial equality prefix, "=" on 1st, "<" on 2nd
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 10
and u2 < 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s16')
    # should select 5 rows
    
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 < 10,20  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s17')
    # should select 5 rows
    
    #Partial equality prefix, "=" on 1st, "<=" on 2nd
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 10
and u2 <= 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s18')
    # should select 8 rows
    
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 <= 10,20 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s19')
    # should select 8 rows
    
    #Partial equality prefix, "=" on 1st, ">" on 2nd
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 30
and u2 > 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s20')
    # should select 3 rows
    
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 > 30,20  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s21')
    # should select 0 rows
    
    #Partial equality prefix, "=" on 1st, ">=" on 2nd
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 30
and u2 >= 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s22')
    # should select 6 rows
    
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 >= 30,20 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s23')
    
    # should select 6 rows
    
    #Partial equality prefix,"=" on 1st, "=" on 2nd
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 20
and u2 = 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s24')
    # should select 3 rows
    
    #Multivalued = comparison on 1st and 2nd key columns
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 = 20,20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s25')
    # should select 3 rows
    
    #ISNULL on the first column and < on the 2nd column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 is null
and u2 < 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s26')
    # should select 3 rows
    
    #ISNULL on the first column and > on the 2nd column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 is null
and u2 > 0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s27')
    # should select 3 rows
    
    #ISNULL on the first as well as on the 2nd column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 is null
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s28')
    # should select 2 rows
    
    # range (>, <) on the 1st key column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 > 10
and u1 < 30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s29')
    # should select 9 rows
    
    #= on the 1st key column, range (>, <) on the 2nd key column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 10 and u2 > 10
and u2 < 30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s30')
    # should select 3 rows
    
    #Range searches
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 >  10,10
and u1,u2 <  10,30 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s31')
    # should select 3 rows
    
    #Range searches
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 >= 10,10
and u1 < 20 and u2 < 20 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s32')
    # should select 4 rows
    
    #Range searches
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 >= 10
and u1,u2 < 10,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s33')
    # should select 8 rows
    
    #ISNULL on the first column and < on the 2nd column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 is null
and u2 < 10 + 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s34')
    # should select 3 rows
    
    #ISNULL on the first column and < on the 2nd column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 is null
and u2 < 10 + 10
and upshift(c3) between 'A' and 'C'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s35')
    # should select 2 rows
    
    # Case 2) 1st Asc, 2nd Asc, 3rd Desc
    
    stmt = """drop index iuaaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop index iuaad;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuada;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuadd;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudaa;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudad;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudda;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuddd;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index iuaad on OPTABLE(U1 asc, u2 asc, u3 desc)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # KETTST
    
    #An unbounded (<) range scan, only the first key column
    stmt = """prepare x from
select count(*)
from OPTABLE 
where u1 < 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(25)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s43')
    # COUNT should be 13
    
    #An unbounded (<=) range scan, only the first key column
    stmt = """prepare x from
select count(*)
from OPTABLE 
where u1 <= 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(25)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s44')
    # COUNT should be 13
    
    #An unbounded (>=) range scan, only the first key column
    stmt = """prepare x from
select count(*)
from OPTABLE 
where u1 > 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(25)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s45')
    # COUNT should be 9
    
    #An unbounded (<=) range scan, only the first key column
    stmt = """prepare x from
select count(*)
from OPTABLE 
where u1 >= 30;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(25)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s46')
    # COUNT should be 9
    
    #Partial equality prefix, only the first column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works (should not see any null values)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s47')
    # should select 13 rows
    
    #Partial equality prefix, expression for key value
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 5 + 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan, should select indexed access
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s48')
    # should select 13 rows
    
    #Partial equality prefix, select null values only
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 is null
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s49')
    # should select 5 rows
    
    #Partial equality prefix, "=" on 1st, "<" on 2nd
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 10
and u2 < 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s50')
    # should select 5 rows
    
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 < 10,20  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s51')
    # should select 5 rows
    
    #Partial equality prefix, "=" on 1st, "<=" on 2nd
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 10
and u2 <= 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s52')
    # should select 8 rows
    
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 <= 10,20 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s53')
    # should select 8 rows
    
    #Partial equality prefix, "=" on 1st, ">" on 2nd
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 30
and u2 > 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s54')
    # should select 3 rows
    
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 > 30,20  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s55')
    # should select 0 rows
    
    #Partial equality prefix, "=" on 1st, ">=" on 2nd
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 30
and u2 >= 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s56')
    # should select 6 rows
    
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 >= 30,20 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s57')
    # should select 6 rows
    
    #Partial equality prefix,"=" on 1st, "=" on 2nd
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 20
and u2 = 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s58')
    # should select 3 rows
    
    #Multivalued = comparison on 1st and 2nd key columns
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 = 20,20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s59')
    # should select 3 rows
    
    #ISNULL on the first column and < on the 2nd column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 is null
and u2 < 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s60')
    # should select 3 rows
    
    #ISNULL on the first column and > on the 2nd column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 is null
and u2 > 0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s61')
    # should select 3 rows
    
    #ISNULL on the first as well as on the 2nd column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 is null
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s62')
    # should select 2 rows
    
    # range (>, <) on the 1st key column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 > 10
and u1 < 30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s63')
    # should select 9 rows
    
    #= on the 1st key column, range (>, <) on the 2nd key column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 10 and u2 > 10
and u2 < 30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s64')
    # should select 3 rows
    
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 >  10,10
and u1,u2 <  10,30 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s65')
    # should select 3 rows
    
    #Range searches
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 >= 10,10
and u1 < 20 and u2 < 20 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s66')
    # should select 4 rows
    
    #Range searches
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 >= 10
and u1,u2 < 10,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s67')
    # should select 8 rows
    
    #ISNULL on the first column and < on the 2nd column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 is null
and u2 < 10 + 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s68')
    # should select 3 rows
    
    #ISNULL on the first column and < on the 2nd column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 is null
and u2 < 10 + 10
and upshift(c3) between 'A' and 'C'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s69')
    #  should select 2 rows
    
    #  Case 3) 1st Asc, 2nd Desc, 3rd Asc
    
    stmt = """drop index iuaaa;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuaad;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuada;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuadd;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudaa;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudad;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudda;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuddd;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index iuada on OPTABLE(U1 asc, u2 desc, u3 asc) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # KETTST
    
    #An unbounded (<) range scan, only the first key column
    stmt = """prepare x from
select count(*)
from OPTABLE 
where u1 < 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(25)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s77')
    # COUNT should be 13
    
    #An unbounded (<=) range scan, only the first key column
    stmt = """prepare x from
select count(*)
from OPTABLE 
where u1 <= 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(25)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s78')
    # COUNT should be 13
    
    #An unbounded (>=) range scan, only the first key column
    stmt = """prepare x from
select count(*)
from OPTABLE 
where u1 > 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s79')
    # COUNT should be 9
    
    #An unbounded (<=) range scan, only the first key column
    stmt = """prepare x from
select count(*)
from OPTABLE 
where u1 >= 30;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s80')
    # COUNT should be 9
    
    #Partial equality prefix, only the first column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works (should not see any null values)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s81')
    # should select 13 rows
    
    #Partial equality prefix, expression for key value
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 5 + 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan, should select indexed access
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s82')
    # should select 13 rows
    
    #Partial equality prefix, select null values only
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 is null
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s83')
    # should select 5 rows
    
    #Partial equality prefix, "=" on 1st, "<" on 2nd
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 10
and u2 < 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s84')
    # should select 5 rows
    
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 < 10,20  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s85')
    # should select 5 rows
    
    #Partial equality prefix, "=" on 1st, "<=" on 2nd
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 10
and u2 <= 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s86')
    # should select 8 rows
    
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 <= 10,20 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s87')
    # should select 8 rows
    
    #Partial equality prefix, "=" on 1st, ">" on 2nd
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 30
and u2 > 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s88')
    # should select 3 rows
    
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 > 30,20  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s89')
    # should select 0 rows
    
    #Partial equality prefix, "=" on 1st, ">=" on 2nd
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 30
and u2 >= 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s90')
    # should select 6 rows
    
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 >= 30,20 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s91')
    # should select 6 rows
    
    #Partial equality prefix,"=" on 1st, "=" on 2nd
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 20
and u2 = 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s92')
    # should select 3 rows
    
    #Multivalued = comparison on 1st and 2nd key columns
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 = 20,20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s93')
    # should select 3 rows
    
    #ISNULL on the first column and < on the 2nd column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 is null
and u2 < 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s94')
    # should select 3 rows
    
    #ISNULL on the first column and > on the 2nd column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 is null
and u2 > 0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s95')
    # should select 3 rows
    
    #ISNULL on the first as well as on the 2nd column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 is null
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s96')
    # should select 2 rows
    
    # range (>, <) on the 1st key column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 > 10
and u1 < 30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s97')
    # should select 9 rows
    
    #= on the 1st key column, range (>, <) on the 2nd key column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 10 and u2 > 10
and u2 < 30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s98')
    # should select 3 rows
    
    #Range searches
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 >  10,10
and u1,u2 <  10,30 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s99')
    # should select 3 rows
    
    #Range searches
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 >= 10,10
and u1 < 20 and u2 < 20 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s100')
    # should select 4 rows
    
    #Range searches
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 >= 10
and u1,u2 < 10,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s101')
    # should select 8 rows
    
    #ISNULL on the first column and < on the 2nd column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 is null
and u2 < 10 + 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s102')
    # should select 3 rows
    
    #ISNULL on the first column and < on the 2nd column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 is null
and u2 < 10 + 10
and upshift(c3) between 'A' and 'C'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s103')
    #  should select 2 rows
    
    #  Case 4) 1st Asc, 2nd Desc, 3rd Desc
    
    stmt = """drop index iuaaa;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuaad;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuada;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuadd;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudaa;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudad;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudda;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuddd;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index iuadd on OPTABLE(U1 asc, u2 desc, u3 desc) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # KETTST
    
    #An unbounded (<) range scan, only the first key column
    stmt = """prepare x from
select count(*)
from OPTABLE 
where u1 < 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(25)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s111')
    # COUNT should be 13
    
    #An unbounded (<=) range scan, only the first key column
    stmt = """prepare x from
select count(*)
from OPTABLE 
where u1 <= 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(25)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s112')
    # COUNT should be 13
    
    #An unbounded (>=) range scan, only the first key column
    stmt = """prepare x from
select count(*)
from OPTABLE 
where u1 > 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(25)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s113')
    # COUNT should be 9
    
    #An unbounded (<=) range scan, only the first key column
    stmt = """prepare x from
select count(*)
from OPTABLE 
where u1 >= 30;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(25)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s114')
    # COUNT should be 9
    
    #Partial equality prefix, only the first column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works (should not see any null values)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s115')
    # should select 13 rows
    
    #Partial equality prefix, expression for key value
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 5 + 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan, should select indexed access
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s116')
    # should select 13 rows
    
    #Partial equality prefix, select null values only
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 is null
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s117')
    # should select 5 rows
    
    #Partial equality prefix, "=" on 1st, "<" on 2nd
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 10
and u2 < 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s118')
    # should select 5 rows
    
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 < 10,20  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s119')
    # should select 5 rows
    
    #Partial equality prefix, "=" on 1st, "<=" on 2nd
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 10
and u2 <= 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s120')
    # should select 8 rows
    
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 <= 10,20 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s121')
    # should select 8 rows
    
    #Partial equality prefix, "=" on 1st, ">" on 2nd
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 30
and u2 > 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s122')
    # should select 3 rows
    
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 > 30,20  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s123')
    # should select 0 rows
    
    #Partial equality prefix, "=" on 1st, ">=" on 2nd
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 30
and u2 >= 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s124')
    # should select 6 rows
    
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 >= 30,20 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s125')
    # should select 6 rows
    
    #Partial equality prefix,"=" on 1st, "=" on 2nd
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 20
and u2 = 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s126')
    # should select 3 rows
    
    #Multivalued = comparison on 1st and 2nd key columns
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 = 20,20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s127')
    # should select 3 rows
    
    #ISNULL on the first column and < on the 2nd column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 is null
and u2 < 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s128')
    # should select 3 rows
    
    #ISNULL on the first column and > on the 2nd column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 is null
and u2 > 0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s129')
    # should select 3 rows
    
    #ISNULL on the first as well as on the 2nd column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 is null
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s130')
    # should select 2 rows
    
    # range (>, <) on the 1st key column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 > 10
and u1 < 30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s131')
    # should select 9 rows
    
    #= on the 1st key column, range (>, <) on the 2nd key column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 10 and u2 > 10
and u2 < 30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s132')
    # should select 3 rows
    
    #Range searches
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 >  10,10
and u1,u2 <  10,30 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s133')
    # should select 3 rows
    
    #Range searches
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 >= 10,10
and u1 < 20 and u2 < 20 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s134')
    # should select 4 rows
    
    #Range searches
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 >= 10
and u1,u2 < 10,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s135')
    # should select 8 rows
    
    #ISNULL on the first column and < on the 2nd column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 is null
and u2 < 10 + 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s136')
    # should select 3 rows
    
    #ISNULL on the first column and < on the 2nd column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 is null
and u2 < 10 + 10
and upshift(c3) between 'A' and 'C'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s137')
    #  should select 2 rows
    
    #  Case 5) 1st Desc, 2nd Asc, 3rd Asc
    
    stmt = """drop index iuaaa;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuaad;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuada;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuadd;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudaa;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudad;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudda;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuddd;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index iudaa on OPTABLE(U1 desc, u2 asc, u3 asc) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # KETTST
    
    #An unbounded (<) range scan, only the first key column
    stmt = """prepare x from
select count(*)
from OPTABLE 
where u1 < 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(25)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s145')
    # COUNT should be 13
    
    #An unbounded (<=) range scan, only the first key column
    stmt = """prepare x from
select count(*)
from OPTABLE 
where u1 <= 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(25)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s146')
    # COUNT should be 13
    
    #An unbounded (>=) range scan, only the first key column
    stmt = """prepare x from
select count(*)
from OPTABLE 
where u1 > 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(25)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s147')
    # COUNT should be 9
    
    #An unbounded (<=) range scan, only the first key column
    stmt = """prepare x from
select count(*)
from OPTABLE 
where u1 >= 30;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(25)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s148')
    # COUNT should be 9
    
    #Partial equality prefix, only the first column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works (should not see any null values)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s149')
    # should select 13 rows
    
    #Partial equality prefix, expression for key value
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 5 + 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan, should select indexed access
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s150')
    # should select 13 rows
    
    #Partial equality prefix, select null values only
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 is null
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s151')
    # should select 5 rows
    
    #Partial equality prefix, "=" on 1st, "<" on 2nd
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 10
and u2 < 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s152')
    # should select 5 rows
    
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 < 10,20  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s153')
    # should select 5 rows
    
    #Partial equality prefix, "=" on 1st, "<=" on 2nd
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 10
and u2 <= 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s154')
    # should select 8 rows
    
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 <= 10,20 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s155')
    # should select 8 rows
    
    #Partial equality prefix, "=" on 1st, ">" on 2nd
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 30
and u2 > 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s156')
    # should select 3 rows
    
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 > 30,20  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s157')
    # should select 0 rows
    
    #Partial equality prefix, "=" on 1st, ">=" on 2nd
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 30
and u2 >= 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s158')
    # should select 6 rows
    
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 >= 30,20 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s159')
    # should select 6 rows
    
    #Partial equality prefix,"=" on 1st, "=" on 2nd
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 20
and u2 = 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s160')
    # should select 3 rows
    
    #Multivalued = comparison on 1st and 2nd key columns
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 = 20,20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s161')
    # should select 3 rows
    
    #ISNULL on the first column and < on the 2nd column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 is null
and u2 < 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s162')
    # should select 3 rows
    
    #ISNULL on the first column and > on the 2nd column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 is null
and u2 > 0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s163')
    # should select 3 rows
    
    #ISNULL on the first as well as on the 2nd column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 is null
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s164')
    # should select 2 rows
    
    # range (>, <) on the 1st key column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 > 10
and u1 < 30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s165')
    # should select 9 rows
    
    #= on the 1st key column, range (>, <) on the 2nd key column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 10 and u2 > 10
and u2 < 30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s166')
    # should select 3 rows
    
    #Range searches
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 >  10,10
and u1,u2 <  10,30 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s167')
    # should select 3 rows
    
    #Range searches
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 >= 10,10
and u1 < 20 and u2 < 20 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s168')
    # should select 4 rows
    
    #Range searches
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 >= 10
and u1,u2 < 10,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s169')
    # should select 8 rows
    
    #ISNULL on the first column and < on the 2nd column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 is null
and u2 < 10 + 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s170')
    # should select 3 rows
    
    #ISNULL on the first column and < on the 2nd column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 is null
and u2 < 10 + 10
and upshift(c3) between 'A' and 'C'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s171')
    #  should select 2 rows
    
    #  Case 6) 1st Desc, 2nd Asc, 3rd Desc
    
    stmt = """drop index iuaaa;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuaad;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuada;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuadd;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudaa;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudad;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudda;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuddd;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index iudad on OPTABLE(U1 desc, u2 asc, u3 desc) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # KETTST
    
    #An unbounded (<) range scan, only the first key column
    stmt = """prepare x from
select count(*)
from OPTABLE 
where u1 < 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(25)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s179')
    # COUNT should be 13
    
    #An unbounded (<=) range scan, only the first key column
    stmt = """prepare x from
select count(*)
from OPTABLE 
where u1 <= 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(25)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s180')
    # COUNT should be 13
    
    #An unbounded (>=) range scan, only the first key column
    stmt = """prepare x from
select count(*)
from OPTABLE 
where u1 > 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(25)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s181')
    # COUNT should be 9
    
    #An unbounded (<=) range scan, only the first key column
    stmt = """prepare x from
select count(*)
from OPTABLE 
where u1 >= 30;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(25)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s182')
    # COUNT should be 9
    
    #Partial equality prefix, only the first column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works (should not see any null values)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s183')
    # should select 13 rows
    
    #Partial equality prefix, expression for key value
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 5 + 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan, should select indexed access
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s184')
    # should select 13 rows
    
    #Partial equality prefix, select null values only
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 is null
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s185')
    # should select 5 rows
    
    #Partial equality prefix, "=" on 1st, "<" on 2nd
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 10
and u2 < 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s186')
    # should select 5 rows
    
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 < 10,20  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s187')
    # should select 5 rows
    
    #Partial equality prefix, "=" on 1st, "<=" on 2nd
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 10
and u2 <= 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s188')
    # should select 8 rows
    
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 <= 10,20 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s189')
    # should select 8 rows
    
    #Partial equality prefix, "=" on 1st, ">" on 2nd
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 30
and u2 > 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s190')
    # should select 3 rows
    
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 > 30,20  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s191')
    # should select 0 rows
    
    #Partial equality prefix, "=" on 1st, ">=" on 2nd
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 30
and u2 >= 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s192')
    # should select 6 rows
    
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 >= 30,20 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s193')
    # should select 6 rows
    
    #Partial equality prefix,"=" on 1st, "=" on 2nd
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 20
and u2 = 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s194')
    # should select 3 rows
    
    #Multivalued = comparison on 1st and 2nd key columns
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 = 20,20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s195')
    # should select 3 rows
    
    #ISNULL on the first column and < on the 2nd column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 is null
and u2 < 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s196')
    # should select 3 rows
    
    #ISNULL on the first column and > on the 2nd column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 is null
and u2 > 0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s197')
    # should select 3 rows
    
    #ISNULL on the first as well as on the 2nd column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 is null
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s198')
    # should select 2 rows
    
    # range (>, <) on the 1st key column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 > 10
and u1 < 30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s199')
    # should select 9 rows
    
    #= on the 1st key column, range (>, <) on the 2nd key column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 10 and u2 > 10
and u2 < 30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s200')
    # should select 3 rows
    
    #Range searches
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 >  10,10
and u1,u2 <  10,30 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s201')
    # should select 3 rows
    
    #Range searches
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 >= 10,10
and u1 < 20 and u2 < 20 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s202')
    # should select 4 rows
    
    #Range searches
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 >= 10
and u1,u2 < 10,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s203')
    # should select 8 rows
    
    #ISNULL on the first column and < on the 2nd column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 is null
and u2 < 10 + 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s204')
    # should select 3 rows
    
    #ISNULL on the first column and < on the 2nd column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 is null
and u2 < 10 + 10
and upshift(c3) between 'A' and 'C'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s205')
    #  should select 2 rows
    
    #  Case 7) 1st Desc, 2nd Desc, 3rd Asc
    
    stmt = """drop index iuaaa;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuaad;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuada;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuadd;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudaa;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudad;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudda;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuddd;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index iudda on OPTABLE(U1 desc, u2 desc, u3 asc);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # KETTST
    
    #An unbounded (<) range scan, only the first key column
    stmt = """prepare x from
select count(*)
from OPTABLE 
where u1 < 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(25)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s213')
    # COUNT should be 13
    
    #An unbounded (<=) range scan, only the first key column
    stmt = """prepare x from
select count(*)
from OPTABLE 
where u1 <= 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(25)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s214')
    # COUNT should be 13
    
    #An unbounded (>=) range scan, only the first key column
    stmt = """prepare x from
select count(*)
from OPTABLE 
where u1 > 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(25)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s215')
    # COUNT should be 9
    
    #An unbounded (<=) range scan, only the first key column
    stmt = """prepare x from
select count(*)
from OPTABLE 
where u1 >= 30;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(25)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s216')
    # COUNT should be 9
    
    #Partial equality prefix, only the first column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works (should not see any null values)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s217')
    # should select 13 rows
    
    #Partial equality prefix, expression for key value
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 5 + 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan, should select indexed access
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s218')
    # should select 13 rows
    
    #Partial equality prefix, select null values only
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 is null
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s219')
    # should select 5 rows
    
    #Partial equality prefix, "=" on 1st, "<" on 2nd
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 10
and u2 < 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s220')
    # should select 5 rows
    
    #Multivalued "<" comparison on 1st and 2nd key columns
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 < 10,20  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s221')
    # should select 5 rows
    
    #Partial equality prefix, "=" on 1st, "<=" on 2nd
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 10
and u2 <= 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s222')
    # should select 8 rows
    
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 <= 10,20 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s223')
    # should select 8 rows
    
    #Partial equality prefix, "=" on 1st, ">" on 2nd
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 30
and u2 > 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s224')
    # should select 3 rows
    
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 > 30,20  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s225')
    # should select 0 rows
    
    #Partial equality prefix, "=" on 1st, ">=" on 2nd
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 30
and u2 >= 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s226')
    # should select 6 rows
    
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 >= 30,20 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s227')
    # should select 6 rows
    
    #Partial equality prefix,"=" on 1st, "=" on 2nd
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 20
and u2 = 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s228')
    # should select 3 rows
    
    #Multivalued = comparison on 1st and 2nd key columns
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 = 20,20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s229')
    # should select 3 rows
    
    #ISNULL on the first column and < on the 2nd column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 is null
and u2 < 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s230')
    # should select 3 rows
    
    #ISNULL on the first column and > on the 2nd column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 is null
and u2 > 0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s231')
    # should select 3 rows
    
    #ISNULL on the first as well as on the 2nd column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 is null
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s232')
    # should select 2 rows
    
    # range (>, <) on the 1st key column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 > 10
and u1 < 30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s233')
    # should select 9 rows
    
    #= on the 1st key column, range (>, <) on the 2nd key column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 10 and u2 > 10
and u2 < 30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s234')
    # should select 3 rows
    
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 >  10,10
and u1,u2 <  10,30 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s235')
    # should select 3 rows
    
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 >= 10,10
and u1 < 20 and u2 < 20 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s236')
    # should select 4 rows
    
    #Range searches
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 >= 10
and u1,u2 < 10,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s237')
    # should select 8 rows
    
    #ISNULL on the first column and < on the 2nd column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 is null
and u2 < 10 + 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s238')
    # should select 3 rows
    
    #ISNULL on the first column and < on the 2nd column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 is null
and u2 < 10 + 10
and upshift(c3) between 'A' and 'C'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s239')
    #  should select 2 rows
    
    #  Case 8) 1st Desc, 2nd Desc, 3rd Desc
    
    stmt = """drop index iuaaa;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuaad;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuada;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuadd;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudaa;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudad;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudda;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuddd;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index iuddd on OPTABLE(U1 desc, u2 desc, u3 desc) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # KETTST
    
    #An unbounded (<) range scan, only the first key column
    stmt = """prepare x from
select count(*)
from OPTABLE 
where u1 < 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(25)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s247')
    # COUNT should be 13
    
    #An unbounded (<=) range scan, only the first key column
    stmt = """prepare x from
select count(*)
from OPTABLE 
where u1 <= 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(25)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s248')
    # COUNT should be 13
    
    #An unbounded (>=) range scan, only the first key column
    stmt = """prepare x from
select count(*)
from OPTABLE 
where u1 > 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(25)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s249')
    # COUNT should be 9
    
    #An unbounded (<=) range scan, only the first key column
    stmt = """prepare x from
select count(*)
from OPTABLE 
where u1 >= 30;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(25)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s250')
    # COUNT should be 9
    
    #Partial equality prefix, only the first column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works (should not see any null values)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s251')
    # should select 13 rows
    
    #Partial equality prefix, expression for key value
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 5 + 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan, should select indexed access
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s252')
    # should select 13 rows
    
    #Partial equality prefix, select null values only
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 is null
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s253')
    # should select 5 rows
    
    #Partial equality prefix, "=" on 1st, "<" on 2nd
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 10
and u2 < 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s254')
    # should select 5 rows
    
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 < 10,20  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s255')
    # should select 5 rows
    
    #Partial equality prefix, "=" on 1st, "<=" on 2nd
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 10
and u2 <= 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s256')
    # should select 8 rows
    
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 <= 10,20 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s257')
    # should select 8 rows
    
    #Partial equality prefix, "=" on 1st, ">" on 2nd
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 30
and u2 > 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s258')
    # should select 3 rows
    
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 > 30,20  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s259')
    # should select 0 rows
    
    #Partial equality prefix, "=" on 1st, ">=" on 2nd
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 30
and u2 >= 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s260')
    # should select 6 rows
    
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 >= 30,20 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s261')
    # should select 6 rows
    
    #Partial equality prefix,"=" on 1st, "=" on 2nd
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 20
and u2 = 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s262')
    # should select 3 rows
    
    #Multivalued = comparison on 1st and 2nd key columns
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 = 20,20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s263')
    # should select 3 rows
    
    #ISNULL on the first column and < on the 2nd column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 is null
and u2 < 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s264')
    # should select 3 rows
    
    #ISNULL on the first column and > on the 2nd column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 is null
and u2 > 0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s265')
    # should select 3 rows
    
    #ISNULL on the first as well as on the 2nd column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 is null
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s266')
    # should select 2 rows
    
    # range (>, <) on the 1st key column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 > 10
and u1 < 30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s267')
    # should select 9 rows
    
    #= on the 1st key column, range (>, <) on the 2nd key column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 = 10 and u2 > 10
and u2 < 30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s268')
    # should select 3 rows
    
    #Range searches
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 >  10,10
and u1,u2 <  10,30 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s269')
    # should select 3 rows
    
    #Range searches
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1,u2 >= 10,10
and u1 < 20 and u2 < 20 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s270')
    # should select 4 rows
    
    #Range searches
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 >= 10
and u1,u2 < 10,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s271')
    # should select 8 rows
    
    #ISNULL on the first column and < on the 2nd column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 is null
and u2 < 10 + 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s272')
    # should select 3 rows
    
    #ISNULL on the first column and < on the 2nd column
    stmt = """prepare x from
select u1, u2, u3, c3
from OPTABLE 
where u1 is null
and u2 < 10 + 10
and upshift(c3) between 'A' and 'C'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check the plan
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    #  see whether it works
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s273')
    
    #drop table OPTABLE;
    
    _testmgr.testcase_end(desc)

def test002(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A02
    #  Description:        This test verifies the SQL <specify>
    #                      feature.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # Select on a protection view was causing a run-time error.
    # (The optimizer was using an offset to the column in the base table
    #  instead of the protection view)
    
    stmt = """create table ta151203 
(vc      varchar(10)
,c       char(10)
,pic99   pic 9(2)
,num     numeric(2,0)
) no partition
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view vu151203 
as select * from ta151203 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Should return 0 rows (no run-time error)
    stmt = """select * from vu151203 
where pic99 = (select pic99 from vu151203 where pic99 = 0)
for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # cleanup
    stmt = """drop view vu151203;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table ta151203;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # Sort error when sort primary key contains an odd-length field
    
    stmt = """create table oddlen(a char(3),
b int,
c char(7)) no partition
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into oddlen values ('A', 1, 'z');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into oddlen values ('Z', 2, 'a');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  Should return 2 records (no errors => success)
    stmt = """select * from oddlen order by c,b,a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    
    # cleanup
    stmt = """drop table oddlen;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Subqueries incorrectly associated by the optimizer.
    
    stmt = """create table befm 
(
EXPNO                         CHAR( 6 ) not null
, TYPE1                          CHAR( 4 ) not null
, ANOREL                        CHAR( 4 ) not null
, DXNO                          CHAR( 3 ) not null
, MODCNT                        NUMERIC( 5, 0) UNSIGNED not null
, TCODE                         CHAR( 8 )
, MCODE                         CHAR( 8 )
, SIZE1                          CHAR( 4 )
, DISTR                         CHAR( 3 )
, QUANT                         CHAR( 4 )
, LAT                           CHAR( 3 )
, CROSSREF                      CHAR( 3 )
, VALID                         CHAR( 1 )
, CREATED                       largeint
, C_GID                         NUMERIC( 5, 0) UNSIGNED
, C_UID                         NUMERIC( 5, 0) UNSIGNED
, REASON                        NUMERIC( 5, 0) UNSIGNED
, FIX1                          CHAR( 3 )
, FIX2                          CHAR( 3 )
, FIX3                          CHAR( 3 )
, OLDGRL                        CHAR( 1 )
, primary key (expno,type1,anorel,dxno,modcnt)
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table dtglos 
(
T_GLOS_GEN                    NUMERIC( 5, 0) UNSIGNED not null
, TCODE                         CHAR( 8 ) not null
, MODCNT                        NUMERIC( 5, 0) UNSIGNED not null
, t1                            CHAR( 1 )
, t2                            CHAR( 1 )
, t3                            CHAR( 1 )
, T4                            CHAR( 1 )
, T5                            CHAR( 1 )
, T6                            CHAR( 1 )
, TABBR                         CHAR( 20 )
, TTEXT                         CHAR( 60 )
, TSECT                         CHAR( 4 )
, SUBSECT                       CHAR( 4 )
, USEDBY                        CHAR( 4 )
, VALID                         CHAR( 1 )
, CREATED                       largeint
, C_GID                         NUMERIC( 5, 0) UNSIGNED
, C_UID                         NUMERIC( 5, 0) UNSIGNED
, REASON                        NUMERIC( 5, 0) UNSIGNED
, primary key (t_glos_gen,tcode,modcnt)
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index dtglosi on dtglos 
(t_glos_gen,tabbr,modcnt)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table dmglos 
(
M_GLOS_GEN                    NUMERIC( 5, 0) UNSIGNED not null
, MCODE                         CHAR( 8 ) not null
, MODCNT                        NUMERIC( 5, 0) UNSIGNED not null
, M1                            CHAR( 1 )
, M2                            CHAR( 1 )
, M3                            CHAR( 1 )
, M4                            CHAR( 1 )
, M5                            CHAR( 1 )
, M6                            CHAR( 1 )
, MABBR                         CHAR( 20 )
, MTEXT                         CHAR( 60 )
, MSECTH                        CHAR( 4 )
, MSECTM                        CHAR( 4 )
, USEDBY                        CHAR( 4 )
, VALID                         CHAR( 1 )
, CREATED                       largeint
, C_GID                         NUMERIC( 5, 0) UNSIGNED
, C_UID                         NUMERIC( 5, 0) UNSIGNED
, REASON                        NUMERIC( 5, 0) UNSIGNED
, primary key (m_glos_gen,mcode,modcnt)
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index dmglosi on dmglos 
(m_glos_gen,mabbr,modcnt)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """prepare diag from
select  b.dxno,
b.modcnt,
t.tabbr,
m.mabbr,
b.size1,
b.distr,
b.quant,
b.lat,
b.crossref,
b.fix1,
b.fix2,
b.fix3,
b.oldgrl,
b.reason,
b.valid
from     befm b,
 dtglos t,
 dmglos m
where       t.tabbr   =
(select tabbr from dtglos x
where x.tcode = b.tcode
)
and  m.mabbr   =
(select mabbr from dmglos y
where y.mcode = b.mcode
)
read uncommitted access
order by b.expno, b.type1, b.anorel, b.dxno, b.modcnt ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #    read uncommitted access;
    
    stmt = """drop table befm;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table dtglos;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table dmglos;"""
    output = _dci.cmdexec(stmt)
    
    # Could not order by a constant (normalizer was eliminating it)
    
    stmt = """create table mr161516(a int) no partition
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into mr161516 values (4096);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select 'Sher Khan', a from mr161516 
union all
select 'Bagheera', a from mr161516 
union all
select 'Mowgli', a from mr161516 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    
    stmt = """select 'Sher Khan', a from mr161516 
union
select 'Bagheera', a from mr161516 
union
select 'Mowgli', a from mr161516 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    
    stmt = """drop table mr161516;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # A SELECT DISTINCT (constant) in a subquery returned an internal error
    
    stmt = """create table mr271659(x int, y int) no partition
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into mr271659 values (1,10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mr271659 values (2,20);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mr271659 values (3,30);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select x, max(y)
from mr271659 t1 
group by x
having max(y) = (select distinct min(t1.y)
from mr271659 t2 
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    
    stmt = """drop table mr271659;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE TABLE ta022023 
(
col_1                  VARCHAR(5) UPSHIFT
, col_2                  NUMERIC(9,2) SIGNED default 1.0 not null
, col_3                  LARGEINT SIGNED not null
HEADING 'Large Integer Column'
, col_join               CHAR(30) UPSHIFT
default 'JOIN' not null
HEADING 'Join Column'
, col_4                  PIC 9(7)V99 COMP
, col_5                  DECIMAL(7,2) SIGNED
, col_6                  PIC S9(18) not null
, col_7                  PIC X(5) UPSHIFT
default '' not null
, col_8                  NUMERIC(4) UNSIGNED
, col_9                  DECIMAL(4) UNSIGNED default 5 not null
HEADING '4-digit Decimal Column'
) no partition
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into ta022023 
values ('AAAAA',3.14,123456789,'frank',284.13,
74.65,22546,'aaaaa',1010,2020);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into ta022023     -- col_1,col_4,col_5,col_8 are NULL
values (NULL,6.37,4908763,'rich',NULL,
NULL,653326,'bbbbb',NULL,4040);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into ta022023 
values ('CREEQ',432166.55,-2167543,'JOIN',86888.97,
4112.87,17844536,'ccccc',507,3097);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into ta022023 
values ('WWAAA',4.55,3215,'JOIN',195.01,
29.88,-34336,'ddddd',1111,2222);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into ta022023            -- col_8 is NULL
values ('AAAB',264.7,-61098,'ronnie',216.28,
755.12,19415,'eeeee',NULL,4444);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into ta022023 
values ('A',7.48,321,'gary',909862.91,
31225.88,777777,'fffff',555,666);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into ta022023 
values ('AAAB',7.11,1230987,'ronnie',1122322.51,
7990.66,324141,'ggggg',22,335);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into ta022023        -- col_1,col_4 and col_8 are NULL
values (NULL,4336.08,-98,'senior',NULL,
31.76,111111,'hhhhh',NULL,7777);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into ta022023 
values ('AAA',29.44,3214567,'junior',88.63,
24168.54,222222,'iiiii',8888,9999);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into ta022023 
values ('BBBBB',32.71,100100,'junior',1185.25,
5770.66,333333,'jjjjj',400,3139);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into ta022023 
values ('AAB',1.11,222222,'JOIN',86.72,
9981.11,444444,'kkkkk',5551,2134);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into ta022023 
values ('AAA',99.14,333333,'senior',62.21,
62012.00,555555,'lllll',100,2200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into ta022023 
values ('C',8.88,4949494949,'bobbie',55.22,
228.77,-666666,'mmmmm',9090,4898);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into ta022023      -- col_1 and col_5 are NULL
values (NULL,3.49,5666,'conrad',2244.59,
NULL,777777,'nnnnn',313,4141);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into ta022023      -- col_4 and col_8 are NULL
values ('CAB',33347.24,77777,'faye',NULL,
444.44,888888,'ooooo',NULL,4545);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #
    #Index ix022023A: 1 column, nullable
    #
    
    stmt = """CREATE INDEX ix022023 
ON ta022023 ( col_8 )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # update statistics for table ta022023;
    
    stmt = """set param ?p0 22;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?i0 -1;"""
    output = _dci.cmdexec(stmt)
    
    #display_explain  select col_8 from ta022023 where (col_8 > ?p0 );
    stmt = """explain options 'f' select col_8 from ta022023 where (col_8 > ?p0 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # prepare q3 from
    #  'select col_8 from ta022023 where (col_8 > ?p0 ?i0 )';
    
    stmt = """prepare q3 from select col_8 from ta022023 where (col_8 > ?p0 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #  Note setting ?i0 to -1 would make it a null!
    #  set param ?p0 22;
    #  set param ?i0 1;
    
    #  Check inserted values
    stmt = """select col_8 from ta022023;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s4')
    
    #  Should return 10 rows. (col_8 > 22)
    stmt = """execute q3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')
    
    # cleanup
    
    stmt = """drop table ta022023;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # A primary key predicate from the WHERE clause of a protection view definition
    # is not used as a begin/end primary key.
    
    stmt = """create table ta031516 (a int,b int) no partition  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view vu031516 as
select b
from ta031516 
where b is not null
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into ta031516 values (1, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ta031516 values (1, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  should get 1 row
    stmt = """select * from vu031516;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s6')
    
    stmt = """drop view vu031516;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table ta031516;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Predicates from the WHERE clause of a view
    # containing an outer join
    # were associated with the ON clause of its
    # outer join with another
    # table.
    
    stmt = """create table t1(a int) no partition ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into t1 values (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values (2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create table t2(b int) no partition  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into t2 values (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create table t3(c int) no partition  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into t3 values (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create view v (x, y) as
select a, b
from t1 left join t2 on a = b
where b = 1 or b is null
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # 04/16/09 added order by
    stmt = """select * from v;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s7')
    
    # Visual check for association of predicates
    stmt = """explain options 'f'
select *
from v left join t3 on y = c ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Acid test. Is the correct data returned ? Should see 2 rows.
    # 04/16/09 added order by
    stmt = """select * from v left join t3 on y = c ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s8')
    
    # Cleanup
    
    stmt = """drop view v;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table t2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table t3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # A correlated quantified subquery in the ON clause of an outer join
    # was not transformed into an EXISTS subquery. Used to kill SQLCOMP.
    
    stmt = """create table my071039(a int) no partition  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into my071039 values (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from my071039 X
left join my071039 Y
on X.a = ANY (select a
from my071039 Z
where Z.a = X.a
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s9')
    
    stmt = """drop table my071039;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # 3 table outer join with the same predicate duplicated in both
    # the ON clauses. 
    
    stmt = """create table my071050 (a int) no partition  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into my071050 values (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into my071050 values (2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # prepare x from
    #  ' select *       '
    # '   from my071050 T1 left join my071050 T2 on T1.a = T2.a '
    # '                    left join my071050 T3 on T1.a = T2.a '
    # ;
    
    stmt = """prepare x from
select *
from my071050 t1 
left join my071050 t2 
on t1.a = t2.a
left join my071050 t3 
on t1.a = t2.a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #  check plan to see where preds evaluated
    # plan often changes, when the plan changes, the number of rows returned will
    # be different
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(25)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(tname as char(30)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s11')
    
    # prepare x from
    #  ' select *       '
    # '   from my071050 T1 left join my071050 T2 on T1.a <> T2.a '
    # '                    left join my071050 T3 on T1.a <> T2.a '
    # ;
    
    stmt = """prepare x from
select *
from my071050 t1 left join my071050 t2 on t1.a <> t2.a
left join my071050 t3 on t1.a <> t2.a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #  check plan to see where preds evaluated
    # plan often changes, when the plan changes, the number of rows returned will
    # be different
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(25)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(tname as char(30)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s13')
    
    # prepare x from
    #  ' select *       '
    # '   from my071050 T1 left join my071050 T2 on T1.a = T2.a '
    # '                    left join my071050 T3 on T1.a <> T2.a '
    # ;
    #
    stmt = """prepare x from
select *
from my071050 t1 left join my071050 t2 on t1.a = t2.a
left join my071050 t3 on t1.a <> t2.a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #  check plan to see where preds evaluated
    # plan often changes, when the plan changes, the number of rows returned will
    # be different
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(25)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(tname as char(30)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s15')
    
    stmt = """prepare x from
select *
from my071050 t1 left join my071050 t2 on t1.a <> t2.a
left join my071050 t3 on t1.a =  t2.a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #  check plan to see where preds evaluated
    # plan often changes, when the plan changes, the number of rows returned will
    # be different
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(25)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(tname as char(30)) as Tab
from table (explain(NULL,'X'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s17')
    
    stmt = """drop table my071050;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Datetime column compared with a parameter caused internal error.
    # (Type propagation is introducing datetime function nodes but
    #  optimizer was unaware of it)
    
    stmt = """create table my141717 
(
last_name                      pic   x(20) no default not null
, first_name                     pic   x(20) no default not null
, middle_initial                 pic   x no default not null
, reference_number               timestamp(0)  no default not null
, street                         pic   x(40) default null
, city                           pic   x(30) default null
, state                          pic   x(2) default null
, zip_code                       pic   9(5) default null
, area_code                      pic   9(3) default null
, district_code                  pic   9(3) default null
, last_4_digits                  pic   9(4) default null
, model_ordered                  pic   9(4) default null
, qty_ordered                    pic   9(8) default null
, unit_price                     pic   9(4)v99 default null
, total_price                    pic   s9(12)v99 default null
, order_status                   pic   x(1) default null
, primary key ( last_name, middle_initial, reference_number )
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # prepare q1 from
    #  'select * from my141717 '
    # ' where (last_name, middle_initial, reference_number > '
    # '       ?p0, ?p1, ?p2) '
    # ;
    stmt = """prepare q1 from
select * from my141717 
where (last_name, middle_initial, reference_number >
?p0, ?p1, ?p2)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #  ensure that primary keyed access was chosen
    stmt = """select cast(seq_num as smallint) as SEQ_NUM,
cast(operator as char(20)) as OP,
cast(left_child_seq_num as smallint) as L_Child,
cast(right_child_seq_num as smallint) as R_Child,
cast(right(rtrim(tname), 25) as char(25)) as Tab
from table (explain(NULL,'Q1'))
order by seq_num desc;"""
    output = _dci.cmdexec(stmt)
    
    # cleanup
    
    stmt = """drop table my141717;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table jl171731 
(a  int, b int, c int) no partition
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into jl171731 values (200, 1, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into jl171731 values (300, 1, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into jl171731 values (350, 2, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into jl171731 values (450, 2, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select 1, avg(a/100), b, c, count(*)
from jl171731 
where a > 100 and a <= 300
group by b, c
union all
select 2, avg(a/100), b, c, count(*)
from jl171731 
where a > 300 and a <= 500
group by b, c ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s19')
    
    stmt = """drop table jl171731;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table jl191034 
(a char(1)) no partition  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into jl191034 values ('a');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into jl191034 values ('b');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into jl191034 values ('c');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into jl191034 values ('c');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  Null string constant is first sort primary key column  (sort for order by)
    stmt = """select '', a from jl191034 order by 1,a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s20')
    
    #  Null string constant is second sort primary key column (sort for order by)
    stmt = """select '', a from jl191034 order by a, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s21')
    
    #  Null string constant is first sort primary key column  (sort for distinct)
    stmt = """select distinct '', a from jl191034;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s22')
    
    #  Null string constant is second sort primary key column  (sort for distinct)
    stmt = """select distinct a, '' from jl191034;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s23')
    
    #  Null string constant is first sort primary key column  (sort for group by)
    #  select a, '', min(a), count(*) from jl191034 group by 2,1;
    
    #  Null string constant is second sort primary key column (sort for group by)
    #  select a, '', min(a), count(*) from jl191034 group by 1,2;
    
    #  Null string constant is the argument of an aggregate function
    stmt = """select a, min('') from jl191034 group by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s24')
    stmt = """select a, max('') from jl191034 group by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s25')
    #  select a, '', min('') from jl191034 group by a,2;
    stmt = """select a, '', min('') from jl191034 group by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s26')
    #  select a, '', min('') from jl191034 group by 2,1;
    stmt = """select a, '', max('') from jl191034 group by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s27')
    #  select a, '', max('') from jl191034 group by a,2;
    # select a, '', max('') from jl191034 group by 2,1;
    
    #  Null string constant is the argument of an UPSHIFT function
    stmt = """select a, upshift('') from jl191034 group by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s28')
    #  select a, upshift('') from jl191034 group by a,2;
    #  select a, upshift('') from jl191034 group by 2,1;
    stmt = """select a, upshift('') from jl191034 order by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s29')
    #  select a, upshift('') from jl191034 order by a,2;
    #  select a, upshift('') from jl191034 order by 2,1;
    stmt = """select distinct a, upshift('') from jl191034;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s30')
    stmt = """select distinct upshift(''), a from jl191034;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s31')
    
    stmt = """drop table jl191034;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table test1 ( key1 char(4) not null
, a1   char(4) not null
, b1   char(4) not null
) no partition
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table test2 ( key2 char(4) not null
, a2   char(4) not null
, b2   char(4) not null
) no partition
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into test1 values ('01', 'A', 'B');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into test1 values ('02', 'B', 'C');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into test1 values ('03', 'C', 'D');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into test1 values ('04', 'D', 'E');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into test1 values ('05', 'E', 'F');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into test1 values ('06', 'F', 'G');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into test1 values ('07', 'G', 'H');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into test1 values ('08', 'H', 'I');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into test1 values ('09', 'I', 'J');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into test1 values ('10', 'J', 'K');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into test2 values ('01', 'a', 'b');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into test2 values ('02', 'b', 'c');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into test2 values ('03', 'c', 'd');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into test2 values ('04', 'd', 'e');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into test2 values ('05', 'e', 'f');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into test2 values ('06', 'f', 'g');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into test2 values ('07', 'g', 'h');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into test2 values ('08', 'h', 'i');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into test2 values ('09', 'i', 'j');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into test2 values ('10', 'j', 'k');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create view v (key1, key2, a1, b1, a2, b2)
as select  key1, key2, a1, b1, a2, b2
from  test1 left join test2 
on  key1 = key2
where  key1 > '0'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  should return 2 rows
    stmt = """select * from v where key2 in ('02', '03') order by key2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s32')
    
    stmt = """drop view v;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table test2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table up 
(a int, b int, c int, u char(4) upshift) no partition  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into up values(1,2,3,'abcd');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into up values(1,2,4,'abcd');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into up values(1,2,3,'ebcd');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from up;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s33')
    
    # The sort primary key must contain 3 elements
    stmt = """explain options 'f'
select distinct a+b, upshift(u), c
from up ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  should see three rows
    stmt = """select distinct a+b, upshift(u), c
from up ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s34')
    
    stmt = """explain options 'f' select u from up where u = upshift('abcd');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  will return 2 rows
    stmt = """select u from up where u = upshift('abcd');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s35')
    
    # Primary access will be chosen
    stmt = """explain options 'f' select u from up 
where u between upshift('abcd')
and upshift('abce');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  will return 1 row
    stmt = """select u from up 
where u between upshift('abcd')
and upshift('abce');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s36')
    
    stmt = """create index ui on
 up(u)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Primary access will be chosen
    stmt = """explain options 'f' select u from up 
where u = upshift('abcd');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  will return 1 row
    stmt = """select u from up where u = upshift('abcd');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s37')
    
    # Index only access using ui
    stmt = """explain options 'f' select u from up 
where u between upshift('abcd')
and upshift('abce');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  will return 1 row
    stmt = """select u from up 
where u between upshift('abcd')
and upshift('abce');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s38')
    
    # Alternate access using ui
    stmt = """explain options 'f'
select u
from up 
where u between upshift('abcd')
and upshift('abce')
and b = 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  will return 1 row
    stmt = """select u from up 
where u between upshift('abcd')
and upshift('abce') and b = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s39')
    
    stmt = """drop table up;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table nv031744 
(a smallint, b int, c decimal (2,0), junk char(3000)) no partition  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into nv031744 values(32767,       null, null, 'A');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into nv031744 values( null, 2147483647, null, 'B');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into nv031744 values( null,       null,   99, 'B');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #Case I : smallint column
    
    stmt = """create index nvi on nv031744(a, b, c)  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Check if index access is chosen
    stmt = """explain options 'f' select min(a) from nv031744;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select min(a) from nv031744;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s40')
    
    stmt = """drop index nvi;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Case II : int column
    
    stmt = """create index nvi on nv031744(b, c, a)  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Check if index access is chosen
    stmt = """explain options 'f' select min(b) from nv031744;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select min(b) from nv031744;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s41')
    
    stmt = """drop index nvi;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Case III : decimal column
    
    stmt = """create index nvi on nv031744(c, a, b)  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Check if index access is chosen
    stmt = """explain options 'f' select min(c) from nv031744;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select min(c) from nv031744;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s42')
    
    stmt = """drop table nv031744;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE TABLE customer (
custnum         NUMERIC (4) UNSIGNED
NO DEFAULT
NOT NULL
HEADING 'Cust/Num'
,custname        CHARACTER (18)
NO DEFAULT
NOT NULL
HEADING 'Customer Name'
,street          CHARACTER (22)
NO DEFAULT
NOT NULL
HEADING 'street'
,city            CHARACTER (14)
NO DEFAULT
NOT NULL
HEADING 'city'
,state           CHARACTER (12)
NOT NULL
HEADING 'state'
,postcode        CHARACTER (10)
NO DEFAULT
NOT NULL
HEADING 'Post Code'
,credit          CHARACTER (2)
DEFAULT 'C1'
NOT NULL
HEADING 'CR'
,PRIMARY KEY     (custnum)
)
STORE BY PRIMARY KEY
--     ORGANIZATION KEY SEQUENCED
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE VIEW custlist 
AS SELECT
custnum
,custname
,street
,city
,state
,postcode
FROM customer 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX XCUSTNAM 
ON customer (
custname
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO customer VALUES ( 22, 'Tester', '4300 The Woods Dr.', 'San Jose',
'CA', '95136', 'A1');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    _testmgr.testcase_end(desc)

def test003(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:         A03
    #  Description:
    #  Test case inputs:       This test relies on the existence of
    #                          the files OPTTST, AGGTST
    #  Test case outputs:
    #  Expected Results:        (provide a high-level description)
    #
    # Description: Test MIN/MAX optimization.
    # NOTE:
    #   This test relies on the existence of the files OPTTST,
    #   AGGTST (DEFINEs in SQLDEFS in test library subvolume).
    #  =================== End Test Case Header  ===================
    
    stmt = """drop table OPTABLE;"""
    output = _dci.cmdexec(stmt)
    
    # delete define =T;
    
    # Create the test database
    # add define =T, class map, file t;
    
    stmt = """create table OPTABLE 
( p1  largeint not null
, u1  smallint unsigned
, zi1 smallint not null
, f1  double precision
, n1  numeric (4,2) unsigned
, d1  decimal (4,2)
, t1  date
, c1  char
, p2  integer not null
, u2  integer unsigned
, zi2 integer not null
, f2  real
, n2  numeric (6,3) unsigned
, d2  decimal (6,3)
, t2  time
, c2  char(2)
, p3  smallint not null
, u3  largeint
, zi3 largeint not null
, f3  float
, n3  numeric (12,4)
, d3  decimal (12,4)
, t3  interval hour to second
, c3  char(3)
, z   char (10)
, primary key (p1, p2, p3) )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #?section ins
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1959-12-31',  'a' ,
9,   9,   9,   9,   9,   9, time '23:59:59', 'aa',
9,null,  -1,null,null,null, null, null, null
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1960-01-01', 'a'  ,
10,  10,  10,  10,  10,  10, time '00:00:00', 'aa' ,
10,  10,  10,  10,  10,  10, interval '00:00:00' hour to second, 'aaa', 'Row01'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10, 10, date '1960-01-01',  'a'  ,
10,  10,  10,  10,  10, 10, time '00:00:15', 'aa' ,
20,  20,  20,  20,  20, 20, interval '00:00:15' hour to second, 'aab', 'Row02'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
10,  10,  10,  10,  10,  10, time '00:00:30', 'aa' ,
30,  30,  30,  30,  30,  30, interval '00:00:30' hour to second, 'aac', 'Row03'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
20,  20,  20,  20,  20,  20, time '00:00:45', 'ab' ,
10,  10,  10,  10,  10,  10, interval '00:00:45' hour to second, 'aba', 'Row04'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
20,  20,  20,  20,  20,  20, time '00:01:00', 'ab' ,
20,  20,  20,  20,  20,  20, interval '00:01:00' hour to second, 'abb', 'Row05'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
20,  20,  20,  20,  20,  20, time '00:01:15', 'ab' ,
30,  30,  30,  30,  30,  30, interval '00:01:15' hour to second, 'abc', 'Row06'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
30,  30,  30,  30,  30,  30, time '00:01:30', 'ac' ,
10,  10,  10,  10,  10,  10, interval '00:01:30' hour to second, 'aca', 'Row07'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
30,  30,  30,  30,  30,  30, time '00:01:45', 'ac' ,
20,  20,  20,  20,  20,  20, interval '00:01:45' hour to second, 'acb', 'Row08'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
10,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
30,  30,  30,  30,  30,  30, time '00:02:00', 'ac' ,
30,  30,  30,  30,  30,  30, null, 'acc', 'Row09'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
10,  10,  10,  10,  10,  10, null,                               'ba' ,
10,  10,  10,  10,  10,  10, interval '00:02:00' hour to second, 'baa', 'Row10'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
10,  10,  10,  10,  10,  10, time '00:59:00', 'ba' ,
20,  20,  20,  20,  20,  20, interval '00:59:00' hour to second, 'bab', 'Row11'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
10,  10,  10,  10,  10,  10, time '00:59:15', 'ba' ,
30,  30,  30,  30,  30,  30, interval '00:59:15' hour to second, 'bac', 'Row12'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
20,  20,  20,  20,  20,  20, time '00:59:30', 'bb' ,
10,  10,  10,  10,  10,  10, interval '00:59:30' hour to second, 'bba', 'Row13'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
20,  20,  20,  20,  20,  20, time '00:59:45', 'bb' ,
20,  20,  20,  20,  20,  20, interval '00:59:45' hour to second, 'bbb', 'Row14'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
20,  20,  20,  20,  20,  20, time '01:00:00', 'bb' ,
30,  30,  30,  30,  30,  30, interval '01:00:00' hour to second, 'bbc', 'Row15'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
30,  30,  30,  30,  30,  30, time '01:00:00', 'bc' ,
10,  10,  10,  10,  10,  10, null,                               'bca', 'Row16'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
30,  30,  30,  30,  30,  30, time '01:00:15', 'bc' ,
20,  20,  20,  20,  20,  20, interval '01:00:15' hour to second, 'bcb', 'Row17'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
20,  20,  20,  20,  20,  20, date '1960-01-01',  'b'  ,
30,  30,  30,  30,  30,  30, time '01:00:30', 'bc' ,
30,  30,  30,  30,  30,  30, interval '01:00:30' hour to second, 'bcc', 'Row18'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
10,  10,  10,  10,  10,  10, time '01:00:45', 'ca' ,
10,  10,  10,  10,  10,  10, interval '01:00:45' hour to second, 'caa', 'Row19'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
10,  10,  10,  10,  10,  10, null,                               'ca' ,
20,  20,  20,  20,  20,  20, interval '01:01:00' hour to second, 'cab', 'Row20'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
10,  10,  10,  10,  10,  10, time '01:59:00', 'ca' ,
30,  30,  30,  30,  30,  30, interval '01:59:00' hour to second, 'cac', 'Row21'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
20,  20,  20,  20,  20,  20, time '01:59:15', 'cb' ,
10,  10,  10,  10,  10,  10, interval '01:59:15' hour to second, 'cba', 'Row22'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
20,  20,  20,  20,  20,  20, time '01:59:30', 'cb' ,
20,  20,  20,  20,  20,  20, interval '01:59:30' hour to second, 'cbb', 'Row23'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
20,  20,  20,  20,  20,  20, time '01:59:45', 'cb' ,
30,  30,  30,  30,  30,  30, interval '01:59:45' hour to second, 'cbc', 'Row24'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
30,  30,  30,  30,  30,  30, time '02:00:00', 'cc' ,
10,  10,  10,  10,  10,  10, interval '02:00:00' hour to second, 'cca', 'Row25'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
30,  30,  30,  30,  30,  30, time '11:59:00', 'cc' ,
20,  20,  20,  20,  20,  20, interval '11:59:00' hour to second, 'ccb', 'Row26'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  30,  30,  30,  30,  30, date '1960-01-01',  'c'  ,
30,  30,  30,  30,  30,  30, time '11:59:15', 'cc' ,
30,  30,  30,  30,  30,  30, interval '11:59:15' hour to second, 'ccc', 'Row27'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
30,  10,  10,  10,  10,  10, time '11:59:30', 'ac' ,
40,null,  -1,null,null,null, interval '11:59:30' hour to second, 'aca', 'Row28'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
40,null,  -1,null,null,null, time '11:59:45', 'aa' ,
30,  10,  10,  10,  10,  10, interval '11:59:45' hour to second, null,  'Row29'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
30,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
40,null,  -1,null,null,null, time '12:00:00', null ,
40,null,  -1,null,null,null, interval '12:00:00' hour to second, 'aaa', 'Row30'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
40,null,  -1,null,null,null, date '1960-01-01',  null ,
30,  10,  10,  10,  10,  10, time '12:00:00', 'aa' ,
30,  10,  10,  10,  10,  10, interval '12:00:00' hour to second, 'aaa', 'Row31'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
40,null,  -2,null,null,null, date '1960-01-01',  'b'  ,
30,  10,  10,  10,  10,  10, time '23:59:15', 'bb' ,
40,  10,  10,  10,  10,  10, interval '23:59:15' hour to second, null , 'Row32'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
40,null,  -1,null,null,null, date '1960-01-01',  'b'  ,
40,  10,  10,  10,  10,  10, time '23:59:30', null ,
30,null,  -1,null,null,null, interval '23:59:30' hour to second, 'bbb', 'Row33'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
40,null,  -1,null,null,null, date '1960-01-01',  null ,
40,null,  -1,null,null,null, time '23:59:45', 'bb' ,
40,  10,  10,  10,  10,  10, interval '23:59:45' hour to second, 'bbb', 'Row34'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into OPTABLE values (
40,null,  -1,null,null,null, date '1960-01-02',  'c'  ,
40,null,  -1,null,null,null, time '00:00:00', 'cc' ,
50,null,  -1,null,null,null, interval '24:00:00' hour to second, null , 'Row35'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  update statistics for table OPTABLE;
    
    #  Primary Key only
    
    stmt = """drop index iuaaa;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuaad;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuada;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuadd;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudaa;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudad;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudda;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuddd;"""
    output = _dci.cmdexec(stmt)
    
    # ?section p0
    # Min on 1st primary key column, unbounded scan (no keys)
    stmt = """prepare x from
select min(p1)
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s9')
    
    # display statistics;
    
    # ?section p1
    # Max on 1st primary key column, unbounded scan (no keys)
    stmt = """prepare x from
select max(p1)
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 40
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s10')
    
    # display statistics;
    
    # ?section p2
    # Min on 1st primary key column, unbounded scan
    stmt = """prepare x from
select min(p1)
from OPTABLE 
where p1 < 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s11')
    
    # display statistics;
    
    # ?section p3
    # Max on 1st primary key column, unbounded scan
    stmt = """prepare x from
select max(p1)
from OPTABLE 
where p1 > 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 40
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s12')
    
    # display statistics;
    
    # ?section p4
    # Min on 1st primary key column, range scan
    stmt = """prepare x from
select min(p1)
from OPTABLE 
where p1 > 10
and p1 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 20
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s13')
    
    # display statistics;
    
    # ?section p5
    # Max on 1st primary key column, range scan
    stmt = """prepare x from
select max(p1)
from OPTABLE 
where p1 > 10
and p1 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 40
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s14')
    
    # display statistics;
    
    # ?section p6
    # Min on 1st primary key column, equality predicate
    stmt = """prepare x from
select min(p1)
from OPTABLE 
where p1 = 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 20
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s15')
    
    # display statistics;
    
    # ?section p7
    # Max on 1st primary key column, equality predicate
    stmt = """prepare x from
select max(p1)
from OPTABLE 
where p1 = 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 20
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s16')
    
    # display statistics;
    
    # ?section p8
    # Min on 2nd primary key column, partial equality key prefix
    stmt = """prepare x from
select min(p2)
from OPTABLE 
where p1 = 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s17')
    
    # display statistics;
    
    # ?section p9
    # Min on 2nd primary key column, partial equality key prefix
    stmt = """prepare x from
select max(p2)
from OPTABLE 
where p1 = 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s18')
    
    # display statistics;
    
    # ?section p10
    # Min on 1st primary key column, partial equality key prefix
    stmt = """prepare x from
select min(p1)
from OPTABLE 
where p1 = 20
and p2 < 30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 20
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s19')
    
    # display statistics;
    
    # ?section p11
    # Min on 2nd primary key column, partial equality key prefix
    stmt = """prepare x from
select min(p2)
from OPTABLE 
where p1 = 20
and p2 < 30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s20')
    
    # display statistics;
    
    # ?section p12
    # Max on 1st primary key column, partial equality key prefix
    stmt = """prepare x from
select max(p1)
from OPTABLE 
where p1 = 20
and p2 > 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 20
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s21')
    
    # display statistics;
    
    # ?section p13
    # Max on 2nd primary key column, partial equality key prefix
    stmt = """prepare x from
select max(p2)
from OPTABLE 
where p1 = 20
and p2 > 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s22')
    
    # display statistics;
    
    # ?section p14
    # Min on 3rd primary key column, partial equality key prefix
    stmt = """prepare x from
select min(p3)
from OPTABLE 
where p1 = 20
and p2 = 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s23')
    
    # display statistics;
    
    # ?section p15
    # Max on 3rd primary key column, partial equality key prefix
    stmt = """prepare x from
select max(p3)
from OPTABLE 
where p1 = 20
and p2 = 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s24')
    
    # display statistics;
    
    # ?section p16
    # Min on 1st primary key column, fully qualified key
    stmt = """prepare x from
select min(p1)
from OPTABLE 
where p1 = 20
and p2 = 20
and p3 < 30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 20
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s25')
    
    # display statistics;
    
    # ?section p17
    # Min on 2nd primary key column, fully qualified key
    stmt = """prepare x from
select min(p2)
from OPTABLE 
where p1 = 20
and p2 = 20
and p3 < 30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 20
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s26')
    
    # display statistics;
    
    # ?section p18
    # Min on 3rd primary key column, fully qualified key
    stmt = """prepare x from
select min(p3)
from OPTABLE 
where p1 = 20
and p2 = 20
and p3 < 30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s27')
    
    # display statistics;
    
    # ?section p19
    # Min on 1st primary key column, fully qualified key
    stmt = """prepare x from
select max(p1)
from OPTABLE 
where p1 = 20
and p2 = 20
and p3 > 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 20
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s28')
    
    # display statistics;
    
    # ?section p20
    # Max on 2nd primary key column, fully qualified key
    stmt = """prepare x from
select max(p2)
from OPTABLE 
where p1 = 20
and p2 = 20
and p3 > 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 20
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s29')
    
    # display statistics;
    
    # ?section p21
    # Max on 3rd primary key column, fully qualified key
    stmt = """prepare x from
select max(p3)
from OPTABLE 
where p1 = 20
and p2 = 20
and p3 > 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s30')
    
    # display statistics;
    
    # ?section p22
    # Max on 3rd primary key column, full equality key prefix
    stmt = """prepare x from
select max(p3)
from OPTABLE 
where p1 = 20
and p2 = 20
and p3 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s31')
    
    # display statistics;
    
    # ?section p23
    # Min on 1st primary key column, full key prefix
    stmt = """prepare x from
select min(p1)
from OPTABLE 
where p1,p2,p3 > 10,100,100
and p1       < 30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 20
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s32')
    
    # display statistics;
    
    # ?section p24
    # Max on 1st primary key column, full key prefix
    stmt = """prepare x from
select max(p1)
from OPTABLE 
where p1       > 20
and p1,p2,p3 < 30, 30, 30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s33')
    
    # display statistics;
    
    # Plans that should not use the MIN/MAX optimization
    # ?section p25
    # Min on 2nd primary key column, full key prefix
    stmt = """prepare x from
select min(p2)
from OPTABLE 
where p1,p2,p3 > 20,0,0
and p1       < 30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s34')
    
    # display statistics;
    
    # ?section p26
    # Min on 3rd primary key column, full key prefix
    stmt = """prepare x from
select min(p3)
from OPTABLE 
where p1,p2,p3 > 20, 10, 10
and p1       < 30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s35')
    
    # display statistics;
    
    # ?section p27
    # Max on 2nd primary key column, full key prefix
    stmt = """prepare x from
select max(p2)
from OPTABLE 
where p1       > 20
and p1,p2,p3 < 30, 30, 30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s36')
    
    # display statistics;
    
    # ?section p28
    # Max on 3rd primary key column, full key prefix
    stmt = """prepare x from
select max(p3)
from OPTABLE 
where p1       > 20
and p1,p2,p3 < 30, 30, 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s37')
    
    # display statistics;
    
    # ?section p29
    # Min on 2nd primary key column, query has a GROUP BY
    stmt = """prepare x from
select min(p2)
from OPTABLE 
where p1 = 20
group by p1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should expect 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s38')
    
    # display statistics;
    
    # ?section p30
    # Min on 2nd primary key column, query has a HAVING
    stmt = """prepare x from
select min(p2)
from OPTABLE 
where p1 = 20
having sum(p3) < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # check its result, should expect 0 rows
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # display statistics;
    
    # ?section p31
    # Min on 2nd primary key column, query has an Executor predicate
    stmt = """prepare x from
select min(p2)
from OPTABLE A
where p1 IN (select p1
from OPTABLE B
where p1 < 100)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should see 1 row
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s39')
    
    # display statistics;
    
    # ?section p32
    # Min on 2nd primary key column, query uses multiple scans
    stmt = """prepare x from
select min(p3)
from OPTABLE 
where p1,p2 = 20,20
or p1,p2 = 30,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan, must see two scans
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s40')
    
    #  display statistics;
    
    #  Case 1) Ascending index on all columns
    
    stmt = """drop index iuaaa;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuaad;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuada;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuadd;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudaa;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudad;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudda;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuddd;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index iuaaa on OPTABLE(U1 asc, u2 asc, u3 asc)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # ?section u1
    # Min on 1st alternate key column, unbounded scan (no keys)
    stmt = """prepare x from
select min(u1)
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s49')
    
    # display statistics;
    
    # ?section u2
    # Min on 1st alternate key column, unbounded scan (no keys)
    stmt = """prepare x from
select max(u1)
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s50')
    
    # display statistics;
    
    # ?section u3
    # Max on 1st alternate key column, unbounded scan
    stmt = """prepare x from
select max(u1)
from OPTABLE 
where u1 > 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30 (should not see null)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s51')
    
    # display statistics;
    
    # ?section u4
    # Min on 1st alternate key column, equality predicate
    stmt = """prepare x from
select min(u1)
from OPTABLE 
where u1 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s52')
    
    # display statistics;
    
    # ?section u5
    # Max on 1st alternate key column, equality predicate
    stmt = """prepare x from
select max(u1)
from OPTABLE 
where u1 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s53')
    
    # display statistics;
    
    # ?section u6
    # Min on 2nd alternate key column, equality predicate
    stmt = """prepare x from
select min(u2)
from OPTABLE 
where u1 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 9
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s54')
    
    # display statistics;
    
    # ?section u7
    # Max on 2nd alternate key column, equality predicate
    stmt = """prepare x from
select max(u2)
from OPTABLE 
where u1 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30 (should not see a null value)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s55')
    
    # display statistics;
    
    # ?section u8
    # Min on 3rd alternate key column, partial equality key prefix
    # (Have one row with values {10, 9, null}
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1 = 10
and u2 = 9
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get null (0 rows)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s56')
    
    # display statistics;
    
    # ?section u9
    # Min on 3rd alternate key column, partial equality prefix of key
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1 = 20
and u2 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s57')
    
    # display statistics;
    
    # ?section u10
    # Max on 3rd alternate key column, partial equality prefix of key
    stmt = """prepare x from
select max(u3)
from OPTABLE 
where u1 = 20
and u2 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s58')
    
    # display statistics;
    
    # ?section u11
    # Max on 3rd alternate key column, partial equality prefix of key
    stmt = """prepare x from
select max(u3)
from OPTABLE 
where u1 = 10
and u2 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30 (should not be NULL)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s59')
    
    # display statistics;
    
    # ?section u12
    # Min on 1st primary key column full equality prefix of alternate key
    stmt = """prepare x from
select min(p1)
from OPTABLE 
where u1 = 30
and u2 = 10
and u3 = 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30 (should not be NULL)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s60')
    
    # display statistics;
    
    # ?section u13
    # Max on 1st primary key column full equality prefix of alternate key
    stmt = """prepare x from
select max(p1)
from OPTABLE 
where u1 = 30
and u2 = 10
and u3 = 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s61')
    
    # display statistics;
    
    # ?section u14
    # Min on 2nd alternate key column, equality on 1st, > on 2nd
    stmt = """prepare x from
select min(u2)
from OPTABLE 
where u1 = 10
and u2 > 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 20
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s62')
    
    # display statistics;
    
    # ?section u15
    # Max on 2nd alternate key column, equality on 1st, > on 2nd
    stmt = """prepare x from
select max(u2)
from OPTABLE 
where u1 = 10
and u2 > 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s63')
    
    # display statistics;
    
    # ?section u16
    # Min on 2nd alternate key column, equality on 1st, < on 2nd
    stmt = """prepare x from
select min(u2)
from OPTABLE 
where u1 = 10
and u2 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 9
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s64')
    
    # display statistics;
    
    # ?section u17
    # Max on 2nd alternate key column, equality on 1st, < on 2nd
    stmt = """prepare x from
select max(u2)
from OPTABLE 
where u1 = 10
and u2 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s65')
    
    # display statistics;
    
    # ?section u18
    # Min on 3rd alternate key column, equality on 1st and 2nd,
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1 = 10
and u2 = 30
and u3 > 0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s66')
    
    # display statistics;
    
    # ?section u19
    # Max on 3rd alternate key column, equality on 1st and 2nd,
    stmt = """prepare x from
select max(u3)
from OPTABLE 
where u1 = 10
and u2 = 30
and u3 > 0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s67')
    
    # display statistics;
    
    # ?section u20
    # Min on 3rd alternate key column, equality on 1st and 2nd,
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1 = 10
and u2 = 30
and u3 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s68')
    
    # display statistics;
    
    # ?section u21
    # Max on 3rd alternate key column, equality on 1st and 2nd,
    stmt = """prepare x from
select max(u3)
from OPTABLE 
where u1 = 10
and u2 = 30
and u3 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s69')
    
    # display statistics;
    
    # ?section u22
    # Min on 1st alternate key column, range scan
    stmt = """prepare x from
select min(u1)
from OPTABLE 
where u1 > 10
and u1 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 20
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s70')
    
    # display statistics;
    
    # ?section u23
    # Max on 1st alternate key column, range scan
    stmt = """prepare x from
select max(u1)
from OPTABLE 
where u1 > 10
and u1 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s71')
    
    # display statistics;
    
    # ?section u24
    # Min on 1st alternate key column, range scan
    stmt = """prepare x from
select min(u1)
from OPTABLE 
where u1,u2,u3 > 10,20,30
and u1,u2,u3 < 30,20,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s72')
    
    # display statistics;
    
    # ?section u25
    # Max on 1st alternate key column, range scan
    stmt = """prepare x from
select max(u1)
from OPTABLE 
where u1,u2,u3 > 10,20,30
and u1,u2,u3 < 30,20,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s73')
    
    # display statistics;
    
    # ?section u26
    # Min on 1st alternate key column, range scan
    stmt = """prepare x from
select min(u1)
from OPTABLE 
where u1,u2,u3 > 10,20,30
and u1,u2,u3 < 30,20,30
and  c1 = 'b'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 20
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s74')
    
    # display statistics;
    
    # ?section u27
    # Max on 1st alternate key column, range scan
    stmt = """prepare x from
select max(u1)
from OPTABLE 
where u1,u2,u3 > 10,20,30
and u1,u2,u3 < 30,20,30
and c1 = 'c'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s75')
    
    # display statistics;
    
    # ?section u28
    # Min on 3rd alternate key column, full equality prefix
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1,u2,u3,p1,p2,p3 = 10,30,30,10,30,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s76')
    
    # display statistics;
    
    # ?section u29
    # Min on 3rd alternate key column, full equality prefix
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1,u2,u3 = 10,30,30
and p1,p2,p3 = 10,30,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s77')
    
    # display statistics;
    
    # Case 2) 1st Asc, 2nd Asc, 3rd Desc
    
    stmt = """drop index iuaaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop index iuaad;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuada;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuadd;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudaa;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudad;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudda;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuddd;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index iuaad on OPTABLE(U1 asc, u2 asc, u3 desc)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # ?section u1
    # Min on 1st alternate key column, unbounded scan (no keys)
    stmt = """prepare x from
select min(u1)
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s85')
    
    # display statistics;
    
    # ?section u2
    # Min on 1st alternate key column, unbounded scan (no keys)
    stmt = """prepare x from
select max(u1)
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s86')
    
    # display statistics;
    
    # ?section u3
    # Max on 1st alternate key column, unbounded scan
    stmt = """prepare x from
select max(u1)
from OPTABLE 
where u1 > 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30 (should not see null)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s87')
    
    # display statistics;
    
    # ?section u4
    # Min on 1st alternate key column, equality predicate
    stmt = """prepare x from
select min(u1)
from OPTABLE 
where u1 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s88')
    
    # display statistics;
    
    # ?section u5
    # Max on 1st alternate key column, equality predicate
    stmt = """prepare x from
select max(u1)
from OPTABLE 
where u1 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s89')
    
    # display statistics;
    
    # ?section u6
    # Min on 2nd alternate key column, equality predicate
    stmt = """prepare x from
select min(u2)
from OPTABLE 
where u1 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 9
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s90')
    
    # display statistics;
    
    # ?section u7
    # Max on 2nd alternate key column, equality predicate
    stmt = """prepare x from
select max(u2)
from OPTABLE 
where u1 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30 (should not see a null value)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s91')
    
    # display statistics;
    
    # ?section u8
    # Min on 3rd alternate key column, partial equality key prefix
    # (Have one row with values {10, 9, null}
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1 = 10
and u2 = 9
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get null (0 rows)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s92')
    
    # display statistics;
    
    # ?section u9
    # Min on 3rd alternate key column, partial equality prefix of key
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1 = 20
and u2 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s93')
    
    # display statistics;
    
    # ?section u10
    # Max on 3rd alternate key column, partial equality prefix of key
    stmt = """prepare x from
select max(u3)
from OPTABLE 
where u1 = 20
and u2 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s94')
    
    # display statistics;
    
    # ?section u11
    # Max on 3rd alternate key column, partial equality prefix of key
    stmt = """prepare x from
select max(u3)
from OPTABLE 
where u1 = 10
and u2 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30 (should not be NULL)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s95')
    
    # display statistics;
    
    # ?section u12
    # Min on 1st primary key column full equality prefix of alternate key
    stmt = """prepare x from
select min(p1)
from OPTABLE 
where u1 = 30
and u2 = 10
and u3 = 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30 (should not be NULL)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s96')
    
    # display statistics;
    
    # ?section u13
    # Max on 1st primary key column full equality prefix of alternate key
    stmt = """prepare x from
select max(p1)
from OPTABLE 
where u1 = 30
and u2 = 10
and u3 = 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s97')
    
    # display statistics;
    
    # ?section u14
    # Min on 2nd alternate key column, equality on 1st, > on 2nd
    stmt = """prepare x from
select min(u2)
from OPTABLE 
where u1 = 10
and u2 > 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 20
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s98')
    
    # display statistics;
    
    # ?section u15
    # Max on 2nd alternate key column, equality on 1st, > on 2nd
    stmt = """prepare x from
select max(u2)
from OPTABLE 
where u1 = 10
and u2 > 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s99')
    
    # display statistics;
    
    # ?section u16
    # Min on 2nd alternate key column, equality on 1st, < on 2nd
    stmt = """prepare x from
select min(u2)
from OPTABLE 
where u1 = 10
and u2 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 9
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s100')
    
    # display statistics;
    
    # ?section u17
    # Max on 2nd alternate key column, equality on 1st, < on 2nd
    stmt = """prepare x from
select max(u2)
from OPTABLE 
where u1 = 10
and u2 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s101')
    
    # display statistics;
    
    # ?section u18
    # Min on 3rd alternate key column, equality on 1st and 2nd,
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1 = 10
and u2 = 30
and u3 > 0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s102')
    
    # display statistics;
    
    # ?section u19
    # Max on 3rd alternate key column, equality on 1st and 2nd,
    stmt = """prepare x from
select max(u3)
from OPTABLE 
where u1 = 10
and u2 = 30
and u3 > 0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s103')
    
    # display statistics;
    
    # ?section u20
    # Min on 3rd alternate key column, equality on 1st and 2nd,
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1 = 10
and u2 = 30
and u3 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s104')
    
    # display statistics;
    
    # ?section u21
    # Max on 3rd alternate key column, equality on 1st and 2nd,
    stmt = """prepare x from
select max(u3)
from OPTABLE 
where u1 = 10
and u2 = 30
and u3 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s105')
    
    # display statistics;
    
    # ?section u22
    # Min on 1st alternate key column, range scan
    stmt = """prepare x from
select min(u1)
from OPTABLE 
where u1 > 10
and u1 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 20
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s106')
    
    # display statistics;
    
    # ?section u23
    # Max on 1st alternate key column, range scan
    stmt = """prepare x from
select max(u1)
from OPTABLE 
where u1 > 10
and u1 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s107')
    
    # display statistics;
    
    # ?section u24
    # Min on 1st alternate key column, range scan
    stmt = """prepare x from
select min(u1)
from OPTABLE 
where u1,u2,u3 > 10,20,30
and u1,u2,u3 < 30,20,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s108')
    
    # display statistics;
    
    # ?section u25
    # Max on 1st alternate key column, range scan
    stmt = """prepare x from
select max(u1)
from OPTABLE 
where u1,u2,u3 > 10,20,30
and u1,u2,u3 < 30,20,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s109')
    
    # display statistics;
    
    # ?section u26
    # Min on 1st alternate key column, range scan
    stmt = """prepare x from
select min(u1)
from OPTABLE 
where u1,u2,u3 > 10,20,30
and u1,u2,u3 < 30,20,30
and  c1 = 'b'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 20
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s110')
    
    # display statistics;
    
    # ?section u27
    # Max on 1st alternate key column, range scan
    stmt = """prepare x from
select max(u1)
from OPTABLE 
where u1,u2,u3 > 10,20,30
and u1,u2,u3 < 30,20,30
and c1 = 'c'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s111')
    
    # display statistics;
    
    # ?section u28
    # Min on 3rd alternate key column, full equality prefix
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1,u2,u3,p1,p2,p3 = 10,30,30,10,30,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s112')
    
    # display statistics;
    
    # ?section u29
    # Min on 3rd alternate key column, full equality prefix
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1,u2,u3 = 10,30,30
and p1,p2,p3 = 10,30,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s113')
    
    #  display statistics;
    
    #  Case 3) 1st Asc, 2nd Desc, 3rd Asc
    
    stmt = """drop index iuaaa;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuaad;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuada;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuadd;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudaa;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudad;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudda;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuddd;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index iuada on OPTABLE(U1 asc, u2 desc, u3 asc)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # ?section u1
    # Min on 1st alternate key column, unbounded scan (no keys)
    stmt = """prepare x from
select min(u1)
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s121')
    
    # display statistics;
    
    # ?section u2
    # Min on 1st alternate key column, unbounded scan (no keys)
    stmt = """prepare x from
select max(u1)
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s122')
    
    # display statistics;
    
    # ?section u3
    # Max on 1st alternate key column, unbounded scan
    stmt = """prepare x from
select max(u1)
from OPTABLE 
where u1 > 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30 (should not see null)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s123')
    
    # display statistics;
    
    # ?section u4
    # Min on 1st alternate key column, equality predicate
    stmt = """prepare x from
select min(u1)
from OPTABLE 
where u1 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s124')
    
    # display statistics;
    
    # ?section u5
    # Max on 1st alternate key column, equality predicate
    stmt = """prepare x from
select max(u1)
from OPTABLE 
where u1 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s125')
    
    # display statistics;
    
    # ?section u6
    # Min on 2nd alternate key column, equality predicate
    stmt = """prepare x from
select min(u2)
from OPTABLE 
where u1 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 9
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s126')
    
    # display statistics;
    
    # ?section u7
    # Max on 2nd alternate key column, equality predicate
    stmt = """prepare x from
select max(u2)
from OPTABLE 
where u1 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30 (should not see a null value)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s127')
    
    # display statistics;
    
    # ?section u8
    # Min on 3rd alternate key column, partial equality key prefix
    # (Have one row with values {10, 9, null}
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1 = 10
and u2 = 9
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get null (0 rows)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s128')
    
    # display statistics;
    
    # ?section u9
    # Min on 3rd alternate key column, partial equality prefix of key
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1 = 20
and u2 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s129')
    
    # display statistics;
    
    # ?section u10
    # Max on 3rd alternate key column, partial equality prefix of key
    stmt = """prepare x from
select max(u3)
from OPTABLE 
where u1 = 20
and u2 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s130')
    
    # display statistics;
    
    # ?section u11
    # Max on 3rd alternate key column, partial equality prefix of key
    stmt = """prepare x from
select max(u3)
from OPTABLE 
where u1 = 10
and u2 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30 (should not be NULL)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s131')
    
    # display statistics;
    
    # ?section u12
    # Min on 1st primary key column full equality prefix of alternate key
    stmt = """prepare x from
select min(p1)
from OPTABLE 
where u1 = 30
and u2 = 10
and u3 = 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30 (should not be NULL)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s132')
    
    # display statistics;
    
    # ?section u13
    # Max on 1st primary key column full equality prefix of alternate key
    stmt = """prepare x from
select max(p1)
from OPTABLE 
where u1 = 30
and u2 = 10
and u3 = 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s133')
    
    # display statistics;
    
    # ?section u14
    # Min on 2nd alternate key column, equality on 1st, > on 2nd
    stmt = """prepare x from
select min(u2)
from OPTABLE 
where u1 = 10
and u2 > 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 20
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s134')
    
    # display statistics;
    
    # ?section u15
    # Max on 2nd alternate key column, equality on 1st, > on 2nd
    stmt = """prepare x from
select max(u2)
from OPTABLE 
where u1 = 10
and u2 > 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s135')
    
    # display statistics;
    
    # ?section u16
    # Min on 2nd alternate key column, equality on 1st, < on 2nd
    stmt = """prepare x from
select min(u2)
from OPTABLE 
where u1 = 10
and u2 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 9
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s136')
    
    # display statistics;
    
    # ?section u17
    # Max on 2nd alternate key column, equality on 1st, < on 2nd
    stmt = """prepare x from
select max(u2)
from OPTABLE 
where u1 = 10
and u2 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s137')
    
    # display statistics;
    
    # ?section u18
    # Min on 3rd alternate key column, equality on 1st and 2nd,
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1 = 10
and u2 = 30
and u3 > 0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s138')
    
    # display statistics;
    
    # ?section u19
    # Max on 3rd alternate key column, equality on 1st and 2nd,
    stmt = """prepare x from
select max(u3)
from OPTABLE 
where u1 = 10
and u2 = 30
and u3 > 0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s139')
    
    # display statistics;
    
    # ?section u20
    # Min on 3rd alternate key column, equality on 1st and 2nd,
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1 = 10
and u2 = 30
and u3 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s140')
    
    # display statistics;
    
    # ?section u21
    # Max on 3rd alternate key column, equality on 1st and 2nd,
    stmt = """prepare x from
select max(u3)
from OPTABLE 
where u1 = 10
and u2 = 30
and u3 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s141')
    
    # display statistics;
    
    # ?section u22
    # Min on 1st alternate key column, range scan
    stmt = """prepare x from
select min(u1)
from OPTABLE 
where u1 > 10
and u1 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 20
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s142')
    
    # display statistics;
    
    # ?section u23
    # Max on 1st alternate key column, range scan
    stmt = """prepare x from
select max(u1)
from OPTABLE 
where u1 > 10
and u1 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s143')
    
    # display statistics;
    
    # ?section u24
    # Min on 1st alternate key column, range scan
    stmt = """prepare x from
select min(u1)
from OPTABLE 
where u1,u2,u3 > 10,20,30
and u1,u2,u3 < 30,20,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s144')
    
    # display statistics;
    
    # ?section u25
    # Max on 1st alternate key column, range scan
    stmt = """prepare x from
select max(u1)
from OPTABLE 
where u1,u2,u3 > 10,20,30
and u1,u2,u3 < 30,20,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s145')
    
    # display statistics;
    
    # ?section u26
    # Min on 1st alternate key column, range scan
    stmt = """prepare x from
select min(u1)
from OPTABLE 
where u1,u2,u3 > 10,20,30
and u1,u2,u3 < 30,20,30
and  c1 = 'b'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 20
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s146')
    
    # display statistics;
    
    # ?section u27
    # Max on 1st alternate key column, range scan
    stmt = """prepare x from
select max(u1)
from OPTABLE 
where u1,u2,u3 > 10,20,30
and u1,u2,u3 < 30,20,30
and c1 = 'c'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s147')
    
    # display statistics;
    
    # ?section u28
    # Min on 3rd alternate key column, full equality prefix
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1,u2,u3,p1,p2,p3 = 10,30,30,10,30,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s148')
    
    # display statistics;
    
    # ?section u29
    # Min on 3rd alternate key column, full equality prefix
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1,u2,u3 = 10,30,30
and p1,p2,p3 = 10,30,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s149')
    
    #  display statistics;
    
    #  Case 4) 1st Asc, 2nd Desc, 3rd Desc
    
    stmt = """drop index iuaaa;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuaad;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuada;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuadd;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudaa;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudad;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudda;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuddd;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index iuadd on OPTABLE(U1 asc, u2 desc, u3 desc)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # ?section u1
    # Min on 1st alternate key column, unbounded scan (no keys)
    stmt = """prepare x from
select min(u1)
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s157')
    
    # display statistics;
    
    # ?section u2
    # Min on 1st alternate key column, unbounded scan (no keys)
    stmt = """prepare x from
select max(u1)
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s158')
    
    # display statistics;
    
    # ?section u3
    # Max on 1st alternate key column, unbounded scan
    stmt = """prepare x from
select max(u1)
from OPTABLE 
where u1 > 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30 (should not see null)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s159')
    
    # display statistics;
    
    # ?section u4
    # Min on 1st alternate key column, equality predicate
    stmt = """prepare x from
select min(u1)
from OPTABLE 
where u1 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s160')
    
    # display statistics;
    
    # ?section u5
    # Max on 1st alternate key column, equality predicate
    stmt = """prepare x from
select max(u1)
from OPTABLE 
where u1 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s161')
    
    # display statistics;
    
    # ?section u6
    # Min on 2nd alternate key column, equality predicate
    stmt = """prepare x from
select min(u2)
from OPTABLE 
where u1 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 9
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s162')
    
    # display statistics;
    
    # ?section u7
    # Max on 2nd alternate key column, equality predicate
    stmt = """prepare x from
select max(u2)
from OPTABLE 
where u1 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30 (should not see a null value)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s163')
    
    # display statistics;
    
    # ?section u8
    # Min on 3rd alternate key column, partial equality key prefix
    # (Have one row with values {10, 9, null}
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1 = 10
and u2 = 9
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get null (0 rows)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s164')
    
    # display statistics;
    
    # ?section u9
    # Min on 3rd alternate key column, partial equality prefix of key
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1 = 20
and u2 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s165')
    
    # display statistics;
    
    # ?section u10
    # Max on 3rd alternate key column, partial equality prefix of key
    stmt = """prepare x from
select max(u3)
from OPTABLE 
where u1 = 20
and u2 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s166')
    
    # display statistics;
    
    # ?section u11
    # Max on 3rd alternate key column, partial equality prefix of key
    stmt = """prepare x from
select max(u3)
from OPTABLE 
where u1 = 10
and u2 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30 (should not be NULL)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s167')
    
    # display statistics;
    
    # ?section u12
    # Min on 1st primary key column full equality prefix of alternate key
    stmt = """prepare x from
select min(p1)
from OPTABLE 
where u1 = 30
and u2 = 10
and u3 = 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30 (should not be NULL)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s168')
    
    # display statistics;
    
    # ?section u13
    # Max on 1st primary key column full equality prefix of alternate key
    stmt = """prepare x from
select max(p1)
from OPTABLE 
where u1 = 30
and u2 = 10
and u3 = 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s169')
    
    # display statistics;
    
    # ?section u14
    # Min on 2nd alternate key column, equality on 1st, > on 2nd
    stmt = """prepare x from
select min(u2)
from OPTABLE 
where u1 = 10
and u2 > 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 20
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s170')
    
    # display statistics;
    
    # ?section u15
    # Max on 2nd alternate key column, equality on 1st, > on 2nd
    stmt = """prepare x from
select max(u2)
from OPTABLE 
where u1 = 10
and u2 > 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s171')
    
    # display statistics;
    
    # ?section u16
    # Min on 2nd alternate key column, equality on 1st, < on 2nd
    stmt = """prepare x from
select min(u2)
from OPTABLE 
where u1 = 10
and u2 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 9
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s172')
    
    # display statistics;
    
    # ?section u17
    # Max on 2nd alternate key column, equality on 1st, < on 2nd
    stmt = """prepare x from
select max(u2)
from OPTABLE 
where u1 = 10
and u2 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s173')
    
    # display statistics;
    
    # ?section u18
    # Min on 3rd alternate key column, equality on 1st and 2nd,
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1 = 10
and u2 = 30
and u3 > 0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s174')
    
    # display statistics;
    
    # ?section u19
    # Max on 3rd alternate key column, equality on 1st and 2nd,
    stmt = """prepare x from
select max(u3)
from OPTABLE 
where u1 = 10
and u2 = 30
and u3 > 0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s175')
    
    # display statistics;
    
    # ?section u20
    # Min on 3rd alternate key column, equality on 1st and 2nd,
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1 = 10
and u2 = 30
and u3 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s176')
    
    # display statistics;
    
    # ?section u21
    # Max on 3rd alternate key column, equality on 1st and 2nd,
    stmt = """prepare x from
select max(u3)
from OPTABLE 
where u1 = 10
and u2 = 30
and u3 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s177')
    
    # display statistics;
    
    # ?section u22
    # Min on 1st alternate key column, range scan
    stmt = """prepare x from
select min(u1)
from OPTABLE 
where u1 > 10
and u1 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 20
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s178')
    
    # display statistics;
    
    # ?section u23
    # Max on 1st alternate key column, range scan
    stmt = """prepare x from
select max(u1)
from OPTABLE 
where u1 > 10
and u1 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s179')
    
    # display statistics;
    
    # ?section u24
    # Min on 1st alternate key column, range scan
    stmt = """prepare x from
select min(u1)
from OPTABLE 
where u1,u2,u3 > 10,20,30
and u1,u2,u3 < 30,20,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s180')
    
    # display statistics;
    
    # ?section u25
    # Max on 1st alternate key column, range scan
    stmt = """prepare x from
select max(u1)
from OPTABLE 
where u1,u2,u3 > 10,20,30
and u1,u2,u3 < 30,20,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s181')
    
    # display statistics;
    
    # ?section u26
    # Min on 1st alternate key column, range scan
    stmt = """prepare x from
select min(u1)
from OPTABLE 
where u1,u2,u3 > 10,20,30
and u1,u2,u3 < 30,20,30
and  c1 = 'b'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 20
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s182')
    
    # display statistics;
    
    # ?section u27
    # Max on 1st alternate key column, range scan
    stmt = """prepare x from
select max(u1)
from OPTABLE 
where u1,u2,u3 > 10,20,30
and u1,u2,u3 < 30,20,30
and c1 = 'c'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s183')
    
    # display statistics;
    
    # ?section u28
    # Min on 3rd alternate key column, full equality prefix
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1,u2,u3,p1,p2,p3 = 10,30,30,10,30,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s184')
    
    # display statistics;
    
    # ?section u29
    # Min on 3rd alternate key column, full equality prefix
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1,u2,u3 = 10,30,30
and p1,p2,p3 = 10,30,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s185')
    
    #  display statistics;
    
    #  Case 5) 1st Desc, 2nd Asc, 3rd Asc
    
    stmt = """drop index iuaaa;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuaad;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuada;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuadd;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudaa;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudad;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudda;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuddd;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index iudaa on OPTABLE(U1 desc, u2 asc, u3 asc)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # ?section u1
    # Min on 1st alternate key column, unbounded scan (no keys)
    stmt = """prepare x from
select min(u1)
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s193')
    
    # display statistics;
    
    # ?section u2
    # Min on 1st alternate key column, unbounded scan (no keys)
    stmt = """prepare x from
select max(u1)
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s194')
    
    # display statistics;
    
    # ?section u3
    # Max on 1st alternate key column, unbounded scan
    stmt = """prepare x from
select max(u1)
from OPTABLE 
where u1 > 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30 (should not see null)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s195')
    
    # display statistics;
    
    # ?section u4
    # Min on 1st alternate key column, equality predicate
    stmt = """prepare x from
select min(u1)
from OPTABLE 
where u1 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s196')
    
    # display statistics;
    
    # ?section u5
    # Max on 1st alternate key column, equality predicate
    stmt = """prepare x from
select max(u1)
from OPTABLE 
where u1 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s197')
    
    # display statistics;
    
    # ?section u6
    # Min on 2nd alternate key column, equality predicate
    stmt = """prepare x from
select min(u2)
from OPTABLE 
where u1 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 9
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s198')
    
    # display statistics;
    
    # ?section u7
    # Max on 2nd alternate key column, equality predicate
    stmt = """prepare x from
select max(u2)
from OPTABLE 
where u1 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30 (should not see a null value)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s199')
    
    # display statistics;
    
    # ?section u8
    # Min on 3rd alternate key column, partial equality key prefix
    # (Have one row with values {10, 9, null}
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1 = 10
and u2 = 9
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get null (0 rows)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s200')
    
    # display statistics;
    
    # ?section u9
    # Min on 3rd alternate key column, partial equality prefix of key
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1 = 20
and u2 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s201')
    
    # display statistics;
    
    # ?section u10
    # Max on 3rd alternate key column, partial equality prefix of key
    stmt = """prepare x from
select max(u3)
from OPTABLE 
where u1 = 20
and u2 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s202')
    
    # display statistics;
    
    # ?section u11
    # Max on 3rd alternate key column, partial equality prefix of key
    stmt = """prepare x from
select max(u3)
from OPTABLE 
where u1 = 10
and u2 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30 (should not be NULL)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s203')
    
    # display statistics;
    
    # ?section u12
    # Min on 1st primary key column full equality prefix of alternate key
    stmt = """prepare x from
select min(p1)
from OPTABLE 
where u1 = 30
and u2 = 10
and u3 = 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30 (should not be NULL)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s204')
    
    # display statistics;
    
    # ?section u13
    # Max on 1st primary key column full equality prefix of alternate key
    stmt = """prepare x from
select max(p1)
from OPTABLE 
where u1 = 30
and u2 = 10
and u3 = 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s205')
    
    # display statistics;
    
    # ?section u14
    # Min on 2nd alternate key column, equality on 1st, > on 2nd
    stmt = """prepare x from
select min(u2)
from OPTABLE 
where u1 = 10
and u2 > 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 20
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s206')
    
    # display statistics;
    
    # ?section u15
    # Max on 2nd alternate key column, equality on 1st, > on 2nd
    stmt = """prepare x from
select max(u2)
from OPTABLE 
where u1 = 10
and u2 > 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s207')
    
    # display statistics;
    
    # ?section u16
    # Min on 2nd alternate key column, equality on 1st, < on 2nd
    stmt = """prepare x from
select min(u2)
from OPTABLE 
where u1 = 10
and u2 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 9
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s208')
    
    # display statistics;
    
    # ?section u17
    # Max on 2nd alternate key column, equality on 1st, < on 2nd
    stmt = """prepare x from
select max(u2)
from OPTABLE 
where u1 = 10
and u2 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s209')
    
    # display statistics;
    
    # ?section u18
    # Min on 3rd alternate key column, equality on 1st and 2nd,
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1 = 10
and u2 = 30
and u3 > 0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s210')
    
    # display statistics;
    
    # ?section u19
    # Max on 3rd alternate key column, equality on 1st and 2nd,
    stmt = """prepare x from
select max(u3)
from OPTABLE 
where u1 = 10
and u2 = 30
and u3 > 0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s211')
    
    # display statistics;
    
    # ?section u20
    # Min on 3rd alternate key column, equality on 1st and 2nd,
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1 = 10
and u2 = 30
and u3 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s212')
    
    # display statistics;
    
    # ?section u21
    # Max on 3rd alternate key column, equality on 1st and 2nd,
    stmt = """prepare x from
select max(u3)
from OPTABLE 
where u1 = 10
and u2 = 30
and u3 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s213')
    
    # display statistics;
    
    # ?section u22
    # Min on 1st alternate key column, range scan
    stmt = """prepare x from
select min(u1)
from OPTABLE 
where u1 > 10
and u1 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 20
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s214')
    
    # display statistics;
    
    # ?section u23
    # Max on 1st alternate key column, range scan
    stmt = """prepare x from
select max(u1)
from OPTABLE 
where u1 > 10
and u1 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s215')
    
    # display statistics;
    
    # ?section u24
    # Min on 1st alternate key column, range scan
    stmt = """prepare x from
select min(u1)
from OPTABLE 
where u1,u2,u3 > 10,20,30
and u1,u2,u3 < 30,20,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s216')
    
    # display statistics;
    
    # ?section u25
    # Max on 1st alternate key column, range scan
    stmt = """prepare x from
select max(u1)
from OPTABLE 
where u1,u2,u3 > 10,20,30
and u1,u2,u3 < 30,20,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s217')
    
    # display statistics;
    
    # ?section u26
    # Min on 1st alternate key column, range scan
    stmt = """prepare x from
select min(u1)
from OPTABLE 
where u1,u2,u3 > 10,20,30
and u1,u2,u3 < 30,20,30
and  c1 = 'b'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 20
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s218')
    
    # display statistics;
    
    # ?section u27
    # Max on 1st alternate key column, range scan
    stmt = """prepare x from
select max(u1)
from OPTABLE 
where u1,u2,u3 > 10,20,30
and u1,u2,u3 < 30,20,30
and c1 = 'c'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s219')
    
    # display statistics;
    
    # ?section u28
    # Min on 3rd alternate key column, full equality prefix
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1,u2,u3,p1,p2,p3 = 10,30,30,10,30,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s220')
    
    # display statistics;
    
    # ?section u29
    # Min on 3rd alternate key column, full equality prefix
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1,u2,u3 = 10,30,30
and p1,p2,p3 = 10,30,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s221')
    
    #  display statistics;
    
    #  Case 6) 1st Desc, 2nd Asc, 3rd Desc
    
    stmt = """drop index iuaaa;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuaad;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuada;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuadd;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudaa;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudad;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudda;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuddd;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index iudad on OPTABLE(U1 desc, u2 asc, u3 desc)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # ?section u1
    # Min on 1st alternate key column, unbounded scan (no keys)
    stmt = """prepare x from
select min(u1)
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s229')
    
    # display statistics;
    
    # ?section u2
    # Min on 1st alternate key column, unbounded scan (no keys)
    stmt = """prepare x from
select max(u1)
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s230')
    
    # display statistics;
    
    # ?section u3
    # Max on 1st alternate key column, unbounded scan
    stmt = """prepare x from
select max(u1)
from OPTABLE 
where u1 > 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30 (should not see null)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s231')
    
    # display statistics;
    
    # ?section u4
    # Min on 1st alternate key column, equality predicate
    stmt = """prepare x from
select min(u1)
from OPTABLE 
where u1 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s232')
    
    # display statistics;
    
    # ?section u5
    # Max on 1st alternate key column, equality predicate
    stmt = """prepare x from
select max(u1)
from OPTABLE 
where u1 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s233')
    
    # display statistics;
    
    # ?section u6
    # Min on 2nd alternate key column, equality predicate
    stmt = """prepare x from
select min(u2)
from OPTABLE 
where u1 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 9
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s234')
    
    # display statistics;
    
    # ?section u7
    # Max on 2nd alternate key column, equality predicate
    stmt = """prepare x from
select max(u2)
from OPTABLE 
where u1 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30 (should not see a null value)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s235')
    
    # display statistics;
    
    # ?section u8
    # Min on 3rd alternate key column, partial equality key prefix
    # (Have one row with values {10, 9, null}
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1 = 10
and u2 = 9
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get null (0 rows)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s236')
    
    # display statistics;
    
    # ?section u9
    # Min on 3rd alternate key column, partial equality prefix of key
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1 = 20
and u2 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s237')
    
    # display statistics;
    
    # ?section u10
    # Max on 3rd alternate key column, partial equality prefix of key
    stmt = """prepare x from
select max(u3)
from OPTABLE 
where u1 = 20
and u2 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s238')
    
    # display statistics;
    
    # ?section u11
    # Max on 3rd alternate key column, partial equality prefix of key
    stmt = """prepare x from
select max(u3)
from OPTABLE 
where u1 = 10
and u2 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30 (should not be NULL)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s239')
    
    # display statistics;
    
    # ?section u12
    # Min on 1st primary key column full equality prefix of alternate key
    stmt = """prepare x from
select min(p1)
from OPTABLE 
where u1 = 30
and u2 = 10
and u3 = 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30 (should not be NULL)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s240')
    
    # display statistics;
    
    # ?section u13
    # Max on 1st primary key column full equality prefix of alternate key
    stmt = """prepare x from
select max(p1)
from OPTABLE 
where u1 = 30
and u2 = 10
and u3 = 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s241')
    
    # display statistics;
    
    # ?section u14
    # Min on 2nd alternate key column, equality on 1st, > on 2nd
    stmt = """prepare x from
select min(u2)
from OPTABLE 
where u1 = 10
and u2 > 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 20
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s242')
    
    # display statistics;
    
    # ?section u15
    # Max on 2nd alternate key column, equality on 1st, > on 2nd
    stmt = """prepare x from
select max(u2)
from OPTABLE 
where u1 = 10
and u2 > 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s243')
    
    # display statistics;
    
    # ?section u16
    # Min on 2nd alternate key column, equality on 1st, < on 2nd
    stmt = """prepare x from
select min(u2)
from OPTABLE 
where u1 = 10
and u2 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 9
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s244')
    
    # display statistics;
    
    # ?section u17
    # Max on 2nd alternate key column, equality on 1st, < on 2nd
    stmt = """prepare x from
select max(u2)
from OPTABLE 
where u1 = 10
and u2 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s245')
    
    # display statistics;
    
    # ?section u18
    # Min on 3rd alternate key column, equality on 1st and 2nd,
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1 = 10
and u2 = 30
and u3 > 0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s246')
    
    # display statistics;
    
    # ?section u19
    # Max on 3rd alternate key column, equality on 1st and 2nd,
    stmt = """prepare x from
select max(u3)
from OPTABLE 
where u1 = 10
and u2 = 30
and u3 > 0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s247')
    
    # display statistics;
    
    # ?section u20
    # Min on 3rd alternate key column, equality on 1st and 2nd,
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1 = 10
and u2 = 30
and u3 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s248')
    
    # display statistics;
    
    # ?section u21
    # Max on 3rd alternate key column, equality on 1st and 2nd,
    stmt = """prepare x from
select max(u3)
from OPTABLE 
where u1 = 10
and u2 = 30
and u3 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s249')
    
    # display statistics;
    
    # ?section u22
    # Min on 1st alternate key column, range scan
    stmt = """prepare x from
select min(u1)
from OPTABLE 
where u1 > 10
and u1 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 20
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s250')
    
    # display statistics;
    
    # ?section u23
    # Max on 1st alternate key column, range scan
    stmt = """prepare x from
select max(u1)
from OPTABLE 
where u1 > 10
and u1 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s251')
    
    # display statistics;
    
    # ?section u24
    # Min on 1st alternate key column, range scan
    stmt = """prepare x from
select min(u1)
from OPTABLE 
where u1,u2,u3 > 10,20,30
and u1,u2,u3 < 30,20,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s252')
    
    # display statistics;
    
    # ?section u25
    # Max on 1st alternate key column, range scan
    stmt = """prepare x from
select max(u1)
from OPTABLE 
where u1,u2,u3 > 10,20,30
and u1,u2,u3 < 30,20,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s253')
    
    # display statistics;
    
    # ?section u26
    # Min on 1st alternate key column, range scan
    stmt = """prepare x from
select min(u1)
from OPTABLE 
where u1,u2,u3 > 10,20,30
and u1,u2,u3 < 30,20,30
and  c1 = 'b'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 20
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s254')
    
    # display statistics;
    
    # ?section u27
    # Max on 1st alternate key column, range scan
    stmt = """prepare x from
select max(u1)
from OPTABLE 
where u1,u2,u3 > 10,20,30
and u1,u2,u3 < 30,20,30
and c1 = 'c'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s255')
    
    # display statistics;
    
    # ?section u28
    # Min on 3rd alternate key column, full equality prefix
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1,u2,u3,p1,p2,p3 = 10,30,30,10,30,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s256')
    
    # display statistics;
    
    # ?section u29
    # Min on 3rd alternate key column, full equality prefix
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1,u2,u3 = 10,30,30
and p1,p2,p3 = 10,30,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s257')
    
    #  display statistics;
    
    #  Case 7) 1st Desc, 2nd Desc, 3rd Asc
    
    stmt = """drop index iuaaa;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuaad;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuada;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuadd;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudaa;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudad;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudda;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuddd;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index iudda on OPTABLE(U1 desc, u2 desc, u3 asc)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # ?section u1
    # Min on 1st alternate key column, unbounded scan (no keys)
    stmt = """prepare x from
select min(u1)
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s265')
    
    # display statistics;
    
    # ?section u2
    # Min on 1st alternate key column, unbounded scan (no keys)
    stmt = """prepare x from
select max(u1)
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s266')
    
    # display statistics;
    
    # ?section u3
    # Max on 1st alternate key column, unbounded scan
    stmt = """prepare x from
select max(u1)
from OPTABLE 
where u1 > 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30 (should not see null)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s267')
    
    # display statistics;
    
    # ?section u4
    # Min on 1st alternate key column, equality predicate
    stmt = """prepare x from
select min(u1)
from OPTABLE 
where u1 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s268')
    
    # display statistics;
    
    # ?section u5
    # Max on 1st alternate key column, equality predicate
    stmt = """prepare x from
select max(u1)
from OPTABLE 
where u1 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s269')
    
    # display statistics;
    
    # ?section u6
    # Min on 2nd alternate key column, equality predicate
    stmt = """prepare x from
select min(u2)
from OPTABLE 
where u1 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 9
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s270')
    
    # display statistics;
    
    # ?section u7
    # Max on 2nd alternate key column, equality predicate
    stmt = """prepare x from
select max(u2)
from OPTABLE 
where u1 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30 (should not see a null value)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s271')
    
    # display statistics;
    
    # ?section u8
    # Min on 3rd alternate key column, partial equality key prefix
    # (Have one row with values {10, 9, null}
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1 = 10
and u2 = 9
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get null (0 rows)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s272')
    
    # display statistics;
    
    # ?section u9
    # Min on 3rd alternate key column, partial equality prefix of key
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1 = 20
and u2 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s273')
    
    # display statistics;
    
    # ?section u10
    # Max on 3rd alternate key column, partial equality prefix of key
    stmt = """prepare x from
select max(u3)
from OPTABLE 
where u1 = 20
and u2 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s274')
    
    # display statistics;
    
    # ?section u11
    # Max on 3rd alternate key column, partial equality prefix of key
    stmt = """prepare x from
select max(u3)
from OPTABLE 
where u1 = 10
and u2 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30 (should not be NULL)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s275')
    
    # display statistics;
    
    # ?section u12
    # Min on 1st primary key column full equality prefix of alternate key
    stmt = """prepare x from
select min(p1)
from OPTABLE 
where u1 = 30
and u2 = 10
and u3 = 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30 (should not be NULL)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s276')
    
    # display statistics;
    
    # ?section u13
    # Max on 1st primary key column full equality prefix of alternate key
    stmt = """prepare x from
select max(p1)
from OPTABLE 
where u1 = 30
and u2 = 10
and u3 = 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s277')
    
    # display statistics;
    
    # ?section u14
    # Min on 2nd alternate key column, equality on 1st, > on 2nd
    stmt = """prepare x from
select min(u2)
from OPTABLE 
where u1 = 10
and u2 > 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 20
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s278')
    
    # display statistics;
    
    # ?section u15
    # Max on 2nd alternate key column, equality on 1st, > on 2nd
    stmt = """prepare x from
select max(u2)
from OPTABLE 
where u1 = 10
and u2 > 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s279')
    
    # display statistics;
    
    # ?section u16
    # Min on 2nd alternate key column, equality on 1st, < on 2nd
    stmt = """prepare x from
select min(u2)
from OPTABLE 
where u1 = 10
and u2 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 9
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s280')
    
    # display statistics;
    
    # ?section u17
    # Max on 2nd alternate key column, equality on 1st, < on 2nd
    stmt = """prepare x from
select max(u2)
from OPTABLE 
where u1 = 10
and u2 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s281')
    
    # display statistics;
    
    # ?section u18
    # Min on 3rd alternate key column, equality on 1st and 2nd,
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1 = 10
and u2 = 30
and u3 > 0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s282')
    
    # display statistics;
    
    # ?section u19
    # Max on 3rd alternate key column, equality on 1st and 2nd,
    stmt = """prepare x from
select max(u3)
from OPTABLE 
where u1 = 10
and u2 = 30
and u3 > 0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s283')
    
    # display statistics;
    
    # ?section u20
    # Min on 3rd alternate key column, equality on 1st and 2nd,
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1 = 10
and u2 = 30
and u3 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s284')
    
    # display statistics;
    
    # ?section u21
    # Max on 3rd alternate key column, equality on 1st and 2nd,
    stmt = """prepare x from
select max(u3)
from OPTABLE 
where u1 = 10
and u2 = 30
and u3 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s285')
    
    # display statistics;
    
    # ?section u22
    # Min on 1st alternate key column, range scan
    stmt = """prepare x from
select min(u1)
from OPTABLE 
where u1 > 10
and u1 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 20
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s286')
    
    # display statistics;
    
    # ?section u23
    # Max on 1st alternate key column, range scan
    stmt = """prepare x from
select max(u1)
from OPTABLE 
where u1 > 10
and u1 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s287')
    
    # display statistics;
    
    # ?section u24
    # Min on 1st alternate key column, range scan
    stmt = """prepare x from
select min(u1)
from OPTABLE 
where u1,u2,u3 > 10,20,30
and u1,u2,u3 < 30,20,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s288')
    
    # display statistics;
    
    # ?section u25
    # Max on 1st alternate key column, range scan
    stmt = """prepare x from
select max(u1)
from OPTABLE 
where u1,u2,u3 > 10,20,30
and u1,u2,u3 < 30,20,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s289')
    
    # display statistics;
    
    # ?section u26
    # Min on 1st alternate key column, range scan
    stmt = """prepare x from
select min(u1)
from OPTABLE 
where u1,u2,u3 > 10,20,30
and u1,u2,u3 < 30,20,30
and  c1 = 'b'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 20
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s290')
    
    # display statistics;
    
    # ?section u27
    # Max on 1st alternate key column, range scan
    stmt = """prepare x from
select max(u1)
from OPTABLE 
where u1,u2,u3 > 10,20,30
and u1,u2,u3 < 30,20,30
and c1 = 'c'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s291')
    
    # display statistics;
    
    # ?section u28
    # Min on 3rd alternate key column, full equality prefix
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1,u2,u3,p1,p2,p3 = 10,30,30,10,30,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s292')
    
    # display statistics;
    
    # ?section u29
    # Min on 3rd alternate key column, full equality prefix
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1,u2,u3 = 10,30,30
and p1,p2,p3 = 10,30,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s293')
    
    #  display statistics;
    
    #  Case 8) 1st Desc, 2nd Desc, 3rd Desc
    
    stmt = """drop index iuaaa;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuaad;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuada;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuadd;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudaa;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudad;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iudda;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index iuddd;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index iuddd on OPTABLE(U1 desc, u2 desc, u3 desc)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # ?section u1
    # Min on 1st alternate key column, unbounded scan (no keys)
    stmt = """prepare x from
select min(u1)
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s301')
    
    # display statistics;
    
    # ?section u2
    # Min on 1st alternate key column, unbounded scan (no keys)
    stmt = """prepare x from
select max(u1)
from OPTABLE 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s302')
    
    # display statistics;
    
    # ?section u3
    # Max on 1st alternate key column, unbounded scan
    stmt = """prepare x from
select max(u1)
from OPTABLE 
where u1 > 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30 (should not see null)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s303')
    
    # display statistics;
    
    # ?section u4
    # Min on 1st alternate key column, equality predicate
    stmt = """prepare x from
select min(u1)
from OPTABLE 
where u1 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s304')
    
    # display statistics;
    
    # ?section u5
    # Max on 1st alternate key column, equality predicate
    stmt = """prepare x from
select max(u1)
from OPTABLE 
where u1 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s305')
    
    # display statistics;
    
    # ?section u6
    # Min on 2nd alternate key column, equality predicate
    stmt = """prepare x from
select min(u2)
from OPTABLE 
where u1 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 9
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s306')
    
    # display statistics;
    
    # ?section u7
    # Max on 2nd alternate key column, equality predicate
    stmt = """prepare x from
select max(u2)
from OPTABLE 
where u1 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30 (should not see a null value)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s307')
    
    # display statistics;
    
    # ?section u8
    # Min on 3rd alternate key column, partial equality key prefix
    # (Have one row with values {10, 9, null}
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1 = 10
and u2 = 9
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get null (0 rows)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s308')
    
    # display statistics;
    
    # ?section u9
    # Min on 3rd alternate key column, partial equality prefix of key
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1 = 20
and u2 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s309')
    
    # display statistics;
    
    # ?section u10
    # Max on 3rd alternate key column, partial equality prefix of key
    stmt = """prepare x from
select max(u3)
from OPTABLE 
where u1 = 20
and u2 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s310')
    
    # display statistics;
    
    # ?section u11
    # Max on 3rd alternate key column, partial equality prefix of key
    stmt = """prepare x from
select max(u3)
from OPTABLE 
where u1 = 10
and u2 = 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30 (should not be NULL)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s311')
    
    # display statistics;
    
    # ?section u12
    # Min on 1st primary key column full equality prefix of alternate key
    stmt = """prepare x from
select min(p1)
from OPTABLE 
where u1 = 30
and u2 = 10
and u3 = 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30 (should not be NULL)
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s312')
    
    # display statistics;
    
    # ?section u13
    # Max on 1st primary key column full equality prefix of alternate key
    stmt = """prepare x from
select max(p1)
from OPTABLE 
where u1 = 30
and u2 = 10
and u3 = 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s313')
    
    # display statistics;
    
    # ?section u14
    # Min on 2nd alternate key column, equality on 1st, > on 2nd
    stmt = """prepare x from
select min(u2)
from OPTABLE 
where u1 = 10
and u2 > 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 20
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s314')
    
    # display statistics;
    
    # ?section u15
    # Max on 2nd alternate key column, equality on 1st, > on 2nd
    stmt = """prepare x from
select max(u2)
from OPTABLE 
where u1 = 10
and u2 > 10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s315')
    
    # display statistics;
    
    # ?section u16
    # Min on 2nd alternate key column, equality on 1st, < on 2nd
    stmt = """prepare x from
select min(u2)
from OPTABLE 
where u1 = 10
and u2 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 9
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s316')
    
    # display statistics;
    
    # ?section u17
    # Max on 2nd alternate key column, equality on 1st, < on 2nd
    stmt = """prepare x from
select max(u2)
from OPTABLE 
where u1 = 10
and u2 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s317')
    
    # display statistics;
    
    # ?section u18
    # Min on 3rd alternate key column, equality on 1st and 2nd,
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1 = 10
and u2 = 30
and u3 > 0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s318')
    
    # display statistics;
    
    # ?section u19
    # Max on 3rd alternate key column, equality on 1st and 2nd,
    stmt = """prepare x from
select max(u3)
from OPTABLE 
where u1 = 10
and u2 = 30
and u3 > 0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s319')
    
    # display statistics;
    
    # ?section u20
    # Min on 3rd alternate key column, equality on 1st and 2nd,
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1 = 10
and u2 = 30
and u3 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s320')
    
    # display statistics;
    
    # ?section u21
    # Max on 3rd alternate key column, equality on 1st and 2nd,
    stmt = """prepare x from
select max(u3)
from OPTABLE 
where u1 = 10
and u2 = 30
and u3 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s321')
    
    # display statistics;
    
    # ?section u22
    # Min on 1st alternate key column, range scan
    stmt = """prepare x from
select min(u1)
from OPTABLE 
where u1 > 10
and u1 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 20
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s322')
    
    # display statistics;
    
    # ?section u23
    # Max on 1st alternate key column, range scan
    stmt = """prepare x from
select max(u1)
from OPTABLE 
where u1 > 10
and u1 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s323')
    
    # display statistics;
    
    # ?section u24
    # Min on 1st alternate key column, range scan
    stmt = """prepare x from
select min(u1)
from OPTABLE 
where u1,u2,u3 > 10,20,30
and u1,u2,u3 < 30,20,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 10
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s324')
    
    # display statistics;
    
    # ?section u25
    # Max on 1st alternate key column, range scan
    stmt = """prepare x from
select max(u1)
from OPTABLE 
where u1,u2,u3 > 10,20,30
and u1,u2,u3 < 30,20,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s325')
    
    # display statistics;
    
    # ?section u26
    # Min on 1st alternate key column, range scan
    stmt = """prepare x from
select min(u1)
from OPTABLE 
where u1,u2,u3 > 10,20,30
and u1,u2,u3 < 30,20,30
and  c1 = 'b'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 20
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s326')
    
    # display statistics;
    
    # ?section u27
    # Max on 1st alternate key column, range scan
    stmt = """prepare x from
select max(u1)
from OPTABLE 
where u1,u2,u3 > 10,20,30
and u1,u2,u3 < 30,20,30
and c1 = 'c'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s327')
    
    # display statistics;
    
    # ?section u28
    # Min on 3rd alternate key column, full equality prefix
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1,u2,u3,p1,p2,p3 = 10,30,30,10,30,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s328')
    
    # display statistics;
    
    # ?section u29
    # Min on 3rd alternate key column, full equality prefix
    stmt = """prepare x from
select min(u3)
from OPTABLE 
where u1,u2,u3 = 10,30,30
and p1,p2,p3 = 10,30,30
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # check its plan
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  check its result, should get 30
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s329')
    
    stmt = """drop table OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test004(desc="""a05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A05
    #  Description:        Merge Join Tests
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # Description: Merge Join Tests
    #              Modified statistics to 'trick' the optimizer to
    #              choose merge join.  This script includes tests for
    #              left join, inner join, order by asc/desc, null values,
    #              and combinations of 3 table joins.  Does not test
    #              handling of datatypes.  (Tables contain one integer
    #              column only).
    #
    
    stmt = """create table ojtab1 (a int) no partition  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table ojtab2 (b int) no partition  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table ojtab3 (c int) no partition  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into ojtab1 values (0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ojtab2 values (0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ojtab3 values (0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update statistics for table ojtab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update statistics for table ojtab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update statistics for table ojtab3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from ojtab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    stmt = """select * from ojtab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
    stmt = """select * from ojtab3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    
    stmt = """delete from ojtab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """delete from ojtab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """delete from ojtab3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    # Modify statistics to fool optimizer to choose merge join
    # update basetabs set rowcount = 1000 where tablename like '%OJTAB1%';
    # update basetabs set rowcount = 1000 where tablename like '%OJTAB2%';
    # update basetabs set rowcount = 1000 where tablename like '%OJTAB3%';
    
    stmt = """prepare x from
select * from ojtab1 t1 
left join ojtab2 t2 
on a = b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """delete from ojtab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    stmt = """delete from ojtab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    stmt = """delete from ojtab3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    stmt = """select * from ojtab1 t1, ojtab2 t2 where a = b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    # should return no rows
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on a = b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    # Should return no rows
    
    stmt = """insert into ojtab1 values (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from ojtab1 t1, ojtab2 t2 where a = b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #  Should return no rows
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on a = b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
    #  Should return 1 row:  1,null
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on t1.a=t2.b left join ojtab1 t3 
on t2.b = t3.a order by t1.a, t2.b, t3.a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s4')
    # Should return 1 row:  1,null,null
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on t1.a=t2.b inner join ojtab1 t3 
on t2.b = t3.a order by t1.a, t2.b, t3.a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #  Should return no rows
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on t1.a=t2.b inner join ojtab1 t3 
on t1.a = t3.a order by t1.a, t2.b, t3.a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s5')
    # This query should perform pipelined merge join (should not sort composite)
    # Should return 1 row:  (1,?,1)
    
    stmt = """insert into ojtab2 values (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from ojtab1 t1, ojtab2 t2 where a = b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s6')
    #  Should return 1 row: 1,1
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on a = b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s7')
    #  Should return 1 row: 1,1
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on t1.a=t2.b left join ojtab1 t3 
on t2.b = t3.a order by t1.a, t2.b, t3.a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s8')
    #  Should return 1 row:  1,1,1
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on t1.a=t2.b inner join ojtab1 t3 
on t2.b = t3.a order by t1.a, t2.b, t3.a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s9')
    # Should return 1 row: 1,1,1
    
    stmt = """insert into ojtab1 values (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from ojtab1 t1, ojtab2 t2 where a = b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s10')
    #  Should return 2 rows:  1,1 and 1,1
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on a = b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s11')
    # Should return 2 rows:  1,1 and 1,1
    
    stmt = """insert into ojtab2 values (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from ojtab1 t1, ojtab2 t2 where a = b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s12')
    #  Should return 4 rows
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on a = b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s13')
    #  Should return 4 rows
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on a = b order by a desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s14')
    # Should return same 4 rows
    
    stmt = """insert into ojtab2 values (0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from ojtab1 t1, ojtab2 t2 where a = b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s15')
    #  Should return 4 rows (all 1's)
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on a = b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s16')
    #  Should return same 4 rows
    
    stmt = """select * from ojtab2 t2 left join ojtab1 t1 on b = a order by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s17')
    #  Should return 5 rows:  (4 x 1,1 + 0,?)
    
    stmt = """select * from ojtab2 t2 left join ojtab1 t1 on b = a order by b desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s18')
    #  Should return same 5 rows, reversed order
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on t1.a=t2.b left join ojtab1 t3 
on t2.b = t3.a order by t1.a, t2.b, t3.a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s19')
    #  Should return 8 rows : all 1's
    
    stmt = """select * from ojtab2 t1 left join ojtab1 t2 on t1.b=t2.a left join ojtab1 t3 
on t2.a = t3.a order by t1.b, t2.a, t3.a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s20')
    # Should return 9 rows: all 1's + (0,?,?)
    
    stmt = """insert into ojtab2 values (2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from ojtab1 t1, ojtab2 t2 where a = b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s21')
    #  Should return 4 rows: all 1's
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on a = b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s22')
    #  Should return same 4 rows
    
    stmt = """select * from ojtab2 t2 left join ojtab1 t1 on b = a order by b ,a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s23')
    #  Should return 6 rows:  4 1's + (0,?) + (2,?)
    
    stmt = """select * from ojtab2 t2 left join ojtab1 t1 on b = a order by b desc, a desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s24')
    #  Should return same 6 rows, reversed order
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on t1.a=t2.b left join ojtab1 t3 
on t2.b = t3.a order by t1.a, t2.b, t3.a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s25')
    #  Should return 8 rows: all 1's
    
    stmt = """select * from ojtab2 t1 left join ojtab1 t2 on t1.b=t2.a left join ojtab2 t3 
on t2.a = t3.b order by t1.b, t2.a, t3.b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s26')
    # Should return 10 rows: 8 1's + (0,?,?) + (2,?,?)
    
    stmt = """prepare x from
select * from ojtab2 t1 
left join
 ojtab1 t2 on t1.b = t2.a
left join
 ojtab2 t3   on t1.b = t3.b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'X'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    #  Should be a pipelined merge join: last outer join should involve only 1 sort
    
    stmt = """select * from ojtab2 t1 left join ojtab1 t2 on t1.b = t2.a left join
 ojtab2 t3   on t1.b = t3.b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s27')
    # Should return 10 rows: 8x1's + (0,?,0) + (2,?,2)
    
    stmt = """delete from ojtab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    stmt = """delete from ojtab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    
    stmt = """insert into ojtab1 values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from ojtab1 t1, ojtab2 t2 where a = b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    # Should return no rows
    
    stmt = """select * from ojtab1 t1, ojtab2 t2 where a = b order by a desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #  Should return no rows
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on a = b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s28')
    #  Should return 1 row:  (null,null)
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on a = b order by a desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s29')
    # Should return same row.
    
    stmt = """delete from ojtab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """insert into ojtab2 values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from ojtab1 t1, ojtab2 t2 where a = b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    # Should return 0 rows
    
    stmt = """select * from ojtab1 t1, ojtab2 t2 where a = b order by a desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    # Should return 0 rows
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on a = b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    # Should return 0 rows
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on a = b order by a desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    # Should return 0 rows
    
    stmt = """insert into ojtab1 values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from ojtab1 t1, ojtab2 t2 where a = b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    # Should return 0 rows
    
    stmt = """select * from ojtab1 t1, ojtab2 t2 where a = b order by a desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #  Should return 0 rows
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on a = b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s30')
    #  Should return 1 row:  null,null
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on a = b order by a desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s31')
    #  Should return 1 row: null,null
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on t1.a=t2.b left join ojtab1 t3 
on t1.a = t3.a order by t1.a, t2.b, t3.a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s32')
    # Should return 1 row:  null,null,null (pipelined join)
    
    stmt = """insert into ojtab1 values (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """delete from ojtab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """insert into ojtab2 values (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from ojtab1 t1, ojtab2 t2 where a = b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s33')
    #  Should return 1 row: 1,1
    
    stmt = """select * from ojtab1 t1, ojtab2 t2 where a = b order by a desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s34')
    #  Should return 1 row: 1,1
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on a = b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s35')
    #  Should return 2 rows: 1,1    and (?,?)
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on a = b order by a desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s36')
    # Should return 2 rows: (?,?) and (1,1)
    
    stmt = """insert into ojtab2 values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from ojtab1 t1, ojtab2 t2 where a = b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s37')
    #  Should return 1 row: 1,1
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on a = b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s38')
    #  Should return 2 rows: (1,1) and (?,?)
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on a = b order by a desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s39')
    # Should return 2 rows: (?,?) and (1,1)
    
    stmt = """delete from ojtab1 where a is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """select * from ojtab1 t1, ojtab2 t2 where a = b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s40')
    #  Should return 1 row: 1,1
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on a = b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s41')
    #  Should return 1 row: 1,1
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on a = b order by a desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s42')
    # Should return 1 row: 1,1
    
    stmt = """delete from ojtab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """delete from ojtab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    
    stmt = """insert into ojtab1 values (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ojtab1 values (2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ojtab2 values (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from ojtab1 t1, ojtab2 t2 where a = b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s43')
    #  Should return 1 row: 1,1
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on a = b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s44')
    # Should return 2 rows: 1,1  and 2,?
    
    stmt = """delete from ojtab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """insert into ojtab2 values (2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from ojtab1 t1, ojtab2 t2 where a = b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s45')
    #  Should return 1 row: 2,2
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on a = b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s46')
    #  Should return 2 rows: (1,?) and (2,2)
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on t1.a=t2.b left join ojtab1 t3 
on t2.b = t3.a order by t1.a, t2.b, t3.a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s47')
    #  Should return 2 rows: (1,?,?) and (2,2,2)
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on t1.a=t2.b left join ojtab2 t3 
on t2.b = t3.b order by t1.a, t2.b, t3.b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s48')
    # Should return 2 rows: (1,?,?) and (2,2,2)
    
    stmt = """insert into ojtab2 values (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on a = b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s49')
    # Should return 2 rows: (1,?) and (2,2)
    
    stmt = """insert into ojtab1 values (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on a = b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s50')
    # Should return 3 rows: (1,?) and (2,2) and (3,3)
    
    stmt = """insert into ojtab1 values (4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from ojtab1, ojtab2 where a=b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s51')
    #  Should return 2 rows: (2,2) and (3,3)
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on a = b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s52')
    # Should return 4 rows: (1,?) and (2,2) and (3,3) and (4,?)
    
    stmt = """insert into ojtab1 values (2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on a = b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s53')
    # Should return 5 rows: (1,?) and (2,2) and (2,2) and (3,3) and (4,?)
    
    stmt = """insert into ojtab2 values (2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on a = b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s54')
    #  Should return 7 rows: (1,?) and 4 x (2,2) and (3,3) and (4,?)
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on t1.a=t2.b left join
 ojtab1 t3  on t2.b = t3.a order by t1.a, t2.b, t3.a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s55')
    #  Should return 11 rows: (1,?,?) and 8x(2,2,2) and (3,3,3) and (4,?,?)
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on t1.a=t2.b inner join ojtab2 t3 
on t2.b = t3.b order by t1.a, t2.b, t3.b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s56')
    #  Should return 9 rows: 8 x (2,2,2) and (3,3,3)
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on t1.a=t2.b inner join ojtab1 t3 
on t2.b = t3.a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s57')
    # Should return 9 rows: 8 x (2,2,2) and (3,3,3)
    
    stmt = """insert into ojtab1 values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on a = b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s58')
    # Should return 8 rows: (1,?) and 4x(2,2) and (3,3) and (4,?) and (?,?)
    
    stmt = """insert into ojtab2 values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on a = b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s59')
    # Should return 8 rows: (1,?) and 4x(2,2) and (3,3) and (4,?) and (?,?)
    
    stmt = """insert into ojtab1 values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on a = b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s60')
    # Should return 9 rows: (1,?) and 4x(2,2) and (3,3) and (4,?) and 2x(?,?)
    
    stmt = """insert into ojtab2 values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on a = b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s61')
    #  Should return the same 9 rows
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on t1.a=t2.b left join ojtab1 t3 
on t2.b = t3.a order by t1.a, t2.b, t3.a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s62')
    #  Should return 13 rows: (1,?,?) and 8x(2,2,2) and (3,3,3) and (4,?,?)
    #                        and 2x(?,?,?)
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on t1.a=t2.b left join ojtab2 t3 
on t2.b = t3.b order by t1.a desc, t2.b desc,t3.b desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s63')
    # Should return 13 rows: (1,?,?) and 8x(2,2,2) and (3,3,3) and (4,?,?)
    #                       and 2x(?,?,?)
    
    stmt = """delete from ojtab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 7)
    stmt = """delete from ojtab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 5)
    
    stmt = """insert into ojtab1 values (0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ojtab1 values (2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ojtab1 values (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ojtab1 values (4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ojtab1 values (4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ojtab1 values (5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ojtab1 values (6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ojtab1 values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into ojtab2 values (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ojtab2 values (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ojtab2 values (4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ojtab2 values (4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ojtab2 values (5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ojtab2 values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into ojtab2 values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from ojtab1 t1, ojtab2 t2 where a=b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s64')
    #  Should return 6 rows: (3,3) 4x(4,4) (5,5)
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on a = b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s65')
    #  Should return 10 rows: (0,?) (2,?) (3,3) 4x(4,4) (5,5) (6,?) (?,?)
    
    stmt = """select * from ojtab2 t2, ojtab1 t1 where a=b order by a,b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s66')
    #  Should return 6 rows: (3,3) 4x(4,4) (5,5)
    
    stmt = """select * from ojtab2 t2 left join ojtab1 t1 on b = a order by b,a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s67')
    #  Should return 9 rows: (1,?) (3,3) 4x(4,4) (5,5) 2x(?,?)
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on t1.a=t2.b left join ojtab1 t3 
on t2.b = t3.a order by t1.a, t2.b, t3.a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s68')
    #  Should return 14 rows: (0,?,?) (2,?,?) (3,3,3) 8x(4,4,4) (5,5,5) (6,?,?)
    #                        (?,?,?)
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on t1.a=t2.b left join ojtab2 t3 
on t2.b = t3.b order by t1.a, t2.b, t3.b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s69')
    #  Should return 14 rows: (0,?,?) (2,?,?) (3,3,3) 8x(4,4,4) (5,5,5) (6,?,?)
    #                         (?,?,?)
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on t1.a=t2.b inner join ojtab1 t3 
on t2.b = t3.a order by t1.a, t2.b, t3.a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s70')
    #  Should return 10 rows: (3,3,3) 8x(4,4,4) (5,5,5)
    
    stmt = """select * from ojtab1 t1 left join ojtab2 t2 on t1.a=t2.b inner join ojtab2 t3 
on t2.b = t3.b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s71')
    # Should return 10 rows: (3,3,3) 8x(4,4,4) (5,5,5)
    
    stmt = """drop table ojtab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table ojtab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table ojtab3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test005(desc="""a06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A06
    # Description:         Merge Join tests
    #                      Includes Outer/Inner Joins with executor predicates
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # Description:  Merge Join tests
    #               Includes Outer/Inner Joins with executor predicates
    
    stmt = """create table omerg1 (a int default null,
b int default null,
c int default null) no partition
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table omerg2 (a int default null,
b int default null,
c int default null) no partition
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table omerg3 (a int default null,
b int default null,
c int default null) no partition
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into omerg1 values (0,0,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into omerg2 values (0,0,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into omerg3 values (0,0,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update  statistics for table omerg1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update  statistics for table omerg2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update  statistics for table omerg3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """delete from omerg1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """delete from omerg2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """delete from omerg3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #  Modify statistics to fool optimizer to choose merge join
    stmt = """update basetabs set rowcount = 50000 where tablename like '%OMERG1%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    stmt = """update basetabs set rowcount = 50000 where tablename like '%OMERG2%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    stmt = """update basetabs set rowcount = 50000 where tablename like '%OMERG3%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    stmt = """set param ?a 10;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?b 1;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?c 1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s from insert into omerg1 values(?a, ?b, ?c);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """set param ?a 10;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?b 10;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?c 10;"""
    output = _dci.cmdexec(stmt)
    
    # prepare s from 'insert into omerg2 values(?, ?, ?)';
    stmt = """prepare s from insert into omerg2 values(?a, ?b, ?c);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """set param ?a 10;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?b 5;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?c 1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s from insert into omerg2 values(?a, ?b, ?c);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """set param ?a 10;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?b 10;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?c 1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s from insert into omerg2 values(?a, ?b, ?c);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # prepare s from 'select * from omerg1
    # t1 left join omerg2 t2      '
    # &'                on t2.a=t1.a and t1.b<=t2.b';
    
    stmt = """prepare s from select * from omerg1 t1 left join omerg2 t2 
on t2.a=t1.a and t1.b<=t2.b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s3')
    # Should return one row with 10, 10, 10, 10, 10, 1
    
    # prepare s from 'select * from omerg2
    # t1 left join omerg1 t2      '
    # &'                on t2.a=t1.a and t2.b<=t1.b';
    stmt = """prepare s from select * from omerg2 t1 left join omerg1 t2 
on t2.a=t1.a and t2.b<=t1.b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s4')
    # Should return three rows with:
    #           10, 1,  1,  ?,  ?,  ?
    #           10, 5,  1,  ?,  ?,  ?
    #           10, 10, 1, 10, 10, 10
    
    # prepare s from 'select * from omerg2
    # t1 left join omerg1 t2      '
    # &'                on t2.a=t1.a and t2.b<=t1.b*2';
    stmt = """prepare s from select * from omerg2 t1 left join omerg1 t2 
on t2.a=t1.a and t2.b<=t1.b*2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s5')
    # Should return three rows with:
    #           10, 1,  1,  ?,  ?,  ?
    #           10, 5,  1, 10, 10, 10
    #           10, 10, 1, 10, 10, 10
    
    # prepare s from 'select * from omerg2
    # t1 left join omerg1 t2      '
    # &'                on t2.a=t1.a and t2.b>=t1.b*2';
    stmt = """prepare s from select * from omerg2 t1 left join omerg1 t2 
on t2.a=t1.a and t2.b>=t1.b*2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s6')
    # Should return three rows with:
    #           10, 1,  1, 10, 10, 10
    #           10, 5,  1, 10, 10, 10
    #           10, 10, 1,  ?,  ?,  ?
    
    # prepare s from 'select * from omerg1
    # t1 left join omerg2 t2      '
    # &'                on t2.a=t1.a and t1.b>=t2.b*2';
    stmt = """prepare s from select * from omerg1 t1 left join omerg2 t2 
on t2.a=t1.a and t1.b>=t2.b*2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s7')
    # Should return two rows with:
    #           10, 10, 10, 10, 1,  1
    #           10, 10, 10, 10, 5,  1
    
    # Try some inner joins
    # prepare s from 'select * from omerg1
    # t1 inner join omerg2 t2      '
    # &'                on t2.a=t1.a and t1.b<=t2.b';
    stmt = """prepare s from select * from omerg1 t1 inner join omerg2 t2 
on t2.a=t1.a and t1.b<=t2.b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s8')
    # Should return one row with 10, 10, 10, 10, 10, 1
    
    # prepare s from 'select * from omerg2
    # t1 inner join omerg1 t2      '
    # &'                on t2.a=t1.a and t2.b<=t1.b';
    stmt = """prepare s from select * from omerg2 t1 inner join omerg1 t2 
on t2.a=t1.a and t2.b<=t1.b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s9')
    # Should return one row with 10, 10, 1, 10, 10, 10
    
    # prepare s from 'select * from omerg2
    # t1 inner join omerg1 t2      '
    # &'                on t2.a=t1.a and t1.b*2<=t2.b';
    stmt = """prepare s from select * from omerg2 t1 inner join omerg1 t2 
on t2.a=t1.a and t1.b*2<=t2.b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    # Should return two rows with:
    #           10, 1,  1, 10, 10, 10
    #           10, 5,  1, 10, 10, 10
    
    # prepare s from 'insert into omerg3 values(?, ?, ?)';
    stmt = """set param ?a 10;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?b 5;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?c 1;"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s from insert into omerg3 values(?a, ?b, ?c);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """set param ?a 10;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?b 10;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?c 1;"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s from insert into omerg3 values(?a, ?b, ?c);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # prepare s from
    # 'select * from omerg2 t1 left join
    # omerg3 t2 on t1.b=t2.b'
    # & '       inner join omerg3 t3
    # on (t2.b=t3.a and t2.c=t3.b and t3.c=0)'-- ;
    stmt = """prepare s from
select * from omerg2 t1 
left join omerg3 t2 on t1.b=t2.b
inner join omerg3 t3  on
(t2.b=t3.a and t2.c=t3.b and t3.c=0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    # should return 0 rows
    
    stmt = """delete from omerg3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    stmt = """insert into omerg3 values (10,1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into omerg3 values (10,5,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into omerg3 values (null,10,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # prepare s from 'select * from omerg3
    # t1 inner join omerg3 t2 on t1.a=t2.a';
    
    stmt = """prepare s from select * from omerg3 t1 
inner join omerg3 t2 on t1.a=t2.a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """Select SEQ_NUM, OPERATOR, TOTAL_COST from table (explain(NULL,'S'));"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s10')
    # 4 rows should be returned:
    #           10, 1,  1, 10,  1, 1
    #           10, 1,  1, 10,  5, 1
    #           10, 5,  1, 10,  1, 1
    #           10, 5,  1, 10,  5, 1
    #
    
    stmt = """drop table omerg1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table omerg2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table omerg3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test006(desc="""a07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A07
    #  Description:        Outer Join tests for merge join
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # Description: Outer Join tests for merge join
    #
    
    # CREATE and POPULATE tables used later
    stmt = """create table oj1 (a int) no partition  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table oj2 (b int) no partition  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table oj3 (c int) no partition  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table oj4 (d int not null) no partition  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into oj1 values (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into oj1 values (2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into oj2 values (2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into oj3 values (2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into oj4 values (0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update statistics for table oj1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update statistics for table oj2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update statistics for table oj3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update statistics for table oj4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """delete from oj4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """create table oj1k (a int not null, primary key (a))  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table oj2k (b int not null, primary key (b))  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table oj3k (c int not null, primary key (c))  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into oj1k values (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into oj1k values (2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into oj2k values (2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into oj3k values (0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update statistics for table oj1k;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update statistics for table oj2k;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update statistics for table oj3k;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """delete from oj3k;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """set param ?p '1989-03-17:8:45:58.123';"""
    output = _dci.cmdexec(stmt)
    
    #  TWO TABLE OUTER JOINS
    stmt = """select * from oj1 
left join oj2 on a = b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s0')
    
    stmt = """select * from oj1 
left join oj2 on a = 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s1')
    
    stmt = """select * from oj1 
left join oj2 on b = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s2')
    
    stmt = """select * from oj1 
left join oj2 on 1 = 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s3')
    
    stmt = """select * from oj1 
left join oj2 on a = b and b is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s4')
    
    stmt = """select * from oj1 
left join oj2 on a = b where a = b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s5')
    
    stmt = """select * from oj1 
left join oj2 on a = b where a = 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s6')
    
    stmt = """select * from oj1 
left join oj2 on a = b where b = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s7')
    
    stmt = """select * from oj1k 
left join oj2k on a = 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s8')
    
    stmt = """select * from oj1k 
left join oj2k on a > 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s9')
    
    stmt = """select * from oj1k 
left join oj2k on a = b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s10')
    
    stmt = """select * from oj1k 
left join oj2k on a = b where b is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s11')
    
    stmt = """select * from oj1k 
left join oj2k on a = b and 1 = 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s12')
    
    stmt = """select * from oj1 
left join oj2 on a = b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s13')
    
    stmt = """select current from oj1 
left join oj2 on a = b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    #  3 TABLE OUTER JOINS
    stmt = """select * from oj1k 
left join oj2k on a = b
left join oj3k on b = c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s15')
    
    #  OUTER JOINS and CARTESIAN PRODUCTS
    #  select * from oj1
    #    left join oj2 on a = b, oj2;
    
    stmt = """select * from oj1 
left join oj2 t1 on a = b, oj2 t2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s16')
    
    #  select * from oj1
    #     left join oj2 on a = b, oj1
    #     left join oj2 on a = b;
    
    stmt = """select * from oj1 
left join oj2 on a = b, oj3 
left join oj4 on c = d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s17')
    
    # 12/08/06 AR added order by
    stmt = """select * from oj1 
left join oj2 
right join oj3 
left join oj4 on 1 = 1
on 1 = 1 on 1 = 1 order by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s18')
    
    #  ORDER BY and DISTINCT
    stmt = """select * from oj1 
left join oj2 on a = b order by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s19')
    
    stmt = """select * from oj1 
left join oj2 on a = b where a=1 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s20')
    
    stmt = """select * from oj1 
left join oj2 on a = b where b=2 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s21')
    
    stmt = """select * from oj1 
left join oj2 on a = b where b is null order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s22')
    
    stmt = """select * from oj1 
left join oj2 on b is null
where b is not null order by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select * from oj1 
left join oj2 on a = b order by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s23')
    
    stmt = """select * from oj1 
left join oj2 on a = b where a=1 order by 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s24')
    
    stmt = """select * from oj1 
left join oj2 on a = b where b=2 order by 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s25')
    
    stmt = """select * from oj1 
left join oj2 on a = b where b is null order by 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s26')
    
    stmt = """select * from oj1 
left join oj2 on b is null
where b is not null order by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select distinct a from oj1 
left join oj2 on a = b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s27')
    
    stmt = """select distinct b from oj1 
left join oj2 on a = b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s28')
    
    #  AGGREGATES and GROUP BYs
    stmt = """select sum(b), count(*) from oj1 
left join oj2 on a = b group by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s29')
    
    #  select * from oj1
    #   left join oj2 on count(*) = 1;
    
    #  OUTER JOINS and SUBQUERIES
    
    stmt = """select * from oj1 where a in
(select a from oj1 
left join oj2 on a = b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s30')
    
    stmt = """select * from oj1 
left join oj2 on a = b and b in
(select * from oj2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s31')
    
    stmt = """select * from oj1 
left join oj2 on a =
(select a from oj1 where a = 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s32')
    
    #  select * from oj1 where a =
    #  (select a from oj2
    #   left join oj1 on b = a);
    
    #  select * from oj1k where a =
    #  (select a from oj1k
    #  left join oj2k on a = b);
    
    stmt = """select * from oj1 
left join oj2 on a =
(select sum(a) from oj1 
left join oj2 on a = 8 where b is not null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s33')
    
    stmt = """select * from oj1 
left join oj2 on a = b where a in
(select * from oj1 where b is null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s34')
    
    # VIEWS with OUTER JOINS
    
    # drop view vt;
    
    stmt = """create view vt as
select * from oj1 
left join oj2 on a = b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s35')
    
    stmt = """select * from vt where b = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s36')
    
    # drop view v1;
    
    # drop view v2;
    
    stmt = """create view v1 as select * from oj1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create view v2 as select * from oj2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """select * from v1 left join v2 on a = b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s37')
    
    stmt = """drop view v1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view v2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # create view v1 as
    #  select * from oj1 t1
    #  left join oj1 t2 on t1.a=t2.a;
    
    # OUTER JOINS and INVOKE
    
    stmt = """drop view vt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view vt 
as select * from oj1 
left join oj4 on a = d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """invoke vt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  OUTER JOINS and UNIONS
    
    stmt = """select * from oj1 
left join oj2 on a = b
union all select * from oj1 
left join oj2 on a = b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s39')
    
    stmt = """drop view vt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table oj1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table oj2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table oj3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table oj4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table oj1k;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table oj2k;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table oj3k;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

