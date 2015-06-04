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
    global testid
    global tblname

    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()

# -------------------------------------------------------------------------
#testcase a001 Columns specified in WHERE predicate - update
#  MAP: A001
#  WHERE clause condition allows the update request
#expect purge immediate
#sh testid=a001
#sh tblname=t_$testid
 
def test001(desc="""a001 Columns specified in WHERE predicate - update"""):
    global _testmgr
    global _testlist
    global _dci
    testid = """a001"""
    tblname = """t_""" + testid

    if not _testmgr.testcase_begin(_testlist): return
    

    
    stmt = """drop table """ + tblname +""" cascade;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table """ + tblname +"""b cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table """ + tblname +"""
(
  a1 int not null
 ,a2 int
 ,a3 int
 ,a4 int
 ,b1 int
 ,primary key(a1)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into """ + tblname +""" values 
 (1,1,1,1,1)
,(2,2,2,2,2)
,(3,3,3,3,3)
,(4,4,4,4,4)
,(5,null,null,null,null)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)

    stmt = """create table """ + tblname +"""b like """ + tblname +""";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into """ + tblname +"""b select * from """ + tblname +""";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)

    #  column from target table in WHERE clause
    #  should update the row
    stmt = """merge into """ + tblname +""" on a1=1
when matched then update set b1=-b1 
where a4=1
when not matched then insert values(20,20,20,20,20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v01')

    #  reset the table

    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    stmt = """select a1,b1 from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    
    #  debug:
    stmt = """select * from """ + tblname +"""b;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from """ + tblname +""";"""
    output = _dci.cmdexec(stmt)
    
    #  column from source table in WHERE clause
    stmt = """merge into """ + tblname +"""
using  (
  select a2
  from """ + tblname +"""b
) as t2(a2)
on a1=t2.a2
when matched then update set b1=-b1 
where a2=2
when not matched then insert values(20,20,20,20,20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v02')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    stmt = """select a1,b1 from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)

    #  columns from both source and target table in WHERE clause
    stmt = """merge into """ + tblname +""" 
using  (
  select a4
  from """ + tblname +"""b
) as t2(a4)
on a1=3
when matched then update set b1=-b1 
where a4=t2.a4
when not matched then insert values(20,20,20,20,20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v03')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    stmt = """select a1,b1 from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    
    #  columns from both source and target table in WHERE clause
    #  with logical operator
    stmt = """merge into """ + tblname +""" 
using  (
  select a4
  from """ + tblname +"""b
) as t2(a4)
on a1=4
when matched then update set b1=-b1
where a4=t2.a4 and a3 > 0 and t2.a4 > 0
when not matched then insert values(20,20,20,20,20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v04')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    stmt = """select a1,b1 from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    
    #  no reference to either table
    stmt = """set param ?hv 5;"""
    output = _dci.cmdexec(stmt)

    stmt = """merge into """ + tblname +""" 
using  (
  select a4
  from """ + tblname +"""b
) as t2(a4)
on a1=4
when matched then update set b1=-b1
where ?hv = 5
when not matched then insert values(20,20,20,20,20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v05')
    
    stmt = """drop table """ + tblname +""" cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table """ + tblname +"""b cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -
#testcase a002 Columns specified in WHERE predicate - reject
#  MAP: A001
#  WHERE clause condition rejects the update request
#expect purge immediate
#sh testid=a002
#sh tblname=t_$testid
 
def test002(desc="""a002 Columns specified in WHERE predicate - reject"""):
    global _testmgr
    global _testlist
    global _dci
    testid = """a002"""
    tblname = """t_""" + testid

    if not _testmgr.testcase_begin(_testlist): return

    stmt = """drop table """ + tblname +""" cascade;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table """ + tblname +"""b cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table """ + tblname +"""
(
  a1 int not null
 ,a2 int
 ,a3 int
 ,a4 int
 ,b1 int
 ,primary key(a1)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into """ + tblname +""" values 
 (1,1,1,1,1)
,(2,2,2,2,2)
,(3,3,3,3,3)
,(4,4,4,4,4)
,(5,null,null,null,null)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)

    stmt = """create table """ + tblname +"""b like """ + tblname +""";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into """ + tblname +"""b select * from """ + tblname +""";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)

    #  column from target table in WHERE clause
    #  should update the row
    stmt = """merge into """ + tblname +""" on a1=1
when matched then update set b1=-b1 
where a4=100
when not matched then insert values(20,20,20,20,20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v01')

    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)

    #  column from source table in WHERE clause
    stmt = """merge into """ + tblname +""" 
