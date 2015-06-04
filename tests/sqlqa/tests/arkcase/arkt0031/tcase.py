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
    
def test001(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     psttsta02
    #  Description:        This test drops catalog used in the test
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    #
    #
    #  Table Name:      keytaba
    #  Primary Key:     SYSKEY
    #  Attributes:      key sequenced table
    #  Prot. View (1):  VTAB1; col_2 WHERE col_2 > 5
    #
    #  ========================================
    #  |col name:       | col_1      | col_2  |
    #  |col defn:       | pic 99     | pic 9  |
    #  |special attrib: | NO DEFAULT |        |
    #  |================|============|========|
    #  |                |    13      |   1    |
    #  |                |    21      |   3    |
    #  |                |    43      |   5    |
    #  |                |    86      |   7    |
    #  |                |    99      |   9    |
    #  |                |    77      |   4    |
    #  ========================================
    #
    #  Create table keytaba
    
    stmt = """drop view pview3;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view pview4;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view pview5;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view pview6;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view pview7;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view sview2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view vtab1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view vtab2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view stab1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view tab2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """DROP TABLE keytaba;"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE TABLE keytaba (col_1 pic 99 NO DEFAULT,
col_2 pic 9) no partition;"""
    output = _dci.cmdexec(stmt)
    
    #  Create protection view (VTAB1) on keytaba
    
    stmt = """CREATE VIEW vtab1 (col_2)
AS SELECT col_2 FROM keytaba 
WHERE col_2 > 5
WITH CHECK OPTION;"""
    output = _dci.cmdexec(stmt)
    
    #  Insert records into keytaba
    
    stmt = """INSERT INTO keytaba VALUES (13,1);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO keytaba VALUES (21,3);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO keytaba VALUES (43,5);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO keytaba VALUES (86,7);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO keytaba VALUES (99,9);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO keytaba VALUES (77,4);"""
    output = _dci.cmdexec(stmt)
    
    ###############################################################################
    #
    #  Table Name:      keytabb
    #  Primary Key:     col_2 and col_3
    #  Attributes:      key sequenced table
    #                   contiguous key columns
    #                   table not audited
    #  Prot. View (1):  PVIEW4; SELECT * FROM keytabb
    #
    #  |col name:       | col_1        | col_2    | col_3    |
    #  |col defn:       | pic x(3)     | pic x(7) | pic 9(3) |
    #  |special attrib: | default = 'L'|          |          |
    #  |================|==============|==========|==========|
    #  |                |     abc      |     a    |   123    |
    #  |                |     def      |     b    |   456    |
    #  |                |     ghi      |     c    |   789    |
    #  |                |     jkl      |     d    |   987    |
    #  |                |     mno      |     e    |   654    |
    #  |                |     pqr      |     f    |   321    |
    #  |                |     stu      |     g    |   246    |
    #  |                |     vwx      |     h    |   802    |
    #
    #
    #  Create table keytabb
    #
    
    stmt = """DROP   TABLE keytabb;"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE TABLE keytabb 
(col_1 pic x(3) DEFAULT 'L',
col_2 pic x(7) NOT NULL,
col_3 pic 9(3) NOT NULL,
PRIMARY KEY (col_2, col_3)
)
;"""
    output = _dci.cmdexec(stmt)
    
    #  Create protection view (PVIEW4) on keytabb
    
    stmt = """CREATE VIEW pview4 
AS SELECT * FROM keytabb 
WITH CHECK OPTION;"""
    output = _dci.cmdexec(stmt)
    
    #  Insert records into keytabb
    
    stmt = """INSERT INTO keytabb VALUES ('abc', 'a', 123);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO keytabb VALUES ('def', 'b', 456);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO keytabb VALUES ('ghi', 'c', 789);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO keytabb VALUES ('jkl', 'd', 987);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO keytabb VALUES ('mno', 'e', 654);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO keytabb VALUES ('pqr', 'f', 321);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO keytabb VALUES ('stu', 'g', 246);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO keytabb VALUES ('vwx', 'h', 802);"""
    output = _dci.cmdexec(stmt)
    
    ###############################################################################
    #
    #
    #  Table Name:      keytabc
    #  Primary Key:     col_1 and col_3
    #  Attributes:      key sequenced table
    #                   non-contiguous key columns
    #  Prot. View (1):  PVIEW5; SELECT * FROM keytabc
    #  Indexes:         UNIQUE; col_2 DESC; KEYTAG 'AH'
    #
    #  |col name:       | col_1    | col_2    | col_3    |
    #  |col defn:       | pic x(3) | pic x(7) | pic 9(3) |
    #  |special attrib: |          |          |          |
    #  |================|==========|==========|==========|
    #  |                |    abc   |     z    |   246    |
    #  |                |    def   |     y    |   802    |
    #  |                |    ghi   |     x    |   468    |
    #  |                |    jkl   |     w    |   024    |
    #  |                |    zyx   |     v    |   135    |
    #  |                |    wvu   |     u    |   791    |
    #  |                |    tsr   |     t    |   357    |
    #  |                |    qpo   |     s    |   913    |
    
    #  Create table keytabc
    
    stmt = """DROP   TABLE keytabc;"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE TABLE keytabc 
(col_1 pic x(3) NOT NULL,
col_2 pic x(7) NOT NULL,
col_3 pic 9(3) NOT NULL,
PRIMARY KEY (col_1, col_3));"""
    output = _dci.cmdexec(stmt)
    
    #  Create protection view (PVIEW5) on keytabc
    
    stmt = """CREATE VIEW pview5 
AS SELECT * FROM keytabc;"""
    output = _dci.cmdexec(stmt)
    
    #  Create unique index (index1) keytabc
    
    stmt = """CREATE UNIQUE INDEX index1 
on keytabc (col_2 DESC);"""
    output = _dci.cmdexec(stmt)
    
    #  Insert records into keytabc
    
    stmt = """INSERT INTO keytabc VALUES ('abc', 'z', 246);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO keytabc VALUES ('def', 'y', 802);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO keytabc VALUES ('ghi', 'x', 468);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO keytabc VALUES ('jkl', 'w', 024);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO keytabc VALUES ('zyx', 'v', 135);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO keytabc VALUES ('wvu', 'u', 791);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO keytabc VALUES ('tsr', 't', 357);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO keytabc VALUES ('qpo', 's', 913);"""
    output = _dci.cmdexec(stmt)
    
    #  CREATE VIEW (join) between keytabb and keytabc
    
    stmt = """CREATE VIEW sview2 
