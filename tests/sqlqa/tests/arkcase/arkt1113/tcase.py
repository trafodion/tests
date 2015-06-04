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
    # ---------------------------------------
    # Includes SQL features (from list of May 19, 1997):
    #	G001 ANSI names.
    #	G002 ANSI views. And see also A15 for updateable views.
    #	G022 VARCHAR data type.
    #	G023 UNION in view definition.
    #	G024 Case-insensitive identifiers.
    #	G050 Underscore in identifiers.
    #
    #
    #  ---------------------------------------
    #  Table BTloc8 has only 6 columns; VNloc8 is a "union view"
    #  on that table. Variable catsch represents local catalog.schema.
    #  ---------------------------------------
    #
    #  ---------------------------------------
    #  Initially check contents of table and view..
    #  ---------------------------------------
    #  Expect 6 rows.
    
    stmt = """select * from BTloc8 order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    #
    #  Expect 5 rows.
    stmt = """select *
from VNloc8 
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    #
    #  ---------------------------------------
    #  Simple selects on table, including VARCHAR column, column names are
    #  case-insensitive.
    #  ---------------------------------------
    #  Expect 4 rows {(1,'ACAABAAA') (1,'BBA%FAAA')
    #  (1,'BBAABA_A') (1,'BBAADAAA')}
    stmt = """select sbin0_4, VARchar0_500
from BTloc8 where varChar0_500 < 'BDA'
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    #
    #  Expect 4 rows {(1, 3917,'BBAA') (3,1993,'BDAA')
    #  (3, 3293,'BD') (7, 2701,'BCAA')}
    stmt = """select ubin16_n10, sdec16_uniq, char16_n20
from BTloc8 where varCHAR0_500 < 'BDA'
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    #
    #  Expect 2 rows {('AAAAAAAA') ('BAAAAAAA')}
    stmt = """select char17_2
from BTloc8 where vARcHAR0_500 >= 'BDA'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    #
    #  ---------------------------------------
    #  Simple select on Union View.
    #  ---------------------------------------
    #  Expect 5 rows {(0,'BDAAAAAA') (1,'ACAABAAA') (1,'BBA%FAAA')
    # 		  (1,'BBAABA_A') (3,'CAAAGAAA')}
    stmt = """select v_1.sbin0_4, v_1.VARchar0_500
from VNloc8 v_1
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    #
    #  ---------------------------------------
    #  Right join on UNION view.
    #  ---------------------------------------
    #  Expect 5 rows {(0,0,'BDAAAAAA','BDAAAAAA') (1,1,'ACAABAAA','ACAABAAA')
    #                 (1,1,'BBA%FAAA','BBA%FAAA') (3,3,'CAAAGAAA','CAAAGAAA')
    # 		  (NULL,1,NULL,'BBAABA_A')}
    stmt = """select a.sbin0_4 as a04, b.sbin0_4 as b04
, A.VARchar0_500 as a500, B.VARchar0_500 as b500
from VNloc8 a
right join VNloc8 B
on (A.vARchar0_500 = B.char16_n20) or
(a.char17_2     = b.VaRchar0_500) or
(A.VArchar0_500 = b.VARchar0_500)
and
(a.varchar0_500 <> 'BBAADAAA')
and
('BBAABA_A' <> A.VARCHAR0_500)
order by 1,2,3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')
    
    _testmgr.testcase_end(desc)

def test002(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Includes SQL features (from list of May 19, 1997):
    #	G025 SUBSTRING, TRIM, CHAR_LENGTH, concatenation.
    #	G068 UPSHIFT.
    # Also include parameters.
    #
    # ---------------------------
    # Ensure (even if SQLCI default changes to AUTOCOMMIT OFF) that
    # each SQL statement is committed immediately.
    # ---------------------------
    
    stmt = """SET TRANSACTION AUTOCOMMIT ON;"""
    output = _dci.cmdexec(stmt)
    
    # ---------------------------------------
    # Table BTloc7 has only 7 columns; VNloc7 is a view that
    # uses the 'G' features noted above.
    # Variable catsch represents local catalog.schema.
    # ---------------------------------------
    #
    # ---------------------------------------
    stmt = """set param ?p_param ' bcDEFg8i ';"""
    output = _dci.cmdexec(stmt)
    #  ---------------------------------------
    #
    #  ---------------------------------------
    #  Initially check contents of table, view.
    #  ---------------------------------------
    #  Expect 6 rows:
    stmt = """select *
from BTloc7 
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    #
    #  Expect 6 rows, with length column (16, 7, 8, 7, 16, 16)
    stmt = """select CUPPER, CLOWER
, CCHAR_LENGTH as FivePlusVarChar
from VNloc7 
order by 1,2,3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    #  Expect 6 rows:
    #  { (7  0  AA)  (7  0  BA)  (8  0  ABC)  (16  1   LEADING B.)
    #     (16  9  EBAAEAAC)  (16  9  TRAILING B) }
    stmt = """select COCTET_LENGTH, CPOSITION, CSUBSTRING
from VNloc7 
order by 1,2,3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    #  Expect 6 rows demonstrating TRIM and CONCATENATION:
    stmt = """select CTRIM, CCONCATCHAR, CCONCATVARCHAR
from VNloc7 
order by 1,2,3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    #
    #  ---------------------------------------
    #  Simple select of substring on column of basetable,
    #  and of view column that uses that feature.
    #  ---------------------------------------
    #  Table: Expect 6 rows:
    #  { ('A') ('A') ('BAAEAAC') ('BC') ('LEADING B.') ('RAILING B ') }
    stmt = """select substring (varchar0_nuniq from 2)
from BTloc7 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s4')
    #
    #  Table: Expect 4 rows:
    #  { (' LEADING B. bcDEFg8i' 'EFg8i  LEADING B.' 'bcDEFg8i')
    #    ('ABC bcDEFg8i'         'EFg8i ABC'         '')
    #    ('EBAAEAAC    bcDEFg8i' 'EFg8i EBAAEAAC'    'bcDEFg8i')
    #    ('TRAILING B  bcDEFg8i' 'EFg8i TRAILING B'  'bcDEFg8i') }
    stmt = """select substring ((varchar0_nuniq || ?p_param ) from 1) as From1
, substring ((?p_param || varchar0_nuniq ) from 5) as From5
, substring ((varchar0_nuniq || ?p_param ) from 13) as From13
from BTloc7 
where substring (varchar0_nuniq from 2) > 'B'
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')
    #
    #  View: Expect 4 rows:
    #  { (' LEADING B.' 'EADING B.')  ('ABC' 'C')
    #    ('EBAAEAAC' 'AAEAAC') ('TRAILING B' 'AILING B') }
    stmt = """select cSubstring
, substring(cSubstring from 3) as substringFrom3
from VNloc7 
where substring (csubstring from 2) > 'B'
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s6')
    #
    #  ---------------------------------------
    #  Simple select of trim on column of basetable,
    #  and of view column that uses that feature.
    #  ---------------------------------------
    #  Table: Expect 6 rows:
    #  { ('startAAend'         'startAAend')
    #    ('startABCend'        'startABCend')
    #    ('startBAend'         'startBAend')
    #    ('startEBAAEAACend'   'startEBAAEAAC   end')
    #    ('startLEADING B.end' 'start LEADING B.end')
    #    ('startTRAILING Bend' 'startTRAILING B end') }
    stmt = """select 'start' || trim(varchar0_nuniq) || 'end' as trimmed
, 'start' ||      varchar0_nuniq  || 'end' as untrimmed
from BTloc7 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s7')
    #
    #  View: Expect 6 rows:
    #  { ('trim leading spaces  LEADING B.')
    #    ('trim leading spaces AA')
    #    ('trim leading spaces ABC')
    #    ('trim leading spaces BA')
    #    ('trim leading spaces EBAAEAAC   ')
    #    ('trim leading spaces TRAILING B ') }
    stmt = """select cTrim
from VNloc7 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s8')
    #
    #  ---------------------------------------
    #  Simple selects on view columns that use Char_length and concatentation.
    #  ---------------------------------------
    #  Expect 6 rows from base table, for which next query gets
    #  char_length (see view definition)
    #  Expect:
    #   { ('AABF TRAILING B ') ('ABAE BA') ('BABB AA')
    #     ('BACC EBAAEAAC') ('BADD  LEADING B.') ('BEAA ABC') }
    stmt = """select char2_2 || char9_100 || varchar0_nuniq
from BTloc7 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s9')
    #
    #  Expect 6 rows: { (7) (7) (8) (16) (16) (16) }
    stmt = """select char_length(char2_2 || char9_100 || varchar0_nuniq)
from BTloc7 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s10')
    #
    #  ---------------------------------------
    #  Simple selects on view columns that use upper, lower, upshift.
    #  ---------------------------------------
    #  Expect 6 rows:
    #  { (' LEADING B. LEADING B.' ' leading b. leading b.')
    #    ('AAAA'                   'aaaa')
    #    ('ABCABC'                 'abcabc')
    #    ('BABA'                   'baba')
    #    ('EBAAEAAC   EBAAEAAC   ' 'ebaaeaac   ebaaeaac   ')
    #    ('TRAILING B TRAILING B ' 'trailing b trailing b ')
    stmt = """select cUpper, cLower
from VNloc7 
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s11')
    
    _testmgr.testcase_end(desc)

def test003(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Includes SQL features (from list of May 19, 1997):
    #	G026 NATURAL JOIN.
    #	See A04-A06 for Inner, Left Outer, Right Outer Joins.
    #
    #
    # ---------------------------
    # Ensure (even if SQLCI default changes to AUTOCOMMIT OFF) that
    # each SQL statement is committed immediately.
    # ---------------------------
    
    stmt = """SET TRANSACTION AUTOCOMMIT ON;"""
    output = _dci.cmdexec(stmt)
    #
    #  ---------------------------------------
    #  Natural joins of a variety of tables and views.
    #  ---------------------------------------
    #
    #  ---------------------------------------
    #  Initially check contents of table, view.
    #  ---------------------------------------
    #  Expect 5 rows:
    stmt = """select * from BTloc1 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s0')
    #
    #  Expect 7 rows:
    stmt = """select * from BTloc2 
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    #
    #  Expect 4 rows:
    stmt = """select * from BTloc3 
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    #
    #  Expect 12 rows:
    stmt = """select * from VNloc4 
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s3')
    #
    #  Expect 7 rows:
    stmt = """select * from VNloc5 
