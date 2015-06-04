# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2015 Hewlett-Packard Development Company, L.P.
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

    stmt = """create table neoemp 
(
Num           integer unsigned no default  not null not droppable ,
LastName      char(24)         no default  not null not droppable ,
FirstName     char(14)         no default  not null not droppable ,
MiddleInitial char             no default  not null not droppable ,
Sex           char             no default  not null not droppable ,
WorkGroupNum  integer unsigned no default  not null not droppable ,
PayGrade      integer unsigned no default  not null not droppable ,
AnnualSalary  integer unsigned no default  not null not droppable ,
DateOfBirth   date             no default  not null not droppable ,
primary key ( Num ) not droppable
)
store by primary key ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into neoemp values
(1,'Anderson','Alvin','A','M',1,1,21,DATE '12/08/1941'),
(2,'Anderson','Anna ','A','F',1,2,22,DATE '12/10/1942'),
(3,'Anderson','Aloysius','A','M',1,3,23,DATE '11/07/1943'),
(4, 'Anderson','Abby ','A','F',1,4,24 ,DATE '08/15/1947'),
(5,'Anderson','Alan ','A','M',1,5,25, DATE '12/07/1961'),
(6,'Anderson','Anne ','A','F',1,6,26,DATE '12/07/1972'),
(7,'Anderson','Abelard','A','M',1,7,27,DATE '12/07/1965'),
(8,'Anderson','Alice','A','F',1,8,28,DATE '12/07/1932'),
(9,'Anderson','Anton','A','M',1,9,29,DATE '12/07/1918'),
(10,'Anderson','Alicia ','A','F',1,10,30,DATE '12/07/1954'),
(11,'Anderson','Abe','A','M',2,1,21,DATE '12/07/1912'),
(12,'Anderson','Amanda ','A','F',2,2,22,DATE '12/07/1913'),
(13,'Anderson','Andrew ','A','M',2,3,23,DATE '12/07/1975'),
(14,'Anderson','Annette','A','F',2,4,24,DATE '12/07/1976'),
(15,'Anderson','Akihiro','A','M',2,5,25,DATE '09/06/1977'),
(16,'Anderson','Andrea ','A','F',2,6,26,DATE '12/05/1978'),
(17,'Anderson','Arthur ','A','M',2,7,27,DATE '12/04/1979'),
(18,'Anderson','Amy  ','A','F',2,8,28,DATE '12/07/1951'),
(19,'Anderson','Arnold ','A','M',2,9,29,DATE '12/21/1957'),
(20,'Anderson','Adriana','A','F',2,10,30,DATE '12/17/1967'),
(21,'Anderson','Arturo ','A','M',3,1,21,DATE '12/27/1990'),
(22,'Anderson','Annabelle','A','F',3,2,22,DATE '12/09/1992'),
(23,'Anderson','Andreas','A','M',3,3,23,DATE '12/12/1995'),
(24,'Anderson','Becky','A','F',3,4,24,DATE '12/01/2001'),
(25,'Anderson','Bill ','A','M',3,5,25,DATE '12/02/2002'),
(26,'Anderson','Betsy','A','F',3,6,26,DATE '12/03/1998'),
(27,'Anderson','Bob  ','A','M',3,7,27,DATE '11/04/1998'),
(28,'Anderson','Belinda','A','F',3,8,28,DATE '09/07/1998'),
(29,'Anderson','Bruce','A','M',3,9,29,DATE '11/30/1997'),
(30,'Anderson','Bridget','A','F',3,10,30,DATE '12/07/1966');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 30)

    stmt = """CREATE TABLE d2 (
i1 NUMERIC (9,0) NOT NULL NOT DROPPABLE
, i2 PIC S9(4) CONSTRAINT """ + defs.w_schema + """_i200446Fht7ijkR NOT NULL NOT DROPPABLE
, i3 DECIMAL (9,0) DEFAULT 23
, CONSTRAINT """ + defs.w_schema + """_d2C25 primary key (i2 DESC) NOT DROPPABLE
)    
ATTRIBUTE MAXEXTENTS 719 AUDITCOMPRESS EXTENT (396, 127) BLOCKSIZE 4096
store by (i2 DESC);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """INSERT INTO d2 VALUES
(-65, 799, -50251822),
(-163, 802, -50251814),
(346, 805, -50251806),
(434334, 280, -0251806),
(6786734, 380, -15025186),
(687834, 480, -25025186),
(878434, 580, -35025186),
(5346434, 680, -45025186),
(8678636, 780,  -55025186),
(089746, 880, -65025186),
(646546, 980, -75025186),
(43346, 800, -850251806),
(6576346, 108, -950251806);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 13)
    
    stmt = """create table ee1 
