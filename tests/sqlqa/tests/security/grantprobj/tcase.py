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
import time
import unittest

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
 


def testa01(desc="""characters invalid and missing some keywords and disordering"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """drop role gra_a01role1;"""
    output = _dci.cmdexec(stmt)
        
    stmt = """drop role gra_a01role2;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop role gra_a01role3;"""
    output = _dci.cmdexec(stmt)
        
    stmt = """create role gra_a01role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """create role gra_a01role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create role gra_a01role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """unregister user qauser31;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop role gra_a01role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create schema grantsch1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """set schema grantsch1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """drop table granttab1;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table granttab2;"""
    output = _dci.cmdexec(stmt)   
     
    stmt = """create table granttab1(a int not null, b int, primary key (a));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """create table granttab2(a int not null, b int, primary key (a));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """grant all on granttab1 to gra_a01role3 by db__root;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1008')
        
    stmt = """grant all on granttab1 to qauser31,gra_a01role3 by db__root;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1011')

    stmt = """grant all on granttab1 to current with grant option by db__root;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """grant all on granttab1 to NONE with grant option by db__root;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
        
    stmt = """grant all on grnattab1 to _System with grant option by db__root;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
        
    stmt = """grant all on granttab1 to gra_a01role1 granted by db__root with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """grant all to gra_a01role1 on granttab1 granted by db__root;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
        
    stmt = """grant all on granttab1 to gra_a01role3  by gra_a01role2g;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1008')

    stmt = """grant all on granttab1 to gra_a01role1 with grant option by public;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
        
    stmt = """grant all on granttab1 to gra_a03role3 with grant option by NONE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """grant all on granttab1 to gra_a01role1 with grant option by _system;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
        
    stmt = """grant all on grattab1,grattab1 to gra_a01role3 with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
        
    stmt = """grant all on grattab1,grattab2,grattab2 to gra_a01role3 with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
        
    stmt = """grant all on grattab1,grattab2 to gra_a01role3 with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
        
    stmt = """grant select on gra_a01role1 to gra_a01role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')

    stmt = """grant select on qauser_tsang to gra_a01role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')

    stmt = """grant select on a to gra_a01role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
        
    stmt = """grant select on select to gra_a01role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """grant select on create to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
        
    stmt = """grant all on test to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3128')
               
    stmt = """grant all on granttab1 to qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456789132;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')

    stmt = """grant all on granttab1 to;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
        
    stmt = """grant all on granttab1 to gra_a01role1,gra_a01role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1011')  

    stmt = """grant all on granttab1 to gra_a01role1,gra_a01role2,gra_a01role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1011')      

    stmt = """grant all on granttab1 to qauser_sqlqaa,qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1011')       

    stmt = """grant all on granttab1 to grattab2d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1008')

    stmt = """grant all on granttab1 to gra_a01role1g;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1008')

    stmt = """grant all on granttab1 to gra_a01role1,gra_a01role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1011')

    stmt = """grant all on granttab1 to gra_a01role1,qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1011')

    stmt = """grant all on granttab1 to grattab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1008')
        
    stmt = """grant select on granttab1 to gra_a01role1 by public;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """grant insert on granttab1 to gra_a01role1 by test;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3128')
    
    stmt = """drop table granttab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """drop table granttab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """drop schema grantsch1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """drop role gra_a01role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """drop role gra_a01role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    _testmgr.testcase_end(desc)

 
def testa02(desc="""ordinary user with/without WGO execute command without by clause"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """set schema grantsch2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table gra2tab1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop schema grantsch2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role gra_a02role1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role gra_a02role2;"""
    output = _dci.cmdexec(stmt)
        
    stmt = """create role gra_a02role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """create role gra_a02role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create schema grantsch2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """set schema grantsch2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """create table gra2tab1(a int not null, b int, primary key (a));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)         

    stmt = """grant all on gra2tab1 to qauser_sqlqaa with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """grant all on gra2tab1 to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    #user2
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 
    
    stmt = """grant all on gra2tab1 to gra_a02role1 with grant option;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 
    
    stmt = """grant all on gra2tab1 to qauser_sqlqab with grant option;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
        
    stmt = """revoke all on gra2tab1 from gra_a02role1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 
    
    stmt = """revoke all on gra2tab1 from qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user4()

    stmt = """set schema grantsch2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 

    stmt = """grant all on gra2tab1 to gra_a02role2 with grant option;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    stmt = """grant all on gra2tab1 to qauser_teg with grant option;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
        
    stmt = """set schema grantsch2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """revoke all on gra2tab1 from qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """revoke all on gra2tab1 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """drop table gra2tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """drop schema grantsch2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """drop role gra_a02role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """drop role gra_a02role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    _testmgr.testcase_end(desc)


def testa03(desc="""grant all single dml multiple dml to role/user"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
       
    stmt = """create role grobj_a01role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create role grobj_a01role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create schema grantsch3;"""
    _dci.expect_complete_msg(output) 
    output = _dci.cmdexec(stmt)
        
    stmt = """set schema grantsch3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)        
        
    stmt = """create table a01tab1(col1 int, col2 int, col3 varchar(10))no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """create table a01tab2(col1 int, col2 varchar(10))no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant all on a01tab1 to grobj_a01role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """grant insert on a01tab2 to grobj_a01role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """grant insert on a01tab2 to qauser_teg;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant select , delete , update on a01tab2 to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a01role1 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a01role2 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    #qauser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()   
    
    stmt = """set schema grantsch3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 
        
    stmt = """insert into a01tab1 values(1,2,'qaz');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)

    stmt = """select * from a01tab1 ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

    stmt = """update a01tab1 set col1=col1+1 where col2=2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_updated_msg(output,1)

    stmt = """select * from a01tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    
        
    #qauser_sqlqab        
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema grantsch3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 

    stmt = """select * from a01tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
        
    stmt = """insert into a01tab2 values(11,'asd');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
        
    stmt = """select * from a01tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """delete from a01tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """update a01tab2 set col2='das';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    #qauser_teg     

    mydci = basic_defs.switch_session_qi_user5()
    stmt = """set schema grantsch3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 

    stmt = """select * from a01tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
        
    stmt = """insert into a01tab2 values(11,'asd');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
        
    stmt = """select * from a01tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """delete from a01tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """update a01tab2 set col2='das';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
        
        
    #qauser_tsang  
    mydci = basic_defs.switch_session_qi_user4()
    
    stmt = """set schema grantsch3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 
        
    stmt = """select * from a01tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
        
    stmt = """insert into a01tab1 values(12,23,'das');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """select * from a01tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)

    stmt = """insert into a01tab2 values(1,'ewr');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
        
    stmt = """update a01tab2 set col2='we1';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_updated_msg(output,2)
        
    stmt = """delete  from a01tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,2)

    #process supermxci
    stmt = """set schema grantsch3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """revoke role grobj_a01role1 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """revoke role grobj_a01role2 from qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """revoke all on a01tab1 from grobj_a01role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """revoke insert on a01tab2 from grobj_a01role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """revoke insert on a01tab2 from qauser_teg;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke select , delete , update on a01tab2 from qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    

    stmt = """set schema grantsch3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop table a01tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop table a01tab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop schema grantsch3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """drop role grobj_a01role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a01role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    _testmgr.testcase_end(desc)


def testa04(desc="""grant column level priv to role/user"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
       
    stmt = """create role grobj_a02role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """create role grobj_a02role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """create schema grantsch4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """set schema grantsch4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a02tab1(col1 int, col2 int, col3 varchar(10))no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a02tab2(col1 int, col2 varchar(10))no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant insert(col1,col2,col3), select(col1,col2,col3) on a02tab1 to grobj_a02role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant update(col2) on a02tab2 to grobj_a02role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant insert(col1),select(col1,col2) on a02tab2 to qauser_teg;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """grant role grobj_a02role1 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a02role2 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 


    #qauser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch4;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 
        
    stmt = """insert into a02tab1 values(1,2,'we');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
        
    stmt = """select col1,col3 from a02tab1 where col2=2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

    stmt = """select * from  a02tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)
        
    stmt = """delete  from a02tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """select * from a02tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    #qauser_sqlqab    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema grantsch4;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 
        
    stmt = """insert into a02tab1(col1,col2) values(1,2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """update a02tab2 set col2='afd';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_updated_msg(output,1)

    stmt = """update a02tab2 set col2= 'adf' where col1=1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_any_substr(stmt, 'SELECT' )
    mydci.expect_error_msg(output, '4481') 

    stmt = """insert into a02tab2(col1) values(2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """select * from a02tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    #qauser_teg
    mydci = basic_defs.switch_session_qi_user5()
    
    stmt = """set schema grantsch4;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 

    stmt = """insert into a02tab2(col1) values(1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)

    stmt = """insert into a02tab2 values(2,'ew');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
        
    stmt = """select col2 from a02tab2 where col1=1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

    stmt = """select * from a02tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

    stmt = """select * from a02tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
    
    #process supermxci        
    stmt = """revoke insert(col1,col2,col3), select(col1,col2,col3) on a02tab1 from grobj_a02role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """revoke update(col2) on a02tab2 from grobj_a02role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """revoke insert(col1),select(col1,col2) on a02tab2 from qauser_teg;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """revoke role grobj_a02role1 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """revoke role grobj_a02role2 from qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """set schema grantsch4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)     

    stmt = """drop table a02tab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)         
    stmt = """drop table a02tab1;"""  
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop schema grantsch4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """drop role grobj_a02role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a02role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    _testmgr.testcase_end(desc)
        

def testa05(desc="""grant mix obj and column level to role/user"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
               
    stmt = """create role grobj_a03role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create role grobj_a03role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create schema grantsch5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """set schema grantsch5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a03tab1(col1 int, col2 int, col3 varchar(10))no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a03tab2(col1 int, col2 varchar(10))no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """grant insert(col1,col2), select on a03tab1 to grobj_a03role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """grant update(col2), insert,select on a03tab2 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant insert(col1),select(col1), select on a03tab2 to grobj_a03role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1264')
        
    stmt = """grant role grobj_a03role1 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    #process qauser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch5;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a03tab1(col1,col2) values(1,2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)

    stmt = """insert into a03tab1 values(2,3,'adsf');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """select col3 from a03tab1 where col1=1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

    stmt = """select  * from a03tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

    #process qauser_sqlqab
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema grantsch5;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
        
    stmt = """insert into a03tab1 values(2,3,'adf');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    stmt = """insert into a03tab2 values(1, 'sd');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)

    stmt = """insert into a03tab2(col1) values(2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)

    stmt = """select col1 from a03tab2 where col2 like 's%';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

    stmt = """select col1,col2 from a03tab2 ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)

    stmt = """select * from a03tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)

    stmt = """update a03tab2 set col2='sdf' where col1=1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_updated_msg(output,1) 

    stmt = """update a03tab2 set col1=col1+1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
       
    #process supermxci
    stmt = """revoke insert(col1,col2), select on a03tab1 from grobj_a03role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """revoke update(col2), insert,select on a03tab2 from qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """revoke role grobj_a03role1 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)   

    stmt = """drop table a03tab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop table a03tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop schema grantsch5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """drop role grobj_a03role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a03role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a03role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    _testmgr.testcase_end(desc)


def testa06(desc="""grant priv on objects(table view mv) to role/user"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
                       
    stmt = """create role grobj_a05role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create role grobj_a05role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create schema grantsch6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """set schema grantsch6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a05tab1(col1 int, col2 int, col3 varchar(10))no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """insert into a05tab1 values(11,22, 'ads');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,1);
        
    stmt = """create table a05tab2(a int, b int, c varchar(10))no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create view  a05view1 as select * from a05tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create view a05view2(a,c) as select a05tab1.col1, a05tab2.c from a05tab1,a05tab2 where a05tab1.col2=a05tab2.b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create mv a05mv1 refresh on request initialize on refresh as select * from a05tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """maintain mv a05mv1, refresh;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create mv a05mv2 refresh on request initialize on refresh as select a05tab1.col1, a05tab2.c from a05tab1,a05tab2 where a05tab1.col2=a05tab2.b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """maintain mv a05mv2, refresh;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """create trigger a05trig1 after update on a05tab1 REFERENCING NEW AS newR FOR EACH ROW insert into a05tab1 values(1,2,'dd');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create synonym syn_a05tab1 for a05tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create synonym syn_a05view1 for a05view1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """create synonym syn_a05mv2 for a05mv2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 


    stmt = """grant select,insert,update on a05tab1 to grobj_a05role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """grant select on a05view1 to grobj_a05role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select,insert on a05tab2 to grobj_a05role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select on a05view2 to grobj_a05role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select on a05mv1 to grobj_a05role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select on a05mv2 to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant insert on syn_a05tab1 to qauser_teg;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select on syn_a05view1 to qauser_teg;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select on syn_a05mv2 to qauser_teg;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 


    stmt = """grant role grobj_a05role1 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a05role2 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 


    #process qauser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch6;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a05tab1 values(1,2,'qw');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
        
    stmt = """update a05tab1 set col3='afd' where col2=2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_updated_msg(output,1) 

    stmt = """select * from a05tab1 where col2=2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)

    stmt = """select * from syn_a05tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,3)
        
    stmt = """insert into a05view1 values(2,3,'we');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
        
    stmt = """select * from a05view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,3)

    stmt = """select * from syn_a05view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,3)

    stmt = """select * from a05view2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """select * from a05mv1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """select * from a05mv2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    #process qauser_sqlqab 
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema grantsch6;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
        
    stmt = """insert into a05tab2 values(2,2,'asd'),(2,3,'adf');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,2)   
        
    stmt = """select * from a05tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)

    stmt = """select * from a05tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """select * from a05view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """select * from a05view2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)

    stmt = """select * from a05mv1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)
        
    stmt = """select * from a05mv2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """select * from syn_a05mv2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
        
    #process qauser_tsang
    mydci = basic_defs.switch_session_qi_user4()
    
    stmt = """set schema grantsch6;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
        
    stmt = """select * from a05tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
        
    stmt = """select * from a05tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """select * from a05mv1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """select * from a05mv2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """select * from syn_a05mv2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    #process qauser_teg
    mydci = basic_defs.switch_session_qi_user5()
    
    stmt = """set schema grantsch6;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into syn_a05tab1 values(1,1,'df');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
        
    stmt = """select * from syn_a05view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,4)

    stmt = """select * from syn_a05mv2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """insert into a05tab1 values(1,2,'df');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
        
    stmt = """select * from syn_a05view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,5)

    stmt = """select * from syn_a05mv2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    #process supermxci
    stmt = """set schema grantsch6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """drop synonym syn_a05tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """drop synonym syn_a05mv2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """drop synonym syn_a05view1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    #process qauser_sqlqaa
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch6;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a05tab1 values(1,2,'df');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)

    stmt = """select * from syn_a05view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  

    stmt = """select * from syn_a05mv2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  
        

    stmt = """revoke select,insert,update on a05tab1 from grobj_a05role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)         
    stmt = """revoke select on a05view1 from grobj_a05role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke select,insert on a05tab2 from grobj_a05role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke select on a05view2 from grobj_a05role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke select on a05mv1 from grobj_a05role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke select on a05mv2 from qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop mv a05mv1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop mv a05mv2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop view a05view2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop table a05tab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop table a05tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop schema grantsch6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """revoke role grobj_a05role1 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a05role2 from qauser_sqlqab;""" 
    output = _dci.cmdexec(stmt)    
    _dci.expect_complete_msg(output) 

    stmt = """drop role grobj_a05role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a05role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    _testmgr.testcase_end(desc)


