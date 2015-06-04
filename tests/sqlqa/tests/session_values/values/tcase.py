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
    #  Description:        The purpose of this test is to test the
    #			VALUE statement executed by itself and
    #			with subquery.  Also performed together
    #			with SELECT/UPDATE/DELETE statements
    #			in the WHERE and HAVING clause.
    #
    #  Purpose:
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #
    #  Revision History:
    #      03/19/01      	Create test case.
    # =================== End Test Case Header  ===================
    
    #  Create table ;
    stmt = """create table tab1 (
char_1                    char(1)        NOT NULL
, varchar_1                 VARCHAR(2)     DEFAULT NULL
, numeric_1                 NUMERIC(4,0)   DEFAULT NULL
, pic_comp_1                PIC S9(3)V9(5) DEFAULT NULL
, medium_1                  INT            NOT NULL
, decimal_1                 DECIMAL(1,0)   DEFAULT NULL
, real_1                    real           DEFAULT NULL
, y_to_d_1                  DATE           DEFAULT NULL
, y_to_d_2                  DATE           DEFAULT NULL
, time_1                    TIME           DEFAULT NULL
, iy_to_mo                  INTERVAL YEAR(4) TO MONTH NOT NULL
, primary key (char_1, medium_1, iy_to_mo)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into tab1 values('C','FF',3000,43.405,65,4,40.4567,DATE '1997-06-12',DATE
'1997-06-13', TIME '12:40:05',INTERVAL '0-4' YEAR TO MONTH);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create table tab2 (
char_1                    char(1)        DEFAULT NULL
, varchar_1                 VARCHAR(2)     DEFAULT NULL
, numeric_1                 NUMERIC(4,0)   DEFAULT NULL
, pic_comp_1                PIC S9(3)V9(5) DEFAULT NULL
, medium_1                  INT            DEFAULT NULL
, decimal_1                 DECIMAL(1,0)   DEFAULT NULL
, real_1                    real           DEFAULT NULL
, y_to_d_1                  DATE           DEFAULT NULL
, y_to_d_2                  DATE           DEFAULT NULL
, time_1                    TIME           DEFAULT NULL
, iy_to_mo                  INTERVAL YEAR(4) TO MONTH DEFAULT NULL
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into tab2 values('A','DD',1000,23.405,45,2,10.31,DATE '1997-06-01',DATE
'1997-06-03', TIME '13:40:05',INTERVAL '2-7' YEAR TO MONTH);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into tab2 values('B','EE',2000,33.405,55,3,20.200,DATE '1997-06-06',DATE
'1997-06-03', TIME '13:00:05',INTERVAL '1-8' YEAR TO MONTH);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into tab2 values('C','FF',3000,43.405,65,4,40.4567,DATE '1997-06-12',DATE
'1997-06-13', TIME '12:40:05',INTERVAL '0-4' YEAR TO MONTH);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into tab2 values('D','AD',1000,23.405,45,2,10.31,DATE '1997-06-01',DATE
'1997-06-03', TIME '13:40:05',INTERVAL '2-7' YEAR TO MONTH);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into tab2 values('E','AE',2000,33.405,55,3,20.200,DATE '1997-06-06',DATE
'1997-06-03', TIME '13:00:05',INTERVAL '1-8' YEAR TO MONTH);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into tab2 values('F','AF',3000,43.405,65,4,40.4567,DATE '1900-06-12',DATE
'1897-06-13', TIME '02:59:59',INTERVAL '4-4' YEAR TO MONTH);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into tab2 values('G','BF',3000,43.405,65,4,40.4567,DATE '1997-06-12',DATE
'1997-06-13', TIME '12:40:05',INTERVAL '0-4' YEAR TO MONTH);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into tab2 (char_1, varchar_1) values('Z','ZE');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # Simple index:
    
    stmt = """create index indtab2 on tab2 ( char_1 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update statistics for table tab1 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update statistics for table tab2 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """values (1, 'aba', '1239', cast(cast('1239' as char(5)) as int));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s0""")
    
    stmt = """values (1, 'aba', position('39' in '1239'),
cast(cast('1239' as char(5)) as int));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s1""")
    
    stmt = """values (1, substring('aba' from 2 for 1), position('39' in '1239'),
cast(cast('1239' as char(5)) as int));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s2""")
    
    stmt = """values (1, substring('aba' from 2 for 1), position('39' in '1239'),
cast(cast('1239' as char(5)) as numeric(7, 1)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s3""")
    
    stmt = """values (1, substring('aba', 2, 2), position('9' in '1239'),
cast(cast('1239' as char(5)) as int));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s4""")
    
    stmt = """values (1, substring(upper(lcase('aba')), 2, 2), position('9' in '1239'),
cast(cast('1239' as char(5)) as int));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s5""")
    
    stmt = """select *
from tab2
where char_1 = (values (upshift('a')));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s6""")
    
    stmt = """select char_1, varchar_1, numeric_1
from tab2
group by char_1, varchar_1, numeric_1
having substring(varchar_1, 1, 1) = (values (upshift('a')));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s7""")
    
    stmt = """create table testval1
(ubin9_n4 numeric (9,0) unsigned,
ubin12_2 numeric (4,0) unsigned) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into testval1 values (1,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into testval1 values (3,4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into testval1 values (1,4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into testval1 values (2,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select ubin9_n4, ubin12_2
from testval1
where ubin9_n4 in (values(1),(2)) and ubin12_2 in (values(0),(1)) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select ubin9_n4, ubin12_2
from testval1
where ubin9_n4 in (values(1),(2)) or ubin12_2 in (values(0),(1)) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s8a""")
    
    stmt = """prepare s from select char_1, numeric_1
from tab2
group by char_1, numeric_1
having  (char_1, numeric_1) in (
values ('A', 1000), ('F', 3000), (char_1, 2000));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select char_1, numeric_1
from tab2
group by char_1, numeric_1
having (char_1, numeric_1) in
(values (char_1, 9999));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select char_1, numeric_1
from tab2
group by char_1, numeric_1
having numeric_1 in (values (1000));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s10""")
    
    stmt = """Begin work;"""
    output = _dci.cmdexec(stmt)
    
    #  Update wrong row on build MX010216.
    stmt = """update tab2 set char_1 = '1', numeric_1 = 1111
where numeric_1 in (values (1000));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    
    #  Delete wrong row on build MX010216.
    stmt = """delete from  tab2 where numeric_1 in (values (3000));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)
    
    stmt = """update tab2 set char_1 = '1', numeric_1 = 1111
where numeric_1 in (values (1000), (12345));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 0)
    
    stmt = """delete from  tab2 where numeric_1 in (values (3000), (12345));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """values ('a'), (substring(upper(lcase('aba')), 2, 2)),
((select varchar_1 from  tab1)), (cast(cast('1239' as int) as char(10))),
((select varchar_1 from tab1 where ucase(varchar_1) =
(values (substring(upper(lcase('aabbFFxxppoo')), 5, 2)))));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s11""")
    
    stmt = """values ('ABCDEFG', 991122, cast('zap' as char(15))),
((select char_1 from tab1), (select medium_1 from tab1), NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s12""")
    
    stmt = """select char_1, numeric_1
from tab2
group by char_1, numeric_1
having (char_1, numeric_1) in
(values ('aaaa', 9999));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select char_1, numeric_1, real_1
from tab2
group by char_1, numeric_1, real_1
having (char_1, numeric_1) in
(values (lcase(char_1), sin(real_1)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select char_1, numeric_1, real_1
from tab1
group by char_1, numeric_1, real_1
having (numeric_1) in (
(values (3000)),
(values (sin(real_1))));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s15""")
    
    stmt = """set param ?p 3000;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select char_1, numeric_1, real_1
from tab1
group by char_1, numeric_1, real_1
having (numeric_1) in (
(values (?p)),
(values (sin(real_1))));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s15""")
    
    stmt = """select char_1, real_1
from tab2
group by char_1, real_1
having FLOOR(POWER(COS(real_1), 2)) in (
(values (1000)),
(values (FLOOR(POWER(COS(real_1), 2)))));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s16""")
    
    stmt = """select char_1, varchar_1, real_1
from tab2
group by char_1, varchar_1, real_1
having FLOOR(POWER(COS(real_1), 2)) in (
(values (1000)),
(values (FLOOR(POWER(COS(real_1), 2))))) and
varchar_1 in (values (substring(upper(lcase('aabbFFxxppoo')), 5, 2)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s17""")
    
    stmt = """select real_1
from tab2
where real_1 = some(values(cos(real_1)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    ##expectfile ${test_dir}/a01exp a01s19
    stmt = """prepare s from
