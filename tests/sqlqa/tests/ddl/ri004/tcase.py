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

import time
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


#  --------------------------------------------------------------
#testcase a001  avg() stddev() variance() indirect group by
#  DESCRIPTION_BEGIN
#  MAP:{5.1.6.02}
#  DESCRIPTION_END
# ***************************************************************************
#testcase #testcase a001  avg() stddev() variance() indirect group by
# ***************************************************************************
def test001(desc="""testcase a001  avg() stddev() variance() indirect group by"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #  cleanup
    stmt = """drop table a001_f1 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a001_d2 cascade;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table a001_d2 (
  d2_pk int not null
, d2_c1 int not null
, d2_v1 int not null
, d2_v2 int        
, primary key(d2_pk)
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table a001_f1 (
  f_pk int not null
, f_d2_fk int 
, f_v1 int not null
, f_v2 int 
, primary key(f_pk)
, foreign key(f_d2_fk) references a001_d2
    on delete cascade
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'ERROR')

    stmt = """create table a001_f1 (
  f_pk int not null
, f_d2_fk int 
, f_v1 int not null
, f_v2 int 
, primary key(f_pk)
, foreign key(f_d2_fk) references a001_d2
    -- on delete cascade
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into a001_d2 values
 (1,1,1,1)
,(2,1,1,2)
,(3,2,2,null)
,(4,2,2,1)
,(5,3,3,2)
,(6,3,3,null)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 6)  

    stmt = """insert into a001_f1 values
 (1,1,10,10)
,(2,2,10,10)
,(3,3,10,null)
,(4,4,20,20)
,(5,5,20,20)
,(6,6,20,null)
,(7,1,30,30)
,(8,2,30,30)
,(9,3,30,null)
,(10,4,40,40)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 10)
    
    stmt = """delete from a001_f1 where f_pk = 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
     
    stmt = """delete from a001_f1 where f_d2_fk = 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """delete from a001_f1 where f_d2_fk = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    
    stmt = """delete from a001_d2 where d2_pk = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """delete from a001_d2 where d2_pk = 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'8103')
    
    stmt = """select * from a001_f1 order by 1,2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", 's1')
    
    stmt = """select * from a001_d2 order by 1,2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", 's2')
    
    #  cleanup
    stmt = """drop table a001_f1 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a001_d2 cascade;"""
    output = _dci.cmdexec(stmt)  
    
    _testmgr.testcase_end(desc)
#  --------------------------------------------------------------
#  Indirect Group By.
#  --------------------------------------------------------------
#testcase a002 Indirect Group By
#  DESCRIPTION_BEGIN
#  MAP:{5.1.6.01,5.1.6.02}
#  Join b/n one fact table and two dimensional tables.
#  There is MAV on the fact table.
#  Assume MAV gets scanned instead of the fact table.
#  Fact-Dim1-Dim2
#  DESCRIPTION_END
def test002(desc="""a002 Indirect Group By"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    

    #expect purge immediate
    #sh testid=a002
    # --#process mxci_ct
    #  cleanup
    stmt = """drop table a002_f_sale cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a002_d_time cascade;"""
    output = _dci.cmdexec(stmt)  
    stmt = """drop table a002_d_prod cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a002_d_store cascade;"""
    output = _dci.cmdexec(stmt)  
    stmt = """drop table a002_d_region cascade;"""
    output = _dci.cmdexec(stmt)

    #sh rm -rf  ${work_dir}/a002.*
    stmt = """create table a002_d_time (
  d_time_pk int not null
, d_time_mo int not null
, d_time_qt int not null
, d_time_yr int not null
, primary key(d_time_pk)
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table a002_d_prod (
  d_prod_pk int not null
, d_prod_desc char(10) not null
, d_prod_category char(10) not null
, d_prod_price real not null
, primary key(d_prod_pk)
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table a002_d_region (
  d_region_pk int not null
, d_region_desc char(2) not null
, primary key(d_region_pk)
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table a002_d_store (
  d_store_pk int not null
, d_store_name char(10) not null
, d_store_city char(10) not null
, d_store_state char(2) not null
, d_store_region int not null
, primary key(d_store_pk)
, foreign key(d_store_region) references a002_d_region
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table a002_f_sale (
  f_sale_pk int not null
, f_sale_time int not null
, f_sale_prod int not null
, f_sale_store int not null
, f_sale_qty int not null
, primary key(f_sale_pk)
, foreign key(f_sale_time) references a002_d_time
, foreign key(f_sale_prod) references a002_d_prod
, foreign key(f_sale_store) references a002_d_store
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a002_d_time values
 (1,1,1,2009)
,(2,2,1,2009)
,(3,3,1,2009)
,(4,4,2,2009)
,(5,5,2,2009)
,(6,6,2,2009)
,(7,7,3,2009)
,(8,8,3,2009)
,(9,9,3,2009)
,(10,10,4,2009)
,(11,11,4,2009)
,(12,12,4,2009)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 12)    

    stmt = """insert into a002_d_prod values
 (1,'prod01','p1',1.25)
,(2,'prod02','p1',1.50)
,(3,'prod03','p1',1.75)
,(4,'prod04','p1',2)
,(5,'prod01','p2',100)
,(6,'prod02','p2',200)
,(7,'prod03','p2',300)
,(8,'prod01','p3',1000)
,(9,'prod02','p3',1500)
,(10,'prod01','p4',5000)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 10)

