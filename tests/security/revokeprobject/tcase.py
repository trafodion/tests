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


def testa01(desc="""revoke all,single dml,multiple dml on obj from role/users"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
 
    stmt = 'create role reobj_a01role1;'
    output = _dci.cmdexec(stmt)

    stmt   = 'create role reobj_a01role2;'
    output = _dci.cmdexec(stmt)

    stmt  ='create role reobj_a01role3;'
    output = _dci.cmdexec(stmt)
	
    stmt  ='create schema rev_sch1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='set schema rev_sch1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='create table a01tab1(col1 int, col2 int, col3 varchar(10))no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a01tab2(col1 int not null primary  key, col2 varchar(10));'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    

    stmt  ='grant all on a01tab1 to reobj_a01role1;'    
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='grant all on a01tab1 to reobj_a01role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select , delete , update on a01tab2 to reobj_a01role3;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='grant insert, delete ,references on a01tab2 to qauser_tsang with grant option;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a01role1 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a01role2  to qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a01role3 to qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke all on a01tab1 from reobj_a01role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke  update on a01tab1 from reobj_a01role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke delete on a01tab1 from reobj_a01role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select on a01tab2 from reobj_a01role3;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke references on a01tab2 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
        
    stmt  ='revoke insert on a01tab2 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
        

    mydci = basic_defs.switch_session_qi_user2()      
    stmt  ='set schema rev_sch1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a01tab1 values(1,2,\'sd\');'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    
    
    stmt  ='select * from a01tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    

    stmt  ='update a01tab1 set col2=col2+1 where col1>0;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    

    stmt  ='delete from a01tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    
    
    stmt  ='insert into a01tab2 values(1,\'sd\');'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    
    
    mydci = basic_defs.switch_session_qi_user3()      
    stmt  ='set schema rev_sch1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    ;
    
    stmt  ='insert into a01tab1 values(1,2,\'sd\');'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt  ='select * from a01tab1 where col2>0;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1) 
    
    stmt  ='delete from a01tab1 where col2>0;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    ;

    stmt  ='update a01tab1 set col3=\'dsf\';'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')   

    mydci = basic_defs.switch_session_qi_user4()  
    stmt  ='set schema rev_sch1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 
    
    stmt  ='select * from a01tab2 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
    
    stmt  ='delete from a01tab2 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,0)

    stmt  ='update a01tab2 set col2=\'ads\';'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  
    
    stmt  ='drop schema rev_sch1 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a01role1 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='revoke role reobj_a01role2 from qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='revoke role reobj_a01role3 from qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt   = 'drop role reobj_a01role1;'
    output = _dci.cmdexec(stmt)

    stmt   = 'drop role reobj_a01role2;'
    output = _dci.cmdexec(stmt)

    stmt  ='drop role reobj_a01role3;'
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)   
    
def testa02(desc="""revoke column level priv from roles/users"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    stmt   = 'create role reobj_a02role1;'
    output = _dci.cmdexec(stmt)

    stmt   = 'create role reobj_a02role2;'
    output = _dci.cmdexec(stmt)

    stmt  ='create role reobj_a02role3;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='create schema rev_sch2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a02tab1(col1 int, col2 int, col3 varchar(10))no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='create table a02tab2(col1 int , col2 varchar(10))no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant insert(col1,col2) on a02tab1 to reobj_a02role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select(col1,col2,col3) on a02tab1 to reobj_a02role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant insert(col1) on a02tab2 to reobj_a02role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select(col2) on a02tab2 to reobj_a02role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant update(col2) on a02tab2 to reobj_a02role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant insert(col1) on a02tab2 to reobj_a02role3;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='grant select(col1,col2) on a02tab2 to reobj_a02role3;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant insert(col2) on a02tab2 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant update(col2) on a02tab2 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a02role1 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a02role2 to qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a02role3 to qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke insert(col1,col2) on a02tab1 from reobj_a02role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke  select(col1,col2) on a02tab1 from reobj_a02role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select(col2) on a02tab2 from reobj_a02role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke insert(col1) on a02tab2 from reobj_a02role3;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select(col1,col2) on a02tab2 from reobj_a02role3;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke update(col2) on a02tab2 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    

    mydci = basic_defs.switch_session_qi_user2()     
    stmt  ='set schema rev_sch2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a02tab1 values(1,2,\'d\');'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')       
    
    stmt  ='insert into a02tab1(col1,col2) values(1,2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    

    stmt  ='insert into a02tab1(col1) values(1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    
    
    stmt  ='select * from a02tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    
    
    stmt  ='select col3 from a02tab1 where col1=1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    
    
    stmt  ='select col3 from a02tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt  ='insert into a02tab2(col1,col2) values(1,\'ad\');'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    
    
    stmt  ='insert into a02tab2(col2) values(\'ad\');'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    
    mydci = basic_defs.switch_session_qi_user3()     
    stmt  ='set schema rev_sch2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a02tab1(col1,col2) values(1,2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')      
    
    stmt  ='insert into a02tab2(col1,col2) values(1,\'ad\');'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')     

    stmt  ='insert into a02tab2(col1) values(1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)     
    
    stmt  ='update a02tab2 set col2=\'df\';'
    output = mydci.cmdexec(stmt)
    mydci.expect_updated_msg(output,2) 
    
    stmt  ='update a02tab2 set col2=\'sd\' where col2=\'df\';'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    
    
    stmt  ='select col2 from a02tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    mydci = basic_defs.switch_session_qi_user4() 
    stmt  ='set schema rev_sch2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='select col2 from a02tab2 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    
    
    stmt  ='insert into a02tab2(col1) values(1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    
    stmt  ='insert into a02tab2(col1,col2) values(1,\'df\');'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')        
    
    stmt  ='select * from a02tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')        
    
    stmt  ='select col1 from a02tab2 where col2=\'ds\';'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    
    
    stmt  ='drop schema rev_sch2 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
    
    stmt  ='revoke role reobj_a02role1 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
    
    stmt  ='revoke role reobj_a02role2 from qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
    
    stmt  ='revoke role reobj_a02role3 from qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt   = 'drop role reobj_a02role1;'
    output = _dci.cmdexec(stmt)

    stmt   = 'drop role reobj_a02role2;'
    output = _dci.cmdexec(stmt)

    stmt  ='drop role reobj_a02role3;'
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)  
 
def testa03(desc="""revoke mix obj and column level from roles/users"""):
        

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='create role reobj_a03role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='create role reobj_a03role2;'
    output = _dci.cmdexec(stmt)

    stmt  ='create schema rev_sch3;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch3;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a03tab1(col1 int, col2 int, col3 varchar(10))no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a03tab2(col1 int not null primary key, col2 varchar(10));'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='grant insert(col1,col2), select on a03tab1 to reobj_a03role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant update(col2), insert,select on a03tab2 to reobj_a03role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='grant insert(col1), select on a03tab2 to qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a03role1 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a03role2 to qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
    
    stmt  ='set schema rev_sch3;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke insert(col1),select on a03tab1 from reobj_a03role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
    
    stmt  ='revoke select on a03tab1 from reobj_a03role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke update(col2),insert on a03tab2 from reobj_a03role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    

    stmt  ='revoke insert(col1),select(col1) on a03tab2 from qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2() 
    stmt  ='set schema rev_sch3;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a03tab1(col1,col2) values(1,2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')     
    
    stmt  ='insert into a03tab1(col2) values(2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt  ='select col1 from a03tab1 where col2=2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')      

    stmt  ='select  * from a03tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')       

    mydci = basic_defs.switch_session_qi_user3() 
    stmt  ='set schema rev_sch3;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a03tab1 values(2,3,\'adf\');'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    

    stmt  ='insert into a03tab2 values(1, \'sd\');'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    
    
    stmt  ='select col1 from a03tab2 where col2 like \'s_\';'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt  ='select col1,col2 from a03tab2 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt  ='select * from a03tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
        
    stmt  ='update a03tab2 set col2=\'sdf\' ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    
    
    stmt  ='update a03tab2 set col1=col1+1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    

    mydci = basic_defs.switch_session_qi_user4() 
    stmt  ='set schema rev_sch3;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a03tab2(col1) values(3);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    
    
    stmt  ='insert into a03tab2 values(10,\'213\');'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    

    stmt  ='select col1 from a03tab2 where col2=\'sd\';'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt  ='select * from a03tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt  ='drop schema rev_sch3 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a03role1 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a03role2 from qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
    
    stmt  ='drop role reobj_a03role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='drop role reobj_a03role2;'
    output = _dci.cmdexec(stmt)    
    
    _testmgr.testcase_end(desc)  
     
def testa04(desc="""revoke blank,invalid,mulitiple_invalid,duplicate ...priv from roles/users"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='create role reobj_a04role1;'
    output = _dci.cmdexec(stmt)

    stmt  ='create role reobj_a04role2;'
    output = _dci.cmdexec(stmt)
        
    stmt  ='create schema rev_sch4;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch4;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a04tab1(col1 int, col2 int, col3 varchar(10))no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='grant insert(col1) on a04tab1 to reobj_a04role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant insert(col2) on a04tab1 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant insert ,select(col1) on a04tab1 to reobj_a04role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select on a04tab1 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a04role1 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke on a04tab1 from  reobj_a04role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt  ='revoke reobj_a04role2 on a04tab1 from reobj_a04role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')    
    
    stmt  ='revoke select ,qauser_tsang on a04tab1 from reobj_a04role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')    
        
    stmt  ='revoke qauser_tsang on a04tab1 from reobj_a04role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')    

    stmt  ='revoke a04tab1 on a04tab1 from reobj_a04role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')    

    stmt  ='revoke selection on a04tab1 from reobj_a04role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')    
    
    stmt  ='revoke create on a04tab1 from reobj_a04role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1328')   
        
    stmt  ='revoke create,select on a04tab1 from reobj_a04role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1328')
    
    stmt  ='revoke select ,create ,create_table on a04tab1 from reobj_a04role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1328')
    
    stmt  ='revoke insert,selection on a04tab1 from reobj_a04role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')    
    
    stmt  ='revoke select ,select on a04tab1 from reobj_a04role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1264')
    
    stmt  ='revoke select ,insert,select on a04tab1 from reobj_a04role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1264')

    stmt  ='revoke select,all on a04tab1 from reobj_a04role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')    
    
    stmt  ='revoke select(col2),select(col2) on a04tab1 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1264')
    
    stmt  ='revoke insert(col2), select(col2),select(col2) on a04tab1 from reobj_a04role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1264')

    mydci = basic_defs.switch_session_qi_user2()     
    stmt  ='set schema rev_sch4;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    

    stmt  ='insert into a04tab1 values(1,2,\'adf\');'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)

    stmt  ='insert into a04tab1(col1,col2) values(2,3);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt  ='select col1 from a04tab1 where col2=2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1);    
    
    stmt  ='delete from a04tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    stmt  ='drop schema rev_sch4 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a04role1 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop role reobj_a04role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)        
    
    stmt  ='drop role reobj_a04role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    

    _testmgr.testcase_end(desc)  
    
def testa05(desc="""revoke priv on objects(table,view,mv,..) from role/users;"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='create role reobj_a05role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
    
    stmt  ='create role reobj_a05role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
    
    stmt  ='create schema rev_sch5;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch5;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='create table a05tab1(col1 int, col2 int, col3 varchar(10))no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a05tab2(a int, b int, c varchar(10))no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='create view  a05view1 as select * from a05tab1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create view a05view2(a,c) as select a05tab1.col1, a05tab2.c from a05tab1,a05tab2 where a05tab1.col2=a05tab2.b;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create mv a05mv1 refresh on request initialize on refresh as select * from a05tab1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='maintain mv a05mv1, refresh;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create mv a05mv2 refresh on request initialize on refresh as select a05tab1.col1, a05tab2.c from a05tab1,a05tab2 where a05tab1.col2=a05tab2.b;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='maintain mv a05mv2, refresh;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create trigger a05trig1 after update on a05tab1 REFERENCING NEW AS newR FOR EACH ROW insert into a05tab1 values(1,2,\'dd\');'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create synonym syn_a05tab1 for a05tab1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create synonym syn_a05view1 for a05view1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create synonym syn_a05mv2 for a05mv2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
        
    stmt  ='grant select(col1,col2,col3) on a05tab1 to reobj_a05role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant insert(col1,col2,col3) on a05tab1 to reobj_a05role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant update on a05tab1 to reobj_a05role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select(col1,col2,col3) on a05view1 to reobj_a05role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select on a05tab2 to reobj_a05role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant insert on a05tab2 to reobj_a05role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select on a05view2 to reobj_a05role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='grant select on a05mv1 to reobj_a05role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select on a05mv2 to qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a05role1 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='grant role reobj_a05role2 to qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
        
    stmt  ='revoke select(col1,col2,col3) on a05tab1 from reobj_a05role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke insert(col1,col2,col3) on a05tab1 from reobj_a05role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke update on a05tab1 from reobj_a05role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select(col1,col2,col3) on a05view1 from reobj_a05role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select on a05tab2 from reobj_a05role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke insert on a05tab2 from reobj_a05role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select on a05view2 from reobj_a05role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
        
    stmt  ='revoke select on a05mv1 from reobj_a05role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select on a05mv2 from qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()     
    stmt  ='set schema rev_sch5;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)        

    stmt  ='insert into a05tab1 values(1,2,\'qw\');'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    

    stmt  ='update a05tab1 set col1=col1+1 where col2=2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    

    stmt  ='select * from a05tab1 where col2=2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    
        
    stmt  ='select * from syn_a05tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    
        
    stmt  ='insert into a05view1 values(2,3,\'we\');'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    

    stmt  ='select * from a05view1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    
    
    stmt  ='select * from syn_a05view1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    
    
    stmt  ='select * from a05view2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')   
    
    stmt  ='select * from a05mv1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    
    
    stmt  ='select * from a05mv2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    mydci = basic_defs.switch_session_qi_user3()     
    stmt  ='set schema rev_sch5;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)     
    
    stmt  ='insert into a05tab2 values(2,2,\'asd\'),(2,3,\'adf\');'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')   
        
    stmt  ='select * from a05tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  

    stmt  ='select * from a05tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
    
    stmt  ='select * from a05view1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  
    
    stmt  ='select * from a05view2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    

    stmt  ='select * from a05mv1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    
    
    stmt  ='select * from a05mv2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')     

    stmt  ='select * from syn_a05mv2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')     

    mydci = basic_defs.switch_session_qi_user4()     
    stmt  ='set schema rev_sch5;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    ;    
    
    stmt  ='select * from a05tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')          

    stmt  ='select * from a05tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')      

    stmt  ='select * from a05mv1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')     

    stmt  ='select * from a05mv2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    

    stmt  ='select * from syn_a05mv2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')   
    
    stmt  ='drop schema rev_sch5 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='revoke role reobj_a05role1 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a05role2 from qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop role reobj_a05role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop role reobj_a05role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
 
    _testmgr.testcase_end(desc)  
    
