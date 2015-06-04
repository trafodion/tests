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
    
def test001(desc="""Update/Rollback transaction tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =====================  Begin Test Case Header  ===================
    # Test case name	: Arkt1424:  testa01
    # Description		: Update/Rollback transaction tests
    # Test case inputs	:
    # Test case outputs	:
    # Expected Results	: (provided a high-level description)
    #
    # Note:
    
    stmt = """drop view VWTAB1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view VWTAB2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table TABLE1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table TABLE2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE TABLE1(Col_fix1 CHAR(20)             NO DEFAULT NOT NULL,
Col_fix2 DATE                 DEFAULT CURRENT_DATE,
Col_fix3 NUMERIC(10,1) SIGNED NO DEFAULT NOT NULL
) no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE TABLE2(Col_var1 VARCHAR(20)          NO DEFAULT NOT NULL,
Col_var2 VARCHAR(25)          DEFAULT NULL,
Col_var3 VARCHAR(30),
PRIMARY KEY (Col_var1)
);"""
    output = _dci.cmdexec(stmt)
    
    # CREATE VIEWS FOR EACH TABLE
    
    stmt = """CREATE VIEW VWTAB1 AS SELECT * FROM TABLE1;"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE VIEW VWTAB2 AS SELECT * FROM TABLE2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO TABLE1 VALUES('First_Row', date '1975-01-01', 100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO TABLE1 VALUES('Second_Row', date '1986-02-12', 200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO TABLE1 VALUES('Third_Row', date '1997-12-31', 300);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from TABLE1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    
    #
    # 1: UPDATE table1
    #
    
    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """UPDATE TABLE1 
SET    col_fix1 = 'Row1'
WHERE  col_fix3 = 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from TABLE1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from TABLE1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    
    stmt = """select * from VWTAB1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    
    #
    # 2: UPDATE vwtab1
    #
    
    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """UPDATE VWTAB1 
SET    col_fix1 = 'Row2'
WHERE  col_fix3 = 200;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from VWTAB1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from VWTAB1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    
    stmt = """select * from TABLE1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')
    
    #
    # 3: UPDATE table2
    #
    stmt = """INSERT INTO TABLE2 VALUES('MICHALE JORDAN', 'DEION SANDERS', 'football');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO TABLE2 VALUES('GWYNETH PALTROWL', 'MERRY STRIP', 'movie');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO TABLE2 VALUES('ELVIS PRESLEY', NULL, 'music');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from TABLE2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s7')
    
    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """UPDATE TABLE2 
SET    col_var2 = 'SHNIA TWAIN',
col_var3 = 'music stars'
WHERE  col_var3 = 'music';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    #  ROLLBACK;
    
    stmt = """select * from TABLE2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s8')
    
    #
    #  4: UPDATE vwtab2
    #
    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8603')
    
    stmt = """select * from VWTAB2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s10')
    
    stmt = """UPDATE VWTAB2 
SET    col_var2 = NULL
WHERE  col_var3 = 'music';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 0)
    
    stmt = """select * from VWTAB2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s11')
    stmt = """select * from TABLE2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s12')
    
    stmt = """ROLLBACK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from VWTAB2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s13')
    
    stmt = """drop view VWTAB1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view VWTAB2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table TABLE1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table TABLE2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test002(desc="""Update/Rollback transaction tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =====================  Begin Test Case Header  ===================
    # Test case name	: Arkt1424:  testa02
    # Description		: Update/Rollback transaction tests
    # Test case inputs	:
    # Test case outputs	:
    # Expected Results	: (provided a high-level description)
    #
    # Note:
    
    stmt = """drop view VWTAB3a;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view VWTAB3b;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view VWTAB3c;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view VWTAB3d;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table TABLE3a;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table TABLE3b;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table TABLE3c;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table TABLE3d;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE TABLE3a(Col_fix1 DECIMAL(4)          NOT NULL,
Col_var2 VARCHAR(30)         NOT NULL,
Col_fix3 TIME                DEFAULT CURRENT_TIME,
Col_var4 VARCHAR(20)         NOT NULL) no partition;"""
    output = _dci.cmdexec(stmt)
    #                     STORE BY ENTRY ORDER;
    
    stmt = """CREATE TABLE TABLE3b(Col_fix1 NUMERIC(6) UNSIGNED NO DEFAULT NOT NULL,
Col_var2 VARCHAR(20)                            ,
Col_fix3 DECIMAL(5,1)        NO DEFAULT NOT NULL,
PRIMARY KEY (Col_fix1))
STORE BY PRIMARY KEY;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE TABLE3c(Col_var1 VARCHAR(15)         DEFAULT NULL,
Col_fix2 INT                 DEFAULT NULL,
Col_var3 VARCHAR(20)         DEFAULT NULL,
Col_fix4 CHAR(20)            DEFAULT NULL
) no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE TABLE3d(Col_var1 VARCHAR(25)         NO DEFAULT NOT NULL,
Col_fix2 INT                 NO DEFAULT NOT NULL,
Col_var3 VARCHAR(30)         NO DEFAULT NOT NULL)
no partition;"""
    output = _dci.cmdexec(stmt)
    
    # CREATE VIEWS FOR EACH TABLE --
    
    stmt = """CREATE VIEW VWTAB3a AS SELECT * FROM TABLE3a;"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE VIEW VWTAB3b AS SELECT * FROM TABLE3b;"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE VIEW VWTAB3c AS SELECT * FROM TABLE3c;"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE VIEW VWTAB3d AS SELECT * FROM TABLE3d;"""
    output = _dci.cmdexec(stmt)
    
    # CREATE INDICIES --
    
    stmt = """CREATE INDEX i3avar2 on TABLE3a(Col_var2);"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE INDEX i3bfix1 on TABLE3b(Col_fix1);"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE INDEX i3cvar3 on TABLE3c(Col_var3);"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE INDEX i3cvar1 on TABLE3d(Col_var1);"""
    output = _dci.cmdexec(stmt)
    
    # INSERT VALUES INTO THE TABLES --
    
    stmt = """INSERT INTO TABLE3a VALUES(11,'MERRY LYNCH',time '12:23:59.999','HEY PAULA'),
(22,'VANGUARD',time '23:23:59.999','THE BODY GUARD'),
(33, 'DATEK',time '23:12:59.999','UNCHANGED MELODY');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO TABLE3b VALUES(12345, 'Pretty Woman', 1111.1),
(23456, NULL, 2222.2),
(34567, 'Song of Music', 3333.3);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO TABLE3c VALUES('Karen',100,'College Station','What a big nice day'),
('Shannon', 200, 'Houston', NULL),
('Cindy', 300, 'Santa Clara', 'What should be done');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO TABLE3d VALUES('Stevens Creek', 1, 'Cupertino'),
('Shoreline Park', 2, 'Mountain View'),
('Ricon Avenue', 3, 'Campbell');"""
    output = _dci.cmdexec(stmt)
    
    # ---------------------
    #  1: UPDATE table3a --
    # ---------------------
    stmt = """select * from TABLE3a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    
    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """UPDATE TABLE3a 
SET col_var2 = 'E-TRADE'
WHERE  col_fix1 = 11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from TABLE3a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from TABLE3a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    
    # ---------------------
    #  2: UPDATE vwtab3a --
    # ---------------------
    stmt = """select * from VWTAB3a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s4')
    
    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """UPDATE VWTAB3a 
SET    col_var2 = 'Broker'
WHERE  col_fix1 = 22;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from VWTAB3a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s6')
    
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from VWTAB3a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s7')
    
    # ---------------------
    #  3: UPDATE table3b &
    #     UPDATE vwtab3b
    # ---------------------
    stmt = """select * from TABLE3b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s8')
    
    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """UPDATE TABLE3b 
SET    col_var2 = 'My Fair Lady',
col_fix3 = 1000
WHERE  col_fix1 = 23456;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from TABLE3b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s9')
    
    stmt = """UPDATE VWTAB3b 
SET    col_var2 = NULL
WHERE  col_fix1 = 23456;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from VWTAB3b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s10')
    
    stmt = """ROLLBACK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from VWTAB3b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s11')
    
    # ---------------------
    #  4: UPDATE table3c &
    #     alter i3cvar3
    # ---------------------
    stmt = """select * from TABLE3c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s12')
    
    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """UPDATE TABLE3c 
SET    col_var1 = NULL,
col_var3 = NULL
WHERE  col_fix2 = 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from TABLE3c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s13')
    
    stmt = """INSERT INTO VWTAB3c(col_fix4) VALUES('This is a test');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from VWTAB3c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s14')
    
    stmt = """ALTER INDEX i3cvar3 ATTRIBUTES AUDITCOMPRESS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ROLLBACK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from VWTAB3c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s15')
    
    # ---------------------
    #  5: UPDATE table3d --
    # ---------------------
    stmt = """select * from TABLE3d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s16')
    
    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """UPDATE TABLE3d 
SET    col_var1 = 'CHANGED VALUE'
WHERE  col_fix2 IN (1, 2, 3)
READ COMMITTED ACCESS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    
    stmt = """select * from VWTAB3d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s17')
    
    stmt = """ROLLBACK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from TABLE3d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s18')
    
    stmt = """drop view VWTAB3a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view VWTAB3b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view VWTAB3c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view VWTAB3d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table TABLE3a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table TABLE3b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table TABLE3c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table TABLE3d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test003(desc="""Update/Rollback transaction tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =====================  Begin Test Case Header  ===================
    # Test case name	: Arkt1424:  testa03
    # Description		: Update/Rollback transaction tests
    # Test case inputs	:
    # Test case outputs	:
    # Expected Results	: (provided a high-level description)
    #
    # Note:
    
    stmt = """drop view VWTAB4a;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view VWTAB4b;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table TABLE4a;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table TABLE4b;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE TABLE4a(Col_fix1 INT,
Col_fix2 DECIMAL(5),
Col_fix3 NUMERIC(6) UNSIGNED,
Col_var4 VARCHAR(20)) no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE TABLE4b(Col_Var1 VARCHAR(30)             NOT NULL,
Col_Var2 VARCHAR(25)             NOT NULL,
Col_Var3 VARCHAR(20),
Col_fix4 INT,
PRIMARY KEY (Col_var1, Col_var2))
STORE BY PRIMARY KEY;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWTAB4a AS SELECT * FROM TABLE4a;"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE VIEW VWTAB4b AS SELECT * FROM TABLE4b;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE INDEX i4avar4 on TABLE4a(Col_var4);"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE INDEX i4bvar2 on TABLE4b(Col_var2);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO TABLE4a VALUES(11, 10000, 12345, 'The first row'),
(22, 20000, 23456, 'The second row'),
(33, 30000, 34567, 'The third row');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO TABLE4b VALUES('INFORMIX', 'ORACLE', 'MICROSOFT', 1234),
('SUN MICROSYSTEMS', 'SILICON GRAPHICS','HEWLETT PACKARD', 3456),
('WAL-MART', 'LUCKY', 'SAFEWAY', 4321);"""
    output = _dci.cmdexec(stmt)
    
    # ---------------------
    #  1: UPDATE table4a --
    # ---------------------
    stmt = """select * from TABLE4a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s0')
    
    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """UPDATE TABLE4a 
SET    col_fix1 = 100000,
col_fix2 = 1234,
col_fix3 = NULL,
col_var4 = 'It is a Varchar(20)'
READ COMMITTED ACCESS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    
    stmt = """select * from TABLE4a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from TABLE4a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    
    # ---------------------
    #  2: UPDATE vwtab4a --
    # ---------------------
    stmt = """select * from VWTAB4a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s3')
    
    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """UPDATE VWTAB4a 
SET    col_var4 = 'CHANGED VALUE'
WHERE  col_var4 like '%third%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from VWTAB4a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s4')
    
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from VWTAB4a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s5')
    
    # ---------------------
    #  3: UPDATE table4b &
    #     UPDATE vwtab4b
    # ---------------------
    stmt = """select * from TABLE4b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s6')
    
    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """UPDATE TABLE4b 
SET    col_var3 = 'The third varchar',
col_fix4 = 1000
SERIALIZABLE ACCESS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    
    stmt = """select * from TABLE4b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s7')
    
    stmt = """UPDATE VWTAB4b 
SET    col_var3 = NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    
    stmt = """select * from VWTAB4b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s8')
    
    stmt = """ALTER INDEX i4bvar2 ATTRIBUTES AUDITCOMPRESS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ROLLBACK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from VWTAB4b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s9')
    
    stmt = """drop view VWTAB4a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view VWTAB4b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table TABLE4a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table TABLE4b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test004(desc="""Update/Rollback transaction tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =====================  Begin Test Case Header  ===================
    # Test case name	: Arkt1424:  testa04
    # Description		: Update/Rollback transaction tests
    # Test case inputs	:
    # Test case outputs	:
    # Expected Results	: (provided a high-level description)
    #
    # Note:
    
    stmt = """drop view VWTAB5a;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view VWTAB5b;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table TABLE5a;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table TABLE5b;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE TABLE5a(Col_fix1  CHAR(20)    NO DEFAULT NOT NULL,
Col_var2  VARCHAR(20) NO DEFAULT NOT NULL,
Col_var3  VARCHAR(40) ,
Col_fix4  DATE        DEFAULT CURRENT_DATE,
Col_var5  VARCHAR(20),
Col_fix6  TIME,
Col_fix7  LARGEINT,
Col_var8  VARCHAR(20),
Col_fix9  NUMERIC(4),
Col_var10 VARCHAR(30),
PRIMARY KEY (Col_fix1, Col_var2)
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE TABLE5b(Col_var1  VARCHAR(30) NO DEFAULT NOT NULL,
Col_fix2  INT,
Col_var3  VARCHAR(20),
Col_fix4  TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
Col_var5  VARCHAR(15),
Col_var6  VARCHAR(20),
Col_fix7  INT,
Col_fix8  INT,
Col_var9  VARCHAR(30),
Col_fix10 INT,
PRIMARY KEY (Col_var1)
);"""
    output = _dci.cmdexec(stmt)
    
    # CREATE VIEWS FOR EACH TABLE --
    
    stmt = """CREATE VIEW VWTAB5a AS SELECT * FROM TABLE5a;"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE VIEW VWTAB5b AS SELECT * FROM TABLE5b;"""
    output = _dci.cmdexec(stmt)
    
    # CREATE INDICIES --
    
    stmt = """CREATE INDEX i5avar2  on TABLE5a(Col_var2);"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE INDEX i5avar5  on TABLE5a(Col_var5);"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE INDEX i5avar8  on TABLE5a(Col_var8);"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE INDEX i5bvar3  on TABLE5b(Col_var5);"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE INDEX i5bvar5  on TABLE5b(Col_var5);"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE INDEX i5bvar9  on TABLE5b(Col_var9);"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE INDEX i5bfix10 on TABLE5b(Col_fix10);"""
    output = _dci.cmdexec(stmt)
    
    # INSERT VALUES INTO THE TABLES --
    
    stmt = """INSERT INTO TABLE5a VALUES('KAREN',
'Ropin the Wind',
'Brooks',
date '1985-03-20',
'Liberty',
time '04:10:00',
120,
'Country',
1000,
'Cupertino'
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO TABLE5a VALUES('CINDY',
'Waynes World',
NULL,
date '1996-02-25',
'Reprise',
time '01:35:00',
140,
'Soundtrack',
2000,
'Sunnyvale'
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO TABLE5a VALUES('SHELLY',
'Luck of the Draw',
'Jackson',
date '1985-03-20',
'Capitol',
time '02:10:00',
160,
'Rock',
3000,
'San Jose'
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO TABLE5b VALUES('Saving Private Ryan',
10111,
'Tom Hanks',
timestamp '1985-03-20 12:12:12.120000',
'AMC20',
'BATTLE',
160,
1203,
'Santa Clara',
3000
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO TABLE5b VALUES('Youve Got Mail',
20222,
'Tom Hanks',
timestamp '1998-02-10 11:11:11.110000',
'AMC16',
'COMDEY',
260,
3402,
'Campbell',
5000
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO TABLE5b VALUES('Shakepear In Love',
30333,
'Gwyneth Paltrowl',
timestamp '1999-01-04 02:10:00.000000',
'AMC6',
'LIGHT COMEDY',
300,
1234,
'San Jose',
4500
);"""
    output = _dci.cmdexec(stmt)
    
    # ---------------------
    #  1: UPDATE table5a --
    # ---------------------
    stmt = """select * from TABLE5a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s0')
    
    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """UPDATE TABLE5a 
SET    col_var3 = 'THE COL_VAR3',
col_fix4 = CURRENT_DATE,
col_var5 = 'THE COL_VAR5',
col_var8 = 'THE COL_VAR8',
col_var10= 'THE COL_VAR10'
REPEATABLE READ ACCESS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    
    stmt = """select * from TABLE5a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from TABLE5a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s2')
    
    # ---------------------
    #  2: UPDATE vwtab5a --
    # ---------------------
    stmt = """select * from VWTAB5a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s3')
    
    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """UPDATE VWTAB5a 
SET    col_var8 = 'CHANGED VALUE'
WHERE  col_var10 like '%San%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from VWTAB5a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s4')
    
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from VWTAB5a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s5')
    
    # ---------------------
    #  3: UPDATE table5b &
    #     UPDATE vwtab5b
    # ---------------------
    stmt = """select * from TABLE5b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s6')
    
    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """UPDATE TABLE5b 
SET    col_var9 = NULL,
col_fix10= 1000000
SERIALIZABLE ACCESS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    
    stmt = """select * from TABLE5b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s7')
    
    stmt = """UPDATE VWTAB5b 
SET    col_var9 = 'CHANGE BACK FROM NULL';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    
    stmt = """select * from VWTAB5b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s8')
    
    stmt = """ALTER INDEX i5bvar9 ATTRIBUTES AUDITCOMPRESS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ROLLBACK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from VWTAB5b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s9')
    
    stmt = """drop view VWTAB5a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view VWTAB5b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table TABLE5a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table TABLE5b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test005(desc="""Update/Rollback transaction tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =====================  Begin Test Case Header  ===================
    # Test case name	: Arkt1424:  testa05
    # Description		: Update/Rollback transaction tests
    # Test case inputs	:
    # Test case outputs	:
    # Expected Results	: (provided a high-level description)
    #
    # Note: (table6a, table6b used)
    
    stmt = """drop view VWTAB6a;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view VWTAB6b;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table TABLE6a;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table TABLE6b;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE TABLE6a(Col_fix1  CHAR(30),
Col_var2  VARCHAR(20),
Col_fix3  INT,
Col_var4  VARCHAR(30),
Col_fix5  DECIMAL(5,1) UNSIGNED,
Col_var6  VARCHAR(30),
Col_fix7  LARGEINT,
Col_var8  VARCHAR(25),
Col_fix9  NUMERIC(10),
Col_var10 VARCHAR(30),
Col_fix11 SMALLINT,
Col_fix12 DATE
) no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE TABLE6b(Col_fix1  CHAR(30),
Col_var2  VARCHAR(20),
Col_fix3  INT,
Col_var4  VARCHAR(30),
Col_fix5  DECIMAL(5,1) UNSIGNED,
Col_var6  VARCHAR(30),
Col_fix7  LARGEINT,
Col_var8  VARCHAR(25),
Col_fix9  NUMERIC(10),
Col_var10 VARCHAR(20),
Col_fix11 SMALLINT,
Col_var12 VARCHAR(20)
) no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWTAB6a AS SELECT * FROM TABLE6a;"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE VIEW VWTAB6b AS SELECT * FROM TABLE6b;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE INDEX i6avar10 ON TABLE6a(col_var10);"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE INDEX i6bvar12 ON TABLE6b(col_var12);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO TABLE6a VALUES('Karen',
'XIONG',
001,
'LOC251',
2200,
'Texas A&M University',
980520,
'China',
94,
'Texas',
1997,
date '1997-12-20'
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO TABLE6a VALUES('Lalitha',
'Maruvada',
002,
'LOC252',
2130,
'University of Colorado',
970320,
'India',
93,
'Colorado',
1997,
date '1997-05-20'
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO TABLE6a VALUES('Jerry',
'Zheng',
003,
'LOC201',
1320,
'Cornell University',
960302,
'Taiwan',
92,
'New York',
1995,
date '1995-12-10'
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO TABLE6b VALUES('Karen',
'XIONG',
001,
'LOC251',
2200,
'San Jose State',
980520,
'China',
94,
'Texas',
1997,
'University relations'
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO TABLE6b VALUES('Lalitha',
'Maruvada',
002,
'LOC252',
2130,
'University of Colorado',
970320,
'India',
93,
'Colorado',
1997,
'Job fair'
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO TABLE6b VALUES('Jerry',
'Zheng',
003,
'LOC201',
1320,
'Cornell University',
960302,
'Taiwan',
92,
'New York',
1995,
'Internal Transfer'
);"""
    output = _dci.cmdexec(stmt)
    
    # ---------------------
    #  1: UPDATE table6a --
    # ---------------------
    stmt = """select * from TABLE6a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    
    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """UPDATE TABLE6a 
SET    col_fix1 = 'FIRST_NAME',
col_var2 = 'LAST_NAME',
col_fix3 = 100,
col_var4 = 'LOCATION',
col_fix5 = 1234,
col_var6 = 'SCHOOL NAME',
col_fix7 = 991231,
col_var8 = 'NATIONALITY',
col_fix9 = 2000,
col_var10= 'STATE',
col_fix11= 1999,
col_fix12= CURRENT_DATE
REPEATABLE READ ACCESS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    
    stmt = """select * from TABLE6a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from TABLE6a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    
    # ---------------------
    #  2: UPDATE vwtab6a --
    # ---------------------
    stmt = """select * from VWTAB6a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
    
    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """UPDATE VWTAB6a 
SET    col_var8 = 'CHANGED VALUE'
WHERE  col_var10 like '%Texas%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from VWTAB6a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s4')
    
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from VWTAB6a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s5')
    
    # ---------------------
    #  3: UPDATE table6b &
    #     UPDATE vwtab6b
    # ---------------------
    stmt = """select * from TABLE6b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s6')
    
    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """UPDATE TABLE6b 
SET    col_fix1 = NULL,
col_var2 = NULL,
col_fix3 = 100,
col_var4 = NULL,
col_fix5 = 1234.5,
col_var6 = NULL,
col_fix7 = 991231,
col_var8 = NULL,
col_fix9 = 2000,
col_var10= NULL,
col_fix11= 1999,
col_var12= NULL    

SERIALIZABLE ACCESS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    
    stmt = """select * from TABLE6b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s7')
    
    stmt = """UPDATE VWTAB6b 
SET    col_fix1 = 'FIRST_NAME',
col_var2 = 'LAST_NAME',
col_fix3 = 100,
col_var4 = 'LOCATION',
col_fix5 = 1234.6,
col_var6 = 'SCHOOL NAME',
col_fix7 = 991231,
col_var8 = 'NATIONALITY',
col_fix9 = 2000,
col_var10= 'STATE',
col_fix11= 1999,
col_var12= 'RECRUITING SOURCES';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    
    stmt = """select * from VWTAB6b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s8')
    
    stmt = """ALTER INDEX i6bvar12 ATTRIBUTES AUDITCOMPRESS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ROLLBACK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from VWTAB6b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s9')
    
    stmt = """drop view VWTAB6a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view VWTAB6b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table TABLE6a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table TABLE6b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test006(desc="""Update/Rollback transaction tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =====================  Begin Test Case Header  ===================
    # Test case name	: Arkt1424:  testa06
    # Description		: Update/Rollback transaction tests
    # Test case inputs	:
    # Test case outputs	:
    # Expected Results	: (provided a high-level description)
    #
    # Note: (table6c, table6d used)
    
    stmt = """drop view VWTAB6c;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view VWTAB6d;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table TABLE6c;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table TABLE6d;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE TABLE6c(Col_var1  VARCHAR(30)     NOT NULL,
Col_fix2  CHAR(20),
Col_var3  VARCHAR(20),
Col_fix4  INT,
Col_var5  VARCHAR(30),
Col_fix6  DECIMAL(5,1) SIGNED,
Col_var7  VARCHAR(30),
Col_fix8  LARGEINT,
Col_var9  VARCHAR(25),
Col_fix10 NUMERIC(10),
Col_var11 Varchar(40)     NOT NULL,
Col_fix12 SMALLINT,
PRIMARY KEY (Col_var1, Col_var11))
STORE BY PRIMARY KEY;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE TABLE6d(Col_var1  VARCHAR(30),
Col_fix2  CHAR(10),
Col_var3  VARCHAR(20),
Col_fix4  INT,
Col_var5  VARCHAR(25),
Col_fix6  DECIMAL(5,1) SIGNED,
Col_var7  VARCHAR(50),
Col_fix8  LARGEINT,
Col_var9  VARCHAR(25),
Col_fix10 NUMERIC(10),
Col_var11 VARCHAR(30),
Col_var12 VARCHAR(35)
) no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWTAB6c AS SELECT * FROM TABLE6c;"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE VIEW VWTAB6d AS SELECT * FROM TABLE6d;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE INDEX i6cvar7  ON TABLE6c(col_var7);"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE INDEX i6cvar9  ON TABLE6c(col_var9);"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE INDEX i6cvar11 ON TABLE6c(col_var11);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE INDEX i6dvar1  ON TABLE6d(col_var1);"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE INDEX i6dvar3  ON TABLE6d(col_var3);"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE INDEX i6dvar5  ON TABLE6d(col_var5);"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE INDEX i6dvar7  ON TABLE6d(col_var7);"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE INDEX i6dvar9  ON TABLE6d(col_var9);"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE INDEX i6dvar11 ON TABLE6d(col_var11);"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE INDEX i6dvar12 ON TABLE6d(col_var12);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO TABLE6c VALUES('Karen',
'XIONG',
'Female',
001,
'LOC251',
2200,
'San Jose State',
980520,
'China',
94,
'Texas',
1997
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO TABLE6c VALUES('Lalitha',
'Maruvada',
'Female',
002,
'LOC252',
2130,
'University of Colorado',
970320,
'India',
93,
'Colorado',
1997
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO TABLE6c VALUES('Jerry',
'Zheng',
'Male',
003,
'LOC201',
1320,
'Cornell University',
960302,
'Taiwan',
92,
'New York',
1995
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO TABLE6d VALUES('Karen',
'XIONG',
'Female',
001,
'LOC251',
2200,
'San Jose State',
980520,
'China',
94,
'Texas',
'University relations'
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO TABLE6d VALUES('Lalitha',
'Maruvada',
'Female',
002,
'LOC252',
2130,
'University of Colorado',
970320,
'India',
93,
'Colorado',
'Job Fair'
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO TABLE6d VALUES('Jerry',
'Zheng',
'Male',
003,
'LOC201',
1320,
'Cornell University',
960302,
'Taiwan',
92,
'New York',
'Internal Transfer'
);"""
    output = _dci.cmdexec(stmt)
    
    # ---------------------
    #  1: UPDATE table6c &
    #     UPDATE vwtab6c
    # ---------------------
    stmt = """select * from TABLE6c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """UPDATE TABLE6c 
SET col_fix2 = 'LAST_NAME',
col_var3=  'GENGER',
col_var5 = 'LOCATION',
col_var7 = 'SCHOOL',
col_var9 = 'COUNTRY'
WHERE EXISTS
(select TABLE6c.col_fix8 from TABLE6c, TABLE6d 
where  TABLE6c.col_fix8 = TABLE6d.col_fix8)
SERIALIZABLE ACCESS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    
    stmt = """select * from TABLE6c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    #08/06/07 Self-referencing updates feature on R2.2.
    stmt = """UPDATE VWTAB6c 
SET
col_fix2 = NULL,
col_var3=  NULL,
col_var5 = 'LOCATION',
col_var7 = 'SCHOOL',
col_var9 = NULL
WHERE EXISTS
(select TABLE6c.col_fix8 from TABLE6c,TABLE6d 
where TABLE6c.col_fix8 = TABLE6d.col_fix8)
SERIALIZABLE ACCESS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    
    stmt = """select * from VWTAB6c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    stmt = """ALTER INDEX i6cvar7  ATTRIBUTES NO AUDITCOMPRESS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ALTER INDEX i6cvar9  ATTRIBUTES AUDITCOMPRESS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ALTER INDEX i6cvar11 ATTRIBUTES BUFFERED;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3073')
    
    stmt = """ROLLBACK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from VWTAB6c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    # ---------------------
    #  2: UPDATE table6d &
    #     UPDATE vwtab6d
    # ---------------------
    stmt = """select * from TABLE6d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """UPDATE TABLE6d 
SET    col_var5 = NULL,
col_var7 = NULL,
col_var9 = NULL,
col_fix10= 1000000,
col_var11= NULL,
col_var12= NULL
WHERE  col_fix8 > 980000    

SERIALIZABLE ACCESS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from TABLE6d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    stmt = """select * from VWTAB6d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    stmt = """ALTER INDEX i6dvar1  ATTRIBUTES AUDITCOMPRESS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """ALTER INDEX i6dvar3  ATTRIBUTES NO AUDITCOMPRESS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """ALTER INDEX i6dvar5  ATTRIBUTES AUDITCOMPRESS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """ALTER INDEX i6dvar7  ATTRIBUTES NO AUDITCOMPRESS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """ALTER INDEX i6dvar9  ATTRIBUTES AUDITCOMPRESS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """ALTER INDEX i6dvar11 ATTRIBUTES NO AUDITCOMPRESS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """ALTER INDEX i6dvar12 ATTRIBUTES AUDITCOMPRESS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ROLLBACK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from VWTAB6d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    stmt = """drop view VWTAB6c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view VWTAB6d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table TABLE6c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table TABLE6d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test007(desc="""Update/Rollback transaction tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =====================  Begin Test Case Header  ===================
    # Test case name	: Arkt1424:  testa07
    # Description		: Update/Rollback transaction tests
    # Test case inputs	:
    # Test case outputs	:
    # Expected Results	: (provided a high-level description)
    #
    # Note: (table7a, table7b used)
    
    stmt = """drop view VWTAB7a;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view VWTAB7b;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table TABLE7a;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table TABLE7b;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE TABLE7a(Col_fix1  CHAR(20),
Col_fix2  CHAR(20),
Col_fix3  INT,
Col_fix4  NUMERIC(4,1),
Col_fix5  DECIMAL(5,1) SIGNED,
Col_fix6  DECIMAL(5),
Col_fix7  LARGEINT,
Col_fix8  CHAR(35),
Col_fix9  NUMERIC(10),
Col_fix10 INT,
Col_fix11 SMALLINT,
Col_fix12 DATE
) no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE TABLE7b(Col_var1  VARCHAR(20),
Col_var2  VARCHAR(20),
Col_var3  VARCHAR(30),
Col_var4  VARCHAR(30),
Col_var5  VARCHAR(30),
Col_var6  VARCHAR(30),
Col_var7  VARCHAR(35),
Col_var8  VARCHAR(35),
Col_var9  VARCHAR(30),
Col_var10 VARCHAR(30),
Col_var11 VARCHAR(30),
Col_var12 VARCHAR(35)
) no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE VIEW VWTAB7a AS SELECT * FROM TABLE7a;"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE VIEW VWTAB7b AS SELECT * FROM TABLE7b;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE INDEX i7afix10 ON TABLE7a(col_fix10);"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE INDEX i7bvar12 ON TABLE7b(col_var12);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO TABLE7a VALUES('The first row',
'The table7a-1',
100,
101,
-1456,
12345,
100000,
'All fixed columns - row1',
100,
11,
001,
date '02/15/1999'
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO TABLE7a VALUES('The second row',
'The table7a-2',
200,
202,
-246,
23456,
200000,
'All fixed columns - row2',
200,
22,
002,
date '02/16/1999'
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO TABLE7a VALUES('The third row',
'The table7a-3',
300,
303,
-357,
34567,
300000,
'All fixed columns - row3',
200,
22,
002,
date '02/17/1999'
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO TABLE7b VALUES('Sun Micro.',
'Menlo Park',
'California',
'95017',
'Jim Mcliney',
'Stanford',
'USA',
'Chief Executive Officer',
'Solaris7',
'Friday',
'January',
'Weekday'
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO TABLE7b VALUES('Oracle',
'Belmont',
'California',
'95035',
'Larry Esson',
'UC Berkeley',
'USA',
'Chief Executive Officer',
'Oracle8',
'Sunday',
'February',
'Weekend'
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO TABLE7b VALUES('Compaq Computers',
'Houston',
'Texas',
'77043',
'Eckard Phiffer',
'Oxford',
'England',
'Chief Executive Officer',
'Presario5',
'Tuesday',
'May',
'Weekday'
);"""
    output = _dci.cmdexec(stmt)
    
    # ---------------------
    #  1: UPDATE table7a --
    # ---------------------
    stmt = """select * from TABLE7a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s0')
    
    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """UPDATE TABLE7a 
SET    col_fix1 = 'first fixed row',
col_fix2 = 'Second fixed row',
col_fix3 = 111,
col_fix4 = 222,
col_fix5 = 333,
col_fix6 = 444,
col_fix7 = 555,
col_fix8 = 'changed column',
col_fix9 = 6666,
col_fix10= 7777,
col_fix11= 8888,
col_fix12= cast(dateformat(CURRENT_DATE,usa) as date)
REPEATABLE READ ACCESS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    
    stmt = """select * from TABLE7a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from TABLE7a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s2')
    
    # ---------------------
    #  2: UPDATE vwtab7a --
    # ---------------------
    stmt = """select * from VWTAB7a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s3')
    
    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """UPDATE VWTAB7a 
SET    col_fix1 ='fffffffffffffffff',
col_fix2 ='ggggggggggggggggg'
WHERE  col_fix8 like '%column%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    
    stmt = """select * from VWTAB7a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s4')
    
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from VWTAB7a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s5')
    
    # ---------------------
    #  3: UPDATE table7b &
    #     UPDATE vwtab7b
    # ---------------------
    stmt = """select * from TABLE7b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s6')
    
    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """UPDATE TABLE7b 
SET    col_var1 = NULL,
col_var2 = NULL,
col_var3 = NULL,
col_var4 = NULL,
col_var5 = NULL,
col_var6 = NULL,
col_var7 = 'CHANGED VALUE',
col_var8 = NULL,
col_var9 = NULL,
col_var10= NULL,
col_var11= NULL,
col_var12= NULL    

SERIALIZABLE ACCESS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    
    stmt = """select * from TABLE7b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s7')
    
    stmt = """UPDATE VWTAB7b 
SET    col_var1 = 'Company name',
col_var2 = 'Location',
col_var3 = 'State',
--       col_var4 = NULL,
col_var5 = NULL,
col_var6 = NULL,
col_var7 = NULL,
col_var8 = NULL,
col_var9 = NULL,
col_var10= 'work date',
col_var11= 'Work month',
col_var12= 'Work time'
WHERE  col_var10= 'Friday'
OR  col_var12= 'Weekend';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 0)
    
    stmt = """select * from VWTAB7b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s8')
    
    stmt = """ALTER INDEX i7bvar12 ATTRIBUTES AUDITCOMPRESS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ROLLBACK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from VWTAB7b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s9')
    
    stmt = """drop view VWTAB7a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view VWTAB7b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table TABLE7a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table TABLE7b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