def testa07(desc="""grant priv on object to single/multiple users"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
                                             
    stmt = """create schema grantsch7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """set schema grantsch7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a08tab1(col1 int ,col2 int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a08tab2(col1 int,col2 int,col3 varchar(10))no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select,insert on a08tab1 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant all on a08tab2 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """grant all on a08tab2 to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    #process qauser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch7;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
        
    stmt = """insert into a08tab1 values(1,2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
        
    stmt = """select * from a08tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)
        
    stmt = """insert into a08tab2 values(1,2,'adf');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    #process qauser_tsang
    mydci = basic_defs.switch_session_qi_user4()
    
    stmt = """set schema grantsch7;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
        
    stmt = """insert into a08tab2 values(1,2,'aer');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)  

    stmt = """select * from a08tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

    stmt = """delete from a08tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,1)
        
    stmt = """insert into a08tab1 values(1,2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  

    stmt = """delete from a08tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  

        
    #process qauser_sqlqab
    mydci = basic_defs.switch_session_qi_user3()    
    
    stmt = """set schema grantsch7;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
        
    stmt = """insert into a08tab2 values(1,2,'aer');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)  

    stmt = """select * from a08tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

    stmt = """delete from a08tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,1)  
        
    stmt = """insert into a08tab1 values(1,2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')   

    stmt = """delete from a08tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')   
        
    #process supermxci
    stmt = """set schema grantsch7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke select ,insert on a08tab1 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke all on a08tab2 from qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """revoke all on a08tab2 from qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
        
    stmt = """drop table a08tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop table a08tab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop schema grantsch7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    _testmgr.testcase_end(desc)


def testa08(desc="""grant priv on object to single/multiple roles"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
  
    stmt = """create role grobj_a09role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create role grobj_a09role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create role grobj_a09role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create schema grantsch9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """set schema grantsch9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a09tab1(col1 int,col2 int,col3 int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a09tab2(col1 int,col2 int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create view a09view1(a,b) as select a09tab1.col1,a09tab2.col2 from a09tab1,a09tab2 where a09tab1.col3=a09tab2.col2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant insert on a09tab1 to grobj_a09role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select,insert on a09tab2 to grobj_a09role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """grant select,insert on a09tab2 to grobj_a09role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant select on a09view1 to grobj_a09role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a09role1,grobj_a09role3 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a09role2 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a09role1,grobj_a09role3 to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    #process secpbmxci
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema grantsch9;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a09tab1 values(1,2,3);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')   

    stmt = """insert into a09tab2 values(1,3);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 

    stmt = """select * from a09tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')   

    stmt = """select * from a09tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

    stmt = """select * from a09view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    #process qauser_sqlqaa;
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch9;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a09tab1 values(1,2,3),(1,3,3);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,2) 

    stmt = """insert into a09tab2 values(1,3);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 

    stmt = """select * from a09tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
        
    stmt = """select * from a09tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)

    stmt = """select * from a09view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,4)

    #process qauser_tsang
    mydci = basic_defs.switch_session_qi_user4()
    
    stmt = """set schema grantsch9;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
        
    stmt = """select * from a09tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  

    stmt = """select * from a09tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)

    stmt = """select * from a09view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,4)

    #process supermxci
    stmt = """set schema grantsch9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """revoke insert on a09tab1 from grobj_a09role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke select,insert on a09tab2 from grobj_a09role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke select,insert on a09tab2 from grobj_a09role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke select on a09view1 from grobj_a09role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)         
    stmt = """revoke role grobj_a09role1,grobj_a09role3 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a09role2 from qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a09role1,grobj_a09role3 from qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop view  a09view1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop table a09tab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop table a09tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop schema grantsch9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)         
    stmt = """drop role grobj_a09role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a09role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a09role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    _testmgr.testcase_end(desc)
        