def testa06(desc="""revoke priv on multiple/duplicate/invalidvalue objects from role/users;"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='create role reobj_a06role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='create role reobj_a06role2;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='create schema rev_sch6;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch6;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a06tab1(col1 int ,col2 int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a06tab2(col1 int ,col2 int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create view a06view1 as select * from a06tab1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant all on a06tab1 to reobj_a06role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select,insert on a06tab2 to reobj_a06role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant  select,insert on a06view1 to reobj_a06role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select ,insert on a06tab1 to qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a06role1 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a06role2 to qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


    mydci = basic_defs.switch_session_qi_user2()     
    stmt  ='set schema rev_sch6;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a06tab1 values(1,1),(2,2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,2)
    
    stmt  ='select * from a06tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)
    
    stmt  ='delete from a06tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,2)
    
    stmt  ='insert into a06tab2 values(2,2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt  ='select col1,col2 from a06tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)
    
    stmt  ='select col1,col2 from a06view1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  

    mydci = basic_defs.switch_session_qi_user3()     
    stmt  ='set schema rev_sch6;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)  
    
    stmt  ='select * from a06tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    
    
    stmt  ='select * from a06view1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    mydci = basic_defs.switch_session_qi_user4()     
    stmt  ='set schema rev_sch6;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a06tab1(col1) values(1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt  ='insert into a06tab1(col2) values(2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt  ='select col1,col2 from a06tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)
    
    stmt  ='set schema rev_sch6;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke insert on a06tab1,a06tab2 from reobj_a06role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt  ='revoke delete on a06tab1,a06tab2 from reobj_a06role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt  ='revoke insert on a06view1,a06tab1 from reobj_a06role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt  ='revoke delete on a06tab2 ,a06tab2 from reobj_a06role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt  ='revoke select on a06tab2 ,a06view1 ,a06tab2 from reobj_a06role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt  ='revoke select on qauser_sqlqab from qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    stmt  ='revoke select on a from qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    stmt  ='revoke select on select from qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt  ='revoke insert on create from qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt  ='revoke all on test from qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    mydci = basic_defs.switch_session_qi_user4()     
    stmt  ='set schema rev_sch6;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a06tab1(col1) values(1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt  ='insert into a06tab1(col2) values(2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt  ='select col1,col2 from a06tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,4)

    mydci = basic_defs.switch_session_qi_user2() 
    stmt  ='set schema rev_sch6;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a06tab1 values(1,1),(2,2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,2)
    
    stmt  ='select * from a06tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,6)
    
    stmt  ='delete from a06tab1;'
    mydci.expect_deleted_msg(output,6)
    
    stmt  ='insert into a06tab2 values(2,2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt  ='select col1,col2 from a06tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)
    
    stmt  ='select col1,col2 from a06view1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  

    mydci = basic_defs.switch_session_qi_user3()     
    stmt  ='set schema rev_sch6;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt  ='select * from a06tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  
    
    stmt  ='select * from a06view1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,6)
    
    stmt  ='drop schema rev_sch6 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a06role1 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a06role2 from qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop role reobj_a06role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='drop role reobj_a06role2;'
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)  

def testa08(desc=""" revoke priv on object from role by one/multiple  role/users;"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='create role reobj_a08role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='create role reobj_a08role2;'
    output = _dci.cmdexec(stmt)    
    
    stmt  ='create schema rev_sch8;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch8;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a08tab1(col1 int, col2 int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create view a08view1 as select * from a08tab1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a08role1 to qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a08role2 to qauser_teg;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant all on a08tab1 to reobj_a08role1, qauser_tsang with grant option;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant all on a08view1 to qauser_sqlqaa with grant option;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select on a08tab1 to reobj_a08role2 by reobj_a08role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant insert on a08tab1 to reobj_a08role2 by qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant insert on a08tab1 to reobj_a08role2 by reobj_a08role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select, insert on a08view1 to reobj_a08role2 by qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user4()     
    stmt  ='set schema rev_sch8;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)   
    
    stmt  ='insert into a08tab1 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt  ='update a08tab1 set col1=col1+1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt  ='delete from a08tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,1)

    mydci = basic_defs.switch_session_qi_user5()     
    stmt  ='set schema rev_sch8;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 
    
    stmt  ='insert into a08tab1 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt  ='update a08tab1 set col1=col1+1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  
    
    stmt  ='delete from a08tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  
    
    stmt  ='select * from a08tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)
    
    stmt  ='insert into a08view1 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt  ='select * from a08view1 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)
    
    stmt  ='set schema rev_sch8;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select on a08tab1 from reobj_a08role2 by reobj_a08role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke insert on a08tab1 from reobj_a08role2 by reobj_a08role1,reobj_a08role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt  ='revoke insert on a08tab1 from reobj_a08role2 by reobj_a08role1,qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt  ='revoke select on a08view1 from reobj_a08role2 by qauser_sqlqaa,qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt  ='revoke insert on a08view1 from reobj_a08role2 by qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user5()     
    stmt  ='set schema rev_sch8;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a08tab1 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt  ='update a08tab1 set col1=col1+1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    
    
    stmt  ='delete from a08tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    
    
    stmt  ='select * from a08tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    
    
    stmt  ='insert into a08view1 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt  ='select * from a08view1 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    
    
    stmt  ='set schema rev_sch8;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop schema rev_sch8 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke  role reobj_a08role1 from qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a08role2 from qauser_teg;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop role reobj_a08role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='drop role reobj_a08role2;'
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)  
   
def testa09(desc="""revoke priv on col from role by one/multiple  role/users;"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='create role reobj_a09role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='create role reobj_a09role2;'
    output = _dci.cmdexec(stmt)    
    
    stmt  ='create schema rev_sch9;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch9;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a09tab1(col1 int, col2 int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a09tab2(col1 int not null primary key default 100, col2 int );'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='grant select(col1) on a09tab1 to qauser_tsang, reobj_a09role1 with grant option;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant insert(col2) on a09tab1 to qauser_tsang with grant option ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
    
    stmt  ='grant references(col1), insert(col2) on a09tab2 to reobj_a09role1 with grant option;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
    
    stmt  ='grant select(col1) ,insert(col2) on a09tab1 to qauser_teg by reobj_a09role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant insert(col2) on a09tab1 to qauser_teg by qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant references(col1) on a09tab2 to reobj_a09role2 by reobj_a09role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a09role2 to qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a09role1 to qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user3()     
    stmt  ='set schema rev_sch9;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a09tab1(col2) values(3);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    
    
    stmt  ='select * from a09tab1 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    
    
    stmt  ='select col1 from a09tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1) 

    mydci = basic_defs.switch_session_qi_user4()     
    stmt  ='set schema rev_sch9;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
        
    stmt  ='create table a09tab3(a int not null primary key, b int, c int, constraint tab2check foreign key (a) references a09tab2(col1));'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a09tab2(col2) values(2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    

    mydci = basic_defs.switch_session_qi_user5()     
    stmt  ='set schema rev_sch9;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a09tab1(col2) values(3);'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)
    
    stmt  ='select col1 from a09tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)
    
    stmt  ='set schema rev_sch9;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
    
    stmt  ='revoke select(col1) on a09tab1 from qauser_teg by reobj_a09role1,reobj_a09role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt  ='revoke select(col1) on a09tab1 from qauser_teg by qauser_tsang, reobj_a09role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt  ='revoke select(col1) on a09tab1 from qauser_teg by reobj_a09role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
    
    stmt  ='revovke insert(col2) on a09tab1 from qauser_teg by qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke references(col1), insert(col2) on a09tab2 from reobj_a09role2 by reobj_a09role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '1015')
    
    stmt  ='revoke references(col1) on a09tab2 from reobj_a09role2 by reobj_a09role1,qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    mydci = basic_defs.switch_session_qi_user5()     
    stmt  ='set schema rev_sch9;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)   
    
    stmt  ='insert into a09tab1(col2) values(3);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')   
    
    stmt  ='select col1 from a09tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')   

    mydci = basic_defs.switch_session_qi_user4() 
    stmt  ='set schema rev_sch9;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
        
    stmt  ='create table a09tab4(a int not null primary key, b int, c int, constraint tab4check foreign key (a) references a09tab2(col1));'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a09tab2(col2) values(2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    

    stmt  ='drop schema rev_sch9 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a09role2 from qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a09role1 from qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop role reobj_a09role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='drop role reobj_a09role2;'
    output = _dci.cmdexec(stmt)    
    
    _testmgr.testcase_end(desc)   
 
def testa10(desc="""revoke priv on object from role by invalid value;"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='create role reobj_a10role1;'    
    output = _dci.cmdexec(stmt)    
    
    stmt  ='create schema rev_sch10;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch10;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a10tab1(col1 int, col2 int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select on a10tab1 to reobj_a10role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant insert on a10tab1 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
        
    stmt  ='grant role reobj_a10role1 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2() 
    stmt  ='set schema rev_sch10;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a10tab1 values(1,2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt  ='select * from a10tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1) 

    stmt  ='delete from a10tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')      

    stmt  ='set schema rev_sch10;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select on a10tab1 from reobj_a10role1 by public;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')    
        
    stmt  ='revoke select on a10tab1 from reobj_a10role1 by test;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')    

    stmt  ='revoke insert on a10tab1 from qauser_tsang by a10tab1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt  ='revoke insert on a10tab1 from qauser_tsang by;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    mydci = basic_defs.switch_session_qi_user2()     
    stmt  ='set schema rev_sch10;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a10tab1 values(1,2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt  ='select * from a10tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)

    stmt  ='delete from a10tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')      

    stmt  ='set schema rev_sch10;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop schema rev_sch10 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a10role1 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop role reobj_a10role1;'
    output = _dci.cmdexec(stmt)        

    _testmgr.testcase_end(desc)  
    