order by N1, C3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s4')
    #
    #  Expect 4 rows:
    stmt = """select * from VNloc6 
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s5')
    #
    #  Expect 6 rows:
    stmt = """select * from VNloc7 
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s6')
    #
    #  Expect 5 rows:
    stmt = """select * from VNloc8 
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s7')
    #
    #  Expect 6 rows:
    stmt = """select * from VNloc9 
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s8')
    #
    #  ---------------------------------------
    #  Simple natural join of substring on column of basetable,
    #  and of view column that uses that feature.
    #  ---------------------------------------
    #  Should show rows as in 1-column base table.
    stmt = """select v
from BTloc1 
natural join BTloc1 t
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s9')
    #
    #  Should show rows as in base table.
    stmt = """select varchar7, char8
from BTloc2 
natural join BTloc2 t
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s10')
    #
    #  Should show rows as in base table.
    stmt = """select varchar15, ubin15 from BTloc3 
natural join BTloc3 t
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s11')
    #
    #  Column names are same in view and table so should be
    #  able to make natural join.
    #  Should show rows as in view.
    stmt = """select varchar0_4, VARCHAR5_10
, VARCHAR13_100, SDEC13_UNIQ, CHAR14_20
from BTloc4 
natural join VNloc4 t
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s12')
    #
    #  Should show rows as in view.
    stmt = """select N1, C2, C3, C4
from VNloc5 
natural join VNloc5 t
order by N1, C3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s13')
    #
    #  Should show number of rows as in view.
    stmt = """select count(*) from VNloc6 
natural join VNloc6 t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s14')
    #
    #  Should show number of rows as in view.
    stmt = """select count(*) from VNloc7 
natural join VNloc7 t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s15')
    #
    #  Should show number of rows as in view, i.e. 6.
    stmt = """select count(*) from VNloc9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s16')
    stmt = """select count(*) from VNloc9 
natural join VNloc9 t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s17')
    
    _testmgr.testcase_end(desc)

def test004(desc="""a04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Includes SQL features (from list of May 19, 1997):
    #	G026 JOIN: INNER.
    #	G028 Implicit casting between different numeric types.
    #
    #
    # ---------------------------------------
    # Start user transaction.
    # ---------------------------------------
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  ---------------------------------------
    #  Initially check contents of table, view.
    #  ---------------------------------------
    #  Expect 13 rows:
    #  udec15_4         Decimal(9,2) unsigned   not null,
    stmt = """select udec15_4, -udec15_4*100, ubin15_uniq
from BTloc4 
order by 1, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s0')
    #
    #  Expect 4 rows.
    #  sbin0_4             Integer      not null,
    #  sdec5_10            Numeric(9,0) signed   not null,
    #  sdec6_4             Numeric(4,0) signed   not null,
    stmt = """select sbin0_4, sdec5_10, sdec6_4
from BTloc6 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s1')
    #
    #  ---------------------------------------
    #  Simple inner joins between columns of different data types.
    #  ---------------------------------------
    #  Scaffolding (to faciliate result checking; expect 16 rows).
    stmt = """select t4.udec15_4, t6.sbin0_4, t6.sdec5_10
from BTloc4 t4
, BTloc6 t6
where t4.ubin15_uniq in (4559,3889,1188,4412)
order by 1,2,3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s2')
    #
    #  Expect 1 row {(0.00 0)}
    stmt = """select t4.udec15_4, t6.sbin0_4
from BTloc4 t4
inner join BTloc6 t6
on t4.udec15_4=t6.sbin0_4
where t4.ubin15_uniq in (4559,3889,1188,4412)
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s3')
    #
    #  Expect 3 rows {(0.00 -1) (0.03  0) (.03 0)}
    stmt = """select t4.udec15_4, t6.sbin0_4
from BTloc4 t4
inner join BTloc6 t6
on -t4.udec15_4*100=t6.sdec5_10
where t4.ubin15_uniq in (4559,3889,1188,4412)
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s4')
    #
    #  Expect 5 rows {(-2 -2) (-2 -2) (-2 -2) (-2 -2) (-1 -1)}
    stmt = """select t.sbin0_4,u.sdec6_4
from BTloc6 t
inner join BTloc6 u
on t.sbin0_4=u.sdec6_4
where t.sbin0_4<>0
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s5')
    #
    #  Expect 6 rows {(-2 -2) (-2 -2) (-2 -2) (-2 -2) (-1 -1) (0 0)}
    stmt = """select t.sdec6_4,u.sdec6_4
from BTloc6 t
inner join BTloc6 u
on t.sdec6_4=u.sdec6_4
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s6')
    #
    # ---------------------------------------
    # Explicitly stop any outstanding transaction.
    # ---------------------------------------
    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test005(desc="""a05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Includes SQL features (from list of May 19, 1997):
    #	G026 JOIN: LEFT OUTER.
    #	G028 Implicit casting between different numeric types.
    #
    # ---------------------------------------
    # Set up local SCHEMA.
    # ---------------------------------------
    #
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  ---------------------------------------
    #  Initially check contents of table, view.
    #  ---------------------------------------
    #  Expect 13 rows.
    stmt = """select udec15_4, ubin15_uniq
from BTloc4 
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    #
    #  Expect 4 rows.
    stmt = """select sbin0_4, sdec5_10, sdec6_4
from BTloc6 
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
    #
    #  ---------------------------------------
    #  Simple left outer joins between columns of different data types.
    #  ---------------------------------------
    #
    #  Using, from BTloc4:
    #  udec15_4         Decimal(9,2) unsigned   not null,
    #  ubin15_uniq      INTEGER unsigned        not null,
    #
    #  Using, from BTloc6:
    #  sbin0_4          Integer      not null,
    #  sdec5_10         Numeric(9,0) signed   not null,
    #  sdec6_4          Numeric(4,0) signed   not null,
    #
    #  Expect 6 rows {(0 4412 0) (0 5000 0) (.01 3889 null)
    #                 (.03 1188 null) (.03 4559 null ) (.06 6000 null)}
    stmt = """select t4.udec15_4, t4.ubin15_uniq, t6.sbin0_4
from BTloc4 t4
left outer join BTloc6 t6
on t4.udec15_4=t6.sbin0_4 -- NOTE: only match on '0' values.
where t4.ubin15_uniq in (4559,3889,1188,4412,5000,6000)
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    #
    #  Expect 6 rows {(0, 4412, -1, 0) (0, 5000, -1, 0) (.01, 3889, null, null)
    #                 (.03, 1188, 0, -3) (.03, 4559, 0, -3 ) (.06, 6000, -2, -6)}
    stmt = """select t4.udec15_4, t4.ubin15_uniq, t6.sbin0_4, t6.sdec5_10
from BTloc4 t4
left outer join BTloc6 t6
on -t4.udec15_4*100=t6.sdec5_10
where t4.ubin15_uniq in (4559,3889,1188,4412,5000,6000)
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
    #
    #  Expect 5 rows {(-2 -2) (-2 -2) (-2 -2) (-2 -2) (-1 -1)}
    stmt = """select t.sbin0_4,u.sdec6_4
from BTloc6 t
left outer join BTloc6 u
on t.sbin0_4=u.sdec6_4
where t.sbin0_4<>0
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s4')
    #
    #  Expect 5 rows {(-6 null) (-3 null) (-2 -2) (-2 -2) (0 0)}
    stmt = """select t.SDEC5_10,u.sdec6_4
