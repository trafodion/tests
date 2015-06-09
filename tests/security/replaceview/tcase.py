# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2015 Hewlett-Packard Development Company, L.P.
#
#  Licensed under the Apache License, Version 2.0 (the "License");"""
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
import defs
import basic_defs
import unittest
import time

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


def testa01(desc="""create/create or replace a non-existing view"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    mydci = basic_defs.switch_session_qi_user2()

    stmt = """create shared schema my_schema1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema my_schema1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a01tab1(a int not null primary key, b int ,constraint tab1check check(b>0));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a01tab2(col1 int, col2 int )no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a01view1 as select * from a01tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a01view2(a,b) as select a, col2 from a01tab1,a01tab2 where b=col1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a01view3 as select * from a01tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create or replace view a01view4(a,b) as select a, col2 from a01tab1,a01tab2 where b=col1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop schema my_schema1 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)  

    _testmgr.testcase_end(desc)

    
def testa02(desc="""create/create or create or replace an existing view which is invalid"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
 
    mydci = basic_defs.switch_session_qi_user2()

    stmt = """create shared schema my_schema2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema my_schema2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a02tab1(a int not null primary key, b int ,constraint tab1check check(b>0));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a02tab2(col1 int, col2 int )no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a02tab3(a1 int,b1 int ,c1 varchar(10))no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a02view1 as select * from a02tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a02view2 as select * from a02tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop table a02tab2 cascade invalidate;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a02view1 as select * from a02tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1390')

    stmt = """create table a02tab2(col1 int, col2 int )no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create or replace  view a02view2(a,b) as select col1,c1 from a02tab2, a02tab3 where col2=b1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a02tab1 values(1,1);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)

    stmt = """select * from a02view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt = """select * from a02view2;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,0)

    stmt = """drop schema my_schema2 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

    
def testa03(desc="""create/create or replace  an existing view which is valid"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
 
    mydci = basic_defs.switch_session_qi_user2()

    stmt = """create shared schema my_schema3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """set schema my_schema3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a03tab1(a int not null primary key, b int ,constraint tab1check check(b>0));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a03tab2(col1 int not null primary key , col2 varchar(10), constraint tab2check foreign key (col1) references a03tab1(a));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a03tab3(a int, b int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a03view1 as select * from a03tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a03view2(a1,b1) as select col2,b from a03tab2, a03tab3 where col1=a;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a03view1 as select * from a03tab3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1390')
    
    stmt = """create or replace  view a03view2 as select a, col2 from a03tab1, a03tab2 where b=col1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a03tab1 values(1,1),(2,2);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,2)

    stmt = """insert into a03tab3 values(12,12);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)

    stmt = """select * from a03view1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,2)   

    stmt = """drop schema my_schema3 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

    
def testa04(desc="""create/create or replace an existing view v1 v1's structure is same with old"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
 
    mydci = basic_defs.switch_session_qi_user2()

    stmt = """create shared schema my_schema4;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema my_schema4;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a04tab1(col1 int not null primary key , col2 varchar(10));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a04tab2(a int, b int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a04tab3(col1 int not null primary key , col2 varchar(10));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a04view1 as select * from a04tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a04view2(aa,bb) as select  a,col2 from a04tab2,a04tab1 where b=col1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop table a04tab1 cascade invalidate;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a04view1 as select * from a04tab3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1390')

    stmt = """create or replace  view a04view2(aa,bb) as select  a,col2 from a04tab2,a04tab3 where b=col1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop schema my_schema4 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

    