def testa11(desc="""revoke priv on object from role by user/roles who cannot grant priv;"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='create role reobj_a11role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='create role reobj_a11role2;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='create schema rev_sch11;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch11;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a11tab1(col1 int,col2 int ,col3 varchar(10))no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create view a11view1(a,b) as select col1,col2 from a11tab1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role DB__rootrole to qauser_teg;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant insert on a11tab1 to qauser_sqlqaa with grant option;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant insert on a11tab1 to reobj_a11role1 by qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant insert on a11tab1 to reobj_a11role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select on a11view1 to qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select on a11view1 to reobj_a11role2 by db__root;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select on a11view1 to reobj_a11role1 by db__root;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user5()     
    stmt  ='set schema rev_sch11;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='revoke insert on a11tab1 from reobj_a11role1 by qauser_sqlqaa;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1012');

    
    stmt  ='revoke insert on a11tab1 from reobj_a11role2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1012');

    
    stmt  ='revoke select on a11view1 from qauser_sqlqab;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1012');

    
    stmt  ='revoke select on a11view1 from reobj_a11role2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1012')



    mydci = basic_defs.switch_session_qi_user3()     
    stmt  ='set schema rev_sch11;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='revoke insert on a11tab1 from reobj_a11role1 by qauser_sqlqaa;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    

    stmt  ='revoke insert on a11tab1 from reobj_a11role2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_warning_msg(output, '1015')
	

    
    stmt  ='revoke select on a11view1 from reobj_a11role2 by DB__ROOT;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1012')

    
    stmt  ='set schema rev_sch11;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke insert on a11tab1 from reobj_a11role1 by qauser_sqlqaa;' 
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke insert on a11tab1 from reobj_a11role1;'
    output = mydci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '1015')

    
    stmt  ='revoke insert on a11tab1 from qauser_sqlqaa restrict;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke insert on a11tab1 from reobj_a11role1 by qauser_sqlqab;'
    output = mydci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1017')

    
    stmt  ='revoke select on a11view1 from reobj_a11role2 by DB__ROOT;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select on a11view1 from reobj_a11role1 by DB__ROOT;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop schema rev_sch11 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role db__rootrole from qauser_teg;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop role reobj_a11role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='drop role reobj_a11role2;'
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)  
 
def testa12(desc="""revoke grant option for all on obj from role/users by(n);"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='create role reobj_a12role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='create role reobj_a12role2;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='create schema rev_sch12;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch12;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a12tab1(col1 int  not null primary key,col2 int ,col3 varchar(10));'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a12tab2(a int ,b int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant insert(col1,col2), select(col1,col2) on a12tab1 to reobj_a12role1 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant update(col2) on a12tab1 to reobj_a12role1 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt  ='grant update(col2) on a12tab1 to  reobj_a12role2 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	

    
    stmt  ='grant select on a12tab2 to reobj_a12role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt  ='grant select on a12tab2 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
		
    
    stmt  ='grant insert, update,delete on a12tab2 to reobj_a12role1 by DB__ROOT;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt  ='grant insert, update,delete on a12tab2 to  qauser_tsang, reobj_a12role2 by DB__ROOT;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='grant insert, update,delete on a12tab2 to  reobj_a12role2 by DB__ROOT;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a12role1,reobj_a12role2 to qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()     
    stmt  ='set schema rev_sch12;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='grant select, insert, update, delete on a12tab2 to qauser_sqlqaa with grant option;' 
    output = mydci.cmdexec(stmt)
    mydci.expect_warning_msg(output, '1012');

    mydci = basic_defs.switch_session_qi_user3()     
    stmt  ='set schema rev_sch12;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a12tab1 values(1,2,\'dfa\');'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='insert into a12tab1(col1,col2) values(2,2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt  ='select * from a12tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select col1 from a12tab1 where col2=2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)
    
    stmt  ='update a12tab1 set col2=1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_updated_msg(output,1)
    
    stmt  ='insert into a12tab2 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt  ='select * from a12tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)
    
    stmt  ='delete from a12tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,1)
    
    stmt  ='set schema rev_sch12;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke grant option for insert(col1,col2), select(col1,col2) on a12tab1 from reobj_a12role1 ;'
    output = mydci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '1015')

    
    stmt  ='revoke grant option for update(col2) on a12tab1 from reobj_a12role1, reobj_a12role2 ;'
    output = mydci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '1015')

    
    stmt  ='revoke grant option for select on a12tab2 from  reobj_a12role1, qauser_tsang ;'
    output = mydci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '1015')

    
    stmt  ='revoke grant option for insert, update,delete on a12tab2 from  reobj_a12role1, qauser_tsang, reobj_a12role2 by DB__ROOT;'
    output = mydci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '1015')


    mydci = basic_defs.switch_session_qi_user3() 
    stmt  ='set schema rev_sch12;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a12tab1 values(1,2,\'dfa\');'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='insert into a12tab1(col1,col2) values(2,2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt  ='select * from a12tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select col1 from a12tab1 where col2=2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)
    
    stmt  ='update a12tab1 set col2=1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_updated_msg(output,1)
    
    stmt  ='insert into a12tab2 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt  ='select * from a12tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)
    
    stmt  ='delete from a12tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)
    
    stmt  ='drop schema rev_sch12 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a12role1,reobj_a12role2 from qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop role reobj_a12role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='drop role reobj_a12role2;'
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)  
     
def testa13(desc="""grantor has no authority to revoke grant option for from role;"""): 

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='create role reobj_a13role1;'
    output = _dci.cmdexec(stmt)        

    stmt  ='create role reobj_a13role2;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='create schema rev_sch13 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch13 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
    
    stmt  ='create table a13tab1(col1 int, col2 int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='grant select on a13tab1 to qauser_tsang with grant option;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select,insert on a13tab1 to qauser_sqlqaa;' 
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select on a13tab1 to reobj_a13role1 by qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select on a13tab1 to reobj_a13role2 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a13role1 to qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a13role2 to qauser_teg;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user4()     
    stmt  ='set schema rev_sch13 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a13tab1 values(1,2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select * from a13tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0);

    mydci = basic_defs.switch_session_qi_user5()     
    stmt  ='set schema rev_sch13 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a13tab1 values(1,2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select * from a13tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    mydci = basic_defs.switch_session_qi_user2()     
    stmt  ='set schema rev_sch13 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='revoke grant option for select on a13tab1 from reobj_a13role1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1012')


    mydci = basic_defs.switch_session_qi_user3()     
    stmt  ='set schema rev_sch13 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='revoke grant option for select,insert on a13tab1 from reobj_a13role2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1012')

    
    stmt  ='set schema rev_sch13 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke grant option for select on a13tab1 from reobj_a13role1 by qauser_tsang;'
    output = mydci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '1015')
    
    stmt  ='revoke grant option for select,insert on a13tab1 from reobj_a13role2 by qauser_sqlqaa;'
    output = mydci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1017')

    
    stmt  ='revoke grant option for select on a13tab1 from reobj_a13role2 by DB__ROOT;'
    output = mydci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '1015')


    mydci = basic_defs.switch_session_qi_user4()     
    stmt  ='set schema rev_sch13 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a13tab1 values(1,2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481');
    
    stmt  ='select * from a13tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0);

    mydci = basic_defs.switch_session_qi_user5()     
    stmt  ='set schema rev_sch13 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a13tab1 values(1,2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481');
    
    stmt  ='select * from a13tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0);
    
    stmt  ='drop schema rev_sch13 cascade ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
    
    stmt  ='revoke role reobj_a13role1 from qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
    
    stmt  ='revoke role reobj_a13role2 from qauser_teg;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
    
    stmt  ='drop role reobj_a13role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='drop role reobj_a13role2;'
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)  
     
