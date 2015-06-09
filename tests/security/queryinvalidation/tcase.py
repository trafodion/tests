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
 

def testa01(desc="""role has dependent privileges and objects"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    #process supermxci
    stmt = """create role rev_a21role1 with admin qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role rev_a21role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role rev_a21role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """grant role rev_a21role1,rev_a21role2,rev_a21role3 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create schema revsch21;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """set schema revsch21;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table rev21tab1(a int not null, b int, primary key (a));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant create,drop on schema revsch21 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant select,delete on rev21tab1 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant all_ddl on schema revsch21 to rev_a21role1,rev_a21role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant select,delete on rev21tab1 to rev_a21role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema revsch21;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table rev21tab2(a int not null, b int, primary key (a));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select * from rev21tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """delete from rev21tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,0)
    
    stmt = """drop table rev21tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """alter table rev21tab1 add column c int;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #process supermxci
    
    stmt = """set schema revsch21;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke role rev_a21role1,rev_a21role2,rev_a21role3 from qauser_sqlqaa cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    time.sleep(10)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema revsch21;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table rev21tab3(a int not null, b int, primary key (a));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select * from rev21tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """delete from rev21tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,0)

    stmt = """drop table rev21tab3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """alter table rev21tab1 add column d int;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 

    #process supermxci
    stmt = """drop schema revsch21 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role rev_a21role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role rev_a21role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role rev_a21role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

    
def testa02(desc="""user grant to user with grant option"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    #process supermxci

    stmt = """create role rev_a22role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role rev_a22role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role rev_a22role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role rev_a22role4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant role rev_a22role1,rev_a22role2,rev_a22role3,rev_a22role4 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create schema revsch22;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """set schema revsch22;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table rev22tab1(a int not null, b int, primary key (a));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant select on rev22tab1 to rev_a22role1,rev_a22role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant select on rev22tab1 to qauser_sqlqab with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant delete on rev22tab1 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant delete on rev22tab1 to rev_a22role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant select,insert,delete,update on rev22tab1 to rev_a22role4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant select on rev22tab1 to qauser_sqlqaa with grant option by qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema revsch22;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """select * from rev22tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """insert into rev22tab1 values(1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt = """delete from rev22tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,1)

    stmt = """update rev22tab1 set a=a+1 where b>1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_updated_msg(output,1)

    #process supermxci
    stmt = """set schema revsch22;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """revoke role rev_a22role1 from qauser_sqlqaa cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    time.sleep(10)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema revsch22;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select * from rev22tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    #process supermxci

    stmt = """set schema revsch22;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """revoke role rev_a22role2 from qauser_sqlqaa cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    time.sleep(10)

    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema revsch22;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select * from rev22tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    #process supermxci

    stmt = """set schema revsch22;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """revoke role rev_a22role3 from qauser_sqlqaa cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    time.sleep(10)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema revsch22;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """delete from rev22tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,0)

    #process supermxci

    stmt = """set schema revsch22;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """revoke role rev_a22role4 from qauser_sqlqaa cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    time.sleep(10)

    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema revsch22;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select * from rev22tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """insert into rev22tab1 values(1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  

    stmt = """delete from rev22tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  

    stmt = """update rev22tab1 set a=a+1 where b>1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  

    stmt = """insert into rev22tab1 values(2,2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  

    #process supermxci
    
    stmt = """drop schema revsch22 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role rev_a22role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop role rev_a22role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role rev_a22role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role rev_a22role4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)
    

def testa03(desc="""role grant to user with grant option"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    #process supermxci

    stmt = """create role rev_a23role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role rev_a23role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role rev_a23role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant role rev_a23role1,rev_a23role2,rev_a23role3 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create schema revsch23;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set schema revsch23;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table rev23tab4(a int not null, b int, primary key (a));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """grant alter,drop on schema revsch23 to rev_a23role1,rev_a23role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant all_ddl,all_dml on schema revsch23 to rev_a23role3 with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant alter,drop on schema revsch23 to qauser_sqlqaa by rev_a23role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema revsch23;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table rev23tab1(a int not null, b int, primary key (a));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """alter table rev23tab1 rename to rev23tab1_1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into rev23tab1_1 values(1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)

    #process supermxci

    stmt = """set schema revsch23;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke role rev_a23role3 from qauser_sqlqaa cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    time.sleep(10)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema revsch23;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table rev23tab2(a int not null, b int, primary key (a));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    stmt = """alter table rev23tab1_1 rename to rev23tab2_1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #process supermxci

    stmt = """set schema revsch23;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """revoke role rev_a23role1 from qauser_sqlqaa cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    time.sleep(10)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema revsch23;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table rev23tab3(a int not null, b int, primary key (a));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')

    stmt = """alter table rev23tab2_1 rename to rev23tab3_1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into rev23tab3_1 values(2,2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)

    #process supermxci

    stmt = """set schema revsch23;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke role rev_a23role2 from qauser_sqlqaa cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema revsch23;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table rev23tab5(a int not null, b int, primary key (a));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')

    stmt = """alter table rev23tab3_1 rename to rev23tab5_1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into rev23tab5_1 values(3,3);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)

    stmt = """drop table rev23tab4;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #process supermxci

    stmt = """drop schema revsch23 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role rev_a23role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role rev_a23role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role rev_a23role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

    
