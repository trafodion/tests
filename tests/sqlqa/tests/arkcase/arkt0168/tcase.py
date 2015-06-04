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
    #  Test case name:     A01
    #  Description:        JOINS
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #
    # =================== End Test Case Header  ===================
    
    stmt = """create table a1t ( a int ) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  insert 61 rows
    
    stmt = """insert into a1t values (-30);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values (-29);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values (-28);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values (-27);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values (-26);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values (-25);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values (-24);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values (-23);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values (-22);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values (-21);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values (-20);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values (-19);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values (-18);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values (-17);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values (-16);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values (-15);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values (-14);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values (-13);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values (-12);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values (-11);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values (-10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values (-09);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values (-08);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values (-07);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values (-06);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values (-05);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values (-04);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values (-03);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values (-02);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values (-01);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values (-00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values (  1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values (  2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values (  3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values (  4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values (  5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values (  6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values (  7);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values (  8);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values (  9);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values ( 10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values ( 11);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values ( 12);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values ( 13);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values ( 14);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values ( 15);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values ( 16);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values ( 17);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values ( 18);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values ( 19);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values ( 20);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values ( 21);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values ( 22);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values ( 23);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values ( 24);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values ( 25);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values ( 26);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values ( 27);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values ( 28);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values ( 29);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1t values ( 30);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update statistics for table a1t ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """prepare p from select * from a1t where a > -20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'P'));"""
    output = _dci.cmdexec(stmt)
    
    # Note, the above query returns the time spent in the optimizer
    # This changes as the code is modified. 
    
    stmt = """create table gbat (
TEAM                CHAR( 2 ) DEFAULT ' ' NOT NULL
, GAME_NUMBER         NUMERIC( 2, 0) DEFAULT 0 NOT NULL
, NAME                CHAR( 12 ) DEFAULT ' ' NOT NULL
, AB                  NUMERIC( 2, 0) DEFAULT 0 NOT NULL
, RUN                 NUMERIC( 2, 0) DEFAULT 0 NOT NULL
, HIT                 NUMERIC( 2, 0) DEFAULT 0 NOT NULL
, RBI                 NUMERIC( 2, 0) DEFAULT 0 NOT NULL
, DOUBLES             NUMERIC( 2, 0) DEFAULT 0 NOT NULL
, TRIPLE              NUMERIC( 2, 0) DEFAULT 0 NOT NULL
, HOMERUN             NUMERIC( 2, 0) DEFAULT 0 NOT NULL
, BB                  NUMERIC( 2, 0) DEFAULT 0 NOT NULL
, SO                  NUMERIC( 2, 0) DEFAULT 0 NOT NULL
, SB                  NUMERIC( 2, 0) DEFAULT 0 NOT NULL
, CS                  NUMERIC( 2, 0) DEFAULT 0 NOT NULL
, ERROR               NUMERIC( 2, 0) DEFAULT 0 NOT NULL
, GBI                 NUMERIC( 2, 0) DEFAULT 0 NOT NULL
, INJURY              NUMERIC( 2, 0) DEFAULT 0 NOT NULL
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into gbat values
( 'Gi' , 1,'*Pitchers', 1, 0, 0, 0 , 0 , 0, 0, 0, 1, 0, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Gi' , 1,'Aldrete', 5, 2, 2, 0 , 0 , 0, 0, 0, 1, 0, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Gi' , 1,'BrownC', 2, 0, 1, 0 , 0 , 0, 0, 1, 0, 0, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Gi' , 1,'Butler', 3, 1, 1, 0 , 1 , 0, 0, 2, 1, 0, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Gi' , 1,'ClarkW', 4, 0, 1, 1 , 0 , 0, 0, 1, 1, 0, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Gi' , 1,'Maldonado', 5, 0, 1, 0 , 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Gi' , 1,'Manwaring', 4, 0, 1, 0 , 0 , 0, 0, 1, 1, 0, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Gi' , 1,'Riles', 5, 0, 2, 1 , 0 , 0, 0, 0, 1, 0, 0, 1, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Gi' , 1,'ThompsonR', 4, 0, 1, 0 , 0 , 0, 0, 1, 1, 0, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Gi' , 1,'Uribe', 1, 0, 0, 0 , 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Gi' , 1,'WilliamsM', 1, 0, 0, 0 , 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Gi' , 1,'Youngblood', 1, 0, 0, 0 , 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Gi' , 2,'*Pitchers', 2, 0, 0, 0 , 0 , 0, 0, 0, 1, 0, 0, 1, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Gi' , 2,'Aldrete', 5, 1, 2, 1 , 0 , 0, 0, 0, 2, 0, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Gi' , 2,'Butler', 4, 1, 1, 0 , 0 , 0, 0, 1, 0, 1, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Gi' , 2,'ClarkW', 2, 1, 1, 1 , 0 , 0, 0, 2, 0, 0, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Gi' , 2,'Maldonado', 4, 0, 0, 0 , 0 , 0, 0, 0, 3, 0, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Gi' , 2,'Manwaring', 3, 0, 2, 0 , 0 , 0, 0, 1, 1, 0, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Gi' , 2,'Melvin', 1, 0, 0, 0 , 0 , 0, 0, 0, 1, 0, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Gi' , 2,'Riles', 4, 1, 2, 0 , 0 , 0, 0, 0, 1, 0, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Gi' , 2,'ThompsonR', 4, 1, 1, 1 , 0 , 0, 0, 0, 3, 0, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Gi' , 2,'WilliamsM', 4, 0, 0, 0 , 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Gi' , 2,'Youngblood', 1, 0, 0, 0 , 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Me' , 1,'*Pitchers', 4, 1, 1, 2 , 0 , 0, 0, 0, 1, 0, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Me' , 1,'Backman', 4, 1, 2, 0 , 0 , 0, 0, 1, 1, 0, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Me' , 1,'Brett', 4, 1, 1, 0 , 0 , 0, 0, 1, 1, 0, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Me' , 1,'DavisJ', 1, 0, 1, 0 , 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Me' , 1,'Dykstra', 3, 2, 1, 2 , 0 , 0, 1, 1, 0, 0, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Me' , 1,'Fitzgerald', 5, 1, 2, 0 , 0 , 0, 0, 0, 0, 0, 0, 1, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Me' , 1,'JohnsonH', 4, 2, 2, 1 , 0 , 0, 0, 0, 0, 1, 1, 1, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Me' , 1,'Lansford', 5, 0, 1, 2 , 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Me' , 1,'Marshall', 4, 0, 1, 0 , 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Me' , 1,'WashingtonC', 4, 0, 2, 1 , 0 , 0, 0, 0, 0, 2, 0, 0, 0, 10
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Me' , 2,'*Pitchers', 1, 0, 0, 0 , 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Me' , 2,'Backman', 4, 0, 2, 1 , 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Me' , 2,'Borders', 1, 0, 0, 0 , 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Me' , 2,'Brett', 4, 0, 1, 0 , 0 , 0, 0, 1, 0, 0, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Me' , 2,'DavisJ', 1, 0, 0, 0 , 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Me' , 2,'Dykstra', 4, 2, 2, 1 , 0 , 0, 0, 0, 0, 1, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Me' , 2,'Elster', 1, 0, 0, 0 , 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Me' , 2,'Fitzgerald', 2, 1, 1, 1 , 0 , 0, 0, 1, 0, 0, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Me' , 2,'Hubbard', 2, 0, 1, 2 , 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Me' , 2,'Jennings', 3, 1, 1, 0 , 0 , 0, 0, 1, 1, 0, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Me' , 2,'JohnsonH', 4, 1, 1, 0 , 1 , 0, 0, 0, 0, 0, 0, 1, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Me' , 2,'Lansford', 3, 0, 1, 0 , 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Me' , 2,'Leonard', 0, 0, 0, 0 , 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Me' , 2,'Marshall', 3, 0, 0, 0 , 0 , 0, 0, 0, 3, 0, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Me' , 2,'MurphyDa', 1, 0, 0, 0 , 0 , 0, 0, 1, 0, 0, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Me' , 2,'Pendleton', 1, 0, 1, 1 , 0 , 0, 0, 0, 0, 0, 0, 0, 1, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into gbat values
( 'Me' , 2,'WilsonW', 1, 1, 1, 0 , 0 , 0, 0, 0, 0, 1, 0, 0, 0, 0
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create table  factor (
ADDER               NUMERIC( 2, 0) DEFAULT 0 NOT NULL
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into  factor values (-2 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  factor values (-1 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  factor values ( 0 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  factor values ( 1 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select team,name, sum(hit),sum(ab),abf.adder
from gbat,
 factor abf
where
--          (sum(ab) = 0 and abf.adder = 1) or
--          (sum(ab) <> 0 and abf.adder = 0)
(ab = 0 and abf.adder = 1) or
(ab <> 0 and abf.adder = 0)
group by team, name, abf.adder
order by 1, 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    
    #   Join query involving a non-equi-join predicate returned
    #   TOO MANY rows when query also contained a GROUP BY that
    #   referenced one of the join columns:
    
    stmt = """select x.homerun from gbat x order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    
    stmt = """select count(*) from gbat x, gbat y order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    
    stmt = """select count(*) from gbat x,
 gbat y where x.homerun  > y.homerun order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    
    stmt = """select count(* )
from gbat x,
 gbat y
where x.homerun  > y.homerun
group by x.homerun
order by 1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    
    stmt = """drop table gbat ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table  factor ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE TABLE program 
(ID                   CHAR(6)        NO DEFAULT not null
,code_name            VARCHAR(30)
,description          VARCHAR(255)
,state                CHAR(1)        DEFAULT 'U'  -- Defined or Undefined
,type                 CHAR(1)        DEFAULT 'D'  -- Dev or Rel??
,PRIMARY KEY (ID ASCENDING));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table program 
ADD CHECK (ID LIKE 'G%') ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO program 
VALUES ('G0001', 'Poppy', 'New Disc Drive', 'D', 'D');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO program 
VALUES ('G0002', 'Carpet', 'Increase wordiness of code by 50%'
,  'D', 'D');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO program 
VALUES ('G0003', 'Bloat',  'Rewrite everything', 'U', 'D');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO program 
VALUES ('G0004', 'Flower', 'Support for Poppy features', 'D', 'D');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """CREATE TABLE project 
(ID                   CHAR(6)        NO DEFAULT not null
,code_name            VARCHAR(30)
,product_number       CHAR(6)
,name                 VARCHAR(30)
,description          VARCHAR(255)
,class1               CHAR(1)        -- Hw, Sw, or Pubs
,type                 CHAR(1)        -- New, Enh, or Maint
,PRIMARY KEY (ID ASCENDING)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table project 
ADD CHECK (ID LIKE 'P%') ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table project 
ADD CHECK (class1 LIKE 'H' OR class1 LIKE 'S' OR class1 LIKE 'P') ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table project 
ADD CHECK (type LIKE 'N' OR type LIKE 'E' OR type LIKE 'M') ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO project 
VALUES ('P0001', 'Poppy', '12345','2222 Drive'
,'High Density Disk Drive', 'H','N');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO project 
VALUES ('P0002', 'Doofus', 'T9000','NonStop Blat'
,'Adding support for Poppy','S','E');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO project 
VALUES ('P0003', 'Foob', 'T9999','Enfold'
,'Yet another new product','S','N');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO project 
VALUES ('P0004', 'Carpet', 'T9002','Doormat'
,'Latest version of doormat','S','M');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """CREATE TABLE product 
(product_number       CHAR(6)        NO DEFAULT not null
,name                 VARCHAR(30)
,description          VARCHAR(255)
,class1               CHAR(1)        -- Hw, Sw, or Pubs
,distribution         CHAR(1)        -- Standard or Optional
,PRIMARY KEY (product_number ASCENDING)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table product 
ADD CHECK (
(product_number LIKE 'T%' AND class1 LIKE 'S')
OR (product_number LIKE '%' AND class1 LIKE 'P')
OR (product_number LIKE '%' AND class1 LIKE 'H')
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table product 
ADD CHECK (class1 LIKE 'H' OR class1 LIKE 'S' OR class1 LIKE 'P'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table product 
ADD CHECK (distribution LIKE 'S' OR distribution LIKE 'O'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO product 
VALUES ('12345','2222 Disc','High Density Disk Drive', 'H','O');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO product 
VALUES ('T9001','NonStop Blat','Adding support for Poppy','S','O');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO product 
VALUES ('T9999','Enfold','Revolutionary Database','S','O');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO product 
VALUES ('T9002','Escapade','OLTP Application Tool','S','S');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """CREATE TABLE projprog 
(project_ID           CHAR(6)  not null
,program_ID           CHAR(6)  not null
,PRIMARY KEY (
program_ID ASCENDING
,             project_ID ASCENDING
)
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ALTER TABLE projprog 
ADD CHECK (project_ID LIKE 'P%') ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """alter table projprog 
ADD CHECK (program_ID LIKE 'G%') ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO projprog VALUES ('P0001', 'G0001');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO projprog VALUES ('P0004', 'G0002');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO projprog VALUES ('P0001', 'G0004');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO projprog VALUES ('P0002', 'G0004');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # sproj shorthand view
    stmt = """CREATE VIEW sproj 
(
proj_ID
,proj_code_name
,prod_number
,proj_description
,proj_class
,proj_type
,prod_name
,prod_class
,prod_distribution
,prog_code_name
,prog_description
,prog_state
,prog_type
)
AS SELECT
 project.ID
,project.code_name
,project.product_number
,project.description
,project.class1
,project.type
,product.name
,product.class1
,product.distribution
,program.code_name
,program.description
,program.state
,program.type
FROM  projprog,
 program,
 project,
 product 
WHERE
(program.ID = projprog.program_ID)
AND (project.ID =projprog.project_ID)
OR NOT (EXISTS (SELECT project_ID FROM projprog 
WHERE project.ID = projprog.project_ID)
)    

AND (project.product_number = product.product_number)
OR NOT (EXISTS (SELECT product_number
FROM product 
WHERE project.product_number = product.product_number)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from sproj where proj_id = 'P0004' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')
    
    stmt = """DROP VIEW  sproj;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE program       ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE project       ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE product       ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE projprog      ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """prepare p from
select max(small_int) from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'P'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # Note, the above query returns the time spent in the optimizer
    # This changes as the code is modified.  So just move the Logaa01
    # file to logea01
    
    #  No longer get problem when DELETE using avail. UNIQUE index.
    
    stmt = """create table a1tabf1 
( large_int      largeint signed   default 0   not null
, col_200x       pic x(200)        default ' ' not null
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create unique index a1tabfi 
on a1tabf1 ( large_int );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a1tabf1 (large_int) values ( 0 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1tabf1 (large_int) values ( 1 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1tabf1 (large_int) values ( 2 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1tabf1 (large_int) values ( 3 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1tabf1 (large_int) values ( 4 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1tabf1 (large_int) values ( 5 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1tabf1 (large_int) values ( 6 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1tabf1 (large_int) values ( 7 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1tabf1 (large_int) values ( 8 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1tabf1 (large_int) values ( 9 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """prepare p from
delete from a1tabf1 where large_int = 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'P'));"""
    output = _dci.cmdexec(stmt)
    
    # Note, the above query returns the time spent in the optimizer
    # This changes as the code is modified.  So just move the Logaa01
    # file to logea01
    
    stmt = """delete from a1tabf1 where large_int = 4 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select large_int from a1tabf1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s11')
    
    stmt = """create table a1tabd1 
( large_int      largeint signed   default 0    not null
, col_200x       pic x(200)        default ' '  not null
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index a1tabd1i on
 a1tabd1 ( large_int );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table a1tabd2 
( large_int    numeric (18) signed    no default   not null
, primary key ( large_int desc )
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a1tabd1 
(large_int) values ( 1234567890 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1tabd1 
(large_int) values ( 12345678901 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1tabd1 
(large_int) values ( 123456789012 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1tabd1 
(large_int) values ( 1234567890123 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1tabd1 
(large_int) values ( 12345678901234 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1tabd1 
(large_int) values ( 123456789012345 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1tabd1 
(large_int) values ( 1234567890123456 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1tabd1 
(large_int) values ( 12345678901234567 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1tabd1 
(large_int) values ( 123456789012345678 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1tabd1 
(large_int) values ( 123456789012345679 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1tabd1 
(large_int) values ( 123456789012345680 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update statistics for table a1tabd1 ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into a1tabd2 values ( 1234567890120 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1tabd2 values ( 1234567890121 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1tabd2 values ( 1234567890122 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1tabd2 values ( 1234567890123 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1tabd2 values ( 1234567890124 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1tabd2 values ( 1234567890125 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1tabd2 values ( 1234567890126 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1tabd2 values ( 1234567890127 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1tabd2 values ( 1234567890128 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1tabd2 values ( 1234567890129 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update statistics for table a1tabd2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select large_int from a1tabd1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s12')
    
    stmt = """select large_int from a1tabd1 
where large_int > 123456789012 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s13')
    stmt = """select large_int from a1tabd1 
where large_int < 12345678901234 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s14')
    stmt = """select large_int from a1tabd1 
where 123456789012345 > large_int ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s15')
    stmt = """select large_int from a1tabd1 
where large_int = 1234567890123456 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s16')
    stmt = """select large_int from a1tabd1 
where large_int > 12345678901234567 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s17')
    
    stmt = """select * from a1tabd2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s18')
    stmt = """select large_int from a1tabd2 
where large_int = 1234567890123 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s19')
    
    stmt = """Drop table a1tabd1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """Drop table a1tabd2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table a1tabc1 
( col_a          pic x   default ' ' not null
, col_b          pic x   default ' ' not null
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index a1tabc1i on
 a1tabc1 ( col_a, col_b );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a1tabc1 values ( 'C' , 'C' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1tabc1 values ( 'E' , 'D' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1tabc1 values ( 'E' , 'E' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1tabc1 values ( 'E' , 'F' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1tabc1 values ( 'G' , 'L' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1tabc1 values ( 'G' , 'M' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1tabc1 values ( 'G' , 'N' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into a1tabc1 values ( 'M' , 'M' ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from a1tabc1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s20')
    
    stmt = """select * from a1tabc1 where col_a , col_b
between 'C', 'E' and  'G', 'M'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s21')
    
    #  Also, SELECT on primary key or alternate index including parameters
    #  multi-values predicates on a table with an index.
    #  With params:
    
    stmt = """set param ?p1 'C' ;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p2 'E' ;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p3 'G' ;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p4 'M' ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from a1tabc1 where col_a , col_b
between ?p1, ?p2 and  ?p3, ?p4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s22')
    
    stmt = """prepare p from
select * from a1tabc1 
where col_a , col_b between 'C', 'E' and  'G', 'M';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'P'));"""
    output = _dci.cmdexec(stmt)
    
    # Note, the above query returns the time spent in the optimizer
    # This changes as the code is modified.  So just move the Logaa01
    # file to logea01
    
    #  Also, SELECTs with multi-values predicates on a primary or
    #  alternate index (including parameters) no longer cause the query
    #  to fail.
    #  Explain plan for
    
    stmt = """prepare p from
select * from a1tabc1 
where col_a , col_b between ?p1, ?p2 and  ?p3, ?p4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'P'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select pic_x_a , pic_x_b , pic_x_c
from """ + gvars.g_schema_arkcasedb + """.btsel06;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s25')
    
    stmt = """select pic_x_a , pic_x_b , pic_x_c
from """ + gvars.g_schema_arkcasedb + """.btsel06 
where pic_x_a , pic_x_b
between 'k', 'E' and  't', 'D';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s26')
    
    stmt = """prepare p from
select pic_x_a, pic_x_b, pic_x_c
from """ + gvars.g_schema_arkcasedb + """.btsel06 
where pic_x_a , pic_x_b
between 'k', 'E' and  't', 'D';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #  Complete support for INSERT with RETURNING for dynamic SQL.
    #  NO TEST HERE - need to add to dynamic SQL tests.
    
    #  Correct closing of cursors for inner table of a join of more than
    #  3 tables in a join and 1 join predicate specified for a pair of
    #  joining tables; or where join predicate connected by OR.
    #  NO TEST HERE.
    #  Correct records are now returned on a join query where a
    #  merge-join occurs.
    #  NO TEST HERE.
    #  These examples omitted - have the form said to cause merge join,
    #  but end up causing a nested join:
    #  select * from .btsel10
    #              , .btsel11
    #     where btsel10.pic_9_7 = btsel11.pic_9_7
    #       and btsel10.binary_unsigned = btsel11.binary_unsigned
    #  ;
    #  select * from .btsel11
    #              , .btsel12
    #     where btsel11.pic_x_a = btsel12.data_x3
    #       and btsel11.binary_unsigned = btsel12.data_93
    #  ;
    
    stmt = """drop index a1tabc1i;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop index a1tabfi;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table a1t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table a1tabf1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table a1tabc1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test002(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A02
    #  Description:        This test verifies the SQL <specify>
    #                      feature.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    stmt = """create table a3table1 (
MERC                pic x     DEFAULT ' ' NOT NULL
, TV                  pic xx    DEFAULT ' ' NOT NULL
, TPO_LIQ             pic xx    DEFAULT ' ' NOT NULL
, CASA                pic x(5)  DEFAULT ' ' NOT NULL
, NOPER               pic 9(5)         DEFAULT 0 NOT NULL
, NEMIS               pic 9(3)         DEFAULT 0 NOT NULL
, VOLUMEN             pic s9(13) comp  DEFAULT 0 NOT NULL
, IMPORTE             pic s9(16)v9(2)  DEFAULT 0 NOT NULL
,PRIMARY KEY (
casa       ASCENDING
,             tv         ASCENDING
,             tpo_liq    ASCENDING
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a3table1 values
('A' , 'B' , '24' , 'PRIME'  , 5 , 5 , 1000 , 2000 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into a3table1 values
('A' , 'B' , '24' , 'VFI'    , 5 , 5 , 1000 , 2000 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select casa, sum(noper), sum(nemis), sum(volumen), sum(importe)
from a3table1 
group by casa
order by casa
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    
    stmt = """insert into a3table1 values
('A' , 'B' , '25' , 'VFI'    , 5 , 5 , 1000 , 2000 ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select casa, sum(noper), sum(nemis), sum(volumen), sum(importe)
from a3table1 
group by casa
order by casa
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    
    stmt = """drop table a3table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test003(desc="""a05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A05
    #  Description:        This test verifies the SQL <specify>
    #                      feature.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    stmt = """create table d1tabd1 
( name           char(30) default ' '   not null
, item_long_name_of_this_column
varchar(50) default ' '   not null
, phone_long_name_of_this_column
char(10) default ' '   not null
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set param ?name 'under14' ;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?namex 'excessively large value - over 14' ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into d1tabd1 ( name )
values ( ?name ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into d1tabd1 ( item_long_name_of_this_column)
values ( ?name ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into d1tabd1 ( phone_long_name_of_this_column)
values ( ?name ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into d1tabd1 
values ( ?name , ?name , ?name ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into d1tabd1 ( phone_long_name_of_this_column)
values ( ?namex) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    stmt = """insert into d1tabd1 ( item_long_name_of_this_column)
values ( ?namex) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into d1tabd1 ( name )
values ( ?namex) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    stmt = """insert into d1tabd1 
values ( ?namex, ?namex, ?namex) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    stmt = """select * from d1tabd1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s6')
    
    stmt = """Drop table d1tabd1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Now do it again which the order of columns slightly different
    # So should only get warnings this time.
    
    stmt = """create table d1tabd1 
( phone_long_name_of_this_column
char(10) default ' '   not null
, name           char(30) default ' '   not null
, item_long_name_of_this_column
varchar(50) default ' '   not null
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set param ?name 'under14' ;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?namex 'excessively large value - over 14' ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into d1tabd1 ( name )
values ( ?name ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into d1tabd1 ( item_long_name_of_this_column)
values ( ?name ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into d1tabd1 ( phone_long_name_of_this_column)
values ( ?name ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into d1tabd1 
values ( ?name , ?name , ?name ) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into d1tabd1 ( phone_long_name_of_this_column)
values ( ?namex) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    stmt = """insert into d1tabd1 ( item_long_name_of_this_column)
values ( ?namex) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into d1tabd1 ( name )
values ( ?namex) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    stmt = """insert into d1tabd1 
values ( ?namex, ?namex, ?namex) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    stmt = """select * from d1tabd1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s10')
    
    stmt = """Drop table d1tabd1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

