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
    
def test001(desc="""Select with subquery, union, inner and outer joins."""):
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
    stmt = """drop   table exptab;"""
    output = _dci.cmdexec(stmt)
    
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
attribute
blocksize 4096;"""
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
    
    stmt = """drop table btun;"""
    output = _dci.cmdexec(stmt)
    
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
attribute
blocksize 4096;"""
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
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    
    stmt = """create index btuna on btun( varchar2_uniq asc );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create unique index btunb on btun( varchar2_uniq ASC );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index btunc on btun( varchar2_uniq desc);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create unique index btund on btun( varchar2_uniq asc );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
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
    
    stmt = """update statistics for table btun;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """update statistics for table exptab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  INVOKE it.
    stmt = """INVOKE exptab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """INVOKE btun;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #EXPLAIN
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
    
    stmt = """select seq_num, operator, total_cost
from table (explain (null, 'P1'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # Explain a union with a subquery and an outer join
    stmt = """prepare p2 from
select sdec1_uniq, sdec0_1000
from exptab where sdec1_uniq IN
(
( select sdec0_1000
from exptab left join """ + gvars.g_schema_arkcasedb + """.orders on sdec0_1000 < 2
)
UNION
(select sdec0_1000
from exptab  where sdec0_1000 > 997
)
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (null, 'P2'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute p2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # explain a select, predicate on key
    stmt = """prepare p3 from
select varchar2_uniq, sdec1_2 from btun 
where varchar2_uniq = 'CAAAAAAAA' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (null, 'P3'));"""
    output = _dci.cmdexec(stmt)
    
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
    
    stmt = """select seq_num, operator, total_cost
from table (explain (null, 'P4'));"""
    output = _dci.cmdexec(stmt)
    
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
    
    stmt = """select seq_num, operator, total_cost
from table (explain (null, 'P5'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute p5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s11')
    
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
    
    stmt = """select seq_num, operator, total_cost
from table (explain (null, 'P6'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute p6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s12')
    
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
    
    stmt = """select seq_num, operator, total_cost
from table (explain (null, 'P7'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute p7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s13')
    
    stmt = """prepare p8 from
SELECT varchar2_uniq FROM btunv1 UNION
SELECT varchar2_uniq FROM btun;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (null, 'P8'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute p8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s15')
    
    stmt = """prepare p9 from
SELECT * FROM btunv1 LEFT JOIN btunv2 ON
 btunv1.varchar2_uniq = btunv2.varchar1_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (null, 'P9'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute p9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s17')
    
    stmt = """select seq_num, operator, total_cost
from table (explain (null, 'P%'));"""
    output = _dci.cmdexec(stmt)
    
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