def testa09(desc="""grant priv on object to role by user/multiple users"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
 
    stmt = """create role grobj_a14role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create role grobj_a14role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """create schema grantsch14;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """set schema grantsch14;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a14tab1(col1 int, col2 varchar(10))no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant all on a14tab1 to qauser_sqlqaa with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """grant all on a14tab1 to qauser_sqlqab with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """grant select on a14tab1 to grobj_a14role1 by qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select on a14tab1 to grobj_a14role1 by DB__ROOT,qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """grant insert on a14tab1 to grobj_a14role2 by qauser_sqlqaa,qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """grant select(col1),delete on a14tab1 to grobj_a14role2 by DB__ROOT,qauser_sqlqaa,qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """grant role grobj_a14role1 to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a14role2 to qauser_teg;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    #process qauser_tsang     
    mydci = basic_defs.switch_session_qi_user4()   
    
    stmt = """set schema grantsch14;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
      
    stmt = """select * from a14tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
        
    stmt = """insert into a14tab1 values(1,'2');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    #process qauser_teg
    mydci = basic_defs.switch_session_qi_user5() 
    
    stmt = """set schema grantsch14;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select * from a14tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """insert into a14tab1 values(1,'2');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """select col1 from a14tab1 where col1=1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """delete from a14tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
              
    stmt = """revoke role grobj_a14role1 from qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)   
    
    stmt = """revoke select on a14tab1 from grobj_a14role1 by qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)         
    stmt = """revoke all on a14tab1 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    stmt = """revoke all on a14tab1 from qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    stmt = """revoke role grobj_a14role2 from qauser_teg;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)          
    stmt = """drop table a14tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop schema grantsch14;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)        
    stmt = """drop role grobj_a14role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a14role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    _testmgr.testcase_end(desc)


def testa10(desc="""grant priv on object to role/user by a/multiple role"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
       
    stmt = """create role grobj_a15role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """create role grobj_a15role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create role grobj_a15role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create schema grantsch15;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """set schema grantsch15;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a15tab1(col1 int, col2 int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant all on table a15tab1 to grobj_a15role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """grant all on table a15tab1 to grobj_a15role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """grant all on table a15tab1 to qauser_sqlqab by grobj_a15role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)         

    stmt = """grant select ,insert on table a15tab1 to grobj_a15role1 by grobj_a15role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '1012');

    stmt = """grant delete on a15tab1 to grobj_a15role1 by grobj_a15role3,DB__Admin;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """grant update(col1,col2),references(col1) to grobj_a15role2 by DB__Admin;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
        
    stmt = """grant role grobj_a15role1 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    #process qauser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch15;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
        
    stmt = """insert into a15tab1 values(1,2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """select * from a15tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """delete from a15tab1 where col1=1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
        
    #process qauser_sqlqab
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema grantsch15;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
        
    stmt = """insert into a15tab1 values(1,2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 

    stmt = """select * from a15tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

    stmt = """delete from a15tab1 where col1=1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,1)      

    #process supermxci        
    stmt = """revoke all on table a15tab1 from grobj_a15role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke all on table a15tab1 from grobj_a15role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """revoke role grobj_a15role1 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a15role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a15role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a15role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop table a15tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop schema grantsch15;"""  
    output = _dci.cmdexec(stmt)    
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)    
            

def testa11(desc="""grant priv on object to role/user by user who cannot grant priv"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
 
    stmt = """create role grobj_a17role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create role grobj_a17role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create schema grantsch11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """set schema grantsch11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """create table a17tab1(col1 int,col2 int ,col3 varchar(10))no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create view a17view1(a,b) as select col1,col2 from a17tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
       
    #user without authority to grant
    stmt = """grant select on a17tab1 to grobj_a17role1 by qauser_teg;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1017')
        
    stmt = """grant select on a17tab1 to qauser_sqlqaa by qauser_teg;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1017')
        
    stmt = """grant all on a17view1 to grobj_a17role2 by DB__ROOT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """grant all on a17view1 to qauser_sqlqaa by DB__ROOT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)         

    stmt = """grant role grobj_a17role1,grobj_a17role2 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    #process qauser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a17tab1 values(2,3,'dfw');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  
        
    stmt = """select * from a17tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  

    stmt = """insert into a17view1 values(1,2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)

    stmt = """select * from a17view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

    #process qauser_sqlqab
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema grantsch11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a17tab1 values(2,3,'dfw');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
        
    stmt = """select * from a17tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    stmt = """insert into a17view1 values(1,2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)

    stmt = """select * from a17view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)  

    stmt = """revoke all on a17view1 from grobj_a17role2 by DB__ROOT;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
        
    stmt = """revoke all on a17view1 from qauser_sqlqaa by DB__ROOT;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)         

    stmt = """revoke role grobj_a17role1,grobj_a17role2 from qauser_sqlqab;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)    
        
    stmt = """set schema grantsch11;"""  
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """drop view a17view1;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """drop table a17tab1;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """drop schema grantsch11;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a17role1;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a17role2;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    
    _testmgr.testcase_end(desc)

    
def testa12(desc="""grant priv on object to role/user with grant option(n) by"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
 
    stmt = """create role grobj_a18role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create role grobj_a18role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create schema grantsch18;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """set schema grantsch18;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a18tab1(col1 int  not null primary key,col2 int ,col3 varchar(10));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a18tab2(a int ,b int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant insert(col1,col2), select(col1,col2) on a18tab1 to grobj_a18role1 with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant update(col2) on a18tab1 to grobj_a18role1 with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """grant update(col2) on a18tab1 to  grobj_a18role2 with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant select on a18tab2 to grobj_a18role1 with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """grant select on a18tab2 to  qauser_sqlqaa with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant insert on a18tab2 to grobj_a18role1 with grant option by DB__ROOT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """grant insert on a18tab2 to  qauser_sqlqaa,  with grant option by DB__ROOT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """grant insert on a18tab2 to grobj_a18role2 with grant option by DB__ROOT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a18role1,grobj_a18role2 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    #process qauser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch18;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant all on a18tab2 to qauser_sqlqab with grant option;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #process qauser_sqlqab
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema grantsch18;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a18tab1 values(1,2,'dfa');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """insert into a18tab1(col1,col2) values(2,2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
        
    stmt = """select * from a18tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """select col1 from a18tab1 where col2=2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

    stmt = """update a18tab1 set col2=1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_updated_msg(output,1) 

    stmt = """insert into a18tab2 values(1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)  

    stmt = """select * from a18tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)
        
    stmt = """delete from a18tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,1) 

        
    stmt = """revoke insert(col1,col2), select(col1,col2) on a18tab1 from grobj_a18role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """revoke update(col2) on a18tab1 from grobj_a18role1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """revoke update(col2) on a18tab1 from  grobj_a18role2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke select on a18tab2 from grobj_a18role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """revoke select on a18tab2 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """revoke insert on a18tab2 from grobj_a18role1 by DB__ROOT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """revoke insert on a18tab2 from  qauser_sqlqaa by DB__ROOT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """revoke insert on a18tab2 from  grobj_a18role2 by DB__ROOT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    

    stmt = """revoke role grobj_a18role1,grobj_a18role2 from qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """set schema grantsch18;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop table a18tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop table a18tab2;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)         
    stmt = """drop schema grantsch18;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a18role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a18role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    _testmgr.testcase_end(desc)
    
def testa13(desc="""grantor has no authority to grant with grant option"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create role grobj_a19role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """create role grobj_a19role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create schema grantsch19;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """set schema grantsch19;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a19tab1(col1 int, col2 int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select on a19tab1 to grobj_a19role1 with grant option by qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1017')
        
    stmt = """grant select on a19tab1 to qauser_teg with grant option by qauser_sqlqaa;"""  
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1017')        

    stmt = """grant select,insert on a19tab1 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select,insert on a19tab1 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """grant select on a19tab1 to grobj_a19role1 with grant option by qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '1012')

    stmt = """grant select on a19tab1 to grobj_a19role1 by qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '1012')

    #process qauser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch19;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant select on a19tab1 to grobj_a19role2 with grant option;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_warning_msg(output, '1012')

    stmt = """grant insert on a19tab1 to grobj_a19role2 with grant option by qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_warning_msg(output, '1012')
        
    #process supermxci
    stmt = """grant role grobj_a19role1 to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a19role2 to qauser_teg;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    #process qauser_tsang
    mydci = basic_defs.switch_session_qi_user4()
    
    stmt = """set schema grantsch19;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select * from a19tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    #process qauser_teg
    mydci = basic_defs.switch_session_qi_user5()
    
    stmt = """set schema grantsch19;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a19tab1 values(1,2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')   

    stmt = """select * from a19tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')   

    stmt = """revoke role grobj_a19role1 from qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a19role2 from qauser_teg;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)      
    stmt = """revoke select,insert on a19tab1 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)   
    stmt = """revoke select,insert on a19tab1 from qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)     
    stmt = """set schema grantsch19;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop table a19tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)        
    stmt = """drop schema grantsch19;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a19role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a19role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    _testmgr.testcase_end(desc)
    

    
