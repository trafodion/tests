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
    
# a01 create schema, vary ordering of clauses, misspell keywords
# a02 Create schema with authorizationID as valid username/rolename
# a03 the user granted db__rootrole create schema
# a04 create schema authorization to users/roles owning more than one schema
# a05 differernt user(including DB__ROOT) create schema with/without AUTHORIZATION clause
# a06 create schema authorize to  NULL PUBLIC nonexistent auth-id  "DB__ROOT"  himself
# a07 DB__ROOT create schema authorize to DB__ROOT user
# a08 create schema using some name treated as reserved name before
# a09 create schema without schemaname
# a10 revoke user's create schema priv
# a11 schema admin user see/operate objects belonging to other users
# a12 schema admin role see/operate objects belonging to other users
# a13 schema admin drop objects belonging to other users not in his schema
# a14 schema admin grant any types priv of his schema to other users(including null public )
# a15 schema admin revoke any types priv of his schema from other users(including null,public)
# a16 schema admin role drop schema with/without cascade
# a17 db_root, db_rootrole user drop schema
# a18 get schema for user/role lists all the schemas managed by a specified user or role
# a19 showddl schema: describes details about schema including the authorization ID in its display
# a20 verify behavior on shared schema
# a21 verify behavior on private schema




def testa01(desc="""create schema, vary ordering of clauses, misspell keywords"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    stmt = """create schema;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001') 
    
    stmt = """create schema private;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001') 
    
    stmt = """create schema .myschema authorization ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')     
    
    stmt = """create private schema   myschema authorization ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """create shared schema  myschema authorization ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """create schema myschema user1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')  
    
    stmt = """create myschema authorization qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001') 
    
    stmt = """create myschema authorization qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001') 
    
    stmt = """create schema authorization auth;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1008')
    
    stmt = """create schema shared authorization auth;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1008')

    _testmgr.testcase_end(desc)

def testa02(desc="""Create schema with authorizationID as valid username/rolename"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """unregister user qauser1;"""  
    output = _dci.cmdexec(stmt)    
    
    stmt = """unregister user qauser2;"""  
    output = _dci.cmdexec(stmt)  
    
    stmt = """unregister user qauser3;"""  
    output = _dci.cmdexec(stmt)  
    
    stmt = """unregister user qauser4;"""  
    output = _dci.cmdexec(stmt)  
    
    stmt = """unregister user qauser1;"""  
    output = _dci.cmdexec(stmt)    
    
    stmt = """unregister user qauser2;"""  
    output = _dci.cmdexec(stmt)  
    
    stmt = """unregister user qauser3;"""  
    output = _dci.cmdexec(stmt)  
    
    stmt = """register user qauser1;"""  
    output = _dci.cmdexec(stmt)  
    
    stmt = """register user qauser2 as qauser2test;"""  
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """register user qauser3 as qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012345128;"""  
    output = _dci.cmdexec(stmt) 
    _dci.expect_complete_msg(output)
    
    stmt = """register user qauser4 as "LMNOP-./ghij_@klmnop";"""  
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create role qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012345129;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create role "13344//23";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create schema myschema1 authorization qauser1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create schema shared myschema2 authorization qauser2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """create private schema  myschema3 authorization qauser2test;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create schema myschema4 authorization qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012345128;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create schema .sh.myschema5 authorization qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012345128;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """create schema myschema6 authorization "LMNOP-./ghij_@klmnop";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create shared schema  myschema7 authorization "13344//23";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create schema sh.myschema8 authorization "13344//23";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """create schema myschema9 authorization qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012345129;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """unregister user qauser2test;"""  
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1343')

    stmt = """drop schema myschema1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop schema myschema2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop schema myschema3;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop schema myschema4;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop schema myschema5;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop schema myschema6;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop schema myschema7;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop schema myschema8;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop schema myschema9;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """unregister user qauser2test;"""  
    output = _dci.cmdexec(stmt)
    
    stmt = """register user qauser2;"""  
    output = _dci.cmdexec(stmt)
    
    stmt = """unregister user qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012345128;"""  
    output = _dci.cmdexec(stmt) 
    
    stmt = """register user qauser3;"""  
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """unregister user "LMNOP-./ghij_@klmnop";"""  
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """register user qauser4;"""  
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop role qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012345129;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop role "13344//23";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    
    
def testa03(desc="""the user granted db__rootrole create schema"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
       
    stmt = """revoke component privilege CREATE_SCHEMA on SQL_OPERATIONS from qauser_sqlqaa;"""  
    output = _dci.cmdexec(stmt)

    stmt = """revoke component privilege CREATE_SCHEMA on SQL_OPERATIONS from qauser_tsang;"""  
    output = _dci.cmdexec(stmt)

    
    stmt = """grant role db__rootrole to qauser_sqlqaa;"""  
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """grant role db__rootrole to qauser_sqlqab;"""  
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create role schrole3;"""  
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    
    stmt = """grant component privilege CREATE_SCHEMA on SQL_OPERATIONS to qauser_tsang;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()

    
    stmt = """create shared schema myschema1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create private schema myschema2 authorization qauser1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user3()

    stmt = """create schema myschema3 authorization schrole3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create shared schema authorization qauser1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user4()
    
    stmt = """create schema myschema4 authorization qauser1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
   
    
    stmt = """revoke component privilege CREATE_SCHEMA on SQL_OPERATIONS from qauser_tsang;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """revoke role db__rootrole from qauser_sqlqaa;"""  
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """revoke role db__rootrole from qauser_sqlqab;"""  
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """create schema myschema5;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop schema myschema5;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop schema myschema1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop schema myschema2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    mydci = basic_defs.switch_session_qi_user3()

    stmt = """create private schema myschema5 authorization schrole3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop schema myschema3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    stmt = """drop schema qauser1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    mydci = basic_defs.switch_session_qi_user4()
    
    stmt = """create shared schema myschema6;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop schema myschema6;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """drop schema myschema4;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    stmt = """grant component privilege CREATE_SCHEMA on SQL_OPERATIONS to qauser_sqlqaa;"""  
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """grant component privilege CREATE_SCHEMA on SQL_OPERATIONS to qauser_tsang;"""  
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
        
    stmt = """ drop role schrole3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ drop schema myschema1;"""
    output = _dci.cmdexec(stmt)
    stmt = """ drop schema myschema2;"""
    output = _dci.cmdexec(stmt)
    stmt = """ drop schema myschema3;"""
    output = _dci.cmdexec(stmt)
    stmt = """ drop schema myschema4;"""
    output = _dci.cmdexec(stmt)
    stmt = """ drop schema myschema5;"""
    output = _dci.cmdexec(stmt)
    stmt = """ drop schema myschema6;"""
    output = _dci.cmdexec(stmt)
    stmt = """ drop schema qauser1;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)
    
    
