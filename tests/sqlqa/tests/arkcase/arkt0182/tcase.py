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
    
def test001(desc="""a06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """drop table floats;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE floats 
(
f_real    REAL,
f_double  DOUBLE PRECISION
) no partition;"""
    output = _dci.cmdexec(stmt)
    
    #  Implicit data conversions (Insert float values into numeric columns)
    
    stmt = """drop table numerics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE numerics 
(
numer2        NUMERIC(2,1) SIGNED,           -- 2 bytes
numer4        NUMERIC(9,2) UNSIGNED,         -- 4 bytes
numer8        NUMERIC(15,6),                 -- 8 bytes
smalli        SMALLINT,
i             INTEGER UNSIGNED,
largei        LARGEINT,
dec4          DECIMAL(4,1) UNSIGNED,
dec12         DECIMAL(12,3) SIGNED,
pic8          PIC S9(6)V9(2)
) no partition;"""
    output = _dci.cmdexec(stmt)
    
    #  Fred Hyden, a developer, noticed there was some funny issues
    #  in how convert small numbers from float to real
    #  There is a range from 0 to 10e-38 that cann't be represented
    #  so what happens which convert from 10-e300 to real
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0182 : A06
    #  Description:        This test verifies SQL FLOAT
    #                      data type and the EXPONENTIATION
    #                      operator.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #  -- TESTCASE SUMMARY
    #  POSITIVE implicit data conversions
    #  and expression coercions.
    #
    #
    #  |                                                     |
    #  |  Test Case Name:  A5                                |
    #  |                                                     |
    #  |  This is a POSITIVE tests.  It causes implicit      |
    #  |  data conversions and expression coercions.         |
    #  |                                                     |
    #
    
    stmt = """INSERT INTO floats 
VALUES (123, 456.78);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO floats 
VALUES (+009, -.01234);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO floats 
VALUES (+123456789012345678, -00123456789.012345678);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """SELECT * FROM floats;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s0')
    
    stmt = """INSERT INTO numerics 
(numer2, numer4, numer8,
smalli, i, largei,
dec4, dec12, pic8)
VALUES (-1.2e0,  1234567e-2,  123456789012345e-10,
-3276.8e+1,  429496.7295e4,  9.2e+18,
1234e-1,  -.123456789012e9,  -1.2345678e5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """SELECT * FROM numerics;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s1')
    
    #  Implicit data coercions (expressions using numerics and floats)
    
    stmt = """SELECT 123 * 1e1,  456 / 1e-1,  -.12345678901234567 * 1.0000000e+9
FROM numerics;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s2')
    
    stmt = """SELECT +000123 + 2.3400000e2,  -99. - .24000000e2,  (1200 + 34)
/ 1.00000000e2
FROM numerics;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s3')
    
    stmt = """SELECT SUM(f_real) / COUNT(*),  AVG(f_real)
FROM floats;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s4')
    
    stmt = """SELECT f_real * smalli,  f_double / numer2
FROM floats, numerics 
WHERE f_real < 1000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s5')
    
    # Fred Hyden, a developer, noticed there was some funny issues
    # in how convert small numbers from float to real
    # There is a range from 0 to 10e-38 that cann't be represented
    # so what happens which convert from 10-e300 to real
    
    stmt = """drop table minmax;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table minmax (
a real NOT NULL, primary key (a)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into minmax values
(-10e10), (-1), (0), (1), (10e10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    stmt = """select a from minmax;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s6')

    stmt = """select * from minmax where a <  10e-77;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s7')

    stmt = """select * from minmax where a >= 10e-77;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s8')
    
    stmt = """drop table minmax;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """DROP TABLE numerics;"""
    output = _dci.cmdexec(stmt)
    stmt = """DROP TABLE floats;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test002(desc="""a07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #  Limits and precision check
    
    stmt = """drop table temptabl;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE temptabl 
(
realval   real             default null,
doubleval double precision default null
) no partition;"""
    output = _dci.cmdexec(stmt)
    
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0182 : A07
    #  Description:        This test verifies SQL FLOAT
    #                      data type and the EXPONENTIATION
    #                      operator.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    stmt = """INSERT INTO temptabl 
VALUES (+3.40282346e+38, +1.7976931348623157e+308);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO temptabl 
VALUES (-3.40282346e+38, -1.7976931348623157e+308);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO temptabl 
VALUES (+3.40282346e+39, +1.7976931348623157e+309);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3166')
    
    stmt = """INSERT INTO temptabl 
VALUES (-3.40282346e+39, -1.7976931348623157e+309);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3166')
    
    # Insert the smallest positive and smallest negative number
    # that can be represented next to zero.
    stmt = """INSERT INTO temptabl 
VALUES (+8.636169e-78, +8.636168555094445e-78);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
 
    stmt = """INSERT INTO temptabl 
VALUES (-8.636169e-78, -8.636168555094445e-78);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    stmt = """INSERT INTO temptabl 
VALUES (+1.7272337E-76, +1.727233337110188889e-77);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    stmt = """INSERT INTO temptabl 
VALUES (-1.7272337E-76, -1.727233337110188889e-77);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')

    stmt = """INSERT INTO temptabl 
VALUES (+1.17549436e-38, +2.2250738585072014e-308);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO temptabl 
VALUES (-1.17549436e-38, +2.2250738585072014e-308);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # Out of range inserts
    # Numbers too small to represent.
    stmt = """INSERT INTO temptabl  (realval)
VALUES (+1.7272337e-78);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    stmt = """INSERT INTO temptabl  (realval)
VALUES (-1.7272337e-78);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    stmt = """INSERT INTO temptabl (realval)
VALUES (+1.7272337e-79);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')

    stmt = """INSERT INTO temptabl (realval)
VALUES (-1.7272337e-79);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    stmt = """INSERT INTO temptabl (doubleval)
VALUES (+2.2250738585072014e-309);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO temptabl (doubleval)
--     VALUES (-1.7272337110188889e-78);
VALUES (-2.2250738585072014e-309);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO temptabl (doubleval)
--     VALUES (+1.7272337110188889e-79);
VALUES (+2.2250738585072014e-310);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO temptabl (doubleval)
--     VALUES (-1.7272337110188889e-79);
VALUES (-2.2250738585072014e-309);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO temptabl  (doubleval)
VALUES (+2.22507385850720e-308);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO temptabl  (doubleval)
VALUES (-2.22507385850720e-308);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
 
    stmt = """INSERT INTO temptabl  (doubleval)
VALUES (+2.2250738585072014e-309);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO temptabl  (doubleval)
VALUES (-2.2250738585072014e-309);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  2/4/99 Now delete the above "zeros"
    
    stmt = """select * from temptabl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """delete from temptabl where realval = 0.0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    stmt = """select * from temptabl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #  Numbers too large to represent.
    stmt = """INSERT INTO temptabl  (realval)
VALUES (+1.157930E+77);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    stmt = """INSERT INTO temptabl  (doubleval)
--     VALUES (+1.15792089237316200E+77);
VALUES (+1.7976931348623157e+309);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3166')
    
    stmt = """INSERT INTO temptabl  (realval)
VALUES (-1.157930E+77);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    stmt = """INSERT INTO temptabl  (doubleval)
--    VALUES (-1.15792089237316200E+77);
VALUES (-1.7976931348623157e+309);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3166')
    
    stmt = """INSERT INTO temptabl  (realval)
VALUES (+1.15740E+78);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    stmt = """INSERT INTO temptabl  (doubleval)
--    VALUES (+1.15792089237310000E+78);
VALUES (+1.7976931348623157e+310);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3166')
    
    stmt = """INSERT INTO temptabl  (realval)
VALUES (-1.15740E+78);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    stmt = """INSERT INTO temptabl  (doubleval)
--     VALUES (-1.15792089237310000E+78);
VALUES (-1.7976931348623157e+310);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3166')
    
    stmt = """INSERT INTO temptabl (doubleval)
VALUES (+1.7976931348623158E+309);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3166')
    
    stmt = """INSERT INTO temptabl (doubleval)
VALUES (-1.7976931348623158e+309);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3166')
    
    stmt = """SELECT * FROM temptabl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s18')
    
    #  Calculations that should remain in range
    
    stmt = """SELECT doubleval * 1.1000000e0
FROM temptabl 
WHERE doubleval < 1
AND doubleval > -1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s19')
    
    stmt = """SELECT realval - 0.02e+77
FROM temptabl 
WHERE realval > 1
AND realval < -1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    #  Calculations that should cause overflow
    
    stmt = """SELECT doubleval * 1.1000000e0
FROM temptabl 
WHERE doubleval < 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    stmt = """SELECT doubleval + 1.0e+308
FROM temptabl 
WHERE doubleval > 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    stmt = """DROP TABLE temptabl;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table efloat (f float default null) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into efloat values (+1.7272337e-76);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into efloat values (-1.7272337e-76);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into efloat values (-1.1579208e+77);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into efloat values (+1.1579208e+77);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from efloat;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """create table ereal (r real default null) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into ereal values (-3.40282346e+38);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into ereal values (+3.40282346e+38);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into ereal values (+1.17549436e-38);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #(+1.7272337e-76);
    
    stmt = """insert into ereal values (-1.17549436e-38);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #(-1.7272337e-76);
    
    stmt = """select * from ereal;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    stmt = """create table edouble (d double precision) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into edouble values (1.1579208890123456e77);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into edouble values (-1.1579208890123456e77);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into edouble values (-1.7272337890123456e76);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into edouble values (+1.7272337890123456e76);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from edouble;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    _testmgr.testcase_end(desc)

def test003(desc="""n01"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """drop table float1;"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE TABLE float1 
(
 float1     FLOAT(1)  NOT NULL,
float22    FLOAT(22),
float23    FLOAT(23) DEFAULT 23e0,
float54    FLOAT(54) DEFAULT 1234567890.123456,
real1      REAL      DEFAULT 22.03,
double1    DOUBLE PRECISION  DEFAULT 2.3450000e56,
double2    FLOAT     DEFAULT 56
) no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table float2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE float2 
(
 float1     FLOAT(1)  NO DEFAULT not null,
float22    FLOAT(22) DEFAULT NULL,
float23    FLOAT(23) DEFAULT 1.23e+10 NOT NULL,
float54    FLOAT(54) NOT NULL,
real1      REAL      NO DEFAULT  NOT NULL,
double1    DOUBLE PRECISION  DEFAULT 2.3450000e56
) no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table float3;"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE TABLE float3 
(
real1      REAL       DEFAULT 1.0 NOT NULL,
char1      CHAR(1)    DEFAULT 'a' NOT NULL,
real2      REAL       DEFAULT 0.2e1 NOT NULL,
varchar7   VARCHAR(7) DEFAULT 'bcdefgh' NOT NULL,
double1    DOUBLE PRECISION  DEFAULT 30.0e-1 NOT NULL,
char5      CHAR(5)    DEFAULT 'ijklm' NOT NULL,
double2    DOUBLE PRECISION  DEFAULT 4 NOT NULL
) no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table badcolum;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE badcolum 
(
badcolumn   FLOAT(54)
) no partition;"""
    output = _dci.cmdexec(stmt)
    
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0182 : N01
    #  Description:        This test verifies SQL FLOAT
    #                      data type and the EXPONENTIATION
    #                      operator.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #  NEGATIVE tests: float overflow,
    #  division by float 0, insert
    #  duplicate values into unique
    #  index and primary key column
    #
    #  |                                                     |
    #  |  Test Case Name:  N1                                |
    #  |                                                     |
    #  |  This is a NEGATIVE test.  It tests for overflow    |
    #  |  involving floats, division by a float 0 value,     |
    #  |  inserting duplicate float values into a unique     |
    #  |  index and primary key column, and for invalid      |
    #  |  arguments to exponentiation.                       |
    #  |                                                     |
    
    stmt = """INSERT INTO float1 
VALUES (1.11, 2.22e22, 3.33e-33, 0.004, 5.55e+22, .6666E66, 777E-7);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO float1 
(float1) VALUES (1.2345e-67);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO float1 
(float1, double1) VALUES (0, 1.11111E+63);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO float2 
VALUES (0.11, 2.22e22, 3.33e-33, 0.004, 5.55e+22, 0.666E66);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = """INSERT INTO float2 
(float1, float23, float54, real1)
VALUES (1e1, 1e-1, 1e-1, 5.55e+22);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO float3 
VALUES (1.2e+3, 'z', 4.5e-6, 'yxwvuts', 7.8e9, 'rqpon', 0.1E-2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO float3 
(real1) VALUES (9.8e7);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO float3 
(double1) VALUES (6.5E-4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  Trigger overflow with expressions.
    stmt = """SELECT double1 * 1e11
FROM float1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s0')
    
    stmt = """SELECT double1 ** real1
FROM float1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    # Division by a float 0.
    
    stmt = """SELECT double1 / float22
FROM float1 
WHERE float22 = 0e0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """SELECT float1 / 0e0
FROM float1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8419')
    
    #  Insert duplicate value into primary key column and unique index.
    stmt = """INSERT INTO float2 
(float1, float23, float54, real1)
VALUES (1e1, 3.4, 4.5, 5.55e+22);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """CREATE UNIQUE INDEX uniqindx 
ON float1 
(float1 ASC);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO float1 (float1) VALUES (0e0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    
    stmt = """SELECT float1, float22 FROM float1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s5')
    
    stmt = """SELECT float1, float22, float1 ** float22
FROM float1 
WHERE float1 = 0e0 AND float22 is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s50')
    
    stmt = """delete from float1 where float1 = 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    stmt = """insert into float1 (float1, float22) values (0, 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """SELECT float1 ** float22
FROM float1 
WHERE float1 = 0e0 AND float22 = 0e0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    stmt = """SELECT float22 ** float1 
FROM float1 
WHERE float1 = 0e0 AND float22 = 0e0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    stmt = """SELECT 0 ** 0 FROM float1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    stmt = """DROP TABLE float1;"""
    output = _dci.cmdexec(stmt)
    stmt = """DROP TABLE float2;"""
    output = _dci.cmdexec(stmt)
    stmt = """DROP TABLE float3;"""
    output = _dci.cmdexec(stmt)
    stmt = """DROP TABLE badcolum;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