def testa14(desc="""grant privs on object to predefine users/roles"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
        
    stmt = """create schema grantsch22;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """set schema grantsch22;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a22tab1(col1 int, col2 int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a22tab2(a int,b int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create view a22view1(c,d) as select a22tab1.col1,a22tab2.a from a22tab1,a22tab2 where a22tab1.col2=a22tab2.b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
        #predefine user
    stmt = """grant select on a22tab1 to DB__ROOTROLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant insert on a22tab1 to DB__ROOTROLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
        #predefine user and role
    stmt = """grant insert on a22tab2 to DB__ROOTROLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
        #predefine role
    stmt = """grant select on a22view1 to DB__ROOTROLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant all on a22tab2 to public;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role DB__ROOTROLE to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
        #current_user
    stmt = """grant all on a22tab1 to current_user ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """grant select on a22tab1 to current_user;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    #process qauser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()
    stmt="""set schema grantsch22;"""
    output = mydci.cmdexec(stmt)

    stmt="""insert into a22tab1 values(1,2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)

    stmt="""select * from a22tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

        #process supermxci
    stmt = """set schema grantsch22;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """insert into a22tab1 values(1,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,1)
        
    stmt = """select * from a22tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output,2)

    stmt = """insert into a22tab2 values(2,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,1)

    stmt = """select * from a22view1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output,2)

      

    stmt = """set schema grantsch22;"""
    output = mydci.cmdexec(stmt)

    stmt = """insert into a22tab1 values(11,22);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)

    stmt = """select * from a22tab1 where col2=22;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    stmt = """select * from a22view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)
        
                
    stmt = """revoke select on a22tab1 from DB__ROOTROLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke insert on a22tab1 from DB__ROOTROLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke insert on a22tab2 from DB__ROOTROLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)        
    stmt = """revoke select on a22view1 from DB__ROOTROLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke all on a22tab2 from public;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke role db__rootrole from quaser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """set schema grantsch22;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop view a22view1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop table a22tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop table a22tab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop schema grantsch22;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)
    

def testa15(desc="""grant privs on object to role by predefined username"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
       
    stmt = """create role grobj_a23role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """create role grobj_a23role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create schema grantsch23;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """set schema grantsch23;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a23tab1(a int,b int,c int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant insert(a,c),select(a) on a23tab1 to grobj_a23role1 by DB__ROOT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant insert(b,c),select(b) on a23tab1 to grobj_a23role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a23role1 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """grant role grobj_a23role1 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant role grobj_a23role2 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """grant role grobj_a23role2 to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    #process qauser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch23;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a23tab1 values(1,2,3);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  

    stmt = """select * from a23tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  

    stmt = """insert into a23tab1(a,c) values(1,3);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 

    stmt = """select a from a23tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

    #process qauser_sqlqab
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema grantsch23;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a23tab1 values(1,2,3);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)

    stmt = """select * from a23tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  

    stmt = """insert into a23tab1(b,c) values(1,3);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 

    stmt = """select a from a23tab1 where b=1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

    stmt = """select c from a23tab1 where b=1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """select * from a23tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    #process qauser_tsang
    mydci = basic_defs.switch_session_qi_user4()
    
    stmt = """set schema grantsch23;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a23tab1(a,b,c) values(1,2,3);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  

    stmt = """insert into a23tab1(c) values(3);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 

    stmt = """select b from a23tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,4)

    stmt = """select c from a23tab1 where b=3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  
        
    #process supermxci
    stmt = """set schema grantsch23;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop table a23tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop schema grantsch23;"""
    output = _dci.cmdexec(stmt)    
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a23role1 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a23role1 from qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """revoke role grobj_a23role2 from qauser_sqlqab,qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a23role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a23role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    _testmgr.testcase_end(desc)
    
    
def testa16(desc="""grant privs on object to user by predefined rolename"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create role grobj_a24role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create schema grantschsch24;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """set schema grantsch24;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a24tab1(a int,b int,c int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select on a24tab1 to qauser_sqlqab by DB__ROOTROLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1017')
        
    stmt = """grant select on grobj_a24role1 to qauser_sqlqab by DB__ROOTROLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1017')
        
    stmt = """grant insert on grobj_a24role1 to qauser_sqlqab by DB__ROOTROLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1017')
        
    stmt = """grant insert on a24tab1 to qauser_sqlqab by DB__ROOTROLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1017')

    stmt = """grant role grobj_a24role1 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    #process qauser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch24;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a24tab1(a,b,c) values(1,2,3);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """select a,b from a24tab1 where c=3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
        
    #process supermxci
    stmt = """set schema grantsch24;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)        
    stmt = """drop table a24tab1;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """drop schema grantsch24;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a24role1 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a24role1;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    
    _testmgr.testcase_end(desc)
    
    
def testa17(desc="""grant priv on obj to user,grant more than one role to user"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create role grobj_a28role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create role grobj_a28role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create schema grantsch28;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """set schema grantsch28;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a28tab1(a int, b int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a28tab2(col1 int, b int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select on table a28tab1 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select on a28tab2 to grobj_a28role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant insert on a28tab2 to grobj_a28role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a28role1,grobj_a28role2 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    #process qauser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch28;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a28tab1 values(1,2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    stmt = """select * from a28tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """insert into a28tab2 values(1,2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)

    stmt = """select * from a28tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

    stmt = """set schema grantsch28;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop table a28tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop table a28tab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop schema grantsch28;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a28role1,grobj_a28role2 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a28role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a28role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    _testmgr.testcase_end(desc)
    
    
def testa18(desc="""grant priv on obj to user plus grant priv on obj to role"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create role grobj_a29role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create schema grantsch29;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """set schema grantsch29;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a29tab1(col1 int, col2 int, col3 varchar(10))no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select ,delete on a29tab1 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select ,insert on a29tab1 to grobj_a29role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a29role1 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    #process qauser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch29;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a29tab1 values(1,2,'af'),(2,4,'asdf');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,2) 

    stmt = """select * from a29tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)

    stmt = """delete  from a29tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,2) 

    #process supermxci
    stmt = """set schema grantsch29;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """revoke select ,insert on a29tab1 from grobj_a29role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    time.sleep(10)
    time.sleep(10)

    #process qauser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch29;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a29tab1 values(1,2,'af'),(2,4,'asdf');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    

    stmt = """select * from a29tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """delete from a29tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,0)  
        #process supermxci
    stmt = """set schema grantsch29;"""
    _dci.expect_complete_msg(output) 

    stmt = """grant select ,insert on a29tab1 to grobj_a29role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """revoke select ,delete on a29tab1 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    time.sleep(10)

    #process auser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch29;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a29tab1 values(1,2,'af'),(2,4,'asdf');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,2) 

    stmt = """select * from a29tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)

    stmt = """delete from a29tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    #process supermxci
    stmt = """revoke select ,delete on a29tab1 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a29role1 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """set schema grantsch29;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop table a29tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)         
    stmt = """drop schema grantsch29;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a29role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    _testmgr.testcase_end(desc)

def testa19(desc="""grant priv on obj to role1 role2 then grant role1 role3 and role4 to user"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create role grobj_a31role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create role grobj_a31role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create role grobj_a31role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create role grobj_a31role4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create schema grantsch31;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """set schema grantsch31;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a31tab1(a int, b int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt ="""create table a31tab2(col1 int, col2 int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """grant select on a31tab1 to grobj_a31role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select on a31tab2 to grobj_a31role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """grant insert,delete on a31tab1 to grobj_a31role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant insert,delete on a31tab2 to grobj_a31role4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a31role1,grobj_a31role3,grobj_a31role4 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    #stmt="""grant create_view on schema grantsch31 to qauser_sqlqaa;"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_complete_msg(output) 

    #process qauser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch31;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
        
    stmt = """insert into a31tab1 values(1,2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
        
    stmt = """select * from a31tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)
        
    stmt = """delete from a31tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,1)

    stmt = """insert into a31tab2(col1) values(1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)

    stmt = """select * from a31tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """delete  from a31tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,1) 
        
    stmt = """create view a31view1 as select * from a31tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a31view2 as select * from a31tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  
        
    stmt = """create view a31view3(a,b) as select a31tab1.a,a31tab2.col1 from a31tab1,a31tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  

    #process supermxci
    stmt = """revoke role grobj_a31role1,grobj_a31role3,grobj_a31role4 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """set schema grantsch31;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop view a31view1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a31tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop table a31tab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop schema grantsch31;"""  
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)         
    stmt = """drop role grobj_a31role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a31role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a31role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a31role4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    _testmgr.testcase_end(desc)
    
    
def testa20(desc="""grant priv to different role then grant roles to user"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return


    stmt = """create role grobj_a32role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create role grobj_a32role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create schema grantsch32;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """set schema grantsch32;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a32tab1(col1 int,col2 int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a32tab2(a int, b int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select, insert on a32tab1 to grobj_a32role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant insert on a32tab2 to grobj_a32role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select on a32tab2 to grobj_a32role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a32role1,grobj_a32role2 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a32role2 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt="""grant create_view on schema grantsch32 to qauser_sqlqaa ;"""
    output = _dci.cmdexec(stmt)
    
    stmt="""grant create_view on schema grantsch32 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)

    #process qauser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch32;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
        
    stmt = """insert into a32tab1 values(1,2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
        
    stmt = """select * from a32tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)
        
    stmt = """insert into a32tab2 values(1,3);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
        
    stmt = """select * from a32tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)
        
    stmt="""create view a32view1(a,b) as select a32tab1.col2,a32tab2.b from a32tab1,a32tab2 where a32tab1.col1=a32tab2.a;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    #process qauser_sqlqab
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema grantsch32;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select * from a32tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

    stmt = """insert into a32tab2 values(1,2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  

    stmt="""select * from a32view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    #process supermxci        
    stmt = """revoke role grobj_a32role1,grobj_a32role2 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a32role2 from qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a32role1 from qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """set schema grantsch32;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop view a32view1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop table a32tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop table a32tab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)         
    stmt = """drop schema grantsch32;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a32role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a32role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    _testmgr.testcase_end(desc)
    
    
def testa21(desc="""grant priv on same obj to role vary  priv and roles on object"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
        
    stmt = """create role grobj_a33role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create role grobj_a33role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create schema grantsch33;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """set schema grantsch33;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a33tab1(col1 int, col2 int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select(col1) on a33tab1 to grobj_a33role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant insert,select(col2) on a33tab1 to grobj_a33role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a33role1 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a33role2 to qauser_sqlqaa, qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt="""grant create_view on schema grantsch33 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    
    stmt="""grant create_view on schema grantsch33 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)

    #process qauser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch33;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a33tab1 values(1,2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
        
    stmt = """select col1 from a33tab1 where col2=2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)
    
    stmt = """create view a33view1 as select * from a33tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #process qauser_sqlqab
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema grantsch33;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
        
    stmt = """insert into a33tab1 values(1,2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 

    stmt = """select col1 from a33tab1 where col2=2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """select col2 from a33tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,2)

    stmt = """create view a33view2 as select * from a33tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """create view a33view3(a) as select a33tab1.col2 from a33tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
        
    #process supermxci
    stmt = """set schema grantsch33;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select(col1) on a33tab1 to grobj_a33role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    #process qauser_sqlqab
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema grantsch33;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select * from a33tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)

    stmt = """create view a33view4 as select * from a33tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
        
        
    #process supermxci
    stmt = """set schema grantsch33;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop view a33view1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view a33view2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view a33view3;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view a33view4;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a33tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop schema grantsch33;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a33role1 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a33role2 from qauser_sqlqaa, qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a33role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a33role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    _testmgr.testcase_end(desc)
    
def testa22(desc="""grant priv to user with grant option then user grant priv to role"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create role grobj_a34role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create role grobj_a34role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create schema grantsch34;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """set schema grantsch34;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a34tab1(a int, b int, c int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select on a34tab1 to  qauser_sqlqaa with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant insert on a34tab1 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant insert on a34tab1 to grobj_a34role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a34role1 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a34role2 to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant create_view on schema grantsch34 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """grant create_view on schema grantsch34 to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #process qauser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch34;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant select on a34tab1 to grobj_a34role1,grobj_a34role2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant insert on a34tab1 to grobj_a34role2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(stmt, '1012') 
        
    #process qauser_sqlqab
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema grantsch34;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a34tab1 values(1,2,3);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt = """select * from a34tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

    stmt = """create view a34view1 as select * from a34tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #process qauser_tsang
    mydci = basic_defs.switch_session_qi_user4()
    
    stmt = """set schema grantsch34;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a34tab1 values(1,2,3);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    stmt = """select * from a34tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

    stmt = """create view a34view2 as select * from a34tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    #process supermxci
    stmt = """set schema grantsch34;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop view a34view1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop view a34view2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop table a34tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop schema grantsch34;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a34role1 from qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a34role2 from qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a34role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a34role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    _testmgr.testcase_end(desc)
    
def testa23(desc="""user unable to grant all priv in <priv-list> to role/user"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create role grobj_a35role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create role grobj_a35role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create schema grantsch35;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """set schema grantsch35;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a35tab1(a int, b int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant insert on a35tab1 to qauser_sqlqaa with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select on a35tab1 to qauser_sqlqab with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a35role1 to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a35role2 to qauser_teg;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    #process qauser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch35;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant select on a35tab1 to grobj_a35role1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1012') 

    stmt = """grant insert ,select on a35tab1 to grobj_a35role1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_warning_msg(output, '1013') 

    stmt = """grant select,insert on a35tab1 to grobj_a35role2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_warning_msg(output, '1013') 

    #process qauser_sqlqab
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema grantsch35;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant delete on a35tab1 to grobj_a35role1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1012') 

    stmt = """grant delete ,select on a35tab1 to grobj_a35role2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_warning_msg(output, '1013') 

    stmt = """grant delete ,insert on a35tab1 to grobj_a35role2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_warning_msg(output, '1013') 

    #process qauser_tsang
    mydci = basic_defs.switch_session_qi_user4()
    
    stmt = """set schema grantsch35;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
        
        #expect any *ERROR[4481]*
        #$SQL_inserted_msg '1'
    stmt = """insert into a35tab1 values(1,2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
        
    stmt = """select * from a35tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    stmt = """delete from a35tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    #process qauser_teg
    mydci = basic_defs.switch_session_qi_user5()
    
    stmt = """set schema grantsch35;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 
        
        #expect any *ERROR[4481]*
        #$SQL_inserted_msg '1'
    stmt = """insert into a35tab1 values(1,2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)

    stmt = """select * from a35tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

    stmt = """delete from a35tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
        
    #process supermxci
    stmt = """set schema grantsch35;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop table a35tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop schema grantsch35;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a35role1 from qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a35role2 from qauser_teg;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a35role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a35role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    _testmgr.testcase_end(desc)
    
    
def testa24(desc="""grant column priv to role that has already granted object priv"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create role grobj_a36role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create role grobj_a36role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """create schema grantsch36;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """set schema grantsch36;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a36tab1(col1 int,col2 int, col3 int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select ,insert on a36tab1 to grobj_a36role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant all on a36tab1 to grobj_a36role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select(col1,col2) on a36tab1 to grobj_a36role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select(col3), insert(col2,col3) on a36tab1 to grobj_a36role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a36role1 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a36role2 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    #process qauser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch36;"""
    
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a36tab1 values(1,2,4);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)

    stmt = """insert into a36tab1(col1,col2) values(2,4);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)

    stmt = """select col1 from a36tab1 where col2=2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

    stmt = """select * from a36tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)

    stmt = """delete from a36tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    #process qauser_sqlqab
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema grantsch36;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a36tab1 values(1,2,4);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)

    stmt = """insert into a36tab1(col2,col3) values(2,4);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)

    stmt = """select col1 from a36tab1 where col3=4;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,3)

    stmt = """select * from a36tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,4)

    stmt = """delete from a36tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,4)

    #process supermxci
    stmt = """set schema grantsch36;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """drop table a36tab1;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """drop schema grantsch36;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a36role1 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a36role2 from qauser_sqlqab;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a36role1;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a36role2;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    
    _testmgr.testcase_end(desc)
    
    
def testa25(desc="""grant column priv to user  grant obj priv to role"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create role grobj_a37role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create role grobj_a37role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create role grobj_a37role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create schema grantsch37;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """set schema grantsch37;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a37tab1(a int ,b int ,c int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a37tab2(col1 int, col2 int ,col3 varchar(10))no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create view a37view1 as select * from a37tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create view a37view2(AA ,BB) as select a37tab1.a,a37tab2.col3 from a37tab1,a37tab2 where a37tab1.b=a37tab2.col2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create mv a37mv1 refresh on request initialize on refresh as select * from a37tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """maintain mv a37mv1, refresh;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create mv a37mv2(a,b) refresh on request initialize on refresh as select a37tab1.a,a37tab2.col3 from a37tab1,a37tab2 where a37tab1.b=a37tab2.col2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """maintain mv a37mv2, refresh;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create trigger a37trig1 after update on a37tab1 REFERENCING NEW AS newR FOR EACH ROW insert into a37tab1 values(1,1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select(a) on a37tab1 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select(col1,col2) on a37tab2 to qauser_sqlqaa,qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select(a,b) on a37view1 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select(AA) on a37view2 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select(b,c) on a37mv1 to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select(a) on a37mv2 to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select, insert on a37tab1 to grobj_a37role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select on a37tab2 to grobj_a37role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select on a37view1 to grobj_a37role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select on a37view2 to grobj_a37role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select on a37mv1 to grobj_a37role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select on a37mv2 to grobj_a37role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a37role1 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a37role2 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a37role3 to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    #process secpamxci
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch37;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select a from a37tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """select * from a37tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """select col1 from a37tab2 where col2=1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """select col1,col3 from a37tab2 where col2=2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """select a,b from a37view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """select * from a37view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """select * from a37view2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """select * from a37mv1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """select * from a37mv2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """update a37tab1 set a=a+1 where a<0;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    #process qauser_sqlqab
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema grantsch37;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select b from a37tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')   

    stmt = """select * from a37tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')   

    stmt = """select col1 from a37tab2 where col2=1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """select col1,col3 from a37tab2 where col2=2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')   

    stmt = """select AA from a37view2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """select BB from a37view2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """select * from a37view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    #process qauser_tsang
    mydci = basic_defs.switch_session_qi_user4()
    
    stmt = """set schema grantsch37;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select b,c from a37mv1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """select b,c from a37mv1 where a=1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """select a from a37mv2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """select a from a37mv2 where b='1';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """select AA from a37view2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """select BB from a37view2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """select a from a37tab1 where b=1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """select col3 from a37tab2 where col2=1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    #process supermxci
    stmt = """set schema grantsch37;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant update(a) on a37tab1 to grobj_a37role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a37role1 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    #process qauser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch37;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
        
    stmt = """update a37tab1 set a=a+1 where a<0;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_updated_msg(output,0) 

    #process qauser_sqlqab
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema grantsch37;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select b from a37tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """select * from a37tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """select col1 from a37tab2 where col2=1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """select col1,col3 from a37tab2 where col2=2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """select AA from a37view2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """select BB from a37view2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """select * from a37view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    #process supermxci
    stmt = """set schema grantsch37;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """drop table a37tab1;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """drop table a37tab2;"""  
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)         
    stmt = """drop schema grantsch37;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a37role1 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a37role2 from qauser_sqlqab;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a37role3 from qauser_tsang;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a37role1;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a37role2;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a37role3;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    
    _testmgr.testcase_end(desc)
    
    
def testa26(desc="""grant obj priv to user  grant column priv to role"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create role grobj_a38role1;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 

    stmt = """create role grobj_a38role2;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 

    stmt = """create role grobj_a38role3;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 

    stmt = """create schema grantsch38;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 

    stmt = """set schema grantsch38;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 

    stmt = """create table a38tab1(a int ,b int ,c int)no partition;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 

    stmt = """create table a38tab2(col1 int, col2 int ,col3 varchar(10))no partition;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 

    stmt = """create view a38view1 as select * from a38tab1;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 

    stmt = """create view a38view2(AA,BB) as select a38tab1.a,a38tab2.col3 from a38tab1,a38tab2 where a38tab1.b=a38tab2.col2;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 

    stmt = """create mv a38mv1 refresh on request initialize on refresh as select * from a38tab1;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 

    stmt = """maintain mv a38mv1, refresh;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 

    stmt = """create mv a38mv2(a,b) refresh on request initialize on refresh as select a38tab1.a,a38tab2.col3 from a38tab1,a38tab2 where a38tab1.b=a38tab2.col2;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 

    stmt = """maintain mv a38mv2, refresh;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 

    stmt = """create trigger a38trig1 after update on a38tab1 REFERENCING NEW AS newR FOR EACH ROW insert into a38tab1(a,b) values(1,1);"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 


    stmt = """grant select,insert(a,b,c) on a38tab1 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 

    stmt = """grant select on a38tab2 to qauser_sqlqaa,qauser_sqlqab;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 

    stmt = """grant select on a38view1 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 

    stmt = """grant select on a38view2 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 

    stmt = """grant select on a38mv1 to qauser_tsang;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 

    stmt = """grant select on a38mv2 to qauser_tsang;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 

    stmt = """grant select(a),insert(a), update(a) on a38tab1 to grobj_a38role1;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 

    stmt = """grant select(col1,col2) on a38tab2 to grobj_a38role1;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    
    stmt = """grant select(col1,col2) on a38tab2 to grobj_a38role2;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)

    stmt = """grant select(a,b) on a38view1 to grobj_a38role1;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 

    stmt = """grant select(AA) on a38view2 to grobj_a38role2;"""
    _dci.expect_complete_msg(output) 

    stmt = """grant select(b,c) on a38mv1 to grobj_a38role3;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 

    stmt = """grant select(a) on a38mv2 to grobj_a38role3;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a38role1 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a38role2 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a38role3 to qauser_tsang;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 

    #process qauser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch38;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select a from a38tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """select * from a38tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """select col1 from a38tab2 where col2>0;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """select col1,col3 from a38tab2 where col2>0;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """update a38tab1 set a=1 where a<0;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_updated_msg(output,0)   
        
    stmt = """select * from a38view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """select AA from a38view2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    stmt = """select * from a38mv1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    stmt = """select * from a38mv2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    #process qauser_sqlqab
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema grantsch38;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
        
    stmt = """select * from a38tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    stmt = """select a from a38tab1 where b>0;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    stmt = """select col1 from a38tab2 where col2>0;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """select * from a38tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """select * from a38view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')   

    stmt = """select AA from a38view2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """select BB from a38view2 where AA>0;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """select * from a38mv1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """select * from a38mv2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    #process qauser_tsang
    mydci = basic_defs.switch_session_qi_user4()
    
    stmt = """set schema grantsch38;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select * from a38tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  

    stmt = """select col1 from a38tab2 where col2>0;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  

    stmt = """select a from a38view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  

    stmt = """select AA from a38view2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  

    stmt = """select col3 from a38tab2 where col2>0;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  

    stmt = """select b,c from a38mv1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """select b from a38mv2 where a>0;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    #process supermxci
    stmt = """set schema grantsch38;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """revoke select(a),insert(a) on a38tab1 from grobj_a38role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    time.sleep(10)

    stmt = """revoke select(a,b) on a38view1 from grobj_a38role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    time.sleep(10)

    stmt = """revoke select(b,c) on a38mv1 from grobj_a38role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    time.sleep(10)

    stmt = """revoke select(a) on a38mv2 from grobj_a38role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    time.sleep(10)

    #process qauser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch38;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
        
    stmt = """select a from a38tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """update a38tab1 set a=1 where a<0;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_updated_msg(output,0) 

    #process qauser_tsang
    mydci = basic_defs.switch_session_qi_user4()
    
    stmt = """set schema grantsch38;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select b from a38mv1 where c>0;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """select a from a38mv2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    #process supermxci
    stmt = """set schema grantsch38;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop view a38view1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop view a38view2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop table a38tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop table a38tab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)        
    stmt = """drop schema grantsch38;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a38role1 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a38role2 from qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a38role3 from qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a38role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a38role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a38role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    _testmgr.testcase_end(desc)
    
    
def testa27(desc="""grant col priv to user  grant col priv to role"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create role grobj_a39role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create role grobj_a39role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create role grobj_a39role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create schema grantsch39;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """set schema grantsch39;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a39tab1(col1 int,col2 int, col3 int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a39tab2(col1 int, col2 int, col3 varchar(10)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create view a39view1(col1,col2,col3) as select a39tab1.col1,a39tab1.col3,a39tab2.col3 from a39tab1,a39tab2  where a39tab1.col2=a39tab2.col2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create mv a39mv1(a,b,c) refresh on request initialize on refresh as select a39tab1.col2, a39tab2.col2,a39tab2.col3 from a39tab1,a39tab2 where a39tab1.col1=a39tab2.col2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """maintain mv a39mv1, refresh;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant insert(col1,col2),select(col1,col2) on a39tab1 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant insert(col1,col3),select(col1,col3) on a39tab2 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select(col1,col2) on a39view1 to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """grant select(a,b) on a39mv1 to qauser_teg;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant insert(col2,col3),select(col2,col3) on a39tab1 to grobj_a39role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant insert(col2,col3),select(col2,col3) on a39tab2 to grobj_a39role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """grant insert(col2,col3),select(col2,col3) on a39tab2 to grobj_a39role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select(col3) on a39view1 to grobj_a39role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select(c) on a39mv1 to grobj_a39role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 


    stmt = """grant role grobj_a39role1 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a39role2 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a39role3 to qauser_tsang,qauser_teg;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    #process qauser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch39;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a39tab1(col1,col2) values(1,2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)  

    stmt = """insert into a39tab1(col2,col3) values(2,4);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)  

    stmt = """insert into a39tab1 values(1,2,4);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)  

    stmt = """select col1,col2 from a39tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,3)

    stmt = """select col2, col3 from a39tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,3)

    stmt = """select col1,col3 from a39tab1 where col2>3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """insert into a39tab2(col2,col3) values(1,'2');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)  

    stmt = """insert into a39tab2(col1,col2) values(1,2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    stmt = """insert into a39tab2 values(1,2,'rt');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    stmt = """select col2,col3 from a39tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

    stmt = """select col2,col3 from a39tab2 where col1=1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    #process qauser_sqlqab
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema grantsch39;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a39tab2(col1,col3) values(1,'df');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)  

    stmt = """insert into a39tab2(col2,col3) values(2,'der');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)  

    stmt = """insert into a39tab2 values(1,2,'ddvc');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)  

    stmt = """select col1 from a39tab2 where col3 like 'd%';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,3)

    stmt = """select col3 from a39tab2 where col2=2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)

    stmt = """select col1,col2 from a39tab2 where col3='df';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

    stmt = """select col2,col3 from a39tab1 ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  

    #process qauser_tsang
    mydci = basic_defs.switch_session_qi_user4()
    
    stmt = """set schema grantsch39;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select col1 from a39view1 where col2=2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """select col1,col2,col3 from a39view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,6)

    stmt = """select * from a39view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,6)

    stmt = """select * from a39mv1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    stmt = """select c from a39mv1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """select col1,col3 from a39tab1 where col2>10;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    stmt = """select col3 from a39tab2 where col1>10;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    #process qauser_teg
    mydci = basic_defs.switch_session_qi_user5()
    
    stmt = """set schema grantsch39;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select a from a39mv1 where b>10;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """select a,c from a39mv1 where b>10;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """select * from a39mv1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """select col1,col2 from a39view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')


    #process supermxci
    stmt = """set schema grantsch39;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop view a39view1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop table a39tab1;"""
    _dci.expect_complete_msg(output) 
    stmt = """drop table a39tab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop schema grantsch39;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a39role1 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a39role2 from qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a39role3 from qauser_tsang,qauser_teg;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a39role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a39role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a39role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    _testmgr.testcase_end(desc)

    