def testa05(desc="""create/create or replace an existing view v1 v1 has same columns with old,the quer-expr is different from old"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    mydci = basic_defs.switch_session_qi_user2()

    stmt = """create shared schema my_schema5;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
     
    stmt = """set schema my_schema5;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a05tab1(col1 int not null primary key , col2 varchar(10));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a05tab2(a1 int, b1 int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a05tab3(a2 int, b2 int) no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a05v1 as select * from a05tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a05v2 as select * from a05tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop table a05tab1 cascade invalidate;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create or replace view a05v1(a,b) as select a1,b1 from a05tab2 where a1>0;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create or replace  view a05v2(aa,bb) as select a1,a2 from a05tab2,a05tab3 where b1=b2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop schema  my_schema5 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

    
def testa06(desc="""create/create or replace  an existing view v1 new view has more/less column than old"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
 
    mydci = basic_defs.switch_session_qi_user2()

    stmt = """create shared schema my_schema6;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema my_schema6;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a06tab1(col1 int not null primary key , col2 varchar(10));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a06tab2(a int , b varchar(10)) no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a06tab3(a1 int , b1 int) no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a06tab4(a2 int not null primary key , b2 varchar(10));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a06v1 as select * from a06tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a06v2(col1,col2) as select b,b1 from a06tab2, a06tab3 where a=a1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop table a06tab1 cascade invalidate;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop table a06tab2 cascade invalidate;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a06tab1(col1 int not null primary key , col2 varchar(10), col3 varchar(8));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create or replace  view a06v1 as select * from a06tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create or replace view a06v2(col1,col2,col3) as select a1,b1,b2 from a06tab3, a06tab4 where a1=a2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create or replace  view a06v2 as select * from a06tab4 ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a06tab4 values(1,'adsf');"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)

    stmt = """select * from a06v2;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,1)  

    stmt = """drop schema my_schema6 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

 
def testa07(desc="""u1 create/create or replace an existing view v1 verify v1's privileges"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """create shared schema my_schema7;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """set schema my_schema7;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a07tab1(col1 int not null primary key , col2 varchar(10));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a07tab2(a int , b varchar(10)) no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a07tab3(col1 int not null primary key , col2 varchar(10));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a07tab4(a int , b varchar(10)) no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a07tab3 values(1,'1'),(2,'2');"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,2)

    stmt = """create view a07v1 as select * from a07tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a07v2 as select * from a07tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant select on a07v1 to  qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant select on a07v1 to  qauser_tsang;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #stmt = """grant select ,insert on a07v2 to qauser_tsang with grant option;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    stmt = """grant select ,insert on a07v2 to qauser_tsang;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop table a07tab1 cascade invalidate;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop table a07tab2 cascade invalidate;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create or replace  view a07v1 as select * from a07tab3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create or replace  view a07v2 as select * from a07tab3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user3()

    stmt = """set schema my_schema7;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select * from a07v1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,2) 

    stmt = """select * from a07v2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    mydci = basic_defs.switch_session_qi_user4()

    stmt = """set schema my_schema7;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select * from a07v1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,2)

    stmt = """insert into a07v2 values(1,'adsf');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '8102')

    stmt = """insert into a07v2 values(3,'adsf');"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)

    stmt = """select * from a07v2;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,3)

    #stmt = """grant select on a07v2 to qauser_sqlqab,qauser_teg with grant option;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    stmt = """grant select on a07v2 to qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant select on a07v2 to qauser_teg;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """drop schema my_schema7 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

    
def testa08(desc="""db__root create or replace view on other user's schema """):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """create shared schema my_schema8;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a08tab1(a int , b varchar(10)) no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a08view1 as select * from a08tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema my_schema8;"""
    output = _dci.cmdexec(stmt)

    stmt = """create or replace view a08view1 as select * from a08tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """drop schema my_schema8 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def testa09(desc="""user granted db__rootrole create or replace view on other user's schema  """):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    stmt = """grant role db__rootrole to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """create shared schema my_schema9;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a09tab1(a int , b varchar(10)) no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a09view1 as select * from a09tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user3()

    stmt = """set schema my_schema9;"""
    output = mydci.cmdexec(stmt)

    stmt = """create or replace view a09view1 as select * from a09tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema my_schema9;"""
    output = mydci.cmdexec(stmt)

    stmt = """grant select on a09tab1 to qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)

    mydci = basic_defs.switch_session_qi_user3()

    stmt = """set schema my_schema9;"""
    output = mydci.cmdexec(stmt)

    stmt = """create or replace view a09view1 as select * from a09tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """drop schema my_schema9 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """revoke role db__rootrole from qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

def testa10(desc="""user granted delete on the view to create or replace view on other user's schema """):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """create shared schema my_schema10;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a10tab1(a int , b varchar(10)) no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a10view1 as select * from a10tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant select on a10tab1 to qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)	

    stmt = """grant delete on a10view1 to qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)	

    mydci = basic_defs.switch_session_qi_user3()

    stmt = """set schema my_schema10;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create or replace view a10view1 as select * from a10tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """drop schema my_schema10 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def testa11(desc="""create shared schema authoration to role graneted to user1 and user2 """):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    stmt = """create role rerole11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant role  rerole11 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant role  rerole11 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create schema my_schema11 authoration to rerole11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema my_schema11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a11tab1(a int , b varchar(10)) no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a11view1 as select * from a11tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user3()

    stmt = """set schema my_schema11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create or replace view a11view1 as select * from a11tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop schema my_schema11 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke role  rerole11 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke role  rerole11 from qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role rerole11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


    _testmgr.testcase_end(desc)