delete from tab2 where varchar_1 in (values (?), (?)) or
numeric_1 in (values(?), (?));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # regular mode deletes 2 rows, but mode1 deleles 3 rows
    stmt = """execute s using 'DD', 'af', 1000, 9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s20""")
    
    _testmgr.testcase_end(desc)

def test002(desc="""N01"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     N01
    #  Description:        Negative test for VALUES statement.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  Revision History:
    #      03/20/01      	Created.
    # =================== End Test Case Header  ===================
    
    # comment out expectfile since Mode1 is returning a different error msg
    ##expectfile ${test_dir}/n01exp n01s0
    stmt = """values (1), ((select varchar_1 from tab2));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """select varchar_1 from tab1;"""
    output = _dci.cmdexec(stmt)
    stmt = """select varchar_1 from tab2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """values ('a'), (substring(upper(lcase('aba')), 2, 2)),
((select varchar_1 from  tab1)), (cast(cast('1239' as int) as char(10))),
((select varchar_1 from tab2));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8401')
    
    # fails on mode1
    ##expectfile ${test_dir}/n01exp n01s2
    #values ('a'),
    #(substring(upper(lcase('aba')), 2, 2)),
    #((select numeric_1 from tab1));
    
    stmt = """values (1, substring(upper(lcase('aba')), 2, 2), position('9' in '1239'),
(select numeric_1, varchar_1, medium_1
from tab2));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """value ('ABCDEFG', 991122, cast('zap' as char(15))),
((select char_1 from tab1), (select medium_1 from tab1), NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select values ('ABCDEFG', 991122, cast('zap' as char(15))),
((select char_1 from tab1), (select medium_1 from tab1), NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """values (select * from tab2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """create table tbl (i1 integer, ts timestamp) no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into tbl values (6215,  timestamp '1950-03-05 08:32:09');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tbl values (28174, timestamp '1951-02-15 14:35:49');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tbl values (19058, timestamp '1955-05-18 08:40:10');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tbl values (4597,  timestamp '1960-09-19 14:40:39');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tbl values (31966, timestamp '1954-05-01 16:41:02');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """values ('a', 'b', (select * from tbl));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """values ('a', 'b', (select i1, ts from tbl where i1 = 6215));"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output)
    elif hpdci.tgtTR():
        _dci.expect_selected_msg(output, 1)
 
    stmt = """values (abc);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    #             End of test case VALUES
    _testmgr.testcase_end(desc)