def testa28(desc="""grant obj priv to user with grant option user grant col pri to role"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create role grobj_a40role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create role grobj_a40role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create schema grantsch40;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """set schema grantsch40;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a40tab1(a int not null primary key, b int, c varchar(10));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create view a40view1(aa,bb,cc) as select a,b,c from a40tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant create_table on schema grantsch40 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select,insert ,delete, update ,references(a) on a40tab1 to qauser_sqlqaa with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant insert, select on a40view1 to qauser_sqlqaa with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
        #process qauser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema grantsch40;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
        
    stmt = """grant select(a,b),insert(a),update(b,c),references(a) on a40tab1 to grobj_a40role1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
        
    stmt = """grant insert(aa,bb) ,select(aa) on a40view1 to grobj_a40role2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #process supermxci
    stmt = """grant role grobj_a40role1,grobj_a40role2 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a40role2 to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    #process qauser_sqlqab
    mydci = basic_defs.switch_session_qi_user3()

    stmt = """set schema grantsch40;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a40tab1(a) values(1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)

    stmt = """insert into a40tab1 values(1,2,'sd');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    stmt = """select * from a40tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    stmt = """select a,b from a40tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
        
        #expect any *ERROR[4481]*SELECT*
    stmt = """update a40tab1 set c='1' where c is null;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    stmt = """create table a40tab2(a int not null primary key, b int, constraint tab2check foreign key (a) references a40tab1(a));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a40view1 values(11,22,'ad');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    stmt = """select * from a40view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    stmt = """select aa from a40view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

        #process qauser_tsang
    mydci = basic_defs.switch_session_qi_user4()
    stmt = """set schema grantsch40;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
        
    stmt = """insert into a40view1 values(12,23,'asf');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    stmt = """select * from a40tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    stmt = """select * from a40view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

        #process supermxci
    stmt = """set schema grantsch40;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop view a40view1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop table a40tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop schema grantsch40;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a40role1,grobj_a40role2 from qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a40role2 from qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a40role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a40role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    _testmgr.testcase_end(desc)

    
def testa29(desc="""grant col priv to user with grant option user grant obj pri to role"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create role grobj_a41role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """create role grobj_a41role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create schema grantsch41;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """set schema grantsch41;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a41tab1(col1 int, col2 int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select(col1,col2),insert(col1,col2) on a41tab1 to qauser_sqlqaa with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    #process qauser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch41;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant select ,insert on a41tab1 to grobj_a41role1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_warning_msg(stmt, '1013') 

    stmt = """grant select(col1,col2), insert(col1,col2) on a41tab1 to grobj_a41role2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #process supermxci
    stmt = """grant role grobj_a41role1 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """grant role grobj_a41role2 to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    #process qauser_sqlqab
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema grantsch41;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a41tab1 values(1,2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 

    stmt = """insert into a41tab1(col1) values(1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 

    stmt = """select * from a41tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)

    stmt = """select col2 from a41tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)

    #process qauser_tsang
    mydci = basic_defs.switch_session_qi_user4()
    
    stmt = """set schema grantsch41;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a41tab1 values(1,2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 

    stmt = """insert into a41tab1(col1) values(1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 

    stmt = """insert into a41tab1(col2) values(3);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 

    stmt = """select * from a41tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,5)

    stmt = """select col2 from a41tab1 where col1=1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,4)

    #process supermxci
    stmt = """set schema grantsch41;"""
    output = _dci.cmdexec(stmt) 
    stmt = """drop table a41tab1;"""
    output = _dci.cmdexec(stmt) 
    stmt = """drop schema  grantsch41;"""
    output = _dci.cmdexec(stmt) 
    stmt = """revoke role grobj_a41role1 from qauser_sqlqab;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a41role2 from qauser_tsang;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a41role1;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a41role2;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    
    _testmgr.testcase_end(desc)

    
def testa30(desc="""grant col priv to role user create view on these cols"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create role grobj_a42role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create role grobj_a42role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create schema grantsch42;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """set schema grantsch42;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a42tab1(col1 int, col2 int,col3 int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a42tab2(a int ,b int ,c varchar(10))no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select(col1,col2),insert on a42tab1 to grobj_a42role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select(a,c),insert(a,c) on a42tab2 to grobj_a42role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a42role1,grobj_a42role2 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a42role2 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant create_view on schema grantsch42 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """grant create_view on schema grantsch42 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #process qauser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch42;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a42tab1 values(1,2,3);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)

    stmt = """select col1,col2 from a42tab1 where col3=3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """create view a42view1 as select col1,col2,col3 from a42tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """create view a42view2(col1,col2) as select col1,col2 from a42tab1 where col3>0;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """create view a42view3(col1,col2) as select col1,col2 from a42tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a42view4(col1,col2) as select col2,c from a42tab1,a42tab2 where col1=a;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a42view5(co11,col2) as select col3,b from a42tab1,a42tab2 where col1=a;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  

    stmt = """create view a42view6(co11,col2) as select col2,c from a42tab1,a42tab2 where col3=a;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  

    #process qauser_sqlqab
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema grantsch42;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a42tab1 values(1,2,3);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  

    stmt = """insert into a42tab2 values(1,2,'da');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  

    stmt = """insert into a42tab2(a,c) values(1,'asd');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)  

    stmt = """select a,c from a42tab2 where b=0;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  

    stmt = """select a,c from a42tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

    stmt = """create view a42view7(a,c) as select a,c from a42tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a42view7(a,c) as select a,b from a42tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  

    stmt = """create view a42view8(co11,col2) as select col3,c from a42tab1,a42tab2 where col1=a;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  

    #process supermxci
    stmt = """set schema grantsch42;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """drop table a42tab1;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """drop table a42tab2;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """drop schema grantsch42;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a42role1,grobj_a42role2 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a42role2 from qauser_sqlqab;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a42role1;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a42role2;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    
    _testmgr.testcase_end(desc)

    
def testa31(desc="""grant priv on obj to role that has been granted"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create role grobj_a44role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create role grobj_a44role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create schema grantsch44;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """set schema grantsch44;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a44tab1(a int, b int, c int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant all on a44tab1 to grobj_a44role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant all on a44tab1 to grobj_a44role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a44role1 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a44role2 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    #process qauser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch44;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a44tab1 values(1,2,3);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)

    stmt = """select * from a44tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

    stmt = """update a44tab1 set b=b+1 where c>2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_updated_msg(output,1)   

    stmt = """delete from a44tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,1)   

    #process qauser_sqlqab
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema grantsch44;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a44tab1 values(2,2,3);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 

    stmt = """select * from a44tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

    stmt = """update a44tab1 set b=b+1 where c>2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_updated_msg(output,1) 

    stmt = """delete from a44tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,1) 

    #process supermxci
    stmt = """set schema grantsch44;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 

    stmt = """grant all on a44tab1 to grobj_a44role1;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 

    stmt = """grant select ,insert, delete ,update on a44tab1 to grobj_a44role2;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 

    #process qauser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch44;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a44tab1 values(3,2,3);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)

    stmt = """select * from a44tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

    stmt = """update a44tab1 set b=b+1 where c>2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_updated_msg(output,1) 

    stmt = """delete from a44tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,1) 

    #process qauser_sqlqab
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema grantsch44;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a44tab1 values(4,2,3);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 

    stmt = """select * from a44tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

    stmt = """update a44tab1 set b=b+1 where c>2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_updated_msg(output,1)

    stmt = """delete from a44tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,1) 

    #process supermxci
    stmt = """set schema grantsch44;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)   
    stmt = """drop table a44tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop schema grantsch44;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a44role1 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a44role2 from qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a44role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a44role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    _testmgr.testcase_end(desc)

    
def testa32(desc="""grant priv to role then grant role to user who has priv to create"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create role grobj_a45role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create role grobj_a45role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create schema grantsch45;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """set schema grantsch45;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """create table a45tab1(a int, b int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """insert into a45tab1 values(1,2),(2,4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,2)

    stmt = """grant select on a45tab1 to grobj_a45role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select(a,b) on a45tab1 to grobj_a45role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a45role1 to qauser_sqlqaa,qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a45role2 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant create_table on schema grantsch45 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)

    #process qauser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch45;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a45tab2(col1 int not null primary key, col2 int);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select a from a45tab1 where b>0;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)

    #process qauser_sqlqab
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema grantsch45;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select * from a45tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)

    stmt = """select * from a45tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    #process qauser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch45;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant insert on a45tab2 to grobj_a45role1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant select(col1,col2) on a45tab2 to grobj_a45role2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)


    time.sleep(10)

    #process qauser_sqlqab
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema grantsch45;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a45tab2 values(1,2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 

    stmt = """insert into a45tab2(col1) values(2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 

    stmt = """select * from a45tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)

    stmt = """select col1 from a45tab2 where col2=2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

    stmt = """select * from a45tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)

    #process supermxci
    stmt = """set schema grantsch45;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """drop table a45tab1;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """drop table a45tab2;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """drop schema grantsch45;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a45role1 from qauser_sqlqaa,qauser_sqlqab;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a45role2 from qauser_sqlqab;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a45role1;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a45role2;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    
    _testmgr.testcase_end(desc)
    
    
