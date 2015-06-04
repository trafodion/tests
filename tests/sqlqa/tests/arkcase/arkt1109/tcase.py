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
    #  Test case name:     T1109:A01
    #  Description:        This test verifies the SQL Reserved Words
    #                      in DML features.
    #
    # =================== End Test Case Header  ===================
    #
    #
    # ---------------------------
    # Data setup
    # ---------------------------
    
    stmt = """delete from TAB4;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into TAB4 values ('abcd' , 'bcdef' , 'efghi', 'jkl' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    #  ---------------------------
    #  Reserved words.
    #  ---------------------------
    #       Id: RW.A        A* reserved words should give error.
    #  ---------------------------
    #  Should get error for 'at'
    stmt = """select * from TAB4 at;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3128')
    stmt = """select * from (select * from TAB4) at;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3128')
    stmt = """select at.* from (select * from TAB4) at;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3128')
    stmt = """select count(*) as at FROM TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3128')
    stmt = """select *  from (select count(*) as at FROM TAB4) dt ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3128')
    stmt = """select at from (select count(*) as n FROM TAB4) dt ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3128')
    #
    #  Derived Table just to check reality.
    stmt = """select dt.* from (select * from TAB4) dt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')
    #
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    #
    # ---------------------------
    #      Id: RW.B        B* reserved words should give error.
    # ---------------------------
    stmt = """insert into TAB4 values ('abcd' , 'bcdef' , 'efghi', 'jkl' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from TAB4 bit_length ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3128')
    stmt = """select * from TAB4 both ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select * from (select * from TAB4) both ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select by.* from (select * from TAB4) by ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #
    stmt = """select count(*) as BIT_LENGTH FROM TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3128')
    stmt = """select max(vc7) as BoTh FROM TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select count(*) as By FROM TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    #
    # ---------------------------
    #      Id: RW.C        C* reserved words should give error.
    # ---------------------------
    stmt = """insert into TAB4 values ('abcd' , 'bcdef' , 'efghi', 'jkl' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select max(vc7) as COALESCE      FROM TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select max(vc5) as CONVERT       FROM TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select max(vc3) as CORRESPONDING FROM TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    #
    # ---------------------------
    #      Id: RW.D        D* reserved words should give error.
    # ---------------------------
    stmt = """insert into TAB4 values ('abcd' , 'bcdef' , 'efghi', 'jkl' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from TAB4 deallocate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #
    stmt = """select max(vc7) as DEALLOCATE FROM TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select max(vc5) as DIAGNOSTICS FROM TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select * from
(select max(vc5) as DIAGNOSTICS FROM TAB4) dt ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select DEALLOCATE from
(select max(vc7) as DEALLOCATE) dt ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select DIAGNOSTICS from
(select max(vc5) FROM TAB4) dt(DIAGNOSTICS) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select DIAGNOSTICS from
(select max(vc5) as DIAGNOSTICS FROM TAB4) dt ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    #
    # ---------------------------
    #      Id: RW.E        E* reserved words should give error.
    # ---------------------------
    stmt = """insert into TAB4 values ('abcd' , 'bcdef' , 'efghi', 'jkl' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from TAB4 end;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3128')
    stmt = """select max(vc7) as EXECUTE FROM TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select max(vc5) as EXTRACT FROM TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    #
    # ---------------------------
    #      Id: RW.F        F* reserved words should give error.
    # ---------------------------
    stmt = """insert into TAB4 values ('abcd' , 'bcdef' , 'efghi', 'jkl' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from TAB4 full;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    #
    # ---------------------------
    #      Id: RW.I        I* reserved words should give error.
    # ---------------------------
    stmt = """insert into TAB4 values ('abcd' , 'bcdef' , 'efghi', 'jkl' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from TAB4 INTERSECT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select * from
(select max(vc7) as ISOLATION) dt ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    #
    # ---------------------------
    #      Id: RW.M        M* reserved words should give error.
    # ---------------------------
    stmt = """insert into TAB4 values ('abcd' , 'bcdef' , 'efghi', 'jkl' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from TAB4 match;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    _testmgr.testcase_end(desc)

def test002(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1109:A02
    #  Description:        This test verifies the SQL INSERT and UPDATE
    #                      features.
    #
    # =================== End Test Case Header  ===================
    #
    #
    # ---------------------------
    # Data setup.
    # ---------------------------
    
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into TAB4 values ('abcd' , 'bcdef' , 'efghi', 'jkl' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into TAB4 values ('abcx' , 'bcdey' , 'efghz', 'jkz' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select vc7 as RegNullify from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    #
    #  ---------------------------
    #  Reserved words.
    #  ---------------------------
    #       Id: RW.N        N* reserved words (NULLIF, NATURAL) should give error.
    #  ---------------------------
    stmt = """select vc7 as NULLIF from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select vc7 as NATURAL from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #
    #  ---------------------------
    #       Id: RW.O        O* reserved words (OCTET_LENGTH, OUTER, OVERLAPS) should give error.
    #  ---------------------------
    stmt = """select vc7 as OCTET_LENGTH from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3128')
    stmt = """select vc7 as OUTER from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select vc7 as OVERLAPS from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #
    #  ---------------------------
    #       Id: RW.P        P* reserved words (PAD, PARTIAL, PREPARE, POSITION) should give error.
    #  ---------------------------
    stmt = """select vc7 as PAD from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3128')
    stmt = """select vc7 as PARTIAL from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select vc7 as PREPARE from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select vc7 as POSITION from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3128')
    #
    #  ---------------------------
    #       Id: RW.R        R* reserved words (READ, RIGHT) should give error.
    #  ---------------------------
    stmt = """select vc7 as READ from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select vc7 as RIGHT from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #
    #  ---------------------------
    #       Id: RW.S        S* reserved words (SIZE, SUBSTRING) should give error.
    #  ---------------------------
    stmt = """select vc7 as SIZE from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select vc7 as SUBSTRING from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3128')
    #
    #  ---------------------------
    #       Id: RW.T        T* reserved words (THEN, TRAILING, TRANSACTION, TRIM) should give error.
    #  ---------------------------
    stmt = """select vc7 as THEN from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select vc7 as TRAILING from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select vc7 as TRANSACTION from TAB order by 14 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select vc7 as TRIM from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3128')
    #
    #  ---------------------------
    #       Id: RW.U        U* reserved words (UNION, UPPER, USING) should give error.
    #  ---------------------------
    stmt = """select vc7 as UNION from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select vc7 as UPPER from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3128')
    stmt = """select vc7 as USING from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #
    #  ---------------------------
    #       Id: RW.V        V* reserved words (VALUE, VALUES) should give error.
    #  ---------------------------
    stmt = """select vc7 as VALUE from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select vc7 as VALUES from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #
    #  ---------------------------
    #       Id: RW.W        W* reserved words (WHEN, WRITE) should give error.
    #  ---------------------------
    stmt = """select vc7 as WHEN from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select vc7 as WRITE from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #
    stmt = """select a from TAB4 when order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #
    #  First select should work and the second should be an error.
    stmt = """select * from (
select vc7 from TAB4 
union all
select vc5 from TAB4 
) t1
, ( select vc3 from TAB4 ) t2
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s26')
    stmt = """select * from (
select vc7 from TAB4 
union all
select vc5 from TAB4 
) t1
, ( select vc3 from TAB4 ) write
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #  At end, attempt to alter contents of table
    stmt = """insert into TAB4 (vc9, vc7)
select * from (
select vc7 from TAB4 
union all
select vc5 from TAB4 
) t1
, ( select vc3 from TAB4 ) when
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select * from TAB4 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s29')
    #
    # ---------------------------
    # Data cleanup.
    # ---------------------------
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    
    _testmgr.testcase_end(desc)

def test003(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1109:A03
    #  Description:        This test verifies the SQL Reserved Words
    #                      with params in DML features.
    #
    # =================== End Test Case Header  ===================
    #
    #
    # ---------------------------
    # Data setup
    # ---------------------------
    
    stmt = """delete from TAB4;"""
    output = _dci.cmdexec(stmt)
    
    # ---------------------------
    # Reserved words and parameters.
    # ---------------------------
    #      Id: RW.A        A* parameter names.
    # ---------------------------
    stmt = """insert into TAB4 values ('abcd' , 'bcdef' , 'efghi', 'jkl' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # Ok for for 'at' as param.
    stmt = """set param ?at 'a' ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into TAB4 values (?at , ?at , '', ?at||?at ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select cast(?at as varchar(3)) as c_at
, * from TAB4 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s0')
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    #
    # ---------------------------
    #      Id: RW.B        B* parameter names.
    # ---------------------------
    stmt = """insert into TAB4 values ('abcd' , 'bcdef' , 'efghi', 'jkl' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """set param ?BIT_LENGTH  'a'  ;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?BOTH       'b' ;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?BY         'c' ;"""
    output = _dci.cmdexec(stmt)
    #
    stmt = """insert into TAB4 values (?BIT_LENGTH , ?BOTH , ?BY, ?BY ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select count(*) FROM TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    #
    # ---------------------------
    #      Id: RW.C        C* parameter names.
    # ---------------------------
    stmt = """insert into TAB4 values ('abcd' , 'bcdef' , 'efghi', 'jkl' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """set param ?CASE        'a' ;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?CAST        'b';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?COALESCE    'c' ;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?CONVERT     'd' ;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?CORRESPONDING 'e' ;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?CROSS         'f' ;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?CURRENT_DATE  'g' ;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?CURRENT_TIME  'h' ;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?CURRENT_TIMESTAMP 'i' ;"""
    output = _dci.cmdexec(stmt)
    #
    stmt = """insert into TAB4 (vc9, vc3) values (?CASE, ?CROSS) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into TAB4 values (?CASE, ?CAST, ?COALESCE, ?CONVERT) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into TAB4 values (?CORRESPONDING, ?CROSS, ?CURRENT_DATE, ?CURRENT_TIME) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into TAB4 values (?CURRENT_TIMESTAMP, ?CASE , ?CAST , ?CASE ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * FROM TAB4 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 5)
    #
    # ---------------------------
    #      Id: RW.D        D* parameter names.
    # ---------------------------
    stmt = """set param ?DEALLOCATE 'a' ;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?DIAGNOSTICS 'a' ;"""
    output = _dci.cmdexec(stmt)
    #
    stmt = """insert into TAB4 (vc9,vc5) values (?DEALLOCATE, 'b' );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into TAB4 (vc9,vc5) values ('c' , ?DIAGNOSTICS);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * FROM TAB4 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s3')
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    #
    # ---------------------------
    #      Id: RW.E        E* parameter names.
    # ---------------------------
    stmt = """set param ?else 'a' ;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?end 'a' ;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?expect 'a' ;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?EXECUTE 'a' ;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?EXTRACT 'a' ;"""
    output = _dci.cmdexec(stmt)
    #
    stmt = """insert into TAB4 (vc9,vc7,vc5) values (?else, ?end, ?expect);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into TAB4 (vc9,vc5) values (?EXECUTE, ?EXTRACT);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * FROM TAB4 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s4')
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    #
    # ---------------------------
    #      Id: RW.F        F* parameter names.
    #      Id: RW.I        I* parameter names.
    #      Id: RW.M        M* parameter names.
    # ---------------------------
    stmt = """set param ?full 'full up' ;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?IMMEDIATE 'immediate' ;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?match 'matching' ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into TAB4 (vc9, vc7) values (?IMMEDIATE, ?full);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into TAB4 (vc9, vc7) values (?match , ?full);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select vc9
, cast(?full as varchar(3)) as c_full
, vc7 from TAB4 
order by vc9
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    #
    # ---------------------------
    #      Id: RW.P        Sample of subset of P* reserved words (PAD, PARTIAL, PREPARE, POSITION).
    #      Id: RW.W        Sample of subset of W* reserved words (WHEN, WRITE).
    # ---------------------------
    stmt = """set param ?pad 'lily' ;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?when 'pad' ;"""
    output = _dci.cmdexec(stmt)
    #
    stmt = """insert into TAB4 (vc9,vc7,vc5) values (?pad , ?when , ?pad );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    stmt = """select * FROM TAB4 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s6')
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    _testmgr.testcase_end(desc)

def test004(desc="""a04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1109:A04
    #  Description:        This test verifies the SQL DML Reserved Words
    #                      in DDL creates.
    #
    # =================== End Test Case Header  ===================
    #
    #
    #  ---------------------------
    #  Catalog name.
    #  ---------------------------
    #  Should get error for 'at' as name.
    # ERROR[3128] AT is a reserved word.  It must be delimited by double-quotes
    # to be used as an identifier.
    stmt = """create catalog at;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    _dci.expect_error_msg(output, '3128')
    #
    # If reserved word is delimited by double-quotes, should be a legal identifier.
    # Save this catalog temporarily for use with 'create schema' below.
    
    stmt = """create catalog "at";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  ---------------------------
    #  Schema name.
    #  ---------------------------
    #  Should get error for use of 'at' or 'by' as name.
    stmt = """create schema by;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """create schema at.by;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3128')
    stmt = """create schema by.by;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #
    # Where reserved word is delimited by double-quotes, it's a legal identifier.
    # Otherwise it's not.
    stmt = """create schema "at"."by";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Clean up -- expect items in double-quotes to succeed and the others to fail
    # because of reserved words.
    # Drop in reverse order to Creation order.
    stmt = """drop schema "at"."by";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop schema by.by;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """drop schema at.by;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3128')
    stmt = """drop schema by;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """drop catalog "at";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop catalog at;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3128')
    #
    #  ---------------------------
    #  Table name and column name.
    #  ---------------------------
    #  Expect error for 'case' as name.
    # This is a negative test to test the keyword 'case'.  IT should fail.
    stmt = """create table case ( x int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """drop table case;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #
    #  Expect  error for 'DEALLOCATE' as name.
    stmt = """create table tempA04 ( DEALLOCATE int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """drop table tempA04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    #
    # If reserved word is delimited by double-quotes, should be a legal identifier.
    stmt = """create table """ + """\"case\"""" + """ (x int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into """ + """\"case\"""" + """ values (4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from """ + """\"case\"""" + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s12')
    stmt = """drop table """ + """\"case\"""" + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table tempA04 ( "DEALLOCATE" int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into tempA04 values (4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from tempA04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s13')
    stmt = """drop table tempA04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test005(desc="""a05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1109:A05
    #  Description:        This test verifies the SQL DML non-Reserved
    #                      keyword Words can be used as identifiers in DML
    #                      and DDL.
    #
    # =================== End Test Case Header  ===================
    #
    
    stmt = """create catalog ada;"""
    output = _dci.cmdexec(stmt)
    #
    # ---------------------------
    # Schema name.
    # ---------------------------
    # Should be ok.
    stmt = """create schema c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create schema ada.Catalog_Name;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create schema Catalog_Name;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create schema ok_with_underscore;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create schema ada.c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Clean up -- expect items in double-quotes to succeed and the others to fail
    # because of reserved words.
    stmt = """drop schema c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop schema ada.Catalog_Name;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop schema Catalog_Name;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop schema ok_with_underscore;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop schema ada.c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop catalog ada;"""
    output = _dci.cmdexec(stmt)
    #
    
    # ---------------------------
    # Table name.
    # ---------------------------
    # Should be ok.
    stmt = """create table Character_Set_Catalog ( x int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """INSERT INTO Character_Set_Catalog  VALUES (2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """SELECT * FROM Character_Set_Catalog ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    stmt = """drop table Character_Set_Catalog ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table ok_with_underscore ( x int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """INSERT INTO ok_with_underscore VALUES (2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """SELECT * FROM ok_with_underscore ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
    stmt = """drop table ok_with_underscore ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # ---------------------------
    # Column name.
    # ---------------------------
    # Should be ok.
    stmt = """create table tempA05 ( CHARACTER_SET_SCHEMA int
, CLASS_ORIGIN INT
, COBOL INT
, COLLATION_CATALOG INT
, COLLATION_NAME INT
, COLLATION_SCHEMA INT
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """INSERT INTO tempA05 VALUES (1,2,3,4,5,6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """SELECT * FROM tempA05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    stmt = """drop table tempA05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """create table tempA05 ( CLASS_ORIGIN INT ) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """INSERT INTO tempA05 VALUES (2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """SELECT * FROM tempA05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
    stmt = """drop table tempA05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """create table tempA05 ( COBOL INT ) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """INSERT INTO tempA05 VALUES (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """SELECT * FROM tempA05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s4')
    stmt = """drop table tempA05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """create table tempA05 ( COLLATION_CATALOG INT ) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """INSERT INTO tempA05 VALUES (4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """SELECT * FROM tempA05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s5')
    stmt = """drop table tempA05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """create table tempA05 ( COLLATION_NAME INT ) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """INSERT INTO tempA05 VALUES (5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """SELECT * FROM tempA05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s6')
    stmt = """drop table tempA05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """create table tempA05 ( COLLATION_SCHEMA INT ) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """INSERT INTO tempA05 VALUES (6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """SELECT * FROM tempA05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s7')
    stmt = """drop table tempA05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # ---------------------------
    # Correlation names
    # ---------------------------
    stmt = """create table tempA05 ( goodName INT ) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """INSERT INTO tempA05 VALUES (6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    #  Table Correlation name
    stmt = """SELECT goodName FROM tempA05 COLUMN_NAME ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s8')
    stmt = """SELECT goodName FROM tempA05 COMMAND_FUNCTION;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s9')
    stmt = """SELECT goodName FROM tempA05 COMMITTED;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s10')
    stmt = """SELECT goodName FROM tempA05 CONDITION_NUMBER ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s11')
    stmt = """SELECT goodName FROM tempA05 CONNECTION_NAME ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s12')
    stmt = """SELECT goodName FROM tempA05 CONSTRAINT_CATALOG ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s13')
    stmt = """SELECT goodName FROM tempA05 CONSTRAINT_NAME ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s14')
    stmt = """SELECT goodName FROM tempA05 CONSTRAINT_SCHEMA ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s15')
    stmt = """SELECT goodName FROM tempA05 CURSOR_NAME ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s16')
    stmt = """SELECT goodName FROM tempA05 data;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s17')
    stmt = """SELECT goodName FROM tempA05 DATETIME_INTERVAL_CODE ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s18')
    stmt = """SELECT goodName FROM tempA05 DATETIME_INTERVAL_PRECISION ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s19')
    stmt = """SELECT goodName FROM tempA05 DYNAMIC_FUNCTION ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s20')
    stmt = """SELECT goodName FROM tempA05 FORTRAN;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s21')
    stmt = """SELECT goodName FROM tempA05 LENGTH;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s22')
    stmt = """SELECT goodName FROM tempA05 MESSAGE_LENGTH ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s23')
    stmt = """SELECT goodName FROM tempA05 MESSAGE_OCTET_LENGTH ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s24')
    #
    #  Derived column name
    stmt = """SELECT goodName MESSAGE_TEXT FROM tempA05 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s25')
    stmt = """SELECT goodName MORE         FROM tempA05 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s26')
    stmt = """SELECT goodName MUMP         FROM tempA05 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s27')
    stmt = """SELECT goodName NAME         FROM tempA05 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s28')
    stmt = """SELECT goodName NULLABLE     FROM tempA05 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s29')
    stmt = """SELECT goodName NUMBER       FROM tempA05 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s30')
    stmt = """SELECT goodName pascal       FROM tempA05 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s31')
    stmt = """SELECT goodName PL1          FROM tempA05 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s32')
    stmt = """SELECT goodName REPEATABLE   FROM tempA05 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s33')
    stmt = """SELECT goodName RETURNED_LENGTH FROM tempA05 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s34')
    stmt = """SELECT goodName RETURNED_OCTET_LENGTH FROM tempA05 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s35')
    stmt = """SELECT goodName RETURNED_SQLSTATE FROM tempA05 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s36')
    stmt = """SELECT goodName ROWCOUNT     FROM tempA05 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s37')
    stmt = """SELECT goodName SCALE        FROM tempA05 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s38')
    stmt = """SELECT goodName SCHEMA_NAME  FROM tempA05 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s39')
    stmt = """SELECT goodName SERIALIZABLE FROM tempA05 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s40')
    stmt = """SELECT goodName SERVER_NAME  FROM tempA05 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s41')
    stmt = """SELECT goodName SUBCLASS_ORIGIN FROM tempA05 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s42')
    stmt = """SELECT goodName uncommitted  FROM tempA05 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s43')
    stmt = """SELECT goodName UNNAMED      FROM tempA05 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s44')
    #
    # ---------------------------
    # Data cleanup.
    # ---------------------------
    stmt = """drop table tempA05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #             End of test case ARKT1109
    
    _testmgr.testcase_end(desc)

