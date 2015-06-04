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
    #  Test case name:     T1110:A01
    #  Description:        This test verifies Simple Select and Join of data
    #                      that are taken from an indexed column and a
    #                      non-indexed column of a table; implementationally
    #                      (as checked in Optimizer tests) the latter may use
    #                      non-index-only scan.
    
    # =================== End Test Case Header  ===================
    #
    #  Look at the data, explicitly ordering by primary key.
    
    stmt = """select * from TAB1 order by pkvca , nintb;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    stmt = """select * from TAB2 order by pkvcg , nintc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    #
    #  ---------------------------
    #  Non-index-only scans.
    #  ---------------------------
    #
    #  Note below where special correlation names are used to "fake"
    #  larger row counts.
    #
    #  ---------------------------
    #  test index-only access
    #  ---------------------------
    #
    #  ---------------------------
    #       Id: IX.041      Access column at end of composite primary key or index (index-only access).
    #  ---------------------------
    #  Expect (1), (7), (4) in this order
    stmt = """select nintb from TAB1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    #
    #  Expect 2 * ('LONG1 c5'), ('LONG1 c7'), ('LONG1 c5') , ('e')
    # 	in this order
    stmt = """select vce from TAB2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    #
    #  Expect (101), (101), (100), (5), (7) in this order
    stmt = """select endcomposxf from TAB2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    #
    #  ---------------------------
    #       Id: IX.042      Access column at start of composite primary key or index (index-only access).
    #                       Results should be in order because of indexes and key.
    #                       TAB1's primary key (pkvca , nintb).
    #                          create index I1TAB1 on TAB1(vcc);
    #                          create index I2TAB1 on TAB1(vce);
    #                       TAB2's primary key (pkvcg , nintc , vce )
    #                          Includes index on column that is also part of a
    #                          composite key; leave one column un-indexed.
    #                          Indexes are I1TAB2 has TAB2(vca);
    #                                index I2TAB2 has TAB2(vcb, endcomposxf);
    #                                index I3TAB2 has TAB2(vce);
    #  ---------------------------
    #
    #  Expect 3 result rows * ('a...b')
    stmt = """select 'a'||'...'||'b' from TAB1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    #
    #  Expect 3 result rows: 2 * ('Duplicate allowed...END'),
    # 	('Index col...END')
    stmt = """select vcc||'...'||'END' from TAB1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')
    #
    #  Expect 3 result rows: 2 * ('Duplicate allowed...Duplicate allowed'),
    # 	('Index col...Index col')
    stmt = """select vcc||'...'||vcc
from TAB1 where vcc = vcc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s7')
    #
    #  Expect 3 result rows: ('01 No dup...')
    #  ('02 No dup...')
    #  ('03 No dup...') ordered by pkvca
    stmt = """select pkvca ||'...'
from TAB1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s8')
    #
    #  Expect 3 result rows: (('...1') ('...4')
    #                         ('...7')) ordered by nintb
    stmt = """select '...'|| cast(nintb as pic x(9)) as concat_cast_int_as_picx
from TAB1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s9')
    #
    #  Expect 3 result rows: (('...1                      ')
    #  (Columns 3 char longer than concat_cast_int_as_picx)
    #                         ('...4                      ')
    #                         ('...7                      ')) ordered by nintb
    stmt = """select '...'|| cast(nintb as pic x(23)) as concat_cast_int_as_picx
from TAB1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s10')
    #
    #  Expect ('LONG1 c5'),  ('LONG1 c5'),  ('LONG1 c5'),
    #         ('LONG1 c7'),  ('e')
    stmt = """select vce from TAB2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s11')
    #
    #  Expect 2* ('LONG1 c1'),  2* ('ddd'), (?)
    stmt = """select vca from TAB2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s12')
    #
    #  ---------------------------
    #       Id: IX.043      Join of two indexes
    #  ---------------------------
    #
    #  ??? What determines Order?
    #  Expect ('e...Duplicate allowed'), ('ee...Duplicate allowed'),
    #         ('eee...Index col')
    stmt = """select vce||'...'||vcc from TAB1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s13')
    #
    #  Expect (' 4  Duplicate allowed...01 No dup') ,
    # 	  (' 7  Index col...02 No dup') ,
    # 	  ('10  Duplicate allowed...03 No dup')
    stmt = """select nintb+3, vcc||'...'||pkvca from TAB1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s14')
    #
    #  Expect (1), (7), (4)
    stmt = """select nintb from TAB1 order by vcc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s15')
    #
    #  Expect (4)
    stmt = """select nintb from TAB1 where vcc > 'E';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s16')
    #
    #  ---------------------------
    #       Id: IX.044      Use of index for groupby
    #  ---------------------------
    #
    #  Expect 2 rows: ('Duplicate allowed', 'dd') ,('Index col', 'ddd')
    stmt = """select vcc,max(noindexvcd) from TAB1 group by vcc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s17')
    #
    #  index-only access with groupby
    #  Expect 2 rows: ('Duplicate allowed', 2) ,('Index col', 1)
    stmt = """select vcc,count(*) from TAB1 group by vcc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s18')
    #
    #  Expect 3 rows: ('01 No dup', 1) ,('02 No dup', 1) ,('03 No dup', 1)
    stmt = """select pkvca,count(*) from TAB1 group by pkvca;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s19')
    #
    #  ---------------------------
    #       Id: IX.045      Use of index for join
    #  ---------------------------
    #
    #  Expect ( 1 , ' Duplicate allowed') ,
    # 	  ( 4 , ' Index col') ,
    # 	  ( 7 , ' Duplicate allowed')
    stmt = """select x.nintb, y.vcc
from TAB1 x join TAB1 y
on x.pkvca=y.pkvca
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s20')
    #
    #  Expect ( 1 , ' Duplicate allowed') ,
    # 	  ( 4 , ' Index col') ,
    # 	  ( 7 , ' Duplicate allowed')
    stmt = """select x.nintb, y.vcc
from TAB1 x join TAB1 y
on x.nintb=y.nintb;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s21')
    #
    #  >>    select * from TAB1 order by 1;
    #  PKVCA                  NINTB        VCC                    NOINDEXVCD             VCE
    #  ---------------------  -----------  ---------------------  ---------------------  ---------------------
    #  01 No dup                        1  Duplicate allowed      d                      e
    #  02 No dup                        7  Index col              ddd                    eee
    #  03 No dup                        4  Duplicate allowed      dd                     ee
    #  --- 3 row(s) selected.
    #  >>    select * from TAB2 order by 1;
    #  VCA        VCB        NINTC        NOINDEXVCD  VCE        ENDCOMPOSXF  PKVCG
    #  ---------  ---------  -----------  ----------  ---------  -----------  ---------
    #  LONG1 c1   LONG1 c2             4           ?  LONG1 c7           100  03 No dup
    #  LONG1 c1   LONG1 c2             7  LONG1 c4    LONG1 c5           101  02 No dup
    #  ddd        ee                   3  d           e                    7  Dup Key 1
    #  ddd        ee                   2  LONG3 c4    LONG1 c5             5  Dup Key 1
    #          ?  LONG1 c2             1  LONG1 c4    LONG1 c5           101  01 No dup
    # - 5 row(s) selected.
    #
    #  Expect 15 rows -- the cross product.
    #  ++++++++++++++++++++++++++++++
    stmt = """select rows1E5.pkvca, rows1E4.vca
,   rows1E5.vcc, rows1E4.noindexvcd
from TAB1 rows1E5 join TAB2 rows1E4
on rows1E5.pkvca<>rows1E4.vca
order by 1,2,3,4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s22')
    #
    #  ++++++++++++++++++++++++++++++
    stmt = """select rows1E5.pkvca, rows1E4.vca
,   rows1E5.vcc, rows1E4.noindexvcd
from TAB1 rows1E5 join TAB2 rows1E4
on rows1E5.vcc < rows1E4.noindexvcd
order by 1,2,3,4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s23')
    #
    #  ++++++++++++++++++++++++++++++
    stmt = """select rows1E5.pkvca, rows1E4.vca
,   rows1E5.vcc, rows1E4.noindexvcd
from TAB1 rows1E5 join TAB2 rows1E4
on rows1E5.pkvca<>rows1E4.vca
and rows1E5.vcc < rows1E4.noindexvcd
order by 1,2,3,4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s24')
    #
    #  ++++++++++++++++++++++++++++++
    #  Expect 9 rows (cross product)
    stmt = """select          rows1E5.vca, rows1E4.vca, rows1E5.vce, rows1E4.vce
from TAB2 rows1E5 join TAB2 rows1E4
on (1=1)
order by 1,2,3,4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s25')
    #
    #  ++++++++++++++++++++++++++++++
    #  Expect 8 rows (omit NULL).
    stmt = """select          rows1E5.vca, rows1E4.vca, rows1E5.vce, rows1E4.vce
from TAB2 rows1E5 join TAB2 rows1E4
on rows1E5.vca   =rows1E4.vca
order by 1,2,3,4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s26')
    #
    #  ++++++++++++++++++++++++++++++
    #  Expect 6 rows (omit inequalities).
    stmt = """select          rows1E5.vca, rows1E4.vca, rows1E5.vce, rows1E4.vce
from TAB2 rows1E5 join TAB2 rows1E4
on rows1E5.vca   =rows1E4.vca
and rows1E5.vce >=rows1E4.vce
order by 1,2,3,4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s27')
    #
    #  ---------------------------
    #       Id: IX.046      Use of index for union all, union, ordered union
    #  ---------------------------
    #
    #  Expect 6 rows.
    stmt = """select vce from TAB1 
union all
select noindexvcd from TAB1 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s28')
    #
    #  Expect 5 rows.
    stmt = """select vcc from TAB1 