(
Num           integer unsigned no default  not null not droppable ,
LastName      char(24)         ,
FirstName     char(14)         ,
Gender        char             ,
DeptNum       integer unsigned ,
PayGrade      integer unsigned ,
Salary        numeric(9,2)     ,
Bonus         decimal(9,2)     ,
Commision     pic s9(9)v9(2) comp,
DateOfBirth   date             ,
primary key ( Num ) not droppable
)
attribute
extent (1024, 1024),
maxextents 16
store by primary key ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table workgroup 
(
Num           integer unsigned no default  not null not droppable ,
WorkGrpName   char(24)         ,
DeptNum       integer unsigned ,
primary key ( Num ) not droppable
)
store by primary key ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table insurance 
(
Num           integer unsigned no default  not null not droppable ,
PolicyNum     integer unsigned ,
InsName       char(30)         ,
Coverage      largeint         ,
Deductible    decimal(10,6)                                       ,
CoPayment     numeric(5,2)                                        ,
Status        char             ,
primary key (Num) )
attribute
extent (1024, 1024),
maxextents 16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into ee1 values
(1,'Zacker','Abe','M',1,1, 12000.00,1800.00,200.00,date '1941-12-07'),
(2,'Andersen','Abby','F',9,1, 12100.00,1838.00,210.00,date '1942-11-07'),
(3,'Quan','Abe','M',2,7, 12200.00,NULL,1645,date '1943-12-09'),
(4,'Yang','Arnold','M',3,1, 12300.00,1510.00,173.00,date '1944-10-07'),
(5,'Richarson','Becky','F',9,2, 15000.00,7540.00,220,date '1945-12-09'),
(6,'Li','Arthur','M',2,3, 18000.00,1530.00,150.00,date '1946-12-08'),
(7,'Sharma','Arthur','M',5,3, 18100.00,3200.00,1500.00,date '1947-12-08'),
(8,'Li','Amy','F',2,3, 18200.00,3000.00,1540.00,date '1948-12-07'),
(9,'Martinez','Annette','F',6,4, 24100.00,2300.00,500.00,date '1949-12-09'),
(10,'Zhang','Abby','F',3,4, 24200.00,2005.00,530.00,date '1950-12-07'),
(11,'Yurgu','Becky','F',3,5, 24300.00,NULL,NULL,date '1951-12-07'),
(12,'Kankark','Bill','M',9,4, 24400.00,1810.00,540.00,date '1952-12-07'),
(13,'Wilbert','Aloysius','M',1,6, 72100.00,1270.00,240.00,date '1953-12-08'),
(14,'Nelluru','Bruce','M',9,7, 90100.00,1890.00,550.00,date '1954-12-09'),
(15,'Therber','Arnold','M',2,7, 90200.00,1100.00,225,date '1955-12-09'),
(16,'Andersen','Bruce','M',5,7, 90300.00,3200.00,2520,date '1956-12-07'),
(17,'Cate','Becky','F',9,7, 90400.00,5875.00,2018.00,date '1957-12-08'),
(18,'Linville','Bruce','M',1,8, 92100.00,1235.00,1600.00,date '1958-12-09'),
(19,'Zacker','Bill','M',5,5, 30100.00,NULL,9239.00,date '1959-12-08'),
(20,'Buick','Bridget','F',3,5, 30200.00,1532.00,NULL,date '1960-12-08');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 20)
    
    stmt = """insert into workgroup values
(1,'WG00001',1),
(2,'WG00002',1),
(3,'WG00003',1),
(4,'WG00004',1),
(5,'WG00005',1),
(6,'WG00006',1),
(7,'WG00007',1),
(8,'WG00008',1),
(9,'WG00009',1),
(10,'WG00010',1),
(11,'WG00011',2),
(12,'WG00012',2),
(13,'WG00013',2),
(14,'WG00014',2),
(15,'WG00015',2),
(16,'WG00016',2),
(17,'WG00017',2),
(18,'WG00018',2),
(19,'WG00019',2),
(20,'WG00020',2),
(21,'WG00021',3),
(22,'WG00022',3),
(23,'WG00023',3),
(24,'WG00024',3),
(25,'WG00025',3),
(26,'WG00026',3),
(27,'WG00027',3),
(28,'WG00028',3),
(29,'WG00029',3),
(30,'WG00030',3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 30)
    
    stmt = """insert into insurance values