def testa14(desc="""syntax missing keywords, commas, ordering clauses, special rolenames;"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='create role reobj_a14role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='create role role ;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='create schema rev_sch14;' 
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch14;' 
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a14tab1(a int, b int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant all on a14tab1 to reobj_a14role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select ,insert on a14tab1 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant insert on a14tab1 to role;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role role ,reobj_a14role1 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()     
    stmt  ='set schema rev_sch14;' 
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a14tab1 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt  ='select * from a14tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1) 
    
    stmt  ='delete from a14tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,1);
    
    stmt  ='set schema rev_sch14;' 
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select on a14tab1 qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    
    stmt  ='revoke grant option for select on a14tab1 from reobj_a14role1 qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    
    stmt  ='revoke select insert on a14tab1 from reobj_a14role1 by DB__ROOT ,by qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    
    stmt  ='revoke all on a14tab1 from NONE;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt  ='revoke all on a14tab1 from _SYSTEM;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    
    stmt  ='revoke insert from qauser_tsang on a14tab1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    
    stmt  ='revoke insert on a14tab1 from role; '
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role role from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()     
    stmt  ='set schema rev_sch14;' 
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a14tab1 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt  ='select * from a14tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)
    
    stmt  ='delete from a14tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,1)

    stmt  ='drop schema rev_sch14 cascade;' 
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a14role1 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop role reobj_a14role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='drop role role;'
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)  
  
 
def testa15(desc="""revoke privs on object from predefine users/roles;"""): 

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='create schema rev_sch15;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch15;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a15tab1(col1 int, col2 int)no partition; '
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a15tab2(a int,b int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create view a15view1(c,d) as select a15tab1.col1,a15tab2.a from a15tab1,a15tab2 where a15tab1.col2=a15tab2.b;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select on a15tab1 to DB__SERVICES,DB__ROOT;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1008')
    
    stmt  ='grant insert on a15tab1 to db__rootrole;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1008')
    
    stmt  ='grant insert on a15tab2 to db__rootroleUSER,DB__ADMIN;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1008')
    
    stmt  ='grant select on a15view1 to DB__ADMIN, db__rootrole;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1008')
    
    stmt  ='grant all on a15tab2 to public;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant all on a15tab1 to current_user ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    
    stmt  ='grant select on a15tab1 to current_user; '
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')


    mydci = basic_defs.switch_session_qi_user2()     
    stmt  ='set schema rev_sch15;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a15tab1 values(1,2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt  ='select * from a15tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)
    
    stmt  ='insert into a15tab2 values(2,2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)
    
    stmt  ='select * from a15view1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)
    
    stmt  ='set schema rev_sch15;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select on a15tab1 from DB__SERVICES,DB__ROOT;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1008')
    
    stmt  ='revoke insert on a15tab1 from db__rootrole;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1008')
    
    stmt  ='revoke insert on a15tab2 from db__rootroleUSER,DB__ADMIN;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1008')
    
    stmt  ='revoke select on a15view1 from DB__ADMIN, db__rootrole;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1008')
    
    stmt  ='revoke all on a15tab2 from public;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke all on a15tab1 from current_user ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    
    stmt  ='revoke select on a15tab1 from current_user; '
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    
    stmt  ='drop schema rev_sch15 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)  
    
def testa16(desc="""revoke privs on object from role by predefined rolename/username;"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='create role reobj_a16role1 with admin db__root;'
    output = _dci.cmdexec(stmt)    
    
    stmt  ='create role reobj_a16role2;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='create schema rev_sch16;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch16;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a16tab1(a int,b int,c int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant insert(a,c),select(a) on a16tab1 to reobj_a16role1 by db__root ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant insert(b),select(b) on a16tab1 to reobj_a16role2 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a16role1 to qauser_tsang, qauser_sqlqaa granted by db__root;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
    
    stmt  ='grant role reobj_a16role2 to qauser_sqlqaa, qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user3()     
    stmt  ='set schema rev_sch16;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a16tab1 values(1,2,3);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt  ='select * from a16tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
        
    stmt  ='insert into a16tab1(b,c) values(1,3);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1);
    
    stmt  ='select a from a16tab1 where b=1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)
    
    stmt  ='select c from a16tab1 where b=1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select * from a16tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='set schema rev_sch16;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke insert(a,c),select(a) on a16tab1 from reobj_a16role1 by DB__ROOT;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke insert(b),select(b) on a16tab1 from reobj_a16role2 by DB__ROOT;'

    mydci = basic_defs.switch_session_qi_user3()     
    stmt  ='set schema rev_sch16;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a16tab1 values(1,2,3);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select * from a16tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='insert into a16tab1(b,c) values(1,3);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select a from a6tab1 where b=1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    stmt  ='select c from a16tab1 where b=1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select * from a16tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='drop schema rev_sch16 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a16role1 from qauser_tsang, qauser_sqlqaa granted by db__root;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a16role2 from qauser_sqlqaa,qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop role reobj_a16role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='drop role reobj_a16role2;'
    output = _dci.cmdexec(stmt)
 
    _testmgr.testcase_end(desc)  
    
def testa17(desc="""revoke priv from role ,verify user's priv that has/has not been granted to role"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='create role reobj_a17role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='create role reobj_a17role2;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='create schema rev_sch17;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch17;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a17tab1(col1 int,col2 int, col3 int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
        
    stmt  ='insert into a17tab1 values(1,2,3),(2,4,6);'
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,2)
    
    stmt  ='create table a17tab2(a int ,b varchar(10)) no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
    
    stmt  ='grant select on a17tab1 to reobj_a17role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select,insert on a17tab2 to reobj_a17role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a17role1 to qauser_tsang,qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a17role2 to qauser_sqlqaa,qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2() 
    stmt  ='set schema rev_sch17;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a17tab1 values(1,2,3);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select * from a17tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)
    
    stmt  ='insert into a17tab2 values(1,\'era\');'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select * from a17tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='create view a17view1(a,b) as select col1,col2 from a17tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='create view a17view2(a,b) as select a17tab1.col1,a17tab2.b from a17tab1,a17tab2 where a17tab1.col2=a17tab2.a;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    mydci = basic_defs.switch_session_qi_user3()     
    stmt  ='set schema rev_sch17;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='select * from a17tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)
    
    stmt  ='insert into a17tab2 values(2,\'adf\');'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt  ='select * from a17tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)
    
    stmt  ='select * from a17view1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select * from a17view2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')
    
    stmt  ='create view a17view3(a,b) as select a17tab1.col1,a17tab2.b from a17tab1,a17tab2 where a17tab1.col2=a17tab2.a;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='set schema rev_sch17;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select on a17tab1 from reobj_a17role1 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()     
    stmt  ='set schema rev_sch17;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a17tab1 values(1,2,3);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select * from a17tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='insert into a17tab2 values(1,\'era\');'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select * from a17tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='create view a7view4(a,b) as select col1,col2 from a17tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='create view a17view5(a,b) as select a17tab1.col1,a17tab2.b from a17tab1,a17tab2 where a17tab1.col2=a17tab2.a;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    mydci = basic_defs.switch_session_qi_user3()     
    stmt  ='set schema rev_sch17;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='select * from a17tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='insert into a17tab2 values(2,\'adf\');'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt  ='select * from a17tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)
    
    stmt  ='select * from a17view1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')
    
    stmt  ='select * from a17view2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')
    
    stmt  ='create view a17view6(a,b) as select a17tab1.col1,a17tab2.b from a17tab1,a17tab2 where a17tab1.col2=a17tab2.a;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    mydci = basic_defs.switch_session_qi_user4()     
    stmt  ='set schema rev_sch17;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='select * from a14tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='insert into a17tab2 values(2,\'adf\');'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt  ='select * from a17tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,3)
    
    stmt  ='select * from a17view1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')
    
    stmt  ='select * from a17view2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')
    
    stmt  ='create view a17view7(a,b) as select a17tab1.col1,a17tab2.b from a17tab1,a17tab2 where a17tab1.col2=a17tab2.a;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='create view a17view8 as select * from a17tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    

    stmt  ='drop schema rev_sch17 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a17role1 from qauser_tsang, qauser_sqlqaa;' 
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a17role2 from qauser_sqlqaa, qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop role reobj_a17role2;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='drop role reobj_a17role1;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)  
    

def testa18(desc="""revoke role from user, verify user's priv that is granted to role"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='create role reobj_a18role1;'
    output = _dci.cmdexec(stmt)

    stmt  ='create role reobj_a18role2;'
    output = _dci.cmdexec(stmt)

    stmt  ='create schema rev_sch18;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch18;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a18tab1(a int, b int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='grant insert on a18tab1 to reobj_a18role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select on a18tab1 to reobj_a18role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a18role1,reobj_a18role2 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2() 
    stmt  ='set schema rev_sch18;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a18tab1 values(1,2),(3,4);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,2)
    
    stmt  ='select * from a18tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)
   
    stmt  ='revoke role reobj_a18role1 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    time.sleep(5)
    
    mydci = basic_defs.switch_session_qi_user2()     
    stmt  ='set schema rev_sch18;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a18tab1 values(1,2),(3,4);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select * from a18tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)
    
    stmt  ='revoke role reobj_a18role2 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    time.sleep(5)
    
    mydci = basic_defs.switch_session_qi_user2()     
    stmt  ='set schema rev_sch18;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a18tab1 values(1,2),(3,4);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select * from a18tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='drop schema rev_sch18 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop role reobj_a18role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='drop role reobj_a18role2;'
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)  

 
def testa19(desc="""grant same priv to role and user,then revoke priv obj from role/users"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='create role reobj_a19role1; '
    output = _dci.cmdexec(stmt)
        
    stmt  ='create role reobj_a19role2; '
    output = _dci.cmdexec(stmt)

    stmt  ='create schema rev_sch19;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
        
    stmt  ='set schema rev_sch19;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='create table a19tab1(a int, b int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a19tab2(col1 int, col2 int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
    
    stmt  ='grant select, insert on a19tab1 to reobj_a19role1;' 
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='grant select, delete on a19tab1 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='grant select ,delete on a19tab2 to reobj_a19role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select,insert,update on a19tab2 to qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a19role1 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role  reobj_a19role2 to qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2() 
    stmt  ='set schema rev_sch19;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)        
    
    stmt  ='insert into a19tab1 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt  ='select * from a19tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)
    
    stmt  ='delete from a19tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,1)

    mydci = basic_defs.switch_session_qi_user3()     
    stmt  ='set schema rev_sch19;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)        

    stmt  ='insert into a19tab2 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt  ='select * from a19tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)
    
    stmt  ='delete from a19tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,1)
    
    stmt  ='set schema rev_sch19;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
    
    stmt  ='revoke select,insert on a19tab1 from reobj_a19role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
    
    stmt  ='revoke select,insert,update on a19tab2 from qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    

    mydci = basic_defs.switch_session_qi_user2()     
    stmt  ='set schema rev_sch19;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)        
    
    stmt  ='insert into a19tab1 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select * from a19tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)
    
    stmt  ='delete from a19tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,1)

    mydci = basic_defs.switch_session_qi_user3()     
    stmt  ='set schema rev_sch19;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)        

    stmt  ='insert into a19tab2 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select * from a19tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)
    
    stmt  ='delete from a19tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,1)
    
    stmt  ='create view a19view1 as select * froma 19tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)        

    stmt  ='drop schema rev_sch19 cascade;' 
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
        
    stmt  ='revoke role reobj_a19role1 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='revoke role reobj_a19role2 from qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
        
    stmt  ='drop role reobj_a19role1;'
    output = _dci.cmdexec(stmt)    
    
    stmt  ='drop role reobj_a19role2;'
    output = _dci.cmdexec(stmt)    
    
    _testmgr.testcase_end(desc)  
             
def testa20(desc="""grant priv to role, grant role to u1 and u2, revoke role from u1, verify priv"""):
    
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='create role reobj_a20role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='create schema rev_sch20;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch20;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a20tab1(col1 int, col2 int, col3 varchar(10))no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select ,insert on a20tab1 to reobj_a20role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a20role1 to qauser_tsang, qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()     
    stmt  ='set schema rev_sch20;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into  a20tab1 values(1,1,\'df\');'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt  ='select * from a20tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

    mydci = basic_defs.switch_session_qi_user3()     
    stmt  ='set schema rev_sch20;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into  a20tab1 values(1,1,\'df\');'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt  ='select * from a20tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)  
    
    stmt  ='set schema rev_sch20;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a20role1 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()     
    stmt  ='set schema rev_sch20;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into  a20tab1 values(1,1,\'df\');'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select * from a20tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    mydci = basic_defs.switch_session_qi_user3() 
    stmt  ='set schema rev_sch20;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into  a20tab1 values(1,1,\'df\');'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt  ='select * from a20tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,3)

    stmt  ='drop schema rev_sch20 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='revoke role reobj_a20role1 from qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='drop role reobj_a20role1;'
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)  
         
def testa22(desc="""grant priv on obj to role and user, then revoke priv from user and from role"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='create role reobj_a22role1;'    
    output = _dci.cmdexec(stmt)
    
    stmt  ='create role reobj_a22role2;'    
    output = _dci.cmdexec(stmt)
    
    stmt  ='create schema rev_sch22;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch22;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a22tab1(a int,b int,c int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select on a22tab1 to reobj_a22role1,qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant insert on a22tab1 to reobj_a22role2;' 
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a22role2,reobj_a22role1 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()     
    stmt  ='set schema rev_sch22;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a22tab1 values(1,1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt  ='select * from a22tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)
    
    stmt  ='create view a22view1 as select * from a22tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='set schema rev_sch22;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select on a22tab1 from reobj_a22role1,qauser_tsang cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()     
    stmt  ='set schema rev_sch22;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a22tab1 values(1,1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt  ='select * from a22view1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')
    
    stmt  ='drop view a22view1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')
    
    stmt  ='select * from a22ab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='create view a22view2 as select * from a22tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='drop schema rev_sch22 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a22role1,reobj_a22role2 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop role reobj_a22role2;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='drop role reobj_a22role1;'
    output = _dci.cmdexec(stmt)    
    
    _testmgr.testcase_end(desc)  
             
def testa23(desc="""grant priv on obj to role1,role2 ,user, then revoke priv from user, role1, role2"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='create role reobj_a23role2;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='create role reobj_a23role1;'
    output = _dci.cmdexec(stmt)

    stmt  ='create schema rev_sch23;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch23;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a23tab1(a int, b int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='insert into a23tab1 values(1,1);'
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt  ='create table a23tab2(col1 int, col2 int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select on a23tab1 to reobj_a23role2,reobj_a23role1,qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select, insert on a23tab2 to reobj_a23role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a23role1,reobj_a23role2 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2() 
    stmt  ='set schema rev_sch23;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a23tab2 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt  ='select * from a23tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)
    
    stmt  ='select * from a23tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)
    
    stmt  ='create view a23view1(aa,bb) as select a, col1 from a23tab1,a23tab2 where a23tab1.b=a23tab2.col2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='set schema rev_sch23;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select on a23tab1 from reobj_a23role2,qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2() 
    stmt  ='set schema rev_sch23;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a23tab2 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt  ='select * from a23tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)
    
    stmt  ='select * from a23tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)
    
    stmt  ='select * from a23view1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)
    
    stmt  ='create view a23view2(aa,bb) as select a, col1 from a23tab1,a23tab2 where a23tab1.b=a23tab2.col2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='drop schema rev_sch23 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role  reobj_a23role1,reobj_a23role2 from qauser_tsang;' 
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop role reobj_a23role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='drop role reobj_a23role2;'
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)  

     
def testa24(desc="""u1 was granted r1,r3,r4,revoke priv from r1, r2"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='create role reobj_a24role1;'
    output = _dci.cmdexec(stmt)    

    stmt  ='create role reobj_a24role2;'
    output = _dci.cmdexec(stmt)        

    stmt  ='create role reobj_a24role3;'
    output = _dci.cmdexec(stmt)        

    stmt  ='create role reobj_a24role4;'
    output = _dci.cmdexec(stmt)    

    stmt  ='create schema rev_sch24;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch24;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a24tab1(a int, b int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select,delete on a24tab1 to reobj_a24role1,reobj_a24role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant insert on a24tab1 to reobj_a24role3,reobj_a24role4;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='grant role reobj_a24role1,reobj_a24role3,reobj_a24role4 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()     
    stmt  ='set schema rev_sch24;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a24tab1 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt  ='select * from a24tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1) 
    
    stmt  ='create view a24view1 as select * from a24tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    

    stmt  ='set schema rev_sch24;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select on a24tab1 from reobj_a24role1 restrict;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1014')

    stmt  ='revoke insert on a24tab1 from reobj_a24role3;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    

    mydci = basic_defs.switch_session_qi_user2()     
    stmt  ='set schema rev_sch24;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
            
    stmt  ='insert into a24tab1 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt  ='select * from a24tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)         
            
    stmt  ='insert into a24view1 values(3,3);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 

    stmt  ='select * from a24view1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,3) 
    
    stmt  ='delete from a24view1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,3)   

    stmt  ='drop view a24view1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    

    stmt  ='create view a24view2 as select * from a24tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='drop schema rev_sch24 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a24role1,reobj_a24role3,reobj_a24role4 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
            
    stmt  ='drop role reobj_a24role1;'
    output = _dci.cmdexec(stmt)    

    stmt  ='drop role reobj_a24role2;'
    output = _dci.cmdexec(stmt)        

    stmt  ='drop role reobj_a24role3;'
    output = _dci.cmdexec(stmt)        

    stmt  ='drop role reobj_a24role4;'
    output = _dci.cmdexec(stmt)    

    _testmgr.testcase_end(desc)      
                         