union
select pkvca from TAB1 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s29')
    #
    #  Expect (('Index col'))
    stmt = """select *
from (select vcc from TAB1 
union all
select pkvca from TAB1 
) as t(y)
where y > 'E' order by y
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s30')
    #
    #  Expect 4 rows (4),(5),(7),(8) in this order
    stmt = """select *
from (select nintb+1 from TAB1 
union
select nintb from TAB1 
) as t(y)
where y between 3 and 13 order by y
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s31')
    #
    #  Scaffold: 3 rows.
    stmt = """select nintb+1,vcc from TAB1 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s32')
    #  Scaffold: 3 rows.
    stmt = """select nintb, pkvca||'...'||'A' from TAB1 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s33')
    #  Scaffold: 6 rows
    stmt = """select nintb+1,vcc from TAB1 
union all
select nintb, pkvca||'...'||'A' from TAB1 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s34')
    #  Expect ((7 'Duplicate allowed')) because 'Duplicate allowed'
    #  is the only duplicate value of VCC.
    stmt = """select sum(y), z
from (select nintb+1,vcc from TAB1 
union all
select nintb, pkvca||'...'||'A' from TAB1 
) as t(y,z)
group by z having count(*) > 1 order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s35')
    #
    #  ---------------------------
    #       Id: IX.047      Use of index for distinct aggregates
    #  ---------------------------
    #
    #  Expect ((2))
    stmt = """select count(distinct vca) from TAB2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s36')
    #
    #  Expect (('Dup Key 1'))
    stmt = """select max(distinct pkvcg) from TAB2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s37')
    #
    #  Expect (('LONG1 c4...ee...LONG1 c1'))
    stmt = """select min(distinct noindexvcd) ||'...'|| max(distinct vcb) ||'...'|| min(vca)
from TAB2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s38')
    #
    #  Expect ((1) (1))
    stmt = """select count(distinct vca) from TAB2 group by vcb;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s39')
    #
    #  Expect ((1) (1) (1))
    stmt = """select count(distinct vcb) from TAB2 group by vca;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s40')
    #
    #  Expect 3 rows:
    #       (('LONG1 c1...C' 1 'LONG1 c4')
    #        ('ddd...C'      1 'd')
    #        ( NULL          1 'LONG1 c4'))
    stmt = """select vca||'...'||'C',count(distinct vcb),max(distinct noindexvcd)
from TAB2 group by vca
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s41')
    #
    stmt = """select count(distinct vcb), min(distinct vcb),
cast(count(distinct vcb)/count(distinct vcb) as int)
from TAB2 group by vca
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s42')
    #
    #  Expect 4 rows; this works after 'common item subexpressions'
    #  are implemented
    stmt = """select max(distinct vca||'...'|| vcb),
count(distinct vca||'...'|| vcb), max(pkvcg)
from TAB2 group by noindexvcd
order by 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s43')
    #
    #  ---------------------------
    #       Id: IX.048     Use of index for queries where SQL should eliminate unnecessary groupbys
    #  ---------------------------
    #
    stmt = """select distinct pkvca,nintb from TAB1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s44')
    #
    stmt = """select count(distinct pkvcg) from TAB2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s45')
    #
    #  Expect 3 rows.
    stmt = """select pkvca,nintb,vcc,cast(max(noindexvcd) as char(3))
from TAB1 
group by pkvca,nintb,vcc
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s46')
    #
    #  Expect 3 rows.
    stmt = """select vca,sum(distinct nintc ),max(distinct vcb),count(vcb)
from TAB2 group by vca
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s47')
    #
    #  Expect 9 rows of cross product!
    stmt = """select xa,yb,count(*)
from (select * from TAB1 x
cross join TAB1 y
) as j(xa,xb,xc,xd,xe,ya,yb,yc,yd,ye)
group by xa,xb,ya,yb
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s48')
    #
    # ++++++++++++++++++++++++++++++
    stmt = """select a1,c2,count(*)
from (select * from TAB1,TAB2 
) as t(a1,b1,c1,d1,e1,a2,b2,c2,d2,e2,f2,g2)
where a1 > '02' and b2 < 'E'
group by a1,b1,c2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #
    #  Expect 3 rows.
    stmt = """select pkvca,min(vcc),max(noindexvcd ||'...'|| 'MAX' )
from TAB1 
group by pkvca,nintb
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s49')
    
    _testmgr.testcase_end(desc)

def test002(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    # Test case name:      T1110:A02
    # Description:         This test verifies Simple Select and Join of data
    #                      that are taken from an indexed column and a
    #                      non-indexed column of a table; implementationally
    #                      (as checked in Optimizer tests) the latter may
    #                      use non-index-only scan.
    #
    # =================== End Test Case Header  ===================
    #
    # ---------------------------------------
    # Set up defines globally, then reset with local override for SCHEMA.
    # Set up defines globally.
    # *** EITHER rely on global database including indexes.
    # *** OR make local copy and control indexes.
    # ---------------------------------------
    #
    #  Indexes of global tables:
    #  Scaffolding, to test index-only access, and to check
    #  the values of interest.
    #
    #  Access index columns; should be reported in index order.
    #
    #  ---------------------------
    #  BTA1P001 has multi-column indexes.
    #  ---------------------------
    #
    #  Primary key is ( varchar5_10, ubin15_uniq , char0_10 ).
    #  This set of indexes overlaps columns:
    #    INA1PA04 ( sbin16_20, sbin17_uniq, sbin12_1000, char6_20, udec5_20 ) ;
    #    INA1PA05 ( sbin16_20, sbin17_uniq, sbin12_1000, char6_20 ) ;
    #    INA1PA06 ( sbin16_20, sbin17_uniq, sbin12_1000 ) ;
    #    INA1PA07 ( sbin16_20, sbin17_uniq ) ;
    #    INA1PA08 ( sbin16_20 ) ;
    #
    #  All columns in a primary key:
    
    stmt = """select varchar5_10, ubin15_uniq, char0_10
from BTA1P001 t1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    #
    #  All columns present in an alternate key:
    stmt = """select varchar5_10, ubin15_uniq , varchar0_4 , varchar15_uniq
from BTA1P001 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    stmt = """select sbin16_20, sbin17_uniq, sbin12_1000, char6_20, udec5_20
from BTA1P001 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    stmt = """select sbin16_20, sbin17_uniq
from BTA1P001 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    #
    #  Non-key columns.
    stmt = """select t1.char19_2, t1.udec20_uniq, t1.sbin19_4
from BTA1P001 t1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s4')
    #
    #  ---------------------------
    #  BTA1P006 has single-column alternate indexes.
    #  ---------------------------
    #
    #  All columns present in a primary key:
    #
    stmt = """select sdec9_uniq , sdec0_100 , sdec1_20
from BTA1P006 t1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')
    #
    #  Columns present in an alternate key:
    stmt = """select varchar0_uniq from BTA1P006 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s6')
    stmt = """select CHAR3_4 from BTA1P006 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s7')
    stmt = """select CHAR5_N20 from BTA1P006 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s8')
    stmt = """select SBIN0_4 , SDEC6_4 from BTA1P006 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s9')
    #
    #  Non-key columns.
    #
    stmt = """select char15_100 -- varchar
from BTA1P006 t1
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s10')
    stmt = """select ubin16_n10 -- NULL values
from BTA1P006 t1
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s11')
    stmt = """select sbin17_uniq
, sdec17_nuniq -- Allows NULL
, char17_2     -- varchar
from BTA1P006 t1
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s12')
    #
    #  ---------------------------
    #       Id: JT.051      Index joins, non-index-only scans: RIGHT JOIN on single index column.
    #  ---------------------------
    #  That is:
    #  SELECT { * | <non-index-cols>} FROM Table1
    #  RIGHT JOIN Table2
    #  ON <index1-col1> = <value>
    #  ORDER BY {<index1-col1> |<index1-col2>} ;
    #
    #  Examples:
    #  SELECT <non-index-cols> FROM Table1
    #    ORDER BY <index1 col1> ;
    #
    #  SELECT * FROM Table1
    #    RIGHT JOIN Table2
    #    ON <index1 col1> = <value1>
    #    ORDER BY <index1 col1> ;
    #
    #  SELECT * FROM Table1
    #    RIGHT JOIN Table2
    #    ON <index1 col1> = <value1>
    #    ORDER BY <index1 col2> ;
    #
    #  SELECT * FROM Table1
    #    RIGHT JOIN Table2
    #    ON <index2 col1> = <value2>
    #    ORDER BY <index1 col1> ;
    #
    #  ---------------------------
    #  Index joins: RIGHT JOINs, access one (1) column of an index.
    #  Non-index-only scan.  Select * or select non-index columns
    #  ---------------------------
    #
    #  Should get same order with or without ORDER BY.
    #  Note, if you want to ORDER BY any column, you get "error"
    #  that "column is not in table", unless you include that column in
    #  the select list.
    #
    #  SELECT <non-index-cols> FROM Table1
    #    ORDER BY <index1 col1> ;
    stmt = """select char15_100, char17_2 -- varchar non-key
from BTA1P006 t1
order by varchar0_uniq ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s13')
    #
    #  Expect 16.
    stmt = """SELECT count(*) FROM
