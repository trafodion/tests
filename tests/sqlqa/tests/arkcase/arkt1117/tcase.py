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
    #  Test case name:     arkt1117:A01
    #
    #  Description:        Select [First N] with Order By
    #                      using ESP parallelism returned incorrect
    #                      results.
    #
    # =================== End Test Case Header  ===================
    #
    # ---------------------------------
    # Set up default schema.
    # Use partitioned global database.
    # ---------------------------------
    #
    # ---------------------------------
    # The error was that with [FIRST N], when parallel sort with ESP's
    # were used, [FIRST N] was treated like [ANY N]; the rows returned
    # were NOT the sorted first N rows, but were the sorted ANY rows.
    # This would show up either as incorrect results -- or as a query
    # that performs better than expected -- because we are not retrieving
    # and sorting all the rows.
    # ---------------------------------
    #
    # Get parallelism defaults for this test unit's execution.
    # *** Run first without this OBEY -- then with.
    
    stmt = """Control Query Default ATTEMPT_ESP_PARALLELISM 'ON' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Select
-- primary key columns
varchar5_10, ubin15_uniq , char0_10
, udec0_2000 , ubin0_1000  , varchar0_4
From BTA1P001 
Order By varchar0_4, ubin15_uniq ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    #
    # The test result could be un-deterministics by varchar0_4
    stmt = """Select [First 1]
-- primary key columns
varchar5_10, ubin15_uniq , char0_10
, udec0_2000 , ubin0_1000  , varchar0_4
From BTA1P001 
Order By varchar0_4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    #
    #  (2) Compare without and with [First 1].
    stmt = """Select
-- primary key column -- DESC
ubin3_uniq
, varchar0_4
From BTA1P002 
Order By varchar0_4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    #
    #  981120FCS -- BUG -- dies on parallel execution
    #  Program aborted in "..\common\Collections.h", line 375:
    #  referencing an unused element of a collection
    #  plan is simple but user has parallel on and specifies 2 processors:
    #  control query shape esp_exchange(sort(esp_exchange(partition_access(
    #  scan(path 'CAT11GLO.SCH11GLO.BTA1P002', forward, mdam off)))));
    stmt = """Select [First 1]
-- primary key column -- DESC
ubin3_uniq
, varchar0_4
From BTA1P002 
Order By varchar0_4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    #
    #  (3) Compare without and with [First 1].
    stmt = """Select
-- primary key columns -- DESC/ASC
cast( varchar11_2 as char(16) ) as varchar11_2
, varchar2_10, varchar15_uniq
, varchar2_100
From BTA1P003 
Order By varchar2_100 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    #
    stmt = """Select [First 1]
-- primary key columns -- DESC/ASC
cast( varchar11_2 as char(16) ) as varchar11_2
, varchar2_10, varchar15_uniq
, varchar2_100
From BTA1P003 
Order By varchar2_100 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    #
    #  (4) Compare without and with [First 1].
    stmt = """Select
-- primary key columns -- DESC/ASC
varchar13_100, sdec13_uniq, char14_20, varchar15_uniq
, ubin15_uniq
From BTA1P004 
Order By ubin15_uniq ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')
    #
    stmt = """Select [First 1]
-- primary key columns -- DESC/ASC
varchar13_100, sdec13_uniq, char14_20, varchar15_uniq
, ubin15_uniq
From BTA1P004 
Order By ubin15_uniq ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s7')
    #
    #  (5) Compare without and with [First 1].
    stmt = """Select
-- primary key columns
cReal, cFloat
, char17_2
From BTA1P005 
Order By char17_2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s8')
    #
    stmt = """Select [First 1]
-- primary key columns
cReal, cFloat
, char17_2
From BTA1P005 
Order By char17_2, cReal ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s9')
    #
    #  (6) Compare without and with [First 1].
    stmt = """Select
-- primary key columns -- ASC/DESC
sdec9_uniq, sdec0_100, sdec1_20
, sbin0_4
From BTA1P006 
Order By sbin0_4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s10')
    #
    #two rows of -2 on the sbin0_4. expected one row only but will be different
    stmt = """Select [First 1]