(1,1343290,'BlueCross', 500000, 1000.323, 50.50,'I'),
(2,2392093,'Kaiser', 200000, 403.2330, 89.50,'A'),
(3,3199382,'BlueShield', 200000, 6003.893,50.50,'A'),
(4,4199933,'Kaiser', 34000, 1032.2320,50.50,'A'),
(5,5118983,'Kaiser', 332000, 1102.2320, 40.55,'A'),
(6,6175988,'BlueCross', 340000, 120.8900, 40.40,'A'),
(7,7192137,'Kaiser', 35500, 1040.82039, 25.25,'A'),
(8,8193128,'Kaiser', 31200, 115.1300, 50.00,'A'),
(9,9191755,'BlueCross', 12000, 522.40, 30.50,'A'),
(10,9111603,'Kaiser', 34000, 1502.890, 44.33,'I'),
(11,1307090,'BlueCross', 500000, 1002.530, 25.25,'I'),
(12,2352393,'Kaiser', 200000, 4003.98, 50.50,'A'),
(13,5119382,'BlueShield', 200000, 6009.43, 60.60,'A'),
(14,3191933,'Kaiser', 34000, 1006.758, 45.45,'A'),
(15,9114293,'Kaiser', 332000, 1106.2320, 35.35,'A'),
(16,3174293,'BlueCross', 340000, 1200.928, 55.55,'A'),
(17,7212437,'Kaiser', 35500, 1040.8902, 45.55,'A'),
(18,3193156,'Kaiser', 31200, 310.938, 50.50,'A'),
(19,9974293,'BlueCross', 340000, 1200.928, 55.55,'A'),
(20,3110902,'Kaiser', 34000, 1500.0092, 35.35,'I'),
(21,4323090,'BlueCross', 500000, 2000.532, 44.33,'I'),
(22,9366393,'Kaiser', 200000, 4005.892, 89.50,'A'),
(23,4228882,'BlueShield', 200000, 6090.290, 30.50,'A'),
(24,2211933,'Kaiser', 34000, 2008.028, 50.50,'A'),
(25,8211993,'Kaiser', 332000, 2200.779, 35.35,'A'),
(26,6211993,'BlueCross', 340000, 334.500, 44.33,'A'),
(27,9328882,'BlueShield', 200000, 6090.290, 30.50,'A'),
(28,1293256,'Kaiser', 32200, 7893.54, 89.50,'A'),
(29,2552344,'BlueCross', 22000, 8793.55, 89.50,'A'),
(30,4233902,'Kaiser', 34000, 250.549, 895.50,'I');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 30)
    
    stmt = """select count(*) from ee1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '20')

    stmt = """select count(*) from workgroup;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '30')

    stmt = """select count(*) from insurance;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '30')

    stmt = """CREATE VIEW REVENUE (SUPPLIER_NO, TOTAL_REVENUE) AS
SELECT LINEITEM.L_SUPPKEY,
SUM(LINEITEM.L_EXTENDEDPRICE * (1 - LINEITEM.L_DISCOUNT))
FROM """ + gvars.g_schema_tpch2x + """.LINEITEM as LINEITEM WHERE
LINEITEM.L_SHIPDATE >= DATE '1993-02-01' AND
LINEITEM.L_SHIPDATE < DATE '1993-02-01' + INTERVAL '3' MONTH
GROUP BY LINEITEM.L_SUPPKEY ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

