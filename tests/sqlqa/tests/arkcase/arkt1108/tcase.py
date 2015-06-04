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
    #  Test case name:     T1108:A01
    #                      .... as a function of select, with different
    #                      locking for the select part and the update part.
    #
    # =================== End Test Case Header  ===================
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into TAB1 values
('c') , ('d')
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    stmt = """select * from TAB1 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    stmt = """insert into TAB4 values
('abcd' , 'bcdef' , 'efghi', 'jkl' ),
('2bcd' , '2cdef' , '2fghi', '2kl' ),
('3bcd' , '3cdef' , '3fghi', '3kl' )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)
    stmt = """select * from TAB4 
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # ---------------------------
    #      Locking: Different locking for tables in SELECT -- one user.
    # ---------------------------
    #
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  Expect ('c') , ('d')
    stmt = """select *
from TAB1 t1 FOR READ UNCOMMITTED ACCESS
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    #
    #  Expect ('c' 'c') , ('c' 'd') , ('d' 'c') , ('d' 'd')
    stmt = """select * from
(select vc from TAB1 FOR READ UNCOMMITTED ACCESS) as tsa,
(select vc from TAB1 READ COMMITTED ACCESS) as trua
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  Expect ('2fghi' '2fghi') , ('2fghi' '3fghi') , ('2fghi' 'efghi') ,
    #         ('3fghi' '2fghi') , ('3fghi' '3fghi') , ('3fghi' 'efghi') ,
    #         ('efghi' '2fghi') , ('efghi' '3fghi') , ('efghi' 'efghi')
    stmt = """select * from
(select vc5 from TAB4 READ UNCOMMITTED ACCESS) as tsa,
(select vc5 from TAB4 FOR SERIALIZABLE ACCESS) as trua
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  Expect 3 rows as inserted above.
    stmt = """select *
from TAB4 READ COMMITTED ACCESS
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    #  Expect ('2fghi' '2fghi') , ('2fghi' '3fghi') , ('2fghi' 'efghi') ,
    #         ('3fghi' '2fghi') , ('3fghi' '3fghi') , ('3fghi' 'efghi') ,
    #         ('efghi' '2fghi') , ('efghi' '3fghi') , ('efghi' 'efghi')
    stmt = """select * from
(select vc5 from TAB4 FOR READ COMMITTED ACCESS) as tsa,
(select vc5 from TAB4 FOR READ UNCOMMITTED ACCESS) as trua
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')
    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  Reality check -- expect 6 rows from view.
    #  ( 'AA' 'BA' 'BA' ), ( 'BA' 'AA' 'AA' ), ( 'BA' 'AA' 'AA' )
    #  ( 'DA' 'EA' null ), ( null 'BA' 'BA' ), ( null 'DA' 'DA' )
    stmt = """select c2, c3, c4 from VNRead5 
order by 1,2,3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s7')
    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  Expect 36 rows, the cross-product of the view.
    stmt = """select * from
(select c2,c4 from VNRead5 READ COMMITTED ACCESS) as tsa,
(select c3 from VNRead5 SERIALIZABLE ACCESS) as trua
order by 1,2,3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s8')
    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  Expect 4 rows, the cross-product.
    stmt = """select * from
(select vc from TAB1 FOR SERIALIZABLE ACCESS) as tsa,
(select vc from TAB1 FOR READ COMMITTED ACCESS) as trua
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s9')
    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  Expect 6 rows from view.
    stmt = """select *
from VNRead5 FOR SERIALIZABLE ACCESS
order by 1,3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s10')
    #  Expect 36 rows from cross-product of views.
    stmt = """select * from
(select c2 from VNRead5 FOR SERIALIZABLE ACCESS) as tsa,
(select c3 from VNRead5 FOR READ UNCOMMITTED ACCESS) as trua
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s11')
    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Same table, same column, table expressions each with different
    # access options:
    #
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  Expect 8 rows, the cross-product of 3 2-row tables.
    stmt = """select * from (select * from TAB1 FOR READ COMMITTED ACCESS) as trca,
(select * from TAB1 FOR SERIALIZABLE ACCESS) as tsa,
(select * from TAB1 FOR READ UNCOMMITTED ACCESS) as trua
order by 1,2,3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s12')
    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  Expect 27 rows, the cross-product of 3 3-row tables.
    stmt = """select * from (select vc5 from TAB4 FOR READ COMMITTED ACCESS) as trca,
(select vc5 from TAB4 FOR SERIALIZABLE ACCESS) as tsa,
(select vc5 from TAB4 FOR READ UNCOMMITTED ACCESS) as trua
order by 1,2,3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s13')
    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  Expect 27 rows, the cross-product of 3 3-row tables.
    stmt = """select trca.*,tsa.*,trua.* from
(select vc5 from TAB4 FOR READ COMMITTED ACCESS) as trca,
(select vc5 from TAB4 FOR SERIALIZABLE ACCESS) as tsa,
(select vc5 from TAB4 FOR READ UNCOMMITTED ACCESS) as trua
order by 1,2,3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s14')
    #  Expect 8 rows, the cross-product of 3 2-row tables.
    stmt = """select * from (select * from TAB1) as trca,
(select * from TAB1 ) as tsa,
(select * from TAB1 ) as trua
order by 1,2,3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s15')
    stmt = """select * from TAB1 trca, TAB1 tsa, TAB1 trua
order by 1,2,3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s16')
    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # ---------------------------
    #
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)
    stmt = """delete from TAB1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    
    _testmgr.testcase_end(desc)

def test002(desc="""n01"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1108:N01
    #                      .... as a function of select, with different
    #                      locking for the select part and the update part.
    #
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into TAB1 values
('c') , ('d')
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    stmt = """select * from TAB1 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s0')
    stmt = """insert into TAB4 values
('abcd' , 'bcdef' , 'efghi', 'jkl' ),
('2bcd' , '2cdef' , '2fghi', '2kl' ),
('3bcd' , '3cdef' , '3fghi', '3kl' )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)
    stmt = """select * from TAB4 
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s1')
    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # ---------------------------
    #      Locking: Different locking for tables in SELECT -- one user.
    # ---------------------------
    #
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """select t1.vc9, t2.vc7, t3.vc5
from TAB4 t1 FOR READ UNCOMMITTED ACCESS,
 TAB4 t2 FOR READ COMMITTED ACCESS,
 TAB4 t3 FOR SERIALIZABLE ACCESS
order by 1,2,3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """prepare s from
select t1.vc9, t2.vc7, t3.vc5
from -- TAB4 t1 FOR READ UNCOMMITTED ACCESS,
 TAB4 t2 FOR READ COMMITTED ACCESS,
 TAB4 t3 FOR SERIALIZABLE ACCESS
order by 1,2,3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """prepare s from
select t1.vc9, t2.vc7, t3.vc5
from TAB4 t1 FOR READ UNCOMMITTED ACCESS,
-- TAB4 t2 FOR READ COMMITTED ACCESS,
 TAB4 t3 FOR SERIALIZABLE ACCESS
order by 1,2,3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """prepare s from
select t1.vc9, t2.vc7, t3.vc5
from TAB4 t1 FOR READ UNCOMMITTED ACCESS,
 TAB4 t2 FOR READ COMMITTED ACCESS,
-- TAB4 t3 FOR SERIALIZABLE ACCESS
order by 1,2,3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '29431')
    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #
    stmt = """delete from TAB4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)
    stmt = """delete from TAB1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    
    _testmgr.testcase_end(desc)