def testa25(desc="""revoke priv from roles and users in a stat ,some of them are never granted priv"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='create role reobj_a25role1; '
    output = _dci.cmdexec(stmt)    

    stmt  ='create role reobj_a25role2; '
    output = _dci.cmdexec(stmt)    
    
    stmt  ='create role reobj_a25role3; '
    output = _dci.cmdexec(stmt)    

    stmt  ='create schema rev_sch25;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch25;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a25tab1(a int ,b int ,c int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='create table a25tab2(col1 int, col2 int ,col3 varchar(10))no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='create view a25view1 as select * from a25tab1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select on a25tab1 to reobj_a25role1,reobj_a25role2,qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
        
    stmt  ='grant select on a25tab2 to reobj_a25role2 ,reobj_a25role3 ,qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
        
    stmt  ='grant select on a25view1 to reobj_a25role3 ,qauser_tsang,qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    

    stmt  ='grant role reobj_a25role1 ,reobj_a25role2,reobj_a25role3 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2() 
    stmt  ='set schema rev_sch25 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='select * from a25tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)   

    stmt  ='select * from a25tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt  ='select * from a25view1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt  ='create view a25view2(aa,bb) as select a,col1 from a25tab1,a25tab2 where a25tab1.b=a25tab2.col2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    

    mydci = basic_defs.switch_session_qi_user3()     
    stmt  ='set schema rev_sch25 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
        
    stmt  ='select * from a25tab1;'    
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')       
    
    stmt  ='select * from a25tab2;'    
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')       
        
    stmt  ='select * from a25view1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)     
    
    stmt  ='set schema rev_sch25 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select on a25tab1 from reobj_a25role1,reobj_a25role2,qauser_tsang,qauser_sqlqaa cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '1015')    
        
    stmt  ='revoke select on a38tab2 from reobj_a25role1,reobj_a25role2,qauser_tsang,reobj_a25role3 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '1015')
    
    stmt  ='revoke select,insert on a25view1 from reobj_a25role3 ,qauser_tsang,qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '1015')
    
    mydci = basic_defs.switch_session_qi_user2() 
    stmt  ='set schema rev_sch25 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
        
    stmt  ='select * from a25tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    

    stmt  ='select * from a25tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select * from a25view1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select * from a25view2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')  

    mydci = basic_defs.switch_session_qi_user3()     
    stmt  ='set schema rev_sch25 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='select * from a25tab1;'    
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')        
    
    stmt  ='select * from a25tab2;'    
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')       
        
    stmt  ='select * from a25view1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')   

    stmt  ='select * from a25view2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')   
    
    stmt  ='drop schema rev_sch25 cascade ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a25role1 ,reobj_a25role2,reobj_a25role3 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
    
    stmt  ='drop role reobj_a25role1; '
    output = _dci.cmdexec(stmt)    

    stmt  ='drop role reobj_a25role2; '
    output = _dci.cmdexec(stmt)    
    
    stmt  ='drop role reobj_a25role3; '
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)      
        
        
def testa26(desc="""revoke priv from role that was given by user 'wgo',verify the user who was granted to role"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='create role reobj_a26role1; '
    output = _dci.cmdexec(stmt)    
    
    stmt  ='create role reobj_a26role2; '
    output = _dci.cmdexec(stmt)    
    
    stmt  ='create schema rev_sch26 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
        
    stmt  ='set schema rev_sch26 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a26tab1(col1 int,col2 int, col3 int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
        
    stmt  ='grant all on table a26tab1 to qauser_tsang with grant option;'    
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a26role1,reobj_a26role2 to qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()     
    stmt  ='set schema rev_sch26 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='grant select on a26tab1 to reobj_a26role1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='grant insert on a26tab1 to reobj_a26role2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    

    mydci = basic_defs.switch_session_qi_user3() 
    stmt  ='set schema rev_sch26 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a26tab1 values(1,2,3);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt  ='select col1,col3 from a26tab1 where col2>1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1) 
    
    stmt  ='set schema rev_sch26 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke all on table a26tab1 from qauser_tsang cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
        
    mydci = basic_defs.switch_session_qi_user3()         
    stmt  ='set schema rev_sch26 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a26tab1 values(1,2,3);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')   
    
    stmt  ='select col1,col3 from a26tab1 where col2>1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  
    
    stmt  ='drop schema rev_sch26 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a26role1,reobj_a26role2 from qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop role reobj_a26role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='drop role reobj_a26role2;'
    output = _dci.cmdexec(stmt)        
        
    _testmgr.testcase_end(desc)  
    
def testa27(desc="""grant priv to role/users wgo,revoke priv from role/user,verify user's priv"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='create role reobj_a27role1; '
    output = _dci.cmdexec(stmt)    
    
    stmt  ='create role reobj_a27role2; '
    output = _dci.cmdexec(stmt)    
    
    stmt  ='create schema rev_sch27 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
        
    stmt  ='set schema rev_sch27 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='create table a27tab1(a int not null primary key, b int, c varchar(10));'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='create table a27tab2(col1 int, col2 int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='grant insert on a27tab1 to reobj_a27role1 with grant option;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select on a27tab1 to reobj_a27role1 with grant option;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select on a27tab2 to qauser_sqlqaa with grant option;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant delete on a27tab2 to qauser_sqlqaa with grant option;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant insert on a27tab2 to qauser_sqlqaa with grant option;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    
    stmt  ='grant insert on a27tab1 to reobj_a27role2 by reobj_a27role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select on a27tab1 to reobj_a27role2 by reobj_a27role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant insert on a27tab2 to qauser_sqlqab by qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select on  a27tab2 to qauser_sqlqab by qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    
    stmt  ='grant role reobj_a27role1 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a27role2 to qauser_teg;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user5()     
    stmt  ='set schema rev_sch27 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a27tab1 values(1,1,\'df\');'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt  ='select * from a27tab1 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1) 
    
    stmt  ='delete from a27tab1 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='create view a27view1 as select * from a27tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    

    mydci = basic_defs.switch_session_qi_user4()     
    stmt  ='set schema rev_sch27 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a27tab2 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt  ='select * from a27tab2 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1) 
    
    stmt  ='delete from a27tab2 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    
    
    stmt  ='create view a27view2 as select * from a27tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='set schema rev_sch27 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke insert on a27tab1 from reobj_a27role2 by reobj_a27role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select on a27tab1 from reobj_a27role2 by reobj_a27role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1014')
    
    stmt  ='revoke select on a27tab1 from reobj_a27role2 by reobj_a27role1 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke insert on a27tab2 from qauser_sqlqab by qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select on a27tab2 from qauser_sqlqab by qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1014')
    
    stmt  ='revoke select on a27tab2 from qauser_sqlqab by qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()     
    stmt  ='set schema rev_sch27 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a27tab1 values(1,1,\'fd\');'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt  ='select * from a27tab1 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2) 
    
    stmt  ='delete from a27tab1 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    
    
    stmt  ='select * from a27view1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')
    
    mydci = basic_defs.switch_session_qi_user3()     
    stmt  ='set schema rev_sch27 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    

    stmt  ='insert into a27tab2 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt  ='select * from a27tab2 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2) 
    
    stmt  ='delete from a27tab2 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2) 
    
    stmt  ='create view a27view3 as select * from a27tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='drop schema rev_sch27 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a27role1 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a27role2 from qauser_teg;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop role reobj_a27role1;'
    output = _dci.cmdexec(stmt)

    stmt  ='drop role reobj_a27role2;'
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)  

def testa28(desc="""revoke priv from user restrict who has granted priv to role"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='create role reobj_a28role1;'
    output = _dci.cmdexec(stmt)

    stmt  ='create role reobj_a28role2;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='create schema rev_sch28 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set  schema rev_sch28 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a28tab1(col1 int, col2 int) no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select on a28tab1 to qauser_tsang with grant option;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant insert on a28tab1 to qauser_tsang with grant option;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()     
    stmt  ='set  schema rev_sch28 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a28tab1 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt  ='select * from a28tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1) 
    
    stmt  ='grant select on a28tab1 to reobj_a28role1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='grant insert on a28tab1 to reobj_a28role2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='set  schema rev_sch28 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select,insert on a28tab1 from qauser_tsang restrict;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1014')

    mydci = basic_defs.switch_session_qi_user2()     
    stmt  ='set  schema rev_sch28 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='revoke select on a28tab1 from reobj_a28role1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='set  schema rev_sch28 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select on a28tab1 from qauser_tsang ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select,insert on a28tab1 from qauser_tsang restrict;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1014')

    mydci = basic_defs.switch_session_qi_user2()     
    stmt  ='set  schema rev_sch28 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='revoke insert on a28tab1 from reobj_a28role1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='set  schema rev_sch28 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke insert on a28tab1 from qauser_tsang restrict;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop schema rev_sch28 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop role reobj_a28role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='drop role reobj_a28role2;'
    output = _dci.cmdexec(stmt)        

    _testmgr.testcase_end(desc)      
        
