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
    
def test001(desc="""create tables"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # ==============================
    # BTloc1 is a single-column table.
    # ==============================
    stmt = """create table BTloc1(
v  varchar(8)  not null
, primary key (v DESC)
);"""
    output = _dci.cmdexec(stmt)
    #
    # Insert before making views.
    stmt = """Insert Into BTloc1 Values('CA');"""
    output = _dci.cmdexec(stmt)
    stmt = """Insert Into BTloc1 Values('CCAA');"""
    output = _dci.cmdexec(stmt)
    stmt = """Insert Into BTloc1 Values('CACAAAAA');"""
    output = _dci.cmdexec(stmt)
    stmt = """Insert Into BTloc1 Values('CCCCAAAA');"""
    output = _dci.cmdexec(stmt)
    stmt = """Insert Into BTloc1 Values('CCCCA');"""
    output = _dci.cmdexec(stmt)
    #
    # Create View; updateable.
    stmt = """create view  VUlocal1 as
select * from BTloc1;"""
    output = _dci.cmdexec(stmt)
    #
    # Check values.
    stmt = """select v from BTloc1 order by 1;"""
    output = _dci.cmdexec(stmt)
    stmt = """select v from VUlocal1 order by 1;"""
    output = _dci.cmdexec(stmt)
    #
    # ==============================
    # BTloc2.
    # ==============================
    stmt = """create table BTloc2(
varchar7  varchar(7)
, char8     PIC X(8)
) no partition;"""
    output = _dci.cmdexec(stmt)
    #
    # Insert.
    stmt = """Insert Into BTloc2 Values ('X', 'X');"""
    output = _dci.cmdexec(stmt)
    stmt = """Insert Into BTloc2 Values ('EE', 'EE');"""
    output = _dci.cmdexec(stmt)
    stmt = """Insert Into BTloc2 Values (null, 'EE');"""
    output = _dci.cmdexec(stmt)
    stmt = """Insert Into BTloc2 Values ('CAAAAAA', 'CAAAAAA');"""
    output = _dci.cmdexec(stmt)
    stmt = """Insert Into BTloc2 Values ('DAAAAAA', 'CAAAAAAX');"""
    output = _dci.cmdexec(stmt)
    stmt = """Insert Into BTloc2 Values ('AAAAAAA', null);"""
    output = _dci.cmdexec(stmt)
    stmt = """Insert Into BTloc2 Values ('X', 'EE');"""
    output = _dci.cmdexec(stmt)
    #
    stmt = """create table BTloc2b(
varchar7  varchar(7)
, char8     PIC X(8)
) no partition;"""
    output = _dci.cmdexec(stmt)
    # Insert.
    stmt = """Insert Into BTloc2b select * from BTloc2;"""
    output = _dci.cmdexec(stmt)
    #
    # Expect { (CAAAAAA) (CAAAAAAX)
    #         (EE) (EE) (EE) (X) (null) }
    stmt = """select BTloc2b.char8 from BTloc2b order by 1;"""
    output = _dci.cmdexec(stmt)
    
    # Expect {(CAAAAAA, CAAAAAA)
    #         (EE, EE) (EE, EE) (EE, EE) (X, X) (X, X)
    #         (null, CAAAAAAX) (null, null) }
    stmt = """select BTloc2.varchar7, BTloc2b.char8
from BTloc2 
right join BTloc2b 
on BTloc2.varchar7=BTloc2b.char8
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select BTloc2.varchar7, BTloc2b.char8
from BTloc2 
right join BTloc2b 
on BTloc2.varchar7=BTloc2b.char8
group by BTloc2.varchar7, BTloc2b.char8
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view VNloc2 (c1, c2) as
select BTloc2.varchar7, BTloc2b.char8
from BTloc2 
right join BTloc2b 
on BTloc2.varchar7=BTloc2b.char8
group by BTloc2.varchar7, BTloc2b.char8
;"""
    output = _dci.cmdexec(stmt)
    
    # Check values.
    stmt = """select *
from BTloc2 T1 
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    stmt = """select *
from VNloc2 T1 
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    #
    # ==============================
    # BTloc3.
    # ==============================
    stmt = """create table BTloc3(
varchar15   VarChar(8)  not null
, ubin15      INTEGER unsigned  not null
, primary key (varchar15, ubin15)
);"""
    output = _dci.cmdexec(stmt)
    #
    # Insert before making views.
    stmt = """insert Into BTloc3 
Values ('CCAAKAAB', 7);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert Into BTloc3 
Values ('DEAACAAE', 1995);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert Into BTloc3 
Values ('FGAADAAE', 1997);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert Into BTloc3 
Values ('DDAABAAD', 1996);"""
    output = _dci.cmdexec(stmt)
    #
    # June 13 '97 -- Create commented out temporarily.
    # July 11 '97 - Restored Create for July 30 code.
    stmt = """create view VUlocal3 as
select *
from BTloc3 
where ubin15 > 1000
;"""
    output = _dci.cmdexec(stmt)
    #
    # Check values.
    # Expect 4 rows.
    stmt = """select varchar15, ubin15
from BTloc3 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    #
    # Expect 3 rows.
    stmt = """select varchar15, ubin15
from VUlocal3 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    #
    # ==============================
    # BTloc4.
    # ==============================
    stmt = """create table BTloc4(
varchar0_4       varchar(3)              not null,
--     char0_1000       PIC X(64)               not null,
varchar5_10      VarChar(8)              not null,
--     char6_20         PIC X(8)                not null,    

varchar13_100    VarChar(5)              not null,
sdec13_uniq      Numeric(9,0) signed     not null,    

char14_20        Char(2)                 not null,
udec15_4         Decimal(9,2) unsigned   not null,    

varchar15_uniq   VarChar(9)              not null,
ubin15_uniq      INTEGER unsigned        not null,
char16_uniq      PIC X(8)                not null
-- leading odd-length column on key.
, primary key
( varchar13_100  DESC
, sdec13_uniq    ASC
, char14_20
, varchar15_uniq
)
)
;"""
    output = _dci.cmdexec(stmt)
    #
    # Insert before making views.
    stmt = """Insert Into BTloc4 
Values ('A',
'AEAAAAA',
'AJAA ', 3112,
'AE',
.03,
'FJAAGAA', 4559,
'FJAAGAAE'
);"""
    output = _dci.cmdexec(stmt)
    stmt = """Insert Into BTloc4 
Values ('CAA',
'ACAAA',
'ARAA ', 1413,
'CC',
.01,
'EJAAJAA',  3889,
'EJAAJAAC'
);"""
    output = _dci.cmdexec(stmt)
    stmt = """Insert Into BTloc4 
Values ('AAA',
'ABAAAAAA',
'AG', 4217,
'AB',
.03,
'FGAAAAAB',  1188,
'FGAAAAAB'
);"""
    output = _dci.cmdexec(stmt)
    stmt = """Insert Into BTloc4 
Values ('A',
'ACAAA',
'AM', 3030,
'AC',
.00,
'BEAAGAAC',  4412,
'BEAAGAAC'
);"""
    output = _dci.cmdexec(stmt)
    #
    # Start of rows added for adjacent values of primary keys.
    # This is row 5; columns of primary key:
    #
    #       VARCHAR13_100  SDEC13_UNIQ  CHAR14_20  VARCHAR15_UNIQ
    #
    # is same as in row 4 above:
    #
    #       AM                    3030  AC         BEAAGAAC
    #
    # except last column is one later (BEAAGAAD).  The plan for
    # these columns is to change each column to:
    # (a) 'adjacent' value (e.g. 3030 to 3031; BEAAGAAC to BEAAGAAD)
    # (b) value separated by a gap of 1 or more letters or digits,
    #     (e.g. 3031 to 3050; BEAAGAAC to BEAAGAAF).
    #
    #       VARCHAR13_100  SDEC13_UNIQ  CHAR14_20  VARCHAR15_UNIQ
    #       --==========-  --========-  --======-  --============
    # (4)   AM                    3030  AC         BEAAGAAC
    # (5)   (s)=same               (s)  (s)        BEAAGAAD
    # (6)   (s)                    (s)  AE         BEAAGAAC
    # (7)   (s)                    (s)  (s)        BEAAGAAE
    # (8)   (s)                   3031  AC         BEAAGAAC
    # (9)   (s)                    (s)  (s)        BEAAGAAF
    # (10)  (s)                    (s)  (s)        BEAAGAAG
    # (11)  (s)                    (s)  AD         BEAAGAAD
    # (12)  (s)                   3050  AC         BEAAGAAC
    # (13)  AN                    3030  AC         BEAAGAAC
    #
    stmt = """Insert Into BTloc4 
Values ('E',
'AE',
'AM', 3030,
'AC', .00,
'BEAAGAAD', 5000,
'BF'
);"""
    output = _dci.cmdexec(stmt)
    #
    # Row 6:
    stmt = """Insert Into BTloc4 
Values ('F',
'AF',
'AM', 3030,
'AE', .06,
'BEAAGAAC', 6000,
'BF'
);"""
    output = _dci.cmdexec(stmt)
    #
    # Row 7:
    stmt = """Insert Into BTloc4 
Values ('G',
'AG',
'AM', 3030,
'AE',
.07,
'BEAAGAAE', 7000,
'BG'
);"""
    output = _dci.cmdexec(stmt)
    #
    # Row 8:
    stmt = """Insert Into BTloc4 
Values ('H',
'AH',
'AM', 3031,
'AC',
.08,
'BEAAGAAC', 8000,
'BH'
);"""
    output = _dci.cmdexec(stmt)
    #
    # Row 9:
    stmt = """Insert Into BTloc4 
Values ('I',
'AI',
'AM', 3031,
'AC',
.09,
'BEAAGAAF', 9000,
'BI'
);"""
    output = _dci.cmdexec(stmt)
    #
    # Row 10:
    stmt = """Insert Into BTloc4 
Values ('J',
'AJ',
'AM', 3031,
'AC',
.10,
'BEAAGAAG', 10000,
'BJ'
);"""
    output = _dci.cmdexec(stmt)
    #
    # Row 11:
    stmt = """Insert Into BTloc4 
Values ('K',
'AK',
'AM', 3031,
'AD',
.11,
'BEAAGAAD', 11000,
'BK'
);"""
    output = _dci.cmdexec(stmt)
    #
    # Row 12:
    stmt = """Insert Into BTloc4 
Values ('L',
'AL',
'AM', 3050,
'AC',
.12,
'BEAAGAAC', 12000,
'BL'
);"""
    output = _dci.cmdexec(stmt)
    #
    # Row 13:
    stmt = """Insert Into BTloc4 
Values ('M',
'AM',
'AN', 3030,
'AC',
.13,
'BEAAGAAC', 13000,
'BM'
);"""
    output = _dci.cmdexec(stmt)
    #
    # Check values in the primary key.
    stmt = """select varchar13_100
, sdec13_uniq
, char14_20
, varchar15_uniq
from BTloc4 
order by 1 DESC, 2, 3;"""
    output = _dci.cmdexec(stmt)
    #
    # Create View; non-updateable, because of grouping operations.
    # Purpose: (1) test multi-column row value constructor in HAVING.
    #          (2) provide a view whose use tests Grouped Views
    #              for no extra cost of testware development.
    #
    #      Id: RV.072       Row value constructors compared with <> comparison operator.
    #      Id: RV.113       Row value constructor in HAVING clause
    #                          to Create Grouped view.
    #
    # TEMPORARY SELECT TO LOOK AT VALUES FOR GROUP BY ...
    stmt = """select varchar0_4
, varchar5_10
, varchar15_uniq
from BTloc4 
where  (  varchar0_4,'ACAAA' , varchar15_uniq )
<>
( 'CAA' , varchar5_10 , 'EJAAJAA' )
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    stmt = """select varchar0_4
, varchar5_10
, varchar15_uniq , char16_uniq
from BTloc4 
where ubin15_uniq > 1000
group by   varchar0_4
, varchar5_10
, varchar15_uniq , char16_uniq
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    #
    stmt = """create view  VNloc4 as
select varchar0_4
, varchar5_10
, varchar15_uniq , char16_uniq
from BTloc4 
where ubin15_uniq > 1000
group by   varchar0_4
, varchar5_10
, varchar15_uniq , char16_uniq
having
(  varchar0_4,'ACAAA' , varchar15_uniq )
<>
( 'CAA' , varchar5_10 , 'EJAAJAA' )
;"""
    output = _dci.cmdexec(stmt)
    #
    # Check values.
    # Expect 13 rows.
    stmt = """select varchar0_4, VARCHAR5_10
, VARCHAR13_100, SDEC13_UNIQ, CHAR14_20
from BTloc4 
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    stmt = """select varchar0_4, UDEC15_4, VARCHAR15_UNIQ
, UBIN15_UNIQ, CHAR16_UNIQ
from BTloc4 
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    stmt = """select varchar0_4, VARCHAR5_10
, VARCHAR15_UNIQ, CHAR16_UNIQ
from VNloc4 
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    #
    # ==============================
    # BTloc5.
    # ==============================
    stmt = """create table BTloc5(
char2_2             Char(2)               not null,
sbin2_nuniq         Largeint                      ,
sdec2_500           Numeric(9,0) signed   not null,
varchar3_4          VarChar(8)            not null,
sbinneg15_nuniq     Largeint
, primary key ( sdec2_500, varchar3_4 )
)
;"""
    output = _dci.cmdexec(stmt)
    stmt = """create table BTloc5b(
char2_2             Char(2)               not null,
sbin2_nuniq         Largeint                      ,
sdec2_500           Numeric(9,0) signed   not null,
varchar3_4          VarChar(8)            not null,
sbinneg15_nuniq     Largeint
, primary key ( sdec2_500, varchar3_4 )
)
;"""
    output = _dci.cmdexec(stmt)
    stmt = """create table BTloc5c(
char2_2             Char(2)               not null,
sbin2_nuniq         Largeint                      ,
sdec2_500           Numeric(9,0) signed   not null,
varchar3_4          VarChar(8)            not null,
sbinneg15_nuniq     Largeint
, primary key ( sdec2_500, varchar3_4 )
)
;"""
    output = _dci.cmdexec(stmt)
    #
    # Insert before making views.
    #
    stmt = """Insert Into BTloc5 
Values ( 'AA', -3766, -266, 'BA',  -4344);"""
    output = _dci.cmdexec(stmt)
    # To provide duplicate data values, the following row is the same
    # as the above except for an extra character in the varchar value.
    stmt = """Insert Into BTloc5 
Values ( 'AA', -3766, -266,'BAA',  -4344);"""
    output = _dci.cmdexec(stmt)
    stmt = """Insert Into BTloc5 
Values ( 'BA', -772, -272, 'AA',   -3552);"""
    output = _dci.cmdexec(stmt)
    stmt = """Insert Into BTloc5 
Values ( 'BA', -2065, -65, 'CA',   -2389);"""
    output = _dci.cmdexec(stmt)
    stmt = """Insert Into BTloc5 
Values ( 'DA', -2536, -36, 'CA',   -2789);"""
    output = _dci.cmdexec(stmt)
    stmt = """Insert Into BTloc5 
Values ( 'EA', -284, -284, 'DA',   -1950);"""
    output = _dci.cmdexec(stmt)
    #
    # Insert into other tables.
    stmt = """Insert Into BTloc5b 
select * from BTloc5;"""
    output = _dci.cmdexec(stmt)
    stmt = """Insert Into BTloc5c 
select * from BTloc5;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from BTloc5 
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from BTloc5b 
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from BTloc5c 
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    #
    # Create View of some rows and columns; non-updateable because it
    # involves joins (left and right).
    # Expected to return 7 rows:
    #
    # (EXPR)                (EXPR)  (EXPR)  (EXPR)
    # ====================  --====  --====  --======
    #
    #                -4344  AA      BA      BA
    #                -3552  BA      AA      AA
    #                -2789  DA      EA             ?
    #                -2389  BA      AA      AA
    #                    ?       ?  AA      AA
    #                    ?       ?  BA      BA
    #                    ?       ?  DA      DA
    #
    # --- 7 row(s) selected.
    #
    # June 13 '97 -- View fails; commented out.
    # July 18 '97 -- Replaced with work-around to
    # avoid correlation name causing bogus catman error.
    # When correlation name is supported in View, 1113:A17
    # will pass; do not need to restore correlation name
    # into this view here.
    
    stmt = """create view  VNloc5 ( n1, c2, c3, c4 ) as
select  max(BTloc5.sbinneg15_nuniq) , min(BTloc5.char2_2)
, min(BTloc5b.char2_2) , max(BTloc5c.varchar3_4)
from BTloc5 
right join BTloc5b 
on BTloc5.char2_2   = BTloc5b.varchar3_4
left  join BTloc5c 
on BTloc5b.char2_2   = BTloc5c.varchar3_4
group by BTloc5.sbinneg15_nuniq, BTloc5.char2_2,
 BTloc5b.char2_2, BTloc5c.varchar3_4
;"""
    output = _dci.cmdexec(stmt)
    
    # Select of 2 tables making view:
    
    stmt = """select  max(BTloc5.sbinneg15_nuniq) , min(BTloc5.char2_2)
, min(BTloc5b.char2_2)
from BTloc5 
right join BTloc5b 
on BTloc5.char2_2   = BTloc5b.varchar3_4
group by BTloc5.sbinneg15_nuniq, BTloc5.char2_2, BTloc5b.char2_2
order by 1,2,3
;"""
    output = _dci.cmdexec(stmt)
    #
    # Select another combination of 2 tables making view:
    stmt = """select  min(BTloc5b.char2_2) , max(BTloc5c.varchar3_4)
from BTloc5b 
left  join BTloc5c 
on BTloc5b.char2_2   = BTloc5c.varchar3_4
group by BTloc5b.char2_2, BTloc5c.varchar3_4
order by 1,2
;"""
    output = _dci.cmdexec(stmt)
    #
    # Select full query making the view:
    stmt = """select  max(BTloc5.sbinneg15_nuniq) , min(BTloc5.char2_2)
, min(BTloc5b.char2_2) , max(BTloc5c.varchar3_4)
from BTloc5 
right join BTloc5b 
on BTloc5.char2_2   = BTloc5b.varchar3_4
left  join BTloc5c 
on BTloc5b.char2_2   = BTloc5c.varchar3_4
group by BTloc5.sbinneg15_nuniq, BTloc5.char2_2, BTloc5b.char2_2, BTloc5c.varchar3_4
order by 1,2,3
;"""
    output = _dci.cmdexec(stmt)
    #
    stmt = """select     (BTloc5.sbinneg15_nuniq) ,    (BTloc5.char2_2)
,    (BTloc5b.char2_2) ,    (BTloc5c.varchar3_4)
from BTloc5 
right join BTloc5b 
on BTloc5.char2_2   = BTloc5b.varchar3_4
left  join BTloc5c 
on BTloc5b.char2_2   = BTloc5c.varchar3_4
group by BTloc5.sbinneg15_nuniq, BTloc5.char2_2, BTloc5b.char2_2, BTloc5c.varchar3_4
order by 1,2,3
;"""
    output = _dci.cmdexec(stmt)
    #
    # Check values.
    # Expect 7 rows.
    stmt = """select * from VNloc5 
order by 1,2,3;"""
    output = _dci.cmdexec(stmt)
    #
    # ==============================
    # BTloc6.
    # ==============================
    stmt = """create table BTloc6(
sbin0_4             Integer      not null,
varchar0_uniq       VarChar(8)   not null,
sdec0_100           Numeric(9,0) not null,
sdec5_10            Numeric(9,0) signed   not null,
sdec6_4             Numeric(4,0) signed   not null,
sdec9_uniq          Numeric(18,1) signed  not null,
char9_100           Char(2)      not null
, primary key ( sdec9_uniq ASC
, sdec0_100  DESC
, varchar0_uniq ASC )
)
;"""
    output = _dci.cmdexec(stmt)
    #
    # Insert before making views.
    
    stmt = """Insert Into BTloc6 
Values (
-0, 'CJAAAAAC', -81,
-3, -2,
-201.1, 'BX'
);"""
    output = _dci.cmdexec(stmt)
    stmt = """Insert Into BTloc6 
Values (
-1, 'AEAAJAAB', -44,
-0, -2,
-200.2, 'AK'
);"""
    output = _dci.cmdexec(stmt)
    stmt = """Insert Into BTloc6 
Values (
-2, 'CCAAFAAC', -52,
-6, -0,
-101.3, 'CL'
);"""
    output = _dci.cmdexec(stmt)
    stmt = """Insert Into BTloc6 
Values (
-2, 'AIAALAAA', -89,
-2, -1,
-100, 'AM'
);"""
    output = _dci.cmdexec(stmt)
    #
    # Check values in the primary key.
    stmt = """select sdec9_uniq , sdec0_100 , varchar0_uniq
from BTloc6 
order by 1, 2 DESC, 3
;"""
    output = _dci.cmdexec(stmt)
    #
    # Create View of some rows and columns; non-updateable, because of
    # joins.
    # Natural join is equijoin with duplicate column omitted.
    stmt = """select sbin0_4
, sdec5_10
, sdec6_4
, varchar0_uniq
from BTloc6 T1 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    
    # Purpose: Create Global view that contains Natural Join.
    
    stmt = """create view VNloc6 as
select * from
(select sbin0_4 , sdec5_10 , sdec6_4 , varchar0_uniq
from BTloc6 T1 ) t2
natural    join
(select sbin0_4 , sdec5_10 , sdec6_4 , varchar0_uniq
from BTloc6 T3 ) t4
;"""
    output = _dci.cmdexec(stmt)
    
    # Check values.
    # Expect 4 rows.
    stmt = """select * from BTloc6 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from VNloc6 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    #
    # ==============================
    # BTloc7.
    # ==============================
    stmt = """create table BTloc7(
varchar0_nuniq      VarChar(11) ,
char2_2             Char(2)     not null,
char3_4             Char(9)     not null,
sdec9_uniq          Numeric(18,0) signed not null,
char9_100           Char(3)              not null,
ubin9_n4            Numeric(9,0) unsigned
) no partition
;"""
    output = _dci.cmdexec(stmt)
    #
    # Insert before making views.
    #
    stmt = """Insert Into BTloc7 
Values (' LEADING B.', 'BA', 'AAAAAAAA',
3, 'DD', NULL
);"""
    output = _dci.cmdexec(stmt)
    stmt = """Insert Into BTloc7 
Values ('AA' ,         'BA', 'CAAAAAAA',
1, 'BB', NULL
);"""
    output = _dci.cmdexec(stmt)
    stmt = """Insert Into BTloc7 
Values ('ABC' ,        'BE', 'AAAAAAAA',
0, 'AA', NULL
);"""
    output = _dci.cmdexec(stmt)
    stmt = """Insert Into BTloc7 
Values ('TRAILING B ', 'AA', 'DAAAAAAA',
5, 'BF', NULL
);"""
    output = _dci.cmdexec(stmt)
    stmt = """Insert Into BTloc7 
Values ('BA' ,         'AB', 'BAAAAAAA',
4, 'AE', NULL
);"""
    output = _dci.cmdexec(stmt)
    stmt = """Insert Into BTloc7 
Values ('EBAAEAAC   ', 'BA', 'AAAAAAA',
2, 'CC', NULL
);"""
    output = _dci.cmdexec(stmt)
    #
    # Create View; non-updateable, because of string operations.
    # Purpose: (1) test ANSI string features and
    #          (2) provide a view whose use tests string manipulation
    #              for no extra cost of testware development.
    #
    #      Id: AS.001       UPPER, LOWER on varchar columns.
    #      Id: AS.002       Arithmetic on CHAR_LENGTH.
    #      Id: AS.003       Arithmetic on OCTET_LENGTH.
    #      Id: AS.004       POSITION of literal in varchar
    #      Id: AS.005       SUBSTRING in varchar
    #      Id: AS.006       TRIM of Concatenated string literal and varchar
    #      Id: AS.007       Concatenated string literals and chars and varchars
    #
    stmt = """create view  VNloc7 ( cUpper, cLower, cChar_length
, cOctet_length,  cPosition
, cSubstring ,    cTrim
, cConcatChar ,   cConcatVarchar)
as select upper(lower( varchar0_nuniq || varchar0_nuniq ))
, lower(upshift( varchar0_nuniq || varchar0_nuniq ))
, 1 * char_length (char2_2 || char9_100 || varchar0_nuniq )
-- Expect char_length of 5 plus up to 9 for Varchar.
, 1 * octet_length (char2_2 || char9_100 || varchar0_nuniq)
, position  ( ' ' in varchar0_nuniq )
, substring ( varchar0_nuniq from 1 )
, trim ('   trim leading spaces ' || varchar0_nuniq)
, 'start ' || char2_2 || ' end'
, varchar0_nuniq || varchar0_nuniq
from BTloc7 ;"""
    output = _dci.cmdexec(stmt)
    #
    # Check values.
    # Expect 6 rows.
    stmt = """select * from BTloc7 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    stmt = """select upper(lower( varchar0_nuniq ))
, lower(upshift( varchar0_nuniq ))
, 1 * char_length (char2_2 || char9_100 || varchar0_nuniq )
-- Expect char_length of 5 plus up to 9 for Varchar.
, 1 * octet_length (char2_2 || char9_100 || varchar0_nuniq)
, position  ( ' ' in varchar0_nuniq )
, substring ( varchar0_nuniq from 1 )
, trim ('   trim leading spaces ' || varchar0_nuniq)
, 'start ' || char2_2 || ' end'
, varchar0_nuniq || varchar0_nuniq
from BTloc7 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    #
    stmt = """select upper(lower( varchar0_nuniq || varchar0_nuniq ))
, lower(upshift( varchar0_nuniq || varchar0_nuniq ))
, 1 * char_length (char2_2 || char9_100 || varchar0_nuniq )
-- Expect char_length of 5 plus up to 9 for Varchar.
, 1 * octet_length (char2_2 || char9_100 || varchar0_nuniq)
, position  ( ' ' in varchar0_nuniq )
, substring ( varchar0_nuniq from 1 )
, trim ('   trim leading spaces ' || varchar0_nuniq)
, 'start ' || char2_2 || ' end'
, varchar0_nuniq || varchar0_nuniq
from BTloc7 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    #
    stmt = """select * from VNloc7 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    #
    # ==============================
    # BTloc8.
    # ==============================
    stmt = """create table BTloc8(
sbin0_4         Integer not null --   default 3
, varchar0_500  VarChar(11) not null
-- default 'GDAAIAAA'
-- heading 'varchar(11)'
, ubin16_n10    Numeric(4,0) unsigned
, sdec16_uniq   Numeric(18,0) signed not null
, char16_n20    Char(5)
, char17_2      Char(8)  not null
) no partition
;"""
    output = _dci.cmdexec(stmt)
    #
    # Insert before making views.
    # Note that the '%' and '_' characters are used by the LIKE/ESCAPE test.
    #
    stmt = """Insert Into BTloc8 
Values ( 1, 'ACAABAAA', 3, 1993, 'BDAA ', 'AAAAAAAA');"""
    output = _dci.cmdexec(stmt)
    stmt = """Insert Into BTloc8 
Values ( 1, 'BBA%FAAA', 3, 3293, 'BD   ', 'BAAAAAAA');"""
    output = _dci.cmdexec(stmt)
    stmt = """Insert Into BTloc8 
Values ( 3, 'CAAAGAAA', 1, 4151, 'BB   ', 'BAAAAAAA');"""
    output = _dci.cmdexec(stmt)
    stmt = """Insert Into BTloc8 
Values ( 1, 'BBAABA_A', 1, 3917, 'BBAA ', 'BAAAAAAA');"""
    output = _dci.cmdexec(stmt)
    stmt = """Insert Into BTloc8 
Values ( 1, 'BBAADAAA', 7, 2701, 'BCAA ', 'AAAAAAAA');"""
    output = _dci.cmdexec(stmt)
    stmt = """Insert Into BTloc8 
Values ( 0, 'BDAAAAAA', 8, 2028, 'AD   ', 'AAAAAAAA');"""
    output = _dci.cmdexec(stmt)
    #
    # Check portions to compose view:
    stmt = """select sbin0_4, varchar0_500
, ubin16_n10, sdec16_uniq, char16_n20
, char17_2
from BTloc8 where sdec16_uniq > 3000
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    #
    stmt = """select sbin0_4, varchar0_500
, ubin16_n10, sdec16_uniq, char16_n20
, char17_2
from BTloc8 where sdec16_uniq < 2500
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    #
    # View gets all columns, omitting only the row where
    # sdec16_uniq is between 2500 and 3000;
    #
    stmt = """create view  VNloc8 
(sbin0_4
, varchar0_500
, ubin16_n10
, sdec16_uniq
, char16_n20
, char17_2
)
as  select *
from BTloc8 where sdec16_uniq > 3000
union -- CORRESPONDING -- Not in first release
select *
from BTloc8 where sdec16_uniq < 2500
;"""
    output = _dci.cmdexec(stmt)
    #
    # Check values.
    # Expect 6 rows from table and 5 rows from view.
    stmt = """select * from BTloc8 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from VNloc8 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    #
    # ==============================
    # BTloc9.
    # ==============================
    
    stmt = """create table BTloc9(
rownum   integer not null
, vc49n    varchar(49) not null
, iyear    interval year to month
, iday     interval day to second not null
, sint      smallint
, primary key (vc49n, rownum)
)
;"""
    output = _dci.cmdexec(stmt)
    
    # Insert 14 rows
    stmt = """insert into BTloc9 values (
1
, 'This is a 49 character varchar field bbbbbbbbbbbb'
, interval '0-1' year to month
, interval '00:00:00:00.000001' day to second(6)
, -32768
);"""
    output = _dci.cmdexec(stmt)
    # A970718. Regression (as reported by Anu) of -8817 error fetching from TCB tree.
    stmt = """insert into BTloc9 values (
2
, 'This is a 49 character varchar field bbbbbbbbbbbb'
, interval '1-08' year to month
, interval '00:00:00:00.0001' day to second(4)
, 32767
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into BTloc9 values (
5
, 'This is a 49 character varchar field cccccccccccc'
, interval '1-1' year to month
, interval '00:00:00:00.000001' day to second(6)
, -32768
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into BTloc9 values (
7
, 'This is a 49 character varchar field cccccccccccc'
, interval '1-08' year to month
, interval '00:00:00:00.0001' day to second(4)
, -32768
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into BTloc9 values (
9
, 'This is a 49 character varchar field bbbbbbbbbbbb'
, interval '0-1' year to month
, interval '00:00:00:00.000001' day to second(6)
, -32768
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into BTloc9 values (
10
, 'This is a 49 character varchar field cccccccccccc'
, interval '0-1' year to month
, interval '00:00:00:00.000001' day to second(6)
, -32767
);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into BTloc9 values (
11
, 'This is a 49 character varchar field bbbbbbbbbbbb'
, interval '99-11' year to month
, interval '99:23:59:59.999999' day to second(6)
, -32767
);"""
    output = _dci.cmdexec(stmt)
    #
    # Create View of some rows and columns; non-updateable because it's
    # a CASE; involves columns from a discontiguous-column index.
    #
    #      Id: CA.002a      CASE in Select list for global view -- Simple CASE
    #      Id: CA.002b      CASE in Select list for global view -- Searched CASE
    #
    #
    # First look at data:
    #
    # (1) Check values in the primary key
    #
    stmt = """select vc49n, rownum, sint from BTloc9 
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    #
    # (2) Check values in CASE statements.
    #
    # (2a)  Simple CASE in SELECT list:
    stmt = """select
CASE rownum WHEN 1 THEN 'Value A'
WHEN 2 THEN 'Value B'
WHEN 3 THEN 'Value C'
ELSE 'Value D -- Rowcount > 3'
END
from BTloc9 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    #
    # (2b) Searched CASE or 'CASE with searched conditions'
    #     in SELECT list.
    # Allows multiple conditions to be evaluated in a single query.
    #       SYNTAX: <case specification> ::= <searched case> ::=
    #                   CASE
    #                        WHEN <search condition> THEN
    #                       [  <result expression> | NULL ]
    #                        ...
    #                      [ ELSE <result> ]
    #                   END
    stmt = """select
CASE when rownum > 10 then 'rownum over 10'
when sint  = -32768 then 'sint is the lowest'
else 'the great unknown'
END
from BTloc9 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    #
    # (2c) Searched CASE or 'CASE with searched conditions'
    #     in predicate.
    stmt = """select rownum from BTloc9 
where rownum < CASE
when rownum between 7 and 12   then 2222
when rownum between 1 and 2   then rownum+1
else rownum
end
order by 1
;"""
    output = _dci.cmdexec(stmt)
    
    # June 13 '97 -- Create commented out temporarily.
    # Sept 22 '97 Restored
    
    stmt = """create view VNloc9 (csimple, csearched) as select
CASE rownum WHEN 1 THEN 'Value A'
WHEN 2 THEN 'Value B'
WHEN 3 THEN 'Value C'
ELSE 'Value D -- Rowcount > 3'
END
,   CASE when rownum > 10 then 'rownum over 10'
when sint  = -32768 then 'sint is the lowest'
else 'the great unknown'
END
from BTloc9 
where rownum < CASE
when rownum between 7 and 12   then 2222
when rownum between 1 and 2   then rownum+1
else rownum
end
;"""
    output = _dci.cmdexec(stmt)
    
    # Check values.
    # Expect 7 rows in table and 6 in view.
    
    stmt = """select * from BTloc9 order by 1,2;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from VNloc9 order by 1,2;"""
    output = _dci.cmdexec(stmt)
    _testmgr.testcase_end(desc)

