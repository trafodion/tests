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

import qa04s1
import qa04s2
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
    #  Test case name:         A07
    #  Description:            This test unit tests SQLCI explain
    #                          for simple selects, select with subquery,
    #                          union, inner and outer joins.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:        (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """create table exptab (
char0_20        character(8)  not null,
sbin0_2         numeric(18) signed not null,
udec0_10        decimal(9) unsigned not null,
varchar0_2      varchar(16) not null,
sdec0_1000      pic s9(9)   not null,
ubin0_20        pic 9(7)v9(2) comp not null,
char1_2         character(16) not null,
sdec1_uniq      decimal(18) signed not null,
sbin1_100       numeric(4) signed not null,
varchar1_uniq   varchar(8) not null,
primary key (sdec0_1000 ASC ) )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Insert some values
    
    stmt = """INSERT INTO exptab VALUES
(
'AAAAAAAA',
1,
2,
'BBBBBBBBB',
3,
4,
'CACACA',
5,
6,
'CACAC');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from exptab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    
    stmt = """create table btun(
varchar0_1000        varchar(1000)  not null
, char0_10           char(32)       not null
, udec0_20           decimal(9) UNSIGNED  not null
, ubin0_1000         pic 9(7)v9(2) comp not null
, sdec0_uniq         pic s9(9)     not null
, varchar1_uniq      varchar(18)   not null
, sbin1_uniq         numeric(4) signed not null
, sdec1_2            decimal(18) signed not null
, varchar2_uniq      varchar(64)        not null
, primary key (varchar2_uniq ASC ) )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #insert some values
    stmt = """INSERT INTO btun VALUES
(
'hello',
'there',
1,
2,
3,
'BBBB',
4,
5,
'EFFF' );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from btun;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    
    stmt = """create index btuna on btun( varchar2_uniq asc );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #catalog
    
    stmt = """create unique index btunb on btun( varchar2_uniq ASC );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #catalog
    
    stmt = """create index btunc on btun( varchar2_uniq desc);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #catalog
    
    stmt = """create unique index btund on btun( varchar2_uniq asc );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #catalog
    
    stmt = """create view  btunv1 
( varchar0_1000
, char0_10
, udec0_20
, ubin0_1000
, sdec0_uniq
, varchar1_uniq
, sbin1_uniq
, sdec1_2
, varchar2_uniq )
AS SELECT
varchar0_1000
, char0_10
, udec0_20
, ubin0_1000
, sdec0_uniq
, varchar1_uniq
, sbin1_uniq
, sdec1_2
, varchar2_uniq
FROM btun UNION SELECT
varchar0_1000
, char0_10
, udec0_20
, ubin0_1000
, sdec0_uniq
, varchar1_uniq
, sbin1_uniq
, sdec1_2
, varchar2_uniq
FROM btun 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view btunv2 as select
ubin0_1000
, sdec0_uniq
, varchar1_uniq
from btun 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update statistics for table btun on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update statistics for table exptab on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """prepare p1 from
select sdec1_uniq, sdec0_1000
from exptab where sdec1_uniq IN
(
( select sdec0_1000
from exptab where sdec0_1000 < 2
)
UNION
(select sdec0_1000
from exptab  where sdec0_1000 > 997
)
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # Explain a union with a subquery and an outer join
    
    stmt = """prepare p2 from