def testa29(desc="""grant col priv to role/user, then revoke col priv from role/user"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='create role reobj_a29role1;'
    output = _dci.cmdexec(stmt)
        
    stmt  ='create  schema rev_sch29;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='set  schema rev_sch29;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='create table a29tab1(col1 int, col2 int,col3 int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create view a29view1 as select * from a29tab1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
    
    stmt  ='grant select(col1,col2),insert(col1,col2,col3) on a29tab1 to reobj_a29role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
        
    stmt  ='grant select(col1,col2,col3),insert(col1,col2) on a29view1 to qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a29role1 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()     
    stmt  ='set schema schema rev_sch29;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a29tab1(col1,col2,col3) values(2,2,2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt  ='insert into a29tab1 values(1,2,3);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)     
    
    stmt  ='select col1 from a29tab1 where col2=2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2) 
    
    stmt  ='select col1,col3 from a29tab1 where col2=2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    mydci = basic_defs.switch_session_qi_user3()     
    stmt  ='set schema schema rev_sch29;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a29view1(col1,col2,col3) values(2,2,2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='insert into a29view1(col1,col2) values(1,2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select col1 from a29view1 where col2=2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,3) 
    
    stmt  ='select col1,col3 from a29view1 where col2=2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,3) 
    
    stmt  ='set schema schema rev_sch29;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select(col1,col2),insert(col1,col2,col3) on a29tab1 from reobj_a29role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select(col1,col2,col3),insert(col1,col2) on a29view1 from qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()     
    stmt  ='set schema schema rev_sch29;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a29tab1(col1,col2,col3) values(2,2,2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='insert into a29tab1 values(1,2,3);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')   
    
    stmt  ='select col1 from a29tab1 where col2=2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select col1,col3 from a29tab1 where col2=2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    mydci = basic_defs.switch_session_qi_user3()     
    stmt  ='set schema schema rev_sch29;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a29view1(col1,col2,col3) values(2,2,2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='insert into a29view1(col1,col2) values(1,2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select col1 from a29view1 where col2=2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select col1,col3 from a29view1 where col2=2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='drop schema rev_sch29 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a29role1 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop role reobj_a29role1;'
    output = _dci.cmdexec(stmt)    
    
    _testmgr.testcase_end(desc)  

         
def testa30(desc="""grant obj/col priv to role/users, revoke col/obj priv from role/users"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='create role reobj_a30role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create schema rev_sch30 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch30;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a30tab1(a int, b int,c int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select(a,b,c) , insert(a,b),update on a30tab1 to  reobj_a30role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='grant role  reobj_a30role1 to qauser_tsang;' 
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()     
    stmt  ='set schema rev_sch30;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a30tab1 values(1,1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481');    
    
    stmt  ='insert into a30tab1(a,b) values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt  ='select * from a30tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1) 
    
    stmt  ='select a,c from a30tab1 where b=1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1) 
    
    stmt  ='set schema rev_sch30;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select ,insert ,update on a30tab1 from reobj_a30role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '1015')

    mydci = basic_defs.switch_session_qi_user2()     
    stmt  ='set schema rev_sch30;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a30tab1 values(1,1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  
    
    stmt  ='insert into a30tab1(a,b) values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select * from a30tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select a,c from a30tab1 where b=1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='set schema rev_sch30;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a30role1 from qauser_tsang cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop role reobj_a30role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='create table a30tab2(col1 int, col2 int ,col3 varchar(10))no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create view a30view1 as select * from a30tab1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create view a30view2(AA ,BB) as select a30tab1.a,a30tab2.col3 from a30tab1,a30tab2 where a30ab1.b=a30tab2.col2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create mv a30mv1 refresh on request initialize on refresh as select * from a30tab1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='maintain mv a30mv1, refresh;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create mv a30mv2(a,b) refresh on request initialize on refresh as select a30tab1.a,a30tab2.col3 from a30tab1,a30tab2 where a30tab1.b=a30tab2.col2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='maintain mv a30mv2, refresh;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select on a30tab1 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant selelct on a30tab2 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select on a30view1 to qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select on a30view2 to qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select on a30mv1 to qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select on a30mv2 to qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()     
    stmt  ='set schema rev_sch30;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='select * from a30tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt  ='select * from a30tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt  ='select * from a30view1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select * from a30mv1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481');
    
    stmt  ='create view a30view3(col1,col2) as select b,col3 from a30tab1,a30tab2 where a30tab1.a=a30tab2.col2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    mydci = basic_defs.switch_session_qi_user3()     
    stmt  ='set schema rev_sch30;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='select * from a30tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select * from a30tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select * from a30view3;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select * from a30view1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0) 
    
    stmt  ='select * from a30view2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0) 
    
    mydci = basic_defs.switch_session_qi_user4() 
    stmt  ='set schema rev_sch30;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='select * from a30tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select * from a30tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select * from a30view3;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select * from a30mv1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt  ='select * from a30mv2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt  ='set schema rev_sch30;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select(a,b) on a30tab1 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select(col1,col3) on a30tab2 from qauser_tsang;' 
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select(a,b,c) on a30view1 from qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select(AA ,BB) on a30view2 from  qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select(a,b,c) on a30mv1 from qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select(a,b) on a30mv1 from qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2() 
    stmt  ='set schema rev_sch30;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='select * from a30tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt  ='select * from a30tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt  ='select * from a30view1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select * from a30mv1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='create view a30view4(col1,col2) as select b,col3 from a30tab1,a30tab2 where a30tab1.a=a30tab2.col2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    

    mydci = basic_defs.switch_session_qi_user3()     
    stmt  ='set schema rev_sch30;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='select * from a30tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select * from a30tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select * from a30view3;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select * from a30view1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0) 
    
    stmt  ='select * from a30view2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0) 

    mydci = basic_defs.switch_session_qi_user4()     
    stmt  ='set schema rev_sch30;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='select * from a30tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select * from a30tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select * from a30view3;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select * from a30mv1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt  ='select * from a30mv2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt  ='drop schema  rev_sch30 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
	
    stmt  ='revoke role  reobj_a30role1 from qauser_tsang;' 
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='drop role  reobj_a30role1 ;' 
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)      
        

def testa31(desc="""grant col and obj priv to role/user ,revoke col priv from role/user """):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='create role reobj_a31role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
    
    stmt  ='create schema rev_sch31 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch31 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a31tab1(a int,b int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant insert, select(a) on a31tab1 to reobj_a31role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select(a,b), insert(a) on a31tab1 to qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='grant role reobj_a31role1 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()     
    stmt  ='set schema rev_sch31 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)        
    
    stmt  ='	insert into a31tab1(a,b) values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)     
    
    stmt  ='select * from a31tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481');
    
    stmt  ='select a from a31tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)     
    
    stmt  ='create view a31view1(a) as select a from a31tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    

    mydci = basic_defs.switch_session_qi_user3()     
    stmt  ='set schema rev_sch31 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)        
    
    stmt  ='insert into a31tab1(a,b) values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output,'4481')    
    
    stmt  ='insert into a31tab1(a) values(2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)     
    
    stmt  ='select * from a31tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2) 
    
    stmt  ='set schema rev_sch31 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
    
    stmt  ='revoke insert(a,b), select(a,b) on a31tab1 from reobj_a48role1 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '1015');
    
    stmt  ='revoke select(a,b), insert(a,b) on a31tab1 from qauser_sqlqaa cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '1015')

    mydci = basic_defs.switch_session_qi_user2()     
    stmt  ='set schema rev_sch31 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    

    stmt  ='insert into a31tab1(a,b) values(11,22);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)     
    
    stmt  ='select a from a31tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select * from a31view1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')   

    mydci = basic_defs.switch_session_qi_user3()     
    stmt  ='set schema rev_sch31 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    

    stmt  ='insert into a31tab1(a,b) values(23,32);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
    
    stmt  ='select a from a31tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')   
    
    stmt  ='select * from a31view1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')  

    stmt  ='drop schema rev_sch31 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a31role1 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop role reobj_a31role1;'
    output = _dci.cmdexec(stmt)    
    
    _testmgr.testcase_end(desc)  
    
def testa32(desc="""grant col and obj priv to role/user ,revoke obj priv from role/user """):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='create role reobj_a32role1;'
    output = _dci.cmdexec(stmt)    
    
    stmt  ='create schema rev_sch32;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch32;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a32tab1(a int,b int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a32tab2(col1 int, col2 int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select(a,b),insert on a32tab1 to reobj_a32role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select(col1,col2),insert(col2) on a32tab2 to qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a32role1 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()     
    stmt  ='set schema rev_sch32;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a32tab1 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 

    stmt  ='insert into a32tab1(b) values(2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 

    stmt  ='select * from a32tab1 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)     

    mydci = basic_defs.switch_session_qi_user3()     
    stmt  ='set schema rev_sch32;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a32tab2 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
        
    stmt  ='insert into a32tab2(col2) values(2);'    
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)     
    
    stmt  ='select * from a32tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1) 
    
    stmt  ='set schema rev_sch32;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke insert,select on a31tab1 from reobj_a31role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '1015')

    stmt  ='revoke insert ,select on a31tab2 from qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '1015')

    mydci = basic_defs.switch_session_qi_user2()         
    stmt  ='set schema rev_sch32;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a32tab1 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    

    stmt  ='insert into a32tab1(b) values(2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  

    stmt  ='select * from a32tab1 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481');    

    mydci = basic_defs.switch_session_qi_user3()         
    stmt  ='set schema rev_sch32;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)        
    
    stmt  ='insert into a32tab2 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')   
        
    stmt  ='insert into a32tab2(col2) values(2);'    
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')        
    
    stmt  ='select * from a32tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')   
    
    stmt  ='drop schema rev_sch32 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a32role1 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop role reobj_a32role1;'
    output = _dci.cmdexec(stmt)    
    
    _testmgr.testcase_end(desc)  

