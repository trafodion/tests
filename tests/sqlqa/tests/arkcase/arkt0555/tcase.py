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
    #  Test case name:     testA01
    #  Description:        This test verifies the SQL single
    #			table SELECT queries. Tests concatenation
    #			with Params.
    #  Test Objectives:	To test the usage of '||' both
    #			syntactically and for correctness of the
    #			resultant data.  Also to check on the
    #			appropriate error message for wrong usage.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    stmt = """CREATE TABLE xlong 
( CH1 CHAR(4000)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SELECT VARCHAR1_UNIQ || '   '||''||VARCHAR1_UNIQ
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    
    # The Result will be
    # "Robert John abc"
    
    # concatenation of Param with literal
    # Hello ,Robert John"
    
    stmt = """SET PARAM ?P1 'Hello ,';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT (?P1 || 'Robert John' ),('Robert John'|| ?P1)
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    
    # concatenation of 2 params
    # "Hello ,Robert John Smith"
    
    stmt = """SET PARAM ?P1 'HELLO ,';"""
    output = _dci.cmdexec(stmt)
    stmt = """SET PARAM ?P2 ' ROBERT JOHN SMITH ';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT (?P1 || ?P2 )
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    
    # Concatenation of PARAM with columns
    # ABC00001265
    # ABC00001106
    # ABC00001421
    # ABC00000150
    # ABC00001382
    
    stmt = """SET PARAM ?P1 'ABC';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT (?P1 || CHAR0_09_UNIQ),CHAR0_09_UNIQ,CHAR0_AZ_UNIQ
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    
    # 00001265ABC
    # 00001106ABC
    # 00001421ABC
    # 00000150ABC
    # 00001382ABC
    
    stmt = """SET PARAM ?P1 'ABC';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT ( CHAR0_09_UNIQ || ?P1),CHAR0_09_UNIQ
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    
    # concatenation in use with UPSHIFT function & Params
    # XYYZ012300001265
    # XYYZ012300001106
    # XYYZ012300001421
    # XYYZ012300000150
    
    stmt = """SET PARAM ?P1 'xyyz0123';"""
    output = _dci.cmdexec(stmt)
    stmt = """SELECT ( UPSHIFT(?P1 ||CHAR0_09_UNIQ) ),CHAR0_AZ_UNIQ
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    
    # This is for NULL values with concatenation
    # Result is Null for the expn
    
    stmt = """SET PARAM ?P1 'zzz';"""
    output = _dci.cmdexec(stmt)
    stmt = """SET PARAM ?I -1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT ( UPSHIFT(?P1) || UPSHIFT(CHAR0_AZ_UNIQ))
,CHAR0_AZ_UNIQ
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')
    
    stmt = """SET PARAM ?P1 'ZZZ';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT ( UPSHIFT(?P1) || UPSHIFT(CHAR0_AZ_UNIQ))
,?P1 || CHAR0_09_UNIQ ,CHAR0_AZ_UNIQ
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s7')
    
    stmt = """SELECT MAX(VARCHAR1_UNIQ||CHAR0_09_UNIQ),VARCHAR1_UNIQ
,CHAR0_09_UNIQ
FROM b3uns01 
WHERE UDEC1_UNIQ < 5
GROUP BY VARCHAR0_MONEY_100, CHAR0_AZ_UNIQ,
VARCHAR1_UNIQ, CHAR0_09_UNIQ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s8')
    
    stmt = """SELECT ( '' || CHAR0_09_UNIQ ||'')
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s9')
    
    stmt = """SELECT CHAR1_AZ_2 || CHAR1_COLCHSET_4
FROM b3uns05 
WHERE SBIN0_UNIQ < 5
UNION
SELECT CHAR0_09_UNIQ || CHAR0_AZ_UNIQ
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s10')
    
    stmt = """set param ?p 'y';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select char0_az_uniq
from b3uns01 
where upshift(char0_az_uniq || ?p) = 'AGAAAAAAY';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s11')
    
    stmt = """SELECT CHAR0_09_UNIQ || CHAR0_09_UNIQ || CHAR0_09_UNIQ ||
VARCHAR0_MONEY_100 || CHAR0_AZ_UNIQ || CHAR0_09_UNIQ ||
VARCHAR0_AZAZ_20 || VARCHAR0_AZAZ_20 || CHAR0_AZ_UNIQ ||
CHAR0_AAZY_UNIQ || VARCHAR1_AAZZB_500 || CHAR0_AAZY_UNIQ ||
CHAR1_AAZZ09BP_UNIQ || VARCHAR1_ASCII_UNIQ ||
VARCHAR1_ASCII_UNIQ || VARCHAR1_ASCII_UNIQ ||
VARCHAR1_UNIQ || CHAR1_AAZZ09BP_UNIQ || VARCHAR1_UNIQ ||
VARCHAR0_AZAZ_20 || CHAR1_AAZZ09BP_UNIQ || VARCHAR1_UNIQ ||
CHAR0_AZ_UNIQ || VARCHAR1_AAZZB_500 || VARCHAR1_AAZZB_500 ||
VARCHAR1_ASCII_UNIQ || CHAR0_09_UNIQ || CHAR0_AAZY_UNIQ ||
VARCHAR0_MONEY_100 || VARCHAR0_MONEY_100 || VARCHAR1_UNIQ ||
VARCHAR1_UNIQ || VARCHAR1_ASCII_UNIQ || CHAR1_AAZZ09BP_UNIQ  ||
VARCHAR1_AAZZB_500 || CHAR0_AAZY_UNIQ || VARCHAR0_AZAZ_20 ||
CHAR0_AZ_UNIQ || VARCHAR0_MONEY_100 || CHAR0_09_UNIQ ||
CHAR0_09_UNIQ || VARCHAR0_MONEY_100 || CHAR0_AZ_UNIQ ||
VARCHAR0_AZAZ_20 || CHAR0_AAZY_UNIQ || VARCHAR1_AAZZB_500 ||
CHAR1_AAZZ09BP_UNIQ || VARCHAR1_UNIQ || VARCHAR1_UNIQ ||
CHAR1_AAZZ09BP_UNIQ || CHAR1_AAZZ09BP_UNIQ
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s12')
    
    stmt = """SELECT CHAR0_09_UNIQ || CHAR0_09_UNIQ || CHAR0_09_UNIQ ||
VARCHAR0_MONEY_100 || CHAR0_AZ_UNIQ || CHAR0_09_UNIQ ||
VARCHAR0_AZAZ_20 || VARCHAR0_AZAZ_20 || CHAR0_AZ_UNIQ ||
CHAR0_AAZY_UNIQ || VARCHAR1_AAZZB_500 || CHAR0_AAZY_UNIQ ||
CHAR1_AAZZ09BP_UNIQ || VARCHAR1_ASCII_UNIQ ||
VARCHAR1_ASCII_UNIQ || VARCHAR1_ASCII_UNIQ ||
VARCHAR1_UNIQ || CHAR1_AAZZ09BP_UNIQ || VARCHAR1_UNIQ ||
VARCHAR0_AZAZ_20 || CHAR1_AAZZ09BP_UNIQ || VARCHAR1_UNIQ ||
CHAR0_AZ_UNIQ || VARCHAR1_AAZZB_500 || VARCHAR1_AAZZB_500 ||
VARCHAR1_ASCII_UNIQ || CHAR0_09_UNIQ || CHAR0_AAZY_UNIQ ||
VARCHAR0_MONEY_100 || VARCHAR0_MONEY_100 || VARCHAR1_UNIQ ||
VARCHAR1_UNIQ || VARCHAR1_ASCII_UNIQ || CHAR1_AAZZ09BP_UNIQ  ||
VARCHAR1_AAZZB_500 || CHAR0_AAZY_UNIQ || VARCHAR0_AZAZ_20 ||
CHAR0_AZ_UNIQ || VARCHAR0_MONEY_100 || CHAR0_09_UNIQ ||
CHAR0_09_UNIQ || VARCHAR0_MONEY_100 || CHAR0_AZ_UNIQ ||
VARCHAR0_AZAZ_20 || CHAR0_AAZY_UNIQ || VARCHAR1_AAZZB_500 ||
CHAR1_AAZZ09BP_UNIQ || VARCHAR1_UNIQ || VARCHAR1_UNIQ ||
CHAR1_AAZZ09BP_UNIQ || CHAR1_AAZZ09BP_UNIQ ||
CHAR0_09_UNIQ || CHAR0_09_UNIQ || CHAR0_09_UNIQ ||
VARCHAR0_MONEY_100 || CHAR0_AZ_UNIQ || CHAR0_09_UNIQ ||
VARCHAR0_AZAZ_20 || VARCHAR0_AZAZ_20 || CHAR0_AZ_UNIQ ||
CHAR0_AAZY_UNIQ || VARCHAR1_AAZZB_500 || CHAR0_AAZY_UNIQ ||
CHAR1_AAZZ09BP_UNIQ || VARCHAR1_ASCII_UNIQ ||
VARCHAR1_ASCII_UNIQ || VARCHAR1_ASCII_UNIQ ||
VARCHAR1_UNIQ || CHAR1_AAZZ09BP_UNIQ || VARCHAR1_UNIQ ||
VARCHAR0_AZAZ_20 || CHAR1_AAZZ09BP_UNIQ || VARCHAR1_UNIQ ||
CHAR0_AZ_UNIQ || VARCHAR1_AAZZB_500 || VARCHAR1_AAZZB_500 ||
VARCHAR1_ASCII_UNIQ || CHAR0_09_UNIQ || CHAR0_AAZY_UNIQ ||
VARCHAR0_MONEY_100 || VARCHAR0_MONEY_100 || VARCHAR1_UNIQ ||
VARCHAR1_UNIQ || VARCHAR1_ASCII_UNIQ || CHAR1_AAZZ09BP_UNIQ  ||
VARCHAR1_AAZZB_500 || CHAR0_AAZY_UNIQ || VARCHAR0_AZAZ_20 ||
CHAR0_AZ_UNIQ || VARCHAR0_MONEY_100 || CHAR0_09_UNIQ ||
CHAR0_09_UNIQ || VARCHAR0_MONEY_100 || CHAR0_AZ_UNIQ ||
VARCHAR0_AZAZ_20 || CHAR0_AAZY_UNIQ || VARCHAR1_AAZZB_500 ||
CHAR1_AAZZ09BP_UNIQ || VARCHAR1_UNIQ || VARCHAR1_UNIQ ||
CHAR1_AAZZ09BP_UNIQ || CHAR1_AAZZ09BP_UNIQ
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s13')
    
    stmt = """INSERT INTO xlong values
('once upon a time' || 'there is a story ' ||  ' telling story   ' ||
'April rain is falling down  ' || '  Spring time is here already ' ||
'once upon a time' || 'there is a story ' ||  ' telling story   ' ||
'April rain is falling down  ' || '  Spring time is here already ' ||
'April rain is falling down  ' || '  Spring time is here already ' ||
'once upon a time' || 'there is a story ' ||  ' telling story   ' ||
'April rain is falling down  ' || '  Spring time is here already ' ||
'April rain is falling down  ' || '  Spring time is here already ' ||
'once upon a time' || 'there is a story ' ||  ' telling story   ' ||
'April rain is falling down  ' || '  Spring time is here already ' ||
'April rain is falling down  ' || '  Spring time is here already ' ||
'once upon a time' || 'there is a story ' ||  ' telling story   ' ||
'April rain is falling down  ' || '  Spring time is here already ' ||
'April rain is falling down  ' || '  Spring time is here already ' ||
'once upon a time' || 'there is a story ' ||  ' telling story   ' ||
'April rain is falling down  ' || '  Spring time is here already ' ||
'April rain is falling down  ' || '  Spring time is here already ' ||
'once upon a time' || 'there is a story ' ||  ' telling story   ' ||
'April rain is falling down  ' || '  Spring time is here already ' ||
'April rain is falling down  ' || '  Spring time is here already ' ||
'once upon a time' || 'there is a story ' ||  ' telling story   ' ||
'April rain is falling down  ' || '  Spring time is here already ' ||
'April rain is falling down  ' || '  Spring time is here already ' ||
'once upon a time' || 'there is a story ' ||  ' telling story   ' ||
'April rain is falling down  ' || '  Spring time is here already ' ||
'April rain is falling down  ' || '  Spring time is here already ' ||
'once upon a time' || 'there is a story ' ||  ' telling story   ' ||
'April rain is falling down  ' || '  Spring time is here already ' ||
'April rain is falling down  ' || '  Spring time is here already ' ||
'once upon a time' || 'there is a story ' ||  ' telling story   ' ||
'April rain is falling down  ' || '  Spring time is here already ' ||
'April rain is falling down  ' || '  Spring time is here already ' ||
'once upon a time' || 'there is a story ' ||  ' telling story   ' ||
'April rain is falling down  ' || '  Spring time is here already ' ||
'April rain is falling down  ' || '  Spring time is here already ' ||
'once upon a time' || 'there is a story ' ||  ' telling story   ' ||
'April rain is falling down  ' || '  Spring time is here already ' ||
'April rain is falling down  ' || '  Spring time is here already ' ||
'once upon a time' || 'there is a story ' ||  ' telling story   ' ||
'April rain is falling down  ' || '  Spring time is here already ' ||
'April rain is falling down  ' || '  Spring time is here already ' ||
'once upon a time' || 'there is a story ' ||  ' telling story   ' ||
'April rain is falling down  ' || '  Spring time is here already ' ||
'April rain is falling down  ' || '  Spring time is here already ' ||
'once upon a time' || 'there is a story ' ||  ' telling story   ' ||
'April rain is falling down  ' || '  Spring time is here already ' ||
'April rain is falling down  ' || '  Spring time is here already ' ||
'once upon a time' || 'there is a story ' ||  ' telling story   ' ||
'April rain is falling down  ' || '  Spring time is here already ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """SELECT * FROM xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    stmt = """CREATE VIEW vt (v_col) as
(SELECT CHAR0_09_UNIQ || CHAR0_09_UNIQ || CHAR0_09_UNIQ ||
VARCHAR0_MONEY_100 || CHAR0_AZ_UNIQ || CHAR0_09_UNIQ ||
VARCHAR0_AZAZ_20 || VARCHAR0_AZAZ_20 || CHAR0_AZ_UNIQ ||
CHAR0_AAZY_UNIQ || VARCHAR1_AAZZB_500 || CHAR0_AAZY_UNIQ ||
CHAR1_AAZZ09BP_UNIQ || VARCHAR1_ASCII_UNIQ ||
VARCHAR1_ASCII_UNIQ || VARCHAR1_ASCII_UNIQ ||
VARCHAR1_UNIQ || CHAR1_AAZZ09BP_UNIQ || VARCHAR1_UNIQ ||
VARCHAR0_AZAZ_20 || CHAR1_AAZZ09BP_UNIQ || VARCHAR1_UNIQ ||
CHAR0_AZ_UNIQ || VARCHAR1_AAZZB_500 || VARCHAR1_AAZZB_500 ||
VARCHAR1_ASCII_UNIQ || CHAR0_09_UNIQ || CHAR0_AAZY_UNIQ ||
VARCHAR0_MONEY_100 || VARCHAR0_MONEY_100 || VARCHAR1_UNIQ ||
VARCHAR1_UNIQ || VARCHAR1_ASCII_UNIQ || CHAR1_AAZZ09BP_UNIQ  ||
VARCHAR1_AAZZB_500 || CHAR0_AAZY_UNIQ || VARCHAR0_AZAZ_20 ||
CHAR0_AZ_UNIQ || VARCHAR0_MONEY_100 || CHAR0_09_UNIQ ||
CHAR0_09_UNIQ || VARCHAR0_MONEY_100 || CHAR0_AZ_UNIQ ||
VARCHAR0_AZAZ_20 || CHAR0_AAZY_UNIQ || VARCHAR1_AAZZB_500 ||
CHAR1_AAZZ09BP_UNIQ || VARCHAR1_UNIQ || VARCHAR1_UNIQ ||
CHAR1_AAZZ09BP_UNIQ || CHAR1_AAZZ09BP_UNIQ
FROM b3uns01 
WHERE UDEC1_UNIQ < 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SELECT * FROM vt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s15')
    
    # ---------------------------------
    # Cleanup section
    # ---------------------------------
    
    stmt = """drop view vt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table xlong;"""
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
    #  Test case name:     testA02
    #  Description:        This test verifies the SQL substring.
    #  Test Objectives:    To test the SUBSTRING function in
    #			isolation and nested with other string
    #			functions.  Test with params, with literals,
    #			chars, and varchar data type where char
    #			expressions are needed.  Also test for
    #			boundary conditions.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # Create LOG file
    
    stmt = """CREATE TABLE x 
(X1 CHAR(4)
,X2 CHAR(2)  NOT NULL) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO x 
VALUES( 'abc','ab');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO x 
VALUES( null,'yz');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO x 
VALUES( NULL,'00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO x 
VALUES( '1234','12');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """CREATE TABLE xlong 
( CH1 CHAR(4000)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO xlong 
( SELECT SUBSTRING(X1 FROM 1 FOR 3) FROM x);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 4)
    
    #  "John Smith"
    
    stmt = """SELECT SUBSTRING('Robert John Smith' FROM 8 FOR 15),CHAR0_AZ_UNIQ
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    
    #  "Robe"
    
    stmt = """SELECT CHAR0_09_UNIQ,SUBSTRING('Robert John Smith' FROM 0 FOR 5)
,CHAR0_AZ_UNIQ
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    
    stmt = """SELECT CHAR0_09_UNIQ,
SUBSTRING('Robert John Smith' FROM 5 FOR 0),
CHAR0_AZ_UNIQ
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    
    stmt = """SELECT CHAR0_09_UNIQ,
SUBSTRING('Robert John Smith' FROM 17 FOR 1)
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    
    stmt = """SELECT CHAR0_09_UNIQ, SUBSTRING('Robert John Smith' FROM 8)
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s4')
    
    #  test for Position & SUBSTRING
    
    stmt = """SELECT POSITION(UPSHIFT(SUBSTRING(CHAR0_09_UNIQ FROM 6 FOR 4)) IN
CHAR0_09_UNIQ),CHAR0_AZ_UNIQ
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')
    
    stmt = """SELECT POSITION(UPSHIFT(SUBSTRING(CHAR0_09_UNIQ FROM 0 FOR 5)) IN
CHAR0_09_UNIQ),CHAR0_AZ_UNIQ
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s6')
    
    #   agaaaa        ,X*      agaaaaaa
    #   ebaaoa        ,[.      ebaaoaaa
    #   cjaaoa        ,.!      cjaaoaaa
    #   adaaia        ,r'      adaaiaaa
    #   dkaafa        ,1%      dkaafaaa
    
    stmt = """SELECT DISTINCT(SUBSTRING(VARCHAR1_ASCII_UNIQ||CHAR0_AZ_UNIQ FROM 5
FOR 10)) ,VARCHAR1_ASCII_UNIQ||CHAR0_AZ_UNIQ
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s7')
    
    stmt = """SET PARAM ?P1 '0';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT SUBSTRING('Robert John Smith' FROM (POSITION ('Jo' IN
'Hi John'))
FOR POSITION (cast(?P1 as char) IN CHAR0_09_UNIQ)),
POSITION('Jo' IN 'Hi John'),
CHAR0_09_UNIQ,
POSITION(cast(?P1 as char) IN CHAR0_09_UNIQ)
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s8')
    
    #  Test with union
    
    stmt = """SELECT SUBSTRING(VARCHAR1_UNIQ  || CHAR0_09_UNIQ  FROM 5 FOR 6)
FROM b3uns01 
UNION
SELECT CH1 FROM xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 23)
    
    #  test for union SUBSTRING should SELECT only from col 2
    
    stmt = """SELECT SUBSTRING(VARCHAR1_UNIQ  || CHAR0_09_UNIQ  FROM 10 FOR 5)
FROM b3uns01 
UNION
SELECT CH1 FROM xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 18)
    
    stmt = """SELECT SUBSTRING(CHAR1_AZ_2 || CHAR1_COLCHSET_4 FROM 5 FOR 10)
FROM b3uns05 
WHERE SBIN0_UNIQ < 5
UNION
SELECT SUBSTRING(CHAR0_09_UNIQ || CHAR0_AZ_UNIQ  FROM 5 FOR 10)
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s11')
    
    stmt = """SELECT MAX(SUBSTRING(CHAR1_AZ_2 || CHAR1_COLCHSET_4
FROM 1 FOR  10))
FROM b3uns05 
WHERE SBIN0_UNIQ < 5
UNION ALL
SELECT MAX(CHAR0_09_UNIQ || CHAR0_AZ_UNIQ  )
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s12')
    
    stmt = """SELECT SUBSTRING(VARCHAR1_UNIQ || CHAR0_09_UNIQ FROM 5)
FROM b3uns01 
WHERE substring(varchar0_azaz_20 from 2 for 1) = 'A' and
UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s13')
    
    stmt = """SELECT SUBSTRING(VARCHAR1_UNIQ || CHAR0_09_UNIQ FROM 5)
FROM b3uns01 
WHERE UDEC1_UNIQ < 5 AND
(SUBSTRING(VARCHAR1_UNIQ FROM 3 FOR 3) IN ('AAQ', 'AAP'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s14')
    
    stmt = """SELECT SUBSTRING(VARCHAR1_UNIQ || CHAR0_09_UNIQ FROM 5)
FROM b3uns01 
WHERE UDEC1_UNIQ < 5 AND
(EXISTS
(SELECT SUBSTRING(VARCHAR1_UNIQ FROM 3 FOR 3)
FROM b3uns01 
WHERE (SUBSTRING(VARCHAR1_UNIQ FROM 3 FOR 3) IN ('AAQ', 'AAP'))));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s15')
    
    stmt = """SELECT CHAR0_09_UNIQ,
SUBSTRING('Robert John Smith' FROM 8 FOR 20)
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s16')
    
    stmt = """SELECT CHAR0_09_UNIQ,
SUBSTRING('Robert John Smith' FROM 30 FOR 2)
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s17')
    
    # ---------------------------------
    # Cleanup section
    # ---------------------------------
    
    stmt = """drop table xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test003(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA03
    #  Description:        This test verifies the SQL single
    #                      table SELECT queries. Tests with
    #                      position, aggregates.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # Create LOG file
    
    stmt = """SELECT MAX(POSITION('AAA' IN VARCHAR1_UNIQ))
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s0')
    
    stmt = """SELECT DISTINCT(POSITION('AAA' IN VARCHAR1_UNIQ))
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    
    stmt = """SELECT DISTINCT(POSITION(SUBSTRING(VARCHAR1_UNIQ FROM 2 FOR 3) IN
varchar1_uniq))
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    
    #  test for position with occurance & SUBSTRING
    #  data type char
    stmt = """SELECT CHAR0_09_UNIQ,POSITION(SUBSTRING(CHAR0_09_UNIQ FROM 5 FOR 2)
--                      IN CHAR0_09_UNIQ,4),CHAR0_AZ_UNIQ
IN CHAR0_09_UNIQ),CHAR0_AZ_UNIQ
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s3')
    
    #  test for occurance  ,data type varchar
    stmt = """SELECT CHAR0_AZ_UNIQ,POSITION(SUBSTRING(VARCHAR1_UNIQ FROM 3 FOR 2)
--                     IN VARCHAR1_UNIQ,2),VARCHAR1_UNIQ
IN VARCHAR1_UNIQ),VARCHAR1_UNIQ
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s4')
    
    #  test for position with occurance
    #  use of occurance was not effective,tpr filed
    #  data type varchar,occurance beyond the length of string
    stmt = """SELECT CHAR0_AZ_UNIQ,POSITION(SUBSTRING(VARCHAR1_UNIQ FROM 3 FOR 2)
--                     IN VARCHAR1_UNIQ,7),VARCHAR1_UNIQ
IN VARCHAR1_UNIQ),VARCHAR1_UNIQ
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s5')
    
    stmt = """SELECT CHAR0_AZ_UNIQ,POSITION(SUBSTRING(VARCHAR1_UNIQ FROM 3 FOR 2)
in varchar1_uniq),varchar1_uniq
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s6')
    
    #  empty string retrieved from SUBSTRING function
    
    stmt = """SELECT CHAR0_AZ_UNIQ,POSITION(SUBSTRING(VARCHAR1_UNIQ FROM 3 FOR 0)
IN VARCHAR1_UNIQ),VARCHAR1_UNIQ
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s7')
    
    #  test with literals
    
    stmt = """SELECT CHAR0_AZ_UNIQ,POSITION(SUBSTRING(VARCHAR1_UNIQ FROM 3 FOR 5)
IN 'AAAA' ),VARCHAR1_UNIQ
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s8')
    
    # test with params
    
    stmt = """SET PARAM ?P1 '!@#$%^&*0)';"""
    output = _dci.cmdexec(stmt)
    stmt = """SET PARAM ?P2 'ABC!@123!%^&!@#$%^&*0)@#$%&^%XYZ';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT CHAR0_AZ_UNIQ,POSITION(UPSHIFT(?P1) IN ?P2 )
,VARCHAR1_UNIQ
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s9')
    
    # test with occurance also as param
    stmt = """SET PARAM ?P1 'a!b@c';"""
    output = _dci.cmdexec(stmt)
    stmt = """SET PARAM ?P2 'a!b@cA!B@C*7';"""
    output = _dci.cmdexec(stmt)
    stmt = """SET PARAM ?P3 1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT CHAR0_AZ_UNIQ,POSITION(UPSHIFT(?P1) IN ?P2)
,VARCHAR1_UNIQ
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s10')
    
    # test with occurance as an expression
    stmt = """SET PARAM ?P1 'ab';"""
    output = _dci.cmdexec(stmt)
    stmt = """SET PARAM ?P2 'cabababababababc';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT CHAR0_AZ_UNIQ,POSITION(UPSHIFT(?P1) IN ?P2)
, POSITION (?P1 IN ?P2)
,VARCHAR1_UNIQ
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s11')
    
    stmt = """SELECT POSITION('   ' IN VARCHAR1_UNIQ)
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s12')
    
    stmt = """SELECT POSITION('Singing in the rain' IN '')
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s13')
    
    # Substring-expression not found in the source-expression
    stmt = """SELECT *
FROM b3uns01 
WHERE POSITION('April' IN CHAR0_09_UNIQ) > 0 and
UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    #  Substring-expression length is greater than the source-expression
    stmt = """SELECT POSITION('April spring time' IN 'April rain')
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s14')
    
    stmt = """SELECT POSITION('' IN 'April rain')
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s15')
    
    _testmgr.testcase_end(desc)

def test004(desc="""a04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA04
    #  Description:        This test verifies the SQL single
    #                      table SELECT queries. Tests with literals
    #                      params, char_length, octet_length, lower,
    #			upper, upshift, concatenation operator.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # Create LOG file
    
    stmt = """CREATE TABLE x 
(x1 char(4)
,x2 char(2)  not null) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO x 
VALUES( 'abc','ab');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO x 
VALUES( null,'yz');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO x 
VALUES( NULL,'00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO x 
VALUES( '1234','12');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """CREATE TABLE xlong 
( ch1 char(4000)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO xlong 
( SELECT SUBSTRING(x1 from 1 for 3) from x);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 4)
    
    #  create table query for testing lower, upper, upshift functions.
    stmt = """drop table t;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table t (t1 char(4),
t2 char(2)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO t 
VALUES( 'abcd','ab');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO t 
VALUES( null,'yz');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO t 
VALUES( NULL,'00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO t 
VALUES( '1234','12');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """SELECT octet_length ('Robert' || ' ' || 'Smith')
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s1')
    
    # testing the octet length of a null value.
    stmt = """SELECT octet_length(ch1)
FROM xlong 
WHERE ch1 is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s2')
    
    #  testing data type varchar, it should
    #  return the actural length of the string stored in.
    stmt = """SELECT octet_length(VARCHAR0_AZAZ_20)
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s3')
    
    stmt = """SET PARAM ?P1 '0';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT char_length (?P1),?P1
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s4')
    
    stmt = """SELECT character_length(ch1),octet_length(ch1)
from xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s5')
    
    # testing octet_length with multi ||
    
    stmt = """SET PARAM ?P 'HELLO';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT octet_length
(CHAR0_09_UNIQ || CHAR0_09_UNIQ || CHAR0_09_UNIQ ||
VARCHAR0_MONEY_100 || CHAR0_AZ_UNIQ || CHAR0_09_UNIQ ||
VARCHAR0_AZAZ_20 || VARCHAR0_AZAZ_20 || CHAR0_AZ_UNIQ ||
CHAR0_AAZY_UNIQ || VARCHAR1_AAZZB_500 || CHAR0_AAZY_UNIQ ||
CHAR1_AAZZ09BP_UNIQ || VARCHAR1_ASCII_UNIQ ||
VARCHAR1_ASCII_UNIQ || VARCHAR1_ASCII_UNIQ ||
VARCHAR1_UNIQ || CHAR1_AAZZ09BP_UNIQ || VARCHAR1_UNIQ ||
VARCHAR0_AZAZ_20 || CHAR1_AAZZ09BP_UNIQ || VARCHAR1_UNIQ ||
UPPER('Robert John') || ?P || '  ' || LOWER(?P) ||
UPSHIFT('good luck') || UPSHIFT('the end') ||
CHAR0_AZ_UNIQ || VARCHAR1_AAZZB_500 || VARCHAR1_AAZZB_500 ||
VARCHAR1_ASCII_UNIQ || CHAR0_09_UNIQ || CHAR0_AAZY_UNIQ ||
VARCHAR0_MONEY_100 || VARCHAR0_MONEY_100 || VARCHAR1_UNIQ ||
VARCHAR1_UNIQ || VARCHAR1_ASCII_UNIQ || CHAR1_AAZZ09BP_UNIQ  ||
VARCHAR1_AAZZB_500 || CHAR0_AAZY_UNIQ || VARCHAR0_AZAZ_20 ||
CHAR0_AZ_UNIQ || VARCHAR0_MONEY_100 || CHAR0_09_UNIQ ||
CHAR0_09_UNIQ || VARCHAR0_MONEY_100 || CHAR0_AZ_UNIQ ||
VARCHAR0_AZAZ_20 || CHAR0_AAZY_UNIQ || VARCHAR1_AAZZB_500 ||
CHAR1_AAZZ09BP_UNIQ || VARCHAR1_UNIQ || VARCHAR1_UNIQ ||
CHAR1_AAZZ09BP_UNIQ || CHAR1_AAZZ09BP_UNIQ)
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s6')
    
    stmt = """SELECT char_length
(CHAR0_09_UNIQ || CHAR0_09_UNIQ || CHAR0_09_UNIQ ||
VARCHAR0_MONEY_100 || CHAR0_AZ_UNIQ || CHAR0_09_UNIQ ||
VARCHAR0_AZAZ_20 || VARCHAR0_AZAZ_20 || CHAR0_AZ_UNIQ ||
CHAR0_AAZY_UNIQ || VARCHAR1_AAZZB_500 || CHAR0_AAZY_UNIQ ||
CHAR1_AAZZ09BP_UNIQ || VARCHAR1_ASCII_UNIQ ||
VARCHAR1_ASCII_UNIQ || VARCHAR1_ASCII_UNIQ ||
VARCHAR1_UNIQ || CHAR1_AAZZ09BP_UNIQ || VARCHAR1_UNIQ ||
VARCHAR0_AZAZ_20 || CHAR1_AAZZ09BP_UNIQ || VARCHAR1_UNIQ ||
CHAR0_AZ_UNIQ || VARCHAR1_AAZZB_500 || VARCHAR1_AAZZB_500 ||
VARCHAR1_ASCII_UNIQ || CHAR0_09_UNIQ || CHAR0_AAZY_UNIQ ||
VARCHAR0_MONEY_100 || VARCHAR0_MONEY_100 || VARCHAR1_UNIQ ||
VARCHAR1_UNIQ || VARCHAR1_ASCII_UNIQ || CHAR1_AAZZ09BP_UNIQ  ||
VARCHAR1_AAZZB_500 || CHAR0_AAZY_UNIQ || VARCHAR0_AZAZ_20 ||
UPPER('Robert John') || ?P || '  ' || LOWER(?P) ||
UPSHIFT('good luck') || UPSHIFT('the end') ||
CHAR0_AZ_UNIQ || VARCHAR0_MONEY_100 || CHAR0_09_UNIQ ||
CHAR0_09_UNIQ || VARCHAR0_MONEY_100 || CHAR0_AZ_UNIQ ||
VARCHAR0_AZAZ_20 || CHAR0_AAZY_UNIQ || VARCHAR1_AAZZB_500 ||
CHAR1_AAZZ09BP_UNIQ || VARCHAR1_UNIQ || VARCHAR1_UNIQ ||
CHAR1_AAZZ09BP_UNIQ || CHAR1_AAZZ09BP_UNIQ)
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s7')
    
    #  testing LOWER, UPPER, UPSHIFT functions.
    
    stmt = """SELECT LOWER(VARCHAR1_UNIQ), UPPER(CHAR0_AZ_UNIQ),
UPSHIFT(CHAR0_AZ_UNIQ)
FROM b3uns01 
WHERE UDEC1_UNIQ IN (1287, 66, 1467);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s8')
    
    # With the LOWER, UPPER, UPSHIFT functions,
    # group by only can use its column position
    # number.
    stmt = """SELECT UDEC1_UNIQ, LOWER(VARCHAR1_UNIQ), UPPER(CHAR0_AZ_UNIQ),
UPSHIFT(CHAR0_AZ_UNIQ)
FROM b3uns01 
GROUP BY UDEC1_UNIQ, VARCHAR1_UNIQ, CHAR0_AZ_UNIQ
HAVING UDEC1_UNIQ IN (1287, 66, 1467)
ORDER BY UDEC1_UNIQ, 2, 3, 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s9')
    
    stmt = """SELECT VARCHAR0_AZAZ_20, UPSHIFT(CHAR0_AZ_UNIQ)
FROM b3uns01 
WHERE (LOWER(VARCHAR0_AZAZ_20) = 'bdaaaaaa' OR
UPPER(CHAR0_AZ_UNIQ) = 'AGAAAAAA')  AND
UDEC1_UNIQ < 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s10')
    
    stmt = """SELECT VARCHAR0_AZAZ_20, UPSHIFT(CHAR0_AZ_UNIQ)
FROM b3uns01 
WHERE (LOWER(VARCHAR0_AZAZ_20) = 'bdaaaaaa' OR
UPSHIFT(CHAR0_AZ_UNIQ) = 'AGAAAAAA') AND
UDEC1_UNIQ < 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s11')
    
    stmt = """SELECT VARCHAR1_UNIQ, UPSHIFT(CHAR0_AZ_UNIQ)
FROM b3uns01 
WHERE (UPPER(CHAR0_AZ_UNIQ) LIKE 'A%AAAAAA' OR
LOWER(VARCHAR1_UNIQ) = 'efaapaaa')  AND
UDEC1_UNIQ < 200;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s12')
    
    stmt = """SELECT VARCHAR0_AZAZ_20, UPSHIFT(CHAR0_AZ_UNIQ)
FROM b3uns01 
WHERE (LOWER(VARCHAR0_AZAZ_20) LIKE 'bdaaaaaa' OR
UPSHIFT(CHAR0_AZ_UNIQ) LIKE 'AGAAAAAA') AND
UDEC1_UNIQ < 200;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s13')
    
    stmt = """SELECT UDEC1_UNIQ, VARCHAR0_AZAZ_20, CHAR0_AZ_UNIQ
FROM b3uns01 
GROUP BY UDEC1_UNIQ, VARCHAR0_AZAZ_20, CHAR0_AZ_UNIQ
HAVING (LOWER(VARCHAR0_AZAZ_20) > 'bdaaaaaa' OR
UPPER(CHAR0_AZ_UNIQ) > 'AGAAAAAA')   AND
UDEC1_UNIQ < 10
ORDER BY UDEC1_UNIQ, VARCHAR0_AZAZ_20, CHAR0_AZ_UNIQ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s14')
    
    stmt = """SELECT UDEC1_UNIQ, VARCHAR0_AZAZ_20, CHAR0_AZ_UNIQ
FROM b3uns01 
GROUP BY UDEC1_UNIQ, VARCHAR0_AZAZ_20, CHAR0_AZ_UNIQ
HAVING (LOWER(VARCHAR0_AZAZ_20) > 'bdaaaaaa' OR
UPSHIFT(CHAR0_AZ_UNIQ) > 'AGAAAAAA') AND
UDEC1_UNIQ < 10
ORDER BY UDEC1_UNIQ, VARCHAR0_AZAZ_20, CHAR0_AZ_UNIQ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s15')
    
    stmt = """INSERT INTO x VALUES (UPPER('azaz'), LOWER('ZZ'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO x VALUES (UPSHIFT('txtx'), UPPER('mi'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO x VALUES (UPSHIFT('lblb'), LOWER('up'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """UPDATE x SET x1 = LOWER('UPER')
WHERE x1 = 'AZAZ';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """UPDATE x SET x1 = UPPER('lowr')
WHERE x1 = 'TXTX';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """UPDATE x SET x1 = UPSHIFT('usft')
WHERE x2 = 'up';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """SELECT *
FROM t tt LEFT JOIN x t2
ON UPPER(tt.t1) = UPSHIFT(t2.x1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s16')
    
    stmt = """SELECT *
FROM t tt LEFT JOIN x t2
ON LOWER(tt.t1) = LOWER(t2.x1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s17')
    
    # testing inner joins with LOWER, UPPER, UPSHIFT
    stmt = """SELECT *
FROM t tt INNER JOIN x t2
ON UPPER(tt.t1) = UPSHIFT(t2.x1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s18')
    
    stmt = """SELECT *
FROM t tt INNER JOIN x t2
ON LOWER(tt.t1) = LOWER(t2.x1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s19')
    
    stmt = """SELECT UPPER('ab') || UPPER('cd') ||
LOWER('upper') || UPSHIFT('CHAR0_AZ_UNIQ') ||
CHAR0_09_UNIQ || VARCHAR1_UNIQ || LOWER(VARCHAR1_ASCII_UNIQ) ||
UPPER('ab') || UPPER('cd') ||
LOWER('upper') || UPSHIFT('CHAR0_AZ_UNIQ') ||
CHAR0_09_UNIQ || VARCHAR1_UNIQ || LOWER(VARCHAR1_ASCII_UNIQ) ||
UPPER('ab') || UPPER('cd') ||
LOWER('upper') || UPSHIFT('CHAR0_AZ_UNIQ') ||
CHAR0_09_UNIQ || VARCHAR1_UNIQ || LOWER(VARCHAR1_ASCII_UNIQ) ||
UPPER('ab') || UPPER('cd') ||
LOWER('upper') || UPSHIFT('CHAR0_AZ_UNIQ') ||
CHAR0_09_UNIQ || VARCHAR1_UNIQ || LOWER(VARCHAR1_ASCII_UNIQ)
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s20')
    
    # ---------------------------------
    # Cleanup section
    # ---------------------------------
    
    stmt = """drop table xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table t;"""
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
    #  Test case name:     testA05
    #  Description:        This test verifies the SQL single
    #                      table SELECT queries. Tests with TRIM
    #                      function.
    #  Test Objectives:    To test the usage of '||' both
    #                      syntactically and for correctness of the
    #                      resultant data.  Also to check on the
    #                      appropriate error message for wrong usage.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # Create LOG file
    
    stmt = """CREATE TABLE x 
(x1 char(4)
,x2 char(2)  not null
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO x 
VALUES( 'abc','ab');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO x 
VALUES( null,'yz');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO x 
VALUES( NULL,'00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO x 
VALUES( '1234','12');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """CREATE TABLE xlong 
( ch1 char(4000)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO xlong 
( SELECT SUBSTRING(x1 from 1 for 3) from x);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 4)
    
    stmt = """SELECT char_length(trim(both ' ' from     ch1))
from xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    
    stmt = """SET PARAM ?P1 '0';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT char_length(trim(both ' ' from   ?P1 || ' ' ||  ch1))
from xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
    
    stmt = """SET PARAM ?P1 '0';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT char_length(trim(both ' ' from   ?P1 || ' ' ||  ch1)) ,
char_length(SUBSTRING(ch1 from (position('1' in ch1)) for 3))
from xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    
    stmt = """SELECT trim(varchar1_uniq) || ' ' || trim(char0_09_uniq)
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
    
    # Test for Nulls
    stmt = """SET PARAM ?P1 '0';"""
    output = _dci.cmdexec(stmt)
    stmt = """SET PARAM ?Ps 4;"""
    output = _dci.cmdexec(stmt)
    stmt = """SET PARAM ?Pl 5;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT trim(?P1 from char0_09_uniq),
SUBSTRING(char0_09_uniq from cast(?Ps as int)
for cast(?Pl as int))
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s4')
    
    stmt = """SELECT SUBSTRING(trim(leading '0' from char0_09_uniq) from 1 for
char_length(trim(leading '0' from char0_09_uniq)))
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s5')
    
    stmt = """prepare s7 from
SELECT SUBSTRING(trim(leading '0' from char0_09_uniq) from 1 for
char_length(trim(leading '0' from char0_09_uniq)))
FROM b3uns01 
where char_length(trim(leading '0' from char0_09_uniq)) > 3
and udec1_uniq < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #  Explain for the query is wrong for the above ----
    stmt = """select seq_num, operator, total_cost
from table (explain (null, 'S7'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s7')
    
    stmt = """SELECT min  (SUBSTRING(trim(leading '0' from char0_09_uniq) from
position('0' in char0_09_uniq) for
char_length(trim(leading '0' from char0_09_uniq))))
FROM b3uns01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s8')
    
    stmt = """SELECT max(trim(leading '0' from char0_09_uniq)) from
 b3uns01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s9')
    
    stmt = """SELECT min(trim(leading '0' from char0_09_uniq)) from
 b3uns01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s10')
    
    # ---------------------------------
    # Cleanup section
    #----------------------------------
    
    stmt = """drop table xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test006(desc="""a08"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA08
    #  Description:        This test verifies the SQL single
    #                      table SELECT queries. Tests for string
    #			functions with BETWEEN clause in
    #			predicate.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # Create LOG file
    
    stmt = """SELECT char0_09_uniq||char0_az_uniq
FROM b3uns01 
where char0_09_uniq not between '00000008' and '0000'||'1465';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s0')
    
    stmt = """SELECT char0_09_uniq||char0_az_uniq
FROM b3uns01 
where char0_09_uniq not between '0000' || '0008' and '0000'||'1465';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s1')
    
    stmt = """SELECT
char0_09_uniq,varchar1_uniq,char0_09_uniq||char0_az_uniq
FROM b3uns01 
where char0_09_uniq not between
SUBSTRING(char0_09_uniq from 1 for 4) ||
SUBSTRING(char0_09_uniq from 5 for 4)
and '00001400';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s2')
    
    stmt = """SELECT
char0_09_uniq,varchar1_uniq,char0_09_uniq||char0_az_uniq
FROM b3uns01 
WHERE UDEC1_UNIQ   between
position(SUBSTRING(char0_09_uniq from 1 for 4) in char0_09_uniq)
and position(SUBSTRING(char0_09_uniq from 5 for 4) in char0_09_uniq)
and udec1_uniq < 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s3')
    
    stmt = """SELECT
udec1_uniq,char0_09_uniq,varchar1_uniq || char0_09_uniq||char0_az_uniq
FROM b3uns01 
WHERE UDEC1_UNIQ between
position(SUBSTRING(char0_09_uniq from 1 for 4) in char0_09_uniq)
and  25
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s4')
    
    stmt = """SET PARAM ?P1 26;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT
udec1_uniq,char0_09_uniq,varchar1_uniq,char0_09_uniq||char0_az_uniq
FROM b3uns01 
WHERE UDEC1_UNIQ  between
position(SUBSTRING(char0_09_uniq from 1 for 4) in char0_09_uniq)
and  ?P1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s5')
    
    # 10 rows
    
    stmt = """SET PARAM ?P1 '0000';"""
    output = _dci.cmdexec(stmt)
    stmt = """SET PARAM ?P2 '146%';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT
udec1_uniq,(char0_09_uniq),varchar1_uniq,char0_09_uniq||char0_az_uniq
FROM b3uns01 
where char0_09_uniq   like ?P1 || ?P2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s6')
    
    stmt = """SELECT
udec1_uniq,char0_09_uniq,varchar1_uniq,char0_09_uniq||char0_az_uniq
FROM b3uns01 
where char0_09_uniq   like '0000' || '%'
and udec1_uniq < 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s7')
    
    _testmgr.testcase_end(desc)

def test007(desc="""a09"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA09
    #  Description:        This test verifies the SQL single
    #                      table SELECT queries. Tests with string
    #			functions in predicates (no collations)
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # Create LOG file
    
    stmt = """drop table emp;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE emp 
(
LAST_NAME                      CHAR(10) DEFAULT NULL
, FIRST_NAME                     CHAR(10) DEFAULT NULL
, DEPT_NUM                       NUMERIC( 4, 0) DEFAULT NULL
, SALARY                         NUMERIC( 8, 2) DEFAULT NULL
, MARITAL_STATUS                 NUMERIC( 1, 0) DEFAULT NULL
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO emp 
values
( 'CLARK' , 'DINAH',9000, 37000.00, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO emp 
values ( 'CRINAR', 'JESSICA', 3500, 39500.00, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO emp 
values ('GREEN','ROGER',  9000, 175500.00, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO emp 
values ('HOWARD', 'JERRY', 1000, 65000.00, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """SELECT udec1_uniq,char0_09_uniq || varchar0_money_100,
position(SUBSTRING(varchar1_uniq from 1 for 2) in
(char0_09_uniq||char0_az_uniq||varchar1_uniq)),
position(SUBSTRING(varchar1_uniq from 6 for 3) in
(char0_09_uniq||char0_az_uniq||varchar1_uniq))
FROM b3uns01 
WHERE UDEC1_UNIQ between
(position(SUBSTRING(varchar1_uniq from 1 for 2) in
(char0_09_uniq || varchar0_money_100 || varchar1_uniq)))
and position (SUBSTRING(varchar1_uniq from 6 for 3) in
(char0_09_uniq || varchar0_money_100 || varchar1_uniq))
and udec1_uniq < 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """SELECT udec1_uniq,char0_09_uniq || varchar0_money_100,
position(SUBSTRING(varchar1_uniq from 1 for 2) in
(char0_09_uniq||char0_az_uniq||varchar1_uniq)),
position(SUBSTRING(varchar1_uniq from 6 for 3) in
(char0_09_uniq||char0_az_uniq||varchar1_uniq))
,char_length(varchar1_aazzb_500)
FROM b3uns01 
WHERE UDEC1_UNIQ between
(position(SUBSTRING(varchar1_uniq from 1 for 2) in
(char0_09_uniq || varchar0_money_100 || varchar1_uniq)) )
and position (SUBSTRING(varchar1_uniq from 6 for 3) in
(char0_09_uniq || varchar0_money_100 || varchar1_uniq))
and char_length(varchar1_aazzb_500) <= 8
and (char0_09_uniq || trim(trailing 'a' from char0_az_uniq))
like '000%'
and udec1_uniq < 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """SELECT SUBSTRING(trim(leading '0' from char0_09_uniq) from
position('0' in char0_09_uniq) for
char_length(trim(leading '0' from char0_09_uniq))) || char0_09_uniq
FROM b3uns01 
where octet_length(trim( '0' from char0_09_uniq)) > 3
and udec1_uniq < 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s1')
    
    stmt = """SELECT position(SUBSTRING(varchar1_uniq from 6 for 3) in
varchar1_uniq) ,varchar1_uniq
FROM b3uns01 
where position(SUBSTRING(varchar1_uniq from 6 for 3)  in
varchar1_uniq)
=  (SELECT max(position(SUBSTRING(varchar1_uniq from
6 for 3) in varchar1_uniq ))
FROM b3uns01)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s2')
    
    stmt = """SELECT char0_az_uniq
FROM b3uns01 
where trim('b' from char0_az_uniq) = 'caamaaa'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s3')
    
    stmt = """SELECT char0_az_uniq
FROM b3uns01 
where trim(leading 'b' from char0_az_uniq) = 'caamaaa'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s4')
    
    stmt = """SELECT char0_az_uniq
FROM b3uns01 
where trim(trailing 'b' from char0_az_uniq) = 'caamaaa'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """SET PARAM ?P1 'A';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT char6_n100 || char7_500 ,SUBSTRING(char4_n10 from 5 for 5)
,trim (upshift('a') from char2_2 || char4_n10)
--  ,position(upshift(?P1) in char2_2 || char4_n10 ,4),char2_2 ||
,position(upshift(?P1) in char2_2 || char4_n10)
,char2_2 || char4_n10
from b2pwl02 
where sbin4_n1000 < 2 and
SUBSTRING(char2_2 || char4_n10 from 4 for 2) like  upshift('A%')
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s5')
    
    #  Multicolumn predicate
    
    stmt = """SELECT last_name,first_name
from emp 
where not (SUBSTRING(last_name from 1 for 4),
position('J' in first_name)) is null
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s6')
    
    #  Self Join on 2 tables
    #  This query takes too much time to execute
    #  Compiler code not smart enough to identify key predicates,
    #  when string functions used on key columns
    
    stmt = """SELECT max(SUBSTRING(t1.varchar2_10 from 1 for 2 ))
from btpwl08 t1,
 btpwl08 t2
where SUBSTRING(t1.varchar2_10 from 1 for 8)
= SUBSTRING(t2.varchar2_10 from 1 for 8)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s7')
    
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    # ---------------------------------
    # Cleanup section
    # ---------------------------------
    
    stmt = """drop table emp;"""
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
    #  Test case name:     testA10
    #  Description:        This test verifies the SQL single
    #                      table SELECT queries. Tests string
    #			function with LIKE.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    stmt = """SET PARAM ?P1 '0000';"""
    output = _dci.cmdexec(stmt)
    stmt = """SET PARAM ?P2 '%';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT char0_09_uniq||char0_az_uniq
FROM b3uns01 
where char0_09_uniq like ?P1 || ?P2
and char0_09_uniq like ?P1 || ?P2
and char0_09_uniq like ?P1 || ?P2
and char0_09_uniq like ?P1 || ?P2
and char0_09_uniq like ?P1 || ?P2
and char0_09_uniq like ?P1 || ?P2
and char0_09_uniq like ?P1 || ?P2
and char0_09_uniq like ?P1 || ?P2
and char0_09_uniq like ?P1 || ?P2
and char0_09_uniq like ?P1 || ?P2
and char0_09_uniq like ?P1 || ?P2
and char0_09_uniq like ?P1 || ?P2
and char0_09_uniq like ?P1 || ?P2
and char0_09_uniq like ?P1 || ?P2
and char0_09_uniq like ?P1 || ?P2
and char0_09_uniq like ?P1 || ?P2
and char0_09_uniq like ?P1 || ?P2
and char0_09_uniq like ?P1 || ?P2
and char0_09_uniq like ?P1 || ?P2
and char0_09_uniq like ?P1 || ?P2
and udec1_uniq < 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s0')
    
    # Error encountered for the above File system Error
    
    stmt = """SET PARAM ?P1 '00000';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT char0_09_uniq||char0_az_uniq
FROM b3uns01 
where SUBSTRING(char0_09_uniq from 1 for 5) =?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
and SUBSTRING(char0_09_uniq from 1 for 5) = ?P1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s1')
    
    stmt = """SELECT char0_09_uniq||char0_az_uniq
FROM b3uns01 
where char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and char_length ( char0_09_uniq || char0_az_uniq ) > 8
and udec1_uniq < 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s2')
    
    _testmgr.testcase_end(desc)

def test009(desc="""a11"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA11
    #  Description:        This test verifies the SQL single
    #                      table SELECT queries. Tests string
    #			functions with views, indexes, subqueries,
    #			zero length strings.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # Create LOG file
    
    stmt = """drop table emp;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE emp 
(
LAST_NAME                      CHAR(10) DEFAULT NULL
, FIRST_NAME                     CHAR(10) DEFAULT NULL
, DEPT_NUM                       NUMERIC( 4, 0) DEFAULT NULL
, SALARY                         NUMERIC( 8, 2) DEFAULT NULL
, MARITAL_STATUS                 NUMERIC( 1, 0) DEFAULT NULL
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO emp 
values
( 'CLARK' , 'DINAH',9000, 37000.00, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO emp 
values ( 'CRINAR', 'JESSICA', 3500, 39500.00, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO emp 
values ('GREEN','ROGER',  9000, 175500.00, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO emp 
values ('HOWARD', 'JERRY', 1000, 65000.00, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """CREATE TABLE temp 
(
LAST_NAME                      CHAR(10) DEFAULT NULL
, FIRST_NAME                     CHAR(10) DEFAULT NULL
, DEPT_NUM                       NUMERIC( 4, 0) DEFAULT NULL
, SALARY                         NUMERIC( 8, 2) DEFAULT NULL
, MARITAL_STATUS                 NUMERIC( 1, 0) DEFAULT NULL
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #LIKE emp;
    
    stmt = """INSERT into temp 
SELECT * from emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 4)
    
    stmt = """CREATE INDEX  indx1 ON b3uns05 
(char0_aazy_20,char1_aazzb_colcaseins_500)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """UPDATE STATISTICS FOR TABLE b3uns05 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE  INDEX i3uns01 
ON b3uns01(varchar0_money_100 , varchar0_azaz_20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """UPDATE STATISTICS FOR TABLE b3uns01 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update temp 
set last_name =   SUBSTRING(trim(LAST_NAME) ||
trim( FIRST_NAME) FROM 6 FOR 5)
where SUBSTRING(last_name from 2 for 1) = 'R'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    
    stmt = """SELECT * from emp 
where SUBSTRING(last_name from 2 for 3) in
(SELECT SUBSTRING(trim(first_name) || trim(last_name) from 7 for 3)
from temp 
where position('R' in first_name) > 2)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s1')
    
    stmt = """SELECT char0_aazy_20,char1_aazzb_colcaseins_500
,char0_09_coldescan_100
from b3uns05 
where char0_aazy_20 between 'a' and 'z' and
-- and trim('0' from char0_09_coldescan_100 ) between '60' and '55';
trim('0' from char0_09_coldescan_100 ) between '55' and '60';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s2')
    
    stmt = """SELECT char0_n10,date1_n4,SUBSTRING(char0_n10 from 1 for 1)
from b2uns01 
where  '' || char0_n10  = (SELECT SUBSTRING(char0_n10 from 1 for 1)
|| SUBSTRING(char0_n10 from 2 for 1)
from b2uns01 
where sbin0_uniq < 5 and
char0_n10 = 'AA' )
and sbin0_uniq < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s3')
    
    stmt = """SELECT
converttohex(nchar0_az_uniq || nvarchar0_az_1000),
SUBSTRING(char0_aazy_500 from 4),
position(SUBSTRING(char1_coldescan_20 from -3 for 5) in
char1_coldescan_20)
,converttohex(SUBSTRING(char0_iso_colisoasc_100 from 1 for 4) ||
SUBSTRING(char0_iso_colisoasc_100 from 5 for 4))
from b3uns09 
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SET PARAM ?P2 'A' ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SET PARAM ?P1 'H' ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT
SUBSTRING(varchar0_1000 from 1 for 1) || trim(?P2 from char0_10),
position(?P1 in varchar1_uniq),
SUBSTRING(varchar2_uniq from 2 for 4)
from btuns07 
where SUBSTRING(varchar2_uniq from 1 for 4)
= SUBSTRING(varchar2_uniq from  1 for 2)
|| SUBSTRING(varchar2_uniq from 3 for  2)
and sdec0_uniq < 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s5')
    
    stmt = """SELECT char0_azaz_20,SUBSTRING(char0_azaz_20 from 1 for 4)
from b3uns07 
where SUBSTRING(char0_azaz_20 from 1 for 4) = 'adaa'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s6')
    
    stmt = """SELECT char0_09_uniq ,SUBSTRING(char0_az_uniq from  1 for 4)
FROM b3uns01 
where SUBSTRING(char0_az_uniq from 1 for 4) in
(SELECT SUBSTRING(char0_azaz_20 from 1 for 4)
from b3uns07 
)
and udec1_uniq < 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s7')
    
    stmt = """SELECT char0_09_uniq ,SUBSTRING(char0_az_uniq from  1 for 4)||
SUBSTRING(char0_az_uniq from 5 for 4)
FROM b3uns01 
where SUBSTRING(char0_az_uniq from 1 for 4) || 'i' ||
SUBSTRING(char0_az_uniq from 6 for 3) in
(SELECT SUBSTRING(char0_azaz_20 from 1 for 9)
from b3uns07 
)
and udec1_uniq < 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    #  The result would be '00001265' , 'adaaiaaa'
    
    stmt = """SELECT char0_09_uniq ,SUBSTRING(char0_az_uniq from  1 for 4)||
SUBSTRING(char0_az_uniq from 5 for 4)
FROM b3uns01 
where SUBSTRING(char0_az_uniq from 1 for 4) ||
SUBSTRING(char0_az_uniq from 5 for 4) in
(SELECT SUBSTRING(char0_azaz_20 from 1 for 4)|| 'iaaa'
from b3uns07 
)
and udec1_uniq < 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s8')
    
    stmt = """SELECT varchar0_money_100 || varchar0_azaz_20
FROM b3uns01 
where varchar0_money_100 || varchar0_azaz_20 = '$0000.98BEAAAAAA'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s9')
    
    stmt = """SELECT varchar0_money_100 || varchar0_azaz_20
FROM b3uns01 
where SUBSTRING(varchar0_money_100 || varchar0_azaz_20
from 1 for 8)  = '$0000.98'
and trim('A' from varchar0_azaz_20)
= SUBSTRING(varchar0_azaz_20 from 1 for 2)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s10')
    
    #  Test for Zero length string
    stmt = """SELECT char_length(''),
char_length(SUBSTRING('' from 1 for 2)),
position('' in 'AB'),
position('' in ''),
--       position('' in 'ABC',3),
position('' in 'ABC'),
--        position('' in 'AB',6)
position('' in 'AB')
FROM b3uns01 
WHERE UDEC1_UNIQ < 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s11')
    
    # ---------------------------------
    # Cleanup section
    # ---------------------------------
    
    stmt = """drop index indx1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop index i3uns01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table temp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test010(desc="""a12"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA12
    #  Description:        This test verifies the SQL single
    #                      table SELECT queries. Tests string
    #                      functions with views.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # Create LOG file
    
    stmt = """CREATE TABLE emp 
(
LAST_NAME                      CHAR(10) DEFAULT NULL
, FIRST_NAME                     CHAR(10) DEFAULT NULL
, DEPT_NUM                       NUMERIC( 4, 0) DEFAULT NULL
, SALARY                         NUMERIC( 8, 2) DEFAULT NULL
, MARITAL_STATUS                 NUMERIC( 1, 0) DEFAULT NULL
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO emp 
values
( 'CLARK' , 'DINAH',9000, 37000.00, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO emp 
values ( 'CRINAR', 'JESSICA', 3500, 39500.00, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO emp 
values ('GREEN','ROGER',  9000, 175500.00, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO emp 
values ('HOWARD', 'JERRY', 1000, 65000.00, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """CREATE VIEW vemp 
(lname,fname,name,sname,sal)
AS (SELECT last_name,first_name,trim(last_name)||trim(first_name),
SUBSTRING(first_name from 1 for 5),salary
from emp)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SELECT SUBSTRING(trim (' ' from lname)||trim(' ' from fname)
from 3 for 5),
SUBSTRING(fname from 1 for 4),sal
from vemp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s0')
    
    stmt = """prepare s4 from
SELECT octet_length(
(char0_09_uniq ||varchar0_money_100||char0_az_uniq||varchar0_azaz_20
|| char0_aazy_uniq || varchar1_aazzb_500 || char1_aazz09bp_uniq
|| varchar1_ascii_uniq || varchar1_uniq  || char0_09_uniq
|| varchar0_money_100 ||char0_az_uniq|| varchar0_azaz_20
|| char0_aazy_uniq || varchar1_aazzb_500 || char1_aazz09bp_uniq
|| varchar1_ascii_uniq || varchar1_uniq  || char0_09_uniq
|| varchar0_money_100|| char0_az_uniq|| varchar0_azaz_20
|| char0_aazy_uniq || varchar1_aazzb_500 || char1_aazz09bp_uniq
|| varchar1_ascii_uniq || varchar1_uniq  || char0_09_uniq
|| varchar0_money_100 || char0_az_uniq || varchar0_azaz_20
|| char0_09_uniq
|| varchar0_money_100 ||char0_az_uniq ||varchar0_azaz_20
|| char0_aazy_uniq || varchar1_aazzb_500 ||char1_aazz09bp_uniq
|| varchar1_ascii_uniq || varchar1_uniq  || char0_09_uniq
|| varchar0_money_100||char0_az_uniq||varchar0_azaz_20
|| char0_09_uniq
|| varchar0_money_100||char0_az_uniq||varchar0_azaz_20
|| char0_aazy_uniq || varchar1_aazzb_500 ||char1_aazz09bp_uniq
|| varchar1_ascii_uniq || varchar1_uniq  || char0_09_uniq
|| varchar0_money_100||char0_az_uniq||varchar0_azaz_20
|| char0_09_uniq
|| varchar0_money_100||char0_az_uniq||varchar0_azaz_20
|| char0_aazy_uniq || varchar1_aazzb_500 ||char1_aazz09bp_uniq
|| varchar1_ascii_uniq || varchar1_uniq  || char0_09_uniq
|| varchar0_money_100 || char0_az_uniq || varchar0_azaz_20
|| char0_09_uniq
|| varchar0_money_100||char0_az_uniq||varchar0_azaz_20
|| char0_aazy_uniq || varchar1_aazzb_500 ||char1_aazz09bp_uniq
|| varchar1_ascii_uniq || varchar1_uniq  || char0_09_uniq
|| varchar0_money_100||char0_az_uniq||varchar0_azaz_20
|| char0_09_uniq
|| varchar0_money_100 ||char0_az_uniq||varchar0_azaz_20
|| char0_aazy_uniq || varchar1_aazzb_500 ||char1_aazz09bp_uniq
|| varchar1_ascii_uniq || varchar1_uniq  || char0_09_uniq
|| varchar0_money_100||char0_az_uniq||varchar0_azaz_20
|| char0_aazy_uniq || varchar1_aazzb_500 ||char1_aazz09bp_uniq
|| varchar1_ascii_uniq || varchar1_uniq  || char0_09_uniq
|| varchar0_money_100||char0_az_uniq||varchar0_azaz_20
|| char0_aazy_uniq || varchar1_aazzb_500 ||char1_aazz09bp_uniq
|| varchar1_ascii_uniq || varchar1_uniq  || char0_09_uniq
|| varchar0_money_100||char0_az_uniq||varchar0_azaz_20
|| char0_aazy_uniq || varchar1_aazzb_500 ||char1_aazz09bp_uniq
|| varchar1_ascii_uniq || varchar1_uniq  || char0_09_uniq
|| varchar0_money_100||char0_az_uniq||varchar0_azaz_20
|| char0_aazy_uniq || varchar1_aazzb_500 ||char1_aazz09bp_uniq
|| varchar1_ascii_uniq || varchar1_uniq  || char0_09_uniq
|| varchar0_money_100||char0_az_uniq||varchar0_azaz_20
|| ' '
)  )
,char0_09_uniq
from b3uns01 
WHERE UDEC1_UNIQ < 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute s4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s1')
    
    # ---------------------------------
    # Cleanup section
    # ---------------------------------
    
    stmt = """drop view vemp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table emp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test011(desc="""n01"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN01
    #  Description:        This test verifies the SQL single
    #			table SELECT and INSERT queries with
    #			concatenation operator.  This is a
    #			negative test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # Create LOG file
    
    stmt = """drop table x;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE x 
(X1 CHAR(4)
,X2 CHAR(2)  NOT NULL) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO x 
VALUES( 'abc','ab');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO x 
VALUES( null,'yz');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO x 
VALUES( NULL,'00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO x 
VALUES( '1234','12');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  SELECT, Concatenate with no string
    stmt = """SELECT || ||
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  SELECT, Concatenate with an empty string
    stmt = """SELECT VARCHAR1_UNIQ ||
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  SELECT, concatenation of non-string values
    stmt = """SELECT 'concatenation with numbers ' || 12345
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4034')
    
    #  SELECT, concatenation of null value
    stmt = """SELECT VARCHAR1_NUIQ || null
FROM b3uns01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """SELECT 'null' || null || null
FROM b3uns01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    stmt = """SELECT null || varchar1_uniq || null
FROM b3uns01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    #  INSERT, Concatenate with no string
    stmt = """INSERT into x values ( || ||, 'ml');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  INSERT, Concatenate with an empty string
    stmt = """INSERT into x values ('no string' ||, 'jk');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  INSERT, concatenation of non-string values
    stmt = """INSERT into x values ('numb' || 12345, 'ab');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4034')
    
    #  INSERT, concatenation of a string's length longer than
    # 	   the defined data string length.
    stmt = """INSERT into x values ('bad' || ' length', 'xx');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    
    # ---------------------------------
    # Cleanup section
    # ---------------------------------
    
    stmt = """drop table x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test012(desc="""n02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN02
    #  Description:        This test verifies the SQL substring.
    #			This is a negative test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    #  SUBSTRING without character string.
    stmt = """SELECT SUBSTRING(),CHAR0_AZ_UNIQ
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  SUBSTRING without anything.
    stmt = """SELECT SUBSTRING, CHAR0_AZ_UNIQ
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3128')
    
    #  SUBSTRING typed twice.
    stmt = """SELECT CHAR0_09_UNIQ,
SUBSTRING SUBSTRING('Robert John Smith' FROM 0 FOR 5),
CHAR0_AZ_UNIQ
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3128')
    
    #  SUBSTRING string without quotes.
    stmt = """SELECT SUBSTRING(123456789 FROM 8 FOR 15),CHAR0_AZ_UNIQ
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4051')
    
    #  SUBSTRING without FROM clause.
    stmt = """SELECT CHAR0_09_UNIQ,
SUBSTRING('Robert John Smith' 0 FOR 5),
CHAR0_AZ_UNIQ
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  SUBSTRING with negative FOR length
    stmt = """SELECT CHAR0_09_UNIQ,
SUBSTRING('Robert John Smith' FROM 8 FOR -1)
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8403')
    
    #  SUBSTRING with null FOR length
    stmt = """SELECT CHAR0_09_UNIQ,
SUBSTRING('Robert John Smith' FROM 8 FOR )
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  SUBSTRING with non-numeric value FOR length
    stmt = """SELECT CHAR0_09_UNIQ,
SUBSTRING('Robert John Smith' FROM 8 FOR xx)
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    #  SUBSTRING with negative start position
    stmt = """SELECT CHAR0_09_UNIQ,
SUBSTRING('Robert John Smith' FROM -8 FOR 1)
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n02exp""", 'n02s8')
    
    #  SUBSTRING with negative both start position and length
    stmt = """SELECT CHAR0_09_UNIQ,
SUBSTRING('Robert John Smith' FROM -8 FOR -1)
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8403')
    
    #  SUBSTRING with start position omitted
    stmt = """SELECT CHAR0_09_UNIQ,
SUBSTRING('Robert John Smith' FROM  FOR 3)
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  SUBSTRING with start-position a non-numeric value
    stmt = """SELECT CHAR0_09_UNIQ,
SUBSTRING('Robert John Smith' FROM ab FOR 8)
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    #  SUBSTRING with more than one character-expression
    stmt = """SELECT CHAR0_09_UNIQ,
SUBSTRING('Robert John Smith', 'error string' FROM 8 FOR 10)
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    _testmgr.testcase_end(desc)

def test013(desc="""n03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN03
    #  Description:        This test verifies the SQL single
    #                      table SELECT queries. Tests with
    #                      position.  This is a negative test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # Create LOG file
    
    #  POSITION only
    stmt = """SELECT POSITION
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3128')
    
    #  POSITION twice
    stmt = """SELECT POSITION POSITION('AAA' IN VARCHAR1_UNIQ)
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3128')
    
    #  POSITION without IN clause
    stmt = """SELECT POSITION('AAA')
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  POSITION with no substring-expression
    stmt = """SELECT POSITION(IN VARCHAR1_UNIQ))
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  POSITION with no source-expression
    stmt = """SELECT POSITION('AAA' IN )
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  More than one string expression entered
    stmt = """SELECT POSITION(VARCHAR1_UNIQ, VARCHAR1_UNIQ IN
varchar1_uniq)
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """SELECT POSITION(VARCHAR1_UNIQ IN
varchar1_uniq, char0_09_uniq)
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Substring is a numeric value
    stmt = """SELECT POSITION(1234567 IN 'Hello, and Hello')
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4063')
    
    #  Source expression is a numeric value
    stmt = """SELECT POSITION('Hello' IN 98765)
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4063')
    
    #  missing source-expression in the IN clause
    stmt = """SELECT CHAR0_AZ_UNIQ,POSITION(SUBSTRING(VARCHAR1_UNIQ FROM 3 FOR 0)
IN ),VARCHAR1_UNIQ
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  source-expression in the IN clause is a negative number
    stmt = """SELECT POSITION(SUBSTRING(VARCHAR1_UNIQ FROM 3 FOR 0) IN -1)
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4063')
    
    stmt = """SELECT POSITION(('Hello') IN UPSHIFT('Hello, and Hello'),-10 )
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """SELECT POSITION('a' in  '')
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n03exp""", 'n03s12')
    
    stmt = """SELECT POSITION('' in  'abc')
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n03exp""", 'n03s13')
    
    stmt = """SELECT POSITION('a', 'cccc')
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """CREATE TABLE x 
(x1 char(4)
,x2 char(2)  not null) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO x 
VALUES( 'abc','ab');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO x 
VALUES( null,'yz');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO x 
VALUES( NULL,'00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO x 
VALUES( '1234','12');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """SELECT POSITION('z' in x1)
FROM x 
WHERE x1 is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n03exp""", 'n03s15')
    
    _testmgr.testcase_end(desc)

def test014(desc="""n04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN04
    #  Description:        This test verifies the SQL single
    #                      table SELECT queries. Tests with literals
    #                      params, char_length, octet_length, lower,
    #			upper, upshift.  This is a negative test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # Create LOG file
    
    stmt = """drop table x;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE x 
(x1 char(4)
,x2 char(2)  not null) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO x 
VALUES( 'abc','ab');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO x 
VALUES( null,'yz');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO x 
VALUES( NULL,'00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO x 
VALUES( '1234','12');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """CREATE TABLE xlong 
( ch1 char(4000),
chn char(5)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO xlong 
VALUES( 'abc','ab');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO xlong 
VALUES( null,'yz');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO xlong 
VALUES( NULL,'00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO xlong 
VALUES( '1234','12');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select LOWER()
from xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select LOWER LOWER(ch1)
from xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3128')
    
    stmt = """select LOWER(ch1, chn)
from xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select LOWER(121312)
from xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    
    stmt = """select LOWER(udec1_uniq)
from b3uns01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    
    stmt = """select UPPER
from xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3128')
    
    stmt = """select UPPER UPPER(ch1)
from xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3128')
    
    stmt = """select UPPER(ch1, chn)
from xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select UPPER(121312)
from xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    
    stmt = """select UPPER(udec1_uniq)
from b3uns01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    
    stmt = """select UPSHIFT()
from xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select UPSHIFT, UPSHIFT(ch1)
from xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3128')
    
    stmt = """select UPSHIFT(ch1, chn)
from xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select UPSHIFT(121312)
from xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    
    stmt = """select UPSHIFT(udec1_uniq)
from b3uns01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    
    stmt = """SELECT octet_length octet_length ('Robert' || ' ' || 'Smith')
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3128')
    
    stmt = """SELECT char_length char_length ('Robert' || ' ' || 'Smith')
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3128')
    
    stmt = """SELECT octet ("Robert" || ' ' || 'Smith')
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """SELECT char ("Robert" || ' ' || 'Smith')
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """SELECT octet_length ()
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """SELECT char_length ()
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """SELECT octet_length(ch1 ch1)
from xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """SELECT octet_length(121212)
FROM x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    
    stmt = """SELECT octet_length(udec1_uniq)
FROM b3uns01 
WHERE udec1_uniq < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    
    stmt = """SELECT octet_length(non_exist_col)
FROM b3uns01 
WHERE udec1_uniq < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """SELECT char_length(non_exist_col)
FROM b3uns01 
WHERE udec1_uniq < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """SELECT char_length(ch1), octet_length()
from xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """SELECT char_length(), octet_length(ch1)
from xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """SELECT char_length(ch1, ch1)
from xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """SELECT char_length(121314)
from xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    
    stmt = """SELECT char_length(udec1_uniq)
from b3uns01 
where udec1_uniq < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4043')
    
    #  Concatenate strings with upper, lower, upshift functions
    #  and a non-character string.
    stmt = """SELECT UPPER('ab') || UPPER('cd') ||
LOWER('upper') || UPSHIFT('CHAR0_AZ_UNIQ') ||
CHAR0_09_UNIQ || VARCHAR1_UNIQ || LOWER(VARCHAR1_ASCII_UNIQ) ||
UPPER('ab') || UPPER('cd') ||
LOWER('upper') || UPSHIFT('CHAR0_AZ_UNIQ') ||
CHAR0_09_UNIQ || VARCHAR1_UNIQ || LOWER(VARCHAR1_ASCII_UNIQ) ||
UPPER('ab') || 99999999999999 ||
LOWER('12314') || UPSHIFT('CHAR0_AZ_UNIQ') ||
CHAR0_09_UNIQ || VARCHAR1_UNIQ || LOWER(VARCHAR1_ASCII_UNIQ) ||
UPPER('ab') || UPPER('cd') ||
LOWER('upper') || UPSHIFT('CHAR0_AZ_UNIQ') ||
CHAR0_09_UNIQ || VARCHAR1_UNIQ || LOWER(VARCHAR1_ASCII_UNIQ) ||
FROM b3uns01 
WHERE UDEC1_UNIQ < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # ---------------------------------
    # Cleanup section
    # ---------------------------------
    
    stmt = """drop table xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test015(desc="""n05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN05
    #  Description:        This test verifies the SQL single
    #                      table SELECT queries. Tests with TRIM
    #                      function.  This is a negative test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # Create LOG file
    
    stmt = """CREATE TABLE x 
(x1 char(4)
,x2 char(2)  not null
,xn int
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO x 
VALUES( 'abc','ab',123);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO x 
VALUES( null,'yz',234);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO x 
VALUES( NULL,'00',345);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO x 
VALUES( '1234','12',999);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """CREATE TABLE xlong 
( ch1 char(4000)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO xlong 
( SELECT SUBSTRING(x1 from 1 for 3) from x);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 4)
    
    stmt = """SELECT trim()
from xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """SELECT trim trim(from ch1)
from xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3128')
    
    stmt = """SELECT trim(non_exist_col)
from xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """SELECT trim(ch1, ch1)
from xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """SELECT trim(76543)
from xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4133')
    
    stmt = """SELECT trim(xn)
from x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4133')
    
    stmt = """SELECT trim(middle ch1 from   ' ' ||  ch1)
from xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """SELECT trim(995511 ch1 from   ' ' ||  ch1)
from xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """SELECT trim(leading trailing ' ' from ch1)
from xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """SELECT trim(leading ' ' from ch1 ch1)
from xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """SELECT trim (leading ' ' from 4453)
from xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4133')
    
    stmt = """SELECT trim (trailing ' ' from non_exist_col)
from xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """SELECT trim(trailing 'aa' from '  this is aa fun  ')
from xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8404')
    
    # ---------------------------------
    # Cleanup section
    #----------------------------------
    
    stmt = """drop table xlong;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