def testa04(desc="""create schema authorization to users/roles owning more than one schema"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """create role schrole04_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create role schrole04_2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """grant role schrole04_1 to qauser1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """grant role schrole04_1 to qauser2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create shared schema myschema1 authorization qauser1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create private schema myschema2 authorization qauser1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create schema myschema3 authorization schrole04_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create shared schema myschema4 authorization schrole04_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create shared schema myschema2 authorization qauser1,qauser2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
        
    stmt = """create private schema myschema2 authorization qauser1,schrole04_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """create schema myschema2 authorization schrole04_1,schrole04_2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """revoke role schrole04_1 from qauser1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """revoke role schrole04_1 from qauser2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop schema myschema4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
      
    stmt = """drop schema myschema3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop schema myschema2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop schema myschema1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop role schrole04_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop role schrole04_2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
      
    _testmgr.testcase_end(desc)

    
def testa05(desc="""differernt user(including DB__ROOT) create schema with/without AUTHORIZATION clause"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
     
    #process supermxci
    #create schema without authorization clause

    stmt = """create private schema myschema05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #create schema with authorization clause
    stmt = """create schema myschema05_1  Authorization qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema myschema05_1 ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table sqsectab1(a int, b int)NO PARTITION;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant all  on schema myschema05_1 to qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant select on sqsectab1 to qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop schema myschema05_1 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #DB__ROOT user   
    #create schema without authorization clause
    stmt = """create shared schema myschema05_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #create schema with authorization clause
    stmt = """create schema myschema05_4  Authorization qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #verify user3

    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema myschema05_4 ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table myschema05_4.sqsectab1(a int, b int,c varchar(20))NO PARTITION;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant all on schema myschema05_4 to qauser_tsang;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant select,insert on sqsectab1 to qauser_tsang;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop schema myschema05_4 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #process supermxci
    stmt = """drop schema myschema05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop schema  myschema05_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)    

def testa06(desc="""create schema authorize to  NULL PUBLIC nonexistent auth-id  "DB__ROOT"  himself"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
 
    #process supermxci
    #authorize to NULL,PUBLIC
    stmt = """create schema myschema06_1 AUTHORIZATION NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """create shared schema myschema06_1 AUTHORIZATION PUBLIC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """create private schema myschema06_1 AUTHORIZATION NULL,PUBLIC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    #authorize to "NULL","PUBLIC"
    stmt = """create schema myschema06_2 AUTHORIZATION "NULL"; """
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'NULL does not exist' )
    
    stmt = """create schema myschema06_2 AUTHORIZATION "PUBLIC";"""
    output = _dci.cmdexec(stmt)
    #_dci.expect_error_msg(output, '1333')
    _dci.expect_complete_msg(output)

    stmt = """create shared schema myschema06_2 AUTHORIZATION "NULL","PUBLIC"; """
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    #expect any *ERROR** QAUSER_TEST does not exist*
    stmt = """create shared schema myschema06_3 AUTHORIZATION "qauser_test";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'QAUSER_TEST does not exist' )

    stmt = """create private schema myschema06_3 AUTHORIZATION test;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    _dci.expect_error_msg(output, '3128')

    #ordinary user authorize to "DB__ROOT"
    stmt = """create schema myschema06_4 AUTHORIZATION "DB__ROOT";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #ordinary user authorize to himself
    stmt = """create private schema myschema06_5 AUTHORIZATION "DB__ROOT";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #miss spelling keyword
    stmt = """create schema sh.myschema06_6 AUTHOURIZATION "PUBLIC"; """
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    #verify himself
    #process supermxci
    stmt = """set schema myschema06_5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table sqsectab1(a int not null primary key, b int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant all on schema myschema06_5 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant select on table sqsectab1 to qauser_sqlqaa ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #verify DB__ROOT
    #process supermxci
    stmt = """set schema myschema06_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table sqsectab2(a int not null primary key, b int , c varchar(10));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant all on schema myschema06_5 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant select on table myschema06_5.sqsectab1 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #drop schema 
    stmt = """drop schema  myschema06_1 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop schema  myschema06_2 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop schema  myschema06_3 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop schema  myschema06_4 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop schema  myschema06_5 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop schema  myschema06_6 cascade;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)


def testa07(desc="""DB__ROOT create schema authorize to DB__ROOT user/DB__ROOTROLE"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
 
    #process supermxci
    #DB__ROOT user
    
    stmt = """grant role db__rootrole to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create schema myschema07_1 AUTHORIZATION qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #DB_ROOT create schema without AUTHORIZATION clause

    stmt = """create private schema myschema07_2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #AUTHORIZATION TO DB__ROOT
    stmt = """create schema myschema07_3 AUTHORIZATION DB__ROOT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create private schema myschema07_4 AUTHORIZATION DB__ROOTROLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """set schema myschema07_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table myschema07_1.sqsectab(a int ,b int)NO PARTITION;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #verify
    stmt = """set schema myschema07_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table sqsectab1(col1 int not null primary key, col2 int ,col3 varchar(5));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create view sqsecview1 as select sqsectab1.col2,myschema07_1.sqsectab.b from sqsectab1,myschema07_1.sqsectab where sqsectab1.col1=myschema07_1.sqsectab.a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant select,insert on sqsectab1 to qauser_sqlqaa ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant select  on sqsecview1 to qauser_sqlqaa ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


    mydci = basic_defs.switch_session_qi_user2()

    stmt = """grant select on myschema07_1.sqsectab to qauser_sqlqaa ;"""
    output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    mydci.expect_error_msg(output, '1223')
    
    #process secpbmxci
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """create table myschema07_4.sqsectab1(a int ,b int)NO PARTITION;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop schema myschema07_4 cascade;"""
    output = _dci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    #process secpamxci
    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema myschema07_3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into sqsectab1  values(1,2,'sedr'),(11,2,'sdf');"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,2)
    
    stmt = """select * from sqsectab1 ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)

    stmt = """select col1 from sqsectab1 where col2=2;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,2)

    stmt = """select * from sqsecview1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,0)

    stmt = """select myschema07_1.sqsectab.a from myschema07_1.sqsectab where myschema07_1.sqsectab.b=0;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,0)

    #process supermxci
    
    stmt = """revoke role db__rootrole from qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop schema myschema07_1 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop schema myschema07_2 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop schema myschema07_3 cascade;"""
    output = _dci.cmdexec(stmt)
    
    
    _testmgr.testcase_end(desc)
    

    