( SELECT t1.char15_100, t2.char17_2
FROM BTA1P006 t1
RIGHT JOIN BTA1P006 t2
ON t1.varchar0_uniq = t2.varchar0_uniq
) dt
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s14')
    #
    #  Join on leading key column sbin16_20 of indexes INA1PA04 to INA1PA08.
    #
    #  Expect 4.
    stmt = """SELECT count(*) FROM
( SELECT * FROM BTA1P001 t1
RIGHT JOIN BTA1P001 t2
ON t1.sbin16_20 = 0.1
) dt
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s15')
    #
    #  Should get same order with or without ORDER BY.
    #
    stmt = """SELECT t1.char19_2, t1.udec20_uniq, t2.sbin19_4
FROM BTA1P001 t1
RIGHT JOIN BTA1P001 t2
ON t2.sbin16_20 >= 0.06
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s16')
    stmt = """SELECT t1.char19_2, t1.udec20_uniq, t2.sbin19_4
FROM BTA1P001 t1
RIGHT JOIN BTA1P001 t2
ON t2.sbin16_20 >= 0.06
ORDER BY t2.sbin16_20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s17')
    #
    #  Add GROUP BY on all columns.
    #
    stmt = """SELECT t1.char19_2, t1.udec20_uniq, t2.sbin19_4
FROM BTA1P001 t1
RIGHT JOIN BTA1P001 t2
ON t1.sbin16_20 >= 0.06
GROUP BY t1.sbin16_20
, t1.char19_2, t1.udec20_uniq, t2.sbin19_4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s18')
    stmt = """SELECT t1.char19_2, t1.udec20_uniq, t2.sbin19_4
, t1.sbin16_20
FROM BTA1P001 t1
RIGHT JOIN BTA1P001 t2
ON t1.sbin16_20 >= 0.06
GROUP BY t1.sbin16_20
, t1.char19_2, t1.udec20_uniq, t2.sbin19_4
ORDER BY t1.sbin16_20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s19')
    #
    #  Should get same order with or without ORDER BY.
    #
    stmt = """SELECT t1.char19_2, t1.udec20_uniq, t2.sbin19_4
FROM BTA1P001 t1
RIGHT JOIN BTA1P001 t2
ON t1.varchar5_10 LIKE 'ABB%'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s20')
    stmt = """SELECT t1.char19_2, t1.udec20_uniq, t2.sbin19_4
FROM BTA1P001 t1
RIGHT JOIN BTA1P001 t2
ON t1.varchar5_10 LIKE 'ABB%'
ORDER BY t1.varchar5_10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s21')
    #
    #  ---------------------------
    #       Id: JT.053      Index joins, non-index-only scans: NATURAL JOIN on single index columns.
    #  ---------------------------
    #  That is:
    #  SELECT col-non-indexes FROM Table1
    #    NATURAL JOIN Table2
    #    ORDER BY <index1 col1> ;
    #
    #  ---------------------------
    #  Also Index joins: NATURAL JOINs, access one (1) column of an index.
    #  ---------------------------
    #
    #  Expect 4.
    stmt = """SELECT count(*) FROM
( SELECT * FROM BTA1P001 t1
NATURAL JOIN BTA1P001 t2
WHERE sbin16_20 = 0.1
) dt
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s22')
    #
    #  Should get same order with or without ORDER BY.
    #
    stmt = """SELECT char19_2, udec20_uniq, sbin19_4 -- , char20_10
FROM BTA1P001 t1
NATURAL JOIN BTA1P001 t2
WHERE sbin16_20 >= 0.06
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s23')
    stmt = """SELECT char19_2, udec20_uniq, sbin19_4 -- , char20_10
FROM BTA1P001 t1
NATURAL JOIN BTA1P001 t2
WHERE sbin16_20 >= 0.06
ORDER BY sbin16_20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s24')
    #
    #  Add GROUP BY on all columns.
    #
    stmt = """SELECT char19_2, udec20_uniq, sbin19_4 -- , char20_10
FROM BTA1P001 t1
NATURAL JOIN BTA1P001 t2
WHERE sbin16_20 >= 0.06
GROUP BY sbin16_20
, char19_2, udec20_uniq, sbin19_4 -- , char20_10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s25')
    stmt = """SELECT char19_2, udec20_uniq, sbin19_4 -- , char20_10
, sbin16_20
FROM BTA1P001 t1
NATURAL JOIN BTA1P001 t2
WHERE sbin16_20 >= 0.06
GROUP BY sbin16_20
, char19_2, udec20_uniq, sbin19_4 -- , char20_10
ORDER BY sbin16_20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s26')
    #
    #  Should get same order with or without ORDER BY.
    stmt = """SELECT char19_2, udec20_uniq, sbin19_4 -- , char20_10
FROM BTA1P001 t1
NATURAL JOIN BTA1P001 t2
WHERE varchar5_10 LIKE 'ABB%'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s27')
    stmt = """SELECT char19_2, udec20_uniq, sbin19_4 -- , char20_10
FROM BTA1P001 t1
NATURAL JOIN BTA1P001 t2
WHERE varchar5_10 LIKE 'ABB%'
ORDER BY varchar5_10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s28')
    #
    #  ---------------------------
    #       Id: JT.052      Index joins, non-index-only scans: RIGHT JOIN on several index columns.
    #  ---------------------------
    #  Select non-key columns, comparing data using multiple alternate
    #  key columns in ON clause, WHERE clause, ORDER BY, and GROUP BY.
    #  The WHERE clause and the ORDER BY clause should influence the
    #  optimizer to use the index.
    #  ---------------------------
    #
    #  That is:
    #  SELECT col-non-indexes FROM Table1
    #    RIGHT JOIN Table2
    #    ON (<index1 col1>, <index1 col2>) = ( <value1>, <value2 > )
    #    ORDER BY <index1 col1>,<index1 col2> ;
    #
    #  SELECT * FROM Table1, Table2, ...
    #    WHERE (<index1 column1>, <index1 column2>, ...)
    #      = <value1,value2,...>
    #    GROUP BY <index1 col1>,<index1 col2>,... ;
    #
    #  BTA1P006 has single-column indexes.
    #
    #  Scaffold:
    stmt = """SELECT t1.char15_100, char17_2, CHAR5_N20, CHAR3_4, SBIN0_4, SDEC6_4
FROM BTA1P006 t1
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s29')
    #  Expect 5 +++++++++++++++++++++= or 4?
    stmt = """SELECT count(*) FROM
( SELECT t1.char15_100, t2.char17_2
FROM BTA1P006 t1
RIGHT JOIN BTA1P006 t2
ON t1.CHAR5_N20 = t2.CHAR3_4 and t1.SBIN0_4 <> t2.SDEC6_4
) dt
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s30')
    #  Expect 5 +++++++++++++++++++++= or 4?
    stmt = """SELECT count(*) FROM
( SELECT t1.char15_100, t2.char17_2
FROM BTA1P006 t1
RIGHT JOIN BTA1P006 t2
ON (t1.CHAR5_N20, t1.SBIN0_4) = ( t2.CHAR3_4 , t2.SDEC6_4 )
) dt
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s31')
    #
    #  BTA1P001 has multi-column indexes.
    #
    #  Only 1 row matches; expect 6 rows.
    stmt = """SELECT 'AB'||t1.varchar5_10 , t2.VARCHAR15_UNIQ
, t1.char19_2, t1.udec20_uniq, t2.sbin19_4 -- , t2.char20_10
FROM BTA1P001 t1
RIGHT JOIN BTA1P001 t2
ON 'AB'||t1.varchar5_10 = t2.VARCHAR15_UNIQ
ORDER BY t2.VARCHAR15_UNIQ
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s32')
    #
    #  Order by a different column (indexed) than the indexed column in
    #  the ON clause.
    #
    stmt = """SELECT 'AB'||t1.varchar5_10 , t2.VARCHAR15_UNIQ, t2.sbin16_20
, t1.char19_2, t1.udec20_uniq, t2.sbin19_4 -- , t2.char20_10
FROM BTA1P001 t1
RIGHT JOIN BTA1P001 t2
ON 'AB'||t1.varchar5_10 = t2.VARCHAR15_UNIQ
ORDER BY t2.sbin16_20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s33')
    #
    #  Expect 10.
    stmt = """SELECT count(*) FROM BTA1P001 t1
RIGHT JOIN BTA1P001 t2
ON t1.sbin16_20 = t2.sbin16_20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s34')
    #
    #  Expect 10.
    stmt = """SELECT count(*) FROM
( SELECT * FROM BTA1P001 t1
RIGHT JOIN BTA1P001 t2
ON t1.sbin16_20 = t2.sbin16_20
) dt
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s35')
    #
    #  ---------------------------
    #       Id: JT.054      Index joins, non-index-only scans: NATURAL JOIN on several index columns.
    #  ---------------------------
    #  That is:
    #  SELECT col-non-indexes FROM Table1
    #    NATURAL JOIN Table2
    #    ORDER BY <index1 col1>,<index1 col2> ;
    #
    #  BTA1P006 has single-column indexes.
    #
    #  Expect 5
    stmt = """SELECT count(*) FROM
( SELECT char15_100, char17_2
FROM BTA1P006 t1
NATURAL JOIN BTA1P006 t2
) dt
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s36')
    #
    #  BTA1P001 has multi-column indexes.
    #
    #  Select non-key (and key) columns, comparing data using multiple alternate
    #  key columns in WHERE clause, ORDER BY, and GROUP BY.
    #
    stmt = """SELECT VARCHAR15_UNIQ , varchar5_10 -- , VARCHAR15_UNIQ -- don't duplicate cols in NJ?
FROM BTA1P001 t1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s37')
    #
    stmt = """SELECT varchar5_10 , VARCHAR15_UNIQ