(col_b1, col_b2, col_b3, col_c1, col_c2, col_c3)
AS SELECT keytabb.*, keytabc.*
FROM keytabb, keytabc 
WHERE keytabb.col_1 = keytabc.col_1;"""
    output = _dci.cmdexec(stmt)
    
    #########################################################################
    #
    #
    #  Table Name:      keytabd
    #  Primary Key:     col_1, col_2, col_3, col_5
    #  Attributes:      key sequenced table
    #                   4 non-contiguous key columns
    #  Short. View (1): STAB1; col_4 > 6000
    #  Short. View (2): STAB1; SELECT * FROM keytabd
    #
    #  |col name:       | col_1    | col_2    | col_3    | col_4     | col_5     |
    #  |col defn:       | pic x(3) | pic 9(4) | pic x(5) | pic 9(6)  | pic x(7)  |
    #  |special attrib: |          |          |          |           |           |
    #  |================|==========|==========|==========|===========|===========|
    #  |                |   ah     |   1234   |   qual   |   1000    |   ts      |
    #  |                |   jz     |   5678   |   qual   |   2000    |   foxii   |
    #  |                |   cf     |   9012   |   qual   |   3000    |   tsii    |
    #  |                |   pk     |   3456   |   qual   |   4000    |   tsii    |
    #  |                |   sf     |   7890   |   qual   |   5000    |   tsii    |
    #  |                |   xy     |   3333   |   none   |   7777    |   gone    |
    #  Create table keytabd
    
    stmt = """DROP   TABLE keytabd;"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE TABLE keytabd 
(col_1 pic x(3) NOT NULL,
col_2 pic 9(4) NOT NULL,
col_3 pic x(5) NOT NULL,
col_4 pic 9(6),
col_5 pic x(7) NOT NULL,
PRIMARY KEY (col_1, col_2, col_3, col_5));"""
    output = _dci.cmdexec(stmt)
    
    #  CREATE VIEW (STAB1) on keytabd
    
    stmt = """CREATE VIEW stab1 
(col_a, col_b, col_c, col_d, col_e)
AS SELECT * FROM keytabd;"""
    output = _dci.cmdexec(stmt)
    
    #  CREATE VIEW (STAB2) on keytabd
    
    stmt = """CREATE VIEW tab2 
AS SELECT * FROM keytabd 
WHERE col_4 > 6000;"""
    output = _dci.cmdexec(stmt)
    
    #  Insert records into keytabd
    
    stmt = """INSERT INTO keytabd VALUES ('ah', 1234, 'qual', 1000, 'ts');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO keytabd VALUES ('jz', 5678, 'qual', 2000, 'foxii');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO keytabd VALUES ('cf', 9012, 'qual', 3000, 'tsii');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO keytabd VALUES ('pk', 3456, 'qual', 4000, 'tsii');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO keytabd VALUES ('sf', 7890, 'qual', 5000, 'tsii');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO keytabd VALUES ('xy', 3333, 'none', 7777, 'gone');"""
    output = _dci.cmdexec(stmt)
    ###############################################################################
    #
    #
    #  Table Name:      keytabe
    #  Primary Key:     col_2
    #  Attributes:      key sequenced table
    #                   non audited table
    #  Prot. View (1):  VTAB1; col_2 WHERE col_2 > 5
    #
    #  ===========================================
    #  |col name:       | col_1      | col_2     |
    #  |col defn:       | pic x(3)   | binary 64 |
    #  |special attrib: |            |           |
    #  |================|============|===========|
    #  |                |    a1b     | 123456789 |
    #  |                |    c2d     | 345678912 |
    #  |                |    e3f     | 567891234 |
    #  |                |    g4h     | 789123456 |
    #  |                |    i5j     | 912345678 |
    #  ===========================================
    
    stmt = """DROP   TABLE keytabe;"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE TABLE keytabe 
(col_1 pic x(3),
col_2 numeric (18) NOT NULL,
PRIMARY KEY (col_2))
;"""
    output = _dci.cmdexec(stmt)
    
    #  Create protection view (VTAB2) on keytabe
    
    stmt = """CREATE VIEW vtab2 
AS SELECT col_2 FROM keytabe WHERE col_2 > 5;"""
    output = _dci.cmdexec(stmt)
    
    #  Insert records into keytabe
    
    stmt = """INSERT INTO keytabe VALUES ('a1b', 123456789);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO keytabe VALUES ('c2d', 345678912);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO keytabe VALUES ('e3f', 567891234);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO keytabe VALUES ('g4h', 789123456);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO keytabe VALUES ('i5j', 912345678);"""
    output = _dci.cmdexec(stmt)
    
    ###############################################################################
    #  Table Name:      keytabf
    #  Primary Key:     SYSKEY
    #  Attributes:      key sequenced table
    #                   table not audited
    #
    #  |col name:    | col_bin_16 | col_bin_32 | col_bin_64 | varchar_254 |
    #  |col defn:    | binary 16  | binary 32  | binary 64  | varchar 254 |
    #  |spec attrib: |  (9(4))    |  (9(9))    |  (9(17))   |             |
    #  |=============|============|============|============|=============|
    #  |             |   999      | 999999999  |  17 9's    |     abc     |
    #  |             |   977      | 997777777  |  17 8's    |     def     |
    #  |             |   966      | 996666666  |  17 7's    |     ghi     |
    #  |             |   955      | 995555555  |  17 6's    |     jkl     |
    #  Create table keytabf
    
    stmt = """DROP   TABLE keytabf;"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE TABLE keytabf (col_bin_16 numeric (4),