def testa12(desc="""create private schema authoration to role graneted to user1 and user2 """):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    stmt = """create role rerole12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant role  rerole12 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant role  rerole12 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create schema my_schema12 authoration to rerole12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema my_schema12;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a12tab1(a int , b varchar(10)) no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a12view1 as select * from a12tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user3()

    stmt = """set schema my_schema12;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create or replace view a12view1 as select * from a11tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')

    stmt = """grant component privilege "CREATE" on sql_operations to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema my_schema12;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant select on a12tab1 to qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant delete  on a12view1 to qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user3()

    stmt = """set schema my_schema12;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create or replace view a12view1 as select * from a11tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop schema my_schema12 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """revoke role  rerole12 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke role  rerole12 from qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role rerole12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


    _testmgr.testcase_end(desc)

    
def testa13(desc="""user create or replace  a view which is depends on different tables/views.u1 has no/has privileges on all tables/views"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """create shared schema my_schema13;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema my_schema13;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a13tab1(a1 int, b1 int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a13tab2(a2 int, b2 int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a13tab3(a3 int not null primary key, b3 varchar(12));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a13v1 as select * from a13tab1;""" 
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a13v2(col1,col2,col3) as select a2,b2,b3 from a13tab2,a13tab3 where a3>0;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a13v3 as select * from a13tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #stmt = """grant create,drop ,alter on schema my_schema13 to qauser_sqlqab ,qauser_tsang with grant option;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """grant select on a13v1 to qauser_sqlqab,qauser_tsang with grant option;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    
    stmt = """grant select on a13v1 to qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """grant select on a13v1 to qauser_tsang;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #stmt = """grant select on a13tab3 to qauser_sqlqab with grant option;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    
    stmt = """grant select on a13tab3 to qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """grant select on a13tab3 to qauser_tsang;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #stmt = """drop table a13tab2 cascade invalidate;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema my_schema13;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create or replace view a13v2(col1,col2) as select a1,b3 from a13tab3,a13v1 where b1=a3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    #mydci.expect_complete_msg(output)
    
    stmt = """create or replace view a13v13(col1,col2) as select a1,b3 from a13tab3,a13v1 where b1=a3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user4()

    stmt = """set schema my_schema13;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create or replace  view a13v4(col1,col2) as select a1,b3 from a13tab3,a13v1 where b1=a3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()

    stmt = """set schema my_schema13;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant select on a13tab3 to qauser_tsang ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1012')

    mydci = basic_defs.switch_session_qi_user4()

    stmt = """set schema my_schema13;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create or replace  view a13v4(col1,col2) as select a1,b3 from a13tab3,a13v1 where b1=a3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema my_schema13;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select * from a13v2;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,0)

    stmt = """select * from a13v3;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,0)

    stmt = """drop schema my_schema13 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)


    

    