#expect any * 3 row(s) inserted.
    stmt = """insert into a002_d_region values
 (1,'ce')
,(2,'we')
,(3,'ea')
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)
    
    stmt = """insert into a002_d_store values
 (1,'store01','austin','tx',1)
,(2,'store02','dallas','tx',1)
,(3,'store03','la','ca',2)
,(4,'store04','ny','ny',3)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 4)
    
    stmt = """insert into a002_f_sale 
select c1*10+c2
      ,mod(c1*10+c2,12)+1
      ,mod(c1*10+c2,10)+1
      ,mod(c1*10+c2,4)+1
      ,mod(c1*10+c2,7)
from (values(1)) t
transpose 1,2,3,4,5,6,7,8,9,10 as c1
transpose 1,2,3,4,5,6,7,8,9,10 as c2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 100)
    
    stmt = """insert into a002_d_region values (4,'ca');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a002_d_region values (5,'wa');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output) 

    stmt = """insert into a002_f_sale values (9,13,11,5,9);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8103')

    stmt = """insert into a002_d_prod values (11,'prod05','p5',500);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into a002_d_store values (5,'store05','wa','wa',2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output) 

    stmt = """insert into a002_d_time values (13,13,5,2009);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """insert into a002_f_sale values (9,13,11,5,9);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output) 
    
    stmt = """select * from a002_f_sale where f_sale_pk < 11 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002exp""", 's1')
    
    stmt = """select * from a002_d_time order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002exp""", 's2')
    
    stmt = """select * from a002_d_prod order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002exp""", 's3')
    
    stmt = """select * from a002_d_region order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002exp""", 's4')    
    
    #  cleanup
    stmt = """drop table a002_f_sale cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a002_d_time cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a002_d_prod cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a002_d_store cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a002_d_region cascade;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)
#  --------------------------------------------------------------
#testcase a003 Indirect Group By key and non-key col join
#  DESCRIPTION_BEGIN
#  MAP:{5.1.6.01,5.1.6.02}
#  Key col join and non-key col joins.
#  Various aggregate functions.
#  DESCRIPTION_END
def test003(desc="""a003 Indirect Group By key and non-key col join"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    #expect purge immediate
    #sh testid=a003
    # #process mxci_ct
    #  cleanup
    
    stmt = """drop table a003_f1 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a003_f2 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a003_d1 cascade;"""
    output = _dci.cmdexec(stmt)
    
    #sh rm -rf  ${work_dir}/a003.*
    stmt = """create table a003_d1 (
  d_pk int not null  -- distinct key col
, d_c1 int not null  -- col with duplicates
, d_v1 int not null  -- not null data column
, d_v2 int           -- nullable data column
, primary key(d_pk)
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  this will reference to key column d1(d_pk)
    stmt = """create table a003_f1 (
  f_pk int not null
, f_d1_d_pk int 
, f_v1 int not null
, f_v2 int 
, primary key(f_pk)
, foreign key(f_d1_d_pk) references a003_d1
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  this will reference to non-key column d1(d_c1)
    stmt = """create table a003_f2 (
  f_pk int not null
, f_d1_d_c1 int 
, f_v1 int not null
, f_v2 int 
, primary key(f_pk)
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into a003_d1 values
 (1,1,1,1)
,(2,1,1,2)
,(3,2,2,null)
,(4,2,2,1)
,(5,3,3,2)
,(6,3,3,null)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 6)
    
    stmt = """update a003_d1 set d_v2 = d_pk, d_v1 = d_c1;"""
    output = _dci.cmdexec(stmt)
    stmt = """update a003_f1 set f_v2 = f_pk, f_v1 = f_d1_d_pk;"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into a003_f1 values
 (1,1,10,10)
,(2,2,10,10)
,(3,3,10,null)
,(4,4,20,20)
,(5,5,20,20)
,(6,6,20,null)
,(7,1,30,30)
,(8,2,30,30)
,(9,3,30,null)
,(10,4,40,40)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 10)
    
    stmt = """update a003_f1 set f_v2 = f_pk, f_v1 = f_d1_d_pk;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into a003_f2 values
 (1,1,10,10)
,(2,1,10,10)
,(3,2,10,null)
,(4,2,20,20)
,(5,2,20,20)
,(6,3,20,null)
,(7,3,30,30)
,(8,3,30,30)
,(9,3,30,null)
,(10,1,40,40)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 10)
    
    stmt = """select * from a003_f1 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003exp""", 's1')
    
    stmt = """select * from a003_f2 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003exp""", 's2')
    
    stmt = """select * from a003_d1 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003exp""", 's3')
    
    #  cleanup
    stmt = """drop table a003_f1 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a003_f2 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a003_d1 cascade;"""
    output = _dci.cmdexec(stmt)
        
    _testmgr.testcase_end(desc)
#  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#testcase a004 indirect group by with extra query tables
#  DESCRIPTION_BEGIN
#  MAP:{5.1.6.02}
#  Join b/n one fact table and two dimensional tables.
#  MAV on fact table points to key col of one dim table.
#  DESCRIPTION_END
def test004(desc="""a004 indirect group by with extra query tables"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #expect purge immediate
    #sh testid=a004
    # #process mxci_ct
    #  cleanup
    stmt = """drop table a004_f1 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a004_d1 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a004_d2 cascade;"""
    output = _dci.cmdexec(stmt)
    
    #sh rm -rf  ${work_dir}/a004.*
    stmt = """create table a004_d1 (
  d1_pk int not null  --  distinct key col
, d1_c1 int not null  --  col with duplicates
, d1_v1 int not null  --  not null data column
, d1_v2 int           --  nullable data column
, primary key(d1_pk)
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table a004_d2 (
  d2_pk int not null  --  distinct key col
, d2_c1 int not null  --  col with duplicates
, d2_v1 int not null  --  not null data column
, d2_v2 int           --  nullable data column
, primary key(d2_pk)
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table a004_f1 (
  f_pk int not null
, f_d1_pk int 
, f_d2_pk int 
, f_v1 int not null
, f_v2 int 
, primary key(f_pk)
, foreign key(f_d1_pk) references a004_d1
, foreign key(f_d2_pk) references a004_d2
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a004_f1 values
 (1,1,1,10,10)
,(2,2,2,10,10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'8103')
    
    stmt = """insert into a004_d1 values
 (1,1,1,1)
,(2,1,1,2)
,(3,2,2,null)
,(4,2,2,1)
,(5,3,3,2)
,(6,3,3,null)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 6) 
    
    stmt = """insert into a004_d2 values
 (1,1,1,1)
,(2,1,1,2)
,(3,2,2,null)
,(4,2,2,1)
,(5,3,3,2)
,(6,3,3,null)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 6) 
    
    stmt = """insert into a004_f1 values
 (1,1,1,10,10)
,(2,2,2,10,10)
,(3,3,3,10,null)
,(4,4,4,20,20)
,(5,5,5,20,20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    stmt = """select * from a004_f1 order by 1,2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a004exp""", 's1')
    
    stmt = """select * from a004_d1 order by 1,2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a004exp""", 's2')
    
    stmt = """select * from a004_d2 order by 1,2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a004exp""", 's3')
    # 
    #  cleanup
    # 
    stmt = """drop table a004_f1 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a004_d1 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a004_d2 cascade;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

    # *******************************************************************************