col_bin_32 numeric (9),
col_bin_64 numeric (18),
varchar_254 varchar (254)) no partition
;"""
    output = _dci.cmdexec(stmt)
    
    #  Insert records into keytabf
    
    stmt = """INSERT INTO keytabf VALUES (999, 999999999, 99999999999999999, 'abc');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO keytabf VALUES (977, 997777777, 88888888888888888, 'def');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO keytabf VALUES (966, 996666666, 77777777777777777, 'ghi');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO keytabf VALUES (955, 995555555, 66666666666666666, 'jkl');"""
    output = _dci.cmdexec(stmt)
    
    ###############################################################################
    #
    #
    #  Table Name:      reltaba
    #  Primary Key:     SYSKEY
    #  Attributes:      relative table
    #  Prot. View (1):  PVIEW6; col_1, col_2 WHERE col_2 < 5
    #  Prot. View (2):  PVIEW7; col_1, col_2 WHERE col_2 > 6 and col_2 < 10
    #
    #  =====================================
    #  |col name:       | col_1   | col_2  |
    #  |col defn:       | pic xx  | pic 99 |
    #  |special attrib: |         |        |
    #  |================|=========|========|
    #  |                |   ab    |   1    |
    #  |                |   de    |   6    |
    #  |                |   gh    |   2    |
    #  |                |   jk    |   7    |
    #  |                |   mn    |   3    |
    #  |                |   pq    |   8    |
    #  |                |   st    |   4    |
    #  |                |   vw    |   9    |
    #  |                |   yz    |   5    |
    #  =====================================
    # Changed from Relative table to Key-sequenced table.
    
    stmt = """DROP   TABLE reltaba;"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE TABLE reltaba (col_1 pic xx, col_2 pic 99) no partition;"""
    output = _dci.cmdexec(stmt)
    
    #  Create protection view (PVIEW6) on reltaba
    
    stmt = """CREATE VIEW pview6 
AS SELECT col_1, col_2 FROM reltaba WHERE col_2 < 5
WITH CHECK OPTION;"""
    output = _dci.cmdexec(stmt)
    
    #  Create protection view (PVIEW7) on reltaba
    
    stmt = """CREATE VIEW pview7 
AS SELECT col_1, col_2 FROM reltaba 
WHERE col_2 > 6 AND col_2 < 10;"""
    output = _dci.cmdexec(stmt)
    
    #  Insert records into reltaba
    
    stmt = """INSERT INTO reltaba VALUES ('AB', 1);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO reltaba VALUES ('de', 6);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO reltaba VALUES ('gh', 2);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO reltaba VALUES ('jk', 7);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO reltaba VALUES ('mn', 3);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO reltaba VALUES ('pq', 8);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO reltaba VALUES ('st', 4);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO reltaba VALUES ('vw', 9);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO reltaba VALUES ('yz', 5);"""
    output = _dci.cmdexec(stmt)
    
    ###############################################################################
    #
    #
    #  Table Name:      reltabb
    #  Primary Key:     SYSKEY
    #  Attributes:      relative table
    #                   non audited table
    #  Prot. View (1):  PVIEW3; col_1 and col_4 WHERE col_1 = 'TU' and col_4 < 4
    #  Assertion (1):   col_1 IN ('AB', 'QR', 'TU', 'WX', 'AZ', 'QZ', 'XR', 'QT')
    #  Assertion (2):   col_3 < 99
    #  Assertion (3):   col_5 <> 7
    #  Assertion (4):   col_4 > 0.00
    #
    #  |col name:       | col_1    | col_2    | col_3  | col_4    | col_5  |
    #  |col defn:       | pic x(2) |varchar 7 | pic 99 | pic 9v99 | pic 9  |
    #  |special attrib: |          |          |        |          |        |
    #  |================|==========|==========|========|==========|========|
    #  |                |    XR    |  A       |   11   |   2.22   |   6    |
    #  |                |    AB    |  A       |   33   |   1.11   |   4    |
    #  |                |    QR    |  ABC     |   55   |   2.22   |   6    |
    #  |                |    TU    |  ABCD    |   77   |   3.33   |   8    |
    #  |                |    AZ    |  ABCDE   |   11   |   4.44   |   2    |
    #  |                |    XR    |  B       |   33   |   2.22   |   6    |
    #  |                |    WX    |  ABCDEF  |   21   |   1.23   |   1    |
    #  |                |    WX    |  QRSTUV  |   32   |   2.34   |   3    |
    #  |                |    QZ    |  ABCDEFG |   14   |   3.11   |   5    |
    #  |                |    XR    |  C       |   22   |   2.22   |   6    |
    #  |                |    QT    |  A1B2C3D |   53   |   0.11   |   9    |
    #
    #
    #  Create table reltabb
    #
    # Changed from Relative table to Key-sequenced table.
    
    stmt = """DROP   TABLE reltabb;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE reltabb (col_1 pic x(2),
col_2 varchar (7),
col_3 pic 99,
col_4 pic 9v99,
col_5 pic 9) no partition;"""
    output = _dci.cmdexec(stmt)
    
    #  Create protection view (PVIEW3) on reltabb
    
    stmt = """CREATE VIEW pview3 
AS SELECT col_1, col_4 FROM reltabb 
WHERE col_1 = 'TU' AND col_4 < 4;"""
    output = _dci.cmdexec(stmt)
    
    #  Create assertion (ASSERT1) on reltabb
    
    stmt = """ALTER TABLE reltabb ADD CONSTRAINT assert1
CHECK (col_1 IN('AB', 'QR', 'TU', 'WX', 'AZ', 'QZ', 'XR', 'QT'));"""
    output = _dci.cmdexec(stmt)
    
    #  Create assertion (ASSERT2) on reltabb
    
    stmt = """ALTER TABLE reltabb ADD CONSTRAINT assert2
CHECK (col_3 < 99);"""
    output = _dci.cmdexec(stmt)
    
    #  Create assertion (ASSERT3) on reltabb
    
    stmt = """ALTER TABLE reltabb ADD CONSTRAINT assert3
CHECK (col_5 <> 7);"""
    output = _dci.cmdexec(stmt)
    
    #  Create assertion (ASSERT4) on reltabb
    
    stmt = """ALTER TABLE reltabb ADD CONSTRAINT assert4
CHECK (col_4 > 0.00);"""
    output = _dci.cmdexec(stmt)
    
    #  Insert records into reltabb
    
    stmt = """INSERT INTO reltabb VALUES ('XR', 'A',       11, 2.22, 6);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO reltabb VALUES ('AB', 'A',       33, 1.11, 4);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO reltabb VALUES ('QR', 'ABC',     55, 2.22, 6);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO reltabb VALUES ('TU', 'ABCD',    77, 3.33, 8);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO reltabb VALUES ('AZ', 'ABCDE',   11, 4.44, 2);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO reltabb VALUES ('XR', 'B',       33, 2.22, 6);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO reltabb VALUES ('WX', 'ABCDEF',  21, 1.23, 1);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO reltabb VALUES ('WX', 'QRSTUV',  32, 2.34, 3);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO reltabb VALUES ('QZ', 'ABCDEFG', 14, 3.11, 5);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO reltabb VALUES ('XR', 'C',       22, 2.22, 6);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO reltabb VALUES ('QT', 'A1B2C3D', 53, 0.11, 9);"""
    output = _dci.cmdexec(stmt)
    
    ###############################################################################
    #
    #
    #  Table Name:      reltabc
    #  Primary Key:     SYSKEY
    #  Attributes:      relative table
    #
    #  |col name:    | col_bin_16 | col_bin_32 | col_bin_64 | varchar_254 |
    #  |col defn:    | binary 16  | binary 32  | binary 64  | varchar 254 |
    #  |spec attrib: |  (9(4))    |  (9(9))    |  (9(17))   |             |
    #  |=============|============|============|============|=============|
    #  |             |   999      | 999999999  |  17 9's    |     qrs     |
    #  |             |   977      | 888888888  |  17 8's    |     tuv     |
    #  |             |   966      | 777777777  |  17 7's    |     wxy     |
    #  |             |   955      | 666666666  |  17 6's    |     z       |
    #
    #
    #  Create table reltabc
    #
    
    # Changed from Relative table to Key-sequenced table.
    stmt = """CREATE TABLE reltabc (col_bin_16 numeric (4),
col_bin_32 numeric (9),
col_bin_64 numeric (18),
varchar_254 varchar (254)) no partition;"""
    output = _dci.cmdexec(stmt)
    #     CATALOG $arkt0031 ORGANIZATION R;
    #       CATALOG $arkt0031 ORGANIZATION K;
    
    #
    #  Insert records into reltabc
    #
    stmt = """INSERT INTO reltabc VALUES (999, 999999999, 99999999999999999, 'qrs');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO reltabc VALUES (977, 888888888, 88888888888888888, 'tuv');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO reltabc VALUES (966, 777777777, 77777777777777777, 'wxy');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO reltabc VALUES (955, 666666666, 66666666666666666, 'z');"""
    output = _dci.cmdexec(stmt)
    
    ###############################################################################
    #
    #
    #  Table Name:      enttaba
    #  Primary Key:     SYSKEY
    #  Attributes:      entry sequence table
    #                   non audited table
    #
    #  |col name:    | col_bin_16 | col_bin_32 | col_bin_64 | varchar_254 |
    #  |col defn:    | binary 16  | binary 32  | binary 64  | varchar 254 |
    #  |spec attrib: |  (9(4))    |  (9(9))    |  (9(17))   |             |
    #  |=============|============|============|============|=============|
    #  |             |   999      | 999999999  |  17 9's    | mno         |
    #  |             |   977      | 888888888  |  17 8's    | pqr         |
    #  |             |   966      | 777777777  |  17 7's    | stu         |
    #  |             |   955      | 666666666  |  17 6's    | vwx         |
    #  |             |   944      | 555555555  |  17 5's    | yza         |
    #  |             |   933      | 444444444  |  17 4's    | bcd         |
    #  |             |   922      | 333333333  |  17 3's    | efg         |
    #  |             |   911      | 222222222  |  17 2's    | hi          |
    #  |             |   900      | 111111111  |  17 1's    | abcdefghij  |
    #
    #  |col name:    | col_varchar_3 | col_varchar_4 | col_varchar_5 |
    #  |col defn:    | varchar 3     | varchar 4     | varchar 5     |
    #  |spec attrib: |               |               |               |
    #  |=============|===============|===============|===============|
    #  |             |      a        |      bc       |     def       |
    #  |             |      gh       |      ijk      |     lmno      |
    #  |             |      pqr      |      stuv     |     wxyza     |
    #  |             |      b        |      cd       |     efg       |
    #  |             |      hi       |      jkl      |     mnop      |
    #  |             |      qrs      |      tuvw     |     xyzab     |
    #  |             |      c        |      de       |     fgh       |
    #  |             |      ij       |      klm      |     nopq      |
    #  |             |      abc      |      def      |     ghi       |
    #
    #  Create table enttaba
    
    stmt = """DROP   TABLE enttaba;"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE TABLE enttaba (col_bin_16 numeric (4),
col_bin_32 numeric (9),
col_bin_64 numeric (18),
varchar_254 varchar (254),
col_varchar_3 varchar (3),
col_varchar_4 varchar (4),
col_varchar_5 varchar (5)) no partition;"""
    output = _dci.cmdexec(stmt)
    
    #  Insert records into enttaba
    
    stmt = """INSERT INTO enttaba VALUES (999, 999999999, 99999999999999999, 'mno',
'a', 'bc', 'def');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO enttaba VALUES (977, 888888888, 88888888888888888, 'pqr',
'gh', 'ijk', 'lmno');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO enttaba VALUES (966, 777777777, 77777777777777777, 'stu',
'pqr', 'stuv', 'wxyza');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO enttaba VALUES (955, 666666666, 66666666666666666, 'vwx',
'b', 'cd', 'efg');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO enttaba VALUES (944, 555555555, 55555555555555555, 'yza',
'hi', 'jkl', 'mnop');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO enttaba VALUES (933, 444444444, 44444444444444444, 'bcd',
'qrs', 'tuvw', 'xyzab');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO enttaba VALUES (922, 333333333, 33333333333333333, 'efg',
'c', 'de', 'fgh');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO enttaba VALUES (911, 222222222, 22222222222222222, 'hi',
'ij', 'klm', 'nopq');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO enttaba VALUES (900, 111111111, 11111111111111111,
'abcdefghij', 'abc', 'def', 'ghi');"""
    output = _dci.cmdexec(stmt)
    
    ###############################################################################
    #
    #
    #  Table Name:      enttabb
    #  Primary Key:     SYSKEY
    #  Attributes:      entry sequence table
    #
    #  |col name:    | col_1  | col_2    | col_3     | col_4     | col_5     |
    #  |col defn:    | char 3 | pic x(3) | binary 16 | binary 16 | binary 32 |
    #  |spec attrib: |        |          | signed    | unsigned  | signed    |
    #  |=============|========|==========|===========|===========|===========|
    #  |             |  abc   |   def    |  -1234    |   1234    |-123456789 |
    #
    #  =================================================
    #  |col name:    | col_6      | col_7              |
    #  |col defn:    | binary 32  | binary 64          |
    #  |spec attrib: | unsigned   | signed             |
    #  |=============|============|====================|
    #  |             | 123456789  |-123456789123456789 |
    #  =================================================
    #
    #  |col name:    | col_8      | col_9    | col_10   | col_11  | col_12   |
    #  |col defn:    | pic s9(2)  | smallint | smallint | integer | integer  |
    #  |spec attrib: | comp       | signed   | unsigned | signed  | unsigned |
    #  |=============|============|==========|==========|=========|==========|
    #  |             |    12      |  -100    |   100    |  -1000  |  1000    |
    #
    #  |col name:    | col_13     | col_14   | col_15    | col_16    |
    #  |col defn:    | largeint   | largeint | decimal 3 | decimal 3 |
    #  |spec attrib: | signed     | signed   | signed    | unsigned  |
    #  |=============|============|==========|===========|===========|
    #  |             |  -10000    |  -10000  |   -123    |    123    |
    #
    #  |col name:    | col_17          | col_18  | col_19          | col_20   |
    #  |col defn:    | decimal 3       | pic s9  | pic s9          | pic 9v99 |
    #  |spec attrib: | sign is leading | display | sign is leading | display  |
    #  |             | embedded        |         | embedded        |          |
    #  |=============|=================|=========|=================|==========|
    #  |             |       123       |    1    |       2         |   1.23   |
    #
    #
    #  Create table enttabb
    #
    
    stmt = """DROP   TABLE enttabb;"""
    output = _dci.cmdexec(stmt)
    stmt = """CREATE TABLE enttabb (  col_1 char (3),
col_2 pic x(3),
col_3 numeric (4) signed,
col_4 numeric (4) unsigned,
col_5 numeric (9) signed,
col_6 numeric (9) unsigned,
col_7 numeric (18) signed,
col_8 pic s9(2) comp,
col_9 smallint signed,
col_10 smallint unsigned,
col_11 integer signed,
col_12 integer unsigned,
col_13 largeint signed,
col_14 largeint signed,
col_15 decimal (3) signed,
col_16 decimal (3) unsigned,
col_17 decimal (3),
col_18 pic s9 display,
col_19 pic s9,
col_20 pic 9v99 display) no partition;"""
    output = _dci.cmdexec(stmt)
    
    #  Insert record into enttabb
    
    stmt = """INSERT INTO enttabb VALUES ('abc',
'def',
-1234,
1234,
-123456789,
123456789,
-12345678912345678,
12,
-100,
100,
-1000,
1000,
-10000,
10000,
-123,
123,
123,
1,
2,
1.23);"""
    output = _dci.cmdexec(stmt)
    
    ####################################################################
    
    #  SECURITY VIOLATION
    #  updating table where user has read
    #  authority but not write authority
    
    stmt = """select * from keytaba;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    
    stmt = """UPDATE keytaba SET col_1 = 55 WHERE col_1 = 21;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from keytaba;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    
    stmt = """select * from pview3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    
    stmt = """UPDATE pview3 SET col_4 = 5.55 WHERE col_4 = 3.33;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from pview3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    _testmgr.testcase_end(desc)