-- primary key columns -- ASC/DESC
sdec9_uniq, sdec0_100, sdec1_20
, sbin0_4
From BTA1P006 
Order By sbin0_4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    #
    #  Also try [First 2]
    stmt = """Select [First 2]
-- primary key columns -- ASC/DESC
sdec9_uniq, sdec0_100, sdec1_20
, sbin0_4
From BTA1P006 
Order By sbin0_4, sdec1_20 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s12')
    #
    #  (7) Compare without and with [First 1].
    stmt = """Select
-- primary key columns
cIntervalYM, cIntervalDS
, cDate
From BTA1P007 
Order By cDate ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s13')
    #
    stmt = """Select [First 1]
-- primary key columns
cIntervalYM, cIntervalDS
, cDate
From BTA1P007 
Order By cDate ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s14')
    #
    #  (8) Compare without and with [First 1].
    stmt = """Select
-- primary key column
cDate
, cTime
From BTA1P008 
Order By cTime ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s15')
    #
    stmt = """Select [First 1]
-- primary key column
cDate
, cTime
From BTA1P008 
Order By cTime ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s16')
    #
    #  (9) Compare without and with [First 1].
    stmt = """Select
-- primary key column
cBitPK
, cBitIX
From BTA1P009 
Order By cBitIX ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s17')
    #
    stmt = """Select [First 1]
-- primary key column
cBitPK
, cBitIX
From BTA1P009 
Order By cBitIX ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s18')
    
    stmt = """Control Query Shape Off;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test002(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1117:A02
    #
    #  Description:        Forced plan (nested semi join)
    #                      returned wrong results. Correct results from
    #                      hybrid hash semi join.
    #
    # =================== End Test Case Header  ===================
    #
    # ---------------------------------
    # A forced plan (nested semi join) returned a different result than
    # another forced plan (hybrid hash semi join). It's the nested semi-join
    # that's returning the wrong result.
    # ---------------------------------
    #
    # Force two different plans in order to show that one of them is broken.
    #
    # note that this error comes from a query on the TPCD tables
    # if you've got 'em already, then you can ignore the table creation and
    # population statements
    #
    # DROP/CREATE in pre-test code.
    #
    # load a few records into orders.
    #
    
    stmt = """prepare xx from
insert into ORDERS 
values(?a, ?b, ?c, ?d, cast(cast(?e as char(10)) as date), ?f, ?g, ?h, ?i);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """set param ?a 193;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?b 331;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?c 'F';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?d 102889.64;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?e '1993-08-08';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?f '1-URGENT';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?g 'Clerk#000000025';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?h 0;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?i 'C1ONm713zmnL363Qnki56xihj0gyRhLh3Q0C7jQ1njMC0i0N442PAC';"""
    output = _dci.cmdexec(stmt)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """set param ?a 226;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?b 1411;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?c 'F';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?d 278333.63;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?e '1993-03-10';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?f '2-HIGH';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?g 'Clerk#000000756';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?h 0;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?i 'g7C LNzwj34w5 LC7hM1m5CkSB7nMm0QyBxw6niy6R02MNSC4Q3n0Lx1xBNAgnLyhil50Ok4hL';"""
    output = _dci.cmdexec(stmt)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """set param ?a 259;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?b 401;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?c 'F';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?d 185844.64;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?e '1993-09-29';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?f '4-NOT SPECIFIED';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?g 'Clerk#000000601';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?h 0;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?i 'w3S1zl5 BjRNM5xN0Sn 6ii57LynimP2';"""
    output = _dci.cmdexec(stmt)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    # load a few records into lineitem
    #
    stmt = """prepare xx from insert into LINEITEM values(?a, ?b, ?c, ?d, ?e, ?f, ?g, ?h, ?i, ?j,
cast(cast(?k as char(10)) as date), cast(cast(?l as char(10)) as date),
cast(cast(?m as char(10)) as date), ?n, ?o, ?p);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """set param ?a 193;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?b 381;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?c 38;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?d 1;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?e 14;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?f 17939.32;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?g 0.06;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?h 0.03;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?i 'A';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?j 'F';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?k '1993-10-30';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?l '1993-10-09';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?m '1993-11-11';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?n 'COLLECT COD';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?o 'MAIL';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p 'glzNC5L3NAR k l771A';"""
    output = _dci.cmdexec(stmt)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """set param ?a 193;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?b 535;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?c 26;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?d 2;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?e 37;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?f 53114.61;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?g 0.05;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?h 0.00;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?i 'A';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?j 'F';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?k '1993-08-14';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?l '1993-09-24';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?m '1993-09-08';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?n 'TAKE BACK RETURN';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?o 'TRUCK';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p 'n2Qzh24mNL12Mw';"""
    output = _dci.cmdexec(stmt)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """set param ?a 1284;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?b 1855;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?c 42;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?d 2;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?e 12;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?f 21082.20;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?g 0.01;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?h 0.02;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?i 'N';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?j 'O';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?k '1996-02-23';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?l '1996-03-03';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?m '1996-03-11';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?n 'DELIVER IN PERSON';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?o 'MAIL';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p 'OSilkLgBkNSxL3 C13NCwS7h01yyRBBQPOl2Q';"""
    output = _dci.cmdexec(stmt)
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """prepare Q04BAD from SELECT o_orderkey FROM ORDERS 
WHERE o_orderdate >= DATE '1993-07-01' AND o_orderdate < DATE '1993-10-01'
AND EXISTS (SELECT * FROM LINEITEM WHERE l_orderkey = o_orderkey ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """prepare Q04GOOD from SELECT o_orderkey FROM ORDERS 
WHERE o_orderdate >= DATE '1993-07-01' AND o_orderdate < DATE '1993-10-01'
AND EXISTS (SELECT * FROM LINEITEM WHERE l_orderkey = o_orderkey ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """select cast(SEQ_NUM as numeric(2)) as SEQ,
cast(RIGHT_CHILD_SEQ_NUM as numeric(2)) as R_IGHT,
cast(LEFT_CHILD_SEQ_NUM as numeric(2)) as L_EFT,
cast(OPERATOR as char(25)) as OPERATOR,
cast(TNAME as char(25)) as TNAME,
cast(cardinality as numeric(8,2)) as EST_ROWS
from TABLE (explain(NULL,'Q04BAD')) ;"""
    output = _dci.cmdexec(stmt)
    stmt = """select cast(SEQ_NUM as numeric(2)) as SEQ,
cast(RIGHT_CHILD_SEQ_NUM as numeric(2)) as R_IGHT,
cast(LEFT_CHILD_SEQ_NUM as numeric(2)) as L_EFT,
cast(OPERATOR as char(25)) as OPERATOR,
cast(TNAME as char(25)) as TNAME,
cast(cardinality as numeric(8,2)) as EST_ROWS
from TABLE (explain(NULL,'Q04GOOD')) ;"""
    output = _dci.cmdexec(stmt)
    #
    #  notice the two plans are the same except for their root nodes
    #
    stmt = """execute Q04BAD ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    #
    #  Should be non-zero rows!
    #
    stmt = """execute Q04GOOD ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    #
    # > zero rows!
    #
    stmt = """DROP TABLE LINEITEM;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE ORDERS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Control Query Shape Off;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test003(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1117:A03 -- same as arkt1116:A07,
    #                                      but the current test is on
    #                                      partitioned tables.
    #
    #  Description:        This test verifies the SQL STRING features.
    #                      Predicates involving ANSI string functions
    #                      on update; when update primary key is supported
    #                      we can change some columns to primary keys.
    #
    # =================== End Test Case Header  ===================
    #
    #
    stmt = """set transaction autocommit off;"""
    output = _dci.cmdexec(stmt)
    
    # ---------------------------------
    # Populate table.
    # ---------------------------------
    
    stmt = """delete from depart;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into depart values
('Srinivas Morton' , 16, 'ALGORITHMS', 10, 'CS600',  'CS300', 'fall', 3
,'a');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # 04/24/09 change primary key values from A to B, since in mode_special_1
    # it's case-insensive, the insert opertion will fail
    stmt = """insert into depart values
('George Memory' , 15,  'Computer ARCHITECTURE',21, 'CS555',  'CS200', 'spring', 3
,'B');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #,'A');
    stmt = """insert into depart values
('David Crane', 15, 'Computer Graphics', 16, 'CS500', 'CS150', 'summer',3
,'x');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # 04/24/09 change primary key values from X to Y, since in mode_special_1
    # it's case-insensive, the insert opertion will fail
    stmt = """insert into depart values
('Srinivas Morton' , 16, 'Software Engineering', 20, 'CS700', 'CS300', 'fall',3
,'Y');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #,'X');
    stmt = """insert into depart values
('Simon Chu', 11, 'Computer Networks', 17, 'CS777', ' ' , 'fall', 3
,'Q');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # 04/24/09 change primary key values from q to r, since in mode_special_1
    # it's case-insensive, the insert opertion will fail
    stmt = """insert into depart values
('Simon Chu', 11,  'Data Base', 9, 'CS666', 'CS100', 'summer', 3
,'r');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    #  Check the inserted rows.
    stmt = """select PROF, CNUM, CNAME, NAMELEN, CLEN
from depart 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s0')
    stmt = """select PROF, CNUM, PREREQ, SEMESTER, CREDITS
from depart 
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    #
    #  Expect 3 rows, (('srinivas morton' 'ALGORITHMS CS600' 5)
    #  ('srinivas morton' 'SOFTWARE ENGINEERING CS700' 5)
    #  ('simon chu' 'COMPUTER NETWORKS CS777' 5))
    stmt = """select lower(prof), upper(cname || ' ' || cnum), char_length(cnum)
from depart 
where upper(lower(semester)) = 'FALL'
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    #
    stmt = """commit work ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #-------------------------
    # AS.081
    # ANSI string functions providing values for updating a group of
    # primary keys. Update primary key is not supported in 1998, so
    # leave primary key out of definition in preunit.
    #-------------------------
    #
    stmt = """begin work ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  Check which row might change.
    #
    #  Expect 6 rows with basic data.
    stmt = """select cast(lower(prof) as char(15)) as prof
, cast(namelen as smallint)    as namelen
, lower(cname)                 as cname
, cast(clen as smallint)       as clen
--       ,      clen                    as clen
, cast(lower(cnum) as char(7)) as cnum
, cast(credits as smallint)    as credits
--     ,      credits                 as credits
from depart 
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s3')
    #
    #  Expect 1 row (('simon chu' ... cs666 3))
    stmt = """select cast(lower(prof) as char(15)) as prof
, cast(namelen as smallint)    as namelen
, lower(cname)                 as cname
, cast(clen as smallint)       as clen
, cast(lower(cnum) as char(7)) as cnum
, cast(credits as smallint)    as credits
from depart 
where trim(leading 's' from
(substring(lower(prof) from 1 for 5))
) = 'imon'
and lower(semester) = 'summer'
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s4')
    #
    stmt = """update depart 
set prof    = (upper('angela' || ' ' || lower('davis') ) ),
namelen = (octet_length('angela' || ' ' || 'davis')),
cname   = (substring('Programming Languages' from 13 for 9)),
clen    = (position('s' in 'Languages')),
cnum    = (trim(both 'S' from ('SCS' || '111S') )),
credits = (char_length(substring('phoenix' from 4 for 3)))
where trim(leading 's' from
(substring(lower(prof) from 1 for 5))
) = 'imon'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    #
    #  Check result of Update.
    #  Expect 6 rows with 'angela davis' replacing 'simon chu'.
    stmt = """select cast(lower(prof) as char(15)) as prof
, cast(namelen as smallint)    as namelen
, lower(cname)                 as cname
, cast(clen as smallint)       as clen
, cast(lower(cnum) as char(5)) as cnum
, cast(credits as smallint)    as credits
from depart 
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s5')
    #
    #  Check subcomponents of update:
    #  Expect david crane's data.
    stmt = """select cast(lower(prof) as char(15)) as prof
, cast(namelen as smallint)    as namelen
, lower(cname)                 as cname
, cast(clen as smallint)       as clen
, cast(lower(cnum) as char(5)) as cnum
, cast(credits as smallint)    as credits
from depart 
where lower(prof) = 'david crane' and credits = 3
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s6')
    #
    stmt = """rollback work ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """begin work ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  Check after rollback
    stmt = """select cast(lower(prof) as char(15)) as prof
, cast(namelen as smallint)    as namelen
, lower(cname)                 as cname
, cast(clen as smallint)       as clen
, cast(lower(cnum) as char(7)) as cnum
, cast(credits as smallint)    as credits
from depart 
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s7')
    #
    # Populating table empA07
    #
    stmt = """delete from empA07 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    stmt = """insert into empA07 values
('sulu', 'kapoor', 'manager', 'female', 90000, 13, 'B'
,'K');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into empA07 values
('BHAVESH', 'MEHTA', 'ENGINEER', 'MALE', 50000, 14 , 'C'
,'J');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into empA07 values
('YUGAL', 'AGGARWAL', 'SYSADMIN', 'MALE', 80000, 14, 'D'
,'I');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into empA07 values
('ANANDHI', 'RAMASWAMY', 'PROGRAMMER', 'FEMALE', 50000, 13, 'E'
,'H');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #
    stmt = """commit work ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """begin work ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  Expect (('sulu'))
    stmt = """select first_name from empA07 
where lower(job) = 'manager'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s8')
    #  Expect (('male'))
    stmt = """select lower(gender) from empA07 
where lower(last_name) = 'mehta'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s9')
    #  Expect (('sysadmin'))
    stmt = """select lower(job) from empA07 
where lower(last_name) = 'aggarwal'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s10')
    #  Expect (('programmer'))
    stmt = """select lower(job) from empA07 
where first_name = 'ANANDHI'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s11')
    #  Expect (('kapoor' 'female'))
    stmt = """select last_name, gender from empA07 
where upper(first_name)='SULU'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s12')
    #  Expect (('aggarwal'))
    stmt = """select last_name from empA07 
where lower(first_name) = 'yugal'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s13')
    #
    # Attempt update in small, rolled-back transactions.
    stmt = """commit work ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    stmt = """update depart 
set prof = ( select first_name from empA07 
where lower(job) = 'manager')
|| ' ' || lower('KAPOOR')
where lower(prof) = 'david crane'
and credits = 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    #  Expect 6 lines, with 'sulu kapoor' for CNUM of 'cs500'.
    stmt = """select cast(lower(prof) as char(15)) as prof
, cast(namelen as smallint)    as namelen
, lower(cname)                 as cname
, cast(clen as smallint)       as clen
, cast(lower(cnum) as char(5)) as cnum
, cast(credits as smallint)    as credits
from depart 
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s14')
    #
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  Check use of scalar subquery to return character expression
    #  for argument of upper function.
    #  Expect (('SULU')).
    stmt = """select DISTINCT upper (
(select first_name from empA07 
where lower(job) = 'manager')
)
from depart 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s15')
    #  Expect (('SULU')).
    stmt = """select DISTINCT upper (( select max(first_name) from empA07 ))
from depart 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s16')
    #
    stmt = """update depart 
set prof = ( upper
( ( select first_name from empA07 
where lower(job) = 'manager') )
|| ' ' || lower('KAPOOR')
)
where
lower(prof) = 'david crane'
and credits = 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    #
    stmt = """select cast(lower(prof) as char(15)) as prof
,      namelen                 as namelen
, lower(cname)                 as cname
, cast(clen as smallint)       as clen
, cast(lower(cnum) as char(5)) as cnum
, cast(credits as smallint)    as credits
from depart 
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s17')
    #
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  Now do 4 updates, look at results, then roll back.
    stmt = """select prof
from depart 
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s18')
    #
    stmt = """update depart set
namelen = ( select octet_length(gender)
from empA07 
where lower(last_name) = 'mehta'
)
where
lower(prof) = 'david crane'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    #
    stmt = """update depart set
cname   = ( select substring(lower(job) from 1 for 7)
from empA07 
where first_name = 'ANANDHI'
)
where
lower(prof) = 'david crane'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    #
    stmt = """update depart set
clen    = ( position ( 's' in lower
(( select last_name from empA07 
where upper(first_name)='SULU' ))
) )
where
lower(prof) = 'david crane'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    #
    stmt = """update depart set
cnum    = trim ( trailing 'x' from 'CSxxx' ) ||
(( select substring( last_name from 1 for 1 )
from empA07 
where lower( first_name ) = 'yugal' ))
where
lower(prof) = 'david crane'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select cast(lower(prof) as char(15)) as prof
, cast(namelen as smallint)    as namelen
, lower(cname)                 as cname
, cast(clen as smallint)       as clen
, cast(lower(cnum) as char(5)) as cnum
, cast(credits as smallint)    as credits
from depart 
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s19')
    #
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Finally the last update/rollback before the big update.
    stmt = """update depart set
credits = ( select (char_length (
substring (gender from 1)))
from empA07 
where first_name = 'sulu'
)
where
lower(prof) = 'david crane'
and credits = 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    # If the above is incorrect, then ....
    stmt = """update depart set
credits =
(select char_length (substring (gender from 1) )
from empA07 
where first_name = 'sulu'
)
where
lower(prof) = 'david crane'
and credits = 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 0)
    #
    stmt = """select cast(lower(prof) as char(15)) as prof
, cast(namelen as smallint)    as namelen
, lower(cname)                 as cname
, cast(clen as smallint)       as clen
, cast(lower(cnum) as char(5)) as cnum
, cast(credits as smallint)    as credits
from depart 
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s20')
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """set transaction autocommit on;"""
    output = _dci.cmdexec(stmt)
    #
    stmt = """select cast(clen as smallint)       as clen
from depart 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s21')
    #
    stmt = """select cast(credits as smallint)    as credits
from depart 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s22')
    #
    # ---------------------------------
    # Empty all rows inserted into table(s) in this testcase,
    # to avoid conflict with other testcases.
    # ---------------------------------
    #
    stmt = """delete from empA07;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    stmt = """delete from depart;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 6)
    
    _testmgr.testcase_end(desc)

def test004(desc="""n01"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1117:N01
    #
    #  Description:        Negative regression test added to check fix
    #                      for Insert duplicates truncated rows
    #                      on a partitioned desc non-audited table.
    #
    # =================== End Test Case Header  ===================
    #
    
    stmt = """Set Transaction Autocommit On;"""
    output = _dci.cmdexec(stmt)
    
    #  NO AUDIT; DESC; 3 partitions.
    #  Bug showed bad data inserted AND erroneously multiple errors.
    
    stmt = """Drop Table temp4 ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """Create Table temp4 ( varchar2_10 VarChar(25) not null
, varchar11_2 VarChar(32) not null
, varchar15_uniq VarChar(8) not null
, primary key ( varchar11_2 DESC, varchar2_10 ASC, varchar15_uniq ASC )
NOT DROPPABLE ) number of partitions 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Insert Into temp4 Values ( 'CCAAKAAAAAAAAAAAAAAAAAAAAAAAAAAA', 'AB', 'BB' );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    
    stmt = """Insert Into temp4 Values ( 'CC123456789012345678901234', 'AB', 'BB' );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    
    stmt = """Insert Into temp4 Values ( 'xy12345678901234567890123', 'AB', 'BB' );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select count(*) from temp4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s3')
    stmt = """select * from temp4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s4')
    
    # NO AUDIT; remove 1 partition. ==> multiple errors. AND bad data inserted.
    stmt = """Drop Table temp4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create Table temp4 ( varchar2_10 VarChar(25) not null
, varchar11_2 VarChar(32) not null
, varchar15_uniq VarChar(8) not null
, primary key ( varchar11_2 DESC, varchar2_10 ASC, varchar15_uniq ASC )
NOT DROPPABLE) number of partitions 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Insert Into temp4 Values ( 'CCAAKAAAAAAAAAAAAAAAAAAAAAAAAAAA', 'AB', 'BB' );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    
    stmt = """Insert Into temp4 Values ( 'CC123456789012345678901234', 'AB', 'BB' );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    
    stmt = """Insert Into temp4 Values ( 'xy12345678901234567890123', 'AB', 'BB' );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select count(*) from temp4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s7')
    stmt = """select * from temp4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s8')
    
    # AUDIT; DESC; partitioning. ==> multiple errors. And no inserts on string overflow.
    stmt = """Drop Table temp4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create Table temp4 ( varchar2_10 VarChar(25) not null
, varchar11_2 VarChar(32) not null
, varchar15_uniq VarChar(8) not null
, primary key ( varchar11_2 DESC, varchar2_10 ASC, varchar15_uniq ASC )
NOT DROPPABLE ) number of partitions 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Insert Into temp4 Values ( 'CCAAKAAAAAAAAAAAAAAAAAAAAAAAAAAA', 'AB', 'BB' );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    
    stmt = """Insert Into temp4 Values ( 'CC123456789012345678901234', 'AB', 'BB' );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    
    stmt = """Insert Into temp4 Values ( 'CC12345678901234567890123', 'AB', 'BB' );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select count(*) from temp4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s11')
    
    # NO AUDIT; partitioning. ==> multiple errors.
    # Remove DESC.
    # Data inserted, trucated on the right as in Ref Man.
    # So the Executor error should be a warning.
    stmt = """Drop Table temp4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create Table temp4 ( varchar2_10 VarChar(25) not null
, varchar11_2 VarChar(32) not null
, varchar15_uniq VarChar(8) not null
, primary key ( varchar11_2 , varchar2_10, varchar15_uniq )
NOT DROPPABLE ) number of partitions 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Insert Into temp4 Values ( 'CCAAKAAAAAAAAAAAAAAAAAAAAAAAAAAA', 'AB', 'BB' );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    
    stmt = """Insert Into temp4 Values ( 'CC123456789012345678901234', 'AB', 'BB' );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    
    stmt = """Insert Into temp4 Values ( 'xy12345678901234567890123', 'AB', 'BB' );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select count(*) from temp4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s14')
    stmt = """select * from temp4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s15')
    
    # ---------------------------
    # Cleanup:
    # ---------------------------
    stmt = """Drop Table temp4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test005(desc="""r01"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt1117:R01
    #
    #  Description:        Adapted from a SQL regression test
    #                      on a partitioned table.
    #
    # =================== End Test Case Header  ===================
    
    stmt = """create table r1tabd3 
( large_int      pic s9(16) comp      no default   not null
, col_200x       pic x(200)       default ' '      not null
, primary key (large_int)
) number of partitions 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into r1tabd3 (large_int) values (  0 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into r1tabd3 (large_int) values (  1 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into r1tabd3 (large_int) values (  2 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into r1tabd3 (large_int) values (  3 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into r1tabd3 (large_int) values (  4 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into r1tabd3 (large_int) values (  5 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into r1tabd3 (large_int) values (  6 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into r1tabd3 (large_int) values (  7 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into r1tabd3 (large_int) values (  8 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into r1tabd3 (large_int) values (  9 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into r1tabd3 
(large_int) values ( 200000000000000 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into r1tabd3 
(large_int) values ( 200000000000001 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into r1tabd3 
(large_int) values ( 200000000000002 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into r1tabd3 
(large_int) values ( 200000000000003 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into r1tabd3 
(large_int) values ( 200000000000004 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into r1tabd3 
(large_int) values ( 200000000000005 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into r1tabd3 
(large_int) values ( 200000000000006 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into r1tabd3 
(large_int) values ( 200000000000007 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into r1tabd3 
(large_int) values ( 200000000000008 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into r1tabd3 
(large_int) values ( 200000000000009 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into r1tabd3 
(large_int) values ( 500000000000000 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into r1tabd3 
(large_int) values ( 500000000000001 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into r1tabd3 
(large_int) values ( 500000000000002 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into r1tabd3 
(large_int) values ( 500000000000003 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into r1tabd3 
(large_int) values ( 500000000000004 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into r1tabd3 
(large_int) values ( 500000000000005 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into r1tabd3 
(large_int) values ( 500000000000006 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into r1tabd3 
(large_int) values ( 500000000000007 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into r1tabd3 
(large_int) values ( 500000000000008 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into r1tabd3 
(large_int) values ( 500000000000009 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update statistics for table r1tabd3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  ---------------------------
    #  Select:
    #  ---------------------------
    #  Expect 30 rows.
    stmt = """select large_int from r1tabd3 
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/r01exp""", 'r01s0')
    #
    #  Expect 19 rows.
    stmt = """select large_int from r1tabd3 
where large_int > 200000000000000
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/r01exp""", 'r01s1')
    #
    #  Expect 1 row.
    stmt = """select large_int from r1tabd3 
where large_int = 200000000000000
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/r01exp""", 'r01s2')
    #
    #  Expect 10 rows.
    stmt = """select large_int from r1tabd3 
where large_int < 200000000000000
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/r01exp""", 'r01s3')
    #
    #  Expect 1 row.
    stmt = """select large_int from r1tabd3 
where large_int = 500000000000000
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/r01exp""", 'r01s4')
    #
    #  Expect 20 rows.
    stmt = """select large_int from r1tabd3 
where large_int < 500000000000000
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/r01exp""", 'r01s5')
    #
    #  Expect 9 rows.
    stmt = """select large_int from r1tabd3 
where large_int > 500000000000000
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/r01exp""", 'r01s6')
    
    # ---------------------------
    # Cleanup:
    # ---------------------------
    stmt = """Drop table r1tabd3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