def testa15(desc="""grant privileges on view to user/role"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    #process supermxci

    stmt = """create role rp_a19role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant role rp_a19role1 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """create shared schema my_schema19;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema my_schema19;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a19tab1(a1 int not null primary key, b1 varchar(10));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a19tab2(a2 int not null primary key, b2 varchar(10));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a19v1 as select * from a19tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a19v2(col1,col2) as select b1,b2 from a19v1,a19tab2 where a1>a2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #stmt = """drop table a19tab1 cascade invalidate;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    stmt = """select * from a19v1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt = """select * from a19v2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    #stmt = """grant select ,insert on a19v1 to rp_a19role1 with grant option;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    
    stmt = """grant select ,insert on a19v1 to rp_a19role1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant select(col1,col2) ,insert on a19v2 to  qauser_tsang;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #process supermxci
    stmt = """set schema my_schema19;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop schema my_schema19 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke role rp_a19role1 from qauser_sqlqab ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role rp_a19role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

    
def testa16(desc="""revoke privileges on view from user/role"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    #process supermxci

    stmt = """create role rp_a20role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant role rp_a20role1 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


    mydci = basic_defs.switch_session_qi_user2()

    stmt = """create shared schema my_schema20;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema my_schema20;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a20tab1(a1 int not null primary key, b1 varchar(10));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a20tab2(a2 int not null primary key, b2 varchar(10));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a20v1 as select * from a20tab1;"""
    output = mydci.cmdexec(stmt)

    stmt = """create view a20v2(col1,col2) as select b1,b2 from a20v1,a20tab2 where a1>a2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #stmt = """grant all on a20v1 to rp_a20role1 with grant option;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    
    stmt = """grant all on a20v1 to rp_a20role1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant select(col1,col2) on a20v2 to qauser_tsang;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """grant select, insert on a20v1 to qauser_teg;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user3()

    stmt = """set schema my_schema20;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a20v1 values(1,'adf');"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)

    #stmt = """grant select, insert on a20v1 to qauser_teg with grant option granted by  rp_a20role1;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema my_schema20;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop table a20tab1 cascade invalidate;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """revoke select(col1,col2) on a20v2 from  qauser_tsang;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a20tab1(a1 int not null primary key, b1 varchar(10));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """alter view a20v1 compile;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """alter view a20v2 compile;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #process supermxci

    stmt = """set schema my_schema20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #stmt = """revoke all on a20v1 from  qauser_teg granted by rp_a20role1;"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user5()

    stmt = """set schema my_schema20;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a20v1 values(2,'da');"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)
    
    stmt = """grant select on a20v1 to  qauser_tsang;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1012')

    mydci = basic_defs.switch_session_qi_user3()

    stmt = """set schema my_schema20;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a20v1 values(3,'da');"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)

    stmt = """select * from a20v1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,2)

    mydci = basic_defs.switch_session_qi_user4()

    stmt = """set schema my_schema20;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select * from a20v2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    #process supermxci

    stmt = """drop schema my_schema20 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke role rp_a20role1 from qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role rp_a20role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)
    
def testa17(desc="""revoke role which has dependent view from users restrict"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    #process supermxci

    stmt = """create role rp_a22role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role rp_a22role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant role rp_a22role1,rp_a22role2 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create shared schema my_schema22;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


    stmt = """set schema my_schema22;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #stmt = """grant create on schema my_schema22 to qauser_sqlqab;"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_complete_msg(output)

    stmt = """create table a22tab1(a1 int not null primary key, b1 varchar(10));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table a22tab2(a2 int ,b2 varchar(10))no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create view a22v1 as select * from a22tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant select on a22tab2 to rp_a22role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #stmt = """grant select on a22v1 to rp_a22role2 with grant option;"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_complete_msg(output)

    stmt = """grant select on a22v1 to rp_a22role2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user3()

    stmt = """set schema my_schema22;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a22v3(col1,col2) as select b1,b2 from a22v1,a22tab2 where a1=a2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #process supermxci

    stmt = """set schema my_schema22;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #stmt = """drop  table a22tab2 cascade invalidate;"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_complete_msg(output)

    #stmt = """drop  table a22tab1 cascade invalidate;"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_complete_msg(output)

    stmt = """revoke role rp_a22role1 from qauser_sqlqab ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1364')

    stmt = """revoke role rp_a22role2 from qauser_sqlqab restrict;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1364')

    mydci = basic_defs.switch_session_qi_user3()

    stmt = """set schema my_schema22;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select * from a22v3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0) 

    #process supermxci

    stmt = """set schema my_schema22;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop view a22v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop view a22v1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke role rp_a22role2 from qauser_sqlqab restrict;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)



    stmt = """drop role rp_a22role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop schema my_schema22 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """revoke role rp_a22role1 from qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop role rp_a22role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)
    

    

def testa18(desc="""drop role r1 user with r1 owns view"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    #process supermxci

    stmt = """create role rp_a27role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant role rp_a27role1 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #create shared schema my_schema27;"""

    stmt = """create shared schema my_schema27;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """set schema my_schema27;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table a27tab1(a1 int not null primary key, b1 varchar(10));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant select on a27tab1 to rp_a27role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #stmt = """grant create on schema my_schema27 to qauser_sqlqaa;"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()
    #connect qauser_sqlqaa/QAPassword;"""
    stmt = """set schema my_schema27;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a27v1 as select * from a27tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #process supermxci

    stmt = """set schema my_schema27;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #stmt = """drop table a27tab1 cascade invalidate;"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_complete_msg(output)

    stmt = """drop role rp_a27role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1348')

    stmt = """revoke role rp_a27role1 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1364')
    
    stmt = """select * from a27v1;"""
    output = _dci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)  

    stmt = """drop schema my_schema27 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """revoke role rp_a27role1 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role rp_a27role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

  
    _testmgr.testcase_end(desc)