def testa33(desc="""grant select on obj to role ,then grant all on obj to role"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create role grobj_a46role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create role grobj_a46role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create schema grantsch46;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """set schema grantsch46;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """create table a46tab1(a int, b int,c int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select on  a46tab1 to grobj_a46role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select(a, b) on a46tab1 to grobj_a46role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a46role1 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a46role2 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    #process qauser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch46;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select * from a46tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """insert into a46tab1 values(1,1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')    

    #process qauser_sqlqab
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema grantsch46;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select * from a46tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    stmt = """select a ,b from a46tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """insert into a46tab1 values(1,1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    #process supermxci
    stmt = """set schema grantsch46;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 

    stmt = """grant all on a46tab1 to grobj_a46role1;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 

    stmt = """grant select(c),insert,update ,delete on a46tab1 to grobj_a46role2;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 

    #process qauser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch46;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a46tab1 values(1,2,3);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
        
    stmt = """insert into a46tab1(a,b) values(11,22);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
        
    stmt = """select a,b from a46tab1 where c=3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

    stmt = """update a46tab1 set b=b+1 where c>2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_updated_msg(output,1) 

    stmt = """delete from a46tab1 where c>2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,1)

    #process qauser_sqlqab
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema grantsch46;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a46tab1 values(12,12,12);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 

    stmt = """select a, b from a46tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)       

    stmt = """select * from a46tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)

    stmt = """update a46tab1 set c=c+1 where b=12;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_updated_msg(output,1)

    stmt = """delete from a46tab1 where b=3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,0) 
        
    #process supermxci
    stmt = """set schema grantsch46;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop table a46tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop schema grantsch46 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a46role1 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a46role2 from qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a46role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a46role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    _testmgr.testcase_end(desc)

    
def testa34(desc="""grantor did not create table has no priv but is granted role"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create role grobj_a47role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create role grobj_a47role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create schema grantsch47;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """set schema grantsch47;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a47tab1(a int,b int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a47tab2(col1 int ,col2 int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create view a47view1(aa,bb) as select b,col2 from a47tab1,a47tab2 where a=col1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select on a47view1 to qauser_sqlqaa with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a47role1,grobj_a47role2 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a47role2 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    #process to qauser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch47;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant select on a47view1 to grobj_a47role2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant select on a47view1 to grobj_a47role1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant select on a47tab1 to grobj_a47role1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(stmt, '1017')

    stmt = """grant select on a47tab2 to grobj_a47role1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(stmt, '1017')
    
    stmt = """grant select on a47tab2 to grobj_a47role2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(stmt, '1017')

    stmt = """select * from a47tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """select * from a47tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """select * from a47view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    #process qauser_sqlqab
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema grantsch47;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select * from a47view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """select * from a47tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """select * from a47tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    #process supermxci
    stmt = """set schema grantsch47;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop table a47tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop table a47tab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop schema grantsch47;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a47role1,grobj_a47role2 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a47role2 from qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a47role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a47role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    _testmgr.testcase_end(desc)

def testa35(desc="""u1 grant priv on obj to role u2 consecutive grant priv to role"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create role grobj_a49role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create role grobj_a49role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create schema grantsch49;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """set schema grantsch49;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a49tab1(a int,b int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a49tab2(col1 int, col2 int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select on schema grantsch49 to qauser_sqlqaa with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select on a49tab1 to qauser_sqlqab with grant option ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select(col1,col2) on a49tab2 to  qauser_sqlqab with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    #process qauser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch49;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant select on a49tab1 to grobj_a49role1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(stmt, '1017')
        
    stmt = """grant select(a,b) on a49tab1 to grobj_a49role2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(stmt, '1017')

    stmt = """grant select on a49tab1 to grobj_a49role2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(stmt, '1017')

    #process qauser_sqlqab
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema grantsch49;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
        
    stmt = """grant select on a49tab1 to grobj_a49role1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant select on a49tab2 to grobj_a49role2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_warning_msg(stmt, '1013')

    stmt = """grant select(col1,col2) on a49tab2 to grobj_a49role2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #process supermxci
    stmt = """grant role grobj_a49role1 to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a49role2 to qauser_teg;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    #process qauser_tsang
    mydci = basic_defs.switch_session_qi_user4()
    
    stmt = """set schema grantsch49;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select * from a49tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """select a from a49tab1 where b>0;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

    stmt = """select col1 from a49tab2 where col2>0;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    #process qauser_teg
    mydci = basic_defs.switch_session_qi_user5()
    
    stmt = """set schema grantsch49;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select * from a49tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    stmt = """select a from a49tab1 where b>0;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    stmt = """select col1 from a49tab2 where col2>0;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """select * from a49tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    #process supermxci
    stmt = """set schema grantsch49;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)        
    stmt = """drop table a49tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop table a49tab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop schema grantsch49;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a49role1 from qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a49role2 from qauser_teg;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a49role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a49role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    _testmgr.testcase_end(desc)
    
    
def testa36(desc="""u1 get select priv then create view and mv in his own schema"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create role grobj_a50role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create role grobj_a50role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create schema grantsch50a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """set schema grantsch50a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a50tab1(a int,b int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select(a) on a50tab1 to grobj_a50role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant select(b) on a50tab1 to grobj_a50role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a50role1,grobj_a50role2 to qauser_sqlqaa,qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    #process qauser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """create schema grantsch50b;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema grantsch50b;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a50view1 as select * from grantsch50a.a50tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a50view2(a) as select a from grantsch50a.a50tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt="""create mv a50mv1 refresh on request initialize on refresh as select * from grantsch50a.a50tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #process secpbmxci
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema grantsch50a;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select * from a50tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """select * from grantsch50b.a50view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  

    stmt = """select * from grantsch50b.a50view2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  

    stmt="""select * from grantsch50b.a50mv1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    #process supermxci
    stmt = """set schema grantsch50b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop view a50view1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop view a50view2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """set schema grantsch50a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop table a50tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop schema grantsch50a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop schema grantsch50b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a50role1,grobj_a50role2 from qauser_sqlqaa,qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a50role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a50role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    _testmgr.testcase_end(desc)

    
def testa37(desc="""add column to table verify user priv on new columns"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
        
        
    stmt = """create role grobj_a52role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create role grobj_a52role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create schema grantsch52;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """set schema grantsch52;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a52tab1(a int,b int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table a52tab2(col1 int, col2 int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """alter table a52tab1 add column c varchar(10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """alter table a52tab2 add column col3 varchar(10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant insert,select on a52tab1 to grobj_a52role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant insert(col1,col2),select(col1,col2) on a52tab2 to grobj_a52role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a52role1 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant role grobj_a52role2 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    #process qauser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch52;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a52tab1 values(1,1,'sdf');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)

    stmt = """select a,b from a52tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

    stmt = """select * from a52tab1 ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

    #process qauser_sqlqab
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema grantsch52;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a52tab2(col1,col2) values(1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)

    stmt = """insert into a52tab2 values(1,1,'adf');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    stmt = """select col1 from a52tab2 where col2=1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

    stmt = """select * from a52tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    #process supermxci
    stmt = """set schema grantsch52;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
   
    stmt = """alter table a52tab1 add column d varchar(10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """alter table a52tab2 add column col4 varchar(10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """grant insert(col3),select(col3) on a52tab2 to grobj_a52role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    #process qauser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch52;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a52tab1 values(1,1,'sdf','adffad');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)

    stmt = """select a,b,c from a52tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)

    stmt = """select * from a52tab1 ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)

    #process qauser_sqlqab
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema grantsch52;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a52tab2(col1,col2) values(1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)

    stmt = """insert into a52tab2(col1,col2,col3) values(1,2,'adf');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)

    stmt = """insert into a52tab2(col1,col2,col3,col4) values(1,1,'adf','adfa');"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  

    stmt = """select col1 from a52tab2 where col2=2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

    stmt = """select col1,col2,col3 from a52tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,3)

    stmt = """select * from a52tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  

    #process supermxci        
    stmt = """set schema grantsch52;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop table a52tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop table a52tab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop schema grantsch52;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a52role1 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a52role2 from qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a52role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a52role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    _testmgr.testcase_end(desc)


def testa38(desc="""grant prv on library to user/role"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
          
    stmt = """create role grobj_a53role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)   
        
    stmt = """create schema grantsch39;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """set schema grantsch39;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """create library lib1 file '/opt/home/chenjuan/pyframe/dfr.jar';"""    
    output = _dci.cmdexec(stmt)    
    _dci.expect_complete_msg(output) 
        
    stmt = """grant COMPONENT privilege create_library on sql_operations to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """ grant alter_library on lib1 to grobj_a53role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt = """grant role grobj_a53role1 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    #process qauser_sqlqaa
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema grantsch39;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create library lib2 file '/opt/home/chenjuan/pyframe/dfr_rs.jar';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
        
    stmt = """ alter library lib1 file '/opt/home/chenjuan/pyframe/dfr.jar';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(stmt, '1017')    
        
    stmt = """drop library lib1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(stmt, '1017') 
        
    stmt = """drop library lib2;"""       
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
        
    #process qauser_sqlqab
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema grantsch39;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create library lib3 file '/opt/home/chenjuan/pyframe/dfr_rs.jar';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(stmt, '1017')
        
    stmt = """alter library lib1 file '/opt/home/chenjuan/pyframe/dfr.jar';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
        
    stmt = """drop library lib1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(stmt, '1017')
        
    #process db-root
    stmt = """set schema grantsch39;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)         
    stmt = """revoke COMPONENT privilege create_library on sql_operations from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """ revoke alter_library on lib1 from grobj_a53role1;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """revoke role grobj_a53role1 from qauser_sqlqab;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """drop library lib1;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output) 
    stmt = """drop role grobj_a53role1;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)  
    stmt = """drop schema grantsch39;"""
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)        
    
    _testmgr.testcase_end(desc)


 
def testa39(desc="""propagate privileges to referencing views at grant time"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    #run as user1
    stmt = """create schema user1;"""
    output = _dci.cmdexec(stmt)

    stmt = """set schema user1;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop view v1_user1;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop view v2_user1;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop view v1_user2;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop view v2_user2;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table t1_user1;"""
    output = _dci.cmdexec(stmt)

    stmt = """set schema user1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """create table t1_user1 (c1 int not null primary key, c2 int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt = """create view v1_user1 as select * from t1_user1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt = """create view v2_user1 as select * from t1_user1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt = """grant select on t1_user1 to qauser_sqlqaa with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt = """showddl t1_user1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'GRANT SELECT ON TRAFODION.USER1.T1_USER1 TO QAUSER_SQLQAA WITH GRANT OPTION;' );

    stmt = """showddl v1_user1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'GRANT SELECT ON TRAFODION.USER1.V1_USER1 TO QAUSER_SQLQAA WITH GRANT OPTION;' );

    stmt = """showddl v2_user1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'GRANT SELECT ON TRAFODION.USER1.V1_USER1 TO QAUSER_SQLQAA WITH GRANT OPTION;' );
 
    #-- run as user2
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema user1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view v1_user2 as select * from t1_user1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view v2_user2 as select * from t1_user1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant select on t1_user1 to qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant select on v2_user2 to qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """showddl t1_user1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'GRANT SELECT ON TRAFODION.USER1.T1_USER1 TO QAUSER_SQLQAA WITH GRANT OPTION;');
    _dci.expect_any_substr(output,'GRANT SELECT ON TRAFODION.USER1.T1_USER1 TO QAUSER_SQLQAB;');

    stmt = """showddl v1_user2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'GRANT SELECT ON TRAFODION.USER1.V1_USER2 TO QAUSER_SQLQAA WITH GRANT OPTION;' );

    stmt = """showddl v2_user2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'GRANT SELECT ON TRAFODION.USER1.V2_USER2 TO QAUSER_SQLQAA WITH GRANT OPTION;' );
    _dci.expect_any_substr(output,'GRANT SELECT ON TRAFODION.USER1.V2_USER2 TO PAULLOW91;' );


    #-- run as user1
    
    stmt = """set schema user1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

         #-- adds "update" to v1_user2 and v2_user2 in addition to t1_user1
    stmt = """grant update on t1_user1 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

         #-- adds WGO to v1_user2 and v2_user2 in additiont1_user1
    stmt = """grant update on t1_user1 to qauser_sqlqaa with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """showddl t1_user1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,' GRANT SELECT,UPDATE ON TRAFODION.USER1.T1_USER1 TO QAUSER_SQLQAA WITH GRANT OPTION');
    _dci.expect_any_substr(output,' GRANT SELECT ON TRAFODION.USER1.T1_USER1 TO QAUSER_SQLQAB;' );

    stmt = """showddl v1_user2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,' GRANT SELECT,UPDATE ON TRAFODION.USER1.V1_USER2 TO QAUSER_SQLQAA WITH GRANT OPTION;');

    stmt = """showddl v2_user2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,' GRANT SELECT,UPDATE ON TRAFODION.USER1.V2_USER2 TO QAUSER_SQLQAA WITH GRANT OPTION;' );
    _dci.expect_any_substr(output,' GRANT SELECT ON TRAFODION.USER1.V2_USER2 TO PAULLOW91;' );

    stmt = """revoke select on t1_user1 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """drop table t1_user1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """drop schema user1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    _testmgr.testcase_end(desc)
 

