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
    # Test case name:      T1100:A01
    # Description:         This test verifies the SQL Derived table
    #                      features, with SELECT, INSERT, and UPDATE.
    #
    # =================== End Test Case Header  ===================
    
    stmt = """Delete From T1 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """Delete From T2 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """Delete From T3 ;"""
    output = _dci.cmdexec(stmt)
    
    #  ---------------------------
    #  Insert.
    #  ---------------------------
    
    stmt = """select min(c4)   as min_c4
, min (dt.c3) as min_c3
, cast(sum (n1) as integer signed) as sum_n1
, cast(max (n1) as numeric(9,2) signed) as max_n1
, min (n1) as min_n1
, avg (n1) as avg_n1
from (select * from VNA1P005) dt
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    #
    stmt = """insert into T1 
(select min(c4)
, min (dt.c3)
, sum (n1)
, max (n1)
, min (n1)
, avg (n1)
from (select * from VNA1P005) dt
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    stmt = """insert into T1 ( ch7, ch2, nint ) values ('BA', 'a', 1)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    stmt = """select max(c4)
, max (dt.c3)
, sum (n1)
from (select * from VNA1P005) dt
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    #
    stmt = """insert into T1 ( ch2, ch7, nnum9 )
( select max(c4), max (dt.c3), sum (n1)
from (select * from VNA1P005) dt
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select max(sbin0_4)
, 'jz'
, sum (dt.sdec5_10 + dt.sdec6_4 + sbin0_4)
from (select * from VNA1P006) dt
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    #
    stmt = """insert into T1 ( nint, ch7, nnum9 )
(select max(sbin0_4)
, 'jz'
, sum (dt.sdec5_10 + dt.sdec6_4 + sbin0_4)
from (select * from VNA1P006) dt
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    #  Self-insert not supported 1998-01-29.
    #  Sent: Monday, February 02, 1998 10:10 AM
    #  From: Pong, Mike
    #          There is no plan in the immediate future to support
    #          this feature. May be when we can support user define
    #          functions then we can support this feature.
    #     insert into T1 (select 'self-insert' || ch7
    #                    , ch2
    #                    , nint
    #                    , nlarge
    #                    , nnum9
    #                    , nnum4
    #                    from T1
    #                    )
    #     ;
    stmt = """select * from T1 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    #
    #  ---------------------------
    #       Id: DT.006a      DT on one base table.
    #  ---------------------------
    stmt = """select * from
(
select varchar0_500 , char2_2 , sbin7_n20 , 4002
from BTA1P008 
) dt
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    #
    #  ---------------------------
    #       Id: DT.022a      Insert from DT on columns that disallow NULL value (${arkt1100}.VUA1P001).
    #       Id: DT.022b      Insert from DT on columns that allow NULL value though none is present (${arkt1100}.VUA1P003).
    #       Id: DT.034a      Insert from DT on Union (Corresponding) view (${arkt1100}.VUA1P008)
    #       Id: DT.034b      Insert from DT's with UNION and UNION ALL
    #       Id: IN.042       Insert test using Derived Tables (cross-over test).
    #       Id: UC.82        Insert from UNION used inside DT (same test as DT.034b)
    #  ---------------------------
    #
    #  Columns that disallow NULL value (${arkt1100}.VUA1P001)
    stmt = """select
char1_4      --  PIC X(5)   not null, -- len = 2,4
, char2_2      --  PIC X(2)   not null,
, varchar5_10  --  VarChar(9) not null,  -- Made odd length
, char10_20    --  PIC X(5)   not null, -- len = 2,4
, char12_10    --  PIC X(2)   not null,
, char13_100   --  Char(5)    not null, -- len = 2,4
from VUA1P001 
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    #
    stmt = """select * from (select
char1_4      , char2_2   , varchar5_10
, char10_20    , char12_10 , char13_100
from VUA1P001 ) dt
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')
    #
    #  Columns that allow NULL value though none is present (${arkt1100}.VUA1P003).
    #  View and table have same columns.
    stmt = """select
char1_4       -- PIC X(5)   not null, -- len = 2,4
, char2_2
, varchar2_10   -- VarChar(15)   not null, -- len = 2
, varchar2_100  -- VarChar(25)   not null, -- len = 16
, char13_100    -- Char(5)   not null, -- len = 2,4
from VUA1P003 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s7')
    #
    stmt = """select * from (select
char1_4      , char2_2   , varchar2_10
, varchar2_100 , char13_100
from VUA1P003 ) dt
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s8')
    #
    # Insert into table values selected from global SQL tables
    # via DT:
    # View VNA1P008 contains Union Corresponding.
    stmt = """insert into T2 (select cast(varchar0_500 as varchar(7))
, cast(dt.char2_2 as varchar(2))
, sbin7_n20
, sbin6_nuniq
from (select * from VNA1P008) dt
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    #
    # DT contains Union -- expect no duplicate 4001's.
    stmt = """insert into T2 (select * from
(select cast(varchar0_500 as varchar(7))
, cast(char2_2 as varchar(2))
, sbin7_n20 , 4001
from BTA1P008 
union
select cast(varchar0_500 as varchar(7))
, cast(char2_2 as varchar(2))
, sbin7_n20 , 4001
from BTA1P008 
) dt
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 6)
    #
    # DT contains Union All -- expect duplicate 4002's.
    stmt = """insert into T2 (select * from
(select cast(varchar0_500 as varchar(7))
, cast(char2_2 as varchar(2))
, sbin7_n20 , 4002
from BTA1P008 
union
select cast(varchar0_500 as varchar(7))
, cast(char2_2 as varchar(2))
, sbin7_n20 , 4002
from BTA1P008 
) dt
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 6)
    #
    stmt = """select * from T2 
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s9')
    stmt = """delete from T2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 17)
    #
    # ----------------------------
    #       Id: DT.037       Insert from DT upon view containing ANSI functions.
    #  ---------------------------
    #  Check what will be inserted.
    stmt = """select cast(cLower as varchar(7))
, cast(dt.cUpper as varchar(2))
, cChar_length
, cPosition
from (select * from VNA1P007) dt
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s10')
    #
    stmt = """insert into T2 (select cast(cLower as varchar(7))
, cast(dt.cUpper as varchar(2))
, cChar_length
, cPosition
from (select * from VNA1P007) dt
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 6)
    #
    stmt = """select * from T2 
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s11')
    #
    # ---------------------------
    # Update.
    # ---------------------------
    #      Id: DT.004a      Explicit derived column name differs from underlying name.
    #      Id: DT.041a      Update/select integer Data type.
    #      Id: DT.041b      Update/select large integer Data type.
    #      Id: DT.042a      Update/select with single DT in a statement.
    #      Id: DT.042b      Update/select with Multiple DT's.
    #      Id: DI.061*      Update/select with DISTINCT and
    #                       aggregate/DISTINCT/expression inside DT.
    # ---------------------------
    # Insert (preparation for subsequent update)
    stmt = """Insert into T3 
Values ('1st orig value' ,99 , 'o'   , 1 )
, ('2nd orig value' ,98 , 'ov'  , 2 )
, ('3rd orig value' ,97 , 'ovc' , 3 )
, ('4th orig value' ,96 , 'ov ' , 4 )
, ('5th orig value' ,95 , 'o  ' , 5 )
, ('6 is short'     ,97 , 'o'   , 6 )
, ('7'              ,94 , 'OVC' , 7 )
, ('8th orig value' ,93 , 'OV'  , 8 )
, ('9th orig val  ' ,92 , 'O'   , 9 )
, ('10th val'       ,92 , 'O'   , 9 )
, ('11th val'       ,92 , 'O'   , 9 )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 11)
    stmt = """Select * From T3 Order By 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s12')
    #
    stmt = """select c from (select distinct count(distinct nint)
from T3)dt(c)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s13')
    #
    stmt = """Update T3 set nint =
(select c from (select distinct count(distinct nint)
from T3) dt(c))
where nint=99
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    #
    stmt = """Update T3 set nlarge =
(select c from
(select max(ubin6_2) from VUA1P001) dt(c))
, ch3 =
(select c from
(select max(char2_2) from VUA1P001) dt(c))
, vch15 =
(select c from
(select max(varchar0_4) from VUA1P001) dt(c))
where nint=98 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    #
    stmt = """select * from T3 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s14')
    #
    # ---------------------------
    #      Id: DT.043       Update/select, DISTINCT w/expressions, outer JOINs.
    # ---------------------------
    #
    stmt = """Update T3 set nlarge = (select c
from ( select distinct count(distinct c1 )
from ( select T1.sbinneg15_nuniq , T1.char2_2 ,
 T2.char2_2 , T3.char3_4
from BTA1P005 T1 
right join BTA1P005 T2 
on T1.char2_2   = T2.char2_2
left  join BTA1P005 T3 
on T2.char2_2   = T3.char3_4
) dt(c1,c2,c3,c4)
) dt(c) )
where nint=97
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    #
    stmt = """select distinct count(distinct c1 )
from ( select T1.sbinneg15_nuniq , T1.char2_2 ,
 T2.char2_2 , T3.char3_4
from BTA1P005 T1 
right join BTA1P005 T2 
on T1.char2_2   = T2.char2_2
left  join BTA1P005 T3 
on T2.char2_2   = T3.char3_4
) dt(c1,c2,c3,c4)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s15')
    
    stmt = """select T1.sbinneg15_nuniq , T1.char2_2 , T2.char2_2 , T3.char3_4
from BTA1P005 T1 
right join BTA1P005 T2 
on T1.char2_2   = T2.char2_2
left  join BTA1P005 T3 
on T2.char2_2   = T3.char3_4
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s16')
    stmt = """select * from T3 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s17')
    #
    #  ---------------------------
    #       Id: DT.041c      Update/select varchar Data type.
    #       Id: DT.044       Update updateable view with DT upon
    #                        view containing NATURAL JOIN.
    #  ---------------------------
    stmt = """select varchar0_uniq from VNA1P006 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s18')
    #
    stmt = """select * from VU 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s19')
    #
    stmt = """update VU set vch15 = (select max(c)
from ( select varchar0_uniq
from VNA1P006 ) dt(c)
)
where nint=96 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from VU 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s20')
    #
    # ---------------------------
    #      Id: DT.045       Update table with DT upon view containing UNION.
    # ---------------------------
    stmt = """Update T3 set vch15 = (select max(c)
from ( select varchar0_500
from VNA1P008 ) dt(c)
)
where nint=95 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from T3 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s21')
    #
    # ---------------------------
    #      Id: DT.047       Update with expressions, predicates, subqueries.
    # ---------------------------
    # (1999-02-22)  jz  Moved to arkt1100:A18
    #                   because of update error-handling failure.
    #
    # ---------------------------
    # DT with CASE.  See also testA06.
    # ---------------------------
    #      Id: DT.038       Insert data from view containing CASE.
    # ---------------------------
    # Use table created above.
    stmt = """delete from T2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 6)
    stmt = """select cast(csimple as varchar(7))
, cast(csearched as varchar(2))
, 9, 81
from VNA1P009 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 8)
    stmt = """insert into T2 
(
select * from
( select cast(csimple as varchar(7))
, cast(csearched as varchar(2))
, 9, 81
from VNA1P009 
) dt
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 8)
    stmt = """select * from T2 
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s23')
    #
    #  ---------------------------
    #  DT with ANSI functions.  See also testA06.
    #  ---------------------------
    #       Id: DT.048       Update updateable view with DT upon
    #                        view containing ANSI functions.
    #  ---------------------------
    stmt = """select cLower from VNA1P007 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s24')
    #
    stmt = """select max(c)
from ( select cLower from VNA1P007 ) dt(c)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s25')
    #
    stmt = """Update T3 Set vch15 = (Select Max( Cast( c As Char(15) ) )
from ( select cLower from VNA1P007 ) dt(c) )
where nint=93
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    #
    stmt = """select * from T3 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s26')
    #
    # ---------------------------
    #      Id: DT.049       Update updateable view with DT upon
    #                       view containing CASE.
    # ---------------------------
    # Expect 3 rows updated.
    stmt = """Update T3 set vch15 =
(select cast( max( csimple ) as char(15) )
from ( select csimple, csearched
from VNA1P009 ) dt(csearched, csimple )
-- NOTE reversal of column names in DT !!
) where nint=92 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    stmt = """select * from T3 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s27')
    #
    #  ---------------------------
    #  Grouped views within DT's
    #  ---------------------------
    #
    #  ---------------------------
    #       Id: DT.071       Group By (e.g., global view VNA1P002) in DT.
    #       Id: DT.072       Insert/Select from DT containing Group By.
    #  ---------------------------
    stmt = """select * from VNA1P002 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s28')
    stmt = """insert into T2 (nint)
( select count(*)
from (select * from VNA1P002) dt
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    stmt = """select * from T2 
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s29')
    #
    #  ---------------------------
    #       Id: DT.073       Group By Having (global view VNA1P004) in DT.
    #       Id: DT.074       Insert/Select from DT containing Group By and Having.
    #  ---------------------------
    stmt = """select * from VNA1P004 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s30')
    stmt = """insert into T2 (nint)
( select count(*)
from (select * from VNA1P004) dt
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into T2 (nint)
( select count(*)
from (select * from VNA1P004) dt
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    stmt = """select * from T2 
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s31')
    #
    # Expect 2 row updated.
    stmt = """Update T3 set vch15 =
( select upshift( cast( max( csimple ) as char(15) ) )
from ( select csimple, csearched
from VNA1P009 ) dt(csearched, csimple )
-- NOTE reversal of column names in DT !!
) where nint=97
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    stmt = """select * from T3 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s32')
    #
    #  ---------------------------
    #  Delete.
    #  ---------------------------
    #       Id: DT.051       Delete row(s), using values from DT:
    #       		See testB01 for DT.052 (Delete row(s) using DT with UNION CORRESPONDING).
    #       Id: DT.053       Delete row(s), using DT on view containing JOIN.
    #       Id: DT.054       Delete row(s) from updateable view, using DT on view containing JOIN.
    #  ---------------------------
    #       Note -- see Row Value Constructor tests for tests like:
    #       delete from tt where c = (select min(c) from tt);
    #
    #  Note that table is created and populated in pretestA01.
    stmt = """select * from TDEL 
order by rowcounter
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s33')
    #
    stmt = """select varchar5_10 from BTA1P001 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s34')
    stmt = """select min(c)
from (select varchar5_10 from BTA1P001)
dt (c)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s35')
    #
    # Delete from <table> where <column>=<subquery of derived table>.
    stmt = """delete from TDEL where ch3 =
( select min(c) from
( select varchar5_10 from BTA1P001 
) dt (c)
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    #
    stmt = """select varchar5_10 from BTA1P001 
UNION
select varchar5_10 from BTA1P001 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s36')

    stmt = """select * from VNA1P005 
order by N1, C3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s37')

    stmt = """select 'X'||min(c2) from VNA1P005 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s38')
    stmt = """select * from
(select 'X'||min(c2) from VNA1P005 
) dt (c)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s39')
    stmt = """delete from TDEL where ch3=
(select * from
(select 'X'||min(c2) from VNA1P005 
) dt
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """delete from TDEL where ch3=
(select c from
(select 'Z'||min(c2) from VNA1P005 
) dt (c)
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """select min(c2)||'Y' from VNA1P005 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s40')
    stmt = """delete from TDEL where ch3=
(select c from
(select min(c2)||'Y' from VNA1P005 
) dt (c)
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    #
    # ---------------------------
    # Clean up tables at the end.
    # ---------------------------
    stmt = """Delete From T1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    stmt = """Delete From T2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 11)
    stmt = """Delete From T3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 11)
    stmt = """Delete From TDEL ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 7)
    
    _testmgr.testcase_end(desc)

def test002(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    # Test case name:      T1100:A02
    # Description:         This test verifies the SQL Derived Table
    #                      feature via SELECT, testing in combination with
    #                      JOIN.
    #
    # =================== End Test Case Header  ===================
    #
    #
    # Force autocommit:
    stmt = """SET transaction Autocommit on;"""
    output = _dci.cmdexec(stmt)
    #
    #  ---------------------------
    #  Grouped views within DT's
    #  ---------------------------
    #
    #  ---------------------------
    #       Id: DT.001b      Named implicit derived col.
    #       Id: DT.006b      DT on one view.
    #       As tested elsewhere,  DT contains View with Group By (removes duplicates)
    #  ---------------------------
    
    stmt = """select * from VNA1P002 
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    stmt = """select char17_100
from (select * from VNA1P002) dt
group by char17_100
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    #
    #  ---------------------------
    #       Id: DT.003b      Named DT in select list of derived cols.
    #       Id: DT.004b      Qualified and unqualified names of derived cols differ from underlying derived table.
    #       Id: DT.073       DT contains View with Group By and Having; O.By
    #  ---------------------------
    stmt = """select * from VNA1P005 
order by 1, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    stmt = """select wn1, dt.xxxc2, yyc3, dt.zc4
from
(select * from VNA1P005 
) dt(wn1,xxxc2,yyc3,zc4)
order by 3, 4, 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    #
    #  ---------------------------
    #       Id: DT.004c      Select * where names of derived cols differ from those underlying derived table.
    #  ---------------------------
    stmt = """select *
from
(select * from VNA1P005 
) dt(wn1,xxxc2,yyc3,zc4)
order by 3, 4, 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s4')
    #
    #  ---------------------------
    #  Right Outer join and DT's on grouped view.
    #  ---------------------------
    #
    #  ---------------------------
    #       Id: DT.001a      Wildcarded all implicit derived col.
    #       Id: DT.091       DT contains Right Outer Joins.
    #       Id: GV.022       Inner Join on Grouped View (GROUP BY and aggregates)
    #  ---------------------------
    stmt = """select T3.*
from (select T1.c2, T1.c3, T2.c2, T2.c3, T3.char2_2, T3.char3_4
from VNA1P005 T1 
right join VNA1P005 T2 
on T1.c2 = T2.c3
right join BTA1P005 T3 
on T2.c3 = T3.char3_4
) T3 (a,b,c,d,e,f) -- Note using this name as derived table name
-- and as correlation name.
order by 1, 2, 3, 4, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')
    #
    #  ---------------------------
    #       Id: DT.003a      Named DT in wildcarded select list of derived cols.
    #       Id: DT.007       Joined 2 DT on different tables (views)
    #       Id: DT.008       Joined 2 DT made on same table (a view).
    #       Id: DT.009       Names of derived columns are same in different DT.
    #       Id: DT.010       Names of derived columns are different in different DT.
    #       Id: DT.092       Select from DT's linked by Right Outer Join.
    #  ---------------------------
    stmt = """select dta.*, dtb.*
from (select c2, c3 from VNA1P005) dta
right join (select c2, c3 from VNA1P005) dtb
on dta.c2 = dtb.c3
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s6')
    #
    stmt = """select *
from (select c2, c3 from VNA1P005) dta
right join
(select char2_2 , char3_4 from BTA1P005) dtc
on dta.c3 = dtc.char3_4
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s7')
    #
    #  Tables join.
    stmt = """select dta.char3_4, dta.sbin2_nuniq   , dtc.*
from (select * from BTA1P005) dta
right join
(select char3_4, sbin2_nuniq from BTA1P005) dtc
on dta.char3_4 = dtc.char3_4
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s8')
    #
    stmt = """select dta.*, dtb.*, dtc.*
from (select c2, c3 from VNA1P005) dta
right join (select c2, c3 from VNA1P005) dtb
on dta.c2 = dtb.c3
right join
(select char3_4, sbin2_nuniq from BTA1P005) dtc
on dtb.c3 = dtc.char3_4
order by 1, 2, 3, 4, 5, 6
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s9')
    #
    #  ---------------------------
    #  Natural join and DT's
    #  ---------------------------
    #
    #  ---------------------------
    #       Id: DT.002       DT name in select list with one col.
    #       Id: DT.096       DT contains Natural Join.
    #       Id: DT.102       Natural Join of DT.
    #       Id: GV.021       Outer Join on Grouped View (GROUP BY and aggregates)
    #       Id: JT.187a      Multiple outer joins within one derived table.
    #  ---------------------------
    #
    #  Expect (('AA' 'BA') 2* ('BA' 'AA'))
    stmt = """select c2, c3
from VNA1P005 T1 
natural join VNA1P005 T2 
natural join VNA1P005 T3 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s10')
    #
    #  Expect (('AA') ('AA') ('BA'))
    stmt = """select T3.dtc3
from (select c2, c3
from VNA1P005 T1 
natural join VNA1P005 T2 
natural join VNA1P005 T3 
) T3 ( dtc2, dtc3 )
-- Note using 't3' as derived table name
-- and as correlation name.
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s11')
    #
    #  Expect (('AA' 'BA') 4* ('BA' 'AA') ('DA' 'EA'))
    stmt = """select *
from (select c2, c3 from VNA1P005) dta
natural join (select c2, c3 from VNA1P005) dtb
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s12')
    #
    #  Expect (('AA') 8*('BA') ('DA'))
    stmt = """select c2
from (select c2, c3 from VNA1P005) dta
natural join (select c2 from VNA1P005) dtb
natural join (select c2, c3 from VNA1P005) dtc
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s13')
    #
    #  ---------------------------
    #       Id: DT.097       SELECT * from (SELECT * from NJ)
    #  ---------------------------
    #
    #  Expect 3 rows as in natural join of view without derived tables.
    stmt = """SELECT * from
(
select *
from VNA1P005 T1 
natural join VNA1P005 T2 
) dt
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s14')
    #
    #  ---------------------------
    #       Id: DT.098       SELECT col from (SELECT * from NJ)
    #  ---------------------------
    #
    #  Expect 3 rows as in natural join of view without derived tables.
    stmt = """select c2 from
(
select *
from VNA1P005 T1 
natural join VNA1P005 T2 
) dt
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s15')
    #
    #  ---------------------------
    #       Id: DT.099       SELECT col1, dt.col2 from (SELECT * from NJ) dt
    #  ---------------------------
    #
    #  Expect 3 rows as in natural join of view without derived tables.
    stmt = """select n1, dt.c3 from
(
select *
from VNA1P005 T1 
natural join VNA1P005 T2 
) dt
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s16')
    
    _testmgr.testcase_end(desc)

def test003(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    # Test case name:      T1100:A03
    # Description:         This test verifies the SQL Derived Table
    #                      feature; JOIN and transitivity.
    #
    # =================== End Test Case Header  ===================
    #
    # Catalog for 'global database #11'.
    #
    #  Select with "transitivity" between "islands".
    #  THE QUERIES BELOW ARE SCAFFOLDING TILL GET TO ISLANDS ....
    #  ---------------------------
    #
    #  JOIN/ON that set up interesting transitivity challenges
    #  through equalities between columns in DT. (See also "JOIN Tables")
    #  Code (generator/GenPreCode.C) comment says: "This is a set of values
    #  for which '=' predicates MUST be generated for correctness as well
    #  as to guarantee that transitivity is upheld. For example,
    #  the following query:
    #      select ax, bz, cx, dz
    #           from (select A.x, B.z from A join B on A.x = B.z) T1(ax,bz)
    #           join (select C.x, D.z from C join D on C.x = D.z) T2(cx,dz)
    #          on T1.ax = T2.cx
    #  shows two 'islands' (self-contained pool of rows) defined by
    #  the derived tables T1 and T2 respectively. It is possible to
    #  deduce that A.x = D.y only after the predicate A.x = C.x has
    #  been applied. The values A.x, C.x establish the transitivity
    #  between the two islands. Such values are called inter-island
    #  links or bridge values.'
    #
    #  ---------------------------
    #       Id: DT.223a     DT, JOIN/ON self-contained 'islands'.
    #  ---------------------------
    #
    
    stmt = """select T1.char2_2 from BTA1P001 T1 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s0')
    #
    stmt = """select T2.char2_2 from BTA1P005 T2 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    #
    stmt = """select ca, cb from
(select T1.char2_2 , T2.char2_2
from BTA1P001 T1 
join BTA1P005 T2 
on T1.char2_2 = T2.char2_2
) dt1(ca,cb)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    #
    stmt = """select T1.varchar2_10 from BTA1P003 T1 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s3')
    #
    stmt = """select T2.char16_n20  from BTA1P006 T2 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s4')
    #
    stmt = """select cc, cd from
(select T1.varchar2_10 , T2.char16_n20
from BTA1P003 T1 
join BTA1P006 T2 
on T1.varchar2_10 = T2.char16_n20
) dt1(cc,cd)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s5')
    #
    stmt = """select ca, cb, cc, cd from
(select T1.char2_2 , T2.char2_2
from BTA1P001 T1 
join BTA1P005 T2 
on T1.char2_2 = T2.char2_2
) dt1(ca,cb)
join
(select T1.varchar2_10 , T2.char16_n20
from BTA1P003 T1 
join BTA1P006 T2 
on T1.varchar2_10 = T2.char16_n20
) dt2(cc,cd)
on dt1.ca = dt2.cc
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s6')
    #
    #  ---------------------------
    #       Id: DT.223b     DT, JOIN/ON self-contained 'islands'; Simple ON, interesting WHERE.
    #  ---------------------------
    #
    stmt = """select ca, cb, cc, cd
from (select T1.char2_2 , T2.char2_2
from BTA1P001 T1 
join BTA1P005 T2 
on T1.char2_2 = T2.char2_2
) dt1(ca,cb)
join (select T1.varchar2_10 , T2.char16_n20
from BTA1P003 T1 
join BTA1P006 T2 
on T1.varchar2_10 = T2.char16_n20
) dt2(cc,cd)
on 1 = 1
where dt1.ca = dt2.cc
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s7')
    #
    #  ---------------------------
    #       Id: DT.223c     DT, RIGHT JOIN/ON self-contained 'islands'; ON clause with additional pred.
    #  ---------------------------
    #
    stmt = """select ca, cb from
(select T1.char2_2 , T2.char2_2
from BTA1P001 T1 
RIGHT join BTA1P005 T2 
on T1.char2_2 = T2.char2_2
) dt1(ca,cb)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s8')
    #
    stmt = """select cc, cd from
(select T1.varchar2_10 , T2.char16_n20
from BTA1P003 T1 
RIGHT join BTA1P006 T2 
on T1.varchar2_10 = T2.char16_n20
) dt1(cc,cd)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s9')
    #
    stmt = """select ca, cb, cc, cd from
(select T1.char2_2 , T2.char2_2
from BTA1P001 T1 
RIGHT join BTA1P005 T2 
on T1.char2_2 = T2.char2_2
) dt1(ca,cb)
RIGHT join
(select T1.varchar2_10 , T2.char16_n20
from BTA1P003 T1 
RIGHT join BTA1P006 T2 
on T1.varchar2_10 = T2.char16_n20
) dt2(cc,cd)
on dt1.ca = dt2.cc and 1=1
order by 1, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s10')
    #  Portions of the above query for debugging purposes --
    #  remove when SQL works.
    #  First half.
    stmt = """select ca, cb from
(select T1.char2_2 , T2.char2_2
from BTA1P001 T1 
RIGHT join BTA1P005 T2 
on T1.char2_2 = T2.char2_2
) dt1(ca,cb)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s11')
    stmt = """select T1.char2_2 , T2.char2_2
from BTA1P001 T1 
,    BTA1P005 T2 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s12')
    #
    #  Second half.
    stmt = """select * from (
select T1.varchar2_10 , T2.char16_n20
from BTA1P003 T1 
RIGHT join BTA1P006 T2 
on T1.varchar2_10 = T2.char16_n20
) dt2(cc,cd)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s13')
    stmt = """select T1.varchar2_10 , T2.char16_n20
from BTA1P003 T1 
,  BTA1P006 T2 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s14')
    #
    #  ---------------------------
    #       Id: DT.223d     DT, NATURAL JOIN; self-contained 'islands'.
    #  ---------------------------
    #
    stmt = """select char2_2
from BTA1P001 T1 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s15')
    stmt = """select char2_2
from BTA1P005 T2 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s16')
    #
    #  ---------------------------
    #  (96-12-06)  USING not supported; tests moved to testB02.
    #  ---------------------------
    #
    stmt = """select char2_2 from BTA1P003 T1 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s17')
    stmt = """select char2_2 from BTA1P006 T2 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s18')
    #
    # Need support for USING to limit columns used in NATURAL join;
    # otherwise, get 0 rows.
    
    stmt = """select char2_2 from BTA1P003 T1 
NATURAL join BTA1P006 T2 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #
    # Need support for USING to limit columns used in NATURAL join;
    # otherwise, get 0 rows.
    stmt = """select ca from
(select char2_2
from BTA1P001 T1 
NATURAL join BTA1P005 T2 
) dt1(ca)
NATURAL join
(select varchar2_10
from BTA1P003 T1 
NATURAL join BTA1P006 T2 
) dt2(ca)
-- Natural join disallows qualification by table name
-- and removes need for a WHERE clause like 'where dt1.ca = dt2.ca'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #
    #  ---------------------------
    #       Id: DT.223e     DT, JOIN/ON 'islands'; Multi-valued pred. in ON clause.
    #  ---------------------------
    #
    stmt = """select ca, cb, cc, cd from
(select T1.char2_2 , T2.char2_2
from BTA1P001 T1 
join BTA1P005 T2 
on T1.char2_2 = T2.char2_2
) dt1(ca,cb)
join
(select T1.varchar2_10 , T2.char16_n20
from BTA1P003 T1 
join BTA1P006 T2 
on T1.varchar2_10 = T2.char16_n20
) dt2(cc,cd)
on ( dt1.ca , 1 ) = (dt2.cc , 1 )
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s19')
    #
    #  With more columns and equalities, so there is more than
    #     one 'bridge' between the 'islands'.
    #  May include a combination of additional JOINs, WHERE clauses,
    #     and ON clauses.
    stmt = """select char2_2 from VUA1P001 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s20')
    stmt = """select c2, c3, c4 from VNA1P005 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s21')
    stmt = """select csubstring from VNA1P007 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s22')
    #
    stmt = """select ca, cb
from (select T1.c2 , T2.c4
from VNA1P005 T1 
join VNA1P005 T2 
on T1.c2 = T2.c4
) dt1(ca,cb)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s23')
    #
    stmt = """select cc, cd
from (select T1.char2_2 , T2.csubstring
from VUA1P001 T1 
join VNA1P007 T2 
on T1.char2_2 = T2.csubstring
) dt1(cc,cd)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s24')
    #
    stmt = """select ca, cb, cc, cd
from (select T1.c2 , T2.c4
from VNA1P005 T1 
join VNA1P005 T2 
on T1.c2 = T2.c4
) dt1(ca,cb)
join (select T1.char2_2 , T2.csubstring
from VUA1P001 T1 
join VNA1P007 T2 
on T1.char2_2 = T2.csubstring
) dt2(cc,cd)
on dt1.ca = dt2.cc
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s25')
    #
    #  Simple ON, interesting WHERE predicate.
    stmt = """select ca, cb, cc, cd
from (select T1.c2 , T2.c4
from VNA1P005 T1 
join VNA1P005 T2 
on T1.c2 = T2.c4
) dt1(ca,cb)
join (select T1.char2_2 , T2.csubstring
from VUA1P001 T1 
join VNA1P007 T2 
on T1.char2_2 = T2.csubstring
) dt2(cc,cd)
on 1 = 1
where dt1.ca = dt2.cc
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s26')
    #
    #  Interesting ON clause, with additional predicate.
    stmt = """select ca, cb, cc, cd
from (select T1.c2 , T2.c4
from VNA1P005 T1 
join VNA1P005 T2 
on T1.c2 = T2.c4
) dt1(ca,cb)
join (select T1.char2_2 , T2.csubstring
from VUA1P001 T1 
join VNA1P007 T2 
on T1.char2_2 = T2.csubstring
) dt2(cc,cd)
on dt1.ca = dt2.cc and 1=1
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s27')
    #
    #  Multi-valued predicate in ON clause.
    stmt = """select ca, cb, cc, cd
from (select T1.c2 , T2.c4
from VNA1P005 T1 
join VNA1P005 T2 
on T1.c2 = T2.c4
) dt1(ca,cb)
join (select T1.char2_2 , T2.csubstring
from VUA1P001 T1 
join VNA1P007 T2 
on T1.char2_2 = T2.csubstring
) dt2(cc,cd)
on ( dt1.ca , 1 ) = (dt2.cc , 1 )
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s28')
    
    _testmgr.testcase_end(desc)

def test004(desc="""a04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    # Test case name:      T1100:A04
    # Description:         This test verifies the SQL Derived Table
    #                      feature via DT of JRAN-generated queries.
    #                      Because of many memory faults, tests put into
    #                      separate cases; see also A05, A08-A13.
    #
    # ---------------------------
    #      Id: DT.242       Complex queries, leveraging a half-dozen JRAN
    #                       queries whose results we know for SQL and SQL.
    #                       Queries picked as the more interesting of a set
    #                       of 20 run at MS2 with 5 failures in 11 of the 20.
    #                       Include OUTER JOIN, UNION, and subquery.
    #                       Spot check that DT definitions can support
    #                       constructs also present in SQL query
    #                       specification, including use of expressions
    #                       in select lists and use of predicates:
    #      Id: DT.181       Aggregates in DT.
    #      Id: DT.182       Arithmetic operators(+, - *, /) in DT
    #      Id: DT.183       BETWEEN predicate in DT
    #      Id: DT.184       Comparison (>, <, =) in DT
    #         (no 185       Date/time functions (e.g. EXTEND))
    #      Id: DT.186       DISTINCT (added to query s2 below) in DT
    #      Id: DT.187       GROUP BY in DT
    #      Id: DT.188       HAVING in DT
    #      Id: DT.189       IN predicate in DT
    #      Id: DT.190       LEFT JOIN in DT
    #      Id: DT.191       LIKE (added to query s2 below) in DT
    #      Id: DT.192       Literals in DT
    #      Id: DT.193       Negation (NOT) in DT
    #      Id: DT.194       NULL predicate (added to query s2 below) in DT
    #      Id: DT.195       Parameters in DT
    #      Id: DT.196       Subqueries -- correlated
    #      Id: DT.197       Subqueries -- uncorrelated
    # ---------------------------
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT * FROM ( select * from D1 ) dt ORDER BY 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s0')
    stmt = """SELECT * FROM ( select * from D2 ) dt ORDER BY 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s1')
    stmt = """SELECT * FROM ( select * from D3 ) dt ORDER BY 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s2')
    #  --------------------
    #  Param specification.
    #  --------------------
    
    stmt = """reset param ;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?pa2   4;"""
    output = _dci.cmdexec(stmt)
    #
    #  -------------------------
    #  Generated SQL statements.
    #  -------------------------
    #
    #---------------------------------------
    # section s1 -- Expect 0 rows
    # Seed is 28387
    #---------------------------------------
    #
    stmt = """SELECT * FROM ( SELECT --  sel^info.level (Starting SELECT, depth) = 0
( ( ( 26.18 )/1 )*1 )-0 , T1.i2
FROM D1 T0, D3 T1 
--  TEMPORARY HARD CODE ..... JOIN
--  sel^info.outjoin =1
INNER JOIN D1 JT ON JT.I1 = 1
WHERE
( ?pa2 )-0 BETWEEN ( T0.i3 ) AND ( ( T1.i1 )/1 )
--  sel^info.level (ending SELECT, depth) = 0
) dt ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    _testmgr.testcase_end(desc)

def test005(desc="""a05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    # Test case name:      T1100:A05
    # Description:         This test verifies the SQL Derived Table
    #                      feature via DT of JRAN-generated queries,
    #                      modified to test correlated references.
    #                      See also A04.
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SELECT * FROM ( select * from D1 ) dt ORDER BY 1, 2, 3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    stmt = """SELECT * FROM ( select * from D2 ) dt ORDER BY 1, 2, 3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
    stmt = """SELECT * FROM ( select * from D3 ) dt ORDER BY 1, 2, 3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    #  --------------------
    #  Generated SQL statements.
    #  -------------------------
    
    # ---------------------------------------
    #  section s15 -- 27 rows
    #  Seed is 27378
    # ---------------------------------------
    #
    #  Added Derived Table dt1 in subquery.
    #  Strip some bogus parens and double NOT's compared to generated statement.
    stmt = """SELECT * FROM ( SELECT T0.i1 , T2.i3 , T2.i2
FROM D1 T0, D2 T1, D2 T2 
WHERE (  NOT ( T2.i2 BETWEEN T0.i2 AND T0.i2 ) AND EXISTS (
SELECT --  sel^info.level (Starting SELECT, depth) = 1
* FROM ( SELECT SUM ( T3.i2 )
FROM D3 T3, D3 T4
WHERE NOT ( T4.i2 +0 <> T3.i2 )
GROUP BY T4.i3
) dt1
--   sel^info.level (ending SELECT, depth) = 1
) AND NOT ( -18 BETWEEN T1.i1 AND T2.i2 ) )
) dt (c1, c2, c3)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
    #
    #  Repeat the above with Group By referring to
    #  column in Where clause.  i.e.,
    #           GROUP BY T4.i3
    #  replaced by:
    #           GROUP BY T4.i2
    #
    stmt = """SELECT * FROM ( SELECT T0.i1 , T2.i3 , T2.i2
FROM D1 T0, D2 T1, D2 T2 
WHERE (  NOT ( T2.i2 BETWEEN T0.i2 AND T0.i2 ) AND EXISTS (
SELECT --  sel^info.level (Starting SELECT, depth) = 1
* FROM ( SELECT SUM ( T3.i2 )
FROM D3 T3, D3 T4
WHERE NOT ( T4.i2 +0 <> T3.i2 )
GROUP BY T4.i2 -- <<<+++ changed.
) dt1
--   sel^info.level (ending SELECT, depth) = 1
) AND NOT ( -18 BETWEEN T1.i1 AND T2.i2 ) )
) dt (c1, c2, c3)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s4')
    #
    #  Same with removal of between clause in outer query.
    stmt = """SELECT * FROM (
SELECT T0.i1 , T2.i3 , T2.i2
FROM D1 T0, D2 T1, D2 T2 
WHERE (  NOT ( T2.i2 BETWEEN T0.i2 AND T0.i2 ) AND EXISTS (
SELECT --  sel^info.level (Starting SELECT, depth) = 1
* FROM ( SELECT SUM ( T3.i2 )
FROM D3 T3, D3 T4
WHERE NOT ( T4.i2 +0 <> T3.i2 )
GROUP BY T4.i2 -- <<<+++ changed.
) dt1
--   sel^info.level (ending SELECT, depth) = 1
)
--  AND NOT ( -18 BETWEEN T1.i1 AND T2.i2 )
)
) dt (c1, c2, c3)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s5')
    #
    #  Same with removal of outer query.
    #  SELECT * FROM (
    stmt = """SELECT T0.i1 , T2.i3 , T2.i2
FROM D1 T0, D2 T1, D2 T2 
WHERE (  NOT ( T2.i2 BETWEEN T0.i2 AND T0.i2 ) AND EXISTS (
SELECT --  sel^info.level (Starting SELECT, depth) = 1
* FROM ( SELECT SUM ( T3.i2 )
FROM D3 T3, D3 T4
WHERE NOT ( T4.i2 +0 <> T3.i2 )
GROUP BY T4.i2 -- <<<+++ changed.
) dt1
--   sel^info.level (ending SELECT, depth) = 1
) AND NOT ( -18 BETWEEN T1.i1 AND T2.i2 ) )
--  ) dt (c1, c2, c3)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s6')
    #
    #  ---------------------------
    #       Id: DT.198a      Correlated reference in derived table SELECT list.
    #       Id: DT.199a      Correlated reference in aggregate in derived table.
    #       Id: DT.199b      Correlated reference with arithmetic operators in derived table.
    #  ---------------------------
    #
    stmt = """SELECT * FROM (
SELECT T0.i1 , T2.i3 , T2.i2
FROM D1 T0, D2 T1, D2 T2 
GROUP BY T0.i1, T2.i3, T2.i2, T0.i2, T1.i1
HAVING ( NOT ( T2.i2 BETWEEN T0.i2 AND T0.i2 ) AND EXISTS (
SELECT --  sel^info.level (Starting SELECT, depth) = 1
* FROM (
SELECT SUM ( T3.i2 ), SUM ( T0.i1 )
FROM D3 T3, D3 T4
WHERE NOT ( T4.i2 +0 <> T3.i2 )
GROUP BY T4.i3
) dt1
--  sel^info.level (ending SELECT, depth) = 1
) AND NOT ( -18 BETWEEN T1.i1 AND T2.i2 ) )
) dt (c1, c2, c3)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s7')
    #
    stmt = """SELECT * FROM ( SELECT T0.i1 , T2.i3 , T2.i2
FROM D1 T0, D2 T1, D2 T2 
-- Added T0.i2 must be a grouping column
GROUP BY T0.i1, T2.i3, T2.i2, T0.i2, T1.i1
HAVING ( NOT ( T2.i2 BETWEEN T0.i2 AND T0.i2 ) AND EXISTS (
SELECT
* FROM ( SELECT SUM ( T3.i2 ), SUM ( T0.i1 )
FROM D3 T3, D3 T4
WHERE NOT ( T4.i2 +0 <> T3.i2 )
GROUP BY T4.i3
) dt1
) AND NOT ( -18 BETWEEN T1.i1 AND T2.i2 ) )
) dt (c1, c2, c3)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s8')
    #
    #  ---------------------------
    #       Id: DT.198b      Correlated reference in derived table WHERE predicate.
    #       Id: DT.198c      Correlated reference in derived table ON clause.
    #       Id: DT.199b      Correlated reference with logical operators in derived table.
    #       Id: DT.199c      Correlated reference in BETWEEN predicate in derived table.
    #  ---------------------------
    #
    stmt = """SELECT * FROM ( SELECT T0.i1 , T2.i3 , T2.i2
FROM D1 T0, D2 T1, D2 T2 
WHERE (  NOT ( T2.i2 BETWEEN T0.i2 AND T0.i2 ) AND EXISTS (
SELECT --  sel^info.level (Starting SELECT, depth) = 1
* FROM ( SELECT SUM ( T3.i2 )
FROM D3 T3, D3 T4
WHERE ( 20 BETWEEN T0.i1 AND T2.i3 )
OR ( T0.i1 BETWEEN T2.i3 AND 20 )    

GROUP BY T4.i3
) dt1
--   sel^info.level (ending SELECT, depth) = 1
) AND NOT ( -18 BETWEEN T1.i1 AND T2.i2 ) )
) dt (c1, c2, c3)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s9')
    #
    #  Original.
    #  Expect 27 (3*3*3) rows.
    stmt = """SELECT * FROM ( SELECT --  sel^info.level (Starting SELECT, depth) = 0
T0.i1 , T2.i3 , T2.i2 , T2.i3
FROM D1 T0, D2 T1, D2 T2 
WHERE
NOT ( NOT ( ( ( NOT ( T2.i2 BETWEEN T0.i2 AND T0.i2 )
) AND ( NOT ( NOT ( ( EXISTS (    

SELECT --  sel^info.level (Starting SELECT, depth) = 1
* FROM ( SELECT
SUM ( T3.i2 )
FROM D3 T3, D3 T4
WHERE
NOT ( ( T4.i2 )+0 <> T3.i2 )
GROUP BY T4.i3, T4.i3
) dt1
--   sel^info.level (ending SELECT, depth) = 1
) ) AND ( NOT ( -18.18 BETWEEN ( T1.i1 ) AND ( T2.i2 ) ) ) ) ) )
) AND ( T0.i1 >= T0.i1 ) ) )
--   sel^info.level (ending SELECT, depth) = 0    

) dt (c1, c2, c3, c4)
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s10')
    
    _testmgr.testcase_end(desc)

def test006(desc="""a06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    # Test case name:      T1100:A06
    # Description:         This test verifies the SQL Derived table
    #                      features, with string, CASE, and embedded quotes.
    #
    # =================== End Test Case Header  ===================
    #
    #  ---------------------------
    #  Columns that disallow NULL value (VUA1P001)
    #  Expect 6 rows.
    
    stmt = """select
char1_4      --  PIC X(5)   not null
, char2_2      --  PIC X(2)   not null
, varchar5_10  --  VarChar(9) not null
, char10_20    --  PIC X(5)   not null
, char12_10    --  PIC X(2)   not null
, char13_100   --  Char(5)    not null
from VUA1P001 
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s0')
    #
    #  Expect same 6 rows.
    stmt = """select * from
(select  char1_4      , char2_2   , varchar5_10
, char10_20    , char12_10 , char13_100
from VUA1P001 
) dt
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s1')
    #
    #  Columns that allow NULL value though none is present (VUA1P003).
    #  View and table have same columns.
    #  Expect 3 rows.
    stmt = """select
char1_4       -- PIC X(5)   not null
, char2_2
, varchar2_10   -- VarChar(15)   not null
, varchar2_100  -- VarChar(25)   not null
, char13_100    -- Char(5)   not null
from VUA1P003 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s2')
    #
    #  ---------------------------
    #       Id: DT.061a     Within DT use ANSI string functions on columns of DT on a table.
    #       Id: DT.061b     Within DT use ANSI string functions on columns of DT on a view.
    #       Id: DT.061c     Within DT use view containing ANSI string functions.
    #       Id: DT.062      Select ANSI string functions on columns DT.
    #  ---------------------------
    #
    #  Expect 6 rows; note that the 3 longer values of varchar0_nuniq
    #  are null-extended.
    stmt = """select varchar0_nuniq
, char9_100
, varchar0_nuniq || 'x'
from BTA1P007 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s3')
    #
    #  Expect 6 rows, ending with 'trim leading spaces' in all rows.
    stmt = """select upper(lower( varchar0_nuniq || char9_100 ))
, lower(upper( varchar0_nuniq || char9_100 ) )
, position  ( ' ' in varchar0_nuniq )
, substring ( varchar0_nuniq from 1 )
, trim ('   trim leading spaces ' || varchar0_nuniq)
from BTA1P007 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s4')
    #
    #  Expect 6 rows.
    stmt = """select e, b || a, lower(d)
from ( select upper(lower( varchar0_nuniq || char9_100 ))
, lower(upper( varchar0_nuniq || char9_100 ) )
, position  ( ' ' in varchar0_nuniq )
, substring ( varchar0_nuniq from 1 )
, trim ('   trim leading spaces ' || varchar0_nuniq)
from BTA1P007 ) dt(a,b,c,d,e)
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s5')
    #
    #  Expect 6 rows.
    stmt = """select cLower, cConcatChar, cPosition
from VNA1P007 
order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s6')
    #
    #  Expect 6 rows: ( 3 * ( 7 0 ) 3 * ( 7 9 ) ).
    stmt = """select position ( ' ' in c ), d from
( select cLower, cConcatChar, cConcatChar, cPosition
from VNA1P007 
) dt(a,b,c,d)
order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s7')
    #
    #  ---------------------------
    #  DT with CASE.
    #  ---------------------------
    #       Id: DT.063a     Select from DT containing simple CASE.
    #       Id: DT.063b     Select from DT containing searched CASE.
    #       Id: DT.063c     Select from DT containing CASE upon a view containing CASE.
    #  ---------------------------
    #
    #  Expect 14 rows.
    stmt = """select rownum, sint, inun from BTA1P009 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s8')
    #  Expect 8 rows.
    stmt = """select * from VNA1P009 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s9')
    #  Simple CASE of form.
    #  Expect 8 rows.
    stmt = """select * from (select csimple,
CASE csimple WHEN 'Value A' THEN 'A OK'
WHEN 'Value B' THEN 'B prepared'
WHEN 'Value C' THEN 'C sick?'
ELSE 'Now what?'
END
from VNA1P009 ) dt(a, b)
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s10')
    #  Searched CASE or 'CASE with searched conditions'.
    #        SYNTAX: <case specification> ::= <searched case> ::=
    #                    CASE
    #                        { WHEN <search condition> THEN
    #                          {<result expression> | NULL }
    #                        } ...
    #                       [ ELSE <result> ]
    #                    END
    #  Expect 14 rows.
    stmt = """select info from (select
CASE when rownum > 10 then 'rownum over 10'
when sint < 0    then 'sint is negative'
else 'the great unknown'
END
from BTA1P009 ) dt(info)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s11')
    #
    #  CASE upon aggregates from view containing CASE.
    #  Expect ( ( 14 , -14043 , 'cake for everyone' ) )
    stmt = """select * from (select count(*)
, cast (avg(sint) as int) as avg_sint
, CASE
when count(*) < 10 then 'rownum over 10'
when avg(sint) = 0 then 'no sint'
else 'cake for everyone'
END
from BTA1P009 ) dt(
aggCount, avgSint, TextForAggregateValues
)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s12')
    #
    #  ---------------------------
    #       Id: DT.064       Select CASE upon DT upon view.
    #  ---------------------------
    #
    #  Expect 6 rows.
    stmt = """select ubin19_10, char1_4, varchar5_10 from VUA1P001 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s13')
    #  Simple CASE.
    #  Expect 6 rows.
    stmt = """select a, b, c
,CASE dt.a    WHEN 1 THEN 'One for all and all for one'
WHEN 2 THEN 'Tuba City'
WHEN 0 THEN 'Zero'
ELSE 'Over 2'
END
,CASE dt.b    WHEN 'a     ' THEN 'A OK'
WHEN 'AAAA' THEN 'Extra AA OKOK'
ELSE 'Not AAAA'
END
,CASE dt.c    WHEN 'AAAAAAAA' THEN 'A OK'
WHEN 'XYZ'      THEN 'End of the line'
ELSE 'Now what?'
END
from (select ubin19_10, char1_4, varchar0_4
from VUA1P001) dt(a, b, c)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s14')
    #
    #  ---------------------------
    #  Select with repeated column.
    #  ---------------------------
    #
    #  ---------------------------
    #       Id: DT.201      DT Selects same column more than once with explicit derived columns renaming the same column.
    #  ---------------------------
    #
    #  Expect 5 rows.
    stmt = """select dt.c1, dt.c3, dt.c3, dt.c1 from
( select char2_2 , char2_2 from BTA1P005 T1 
where char2_2 < 'EA'
) dt( c1 , c3 )
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s15')
    #
    #  ---------------------------
    #       Id: DT.202      DT Selects same column more than once with implicit derived columns renaming the same column.
    #                       (See also negative tests for ANSI SQL93, section 6.3, SR6:
    #                       don't repeat column name in explicit derived column list.)
    #  ---------------------------
    #
    #  Expect 5 rows.
    stmt = """select * from
( select char2_2 , char2_2 from BTA1P005 T1 
where char2_2 < 'EA'
) dt( c1 , c3 )
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s16')
    #
    #  ---------------------------
    #  Select with delimited column and table names.
    #  ---------------------------
    #
    #  ---------------------------
    #       Id: DT.011a     Delimited ident'r; dbl quotes round Derived table name.
    #       Id: DT.011b     Delimited ident'r; dbl quotes round Derived column name.
    #  ---------------------------
    #
    #  Expect 5 rows.
    stmt = """select "dt"."c1", "dt".* , "dt"."c1" from
( select char2_2 , char3_4 , char2_2 from BTA1P005 T1 
where char2_2 < 'EA'
) "dt"( "c1" , "c2" , "c3" )
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s17')
    #
    #  ---------------------------
    #       Id: DT.011c     Delimited ident'r; dbl quotes round and within Derived table name.
    #       Id: DT.011d     Delimited ident'r; dbl quotes round and within Derived column name.
    #  ---------------------------
    #
    #  First with no quotes.
    #  Expect 6 rows.
    stmt = """select dembeddedquotest.c1, col2 from
(select char2_2 , char3_4 from BTA1P005 T1 
) dembeddedquotest( c1 , col2 )
order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s18')
    #
    #  Expect 6 rows.
    stmt = """select "quotest".c1 from
(select char2_2 from BTA1P005 T1 
) "quotest"( c1 )
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s19')
    #  Expect 6 rows.
    stmt = """select atest."quotc1" from
(select char2_2 from BTA1P005 T1 
) atest( "quotc1" )
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s20')
    #
    #  Expect 6 rows.
    stmt = """select "dembedded""quotest".c1 from
(select char2_2 from BTA1P005 T1 
) "dembedded""quotest"( c1 )
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s21')
    #
    #  Expect 6 rows.
    stmt = """select "dembedded""quotest".c1, col2, "dembedded""quotest".* from
(select char2_2 , char3_4 from BTA1P005 T1 
) "dembedded""quotest"( c1 , col2 )
order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s22')
    #
    #  Expect 6 rows.
    stmt = """select atest."dembeddedquoc""1", \"""col""2"
, 'dembeddedquoc''1', '''col''2' from
(select char2_2 , char3_4 from BTA1P005 T1 
) atest( "dembeddedquoc""1" , \"""col""2" )
order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s23')
    
    _testmgr.testcase_end(desc)

def test007(desc="""a07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    # Test case name:      T1100:A07
    # Description:         This test verifies the SQL Derived Table
    #                      feature via UNION SELECT and nested Derived Tables.
    #
    # =================== End Test Case Header  ===================
    #
    #  ---------------------------
    #  UNION DT's
    #  ---------------------------
    #
    #  ---------------------------
    #       Id: DT.023      NULL values returned by some DT columns.
    #       Id: DT.218a     DT on Left side of UNION.
    #       Id: DT.218b     DT on Right side of UNION.
    #       Id: DT.218c     DT on Left side of UNION ALL.
    #       Id: DT.218d     DT on Right side of UNION ALL.
    #  ---------------------------
    #  First check the data in the tables then do the UNION.
    #  Expect 6 rows.
    
    stmt = """select c2, c3, c4 from VNA1P005 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s0')
    #
    #  Union; expect 5 rows (('AA') ('BA') ('DA') ('EA')
    #  (NULL) )
    stmt = """select * from
( select * from
( select c2 from VNA1P005 
union
select c3 from VNA1P005 
) dta
union
select * from
( select c3 from VNA1P005 
union
select c4 from VNA1P005 
) dtb
union
select * from
( select c4 from VNA1P005 
union
select c2 from VNA1P005 
) dtc
) dtb
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s1')
    #
    #  Union; expect 14 rows (3*('AA') 3*('BA') 3*('DA')
    #  2*('EA') 3*(NULL) )
    stmt = """select * from
( select * from
( select c2 from VNA1P005 
union
select c3 from VNA1P005 
) dta
union all
select * from
( select c3 from VNA1P005 
union
select c4 from VNA1P005 
) dtb
union all
select * from
( select c4 from VNA1P005 
union
select c2 from VNA1P005 
) dtc
) dtb
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s2')
    #
    #  ---------------------------
    #  Nested DT's
    #  ---------------------------
    #
    #  ---------------------------
    #       Id: DT.205a     DT nested deeply to 16 (no limit).
    #  ---------------------------
    #  Expect 6 rows:
    #  (('AA') ('AA') ('BA') ('BA') ('DA') ('EA'))
    stmt = """select c3 from
(select c2, c3 from
(select c2, c3 from
(select c2, c3 from
(select c2, c3 from
(select c2, c3 from
(select c2, c3 from
(select c2, c3, c4 from
(select c2, c3, c4 from
(select c2, c3, c4 from
(select c2, c3, c4 from
(select c2, c3, c4 from
(select c2, c3, c4 from
(select c2, c3, c4 from
(select c2, c3, c4 from
(select n1, c2, c3, c4 from VNA1P005) dt
) dt ) dt ) dt ) dt ) dt ) dt ) dt ) dt
) dt ) dt ) dt ) dt ) dt ) dt
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s3')
    #
    #  ---------------------------
    #       Id: DT.205b     DT nested deeply to 40 (no limit).
    #  ---------------------------
    #  Expect 6 rows:
    #  (('AA') ('AA') ('BA') ('BA') ('DA') ('EA'))
    stmt = """select c3 from (select c3 from
(select c3 from (select c3 from
(select c3 from
(select c2, c3 from  (select c2, c3 from
(select c2, c3 from  (select c2, c3 from
(select c2, c3 from  (select c2, c3 from
(select c2, c3 from  (select c2, c3 from
(select c2, c3 from  (select c2, c3 from
(select c2, c3, c4 from  (select c2, c3, c4 from
(select c2, c3, c4 from  (select c2, c3, c4 from
(select c2, c3, c4 from  (select c2, c3, c4 from
(select c2, c3, c4 from  (select c2, c3, c4 from
(select c2, c3, c4 from  (select c2, c3, c4 from
(select c2, c3, c4 from  (select c2, c3, c4 from
(select c2, c3, c4 from  (select c2, c3, c4 from
(select c2, c3, c4 from  (select c2, c3, c4 from
(select c2, c3, c4 from  (select c2, c3, c4 from
(select c2, c3, c4 from  (select c2, c3, c4 from
(select * from (select * from (select * from (select * from
(select n1, c2, c3, c4 from VNA1P005) dt
) dt ) dt ) dt ) dt
) dt ) dt ) dt ) dt ) dt ) dt ) dt ) dt ) dt ) dt
) dt ) dt ) dt ) dt ) dt ) dt ) dt ) dt ) dt ) dt
) dt ) dt ) dt ) dt ) dt ) dt ) dt ) dt ) dt ) dt
) dt ) dt ) dt ) dt
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s4')
    
    _testmgr.testcase_end(desc)

def test008(desc="""a08"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    # Test case name:      T1100:A08
    # Description:         This test verifies the SQL Derived Table
    #                      feature via DT of JRAN-generated queries.
    #                      Because of many memory faults, tests put into
    #                      separate cases; see documentation in A04.
    #
    #                      A DERIVED TABLE SCRIPT created by
    #                      modifying JRAN non-DT scripts.
    #
    # =================== End Test Case Header  ===================
    #
    # ---------------------------------------
    #  section s5 -- 1 row.
    #  Seed is -28370
    # ---------------------------------------
    
    stmt = """SELECT * FROM (    SELECT --  sel^info.level (Starting SELECT, depth) = 0
T0.i3 , T0.i3 , T0.i3
FROM D1 T0
WHERE
EXISTS (    

SELECT --  sel^info.level (Starting SELECT, depth) = 1
AVG ( T1.i2 )
FROM D2 T1 
WHERE
 T1.i1 >= T1.i1
GROUP BY T1.i2
--  sel^info.level (ending SELECT, depth) = 1
)
GROUP BY T0.i1, T0.i3
HAVING EXISTS (    

SELECT --  sel^info.level (Starting SELECT, depth) = 1
 T2.i1
FROM D2 T1, D2 T2, D1 T3 
WHERE
 T1.i3 <= T0.i1
--  sel^info.level (ending SELECT, depth) = 1
)
--  sel^info.level (ending SELECT, depth) = 0
) dt (c1, c2, c3)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s0')
    #
    #  This Simplification omitting EXISTS in WHERE clause.
    stmt = """SELECT * FROM (    SELECT --  sel^info.level (Starting SELECT, depth) = 0
T0.i3 , T0.i3 , T0.i3
FROM D1 T0
--    WHERE   EXISTS ( .. --  )
GROUP BY T0.i1, T0.i3
HAVING EXISTS (    

SELECT --  sel^info.level (Starting SELECT, depth) = 1
 T2.i1
FROM D2 T1, D2 T2, D1 T3 
WHERE
 T1.i3 <= T0.i1
--  sel^info.level (ending SELECT, depth) = 1
)
--  sel^info.level (ending SELECT, depth) = 0
) dt (c1, c2, c3)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s1')
    
    _testmgr.testcase_end(desc)

def test009(desc="""a09"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    # Test case name:      T1100:A09
    # Description:         This test verifies the SQL Derived Table
    #                      feature via DT of JRAN-generated queries.
    #                      Because of many memory faults, tests put into
    #                      separate cases; see documentation in A04.
    #
    # =================== End Test Case Header  ===================
    #
    #
    # Force autocommit:
    
    stmt = """SET transaction Autocommit on;"""
    output = _dci.cmdexec(stmt)
    #
    #  -------------------------
    #  Generated SQL statement.
    #  -------------------------
    #
    # ---------------------------------------
    #  section s10
    #  Seed is -29548
    # ---------------------------------------
    stmt = """SELECT * FROM ( SELECT --  sel^info.level (Starting SELECT, depth) = 0
 T1.i1
FROM D1 T0, D2 T1, D1 T2 
WHERE
NOT ( ( T2.i1 BETWEEN 88.76 AND 39
) AND EXISTS (    

SELECT --  sel^info.level (Starting SELECT, depth) = 1
T4.i1
FROM D2 T3, D2 T4
WHERE
NOT ( ( T3.i1 )-0 < T3.i3 )
GROUP BY T4.i1
--   sel^info.level (ending SELECT, depth) = 1
) )
--   sel^info.level (ending SELECT, depth) = 0
) dt ORDER BY 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s0')
    #
    #  Remove derived table and order by and inner WHERE and table T3, to
    #  see simplified query.
    stmt = """SELECT T1.i1
FROM D1 T0, D2 T1, D1 T2 
WHERE
NOT ( ( T2.i1 BETWEEN 88.76 AND 39
) AND EXISTS (
SELECT T4.i1
FROM D2 T4
GROUP BY T4.i1
) )
ORDER BY 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s1')
    
    _testmgr.testcase_end(desc)

def test010(desc="""a10"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    # Test case name:      T1100:A10
    # Description:         This test verifies the SQL Derived Table
    #                      feature via DT of JRAN-generated queries.
    #                      Because of many memory faults, tests put into
    #                      separate cases; see documentation in A04.
    #
    # =================== End Test Case Header  ===================
    #
    #
    # Force autocommit:
    stmt = """SET transaction Autocommit on;"""
    output = _dci.cmdexec(stmt)
    #
    #  -------------------------
    #  Generated SQL statement.
    #  -------------------------
    
    # ---------------------------------------
    #  section s11
    #  Seed is 28775
    # ---------------------------------------
    stmt = """SELECT * FROM ( SELECT --  sel^info.level (Starting SELECT, depth) = 0
 T1.i2 , ( T1.i2 )*1 , T1.i2 , MIN ( ( T1.i3 )/1 )
FROM D1 T0, D1 T1 
WHERE
( ( EXISTS (    

SELECT --  sel^info.level (Starting SELECT, depth) = 1
 T2.i2
FROM D2 T2, D1 T3 
WHERE
( -85.82 BETWEEN ( ( T2.i1 )/1 ) AND ( T0.i2 ) ) AND ( T2.i2 BETWEEN (
T0.i2 ) AND ( ( T2.i1 )+0 ) )
--   sel^info.level (ending SELECT, depth) = 1
) ) OR ( ( ( NOT ( ( 30.11 )*1 BETWEEN ( T1.i2 ) AND ( ( ( T0.i3 )+0
)-0 ) ) ) OR ( ( ( T1.i1 <= T1.i1 ) OR ( EXISTS (    

SELECT --  sel^info.level (Starting SELECT, depth) = 1
 T3.i3
FROM D2 T2, D2 T3, D2 T4
WHERE
T4.i2 = T4.i3
GROUP BY T3.i3
--   sel^info.level (ending SELECT, depth) = 1
) ) ) OR ( NOT ( ( T1.i3 )*1 BETWEEN ( T0.i2 ) AND ( T0.i3 ) ) ) )
) AND ( ( -55.97 )+0 BETWEEN ( ( ( T0.i1 )/1 )/1 ) AND ( T1.i2 ) ) )
) OR ( NOT ( NOT ( T1.i1 >= ALL (    

SELECT --  sel^info.level (Starting SELECT, depth) = 1
( SUM ( ( -22.63 )*1 ) )*1
FROM D3 T2 
WHERE
NOT ( -6.82 BETWEEN ( ( 28.40 )-0 ) AND ( ( T2.i1 )-0 ) )
GROUP BY T2.i3, T2.i1, T2.i1
--   sel^info.level (ending SELECT, depth) = 1
)
) ) )
GROUP BY T1.i2
--   sel^info.level (ending SELECT, depth) = 0
) dt (c1, c2, c3, c4)  ORDER BY 4, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s0')
    #
    #  ---------------------------
    #  Same query as above, except with DT and correlation names
    #  on SELECT at "depth 1":
    #  ---------------------------
    #
    stmt = """SELECT * FROM ( SELECT --  sel^info.level (Starting SELECT, depth) = 0
 T1.i2 , ( T1.i2 )*1 , T1.i2 , MIN ( ( T1.i3 )/1 )
FROM D1 T0, D1 T1 
WHERE
( ( EXISTS (
--  ---------------------------
--       Id: DT.199a      Correlated reference Subqueries -- uncorrelated
--  ---------------------------
--  Added DT, to test correlation names, as SELECT refers to columns
--  from outer table T0.
SELECT * FROM ( SELECT --  sel^info.level (Starting SELECT, depth) = 1
 T2.i2
FROM D2 T2, D1 T3 
WHERE
( -85.82 BETWEEN ( ( T2.i1 )/1 ) AND ( T0.i2 ) ) AND ( T2.i2 BETWEEN (
T0.i2 ) AND ( ( T2.i1 )+0 ) )
--   sel^info.level (ending SELECT, depth) = 1
) dt1    

) ) OR ( ( ( NOT ( ( 30.11 )*1 BETWEEN ( T1.i2 ) AND ( ( ( T0.i3 )+0
)-0 ) ) ) OR ( ( ( T1.i1 <= T1.i1 ) OR ( EXISTS (    

--  SELECT refers to no columns from outer tables.
SELECT --  sel^info.level (Starting SELECT, depth) = 1
 T3.i3
FROM D2 T2, D2 T3, D2 T4
WHERE
T4.i2 = T4.i3
GROUP BY T3.i3
--   sel^info.level (ending SELECT, depth) = 1    

) ) ) OR ( NOT ( ( T1.i3 )*1 BETWEEN ( T0.i2 ) AND ( T0.i3 ) ) ) )
) AND ( ( -55.97 )+0 BETWEEN ( ( ( T0.i1 )/1 )/1 ) AND ( T1.i2 ) ) )
) OR ( NOT ( NOT ( T1.i1 >= ALL (    

--  SELECT refers to no columns from outer tables.
SELECT --  sel^info.level (Starting SELECT, depth) = 1
( SUM ( ( -22.63 )*1 ) )*1
FROM D3 T2 
WHERE
NOT ( -6.82 BETWEEN ( ( 28.40 )-0 ) AND ( ( T2.i1 )-0 ) )
GROUP BY T2.i3, T2.i1, T2.i1
--   sel^info.level (ending SELECT, depth) = 1
)
) ) )
GROUP BY T1.i2
--   sel^info.level (ending SELECT, depth) = 0
) dt (c1, c2, c3, c4)  ORDER BY 4, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s1')
    
    _testmgr.testcase_end(desc)

def test011(desc="""a11"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    # Test case name:      T1100:A11
    # Description:         This test verifies the SQL Derived Table
    #                      feature via DT of JRAN-generated queries.
    #                      Because of many memory faults, tests put into
    #                      separate cases; see documentation in A04.
    #
    # =================== End Test Case Header  ===================
    #
    #
    # Force autocommit:
    stmt = """SET transaction Autocommit on;"""
    output = _dci.cmdexec(stmt)
    #
    # -------------------------
    # Generated SQL statement.
    # -------------------------
    #
    #---------------------------------------
    # section s12
    # Seed is -21996
    #---------------------------------------
    
    stmt = """SELECT * FROM ( SELECT --  sel^info.level (Starting SELECT, depth) = 0
 T2.i1 , MAX ( T0.i1 )
FROM D1 T0, D3 T1, D1 T2 
WHERE
NOT ( EXISTS (    

SELECT --  sel^info.level (Starting SELECT, depth) = 1
( ( T3.i1 )-0 )/1
FROM D3 T3 
WHERE
 T3.i3 = T3.i3
--  sel^info.level (ending SELECT, depth) = 1
) )
GROUP BY T2.i1
HAVING EXISTS (    

SELECT --  sel^info.level (Starting SELECT, depth) = 1
 T3.i2
FROM D1 T3, D2 T4
WHERE
 T3.i3 IN ( ( -49.84 )/1 , MAX ( ( ( T0.i3 )/1 )-0 ) )
GROUP BY T3.i2, T3.i1
HAVING T3.i1 BETWEEN T3.i2 AND T3.i1
--  sel^info.level (ending SELECT, depth) = 1
)
--  sel^info.level (ending SELECT, depth) = 0
) dt ORDER BY 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    _testmgr.testcase_end(desc)

def test012(desc="""a12"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    # Test case name:      T1100:A12
    # Description:         This test verifies the SQL Derived Table
    #                      feature via DT of JRAN-generated queries.
    #                      Because of many memory faults, tests put into
    #                      separate cases; see documentation in A04.
    #
    # =================== End Test Case Header  ===================
    #
    # Force autocommit:
    stmt = """SET transaction Autocommit on;"""
    output = _dci.cmdexec(stmt)
    #
    #  -------------------------
    #  Generated SQL statement.
    #  -------------------------
    #
    # ---------------------------------------
    #  section s16 -- 3 rows
    #  Seed is 543
    # ---------------------------------------
    #
    stmt = """SELECT * FROM ( SELECT
MIN ( T2.i3 )
FROM D3 T0, D3 T1, D1 T2 
WHERE
( NOT ( T2.i1 BETWEEN ( ( ( -12.85 )-0 )/1 ) AND T2.i1
) ) OR ( ( T0.i2 )/1 BETWEEN T2.i3 AND 81.91 )
GROUP BY T0.i1
) dt ORDER BY 1, 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s0')
    
    _testmgr.testcase_end(desc)

def test013(desc="""a13"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    # Test case name:      T1100:A13
    # Description:         This test verifies the SQL Derived Table
    #                      feature via DT of JRAN-generated queries.
    #                      Because of many memory faults, tests put into
    #                      separate cases; see documentation in A04.
    #
    # =================== End Test Case Header  ===================
    #
    #
    # Force autocommit:
    stmt = """SET transaction Autocommit on;"""
    output = _dci.cmdexec(stmt)
    #
    #  --------------------
    #  Param specification.
    #  --------------------
    
    stmt = """set param ?parameter4with30charactersHere 5;"""
    output = _dci.cmdexec(stmt)
    #
    #  -------------------------
    #  Generated SQL statement.
    #  -------------------------
    #
    #---------------------------------------
    # section s19 -- Expect 0 rows
    # Seed is 7620
    #---------------------------------------
    #
    stmt = """SELECT c1, c2, c3 FROM ( SELECT
T0.i2 , ( T1.i2 )-0, T0.i3
FROM D2 T0, D2 T1, D1 T2 
WHERE
( T2.i3 >= ( T0.i1 )*1 ) AND ( ( T1.i3 BETWEEN ( ( T2.i3 )-0 ) AND ( (
 T1.i1 )*1 ) ) AND ( ( ?parameter4with30charactersHere )-0 IN ( T0.i3 )
) )
) dt (c1, c2, c3) ORDER BY c3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #
    #  Components.
    #  Select without WHERE.
    stmt = """SELECT c1, c2, c3, i3, i1 FROM ( SELECT
T0.i2 , T1.i2 , T0.i3 , T2.i3 , T0.i1
FROM D2 T0, D2 T1, D1 T2 
) dt (c1, c2, c3, i3, i1) ORDER BY c3, c2, c1, i3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s0')
    #
    #  Select with WHERE ... BETWEEN.
    stmt = """SELECT c1, c2, c3 FROM ( SELECT
T0.i2 , T1.i2, T0.i3
FROM D2 T0, D2 T1, D1 T2 
WHERE ( T1.i3 BETWEEN T2.i3 AND T1.i1 )
) dt (c1, c2, c3) ORDER BY c3, c2, c1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s1')
    # This gets 0 rows. The predicate shown here is AND'd with the
    # above predicate, and the result is also 0 rows, so that no rows
    # are returned in large query by predicate after OR operator.
    stmt = """SELECT c1, c2, c3 FROM ( SELECT
T0.i2 , T1.i2, T0.i3
FROM D2 T0, D2 T1, D1 T2 
WHERE ?parameter4with30charactersHere IN ( T0.i3 )
) dt (c1, c2, c3) ORDER BY c3, c2, c1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #
    #  Modified query: WHERE AND changed to WHERE OR.
    #  Expect 12 rows only, as in subset of query before OR.
    stmt = """SELECT c1, c2, c3 FROM ( SELECT
T0.i2 , ( T1.i2 )-0, T0.i3
FROM D2 T0, D2 T1, D1 T2 
WHERE
( T2.i3 >= ( T0.i1 )*1 )
OR ( ( T1.i3 BETWEEN ( ( T2.i3 )-0 ) AND ( (
 T1.i1 )*1 ) ) AND ( ( ?parameter4with30charactersHere )-0 IN ( T0.i3 )
) )
) dt (c1, c2, c3) ORDER BY c3, c2, c1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s2')
    
    _testmgr.testcase_end(desc)

def test014(desc="""a14"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    # Test case name:      T1100:A14
    # Description:         This test verifies the SQL Derived Table
    #                      feature via Row Value Constructor and
    #                      Table Value Constructor.
    #
    # =================== End Test Case Header  ===================
    #
    # Force autocommit:
    stmt = """SET transaction Autocommit on;"""
    output = _dci.cmdexec(stmt)
    #
    #  ---------------------------
    #  Row-value constructor
    #  ---------------------------
    #       Id: DT.151       Within DT, use Row Value Constructor.
    #       Id: DT.152       DT in FROM clause of query whose predicate include Row Value Constructor.
    #  ---------------------------
    
    #
    #  Expect 6 rows.
    stmt = """select * from VNA1P005 
order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s0')
    #
    #  Expect 5 rows.
    stmt = """select dt.yyc3, dt.xxxc2, dt.wn1, dt.zc4
from
(
select * from VNA1P005 
where (C3) = (C4)
) dt(wn1,xxxc2,yyc3,zc4)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s1')
    #
    #  Expect 1 row { ('EA' 'DA' -2789  ?) }
    stmt = """select dt.yyc3, dt.xxxc2, dt.wn1, dt.zc4
from
(
select * from VNA1P005 
where C3 is not null and (C4 is null)
) dt(wn1,xxxc2,yyc3,zc4)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s2')
    #
    #  Expect 5 rows.
    stmt = """select dt.yyc3, dt.xxxc2, dt.wn1, dt.zc4
from
(
select * from VNA1P005 
) dt(wn1,xxxc2,yyc3,zc4)
where (yyc3,zc4) = (zc4,yyc3)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s3')
    #
    #  ---------------------------
    #  Right Outer join and DT's on grouped view.
    #  ---------------------------
    #       Id: DT.161       Within DT, use Table Value Constructor.
    #       Id: TV.002       SELECT <select-list> FROM VALUES <Table Value Constructor>.
    #  ---------------------------
    #
    #  Expect ((1,2), (3,4))
    stmt = """select * from (values (1,2), (3,4)) x
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s4')
    #
    #  Expect ((1,2,1,2), (3,4,3,4))
    stmt = """select x.my1, x.my2, y.my1, y.my2
from (values (1,2), (3,4)) x (my1, my2)
left join (values (1,2), (3,4)) y (my1, my2)
on x.my1 = y.my1
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s5')
    #
    #  With TRUE on clause should get all 4 rows:
    stmt = """select x.my1, x.my2, y.my1, y.my2
from (values (1,2), (3,4)) x (my1, my2)
left join (values (1,2), (3,4)) y (my1, my2)
on ( 1 = 1 )
order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s6')
    #  With FALSE on clause should only get 2 rows, NULL-extended:
    stmt = """select x.my1, x.my2, y.my1, y.my2
from (values (1,2), (3,4)) x (my1, my2)
left join (values (1,2), (3,4)) y (my1, my2)
on ( 0 = 1 )
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s7')
    #
    #  Expect 2 rows with matching values: ((1,2,1,2), (3,4,3,4))
    stmt = """select x.my1, x.my2, y.my1, y.my2
from (values (1,2), (3,4)) x (my1, my2)
join (values (1,2), (3,4)) y (my1, my2)
on x.my1 = y.my1
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s8')
    #
    stmt = """set param ?pn3 3;"""
    output = _dci.cmdexec(stmt)
    #  Expect ((1,2,?,?), (3,4,1,3))
    stmt = """select x.my1, x.my2, y.my1, y.my2
from (values (1,2), (3,4)) x (my1, my2)
left join (values (1,?pn3), (?pn3,4)) y (my1, my2)
on x.my1 = y.my2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s9')
    #
    #  Expect 6 rows.
    stmt = """select C2, C3
from ( select * from VNA1P005 T3 ) z
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s10')
    #
    #  Expect 3 rows { (AA  BA  AA  BA) (AA  BA  ?  BA) (J  Z  ?  ?) }
    stmt = """select *
from (values ('AA','BA'), ('J','Z') ) x (my1, my2)
left join
(
select C2, C3
from ( select * from VNA1P005 T3 ) z
) y
on x.my2 = y.C3
order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s11')
    #
    # Expect same 3 rows.
    stmt = """set param ?pc 'J';"""
    output = _dci.cmdexec(stmt)
    stmt = """select *
from (values ('AA','BA'), (?pc,'Z') ) x (my1, my2)
left join
(
select C2, C3
from ( select * from VNA1P005 T3 ) z
) y
on x.my2 = y.C3
order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s12')
    #
    # Expect same 3 rows.
    stmt = """set param ?pc 'BA';"""
    output = _dci.cmdexec(stmt)
    stmt = """select *
from
(
select *
from (values ('AA',cast(?pc as pic xx) ), ('J','Z') ) x (my1, my2)
left join
(
select C2, C3
from ( select * from VNA1P005 T3 ) z
) y
on x.my2 = y.C3
) dt
order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s13')
    #
    stmt = """set param ?pc 'Z';"""
    output = _dci.cmdexec(stmt)
    #  Expect 1 row { ('J' 'Z') ('Z' 'BA') }
    stmt = """select *
from
( values (cast(?pc as pic xx), 'BA'), ('J','Z') ) x (my1, my2)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s14')
    #  Expect 2 rows, null-extended (no match)
    #  { (J  Z  ?  ?) (Z  BA  ?  ?)  }
    stmt = """select *
from
(
select *
from
( values (cast(?pc as pic xx), 'BA'), ('J','Z') ) x (my1, my2)
left join
(
select C2, C3
from ( select * from VNA1P005 T3 ) z
) y
on x.my1 = y.C2
) dt
order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s15')
    #  Expect 3 rows (1 null-extended; 2 matching)
    #  { (J  Z  ?  ?) (Z  BA  BA  AA) (Z  BA  BA  AA) }
    stmt = """select *
from
(
select *
from
( values (cast(?pc as pic xx), 'BA'), ('J','Z') ) x (my1, my2)
left join
(
select C2, C3
from ( select * from VNA1P005 T3 ) z
) y
on x.my2 = y.C2
) dt
order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s16')
    
    _testmgr.testcase_end(desc)

def test015(desc="""a15"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    # Test case name:      T1100:A15
    # Description:         This test verifies the SQL Derived Table
    #                      feature via DT within views.  These tests
    #                      added because of bug with DT in views
    #                      found in testing 971022-beta build.
    #
    # =================== End Test Case Header  ===================
    #
    #
    # Force autocommit:
    stmt = """SET transaction Autocommit on;"""
    output = _dci.cmdexec(stmt)
    #
    # Tables and views created in this test case are dropped in pre- and
    # post-test.
    
    # 04/20/09 remove query_cache CQD
    #control query default query_cache '0';
    stmt = """create table myT(c Integer) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into myT Values (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into myT Values (49);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into myT Values (108);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """Insert Into myT Values ( -0 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """Insert Into myT Values ( -2 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """Insert Into myT Values ( -2 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """Insert Into myT Values ( NULL );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select c from myT order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s0')
    #
    stmt = """create table myT2(c Integer) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into myT2 Values (7);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into myT2 Values (108);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """Insert Into myT2 Values ( -2 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """Insert Into myT2 Values ( -2 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """Insert Into myT2 Values ( NULL );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select c from myT2 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s1')
    #
    stmt = """create table myT3(c Integer, d Integer) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into myT3 Values (1,7);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into myT3 Values (1,NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """Insert Into myT3 Values ( 0,-2 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """Insert Into myT3 Values ( 0,-2 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """Insert Into myT3 Values ( NULL, -2 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select c,d from myT3 order by 1,2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s2')
    #
    # ---------------------------
    #      Id: DT.231a      Create View upon one column in Derived Table.
    # ---------------------------
    
    stmt = """create view myV as
select c from
(select c from myT T1 ) t 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Expect rows as in base table.
    stmt = """select * from myV order by c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s3')
    stmt = """drop view myV;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # ---------------------------
    #      Id: DT.231b      Create View upon multiple columns in Derived Table.
    # ---------------------------
    #
    stmt = """create view myV as
select * from
(select c,d from myT3 T3 ) t 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Expect rows as in base table.
    stmt = """select c,d from myV order by 1,2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s4')
    stmt = """drop view myV;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """create view myV as
select d from
(select * from myT3 T3 ) t 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Expect rows as in base table.
    stmt = """select * from myV order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s5')
    stmt = """drop view myV;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # ---------------------------
    #      Id: DT.232a      Create View upon Natural join of Derived Tables.
    # ---------------------------
    #
    stmt = """create view myV as select * from
(select c from myT T1 ) T2 
natural    join
(select c from myT T3 ) t4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Expect ( 4*(-2) (0) (1) (49) (108)) .
    stmt = """select c from myV order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s6')
    stmt = """drop view myV;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    
    stmt = """create view myV as select c from
(select c from myT T1 ) T2 
natural    join
(select c from myT2 T3 ) t4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  Expect ( 4*(-2) (108)) .
    stmt = """select c from myV order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s7')
    stmt = """drop view myV;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """create view myV as
select * from myT T1 
natural join (select c from myT2 T3 ) t4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  Expect (( -2 )( -2 ) (108) ( NULL ))
    stmt = """select c from myV order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s8')
    stmt = """drop view myV;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """create view myV as
select * from (select c from myT T1 ) T2 
natural join myT2 T3 
where c > 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  Expect ((108))
    stmt = """select c from myV order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s9')
    stmt = """drop view myV;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """create view myV as
select * from
(select c from myT2 T1 ) T2 
natural    join
(select c from myT T3 ) t4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  Expect ( 4*( -2 ) (108))
    stmt = """select c from myV order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s10')
    stmt = """drop view myV;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """create view myV as
select * from
(select * from myT T1 ) T2 
natural    join
(select * from myT3 T3 ) t4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  Expect ((0) (0) (1) (1))
    stmt = """select c from myV order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s11')
    stmt = """drop view myV;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """create view myV as
select d from
(select * from myT3 T1 ) T2 
natural    join
(select * from myT3 T3 ) t4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  Expect ( 4*(-2) (7))
    stmt = """select d from myV order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s12')
    stmt = """drop view myV;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # ---------------------------
    #      Id: DT.232b      Create View upon Inner join of Derived Tables.
    # ---------------------------
    #
    stmt = """create view myV as select * from
(select c from myT T1 ) T2 (a)
inner join
(select d from myT3 T3 ) t4
on T2.a=t4.d
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  Expect ( 6*(-2 -2))
    stmt = """select a,d from myV order by 1,2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s13')
    stmt = """drop view myV;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """create view myV as select * from
(select c from myT T1 ) T2 (a)
inner join
(select c,d from myT3 T3 ) t4
on 1=1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  Expect 35 rows (all combinations of 7*5 rows).
    stmt = """select * from myV order by 1,2,3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s14')
    stmt = """drop view myV;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # ---------------------------
    #      Id: DT.232c      Create View upon Right Outer join of Derived Tables.
    # ---------------------------
    #
    stmt = """create view myV as
select * from
(select c from myT T1 ) T2 (a)
right outer join
(select c,d from myT3 T3 ) t4
on T2.a=t4.d
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  Expect ( 6*(-2 -2) (7 NULL) (NULL NULL) )
    stmt = """select d, a from myV order by 1,2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s15')
    stmt = """drop view myV;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """create view myV as
select * from
(select c from myT T1 ) T2 (a)
right outer join
(select d from myT3 T3 ) t4
on 1=1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  Expect 35 rows (all combinations of 7*5 rows).
    stmt = """select * from myV order by 1,2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s16')
    stmt = """drop view myV;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # ---------------------------
    #      Id: DT.232d      Create View upon cross-product of Derived Tables.
    # ---------------------------
    #
    stmt = """create view myV as
select * from
(select c from myT T1 ) t(a)
, (select c,d from myT3 T3 ) tx
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  Expect 35 rows (all combinations of 7*5 rows)
    #  as in cross-product of base tables.
    stmt = """select a,c,d from myV order by 1,2,3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s17')
    stmt = """drop view myV;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # ---------------------------
    #      Id: DT.232e      Create View upon Union of Derived Tables.
    # ---------------------------
    #
    stmt = """create view myV as
select a from (select c from myT T1 ) t(a)
UNION
select c from (select c,d from myT3 T3 ) tx
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  Expect ( (-2) (0) (1) (49) (108) (NULL) )
    stmt = """select * from myV order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s18')
    stmt = """drop view myV;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """create view myV as
select c from (select c from myT T1 ) t 
UNION
select d from (select c,d from myT3 T3 ) t 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  Expect ( (-2) (0) (1) (7) (49) (108) (NULL) )
    stmt = """select * from myV order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s19')
    stmt = """drop view myV;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """create view myV as
select * from (select c from myT T1 ) t(a)
UNION
select d from (select c,d from myT3 T3 ) tx
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  Expect ( (-2) (0) (1) (7) (49) (108) (NULL) )
    stmt = """select * from myV order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s20')
    stmt = """drop view myV;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """control query default query_cache reset;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test016(desc="""a16"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    # Test case name:      T1100:A16
    # Description:         This test verifies the SQL Derived Table
    #                      feature via SELECT, testing in combination with
    #                      JOIN.
    #
    # =================== End Test Case Header  ===================
    #
    #
    # Force autocommit:
    stmt = """SET transaction Autocommit on;"""
    output = _dci.cmdexec(stmt)
    #
    #  ---------------------------
    #       Id: JT.187b      JOINs inside many different Derived Tables in same query.
    #       Id: JT.187c      Predicates with JOINs inside DT's.
    #  ---------------------------
    #  Natural join (see also test for JT.187a).
    #  Expect ( 8*('AA' 'AA') 4*('AA' 'BA') 2*('BA' 'AA') ('BA' 'BA'))
    #  12/12/98 temporarily commented out because of looping!
    
    stmt = """select * from
-- See NJ results above.
( select c3 from VNA1P005 T1 
natural join VNA1P005 T2 
natural join VNA1P005 T3 
) ta ( dtc3 )
natural join
( select c3 from VNA1P005 T1 
natural join VNA1P005 T2 
natural join VNA1P005 T3 
) tb ( dtc3 )
right join
-- { (AA) (AA) (BA) }
( select c3 from VNA1P005 T1 
natural join VNA1P005 T2 
natural join VNA1P005 T3 
) tc ( dtc3 )
on (1=1)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s0')
    #
    #  Subset -- NJ only from the above:
    #  Expect ( 4*('AA') ('BA'))
    stmt = """select * from
-- ( (AA) (AA) (BA) )
( select c3 from VNA1P005 T1 
natural join VNA1P005 T2 
natural join VNA1P005 T3 
) ta ( dtc3 )
natural join
-- ( (AA) (AA) (BA) )
( select c3 from VNA1P005 T1 
natural join VNA1P005 T2 
natural join VNA1P005 T3 
) tb ( dtc3 )
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s1')
    #
    #  Subset -- NJ plus Table Value constants in outer join.
    #  Expect ( 8*('AA' 'AA') 4*('AA' 'BA') 2*('BA' 'AA') ('BA' 'BA'))
    stmt = """select * from
( select c3 from VNA1P005 T1 
natural join VNA1P005 T2 
natural join VNA1P005 T3 
) ta ( dtc3 )
natural join
( select c3 from VNA1P005 T1 
natural join VNA1P005 T2 
natural join VNA1P005 T3 
) tb ( dtc3 )
right join (values ('AA'), ('AA'), ('BA')) tc (dtc3)
on (1=1)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s2')
    #
    #  Subset -- RJ only from the above:
    #  Expect ( 4*('AA' 'AA') 2*('AA' 'BA') 2*('BA' 'AA') ('BA' 'BA'))
    stmt = """select * from
( select c3 from VNA1P005 T1 
natural join VNA1P005 T2 
natural join VNA1P005 T3 
) tb ( dtc3 )
right join
( select c3 from VNA1P005 T1 
natural join VNA1P005 T2 
natural join VNA1P005 T3 
) tc ( dtc3 )
on (1=1)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s3')
    #
    #  Subset -- RJ plus Table Value constrants in natural join.
    #  Expect ( 8*('AA' 'AA') 4*('AA' 'BA') 2*('BA' 'AA') ('BA' 'BA'))
    stmt = """select * from
(values ('AA'), ('AA'), ('BA')) ta (dtc3)
natural join
( select c3 from VNA1P005 T1 
natural join VNA1P005 T2 
natural join VNA1P005 T3 
) tb ( dtc3 )
right join
( select c3 from VNA1P005 T1 
natural join VNA1P005 T2 
natural join VNA1P005 T3 
) tc ( dtc3 )
on (1=1)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s4')
    #
    #  As above with smaller NJ within DT.
    stmt = """select * from
( select c3 from VNA1P005 T1 
natural join VNA1P005 T2 
) ta ( dtc3 )
natural join
( select c3 from VNA1P005 T1 
natural join VNA1P005 T2 
) tb ( dtc3 )
right join
( select c3 from VNA1P005 T1 
natural join VNA1P005 T2 
) tc ( dtc3 )
on (1=1)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s5')
    #
    stmt = """select * from
( select c3 from VNA1P005 T1 
natural join VNA1P005 T2 
natural join VNA1P005 T3 
where c2 <> c3
) T3 ( dtc3 )
-- Note using 't3' as derived table name
-- and as correlation name.
natural join
( select c3 from VNA1P005 T1 
natural join VNA1P005 T2 
natural join VNA1P005 T3 
where c3 is not null
) tb ( dtc3 )
right join
( select c3 from VNA1P005 T1 
natural join VNA1P005 T2 
natural join VNA1P005 T3 
where c3 < 'CA'
) tc ( dtc3 )
on (1=1)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s6')
    #
    #  BUG fixed 980630Beta2 -- now get correct rows.
    #  Right join from above (see test for DT.091).
    #  Expect { (BA  AA   ?  BA  AA  BA )
    #   ( BA  AA   ?  BA  AA  BA )
    #   ( BA  AA   ?  BA  AA  BA )
    #   ( BA  AA   ?  BA  AA  BA )
    #   ( DA  EA   ?  DA  EA  DA ) }
    #
    stmt = """select T3.*
from ( select T1.c2, T1.c3, T2.c2, T2.c3, T3.char2_2, T3.char3_4
from VNA1P005 T1 
right join VNA1P005 T2 
on T1.c2 = T2.c3
right join BTA1P005 T3 
on T2.c3 = T3.char3_4
where T1.c2 is not null
and T2.c2 is null
) T3 (a,b,c,d,e,f) -- Note using this name as derived table name
-- and as correlation name.
order by 1, 2, 4, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s7')
    #
    #  Expect 10 rows (2 for DISTINCT * all 5 from above table).
    stmt = """select *
from ( select T1.c2, T1.c3, T2.c2, T2.c3, T3.char2_2, T3.char3_4
from VNA1P005 T1 
right join VNA1P005 T2 
on T1.c2 = T2.c3
right join BTA1P005 T3 
on T2.c3 = T3.char3_4
where T1.c2 is not null
and T2.c2 is null
) T3 (a,b,c,d,e,f) -- Note using this name as derived table name
-- and as correlation name.
right join
( select distinct
 T1.c2, T1.c3, T2.c2
from VNA1P005 T1 
right join VNA1P005 T2 
on T1.c2 = T2.c3
right join BTA1P005 T3 
on T2.c3 = T3.char3_4
where T1.c2 is not null
and T2.c2 is null
) t4 (a,b,c)
on (1=1)
order by 1, 7
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s8')
    
    _testmgr.testcase_end(desc)

def test017(desc="""a17"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1100:A17
    #  Description:        This tests SQL UNION in Derived tables.
    #
    # =================== End Test Case Header  ===================
    #  Reality check:
    stmt = """select a from t order by a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s0')
    stmt = """select job from EMPLOYEE order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s1')
    stmt = """select branchname from BRANCH order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s2')
    #
    #  This is a simplified version of a query from regress/fullstack/TEST003.
    #  The duplicate elimination of the union relies on sorted rows.
    #  The second group by is a HGB. This violates the sort requirement.
    #  In the regressions this bug is hidden, because the HGB returns the rows in the right order.
    #  If, for example, HGB-bitmux is disabled, the wrong result is returned.
    #  ---------------------------
    
    #
    #  The following query should return (( 2 )).
    stmt = """select count(*)
from (
select a from t group by a having a = 10
union
select a from t group by a
) x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s3')
    #
    #  Can simplify incorrect-result-producing query even further:
    #  Expect (( 2 )).
    stmt = """select count(*)
from (
select a from t where a = 10
union
select a from t 
) x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s4')
    #
    #  ---------------------------
    #  Similar tests using other pre-created tables, with varchar columns.
    #  ---------------------------
    #  Union of data from single table.
    #  Expect (( 15 )).
    stmt = """select count(*)
from (
select branchname from BRANCH where branchname = 'TORONTO'
union
select branchname from BRANCH 
) x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s5')
    #  Expect (( 7 )).
    stmt = """select count(*)
from (
select job from EMPLOYEE where job = 'ENGINEER'
union
select job from EMPLOYEE 
) x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s6')
    #  Union of data from different tables.
    #  Expect (( 16 )).
    stmt = """select count(*)
from (
select job from EMPLOYEE where job = 'ENGINEER'
union
select branchname from BRANCH 
) x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s7')
    
    _testmgr.testcase_end(desc)

def test018(desc="""a18"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    # Test case name:      T1100:A18
    # Description:         This test verifies the SQL Derived table
    #                      features, with SELECT, INSERT, and UPDATE.
    #
    # =================== End Test Case Header  ===================
    #
    #
    # Force autocommit:
    stmt = """Set Transaction Autocommit on;"""
    output = _dci.cmdexec(stmt)
    #
    # ---------------------------
    # Make sure all tables start empty.
    # ---------------------------
    
    stmt = """Delete From T3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    # Should be empty.
    #
    # ---------------------------
    #	Insert (preparation for subsequent update)
    # ---------------------------
    stmt = """Insert into T3 
Values ('1st orig value' ,99 , 'o'   , 1 )
, ('2nd orig value' ,98 , 'ov'  , 2 )
, ('3rd orig value' ,97 , 'ovc' , 3 )
, ('4th orig value' ,96 , 'ov ' , 4 )
, ('5th orig value' ,95 , 'o  ' , 5 )
, ('6 is short'     ,97 , 'o'   , 6 )
, ('7'              ,94 , 'OVC' , 7 )
, ('8th orig value' ,93 , 'OV'  , 8 )
, ('9th orig val  ' ,92 , 'O'   , 9 )
, ('10th val'       ,92 , 'O'   , 9 )
, ('11th val'       ,92 , 'O'   , 9 )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 11)
    stmt = """Select * From T3 Order By 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s0')
    #
    #  ---------------------------
    #       Id: DT.047       Update with expressions, predicates, subqueries.
    #  ---------------------------
    #  From SQL test T016:A6
    #  Needs tables branch, parts, fromsup, employee.
    #     select correlated subquery in WHERE clause test - this tests the
    #     selection of aggregate functions (COUNT, AVG, MAX, MIN, SUM).
    #     Aggregates are tested in the SELECT clause and in the HAVING clause.
    
    #  Get partnames whose price is less than 2000 more than its
    #  average cost from all suppliers who supply it.
    #  Expect 21 rows (character data) as in 1st example in T016:A6.
    stmt = """SELECT * FROM (       select partname
from PARTS 
where price <
(select avg(partcost) + 2000
from FROMSUP 
where partnum =  PARTS.partnum
)
) dt ORDER BY 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s1')
    #
    #  Get branchnames of branches whose total yearly payroll
    #  exceeds 150000.
    #  Expect 4 rows (character data) as in 2nd example in T016:A6.
    stmt = """SELECT * FROM (       select branchname
from BRANCH 
where exists
(select regnum
from EMPLOYEE 
where  EMPLOYEE.regnum =  BRANCH.regnum
and    EMPLOYEE.branchnum =  BRANCH.branchnum
group by regnum, branchnum
having sum(salary) > 150000
)
) dt ORDER BY 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s2')
    #
    #  Get employee names of those employees whose age is greater
    #  than or equal to the max. age of the branch in their region
    #  with the highest average age (eliminate middle WHERE clause).
    #  Expect 12 rows (character data) as in 6th example in T016:A6.
    stmt = """SELECT * FROM (       select empname
from EMPLOYEE X
where age >=ALL
(select max(age)
from EMPLOYEE Y
group by regnum, branchnum
having Y.regnum = X.regnum
and avg(age) >=ALL
(select avg(age)
from EMPLOYEE Z
where Z.regnum = X.regnum
group by branchnum
)
)
) dt ORDER BY 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s3')
    stmt = """Select * From T3 Order By 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s4')
    #
    stmt = """Select min(c), max(c) from
( SELECT * FROM
( select empname
from EMPLOYEE X
where age >=ALL
(select max(age)
from EMPLOYEE Y
group by regnum, branchnum
having Y.regnum = X.regnum
and avg(age) >=ALL
(select avg(age)
from EMPLOYEE Z
where Z.regnum = X.regnum
group by branchnum
)
)
) dt
) dt(c)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s5')
    stmt = """Select min(c), max(c) from
( SELECT * FROM
( select partname
from PARTS 
where price <
(select avg(partcost) + 2000
from FROMSUP 
where partnum =  PARTS.partnum
)
) dt
) dt(c)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s6')
    #
    # Must use CAST to avoid ERROR on update, or (worse) corrupt data
    # which is tested for in companion test case N01.
    stmt = """Update T3 set ch3   = -- char from 3rd DT
(select cast( min(c) as char(3) ) from
( SELECT * FROM
( select empname
from EMPLOYEE X
where age >=ALL
(select max(age)
from EMPLOYEE Y
group by regnum, branchnum
having Y.regnum = X.regnum
and avg(age) >=ALL
(select avg(age)
from EMPLOYEE Z
where Z.regnum = X.regnum
group by branchnum
)
)
) dt
) dt(c)
)
where nint=94
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from T3 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s7')
    #
    stmt = """Update T3 set ch3   = -- char from 3rd DT
(select cast(max(c) as char(3)) from
( SELECT * FROM
( select empname
from EMPLOYEE X
where age >=ALL
(select max(age)
from EMPLOYEE Y
group by regnum, branchnum
having Y.regnum = X.regnum
and avg(age) >=ALL
(select avg(age)
from EMPLOYEE Z
where Z.regnum = X.regnum
group by branchnum
)
)
) dt
) dt(c)
)
where nint=94
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from T3 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s8')
    #
    # Addition because subquery appeared to not return MAX value for insert:
    stmt = """Update T3 set vch15 = -- string from first DT
( select max(c) from
( SELECT * FROM
( select partname
from PARTS 
where price <
(select avg(partcost) + 2000
from FROMSUP 
where partnum =  PARTS.partnum
)
) dt
) dt(c)
)
, ch3   = -- char from 3rd DT
(select cast(min(c) as char(3)) from
( SELECT * FROM
( select empname
from EMPLOYEE X
where age >=ALL
(select max(age)
from EMPLOYEE Y
group by regnum, branchnum
having Y.regnum = X.regnum
and avg(age) >=ALL
(select avg(age)
from EMPLOYEE Z
where Z.regnum = X.regnum
group by branchnum
)
)
) dt
) dt(c)
)
where nint=94
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from T3 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s9')
    #
    # Update T3 with data aggregating from these 3 queries:
    stmt = """Update T3 set vch15 = -- string from first DT
( select max(c) from
( SELECT * FROM
( select partname
from PARTS 
where price <
(select avg(partcost) + 2000
from FROMSUP 
where partnum =  PARTS.partnum
)
) dt
) dt(c)
)
, nint  = -- char from 2nd DT
(select count(c) from
( SELECT * FROM
( select branchname
from BRANCH 
where exists
( select regnum
from EMPLOYEE 
where  EMPLOYEE.regnum =  BRANCH.regnum
and EMPLOYEE.branchnum =  BRANCH.branchnum
group by regnum, branchnum
having sum(salary) > 150000
)
) dt
) dt(c)
)
, ch3   = -- char from 3rd DT
(select cast(max(c) as char(3)) from
( SELECT * FROM
( select empname
from EMPLOYEE X
where age >=ALL
(select max(age)
from EMPLOYEE Y
group by regnum, branchnum
having Y.regnum = X.regnum
and avg(age) >=ALL
(select avg(age)
from EMPLOYEE Z
where Z.regnum = X.regnum
group by branchnum
)
)
) dt
) dt(c)
)
where nint=94
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from T3 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s10')
    #
    # ---------------------------
    # Clean up tables at the end.
    # ---------------------------
    stmt = """Delete From T3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 11)
    
    _testmgr.testcase_end(desc)

def test019(desc="""b01"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #
    #   Test case name:	T1100:B01
    #   Description:	This test verifies the SQL Derived table
    #                       features, with INSERT and UPDATE.
    #
    #  =================== End Test Case Header  ===================
    #
    #  ---------------------------
    #  Create tables to receive local data.
    #  ---------------------------
    #  Delete.
    #  ---------------------------
    #       Id: DT.052       Delete row(s), using DT with UNION CORRESPONDING.
    # 			(CORRESPONDING dropped from Feb 1997 FCS).
    #
    
    stmt = """select varchar5_10 from BTA1P001 
UNION CORRESPONDING
select varchar5_10 from BTA1P001 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #
    stmt = """select varchar5_10 from BTA1P001 
UNION CORRESPONDING BY (varchar5_10)
select varchar5_10 from BTA1P001 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """select * from
( select varchar5_10 from BTA1P001 
UNION CORRESPONDING
select varchar5_10 from BTA1P001 ) dt
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """delete from TDEL where ch3=(
select max(c) from (
select varchar5_10 from BTA1P001 
UNION CORRESPONDING
select varchar5_10 from BTA1P001)
dt (c) ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #
    #  ---------------------------
    #  UNION CORRESPONDING and DT's
    #  ---------------------------
    #
    #       Id: DT.175      <table> UNION CORRESPONDING <DT on views containing UNIONs>
    # 			(CORRESPONDING dropped from Feb 1997 FCS).
    #  Expect 2 columns.
    stmt = """select ubin1_20, sbin4_n1000
from BTA1P008 
UNION CORRESPONDING select * from
( select * from VNA1P008) dt
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #
    #       Id: DT.005       Explicit derived cols; names same as names
    #                       of underlying cols.
    #       Id: DT.176      <view> UNION CORRESPONDING <DT on a view containing OUTER JOINs>
    # 			(CORRESPONDING dropped from Feb 1997 FCS).
    stmt = """select  c2, c3
from VNA1P005 
UNION -- CORRESPONDING
select c2, c3 from
( select * from VNA1P005) dt (n1, c2, c3, c4)
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b01exp""", 'b01s5')
    #
    stmt = """select  c2, c3
from VNA1P005 
UNION CORRESPONDING
select c2, c3 from
( select * from VNA1P005) dt (n1, c2, c3, c4)
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #
    #       Id: DT.177      <view> UNION CORRESPONDING <DT on a view containing NATURAL JOINs>
    # 			(CORRESPONDING dropped from Feb 1997 FCS).
    stmt = """select ubin1_20, sbin4_n1000
from BTA1P008 
UNION CORRESPONDING
select * from
( select * from VNA1P008) dt
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #
    # exit ;
    #
    
    _testmgr.testcase_end(desc)

def test020(desc="""b02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #
    #  Test case name:	T1100:B02
    #  Description:	This test verifies the SQL Derived table
    #                      features, with USING in join.
    #
    # =================== End Test Case Header  ===================
    #
    # ---------------------------
    # DT and Join with USING.
    # ---------------------------
    #
    # Need support for USING to limit columns used in NATURAL join;
    # otherwise, get 0 rows.
    
    stmt = """select char2_2
from BTA1P001 T1 
NATURAL join
 BTA1P005 T2 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select char2_2
from BTA1P001 T1 
NATURAL join
 BTA1P005 T2 
USING char2_2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select char2_2
from BTA1P003 T1 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s1')
    
    stmt = """select char2_2
from BTA1P006 T2 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b02exp""", 'b02s2')
    #
    # Need support for USING to limit columns used in NATURAL join;
    # otherwise, get 0 rows.
    stmt = """select char2_2
from BTA1P003 T1 
NATURAL join
 BTA1P006 T2 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select char2_2
from BTA1P003 T1 
NATURAL join
 BTA1P006 T2 
USING char2_2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #
    #  Need support for USING to limit columns used in NATURAL join;
    #  otherwise, get 0 rows.
    stmt = """select ca
from (select char2_2
from BTA1P001 T1 
NATURAL join
 BTA1P005 T2 
USING char2_2
) dt1(ca)
NATURAL join (select varchar2_10
from BTA1P003 T1 
NATURAL join
 BTA1P006 T2 
USING char2_2
) dt2(ca)
where dt1.ca = dt2.ca
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #
    # exit ;
    #
    
    _testmgr.testcase_end(desc)

def test021(desc="""n01"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    # Test case name:      T1100:N01
    # Description:         Negative test to verify the SQL Derived table
    #                      features, with UPDATE where ERROR truncation
    #                      should be reported.
    #
    # =================== End Test Case Header  ===================
    
    stmt = """set warnings off;"""
    output = _dci.cmdexec(stmt)
    
    #
    # ---------------------------
    # Make sure all tables start empty.
    # ---------------------------
    
    stmt = """Delete From T3 ;"""
    output = _dci.cmdexec(stmt)
    
    # ---------------------------
    #	Insert (preparation for subsequent update)
    # ---------------------------
    
    stmt = """insert into T3 
values ('1st orig value' ,99 , 'o'   , 1 )
, ('2nd orig value' ,98 , 'ov'  , 2 )
, ('3rd orig value' ,97 , 'ovc' , 3 )
, ('4th orig value' ,96 , 'ov ' , 4 )
, ('5th orig value' ,95 , 'o  ' , 5 )
, ('6 is short'     ,97 , 'o'   , 6 )
, ('7'              ,94 , 'OVC' , 7 )
, ('8th orig value' ,93 , 'OV'  , 8 )
, ('9th orig val  ' ,92 , 'O'   , 9 )
, ('10th val'       ,92 , 'O'   , 9 )
, ('11th val'       ,92 , 'O'   , 9 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 11)
    #
    #  ---------------------------
    #       Id: DT.047       Update with expressions, predicates, subqueries.
    #  ---------------------------
    #  From SQL test T016:A6
    #  Needs tables branch, parts, fromsup, employee.
    #     select correlated subquery in WHERE clause test - this tests the
    #     selection of aggregate functions (COUNT, AVG, MAX, MIN, SUM).
    #     Aggregates are tested in the SELECT clause and in the HAVING clause.
    
    #  Get partnames whose price is less than 2000 more than its
    #  average cost from all suppliers who supply it
    #  Expect 21 rows (character data) as in 1st example in T016:A6.
    
    stmt = """SELECT * FROM (       select partname
from PARTS 
where price <
(select avg(partcost) + 2000
from FROMSUP 
where partnum =  PARTS.partnum
)
) dt ORDER BY 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s0')
    #
    #  Get branchnames of branches whose total yearly payroll
    #  exceeds 150000
    #  Expect 4 rows (character data) as in 2nd example in T016:A6.
    stmt = """SELECT * FROM (       select branchname
from BRANCH 
where exists
(select regnum
from EMPLOYEE 
where  EMPLOYEE.regnum =  BRANCH.regnum
and    EMPLOYEE.branchnum =  BRANCH.branchnum
group by regnum, branchnum
having sum(salary) > 150000
)
) dt ORDER BY 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s1')
    #
    #  Get employee names of those employees whose age is greater
    #  than or equal to the max. age of the branch in their region
    #  with the highest average age (eliminate middle WHERE clause)
    #  Expect 12 rows (character data) as in 6th example in T016:A6.
    stmt = """SELECT * FROM (       select empname
from EMPLOYEE X
where age >=ALL
(select max(age)
from EMPLOYEE Y
group by regnum, branchnum
having Y.regnum = X.regnum
and avg(age) >=ALL
(select avg(age)
from EMPLOYEE Z
where Z.regnum = X.regnum
group by branchnum
)
)
) dt ORDER BY 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s2')
    #
    stmt = """select * from T3 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s3')
    #
    #  Addition because subquery appeared to not return MAX value for insert:
    stmt = """(select max(c) from
( SELECT * FROM
( select empname
from EMPLOYEE X
where age >=ALL
(select max(age)
from EMPLOYEE Y
group by regnum, branchnum
having Y.regnum = X.regnum
and avg(age) >=ALL
(select avg(age)
from EMPLOYEE Z
where Z.regnum = X.regnum
group by branchnum
)
)
) dt
) dt(c)
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s4')
    #
    #  Addition because subquery appeared to not return MAX value for insert:
    #  This shows ERROR on string overflow, as it should in SQL.
    stmt = """Update T3 set ch3   = -- char from 3rd DT
(select max(c) from
( SELECT * FROM
( select empname
from EMPLOYEE X
where age >=ALL
(select max(age)
from EMPLOYEE Y
group by regnum, branchnum
having Y.regnum = X.regnum
and avg(age) >=ALL
(select avg(age)
from EMPLOYEE Z
where Z.regnum = X.regnum
group by branchnum
)
)
) dt
) dt(c)
)
where nint=94
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    #  Addition because subquery appeared to not return MAX value for insert:
    #  This shows ERROR on string overflow, as it should in SQL.
    stmt = """Update T3 set ch3   = -- char from 3rd DT
(select max(c) from
( SELECT empname FROM EMPLOYEE 
) dt(c)
)
where nint=94
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    
    stmt = """select * from T3 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s7')
    #
    #  test 1100:A18 shows correct updates with Case.
    #
    #  Should show ERROR on string overflow.
    stmt = """Update T3 set vch15 = -- string from first DT
( select max(c) from
( SELECT partname
from PARTS 
) dt(c)
)
, ch3   = -- char from 3rd DT
(select min(c) from
( SELECT empname
from EMPLOYEE X
) dt(c)
)
where nint=94
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    
    stmt = """select * from T3 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s9')
    #
    #  Addition because subquery appeared to not return MAX value for insert.
    #  Bug.
    #  Should show ERROR on string overflow.
    stmt = """Update T3 set vch15 = -- string from first DT
( select max(c) from
( SELECT * FROM
( select partname
from PARTS 
where price <
(select avg(partcost) + 2000
from FROMSUP 
where partnum =  PARTS.partnum
)
) dt
) dt(c)
)
, ch3   = -- char from 3rd DT
(select min(c) from
( SELECT * FROM
( select empname
from EMPLOYEE X
where age >=ALL
(select max(age)
from EMPLOYEE Y
group by regnum, branchnum
having Y.regnum = X.regnum
and avg(age) >=ALL
(select avg(age)
from EMPLOYEE Z
where Z.regnum = X.regnum
group by branchnum
)
)
) dt
) dt(c)
)
where nint=94
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    stmt = """select * from T3 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s11')
    # Set string values.
    stmt = """Update T3 set vch15 = 'vch15' , ch3 = 'ch3' where nint=94 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from T3 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s12')
    #
    # ---------------
    #  Set Showshape On;
    # ---------------
    #
    #  Simplified 2nd query.
    #  Bug.
    #  Should show ERROR on string overflow.
    stmt = """Update T3 set vch15 = -- string from first DT
( select max(c) from
( SELECT * FROM
( select partname
from PARTS 
where price <
(select avg(partcost) + 2000
from FROMSUP 
where partnum =  PARTS.partnum
)
) dt
) dt(c)
)
, ch3   = -- char from 3rd DT
(select min(c) from
( SELECT * FROM
( select empname
from EMPLOYEE X
where age >=ALL
(select max(age)
from EMPLOYEE Y
group by regnum, branchnum
having Y.regnum = X.regnum
)
) dt
) dt(c)
)
where nint=94
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    stmt = """select * from T3 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s14')
    # Set string values.
    stmt = """Update T3 set vch15 = 'vch15' , ch3 = 'ch3' where nint=94 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from T3 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s15')
    #
    #  Simplified 1st as well as 2nd query.
    #  Bug.
    #  Should show ERROR on string overflow.
    stmt = """Update T3 set vch15 = -- string from first DT
( select max(c) from
( SELECT * FROM
( select partname
from PARTS 
) dt
) dt(c)
)
, ch3   = -- char from 3rd DT
(select min(c) from
( SELECT * FROM
( select empname
from EMPLOYEE X
where age >=ALL
(select max(age)
from EMPLOYEE Y
group by regnum, branchnum
having Y.regnum = X.regnum
)
) dt
) dt(c)
)
where nint=94
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    stmt = """select * from T3 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s17')
    # Set string values.
    stmt = """Update T3 set vch15 = 'vch15' , ch3 = 'ch3' where nint=94 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from T3 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s18')
    #
    #  Further simplified 2nd query.
    #  Bug.
    #  Should show ERROR on string overflow.
    stmt = """Update T3 set vch15 = -- string from first DT
( select max(c) from
( SELECT * FROM
( select partname
from PARTS 
) dt
) dt(c)
)
, ch3   = -- char from 3rd DT
(select min(c) from
( SELECT * FROM
( select empname
from EMPLOYEE X
where age >=ALL
(select max(age)
from EMPLOYEE Y
)
) dt
) dt(c)
)
where nint=94
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    stmt = """select * from T3 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s20')
    # Set string values.
    stmt = """Update T3 set vch15 = 'vch15' , ch3 = 'ch3' where nint=94 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from T3 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s21')
    #
    #  Further simplified 2nd query.
    #  Bug.
    #  Should show ERROR on string overflow.
    stmt = """Update T3 set vch15 = -- string from first DT
( select max(c) from
( SELECT * FROM
( select partname
from PARTS 
) dt
) dt(c)
)
, ch3   = -- char from 3rd DT
(select min(c) from
( SELECT * FROM
( select empname
from EMPLOYEE X
) dt
) dt(c)
)
where nint=94
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    stmt = """select * from T3 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s23')
    # Set string values.
    stmt = """Update T3 set vch15 = 'vch15' , ch3 = 'ch3' where nint=94 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from T3 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s24')
    #
    #  Further Simplified 1st as well as 2nd query.
    #  Bug.
    #  Should show ERROR on string overflow.
    stmt = """Update T3 set vch15 = -- string from first DT
( select max(c) from
( SELECT partname
from PARTS 
) dt(c)
)
, ch3   = -- char from 3rd DT
(select min(c) from
( SELECT * FROM
( select empname
from EMPLOYEE X
where age >=ALL
(select max(age)
from EMPLOYEE Y
group by regnum, branchnum
having Y.regnum = X.regnum
)
) dt
) dt(c)
)
where nint=94
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    stmt = """select * from T3 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s26')
    # Set string values.
    stmt = """Update T3 set vch15 = 'vch15' , ch3 = 'ch3' where nint=94 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from T3 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s27')
    #
    #  Further simplified 2nd query. (1st query not simplified).
    #  Does show ERROR on string overflow.
    stmt = """Update T3 set vch15 = -- string from first DT
( select max(c) from
( SELECT * FROM
( select partname
from PARTS 
where price <
(select avg(partcost) + 2000
from FROMSUP 
where partnum =  PARTS.partnum
)
) dt
) dt(c)
)
, ch3   = -- char from 3rd DT
(select min(c) from
( SELECT * FROM
( select empname
from EMPLOYEE X
) dt
) dt(c)
)
where nint=94
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    stmt = """select * from T3 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s29')
    # Set string values.
    stmt = """Update T3 set vch15 = 'vch15' , ch3 = 'ch3' where nint=94 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from T3 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s30')
    #
    #  With first portion set to literal, get correct overflow error.
    #  Should show ERROR on string overflow.
    stmt = """Update T3 set vch15 = 'x'
, ch3   = -- char from 3rd DT
(select min(c) from
( SELECT * FROM
( select empname
from EMPLOYEE X
where age >=ALL
(select max(age)
from EMPLOYEE Y
group by regnum, branchnum
having Y.regnum = X.regnum
and avg(age) >=ALL
(select avg(age)
from EMPLOYEE Z
where Z.regnum = X.regnum
group by branchnum
)
)
) dt
) dt(c)
)
where nint=94
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    stmt = """select * from T3 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s32')
    # Set string values.
    stmt = """Update T3 set vch15 = 'vch15' , ch3 = 'ch3' where nint=94 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from T3 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s33')
    #
    #  Should show ERROR on string overflow.
    stmt = """Update T3 set vch15 = -- string from first DT
( select max(c)||max(c)||max(c) from
( SELECT partname
from PARTS 
) dt(c)
)
, ch3   = -- char from 3rd DT
(select cast( min(c) As Char(3) ) from
( SELECT empname
from EMPLOYEE X
) dt(c)
)
where nint=94
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    stmt = """select * from T3 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s35')
    # Set string values.
    stmt = """Update T3 set vch15 = 'vch15' , ch3 = 'ch3' where nint=94 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from T3 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s36')
    #
    # ---------------------------
    # Clean up tables at the end.
    # ---------------------------
    stmt = """Delete From T3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 11)
    
    _testmgr.testcase_end(desc)