using  (
  select a2
  from """ + tblname +"""b
) as t2(a2)
on a1=t2.a2
when matched then update set b1=-b1 
where t2.a2 = 100
when not matched then insert values(20,20,20,20,20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v02')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a2>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)

    #  columns from both source and target table in WHERE clause
    stmt = """merge into """ + tblname +""" 
using  (
  select a2
  from """ + tblname +"""b
) as t2(a2)
on a1=3
when matched then update set b1=-b1 
where a4=t2.a2*100 
when not matched then insert values(20,20,20,20,20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v03')
    
    #  columns from both source and target table in WHERE clause
    #  with logical operator
    stmt = """merge into """ + tblname +""" 
using  (
  select a2
  from """ + tblname +"""b
) as t2(a2)
on a1=4
when matched then update set b1=-b1
where a4=t2.a2 and a3 > 0 and t2.a2 > 100
when not matched then insert values(20,20,20,20,20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v04')
    
    #  no reference to either table
    stmt = """set param ?hv 5;"""
    output = _dci.cmdexec(stmt)

    stmt = """merge into """ + tblname +""" 
using  (
  select a2
  from """ + tblname +"""b t2
) as t(a2)
on a1=4
when matched then update set b1=-b1
where ?hv = 100
when not matched then insert values(20,20,20,20,20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v05')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a2>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    #  debug:
    stmt = """select * from """ + tblname +"""b;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from """ + tblname +""";"""
    output = _dci.cmdexec(stmt)
    #  column from source table in WHERE clause
    stmt = """merge into """ + tblname +"""
using  (
  select a2
  from """ + tblname +"""b
) as t2(a2)
on a1=t2.a2
when matched then update set b1=-b1
where t2.a2 > 2
when not matched then insert values(20,20,20,20,20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v06')

    #  reset the table
    stmt = """delete from """ + tblname +""" where a2>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table """ + tblname +""" cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table """ + tblname +"""b cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)
    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -
#testcase a003 Key column in WHERE predicate
#  MAP: A002
#  Different types of key columns specified in WHERE clause
#expect purge immediate
#sh testid=a003
#sh tblname=t_$testid
 
def test003(desc="""a003 Key column in WHERE predicate"""):
    global _testmgr
    global _testlist
    global _dci
    testid = """a003"""
    tblname = """t_""" + testid

    if not _testmgr.testcase_begin(_testlist): return

    stmt = """drop table """ + tblname +""" cascade;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table """ + tblname +"""b cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table """ + tblname +"""c cascade;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table """ + tblname +"""d cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table """ + tblname +"""e cascade;"""
    output = _dci.cmdexec(stmt)
    
    # 
    #  primary key column
    # 
    stmt = """create table """ + tblname +"""
(
  a1 int not null
 ,a2 int
 ,a3 int
 ,a4 int
 ,b1 int
 ,primary key(a1)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into """ + tblname +""" values
 (1,1,1,1,1)
,(2,2,2,2,2)
,(3,3,3,3,3)
,(4,4,4,4,4)
,(5,null,null,null,null)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)

    stmt = """merge into """ + tblname +""" on a1=1
when matched then update set b1=-b1 
where a1 = 1
when not matched then insert values(20,20,20,20,20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
     
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v01')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a2>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    #  reject
    stmt = """merge into """ + tblname +""" on a1=1
when matched then update set b1=-b1
where a1 = 100
when not matched then insert values(20,20,20,20,20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
         
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v01a')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a2>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    # 
    #  clustering key column
    # 
    stmt = """create table """ + tblname +"""b
(
  a1 int not null
 ,a2 int
 ,a3 int
 ,a4 int
 ,b1 int
)
store by(a1)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into """ + tblname +"""b  values
 (1,1,1,1,1)
,(2,2,2,2,2)
,(3,3,3,3,3)
,(4,4,4,4,4)
,(5,null,null,null,null)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    stmt = """merge into """ + tblname +"""b on a1=1
when matched then update set b1=-b1
where a1 < 10
when not matched then insert values(20,20,20,20,20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3241')

    
    stmt = """select * from """ + tblname +"""b order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v02')

    #  reset the table
    stmt = """delete from """ + tblname +"""b  where a2>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +"""b  set b1=a1;"""
    output = _dci.cmdexec(stmt)

    #  #  reject
    stmt = """merge into """ + tblname +"""b on a1=1
when matched then update set b1=-b1
where a1 > 1
when not matched then insert values(20,20,20,20,20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3241')
    
    stmt = """select * from """ + tblname +"""b order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v02a')
    
    #  reset the table
    stmt = """delete from """ + tblname +"""b where a2>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +"""b set b1=a1;"""
    output = _dci.cmdexec(stmt)

    # 
    #  index key column
    # 
    stmt = """create table """ + tblname +"""c
(
  a1 int not null
 ,a2 int
 ,a3 int
 ,a4 int
 ,b1 int
 ,primary key(a1)
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index """ + tblname +"""c_idx1 on """ + tblname +"""c(a3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index """ + tblname +"""c_idx2 on """ + tblname +"""c(a4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into """ + tblname +"""c values
 (1,1,1,1,1)
,(2,2,2,2,2)
,(3,3,3,3,3)
,(4,4,4,4,4)
,(5,null,null,null,null)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    #  index key in where clause
    stmt = """prepare s from
merge into """ + tblname +"""c on a1=1
when matched then update set b1=-b1
where a3 = 1
when not matched then insert values(20,20,20,20,20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #  make sure index is used 
    # #expect any *index*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    stmt = """select * from """ + tblname +"""c order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v03')
    
    #  reset the table
    stmt = """delete from """ + tblname +"""c where a2>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +"""c set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    #  reject
    stmt = """merge into """ + tblname +"""c on a1=1
when matched then update set b1=-b1
where a3 < -1
when not matched then insert values(20,20,20,20,20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +"""c order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v03a')
    
    #  reset the table
    stmt = """delete from """ + tblname +"""c where a2>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +"""c set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    #  update index column
    stmt = """merge into """ + tblname +"""c on a1=1
when matched then update set a4=-a4
where a3 = 1
when not matched then insert values(20,20,20,20,20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +"""c order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v03b')
    
    #  reset the table
    stmt = """delete from """ + tblname +"""c where a2>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +"""c set a4=a1;"""
    output = _dci.cmdexec(stmt)
    
    # 
    #  non-key column
    # 
    stmt = """create table """ + tblname +"""d
(
  a1 int not null
 ,a2 int
 ,a3 int
 ,a4 int
 ,b1 int
 ,primary key(a1)
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into """ + tblname +"""d values
 (1,1,1,1,1)
,(2,2,2,2,2)
,(3,3,3,3,3)
,(4,4,4,4,4)
,(5,null,null,null,null)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    stmt = """merge into """ + tblname +"""d on a1=1
when matched then update set b1=-b1
where a3 > 0
when not matched then insert values(20,20,20,20,20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +"""d order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v04')
    
    #  reset the table
    stmt = """delete from """ + tblname +"""d where a2>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +"""d set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    #  reject
    stmt = """merge into """ + tblname +"""d on a1=1
when matched then update set b1=-b1
where a3 > 100
when not matched then insert values(20,20,20,20,20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +"""d order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v04a')
    
    #  reset the table
    stmt = """delete from """ + tblname +"""d where a2>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +"""d set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    # 
    #  composite primary key column
    # 
    stmt = """create table """ + tblname +"""e
(
  a1 int not null
 ,a2 int not null
 ,a3 int
 ,a4 int
 ,b1 int
 ,primary key(a1,a2)
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into """ + tblname +"""e values
 (1,1,1,1,1)
,(2,2,2,2,2)
,(3,3,3,3,3)
,(4,4,4,4,4)
,(5,5,null,null,null)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    stmt = """merge into """ + tblname +"""e on (a1=1 and a2=1)
when matched then update set b1=-b1
where a1=1 and a2=1
when not matched then insert values(20,20,20,20,20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +"""e order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v05')
    
    #  reset the table
    stmt = """delete from """ + tblname +"""e where a2>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +"""e set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    #  reject
    stmt = """merge into """ + tblname +"""e on (a1=1 and a2=1)
when matched then update set b1=-b1
where a1=1 and a2=2
when not matched then insert values(20,20,20,20,20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +"""e order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v05a')
    
    #  reset the table
    stmt = """delete from """ + tblname +"""e where a2>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +"""e set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    #  part of pkey
    stmt = """merge into """ + tblname +"""e on (a1=1 and a2=1)
when matched then update set b1=-b1
where a1=1
when not matched then insert values(20,20,20,20,20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +"""e order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v05b')
    
    #  reset the table
    stmt = """delete from """ + tblname +"""e where a2>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +"""e set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    #  part of pkey
    stmt = """merge into """ + tblname +"""e on (a1=1 and a2=1)
when matched then update set b1=-b1
where a2=1
when not matched then insert values(20,20,20,20,20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +"""e order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v05c')
    
    #  reset the table
    stmt = """delete from """ + tblname +"""e where a2>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +"""e set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table """ + tblname +""" cascade;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table """ + tblname +"""b cascade;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table """ + tblname +"""c cascade;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table """ + tblname +"""d cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table """ + tblname +"""e cascade;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -
    #testcase a004 WHERE comparison predicates
    #  MAP: A003
    #  WHERE predicates
    #expect purge immediate
    #sh testid=a004
    #sh tblname=t_$testid
def test004(desc="""a004 WHERE comparison predicates"""):
    global _testmgr
    global _testlist
    global _dci
    testid = """a004"""
    tblname = """t_""" + testid

    if not _testmgr.testcase_begin(_testlist): return

    stmt = """drop table """ + tblname +""" cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table """ + tblname +"""
(
  a1 int not null
 ,b1 int
 ,a_int1 int
 ,a_int2 int
 ,a_cha1 char(10)
 ,a_cha2 char(10)
 ,primary key(a1)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into """ + tblname +""" values 
 (1,1,1,1,'aaa','aaaaa')
,(2,2,2,2,'bbb','bbbbb')
,(3,3,3,3,'ccc','ccccc')
,(4,4,4,4,'ddd','ddddd')
,(5,5,null,null,null,null)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)

    #  comparison predicates
    stmt = """merge into """ + tblname +""" on a1 = 3
when matched then update set b1=-b1
where a_int1 > 1
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v01')

    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)

    #  reject
    stmt = """merge into """ + tblname +""" on a1 = 3
when matched then update set b1=-b1
where a_int1 > 100
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v01a')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)

    #  comparison predicates
    stmt = """merge into """ + tblname +""" on a1 = 3
when matched then update set b1=-b1
where a_int1 >= 1
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v02')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)

    #  reject
    stmt = """merge into """ + tblname +""" on a1 = 3
when matched then update set b1=-b1
where a_int1 >= 30
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v02a')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    #  comparison predicates

    stmt = """merge into """ + tblname +""" on a1 = 1
when matched then update set b1=-b1
where a_int1 < 3 
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v03')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    #  reject
    stmt = """merge into """ + tblname +""" on a1 = 1
when matched then update set b1=-b1
where a_int1 < -3
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v03a')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    #  comparison predicates
    stmt = """merge into """ + tblname +""" on a1 = 1 
when matched then update set b1=-b1
where a_int1 <= 3
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v04')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    #  reject
    stmt = """merge into """ + tblname +""" on a1 = 1
when matched then update set b1=-b1
where a_int1 <= -3
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v04a')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    #  comparison predicates
    stmt = """merge into """ + tblname +""" on a1 = 1
when matched then update set b1=-b1
where a_int1 = 1
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v05')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    #  reject
    stmt = """merge into """ + tblname +""" on a1 = 1
when matched then update set b1=-b1
where a_int1 = 100
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v05a')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    #  comparison predicates
    stmt = """merge into """ + tblname +""" on a1 = 1
when matched then update set b1=-b1
where a_int1 <> 3
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v06')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    #  reject
    stmt = """merge into """ + tblname +""" on a1 = 1
when matched then update set b1=-b1
where a_int1 <> 1
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v06a')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    # 
    #  with logical operators
    # 

    #  AND
    stmt = """merge into """ + tblname +""" on a1 = 3
when matched then update set b1=-b1
where a_int1 > 1 and a_int2 < 4
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v07')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    #  OR
    stmt = """merge into """ + tblname +""" on a1 = 3
when matched then update set b1=-b1
where a_int1 < -1 or a_int2 > 3
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v08')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    #  multiple ANDs
    stmt = """merge into """ + tblname +""" on a1 = 3
when matched then update set b1=-b1
where (a_int1 > 1 and a_int2 <= 3) and a_cha1 > 'b'
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v09')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    #  first condition fails
    stmt = """merge into """ + tblname +""" on a1 = 3
when matched then update set b1=-b1
where a_int1 <1 and a_int2 <= 3
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v10')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    #  second condition fails
    stmt = """merge into """ + tblname +""" on a1 = 3
when matched then update set b1=-b1
where a_int1 >1 and a_int2 > 100
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v11')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    #  both conditions fail
    stmt = """merge into """ + tblname +""" on a1 = 3
when matched then update set b1=-b1
where a_int1 > 100  or a_int2 > 100
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v12')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table """ + tblname +""" cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -
    #testcase a005 WHERE comparison predicates with USING clause
    #  MAP: A003
    #  WHERE predicates 
    #expect purge immediate
    #sh testid=a005
    #sh tblname=t_$testid
def test005(desc="""a005 WHERE comparison predicates with USING clause"""):
    global _testmgr
    global _testlist
    global _dci
    testid = """a005"""
    tblname = """t_""" + testid

    if not _testmgr.testcase_begin(_testlist): return

    stmt = """drop table """ + tblname +""" cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table """ + tblname+"""
(
  a1 int not null
 ,b1 int
 ,a_int1 int
 ,a_int2 int
 ,a_cha1 char(10)
 ,a_cha2 char(10)
 ,primary key(a1)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into """ + tblname+""" values 
 (1,1,1,1,'aaa','aaaaa')
,(2,2,2,2,'bbb','bbbbb')
,(3,3,3,3,'ccc','ccccc')
,(4,4,4,4,'ddd','ddddd')
,(5,5,null,null,null,null)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)

    stmt = """drop table """ + tblname+"""b cascade;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table """ + tblname+"""b like """ + tblname+""";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into """ + tblname+"""b select * from """ + tblname+""";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    #  update all
    stmt = """merge into """ + tblname+"""
using  (
  select a1
  from """ + tblname+"""b
) as t2(a1)
on a1=t2.a1
when matched then update set b1=-b1
where a_int1 > 0
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v01')

    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)

    #  partial update
    stmt = """merge into """ + tblname+"""
using  (
  select a1
  from """ + tblname+"""b
) as t2(a1)
on a1=t2.a1
when matched then update set b1=-b1
where a_int1 > 3
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v02')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)

    #  reject all
    stmt = """merge into """ + tblname+"""
using  (
  select a1
  from """ + tblname+"""b
) as t2(a1)
on a1=t2.a1
when matched then update set b1=-b1
where a_int1 < 0
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v03')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)

    #  reject based on target table condition
    stmt = """merge into """ + tblname+"""
using  (
  select a1
  from """ + tblname+"""b
) as t2(a1)
on a1=t2.a1
when matched then update set b1=-b1
where a_int1 = 100 and t2.a1 is null
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v04')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    #  reject based on source table condition
    stmt = """merge into """ + tblname+"""
using  (
  select a1
  from """ + tblname+"""b
) as t2(a1)
on a1=t2.a1
when matched then update set b1=-b1
where a_int1 is null and t2.a1 > 100
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v05')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    #  both conditions fail
    stmt = """merge into """ + tblname+"""
using  (
  select a1
  from """ + tblname+"""b
) as t2(a1)
on a1=t2.a1
when matched then update set b1=-b1
where a_int1 = 100 and t2.a1 = 100
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v06')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table """ + tblname +""" cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table """ + tblname +"""b cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _testmgr.testcase_end(desc)
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -
    #testcase a006 WHERE predicates
    #  MAP: A003
    #  WHERE predicates
    #expect purge immediate
    #sh testid=a006
    #sh tblname=t_$testid
def test006(desc="""a006 WHERE predicates"""):
    global _testmgr
    global _testlist
    global _dci
    testid = """a006"""
    tblname = """t_""" + testid

    if not _testmgr.testcase_begin(_testlist): return

    stmt = """drop table """ + tblname +""" cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table """ + tblname +"""b  cascade;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table """ + tblname+"""
(
  a1 int not null
 ,b1 int
 ,a_int1 int
 ,a_int2 int
 ,a_cha1 char(10)
 ,a_cha2 char(10)
 ,primary key(a1)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into """ + tblname+""" values 
 (1,1,1,1,'aaa','aaaaa')
,(2,2,2,2,'bbb','bbbbb')
,(3,3,3,3,'ccc','ccccc')
,(4,4,4,4,'ddd','ddddd')
,(5,5,null,null,null,null)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)

    stmt = """create table """ + tblname+"""b like """ + tblname+""";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into """ + tblname+"""b select * from """ + tblname+""";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    #  between predicate
    stmt = """merge into """ + tblname+""" on a1 = 3
when matched then update set b1=-b1
where a_int1 between 2 and 3
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v01')

    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)

    #  reject
    stmt = """merge into """ + tblname+""" on a1 = 3
when matched then update set b1=-b1
where a_int1 between 20 and 30
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v01a')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)

    #  not between
    stmt = """merge into """ + tblname+""" on a1 = 3
when matched then update set b1=-b1
where a_int1 not between 1 and 2
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v01b')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)

    #  exists predicate
    stmt = """merge into """ + tblname+""" on a1 = 3
when matched then update set b1=-b1
where exists (select a_int1 from """ + tblname+"""b where a1 > 0)
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3241')

    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v02')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    #  exists predicate
    #  reject
    stmt = """merge into """ + tblname+""" on a1 = 1
when matched then update set b1=-b1
where exists ( select a_int1 from """ + tblname+"""b where a1 > 100)
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3241')
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v02a')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    #  exists predicate
    #  NOT exists
    stmt = """merge into """ + tblname+""" on a1 = 1
when matched then update set b1=-b1
where not exists (select a_int1 from """ + tblname+"""b where a1 > 100)
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3241')
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v02b')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    #  in predicate
    stmt = """merge into """ + tblname+""" on a1 = 1
when matched then update set b1=-b1
where a_int1 in (1,3,5)
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v03')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)

    #  in predicate
    #  reject
    stmt = """merge into """ + tblname+""" on a1 = 1
when matched then update set b1=-b1
where a_int1 in (10,30,50)
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v03a')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    #  in predicate
    #  NOT in
    stmt = """merge into """ + tblname+""" on a1 = 1
when matched then update set b1=-b1
where a_int1 not in (2,3,5)
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v03b')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    #  in predicate
    #  using subquery
    stmt = """merge into """ + tblname+""" on a1 = 1
when matched then update set b1=-b1
where a_int1 in (select a_int1 from """ + tblname+"""b where a1 between 1 and 3)
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3241')
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v03c')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    #  in predicate subq
    #  reject 
    stmt = """merge into """ + tblname+""" on a1 = 1
when matched then update set b1=-b1
where a_int1 in (select a_int1+10 from """ + tblname+"""b where a1 between 1 and 3)
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3241')
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v03d')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    #  like predicate
    stmt = """merge into """ + tblname+""" on a1 = 1
when matched then update set b1=-b1
where a_cha1 like 'a%' or a_cha1 like '%b'
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v04')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    #  like predicate
    #  reject
    stmt = """merge into """ + tblname+""" on a1 = 1
when matched then update set b1=-b1
where a_cha1 like 'z%'
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v04a')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    #  like predicate with escape char
    #  reject
    stmt = """merge into """ + tblname+""" on a1 = 1
when matched then update set b1=-b1
where a_cha1 like 'az_%' escape 'z'
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v04b')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    #  like predicate
    #  NOT like
    stmt = """merge into """ + tblname+""" on a1 = 1
when matched then update set b1=-b1
where a_cha1 not like 'az_%' escape 'z'
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v04c')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    #  null predicate
    stmt = """merge into """ + tblname+""" on a1 = 5
when matched then update set b1=-b1
where a_int1 is null
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v05')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    
    #  null predicate
    #  reject
    stmt = """merge into """ + tblname+""" on a1 = 1
when matched then update set b1=-b1
where a_int1 is null
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v05a')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    #  null predicate
    #  not null
    stmt = """merge into """ + tblname+""" on a1 = 1
when matched then update set b1=-b1
where a_int1 is not null
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v05b')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table """ + tblname +""" cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table """ + tblname +"""b cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -
    #testcase a007 WHERE predicates contains character value expression
    #  MAP: A004
    #expect purge immediate
    #sh testid=a007
    #sh tblname=t_$testid
def test007(desc="""a007 WHERE predicates contains character value expression"""):
    global _testmgr
    global _testlist
    global _dci
    testid = """a007"""
    tblname = """t_""" + testid

    if not _testmgr.testcase_begin(_testlist): return

    stmt = """drop table """ + tblname +""" cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table """ + tblname +"""b  cascade;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table """ + tblname+"""
(
  a1 int not null
 ,b1 int
 ,a_int1 int
 ,a_int2 int
 ,a_cha1 char(10)
 ,a_cha2 char(10)
 ,primary key(a1)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into """ + tblname+""" values 
 (1,1,1,1,'aaa','aaaaa')
,(2,2,2,2,'bbb','bbbbb')
,(3,3,3,3,'ccc','ccccc')
,(4,4,4,4,'ddd','ddddd')
,(5,5,null,null,null,null)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)

    stmt = """create table """ + tblname+"""b like """ + tblname+""";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into """ + tblname+"""b select * from """ + tblname+""";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    #  character string literal
    stmt = """merge into """ + tblname+""" on a1 = 3
when matched then update set b1=-b1
where a_cha1 = 'ccc'
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v01')

    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)

    #  column references
    stmt = """merge into """ + tblname+""" on a1 = 3 
when matched then update set b1=-b1
where a_cha1 between 'a' and a_cha2
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v02')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)

    #  character type host var
    stmt = """set param ?hv 'ccc';"""
    output = _dci.cmdexec(stmt)
    stmt = """merge into """ + tblname+""" on a1 = 3
when matched then update set b1=-b1
where a_cha1 = ?hv
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v03')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    
    #  character function
    stmt = """merge into """ + tblname+""" on a1 = 1
when matched then update set b1=-b1
where a_cha1 = substring(a_cha2, 1, 3) and a_cha2 < 'd'
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v04')
    
    #  reset b1 value
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    
    #  aggregate function
    stmt = """merge into """ + tblname+""" on a1 = 1
when matched then update set b1=-b1
where max(a_cha1) < 'z'
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3241')
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v05')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    
    
    #  aggregate function
    stmt = """merge into """ + tblname+"""
using (select max(a_cha1) from """ + tblname+"""b) as t(m)
on a1=1
when matched then update set b1=-b1
where m < 'z'
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v06')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    
    
    #  cast
    stmt = """merge into """ + tblname+""" on a1 = 1
when matched then update set b1=-b1
where char_length(cast(a_cha1 as varchar(10))) < 15
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v07')
    
    #  reset b1 value
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    
    #  case expression
    stmt = """merge into """ + tblname+""" on a1 = 3
when matched then update set b1=-b1
where (case a_cha1 
         when 'ccc' then 3
         when 'ddd' then 4
         else 0
      end) = 3
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v08')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    
    stmt = """drop table """ + tblname +""" cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table """ + tblname +"""b cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -
    #testcase a008 WHERE predicates contains character value expression - reject
    #  MAP: A004
    #expect purge immediate
    #sh testid=a008
    #sh tblname=t_$testid
def test008(desc="""a008 WHERE predicates contains character value expression - reject"""):
    global _testmgr
    global _testlist
    global _dci
    testid = """a008"""
    tblname = """t_""" + testid

    if not _testmgr.testcase_begin(_testlist): return

    stmt = """drop table """ + tblname +""" cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table """ + tblname +"""b  cascade;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table """ + tblname+"""
(
  a1 int not null
 ,b1 int
 ,a_int1 int
 ,a_int2 int
 ,a_cha1 char(10)
 ,a_cha2 char(10)
 ,primary key(a1)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into """ + tblname+""" values 
 (1,1,1,1,'aaa','aaaaa')
,(2,2,2,2,'bbb','bbbbb')
,(3,3,3,3,'ccc','ccccc')
,(4,4,4,4,'ddd','ddddd')
,(5,5,null,null,null,null)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)

    stmt = """create table """ + tblname+"""b like """ + tblname+""";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into """ + tblname+"""b select * from """ + tblname+""";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    #  character string literal
    stmt = """merge into """ + tblname+""" on a1 = 3
when matched then update set b1=-b1
where a_cha1 > 'ccc'
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v01')

    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)

    #  column references
    stmt = """merge into """ + tblname+""" on a1 = 3 
when matched then update set b1=-b1
where a_cha1 between 'd' and a_cha2
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v02')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)

    #  character type host var
    stmt = """set param ?hv 'ccc';"""
    output = _dci.cmdexec(stmt)
    stmt = """merge into """ + tblname+""" on a1 = 1
when matched then update set b1=-b1
where a_cha1 = ?hv
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v03')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    
    #  character function
    stmt = """merge into """ + tblname+""" on a1 = 1
when matched then update set b1=-b1
where a_cha1 = substring(a_cha2, 1, 3) and a_cha2 > 'd'
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v04')
    
    #  reset b1 value
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    
    #  aggregate function
    stmt = """merge into """ + tblname+"""
using (select max(a_cha1) from """ + tblname+"""b) as t(m)
on a1 = 1
when matched then update set b1=-b1
where m > 'z'
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v06')
    
    #  reset b1 value
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    
    
    #  cast
    stmt = """merge into """ + tblname+""" on a1 = 1
when matched then update set b1=-b1
where char_length(cast(a_cha1 as varchar(10))) > 100
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v07')
    
    #  reset b1 value
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    
    #  case expression
    stmt = """merge into """ + tblname+""" on a1 = 1
when matched then update set b1=-b1
where (case a_cha1 
         when 'ccc' then 3
         when 'ddd' then 4
         else 0
      end) = 3
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v08')
    
    #   reset b1 value
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    
    stmt = """drop table """ + tblname +""" cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table """ + tblname +"""b cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -
    #testcase a009 WHERE predicates contains date value expression
    #  MAP: A004
    #expect purge immediate
    #sh testid=a009
    #sh tblname=t_$testid
def test009(desc="""a009 WHERE predicates contains date value expression"""):
    global _testmgr
    global _testlist
    global _dci
    testid = """a009"""
    tblname = """t_""" + testid

    if not _testmgr.testcase_begin(_testlist): return

    stmt = """drop table """ + tblname +""" cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table """ + tblname +"""b  cascade;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table """ + tblname+"""
(
  a1 int not null
 ,b1 int
 ,a_dte1 date
 ,a_dte2 date
 ,primary key(a1)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into """ + tblname+""" values 
 (1,1,date'11/21/2001',date'11/21/2001')
,(2,2,date'11/22/2001',date'11/22/2001')
,(3,3,date'11/23/2001',date'11/23/2001')
,(4,4,date'11/24/2001',date'11/24/2001')
,(5,5,null,null)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)

    stmt = """create table """ + tblname+"""b like """ + tblname+""";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into """ + tblname+"""b select * from """ + tblname+""";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    #  date literal
    stmt = """merge into """ + tblname+""" on a1 = 3
when matched then update set b1=-b1
where a_dte1 = date'11/23/2001'
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v01')

    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)

    #  date literal
    #  reject
    stmt = """merge into """ + tblname+""" on a1 = 3
when matched then update set b1=-b1
where a_dte1 <> date'11/23/2001'
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v01a')
    
    #  reset b1 value
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)

    #  column references
    stmt = """merge into """ + tblname+""" on a1 = 3
when matched then update set b1=-b1
where a_dte1 between date'11/22/2001' and date'11/24/2001'
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v02')
    
    #  reset b1 value
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    
    #  column references
    #  reject
    stmt = """merge into """ + tblname+""" on a1 = 3
when matched then update set b1=-b1
where a_dte1 not between date'11/22/2001' and date'11/24/2001'
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v02a')
    
    #  reset b1 value
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    
    #  date type host var
    stmt = """set param ?hv '11/23/2001';"""
    output = _dci.cmdexec(stmt)
    stmt = """merge into """ + tblname+""" on a1 = 3
when matched then update set b1=-b1
where a_dte1 = cast(?hv as date)
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v03')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    
    #  date type host var
    #  reject
    stmt = """set param ?hv '11/23/2001';"""
    output = _dci.cmdexec(stmt)
    stmt = """merge into """ + tblname+""" on a1 = 3
when matched then update set b1=-b1
where a_dte1 = cast(?hv as date) + interval '1' day
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v03a')
    
    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    
    #  date function
    stmt = """merge into """ + tblname+""" on a1 = 1
when matched then update set b1=-b1
where dateadd(day, 1, a_dte1) = date'11/22/2001'
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v04')
    
    #  reset b1 value
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    
    #  date function
    #  reject
    stmt = """merge into """ + tblname+""" on a1 = 1
when matched then update set b1=-b1
where dateadd(day, 1, a_dte1) = date'11/23/2001'
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v04a')
    
    #  reset b1 value
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    
    
    #  date expression
    stmt = """set param ?hv '11/23/2001';"""
    output = _dci.cmdexec(stmt)
    stmt = """merge into """ + tblname+""" on a1 = 4
when matched then update set b1=-b1
where a_dte1 - interval '1' day = cast(?hv as date)
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v07')
    
    #  reset b1 value
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    
    #  debug:
    stmt = """select * from """ + tblname+""";"""
    output = _dci.cmdexec(stmt)
    
    #  date expression
    stmt = """set param ?hv '11/23/2001';"""
    output = _dci.cmdexec(stmt)
    stmt = """merge into """ + tblname+""" on a1 = 4
when matched then update set b1=-b1
where a_dte1 - interval '1' day > cast(?hv as date)
when not matched then insert(a1) values(20)
;
# """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    #_dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v07a')
    
    #   reset b1 value
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    
    stmt = """drop table """ + tblname +""" cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table """ + tblname +"""b cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -
    #testcase a010 WHERE predicates contains numeric value expression
    #  MAP: A004
    #expect purge immediate
    #sh testid=a010
    #sh tblname=t_$testid
def test010(desc="""a010 WHERE predicates contains numeric value expression"""):
    global _testmgr
    global _testlist
    global _dci
    testid = """a010"""
    tblname = """t_""" + testid

    if not _testmgr.testcase_begin(_testlist): return

    stmt = """drop table """ + tblname +""" cascade;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table """ + tblname+"""
(
  a1 int not null
 ,b1 int
 ,a_num1 numeric(10,2) signed
 ,a_num2 numeric(10,2) signed
 ,primary key(a1)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into """ + tblname+""" values 
 (1,1,1.11,1.11)
,(2,2,2.22,2.22)
,(3,3,3.33,3.33)
,(4,4,4.44,4.44)
,(5,5,null,null)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    #  numeric literal
    stmt = """merge into """ + tblname+""" on a1 = 2
when matched then update set b1=-b1
where a_num1 = (150/50 - 1) + 0.22
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v01')

    #  reset the table
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)

    #  numeric literal
    #  reject
    stmt = """merge into """ + tblname+""" on a1 = 1
when matched then update set b1=-b1
where a_num1 = (150/50 - 1) + 0.22
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v01a')
    
    #  reset b1 value
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)

    #  numeric type host var
    stmt = """set param ?hv 3.33;"""
    output = _dci.cmdexec(stmt)
    stmt = """merge into """ + tblname+""" on a1 = 4
when matched then update set b1=-b1
where a_num1 > ?hv
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v02')
    
    #  reset b1 value
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    
    #  numeric type host var
    #  reject
    stmt = """set param ?hv 3.33;"""
    output = _dci.cmdexec(stmt)
    stmt = """merge into """ + tblname+""" on a1 = 4
when matched then update set b1=-b1
where a_num1 < ?hv
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v02a')
    
    #  reset b1 value
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)

    stmt = """drop table """ + tblname +""" cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -
    #testcase a011 WHERE predicates contains literals
    #  MAP: A005
    #expect purge immediate
    #sh testid=a011
    #sh tblname=t_$testid
def test011(desc="""a011 WHERE predicates contains literals"""):
    global _testmgr
    global _testlist
    global _dci
    testid = """a011"""
    tblname = """t_""" + testid

    if not _testmgr.testcase_begin(_testlist): return

    stmt = """drop table """ + tblname +""" cascade;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table """ + tblname+"""
(
  a1 int not null
 ,b1 int
 ,a_int1 int
 ,a_cha1 char(10)
 ,a_tms1 timestamp
 ,primary key(a1)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into """ + tblname+""" values 
 (1,1,1,'aaa',timestamp'11/21/2001 11:22:31')
,(2,2,2,'bbb',timestamp'11/21/2001 11:22:32')
,(3,3,3,'ccc',timestamp'11/21/2001 11:22:33')
,(4,4,4,'ddd',timestamp'11/21/2001 11:22:34')
,(5,5,null,null,null)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)

    stmt = """create table """ + tblname+"""b like """ + tblname+""";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into """ + tblname+"""b select * from """ + tblname+""";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    #  character string literal
    stmt = """merge into """ + tblname+""" on a1 = 3
when matched then update set b1=-b1
where a_cha1 like ('c' || 'c' || '%')
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v01')

    #  reset b1 value
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)

    #  character string literal
    #  reject
    stmt = """merge into """ + tblname+""" on a1 = 3
when matched then update set b1=-b1
where a_cha1 like ('c' || 'c' || '%' || 'z')
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v01a')
    
    #  reset b1 value
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)

    #  datetime literal
    stmt = """merge into """ + tblname+""" on a1 = 3
when matched then update set b1=-b1
where a_tms1 = timestamp'11/21/2001 11:22:34' - interval '1' second
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v02')
    
    #  reset b1 value
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    
    #  datetime literal
    #  reject
    stmt = """merge into """ + tblname+""" on a1 = 3
when matched then update set b1=-b1
where a_tms1 < timestamp'11/21/2001 11:22:34' - interval '1' second
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v02a')
    
    #  reset b1 value
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)

    #  numeric literal
    stmt = """merge into """ + tblname+""" on a1 = 3
when matched then update set b1=-b1
where a_int1 > 2e+0 and a_int1 < 40e-1
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v03')
    
    #  reset b1 value
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    
        #  reset b1 value
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)

    #  numeric literal
    #  reject
    stmt = """merge into """ + tblname+""" on a1 = 1
when matched then update set b1=-b1
where a_int1 > 2e+0 and a_int1 < 40e-1
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v03a')
    
    #  reset b1 value
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname +""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    
    stmt = """drop table """ + tblname +""" cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -
    #testcase a012 subquery in where clause
    #  MAP: A005
    #expect purge immediate
    #sh testid=a012
    #sh tblname=t_$testid
def test012(desc="""a012 WHERE predicates contains date value expression"""):
    global _testmgr
    global _testlist
    global _dci
    testid = """a012"""
    tblname = """t_""" + testid

    if not _testmgr.testcase_begin(_testlist): return

    stmt = """drop table """ + tblname +""" cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table """ + tblname +"""b  cascade;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table """ + tblname+"""
(
  a1 int not null
 ,a2 int
 ,a3 int
 ,a4 int
 ,a5 int
 ,primary key(a1)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into """ + tblname+""" values 
 (1,1,1,1,1)
,(2,2,2,2,2)
,(3,3,3,3,3)
,(4,4,4,4,4)
,(5,null,null,null,null)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)

    stmt = """create table """ + tblname+"""b like """ + tblname+""";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into """ + tblname+"""b select * from """ + tblname+""";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    #  subquery in where clause
    stmt = """merge into """ + tblname+""" on a1=1
when matched then update set b1=-b1 
where a4= (select max(a4) from """ + tblname+"""b)
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'3241')
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v01')

    #  reset a4 values
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname+""" set a5=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output,5)

    #  subquery in where clause with quantifier
    stmt = """merge into """ + tblname+""" on a1=1
when matched then update set b1=-b1
where a4 > some (select a4 from """ + tblname+"""b where a4 is not null)
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'3241')
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v02')
    
    #  reset a4 values
    stmt = """delete from """ + tblname +""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname+""" set a5=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)

    stmt = """drop table """ + tblname +""" cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table """ + tblname +"""b cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -
    #testcase a013 Check the behavior of WHERE clause along with ON clause
    #  MAP: B001
    #expect purge immediate
    #sh testid=a013
    #sh tblname=t_$testid
def test013(desc="""a013 Check the behavior of WHERE clause along with ON clause"""):
    global _testmgr
    global _testlist
    global _dci
    testid = """a013"""
    tblname = """t_""" + testid

    if not _testmgr.testcase_begin(_testlist): return

    stmt = """drop table """ + tblname +""" cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table """ + tblname+"""
(
  a1 int not null
 ,a2 int
 ,a3 int
 ,a4 int
 ,b1 int
 ,primary key(a1)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into """ + tblname+""" values 
 (1,1,1,1,1)
,(2,2,2,2,2)
,(3,3,3,3,3)
,(4,4,4,4,4)
,(5,null,null,null,null)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    #  ON predicate fails, WHERE predicate fails
    stmt = """merge into """ + tblname+""" on a1 = -1
when matched then update set b1=-b1 
where a4= -1
when not matched then insert(a1) values(-1)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v01')

    #  reset a4 values
    stmt = """delete from """ + tblname+""" where a1<0;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname+""" set b1=a1;"""
    output = _dci.cmdexec(stmt)


    #  ON predicate fails, WHERE predicate passes
    stmt = """merge into """ + tblname+""" on a1 = -1
when matched then update set b1=-b1
where a4= 1
when not matched then insert(a1) values(-1)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v02')
    
    #  reset a4 values
    stmt = """delete from """ + tblname+""" where a1<0;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname+""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)

    #  ON predicate passes, WHERE predicate fails
    stmt = """merge into """ + tblname+""" on a1 = 1
when matched then update set b1=-b1
where a4= -1
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v03')
    
    #  reset a4 values
    stmt = """delete from """ + tblname+""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname+""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    
    #  ON predicate passes, WHERE predicate passes
    stmt = """merge into """ + tblname+""" on a1 = 1
when matched then update set b1=-b1
where a4= 1
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v04')
    
    #  reset a4 values
    stmt = """delete from """ + tblname+""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname+""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)

    stmt = """drop table """ + tblname +""" cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -
    #testcase a014 Columns involved in ON and WHERE 
    #  MAP: B002
    #  This testcase only covers the case where ON and WHERE both contain
    #  the same column. The different column case is covered in other tests.
    #expect purge immediate
    #sh testid=a014
    #sh tblname=t_$testid
def test014(desc="""a014 Columns involved in ON and WHERE """):
    global _testmgr
    global _testlist
    global _dci
    testid = """a014"""
    tblname = """t_""" + testid

    if not _testmgr.testcase_begin(_testlist): return

    stmt = """drop table """ + tblname +""" cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table """ + tblname +"""b  cascade;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table """ + tblname+"""
(
  a1 int not null
 ,a2 int
 ,a3 int
 ,a4 int
 ,b1 int
 ,primary key(a1)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into """ + tblname+""" values 
 (1,1,1,1,1)
,(2,2,2,2,2)
,(3,3,3,3,3)
,(4,4,4,4,4)
,(5,null,null,null,null)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    stmt = """create table """ + tblname+"""b like """ + tblname+""";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into """ + tblname+"""b select * from """ + tblname+""";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)

    #  ON predicate and WHERE predicate both contain the same column
    #  same condition
    stmt = """merge into """ + tblname+""" on a1 = 1
when matched then update set b1=-b1 
where a1 = 1 and a3 = 1
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v01')

    #  reset b1 values
    stmt = """delete from """ + tblname+""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname+""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)

    #  ON predicate and WHERE predicate both contain the same column
    #  different condition
    stmt = """merge into """ + tblname+""" on a1 =3
when matched then update set b1=-b1
where a1 < 4  and a3 = 3
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v02')
    
    #  reset b1 values
    stmt = """delete from """ + tblname+""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname+""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)

    #  ON predicate and WHERE predicate both contain the same column
    #  conflicts
    stmt = """merge into """ + tblname+""" on a1 = 1
when matched then update set b1=-b1
where a1 <> 1  and a3 = 2
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v03')
    
    #  reset a4 values
    stmt = """delete from """ + tblname+""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname+""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)

    stmt = """drop table """ + tblname +""" cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -
#testcase a015 WHERE predicate is specified for DELETE clause
#  MAP: B003
#  WHERE on DELETE is not supported.
#expect purge immediate
#sh testid=a015
#sh tblname=t_$testid
def test015(desc="""a015 WHERE predicate is specified for DELETE clause """):
    global _testmgr
    global _testlist
    global _dci
    testid = """a015"""
    tblname = """t_""" + testid

    if not _testmgr.testcase_begin(_testlist): return

    stmt = """drop table """ + tblname +""" cascade;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table """ + tblname+"""
(
  a1 int not null
 ,a2 int
 ,a3 int
 ,a4 int
 ,b1 int
 ,primary key(a1)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into """ + tblname+""" values 
 (1,1,1,1,1)
,(2,2,2,2,2)
,(3,3,3,3,3)
,(4,4,4,4,4)
,(5,null,null,null,null)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)

    #  delete with INSERT present
    stmt = """merge into """ + tblname+""" on a1 = 1
when matched then delete 
where a3 = 1
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'15001')
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v01')

    stmt = """drop table """ + tblname +""" cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -
#testcase a017 Verify the equality set expressions work as expected
#  MAP: B006
#expect purge immediate
#sh testid=a017
#sh tblname=t_$testid
def test017(desc="""a017 Verify the equality set expressions work as expected """):
    global _testmgr
    global _testlist
    global _dci
    testid = """a017"""
    tblname = """t_""" + testid

    if not _testmgr.testcase_begin(_testlist): return

    stmt = """drop table """ + tblname +""" cascade;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table """ + tblname+"""
(
  a1 int not null
 ,a2 int
 ,a3 int
 ,a4 int
 ,b1 int
 ,primary key(a1)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into """ + tblname+""" values 
 (1,1,1,1,1)
,(2,2,2,2,2)
,(3,3,3,3,3)
,(4,4,4,4,4)
,(5,null,null,null,null)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    stmt = """create table """ + tblname+"""b like """ + tblname+""";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into """ + tblname+"""b select * from """ + tblname+""";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    stmt = """merge into """ + tblname+""" on a1 = 1
when matched then update set b1=-b1 
where a2 = 3
  or a2 in (2,4)
  or a2 = (1 - a3 + a1)
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v01')

    #  reset b1 values
    stmt = """delete from """ + tblname+""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname+""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    
    #  reject the row
    stmt = """merge into """ + tblname+""" on a1 = 1
when matched then update set b1=-b1
where a2 = 3
  or a2 in (2,4)
  or a2 in (2,3,5)
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v01a')

    #  reset b1 values
    stmt = """delete from """ + tblname+""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname+""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    
    stmt = """merge into """ + tblname+""" on a1 = 1
when matched then update set b1=-b1
where a1 = a2 and a2 = a3
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v02')

    #  reset b1 values
    stmt = """delete from """ + tblname+""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname+""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    
    #  reject
    stmt = """merge into """ + tblname+""" on a1 = 1
when matched then update set b1=-b1
where a1=a2 and a2 = 2
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v02a')

    #  reset b1 values
    stmt = """delete from """ + tblname+""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname+""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    
    stmt = """merge into """ + tblname+""" 
using (select a1,a2,a3,a4 from """ + tblname+"""b where a1>0) t2(a1,a2,a3,a4)
on a1=t2.a1
when matched then update set b1=-b1
where a2=t2.a2 and t2.a2=a3 and a3=t2.a3 and t2.a3=a4 and a4=t2.a4 and t2.a4 = 1
when not matched then insert(a1) values(20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v03')

    #  reset b1 values
    stmt = """delete from """ + tblname+""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname+""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    
    stmt = """drop table """ + tblname +""" cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table """ + tblname +"""b  cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -
#testcase a018 UPDATE is present with WHERE clause and no INSERT is specified
#  MAP: B007
#expect purge immediate
#sh testid=a018
#sh tblname=t_$testid
def test018(desc="""a018 UPDATE is present with WHERE clause and no INSERT is specified"""):
    global _testmgr
    global _testlist
    global _dci
    testid = """a018"""
    tblname = """t_""" + testid

    if not _testmgr.testcase_begin(_testlist): return

    stmt = """drop table """ + tblname +""" cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table """ + tblname +"""b cascade;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table """ + tblname+"""
(
  a1 int not null
 ,a2 int
 ,a3 int
 ,a4 int
 ,b1 int
 ,primary key(a1)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into """ + tblname+""" values 
 (1,1,1,1,1)
,(2,2,2,2,2)
,(3,3,3,3,3)
,(4,4,4,4,4)
,(5,null,null,null,null)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    stmt = """create table """ + tblname+"""b like """ + tblname+""";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into """ + tblname+"""b select * from """ + tblname+""";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    #  should update the row
    stmt = """merge into """ + tblname+""" on a2=1
when matched then update set b1=-b1 
where a4=1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v01')

    #  reset b1 values
    stmt = """update """ + tblname+""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    
    #  debug:
    stmt = """select * from """ + tblname+"""b;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from """ + tblname+""";"""
    output = _dci.cmdexec(stmt)

    #  column from source table in WHERE clause
    stmt = """merge into """ + tblname+""" 
using  (
  select a2
  from """ + tblname+"""b
) as t2(a2)
on a2=t2.a2
when matched then update set b1=-b1 
where t2.a2=2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    #_dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v02')

    #  reset b1 values
    stmt = """update """ + tblname+""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    
    #  columns from both source and target table in WHERE clause
    stmt = """merge into """ + tblname+""" 
using  (
  select a4
  from """ + tblname+"""b
) as t2(a4)
on a2 > 3
when matched then update set b1=-b1 
where a4=t2.a4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v03')

    #  reset b1 values
    stmt = """update """ + tblname+""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    
    #  columns from both source and target table in WHERE clause
    #  with logical operator
    stmt = """merge into """ + tblname+""" 
using  (
  select a3,a4
  from """ + tblname+"""b
) as t2(a3,a4)
on a2 > 3
when matched then update set b1=-b1
where a4=t2.a4 and a3 > 0 and t2.a4 > 0
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v04')

    #  reset b1 values
    stmt = """update """ + tblname+""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    
    #  no reference to either table
    stmt = """set param ?hv 5;"""
    output = _dci.cmdexec(stmt)
    stmt = """merge into """ + tblname+""" 
using  (
  select a2
  from """ + tblname+"""b
) as t2(a2)
on a2 > 3
when matched then update set b1=-b1
where ?hv = 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v05')

    stmt = """drop table """ + tblname +""" cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table """ + tblname +"""b  cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -
#testcase a019 self join
#  MAP: A019
#  self join used in USING clause
#expect purge immediate
#sh testid=a019
#sh tblname=t_$testid
def test019(desc="""a019 self join"""):
    global _testmgr
    global _testlist
    global _dci
    testid = """a019"""
    tblname = """t_""" + testid

    if not _testmgr.testcase_begin(_testlist): return

    stmt = """drop table """ + tblname +""" cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table """ + tblname +"""b cascade;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table """ + tblname+"""
(
  a1 int not null
 ,a2 int
 ,a3 int
 ,a4 int
 ,b1 int
 ,primary key(a1)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into """ + tblname+""" values 
 (1,1,1,1,1)
,(2,2,2,2,2)
,(3,3,3,3,3)
,(4,4,4,4,4)
,(5,null,null,null,null)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    #  column from source table in WHERE clause
    stmt = """merge into """ + tblname+"""
using  (
  select a2
  from """ + tblname+"""
) as t2(a2)
on a1=t2.a2
when matched then update set b1=-b1 
where a1=1
when not matched then insert values(20,20,20,20,20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v02')

    #  reset b1 values
    stmt = """delete from """ + tblname+""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname+""" set b1=a1;"""
    output = _dci.cmdexec(stmt)
    
    #  debug:
    stmt = """select * from """ + tblname+""";"""
    output = _dci.cmdexec(stmt)

    #  updated column is also used in WHERE clause
    stmt = """merge into """ + tblname+""" 
using  (
  select a2, a4
  from """ + tblname+"""
) as t2(a2, a4)
on a1=t2.a2
when matched then update set a4=-a4
where a4=t2.a4
when not matched then insert values(20,20,20,20,20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v03')

    #  reset b1 values
    stmt = """delete from """ + tblname+""" where a1>10;"""
    output = _dci.cmdexec(stmt)
    stmt = """update """ + tblname+""" set a4=a1;"""
    output = _dci.cmdexec(stmt)
    
    #  updated column is a key column and used in ON clause
    stmt = """merge into """ + tblname+""" 
using  (
  select a4
  from """ + tblname+"""
) as t2(a4)
on a1=t2.a4
when matched then update set a1=-a1
where a4=t2.a4 and a3 > 0 and t2.a4 > 0
when not matched then insert values(20,20,20,20,20)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4033')
    
    stmt = """select * from """ + tblname +""" order by a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/"""+testid+"""exp""", 'v04')

    stmt = """drop table """ + tblname +""" cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 