def testa08(desc="""create schema using some name treated as reserved name before"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    #process supermxci
    #These names are not reserved (you can create schema with these names): SYSTEM_SCHEMA,
    #SYSTEM_DEFAULTS_SCHEMA, MXCS_SCHEMA.
    stmt = """create private schema SYSTEM_SCHEMA Authorization qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create schema SYSTEM_DEFAULTS_SCHEMA Authorization qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create schema MXCS_SCHEMA Authorization qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #process secpamxci
    mydci = basic_defs.switch_session_qi_user2()

    stmt = """create table SYSTEM_SCHEMA.sqsectab1(a int ,b int)No partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view SYSTEM_DEFAULTS_SCHEMA.sqsecview1 as select * from SYSTEM_SCHEMA.sqsectab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #stmt = """create mv MXCS_SCHEMA.sqsecmv1 refresh on request initialize on refresh as select * from SYSTEM_SCHEMA.sqsectab1;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    stmt = """drop view SYSTEM_DEFAULTS_SCHEMA.sqsecview1;"""
    output = mydci.cmdexec(stmt)


    stmt = """drop table SYSTEM_SCHEMA.sqsectab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop schema SYSTEM_SCHEMA cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop schema SYSTEM_DEFAULTS_SCHEMA cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop schema MXCS_SCHEMA cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop schema PUBLIC_ACCESS_SCHEMA cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1003')

    _testmgr.testcase_end(desc)
    
def testa09(desc="""create schema without schemaname"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #process supermxci
    #stmt = """set catalog schcat;"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_error_msg(output, '15001')

    stmt = """create schema ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """create role schrole09_1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ grant component privilege create_view on SQL_OPERATIONS to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ grant component privilege create_view on SQL_OPERATIONS to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """grant role schrole09_1 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create schema authorization qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create private schema authorization schrole09_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create schema authorization qauser_sqlqaa,qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """create table qauser_sqlqaa.sqsectab1(a int,b int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table schrole09_1.sqsectab3(a int,b int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #process secpamxci
    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema  qauser_sqlqaa;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table sqsectab2(col1 int,col2 int, col3 varchar(5))no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #stmt = """grant create on schema qauser_sqlqaa to qauser_sqlqab ;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    stmt = """grant select on table sqsectab2 to qauser_sqlqab ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant select on table sqsectab1 to qauser_sqlqab ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #process secpbmxci
    mydci = basic_defs.switch_session_qi_user3()

    stmt = """set schema  qauser_sqlqaa;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view sqsecv1 as select sqsectab1.a, sqsectab2.col1 from sqsectab1,sqsectab2 where sqsectab1.b= sqsectab2.col2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """set schema  schrole09_1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    #stmt = """grant create on schema schrole09_1 to qauser_tsang ;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    
    stmt = """grant select on table sqsectab3 to qauser_tsang ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user4()
    
    #stmt = """set schema  schrole09_1;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    
    stmt = """create view schrole09_1.sqsecv2 as select a from schrole09_1.sqsectab3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #process secpamxci
    mydci = basic_defs.switch_session_qi_user2()

    #stmt = """revoke create on schema qauser_sqlqaa from qauser_sqlqab cascade;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    stmt = """drop view qauser_sqlqaa.sqsecv1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop view schrole09_1.sqsecv2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')


    stmt = """revoke select on  qauser_sqlqaa.sqsectab2 from qauser_sqlqab cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """revoke select on qauser_sqlqaa.sqsectab1 from qauser_sqlqab cascade;"""
    time.sleep(10)
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop schema qauser_sqlqaa cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)


    stmt = """drop table  schrole09_1.sqsectab3 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop schema schrole09_1 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """revoke role schrole09_1 from qauser_tsang;"""
    output = _dci.cmdexec(stmt)

    stmt = """revoke role schrole09_1 from qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop role schrole09_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ revoke component privilege create_view on SQL_OPERATIONS from qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ revoke component privilege create_view on SQL_OPERATIONS from qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)
    
    
    
def testa10(desc="""revoke user's create schema priv"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #process supermxci
    stmt = """create role schrole10_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create schema myschema10_1 Authorization qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create private schema myschema10_2 Authorization schrole10_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """grant role schrole10_1 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #process secpbmxci
    mydci = basic_defs.switch_session_qi_user3()

    stmt = """create schema myschema10_3 ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #revoke user's create schema priv
    #process supermxci
    stmt = """revoke create_schema ,drop_schema on schcat from qauser_sqlqaa ,qauser_sqlqab ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """revoke create_schema ,drop_schema on schcat from schrole10_1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    time.sleep(10)

    stmt = """drop schema myschema10_1 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop schema myschema10_2 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop schema myschema10_3 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """revoke role schrole10_1 from qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop role schrole10_1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)


def testa11(desc="""schema admin user see/operate objects belonging to other users"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #process supermxci
    stmt = """create schema myschema11_1 AUTHORIZATION qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table myschema11_1.sqsectab1(col1 int ,col2 int,col3 varchar(5))no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant select on myschema11_1.sqsectab1 to qauser_tsang ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into myschema11_1.sqsectab1 values(1,2,'der'),(2,22,'ser');"""
    output = _dci.cmdexec(stmt)    
    _dci.expect_inserted_msg(output,2)

    stmt = """grant select on myschema11_1.sqsectab1 to qauser_sqlqab ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant component privilege "CREATE" on SQL_OPERATIONS to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """grant select on myschema11_1.sqsectab1 to qauser_tsang ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant select on myschema11_1.sqsectab1 to qauser_sqlqab ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
 
    #user3 create some objects
    mydci = basic_defs.switch_session_qi_user3()

    stmt = """create table myschema11_1.sqsectab2(col1 int,col2 int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into myschema11_1.sqsectab2 values(1,2),(11,22);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,2)

    stmt = """create view myschema11_1.sqsecview1 as select * from myschema11_1.sqsectab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #stmt = """create index index1 on myschema11_1.sqsectab2(col1,col2);"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    stmt = """grant select,insert on myschema11_1.sqsectab2 to qauser_tsang ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #user2 is owner of myschema11_1
    #process secpamxci
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """insert into  myschema11_1.sqsectab1 values(3,2,'der'),(4,22,'ser');"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,2)

    stmt = """select * from myschema11_1.sqsectab1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,4) 

    stmt = """update myschema11_1.sqsectab1 set col1=col1+1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_updated_msg(output,4) 

    stmt = """delete from myschema11_1.sqsectab1 ;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_deleted_msg(output,4) 

    stmt = """grant select(col3) on table myschema11_1.sqsectab1 to qauser_tsang ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into myschema11_1.sqsectab2 values(3,2),(4,22);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,2)

    stmt = """select * from myschema11_1.sqsectab2;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,4) 

    stmt = """select * from myschema11_1.sqsecview1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,0) 

    stmt = """update myschema11_1.sqsectab2 set col1=col1+1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_updated_msg(output,4)

    stmt = """delete from myschema11_1.sqsectab2;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_deleted_msg(output,4) 

    #stmt = """drop index myschema11_1.index1;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    stmt = """revoke select on myschema11_1.sqsectab2 from qauser_tsang cascade;"""
    output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '1017')
    mydci.expect_complete_msg(output)
    
    time.sleep(10)

    #verify user4
    #process secpcmxci
    mydci = basic_defs.switch_session_qi_user4()

    stmt = """select * from myschema11_1.sqsectab1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,0) 

    stmt = """insert into myschema11_1.sqsectab2 values(1,2);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)

    stmt = """select * from myschema11_1.sqsectab2;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,1)
    
    #process secpamxci
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """drop view myschema11_1.sqsecview1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #stmt = """drop index index1;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    
    stmt = """drop table myschema11_1.sqsectab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop table myschema11_1.sqsectab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #process supermxci
    stmt = """drop schema myschema11_1 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """REVOKE component privilege "CREATE" on SQL_OPERATIONS FROM qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def testa12(desc="""schema admin role see/operate objects belonging to other users"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #process supermxci
    stmt = """create role schrole12_1 with admin qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create private schema myschema12_1 AUTHORIZATION schrole12_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table myschema12_1.sqsectab1(col1 int ,col2 int,col3 varchar(5))no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant component privilege "CREATE" on SQL_OPERATIONS to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """grant select on myschema12_1.sqsectab1 to qauser_tsang ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into myschema12_1.sqsectab1 values(1,2,'der'),(2,22,'ser');"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,2)

    stmt = """grant select on myschema12_1.sqsectab1 to qauser_sqlqab ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
 
    #user3 create some objects
    mydci = basic_defs.switch_session_qi_user3()

    stmt = """create table myschema12_1.sqsectab2(col1 int,col2 int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into myschema12_1.sqsectab2 values(1,2),(11,22);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,2)

    stmt = """create view myschema12_1.sqsecview1 as select * from myschema12_1.sqsectab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #stmt = """create index index1 on myschema12_1.sqsectab2(col1,col2);"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    stmt = """grant select,insert on myschema12_1.sqsectab2 to qauser_tsang ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #user2 is owner of myschema12_1
    #process secpamxci
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """insert into  myschema12_1.sqsectab1 values(3,2,'der'),(4,22,'ser');"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,2)

    stmt = """select * from myschema12_1.sqsectab1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,4) 

    stmt = """update myschema12_1.sqsectab1 set col1=col1+1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_updated_msg(output,4) 

    stmt = """delete from myschema12_1.sqsectab1 ;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_deleted_msg(output,4) 

    stmt = """grant select(col3) on table myschema12_1.sqsectab1 to qauser_tsang ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into myschema12_1.sqsectab2 values(3,2),(4,22);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,2)

    stmt = """select * from myschema12_1.sqsectab2;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,4) 

    stmt = """select * from myschema12_1.sqsecview1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,0) 

    stmt = """update myschema12_1.sqsectab2 set col1=col1+1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_updated_msg(output,4)

    stmt = """delete from myschema12_1.sqsectab2;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_deleted_msg(output,4) 

    #stmt = """drop index myschema12_1.index1;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    stmt = """revoke select on myschema12_1.sqsectab2 from qauser_tsang cascade;"""
    output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '1017')
    mydci.expect_complete_msg(output)

    
    time.sleep(10)

    #verify user4
    #process secpcmxci
    mydci = basic_defs.switch_session_qi_user4()

    stmt = """select * from myschema12_1.sqsectab1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,0) 

    stmt = """insert into myschema12_1.sqsectab2 values(1,2);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)

    stmt = """select * from myschema12_1.sqsectab2;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,1)
    
    #process secpamxci
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """drop view myschema12_1.sqsecview1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #stmt = """drop index index1;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    
    stmt = """drop table myschema12_1.sqsectab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop table myschema12_1.sqsectab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    #process supermxci
    stmt = """drop schema myschema12_1 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop role schrole12_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


    stmt = """REVOKE component privilege "CREATE" on SQL_OPERATIONS FROM qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    _testmgr.testcase_end(desc)
    


    
def testa13(desc="""schema admin drop objects belonging to other users not in his schema"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #process supermxci
    stmt = """create role schrole13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """grant role schrole13 to qauser_teg;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create schema myschema13_1 AUTHORIZATION qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create schema myschema13_2 AUTHORIZATION schrole13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ grant component privilege create_view on SQL_OPERATIONS to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


    #process secpamxci
    #mydci = basic_defs.switch_session_qi_user2()
    
    #stmt = """grant all on schema myschema13_1 to qauser_sqlqab ;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    
    #mydci = basic_defs.switch_session_qi_user5()
    
    #stmt = """grant all on schema myschema13_2 to qauser_sqlqab ;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output) 

    #user3 create schema and some object
    #process secpbmxci
    mydci = basic_defs.switch_session_qi_user3()    

    stmt = """create schema myschema13_3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table myschema13_3.sqsectab2(a int,b int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #stmt = """grant create on schema myschema13_1 to qauser_tsang ;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    
    #stmt = """grant create on schema myschema13_2 to qauser_tsang ;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """grant select on schema myschema13_3 to qauser_tsang ;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    stmt = """grant select on myschema13_3.sqsectab2 to qauser_tsang ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #process secpcmxci
    mydci = basic_defs.switch_session_qi_user4()

    stmt = """create table myschema13_1.sqsectab3(a int,b int,c decimal(2))no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')

    stmt = """create view myschema13_1.sqsecview as select * from myschema13_3.sqsectab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table myschema13_2.sqsectab4(a int,b int,c decimal(2))no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    #process secpamxci
    mydci = basic_defs.switch_session_qi_user2()

    stmt = """drop table myschema13_3.sqsectab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')

    stmt = """drop table myschema13_3.sqsectab2 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')

    stmt = """drop schema myschema13_1 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user5()
    
    stmt = """drop table myschema13_3.sqsectab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')

    stmt = """drop table myschema13_3.sqsectab2 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')

    stmt = """drop table myschema13_2.sqsectab4 cascade;"""
    output = mydci.cmdexec(stmt)
    

    #process supermxci

    stmt = """drop schema myschema13_2 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop schema myschema13_3 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """revoke role schrole13 from qauser_teg;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop role schrole13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ revoke component privilege create_view on SQL_OPERATIONS from qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    
    _testmgr.testcase_end(desc)
    

def testa14(desc="""schema admin grant any types priv of his schema to other users(including null public )"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #process supermxci


    stmt = """grant component privilege "CREATE" on SQL_OPERATIONS to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role schrole14;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ grant role schrole14 to qauser_teg;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create schema myschema14_1 AUTHORIZATION qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create schema myschema14_2 AUTHORIZATION schrole14;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table myschema14_1.sqsectab1(col1 int not null primary key, col2 int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create view myschema14_1.sqsecview1 as select * from myschema14_1.sqsectab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #stmt = """create mv myschema14_1.seqsecmview refresh on request initialize on refresh as select col1,col2 from myschema14_1.sqsectab1;"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_complete_msg(output)

    #stmt = """create trigger myschema14_1.seqsectrig1 before update on myschema14_1.sqsectab1 REFERENCING NEW AS newR FOR EACH ROW SET newR.col2= newR.col2+ 1;"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_complete_msg(output)
    
    stmt = """create table myschema14_2.sqsectab2(col1 int not null primary key, col2 int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create view myschema14_2.sqsecview2 as select * from myschema14_2.sqsectab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #process secpamxci
    mydci = basic_defs.switch_session_qi_user2()
    #grant priv to other users

    #stmt = """grant create on schema myschema14_1 to qauser_sqlqab ;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    stmt = """grant select,update on myschema14_1.sqsectab1 to qauser_tsang ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant select,insert on myschema14_1.sqsecview1 to qauser_tsang ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user5()
    
    #stmt = """grant create on schema myschema14_2 to qauser_sqlqab ;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    stmt = """grant select,update on myschema14_2.sqsectab2 to qauser_tsang ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant select,insert on myschema14_2.sqsecview2 to qauser_tsang ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #process secpbmxci
    mydci = basic_defs.switch_session_qi_user3()

    stmt = """create schema myschema14_3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema myschema14_3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table sqsectab3(a int,b int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table myschema14_1.sqsectab2(a int,b int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant create on schema myschema14_1 to qauser_cmp;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #process secpcmxci
    mydci = basic_defs.switch_session_qi_user4()

    stmt = """insert into myschema14_1.sqsecview1 values(1,2);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)

    stmt = """select col1 from myschema14_1.sqsectab1 where myschema14_1.sqsectab1.col2>0;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,1)

    stmt = """select * from myschema14_1.sqsecview1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,1)

    stmt = """update myschema14_1.sqsectab1 set col2=col2+1 where col2>1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_updated_msg(output,1)
    
    stmt = """insert into myschema14_2.sqsecview2 values(1,2);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)
    
    stmt = """select * from myschema14_2.sqsecview2;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,1)
    
    #process secpamxci
    mydci = basic_defs.switch_session_qi_user2()
    
    #expect any *ERROR[1017]*
    stmt = """grant select on myschema14_1.sqsectab2 to qauser_teg ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    #grant priv on others'schema
    #expect any *ERROR[1017]*
    stmt = """grant select on myschema14_3.sqsectab3 to qauser_teg ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1012')

    #grant priv to other users
    stmt = """grant create on schema  myschema14_1 to \"NULL\" ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4222')

    stmt = """grant create on schema  myschema14_1 to NULL ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """grant create on schema  myschema14_1 to PUBLIC ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant create on schema  myschema14_1 to \"PUBLIC\" ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop schema  myschema14_1 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    stmt = """drop schema  myschema14_3 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user5()

    stmt = """drop table myschema14_1.sqsectab2;"""
    output = mydci.cmdexec(stmt)

    stmt = """drop table myschema14_2.sqsectab2 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop schema  myschema14_2 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ revoke role schrole14 from qauser_teg;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop role schrole14;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


    stmt = """REVOKE component privilege "CREATE" on SQL_OPERATIONS FROM qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def testa15(desc="""schema admin revoke any types priv of his schema from other users(including null,public)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #process supermxci
    stmt = """create role schrole15 with admin qauser_teg;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create schema myschema15_1 AUTHORIZATION qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create private schema myschema15_2 AUTHORIZATION schrole15;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant component privilege CREATE_TABLE on SQL_OPERATIONS to qauser_sqlqab;"""  
    output = _dci.cmdexec(stmt)

    stmt = """grant component privilege CREATE_VIEW on SQL_OPERATIONS to qauser_sqlqab;"""  
    output = _dci.cmdexec(stmt)

    #process secpamxci
    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema myschema15_1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table sqsectab1(col1 int not null primary key,col2 int) ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #grant priv to other users
    #stmt = """grant create,select on schema myschema15_1 to qauser_sqlqab ;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    stmt = """grant select on myschema15_1.sqsectab1 to qauser_sqlqab ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """grant select on myschema15_1.sqsectab1 to qauser_tsang ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user5()

    stmt = """set schema myschema15_2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table sqsectab2(col1 int not null primary key,col2 int) ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #grant priv to other users
    #stmt = """grant create,select on schema myschema15_2 to qauser_sqlqab ;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    stmt = """grant select on myschema15_2.sqsectab2 to qauser_sqlqab ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant select on myschema15_2.sqsectab2 to qauser_tsang ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #process secpbmxci
    mydci = basic_defs.switch_session_qi_user3()

    stmt = """create schema myschema15_3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table myschema15_3.sqsectab3(aa int,bb int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant select on table myschema15_3.sqsectab3 to qauser_tsang ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table myschema15_1.sqsectab2(a int,b int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view myschema15_1.sqsecview1 as select myschema15_1.sqsectab1.col2, myschema15_1.sqsectab2.b from myschema15_1.sqsectab1, myschema15_1.sqsectab2 where myschema15_1.sqsectab1.col1=myschema15_1.sqsectab2.a;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table myschema15_2.sqsectab3(a int,b int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create view myschema15_2.sqsecview2 as select myschema15_2.sqsectab2.col2, myschema15_2.sqsectab3.b from myschema15_2.sqsectab2, myschema15_2.sqsectab3 where myschema15_2.sqsectab2.col1=myschema15_2.sqsectab3.a;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #revoke
    #process secpamxci
    mydci = basic_defs.switch_session_qi_user2()
    
    #stmt = """revoke create ,select on schema myschema15_1 from qauser_sqlqab cascade;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    stmt = """revoke select  on  myschema15_1.sqsectab1 from qauser_tsang cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """revoke select  on  myschema15_1.sqsectab1 from qauser_sqlqab cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #stmt = """revoke select on schema myschema15_3 from  qauser_tsang cascade;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '1017')

    #time.sleep(10)

    #reovke from null public
    #expect any *ERROR** NULL does not exist*
    #stmt = """revoke create on schema  myschema15_1 from \"NULL\" cascade;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_any_substr(output,'NULL does not exist' )

    #stmt = """revoke  create on schema  myschema15_1 from NULL cascade;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '15001')

    #stmt = """revoke  create on schema  myschema15_1 from  PUBLIC cascade;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_warning_msg(output, '1015')

    #stmt = """revoke  create on schema  myschema15_1 from \"PUBLIC\" cascade;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_warning_msg(output, '1015')
    
    time.sleep(10)

    mydci = basic_defs.switch_session_qi_user5()
    
    #stmt = """revoke create ,select on schema myschema15_2 from qauser_sqlqab cascade;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    stmt = """revoke select on  myschema15_2.sqsectab2 from qauser_tsang cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """revoke select on  myschema15_2.sqsectab2 from qauser_sqlqab cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #stmt = """revoke select on schema myschema15_3 from  qauser_tsang cascade;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '1017')
        
    #process secpbmxci
    mydci = basic_defs.switch_session_qi_user3()

    stmt = """select col1 from myschema15_1.sqsectab1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_error_msg(output, '4481')

    stmt = """select * from myschema15_1.sqsectab2;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,0)

    stmt = """select * from myschema15_1.sqsecview1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    stmt = """select * from myschema15_2.sqsectab3;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,0)

    stmt = """select * from myschema15_2.sqsecview2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt = """drop schema myschema15_3 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    #process supermxci
    stmt = """drop schema  myschema15_1 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop schema  myschema15_2 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop role schrole15;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke component privilege CREATE_TABLE on SQL_OPERATIONS from qauser_sqlqab;"""  
    output = _dci.cmdexec(stmt)

    stmt = """revoke component privilege CREATE_VIEW on SQL_OPERATIONS from qauser_sqlqab;"""  
    output = _dci.cmdexec(stmt)


    _testmgr.testcase_end(desc)
    
def testa16(desc="""schema admin role drop schema with/without cascade"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #process supermxci
    stmt = """create private schema myschema16_1 AUTHORIZATION qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create role schrole16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt= """ grant role schrole16 to qauser_teg;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create schema myschema16_2 AUTHORIZATION schrole16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """GRANT component privilege CREATE_TABLE on SQL_OPERATIONS to qauser_sqlqab;"""  
    output = _dci.cmdexec(stmt)
    

    #process secpbmxci
    mydci = basic_defs.switch_session_qi_user3()

    stmt = """create table myschema16_1.sqsectab1(a int,b int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table myschema16_2.sqsectab2(a int,b int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #verify with/without cascade 
    #process secpamxci
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """drop schema myschema16_1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1028')

    stmt = """drop schema myschema16_1 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user5()
    
    stmt = """drop schema myschema16_2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1028')

    stmt = """drop schema myschema16_2 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)


    stmt = """drop schema myschema16_2 cascade;"""
    output = _dci.cmdexec(stmt)

    #process supermxci

    stmt = """create schema myschema16_3 AUTHORIZATION qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create schema myschema16_4 AUTHORIZATION schrole16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #process secpbmxci

    mydci = basic_defs.switch_session_qi_user3()

    stmt = """create table myschema16_3.sqsectab1(a int,b int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table myschema16_4.sqsectab2(a int,b int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop table myschema16_3.sqsectab1 ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    stmt = """drop table myschema16_4.sqsectab2 ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')

    stmt = """drop table myschema16_3.sqsectab1 ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table myschema16_4.sqsectab2 ;"""
    output = _dci.cmdexec(stmt)
    
    #verify with/without cascade 
    #process secpamxci
    mydci = basic_defs.switch_session_qi_user2()

    stmt = """drop schema myschema16_3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user5()
    
    stmt = """drop schema myschema16_4;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop schema myschema16_3;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop schema myschema16_4;"""
    output = _dci.cmdexec(stmt)

    #process supermxci

    stmt = """create schema myschema16_5 AUTHORIZATION qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create schema myschema16_6 AUTHORIZATION schrole16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   

    #verify with/without cascade 
    #process secpamxci
    mydci = basic_defs.switch_session_qi_user2()

    stmt = """drop schema myschema16_5;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user5()
    
    stmt = """drop schema myschema16_6;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop schema myschema16_6;"""
    output = _dci.cmdexec(stmt)

    #process supermxci

    stmt = """create schema myschema16_7 AUTHORIZATION qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create schema myschema16_8 AUTHORIZATION schrole16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table myschema16_7.sqsectab1(a int,b int)no partition ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table myschema16_8.sqsectab1(a int,b int)no partition ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #verify with/without cascade 
    #process secpamxci
    mydci = basic_defs.switch_session_qi_user2()

    stmt = """drop table myschema16_7.sqsectab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop schema myschema16_7;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user5()

    stmt = """drop table myschema16_8.sqsectab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop schema myschema16_8;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop table myschema16_8.sqsectab1;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop schema myschema16_8;"""
    output = _dci.cmdexec(stmt)

    #process supermxci

    stmt = """create schema myschema16_9 AUTHORIZATION qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create schema myschema16_10 AUTHORIZATION schrole16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table myschema16_9.sqsectab1(a int,b int)no partition ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table myschema16_10.sqsectab1(a int,b int)no partition ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #process secpamxci
    mydci = basic_defs.switch_session_qi_user2()

    stmt = """create schema myschema16_11 AUTHORIZATION qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create schema myschema16_12 AUTHORIZATION qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    #expect any *ERROR[1017]*
    stmt = """create table myschema16_12.sqsectab2(a int,b int)no partition ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')

    #stmt = """grant create on schema myschema16_9 to qauser_sqlqab ;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user5()

    stmt = """create schema myschema16_13 AUTHORIZATION qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create schema myschema16_14 AUTHORIZATION qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    #expect any *ERROR[1017]*
    stmt = """create table myschema16_14.sqsectab2(a int,b int)no partition ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')

    #stmt = """grant create on schema myschema16_10 to qauser_sqlqab ;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    
    #verify with/without cascade 
    #process secpamxci
    mydci = basic_defs.switch_session_qi_user2()

    stmt = """drop schema myschema16_9;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1028')
    
    mydci = basic_defs.switch_session_qi_user5()

    stmt = """drop schema myschema16_10;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1028')
    

    #process secpbmxci
    mydci = basic_defs.switch_session_qi_user3()
    #drop myschema16_11

    stmt = """drop schema myschema16_11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop schema myschema16_13;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop schema myschema16_12;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    #process secpamxci
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """drop table myschema16_9.sqsectab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop schema myschema16_9;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user5()
    
    stmt = """drop table myschema16_10.sqsectab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop schema myschema16_10;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop schema myschema16_14;"""
    output = _dci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop table myschema16_10.sqsectab1;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop schema myschema16_10;"""
    output = _dci.cmdexec(stmt)


    stmt= """ revoke role schrole16 from qauser_teg;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop role schrole16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke component privilege CREATE_TABLE on SQL_OPERATIONS from qauser_sqlqab;"""  
    output = _dci.cmdexec(stmt)
    

    _testmgr.testcase_end(desc)
    
def testa17(desc="""db_root, db_rootrole user drop schema"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """ create role schrole17;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """grant role schrole17 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ grant role db__rootrole to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ revoke component privilege drop_schema on SQL_OPERATIONS from qauser_teg;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """ create schema myschema17_1 AUTHORIZATION db__rootrole;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ create schema myschema17_2 AUTHORIZATION qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ create schema myschema17_3 AUTHORIZATION schrole17;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ create schema myschema17_4 AUTHORIZATION qauser_teg;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ create schema myschema17_5 AUTHORIZATION qauser_teg;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """grant component privilege CREATE_TABLE on SQL_OPERATIONS to qauser_tsang;"""  
    output = _dci.cmdexec(stmt)
    
    mydci = basic_defs.switch_session_qi_user4()
    
    stmt = """create table myschema17_1.sqsectab1(a int,b int)no partition ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table myschema17_2.sqsectab1(a int,b int)no partition ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table myschema17_3.sqsectab1(a int,b int)no partition ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table myschema17_4.sqsectab1(a int,b int)no partition ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table myschema17_5.sqsectab1(a int,b int)no partition ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop schema myschema17_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1028')
    
    stmt = """ drop schema myschema17_2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1028')
    
    stmt = """ drop schema myschema17_3 restrict;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1028')
    
    stmt = """ drop schema myschema17_4 restrict;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1028')
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ drop schema myschema17_1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1028')
    
    stmt = """ drop schema myschema17_2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1028')
    
    stmt = """ drop schema myschema17_1 restrict;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1028')
    
    stmt = """ drop schema myschema17_2 restrict;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1028')
    
    mydci = basic_defs.switch_session_qi_user5()
    
    stmt = """ drop schema myschema17_4;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1028')
    
    stmt = """ drop schema myschema17_5 restrict;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1028')
    
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """ drop schema myschema17_3 restrict;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1028')
    

    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ drop schema myschema17_1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1028')

    stmt = """ drop schema myschema17_2 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop schema myschema17_1 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)


    stmt = """ drop schema myschema17_3 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ drop schema myschema17_4 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ drop schema myschema17_5 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """revoke role schrole17 from qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ drop role schrole17;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke component privilege CREATE_TABLE on SQL_OPERATIONS from qauser_tsang;"""  
    output = _dci.cmdexec(stmt)

    stmt = """ revoke role db__rootrole from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

    
def testa18(desc="""showddl schema: describes details about schema including the authorization ID in its display"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """ create role schrole19;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
        
    stmt = """grant role SCHROLE19 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ create private schema myschema19_1 AUTHORIZATION schrole19;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ create shared schema myschema19_3 AUTHORIZATION qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ create schema myschema19_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ create schema myschema19_5 AUTHORIZATION qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ create schema myschema19_6;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ showddl schema myschema19_4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'CREATE PRIVATE SCHEMA "TRAFODION"."MYSCHEMA19_4" AUTHORIZATION "DB__ROOT"' )
    
    stmt = """ showddl schema myschema19_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'CREATE PRIVATE SCHEMA "TRAFODION"."MYSCHEMA19_1" AUTHORIZATION "SCHROLE19";' )
    
    stmt = """ showddl schema myschema19_3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'CREATE SHARED SCHEMA "TRAFODION"."MYSCHEMA19_3" AUTHORIZATION "QAUSER_SQLQAA";' )
    
    stmt = """ showddl schema myschema19_5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'CREATE PRIVATE SCHEMA "TRAFODION"."MYSCHEMA19_5" AUTHORIZATION "QAUSER_SQLQAB";' )
    
    stmt = """ showddl schema myschema19_6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'CREATE PRIVATE SCHEMA "TRAFODION"."MYSCHEMA19_6" AUTHORIZATION "QAUSER_SQLQAA";' )

    stmt = """revoke role schrole19 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ drop schema myschema19_1 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
        
    stmt = """ drop schema myschema19_2 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """ drop role schrole19;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ drop schema myschema19_3 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """ drop schema myschema19_4 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """ drop schema myschema19_5 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """ drop schema myschema19_6 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc) 
    
def testa19(desc="""verify behavior on shared schema"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """ create role schrole20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
        
    stmt = """grant role SCHROLE20 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ create shared schema myschema20_1 AUTHORIZATION schrole20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ create shared schema myschema20_2 AUTHORIZATION qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ create table myschema20_1.sqsectab1(a int,b int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ create table myschema20_2.sqsectab2(a int,b int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ insert into myschema20_1.sqsectab1 values(1,3);"""
    output = _dci.cmdexec(stmt)    
    _dci.expect_inserted_msg(output,1)
    
    stmt = """ insert into myschema20_2.sqsectab2 values(1,3);"""
    output = _dci.cmdexec(stmt)    
    _dci.expect_inserted_msg(output,1)

    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ insert into myschema20_1.sqsectab1 values(2,3);"""
    output = _dci.cmdexec(stmt)    
    _dci.expect_inserted_msg(output,1)
    
    stmt = """ select * from myschema20_1.sqsectab1;"""
    output = _dci.cmdexec(stmt)    
    _dci.expect_selected_msg(output,2)
    
    stmt = """ create table myschema20_1.sqsectab3(a int,b int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ create table myschema20_2.sqsectab4(a int,b int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """ create table myschema20_1.sqsectab5(a int,b int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ create table myschema20_2.sqsectab6(a int,b int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from  myschema20_1.sqsectab5;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,0) 
    
    stmt = """ insert into table myschema20_1.sqsectab5 values(3,4);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1) 
    
    stmt = """ update myschema20_1.sqsectab5 set a=a+1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_updated_msg(output,1)
    
    stmt = """ select * from myschema20_2.sqsectab6;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,0) 
    
    stmt = """ insert into myschema20_2.sqsectab6 values(3,4);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1) 
    
    stmt = """ update myschema20_2.sqsectab6 set a=a+1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_updated_msg(output,1)
    
    stmt = """ select * from  myschema20_1.sqsectab1;"""
    output = mydci.cmdexec(stmt) 
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ delete from  myschema20_2.sqsectab2;"""
    output = mydci.cmdexec(stmt) 
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ delete from  myschema20_1.sqsectab3;"""
    output = mydci.cmdexec(stmt) 
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ select * from myschema20_2.sqsectab4;"""
    output = mydci.cmdexec(stmt) 
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ insert into  myschema20_1.sqsectab1 values(3,4);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ revoke select, delete on table myschema20_1.sqsectab1 from qauser_sqlqaa;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    stmt = """ revoke select, delete on table myschema20_2.sqsectab2 from qauser_sqlqaa;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    stmt = """ grant select, delete on table myschema20_1.sqsectab5 to qauser_teg;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant insert on table myschema20_2.sqsectab6 to qauser_teg;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user5()
    
    stmt = """ select * from myschema20_1.sqsectab5;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,1) 
    
    stmt = """ insert into myschema20_1.sqsectab5 values(1,1);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ delete from myschema20_1.sqsectab5;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_deleted_msg(output,1)
    
    stmt = """ select * from myschema20_2.sqsectab6;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ insert into myschema20_2.sqsectab6 values(1,1);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)
    
    stmt = """ update myschema20_2.sqsectab6 set a=a+2;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_error_msg(output, '4481')
   
    
    mydci = basic_defs.switch_session_qi_user4()
    
    stmt = """ create table myschema20_1.sqsectab7(a int,b int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ create table myschema20_2.sqsectab8(a int,b int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """ revoke select, delete on table myschema20_1.sqsectab5 from qauser_teg;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ revoke insert on table myschema20_2.sqsectab6 from qauser_teg;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user5()
    
    stmt = """ select * from myschema20_1.sqsectab5;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ insert into myschema20_1.sqsectab5 values(1,1);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ delete from  myschema20_1.sqsectab5;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ select * from myschema20_2.sqsectab6;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ insert into myschema20_2.sqsectab6 values(1,1);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ update myschema20_2.sqsectab6 set a=a+2;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_error_msg(output, '4481')
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ drop schema myschema20_2 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop schema myschema20_1 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """revoke role SCHROLE20 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ drop role schrole20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    
    _testmgr.testcase_end(desc)    

    
def testa20(desc="""verify behavior on private schema"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """ create role schrole21;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
        
    stmt = """grant role SCHROLE21 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """grant component privilege CREATE_TABLE on SQL_OPERATIONS to qauser_teg;"""  
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ create private schema myschema21_1 AUTHORIZATION schrole21;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ create private schema myschema21_2 AUTHORIZATION qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ create table myschema21_1.sqsectab1(a int,b int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ create table myschema21_2.sqsectab2(a int,b int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ insert into myschema21_1.sqsectab1 values(1,3);"""
    output = _dci.cmdexec(stmt)    
    _dci.expect_inserted_msg(output,1)
    
    stmt = """ insert into myschema21_2.sqsectab2 values(1,3);"""
    output = _dci.cmdexec(stmt)    
    _dci.expect_inserted_msg(output,1)

    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ insert into myschema21_1.sqsectab1 values(2,3);"""
    output = _dci.cmdexec(stmt)    
    _dci.expect_inserted_msg(output,1)
    
    stmt = """ select * from myschema21_1.sqsectab1;"""
    output = _dci.cmdexec(stmt)    
    _dci.expect_selected_msg(output,2)
    
    stmt = """ create table myschema21_1.sqsectab3(a int,b int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ create table myschema21_2.sqsectab4(a int,b int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user5()
    
    stmt = """ create table myschema21_1.sqsectab5(a int,b int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ create table myschema21_2.sqsectab6(a int,b int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from  myschema21_1.sqsectab5;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,0) 
    
    stmt = """ insert into  myschema21_1.sqsectab5 values(3,4);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1) 
    
    stmt = """ update myschema21_1.sqsectab5 set a=a+1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_updated_msg(output,1)
    
    stmt = """ select * from  myschema21_2.sqsectab6;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,0) 
    
    stmt = """ insert into myschema21_2.sqsectab6 values(3,4);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1) 
    
    stmt = """ update myschema21_2.sqsectab6 set a=a+1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_updated_msg(output,1)
    
    stmt = """ select * from  myschema21_1.sqsectab1;"""
    output = mydci.cmdexec(stmt) 
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ delete from  myschema21_2.sqsectab2;"""
    output = mydci.cmdexec(stmt) 
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ delete from  myschema21_1.sqsectab3;"""
    output = mydci.cmdexec(stmt) 
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ select * from  myschema21_2.sqsectab4;"""
    output = mydci.cmdexec(stmt) 
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ insert into  myschema21_1.sqsectab1 values(3,4);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    stmt = """ grant select, delete on table myschema21_1.sqsectab1 to qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1012')
    
    stmt = """ grant insert on table myschema21_2.sqsectab2 to qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1012')
    
    stmt = """ grant select, delete on table myschema21_1.sqsectab5 to qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '1017')
    mydci.expect_complete_msg(output)
    
    stmt = """ grant insert on table myschema21_2.sqsectab6 to qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '1017')
    mydci.expect_complete_msg(output)

    stmt = """ revoke select, delete on table myschema21_1.sqsectab5 from qauser_sqlqaa;"""
    output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '1017')
    mydci.expect_complete_msg(output)
    
    stmt = """ revoke select, delete on table myschema21_2.sqsectab6 from qauser_sqlqaa;"""
    output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '1017')
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """ create table myschema21_1.sqsectab50(a int,b int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    stmt = """ create table myschema21_2.sqsectab60(a int,b int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    stmt = """ select * from  myschema21_1.sqsectab1;"""
    output = mydci.cmdexec(stmt) 
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ delete from  myschema21_2.sqsectab2;"""
    output = mydci.cmdexec(stmt) 
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ delete from myschema21_1.sqsectab3;"""
    output = mydci.cmdexec(stmt) 
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ select * from myschema21_2.sqsectab4;"""
    output = mydci.cmdexec(stmt) 
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ insert into  myschema21_1.sqsectab1 values(3,4);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
  
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ grant select, delete on table myschema21_1.sqsectab5 to qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant insert on table myschema21_2.sqsectab6 to qauser_sqlqab;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """ select * from myschema21_1.sqsectab5;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,1) 
    
    stmt = """ insert into myschema21_1.sqsectab5 values(1,1);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ delete from  myschema21_1.sqsectab5;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_deleted_msg(output,1)
    
    stmt = """ select * from myschema21_2.sqsectab6;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ insert into myschema21_2.sqsectab6 values(1,1);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)
    
    stmt = """ update myschema21_2.sqsectab6 set a=a+2;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_error_msg(output, '4481')
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ drop schema myschema21_2 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop schema myschema21_1 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """revoke role SCHROLE21 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ drop role schrole21;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """revoke component privilege CREATE_TABLE on SQL_OPERATIONS from qauser_teg;"""  
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc) 


    


    
    
    
    
    