def testa33(desc="""grant objpriv1 to user, grant objpriv2 to role ,then revoke priv from role/user"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    stmt  ='create role reobj_a33role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='create role reobj_a33role2;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='create schema rev_sch33;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch33;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a33tab1(a int not null primary key,b int,c int);'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a33tab2(col1 int, col2 int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select, insert on a33tab1 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant delete, update, references(a) on a33tab1 to reobj_a33role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant insert,delete on a33tab2 to qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant update ,select on a33tab2 to reobj_a33role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a33role1 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a33role2 to qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()         
    stmt  ='set schema rev_sch33;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='create table a33tab3(a int not null primary key,b int, constraint tab2check foreign key (a) references a33tab1(a));'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a33tab1 values(1,3,3);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt  ='select * from a33tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1) 
    
    stmt  ='update a33tab1 set b=b+1 where c>2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_updated_msg(output,1) 
    
    stmt  ='delete from a33tab1 where c>2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,1) 

    mydci = basic_defs.switch_session_qi_user3()         
    stmt  ='set schema rev_sch33;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a33tab2 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt  ='select * from a33tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1) 
    
    stmt  ='update a33tab2 set col1=col1+1 where col2=1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_updated_msg(output,1) 
    
    stmt  ='delete from a33tab2 where col1=2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_updated_msg(output,1) 
    
    stmt  ='set schema rev_sch33;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke delete, update, references(a) on a33tab1 from reobj_a33role1 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke insert,delete on a33tab2 from qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()         
    stmt  ='set schema rev_sch33;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='create table a33tab4(a int not null primary key,b int ,constraint tab3check foreign key (a) references a33tab1(a));'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1184');

    stmt  ='insert into a33tab1 values(1,3,3);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt  ='select * from a33tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1) 

    stmt  ='update a33tab1 set b=b+1 where c>2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    stmt  ='delete from a33tab1 where c>2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    mydci = basic_defs.switch_session_qi_user3()         
    stmt  ='set schema rev_sch33;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)        
    
    stmt  ='insert into a33tab2 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select * from a33tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0) 
    
    stmt  ='update a33tab2 set col1=col1+1 where col2=1;'
    mydci.expect_updated_msg(output,0) 
    
    stmt  ='delete from a33tab2 where col1=2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='drop schema rev_sch33 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
    
    stmt  ='revoke role reobj_a33role1 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a33role2 from qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop role reobj_a33role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='drop role reobj_a33role2;'
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)  
        
def testa34(desc="""grant col1 to user,grant col2 to role ,then revoke col priv from role/user"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='create role reobj_a34role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='create role reobj_a34role2;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='create schema rev_sch34;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
    
    stmt  ='set schema rev_sch34;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a34tab1(a int not null primary key,b int,c int);'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a34tab2(col1 int,col2 int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select(a,b),insert(a),update(b),references(a) on a34tab1 to reobj_a34role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select(c), insert(b,c) on a34tab1  to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select(col1),insert(col2), update(col1,col2) on a34tab2 to reobj_a34role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select(col2),insert(col1) on a34tab2 to qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a34role2 to qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a34role1 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()         
    stmt  ='set schema rev_sch34;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='create table a34tab3(a int not null primary key,b int, constraint tab3check foreign key (a) references a34tab1(a));'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a34tab1(a) values(1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt  ='insert into a34tab1(a,b) values(2,3);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt  ='insert into a34tab1 values(3,3,3);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt  ='select a,b from a34tab1 where c=3;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1) 
    
    stmt  ='update a34tab1 set b=22 where c=3;'
    output = mydci.cmdexec(stmt)
    mydci.expect_updated_msg(output,1) 

    mydci = basic_defs.switch_session_qi_user3()         
    stmt  ='set schema rev_sch34;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a34tab2 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 

    stmt  ='select * from a34tab2 where col2=1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1) 
    
    stmt  ='update a34tab2 set col1=2 where col2=1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_updated_msg(output,1) 
    
    stmt  ='set schema rev_sch34;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select(a,b),insert(a),update(b),references(a) on a34tab1 from reobj_a34role1 cascade; '
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select(col2),insert(col1) on a34tab2 from  qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()         
    stmt  ='set schema rev_sch34;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='create create table a34tab4(a int not null primary key,b int, constraint tab4check foreign key (a) references a34tab1(a));'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1184')
    
    stmt  ='insert into a34tab1(a) values(22);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='insert into a34tab1(a,b) values(22,33);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='insert into a34tab1(b,c) values(3,3);'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4024')
    
    stmt  ='select a,b from a34tab1 where c=3;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select c from a34tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,3) 
    
    stmt  ='update a34tab1 set b=22 where c=3;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    mydci = basic_defs.switch_session_qi_user3()         
    stmt  ='set schema rev_sch34;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='select * from a34tab2 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
    
    stmt  ='select col1 from a34tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1) 
    
    stmt  ='insert into a34tab2(col2) values(3);'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1) 
    
    stmt  ='insert into a34tab2(col1) values(2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481');
    
    stmt  ='update a34tab2 set col2=1 where col1=1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_updated_msg(output,1) 
    
    stmt  ='drop schema rev_sch34 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a34role1 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a34role2 from qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop role reobj_a34role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='drop role reobj_a34role2;'
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)  
    
    
def testa35(desc="""revoke priv from user who is object's owner"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='create role reobj_a35role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create schema rev_sch35;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch35;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a35tab1(a int, b int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='grant select on a35tab1 to reobj_a35role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a35role1 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()     
    stmt  ='set schema rev_sch35;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='create table a35tab2(col1 int ,col2 int)no partition;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='create view a35view1(aa,bb) as select b,col2 from a5tab1,a54tab2 where a35tab1.a=a35tab2.col1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='set schema rev_sch35;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select on a35tab1 from reobj_a35role1 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select on a35tab1 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '1015')
    
    mydci = basic_defs.switch_session_qi_user2()         
    stmt  ='set schema rev_sch35;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='select * froma 35tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt  ='create table a35tab3(col1 int ,col2 int)no partition;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='create view a35view2(aa,bb) as select b,col2 from a35tab1,a35tab2 where a35tab1.a=a35tab2.col1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='drop schema  rev_sch35 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a35role1 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop role reobj_a35role1;'
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)  
    
def testa40(desc="""revoke subset priv from role/user"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='create role reobj_a40role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='create role reobj_a40role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='create schema rev_sch40;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch40;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a40tab1(col1 int, col2 int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a40tab2(a int ,b int ,c varchar(10)) no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select , insert, delete on a40tab1 to reobj_a40role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select(a,b), insert(a,b,c), update(b) on a40tab2 to reobj_a40role2,qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a40role1 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a40role2 to qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()     
    stmt  ='set schema rev_sch40;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a40tab1 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt  ='insert into a40tab1(col2) values(2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt  ='select col1,col2 from a40tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2) 
    
    stmt  ='delete from a40tab1 where col2=2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,1)
    
    stmt  ='insert into a40tab2 values(1,1,\'we\');'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt  ='select a,b from a40tab2 where c like \'w_\';'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1) 
    
    stmt  ='select a,b from a40tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1) 
    
    stmt  ='select a,b from a56tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1) 
    
    stmt  ='update a40tab2 set b=b+1 where a=1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_updated_msg(output,1) 

    mydci = basic_defs.switch_session_qi_user3()         
    stmt  ='set schema rev_sch40;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a40tab2 values(1,1,\'1\');'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt  ='select a,b from a40tab2 where c like \'1\';'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select a,b from a40tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1) 
    
    stmt  ='update a40tab2 set b=b+1 where a=1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_updated_msg(output,2) 
    
    stmt  ='set schema rev_sch40;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select ,delete on a40tab1 from reobj_a40ole1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select(a), insert(b,c), update(b) on a40tab2 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select(a,b), insert(a) on a40tab2 from reobj_a40role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()         
    stmt  ='set schema rev_sch40;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a40tab1 values(12,13);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt  ='select * from a40tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='delete from a40tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='insert into a40tab2(a) values(11);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt  ='insert into a40tab2(b,c) values(2,\'asf\');'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='insert into a40tab2 values(1,2,\'asdf\');'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select a from a40tab2 where b=2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select b from a40tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,3) 
    
    stmt  ='update a40tab2 set b=1 where a=1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    mydci = basic_defs.switch_session_qi_user3()         
    stmt  ='set schema rev_sch40;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a40tab2(a,b) values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='insert into a40tab2(b,c) values(2,\'asdf\');'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt  ='update a40tab2 set b=1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_updated_msg(output,3)
    
    stmt  ='select a,b from a40tab2 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='drop schema  rev_sch40 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a40role1 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a40role2 from qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop role reobj_a40role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='drop role reobj_a40role2;'
    output = _dci.cmdexec(stmt)    
    
    _testmgr.testcase_end(desc)  


        
def testa42(desc="""revoke priv by user does not have admin priv"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='create role reobj_a42role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='create role reobj_a42role2;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='create schema rev_sch42;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch42;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a42tab1(col1 int, col2 int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant all on a42tab1 to reobj_a42role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a42role1 to qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a42role2 to qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()         
    stmt  ='set schema rev_sch42;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='create table a42tab2(a int, b int)no partition;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='grant all on a42tab2 to reobj_a42role2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='revoke all on a42tab1  from reobj_a42role1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    mydci = basic_defs.switch_session_qi_user3()         
    stmt  ='set schema rev_sch42;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a42tab1 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt  ='select * from a42tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt  ='delete from a42tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,1)

    mydci = basic_defs.switch_session_qi_user4()         
    stmt  ='set schema rev_sch42;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a42tab2 values(1,3);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt  ='select * from a42tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1) 
    
    stmt  ='delete from a42tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,1)
    
    stmt  ='set schema rev_sch42;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke all on a42tab2 from reobj_a42role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1017');

    mydci = basic_defs.switch_session_qi_user4()         
    stmt  ='set schema rev_sch42;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a42tab2 values(1,3);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt  ='select * from a42tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1) 
    
    stmt  ='delete from a42tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,1)
    
    stmt  ='drop schema rev_sch42 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a42role1 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a42role2 from qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop role reobj_a42role2;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='drop role reobj_a42role1;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)  
        
def testa43(desc="""grant by one ,revoke priv by another has/doesn't have admin priv"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='	create role reobj_a43role1;'
    output = _dci.cmdexec(stmt)

    stmt  ='	create role reobj_a43role2;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='create schema  rev_sch43 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema  rev_sch43 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a43tab1(a int,b int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select on a43tab1 to qauser_tsang with grant option;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant insert on a43tab1 to reobj_a43role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role db__rootrole to qauser_sqlaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()         
    stmt  ='set schema  rev_sch43 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='revoke insert on a43tab1 from reobj_a43role2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017');
        
    stmt  ='grant select on a43tab1 to reobj_a43role1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017');

    mydci = basic_defs.switch_session_qi_user3()         
    stmt  ='set schema  rev_sch43 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='revoke insert on a43tab1 from reobj_a43role2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    stmt  ='revoke select on a43tab1 from reobj_a43role1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    stmt  ='revoke insert on a43tab1 from reobj_a43role2 by qauser_tsang;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='set schema  rev_sch43 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke insert on a43tab1 from reobj_a43role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select on a43tab1 from reobj_a43role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output,'1015')
    
    stmt  ='drop schema  rev_sch43 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role db__rootrole from qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop role reobj_a43role2;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='drop role reobj_a43role1;'
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)  
    
def testa44(desc="""grant individually, revoke priv all/grant all,revoke individually"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='create role reobj_a44role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='create role reobj_a44role2;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='create schema rev_sch44;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch44;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a44tab1(a int not null primary key, b int);'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a44tab2(a int not null primary key, b int);'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant all on a44tab1 to reobj_a44role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant insert,select ,update, delete ,references(a,b) on a44tab2 to reobj_a44role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a44role1 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a44role2 to qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()         
    stmt  ='set schema rev_sch44;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='create table a44tab3(a int not null primary key , b int, constraint tab3check foreign key (a) references a44tab1(a));'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a44tab1 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt  ='select * from a44tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1) 
    
    stmt  ='update a44tab1 set b=1 where a=1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_updated_msg(output,1) 
    
    stmt  ='delete from a44tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,1)
    
    mydci = basic_defs.switch_session_qi_user3()         
    stmt  ='set schema rev_sch44;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='create table a44tab4(a int not null primary key , b int, constraint tab4check foreign key (a) references a44tab2(a));'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a44tab2 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt  ='select * from a44tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt  ='update a44tab2 set b=2 where a=1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_updated_msg(output,1) 
    
    stmt  ='delete from a44tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,1)
    
    stmt  ='set schema rev_sch44;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke insert,select ,update, delete on a44tab1 from reobj_a44role1; ';
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke references on a44tab1 from reobj_a44role1 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke all on a44tab2 from reobj_a44role2 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()         
    stmt  ='set schema rev_sch44;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='create table a44tab5(a int not null primary key , b int, constraint tab5check foreign key (a) references a44tab1(a));'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1184')
    
    stmt  ='insert into a44tab1 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select * from a44tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='update a44tab1 set b=1 where a=1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='delete from a44tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select * from a44tab3;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0);

    mydci = basic_defs.switch_session_qi_user3()         
    stmt  ='set schema rev_sch44;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='create table a44tab6(a int not null primary key , b int, constraint tab6check foreign key (a) references a44tab2(a));'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a44tab2 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select * from a44tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='update a44tab2 set b=2 where a=1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='delete from a59tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select * from a59tab4;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0) 
    
    stmt  ='drop schema rev_sch44 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a44role1 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a44role2 from qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop role reobj_a44role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='drop role reobj_a44role2;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)  
    
def testa45(desc="""revoke priv from role/user restrict that has dependent objects"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='drop role reobj_a45role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='drop role reobj_a45role2;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='create schema rev_sch45;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch45;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a45tab1(a int, b int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a45tab2(col1 int, col2 int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select on a45tab1 to reobj_a45role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select on a45tab2 to reobj_a60role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant insert on a45tab2 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a45role1,reobj_a45role2 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()     
    stmt  ='set schema rev_sch45;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='create view a45view1 as select * from a45tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='create mv a45mv1 refresh on request initialize on refresh as select a,col1 from a45tab1,a45tab2 where b=col2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='maintain mv a45mv1, refresh;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a45tab2 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt  ='set schema rev_sch45;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select on a45tab1 from reobj_a45role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1014')
    
    stmt  ='revoke select on a45tab2 from reobj_a45role2 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke insert on a45tab2 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()         
    stmt  ='set schema rev_sch45;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='create view a45view2 as select * from a45tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='create mv a45mv2 refresh on request initialize on refresh as select a,col1 from a45tab1,a45tab2 where b=col2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1051')
    
    stmt  ='delete from a45mv1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1051')
    
    stmt  ='insert into a45tab2 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='drop schema rev_sch45 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a45role1,reobj_a45role2 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop role reobj_a45role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='drop role reobj_a45role2;'
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)  