def testa19(desc="""drop view then revoke role from r1 drop r1"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    #process supermxci

    stmt = """create role rp_a28role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant role rp_a28role1 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #create shared schema my_schema28a;

    stmt = """create shared schema my_schema28a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """set schema my_schema28a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table a28tab1(a1 int, b1 int, c1 varchar(10))no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant select on a28tab1 to rp_a28role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()

    #create shared schema my_schema28b;"""

    stmt = """create shared schema my_schema28b;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)


    stmt = """set schema my_schema28b;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a28tab2(a2 int, b2 varchar(10))no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a28v1(col1,col2) as select c1,b2 from a28tab2,my_schema28a.a28tab1 where a1=a2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #process supermxci

    stmt = """set schema my_schema28a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #stmt = """drop table a28tab1 cascade invalidate;"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_complete_msg(output)

    stmt = """select * from my_schema28b.a28v1;"""
    output = _dci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)  

    stmt = """drop view my_schema28b.a28v1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table my_schema28b.a28tab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke role rp_a28role1 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop schema my_schema28a cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role rp_a28role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop schema my_schema28b cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

    
def testa20(desc="""create a role with admin user1 user1 owns view, drop role"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    #process supermxci

    stmt = """create role rp_a29role1 with admin qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create shared schema my_schema29;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """set schema my_schema29;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table a29tab1(a1 int, b1 int, c1 varchar(10))no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant select on a29tab1 to rp_a29role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #stmt = """grant create on schema my_schema29 to qauser_sqlqaa;"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema my_schema29;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a29v1 as select * from a29tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #process supermxci

    stmt = """set schema my_schema29;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #stmt = """drop table a29tab1 cascade invalidate;"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_complete_msg(output)

    stmt = """select * from a29v1;"""
    output = _dci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0) 

    stmt = """drop role rp_a29role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1228')

    stmt = """drop view a29v1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop schema my_schema29 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop role rp_a29role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)



def testa21(desc="""create or replace view which has some dependent view u1 has privielges on dependent view I"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """create shared schema my_schema32;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema my_schema32;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a32tab1(a1 int, b1 int, c1 varchar(10))no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a32tab2(a2 int, b2 int, c2 varchar(10))no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a32view1 as select * from a32tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a32view2(col1,col2) as select c1,c2 from a32view1, a32tab2 where a1=a2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #stmt = """grant create,drop, alter,select on schema my_schema32 to qauser_sqlqab;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    
    stmt = """grant select on a32tab1 to qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """grant select on a32view1 to qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """grant select on a32view2 to qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """grant select on a32tab2 to qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()

    stmt = """set schema my_schema32;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a32view3 as select * from a32view2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create or replace view a32view1(a1,c1) as select a1,c1 from a32tab1 where b1>0;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')

    stmt = """select * from a32view2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt = """select * from a32view3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)


    stmt = """select * from a32view2;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,0)  

    stmt = """select * from a32view3;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,0)  

    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """drop  schema my_schema32 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

    
def testa22(desc="""u1 create or replace view which has some dependent view u1 has privielges on dependent view II"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """create shared schema my_schema33;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema my_schema33;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a33tab1(a1 int, b1 int, c1 varchar(10))no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a33tab2(a2 int, b2 int, c2 varchar(10))no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a33view1 as select * from a33tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a33view2(col1,col2) as select c1,c2 from a33view1, a33tab2 where a1=a2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #stmt = """grant create ,drop, alter,select on schema my_schema33 to qauser_sqlqab;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    
    stmt = """grant select on a33tab1 to qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """grant select on a33tab2 to qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """grant select on a33view1 to qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """grant select on a33view2 to qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user3()

    stmt = """set schema my_schema33;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a33view3 as select * from a33view2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create or replace view a33view1(a1,c1) as select a1,b1 from a33tab1 where b1>0;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')

    stmt = """select * from a33view2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0) 

    stmt = """select * from a33view3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0) 

    stmt = """select * from a33view2;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,0) 

    stmt = """select * from a33view3;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,0) 

    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """drop  schema my_schema33 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

    