FROM BTA1P001 t1
WHERE 'AB'||varchar5_10 = VARCHAR15_UNIQ
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s38')
    #
    #  Only 1 row matches; expect 6 rows.
    stmt = """SELECT 'AB'||varchar5_10 , VARCHAR15_UNIQ
, char19_2, udec20_uniq, sbin19_4 -- , char20_10
FROM BTA1P001 t1
NATURAL JOIN BTA1P001 t2
WHERE 'AB'||varchar5_10 = VARCHAR15_UNIQ
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s39')
    #
    #  Add ORDER BY -- AND add item to select list.
    stmt = """SELECT 'AB'||varchar5_10 , VARCHAR15_UNIQ
, char19_2, udec20_uniq, sbin19_4 -- , char20_10
FROM BTA1P001 t1
NATURAL JOIN BTA1P001 t2
WHERE 'AB'||varchar5_10 = VARCHAR15_UNIQ
ORDER BY VARCHAR15_UNIQ
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s40')
    #
    #  Add GROUP BY.
    stmt = """SELECT 'AB'||varchar5_10 , VARCHAR15_UNIQ
, sbin16_20
, char19_2, udec20_uniq, sbin19_4 -- , char20_10
--      , VARCHAR15_UNIQ
FROM BTA1P001 t1
NATURAL JOIN BTA1P001 t2
WHERE 'AB'||varchar5_10 = VARCHAR15_UNIQ
GROUP BY sbin16_20
, varchar5_10 , VARCHAR15_UNIQ
, sbin16_20
, char19_2, udec20_uniq, sbin19_4 -- , char20_10
ORDER BY VARCHAR15_UNIQ
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s41')
    #
    #  This should be legal:
    stmt = """SELECT VARCHAR15_UNIQ , VARCHAR15_UNIQ
FROM BTA1P001 t1
NATURAL JOIN BTA1P001 t2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s42')
    stmt = """SELECT VARCHAR15_UNIQ , VARCHAR15_UNIQ
FROM BTA1P001 t1
NATURAL JOIN BTA1P001 t2
ORDER BY 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s43')
    stmt = """SELECT VARCHAR15_UNIQ , VARCHAR15_UNIQ
FROM BTA1P001 t1
NATURAL JOIN BTA1P001 t2
WHERE 'AB'||varchar5_10 = VARCHAR15_UNIQ
ORDER BY 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s44')
    #  NOTE: Illegal to perform GROUP BY <column> nor
    #  ORDER BY <column> on NATURAL JOIN columns.
    #
    #  Order by a different column (indexed) than the indexed column in
    #  the WHERE clause.
    #
    stmt = """SELECT 'AB'||varchar5_10 , VARCHAR15_UNIQ, sbin16_20
, char19_2, udec20_uniq, sbin19_4 -- , char20_10
FROM BTA1P001 t1
NATURAL JOIN BTA1P001 t2
WHERE 'AB'||varchar5_10 = VARCHAR15_UNIQ
ORDER BY sbin16_20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s45')
    #
    #  Add GROUP BY.
    stmt = """SELECT 'AB'||varchar5_10 , VARCHAR15_UNIQ, sbin16_20
, char19_2, udec20_uniq, sbin19_4 -- , char20_10
FROM BTA1P001 t1
NATURAL JOIN BTA1P001 t2
WHERE 'AB'||varchar5_10 = VARCHAR15_UNIQ
GROUP BY sbin16_20
, varchar5_10 , VARCHAR15_UNIQ, sbin16_20
, char19_2, udec20_uniq, sbin19_4 -- , char20_10
ORDER BY sbin16_20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s46')
    #
    stmt = """SELECT sbin16_20 , sbin19_4 FROM BTA1P001 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s47')
    #
    #  Expect 10.
    stmt = """SELECT count(*) FROM BTA1P001 t1
NATURAL JOIN BTA1P001 t2
WHERE sbin16_20 <> sbin19_4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s48')
    #
    stmt = """SELECT count(*) FROM
( SELECT * FROM BTA1P001 t1
NATURAL JOIN BTA1P001 t2
WHERE sbin16_20 <> sbin19_4
) dt
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s49')
    #
    #  ---------------------------
    #  (97-02-21) These statements placed at the end because of seg fault!
    #  ---------------------------
    stmt = """SELECT count(*) FROM BTA1P001 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s50')
    stmt = """SELECT t2.sbin16_20 FROM BTA1P001 t2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s51')
    stmt = """SELECT t1.sbin16_20 , t2.sbin16_20 FROM BTA1P001 t1
RIGHT JOIN BTA1P001 t2
ON 0.1 = 0.1
Order By 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s52')
    stmt = """SELECT t1.sbin16_20 , t2.sbin16_20 FROM BTA1P001 t1
RIGHT JOIN BTA1P001 t2
ON t2.sbin16_20 = 0.1
Order By 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s53')
    #
    #  Expect 16 (4*4).
    stmt = """SELECT count(*) FROM
( SELECT * FROM BTA1P001 t1
RIGHT JOIN BTA1P001 t2
ON t2.sbin16_20 = 0.1
) dt
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s54')
    
    _testmgr.testcase_end(desc)