select sdec1_uniq, sdec0_1000
from exptab where sdec1_uniq IN
(
( select sdec0_1000
from exptab left join """ + gvars.g_schema_arkcasedb + """.ORDERS on sdec0_1000 < 2
)
UNION
(select sdec0_1000
from exptab  where sdec0_1000 > 997
)
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute p2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # explain a select, predicate on key
    
    stmt = """prepare p3 from
select varchar2_uniq, sdec1_2 from btun 
where varchar2_uniq = 'CAAAAAAAA' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute p3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # explain a select with a subquery and union
    
    stmt = """prepare p4 from
select sdec1_uniq, sdec0_1000
from exptab where sdec1_uniq IN
(
( select sdec0_1000
from exptab where sdec0_1000 < 2
)
UNION
(select sdec0_1000
from exptab  where sdec0_1000 > 997
)
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute p4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # Explain a select/join/ order by on key
    
    stmt = """prepare p5 from
SELECT udec0_10, udec0_20, ubin0_20 FROM   btun 
LEFT JOIN exptab ON
 btun.varchar2_uniq = 'CAA' AND exptab.sdec0_1000 > 10 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute p5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s12')
    
    # Explain a 3 way union with an order by
    
    stmt = """prepare p6 from
SELECT udec0_10, ubin0_20, varchar1_uniq
FROM   exptab 
WHERE sdec0_1000 < 50
UNION ALL
(SELECT udec0_20, ubin0_1000, varchar1_uniq
FROM btun 
WHERE varchar1_uniq = 'CAA'
UNION
SELECT udec0_10, ubin0_20, varchar1_uniq
FROM   exptab 
WHERE sdec0_1000 < 50
) ORDER BY 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute p6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s14')
    
    stmt = """prepare p7 from
SELECT udec0_10, ubin0_20, varchar1_uniq
FROM   exptab 
WHERE sdec0_1000 < 50
UNION ALL
(SELECT udec0_20, ubin0_1000, varchar1_uniq
FROM btun 
WHERE varchar1_uniq ='CAA'
UNION
SELECT udec0_10, ubin0_20, varchar1_uniq
FROM   exptab 
WHERE sdec0_1000 < 50
)
UNION ALL
SELECT udec0_10, ubin0_20, varchar1_uniq
FROM   exptab 
WHERE sdec0_1000 < 50
UNION ALL
SELECT udec0_20, ubin0_1000, varchar1_uniq
FROM btun 
WHERE varchar1_uniq = 'CAA' ORDER BY 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute p7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s16')
    
    stmt = """prepare p8 from
SELECT varchar2_uniq FROM btunv1 UNION
SELECT varchar2_uniq FROM btun;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute p8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s18')
    
    stmt = """prepare p9 from
SELECT * FROM btunv1 LEFT JOIN btunv2 ON
 btunv1.varchar2_uniq = btunv2.varchar1_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute p9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s20')
    
    # cleanup
    
    stmt = """DROP index btuna;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP index btunb;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP index btunc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP index btund;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP VIEW  btunv1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP VIEW  btunv2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP table btun;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP table exptab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test002(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:         A03
    #  Description:            IS NULL key predicate
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:        (provide a high-level description)
    #
    #  Notes:
    #
    # =================== End Test Case Header  ===================
    
    stmt = """create table tab1 
(a  varchar(3) default 'abc',
b  varchar(3) upshift default 'DEF',
c  char(3) default 'ghi',
d  date,
e  int default 9) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index itvar on tab1 (a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index itup  on tab1 (b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index itchar on tab1 (c);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index itdate on tab1 (d);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into tab1 values ('ab','ab','ab',date '1992-01-01' ,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab1 values ('abc','abc','abc',date '1993-01-01' , 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab1 values (null, null,null,null,10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tab1 values (null, null,null,null,20);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update statistics for table tab1 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # To force the use of the index
    # control query interactive access on;
    
    # Test generation of IS NULL key predicate on varchar column
    stmt = """prepare s1 from
select * from tab1 where a is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #  Used to generate SQL error -7004
    
    # explain s1;
    
    #  Should use index ITVAR
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    # Should return 2 rows
    
    # Testing the OR-optimization case
    stmt = """prepare s2 from
select * from tab1 where a is null or a = 'ab';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #  Used to generate SQL Error -7004
    
    # explain s2;
    
    #  Should use OR-optimization with index ITVAR
    stmt = """execute s2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s4')
    # Should return 3 rows
    
    # Testing the NOT IS NULL predicate.  Should not be key predicate.
    stmt = """prepare s3 from
select * from tab1 where a is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # explain s3;
    
    #  Should perform table scan.  No key predicate.
    stmt = """execute s3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s6')
    # Should return 2 rows.
    
    # Testing key predicates for join
    stmt = """prepare s4 from
select * from tab1 t1,
 tab1 t2 where t1.a = t2.a and t1.a is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #  Used to generate SQL Error -7004
    
    # explain s4;
    
    # Should build a ISNULL key predicate for index ITVAR
    
    stmt = """execute s4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    # Should return 0 rows
    
    # Test COL IS NULL key predicate on VARCHAR UPSHIFT column
    stmt = """prepare s5 from
select * from tab1 t1 where b is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #  Used to generate SQL Error -7004
    #
    # explain s5;
    
    #  Should build IS NULL key predicates for index ITUP
    stmt = """execute s5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s9')
    # Should return 2 rows
    
    # Test COL IS NULL key predicate on CHAR column
    stmt = """prepare s6 from
select * from tab1 t1 where c is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #
    # explain s6;
    
    #  Should build IS NULL key predicate for index ICHAR
    stmt = """execute s6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s11')
    # Should return 2 rows
    
    # Test COL IS NULL key predicate on DATETIME column
    stmt = """prepare s7 from
select * from tab1 t1 where d is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # explain s7;
    
    #  Should build IS NULL key predicate for index IDATE
    stmt = """execute s7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s13')
    # Should return 2 rows
    
    stmt = """drop table tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test003(desc="""a04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:         A04
    #  Description:            Test WHERE clause with many predicates
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:        (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """CREATE TABLE s0804ta 
(
SDNO1    PIC X(2) NOT NULL ,
SDNO2    PIC X(4) NOT NULL ,
CAS      PIC X(1) NOT NULL ,
KDATE    PIC X(8) NOT NULL ,
KTIME    PIC X(8) NOT NULL ,
CFDAY    PIC X(1) NOT NULL ,
CFTM1    PIC X(4) NOT NULL ,
CFTM2    PIC X(7) NOT NULL ,
CFTM3    PIC X(4) NOT NULL ,
ORN      PIC X(10) NOT NULL ,
PN       PIC X(7) NOT NULL ,
RDGT     PIC X(24) NOT NULL ,
SPN      PIC X(15) NOT NULL ,
CCS      PIC X(1) NOT NULL ,
CID      PIC X(3) NOT NULL ,
CLN      PIC X(16) NOT NULL ,
CLT      PIC X(1) NOT NULL ,
CN       PIC X(1) NOT NULL ,
CN0      PIC X(4) NOT NULL ,
CN1      PIC X(4) NOT NULL ,
ISRTA    PIC X(4) NOT NULL ,
NNP      PIC X(1) NOT NULL ,
ORC      PIC X(2) NOT NULL ,
OSC      PIC X(1) NOT NULL ,
OSRTA    PIC X(4) NOT NULL ,
PFXC     PIC X(5) NOT NULL ,
RDC      PIC X(2) NOT NULL ,
SCS      PIC X(1) NOT NULL ,
SPC      PIC X(2) NOT NULL ,
SSC      PIC X(1) NOT NULL ,
TN0      PIC X(7) NOT NULL ,
TN1      PIC X(7) NOT NULL ,
ANDAY    PIC X(1) NOT NULL ,
ANTM     PIC X(15) NOT NULL ,
CBTM     PIC X(15) NOT NULL ,
CCLS     PIC X(1) NOT NULL ,
CGF      PIC X(1) NOT NULL ,
CHGC     PIC 9(8) NOT NULL ,
CHK      PIC X(2) NOT NULL ,
CLR1     PIC X(1) NOT NULL ,
CLR2     PIC X(3) NOT NULL ,
CPI      PIC X(2) NOT NULL ,
DCC      PIC X(1) NOT NULL ,
FLT      PIC X(1) NOT NULL ,
FSC      PIC X(1) NOT NULL ,
GW       PIC X(1) NOT NULL ,
ICI      PIC X(1) NOT NULL ,
IDSTA    PIC X(3) NOT NULL ,
IDSTN    PIC X(3) NOT NULL ,
IO       PIC X(1) NOT NULL ,
IRTA     PIC X(3) NOT NULL ,
ISG      PIC X(1) NOT NULL ,
ISRTN    PIC X(3) NOT NULL ,
ISTN     PIC X(2) NOT NULL ,
MA       PIC X(5) NOT NULL ,
ODSTA    PIC X(3) NOT NULL ,
ODSTN    PIC X(3) NOT NULL ,
OGTM     PIC X(15) NOT NULL ,
ORTA     PIC X(3) NOT NULL ,
ORDAY    PIC X(1) NOT NULL ,
ORTM     PIC X(15) NOT NULL ,
OSG      PIC X(1) NOT NULL ,
OSTN     PIC X(2) NOT NULL ,
RAI      PIC X(1) NOT NULL ,
SUB      PIC X(1) NOT NULL ,
TMR      PIC X(1) NOT NULL ,
UUIR     PIC 9(2) NOT NULL ,
UUIS     PIC 9(2) NOT NULL ,
VD       PIC X(1) NOT NULL ,
VDT      PIC X(1) NOT NULL ,
VRTA     PIC X(3) NOT NULL
) no partition
ATTRIBUTE
--    BLOCKSIZE 4096,
NO CLEARONPURGE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #    NO BUFFERED;
    
    stmt = """CREATE INDEX s0804tax ON s0804ta  ( CFTM1,
CFTM2,
CFTM3,
ORN,
SPN,
RDGT,
PN,
SDNO2,
SDNO1
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE INDEX s0804tay ON s0804ta  ( CAS,
KDATE,
KTIME );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # reset param *;
    
    #  set param ?CFTMLOW1    'a';
    #  set param ?CFTMLOW2    'b';
    #  set param ?CFTMLOW3  'c';
    #  set param ?CFTMHIGH1   'd';
    #  set param ?CFTMHIGH2   'e';
    #  set param ?CFTMHIGH3 'f';
    #  set param ?SDNO1LOW11  'a';
    #  set param ?SDNO1LOW12  'b';
    #  set param ?SDNO1HIGH11 'd';
    #  set param ?SDNO1HIGH12 'e';
    #  set param ?SDNO2LOW11  'a';
    #  set param ?SDNO2LOW12  'b';
    #  set param ?SDNO2HIGH11 'd';
    #  set param ?SDNO2HIGH12 'e';
    #  set param                    ?CFDAYLOW  '%x';
    #  set param                    ?ORNLOW    '%x';
    #  set param                    ?PNLOW     '%x';
    #  set param                    ?RDGTLOW   '%x';
    #  set param                    ?SPNLOW    '%x';
    #  set param                    ?CCSLOW    '%x';
    #  set param                    ?CIDLOW    '%x';
    #  set param                    ?CLNLOW    '%x';
    #  set param                    ?CLTLOW    '%x';
    #  set param                    ?CNLOW     '%x';
    #  set param                    ?CN0LOW    '%x';
    #  set param                    ?CN1LOW    '%x';
    #  set param                    ?ISRTALOW  '%x';
    #  set param                    ?OSRTALOW  '%x';
    #  set param                    ?NNPLOW    '%x';
    #  set param                    ?ORCLOW    '%x';
    #  set param                    ?OSCLOW    '%x';
    #  set param                    ?PFXCLOW   '%x';
    #  set param                    ?RDCLOW    '%x';
    #  set param                    ?SCSLOW    '%x';
    #  set param                    ?SPCLOW    '%x';
    #  set param                    ?SSCLOW    '%x';
    #  set param                    ?TN0LOW    '%x';
    #  set param                    ?TN1LOW    '%x';
    #  set param                    ?ANDAYLOW  '%x';
    #  set param                    ?ANTMLOW   '%x';
    #  set param                    ?CBTMLOW   '%x';
    #  set param                    ?CCLSLOW   '%x';
    #  set param                    ?CGFLOW    '%x';
    #==set param                    ?CHGCLOW   '%x';
    #  set param                    ?CHKLOW    '%x';
    #  set param                    ?CLR1LOW   '%x';
    #  set param                    ?CLR2LOW   '%x';
    #  set param                    ?CPILOW    '%x';
    #  set param                    ?DCCLOW    '%x';
    #  set param                    ?FLTLOW    '%x';
    #  set param                    ?FSCLOW    '%x';
    #  set param                    ?GWLOW     '%x';
    #  set param                    ?ICILOW    '%x';
    #  set param                    ?IDSTALOW  '%x';
    #  set param                    ?IDSTNLOW  '%x';
    #  set param                    ?IOLOW     '%x';
    #  set param                    ?IRTALOW   '%x';
    #  set param                    ?ISGLOW    '%x';
    #  set param                    ?ISRTNLOW  '%x';
    #  set param                    ?ISTNLOW   '%x';
    #  set param                    ?MALOW     '%x';
    #  set param                    ?ODSTALOW  '%x';
    #  set param                    ?ODSTNLOW  '%x';
    #  set param                    ?OGTMLOW   '%x';
    #  set param                    ?ORTALOW   '%x';
    #  set param                    ?ORDAYLOW  '%x';
    #  set param                    ?ORTMLOW   '%x';
    #  set param                    ?OSGLOW    '%x';
    #  set param                    ?OSTNLOW   '%x';
    #  set param                    ?RAILOW    '%x';
    #  set param                    ?SUBLOW    '%x';
    #  set param                    ?TMRLOW    '%x';
    #==set param                    ?UUIRLOW   '%x';
    #==set param                    ?UUISLOW   '%x';
    #  set param                    ?VDLOW     '%x';
    #  set param                    ?VDTLOW    '%x';
    #  set param                    ?VRTALOW   '%x';
    
    #  Without the fix:  The following PREPARE fails with a       (BAD)
    #                      trap in SQLCOMP.
    #  With the fix:     PREPARE completes successfully           (GOOD)
    
    qa04s1._init(_testmgr)
    
    #$SQL_prepared_msg
    #prepare s1 from
    #               SDNO2   ,
    #               CFDAY   ,
    #               CFTM1   ,
    #               CFTM2   ,
    #               CFTM3   ,
    #               ORN     ,
    #               PN      ,
    #               RDGT    ,
    #               SPN     ,
    #               CCS     ,
    #               CID     ,
    #               CLN     ,
    #               CLT     ,
    #               CN      ,
    #               CN0     ,
    #               CN1     ,
    #               ISRTA   ,
    #               NNP     ,
    #               ORC     ,
    #               OSC     ,
    #               OSRTA   ,
    #               PFXC    ,
    #               RDC     ,
    #               SCS     ,
    #               SPC     ,
    #               SSC     ,
    #               TN0     ,
    #               TN1     ,
    #               ANDAY   ,
    #               ANTM    ,
    #               CBTM    ,
    #               CCLS    ,
    #               CGF     ,
    #               CHGC    ,
    #               CHK     ,
    #               CLR1    ,
    #               CLR2    ,
    #               CPI     ,
    #               DCC     ,
    #               FLT     ,
    #               FSC     ,
    #               GW      ,
    #               ICI     ,
    #               IDSTA   ,
    #               IDSTN   ,
    #               IO      ,
    #               IRTA    ,
    #               ISG     ,
    #               ISRTN   ,
    #               ISTN    ,
    #               MA      ,
    #               ODSTA   ,
    #               ODSTN   ,
    #               OGTM   ,
    #               ORTA    ,
    #               ORDAY   ,
    #               ORTM    ,
    #               OSG     ,
    #               OSTN    ,
    #               RAI     ,
    #               SUB     ,
    #               TMR     ,
    #               UUIR    ,
    #               UUIS    ,
    #               VD      ,
    #               VDT     ,
    #               VRTA
    #       FROM   s0804ta
    #       WHERE  (CFTM1,CFTM2,CFTM3)
    #                        BETWEEN (?CFTMLOW1,?CFTMLOW2,?CFTMLOW3)    AND
    #                                (?CFTMHIGH1,?CFTMHIGH2,?CFTMHIGH3) AND
    #             ((SDNO1,SDNO2)
    #                      BETWEEN (?SDNO1LOW11,?SDNO2LOW12)
    #                                            AND (?SDNO1HIGH11,?SDNO2HIGH12)
    #                                                               AND
    #               CFDAY  LIKE     ?CFDAYLOW                     AND
    #               ORN    LIKE     ?ORNLOW                       AND
    #               PN     LIKE     ?PNLOW                        AND
    #               RDGT   LIKE     ?RDGTLOW                      AND
    #               SPN    LIKE     ?SPNLOW                       AND
    #               CCS    LIKE     ?CCSLOW                       AND
    #               CID    LIKE     ?CIDLOW                       AND
    #               CLN    LIKE     ?CLNLOW                       AND
    #               CLT    LIKE     ?CLTLOW                       AND
    #               CN     LIKE     ?CNLOW                        AND
    #              (CN0    LIKE     ?CN0LOW                       OR
    #               CN1    LIKE     ?CN1LOW)                      AND
    #              (ISRTA  LIKE     ?ISRTALOW                     OR
    #               OSRTA  LIKE     ?OSRTALOW)                    AND
    #               NNP    LIKE     ?NNPLOW                       AND
    #               ORC    LIKE     ?ORCLOW                       AND
    #               OSC    LIKE     ?OSCLOW                       AND
    #               PFXC   LIKE     ?PFXCLOW                      AND
    #               RDC    LIKE     ?RDCLOW                       AND
    #               SCS    LIKE     ?SCSLOW                       AND
    #               SPC    LIKE     ?SPCLOW                       AND
    #               SSC    LIKE     ?SSCLOW                       AND
    #              (TN0    LIKE     ?TN0LOW                       OR
    #               TN1    LIKE     ?TN1LOW)                      AND
    #               ANDAY  LIKE     ?ANDAYLOW                     AND
    #               ANTM   LIKE     ?ANTMLOW                      AND
    #               CBTM   LIKE     ?CBTMLOW                      AND
    #               CCLS   LIKE     ?CCLSLOW                      AND
    #               CGF    LIKE     ?CGFLOW                       AND
    #==             CHGC   LIKE     ?CHGCLOW                      AND
    #               CHK    LIKE     ?CHKLOW                       AND
    #               CLR1   LIKE     ?CLR1LOW                      AND
    #               CLR2   LIKE     ?CLR2LOW                      AND
    #               CPI    LIKE     ?CPILOW                       AND
    #               DCC    LIKE     ?DCCLOW                       AND
    #               FLT    LIKE     ?FLTLOW                       AND
    #               FSC    LIKE     ?FSCLOW                       AND
    #               GW     LIKE     ?GWLOW                        AND
    #               ICI    LIKE     ?ICILOW                       AND
    #               IDSTA  LIKE     ?IDSTALOW                     AND
    #               IDSTN  LIKE     ?IDSTNLOW                     AND
    #               IO     LIKE     ?IOLOW                        AND
    #               IRTA   LIKE     ?IRTALOW                      AND
    #               ISG    LIKE     ?ISGLOW                       AND
    #               ISRTN  LIKE     ?ISRTNLOW                     AND
    #               ISTN   LIKE     ?ISTNLOW                      AND
    #               MA     LIKE     ?MALOW                        AND
    #               ODSTA  LIKE     ?ODSTALOW                     AND
    #               ODSTN  LIKE     ?ODSTNLOW                     AND
    #               OGTM   LIKE     ?OGTMLOW                      AND
    #               ORTA   LIKE     ?ORTALOW                      AND
    #               ORDAY  LIKE     ?ORDAYLOW                     AND
    #               ORTM   LIKE     ?ORTMLOW                      AND
    #               OSG    LIKE     ?OSGLOW                       AND
    #               OSTN   LIKE     ?OSTNLOW                      AND
    #               RAI    LIKE     ?RAILOW                       AND
    #               SUB    LIKE     ?SUBLOW                       AND
    #               TMR    LIKE     ?TMRLOW                       AND
    #==             UUIR   LIKE     ?UUIRLOW                      AND
    #==             UUIS   LIKE     ?UUISLOW                      AND
    #               VD     LIKE     ?VDLOW                        AND
    #               VDT    LIKE     ?VDTLOW                       AND
    #               VRTA   LIKE     ?VRTALOW)                     OR
    #==
    #             ((SDNO1,SDNO2)
    #                      BETWEEN (?SDNO1LOW11,?SDNO2LOW12)
    #                                            AND (?SDNO1HIGH11,?SDNO2HIGH12)
    #                                                               AND
    #               CFDAY  LIKE     ?CFDAYLOW                     AND
    #               ORN    LIKE     ?ORNLOW                       AND
    #               PN     LIKE     ?PNLOW                        AND
    #               RDGT   LIKE     ?RDGTLOW                      AND
    #               SPN    LIKE     ?SPNLOW                       AND
    #               CCS    LIKE     ?CCSLOW                       AND
    #               CID    LIKE     ?CIDLOW                       AND
    #               CLN    LIKE     ?CLNLOW                       AND
    #               CLT    LIKE     ?CLTLOW                       AND
    #               CN     LIKE     ?CNLOW                        AND
    #              (CN0    LIKE     ?CN0LOW                       OR
    #               CN1    LIKE     ?CN1LOW)                      AND
    #              (ISRTA  LIKE     ?ISRTALOW                     OR
    #               OSRTA  LIKE     ?OSRTALOW)                    AND
    #               NNP    LIKE     ?NNPLOW                       AND
    #               ORC    LIKE     ?ORCLOW                       AND
    #               OSC    LIKE     ?OSCLOW                       AND
    #               PFXC   LIKE     ?PFXCLOW                      AND
    #               RDC    LIKE     ?RDCLOW                       AND
    #               SCS    LIKE     ?SCSLOW                       AND
    #               SPC    LIKE     ?SPCLOW                       AND
    #               SSC    LIKE     ?SSCLOW                       AND
    #              (TN0    LIKE     ?TN0LOW                       OR
    #               TN1    LIKE     ?TN1LOW)                      AND
    #               ANDAY  LIKE     ?ANDAYLOW                     AND
    #               ANTM   LIKE     ?ANTMLOW                      AND
    #               CBTM   LIKE     ?CBTMLOW                      AND
    #               CCLS   LIKE     ?CCLSLOW                      AND
    #               CGF    LIKE     ?CGFLOW                       AND
    #==             CHGC   LIKE     ?CHGCLOW                      AND
    #               CHK    LIKE     ?CHKLOW                       AND
    #               CLR1   LIKE     ?CLR1LOW                      AND
    #               CLR2   LIKE     ?CLR2LOW                      AND
    #               CPI    LIKE     ?CPILOW                       AND
    #               DCC    LIKE     ?DCCLOW                       AND
    #               FLT    LIKE     ?FLTLOW                       AND
    #               FSC    LIKE     ?FSCLOW                       AND
    #               GW     LIKE     ?GWLOW                        AND
    #               ICI    LIKE     ?ICILOW                       AND
    #               IDSTA  LIKE     ?IDSTALOW                     AND
    #               IDSTN  LIKE     ?IDSTNLOW                     AND
    #               IO     LIKE     ?IOLOW                        AND
    #               IRTA   LIKE     ?IRTALOW                      AND
    #               ISG    LIKE     ?ISGLOW                       AND
    #               ISRTN  LIKE     ?ISRTNLOW                     AND
    #               ISTN   LIKE     ?ISTNLOW                      AND
    #               MA     LIKE     ?MALOW                        AND
    #               ODSTA  LIKE     ?ODSTALOW                     AND
    #               ODSTN  LIKE     ?ODSTNLOW                     AND
    #               OGTM   LIKE     ?OGTMLOW                      AND
    #               ORTA   LIKE     ?ORTALOW                      AND
    #               ORDAY  LIKE     ?ORDAYLOW                     AND
    #               ORTM   LIKE     ?ORTMLOW                      AND
    #               OSG    LIKE     ?OSGLOW                       AND
    #               OSTN   LIKE     ?OSTNLOW                      AND
    #               RAI    LIKE     ?RAILOW                       AND
    #               SUB    LIKE     ?SUBLOW                       AND
    #               TMR    LIKE     ?TMRLOW                       AND
    #==             UUIR   LIKE     ?UUIRLOW                      AND
    #==             UUIS   LIKE     ?UUISLOW                      AND
    #               VD     LIKE     ?VDLOW                        AND
    #               VDT    LIKE     ?VDTLOW                       AND
    #               VRTA   LIKE     ?VRTALOW)                     OR
    #==
    #             ((SDNO1,SDNO2)
    #                      BETWEEN (?SDNO1LOW11,?SDNO2LOW12)
    #                                            AND (?SDNO1HIGH11,?SDNO2HIGH12)
    #                                                               AND
    #               CFDAY  LIKE     ?CFDAYLOW                     AND
    #               ORN    LIKE     ?ORNLOW                       AND
    #               PN     LIKE     ?PNLOW                        AND
    #               RDGT   LIKE     ?RDGTLOW                      AND
    #               SPN    LIKE     ?SPNLOW                       AND
    #               CCS    LIKE     ?CCSLOW                       AND
    #               CID    LIKE     ?CIDLOW                       AND
    #               CLN    LIKE     ?CLNLOW                       AND
    #               CLT    LIKE     ?CLTLOW                       AND
    #               CN     LIKE     ?CNLOW                        AND
    #              (CN0    LIKE     ?CN0LOW                       OR
    #               CN1    LIKE     ?CN1LOW)                      AND
    #              (ISRTA  LIKE     ?ISRTALOW                     OR
    #               OSRTA  LIKE     ?OSRTALOW)                    AND
    #               NNP    LIKE     ?NNPLOW                       AND
    #               ORC    LIKE     ?ORCLOW                       AND
    #               OSC    LIKE     ?OSCLOW                       AND
    #               PFXC   LIKE     ?PFXCLOW                      AND
    #               RDC    LIKE     ?RDCLOW                       AND
    #               SCS    LIKE     ?SCSLOW                       AND
    #               SPC    LIKE     ?SPCLOW                       AND
    #               SSC    LIKE     ?SSCLOW                       AND
    #              (TN0    LIKE     ?TN0LOW                       OR
    #               TN1    LIKE     ?TN1LOW)                      AND
    #               ANDAY  LIKE     ?ANDAYLOW                     AND
    #               ANTM   LIKE     ?ANTMLOW                      AND
    #               CBTM   LIKE     ?CBTMLOW                      AND
    #               CCLS   LIKE     ?CCLSLOW                      AND
    #               CGF    LIKE     ?CGFLOW                       AND
    #==             CHGC   LIKE     ?CHGCLOW                      AND
    #               CHK    LIKE     ?CHKLOW                       AND
    #               CLR1   LIKE     ?CLR1LOW                      AND
    #               CLR2   LIKE     ?CLR2LOW                      AND
    #               CPI    LIKE     ?CPILOW                       AND
    #               DCC    LIKE     ?DCCLOW                       AND
    #               FLT    LIKE     ?FLTLOW                       AND
    #               FSC    LIKE     ?FSCLOW                       AND
    #               GW     LIKE     ?GWLOW                        AND
    #               ICI    LIKE     ?ICILOW                       AND
    #               IDSTA  LIKE     ?IDSTALOW                     AND
    #               IDSTN  LIKE     ?IDSTNLOW                     AND
    #               IO     LIKE     ?IOLOW                        AND
    #               IRTA   LIKE     ?IRTALOW                      AND
    #               ISG    LIKE     ?ISGLOW                       AND
    #               ISRTN  LIKE     ?ISRTNLOW                     AND
    #               ISTN   LIKE     ?ISTNLOW                      AND
    #               MA     LIKE     ?MALOW                        AND
    #               ODSTA  LIKE     ?ODSTALOW                     AND
    #               ODSTN  LIKE     ?ODSTNLOW                     AND
    #               OGTM   LIKE     ?OGTMLOW                      AND
    #               ORTA   LIKE     ?ORTALOW                      AND
    #               ORDAY  LIKE     ?ORDAYLOW                     AND
    #               ORTM   LIKE     ?ORTMLOW                      AND
    #               OSG    LIKE     ?OSGLOW                       AND
    #               OSTN   LIKE     ?OSTNLOW                      AND
    #               RAI    LIKE     ?RAILOW                       AND
    #               SUB    LIKE     ?SUBLOW                       AND
    #               TMR    LIKE     ?TMRLOW                       AND
    #==             UUIR   LIKE     ?UUIRLOW                      AND
    #==             UUIS   LIKE     ?UUISLOW                      AND
    #               VD     LIKE     ?VDLOW                        AND
    #               VDT    LIKE     ?VDTLOW                       AND
    #               VRTA   LIKE     ?VRTALOW)                     OR
    #==
    #             ((SDNO1,SDNO2)
    #                      BETWEEN (?SDNO1LOW11,?SDNO2LOW12)
    #                                            AND (?SDNO1HIGH11,?SDNO2HIGH12)
    #                                                               AND
    #               CFDAY  LIKE     ?CFDAYLOW                     AND
    #               ORN    LIKE     ?ORNLOW                       AND
    #               PN     LIKE     ?PNLOW                        AND
    #               RDGT   LIKE     ?RDGTLOW                      AND
    #               SPN    LIKE     ?SPNLOW                       AND
    #               CCS    LIKE     ?CCSLOW                       AND
    #               CID    LIKE     ?CIDLOW                       AND
    #               CLN    LIKE     ?CLNLOW                       AND
    #               CLT    LIKE     ?CLTLOW                       AND
    #               CN     LIKE     ?CNLOW                        AND
    #              (CN0    LIKE     ?CN0LOW                       OR
    #               CN1    LIKE     ?CN1LOW)                      AND
    #              (ISRTA  LIKE     ?ISRTALOW                     OR
    #               OSRTA  LIKE     ?OSRTALOW)                    AND
    #               NNP    LIKE     ?NNPLOW                       AND
    #               ORC    LIKE     ?ORCLOW                       AND
    #               OSC    LIKE     ?OSCLOW                       AND
    #               PFXC   LIKE     ?PFXCLOW                      AND
    #               RDC    LIKE     ?RDCLOW                       AND
    #               SCS    LIKE     ?SCSLOW                       AND
    #               SPC    LIKE     ?SPCLOW                       AND
    #               SSC    LIKE     ?SSCLOW                       AND
    #              (TN0    LIKE     ?TN0LOW                       OR
    #               TN1    LIKE     ?TN1LOW)                      AND
    #               ANDAY  LIKE     ?ANDAYLOW                     AND
    #               ANTM   LIKE     ?ANTMLOW                      AND
    #               CBTM   LIKE     ?CBTMLOW                      AND
    #               CCLS   LIKE     ?CCLSLOW                      AND
    #               CGF    LIKE     ?CGFLOW                       AND
    #==             CHGC   LIKE     ?CHGCLOW                      AND
    #               CHK    LIKE     ?CHKLOW                       AND
    #               CLR1   LIKE     ?CLR1LOW                      AND
    #               CLR2   LIKE     ?CLR2LOW                      AND
    #               CPI    LIKE     ?CPILOW                       AND
    #               DCC    LIKE     ?DCCLOW                       AND
    #               FLT    LIKE     ?FLTLOW                       AND
    #               FSC    LIKE     ?FSCLOW                       AND
    #               GW     LIKE     ?GWLOW                        AND
    #               ICI    LIKE     ?ICILOW                       AND
    #               IDSTA  LIKE     ?IDSTALOW                     AND
    #               IDSTN  LIKE     ?IDSTNLOW                     AND
    #               IO     LIKE     ?IOLOW                        AND
    #               IRTA   LIKE     ?IRTALOW                      AND
    #               ISG    LIKE     ?ISGLOW                       AND
    #               ISRTN  LIKE     ?ISRTNLOW                     AND
    #               ISTN   LIKE     ?ISTNLOW                      AND
    #               MA     LIKE     ?MALOW                        AND
    #               ODSTA  LIKE     ?ODSTALOW                     AND
    #               ODSTN  LIKE     ?ODSTNLOW                     AND
    #               OGTM   LIKE     ?OGTMLOW                      AND
    #               ORTA   LIKE     ?ORTALOW                      AND
    #               ORDAY  LIKE     ?ORDAYLOW                     AND
    #               ORTM   LIKE     ?ORTMLOW                      AND
    #               OSG    LIKE     ?OSGLOW                       AND
    #               OSTN   LIKE     ?OSTNLOW                      AND
    #               RAI    LIKE     ?RAILOW                       AND
    #               SUB    LIKE     ?SUBLOW                       AND
    #               TMR    LIKE     ?TMRLOW                       AND
    #==             UUIR   LIKE     ?UUIRLOW                      AND
    #==             UUIS   LIKE     ?UUISLOW                      AND
    #               VD     LIKE     ?VDLOW                        AND
    #               VDT    LIKE     ?VDTLOW                       AND
    #               VRTA   LIKE     ?VRTALOW)                     OR
    #==
    #             ((SDNO1,SDNO2)
    #                      BETWEEN (?SDNO1LOW11,?SDNO2LOW12)
    #                                            AND (?SDNO1HIGH11,?SDNO2HIGH12)
    #                                                               AND
    #               CFDAY  LIKE     ?CFDAYLOW                     AND
    #               ORN    LIKE     ?ORNLOW                       AND
    #               PN     LIKE     ?PNLOW                        AND
    #               RDGT   LIKE     ?RDGTLOW                      AND
    #               SPN    LIKE     ?SPNLOW                       AND
    #               CCS    LIKE     ?CCSLOW                       AND
    #               CID    LIKE     ?CIDLOW                       AND
    #               CLN    LIKE     ?CLNLOW                       AND
    #               CLT    LIKE     ?CLTLOW                       AND
    #               CN     LIKE     ?CNLOW                        AND
    #              (CN0    LIKE     ?CN0LOW                       OR
    #               CN1    LIKE     ?CN1LOW)                      AND
    #              (ISRTA  LIKE     ?ISRTALOW                     OR
    #               OSRTA  LIKE     ?OSRTALOW)                    AND
    #               NNP    LIKE     ?NNPLOW                       AND
    #               ORC    LIKE     ?ORCLOW                       AND
    #               OSC    LIKE     ?OSCLOW                       AND
    #               PFXC   LIKE     ?PFXCLOW                      AND
    #               RDC    LIKE     ?RDCLOW                       AND
    #               SCS    LIKE     ?SCSLOW                       AND
    #               SPC    LIKE     ?SPCLOW                       AND
    #               SSC    LIKE     ?SSCLOW                       AND
    #              (TN0    LIKE     ?TN0LOW                       OR
    #               TN1    LIKE     ?TN1LOW)                      AND
    #               ANDAY  LIKE     ?ANDAYLOW                     AND
    #               ANTM   LIKE     ?ANTMLOW                      AND
    #               CBTM   LIKE     ?CBTMLOW                      AND
    #               CCLS   LIKE     ?CCLSLOW                      AND
    #               CGF    LIKE     ?CGFLOW                       AND
    #==             CHGC   LIKE     ?CHGCLOW                      AND
    #               CHK    LIKE     ?CHKLOW                       AND
    #               CLR1   LIKE     ?CLR1LOW                      AND
    #               CLR2   LIKE     ?CLR2LOW                      AND
    #               CPI    LIKE     ?CPILOW                       AND
    #               DCC    LIKE     ?DCCLOW                       AND
    #               FLT    LIKE     ?FLTLOW                       AND
    #               FSC    LIKE     ?FSCLOW                       AND
    #               GW     LIKE     ?GWLOW                        AND
    #               ICI    LIKE     ?ICILOW                       AND
    #               IDSTA  LIKE     ?IDSTALOW                     AND
    #               IDSTN  LIKE     ?IDSTNLOW                     AND
    #               IO     LIKE     ?IOLOW                        AND
    #               IRTA   LIKE     ?IRTALOW                      AND
    #               ISG    LIKE     ?ISGLOW                       AND
    #               ISRTN  LIKE     ?ISRTNLOW                     AND
    #               ISTN   LIKE     ?ISTNLOW                      AND
    #               MA     LIKE     ?MALOW                        AND
    #               ODSTA  LIKE     ?ODSTALOW                     AND
    #               ODSTN  LIKE     ?ODSTNLOW                     AND
    #               OGTM   LIKE     ?OGTMLOW                      AND
    #               ORTA   LIKE     ?ORTALOW                      AND
    #               ORDAY  LIKE     ?ORDAYLOW                     AND
    #               ORTM   LIKE     ?ORTMLOW                      AND
    #               OSG    LIKE     ?OSGLOW                       AND
    #               OSTN   LIKE     ?OSTNLOW                      AND
    #               RAI    LIKE     ?RAILOW                       AND
    #               SUB    LIKE     ?SUBLOW                       AND
    #               TMR    LIKE     ?TMRLOW                       AND
    #==             UUIR   LIKE     ?UUIRLOW                      AND
    #==             UUIS   LIKE     ?UUISLOW                      AND
    #               VD     LIKE     ?VDLOW                        AND
    #               VDT    LIKE     ?VDTLOW                       AND
    #               VRTA   LIKE     ?VRTALOW)                     OR
    #==
    #             ((SDNO1,SDNO2)
    #                      BETWEEN (?SDNO1LOW11,?SDNO2LOW12)
    #                                            AND (?SDNO1HIGH11,?SDNO2HIGH12)
    #                                                               AND
    #               CFDAY  LIKE     ?CFDAYLOW                     AND
    #               ORN    LIKE     ?ORNLOW                       AND
    #               PN     LIKE     ?PNLOW                        AND
    #               RDGT   LIKE     ?RDGTLOW                      AND
    #               SPN    LIKE     ?SPNLOW                       AND
    #               CCS    LIKE     ?CCSLOW                       AND
    #               CID    LIKE     ?CIDLOW                       AND
    #               CLN    LIKE     ?CLNLOW                       AND
    #               CLT    LIKE     ?CLTLOW                       AND
    #               CN     LIKE     ?CNLOW                        AND
    #              (CN0    LIKE     ?CN0LOW                       OR
    #               CN1    LIKE     ?CN1LOW)                      AND
    #              (ISRTA  LIKE     ?ISRTALOW                     OR
    #               OSRTA  LIKE     ?OSRTALOW)                    AND
    #               NNP    LIKE     ?NNPLOW                       AND
    #               ORC    LIKE     ?ORCLOW                       AND
    #               OSC    LIKE     ?OSCLOW                       AND
    #               PFXC   LIKE     ?PFXCLOW                      AND
    #               RDC    LIKE     ?RDCLOW                       AND
    #               SCS    LIKE     ?SCSLOW                       AND
    #               SPC    LIKE     ?SPCLOW                       AND
    #               SSC    LIKE     ?SSCLOW                       AND
    #              (TN0    LIKE     ?TN0LOW                       OR
    #               TN1    LIKE     ?TN1LOW)                      AND
    #               ANDAY  LIKE     ?ANDAYLOW                     AND
    #               ANTM   LIKE     ?ANTMLOW                      AND
    #               CBTM   LIKE     ?CBTMLOW                      AND
    #               CCLS   LIKE     ?CCLSLOW                      AND
    #               CGF    LIKE     ?CGFLOW                       AND
    #==             CHGC   LIKE     ?CHGCLOW                      AND
    #               CHK    LIKE     ?CHKLOW                       AND
    #               CLR1   LIKE     ?CLR1LOW                      AND
    #               CLR2   LIKE     ?CLR2LOW                      AND
    #               CPI    LIKE     ?CPILOW                       AND
    #               DCC    LIKE     ?DCCLOW                       AND
    #               FLT    LIKE     ?FLTLOW                       AND
    #               FSC    LIKE     ?FSCLOW                       AND
    #               GW     LIKE     ?GWLOW                        AND
    #               ICI    LIKE     ?ICILOW                       AND
    #               IDSTA  LIKE     ?IDSTALOW                     AND
    #               IDSTN  LIKE     ?IDSTNLOW                     AND
    #               IO     LIKE     ?IOLOW                        AND
    #               IRTA   LIKE     ?IRTALOW                      AND
    #               ISG    LIKE     ?ISGLOW                       AND
    #               ISRTN  LIKE     ?ISRTNLOW                     AND
    #               ISTN   LIKE     ?ISTNLOW                      AND
    #               MA     LIKE     ?MALOW                        AND
    #               ODSTA  LIKE     ?ODSTALOW                     AND
    #               ODSTN  LIKE     ?ODSTNLOW                     AND
    #               OGTM   LIKE     ?OGTMLOW                      AND
    #               ORTA   LIKE     ?ORTALOW                      AND
    #               ORDAY  LIKE     ?ORDAYLOW                     AND
    #               ORTM   LIKE     ?ORTMLOW                      AND
    #               OSG    LIKE     ?OSGLOW                       AND
    #               OSTN   LIKE     ?OSTNLOW                      AND
    #               RAI    LIKE     ?RAILOW                       AND
    #               SUB    LIKE     ?SUBLOW                       AND
    #               TMR    LIKE     ?TMRLOW                       AND
    #==             UUIR   LIKE     ?UUIRLOW                      AND
    #==             UUIS   LIKE     ?UUISLOW                      AND
    #               VD     LIKE     ?VDLOW                        AND
    #               VDT    LIKE     ?VDTLOW                       AND
    #               VRTA   LIKE     ?VRTALOW)
    #       read uncommitted access
    # ;
    
    #  Without fix:  The following EXECUTE fails because s1       (BAD)
    #                  was not prepared.
    #  With fix:     EXECUTE fails with file system error 1133
    #                  (selection expression too complex).
    #                  Should return 0 rows.                      (GOOD)
    
    #  Without fix:  The following PREPARE fails with a trap      (BAD)
    #                  in SQLCOMP.
    #  With fix:     PREPARE completes successfully.              (GOOD)
    #  This query is the same as the previous one with the
    #    addition of a dummy EXISTS predicate at the end.
    #    The customer has been advised to use such a dummy
    #    predicate to cause all the predicates to be evaluated
    #    at the Executor level, thereby avoiding the file
    #    system error 1133.
    
    qa04s2._init(_testmgr)
    
    #$SQL_prepared_msg
    #prepare s2 from
    #               SDNO2   ,
    #               CFDAY   ,
    #               CFTM1   ,
    #               CFTM2   ,
    #               CFTM3   ,
    #               ORN     ,
    #               PN      ,
    #               RDGT    ,
    #               SPN     ,
    #               CCS     ,
    #               CID     ,
    #               CLN     ,
    #               CLT     ,
    #               CN      ,
    #               CN0     ,
    #               CN1     ,
    #               ISRTA   ,
    #               NNP     ,
    #               ORC     ,
    #               OSC     ,
    #               OSRTA   ,
    #               PFXC    ,
    #               RDC     ,
    #               SCS     ,
    #               SPC     ,
    #               SSC     ,
    #               TN0     ,
    #               TN1     ,
    #               ANDAY   ,
    #               ANTM    ,
    #               CBTM    ,
    #               CCLS    ,
    #               CGF     ,
    #               CHGC    ,
    #               CHK     ,
    #               CLR1    ,
    #               CLR2    ,
    #               CPI     ,
    #               DCC     ,
    #               FLT     ,
    #               FSC     ,
    #               GW      ,
    #               ICI     ,
    #               IDSTA   ,
    #               IDSTN   ,
    #               IO      ,
    #               IRTA    ,
    #               ISG     ,
    #               ISRTN   ,
    #               ISTN    ,
    #               MA      ,
    #               ODSTA   ,
    #               ODSTN   ,
    #               OGTM   ,
    #               ORTA    ,
    #               ORDAY   ,
    #               ORTM    ,
    #               OSG     ,
    #               OSTN    ,
    #               RAI     ,
    #               SUB     ,
    #               TMR     ,
    #               UUIR    ,
    #               UUIS    ,
    #               VD      ,
    #               VDT     ,
    #               VRTA
    #       FROM   s0804ta
    #       WHERE  (CFTM1,CFTM2,CFTM3)
    #                        BETWEEN (?CFTMLOW1,?CFTMLOW2,?CFTMLOW3)    AND
    #                                (?CFTMHIGH1,?CFTMHIGH2,?CFTMHIGH3) AND
    #             ((SDNO1,SDNO2)
    #                      BETWEEN (?SDNO1LOW11,?SDNO2LOW12)
    #                                            AND (?SDNO1HIGH11,?SDNO2HIGH12)
    #                                                               AND
    #               CFDAY  LIKE     ?CFDAYLOW                     AND
    #               ORN    LIKE     ?ORNLOW                       AND
    #               PN     LIKE     ?PNLOW                        AND
    #               RDGT   LIKE     ?RDGTLOW                      AND
    #               SPN    LIKE     ?SPNLOW                       AND
    #               CCS    LIKE     ?CCSLOW                       AND
    #               CID    LIKE     ?CIDLOW                       AND
    #               CLN    LIKE     ?CLNLOW                       AND
    #               CLT    LIKE     ?CLTLOW                       AND
    #               CN     LIKE     ?CNLOW                        AND
    #              (CN0    LIKE     ?CN0LOW                       OR
    #               CN1    LIKE     ?CN1LOW)                      AND
    #              (ISRTA  LIKE     ?ISRTALOW                     OR
    #               OSRTA  LIKE     ?OSRTALOW)                    AND
    #               NNP    LIKE     ?NNPLOW                       AND
    #               ORC    LIKE     ?ORCLOW                       AND
    #               OSC    LIKE     ?OSCLOW                       AND
    #               PFXC   LIKE     ?PFXCLOW                      AND
    #               RDC    LIKE     ?RDCLOW                       AND
    #               SCS    LIKE     ?SCSLOW                       AND
    #               SPC    LIKE     ?SPCLOW                       AND
    #               SSC    LIKE     ?SSCLOW                       AND
    #              (TN0    LIKE     ?TN0LOW                       OR
    #               TN1    LIKE     ?TN1LOW)                      AND
    #               ANDAY  LIKE     ?ANDAYLOW                     AND
    #               ANTM   LIKE     ?ANTMLOW                      AND
    #               CBTM   LIKE     ?CBTMLOW                      AND
    #               CCLS   LIKE     ?CCLSLOW                      AND
    #               CGF    LIKE     ?CGFLOW                       AND
    #==             CHGC   LIKE     ?CHGCLOW                      AND
    #               CHK    LIKE     ?CHKLOW                       AND
    #               CLR1   LIKE     ?CLR1LOW                      AND
    #               CLR2   LIKE     ?CLR2LOW                      AND
    #               CPI    LIKE     ?CPILOW                       AND
    #               DCC    LIKE     ?DCCLOW                       AND
    #               FLT    LIKE     ?FLTLOW                       AND
    #               FSC    LIKE     ?FSCLOW                       AND
    #               GW     LIKE     ?GWLOW                        AND
    #               ICI    LIKE     ?ICILOW                       AND
    #               IDSTA  LIKE     ?IDSTALOW                     AND
    #               IDSTN  LIKE     ?IDSTNLOW                     AND
    #               IO     LIKE     ?IOLOW                        AND
    #               IRTA   LIKE     ?IRTALOW                      AND
    #               ISG    LIKE     ?ISGLOW                       AND
    #               ISRTN  LIKE     ?ISRTNLOW                     AND
    #               ISTN   LIKE     ?ISTNLOW                      AND
    #               MA     LIKE     ?MALOW                        AND
    #               ODSTA  LIKE     ?ODSTALOW                     AND
    #               ODSTN  LIKE     ?ODSTNLOW                     AND
    #               OGTM   LIKE     ?OGTMLOW                      AND
    #               ORTA   LIKE     ?ORTALOW                      AND
    #               ORDAY  LIKE     ?ORDAYLOW                     AND
    #               ORTM   LIKE     ?ORTMLOW                      AND
    #               OSG    LIKE     ?OSGLOW                       AND
    #               OSTN   LIKE     ?OSTNLOW                      AND
    #               RAI    LIKE     ?RAILOW                       AND
    #               SUB    LIKE     ?SUBLOW                       AND
    #               TMR    LIKE     ?TMRLOW                       AND
    #==             UUIR   LIKE     ?UUIRLOW                      AND
    #==             UUIS   LIKE     ?UUISLOW                      AND
    #               VD     LIKE     ?VDLOW                        AND
    #               VDT    LIKE     ?VDTLOW                       AND
    #               VRTA   LIKE     ?VRTALOW)                     OR
    #==
    #             ((SDNO1,SDNO2)
    #                      BETWEEN (?SDNO1LOW11,?SDNO2LOW12)
    #                                            AND (?SDNO1HIGH11,?SDNO2HIGH12)
    #                                                               AND
    #               CFDAY  LIKE     ?CFDAYLOW                     AND
    #               ORN    LIKE     ?ORNLOW                       AND
    #               PN     LIKE     ?PNLOW                        AND
    #               RDGT   LIKE     ?RDGTLOW                      AND
    #               SPN    LIKE     ?SPNLOW                       AND
    #               CCS    LIKE     ?CCSLOW                       AND
    #               CID    LIKE     ?CIDLOW                       AND
    #               CLN    LIKE     ?CLNLOW                       AND
    #               CLT    LIKE     ?CLTLOW                       AND
    #               CN     LIKE     ?CNLOW                        AND
    #              (CN0    LIKE     ?CN0LOW                       OR
    #               CN1    LIKE     ?CN1LOW)                      AND
    #              (ISRTA  LIKE     ?ISRTALOW                     OR
    #               OSRTA  LIKE     ?OSRTALOW)                    AND
    #               NNP    LIKE     ?NNPLOW                       AND
    #               ORC    LIKE     ?ORCLOW                       AND
    #               OSC    LIKE     ?OSCLOW                       AND
    #               PFXC   LIKE     ?PFXCLOW                      AND
    #               RDC    LIKE     ?RDCLOW                       AND
    #               SCS    LIKE     ?SCSLOW                       AND
    #               SPC    LIKE     ?SPCLOW                       AND
    #               SSC    LIKE     ?SSCLOW                       AND
    #              (TN0    LIKE     ?TN0LOW                       OR
    #               TN1    LIKE     ?TN1LOW)                      AND
    #               ANDAY  LIKE     ?ANDAYLOW                     AND
    #               ANTM   LIKE     ?ANTMLOW                      AND
    #               CBTM   LIKE     ?CBTMLOW                      AND
    #               CCLS   LIKE     ?CCLSLOW                      AND
    #               CGF    LIKE     ?CGFLOW                       AND
    #==             CHGC   LIKE     ?CHGCLOW                      AND
    #               CHK    LIKE     ?CHKLOW                       AND
    #               CLR1   LIKE     ?CLR1LOW                      AND
    #               CLR2   LIKE     ?CLR2LOW                      AND
    #               CPI    LIKE     ?CPILOW                       AND
    #               DCC    LIKE     ?DCCLOW                       AND
    #               FLT    LIKE     ?FLTLOW                       AND
    #               FSC    LIKE     ?FSCLOW                       AND
    #               GW     LIKE     ?GWLOW                        AND
    #               ICI    LIKE     ?ICILOW                       AND
    #               IDSTA  LIKE     ?IDSTALOW                     AND
    #               IDSTN  LIKE     ?IDSTNLOW                     AND
    #               IO     LIKE     ?IOLOW                        AND
    #               IRTA   LIKE     ?IRTALOW                      AND
    #               ISG    LIKE     ?ISGLOW                       AND
    #               ISRTN  LIKE     ?ISRTNLOW                     AND
    #               ISTN   LIKE     ?ISTNLOW                      AND
    #               MA     LIKE     ?MALOW                        AND
    #               ODSTA  LIKE     ?ODSTALOW                     AND
    #               ODSTN  LIKE     ?ODSTNLOW                     AND
    #               OGTM   LIKE     ?OGTMLOW                      AND
    #               ORTA   LIKE     ?ORTALOW                      AND
    #               ORDAY  LIKE     ?ORDAYLOW                     AND
    #               ORTM   LIKE     ?ORTMLOW                      AND
    #               OSG    LIKE     ?OSGLOW                       AND
    #               OSTN   LIKE     ?OSTNLOW                      AND
    #               RAI    LIKE     ?RAILOW                       AND
    #               SUB    LIKE     ?SUBLOW                       AND
    #               TMR    LIKE     ?TMRLOW                       AND
    #==             UUIR   LIKE     ?UUIRLOW                      AND
    #==             UUIS   LIKE     ?UUISLOW                      AND
    #               VD     LIKE     ?VDLOW                        AND
    #               VDT    LIKE     ?VDTLOW                       AND
    #               VRTA   LIKE     ?VRTALOW)                     OR
    #==
    #             ((SDNO1,SDNO2)
    #                      BETWEEN (?SDNO1LOW11,?SDNO2LOW12)
    #                                            AND (?SDNO1HIGH11,?SDNO2HIGH12)
    #                                                               AND
    #               CFDAY  LIKE     ?CFDAYLOW                     AND
    #               ORN    LIKE     ?ORNLOW                       AND
    #               PN     LIKE     ?PNLOW                        AND
    #               RDGT   LIKE     ?RDGTLOW                      AND
    #               SPN    LIKE     ?SPNLOW                       AND
    #               CCS    LIKE     ?CCSLOW                       AND
    #               CID    LIKE     ?CIDLOW                       AND
    #               CLN    LIKE     ?CLNLOW                       AND
    #               CLT    LIKE     ?CLTLOW                       AND
    #               CN     LIKE     ?CNLOW                        AND
    #              (CN0    LIKE     ?CN0LOW                       OR
    #               CN1    LIKE     ?CN1LOW)                      AND
    #              (ISRTA  LIKE     ?ISRTALOW                     OR
    #               OSRTA  LIKE     ?OSRTALOW)                    AND
    #               NNP    LIKE     ?NNPLOW                       AND
    #               ORC    LIKE     ?ORCLOW                       AND
    #               OSC    LIKE     ?OSCLOW                       AND
    #               PFXC   LIKE     ?PFXCLOW                      AND
    #               RDC    LIKE     ?RDCLOW                       AND
    #               SCS    LIKE     ?SCSLOW                       AND
    #               SPC    LIKE     ?SPCLOW                       AND
    #               SSC    LIKE     ?SSCLOW                       AND
    #              (TN0    LIKE     ?TN0LOW                       OR
    #               TN1    LIKE     ?TN1LOW)                      AND
    #               ANDAY  LIKE     ?ANDAYLOW                     AND
    #               ANTM   LIKE     ?ANTMLOW                      AND
    #               CBTM   LIKE     ?CBTMLOW                      AND
    #               CCLS   LIKE     ?CCLSLOW                      AND
    #               CGF    LIKE     ?CGFLOW                       AND
    #==             CHGC   LIKE     ?CHGCLOW                      AND
    #               CHK    LIKE     ?CHKLOW                       AND
    #               CLR1   LIKE     ?CLR1LOW                      AND
    #               CLR2   LIKE     ?CLR2LOW                      AND
    #               CPI    LIKE     ?CPILOW                       AND
    #               DCC    LIKE     ?DCCLOW                       AND
    #               FLT    LIKE     ?FLTLOW                       AND
    #               FSC    LIKE     ?FSCLOW                       AND
    #               GW     LIKE     ?GWLOW                        AND
    #               ICI    LIKE     ?ICILOW                       AND
    #               IDSTA  LIKE     ?IDSTALOW                     AND
    #               IDSTN  LIKE     ?IDSTNLOW                     AND
    #               IO     LIKE     ?IOLOW                        AND
    #               IRTA   LIKE     ?IRTALOW                      AND
    #               ISG    LIKE     ?ISGLOW                       AND
    #               ISRTN  LIKE     ?ISRTNLOW                     AND
    #               ISTN   LIKE     ?ISTNLOW                      AND
    #               MA     LIKE     ?MALOW                        AND
    #               ODSTA  LIKE     ?ODSTALOW                     AND
    #               ODSTN  LIKE     ?ODSTNLOW                     AND
    #               OGTM   LIKE     ?OGTMLOW                      AND
    #               ORTA   LIKE     ?ORTALOW                      AND
    #               ORDAY  LIKE     ?ORDAYLOW                     AND
    #               ORTM   LIKE     ?ORTMLOW                      AND
    #               OSG    LIKE     ?OSGLOW                       AND
    #               OSTN   LIKE     ?OSTNLOW                      AND
    #               RAI    LIKE     ?RAILOW                       AND
    #               SUB    LIKE     ?SUBLOW                       AND
    #               TMR    LIKE     ?TMRLOW                       AND
    #==             UUIR   LIKE     ?UUIRLOW                      AND
    #==             UUIS   LIKE     ?UUISLOW                      AND
    #               VD     LIKE     ?VDLOW                        AND
    #               VDT    LIKE     ?VDTLOW                       AND
    #               VRTA   LIKE     ?VRTALOW)                     OR
    #==
    #             ((SDNO1,SDNO2)
    #                      BETWEEN (?SDNO1LOW11,?SDNO2LOW12)
    #                                            AND (?SDNO1HIGH11,?SDNO2HIGH12)
    #                                                               AND
    #               CFDAY  LIKE     ?CFDAYLOW                     AND
    #               ORN    LIKE     ?ORNLOW                       AND
    #               PN     LIKE     ?PNLOW                        AND
    #               RDGT   LIKE     ?RDGTLOW                      AND
    #               SPN    LIKE     ?SPNLOW                       AND
    #               CCS    LIKE     ?CCSLOW                       AND
    #               CID    LIKE     ?CIDLOW                       AND
    #               CLN    LIKE     ?CLNLOW                       AND
    #               CLT    LIKE     ?CLTLOW                       AND
    #               CN     LIKE     ?CNLOW                        AND
    #              (CN0    LIKE     ?CN0LOW                       OR
    #               CN1    LIKE     ?CN1LOW)                      AND
    #              (ISRTA  LIKE     ?ISRTALOW                     OR
    #               OSRTA  LIKE     ?OSRTALOW)                    AND
    #               NNP    LIKE     ?NNPLOW                       AND
    #               ORC    LIKE     ?ORCLOW                       AND
    #               OSC    LIKE     ?OSCLOW                       AND
    #               PFXC   LIKE     ?PFXCLOW                      AND
    #               RDC    LIKE     ?RDCLOW                       AND
    #               SCS    LIKE     ?SCSLOW                       AND
    #               SPC    LIKE     ?SPCLOW                       AND
    #               SSC    LIKE     ?SSCLOW                       AND
    #              (TN0    LIKE     ?TN0LOW                       OR
    #               TN1    LIKE     ?TN1LOW)                      AND
    #               ANDAY  LIKE     ?ANDAYLOW                     AND
    #               ANTM   LIKE     ?ANTMLOW                      AND
    #               CBTM   LIKE     ?CBTMLOW                      AND
    #               CCLS   LIKE     ?CCLSLOW                      AND
    #               CGF    LIKE     ?CGFLOW                       AND
    #==             CHGC   LIKE     ?CHGCLOW                      AND
    #               CHK    LIKE     ?CHKLOW                       AND
    #               CLR1   LIKE     ?CLR1LOW                      AND
    #               CLR2   LIKE     ?CLR2LOW                      AND
    #               CPI    LIKE     ?CPILOW                       AND
    #               DCC    LIKE     ?DCCLOW                       AND
    #               FLT    LIKE     ?FLTLOW                       AND
    #               FSC    LIKE     ?FSCLOW                       AND
    #               GW     LIKE     ?GWLOW                        AND
    #               ICI    LIKE     ?ICILOW                       AND
    #               IDSTA  LIKE     ?IDSTALOW                     AND
    #               IDSTN  LIKE     ?IDSTNLOW                     AND
    #               IO     LIKE     ?IOLOW                        AND
    #               IRTA   LIKE     ?IRTALOW                      AND
    #               ISG    LIKE     ?ISGLOW                       AND
    #               ISRTN  LIKE     ?ISRTNLOW                     AND
    #               ISTN   LIKE     ?ISTNLOW                      AND
    #               MA     LIKE     ?MALOW                        AND
    #               ODSTA  LIKE     ?ODSTALOW                     AND
    #               ODSTN  LIKE     ?ODSTNLOW                     AND
    #               OGTM   LIKE     ?OGTMLOW                      AND
    #               ORTA   LIKE     ?ORTALOW                      AND
    #               ORDAY  LIKE     ?ORDAYLOW                     AND
    #               ORTM   LIKE     ?ORTMLOW                      AND
    #               OSG    LIKE     ?OSGLOW                       AND
    #               OSTN   LIKE     ?OSTNLOW                      AND
    #               RAI    LIKE     ?RAILOW                       AND
    #               SUB    LIKE     ?SUBLOW                       AND
    #               TMR    LIKE     ?TMRLOW                       AND
    #==             UUIR   LIKE     ?UUIRLOW                      AND
    #==             UUIS   LIKE     ?UUISLOW                      AND
    #               VD     LIKE     ?VDLOW                        AND
    #               VDT    LIKE     ?VDTLOW                       AND
    #               VRTA   LIKE     ?VRTALOW)                     OR
    #==
    #             ((SDNO1,SDNO2)
    #                      BETWEEN (?SDNO1LOW11,?SDNO2LOW12)
    #                                            AND (?SDNO1HIGH11,?SDNO2HIGH12)
    #                                                               AND
    #               CFDAY  LIKE     ?CFDAYLOW                     AND
    #               ORN    LIKE     ?ORNLOW                       AND
    #               PN     LIKE     ?PNLOW                        AND
    #               RDGT   LIKE     ?RDGTLOW                      AND
    #               SPN    LIKE     ?SPNLOW                       AND
    #               CCS    LIKE     ?CCSLOW                       AND
    #               CID    LIKE     ?CIDLOW                       AND
    #               CLN    LIKE     ?CLNLOW                       AND
    #               CLT    LIKE     ?CLTLOW                       AND
    #               CN     LIKE     ?CNLOW                        AND
    #              (CN0    LIKE     ?CN0LOW                       OR
    #               CN1    LIKE     ?CN1LOW)                      AND
    #              (ISRTA  LIKE     ?ISRTALOW                     OR
    #               OSRTA  LIKE     ?OSRTALOW)                    AND
    #               NNP    LIKE     ?NNPLOW                       AND
    #               ORC    LIKE     ?ORCLOW                       AND
    #               OSC    LIKE     ?OSCLOW                       AND
    #               PFXC   LIKE     ?PFXCLOW                      AND
    #               RDC    LIKE     ?RDCLOW                       AND
    #               SCS    LIKE     ?SCSLOW                       AND
    #               SPC    LIKE     ?SPCLOW                       AND
    #               SSC    LIKE     ?SSCLOW                       AND
    #              (TN0    LIKE     ?TN0LOW                       OR
    #               TN1    LIKE     ?TN1LOW)                      AND
    #               ANDAY  LIKE     ?ANDAYLOW                     AND
    #               ANTM   LIKE     ?ANTMLOW                      AND
    #               CBTM   LIKE     ?CBTMLOW                      AND
    #               CCLS   LIKE     ?CCLSLOW                      AND
    #               CGF    LIKE     ?CGFLOW                       AND
    #==             CHGC   LIKE     ?CHGCLOW                      AND
    #               CHK    LIKE     ?CHKLOW                       AND
    #               CLR1   LIKE     ?CLR1LOW                      AND
    #               CLR2   LIKE     ?CLR2LOW                      AND
    #               CPI    LIKE     ?CPILOW                       AND
    #               DCC    LIKE     ?DCCLOW                       AND
    #               FLT    LIKE     ?FLTLOW                       AND
    #               FSC    LIKE     ?FSCLOW                       AND
    #               GW     LIKE     ?GWLOW                        AND
    #               ICI    LIKE     ?ICILOW                       AND
    #               IDSTA  LIKE     ?IDSTALOW                     AND
    #               IDSTN  LIKE     ?IDSTNLOW                     AND
    #               IO     LIKE     ?IOLOW                        AND
    #               IRTA   LIKE     ?IRTALOW                      AND
    #               ISG    LIKE     ?ISGLOW                       AND
    #               ISRTN  LIKE     ?ISRTNLOW                     AND
    #               ISTN   LIKE     ?ISTNLOW                      AND
    #               MA     LIKE     ?MALOW                        AND
    #               ODSTA  LIKE     ?ODSTALOW                     AND
    #               ODSTN  LIKE     ?ODSTNLOW                     AND
    #               OGTM   LIKE     ?OGTMLOW                      AND
    #               ORTA   LIKE     ?ORTALOW                      AND
    #               ORDAY  LIKE     ?ORDAYLOW                     AND
    #               ORTM   LIKE     ?ORTMLOW                      AND
    #               OSG    LIKE     ?OSGLOW                       AND
    #               OSTN   LIKE     ?OSTNLOW                      AND
    #               RAI    LIKE     ?RAILOW                       AND
    #               SUB    LIKE     ?SUBLOW                       AND
    #               TMR    LIKE     ?TMRLOW                       AND
    #==             UUIR   LIKE     ?UUIRLOW                      AND
    #==             UUIS   LIKE     ?UUISLOW                      AND
    #               VD     LIKE     ?VDLOW                        AND
    #               VDT    LIKE     ?VDTLOW                       AND
    #               VRTA   LIKE     ?VRTALOW)                     OR
    #==
    #             ((SDNO1,SDNO2)
    #                      BETWEEN (?SDNO1LOW11,?SDNO2LOW12)
    #                                            AND (?SDNO1HIGH11,?SDNO2HIGH12)
    #                                                               AND
    #               CFDAY  LIKE     ?CFDAYLOW                     AND
    #               ORN    LIKE     ?ORNLOW                       AND
    #               PN     LIKE     ?PNLOW                        AND
    #               RDGT   LIKE     ?RDGTLOW                      AND
    #               SPN    LIKE     ?SPNLOW                       AND
    #               CCS    LIKE     ?CCSLOW                       AND
    #               CID    LIKE     ?CIDLOW                       AND
    #               CLN    LIKE     ?CLNLOW                       AND
    #               CLT    LIKE     ?CLTLOW                       AND
    #               CN     LIKE     ?CNLOW                        AND
    #              (CN0    LIKE     ?CN0LOW                       OR
    #               CN1    LIKE     ?CN1LOW)                      AND
    #              (ISRTA  LIKE     ?ISRTALOW                     OR
    #               OSRTA  LIKE     ?OSRTALOW)                    AND
    #               NNP    LIKE     ?NNPLOW                       AND
    #               ORC    LIKE     ?ORCLOW                       AND
    #               OSC    LIKE     ?OSCLOW                       AND
    #               PFXC   LIKE     ?PFXCLOW                      AND
    #               RDC    LIKE     ?RDCLOW                       AND
    #               SCS    LIKE     ?SCSLOW                       AND
    #               SPC    LIKE     ?SPCLOW                       AND
    #               SSC    LIKE     ?SSCLOW                       AND
    #              (TN0    LIKE     ?TN0LOW                       OR
    #               TN1    LIKE     ?TN1LOW)                      AND
    #               ANDAY  LIKE     ?ANDAYLOW                     AND
    #               ANTM   LIKE     ?ANTMLOW                      AND
    #               CBTM   LIKE     ?CBTMLOW                      AND
    #               CCLS   LIKE     ?CCLSLOW                      AND
    #               CGF    LIKE     ?CGFLOW                       AND
    #==             CHGC   LIKE     ?CHGCLOW                      AND
    #               CHK    LIKE     ?CHKLOW                       AND
    #               CLR1   LIKE     ?CLR1LOW                      AND
    #               CLR2   LIKE     ?CLR2LOW                      AND
    #               CPI    LIKE     ?CPILOW                       AND
    #               DCC    LIKE     ?DCCLOW                       AND
    #               FLT    LIKE     ?FLTLOW                       AND
    #               FSC    LIKE     ?FSCLOW                       AND
    #               GW     LIKE     ?GWLOW                        AND
    #               ICI    LIKE     ?ICILOW                       AND
    #               IDSTA  LIKE     ?IDSTALOW                     AND
    #               IDSTN  LIKE     ?IDSTNLOW                     AND
    #               IO     LIKE     ?IOLOW                        AND
    #               IRTA   LIKE     ?IRTALOW                      AND
    #               ISG    LIKE     ?ISGLOW                       AND
    #               ISRTN  LIKE     ?ISRTNLOW                     AND
    #               ISTN   LIKE     ?ISTNLOW                      AND
    #               MA     LIKE     ?MALOW                        AND
    #               ODSTA  LIKE     ?ODSTALOW                     AND
    #               ODSTN  LIKE     ?ODSTNLOW                     AND
    #               OGTM   LIKE     ?OGTMLOW                      AND
    #               ORTA   LIKE     ?ORTALOW                      AND
    #               ORDAY  LIKE     ?ORDAYLOW                     AND
    #               ORTM   LIKE     ?ORTMLOW                      AND
    #               OSG    LIKE     ?OSGLOW                       AND
    #               OSTN   LIKE     ?OSTNLOW                      AND
    #               RAI    LIKE     ?RAILOW                       AND
    #               SUB    LIKE     ?SUBLOW                       AND
    #               TMR    LIKE     ?TMRLOW                       AND
    #==             UUIR   LIKE     ?UUIRLOW                      AND
    #==             UUIS   LIKE     ?UUISLOW                      AND
    #               VD     LIKE     ?VDLOW                        AND
    #               VDT    LIKE     ?VDTLOW                       AND
    #               VRTA   LIKE     ?VRTALOW)
    #       read uncommitted access
    # ;
    
    #  Without fix:  The following EXECUTE fails because s2       (BAD)
    #                  was not prepared.
    #  With fix:     0 rows selected.  No error.                  (GOOD)
    
    stmt = """DROP TABLE s0804ta;"""
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
    #  Test case name:         A05
    #  Description:
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:        (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """create table tf 
(col1 pic 9 default 0 not null) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table tr 
(col1 pic 9 default 0 not null
,col2 date default date '09/09/1990') no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into tf values (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tf values (2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into tr values (1, date '0001-01-01');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select tf.col1, tr.col2 from tf 
left join tr on (tf.col1 = tr.col1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    
    stmt = """select tf.col1, dateformat(tr.col2, default)
from tf left join tr 
on (tf.col1 = tr.col1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
    
    stmt = """create table test1 (c1 interval minute(3), c2 pic 9999) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into test1 values (interval '10' minute, 1000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # select c2 / ((c1 / 1)  UNITS minute) from test1;
    stmt = """select c2 / (cast (c1 as pic 9999) / 1)
from test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s5')
    
    # select c2 / ( C1 / (1 units minute)) from test1;
    
    # select 1 / (c1 units minute) from test1;
    stmt = """select 1 / (cast (c1 as pic 9999))
from test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s6')
    
    # select (1 / c1) units minute from test1;
    stmt = """select (1 / (cast (c1 as pic 9999)))
from test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s7')
    
    # select (1 units minute / c1)  from test1;
    # select c2 * (1 units minute / c1)  from test1;
    
    # select c2 *( 1 / (c1 units minute))  from test1;
    stmt = """select c2 * (1 / (cast (c1 as pic 9999)))
from test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s8')
    
    # select c2  / (c1 units minute)  from test1;
    stmt = """select c2 / (cast (c1 as pic 9999))
from test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s9')
    
    # select 1 * (c1 units minute) from test1;
    stmt = """select 1 * (cast (c1 as pic 9999))
from test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s10')
    
    # select 1.0 * (c1 units minute) from test1;
    stmt = """select 1.0 * (cast (c1 as pic 9(4)v9(4)))
from test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s11')
    
    # select 1.000 * (c1 units minute) from test1;
    stmt = """select 1.000 * (cast (c1 as pic 9(2)v9(2)))
from test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s12')
    
    # select 1 / (1.0 * (c1 units minute))  from test1;
    stmt = """select 1 / (1.0 * (cast (c1 as pic 9(2)v9(2))))
from test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s13')
    
    stmt = """drop table tf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table tr;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table test1;"""
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
    #  Test case name:         A06
    #  Description:
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:        (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
   
    stmt = """create table tdiv (a largeint,
b largeint) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
 
    stmt = """insert into tdiv 
values(24498000000,10106000000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """CREATE TABLE t1 (a int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE TABLE t2 (a int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE TABLE t3 (a int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO t2 values (2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # don't use err-msg because message text varies
    stmt = """select a, b, a/1 * b from tdiv;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    stmt = """INSERT INTO t3 (SELECT * FROM t1 
UNION ALL SELECT * FROM t2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """drop table tdiv;"""
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
    
    _testmgr.testcase_end(desc)

def test006(desc="""a07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:         A07
    #  Description:            Test for new UPDATE STATISTICS
    #          (1) Test for columns with different unique entry
    #              counts, including the boundary condition of a
    #              column containing only Nulls
    #          (2) Test for large table
    #          (3) Test for various data types
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:        (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    # 06/09/93 AC Creation
    
    #  clear tables and make sure we are running the new Update Statistics
    
    stmt = """create table t1 
(rowid int not null,
col0  int,              -- column with all null values
col1  int,              -- column with one value, no null
col1n int,              -- column with one vlaue, plus null
col2  int,              -- 2 values, no null
col2n int,              -- 2 values, with null
col3  int,              -- 3 values
col3n int,
col10 int,              -- 10 values
col10n int,
col110 int,             -- 110 values
col110n int,
primary key (rowid)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table t2            -- size
(rowid int not null,     -- primary key 4
col0  char(60),         -- column with all null values 62
col1  int,              -- column with one value, no null 6
col1n int,              -- column with one vlaue, plus null 6
col2  int,              -- 2 values, no null 6
col2n int,              -- 2 values, with null 6
col3  int,              -- 3 values 6
col3n int,              -- 6
col10 int,              -- 10 values 6
col10n int,             -- 6
col110 int,             -- 110 values 6
col110n int,            -- 6
primary key (rowid)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table t3                           --  size
(cid        smallint not null,           --     2
cchar      char(1000),                  --  1002
cvarchar   varchar(1000),               --  1004
cnumeric   numeric(18,5),               --    10
cint       int,                         --     6
clint      largeint,                    --    10
cfloat     float(54),                   --    10
creal      real,                        --     6
cdoublep   double precision,            --    10
cdecimal   decimal(18,2),               --    20
cdatetime  timestamp,                   --    13
ctimestmp  timestamp,                   --    13
cdate      date,                        --     6
ctime      time,                        --     5
cinterval  interval year to month,      --   ~20
primary key (cid)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # insert data
    
    stmt = """insert into t1 values( 1, null, 1, null, 1, null, 1, null,  1, null, 1, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 2, null, 1,    1, 2,    1, 2,    1,  2,    1, 2,    1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 3, null, 1,    1, 2,    2, 3,    2,  3,    2, 3,    2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 4, null, 1,    1, 2,    2, 3,    3,  4,    3, 4,    3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 5, null, 1,    1, 2,    2, 3,    3,  5,    4, 5,    4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 6, null, 1,    1, 2,    2, 3,    3,  6,    5, 6,    5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 7, null, 1,    1, 2,    2, 3,    3,  7,    6, 7,    6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 8, null, 1,    1, 2,    2, 3,    3,  8,    7, 8,    7);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 9, null, 1,    1, 2,    2, 3,    3,  9,    8, 9,    8);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values(10, null, 1,    1, 2,    2, 3,    3, 10,    9,10,    9);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values(11, null, 1,    1, 2,    2, 3,    3, 10,   10,11,   10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 12, null, 1, 1, 2, 2, 3, 3, 10, 10, 12, 11);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 13, null, 1, 1, 2, 2, 3, 3, 10, 10, 13, 12);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 14, null, 1, 1, 2, 2, 3, 3, 10, 10, 14, 13);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 15, null, 1, 1, 2, 2, 3, 3, 10, 10, 15, 14);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 16, null, 1, 1, 2, 2, 3, 3, 10, 10, 16, 15);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 17, null, 1, 1, 2, 2, 3, 3, 10, 10, 17, 16);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 18, null, 1, 1, 2, 2, 3, 3, 10, 10, 18, 17);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 19, null, 1, 1, 2, 2, 3, 3, 10, 10, 19, 18);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 20, null, 1, 1, 2, 2, 3, 3, 10, 10, 20, 19);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 21, null, 1, 1, 2, 2, 3, 3, 10, 10, 21, 20);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 22, null, 1, 1, 2, 2, 3, 3, 10, 10, 22, 21);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 23, null, 1, 1, 2, 2, 3, 3, 10, 10, 23, 22);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 24, null, 1, 1, 2, 2, 3, 3, 10, 10, 24, 23);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 25, null, 1, 1, 2, 2, 3, 3, 10, 10, 25, 24);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 26, null, 1, 1, 2, 2, 3, 3, 10, 10, 26, 25);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 27, null, 1, 1, 2, 2, 3, 3, 10, 10, 27, 26);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 28, null, 1, 1, 2, 2, 3, 3, 10, 10, 28, 27);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 29, null, 1, 1, 2, 2, 3, 3, 10, 10, 29, 28);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 30, null, 1, 1, 2, 2, 3, 3, 10, 10, 30, 29);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 31, null, 1, 1, 2, 2, 3, 3, 10, 10, 31, 30);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 32, null, 1, 1, 2, 2, 3, 3, 10, 10, 32, 31);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 33, null, 1, 1, 2, 2, 3, 3, 10, 10, 33, 32);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 34, null, 1, 1, 2, 2, 3, 3, 10, 10, 34, 33);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 35, null, 1, 1, 2, 2, 3, 3, 10, 10, 35, 34);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 36, null, 1, 1, 2, 2, 3, 3, 10, 10, 36, 35);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 37, null, 1, 1, 2, 2, 3, 3, 10, 10, 37, 36);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 38, null, 1, 1, 2, 2, 3, 3, 10, 10, 38, 37);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 39, null, 1, 1, 2, 2, 3, 3, 10, 10, 39, 38);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 40, null, 1, 1, 2, 2, 3, 3, 10, 10, 40, 39);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 41, null, 1, 1, 2, 2, 3, 3, 10, 10, 41, 40);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 42, null, 1, 1, 2, 2, 3, 3, 10, 10, 42, 41);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 43, null, 1, 1, 2, 2, 3, 3, 10, 10, 43, 42);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 44, null, 1, 1, 2, 2, 3, 3, 10, 10, 44, 43);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 45, null, 1, 1, 2, 2, 3, 3, 10, 10, 45, 44);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 46, null, 1, 1, 2, 2, 3, 3, 10, 10, 46, 45);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 47, null, 1, 1, 2, 2, 3, 3, 10, 10, 47, 46);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 48, null, 1, 1, 2, 2, 3, 3, 10, 10, 48, 47);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 49, null, 1, 1, 2, 2, 3, 3, 10, 10, 49, 48);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 50, null, 1, 1, 2, 2, 3, 3, 10, 10, 50, 49);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 51, null, 1, 1, 2, 2, 3, 3, 10, 10, 51, 50);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 52, null, 1, 1, 2, 2, 3, 3, 10, 10, 52, 51);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 53, null, 1, 1, 2, 2, 3, 3, 10, 10, 53, 52);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 54, null, 1, 1, 2, 2, 3, 3, 10, 10, 54, 53);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 55, null, 1, 1, 2, 2, 3, 3, 10, 10, 55, 54);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 56, null, 1, 1, 2, 2, 3, 3, 10, 10, 56, 55);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 57, null, 1, 1, 2, 2, 3, 3, 10, 10, 57, 56);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 58, null, 1, 1, 2, 2, 3, 3, 10, 10, 58, 57);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 59, null, 1, 1, 2, 2, 3, 3, 10, 10, 59, 58);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 60, null, 1, 1, 2, 2, 3, 3, 10, 10, 60, 59);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 61, null, 1, 1, 2, 2, 3, 3, 10, 10, 61, 60);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 62, null, 1, 1, 2, 2, 3, 3, 10, 10, 62, 61);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 63, null, 1, 1, 2, 2, 3, 3, 10, 10, 63, 62);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 64, null, 1, 1, 2, 2, 3, 3, 10, 10, 64, 63);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 65, null, 1, 1, 2, 2, 3, 3, 10, 10, 65, 64);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 66, null, 1, 1, 2, 2, 3, 3, 10, 10, 66, 65);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 67, null, 1, 1, 2, 2, 3, 3, 10, 10, 67, 66);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 68, null, 1, 1, 2, 2, 3, 3, 10, 10, 68, 67);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 69, null, 1, 1, 2, 2, 3, 3, 10, 10, 69, 68);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 70, null, 1, 1, 2, 2, 3, 3, 10, 10, 70, 69);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 71, null, 1, 1, 2, 2, 3, 3, 10, 10, 71, 70);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 72, null, 1, 1, 2, 2, 3, 3, 10, 10, 72, 71);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 73, null, 1, 1, 2, 2, 3, 3, 10, 10, 73, 72);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 74, null, 1, 1, 2, 2, 3, 3, 10, 10, 74, 73);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 75, null, 1, 1, 2, 2, 3, 3, 10, 10, 75, 74);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 76, null, 1, 1, 2, 2, 3, 3, 10, 10, 76, 75);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 77, null, 1, 1, 2, 2, 3, 3, 10, 10, 77, 76);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 78, null, 1, 1, 2, 2, 3, 3, 10, 10, 78, 77);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 79, null, 1, 1, 2, 2, 3, 3, 10, 10, 79, 78);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 80, null, 1, 1, 2, 2, 3, 3, 10, 10, 80, 79);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 81, null, 1, 1, 2, 2, 3, 3, 10, 10, 81, 80);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 82, null, 1, 1, 2, 2, 3, 3, 10, 10, 82, 81);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 83, null, 1, 1, 2, 2, 3, 3, 10, 10, 83, 82);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 84, null, 1, 1, 2, 2, 3, 3, 10, 10, 84, 83);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 85, null, 1, 1, 2, 2, 3, 3, 10, 10, 85, 84);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 86, null, 1, 1, 2, 2, 3, 3, 10, 10, 86, 85);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 87, null, 1, 1, 2, 2, 3, 3, 10, 10, 87, 86);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 88, null, 1, 1, 2, 2, 3, 3, 10, 10, 88, 87);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 89, null, 1, 1, 2, 2, 3, 3, 10, 10, 89, 88);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 90, null, 1, 1, 2, 2, 3, 3, 10, 10, 90, 89);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 91, null, 1, 1, 2, 2, 3, 3, 10, 10, 91, 90);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 92, null, 1, 1, 2, 2, 3, 3, 10, 10, 92, 91);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 93, null, 1, 1, 2, 2, 3, 3, 10, 10, 93, 92);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 94, null, 1, 1, 2, 2, 3, 3, 10, 10, 94, 93);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 95, null, 1, 1, 2, 2, 3, 3, 10, 10, 95, 94);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 96, null, 1, 1, 2, 2, 3, 3, 10, 10, 96, 95);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 97, null, 1, 1, 2, 2, 3, 3, 10, 10, 97, 96);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 98, null, 1, 1, 2, 2, 3, 3, 10, 10, 98, 97);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values( 99, null, 1, 1, 2, 2, 3, 3, 10, 10, 99, 98);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values(100, null, 1, 1, 2, 2, 3, 3, 10, 10,100, 99);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values(101, null, 1, 1, 2, 2, 3, 3, 10, 10,101,100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values(102, null, 1, 1, 2, 2, 3, 3, 10, 10,102,101);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values(103, null, 1, 1, 2, 2, 3, 3, 10, 10,103,102);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values(104, null, 1, 1, 2, 2, 3, 3, 10, 10,104,103);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values(105, null, 1, 1, 2, 2, 3, 3, 10, 10,105,104);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values(106, null, 1, 1, 2, 2, 3, 3, 10, 10,106,105);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values(107, null, 1, 1, 2, 2, 3, 3, 10, 10,107,106);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values(108, null, 1, 1, 2, 2, 3, 3, 10, 10,108,107);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values(109, null, 1, 1, 2, 2, 3, 3, 10, 10,109,108);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values(110, null, 1, 1, 2, 2, 3, 3, 10, 10,110,109);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t1 values(111, null, 1, 1, 2, 2, 3, 3, 10, 10,110,110);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into t2 values( 1, null, 1, null, 1, null, 1, null,  1, null, 1, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 2, null, 1,    1, 2,    1, 2,    1,  2,    1, 2,    1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 3, null, 1,    1, 2,    2, 3,    2,  3,    2, 3,    2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 4, null, 1,    1, 2,    2, 3,    3,  4,    3, 4,    3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 5, null, 1,    1, 2,    2, 3,    3,  5,    4, 5,    4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 6, null, 1,    1, 2,    2, 3,    3,  6,    5, 6,    5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 7, null, 1,    1, 2,    2, 3,    3,  7,    6, 7,    6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 8, null, 1,    1, 2,    2, 3,    3,  8,    7, 8,    7);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 9, null, 1,    1, 2,    2, 3,    3,  9,    8, 9,    8);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values(10, null, 1,    1, 2,    2, 3,    3, 10,    9,10,    9);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values(11, null, 1,    1, 2,    2, 3,    3, 10,   10,11,   10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 12, null, 1, 1, 2, 2, 3, 3, 10, 10, 12, 11);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 13, null, 1, 1, 2, 2, 3, 3, 10, 10, 13, 12);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 14, null, 1, 1, 2, 2, 3, 3, 10, 10, 14, 13);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 15, null, 1, 1, 2, 2, 3, 3, 10, 10, 15, 14);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 16, null, 1, 1, 2, 2, 3, 3, 10, 10, 16, 15);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 17, null, 1, 1, 2, 2, 3, 3, 10, 10, 17, 16);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 18, null, 1, 1, 2, 2, 3, 3, 10, 10, 18, 17);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 19, null, 1, 1, 2, 2, 3, 3, 10, 10, 19, 18);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 20, null, 1, 1, 2, 2, 3, 3, 10, 10, 20, 19);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 21, null, 1, 1, 2, 2, 3, 3, 10, 10, 21, 20);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 22, null, 1, 1, 2, 2, 3, 3, 10, 10, 22, 21);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 23, null, 1, 1, 2, 2, 3, 3, 10, 10, 23, 22);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 24, null, 1, 1, 2, 2, 3, 3, 10, 10, 24, 23);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 25, null, 1, 1, 2, 2, 3, 3, 10, 10, 25, 24);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 26, null, 1, 1, 2, 2, 3, 3, 10, 10, 26, 25);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 27, null, 1, 1, 2, 2, 3, 3, 10, 10, 27, 26);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 28, null, 1, 1, 2, 2, 3, 3, 10, 10, 28, 27);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 29, null, 1, 1, 2, 2, 3, 3, 10, 10, 29, 28);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 30, null, 1, 1, 2, 2, 3, 3, 10, 10, 30, 29);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 31, null, 1, 1, 2, 2, 3, 3, 10, 10, 31, 30);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 32, null, 1, 1, 2, 2, 3, 3, 10, 10, 32, 31);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 33, null, 1, 1, 2, 2, 3, 3, 10, 10, 33, 32);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 34, null, 1, 1, 2, 2, 3, 3, 10, 10, 34, 33);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 35, null, 1, 1, 2, 2, 3, 3, 10, 10, 35, 34);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 36, null, 1, 1, 2, 2, 3, 3, 10, 10, 36, 35);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 37, null, 1, 1, 2, 2, 3, 3, 10, 10, 37, 36);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 38, null, 1, 1, 2, 2, 3, 3, 10, 10, 38, 37);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 39, null, 1, 1, 2, 2, 3, 3, 10, 10, 39, 38);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 40, null, 1, 1, 2, 2, 3, 3, 10, 10, 40, 39);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 41, null, 1, 1, 2, 2, 3, 3, 10, 10, 41, 40);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 42, null, 1, 1, 2, 2, 3, 3, 10, 10, 42, 41);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 43, null, 1, 1, 2, 2, 3, 3, 10, 10, 43, 42);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 44, null, 1, 1, 2, 2, 3, 3, 10, 10, 44, 43);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 45, null, 1, 1, 2, 2, 3, 3, 10, 10, 45, 44);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 46, null, 1, 1, 2, 2, 3, 3, 10, 10, 46, 45);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 47, null, 1, 1, 2, 2, 3, 3, 10, 10, 47, 46);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 48, null, 1, 1, 2, 2, 3, 3, 10, 10, 48, 47);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 49, null, 1, 1, 2, 2, 3, 3, 10, 10, 49, 48);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 50, null, 1, 1, 2, 2, 3, 3, 10, 10, 50, 49);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 51, null, 1, 1, 2, 2, 3, 3, 10, 10, 51, 50);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 52, null, 1, 1, 2, 2, 3, 3, 10, 10, 52, 51);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 53, null, 1, 1, 2, 2, 3, 3, 10, 10, 53, 52);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 54, null, 1, 1, 2, 2, 3, 3, 10, 10, 54, 53);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 55, null, 1, 1, 2, 2, 3, 3, 10, 10, 55, 54);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 56, null, 1, 1, 2, 2, 3, 3, 10, 10, 56, 55);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 57, null, 1, 1, 2, 2, 3, 3, 10, 10, 57, 56);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 58, null, 1, 1, 2, 2, 3, 3, 10, 10, 58, 57);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 59, null, 1, 1, 2, 2, 3, 3, 10, 10, 59, 58);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 60, null, 1, 1, 2, 2, 3, 3, 10, 10, 60, 59);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 61, null, 1, 1, 2, 2, 3, 3, 10, 10, 61, 60);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 62, null, 1, 1, 2, 2, 3, 3, 10, 10, 62, 61);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 63, null, 1, 1, 2, 2, 3, 3, 10, 10, 63, 62);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 64, null, 1, 1, 2, 2, 3, 3, 10, 10, 64, 63);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 65, null, 1, 1, 2, 2, 3, 3, 10, 10, 65, 64);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 66, null, 1, 1, 2, 2, 3, 3, 10, 10, 66, 65);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 67, null, 1, 1, 2, 2, 3, 3, 10, 10, 67, 66);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 68, null, 1, 1, 2, 2, 3, 3, 10, 10, 68, 67);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 69, null, 1, 1, 2, 2, 3, 3, 10, 10, 69, 68);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 70, null, 1, 1, 2, 2, 3, 3, 10, 10, 70, 69);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 71, null, 1, 1, 2, 2, 3, 3, 10, 10, 71, 70);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 72, null, 1, 1, 2, 2, 3, 3, 10, 10, 72, 71);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 73, null, 1, 1, 2, 2, 3, 3, 10, 10, 73, 72);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 74, null, 1, 1, 2, 2, 3, 3, 10, 10, 74, 73);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 75, null, 1, 1, 2, 2, 3, 3, 10, 10, 75, 74);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 76, null, 1, 1, 2, 2, 3, 3, 10, 10, 76, 75);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 77, null, 1, 1, 2, 2, 3, 3, 10, 10, 77, 76);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 78, null, 1, 1, 2, 2, 3, 3, 10, 10, 78, 77);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 79, null, 1, 1, 2, 2, 3, 3, 10, 10, 79, 78);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 80, null, 1, 1, 2, 2, 3, 3, 10, 10, 80, 79);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 81, null, 1, 1, 2, 2, 3, 3, 10, 10, 81, 80);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 82, null, 1, 1, 2, 2, 3, 3, 10, 10, 82, 81);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 83, null, 1, 1, 2, 2, 3, 3, 10, 10, 83, 82);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 84, null, 1, 1, 2, 2, 3, 3, 10, 10, 84, 83);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 85, null, 1, 1, 2, 2, 3, 3, 10, 10, 85, 84);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 86, null, 1, 1, 2, 2, 3, 3, 10, 10, 86, 85);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 87, null, 1, 1, 2, 2, 3, 3, 10, 10, 87, 86);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 88, null, 1, 1, 2, 2, 3, 3, 10, 10, 88, 87);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 89, null, 1, 1, 2, 2, 3, 3, 10, 10, 89, 88);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 90, null, 1, 1, 2, 2, 3, 3, 10, 10, 90, 89);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 91, null, 1, 1, 2, 2, 3, 3, 10, 10, 91, 90);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 92, null, 1, 1, 2, 2, 3, 3, 10, 10, 92, 91);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 93, null, 1, 1, 2, 2, 3, 3, 10, 10, 93, 92);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 94, null, 1, 1, 2, 2, 3, 3, 10, 10, 94, 93);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 95, null, 1, 1, 2, 2, 3, 3, 10, 10, 95, 94);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 96, null, 1, 1, 2, 2, 3, 3, 10, 10, 96, 95);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 97, null, 1, 1, 2, 2, 3, 3, 10, 10, 97, 96);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 98, null, 1, 1, 2, 2, 3, 3, 10, 10, 98, 97);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values( 99, null, 1, 1, 2, 2, 3, 3, 10, 10, 99, 98);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values(100, null, 1, 1, 2, 2, 3, 3, 10, 10,100, 99);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values(101, null, 1, 1, 2, 2, 3, 3, 10, 10,101,100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values(102, null, 1, 1, 2, 2, 3, 3, 10, 10,102,101);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values(103, null, 1, 1, 2, 2, 3, 3, 10, 10,103,102);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values(104, null, 1, 1, 2, 2, 3, 3, 10, 10,104,103);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values(105, null, 1, 1, 2, 2, 3, 3, 10, 10,105,104);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values(106, null, 1, 1, 2, 2, 3, 3, 10, 10,106,105);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values(107, null, 1, 1, 2, 2, 3, 3, 10, 10,107,106);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values(108, null, 1, 1, 2, 2, 3, 3, 10, 10,108,107);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values(109, null, 1, 1, 2, 2, 3, 3, 10, 10,109,108);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values(110, null, 1, 1, 2, 2, 3, 3, 10, 10,110,109);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t2 values(111, null, 1, 1, 2, 2, 3, 3, 10, 10,110,110);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into t3 values(1, '  small char', '  small varchar',
-9999999999,    -32768,
-- -9999999999, -8.62e-75, -8.62e-75, -8.62e-75, -9999999999999999.99,
-9999999999, -8.62e-75, -3.4+38, -8.62e-75, -9999999999999999.99,
timestamp '0001-01-01:00:00:00.000000',
timestamp '0001-01-01:00:00:00.000000',
date '0001-01-01',
time '00:00:00', - interval '99' year);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into t3 values(2, 'Optimizer', 'Update Statistics', 123.456, 4567,
12345678, 10e10, 99e-2, 45e6, -0.12,
timestamp '1993-01-01:20:30:00.000000',
timestamp '1993-06-10:09:43:05.000000',
date '1993-05-11',
time '09:50:00', interval '5' month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into t3 values(3, 'Executor', 'New Update Statistics', 777.888, 4567,
87654321,  5e10, 99e2, 45e-6, 100.12,
timestamp '1993-05-11:09:29:00.000000',
timestamp '1993-06-25:19:30:00.000000',
date '1993-05-05',
time '00:13:05', interval '3' month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into t3 values(4, 'zzzzzzzzzzzz', 'zzzzzzzzzzzzzzz',
9999999999, 32767,
--  99999999999, 1.16e75, 1.16e75, 1.16e75, 9999999999999999.99,
99999999999, 1.16e75, 3.4e38, 1.16e75, 9999999999999999.99,
timestamp '3999-12-31:23:59:59.999999',
timestamp '3999-12-31:23:59:59.999999',
date '3999-12-31',
-- time '23:59:59', - interval '90' year);
time '23:59:59', interval - '90' year);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  test the data
    stmt = """select * from t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s3')
    stmt = """select * from t2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s4')
    stmt = """select * from t3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    # TEST 1: Update Statistics for Columns with Different Unique Entry Counts
    # test new update statistics against small table, with the number of
    #   distinct values (not counting Null) of the coulumns equal to
    #   0, 1, 2, 3, 10 and 110; the effect of the presence of Null is also
    #   tested
    
    stmt = """delete from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update statistics for table t1 on (rowid, col10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  select colname, uniqueentrycount, secondhighvalue, secondlowvalue
    #  from columns
    #  where tablename like '%.T1 %';
    
    # select colname, uniqueentrycount, HIGH_VALUE, LOW_VALUE
    # from columns
    # where tablename like '%.T1 %';
    
    stmt = """select HIGH_VALUE, LOW_VALUE from """ + gvars.histograms + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #
    # TEST 2: Update Statistics for Large Table, with Diff. Options
    #
    # test new update statistics against large table (about 10K bytes)
    #   the numbers of distinct values are the same as that of test 1
    # the options of EXACT, SAMPLE  BLOCK 1, BLOCK 3, and BlOCK 6 are tested
    
    # update statistics with default options
    
    stmt = """update statistics for table t2 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #select colname, uniqueentrycount, secondhighvalue, secondlowvalue
    #from columns
    #where tablename like '%.T2 %';
    
    # update statistics exact
    # update statistics for table t2 exact;
    
    #select colname, uniqueentrycount, secondhighvalue, secondlowvalue
    #from columns
    #where tablename like '%.T2 %';
    
    # update statistics sample 1 blocks (< table size)
    #$SQL_complete_msg
    # update statistics for table t2 sample 1 blocks;
    
    stmt = """update statistics for table t2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update statistics for table t2 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #select colname, uniqueentrycount, secondhighvalue, secondlowvalue
    #from columns
    #where tablename like '%.T2 %';
    
    # update statistics sample 3 blocks (< table size)
    # update statistics for table t2 sample 3 blocks;
    stmt = """update statistics for table t2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #select colname, uniqueentrycount, secondhighvalue, secondlowvalue
    #from columns
    #where tablename like '%.T2 %';
    
    # update statistics sample 6 blocks (> table size)
    
    stmt = """update statistics for table t2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update statistics for table t2 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #select colname, uniqueentrycount, secondhighvalue, secondlowvalue
    #from columns
    #where tablename like '%.T2 %';
    
    #
    # TEST 3: Update Statistics for Various Data Types
    #
    # test Update Statistics against various data type
    
    stmt = """update statistics for table t3 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #select colname, uniqueentrycount, secondhighvalue, secondlowvalue
    #from columns
    #where tablename like '%.T3 %';
    
    # clean up
    stmt = """drop table t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table t2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table t3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test007(desc="""a09"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:         A09
    #  Description:
    #  Description:            Key predicate optimization tests
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:        (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    stmt = """DROP   TABLE s0809ta;"""
    output = _dci.cmdexec(stmt)
    
    # Create tables.
    
    stmt = """CREATE TABLE s0809ta (
a INTEGER NOT NULL,
b INTEGER NOT NULL,
c INTEGER,
v VARCHAR(5),
--                      t DATETIME HOUR TO MINUTE,
t TIME,
PRIMARY KEY ( a, b )
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #                        catalog
    
    stmt = """INSERT INTO s0809ta VALUES( 1, 0, 2, '102', time '01:02:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0809ta VALUES( 1, 1, 2, '112', time '01:12:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0809ta VALUES( 1, 2, 2, '122', time '01:22:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0809ta VALUES( 2, 0, 1, '201', time '02:01:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0809ta VALUES( 2, 1, 1, '211', time '02:11:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0809ta VALUES( 2, 2, 1, '221', time '02:21:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0809ta VALUES( 2, 3, 1, '231', time '02:31:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0809ta VALUES( 2, 4, 1, '241', time '02:41:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0809ta VALUES( 3, 0, 0, '300', time '03:00:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0809ta VALUES( 3, 1, 0, '310', time '03:10:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0809ta VALUES( 3, 2, 0, '320', time '03:20:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0809ta VALUES( 3, 3, 0,  NULL, time '03:30:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0809ta VALUES( 3, 4, 0,  NULL, time '03:40:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
   
    stmt = """CREATE INDEX s0809tai ON s0809ta(t,v);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #---------------
    # s0809(s101) --
    #---------------
    #  When the redundant predicate was on a key column which was
    #    not the last in the index, wrong results were produced.
    
    stmt = """prepare s101 from
SELECT x.a, y.a, x.b, y.b
FROM s0809ta x, s0809ta y
WHERE x.a < y.a
AND y.a > x.a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s101;
    
    # --------
    #   Good:  One pred is used as end key;
    #            the other pred becomes a base table predicate.
    #            Index selectivity: 33.33%     Total cost: 135
    #   Bad:   Both preds used as end-key.
    #            Index selectivity:  0%        Total cost:  19
    # --------
    
    stmt = """execute s101;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s2')
    #--------
    #  Good:  55 rows.
    #  Bad:   83 rows.
    #             (Erroneously selects some rows where x.a = y.a)
    #--------
    
    #---------------
    # s0809(s102) --
    #---------------
    #  Like s101, but predicates given in the opposite order.
    
    stmt = """prepare s102 from
SELECT x.a, y.a, x.b, y.b
FROM s0809ta x, s0809ta y
WHERE y.a > x.a
AND x.a < y.a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s102;
    
    # --------
    #   Good:  One pred is used as end key;
    #            the other pred becomes a base table predicate.
    #            Index selectivity: 33.33%     Total cost: 135
    #   Bad:   Both preds used as end-key.
    #            Index selectivity:  0%        Total cost:  19
    # --------
    
    stmt = """execute s102;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s4')
    #--------
    #  Good:  55 rows.
    #  Bad:   83 rows.
    #             (Erroneously selects some rows where x.a = y.a)
    #--------
    
    #---------------
    # s0809(s103) --
    #---------------
    #  Like s101, but predicates are inverted.
    
    stmt = """prepare s103 from
SELECT x.a, y.a, x.b, y.b
FROM s0809ta x, s0809ta y
WHERE x.a > y.a
AND y.a < x.a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s103;
    
    # --------
    #   Good:  One pred is used as begin key;
    #            the other pred becomes a base table predicate.
    #            Index selectivity: 33.33%     Total cost: 135
    #   Bad:   Both preds used as begin-key.
    #            Index selectivity:  0%        Total cost:  19
    # --------
    
    stmt = """execute s103;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s6')
    #--------
    #  Good:  55 rows.
    #  Bad:   73 rows.
    #             (Erroneously selects some rows where x.a = y.a)
    #--------
    
    #---------------
    # s0809(s104) --
    #---------------
    #  Like s101, but predicates are inverted and given in opposite order.
    
    stmt = """prepare s104 from
SELECT x.a, y.a, x.b, y.b
FROM s0809ta x, s0809ta y
WHERE y.a < x.a
AND x.a > y.a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s104;
    
    # --------
    #   Good:  One pred is used as begin key;
    #            the other pred becomes a base table predicate.
    #            Index selectivity: 33.33%     Total cost: 135
    #   Bad:   Both preds used as begin-key.
    #            Index selectivity:  0%        Total cost:  19
    # --------
    
    stmt = """execute s104;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s8')
    #--------
    #  Good:  55 rows.
    #  Bad:   73 rows.
    #             (Erroneously selects some rows where x.a = y.a)
    #--------
    
    #---------------
    # s0809(s105) --
    #---------------
    #  Like s101, but includes preds along with their inverses.
    #  Note the old SQLCOMP would give correct results for this
    #    query if the 2nd and 3rd predicates were swapped.
    
    stmt = """prepare s105 from
SELECT x.a, y.a, x.b, y.b
FROM s0809ta x, s0809ta y
WHERE x.a <= y.a
AND y.a >= x.a
AND x.a >= y.a
AND y.a <= x.a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s105;
    
    # --------
    #   Good:  One pred is used as begin-key, another as end-key.
    #            (The other two become base table predicates.)
    #            Index selectivity: 20%        Total cost:  88
    #   Bad:   Two preds used as begin-key, none used as end-key.
    #            (The other two become base table predicates.)
    #            Index selectivity:  0%        Total cost:  19
    # --------
    
    stmt = """execute s105;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s10')
    #--------
    #  Good:  59 rows.
    #  Bad:   31 rows.
    #             (Erroneously omits some rows where x.a = y.a)
    #--------
    
    #---------------
    # s0809(s106) --
    #---------------
    #  Like s105, but preds are given in reverse order.
    #  Note the old SQLCOMP would give correct results for this
    #    query if the 2nd and 3rd predicates were swapped.
    
    stmt = """prepare s106 from
SELECT x.a, y.a, x.b, y.b
FROM s0809ta x, s0809ta y
WHERE y.a <= x.a
AND x.a >= y.a
AND y.a >= x.a
AND x.a <= y.a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s106;
    
    # --------
    #   Good:  One pred is used as begin-key, another as end-key.
    #            (The other two become base table predicates.)
    #            Index selectivity: 20%        Total cost:  88
    #   Bad:   Two preds used as end-key, none used as begin-key.
    #            (The other two become base table predicates.)
    #            Index selectivity:  0%        Total cost:  19
    # --------
    
    stmt = """execute s106;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s12')
    #--------
    #  Good:  59 rows.
    #  Bad:   41 rows.
    #             (Erroneously omits some rows where x.a = y.a)
    #--------
    
    #---------------
    # s0809(s107) --
    #---------------
    #  When the redundant predicate was on the last key column
    #    of the index, SQLCOMP croaked in the Generator.
    
    stmt = """prepare s107 from
SELECT x.b, y.b
FROM s0809ta x, s0809ta y
WHERE x.b < y.b
AND y.b > x.b
AND x.a = y.a
AND y.a = 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    # --------
    #   Good:  SQL command prepared.
    #   Bad:   Error [-7001]: The SQL compiler generator detected
    #            an inconsistent internal data structure.
    # --------
    
    #   explain s107;
    
    # --------
    #   Good:  'y.b > x.b' used in end key;
    #          'x.b < y.b' becomes a base table predicate.
    #            Index selectivity: 0.3333%    Total cost: 1
    #   Bad:   Error [-10702]: Statement s107 has not been prepared.
    # --------
    
    stmt = """execute s107;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s14')
    #--------
    #  Good:  10 rows.
    #  Bad:   Error [-10043]: Statement name has not been
    #           successfully prepared.
    #--------
    
    #---------------
    # s0809(s108) --
    #---------------
    #  Like s107, but with predicates inverted.
    
    stmt = """prepare s108 from
SELECT x.b, y.b
FROM s0809ta x, s0809ta y
WHERE x.b > y.b
AND y.b < x.b
AND x.a = y.a
AND y.a = 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    # --------
    #   Good:  SQL command prepared.
    #   Bad:   Error [-8041]: Unable to communicate
    #            with the SQL compiler process.
    # --------
    
    #   explain s108;
    
    # --------
    #   Good:  'y.b < x.b' used in begin key;
    #          'x.b > y.b' becomes a base table predicate.
    #            Index selectivity: 0.3333%    Total cost: 1
    #   Bad:   Error [-10702]: Statement s108 has not been prepared.
    # --------
    
    stmt = """execute s108;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s16')
    #--------
    #  Good:  10 rows.
    #  Bad:   Error [-10043]: Statement name has not been
    #           successfully prepared.
    #--------
    
    #---------------
    # s0809(s109) --
    #---------------
    #  Just to demonstrate that the problem could occur even
    #    when there were no redundant predicates in the original query.
    
    stmt = """prepare s109 from
SELECT x.a, y.a, x.b, y.b
FROM s0809ta x, s0809ta y
WHERE y.a < x.a
AND x.a > 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s109;
    
    # --------
    #   Good:  'x.a > 1'   is begin key for x,
    #          'y.a < x.a' is end key for y.
    #            Index selectivity: 33.33%     Total cost:  45
    #   Bad:   Both preds used as begin-key for x.  No key preds for y.
    #            Index selectivity:  0%        Total cost:  19
    # --------
    
    stmt = """execute s109;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s18')
    #--------
    #  Good:  55 rows.
    #  Bad:   88 rows.
    #             (Erroneously selects some rows where x.a = y.a,
    #                                   and some where x.a = 1)
    #--------
    
    #---------------
    # s0809(s110) --
    #---------------
    #  Like s109, but predicates inverted.
    
    stmt = """prepare s110 from
SELECT x.a, y.a, x.b, y.b
FROM s0809ta x, s0809ta y
WHERE y.a > x.a
AND x.a < 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s110;
    
    #--------
    #  Good:  'x.a < 1'   is end key for x,
    #         'y.a > x.a' is begin key for y.
    #           Index selectivity: 33.33%     Total cost:  45
    #  Bad:   Both preds used as end-key for x.  No key preds for y.
    #           Index selectivity:  0%        Total cost:  19
    #--------
    
    stmt = """execute s110;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #--------
    #  Good:   0 rows.
    #  Bad:   68 rows.
    #             (Erroneously selects some rows where x.a = y.a,
    #                                   and some where x.a >= 1)
    #--------
    
    #---------------
    # s0809(s111) --
    #---------------
    #  Like s109, but predicates in reverse order.
    #  Same results as s109.
    
    stmt = """prepare s111 from
SELECT x.a, y.a, x.b, y.b
FROM s0809ta x, s0809ta y
WHERE x.a > 1
AND y.a < x.a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s111;
    
    # --------
    #   Good:  'x.a > 1'   is begin key for x,
    #          'y.a < x.a' is end key for y.
    #            Index selectivity: 33.33%     Total cost:  45
    #   Bad:   Both preds used as begin-key for x.  No key preds for y.
    #            Index selectivity:  0%        Total cost:  19
    # --------
    
    stmt = """execute s111;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s21')
    #--------
    #  Good:  55 rows.
    #  Bad:   88 rows.
    #             (Erroneously selects some rows where x.a = y.a,
    #                                   and some where x.a = 1)
    #--------
    
    #---------------
    # s0809(s112) --
    #---------------
    #  Like s109, but predicates inverted and in reverse order.
    #  Same results as s110.
    
    stmt = """prepare s112 from
SELECT x.a, y.a, x.b, y.b
FROM s0809ta x, s0809ta y
WHERE x.a < 1
AND y.a > x.a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s112;
    
    #--------
    #  Good:  'x.a < 1'   is end key for x,
    #         'y.a > x.a' is begin key for y.
    #           Index selectivity: 33.33%     Total cost:  45
    #  Bad:   Both preds used as end-key for x.  No key preds for y.
    #           Index selectivity:  0%        Total cost:  19
    #--------
    
    stmt = """execute s112;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #--------
    #  Good:   0 rows.
    #  Bad:   68 rows.
    #             (Erroneously selects some rows where x.a = y.a,
    #                                   and some where x.a >= 1)
    #--------
    
    #---------------
    # s0809(s113) --
    #---------------
    #  Try multi-value predicate...
    #  The predicate includes the last key column, so this is
    #  another case where the Generator got an internal error.
    
    stmt = """prepare s113 from
SELECT x.a, y.a, x.b, y.b
FROM s0809ta x, s0809ta y
WHERE (x.a, x.b) < (y.a, y.b)
AND (y.a, y.b) > (x.a, x.b)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    # --------
    #   Good:  SQL command prepared.
    #   Bad:   Error [-7001]: The SQL compiler generator detected
    #            an inconsistent internal data structure.
    # --------
    
    #   explain s113;
    
    # --------
    #   Good:  One pred is used as end key;
    #            the other pred becomes a base table predicate.
    #            Index selectivity: 11.11%     Total cost: 135
    #   Bad:   Error [-10702]: Statement s113 has not been prepared.
    # --------
    
    #   execute s113;
    
    #--------
    #  Good:  78 rows.
    #  Bad:   Error [-10043]: Statement name has not been
    #           successfully prepared.
    #--------
    
    #---------------
    # s0809(s114) --
    #---------------
    #  What happens if the column with the redundant predicate is
    #    followed, in the index key, by a column of a different data type?
    #  This test uses index s0809tai(t,v,...).   v is varchar, t is datetime
    
    stmt = """prepare s114 from
SELECT x.t, y.t
FROM s0809ta x, s0809ta y
WHERE x.t < y.t
AND y.t > x.t
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    # --------
    #   Good:  SQL command prepared.
    #   Bad:   Error [-7001]: The SQL compiler generator detected
    #            an inconsistent internal data structure.
    # --------
    
    #   explain s114;
    
    # --------
    #   Good:  One pred is used as end key;
    #            the other pred becomes an index predicate.
    #            Index selectivity: 33.33%     Total cost: 135
    #   Bad:   Error [-10702]: Statement s114 has not been prepared.
    # --------
    
    stmt = """execute s114;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s26')
    
    #--------
    #  Good:  78 rows.
    #  Bad:   Error [-10043]: Statement name has not been prepared.
    #--------
    
    #---------------
    # s0809(s115) --
    #---------------
    #  Join on 'problem' GMT datetime column.
    #  This test case revealed a problem with GENT^PROCESS^DATETIME^KEYS:
    #  File system error 1024 (subset not defined) when EVAA^SCCU called
    #  DM^KEYPOSITION for the inner table.
    
    stmt = """prepare s115 from
SELECT x.t, y.t
FROM s0809ta x, s0809ta y
WHERE x.t < y.t
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f'  s115;"""
    output = _dci.cmdexec(stmt)
    
    # --------
    #   (Predicate is used as end key for the inner scan.)
    # --------
    
    stmt = """execute s115;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s28')
    #--------
    #  Good:  78 rows.
    #  Bad:   Error from SQL [-8300]: File system error occurred on S0809TA.
    #         Error from File System [1024]: The specified SQL subset is not
    #           defined to the File System.
    #--------
    
    #---------------
    # s0809(s201) --
    #---------------
    #  Predicate is >=
    
    stmt = """prepare s201 from
SELECT a,b
FROM s0809ta 
WHERE (a,b) >= (b,a)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s201;
    
    # --------
    #   Good:  Predicate is applied upon the base table.  No key preds.
    #            Index selectivity: 100%       Total cost:   4
    #   Bad:   Predicate used as begin-key.
    #            Index selectivity:  33.3267%  Total cost:   2
    # --------
    
    stmt = """execute s201;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s30')
    #--------
    #  Good:   9 rows.
    #  Bad:    0 or 13 rows, or internal error -8420.   (unpredictable)
    #--------
    
    #---------------
    # s0809(s202) --
    #---------------
    #  Predicate is <=
    
    stmt = """prepare s202 from
SELECT a,b
FROM s0809ta 
WHERE (a,b) <= (b,a)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s202;
    
    # --------
    #   Good:  Predicate is applied upon the base table.  No key preds.
    #            Index selectivity: 100%       Total cost:   4
    #   Bad:   Predicate used as end-key.
    #            Index selectivity:  33.3267%  Total cost:   2
    # --------
    
    stmt = """execute s202;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s32')
    #--------
    #  Good:   7 rows.
    #  Bad:    0 or 13 rows, or internal error -8420.   (unpredictable)
    #--------
    
    #---------------
    # s0809(s203) --
    #---------------
    #  Predicate is >
    
    stmt = """prepare s203 from
SELECT a,b
FROM s0809ta 
WHERE (a,b) > (b,a)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s203;
    
    # --------
    #   Good:  Predicate is applied upon the base table.  No key preds.
    #            Index selectivity: 100%       Total cost:   4
    #   Bad:   Predicate used as begin-key.
    #            Index selectivity:  33.3267%  Total cost:   2
    # --------
    
    stmt = """execute s203;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s34')
    #--------
    #  Good:   6 rows.
    #  Bad:    0 rows.
    #--------
    
    #---------------
    # s0809(s204) --
    #---------------
    #  Predicate is <
    
    stmt = """prepare s204 from
SELECT a,b
FROM s0809ta 
WHERE (a,b) < (b,a)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s204;
    
    # --------
    #   Good:  Predicate is applied upon the base table.  No key preds.
    #            Index selectivity: 100%       Total cost:   4
    #   Bad:   Predicate used as end-key.
    #            Index selectivity:  33.3267%  Total cost:   2
    # --------
    
    stmt = """execute s204;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s36')
    #--------
    #  Good:   4 rows.
    #  Bad:    0 or 13 rows, or internal error -8420.   (unpredictable)
    #--------
    
    #---------------
    # s0809(s205) --
    #---------------
    #  Try redundant predicate.
    
    stmt = """prepare s205 from
SELECT a, b
FROM s0809ta 
WHERE (a,b) < (b,a)
AND (b,a) > (a,b)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s205;
    
    # --------
    #   Good:  Predicate is applied upon the base table.  No key preds.
    #            Index selectivity: 100%       Total cost:   4
    #   Bad:   One pred used as begin-key, other pred used as end-key.
    #            Index selectivity:  20%       Total cost:   1
    # --------
    
    stmt = """execute s205;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s38')
    #--------
    #  Good:   4 rows.
    #  Bad:    0 or 13 rows, or internal error -8420.   (unpredictable)
    #--------
    
    #---------------
    # s0809(s206) --
    #---------------
    #  Try low-bound & high-bound predicates.
    
    stmt = """prepare s206 from
SELECT a, b
FROM s0809ta 
WHERE (a,b) >= (b,a)
AND (b,a) >= (a,b)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s206;
    
    # --------
    #   Good:  Predicate is applied upon the base table.  No key preds.
    #            Index selectivity: 100%       Total cost:   4
    #   Bad:   One pred used as begin-key.  The other is base table pred.
    #            Index selectivity:  33.3267%  Total cost:   2
    # --------
    
    stmt = """execute s206;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s40')
    #--------
    #  Good:   3 rows.
    #  Bad:    0 or 13 rows, or internal error -8420.   (unpredictable)
    #--------
    
    #---------------
    # s0809(s207) --
    #---------------
    #  Try expression in multi-value predicate.
    #    (Strangely, this did not provoke SQLCOMP internal error -6010)
    
    stmt = """prepare s207 from
SELECT a, b, c+1
FROM s0809ta 
WHERE (a,b) < (b, c+1)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s207;
    
    # --------
    #   Good:  Predicate is applied upon the base table.  No key preds.
    #            Index selectivity:  33.3333%  Total cost:   4
    #   Bad:   Predicate used as begin-key.
    #            Index selectivity:  33.3267%  Total cost:   2
    # --------
    
    stmt = """execute s207;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s42')
    #--------
    #  Good:   5 rows.
    #  Bad:    0 or 13 rows, or internal error -8420.   (unpredictable)
    #--------
    
    #---------------
    # s0809(s301) --
    #---------------
    #  col1,...,colN  relop  colexpr1,...colexprN
    #
    #  colexprs belonging to same table
    
    stmt = """prepare s301 from
SELECT x.a, x.b, y.a, y.b
FROM s0809ta x, s0809ta y
WHERE (x.a,x.b) >= (y.a+2,y.b*2)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    # --------
    #   Good:  SQL command prepared.
    #   Bad:   Error [-6010]: Internal error: The SQL compiler
    #            detected an inconsistent internal data structure.
    # --------
    
    #   explain s301;
    
    # --------
    #   Good:  Predicate used as begin-key.
    #            Index selectivity:  33.3333%  Total cost: 135
    #   Bad:   Error [-10702]: Statement s301 has not been prepared.
    # --------
    
    stmt = """execute s301;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s44')
    #--------
    #  Good:  9 rows.
    #  Bad:   Error [-10043]: Statement name has not been
    #           successfully prepared.
    #--------
    
    #---------------
    # s0809(s302) --
    #---------------
    #  k1,...,kN  relop  colexpr1,...colexprN
    #
    #  colexprs belonging to same table
    
    stmt = """prepare s302 from
SELECT x.a, x.b, y.a, y.b
FROM s0809ta x, s0809ta y
WHERE (2,2) >= (x.a+1,x.b*2)
AND x.a = y.a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    # --------
    #   Good:  SQL command prepared.
    #   Bad:   Error [-6010]: Internal error: The SQL compiler
    #            detected an inconsistent internal data structure.
    # --------
    
    #   explain s302;
    
    # --------
    #   Good:  Key pred: x.a = y.a      Base table pred: (2,2) >= (...)
    #            Index selectivity:   1%       Total cost:  9
    #   Bad:   Error [-10702]: Statement s302 has not been prepared.
    # --------
    
    stmt = """execute s302;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s46')
    #--------
    #  Good:  6 rows.
    #  Bad:   Error [-10043]: Statement name has not been
    #           successfully prepared.
    #--------
    
    #---------------
    # s0809(s303) --
    #---------------
    #  colexpr1,...colexprN  relop  anyexpr1,...,anyexprN
    #
    #  colexprs belonging to same table
    
    stmt = """prepare s303 from
SELECT x.a, x.b, y.a, y.b
FROM s0809ta x, s0809ta y
WHERE (y.a-1,y.b*2) > (x.b*2,x.a+1)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    # --------
    #   Good:  SQL command prepared.
    #   Bad:   Error [-6010]: Internal error: The SQL compiler
    #            detected an inconsistent internal data structure.
    # --------
    
    #   explain s303;
    
    # --------
    #   Good:  Predicate evaluated upon the base table.  No key preds.
    #            Index selectivity: 100%       Total cost: 376
    #   Bad:   Error [-10702]: Statement s303 has not been prepared.
    
    stmt = """execute s303;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s48')
    #--------
    #  Good:  40 rows.
    #  Bad:   Error [-10043]: Statement name has not been
    #           successfully prepared.
    #--------
    
    #---------------
    # s0809(s304) --
    #---------------
    #  col1,...,colN  relop  colexpr1,...colexprN
    #
    #  colexprs belonging to different tables
    
    stmt = """prepare s304 from
SELECT x.a, x.b, y.a, y.b
FROM s0809ta x, s0809ta y
WHERE (x.a,x.b) >= (y.a+2,x.b*2)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    # --------
    #   Good:  SQL command prepared.
    #   Bad:   Error [-6010]: Internal error: The SQL compiler
    #            detected an inconsistent internal data structure.
    # --------
    
    #   explain s304;
    
    # --------
    #   Good:  Predicate evaluated upon index-only scan.  No key preds.
    #            Index selectivity: 100%       Total cost: 376
    #   Bad:   Error [-10702]: Statement s304 has not been prepared.
    # --------
    
    stmt = """execute s304;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s50')
    #--------
    #  Good:  3 rows.
    #  Bad:   Error [-10043]: Statement name has not been
    #           successfully prepared.
    #--------
    
    #---------------
    # s0809(s305) --
    #---------------
    #  k1,...,kN  relop  colexpr1,...colexprN
    #
    #  colexprs belonging to different tables
    
    stmt = """prepare s305 from
SELECT x.a, x.b, y.a, y.b
FROM s0809ta x, s0809ta y
WHERE (2,2) >= (x.a+1,y.b*2)
AND x.a = y.a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    # --------
    #   Good:  SQL command prepared.
    #   Bad:   Error [-6010]: Internal error: The SQL compiler
    #            detected an inconsistent internal data structure.
    # --------
    
    #   explain s305;
    
    # --------
    #   Good:  Key pred: x.a = y.a      Base table pred: (2,2) >= (...)
    #            Index selectivity:   1%       Total cost:  19
    #   Bad:   Error [-10702]: Statement s305 has not been prepared.
    # --------
    
    stmt = """execute s305;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s52')
    #--------
    #  Good:  6 rows.
    #  Bad:   Error [-10043]: Statement name has not been
    #           successfully prepared.
    #--------
    
    #---------------
    # s0809(s306) --
    #---------------
    #  colexpr1,...colexprN  relop  anyexpr1,...,anyexprN
    #
    #  colexprs belonging to different tables
    
    stmt = """prepare s306 from
SELECT x.a, x.b, y.a, y.b
FROM s0809ta x, s0809ta y
WHERE (y.a-1,x.b*2) > (x.b*2,y.a+1)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    # --------
    #   Good:  SQL command prepared.
    #   Bad:   Error [-6010]: Internal error: The SQL compiler
    #            detected an inconsistent internal data structure.
    # --------
    
    #   explain s306;
    
    # --------
    #   Good:  Predicate evaluated upon index-only scan.  No key preds.
    #            Index selectivity: 100%       Total cost: 376
    #   Bad:   Error [-10702]: Statement s306 has not been prepared.
    # --------
    
    stmt = """execute s306;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s54')
    #--------
    #  Good:  30 rows.
    #  Bad:   Error [-10043]: Statement name has not been
    #           successfully prepared.
    #--------
    
    #---------------
    # s0809(s401) --
    #---------------
    #  col1,...,colN  relop  colexpr1,...colexprN          ==> wrong result
    #
    #  This case is exceptionally strange because OPTU^BUILD^KEYS sees the
    #    column nodes on the lhs and assumes they are the key columns,
    #    although the rhs columns are the ones that have been erroneously
    #    matched with the key column list by OPTA^ANALYZE^INDEX^PREDS.
    
    stmt = """prepare s401 from
SELECT b, a, b-1
FROM s0809ta 
WHERE (b,a) <= (a-1,b+1)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s401;
    
    # --------
    #   Good:  Predicate is applied upon the base table.  No key preds.
    #            Index selectivity: 100%       Total cost:   4
    #   Bad:   Predicate used as begin-key.
    #            Index selectivity:  33.3267%  Total cost:   2
    # --------
    
    stmt = """execute s401;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s56')
    #--------
    #  Good:  6 rows.
    #  Bad:   0 or 13 rows, or internal error -8420.   (unpredictable)
    #--------
    
    #---------------
    # s0809(s402) --
    #---------------
    #  k1,...,kN  relop  colexpr1,...colexprN    ==> SQLCOMP abend
    #                                                  (trap in OPTU^BUILD^KEYS)
    
    stmt = """prepare s402 from
SELECT a, b
FROM s0809ta 
WHERE (2,2) < (a,b+1)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    # --------
    #   Good:  SQL command prepared.
    #   Bad:   Error [-8041]: Unable to communicate
    #            with the SQL compiler process.
    # --------
    
    #   explain s402;
    
    # --------
    #   Good:  Predicate used as begin-key.
    #            Index selectivity: 100%       Total cost: 4
    #   Bad:   Error [-10702]: Statement s402 has not been prepared.
    # --------
    
    stmt = """execute s402;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s58')
    #--------
    #  Good:  8 rows.
    #  Bad:   Error [-10043]: Statement name has not been
    #           successfully prepared.
    #--------
    
    #---------------
    # s0809(s403) --
    #---------------
    #  colexpr1,...colexprN  relop  anyexpr1,...,anyexprN   ==> SQLCOMP abend
    
    stmt = """prepare s403 from
SELECT a, b
FROM s0809ta 
WHERE (a,b+1) < (2,2)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    # --------
    #   Good:  SQL command prepared.
    #   Bad:   Error [-8041]: Unable to communicate
    #            with the SQL compiler process.
    # --------
    
    #   explain s403;
    
    # --------
    #   Good:  Predicate evaluated upon the base table.
    #            Index selectivity: 100%       Total cost: 4
    #   Bad:   Error [-10702]: Statement s403 has not been prepared.
    # --------
    
    stmt = """execute s403;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s60')
    #--------
    #  Good:  4 rows.
    #  Bad:   Error [-10043]: Statement name has not been
    #           successfully prepared.
    #--------
    
    #---------------
    # s0809(s501) --
    #---------------
    #  This test uses index S0809TAI on S0809TA(t,v)
    
    stmt = """prepare s501 from
SELECT t,v
FROM s0809ta 
--     WHERE t = DATETIME '3:30' HOUR TO MINUTE
WHERE t = TIME '03:30:00'
AND v IS NULL
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    # --------
    #   Good:  SQL command prepared.
    #   Bad:   Error [-7004]: Internal error: The SQL compiler generator
    #            encountered an invalid value for a data type.
    # --------
    
    #   explain s501;
    
    # --------
    #   Good:  Both preds used as begin & end keys for index-only scan.
    #            Index selectivity:  0.01%     Total cost:   1
    #   Bad:   Error [-10702]: Statement s501 has not been prepared.
    # --------
    
    stmt = """execute s501;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s62')
    #--------
    #  Good:  1 row.
    #  Bad:   Error [-10043]: Statement name has not been
    #           successfully prepared.
    #--------
    
    #------------------
    # s0809(cleanup) --
    #------------------
    #reset prepared *;
    
    stmt = """DROP TABLE s0809ta;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test008(desc="""a10"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:         A10
    #  Description:
    #  Description:            Key predicate optimization tests
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:        (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    stmt = """DROP   TABLE s0810ta;"""
    output = _dci.cmdexec(stmt)
    
    # Create tables.
    stmt = """CREATE TABLE s0810ta (
a INTEGER NOT NULL,
b INTEGER NOT NULL,
c INTEGER NOT NULL,
v VARCHAR(5),
--                      t DATETIME HOUR TO MINUTE,
t TIME,
PRIMARY KEY ( a, b, c )
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #                       catalog
    
    stmt = """INSERT INTO s0810ta VALUES( 1, 0, 2, '102', time '01:02:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0810ta VALUES( 1, 1, 2, '112', time '01:12:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0810ta VALUES( 1, 2, 2, '122', time '01:22:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0810ta VALUES( 2, 0, 1, '201', time '02:01:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0810ta VALUES( 2, 1, 1, '211', time '02:11:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0810ta VALUES( 2, 2, 1, '221', time '02:21:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0810ta VALUES( 2, 3, 1, '231', time '02:31:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0810ta VALUES( 2, 4, 1, '241', time '02:41:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0810ta VALUES( 3, 0, 0, '300', time '03:00:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0810ta VALUES( 3, 1, 0, '310', time '03:10:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0810ta VALUES( 3, 2, 0, '320', time '03:20:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0810ta VALUES( 3, 3, 0,  NULL, time '03:30:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0810ta VALUES( 3, 4, 0,  NULL, time '03:40:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """CREATE INDEX s0810tai ON s0810ta(c,a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #---------------
    # s0810(s101) --
    #---------------
    #  This test case uses index S0810TAI on KEY01TA(C,A).
    
    stmt = """prepare s101 from
SELECT a,b,c
FROM s0810ta 
WHERE c = 1
AND a = 1+1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    # --------
    #   Good:  SQL command prepared.
    #   Bad:   No response for several minutes while Generator is looping.
    #          Finally ends with the message:
    #          Error [-2033]: The SQL compiler is out of space because
    #            its extended segment is full.
    # --------
    
    #   explain s101;
    
    # --------
    #   Good:  Preds used as begin & end keys for index-only access.
    #            Index selectivity:  0.01%     Total cost:   1
    #   Bad:   Error [-10702]: Statement s101 has not been prepared.
    # --------
    
    stmt = """execute s101;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s2')
    #--------
    #  Good:  5 rows.
    #  Bad:   Error [-10043]: Statement name has not been
    #           successfully prepared.
    #--------
    
    #------------------
    # s0810(cleanup) --
    #------------------
    #reset prepared *;
    
    stmt = """DROP TABLE s0810ta;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test009(desc="""a20"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:         A20
    #  Description:            Key predicate optimization tests
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:        (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """DROP   TABLE s0820ta;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE s0820ta (
a INTEGER NOT NULL,
b INTEGER NOT NULL,
c INTEGER NOT NULL,
v VARCHAR(5),
t TIME,
PRIMARY KEY ( a, b, c )
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #                        catalog
    
    stmt = """INSERT INTO s0820ta VALUES(-2,-4, 2, 'aaa', time '01:02:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0820ta VALUES(-1,-2, 2, 'aaa', time '01:02:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0820ta VALUES(-1,-1, 2, 'ccc', time '01:12:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0820ta VALUES( 1, 1, 2, 'bbb', time '01:22:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0820ta VALUES( 2, 0, 1, 'AAA', time '02:01:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0820ta VALUES( 2, 1, 1, 'EEE', time '02:11:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0820ta VALUES( 2, 2, 1, 'BBB', time '02:21:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0820ta VALUES( 2, 3, 1, 'DDD', time '02:31:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0820ta VALUES( 2, 4, 1, 'CCC', time '02:41:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0820ta VALUES( 3, 0, 0, 'fff', time '03:00:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0820ta VALUES( 3, 1, 0, 'ddd', time '03:10:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0820ta VALUES( 3, 2, 0, 'eee', time '03:20:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0820ta VALUES( 3, 3, 0,  NULL, time '03:30:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0820ta VALUES( 3, 4, 0,  NULL, time '03:40:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """CREATE INDEX s0820tai ON s0820ta(t);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """CREATE INDEX s0820taj ON s0820ta(v);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #---------------
    # s0820(s101) --
    #---------------
    
    stmt = """prepare s101 from
SELECT x.v, y.v
FROM s0820ta x, s0820ta y
WHERE x.v = upshift(y.v)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s101;
    
    # --------
    #   Good:  Predicate is used as begin/end key for inner scan.
    #            Index selectivity:   1%       Total cost:  20
    #   Bad:   No begin/end key.  Predicate is evaluated by FS2 upon each row.
    #            Index selectivity: 100%       Total cost: 476
    # --------
    
    stmt = """execute s101;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s2')
    #  11 rows
    
    #---------------
    # s0820(s201) --
    #---------------
    
    stmt = """prepare s201 from
SELECT x.t, y.t
FROM s0820ta x, s0820ta y
WHERE x.t < y.t
AND x.a = 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s201;
    
    # --------
    #   'x.t < y.t' is used as begin-key for inner scan.
    # --------
    
    stmt = """execute s201;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s4')
    #--------
    #  Good:  35 rows.
    #  Bad:    9 rows, followed by:
    #         Error from SQL [-8300]: File system error occurred on S0820TA.
    #         Error from File System [1024]: The specified SQL subset is not
    #           defined to the File System.
    #--------
    
    #---------------
    # s0820(s202) --
    #---------------
    
    stmt = """prepare s202 from
SELECT x.t, y.t
FROM s0820ta x, s0820ta y
WHERE x.t <= y.t
AND x.a = 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s202;
    
    # --------
    #   'x.t <= y.t' is used as begin-key for inner scan.
    # --------
    
    stmt = """execute s202;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s6')
    #--------
    #  Good:  40 rows.
    #  Bad:   10 rows, followed by:
    #         Error from SQL [-8300]: File system error occurred on S0820TA.
    #         Error from File System [1024]: The specified SQL subset is not
    #           defined to the File System.
    #--------
    
    #---------------
    # s0820(s203) --
    #---------------
    
    stmt = """prepare s203 from
SELECT x.t, y.t
FROM s0820ta x, s0820ta y
WHERE x.t >= y.t
AND x.a = 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s203;
    
    # --------
    #   'x.t >= y.t' is used as end-key for inner scan.
    # --------
    
    stmt = """execute s203;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s8')
    #--------
    #  Good:  35 rows.
    #  Bad:    5 rows, followed by:
    #         Error from SQL [-8300]: File system error occurred on S0820TA.
    #         Error from File System [1024]: The specified SQL subset is not
    #           defined to the File System.
    #--------
    
    #---------------
    # s0820(s204) --
    #---------------
    
    stmt = """prepare s204 from
SELECT x.t, y.t
FROM s0820ta x, s0820ta y
WHERE x.t > y.t
AND x.a = 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s204;
    
    # --------
    #   'x.t > y.t' is used as end-key for inner scan.
    # --------
    
    stmt = """execute s204;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s10')
    #--------
    #  Good:  30 rows.
    #  Bad:    4 rows, followed by:
    #         Error from SQL [-8300]: File system error occurred on S0820TA.
    #         Error from File System [1024]: The specified SQL subset is not
    #           defined to the File System.
    #--------
    
    #---------------
    # s0820(s205) --
    #---------------
    
    stmt = """prepare s205 from
SELECT x.t, y.t
FROM s0820ta x, s0820ta y
WHERE x.a = 2
AND x.t >= y.t
AND x.t <= y.t
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s205;
    
    # --------
    #   'x.t <= y.t' is used as begin-key for inner scan.
    #   'x.t >= y.t' is used as end-key for inner scan.
    # --------
    
    stmt = """execute s205;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s12')
    #--------
    #  Good:  5 rows.
    #  Bad:   1 row, followed by:
    #         Error from SQL [-8300]: File system error occurred on S0820TA.
    #         Error from File System [1024]: The specified SQL subset is not
    #           defined to the File System.
    #--------
    
    #---------------
    # s0820(s206) --
    #---------------
    #  Multi-value '<' predicate
    
    stmt = """prepare s206 from
SELECT x.t, x.a, y.t, y.a
FROM s0820ta x, s0820ta y
WHERE x.a = 2
AND (x.t,x.a) < (y.t, y.a)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s206;
    
    # --------
    #   'x.t, x.a < y.t, y.a' is used as begin-key for inner scan.
    # --------
    
    stmt = """execute s206;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s14')
    #--------
    #  Good:  35 rows.
    #  Bad:    9 rows, followed by:
    #         Error from SQL [-8300]: File system error occurred on S0820TA.
    #         Error from File System [1024]: The specified SQL subset is not
    #           defined to the File System.
    #--------
    
    #---------------
    # s0820(s207) --
    #---------------
    #  Multi-value '<=' predicate
    
    stmt = """prepare s207 from
SELECT x.t, x.a, y.t, y.a
FROM s0820ta x, s0820ta y
WHERE x.a = 2
AND (x.t,x.a) <= (y.t, y.a)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s207;
    
    # --------
    #   'x.t, x.a <= y.t, y.a' is used as begin-key for inner scan.
    # --------
    
    stmt = """execute s207;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s16')
    #--------
    #  Good:  40 rows.
    #  Bad:   10 rows, followed by:
    #         Error from SQL [-8300]: File system error occurred on S0820TA.
    #         Error from File System [1024]: The specified SQL subset is not
    #           defined to the File System.
    #--------
    
    #---------------
    # s0820(s208) --
    #---------------
    #  Multi-value '>=' predicate
    
    stmt = """prepare s208 from
SELECT x.t, x.a, y.t, y.a
FROM s0820ta x, s0820ta y
WHERE x.a = 2
AND (x.t,x.a) >= (y.t, y.a)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s208;
    
    # --------
    #   'x.t, x.a >= y.t, y.a' is used as end-key for inner scan.
    # --------
    
    stmt = """execute s208;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s18')
    #--------
    #  Good:  35 rows.
    #  Bad:    5 rows, followed by:
    #         Error from SQL [-8300]: File system error occurred on S0820TA.
    #         Error from File System [1024]: The specified SQL subset is not
    #           defined to the File System.
    #--------
    
    #---------------
    # s0820(s209) --
    #---------------
    #  Multi-value '>' predicate
    
    stmt = """prepare s209 from
SELECT x.t, x.a, y.t, y.a
FROM s0820ta x, s0820ta y
WHERE x.a = 2
AND (x.t,x.a) > (y.t, y.a)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s209;
    
    # --------
    #   'x.t, x.a > y.t, y.a' is used as end-key for inner scan.
    # --------
    
    stmt = """execute s209;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s20')
    #--------
    #  Good:  30 rows.
    #  Bad:    4 rows, followed by:
    #         Error from SQL [-8300]: File system error occurred on S0820TA.
    #         Error from File System [1024]: The specified SQL subset is not
    #           defined to the File System.
    #--------
    
    #---------------
    # s0820(s210) --
    #---------------
    #  Multi-value '>=' and '<=' predicates
    
    stmt = """prepare s210 from
SELECT x.t, x.a, y.t, y.a
FROM s0820ta x, s0820ta y
WHERE x.a = 2
AND (x.t,x.a) <= (y.t, y.a)
AND (x.t,x.a) >= (y.t, y.a)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s210;
    
    # --------
    #   'x.t, x.a <= y.t, y.a' is used as begin-key for inner scan.
    #   'x.t, x.a >= y.t, y.a' is used as end-key for inner scan.
    # --------
    
    stmt = """execute s210;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s22')
    #--------
    #  Good:   5 rows.
    #  Bad:    1 row, followed by:
    #         Error from SQL [-8300]: File system error occurred on S0820TA.
    #         Error from File System [1024]: The specified SQL subset is not
    #           defined to the File System.
    #--------
    
    #---------------
    # s0820(s211) --
    #---------------
    #  3-way join with multi-value '>=' and '<=' predicates
    
    stmt = """prepare s211 from
SELECT x.t, x.a, y.t, y.a, z.t, z.a
FROM s0820ta x, s0820ta y, s0820ta z
WHERE x.a = 2
AND (x.t,x.a) <= (y.t, y.a)
AND (x.t,x.a) >= (y.t, y.a)
AND (y.t,y.a) >= (z.t, z.a)
AND (x.t,x.a) <= (z.t, z.a)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s211;
    
    # --------
    #   All 4 multi-value predicates are used as begin/end keys.
    # --------
    
    stmt = """execute s211;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s24')
    #--------
    #  Good:   5 rows.
    #  Bad:    1 row, followed by:
    #         Error from SQL [-8300]: File system error occurred on S0820TA.
    #         Error from File System [1024]: The specified SQL subset is not
    #           defined to the File System.
    #--------
    
    #---------------
    # s0820(s301) --
    #---------------
    #  This query shows the desired plan.
    
    stmt = """prepare s301 from
SELECT x.a, x.b, x.c, y.a, y.b, y.c
FROM s0820ta x, s0820ta y
WHERE x.a = 2
AND x.b >= 1
AND x.c = 1
AND y.a = x.a
AND (x.b, x.c) <= (y.b, y.c)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s301;
    
    # --------
    #   Good:  Begin-key for inner scan is:
    #              y.a = x.a  AND  (x.b, x.c) <= (y.b, y.c)
    #          Total cost:  1
    # --------
    
    stmt = """execute s301;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s26')
    #  10 rows.
    
    #---------------
    # s0820(s302) --
    #---------------
    #  In this query, the multi-value predicate is turned around.
    #  With SQLCOMP versions up to and including C30.08, the
    #    begin-key for the inner scan became just y.a = x.a,
    #    and the multi-value predicate became a base table predicate.
    #    This was considered a non-optimal plan.
    #  The problem was not reproducible in C30.09.  Perhaps it was
    #    fixed as a side-effect of the C30S06 fix to opta^find^pred^col.
    
    stmt = """prepare s302 from
SELECT x.a, x.b, x.c, y.a, y.b, y.c
FROM s0820ta x, s0820ta y
WHERE x.a = 2
AND x.b >= 1
AND x.c = 1
AND y.a = x.a
AND (y.b, y.c) >= (x.b, x.c)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s302;
    
    # --------
    #   Good:  Begin-key for inner scan is:
    #              y.a = x.a  AND  (y.b, y.c) >= (x.b, x.c)
    #            Total cost:  1
    #   Bad:   Begin-key for inner scan is just
    #              y.a = x.a
    # --------
    
    stmt = """execute s302;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s28')
    #  10 rows.
    
    #------------------
    # s0820(cleanup) --
    #------------------
    #reset prepared *;
    
    stmt = """DROP TABLE s0820ta;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test010(desc="""a21"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:         A21
    #  Description:            Floating-point comparison predicate test
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:        (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    #
    # Comparison predicates between:
    #   - an integer column with a floating-point column,
    #        constant, or expression;
    #   - a floating-point column with an integer constant
    #        or expression
    #   - a floating-point column with a floating-point
    #        column, constant, or expression
    #
    # The following variations are tested:
    #   - Predicates:  =,  >=/<=,  >/<
    #   - '=' predicate with the column on the
    #       left-hand side vs. the right-hand side
    #   - Key columns vs. non-key columns
    #   - Floating-point constants with zero fractional part
    #       vs. nonzero fractional part
    #   - Single-table queries
    #   - Joins between integer and floating-point columns,
    #       including key and non-key columns
    #   - Multivalue join predicates with a mixture of
    #       integer and floating point columns
    
    stmt = """DROP   TABLE s0821ta;"""
    output = _dci.cmdexec(stmt)
    stmt = """DROP   TABLE s0821tb;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE s0821ta (
a INTEGER NOT NULL,
b INTEGER NOT NULL,
c INTEGER NOT NULL,
PRIMARY KEY ( a, b, c )
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO s0821ta VALUES(-2,-4, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0821ta VALUES(-1,-2, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0821ta VALUES(-1,-1, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0821ta VALUES( 1, 1, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0821ta VALUES( 2, 0, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0821ta VALUES( 2, 1, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0821ta VALUES( 2, 2, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0821ta VALUES( 2, 3, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0821ta VALUES( 2, 4, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0821ta VALUES( 3, 0, 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0821ta VALUES( 3, 1, 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0821ta VALUES( 3, 2, 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0821ta VALUES( 3, 3, 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0821ta VALUES( 3, 4, 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """CREATE TABLE s0821tb (
a FLOAT   NOT NULL,
b FLOAT   NOT NULL,
PRIMARY KEY ( a, b )
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO s0821tb VALUES( -1.2,   -1.2   );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0821tb VALUES( -1.0,   -1.0   );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0821tb VALUES( -0.8,   -0.8   );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0821tb VALUES( -0.6,   -0.6   );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0821tb VALUES( -0.4,   -0.4   );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0821tb VALUES( -0.2,   -0.2   );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0821tb VALUES(  0.0,    0.0   );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0821tb VALUES(  0.2,    0.2   );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0821tb VALUES(  0.4,    0.4   );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0821tb VALUES(  0.6,    0.6   );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0821tb VALUES(  0.8,    0.8   );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0821tb VALUES(  1.0,    1.0   );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0821tb VALUES(  1.250,  1.250 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0821tb VALUES(  1.500,  1.500 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0821tb VALUES(  1.750,  1.750 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0821tb VALUES(  1.825,  1.825 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0821tb VALUES(  2.0,    2.0   );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO s0821tb VALUES(  2.2,    2.2   );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  '=' predicate on integer column;  column on rhs of pred
    #reset prepared *;
    
    #---------------
    # s0821(s201) --
    #---------------
    #  (float constant with zero fraction) = (integer key column)
    
    stmt = """prepare s201 from
SELECT a
FROM s0821ta 
WHERE 1.0E0 = a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s201;
    
    #   The predicate is classified as a base table predicate.
    #     The Optimizer avoids choosing it as a begin/end key
    #       so as to avoid the known bug in Executor.
    #     Optimizer restriction should be removed when Executor is fixed.
    
    stmt = """execute s201;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s3')
    #  1 row
    
    #---------------
    # s0821(s202) --
    #---------------
    #  (float constant with zero fraction) = (integer non-key column)
    
    stmt = """prepare s202 from
SELECT b
FROM s0821ta 
WHERE 1.0E0 = b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s202;
    
    #   The predicate is classified as a base table predicate
    #     because it tests a non-key column.
    
    stmt = """execute s202;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s5')
    #  3 rows
    
    #---------------
    # s0821(s203) --
    #---------------
    #  (float constant with nonzero fraction) = (integer key column)
    
    stmt = """prepare s203 from
SELECT a
FROM s0821ta 
WHERE 1.1E0 = a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s203;
    
    #  The predicate is classified as a base table predicate.
    #    The Optimizer avoids choosing it as a begin/end key
    #      so as to avoid the known bug in Executor.
    #    Optimizer restriction should be removed when Executor is fixed.
    
    # 06/01/09 The result of execution of the statement is non-deterministic, removing
    # the expect line. Here is the comments regarding compare integer
    # with floating data type:
    # in general, an equi comparison between a float and an integer is not guaranteed
    # to always return the expected 'exact' result. This is due to the internal
    # representation of floats and implicit conversion of integer to float before the
    # comparison. The actual value that is being compared will be represented as a
    # float and may not be equal to the original value. For ex., in this case, the
    # value of '1' in column 'a' may be represented as 0.9999e0 internally.
    stmt = """execute s203;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    #  0 rows.
    
    #---------------
    # s0821(s204) --
    #---------------
    #  (float constant with nonzero fraction) = (integer non-key column)
    
    stmt = """prepare s204 from
SELECT b
FROM s0821ta 
WHERE 1.1E0 = b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s204;
    
    #  The predicate is classified as a base table predicate
    #    because it tests a non-key column.
    
    # 06/01/09 The result of execution of the statement is non-deterministic, removing
    # the expect line. Here is the comments regarding compare integer
    # with floating data type:
    # in general, an equi comparison between a float and an integer is not guaranteed
    # to always return the expected 'exact' result. This is due to the internal
    # representation of floats and implicit conversion of integer to float before the
    # comparison. The actual value that is being compared will be represented as a
    # float and may not be equal to the original value. For ex., in this case, the
    # value of '1' in column 'a' may be represented as 0.9999e0 internally.
    stmt = """execute s204;"""
    output = _dci.cmdexec(stmt)
    #  0 rows
    
    #---------------
    # s0821(s205) --
    #---------------
    #  (integer constant + float constant) = (integer key column)
    
    stmt = """prepare s205 from
SELECT a
FROM s0821ta 
WHERE 1 + 0.1E0 = a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s205;
    
    #  The predicate is used as a begin/end key.
    
    stmt = """execute s205;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #--------
    #  Good:  0 rows.
    #  Bad:   1 row.                    <--- Expected
    #--------
    
    #---------------
    # s0821(s206) --
    #---------------
    #  (integer constant + float constant) = (integer non-key column)
    
    stmt = """prepare s206 from
SELECT b
FROM s0821ta 
WHERE 1 + 0.1E0 = b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s206;
    
    #  The predicate is classified as a base table predicate
    #    because it tests a non-key column.
    
    stmt = """execute s206;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #  0 rows
    
    #  '=' predicate on floating-point column; column on lhs
    #reset prepared *;
    
    #---------------
    # s0821(s301) --
    #---------------
    #  (float key column) = (float constant with zero fraction)
    
    stmt = """prepare s301 from
SELECT a
FROM s0821tb 
WHERE a = 1.0E0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s301;
    
    #   The predicate is used as a begin/end key.
    
    stmt = """execute s301;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s11')
    #  1 row
    
    #---------------
    # s0821(s302) --
    #---------------
    #  (float non-key column) = (float constant with zero fraction)
    
    stmt = """prepare s302 from
SELECT b
FROM s0821tb 
WHERE b = 1.0E0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s302;
    
    #   The predicate is classified as a base table predicate
    #     because it tests a non-key column.
    
    stmt = """execute s302;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s13')
    #  1 row
    
    #---------------
    # s0821(s303) --
    #---------------
    #  (float key column) = (float constant with nonzero fraction)
    
    stmt = """prepare s303 from
SELECT a
FROM s0821tb 
WHERE a = 1.25E0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s303;
    
    #   The predicate is used as a begin/end key.
    
    stmt = """execute s303;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s15')
    #  1 row
    
    #---------------
    # s0821(s304) --
    #---------------
    #  (float non-key column) = (float constant with nonzero fraction)
    
    stmt = """prepare s304 from
SELECT b
FROM s0821tb 
WHERE b = 1.25E0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s304;
    
    #   The predicate is classified as a base table predicate
    #     because it tests a non-key column.
    
    stmt = """execute s304;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s17')
    #  1 row
    
    #---------------
    # s0821(s305) --
    #---------------
    #  (float key column) = (integer constant + float constant)
    
    stmt = """prepare s305 from
SELECT a
FROM s0821tb 
WHERE a = 1 + 0.5000001E0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #   Note: At present the literal 0.5E0 suffers roundoff
    #     error when converted to the internal floating point
    #     representation.  (The value becomes 0.49999994039535522.)
    #     However, when the literal is written as 0.5000001E0,
    #     the roundoff error leads to the desired result: the
    #     internal floating point representation equals 1/2.
    #   I think the floating point conversion will be done
    #     more accurately in the D20 release, and that might
    #     cause this query to return 0 rows instead of 1 row.
    #     Change the literal back to the correct value, 0.5E0,
    #     if this occurs.
    
    #   explain s305;
    
    #  The predicate is used as a begin/end key.
    
    stmt = """execute s305;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #  1 row
    
    #---------------
    # s0821(s306) --
    #---------------
    #  (float non-key column) = (integer constant + float constant)
    
    stmt = """prepare s306 from
SELECT b
FROM s0821tb 
WHERE b = 1 + 0.5000001E0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s306;
    
    #  The predicate is classified as a base table predicate
    #    because it tests a non-key column.
    
    stmt = """execute s306;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #  1 row
    
    #---------------
    # s0821(s307) --
    #---------------
    #  (float key column) = (integer constant)
    
    stmt = """prepare s307 from
SELECT a
FROM s0821tb 
WHERE a = 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s307;
    
    #   The predicate is used as a begin/end key.
    
    stmt = """execute s307;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s21')
    #  1 row
    
    #---------------
    # s0821(s308) --
    #---------------
    #  (float non-key column) = (integer constant)
    
    stmt = """prepare s308 from
SELECT b
FROM s0821tb 
WHERE b = 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s308;
    
    #   The predicate is classified as a base table predicate
    #     because it tests a non-key column.
    
    stmt = """execute s308;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s23')
    #  1 row
    
    #  '>=' and '<=' predicates on integer column
    #reset prepared *;
    
    #---------------
    # s0821(s401) --
    #---------------
    #  (integer key column) >=,<= (float constant with zero fraction)
    
    stmt = """prepare s401 from
SELECT a
FROM s0821ta 
WHERE a >= 1.0E0
AND a <= 1.0E0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s401;
    
    #   The predicates are classified as base table predicates.
    #     The Optimizer avoids choosing them as begin/end keys
    #       so as to avoid the known bug in Executor.
    #     Optimizer restriction should be removed when Executor is fixed.
    
    stmt = """execute s401;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s25')
    #  1 row
    
    #---------------
    # s0821(s402) --
    #---------------
    #  (integer non-key column) >=,<= (float constant with zero fraction)
    
    stmt = """prepare s402 from
SELECT b
FROM s0821ta 
WHERE b >= 1.0E0
AND b <= 1.0E0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s402;
    
    #   base table preds
    
    stmt = """execute s402;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s27')
    #  3 rows
    
    #---------------
    # s0821(s403) --
    #---------------
    #  (integer key column) >=,<= (float constant with nonzero fraction)
    
    stmt = """prepare s403 from
SELECT a
FROM s0821ta 
WHERE a >= 1.1E0
AND a <= 1.1E0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s403;
    
    #  The predicate is classified as a base table predicate.
    #    The Optimizer avoids choosing it as a begin/end key
    #      so as to avoid the known bug in Executor.
    #    Optimizer restriction should be removed when Executor is fixed.
    
    stmt = """execute s403;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #---------------
    # s0821(s404) --
    #---------------
    #  (integer non-key column) >=,<= (float constant with nonzero fraction)
    
    stmt = """prepare s404 from
SELECT b
FROM s0821ta 
WHERE b >= 1.1E0
AND b <= 1.1E0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s404;
    
    #  base table predicates
    
    stmt = """execute s404;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #  0 rows
    
    #---------------
    # s0821(s405) --
    #---------------
    #  (integer key column) >=,<= (integer constant + float constant)
    
    stmt = """prepare s405 from
SELECT a
FROM s0821ta 
WHERE a >= 1 + 0.1E0
AND a <= 1 + 0.1E0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s405;
    
    #  begin/end key predicates
    
    stmt = """execute s405;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #--------
    #  Good:  0 rows.
    #  Bad:   1 row.                    <--- Expected
    #--------
    
    #---------------
    # s0821(s406) --
    #---------------
    #  (integer non-key column) >=,<= (integer constant + float constant)
    
    stmt = """prepare s406 from
SELECT b
FROM s0821ta 
WHERE b >= 1 + 0.1E0
AND b <= 1 + 0.1E0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s406;
    
    #  base table predicates
    
    stmt = """execute s406;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #  0 rows
    
    #  '>=' and '<=' predicates on floating-point column
    #reset prepared *;
    
    #---------------
    # s0821(s501) --
    #---------------
    #  (float key column) >=,<= (float constant with zero fraction)
    
    stmt = """prepare s501 from
SELECT a
FROM s0821tb 
WHERE a >= 1.0E0
AND a <= 1.0E0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s501;
    
    #   begin/end key predicates
    
    stmt = """execute s501;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s33')
    #  1 row
    
    #---------------
    # s0821(s502) --
    #---------------
    #  (float non-key column) >=,<= (float constant with zero fraction)
    
    stmt = """prepare s502 from
SELECT b
FROM s0821tb 
WHERE b >= 1.0E0
AND b <= 1.0E0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s502;
    
    #   base table predicates
    
    stmt = """execute s502;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s35')
    #  1 row
    
    #---------------
    # s0821(s503) --
    #---------------
    #  (float key column) >=,<= (float constant with nonzero fraction)
    
    stmt = """prepare s503 from
SELECT a
FROM s0821tb 
WHERE a >= 1.25E0
AND a <= 1.25E0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s503;
    
    #   begin/end key predicates
    
    stmt = """execute s503;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s37')
    #  1 row
    
    #---------------
    # s0821(s504) --
    #---------------
    #  (float non-key column) >=,<= (float constant with nonzero fraction)
    
    stmt = """prepare s504 from
SELECT b
FROM s0821tb 
WHERE b >= 1.25E0
AND b <= 1.25E0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s504;
    
    #   base table predicates
    
    stmt = """execute s504;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s39')
    #  1 row
    
    #---------------
    # s0821(s505) --
    #---------------
    #  (float key column) >=,<= (integer constant + float constant)
    
    stmt = """prepare s505 from
SELECT a
FROM s0821tb 
WHERE a >= 1 + 0.49E0
AND a <= 1 + 0.51E0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s505;
    
    #   begin/end key predicates
    
    stmt = """execute s505;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s41')
    #  1 row
    
    #---------------
    # s0821(s506) --
    #---------------
    #  (float non-key column) >=,<= (integer constant + float constant)
    
    stmt = """prepare s506 from
SELECT b
FROM s0821tb 
WHERE b >= 1 + 0.49E0
AND b <= 1 + 0.51E0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s506;
    
    #   base table predicates
    
    stmt = """execute s506;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s43')
    #  1 row
    
    #---------------
    # s0821(s507) --
    #---------------
    #  (float key column) >=,<= (integer constant)
    
    stmt = """prepare s507 from
SELECT a
FROM s0821tb 
WHERE a >= 1
AND a <= 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s507;
    
    #   begin/end key predicates
    
    stmt = """execute s507;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s45')
    #  1 row
    
    #---------------
    # s0821(s508) --
    #---------------
    #  (float non-key column) >=,<= (integer constant)
    
    stmt = """prepare s508 from
SELECT b
FROM s0821tb 
WHERE b >= 1
AND b <= 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s508;
    
    #   base table predicates
    
    stmt = """execute s508;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s47')
    #  1 row
    
    #  '>' and '<' predicates on integer column
    #reset prepared *;
    
    #---------------
    # s0821(s601) --
    #---------------
    #  (integer key column) >,< (float constant with zero fraction)
    
    stmt = """prepare s601 from
SELECT a
FROM s0821ta 
WHERE a > 1.0E0
AND a < 1.0E0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s601;
    
    #  The predicates are classified as base table predicates.
    #    The Optimizer avoids choosing them as begin/end keys
    #      so as to avoid the known bug in Executor.
    #    Optimizer restriction should be removed when Executor is fixed.
    
    stmt = """execute s601;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #  0 rows
    
    #---------------
    # s0821(s602) --
    #---------------
    #  (integer non-key column) >,< (float constant with zero fraction)
    
    stmt = """prepare s602 from
SELECT b
FROM s0821ta 
WHERE b > 1.0E0
AND b < 1.0E0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s602;
    
    #  base table predicates
    
    stmt = """execute s602;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #  0 rows
    
    #---------------
    # s0821(s603) --
    #---------------
    #  (integer key column) >,< (float constant with nonzero fraction)
    
    stmt = """prepare s603 from
SELECT a
FROM s0821ta 
WHERE a > 1.1E0
AND a < 1.1E0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s603;
    
    #  The predicates are classified as base table predicates.
    #    The Optimizer avoids choosing them as begin/end keys
    #      so as to avoid the known bug in Executor.
    #    Optimizer restriction should be removed when Executor is fixed.
    
    stmt = """execute s603;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #  0 rows
    
    #---------------
    # s0821(s604) --
    #---------------
    #  (integer non-key column) >,< (float constant with nonzero fraction)
    
    stmt = """prepare s604 from
SELECT b
FROM s0821ta 
WHERE b > 1.1E0
AND b < 1.1E0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s604;
    
    #  base table predicate
    
    stmt = """execute s604;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #  0 rows
    
    #---------------
    # s0821(s605) --
    #---------------
    #  (integer key column) >,< (integer constant + float constant)
    
    stmt = """prepare s605 from
SELECT a
FROM s0821ta 
WHERE a > 1 + 0.5000001E0
AND a < 1 + 0.5000001E0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s605;
    
    #  begin/end key predicates
    
    stmt = """execute s605;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #  0 rows
    
    #---------------
    # s0821(s606) --
    #---------------
    #  (integer non-key column) >,< (integer constant + float constant)
    
    stmt = """prepare s606 from
SELECT b
FROM s0821ta 
WHERE b > 1 + 0.1E0
AND b < 1 + 0.1E0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f'  s606;"""
    output = _dci.cmdexec(stmt)
    
    #  base table predicates
    
    stmt = """execute s606;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #  0 rows
    
    #  '>' and '<' predicates on integer column;  column on rhs
    #reset prepared *;
    
    #---------------
    # s0821(s701) --
    #---------------
    #  (float constant with zero fraction) > (integer key column)
    
    stmt = """prepare s701 from
SELECT a
FROM s0821ta 
WHERE 2.0E0 > a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s701;
    
    #   The predicate is classified as a base table predicate.
    #     The Optimizer avoids choosing it as a begin/end key
    #       so as to avoid the known bug in Executor.
    #     Optimizer restriction should be removed when Executor is fixed.
    
    stmt = """execute s701;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s55')
    #  4 rows
    
    #---------------
    # s0821(s702) --
    #---------------
    #  (float constant with zero fraction) > (integer non-key column)
    
    stmt = """prepare s702 from
SELECT b
FROM s0821ta 
WHERE 2.0E0 > b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s702;
    
    #   base table predicate
    
    stmt = """execute s702;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s57')
    #  8 rows
    
    #---------------
    # s0821(s703) --
    #---------------
    #  (float constant with nonzero fraction) > (integer key column)
    
    stmt = """prepare s703 from
SELECT a
FROM s0821ta 
WHERE 2.2E0 > a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s703;
    
    #   The predicate is classified as a base table predicate.
    #     The Optimizer avoids choosing it as a begin/end key
    #       so as to avoid the known bug in Executor.
    #     Optimizer restriction should be removed when Executor is fixed.
    
    stmt = """execute s703;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s59')
    #  9 rows
    
    #---------------
    # s0821(s704) --
    #---------------
    #  (float constant with nonzero fraction) > (integer non-key column)
    
    stmt = """prepare s704 from
SELECT b
FROM s0821ta 
WHERE 2.2E0 > b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s704;
    
    #   base table predicate
    
    stmt = """execute s704;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s61')
    #  10 rows
    
    #---------------
    # s0821(s705) --
    #---------------
    #  (integer constant + float constant) > (integer key column)
    
    stmt = """prepare s705 from
SELECT a
FROM s0821ta 
WHERE 2 + 0.2E0 > a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s705;
    
    #   end key predicate
    
    stmt = """execute s705;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s63')
    #--------
    #  Good:  9 rows.
    #  Bad:   4 rows  (excludes the 2's)  <--- Expected
    #--------
    
    #---------------
    # s0821(s706) --
    #---------------
    #  (integer constant + float constant) > (integer non-key column)
    
    stmt = """prepare s706 from
SELECT b
FROM s0821ta 
WHERE 2 + 0.2E0 > b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s706;
    
    #   base table predicate
    
    stmt = """execute s706;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s65')
    #  10 rows
    
    #  '>' and '<' predicates on float column;  column on rhs
    #reset prepared *;
    
    #---------------
    # s0821(s801) --
    #---------------
    #  (float constant with zero fraction) > (float key column)
    
    stmt = """prepare s801 from
SELECT a
FROM s0821tb 
WHERE 2.0E0 > a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s801;
    
    #   end key predicate
    
    stmt = """execute s801;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s67')
    #  16 rows
    
    #---------------
    # s0821(s802) --
    #---------------
    #  (float constant with zero fraction) > (float non-key column)
    
    stmt = """prepare s802 from
SELECT b
FROM s0821tb 
WHERE 2.0E0 > b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s802;
    
    #   base table predicate
    
    stmt = """execute s802;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s69')
    #  16 rows
    
    #---------------
    # s0821(s803) --
    #---------------
    #  (float constant with nonzero fraction) > (float key column)
    
    stmt = """prepare s803 from
SELECT a
FROM s0821tb 
WHERE 1.2E0 > a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s803;
    
    #   end key predicate
    
    stmt = """execute s803;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s71')
    #  12 rows
    
    #---------------
    # s0821(s804) --
    #---------------
    #  (float constant with nonzero fraction) > (float non-key column)
    
    stmt = """prepare s804 from
SELECT b
FROM s0821tb 
WHERE 1.2E0 > b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s804;
    
    #   base table predicate
    
    stmt = """execute s804;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s73')
    #  12 rows
    
    #---------------
    # s0821(s805) --
    #---------------
    #  (integer constant + float constant) > (float key column)
    
    stmt = """prepare s805 from
SELECT a
FROM s0821tb 
WHERE 1 + 0.2E0 > a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s805;
    
    #   end key predicate
    
    stmt = """execute s805;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s75')
    #  12 rows
    
    #---------------
    # s0821(s806) --
    #---------------
    #  (integer constant + float constant) > (float non-key column)
    
    stmt = """prepare s806 from
SELECT b
FROM s0821tb 
WHERE 1 + 0.2E0 > b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s806;
    
    #   base table predicate
    
    stmt = """execute s806;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s77')
    #  12 rows
    
    #---------------
    # s0821(s807) --
    #---------------
    #  (integer constant) > (float key column)
    
    stmt = """prepare s807 from
SELECT a
FROM s0821tb 
WHERE 1 > a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s807;
    
    #   end key predicate
    
    stmt = """execute s807;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s79')
    #  11 rows
    
    #---------------
    # s0821(s808) --
    #---------------
    #  (integer constant) > (float non-key column)
    
    stmt = """prepare s808 from
SELECT b
FROM s0821tb 
WHERE 1 > b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s808;
    
    #   base table predicate
    
    stmt = """execute s808;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s81')
    #  11 rows
    
    #  Joins between integer and floating-point columns
    
    #reset prepared *;
    
    #---------------
    # s0821(s901) --
    #---------------
    #  join FLOAT (outer) with INT key (inner)
    
    stmt = """prepare s901 from
SELECT tfloat.a, tint.a
FROM s0821tb tfloat, s0821ta tint
WHERE tfloat.a > -2
AND tfloat.a < 4
AND tfloat.a = tint.a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s901;
    
    stmt = """execute s901;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s83')
    #--------
    #  Good:   8 rows.
    #  Bad:   19 rows.                  <--- Expected
    #--------
    
    #---------------
    # s0821(s902) --
    #---------------
    #  join FLOAT (outer) with INT non-key (inner)
    
    stmt = """prepare s902 from
SELECT tfloat.b, tint.b
FROM s0821tb tfloat, s0821ta tint
WHERE tfloat.a > -2
AND tfloat.a < 4
AND tfloat.b = tint.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s902;
    
    stmt = """execute s902;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s85')
    #  8 rows
    
    #---------------
    # s0821(s903) --
    #---------------
    #  join INT (outer) with FLOAT key (inner)
    
    stmt = """prepare s903 from
SELECT tint.a, tfloat.a
FROM s0821ta tint, s0821tb tfloat
WHERE tint.a > -2
AND tint.a < 4
AND tfloat.a = tint.a
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s903;
    
    stmt = """execute s903;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s87')
    #  8 rows
    
    #---------------
    # s0821(s904) --
    #---------------
    #  join INT (outer) with FLOAT non-key (inner)
    
    stmt = """prepare s904 from
SELECT tint.b, tfloat.b
FROM s0821ta tint, s0821tb tfloat
WHERE tint.a > -2
AND tint.a < 4
AND tfloat.b = tint.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s904;
    
    stmt = """execute s904;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s89')
    #  8 rows
    
    #---------------
    # s0821(s905) --
    #---------------
    #  join FLOAT (outer) with FLOAT key (inner)
    
    stmt = """prepare s905 from
SELECT x.b, y.a
FROM s0821tb x, s0821tb y
WHERE x.a > -2
AND x.a < 4
AND y.a = x.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s905;
    
    stmt = """execute s905;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s91')
    #  18 rows
    
    #---------------
    # s0821(s906) --
    #---------------
    #  join FLOAT (outer) with FLOAT non-key (inner)
    
    stmt = """prepare s906 from
SELECT x.b, y.b
FROM s0821tb x, s0821tb y
WHERE x.a > -2
AND x.a < 4
AND y.b = x.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s906;
    
    stmt = """execute s906;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s93')
    #  18 rows
    
    #---------------
    # s0821(s907) --
    #---------------
    #  join INT (outer) with FLOAT key (inner)
    #  using multi-value join preds
    
    stmt = """prepare s907 from
SELECT tint.a, tint.b, tfloat.a, tfloat.b
FROM s0821ta tint, s0821tb tfloat
WHERE tint.a > -2
AND tint.a < 4
AND tfloat.a,tfloat.b >= tint.a, tint.b
AND tfloat.a,tfloat.b <  tint.a+1, tint.b-1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s907;
    
    stmt = """execute s907;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s95')
    #  23 rows
    
    #---------------
    # s0821(s908) --
    #---------------
    #  join INT (outer) with FLOAT non-key (inner)
    #  using multi-value join preds
    
    stmt = """prepare s908 from
SELECT tint.a, tint.b, tfloat.a, tfloat.b
FROM s0821ta tint, s0821tb tfloat
WHERE tint.a > -2
AND tint.a < 4
AND tfloat.b,tfloat.a >  tint.b, tint.a
AND tint.a,tfloat.b < tfloat.a, tint.b
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s908;
    
    stmt = """execute s908;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s97')
    #   41 rows
    
    stmt = """drop table tn;"""
    output = _dci.cmdexec(stmt)
    stmt = """create table tn (a numeric(9,2) not null, primary key(a));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into tn values (-1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tn values (-2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tn values (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tn values (0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tn values (1.5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select a from tn 
where a < 1.1e0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s99')
    
    # good: 4 rows, (-1, -2, 1, 0)
    
    #------------------
    # s0821(cleanup) --
    #------------------
    #reset prepared *;
    
    stmt = """DROP TABLE s0821ta;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE s0821tb;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test011(desc="""a22"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:         A22
    #  Description:            UNION, Nested join between small
    #                          and large table.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:        (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """DROP TABLE empty;"""
    output = _dci.cmdexec(stmt)
    stmt = """DROP TABLE mkey2;"""
    output = _dci.cmdexec(stmt)
    
    # Create tables.
    stmt = """create table empty 
(a int, b int, c int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # catalog
    stmt = """create table mkey2 
(a int, b int, c int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # catalog
    
    stmt = """insert into mkey2 values ( 1, 1, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 1, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 1, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 1, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 1, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 1, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 2, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 2, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 2, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 2, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 2, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 2, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 3, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 3, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 3, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 3, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 3, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 3, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 4, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 4, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 4, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 4, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 4, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 4, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 5, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 5, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 5, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 5, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 5, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, 5, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, null, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, null, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, null, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, null, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, null, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey2 values ( 1, null, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # Create an index to use in the query.
    stmt = """create index mkey2i1 
on mkey2 (a,b,c);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Update statistics
    
    stmt = """update statistics for table mkey2 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Create tables and indexes with fake stats
    stmt = """create table s0822tc (a int,         -- mkey1
b int,
c int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table s0822td (a int,         -- large
b int,
c int,
d char(256) upshift default 'abcdef',
e char(512)         default '12345678' ) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index s0822id on s0822td (a, b, c);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  update basetabs set rowcount =  216
    #              where tablename like '%S0822TC%';
    # update basetabs set rowcount = 3456 where
    #              tablename like '%S0822TD%';
    # update files    set nonemptyblockcount = 3,
    #                eof = 16384     -- mkey1
    #               where filename like '%S0822TC%';
    # update files    set nonemptyblockcount = 707,
    #             eof = 2899968   -- large
    #             where filename like '%S0822TD%';
    # update files    set nonemptyblockcount = 44,
    #               eof = 184320    -- largei
    #               where filename like '%S0822ID%';
    
    # update columns  set uniqueentrycount = 6,
    # mkey1.a
    #                     secondlowvalue   = '+000000000000000002',
    #                     secondhighvalue  = '+000000000000000005'
    #               where tablename like '%S0822TC%'
    #                 and colname   like '%A%';
    # update columns  set uniqueentrycount = 6,
    # mkey1.b
    #                     secondlowvalue   = '+000000000000000002',
    #                     secondhighvalue  = '+000000000000000005'
    #               where tablename like '%S0822TC%'
    #                 and colname   like '%B%';
    # update columns  set uniqueentrycount = 11,
    # large.a
    #                     secondlowvalue   = '-000000000000000040',
    #                     secondhighvalue  = '+000000000000000050'
    #               where tablename like '%S0822TD%'
    #                 and colname   like '%A%';
    
    #---------------
    # s0822(s101) --
    #---------------
    #  UNION ALL
    
    stmt = """prepare s101 from
select *
from empty 
where a in (select b from mkey2 
union all select c from mkey2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s101;
    
    stmt = """execute s101;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # 0 rows
    
    #---------------
    # s0822(s102) --
    #---------------
    #  UNION
    
    stmt = """prepare s102 from
select *
from empty 
where a in (select b from mkey2 union
select c from mkey2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s102;
    
    stmt = """execute s102;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    # 0 rows
    
    #---------------
    # s0822(s201) --
    #---------------
    #  Original query
    
    stmt = """prepare s201 from
select count(*)
from s0822tc t1, s0822td t2 
where t1.a = t2.a
for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s201;
    
    #   Good: T1 outer, T2 inner in nested join
    #           using index-only access for T2 via index S0822ID.
    #   Bad:  T2 outer, T1 inner
    
    stmt = """execute s201;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a22exp""", 'a22s5')
    # 1 row (=0)
    
    #---------------
    # s0822(s202) --
    #---------------
    #  Query modified to bypass the problem (pre-T9095ABO).
    
    stmt = """prepare s202 from
select count(*)
from s0822tc t1, s0822td t2 
where t1.a = t2.a
and (t1.b = t1.b or t1.b is null)
for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #   explain s202;
    
    #   Good: T1 outer, T2 inner in nested join
    #           using index-only access for T2 via index S0822ID.
    
    stmt = """execute s202;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a22exp""", 'a22s7')
    # 1 row (=0)
    
    #------------------
    # s0822(cleanup) --
    #------------------
    #reset prepared *;
    
    stmt = """DROP TABLE empty;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE mkey2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE s0822tc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE s0822td;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