def testa23(desc="""create or replace view which has some dependent view u1 has privileges on dependent view"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """create shared schema my_schema34;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema my_schema34;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a34tab1(a1 int, b1 int, c1 varchar(10))no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a34tab2(a2 int, b2 int, c2 varchar(10))no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a34view1 as select * from a34tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a34view2(col1,col2) as select c1,c2 from a34view1, a34tab2 where a1=a2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #stmt = """grant create ,select,alter,drop on schema my_schema34 to qauser_sqlqab;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    
    stmt = """grant select on a34tab1 to qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """grant select on a34tab2 to qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant select on a34view2 to  qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #stmt = """drop table a34tab2 cascade invalidate;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user3()

    stmt = """set schema my_schema34;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create or replace view cascade a34view1(a1,c1)  as select a1,b1 from a34tab1 where b1>0 ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')

    stmt = """create view a34view3 as select * from a34view2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select * from a34view2;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,0) 

    stmt = """select * from a34view3;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,0) 

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """drop schema my_schema34 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

    
def testa24(desc="""u1 create or replace view cascade which has some dependent view u1 has no privileges on dependent view"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """create shared schema my_schema35;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema my_schema35;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a35tab1(a1 int, b1 int, c1 varchar(10))no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a35tab2(a2 int, b2 int, c2 varchar(10))no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a35view1 as select * from a35tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a35view2(col1,col2) as select c1,c2 from a35view1, a35tab2 where a1=a2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #stmt = """grant create ,drop ,alter on schema my_schema35 to qauser_sqlqab;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    stmt = """grant select on a35tab1 to qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant select on a35view1 to qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """grant select on a35view1 to qauser_tsang;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant select on a35view2 to qauser_tsang;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user3()

    stmt = """set schema my_schema35;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a35view3 as select * from a35view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create or replace view cascade a35view1(a1,c1)  as select a1,b1 from a35tab1 where b1>0  ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema my_schema35;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop table a35tab2 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user3()

    stmt = """set schema my_schema35;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create or replace view a35view(a1,c1)  as select a1,b1 from a35tab1 where b1>0   ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop schema my_schema35 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)



def testa25(desc="""verify the old view definition is dropped and new definition is created"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    mydci = basic_defs.switch_session_qi_user2()

    stmt = """create shared schema my_schema36;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema my_schema36;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a36tab1(a1 int, b1 int, c1 varchar(10))no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a36tab2(a2 int, b2 int, c2 varchar(10))no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a36view1 as select * from a36tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a36view2(col1,col2) as select c1,c2 from a36view1, a36tab2 where a1=a2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create or replace view a36view1(a1,c1)  as select a1,b1 from a36tab1 where b1>0   ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create or replace view a36view2(col1,col2) as select c1,c2 from a36view1, a36tab2 where a1=a2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt = """ showddl a36view1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_any_substr(output,'CREATE OR REPLACE VIEW TRAFODION.MY_SCHEMA36.A36VIEW1 (A1, C1) AS' )
    mydci.expect_any_substr(output,'SELECT TRAFODION.MY_SCHEMA36.A36TAB1.A1, TRAFODION.MY_SCHEMA36.A36TAB1.B1' )
    mydci.expect_any_substr(output,'FROM TRAFODION.MY_SCHEMA36.A36TAB1 WHERE TRAFODION.MY_SCHEMA36.A36TAB1.B1' )
    mydci.expect_any_substr(output,'> 0 ;' )    
    
    stmt = """ showddl a36view2;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_any_substr(output,'CREATE OR REPLACE VIEW TRAFODION.MY_SCHEMA36.A36VIEW2 (COL1, COL2) AS' )
    mydci.expect_any_substr(output,'SELECT TRAFODION.MY_SCHEMA36.A36VIEW1.C1, TRAFODION.MY_SCHEMA36.A36TAB2.C2' )
    mydci.expect_any_substr(output,'FROM TRAFODION.MY_SCHEMA36.A36VIEW1, TRAFODION.MY_SCHEMA36.A36TAB2 WHERE' )
    mydci.expect_any_substr(output,'TRAFODION.MY_SCHEMA36.A36VIEW1.A1 = TRAFODION.MY_SCHEMA36.A36TAB2.A2 ;' )       
    
    stmt = """ drop schema my_schema36 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 
    
    _testmgr.testcase_end(desc)
    
def testa26(desc="""create or replace a valid view, verify the privileges on the new view"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    mydci = basic_defs.switch_session_qi_user2()

    stmt = """create shared schema my_schema37;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema my_schema37;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a37tab1(a1 int, b1 int) no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a37tab2(c1 int, c2 int) no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt = """create view a37view1 as select * from a37tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 

    stmt = """ grant select on a37view1 to qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 
    
    stmt = """ grant insert on a37view1 to qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)     
    
    
    stmt = """set schema my_schema37;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create or replace view a37view1 as select * from a37tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)     

    mydci = basic_defs.switch_session_qi_user3()

    stmt = """set schema my_schema37;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from  a37view1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,0)   

    stmt = """ insert into a37view1 values(1,2);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """drop schema my_schema37 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)  

    _testmgr.testcase_end(desc)
    