def testa04(desc="""different user uses "granted by """):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    #process supermxci

    stmt = """create role rev_a24role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role rev_a24role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role rev_a24role3 with admin qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant role rev_a24role1,rev_a24role2 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant role rev_a24role3 to qauser_sqlqaa granted by qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create schema revsch24;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """set schema revsch24;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table rev24tab1(a int not null, b int, primary key (a));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant all_ddl on schema revsch24 to rev_a24role1,rev_a24role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant select,insert,delete,update on rev24tab1 to rev_a24role3 with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant select,delete,update on rev24tab1 to qauser_sqlqaa by rev_a24role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema revsch24;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table rev24tab2(a int not null, b int, primary key (a));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select * from rev24tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """insert into rev24tab1 values(1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)

    stmt = """update rev24tab1 set a=a+1 where b>1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_updated_msg(output,0)

    #process supermxci

    stmt = """set schema revsch24;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke role rev_a24role3 from qauser_sqlqaa cascade granted by qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    time.sleep(10)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema revsch24;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select * from rev24tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

    stmt = """delete from rev24tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,1)

    stmt = """update rev24tab1 set a=a+2 where b>2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_updated_msg(output,0)

    stmt = """insert into rev24tab1 values(1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    #process supermxci

    stmt = """drop schema revsch24 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke role rev_a24role1,rev_a24role2 from qauser_sqlqaa cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role rev_a24role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role rev_a24role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role rev_a24role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

    
def testa05(desc="""with grant option down the line """):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    #process supermxci

    stmt = """create role rev_a25role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role rev_a25role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role rev_a25role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant role rev_a25role1 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create schema revsch25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set schema revsch25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table rev25tab1(a int not null, b int, primary key (a));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant all_ddl,all_dml on schema revsch25 to rev_a25role1 with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant create,alter,drop on schema revsch25 to rev_a25role2 with grant option by rev_a25role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant create,drop on schema revsch25 to rev_a25role3 by rev_a25role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant role rev_a25role3 to qauser_sqlqaa,qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user3()

    stmt = """set schema revsch25;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table rev25tab2(a int not null, b int, primary key (a));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """alter table rev25tab1 add column c int;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')

    stmt = """select * from rev25tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    stmt = """insert into rev25tab1 values(1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema revsch25;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table rev25tab3(a int not null, b int, primary key (a));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """alter table rev25tab1 add column c int;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select * from rev25tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """insert into rev25tab1 values(1,1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)

    #process supermxci

    stmt = """revoke role rev_a25role3 from qauser_sqlqab cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke role rev_a25role1 from qauser_sqlqaa cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    time.sleep(10)


    mydci = basic_defs.switch_session_qi_user3()

    stmt = """set schema revsch25;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table rev25tab4(a int not null, b int, primary key (a));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')

    stmt = """alter table rev25tab1 add column c int;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')

    stmt = """select * from rev25tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    stmt = """insert into rev25tab1 values(1,1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema revsch25;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table rev25tab4(a int not null, b int, primary key (a));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """alter table rev25tab1 add column c int;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    stmt = """select * from rev25tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    stmt = """insert into rev25tab1 values(1,1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    stmt = """drop table rev25tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #process supermxci

    stmt = """drop schema revsch25 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke role rev_a25role3 from qauser_sqlqaa cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role rev_a25role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role rev_a25role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role rev_a25role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

    
def testa06(desc="""revoke from user who has privileges """):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    #process supermxci

    stmt = """create role rev_a26role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role rev_a26role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant role rev_a26role1,rev_a26role2 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create schema revsch26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set schema revsch26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table rev26tab1(a int not null, b int, primary key (a));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant all_ddl on schema revsch26 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant all_ddl on schema revsch26 to rev_a26role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant all_ddl on schema revsch26 to rev_a26role2 with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant all_ddl on schema revsch26 to qauser_sqlqaa by rev_a26role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema revsch26;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table rev26tab2(a int not null, b int, primary key (a));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """alter table rev26tab1 add column c int;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #process supermxci
    stmt = """revoke all_ddl on schema revsch26 from qauser_sqlqaa cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    time.sleep(10)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema revsch26;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table rev26tab3(a int not null, b int, primary key (a));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #process supermxci

    stmt = """revoke all_ddl on schema revsch26 from rev_a26role1 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    time.sleep(10)


    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema revsch26;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table rev26tab4(a int not null, b int, primary key (a));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #process supermxci

    stmt = """revoke all_ddl on schema revsch26 from rev_a26role2 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    time.sleep(10)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema revsch26;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table rev26tab5(a int not null, b int, primary key (a));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    stmt = """alter table rev26tab1 add column f int;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')

    #process supermxci

    stmt = """drop schema revsch26 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke role rev_a26role1,rev_a26role2 from qauser_sqlqaa cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role rev_a26role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role rev_a26role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc) 

def testa07(desc="""revoke from user/ROLE/with grant option """):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    #process supermxci

    stmt = """create role rev_a27role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role rev_a27role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant role rev_a27role1,rev_a27role2 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create schema revsch27;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set schema revsch27;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table rev27tab1(a int not null, b int, primary key (a));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant select,insert,delete,update on rev27tab1 to qauser_sqlqaa with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant select,insert,delete,update on rev27tab1 to rev_a27role1 with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant select,delete on rev27tab1 to rev_a27role2 with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant update,insert on rev27tab1 to qauser_sqlqab with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant select,delete on rev27tab1 to qauser_sqlqaa with grant option by rev_a27role1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant update,insert on rev27tab1 to qauser_sqlqaa  by qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant select,delete on rev27tab1 to qauser_sqlqaa by rev_a27role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant select,delete on rev27tab1 to qauser_sqlqaa with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant select,delete on rev27tab1 to qauser_tsang by qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant delete on rev27tab1 to qauser_tsang by qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema revsch27;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select * from rev27tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """insert into rev27tab1 values(1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)

    stmt = """update rev27tab1 set a=a+1 where b>1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_updated_msg(output,0)

    mydci = basic_defs.switch_session_qi_user4()

    stmt = """set schema revsch27;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select * from rev27tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

    stmt = """update rev27tab1 set a=a+5 where b>5;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    #process supermxci

    stmt = """set schema revsch27;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke select,insert,delete,update on rev27tab1 from qauser_sqlqaa cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    time.sleep(10)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema revsch27;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select * from rev27tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

    stmt = """update rev27tab1 set a=a+2 where b>2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_updated_msg(output,0)

    mydci = basic_defs.switch_session_qi_user4()

    stmt = """set schema revsch27;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """delete from rev27tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,1)

    stmt = """update rev27tab1 set a=a+5 where b>5;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    #process supermxci

    stmt = """set schema revsch27;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke select,insert,delete,update on rev27tab1 from rev_a27role1 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke update,insert on rev27tab1 from qauser_sqlqab cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    time.sleep(10)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema revsch27;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select * from rev27tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """update rev27tab1 set a=a+2 where b>2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    #process supermxci

    stmt = """drop schema revsch27 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke role rev_a27role1,rev_a27role2 from qauser_sqlqaa cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role rev_a27role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role rev_a27role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

    
def testa08(desc="""revoke from user granted by user/role"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    #process supermxci

    stmt = """create role rev_a28role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role rev_a28role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role rev_a28role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant role rev_a28role3 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant role rev_a28role1 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create schema revsch28;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set schema revsch28;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table rev28tab1(a int not null, b int, primary key (a));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant alter,drop on schema revsch28 to qauser_sqlqab with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant alter,drop on schema revsch28 to qauser_sqlqaa with grant option by qauser_sqlqab ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant alter,drop on schema revsch28 to rev_a28role1 by qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant all_ddl,all_dml on schema revsch28 to rev_a28role2 with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant all_ddl,all_dml on schema revsch28 to rev_a28role3 with grant option by rev_a28role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant all_ddl,all_dml on schema revsch28 to qauser_sqlqaa by rev_a28role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema revsch28;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table rev28tab2(a int not null, b int, primary key (a));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select * from rev28tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    #process supermxci

    stmt = """revoke all on schema revsch28 from qauser_sqlqaa by rev_a28role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '1015') 

    stmt = """revoke alter on schema revsch28 from qauser_sqlqaa cascade by qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    time.sleep(10)

    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema revsch28;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table rev28tab3(a int not null, b int, primary key (a));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select * from rev28tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    #process supermxci

    stmt = """revoke all on schema revsch28 from qauser_sqlqaa cascade by rev_a28role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    time.sleep(10)

    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema revsch28;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table rev28tab4(a int not null, b int, primary key (a));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select * from rev28tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt = """alter table rev28tab1 add column c int;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop table rev28tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #process supermxci

    stmt = """drop schema revsch28 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke role rev_a28role1,rev_a28role3 from qauser_sqlqaa cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role rev_a28role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role rev_a28role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role rev_a28role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

    
def testa09(desc="""grant privs to self"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    #process supermxci

    stmt = """create role rev_a29role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant role rev_a29role1 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create schema revsch29;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set schema revsch29;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table rev29tab1(a int not null, b int, primary key (a));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant all_ddl,all_dml on schema revsch29 to qauser_sqlqab with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant all_ddl,all_dml on schema revsch29 to rev_a29role1 with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant all_ddl,all_dml on schema revsch29 to rev_a29role1 with grant option by rev_a29role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant create,drop on schema revsch29 to qauser_sqlqaa by rev_a29role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant all_ddl,all_dml on schema revsch29 to qauser_sqlqaa with grant option by qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant all_ddl on schema revsch29 to qauser_sqlqab with grant option by qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant create,drop on schema revsch29 to qauser_sqlqaa with grant option by qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant select,insert,delete,update on rev29tab1 to qauser_sqlqaa with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant select,insert,delete,update on rev29tab1 to qauser_sqlqaa with grant option by qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant select on rev29tab1 to qauser_sqlqaa with grant option by qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant insert on rev29tab1 to qauser_sqlqab by qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke all_ddl,all_dml on schema revsch29 from qauser_sqlqab cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    time.sleep(10)

    mydci = basic_defs.switch_session_qi_user3()
    stmt = """set schema revsch29;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table rev29tab2(a int not null, b int, primary key (a));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')

    stmt = """insert into rev29tab1 values(1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)

    #process supermxci

    stmt = """revoke all on schema revsch29 from qauser_sqlqaa cascade by rev_a29role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    time.sleep(10)

    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema revsch29;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table rev29tab3(a int not null, b int, primary key (a));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')

    stmt = """insert into rev29tab1 values(2,2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)

    #process supermxci

    stmt = """drop schema revsch29 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke role rev_a29role1 from qauser_sqlqaa cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role rev_a29role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

    
def testa10(desc="""revoke with grant option for """):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    #process supermxci

    stmt = """create role rev_a30role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role rev_a30role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role rev_a30role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role rev_a30role4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant role rev_a30role1,rev_a30role2 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant role rev_a30role3 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant role rev_a30role4 to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create schema revsch30;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set schema revsch30;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table rev30tab1(a int not null, b int, primary key (a));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant alter,drop on schema revsch30 to rev_a30role1 with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant alter,drop on schema revsch30 to rev_a30role2 with grant option by rev_a30role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant alter,drop on schema revsch30 to rev_a30role3 with grant option by rev_a30role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant alter,drop on schema revsch30 to rev_a30role4 with grant option by rev_a30role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant select,insert,delete,update on rev30tab1 to qauser_sqlqab with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant select,insert,delete,update on rev30tab1 to qauser_sqlqaa with grant option by qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant select,insert on rev30tab1 to rev_a30role3 by qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke grant option for alter,drop on schema revsch30 from rev_a30role3 cascade by rev_a30role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    time.sleep(10)

    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema revsch30;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """alter table rev30tab1 add column c int;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user4()
    
    stmt = """set schema revsch30;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """alter table rev30tab1 add column c int;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')

    stmt = """drop table rev30tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')

    #process supermxci
    stmt = """set schema revsch30;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke select,insert,delete,update on rev30tab1 from qauser_sqlqab cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke alter,drop on schema revsch30 from rev_a30role1 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    time.sleep(10)

    mydci = basic_defs.switch_session_qi_user2()
    stmt = """set schema revsch30;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select * from rev30tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    stmt = """insert into rev30tab1 values(1,1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    mydci = basic_defs.switch_session_qi_user3()
    stmt = """set schema revsch30;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select * from rev30tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    stmt = """insert into rev30tab1 values(1,1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    #process supermxci

    stmt = """drop schema revsch30 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke role rev_a30role1,rev_a30role2 from qauser_sqlqaa cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke role rev_a30role3 from  qauser_sqlqab cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke role rev_a30role4 from qauser_tsang cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role rev_a30role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role rev_a30role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role rev_a30role3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role rev_a30role4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)