from BTloc6 t
left outer join BTloc6 u
on t.SDEC5_10=u.sdec6_4
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s5')
    #
    # ---------------------------------------
    # Explicitly stop any outstanding transaction.
    # ---------------------------------------
    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test006(desc="""a06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Includes SQL features (from list of May 19, 1997):
    #	G026 JOIN: RIGHT outer.
    #	G029 Implicit casting between different character types.
    #
    #
    # ---------------------------------------
    # Start user transaction.
    # ---------------------------------------
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  ---------------------------------------
    #  Initially check contents of view.
    #  This Right-join View VNloc2 joins string data of
    #  different lengths, char versus varchar.
    #  ---------------------------------------
    #  Expect 5 rows from grouped view.
    stmt = """select c1, c2
from VNloc2 
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s0')
    #
    #  ---------------------------------------
    #  Additional selects.
    #  ---------------------------------------
    #  Expect 4 rows {('CAAAAAA' 'EE' 'X' null)}
    stmt = """select c1
from VNloc2 
group by c1
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s1')
    #
    #  Expect 5 rows {('CAAAAAA' 'CAAAAAA') ('EE' 'EE')
    #                 ('X' 'X') (null 'CAAAAAAX') (null null)}
    stmt = """select V1.c1, v2.c2
from VNloc2 V1 
right join (select c2
from VNloc2 
group by c2
) v2
on V1.c1=v2.c2
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s2')
    #
    # ---------------------------------------
    # Explicitly stop any outstanding transaction.
    # ---------------------------------------
    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test007(desc="""a07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Includes SQL features (from list of May 19, 1997):
    #	G003 COMMIT and ROLLBACK.
    # ---------------------------
    #
    #
    # Default for SQLCI on 09/19/1997 is AUTOCOMMIT ON.
    # So we have to set AUTOCOMMIT OFF to check longevity
    # of system-initiated transaction.

    #
    # ---------------------------
    # (1) Create table, insert, commit work (for the automatically
    #     started ANSI transaction; check that can then begin a
    #     user transaction and can see inserted rows.
    # ---------------------------
    
    stmt = """create table T1(
varchar13 varchar(13)
, varchar7  varchar(7)
, somenumber int
) no partition
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """SET TRANSACTION AUTOCOMMIT OFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert Into T1 Values('on', 'off', 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert Into T1 Values('non', 'compos', 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    stmt = """select * from T1 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s0')
    #--------------------------------------
    # During de-bugging TEMPORARILY checked transaction is on
    # using ENV; omit now as it is unneeded, and thereby avoid
    # bogus mismatch for changes to display lines, transaction
    # number, etc.
    #--------------------------------------
    # COMMIT should succeed, if an ANSI transaction has been
    # started on the user's behalf.
    stmt = """COMMIT WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  Expect to see the 2 inserted rows.
    stmt = """select * from T1 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s1')
    #
    # ---------------------------
    # (2) Commit the user transaction; insert (thereby causing an
    #     ANSI transaction to start; rollback work; check that can
    #     now begin a transaction user's and do not see the
    #     inserted rows that were just rolled back.
    # ---------------------------
    stmt = """COMMIT WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # User transaction and ROLLBACK.
    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert Into T1 Values('omega', 'plus', 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    # Should succeed.
    stmt = """ROLLBACK WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # System transaction and ROLLBACK.
    stmt = """insert Into T1 Values('doughnut', 'day', 9998);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert Into T1 Values('volley', 'ball', 9999);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    stmt = """select * from T1 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s2')
    # Should succeed.
    stmt = """ROLLBACK WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  Expect to see the 2 inserted rows but not the 3 from the rolled-back
    #  transaction.
    stmt = """select * from T1 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s3')
    
    # Initially needed to be sure to stop any outstanding transaction.
    
    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    stmt = """SET TRANSACTION AUTOCOMMIT ON;"""
    output = _dci.cmdexec(stmt)
 
    stmt = """drop table T1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test008(desc="""a08"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Includes SQL features (from list of May 19, 1997):
    #	G030 Transaction access modes, isolation levels, SET TRANSACTION.
    #           Access mode determines nature of actions that can occur
    #           within a transaction.
    #           Isolation level determines level of data consistency that can
    #           occur within a transaction.
    # ---------------------------
    #
    #
    # Default for SQLCI on 09/19/1997 is AUTOCOMMIT ON.
    # So we have to set AUTOCOMMIT OFF to check longevity
    # of system-initiated transaction.

    stmt = """create table T1(
varchar1 varchar(21)
, varchar2 varchar(23)
, somenumber int
) no partition
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """SET TRANSACTION AUTOCOMMIT OFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert Into T1 Values('on', 'off', 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # Make sure that we end any active transaction so can
    # set isolation level.
    
    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # ---------------------------
    # SET TRANSACTION READ ONLY;
    # Can read but not write.
    # ---------------------------
    stmt = """SET TRANSACTION READ ONLY;"""
    output = _dci.cmdexec(stmt)
    
    #  read ok.
    stmt = """select * from T1 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s0')
    #  write fails.
    stmt = """insert Into T1 Values('non', 'compos', 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3141')
    #  modify (also writes) fails.
    stmt = """update T1 
set varchar1 = 'fully' where somenumber < 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3141')
    #
    # Make sure that we end any active transaction so can
    # set isolation level.
    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    # _dci.expect_complete_msg(output)
    #
    # ---------------------------
    # There is no "SET TRANSACTION WRITE ONLY" option.
    # ---------------------------
    #
    # ---------------------------
    # SET TRANSACTION READ WRITE;
    # Can read and write.
    # ---------------------------
    stmt = """SET TRANSACTION READ WRITE;"""
    output = _dci.cmdexec(stmt)
    # write ok.
    stmt = """insert Into T1 Values('omega', 'plus', 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert Into T1 Values('doughnut', 'day', 9998);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  read ok.
    stmt = """select * from T1 order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s3')
    #
    # End any active transaction.
    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # ---------------------------
    stmt = """insert Into T1 Values('volley', 'ball', 9999);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from T1 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s4')
    #
    # Make sure that we end any active transaction so can
    # set isolation level.
    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # ---------------------------
    # For setting isolation level see concurrency tests;
    # also see also arkt1106:A01.
    # ---------------------------
    stmt = """SET TRANSACTION AUTOCOMMIT OFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """set transaction isolation level read uncommitted ;"""
    output = _dci.cmdexec(stmt)
    #  Can read but not write (For READ UNCOMMITTED you can specify
    #  only READ ONLY by using SET TRANSACTION).
    stmt = """insert Into T1 Values('this', 'fails', 11);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3140')
    stmt = """select * from T1 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s6')
    # No transaction for READ UNCOMMMITED; do not specify Commit work;
    # that would just cause an error. Just proceed to the next Set Transaction.
    #
    # 9/19/97 Avoid using the multiple arguments because it gives a syntax error;
    stmt = """SET TRANSACTION AUTOCOMMIT OFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """set transaction isolation level read committed ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert Into T1 Values('read', 'committed', 12);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from T1 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s7')
    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """set transaction isolation level repeatable read ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert Into T1 Values('repeatable', 'read', 13);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from T1 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s8')
    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """set transaction isolation level serializable ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert Into T1 Values('serializable', NULL, 14);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from T1 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s9')
    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # ---------------------------
    # Clean up.
    # ---------------------------
   
    stmt = """SET TRANSACTION AUTOCOMMIT ON;"""
    output = _dci.cmdexec(stmt)
 
    stmt = """drop table T1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test009(desc="""a09"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Includes SQL features (from list of May 19, 1997):
    #	G032 Row and table value constructor (RVC and TVC).
    #	     See also PREUNIT which uses TVC (VALUES <RVC>).
    #	     Test Id's indicate test plan topics not touched upon in
    #	     earlier testware.
    #	G053 Relaxed intermediate-level restrictions on DISTINCT
    #           (allow multiple distincts).
    # There are more tests of this Feature in t1100:A14.
    #
    stmt = """SET transaction autocommit on;"""
    output = _dci.cmdexec(stmt)
    
    #  ---------------------------
    #  Table value constructor (TVC).
    #  ---------------------------
    #       Id: TV.031       Table Value Constructor contains 1 column.
    #       Id: TV.043       Table Value Constructor value is aggregate expression.
    #  ---------------------------
    
    #  Expect 6 rows.
    stmt = """select VARCHAR0_NUNIQ, CHAR2_2, CHAR3_4, SDEC9_UNIQ
from BTloc7 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s0')
    stmt = """select VARCHAR0_NUNIQ, CHAR9_100
from BTloc7 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s1')
    #
    #  Expect {(6)}.
    stmt = """select * from (select count(*) from BTloc7) x
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s2')
    #
    #  Expect {('TRAILING B')}.
    stmt = """select * from (select max(varchar0_nuniq) from BTloc7) x
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s3')
    #
    #  Expect {(15)}.
    stmt = """select * from (select sum(SDEC9_UNIQ) from BTloc7) x
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s4')
    #
    #  ---------------------------
    #       Id: TV.032       Table Value Constructor contains Five ('a few') columns.
    #       Id: TV.042       Table Value Constructor values are expressions using operators.
    #  ---------------------------
    #
    #  Expect {(1, 26, 3, 4, 18)}.
    stmt = """select * from (
values (1,2*13,3,4,5+13)
) x
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s5')
    #
    #  Expect {(1,26,3,4,18), (2,52,53,74,85), (11,12,0,14,15)}
    #  First column gains decimal point because of the division.
    stmt = """select * from (
values (1,2*13,3,4,5+13), (11,12,13-13,14,15),
(26/13,52,53,74,85)
) x
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s6')
    #
    #  Expect 2 rows:  {('ConCatEnate' 'z' 6) ('con-cat-enate' 'A' 314)}.
    stmt = """select * from ( Values
('con-'|| 'cat-' || 'enate', upper('a'), cast(('3'|| '14') as int) ),
('Con'|| 'Cat' || 'Enate', lower('Z'), 6)
) anyOldName47
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s7')
    #
    #  Also multiple distincts.
    #  Expect {(1,26,3,4,18,26,3,7)}
    stmt = """select distinct * from (
select distinct * from (
values (1,2*13,3,4,5+13,26,3,7)
, (1,26,3,4,18,26,3,7)
, (1,2*13,3,4,5+13,26,3,7)
, (1,2*13,3,4,118-100,26,3,42/6)
) x
) y
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s8')
    #
    #  ---------------------------
    #       Id: TV.033       Table Value Constructor contains 30 ('many') columns.
    #       Id: TV.041       Table Value Constructor values are numeric and string literals.
    #  ---------------------------
    #  Expect 1 row, 30 columns.
    stmt = """select * from (
values (1,2,3,4,5,1,2,3,4,5,1,2,3,4,5,1,2,3,4,5
,'a','b','c','d','e','f','g','h','i','j'
)
) x(a1,b1,c1,d1,e1,f1,g1,h1,i1,j1,
a2,b2,c2,d2,e2,f2,g2,h2,i2,j2,
a ,b ,c ,d ,e ,f ,g ,h ,i ,j
)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s9')
    #
    # ---------------------------
    #   Moved to arkt1113:b09 on 970923:
    #     VALUES clause (i.e., TVC) can include multiple RVCs.
    #     Within TVC, RVC can include a subquery that returns a single value.
    # ---------------------------
    
    stmt = """drop table T1A09;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table T1A09(
varchar13 varchar(13) not null
, varchar7  varchar(7)  not null
, somenumber int        not null
, primary key ( varchar13, varchar7)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # ---------------------------
    #      Id: TV.061       Table Value Constructor values use string functions.
    # ---------------------------
    stmt = """insert Into T1A09 Values(
('con-'|| 'cat-' || 'enate'), upper('a'), cast(('3'|| '14') as int)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert Into T1A09 Values(
'Con'|| 'Cat' || 'Enate', lower('Z'), 6
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    #  Expect 2 rows:  {('ConCatEnate' 'z' 6) ('con-cat-enate' 'A' 314)}.
    stmt = """select * from T1A09 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s10')
    stmt = """delete from T1A09;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    
    _testmgr.testcase_end(desc)

def test010(desc="""a10"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Includes SQL features (from list of May 19, 1997):
    #	G043 Scalar subqueries. One form of numeric primary is a
    #           scalar subquery, like (query) that returns one value.
    #           Supported at Intermediate Level, which means that:
    #           (a) If a subquery contains a comparison predicate, then
    #               the <table expression> in the <query specification>
    #               - may contain a <group by>,
    #               - may contain a <having>,
    #               - may identify a grouped view.
    #           (b) The <query expression> contained in a <subquery> is no
    #               longer limited to being a <query specification>
    #               i.e. SELECT ...
    #
    #
    # ---------------------------------------
    # Start user transaction.
    # ---------------------------------------
   
    stmt = """create table T1A10(vc varchar(13) not null) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
 
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    #
    #  ---------------------------------------
    #  Initially check contents of table, view.
    #  ---------------------------------------
    #  Expect 5 rows:
    stmt = """select * from VNloc2 
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s0')
    #
    #  ---------------------------
    #  Scalar subquery: (query) that returns one value in select.
    #  ---------------------------
    #  Expect {(5 'X' 'CAAAAAA')}
    stmt = """select count(*), max(c1), min(c2)
from VNloc2 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s1')
    #
    #  Expect 5 rows of 5.
    stmt = """select (select count(*) from VNloc2)
from VNloc2 T1 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s2')
    #
    #  Expect {('XCAAAAAA')}
    stmt = """select distinct
(select max(c1) from VNloc2)
|| (select min(c2) from VNloc2)
from VNloc2 T1 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s3')
    #
    #  ---------------------------
    #  Scalar subquery in insert: See t1113:A09 for that.
    #  ---------------------------
    #
    #  ---------------------------
    #            (a1) If a subquery contains a comparison predicate, then
    #                the <table expression> in the <query specification>
    #                may contain a <group by>.
    #  ---------------------------
    #
    #  Expect {('EE')}
    stmt = """select c2 from VNloc2 
where c2 > 'DZ' and c2 < 'JZ'
group by c2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s4')
    #
    #  Expect {('X' 'X')}
    stmt = """select * from VNloc2 v where v.c1 > 'EE'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s5')
    #  Expect {('X' 'X')} --- Bug in SUN (April 29 1997 version)
    stmt = """select * from VNloc2 v where v.c1 >
(select c2 from VNloc2 
where c2 > 'DZ' and c2 < 'JZ'
group by c2
)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s6')
    #
    #  As above but without Group By or Distinct (scaffolding to check
    #  if bug also appears in simpler case).
    stmt = """select * from VNloc2 v where v.c1 >
(select c2 from VNloc2 
where c2 > 'DZ' and c2 < 'JZ'
)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s7')
    stmt = """select * from VNloc2 v where v.c1 >
(select max('EE') from VNloc2)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s8')
    #  Expect {('X' 'X')}
    stmt = """select * from VNloc2 v where v.c1 >
(select distinct c2 from VNloc2 
where c2 > 'DZ' and c2 < 'JZ'
)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s9')
    #
    #  ---------------------------
    #            (a2) If a subquery contains a comparison predicate, then
    #                the <table expression> in the <query specification>
    #                may contain a <having>,
    #  ---------------------------
    #
    #  Expect {('X' 'X')} --- Bug in SUN (April 29 1997 version)
    stmt = """select * from VNloc2 v where v.c1 >
(select c2 from VNloc2 
where c2 > 'DZ' and c2 < 'JZ'
group by c2
having c2 < 'X'
)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s10')
    #
    #  ---------------------------
    #            (a3) If a subquery contains a comparison predicate, then
    #                the <table expression> in the <query specification>
    #                - may identify a grouped view.
    #                VNloc2 is a grouped view.
    #  ---------------------------
    #
    #  Expect {('X')}
    stmt = """select max(c2) from VNloc2 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s11')
    #  Expect {('CAAAAAA') ('EE')} -- Again watch for bug here.
    stmt = """select * from VNloc2 v where v.c1 <
(select max(c2) from VNloc2)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s12')
    #
    #  ---------------------------
    #            (b1) The <query expression> contained in a <subquery> is no
    #                longer limited to being a <query specification>
    #                but can include UNION.
    #  ---------------------------
    #
    #  Expect {('X') ( '  ')}
    stmt = """select max(c2), max(c1) from VNloc2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s13')
    #
    #  Expect {('X     ')}
    stmt = """select max(c1) from VNloc2 
UNION
select max(c2) from VNloc2 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s14')
    #
    #  Expect .
    stmt = """select * from VNloc2 
where c2 in (
select max(c1) from VNloc2 
UNION
select max(c2) from VNloc2 
) order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s15')
    stmt = """select * from VNloc2 
where c2 NOT in (
select max(c1) from VNloc2 
UNION
select max(c2) from VNloc2 
) order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s16')
    #
    #  ---------------------------
    #            (b2) The <query expression> contained in a <subquery> is no
    #                longer limited to being a <query specification>
    #                i.e. SELECT ... but can be explicit TABLE ...
    #  ---------------------------
    #
    stmt = """select * from (TABLE VNloc2)v order by 1,2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s17')
    #
    #
    stmt = """select * from VNloc2 v where v.c1 >
(TABLE T1A10 )
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #
    stmt = """insert into T1A10 Values('JZ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from (TABLE T1A10)t order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s18')
    #
    stmt = """select * from VNloc2 v where v.c1 <
(TABLE T1A10 )
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s19')
    #
    stmt = """select * from VNloc2 v where v.c1 <
'JZ'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s20')
    #
    stmt = """select * from VNloc2 v where v.c1 >
(TABLE T1A10 )
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s21')
    #
    stmt = """update T1A10 set vc = 'DZ' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from (TABLE T1A10)t order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s22')
    stmt = """select * from VNloc2 v where v.c1 >
(TABLE T1A10)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s23')
    
    # ---------------------------------------
    # Explicitly stop any outstanding transaction.
    # ---------------------------------------
    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table T1A10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test011(desc="""a11"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Includes SQL features (from list of May 19, 1997):
    #	G044 Relaxed entry-level restriction on Table expressions.
    #	G051 Derived tables in FROM clause.
    #
    # ---------------------------------------
    # Set up local SCHEMA.
    # ---------------------------------------
    #
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    #
    #  ---------------------------
    #  Derived table (select in a FROM clause) may include WHERE.
    #  ---------------------------
    #  Scaffolding.
    stmt = """select v from VUlocal1 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s0')
    #  Expect { (CCAA) (CCCCAAAA) (CCCCA) }
    stmt = """select v from VUlocal1 WHERE v > 'CC' order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s1')
    #
    #  Expect { (CCAA) (CCCCAAAA) (CCCCA) }
    stmt = """select * from (
select v from VUlocal1 
WHERE v > 'CC'
) dt
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s2')
    #  Expect { (CCAA) }
    stmt = """select * from (
select v from VUlocal1 
WHERE v > 'CC'
) dt
where v < 'CCCCA'
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s3')
    #
    #  ---------------------------
    #  Derived table (select in a FROM clause) may include HAVING.
    #  Some tests moved from here to arkt1113:B11 because sql dies
    #  in Group by/having/derived table query.
    #  ---------------------------
    #  Expect (9).
    stmt = """select count(VARCHAR13_100)
from BTloc4 
group by VARCHAR13_100
HAVING VARCHAR13_100='AM'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s4')
    #
    #  Expect (9).
    stmt = """select * from (
select count(VARCHAR13_100)
from BTloc4 
group by VARCHAR13_100
HAVING VARCHAR13_100='AM'
) dt
ORDER BY 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s5')
    #
    #  ---------------------------
    #  Derived table (select in a FROM clause) may include GROUP BY.
    #  ---------------------------
    #  Scaffolding to show Base Table.
    stmt = """select VARCHAR13_100, SDEC13_UNIQ, CHAR14_20, VARCHAR15_UNIQ
from BTloc4 
order by 1,2,3,4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s6')
    #
    #  Expect 7 rows:
    #  { (AG 4217) (AJAA 3112) (AM 3030) (AM 3031)
    #    (AM 3050) (AN 3030)   (ARAA 1413) }
    stmt = """select * from (
select VARCHAR13_100, SDEC13_UNIQ
from BTloc4 
GROUP BY VARCHAR13_100, SDEC13_UNIQ
) dt
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s7')
    #
    #  Expect all 13 rows as in base table.
    stmt = """select * from (
select VARCHAR13_100, SDEC13_UNIQ, CHAR14_20, VARCHAR15_UNIQ
from BTloc4 
GROUP BY VARCHAR13_100, SDEC13_UNIQ, CHAR14_20, VARCHAR15_UNIQ
) dt
order by 1,2,3,4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s8')
    #
    # ---------------------------------------
    # Explicitly stop any outstanding transaction.
    # ---------------------------------------
    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test012(desc="""a12"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Includes SQL features (from list of May 19, 1997):
    #	G045 Relaxed entry-level restriction on UNION.
    #           The entry-level restrictions to relax for UNION are:
    #
    #           'If UNION is specified, then except for column names, the
    #            descriptors of the first and second operands shall be identical
    #            and the descriptor of the result is identical to the descriptor
    #            of the operands.'
    #           ANSI standard SQL92 section 7.10.
    #
    #
    # ---------------------------------------
    # Start user transaction.
    # ---------------------------------------
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  ---------------------------
    #  UNION of char and varchar.
    #  ---------------------------
    stmt = """select VARCHAR13_100, CHAR14_20, sdec13_uniq
from BTloc4 
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s0')
    #
    stmt = """select CHAR14_20, VARCHAR15_UNIQ, udec15_4
from BTloc4 
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s1')
    #
    stmt = """select max(VARCHAR13_100), max(CHAR14_20), max(sdec13_uniq)
from BTloc4 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s2')
    #
    #  Expect simple self-union of 9 rows.
    stmt = """select VARCHAR13_100, CHAR14_20, sdec13_uniq
from BTloc4 
union
select VARCHAR13_100, CHAR14_20, sdec13_uniq
from BTloc4 
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s3')
    #
    #  Expect simple self-union of 13 rows.
    stmt = """select CHAR14_20, VARCHAR15_UNIQ, udec15_4
from BTloc4 
union
select CHAR14_20, VARCHAR15_UNIQ, udec15_4
from BTloc4 
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s4')
    #
    #  Expect combination of data shown above, giving 22 unique rows.
    stmt = """select VARCHAR13_100, CHAR14_20, sdec13_uniq
from BTloc4 
union
select CHAR14_20, VARCHAR15_UNIQ, udec15_4
from BTloc4 
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s5')
    #
    #  Expect combination of data shown above, giving 14 unique rows.
    stmt = """select CHAR14_20, VARCHAR15_UNIQ, udec15_4
from BTloc4 
union
select max(VARCHAR13_100), max(CHAR14_20), max(sdec13_uniq)
from BTloc4 
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s6')
    #
    # ---------------------------------------
    # Explicitly stop any outstanding transaction.
    # ---------------------------------------
    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test013(desc="""a13"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Includes SQL features (from list of May 19, 1997):
    #	G046 Relaxed entry-level restriction on Row-value constructor.
    #           'The value for a <default specification> is the default
    #           value indicated in the column descriptor for the corresponding
    #           column of the explicit or implicit <insert column list> simply
    #           contained in the insert statement.'
    #           ANSI standard SQL92 section 7.1.
    #
    #
    # Turn off autocommit so transaction lasts until Commit Work.

    #
    # ---------------------------
    # Table with 'default' DEFAULT values.
    # ---------------------------
    
    stmt = """create table T1A13(
varchar23 varchar(23)
, varchar9  varchar(9)
, somenumber int
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """SET TRANSACTION AUTOCOMMIT OFF;"""
    output = _dci.cmdexec(stmt)

    #
    # Can we insert "DEFAULT VALUES" as in Reference Manual,
    # where page I-12 (August 1997) shows this is equivalent
    # to VALUES(DEFAULT, ...).
    stmt = """insert into T1A13 DEFAULT Values;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select * from T1A13 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s0')
    #
    stmt = """insert into T1A13 (varchar23, varchar9)
Values('some','data');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into T1A13 (somenumber)
Values(42);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into T1A13 (varchar9, somenumber)
Values('datums',13);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into T1A13 DEFAULT Values;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    #  Expect 5 rows each with 1 to 3 default values.
    stmt = """select * from T1A13 order by 1, 2, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s1')
    
    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """SET TRANSACTION AUTOCOMMIT ON;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table T1A13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # ---------------------------
    # Table with user-specified DEFAULT values.
    # ---------------------------
    
    stmt = """create table T1A13(
varchar23 varchar(23) default '23 characters'
, varchar9  varchar(9)  default '9 chars'
, somenumber int        default 9999
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    stmt = """SET TRANSACTION AUTOCOMMIT OFF;"""
    output = _dci.cmdexec(stmt)
 
    stmt = """insert into T1A13 DEFAULT Values;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  Check results so far.
    stmt = """select * from T1A13 order by 1, 2, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s2')
    #
    stmt = """insert into T1A13 (varchar23, varchar9)
Values('some','data');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into T1A13 (somenumber)
Values(42);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into T1A13 (varchar9, somenumber)
Values('some data',13);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into T1A13 DEFAULT Values;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    #  Expect 5 rows each with 1 to 3 default values.
    #
    stmt = """select * from T1A13 order by 1, 2, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s3')
    stmt = """delete from T1A13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 5)
    #
    # Similar insert with NULL (and without explicit DEFAULT) values.
    stmt = """insert into T1A13 Values('just','a',6),('reality','check',7);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    stmt = """insert into T1A13 Values('eight',NULL,8),('nine',NULL,9);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    stmt = """insert into T1A13 Values('ten',NULL,10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into T1A13 Values('eleven','11',NULL),('twelve','12',NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    stmt = """insert into T1A13 Values('thirteen','13',NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    stmt = """select * from T1A13 order by 1, 2, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s4')
    
    # ---------------------------------------
    # Explicitly stop any outstanding transaction.
    # ---------------------------------------
    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    stmt = """SET TRANSACTION AUTOCOMMIT ON;"""
    output = _dci.cmdexec(stmt)
 
    stmt = """drop table T1A13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test014(desc="""a14"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Includes SQL features (from list of May 19, 1997):
    #	G047 Relaxed entry-level restriction on LIKE and NULL predicates.
    #
    #           <like predicate> ::= <match value> [NOT] LIKE <pattern>
    #                                        [ESCAPE <escape character>]
    #                 where <match value>, <pattern>, and <escape character>
    #                 are <character value expressions>.
    #           The entry-level restrictions to relax for LIKE are:
    #           '(a) The match value shall be a column reference.
    #            (b) A <pattern> shall be a <value specification>.
    #            (c) An <escape character> shall be a <value specification>.'
    #           ANSI standard SQL92 section 8.5 for LIKE.
    #
    #           Relax NULL restrictions:
    #           'A <row value constructor> that "IS [NOT] NULL" shall be
    #            a <column reference>.'
    #           ANSI standard SQL92 section 8.6 for NULL.
    #
    # ---------------------------
    # Ensure (even if SQLCI default changes to AUTOCOMMIT OFF) that
    # each SQL statement is committed immediately.
    # ---------------------------
    
    stmt = """SET TRANSACTION AUTOCOMMIT ON;"""
    output = _dci.cmdexec(stmt)
    #
    #  ---------------------------
    #  LIKE predicate. Allow match value to be non-column reference.
    #  ---------------------------
    stmt = """select sbin0_4, varchar0_500 from VNloc8 
order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s0')
    #
    #  Expect all 5 rows as this condition is true.
    stmt = """select sbin0_4, varchar0_500 from VNloc8 
where 'a' like 'a' order by 1, 2  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s1')
    #
    #  Expect all 5 rows as this condition is true.
    stmt = """select sbin0_4, varchar0_500 from VNloc8 
where 'a' like 'a%' order by 1, 2  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s2')
    #
    #  A function, not a simple column reference.
    #  Expect 3 matching rows.
    stmt = """select sbin0_4, varchar0_500 from VNloc8 
where lower(varchar0_500) like 'b%' order by 1, 2  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s3')
    #
    #  Aggregate -- expect "CAAAGAAA".
    stmt = """select max(varchar0_500) from VNloc8 
where lower(varchar0_500) like 'c%' order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s4')
    stmt = """select varchar0_500 from VNloc8 
where
(select max(lower(varchar0_500)) from VNloc8)
like 'c%' order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s5')
    #
    #  ---------------------------
    #  LIKE predicate. Allow a <pattern> to be a non-<value specification>.
    #  Syntax errors on SUN; question sent to Matt; fixed 970921.
    #  ---------------------------
    #  Expect all 5 rows with additional lower-case value.
    stmt = """select varchar0_500, lower(VARCHAR0_500)||'%'
from VNloc8 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s6')
    #
    #  Expect all 5 rows.
    stmt = """select varchar0_500
from VNloc8 
where varchar0_500 like varchar0_500
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s7')
    #
    #  Expect all 5 rows.
    stmt = """select sbin0_4, varchar0_500 from VNloc8 
where varchar0_500 like upper(lower(VARCHAR0_500))||'%'
order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s8')
    #
    #  ---------------------------
    #  LIKE predicate. Allow an <escape character> to be a
    #  non-<value specification>.
    #  ---------------------------
    #
    stmt = """select varchar0_500 from VNloc8 
where varchar0_500 like '%'
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s9')
    #
    #  Expect BBA%FAAA, the value that contains a '%'.
    #  The simple case.
    stmt = """select varchar0_500 from VNloc8 
where varchar0_500 like '%\%%' ESCAPE '\\'
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s10')
    #  String function in ESCAPE -- only 1 character long.
    stmt = """select varchar0_500 from VNloc8 
where varchar0_500 like '%x%%' ESCAPE lower('X')
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s11')
    
    stmt = """set param ?p 'Y';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select varchar0_500 from VNloc8 
where varchar0_500 like '%y%%' ESCAPE lower(?p)
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s12')
    
    #  ---------------------------
    #  Matt's examples:
    #  	select x from t where (select j from s where...)
    #           like (select p from patterntable where...)
    #           escape (select e from patterntable...)
    #  ---------------------------
    
    #  Check that we get 'X':
    
    stmt = """select max(varchar7) from BTloc2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s13')
    
    stmt = """select * from BTloc2 order by 1,2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s14')
    
    stmt = """select * from VNloc2 order by 1,2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s15')
    
    #  Subquery in pattern:
    
    stmt = """select * from VNloc2 
where C1 like '%'||(select max(varchar7) from BTloc2)
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s16')
    
    stmt = """select * from VNloc2 
where C2 like '%'||(select max(varchar7) from BTloc2)
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s17')
    
    #  >>   create table BTloc2(varchar7 varchar(7), char8 PIC X(8));
    #  >>   VNloc2 -> C1       C2
    #
    #   VNloc2
    #        where varchar0_500 like '%y%%' ESCAPE lower(?p);
    #
    #  Subquery in escape clause; string function (1 character long).
    
    stmt = """select varchar0_500 from VNloc8 
where varchar0_500 like '%x%%' ESCAPE lower('X')
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s18')
    
    _testmgr.testcase_end(desc)

def test015(desc="""a15"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Includes SQL features (from list of May 19, 1997):
    #	G002 ANSI views -- DML on updateable views
    #
    #
    # ---------------------------
    # Ensure (even if SQLCI default changes to AUTOCOMMIT OFF) that
    # each SQL statement is committed immediately.
    # ---------------------------
    stmt = """SET TRANSACTION AUTOCOMMIT ON;"""
    output = _dci.cmdexec(stmt)
    #
    # ------------------------------
    # Create single-column table and view; insert/update/delete via view.
    # ------------------------------
    
    stmt = """create table T1A15(
varchar8  varchar(8)  not null
, primary key (varchar8) -- DESC -- A970712: DESC is illegal (bug)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Insert into table then create updateable view.
    
    stmt = """insert Into T1A15 Values('CC');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create view V1 as select * from T1A15;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select varchar8 from T1A15;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s0')
    stmt = """select varchar8 from V1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s1')
    
    # Insert into tables and views.
    stmt = """insert Into V1 Values('AA');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert Into T1A15 Values('CACAAAAA');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert Into V1 Values('CCCCAAAA');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert Into V1 Values('Z');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    #  Check values in the primary key.
    #  Expect 5 rows in descending order.
    stmt = """select varchar8 from T1A15;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s2')
    stmt = """select varchar8 from V1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s3')
    #
    #  Update through view.
    #  +++>>> Bug b970717 -- restore the following when NJ bug is fixed.
    #  +++>>>    update V1 set varchar8='omit'
    #  +++>>>       where varchar8 like 'C%';
    #  +++>>>    update V1 set varchar8='Z ' || varchar8
    #  +++>>>       where varchar8 < 'C';
    stmt = """select varchar8 from V1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s4')
    
    # Delete through view.
    stmt = """delete from V1 where varchar8='empty';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    stmt = """select varchar8 from V1 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s5')
    
    stmt = """delete from V1 where varchar8>='D';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select varchar8 from V1 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s6')
    
    stmt = """delete from V1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    
    stmt = """select count(*) from V1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s7')
    
    stmt = """drop view V1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table T1A15;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # ------------------------------
    # Create multi-column table and view; insert/update/delete via view.
    # ------------------------------
    stmt = """create table T3(
ordering  int not null
, varchar3  varchar(3)
, varchar4  varchar(4)
, primary key (ordering)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Insert into table then create updateable view.
    stmt = """insert Into T3 Values(11,'abc','CC');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select varchar3 from T3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s8')
    
    stmt = """create view V3 as select * from T3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Insert into tables and views.
    stmt = """insert Into V3 Values(21,NULL,'AA');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert Into T3 Values(12,NULL,'CACA');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert Into V3 Values(22,'e','CCCC');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert Into V3 Values(23,'f','Z');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    #  Check values in the primary key.
    #  Expect 5 rows.
    stmt = """select ordering from T3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s9')
    #
    #  Update through view.
    #  +++>>>       update V3 set ordering=99
    #  +++>>>    		       , varchar3='up'
    #  +++>>>    		       , varchar4='date'
    #  +++>>>          where varchar4='CC';
    #  +++>>>       update V3 set varchar4='Z'
    #  +++>>>          where ordering<22;
    stmt = """select * from T3 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s10')
    stmt = """select * from V3 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s11')
    #
    # Delete through view.
    stmt = """delete from V3 where varchar3 is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    #  Expect 3 rows.
    stmt = """select count(*) from V3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s12')
    #
    stmt = """delete from V3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)
    #  Expect 0 rows.
    stmt = """select count(*) from V3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s13')
    #
    # Drop objects.
    stmt = """drop view V3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table T3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test016(desc="""a16"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Includes SQL features (from list of May 19, 1997):
    #	G026 NATURAL JOIN.
    #	See A04-A06 for Inner, Left Outer, Right Outer Joins.
    #
    #
    # ---------------------------
    # Ensure (even if SQLCI default changes to AUTOCOMMIT OFF) that
    # each SQL statement is committed immediately.
    # ---------------------------
    
    stmt = """SET TRANSACTION AUTOCOMMIT ON;"""
    output = _dci.cmdexec(stmt)
    #
    #  ---------------------------------------
    #  Initially check contents of table, view.
    #  ---------------------------------------
    #  Expect 5 rows:
    stmt = """select * from BTloc1 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s0')
    #
    #  Expect 7 rows:
    stmt = """select * from BTloc2 
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s1')
    #
    #  ---------------------------------------
    #  natural inner, outer left, and outer right joins.
    #  ---------------------------------------
    #  Should show rows as in base table.
    stmt = """select T1.varchar7 as t1varchar7, T1.char8 as t1char8,
t2.varchar7 as t2varchar7, t2.char8 as t2char8
from BTloc2 T1 
, BTloc2 t2
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s2')
    #
    #  Should show 5 rows as in base table.
    stmt = """select varchar7, char8
from BTloc2 
natural join BTloc2 t
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s3')
    
    #  Should show 0 rows (no match).
    #  Should show 35 rows (5*7).
    stmt = """select t2.varchar7, t2.char8, T1.v
from BTloc1 T1 
natural INNER join BTloc2 t2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s4')
    
    #  Compare with the unnatural INNER join.
    #  Should show 35 rows (5*7).
    
    stmt = """select t2.varchar7, t2.char8, T1.v
from BTloc1 T1 
INNER join BTloc2 t2
on (1=1)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s5')
    
    #  Note the lack of column ambiguity.
    stmt = """select varchar7, char8, v
from BTloc1 T1 
natural INNER join BTloc2 t2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s6')
    
    #  Should show rows as in base table #1, null extended in other table.
    stmt = """select t2.varchar7, t2.char8, T1.v
from BTloc1 T1 
natural LEFT JOIN BTloc2 t2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s7')
    stmt = """select t2.varchar7, t2.char8, T1.v
from BTloc1 T1 
LEFT JOIN BTloc2 t2
on 1=1
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s8')
    stmt = """select varchar7, char8, v
from BTloc1 T1 
natural LEFT JOIN BTloc2 t2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s9')
    
    #  Should show rows as in base table #2, null extended to left.
    stmt = """select t2.varchar7, t2.char8, T1.v
from BTloc1 T1 
natural RIGHT OUTER JOIN BTloc2 t2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s10')
    stmt = """select t2.varchar7, t2.char8, T1.v
from BTloc1 T1 
RIGHT OUTER JOIN BTloc2 t2
on 1=1
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s11')
    stmt = """select *
from BTloc1 T1 
natural RIGHT OUTER JOIN BTloc2 t2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s12')
    
    _testmgr.testcase_end(desc)

def test017(desc="""a17"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # For SQL functions ABS, VARIANCE, STDDEV.
    # (from list of January 23, 1998, reviewed at QA meeting.
    #
    # Note that CAST is used in this testing to deal with practical number
    # of significant digits; and that CAST truncates; whereas it would be more
    # precise to round, CAST can (according to the ANSI specification) be
    # truncated or rounded at the implementor's discretion. 
    #
    # ---------------------------------------
    # These equivalences are used below:
    # ---------------------------------------
    # (1) SD(X) = square-root of (VARIANCE(X))
    #     Also VARIANCE (X) = STDDEV(X)*STDDEV(X)
    # (2) VARIANCE(a*X+b)=a^2*VARIANCE(X)
    # (3) SD(a*X+b)=|a|*SD(X)
    # (4) VARIANCE(X) = SUM(ABS(X - AVG(X))^2)/(N-1)
    #
    #
    # ---------------------------
    # Ensure (even if SQLCI default changes to AUTOCOMMIT OFF) that
    # each SQL statement is committed immediately.
    # ---------------------------
    
    stmt = """SET TRANSACTION AUTOCOMMIT ON;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table WEATHER;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """Create table WEATHER (
line_item   int
, City        char(10)
, State       char(2)
, Temperature smallint
, Weight      smallint
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # ---------------------------------------
    # Perform ABS on 0-row table.
    # ABS gives absolute value.
    # e.g. The function ABS(-20 + 12) returns the value 8:
    # ---------------------------------------
    # Expect 0 rows thoughout.
    
    stmt = """SELECT ABS(TEMPERATURE), ABS (-2 * WEIGHT)
FROM WEATHER;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """SELECT ABS(TEMPERATURE), ABS (-2 * WEIGHT)
FROM WEATHER 
GROUP BY TEMPERATURE, WEIGHT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #
    stmt = """SELECT COUNT(*)
FROM WEATHER;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s0')
    #
    stmt = """SELECT COUNT(*), ABS(TEMPERATURE), ABS (-2 * WEIGHT)
FROM WEATHER 
GROUP BY TEMPERATURE, WEIGHT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #
    # ---------------------------------------
    # Insert a row of zeros and blanks, then Perform ABS on 1-row table.
    # ---------------------------------------
    #
    stmt = """Insert into WEATHER values ( 0, '', '', 0, 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    #  Expect ( (0  0) )
    stmt = """SELECT ABS(TEMPERATURE), ABS (-2 * WEIGHT)
FROM WEATHER;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s1')
    
    #  Expect ( (1  0  0) )
    
    stmt = """SELECT COUNT(*), ABS(TEMPERATURE), ABS (-2 * WEIGHT)
FROM WEATHER 
GROUP BY TEMPERATURE, WEIGHT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s2')
    
    stmt = """DELETE FROM WEATHER;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    # ---------------------------------------
    # Insert a row then Perform ABS on 1-row table.
    # ---------------------------------------
    
    stmt = """Insert into WEATHER values ( 1,'Austin',    'TX', 50,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  Expect ( (50  2) )
    stmt = """SELECT ABS(TEMPERATURE), ABS (-2 * WEIGHT)
FROM WEATHER;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s3')
    
    #  Expect ( (50  1  50  2) )
    stmt = """SELECT TEMPERATURE, WEIGHT, ABS(TEMPERATURE), ABS (-2 * WEIGHT)
FROM WEATHER;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s4')
    #
    #  ---------------------------------------
    #  Perform ABS on 1-row table.
    #  ABS gives absolute value.
    #  e.g. The following function returns the value 8: ABS (-20 + 12)
    #  Do not perform VARIANCE or STDDEV on 1-row table, as their formulae
    #  divides by (N-1) which ZERO when there is only only row.
    #  ---------------------------------------
    #
    #  Expect ( (50, 1, 50, 2) )
    stmt = """SELECT TEMPERATURE, WEIGHT, ABS(TEMPERATURE), ABS (-2 * WEIGHT)
FROM WEATHER;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s5')
    #
    # ---------------------------------------
    # Perform ABS, VARIANCE, STDDEV on 2-row table.
    # STDDEV ([ALL | DISTINCT] expression [,weight])
    # VARIANCE ([ALL | DISTINCT] expression [,weight])
    # ---------------------------------------
    #
    # Insert second row:
    stmt = """Insert into WEATHER values ( 2,'Austin',    'TX', 40,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  Expect 2 rows.
    stmt = """SELECT *
FROM WEATHER 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s6')
    #
    #  Expect ( (40  1  40  2) (50  1  50  2) )
    stmt = """SELECT TEMPERATURE, WEIGHT, ABS(TEMPERATURE), ABS(-2 * WEIGHT)
FROM WEATHER 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s7')
    #
    #  Formula (4): Expect ( (50) ) = (5^2 + 5^2)/(2-1).
    stmt = """SELECT CAST( VARIANCE(TEMPERATURE) as numeric(6,2))
FROM WEATHER;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s8')
    #
    #  Formula (1): Expect ( squareroot(50) ) = (7.07).
    #  Known bogus DISTINCT error reported elsewhere with DISTINCT and ALL.
    stmt = """SELECT CAST( STDDEV(DISTINCT TEMPERATURE) as numeric(6,2)) as S_DISTINCT
, CAST( STDDEV(ALL TEMPERATURE, 1) as numeric(6,2)) as S_ALL
FROM WEATHER 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s9')
    #  Don't sweat it if the lower-precision digits change a little.
    stmt = """SELECT STDDEV(DISTINCT TEMPERATURE) as S_DISTINCT
FROM WEATHER 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s10')
    #  Expect ( (7.07) )
    stmt = """SELECT CAST( STDDEV(ALL TEMPERATURE, 1) as numeric(6,2)) as S_ALL
FROM WEATHER 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s11')
    #
    #  Also in Formula (1): VARIANCE (X) = STDDEV(X)*STDDEV(X)
    #  Expect ( (50  50) )
    stmt = """SELECT CAST( VARIANCE(TEMPERATURE) as numeric(6,2))
as V
, CAST( STDDEV(TEMPERATURE)*STDDEV(TEMPERATURE) as numeric(6,2))
as S
FROM WEATHER;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s12')
    #
    #  Put weight factor of 1 on VARIANCE and STDDEV.
    #  Expect ( (50  50) )
    stmt = """SELECT CAST( VARIANCE(TEMPERATURE,1) as numeric(6,2))
, CAST( STDDEV(TEMPERATURE,1)*STDDEV(TEMPERATURE,1)
as numeric(6,2))
FROM WEATHER;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s13')
    #
    #  Formula (2): VARIANCE(a*X+b)=a^2*VARIANCE(X)
    #  Expect ( (5000  5000) )
    stmt = """SELECT CAST( VARIANCE(10 * TEMPERATURE + 42) as numeric(6,2))
as VARIANCE_of_a_times_TEMP_plus_b
, CAST( 10 * 10 * VARIANCE(TEMPERATURE) as numeric(6,2))
as a_squared_times_VARIANCE_TEMP
FROM WEATHER;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s14')
    #
    #  Formula (3): SD(a*X+b)=|a|*SD(X)
    #  Expect ( (70.71  70.71) )
    stmt = """SELECT CAST( STDDEV(-10 * TEMPERATURE + 42) as numeric(6,2))
as STDDEV_of_a_times_TEMP_plus_b
, CAST( ABS(-10) * STDDEV(TEMPERATURE) as numeric(6,2))
as ABS_a_times_STDDEV_TEMP
FROM WEATHER;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s15')
    #
    # ---------------------------------------
    # More inserts.
    # ---------------------------------------
    stmt = """Insert into WEATHER values ( 3,'Austin',    'TX', 60,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """Insert into WEATHER values ( 4,'Austin',    'TX', 84,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """Insert into WEATHER values (11,'Cupertino', 'CA', 65,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """Insert into WEATHER values (12,'Cupertino', 'CA', 65,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """Insert into WEATHER values (13,'Cupertino', 'CA', 65,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """Insert into WEATHER values (14,'Cupertino', 'CA', 65,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  Expect 8 rows!
    stmt = """Select * from WEATHER order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s16')
    #
    #  ---------------------------------------
    #  Check other aggregates -- AVG, SUM, COUNT.
    #  ---------------------------------------
    #
    #  As the average temperature is 61.75 we expect ((61.75  0  7))
    stmt = """select CAST( avg(temperature) as numeric(6,2))
as avg_temperature
, CAST( SUM(TEMPERATURE-61.75) as numeric(6,2))
as compare_to_mean
, CAST( (count(temperature) - 1) as numeric(6,2))
as count_less_1
FROM WEATHER;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s17')
    #
    #  ---------------------------------------
    #  ABS gives absolute value.
    #  ---------------------------------------
    #  Expect:
    #    ( ( 40 , 1 ,  2 )
    #      ( 50 , 1 ,  8 )
    #      ( 60 , 2 , 24 )
    #      ( 65 , 1 , 23 )
    #      ( 65 , 1 , 23 )
    #      ( 65 , 2 , 19 )
    #      ( 65 , 2 , 19 )
    #      ( 84 , 2 ,  0 ) )
    stmt = """SELECT TEMPERATURE, WEIGHT
, ABS(TEMPERATURE - (42 * WEIGHT)) as a
FROM WEATHER 
order by 1,2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s18')
    #
    #  ---------------------------------------
    #  Find the VARIANCE of TEMPERATURE.
    #  ---------------------------------------
    #
    #  Expect: ((164.50))
    stmt = """SELECT CAST( VARIANCE(TEMPERATURE) as numeric(6,2))
as variance_temp
FROM WEATHER;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s19')
    #
    #  Find the variance of the TEMPERATURE column by CITY:
    #  Expect: (('Austin' 319.60) ('Cupertino' .00))
    stmt = """SELECT CITY, CAST( VARIANCE (TEMPERATURE, WEIGHT) as numeric(6,2))
as variance_temp
FROM WEATHER GROUP BY CITY
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s20')
    #
    #  Find the weighted variance of the TEMPERATURE column.
    #  Expect: ((146.36))
    stmt = """SELECT CAST( VARIANCE (TEMPERATURE, WEIGHT) as numeric(6,2))
as variance_temp
FROM WEATHER;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s21')
    #
    #  ---------------------------------------
    #  STDDEV ([ALL | DISTINCT] expression [,weight])
    #  ---------------------------------------
    #
    #  Find the standard deviation of the TEMPERATURE column by STATE.
    #  Expect (('CA' 65) then 4 'TX' and their temps)
    stmt = """SELECT STATE, TEMPERATURE
FROM WEATHER GROUP BY STATE, TEMPERATURE
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s22')
    #  Here's the standard deviation for each group.
    #  Expect (('CA' .00) ('TX' 18.85))
    stmt = """SELECT STATE, CAST( STDDEV (TEMPERATURE) as numeric(6,2))
FROM WEATHER GROUP BY STATE
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s23')
    #
    #  ---------------------------------------
    #  Check equivalences.
    #  ---------------------------------------
    #
    #  (1) SD(X) = square-root of (VAR(X)) -- equivalent VAR(X)=SD(X)*SD(X)
    #  Expect ((164.50  164.50 or 164.49))
    #  slight difference is ok (due to rounding errors).
    stmt = """SELECT CAST( VARIANCE(TEMPERATURE) as numeric(6,2))
as VARIANCE_temp
, CAST( STDDEV(TEMPERATURE)*STDDEV(TEMPERATURE)
as numeric(6,2))
as STDDEV_temp_squared
FROM WEATHER;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s24')
    #
    #  (2) VAR(a*X+b)=a^2*VAR(X)
    #  Expect ((16450  16450))
    stmt = """SELECT CAST( VARIANCE(-10 * TEMPERATURE + 42) as int)
as VARIANCE_formula_1
, CAST( (-10)*(-10)* VARIANCE(TEMPERATURE) as int)
as VARIANCE_formula_2
FROM WEATHER;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s25')
    #
    #  (3) SD(a*X+b)=|a|*SD(X)
    #  Expect ((128.25  128.25))
    stmt = """SELECT CAST( STDDEV(-10 * TEMPERATURE + 42) as numeric(6,2))
, CAST( ABS(-10) * STDDEV(TEMPERATURE) as numeric(6,2))
FROM WEATHER;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s26')
    #
    #  (4) VARIANCE(X) = SUM(ABS(X - AVG(X))^2)/(N-1)
    #      Note that 61.75 is values obtained earlier for average.
    #  Expect ((164.50  70.50  164.50))
    stmt = """SELECT CAST( VARIANCE(TEMPERATURE) as numeric(6,2))
, CAST( SUM(ABS(TEMPERATURE - 61.75)) as numeric(6,2))
, CAST( SUM(ABS(TEMPERATURE - 61.75) * ABS(TEMPERATURE - 61.75)) /
((select count(temperature) from WEATHER) -1)
as numeric(6,2)
)
FROM WEATHER;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s27')
    #
    # ---------------------------------------
    # Insert NULLs.
    # ---------------------------------------
    stmt = """Insert into WEATHER values ( 5,'Austin',    NULL, NULL, NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """Select * from WEATHER order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s28')
    #
    #  ---------------------------------------
    #  Check ABS.
    #  ---------------------------------------
    #  Expect ( (74  14) )
    stmt = """SELECT CAST( SUM( ABS( TEMPERATURE -60 ) )
as numeric(6,2)),
CAST( SUM( TEMPERATURE -60 )
as numeric(6,2))
FROM WEATHER;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s29')
    #
    #  ---------------------------------------
    #  Check the equivalence between VARIANCE and STDDEV.
    #  ---------------------------------------
    #
    #  (1) SD(X) = square-root of (VAR(X))
    #  nulls are excluded
    #  Expect ((164.50  164.49)) -- slight difference due to rounding errors.
    stmt = """SELECT CAST( VARIANCE(TEMPERATURE) as numeric(6,2))
as VARIANCE_temp
, CAST( STDDEV(TEMPERATURE)*STDDEV(TEMPERATURE)
as numeric(6,2))
as STDDEV_temp_squared
FROM WEATHER;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s30')
    
    _testmgr.testcase_end(desc)

def test018(desc="""b03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #
    # ---------------------------
    # Ensure (even if SQLCI default changes to AUTOCOMMIT OFF) that
    # each SQL statement is committed immediately.
    # ---------------------------
    
    stmt = """SET TRANSACTION AUTOCOMMIT ON;"""
    output = _dci.cmdexec(stmt)
    #
    #  Expect 5 rows:
    stmt = """select * from VNloc8 
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b03exp""", 'b03s0')
    #
    #  ---------------------------------------
    #  Simple natural join of substring on column of basetable,
    #  and of view column that uses that feature.
    #  ---------------------------------------
    #
    #  Note that the BASE TABLE is joined to the UNION VIEW,
    #  which has all the column names and rows as in base table.
    #  Should show number of rows as in view.
    #
    stmt = """select count(*) from BTloc8 -- 'BT' is correct here.
natural join VNloc8 t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b03exp""", 'b03s1')
    
    _testmgr.testcase_end(desc)

def test019(desc="""b06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #
    # ---------------------------
    # Ensure (even if SQLCI default changes to AUTOCOMMIT OFF) that
    # each SQL statement is committed immediately.
    # ---------------------------
    
    stmt = """SET TRANSACTION AUTOCOMMIT ON;"""
    output = _dci.cmdexec(stmt)
    #
    # ------------------------------
    #    Bug test for inability of SQL to recognize
    #	correlation name in joined views.
    # ------------------------------
    
    stmt = """create table T1B06(
varchar7  varchar(7)
, char8     PIC X(8)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Insert.
    stmt = """Insert Into T1B06 Values ('X', 'X');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """Insert Into T1B06 Values ('EE', 'EE');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """Insert Into T1B06 Values (null, 'EE');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """Insert Into T1B06 Values ('CAAAAAA', 'CAAAAAA');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """Insert Into T1B06 Values ('DAAAAAA', 'CAAAAAAX');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """Insert Into T1B06 Values ('AAAAAAA', null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """Insert Into T1B06 Values ('X', 'EE');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    #  ------------------------------
    #  View with correlation name on single-table select:
    #  ------------------------------
    #  Expect { (CAAAAAA) (CAAAAAAX)
    #          (EE) (EE) (EE) (X) (null) }
    stmt = """select T.char8 from T1B06 T order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b06exp""", 'b06s0')
    #
    # Note this mismatch on # of columns gave internal error 1001
    # for ark 970925:
    #   create view VB06 (c1, c2) as select T.char8 from T1B06 T ;
    #
    stmt = """create view VB06 (c1, c2) as
select varchar7, T.char8 from T1B06 T ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Expect 7 rows.
    stmt = """select  c1, V1.c2
from VB06 V1 
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b06exp""", 'b06s1')
    stmt = """drop view VB06;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  ------------------------------
    #  View with correlation name on joined-table select:
    #  ------------------------------
    #  Expect {(CAAAAAA, CAAAAAA)
    #          (EE, EE) (EE, EE) (EE, EE) (X, X) (X, X)
    #          (null, CAAAAAAX) (null, null) }
    stmt = """select T1.varchar7, T2.char8
from T1B06 T1 
right join T1B06 T2
on T1.varchar7=T2.char8
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b06exp""", 'b06s2')
    
    stmt = """create view VB06 (c1, c2) as
select T1.varchar7, T2.char8
from T1B06 T1 
right join T1B06 T2
on T1.varchar7=T2.char8
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select  c1, V1.c2
from VB06 V1 
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b06exp""", 'b06s3')
    stmt = """drop view VB06;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table T1B06;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test020(desc="""b09"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """set transaction autocommit on;"""
    output = _dci.cmdexec(stmt)
    #
    # ---------------------------
    #      Id: TV.051       VALUES clause (i.e., TVC) can include multiple RVCs.
    #      Id: TV.052       Within TVC, RVC can include a subquery that returns a single value.
    # Hence, the following INSERT statement is valid:
    #          INSERT INTO T VALUES (a, (SELECT ...), b, c) .
    #      Moved to here 970923 from 1113:A09.
    # ---------------------------
    #
    
    stmt = """create table T1B09(
varchar13 varchar(13) not null
, varchar7  varchar(7)  not null
, somenumber int        not null
, primary key ( varchar13, varchar7)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  Expect {(13, 39066)}.
    stmt = """select count(sdec13_uniq), sum(sdec13_uniq)
from BTloc4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b09exp""", 'b09s0')
    #
    stmt = """insert Into T1B09 Values( 'aa', 'aaa', (13) ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select distinct 13 from BTloc4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b09exp""", 'b09s1')
    stmt = """insert Into T1B09 Values( 'bb', 'bbb',
(select distinct 13 from BTloc4 )
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select count(sdec13_uniq), sum(sdec13_uniq) from BTloc4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b09exp""", 'b09s2')
    stmt = """insert Into T1B09 Values( 'on', 'off',
(select count(sdec13_uniq) from BTloc4 )
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert Into T1B09 Values( 'ad', 'astra',
(select sum(sdec13_uniq) from BTloc4 )
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    #  Expect 2 rows.
    stmt = """select * from T1B09 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b09exp""", 'b09s3')
    #
    # ---------------------------
    # Clean up here because tests below can abort SQL
    # before it reaches the end.
    # ---------------------------
    stmt = """drop table T1B09;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  ---------------------------
    #       Id: TV.071       Table Value Constructor values use DISTINCT.
    # 			 e.g. SELECT <select-list> FROM VALUES <TVC
    # 			 containing subquery like Select <cols> from
    # 			 (select AVG(DISTINCT <arithmetic expression>)
    # 			    from t)dt>;
    #  ---------------------------
    #  Expect 13 rows.
    stmt = """select sdec13_uniq from BTloc4 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b09exp""", 'b09s4')
    #
    #  Expect {(6)}.
    stmt = """select DISTINCT sdec13_uniq from BTloc4 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b09exp""", 'b09s5')
    #
    stmt = """select count(DISTINCT sdec13_uniq) from BTloc4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b09exp""", 'b09s6')
    stmt = """select * from (
select count(DISTINCT sdec13_uniq) from BTloc4 
) x
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b09exp""", 'b09s7')

    stmt = """select count( sdec13_uniq)
, sum( sdec13_uniq)
from BTloc4 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b09exp""", 'b09s8')
    #
    stmt = """select a,b from (
select count(sdec13_uniq)
, sum(sdec13_uniq)
from BTloc4 
) x(a,b)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b09exp""", 'b09s9')
    #
    #  Expect {(6, 17853)}.
    stmt = """select count(DISTINCT sdec13_uniq)
, sum(DISTINCT sdec13_uniq)
from BTloc4 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b09exp""", 'b09s10')
    #
    #  Expect {(6, 17853)}.
    stmt = """select a,b from (
select count(DISTINCT sdec13_uniq)
, sum(DISTINCT sdec13_uniq)
from BTloc4 
) x(a,b)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b09exp""", 'b09s11')
    
    stmt = """select a,b from (
select count(DISTINCT sdec13_uniq)
, sum(DISTINCT sdec13_uniq)
from BTloc4 
) x(a,b)
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b09exp""", 'b09s12')
    stmt = """select count(DISTINCT sdec13_uniq)
from BTloc4 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b09exp""", 'b09s13')
    
    _testmgr.testcase_end(desc)

def test021(desc="""b14"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Test pulled out of testA14 to separate out BUGs.
    #
    #           Relax NULL restrictions:
    #           'A <row value constructor> that "IS [NOT] NULL" shall be
    #            a <column reference>.'
    #           ANSI standard SQL92 section 8.6 for NULL.
    #
    #
    # ---------------------------
    # Ensure (even if SQLCI default changes to AUTOCOMMIT OFF) that
    # each SQL statement is committed immediately.
    # ---------------------------
    
    stmt = """SET TRANSACTION AUTOCOMMIT ON;"""
    output = _dci.cmdexec(stmt)
    #
    #  View VNloc8 used here has 5 rows:
    #  SBIN0_4      VARCHAR0_500  UBIN16_N10  SDEC16_UNIQ           CHAR16_N20  CHAR17_2
    #  -----------  ------------  ----------  --------------------  ----------  --------
    #            0  BDAAAAAA               8                  2028  AD          AAAAAAAA
    #            1  ACAABAAA               3                  1993  BDAA        AAAAAAAA
    #            1  BBA%FAAA               3                  3293  BD          BAAAAAAA
    #            1  BBAABA_A               1                  3917  BBAA        BAAAAAAA
    #            3  CAAAGAAA               1                  4151  BB          BAAAAAAA
    #  -----------  ------------  ----------  --------------------  ----------  --------
    #
    #  ---------------------------
    #  NULL predicate. Allow a <row value constructor> that
    #  "IS [NOT] NULL" to be a non-<column reference>.'
    #  ---------------------------
    #  Non-column reference is a string constant.
    #  Expect all 5 rows as predicate is true.
    stmt = """select sbin0_4, varchar0_500 from VNloc8 
where ('a') is not NULL
order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b14exp""", 'b14s0')
    #
    # Similarly with a parameter.
    stmt = """set param ?p 'alpha centauri';"""
    output = _dci.cmdexec(stmt)
    #  Use CAST to avoid internal error 8816 referencing TCB tree.
    #  Expect all 5 rows as predicate is true.
    stmt = """select sbin0_4, varchar0_500 from VNloc8 
where cast(?p as varchar(14)) is not NULL
order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b14exp""", 'b14s1')
    # Expect 0 rows as predicate is false.
    
    stmt = """select sbin0_4, varchar0_500 from VNloc8 
where cast(?p as varchar(14)) is NULL
order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    #  Expect all 5 rows as predicate is true.
    #  JDBC has no knowledge of the length of parameter ?p.
    #  It is recommendated always cast the parameter explicitily 
    stmt = """select sbin0_4, varchar0_500 from VNloc8 
where cast(?p as varchar(14)) = 'alpha centauri'
order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b14exp""", 'b14s2')
    #
    #  Non-column reference is "NULL".
    #  Expect all 5 rows as predicate is true.
    stmt = """select sbin0_4, varchar0_500 from VNloc8 
where NULL is NULL
order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b14exp""", 'b14s3')
    #
    stmt = """set param ?p NULL;"""
    output = _dci.cmdexec(stmt)
    # Expect 0 rows as predicate is false.
    stmt = """select sbin0_4, varchar0_500 from VNloc8 
where cast(?p as varchar(14)) is not NULL
order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    # Expect 0 rows as predicate is false.
    stmt = """select sbin0_4, varchar0_500 from VNloc8 
where cast((?p+sbin0_4) as int) is not NULL
order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #  Expect all 5 rows as predicate is true.
    stmt = """select sbin0_4, varchar0_500 from VNloc8 
where cast(?p as varchar(14)) is NULL
order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/b14exp""", 'b14s4')
    # Expect 0 rows as predicate is false.
    # It will return error "NULL cannot be assigned to a NOT NULL column,
    # parameter 0", the descriptor treat parameter as not nullable
    # see the comments in bugzilla for bug 1709
    stmt = """select sbin0_4, varchar0_500 from VNloc8 
where ?p = 'alpha centauri'
order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    _testmgr.testcase_end(desc)