def testa27(desc="""create or replace an invalid view, verify the privileges on the new view"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    mydci = basic_defs.switch_session_qi_user2()

    stmt = """create shared schema my_schema38;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema my_schema38;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a38tab1(a1 int, b1 int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a38tab2(c1 int, c2 int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt = """create view a38view1 as select * from a38tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 

    stmt = """ grant select on a38view1 to qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 
    
    stmt = """ grant insert on a38view1 to qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)     
    
    stmt = """ drop table a38tab1 cascade invalidate;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 
    
    
    stmt = """set schema my_schema38;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create or replace view a38view1 as select * from a38tab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)     

    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema my_schema38;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from a38view1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,0)   

    stmt = """ insert into a38view1 values(1,2);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """drop schema my_schema38 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)  

    _testmgr.testcase_end(desc)
    
def testa28(desc="""veirfy dependent views will be marked invalid after create or replace view"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    mydci = basic_defs.switch_session_qi_user2()

    stmt = """create shared schema my_schema39;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema my_schema39;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a39tab1(a1 int, b1 int, c1 varchar(10))no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a39tab2(a2 int, b2 int, c2 varchar(10))no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a39view1 as select * from a39tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a39view2(col1,col2) as select c1,c2 from a39view1, a39tab2 where a1=a2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create or replace view a39view1 as select * from a39tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt = """ select * from a39view2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')    
    
    stmt = """drop schema my_schema39 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    _testmgr.testcase_end(desc)
    
def testa29(desc="""verify create or replace view cascade will bring back the dependent view to valid """):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    mydci = basic_defs.switch_session_qi_user2()

    stmt = """create shared schema my_schema40;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema my_schema40;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a40tab1(a1 int, b1 int, c1 varchar(10))no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a40tab2(a2 int, b2 int, c2 varchar(10))no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a40view1 as select * from a40tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a40view2(col1,col2) as select c1,c2 from a40view1, a40tab2 where a1=a2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create or replace view cascade a40view1 as select * from a40tab1 ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt = """ select * from a40view2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')       
    
    stmt = """drop schema my_schema40 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)     
    
    _testmgr.testcase_end(desc)
    
    
def testa30(desc="""different users create or replace views, verify the view owner is same as the original"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    mydci = basic_defs.switch_session_qi_user2()    

    stmt = """create shared schema my_schema41;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema my_schema41;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a41tab1(a1 int, b1 int, c1 varchar(10))no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)   
    
    stmt = """create table a41tab2(a2 int, b2 int, c2 varchar(10))no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a41view1 as select * from a41tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 

    stmt = """set schema my_schema41;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create or replace view a41view1 as select * from a41tab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """Select OBJECT_NAME from "_MD_".OBJECTS where OBJECT_NAME ='A41VIEW1'  and SCHEMA_NAME = 'MY_SCHEMA41' and OBJECT_OWNER= (select AUTH_ID from "_MD_".AUTHS where AUTH_DB_NAME = 'QAUSER_SQLQAA');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output,0)
    
    stmt = """Select OBJECT_NAME from "_MD_".OBJECTS where OBJECT_NAME ='A41VIEW1'  and SCHEMA_NAME = 'MY_SCHEMA41' and OBJECT_OWNER= (select AUTH_ID from "_MD_".AUTHS where AUTH_DB_NAME = 'DB__ROOT');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output,1)

    mydci = basic_defs.switch_session_qi_user2() 

    stmt = """drop schema my_schema41 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)