def test003(desc="""a04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    # Test case name:      T1110:A04
    # Description:         This test verifies Insert, Update, Delete of
    #                      data in indexed columns.
    #
    # =================== End Test Case Header  ===================
    #
    # Make sure that table starts empty.
    
    stmt = """Delete from Twide1;"""
    output = _dci.cmdexec(stmt)
    
    # ---------------------------
    #      Id: IX.091      Insert into 60-index table.
    # ---------------------------
    #
    # Insert values; include duplicates of data in other rows,
    # except for the Indexes required to be Distinct.
    #
    # The following column sequence gives more than one
    # identical value in the first column of the primary key.
    #   , primary  key ( varchar11_2 DESC ASC -- Column 38.
    #       , varchar2_10     ASC -- Column 8
    #       , varchar15_uniq  ASC -- Column 18 from the end.
    #
    # Insert into Wide table with an index on each column.
    # 5th row has all identical except for last field of primary key.
    # 6th and 7th rows insert into a subset of rows.
    stmt = """Insert Into Twide1 
Values ('BQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
'CCAAKAAAAAAAAAAAAAAAAAAAAAAAAAAA', 40,
'BAAA ', 0,
'AB', 'BB',
'DQAAAAAAAAAAAAAA         ', 7,
'CHAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
7, .1, .3,
'CCAAKAAAAAAAAAAA', .1, .1, 0, 0, 0,
'DAAAAAAA', 40,
'DBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', 1, .7,
'CCAAKAABAAAAAAAA', .7, 7, 391,
'CCAAKAABAAAAAAAA', .1,
'CCAAKA  ', 0, 0,
'DBAAAAAA', .00007,
'BAAA',  'DA', 391,
'DAAAAAAAAAAAAAAA', 1,
'BQAA ', 3540, 40, 94, 0, 14, 4,
'CCAAKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
1, .03,
'CCAAKAAB', 7, .07, .11, 3.91,
'BQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
3540, 0,
'DQAAAAAAAAAAAAAA',
'DBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
1194,
'CCAAKAAB', 3,
'BAAAAAAA', 7, .7, .7,
'CHAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert Into Twide1 
Values ('ATAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
'DEAACAAAAAAAAAAAAAAAAAAAAAAAAAAA', 16,
'AAAA ', 0,
'AE', 'AE',
'ATAAAAAAAAAAAAAA         ', 995,
'DEAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
1995, .0, .0,
'DEAACAAAAAAAAAAA', .4, .0, 0, 16, 16,
'AAAAAAAA', 16,
'AEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', 1, .5,
'DEAACAAEAAAAAAAA', 1.5, 95, 444,
'DEAACAAEAAAAAAAA                ', .0,
'DEAACA  ', 6, 16,
'AEAAAAAA', .00015,
'AAAAxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
'A ', 444,
'AAAAAAAAAAAAAAAA                ', 4,
'ATAA ', 3516, 16, 93, 1, 13, 3,
'DEAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
1, .03,
'DEAACAAE', 1995, .05, .04, 4.44,
'ATAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
3516, 16,
'ATAAAAAAAAAAAAAA                                                ',
'AEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
3493,
'DEAACAAE', 3,
'AAAAAAAA', 5, 9.5, 99.5,
'DEAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert Into Twide1 
Values ('AYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
'FGAADAAAAAAAAAAAAAAAAAAAAAAAAAAA', 87,
'AAAA ', 3,
'AA', 'AB',
'AYAAAAAAAAAAAAAA         ', 997,
'FEAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
1997, .0, .0,
'FGAADAAAAAAAAAAA', .4, .0, 3, 7, 7,
'AAAAAAAA', 87,
'AEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', 1, .7,
'FGAADAAEAAAAAAAA                ', 1.7, 97, 524,
'FGAADAAEAAAAAAAA                ', .0,
'FGAADA  ', 7, 7,
'AEAAAAAA                        ', .00017,
'AAAA                            ',
'A ', 524,
'AAAAAAAAAAAAAAAA                ', 4,
'AYAA ', 987, 487, 72, 0, 12, 2,
'FGAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
1, .01,
'FGAADAAE', 1997, .07, .04, 5.24,
'AYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
987, 7,
'AYAAAAAAAAAAAAAA                                                ',
'AEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
2772,
'FGAADAAE', 1,
'AAAAAAAA', 7, 9.7, 99.7,
'FEAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert Into Twide1 
Values ('AIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
'DDAABAAAAAAAAAAAAAAAAAAAAAAAAAAA', 9,
'AAAA ', 1,
'BA', 'AA',
'CIAAAAAAAAAAAAAA', 996,
'DGAAGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
1996, .0, .2,
'DDAABAAAAAAAAAAA', .8, .0, 1, 9, 9,
'CAAAAAAA', 9,
'CDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', 0, .6,
'DDAABAADAAAAAAAA', 1.6, 96, 158,
'DDAABAADAAAAAAAA                ', .0,
'DDAABA  ', 9, 9,
'CDAAAAAA                        ', .00016,
'AAAA                            ',
'CA', 158,
'CAAAAAAAAAAAAAAA                ', 8,
'AIAA ', 2809, 309, 39, 1, 19, 9,
'DDAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
0, .00,
'DDAABAAD', 1996, .06, .18, 1.58,
'AIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
2809, 9,
'CIAAAAAAAAAAAAAA                                                ',
'CDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
3239,
'DDAABAAD', 0,
'AAAAAAAA', 6, 9.6, 99.6,
'DGAAGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    # 5th row has all identical except for 3 fields of primary key:
    #    varchar11_2 , varchar2_10 , varchar15_uniq
    # and 3 unique indexes:
    #    char0_1000 , ubin3_uniq , char7_uniq
    #
    stmt = """Insert Into Twide1 
Values ('AIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
'Row 5, unique index char0_1000 ', 9,
'AAAA ', 1,
'BA',
-- Only 15 characters are allowed
--        '123456789012345'
'Row 5 vc10',
'CIAAAAAAAAAAAAAA', 996,
'DGAAGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
5, -- Unique index on ubin3_uniq
.0, .2,
'DDAABAAAAAAAAAAA', .8, .0, 1, 9, 9,
'CAAAAAAA', 9,
'CDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', 0, .6,
'Row 5, unique index char7_uniq', 1.6, 96, 158,
'DDAABAADAAAAAAAA                ', .0,
'DDAABA  ', 9, 9,
'CDAAAAAA                        ', .00016,
'Row 5, changed varchar11_2',
'CA', 158,
'CAAAAAAAAAAAAAAA                ', 8,
'AIAA ', 2809, 309, 39, 1, 19, 9,
'DDAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
0, .00,
-- Only 8 characters are allowed
--        '12345678'
'Row5 15u', 1996, .06, .18, 1.58,
'AIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
2809, 9,
'CIAAAAAAAAAAAAAA                                                ',
'CDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
3239,
'DDAABAAD', 0,
'AAAAAAAA', 6, 9.6, 99.6,
'DGAAGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    stmt = """Insert Into Twide1 ( -- 3 primary key columns.
varchar11_2 , varchar2_10 , varchar15_uniq
-- 3 unique indexes:
--    char0_1000       PIC X(32)
--    ubin3_uniq       Numeric(5,0) unsigned
--    char7_uniq       Char(100)
, char0_1000 , ubin3_uniq , char7_uniq
--    4 index columns.
--    varchar2_100     VarChar(25)
--    varchar5_4       VarChar(8)
--    ubin7_100        SMALLINT unsigned
--    sbin16_20        Numeric(9,2) signed
, varchar2_100 , varchar5_4
, ubin7_100    , sbin16_20
) values (
-- 3 primary key columns.
'Key part 1', 'Key part 2', 'Key p 3'
, 'Unique index 1', 62, 'Unique index 3'
, 'Index varchar2_100'
, 'Index VC'
, 61
, 62
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    stmt = """Insert Into Twide1 ( -- Same as previous except for
-- 3 columns of primary key.
varchar11_2 , varchar2_10 , varchar15_uniq
-- 3 unique indexes:
, char0_1000 , ubin3_uniq , char7_uniq
, varchar2_100 , varchar5_4
, ubin7_100    , sbin16_20
) values (
-- varchar2_10 -- Only 15 characters are allowed
--                        '123456789012345'
'Key part 1 Val 2', 'Key part 2 Val2', 'K p3 v3'
, 'Uneek i1', 72, 'Uneek i3'
, 'Index varchar2_100'
, 'Index VC'
, 61
, 62
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    #  Check the primary key.
    stmt = """Select varchar11_2, varchar2_10 , varchar15_uniq
From Twide1 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s0')
    #
    #  2nd column of primary key.
    stmt = """Select varchar2_10 From Twide1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s1')
    #
    #  3rd column of primary key.
    stmt = """Select varchar15_uniq From Twide1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s2')
    #
    #  Indexes set explicitly in all rows.
    stmt = """Select varchar2_100 , varchar5_4 , ubin7_100 , sbin16_20
From Twide1 
Order By 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s3')
    #
    #  Sampling of other Indexes.
    stmt = """Select varchar2_100 , varchar5_4 , ubin7_100 , sbin16_20
From Twide1 
Order By 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s4')
    #
    # ---------------------------
    #      Id: IX.101      Update 60-index table.
    # ---------------------------
    #
    # Remove autocommit and start a long-lived transaction:
    stmt = """Set Transaction Autocommit Off ;"""
    output = _dci.cmdexec(stmt)
    stmt = """Begin Work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  Look at these columns in combination.
    stmt = """Select varchar11_2 , varchar2_10 , varchar15_uniq
From Twide1 
Order By 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s5')
    stmt = """Select varchar2_100 , varchar5_4
, ubin7_100 , sbin16_20
From Twide1 
Order By 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s6')
    #
    # Update on basis of value in one Index column then select
    # individually:
    stmt = """Update Twide1 
set varchar2_100 = 'Update 1 row to new value'
where varchar2_100 = 'AYAAAAAAAAAAAAAA'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """Select varchar2_100 , varchar5_4
, ubin7_100 , sbin16_20
From Twide1 
Order By 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s7')
    #
    #  Update many index columns of 1 row then select individually
    #  from some. Exclude columns in primary key and in 3
    #  unique indexes (char0_1000 , ubin3_uniq , char7_uniq)
    stmt = """Select cast(varchar0_100 as varchar(30)) as varchar0_100
, varchar2_10 , ubin4_4
, cast( varchar17_20 as char(5) ) as v17 , sbin16_20
From Twide1 
Order By 1, varchar2_10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '8402')
    
    stmt = """Update Twide1 
set varchar0_100 = 'Update all rows to new value'
--      , char0_1000 = '1' -- Omit Unique Index    

, sbin1_100  = 2
, char1_4    = '3'
, ubin1_4    = 4    

--      , varchar2_10 = '5' -- Omit PK column
, varchar2_100 = '6'    

, sbin3_1000   = 7
, char3_1000   = '8'
--      , ubin3_uniq   = 9 -- Omit Unique Index    

, sbin4_2      = 0
, ubin4_4      = .1
, varchar4_1000 = '12'
, sdec4_10      = .3
, udec4_2       = .4    

, sbin5_4       = 15
, ubin5_20      = 16
, udec5_20      = 17
, varchar5_4    = '18'
, sdec5_100     = 19    

, varchar6_20   = '20'    

, sbin7_2       = 21
, sdec7_10      = 22
--      , char7_uniq    = '23' -- Omit Unique Index
, udec7_20      = 24
, ubin7_100     = 25    

, sbin8_1000    = 26
, varchar8_uniq = '27'
, ubin8_2       = 28    

, char9_uniq    = '29'
, udec9_10      = 30
, sdec9_20      =  31    

, varchar10_20  = '32'    

, sdec11_20     = .33
--      , varchar11_2   = '34' -- Omit PK column
, char11_4      = '35'    

, sbin12_1000   = 36
, varchar12_4   = '37'
, ubin12_10     = 38    

, char13_100    = '39'
, sdec13_uniq   = 40
, udec13_500    = 41    

, sbin14_100    = 42
, ubin14_2      = 43
, sdec14_20     = 44
, udec14_10     = 45
, varchar14_2000 = '46'    

, sbin15_2      = 47
, udec15_4      = 48
--      , varchar15_uniq = '49' -- Omit PK column
, ubin15_uniq   = 50
, sdec15_10     = 51    

, sbin16_20     = 52
, ubin16_1000   = 53
, varchar16_100 = '54'    

, sbin17_uniq   = 55
, sdec17_20     = 56
, char17_100    = '57'
, varchar17_20  = '58'    

, sbin18_uniq   = 59
, varchar18_uniq = '60'    

, sbin19_4      = 61
, char19_2      = '62'
, ubin19_10     = 63
, udec19_100    = 64
, sdec19_1000   = 65    

, varchar20_1000= '66'
where VARCHAR2_100 = 'CIAAAAAAAAAAAAAA'
or VARCHAR2_100 = 'DQAAAAAAAAAAAAAA'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    #
    #  Check some rows.
    stmt = """Select cast(varchar0_100 as varchar(30)) as varchar0_100
, varchar2_10 , ubin4_4
, cast( varchar17_20 as char(5) ) as v17 , sbin16_20
From Twide1 
Order By 1, varchar2_10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '8402')
    
    #
    stmt = """Update Twide1 -- as above -- 1st half.
set varchar0_100 = 'Update all rows to new value'
--      , char0_1000 = '1'    

, sbin1_100  = 2
, char1_4    = '3'
, ubin1_4    = 4    

--      , varchar2_10 = '5' -- Omit PK column
, varchar2_100 = '6'    

, sbin3_1000   = 7
, char3_1000   = '8'
--      , ubin3_uniq   = 9    

, sbin4_2      = .1
, ubin4_4      = .1
, varchar4_1000 = '12'
, sdec4_10      = .3
, udec4_2       = .4    

, sbin5_4       = 15
, ubin5_20      = 16
, udec5_20      = 17
, varchar5_4    = '18'
, sdec5_100     = 19    

, varchar6_20   = '20'    

, sbin7_2       = 21
, sdec7_10      = 22
--    , char7_uniq    = '23'
, udec7_20      = 24
, ubin7_100     = 25    

, sbin8_1000    = 26
, varchar8_uniq = '27'
, ubin8_2       = 28    

, char9_uniq    = '29'
, udec9_10      = 30
, sdec9_20      =  31    

, varchar10_20  = '32'    

;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 7)
    stmt = """Select cast(varchar0_100 as varchar(30)) as varchar0_100
, varchar2_10 , ubin4_4
, cast( varchar17_20 as char(5) ) as v17 , sbin16_20
From Twide1 
Order By 1, varchar2_10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '8402')
    
    #
    stmt = """Update Twide1 -- second half.
set sdec11_20     = .33
--      , varchar11_2   = '34' -- Omit PK column
, char11_4      = '35'    

, sbin12_1000   = 36
, varchar12_4   = '37'
, ubin12_10     = 38    

, char13_100    = '39'
, sdec13_uniq   = 40
, udec13_500    = 41    

, sbin14_100    = 42
, ubin14_2      = 43
, sdec14_20     = 44
, udec14_10     = 45
, varchar14_2000 = '46'    

, sbin15_2      = 47
, udec15_4      = 48
--      , varchar15_uniq = '49' -- Omit PK column
, ubin15_uniq   = 50
, sdec15_10     = 51    

, sbin16_20     = 52
, ubin16_1000   = 53
, varchar16_100 = '54'    

, sbin17_uniq   = 55
, sdec17_20     = 56
, char17_100    = '57'
, varchar17_20  = '58'    

, sbin18_uniq   = 59
, varchar18_uniq = '60'    

, sbin19_4      = 61
, char19_2      = '62'
, ubin19_10     = 63
, udec19_100    = 64
, sdec19_1000   = 65    

, varchar20_1000= '66'    

;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 7)
    stmt = """Select cast(varchar0_100 as varchar(30)) as varchar0_100
, varchar2_10 , ubin4_4
, cast( varchar17_20 as char(5) ) as v17 , sbin16_20
From Twide1 
Order By 1, varchar2_10
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s11')
    #
    #  Indexes set explicitly in all rows.
    stmt = """Select varchar2_100 , varchar5_4 , ubin7_100 , sbin16_20
From Twide1 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s12')
    #
    #  Look at these columns in combination.
    stmt = """Select varchar11_2 , varchar2_10 , varchar15_uniq
, varchar2_100
From Twide1 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s13')
    #
    stmt = """Select varchar15_uniq , varchar2_100 , varchar5_4
, ubin7_100 , sbin16_20
From Twide1 
order by varchar15_uniq , sbin16_20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s14')
    #
    # Update one index column, all rows then select:
    stmt = """Update Twide1 
set varchar2_100 = 'Update all rows'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 7)
    stmt = """Select varchar2_100 From Twide1 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s15')
    #
    # Rollback so all the Updates are undone.
    stmt = """Rollback Work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  Look at these columns in combination (useful also
    #  for Delete below).
    stmt = """Select varchar11_2 , varchar2_10 , varchar15_uniq
, varchar2_100
From Twide1 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s16')
    #
    stmt = """Select varchar15_uniq , varchar2_100 , varchar5_4
, ubin7_100 , sbin16_20
From Twide1 
order by varchar15_uniq , sbin16_20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s17')
    #
    # stmt = """Commit Work ;"""
    # output = _dci.cmdexec(stmt)
    # _dci.expect_complete_msg(output)
    #
    # ---------------------------
    #      Id: IX.111      Update 60-index table.
    # ---------------------------
    #
    # Start a long-lived transaction.
    stmt = """Begin Work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """Select varchar2_10 , varchar2_100 , VARCHAR15_UNIQ
From Twide1 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s18')
    #
    # Delete some rows on basis of value in two Indexes;
    # then select:
    stmt = """delete from Twide1 
where (varchar2_10, VARCHAR15_UNIQ  )
<> ('Row 5, changed', 'Row 5, c' )
and (varchar2_10, VARCHAR15_UNIQ  )
<> ('BB', 'CCAAKAAB' )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 6)
    stmt = """Select varchar2_10 , varchar2_100 , VARCHAR15_UNIQ
From Twide1 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s19')
    #
    # Delete all rows on basis of value in some Index;
    # then select:
    stmt = """delete from Twide1 
where varchar2_100 = 'Update all rows'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    stmt = """Select count(*) From Twide1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s20')
    #
    # Delete them all.
    stmt = """delete from Twide1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    stmt = """Select count(*) From ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #
    #  Expect 0.
    stmt = """Select count(*) From Twide1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s22')
    #
    # Rollback so all the Deletes are undone; then remove autocommit:
    stmt = """Rollback Work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Set Transaction Autocommit On ;"""
    output = _dci.cmdexec(stmt)
    #
    #  Expect 5.
    stmt = """Select count(*) From Twide1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s23')
    #
    # Delete them all.
    stmt = """delete from Twide1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 7)
    #
    stmt = """Commit Work ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8605')
    
    _testmgr.testcase_end(desc)

def test004(desc="""a05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    # Test case name:      T1110:A05
    # Description:         This test verifies Insert, Update, Delete
    #                      through VIEWS of data in indexed columns.
    #
    # =================== End Test Case Header  ===================
    #
    # Make sure that table starts empty.
    
    stmt = """Delete from VUwide1;"""
    output = _dci.cmdexec(stmt)
    #
    # ---------------------------
    #      Id: IX.092      Insert into 60-index view.
    # ---------------------------
    #
    # Insert rows.
    #
    # The following column sequence gives more than one
    # identical value in the first column of the primary key.
    #   , primary  key ( varchar11_2 DESC ASC
    #       , varchar2_10     ASC
    #       , varchar15_uniq  ASC
    #
    # Insert into Wide table with an index on each column.
    stmt = """Insert Into VUwide1 
Values ('BQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
'CCAAKAAAAAAAAAAAAAAAAAAAAAAAAAAA', 40,
'BAAA ', 0,
'AB', 'BB',
'DQAAAAAAAAAAAAAA         ', 7,
'CHAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
7, .1, .3,
'CCAAKAAAAAAAAAAA', .1, .1, 0, 0, 0,
'DAAAAAAA', 40,
'DBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', 1, .7,
'CCAAKAABAAAAAAAA', .7, 7, 391,
'CCAAKAABAAAAAAAA', .1,
'CCAAKA  ', 0, 0,
'DBAAAAAA', .00007,
'BAAA',  'DA', 391,
'DAAAAAAAAAAAAAAA', 1,
'BQAA ', 3540, 40, 94, 0, 14, 4,
'CCAAKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
1, .03,
'CCAAKAAB', 7, .07, .11, 3.91,
'BQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
3540, 0,
'DQAAAAAAAAAAAAAA',
'DBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
1194,
'CCAAKAAB', 3,
'BAAAAAAA', 7, .7, .7,
'CHAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert Into VUwide1 
Values ('ATAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
'DEAACAAAAAAAAAAAAAAAAAAAAAAAAAAA', 16,
'AAAA ', 0,
'AE', 'AE',
'ATAAAAAAAAAAAAAA         ', 995,
'DEAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
1995, .0, .0,
'DEAACAAAAAAAAAAA', .4, .0, 0, 16, 16,
'AAAAAAAA', 16,
'AEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', 1, .5,
'DEAACAAEAAAAAAAA', 1.5, 95, 444,
'DEAACAAEAAAAAAAA                ', .0,
'DEAACA  ', 6, 16,
'AEAAAAAA', .00015,
'AAAAxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
'A ', 444,
'AAAAAAAAAAAAAAAA                ', 4,
'ATAA ', 3516, 16, 93, 1, 13, 3,
'DEAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
1, .03,
'DEAACAAE', 1995, .05, .04, 4.44,
'ATAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
3516, 16,
'ATAAAAAAAAAAAAAA                                                ',
'AEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
3493,
'DEAACAAE', 3,
'AAAAAAAA', 5, 9.5, 99.5,
'DEAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert Into VUwide1 
Values ('AYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
'FGAADAAAAAAAAAAAAAAAAAAAAAAAAAAA', 87,
'AAAA ', 3,
'AA', 'AB',
'AYAAAAAAAAAAAAAA         ', 997,
'FEAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
1997, .0, .0,
'FGAADAAAAAAAAAAA', .4, .0, 3, 7, 7,
'AAAAAAAA', 87,
'AEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', 1, .7,
'FGAADAAEAAAAAAAA                ', 1.7, 97, 524,
'FGAADAAEAAAAAAAA                ', .0,
'FGAADA  ', 7, 7,
'AEAAAAAA                        ', .00017,
'AAAA                            ',
'A ', 524,
'AAAAAAAAAAAAAAAA                ', 4,
'AYAA ', 987, 487, 72, 0, 12, 2,
'FGAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
1, .01,
'FGAADAAE', 1997, .07, .04, 5.24,
'AYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
987, 7,
'AYAAAAAAAAAAAAAA                                                ',
'AEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
2772,
'FGAADAAE', 1,
'AAAAAAAA', 7, 9.7, 99.7,
'FEAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert Into VUwide1 
Values ('AIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
'DDAABAAAAAAAAAAAAAAAAAAAAAAAAAAA', 9,
'AAAA ', 1,
'BA', 'AA',
'CIAAAAAAAAAAAAAA         ', 996,
'DGAAGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
1996, .0, .2,
'DDAABAAAAAAAAAAA', .8, .0, 1, 9, 9,
'CAAAAAAA', 9,
'CDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', 0, .6,
'DDAABAADAAAAAAAA', 1.6, 96, 158,
'DDAABAADAAAAAAAA                ', .0,
'DDAABA  ', 9, 9,
'CDAAAAAA                        ', .00016,
'AAAA                            ',
'CA', 158,
'CAAAAAAAAAAAAAAA                ', 8,
'AIAA ', 2809, 309, 39, 1, 19, 9,
'DDAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
0, .00,
'DDAABAAD', 1996, .06, .18, 1.58,
'AIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
2809, 9,
'CIAAAAAAAAAAAAAA                                                ',
'CDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
3239,
'DDAABAAD', 0,
'AAAAAAAA', 6, 9.6, 99.6,
'DGAAGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    # Insert into subset of rows
    stmt = """Insert Into VUwide1 ( -- 3 primary key columns.
-- 3 primary  key columns
varchar11_2 , varchar2_10 , varchar15_uniq
-- 4 index columns.
, varchar2_100 , varchar5_4
, ubin7_100    , sbin16_20
) values (
'Key1 Val 1', 'Key2 Val 1', '6'
, 'Index varchar2_100'
, 'Index VC'
, 61
, 62
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    #  1st column of primary key
    stmt = """Select varchar11_2 From VUwide1 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    #
    #  2nd column of primary key
    stmt = """Select varchar2_10 From VUwide1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
    #
    #  3rd column of primary key
    stmt = """Select varchar15_uniq From VUwide1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    #
    #  Indexes set explicitly in all rows.
    stmt = """Select varchar2_100 , varchar5_4 , ubin7_100 , sbin16_20
From VUwide1 
Order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
    #
    #  Sampling of other Indexes.
    stmt = """Select varchar11_2 , varchar15_uniq
From VUwide1 
Order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s4')
    #
    #  Look at these columns in combination (useful also
    #  for Update below).
    stmt = """Select varchar11_2 , varchar2_10 , varchar15_uniq
, varchar2_100 , varchar5_4
, ubin7_100 , sbin16_20
From VUwide1 
Order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s5')
    #
    # ---------------------------
    #      Id: IX.101B     Update 60-index table via View.
    # ---------------------------
    #
    # Remove autocommit and start a long-lived transaction:
    stmt = """Set Transaction Autocommit Off ;"""
    output = _dci.cmdexec(stmt)
    stmt = """Begin Work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """Select varchar2_10 , varchar2_100 , ubin7_100 , sbin16_20
From VUwide1 
Order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s6')
    #
    # Update on basis of value in one Index column then select
    # individually:
    stmt = """Update VUwide1 
set varchar2_100 = 'Update 1 row to new value'
where varchar2_100 Like 'AY%'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """Select varchar2_10 , varchar2_100 , ubin7_100 , sbin16_20
From VUwide1 
Order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s7')
    
    #
    # Update several index columns of 1 row then select individually
    # from some:
    stmt = """Update VUwide1 
set -- Omit column of PK varchar2_10
varchar2_100 = 'Update 2_100 col to new value'
, sbin5_4       = 54
, ubin7_100     = 7
-- Omit column of PK varchar11_2
-- Omit column of PK varchar15_uniq
, sbin16_20     = 1620
, ubin16_1000   = 16000    

where varchar2_100 LIKE '%AT%A'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 0)
    #
    stmt = """Select varchar2_10 , varchar2_100 , ubin7_100 , sbin16_20
From VUwide1 
Order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s8')
    #
    # Update one index column, all rows then select:
    stmt = """Update VUwide1 
--        varchar2_100 -- Only 25 characters are allowed
--                       '1234567890123456789012345'
set varchar2_100 = 'Update all rows to new va'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    #
    #  Indexes set explicitly in all rows.
    stmt = """Select varchar2_10 , varchar2_100 , ubin7_100 , sbin16_20
, ubin16_1000
From VUwide1 
Order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s9')
    stmt = """Select varchar11_2 , varchar15_uniq
, varchar2_100 , varchar5_4
From VUwide1 
Order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s10')
    #
    # Rollback so all the Updates are undone.
    stmt = """Rollback Work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  Check a subset of columns, that we are returned to original values, in
    #  indexes set explicitly in all rows.
    stmt = """Select varchar2_10 , varchar2_100 , ubin7_100 , sbin16_20
, ubin16_1000
From VUwide1 
Order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s11')
    stmt = """Select varchar11_2 , varchar15_uniq
, varchar2_100 , varchar5_4
From VUwide1 
Order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s12')
    #
    # stmt = """Commit Work ;"""
    # output = _dci.cmdexec(stmt)
    # _dci.expect_complete_msg(output)
    #
    # ---------------------------
    #      Id: IX.111B     Delete from 60-index table via view.
    # ---------------------------
    #
    # Start a long-lived transaction.
    stmt = """Begin Work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  Check initial values.
    stmt = """Select varchar2_10 , varchar2_100 , varchar5_4
From VUwide1 
Order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s13')
    # delete on basis of value in some Index then select:
    stmt = """delete from VUwide1 
where varchar2_10 like 'AE%'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """Select varchar2_10, varchar2_100 , varchar5_4
From VUwide1 
Order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s14')
    #
    # delete on basis of value in two Indexes then select:
    stmt = """delete from VUwide1 
where ( varchar2_100, varchar5_4 )
= ( 'DQAAAAAAAAAAAAAA', 'DAAAAAAA' )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    stmt = """Select varchar2_10, varchar2_100 , varchar5_4
From VUwide1 
Order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s15')
    #
    # Delete them all.
    stmt = """delete from VUwide1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)
    
    #
    #  Expect 0.
    stmt = """Select count(*) From VUwide1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s16')
    #
    # Rollback so all the Deletes are undone; then remove autocommit:
    stmt = """Rollback Work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Set Transaction Autocommit On ;"""
    output = _dci.cmdexec(stmt)
    #
    #  Expect 5.
    stmt = """Select count(*) From VUwide1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s17')
    #
    # Delete them all.
    stmt = """delete from VUwide1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 5)
    
    _testmgr.testcase_end(desc)

def test005(desc="""n01"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    # Test case name:      T1110:N01
    # Description:         This test verifies Error handling for attempt to
    #                      corrupt Uniquely indexed columns.
    #
    # =================== End Test Case Header  ===================
    #
    # Make every statement automatically committed.
    stmt = """set transaction autocommit on;"""
    output = _dci.cmdexec(stmt)
    #
    # Create the table with 3 unique index cols.
    
    stmt = """Create Table t10 
(
varchar0_100     VarChar(250) not null,
char0_1000       PIC X(32),
ubin3_uniq       Numeric(5,0) unsigned not null,
char7_uniq       Char(100) not null
) no partition
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create  unique index I10W1 on t10 ( varchar0_100 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create  unique index I10W2 on t10 ( ubin3_uniq );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create  unique index I10W3 on t10 ( char7_uniq );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Insert Into t10 
Values ('BQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
'CCAAKAAAAAAAAAAAAAAAAAAAAAAAAAAA',
7,
'CCAAKAABAAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """Insert Into t10 
Values ('ATAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
'DEAACAAAAAAAAAAAAAAAAAAAAAAAAAAA',
1995,
'DEAACAAEAAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """Insert Into t10 
Values ('AYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
'FGAADAAAAAAAAAAAAAAAAAAAAAAAAAAA',
1997,
'FGAADAAEAAAAAAAA                '
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """Insert Into t10 
Values ('AIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
'DDAABAAAAAAAAAAAAAAAAAAAAAAAAAAA',
1996,
'DDAABAADAAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    #  This should give a clean error -- full duplicate of row inserted above.
    stmt = """Insert Into t10 
Values ('AIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
'DDAABAAAAAAAAAAAAAAAAAAAAAAAAAAA',
1996,
'DDAABAADAAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    #  This should give a clean error -- duplicate of varchar0_100 in row
    #  inserted above.
    stmt = """Insert Into t10 
Values ('AIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
'unique 1',
2001,
'unique 1'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    #
    #  This should give a clean error -- duplicate of ubin3_uniq in row
    #  inserted above.
    stmt = """Insert Into t10 
Values ('unique 2',
'unique 2',
1996,
'unique 2'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    #
    #  This should give a clean error -- duplicate of char7_uniq in row
    #  inserted above.
    stmt = """Insert Into t10 
Values ('unique 3',
'unique 3',
2002,
'DDAABAADAAAAAAAA'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    #
    stmt = """Select cast(varchar0_100 as char(40)),
char0_1000     ,
ubin3_uniq     ,
cast(char7_uniq as varchar(16))
From t10 
Order by ubin3_uniq
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s4')
    #
    #  Attempt to update and set the columns to the same value; should also
    #  get clean error for all attempts but char0_100.
    stmt = """Update t10 
set varchar0_100 = 'Update all rows to new value'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    # Expect OK.
    stmt = """Update t10 
set char0_1000 = 'Update all rows to new value'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 4)
    #  Expect error.
    stmt = """Update t10 
set ubin3_uniq = 42
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    #  Expect error.
    stmt = """Update t10 
set char7_uniq = 'Update all rows to new value'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    #
    stmt = """Select cast(varchar0_100 as char(40)),
char0_1000     ,
ubin3_uniq     ,
cast(char7_uniq as varchar(16))
From t10 
Order by ubin3_uniq
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s8')
    #
    # Cleanup.
    stmt = """Drop table t10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test006(desc="""n02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    # Test case name:      T1110:N02
    # Description:         This test verifies error handling on attempt to
    #                      insert NULL value into primary key.
    #
    # =================== End Test Case Header  ===================
    #
    # Make every statement automatically committed.
    stmt = """set transaction autocommit on;"""
    output = _dci.cmdexec(stmt)
    #
    # Create:
    #
    # Primary key of dis-contiguous columns.
    
    stmt = """create table TN02 (
vca         varchar(9) not null
, vcb         varchar(18)
, nintc       int        not null
, primary key ( nintc )
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index I1TN02 
on TN02(vca);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index I2TN02 
on TN02(vcb);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Inserts.
    #
    stmt = """insert into TN02 values ( '01 No dup' , 'Duplicate allowed'
, 1
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    #  Should get error on attempt to insert duplicate primary key.
    #  (Correctly get error 8102 The operation is prevented by a unique constraint.)
    stmt = """insert into TN02 values ( '01 No dup' , 'Duplicate allowed'
, 1
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    #
    #  Should get clean error on attempt to insert NULL primary key.
    stmt = """insert into TN02 values ( '03 No dup' , 'Duplicate allowed'
, NULL
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4122')
    
    # Create constraints.
    stmt = """alter table TN02 add constraint n2c1 unique (vca);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Get error (unique constraint already exists because of primary key) if
    #  attempt to add uniqueness constraint here on nintc)
    #
    #  Test the constraint.
    stmt = """insert into TN02 values ( '01 No dup' , 'Duplicate allowed'
, 2
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    stmt = """insert into TN02 values ( '04 No dup' , 'Duplicate allowed'
, 1
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    
    #  Check contents.
    stmt = """select * from TN02 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n02exp""", 'n02s4')
    
    # Cleanup by removing constraints.
    
    stmt = """drop index I1TN02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop index I2TN02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Drop table TN02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test007(desc="""n03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    # Test case name:      T1110:N03
    # Description:         This test looks to make sure that Contraints
    #                      with Indexes get cleaned up ok.
    #
    # =================== End Test Case Header  ===================
    #
    
    stmt = """drop table TN03;"""
    output = _dci.cmdexec(stmt)
    
    # Make every statement automatically committed.
    stmt = """set transaction autocommit on;"""
    output = _dci.cmdexec(stmt)
    
    # Create:
    # Table and indexes.
    
    stmt = """create table TN03 (
vca         varchar(9) not null
, vcb         varchar(18)
, nintc       int        not null
, primary key ( nintc )
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index I1TN03 
on TN03(vca);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index I2TN03 
on TN03(vcb);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Inserts.
    #
    stmt = """insert into TN03 values ( '01 No dup' , 'Duplicate allowed'
, 1
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    #  Should get error on attempt to insert duplicate primary key.
    #  (Correctly get error 8102 The operation is prevented by a unique
    #  constraint.)
    stmt = """insert into TN03 values ( '01 No dup' , 'Duplicate allowed'
, 1
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    #
    #  Should get clean error on attempt to insert NULL primary key.
    stmt = """insert into TN03 values ( '03 No dup' , 'Duplicate allowed'
, NULL
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4122')
    #
    # Create constraints.
    
    stmt = """alter table TN03 add constraint n3c1 unique (vca);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Create constraint gives error for duplicate key.
    stmt = """alter table TN03 add constraint n3c2 unique (nintc);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1254')
    
    #  Test the constraint. This should give constraint error for
    #  duplicate value attempted in 2 cases.
    
    stmt = """insert into TN03 values ( '01 No dup' , 'Duplicate allowed'
, 2
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    stmt = """insert into TN03 values ( '04 No dup' , 'Duplicate allowed'
, 1
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    
    #  Check contents.
    stmt = """select * from TN03 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n03exp""", 'n03s5')
    
    # Attempt to drop the table without dropping constraints or indexes.
    # Should work.
    stmt = """Drop table TN03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # ---------------------------------------
    # (1) Repeat 1: Attempt to repeat all of the above.
    # ---------------------------------------
    stmt = """create table TN03 (
vca         varchar(9) not null
, vcb         varchar(18)
, nintc       int        not null
, primary key ( nintc )
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index I1TN03 on TN03(vca);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index I2TN03 on TN03(vcb);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Inserts.
    
    stmt = """insert into TN03 values ( '01 No dup' , 'Duplicate allowed'
, 1
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  Should get error on attempt to insert duplicate primary key.
    #  (Correctly get error 8102 The operation is prevented by a unique
    #  constraint.)
    
    stmt = """insert into TN03 values ( '01 No dup' , 'Duplicate allowed'
, 1
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    
    #  Should get clean error on attempt to insert NULL primary key.
    stmt = """insert into TN03 values ( '03 No dup' , 'Duplicate allowed'
, NULL
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4122')
    
    # Create constraints.
    stmt = """alter table TN03 add constraint n3c1 unique (vca);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Create constraint gives error for duplicate key.
    stmt = """alter table TN03 add constraint n3c2 unique (nintc);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1254')
    
    #
    #  Test the constraint. This should give constraint error for
    #  duplicate value attempted in 2 cases.
    stmt = """insert into TN03 values ( '01 No dup' , 'Duplicate allowed'
, 2
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    stmt = """insert into TN03 values ( '04 No dup' , 'Duplicate allowed'
, 1
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    #
    #  Check contents.
    stmt = """select * from TN03 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n03exp""", 'n03s11')
    #
    # Attempt to drop the table without dropping constraints.
    stmt = """Drop table TN03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # ---------------------------------------
    # (2) Repeat 2: Attempt to repeat Create-to-drop.
    # ---------------------------------------
    stmt = """create table TN03 (
vca         varchar(9) not null
, vcb         varchar(18)
, nintc       int        not null
, primary key ( nintc )
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index I1TN03 on TN03(vca);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index I2TN03 on TN03(vcb);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Inserts.
    
    stmt = """insert into TN03 values ( '01 No dup' , 'Duplicate allowed'
, 1
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  Should get error on attempt to insert duplicate primary key.
    #  (Correctly get error 8102 The operation is prevented by a unique
    #  constraint.)
    
    stmt = """insert into TN03 values ( '01 No dup' , 'Duplicate allowed'
, 1
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    #
    #  Should get clean error on attempt to insert NULL primary key.
    stmt = """insert into TN03 values ( '03 No dup' , 'Duplicate allowed'
, NULL
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4122')
    
    # Create constraints.
    stmt = """alter table TN03 add constraint n3c1 unique (vca);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Create constraint gives error for duplicate key.
    stmt = """alter table TN03 add constraint n3c2 unique (nintc);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1254')
    
    #  Test the constraint. This should give constraint error for
    #  duplicate value attempted in 2 cases.
    stmt = """insert into TN03 values ( '01 No dup' , 'Duplicate allowed'
, 2
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    stmt = """insert into TN03 values ( '04 No dup' , 'Duplicate allowed'
, 1
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    
    #  Check contents.
    stmt = """select * from TN03 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n03exp""", 'n03s17')
    #
    # Attempt to drop the table without dropping constraints.
    stmt = """Drop table TN03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  ---------------------------------------
    #  (3) Cleanup by removing constraints and explicit indexes.
    #      These SHOULD have been removed by Drop Table (above).
    #  ---------------------------------------
    #  Should get errors as Drop Table (above) should have removed
    #  constraints.
    stmt = """alter table TN03 drop constraint n3c1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    stmt = """alter table TN03 drop constraint n3c2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Should get errors as Drop Table (above) should have removed
    #  indexes.
    stmt = """drop index I1TN03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    stmt = """drop index I2TN03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    #
    # ---------------------------------------
    # (4) Re-create table, insert, create constraints, then again
    #     cleanup.
    # ---------------------------------------
    stmt = """create table TN03 (
vca         varchar(9) not null
, vcb         varchar(18)
, nintc       int        not null
, primary key ( nintc )
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index I1TN03 on TN03(vca);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index I2TN03 on TN03(vcb);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Inserts.
    
    stmt = """insert into TN03 values ( '01 No dup' , 'Duplicate allowed'
, 1
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    #  Should get error on attempt to insert duplicate primary key.
    #  (Correctly get error 8102 The operation is prevented by a unique
    #  constraint.)
    stmt = """insert into TN03 values ( '01 No dup' , 'Duplicate allowed'
, 1
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    #
    #  Should get clean error on attempt to insert NULL primary key.
    stmt = """insert into TN03 values ( '03 No dup' , 'Duplicate allowed'
, NULL
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4122')
    
    # Create constraints.
    stmt = """alter table TN03 add constraint n3c1 unique (vca);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  Create constraint gives error for duplicate key.
    stmt = """alter table TN03 add constraint n3c2 unique (nintc);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1254')
    
    #  Test the constraint. This should give constraint error for
    #  duplicate value attempted in 2 cases.
    stmt = """insert into TN03 values ( '01 No dup' , 'Duplicate allowed'
, 2
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    stmt = """insert into TN03 values ( '04 No dup' , 'Duplicate allowed'
, 1
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    
    #  Check contents.
    stmt = """select * from TN03 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n03exp""", 'n03s27')
    
    stmt = """Drop table TN03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #                End of test case ARKT1110
    _testmgr.testcase_end(desc)