def testa46(desc="""revoke priv from role/user restrict that has/has no dependent objects"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    stmt  ='create role reobj_a46role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='create schema rev_sch46;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch46;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a46tab1(a int, b int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a46tab2(col1 int, col2 int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select on a46tab1 to reobj_a46role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant insert on a46tab2 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role  reobj_a46role1 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()     
    stmt  ='set schema rev_sch46;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='create view a46view1 as select * from a46tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481');    
    
    stmt  ='insert into a46tab2 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)

    stmt  ='select * from a46tab1;'
    mydci.expect_selected_msg(output,0)
    
    stmt  ='set schema rev_sch46;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select on a46tab1 from reobj_a46role1 restrict;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke insert on a46tab2 from qauser_tsang restrict;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch46;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    

    mydci = basic_defs.switch_session_qi_user2()         
    stmt  ='create view a46view1 as select * from a46tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  
    
    stmt  ='insert into a46tab2 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  
    
    stmt  ='select * from a46tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    
    
    stmt  ='drop schema rev_sch46 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a46role1 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
    
    stmt  ='drop role reobj_a46role1;'
    output = _dci.cmdexec(stmt)    

    _testmgr.testcase_end(desc)      
        
def testa47(desc="""revoke priv from role/user cascade that has/has no dependent objects"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='create role reobj_a47role1;'
    output = _dci.cmdexec(stmt)    
    
    stmt  ='create role reobj_a47role2;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='create schema rev_sch47;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch47;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a47tab1(a int, b int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='create table a47tab2(col1 int, col2 int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='grant select on a47tab1 to reobj_a47role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select on a47tab2 to reobj_a47role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='grant insert on a47tab2 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a47role1,reobj_a47role2 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()         
    stmt  ='set schema rev_sch47;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='create view a47view1 as select * from a47tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='create mv a47mv1 refresh on request initialize on refresh as select a,col1 from a47tab1,a47tab2 where b=col2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='maintain mv a47mv1, refresh;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a47tab2 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt  ='set schema rev_sch47;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select on a47tab1 from reobj_a47role1 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select on a47tab2 from reobj_a62role2 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke insert on a47tab2 from qauser_sqlqaa cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()         
    stmt  ='set schema rev_sch47;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='create view a47view2 as select * from a47tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    
    
    
    stmt  ='create mv a47mv2 refresh on request initialize on refresh as select a,col1 from a47tab1,a47tab2 where b=col2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1051')
    
    stmt  ='insert into a47tab2 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    
    
    stmt  ='select * from a47view1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')   
    
    stmt  ='select * from a47mv2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')   
    
    stmt  ='drop schema rev_sch47 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a47role1,reobj_a47role2 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
    
    stmt  ='drop role reobj_a47role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='drop role reobj_a47role2;'
    output = _dci.cmdexec(stmt)
        
    _testmgr.testcase_end(desc)  
    
def testa48(desc="""revoke priv from role/user cascade that has/has no dependent objects"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='create role reobj_a48role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='create schema rev_sch48;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch48;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a48tab1(a int, b int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a48tab2(col1 int, col2 int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select on a48tab1 to reobj_a48role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant insert on a48tab2 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a48role1 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()         
    stmt  ='set schema rev_sch48;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='create view a48view1 as select * from a48tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')   
    
    stmt  ='insert into a48tab2 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt  ='select * from a48tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1) 
    
    stmt  ='set schema rev_sch48;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select on a48tab1 from reobj_a48role1 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke insert on a48tab2 from qauser_tsang cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()             
    stmt  ='set schema rev_sch48;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='create view a48view1 as select * from a48tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')   
    
    stmt  ='insert into a48tab2 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
    
    stmt  ='select * from a48tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    
    
    stmt  ='drop schema rev_sch48 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a48role1 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop role reobj_a48role1;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)  
    
    
def testa49(desc="""revoke priv from role restrict , verify other role's priv that is grant same priv"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='create role reobj_a49role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='create role reobj_a49role2;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='create schema rev_sch49;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch49;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a49tab1(a int, b int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select on a49tab1 to reobj_a49role1,reobj_a49role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a49role1 to qauser_tsang, qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a49role2 to  qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()         
    stmt  ='set schema rev_sch49;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='select * from a49tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0);

    mydci = basic_defs.switch_session_qi_user3()         
    stmt  ='set schema rev_sch49;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='select * from a49tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='set schema rev_sch49;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select on a49tab1 from reobj_a49role1 restrict;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch49;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='select * from a49tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')   
    
    stmt  ='select * from a49tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='set schema rev_sch49;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop schema rev_sch49 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop role reobj_a49role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='drop role reobj_a49role2;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)      
    
def testa50(desc="""revoke priv from role cascade , verify other role's priv that is grant same priv"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='create role reobj_a50role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='create role reobj_a50role2;'
    output = _dci.cmdexec(stmt)
        
    stmt  ='create schema rev_sch50 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch50 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a50tab1(a int, b int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a50role1 to qauser_tsang, qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='grant role reobj_a50role2 to qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select on a65tab1 to reobj_a50role1,reobj_a50role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    

    mydci = basic_defs.switch_session_qi_user2()         
    stmt  ='set schema rev_sch50 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='select * from a50tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt  ='create view a50view1 as select * from a50tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    

    stmt  ='create mv a50mv1 refresh on request initialize on refresh as select * from a50tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    

    stmt  ='maintain mv a50mv1, refresh;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    

    mydci = basic_defs.switch_session_qi_user3()     
    stmt  ='set schema rev_sch50 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='select * from a50tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0) 
    
    stmt  ='create view a50view2 as select * from a50tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    

    stmt  ='create mv a50mv2 refresh on request initialize on refresh as select * from a50tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)        
    
    stmt  ='maintain mv a50mv1, refresh;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='set schema rev_sch50 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select on a50tab1 from reobj_a50role1 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()     
    stmt  ='set schema rev_sch50 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='select * from a50tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
    
    stmt  ='create view a50view3 as select * from a50tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    

    stmt  ='create mv a50mv3 refresh on request initialize on refresh as select * from a50tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1051')

    mydci = basic_defs.switch_session_qi_user3()         
    stmt  ='set schema rev_sch50 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='select * from a50tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0) 
    
    stmt  ='create view a50view4 as select * from a50tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    

    stmt  ='create mv a50mv4 refresh on request initialize on refresh as select * from a50tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)        
    
    stmt  ='drop schema rev_sch50 cascade ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a50role1 from qauser_tsang, qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a50role2 from  qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
        
    stmt  ='drop role reobj_a50role2;'
    output = _dci.cmdexec(stmt)

    stmt  ='drop role reobj_a50role1;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)      
        
def testa51(desc="""revoke grant option for from user/role who grant priv to role/users"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='create role reobj_a51role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='create role reobj_a51role2;'
    output = _dci.cmdexec(stmt)
    
    
    stmt  ='create schema rev_sch51 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch51 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a51tab1(a int ,b int) no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  = 'grant all on 51tab1 to qauser_tsang , reobj_a51role1 with grant option;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grang select,insert on a51tab1 to qauser_teg granted by reobj_a51role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a51role1 to qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a51role2 to qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()         
    stmt  ='set schema rev_sch51 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='grant insert,update on a51tab1 to reobj_a51role2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    

    mydci = basic_defs.switch_session_qi_user4()         
    stmt  ='set schema rev_sch51 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a51tab1 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt  ='update a51tab1 set a=a+1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_updated_msg(output,1) 
    
    stmt  ='select * from a51tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')   

    mydci = basic_defs.switch_session_qi_user5()         
    stmt  ='set schema rev_sch51 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a51tab1 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt  ='select * from a51tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2) 
    
    stmt  ='create view a51view1 as select * from a51tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='delete form a51taba;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='set schema rev_sch51 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
    
    stmt  = 'revoke grant option for on 51tab1 from qauser_tsang , reobj_a51role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()         
    stmt  ='set schema rev_sch51 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='grant select on a51tab1 to qauser_sqlqaa;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')   
    
    stmt  ='select * from  a51tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2) 
    
    mydci = basic_defs.switch_session_qi_user3()     
    stmt  ='set schema rev_sch51 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='grant select on a51tab1 to qauser_sqlqaa;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')   
    
    stmt  ='select * from  a51tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2) 
    
    mydci = basic_defs.switch_session_qi_user4()         
    stmt  ='set schema rev_sch51 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a51tab1 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')   
    
    stmt  ='update a51tab1 set a=a+1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')   
    
    stmt  ='select * from a51tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  

    mydci = basic_defs.switch_session_qi_user5()     
    stmt  ='set schema rev_sch51 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a51tab1 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select * from a51tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='create view a51view2 as select * from a51tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='select * from a51view1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')
    
    stmt  ='delete form a51taba;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt  ='drop schema  rev_sch51 cascade ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a51role1 from qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a51role2 from qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop role reobj_a51role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='drop role reobj_a51role2;'
    output = _dci.cmdexec(stmt)    
        
    _testmgr.testcase_end(desc)  
    
def testa52(desc="""grant by different user, then revoke"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='create role reobj_a52role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='create role reobj_a52role2;'
    output = _dci.cmdexec(stmt)    
    
    stmt  ='create schema rev_sch52 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='set schema rev_sch52 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
        
    stmt  ='create table a52tab1(a int, b int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='create table a52tab2(a int,b int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant all on a52tab1 to qauser_tsang with grant option;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant all on a52tab2 to qauser_tsang with grant option;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select on a52tab1 to reobj_a52role1 by qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant all on a52tab1 to  reobj_a52role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='grant select on a52tab2 to reobj_a52role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='grant role reobj_a52role1,reobj_a52role2 to  qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()         
    stmt  ='set schema rev_sch52 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='grant all on a52tab1 to reobj_a52role1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='grant all on a52tab1 to reobj_a52role1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='set schema rev_sch52 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke all on a52tab1 from reobj_a52role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '1015')
    
    stmt  ='revoke all on a52tab2 from  reobj_a52role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '1015')
    
    mydci = basic_defs.switch_session_qi_user3()     
    stmt  ='set schema rev_sch52 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a52tab1 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt  ='select * from a52tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1) 
    
    stmt  ='insert into a52tab2 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt  ='select * from a52tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1) 
    
    stmt  ='delete from a52tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    
    
    stmt  ='set schema  rev_sch52 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke all on a52tab1 from reobj_a52role1 by qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke all on a52tab2 from  reobj_a52role2 by qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop schema  rev_sch52 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a52role1,reobj_a52role2 from qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop role reobj_a52role1;'
    output = _dci.cmdexec(stmt)
    
    stmt  ='drop role reobj_a52role2;'
    output = _dci.cmdexec(stmt)    

    _testmgr.testcase_end(desc)      
        
def testa53(desc="""grant priv to role ,then revoke ,consecutive grant"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt  ='create role reobj_a53role2;'
    output = _dci.cmdexec(stmt)    
    
    stmt  ='create schema rev_sch52 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt  ='set schema rev_sch52 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='create table a52tab1(a int,b int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select on a52tab1 to reobj_a52role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant role reobj_a52role1 to qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()     
    stmt  ='set schema rev_sch52 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='select * from a52tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0);
    
    stmt  ='set schema rev_sch52 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke select on a52tab1 from reobj_a52role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='grant select,insert on a52tab1 to reobj_a52role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()     
    stmt  ='set schema rev_sch52 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt  ='insert into a52tab1  values(1,1);'
    mydci.expect_inserted_msg(output,1)
    
    stmt  ='select * from a52tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt  ='drop schema rev_sch52 schema;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='revoke role reobj_a52role1 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt  ='drop role reobj_a52role1;'
    output = _dci.cmdexec(stmt)
        

    _testmgr.testcase_end(desc)           
    
    
    
    
    
    
    
    
    
    
    
    