def test002(desc="""a04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A04
    #  Description:        Updating altered table
    #  Purpose:            Create a table, insert records, add a
    #                      new column, insert records, and update
    #                      both old and new records
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    # create the table
    
    stmt = """CREATE TABLE altable 
(col_1 pic x(3),
col_2 pic 99,
col_3 pic x) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # insert three records
    stmt = """INSERT INTO altable VALUES ('abc', 12, 'a');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO altable VALUES ('def', 34, 'b');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO altable VALUES ('ghi', 56, 'c');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  alter table and add a new column
    
    # ALTER TABLE altable ADD COLUMN col_4 pic 9999 DEFAULT 1111;
    
    #  insert three new records
    # INSERT INTO altable VALUES ('zyx', 98, 'z', 9876);
    # INSERT INTO altable VALUES ('wvu', 76, 'y', 5432);
    # INSERT INTO altable VALUES ('tsr', 54, 'x', 1987);
    
    #  update an old record
    # UPDATE altable SET col_1 = 'old', col_4 = 1234 WHERE col_1 = 'abc';
    
    #  update a new record
    # UPDATE altable SET col_1 = 'new', col_4 = 9999 WHERE col_1 = 'zyx';
    
    stmt = """select * from altable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s0')
    
    # 01/15/98 EL
    
    stmt = """drop table altable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test003(desc="""n01"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     N01
    #  Description:        This test has Negative tests for DML UPDATE
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #
    # =================== End Test Case Header  ===================
    
    stmt = """insert into reltabb values ('ZZ', 'CABBREL', 99, 0.11, 8);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')
    
    #  table name == blank table name
    stmt = """UPDATE SET (col_1 = 39);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  table name == invalid table name
    stmt = """UPDATE nametoolong SET col_1 = 39;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    #  table name == using catalog table
    stmt = """UPDATE TABLES SET groupid = 255;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    #  table name == using a catalog table
    stmt = """UPDATE basetabs SET rowsize = 200
where tablename like '%NOEXIST%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    #  table name == specifying more than one table to update
    stmt = """UPDATE keytaba,
 keytabb SET col_1 = 39;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  column name == using *
    stmt = """UPDATE keytaba SET * = 7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  column name == invalid column name
    stmt = """UPDATE keytaba 
SET thiscolumnnameistoolongforproduct = 999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    #  column name == column not in table
    stmt = """UPDATE keytaba SET no_column = 7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    #  column name == using same column twice
    stmt = """UPDATE keytaba SET col_1 = 9,
col_2 = 5, col_1 = 3 WHERE col_1 > 50;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4022')
    
    #  column name == update view with col in table but NOT in view
    stmt = """UPDATE vtab1 SET col_2 = 4,
col_1 = 5 WHERE col_1 BETWEEN 40 AND 50;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    #  column name == update SYSKEY in relative table
    stmt = """UPDATE reltaba SET SYSKEY = 0, col_1 = 'a';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4013')
    
    #  column name == update SYSKEY in entry sequence table
    stmt = """UPDATE enttaba SET SYSKEY = 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4013')
    
    #  column name == update SYSKEY in key sequence table
    stmt = """UPDATE keytaba SET SYSKEY = 1, col_2 = 77;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4013')
    
    #  column name == one column primary key in $set-list_A
    stmt = """UPDATE keytabe SET col_2 = 24680 WHERE col_2 = 123456789;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4033')
    
    #  column name == one column of a contiguous multi-column primary key
    stmt = """UPDATE keytabb SET col_3 = 777 WHERE col_2 = 'd';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4033')
    
    #  column name == one column of a non-contiguous multi-col primary key
    stmt = """UPDATE keytabc SET col_3 = 777 WHERE col_1 IN ('abc', 'qrs', 'stu');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4033')
    
    #  column name == all columns of the primary key (4 column key)
    stmt = """UPDATE keytabd 
SET col_1 = 'a', col_2 = 7, col_3 = 'qr', col_5 = 'xyz' WHERE col_4 > 3000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4033')
    
    #  column name == blank column list
    stmt = """UPDATE keytaba SET;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  column value == no column value specified (NO DEFAULT specified
    #                  in column definition)
    stmt = """UPDATE keytaba SET col_1, col_2 = 2 WHERE col_1 = 13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  column value == no column value specified (column was defined
    #                  without a default value)
    stmt = """UPDATE keytaba SET col_1 = 22  col_2 WHERE col_1 = 21;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  column value == update table using SYSKEY in an expression and
    #                  SYSKEY is not defined for the table
    stmt = """UPDATE keytabe SET col_2 = (SYSKEY - 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    #  column value == using an aggregate for new column value
    stmt = """UPDATE keytaba SET col_1 = 13, col_2 = AVG(col_1) WHERE col_1 = 77;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4015')
    
    #  column value == using an illegal operator for assignment
    stmt = """UPDATE keytaba SET col_2 := 17;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  where clause == using browse access
    stmt = """UPDATE keytabb SET col_1 = 'str' WHERE col_2 = 'h' browse access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3140')
    
    #  where clause == using stable access with a blank predicate
    stmt = """UPDATE keytabb SET col_1 = 'str' WHERE stable access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  where clause == using repeatable access with a blank predicate
    stmt = """UPDATE keytabb SET col_1 = 'str' WHERE repeatable access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # where clause == no records returned by where clause
    stmt = """UPDATE keytabc SET col_2 = 'L' WHERE col_3 = 651;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 0)
    
    # where clause == using table being updated in FROM clause of SELECT
    # 01/29/01 EL  The subquery can not use the same table as in UPDATE.
    stmt = """UPDATE keytabd SET col_4 = 9999 WHERE col_4 <
(SELECT avg(col_2) FROM keytabd);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01sa')
    
    #  where clause == using table being updated in FROM clause of SELECT
    #                  with an alias specified for the table;
    #                  updates the record with 'abc' in col_1 of keytabb
    stmt = """UPDATE keytabb SET col_1 = 'as' WHERE col_1 =
(SELECT first.col_1 FROM keytabb first
WHERE first.col_1 = 'abc');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  column value == new value violates a single assertion
    stmt = """UPDATE reltabb 
SET col_1 = 'ab', col_2 = 'xyz', col_3 = 22, col_4 = 9.99, col_5 = 3
WHERE col_1 = 'AB';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')
    
    #  column value == new values violates > 1 assertion
    ##expectfile ${test_dir}/n01exp n01s29
    stmt = """UPDATE reltabb 
SET col_1 = 'TU', col_2 = 'xyz', col_3 = 99, col_4 = 0.00, col_5 = 7
WHERE col_1 = 'AZ';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')
    
    #  column value == new values violates all assertions
    ##expectfile ${test_dir}/n01exp n01s30
    stmt = """UPDATE reltabb 
SET col_1 = 'no', col_2 = 'xyz', col_3 = 99, col_4 = 0.00, col_5 = 7
WHERE col_1 = 'QR';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')
    
    #  column value == key seq table; new value longer than original;
    #                  update binary-16 field with binary-32 number;
    #                  too many digits; (max value allowed is pic 9(4));
    #                  arith overflow
    ##expectfile ${test_dir}/n01exp n01s31
    stmt = """UPDATE keytabf SET col_bin_16 = 987654321 WHERE col_bin_16 = 999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    #  column value == key seq table; new value longer than original;
    #                  update binary-16 field with binary-32 number;
    #                  number larger than 2**16; (max value
    #                  allowed is pic 9(4)); arith overflow
    ##expectfile ${test_dir}/n01exp n01s32
    stmt = """UPDATE keytabf SET col_bin_16 = 65537 WHERE col_bin_16 = 999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    #  column value == key seq table; new value longer than original;
    #                  update binary-64 field with > binary-64 number
    #                  (max value allowed is pic 9(18)); number too large
    ##expectfile ${test_dir}/n01exp n01s33
    stmt = """UPDATE keytabf SET col_bin_64 = 9876543219876543219
WHERE col_bin_16 = 977;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    #  column value == key seq table; new value longer than original;
    #                  update binary-64 field with > binary-64 number;
    #                  number larger than 2**64; (max value allowed is
    #                  pic 9(18)); number too large
    ##expectfile ${test_dir}/n01exp n01s34
    stmt = """UPDATE keytabf SET col_bin_64 = 9223372036854775808
WHERE col_bin_16 = 977;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    #  column value == relative table; new value longer than original;
    #                  update binary-16 field with binary-32 number
    #                  (max value allowed is pic 9(4)); arith overflow
    ##expectfile ${test_dir}/n01exp n01s35
    stmt = """UPDATE reltabc SET col_bin_16 = 987654321 WHERE col_bin_16 = 999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    #  column value == relative table; new value longer than original;
    #                  update binary-64 field with > binary-64 number
    #                  (max value allowed is pic 9(18)); number too large
    ##expectfile ${test_dir}/n01exp n01s36
    stmt = """UPDATE reltabc SET col_bin_64 = 9876543219876543219
WHERE col_bin_16 = 977;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    #  column value == relative table; new value longer than original;
    #                  update binary-16 field with binary-32 number;
    #                  number larger than 2**16; (max value
    #                  allowed is pic 9(4)); arith overflow
    ##expectfile ${test_dir}/n01exp n01s37
    stmt = """UPDATE reltabc SET col_bin_16 = 65537 WHERE col_bin_16 = 999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    #  column value == relative table; new value longer than original;
    #                  update binary-64 field with > binary-64 number;
    #                  number larger than 2**64; (max value allowed is
    #                  pic 9(18)); number too large
    ##expectfile ${test_dir}/n01exp n01s38
    stmt = """UPDATE reltabc SET col_bin_64 = 9223372036854775808
WHERE col_bin_16 = 977;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    #  column value == entry seq table; new value longer than original;
    #                  update binary-16 field with binary-32 number
    #                  (max value allowed is pic 9(4)); arith overflow
    ##expectfile ${test_dir}/n01exp n01s39
    stmt = """UPDATE enttaba SET col_bin_16 = 987654321 WHERE col_bin_16 = 999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    #  column value == entry seq table; new value longer than original;
    #                  update binary-64 field with > binary-64 number
    #                  (max value allowed is pic 9(18)); number too large
    ##expectfile ${test_dir}/n01exp n01s40
    stmt = """UPDATE enttaba SET col_bin_64 = 9876543219876543219
WHERE col_bin_16 = 977;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    #  column value == entry seq table; new value longer than original;
    #                  update binary-16 field with binary-32 number;
    #                  number larger than 2**16; (max value
    #                  allowed is pic 9(4)); arith overflow
    ##expectfile ${test_dir}/n01exp n01s41
    stmt = """UPDATE enttaba SET col_bin_16 = 65537 WHERE col_bin_16 = 999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    #  column value == relative table; new value longer than original;
    #                  update binary-64 field with > binary-64 number;
    #                  number larger than 2**64; (max value allowed is
    #                  pic 9(18)); number too large
    ##expectfile ${test_dir}/n01exp n01s42
    stmt = """UPDATE enttaba SET col_bin_64 = 9223372036854775808
WHERE col_bin_16 = 977;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    #  column value == entry seq table; 2 column sizes increase so total
    #                  record length increases
    stmt = """UPDATE enttaba SET col_varchar_3 = 'pqrs', col_varchar_4 = 'stuvw'
WHERE col_bin_16 = 966;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    
    # column value == entry seq table; 2 column sizes decrease so total
    #                 record length decreases
    stmt = """UPDATE enttaba SET col_varchar_4 = 'c', col_varchar_5 = 'ef'
WHERE col_bin_16 = 955;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    # column value == entry seq table; 2 column sizes change, 1 increases
    #                 and one decreases, so total record length decreases
    stmt = """UPDATE enttaba SET col_varchar_5 = 'mnopq', col_varchar_4 = 'l'
WHERE col_bin_16 = 944;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    # column value == entry seq table; 2 column sizes change, 1 increases
    #                 and one decreases, so total record length increases
    stmt = """UPDATE enttaba SET col_varchar_5 = 'gh', col_varchar_3 = 'cde'
WHERE col_bin_16 = 922;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    # column value == entry seq table; varchar field size increases
    stmt = """UPDATE enttaba SET col_varchar_3 = 'ijk' WHERE col_bin_16 = 911;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    #  column value == new column value violates data type of column;
    #                  column defined as char 3
    stmt = """UPDATE enttabb SET col_1 = 123 WHERE col_1 = 'abc';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4039')
    
    #  column value == new column value violates data type of column;
    #                  column defined as pic x(3)
    stmt = """UPDATE enttabb SET col_2 = 987 WHERE col_2 = 'def';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4039')
    
    #  column value == new column value violates data type of column;
    #                  column defined as binary 16 signed
    ##expectfile ${test_dir}/n01exp n01s46
    stmt = """UPDATE enttabb SET col_3 = 9876543 WHERE col_3 = -1234;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    #  column value == new column value violates data type of column;
    #                  column defined as binary 16 unsigned
    ##expectfile ${test_dir}/n01exp n01s47
    stmt = """UPDATE enttabb SET col_4 = -9876 WHERE col_4 = 1234;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8432')
    
    #  column value == new column value violates data type of column;
    #                  column defined as binary 32 signed
    stmt = """UPDATE enttabb SET col_5 = 'abcd' WHERE col_5 = -123456789;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4039')
    
    #  column value == new column value violates data type of column;
    #                  column defined as binary 32 unsigned
    ##expectfile ${test_dir}/n01exp n01s49
    stmt = """UPDATE enttabb SET col_6 = -98765432109 WHERE col_6 = 123456789;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8432')
    
    # column value == new column value violates data type of column;
    #                 column defined as binary 64 signed
    stmt = """UPDATE enttabb 
SET col_7 = 987654321098765432109 WHERE col_7 = -123456789123456789;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 0)
    
    #  column value == new column value violates data type of column;
    #                  column defined as binary 64 unsigned
    stmt = """UPDATE enttabb 
SET col_8 = 'abcd' WHERE col_8 = 12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4039')
    
    #  column value == new column value violates data type of column;
    #                  column defined as pic s9(2) comp
    ##expectfile ${test_dir}/n01exp n01s51
    stmt = """UPDATE enttabb SET col_9 = 32770 WHERE col_9 = -100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    #  column value == new column value violates data type of column;
    #                  column defined as smallint signed
    stmt = """UPDATE enttabb SET col_10 = 'abc' WHERE col_10 = 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4039')
    
    #  column value == new column value violates data type of column;
    #                  column defined as smallint unsigned
    ##expectfile ${test_dir}/n01exp n01s53
    stmt = """UPDATE enttabb SET col_11 = 4294967299 WHERE col_11 = -1000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    #  column value == new column value violates data type of column;
    #                  column defined as integer signed
    ##expectfile ${test_dir}/n01exp n01s54
    stmt = """UPDATE enttabb SET col_12 = -1000 WHERE col_12 = 1000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8432')
    
    #  column value == new column value violates data type of column;
    #                  column defined as integer unsigned
    ##expectfile ${test_dir}/n01exp n01s55
    stmt = """UPDATE enttabb SET col_13 = 9223372036854775809 WHERE col_13 = -10000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    #  column value == new column value violates data type of column;
    #                  column defined as largeint signed
    stmt = """UPDATE enttabb SET col_14 = 'abc' WHERE col_14 = 10000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4039')
    
    #  column value == new column value violates data type of column;
    #                  column defined as largeint unsigned
    ##expectfile ${test_dir}/n01exp n01s57
    stmt = """UPDATE enttabb SET col_15 = -98765 WHERE col_15 = -123;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    #  column value == new column value violates data type of column;
    #                  column defined as decimal 3 signed
    stmt = """UPDATE enttabb SET col_16 = 'abc' WHERE col_16 = 123;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4039')
    
    #  column value == new column value violates data type of column;
    #                  column defined as decimal 3 unsigned
    stmt = """UPDATE enttabb SET col_17 = 'ABC' WHERE col_17 = 123;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4039')
    
    #  column value == new column value violates data type of column;
    #                  column defined as decimal 3 sign is leading embedded
    ##expectfile ${test_dir}/n01exp n01s60
    stmt = """UPDATE enttabb SET col_18 = -987 WHERE col_18 = 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    #  column value == new column value violates data type of column;
    #                  column defined as pic s9 display
    stmt = """UPDATE enttabb SET col_19 = 'abcd' WHERE col_19 = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4039')
    
    #  column value == new column value violates data type of column;
    #                  column defined as pic s9 display sign is leading
    #                  embedded
    ##expectfile ${test_dir}/n01exp n01s62
    stmt = """UPDATE enttabb SET col_20 = -987 WHERE col_20 = 1.23;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8432')
    
    #  shorthand view == update a shorthand view against a single base table
    stmt = """UPDATE stab1 SET col_4 = 99999 WHERE col_1 = 'xy';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    #  shorthand view == update a shorthand view that is a join
    stmt = """UPDATE sview2 SET col_1 = 'xyz' WHERE col_1 = 'abc';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4028')
    
    # protection view == update a view so that the new record violates an
    #                    assertion on the base table
    stmt = """UPDATE pview3 SET col_4 = 0.00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 0)
    
    #  protection view == update the primary key field of the base table
    #                     through a protection view that contains that field
    stmt = """UPDATE pview4 SET col_2 = 'abcdefg' WHERE col_1 = 'stu';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4033')
    
    #  protection view == update a unique index on the base table through
    #                     a protection view that contains that field and
    
    #                     update it to contain a duplicate value
    ##expectfile ${test_dir}/n01exp n01s66
    stmt = """UPDATE pview5 SET col_2 = 'v' WHERE col_1 = 'qpo';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    
    # protection view == update a column of the view so that the row will
    #                    violate the view predicate
    ##expect any *--- 0 row(s) updated.*
    stmt = """UPDATE pview6 SET col_2 = 7 WHERE col_1 = 'ab';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01exp""", 'n01s66a')
    
    #  protection view == update a column of the view so that several rows
    #                     will violate the view predicate; some will be
    #                     updated and some will not
    ##expectfile ${test_dir}/n01exp n01s67
    stmt = """UPDATE pview6 SET col_2 = col_2 + 1 WHERE col_2 BETWEEN 2 and 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8105')
    
    #  protection view == update a column of a table so that several rows
    #                     will be selected but one will violate an assertion
    #                     on the table; some rows will be updated and some
    #                     will not
    ##expectfile ${test_dir}/n01exp n01s68
    stmt = """UPDATE reltabb SET col_3 = col_3 * 3 WHERE col_1 = 'XR';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')
    
    # update table with no search condition supplied (all rows of the
    #        table will be updated)
    stmt = """UPDATE keytabd SET col_4 = col_4 - 1 stable access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 6)
    
    # update varchar columns in entry seq table with two columns changing
    #        (one value is larger and one value is shorter) but the
    #        overall record size remains the same
    stmt = """UPDATE enttaba SET col_varchar_4 = 'axyz', col_varchar_5 = 'onm'
WHERE col_varchar_3 = 'gh' repeatable access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    # update varchar columns in entry seq table with three columns changing
    #        but the overall record size remains the same
    stmt = """UPDATE enttaba SET col_varchar_3 = 'ijk', col_varchar_4 = 'l',
col_varchar_5 = 'qrstu'
WHERE col_varchar_3 = 'ij' stable access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 0)
    
    #  update rows of relative table using an aggregate in the WHERE clause
    #         of the subquery
    stmt = """UPDATE reltaba SET col_2 = 99 WHERE col_2 <
(SELECT col_2 FROM keytaba WHERE col_2 < AVG(col_2)) repeatable access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4015')
    
    #  update rows of key sequenced table using ORDER BY in the SELECT
    #         clause
    #  ORDER BY has no effect on the subquery (SQLCI reference manual 6-6)
    #    SQL normalizer has ignored it since C30.S04 == no error message.
    #    So the following statement is commented out. BH 9/5/91
    #  UPDATE .keytabc SET col_2 = 'updated' WHERE col_1 IN
    #      (SELECT DISTINCT col_1 FROM .keytabb ORDER BY col_2)
    #       stable access;
    
    #    ===========================
    #     secure tables and views
    #     needed for security
    #     tests.
    #    ===========================
    
    #   secure table keytaba so other user has read authority but not write
    stmt = """ALTER TABLE keytaba SECURE 'nocc';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #   The following line produces an error message.
    #
    #   secure table keytabb so other user has write authority but not read
    stmt = """ALTER TABLE keytabb SECURE 'oncc';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #   secure view pview3 so other user has read authority but not write
    stmt = """ALTER VIEW pview3 SECURE 'nonn';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #   The following line produces an error message.
    #
    #   secure view pview4 so other user has write authority but not read
    stmt = """ALTER TABLE pview4 SECURE 'oncc';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # 01/22/98 EL
    stmt = """drop view pview3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view pview4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view pview5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view pview6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view pview7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view sview2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view vtab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view vtab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view stab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view tab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """DROP TABLE keytaba;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE keytabb;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE keytabc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE keytabd;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE keytabe;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE keytabf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """DROP TABLE reltaba;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE reltabb;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE reltabc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """DROP TABLE enttaba;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE enttabb;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """DROP TABLE altable;"""
    output = _dci.cmdexec(stmt)
    
    #        End of test case ARKT0031
    _testmgr.testcase_end(desc)

