# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2015 Hewlett-Packard Development Company, L.P.
#
#  Licensed under the Apache License, Version 2.0 (the "License")
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


def testa01(desc="""test initialize authorization, vary ordering of clauses, misspell keywords"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """initialize authorization,;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """initialize authorization*;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    mydci = basic_defs.switch_session_qi_user2()    

    stmt = """initialize authorization,;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')
    
    stmt = """initialize authorization*;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')
    
    _testmgr.testcase_end(desc) 

    
def testa02(desc="""test initialize authorization,drop, vary ordering of clauses, misspell keywords"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
 
    stmt = """initialize authorization,, drop;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
        
    stmt = """initialize authorization; drop;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """initialize authorization drop;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    _testmgr.testcase_end(desc) 


def testa03(desc="""Test Authorization already is initialized then initialized again"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """initialize authorization;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """initialize authorization;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()  

    stmt = """initialize authorization;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')

    _testmgr.testcase_end(desc) 



def testa04(desc="""Test other users initialize Authorization and drop"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """initialize authorization,drop;"""
    output = _dci.cmdexec(stmt)

    mydci = basic_defs.switch_session_qi_user2()    

    stmt = """initialize authorization;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')

    stmt = """initialize authorization;"""
    output = _dci.cmdexec(stmt)

    stmt = """initialize authorization,drop;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    _testmgr.testcase_end(desc) 


def testa05(desc="""The DROP option removes all the privilege manager metadata tables. Existing objects will be retained"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """initialize authorization;"""
    output = _dci.cmdexec(stmt)

    stmt = """create schema authschema1;"""
    output = _dci.cmdexec(stmt)

    stmt = """set schema authschema1;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table authtaba_05;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table authtaba_05 ( a int, b int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """initialize authorization,drop;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from "_PRIVMGR_MD_".OBJECT_PRIVILEGES where OBJECT_NAME='TRAFODION.AUTHSCHEMA1.AUTHTABA_05' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')

    stmt = """get schemas;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output,'"_PRIVMGR_MD_"' )

    stmt = """set schema AUTHSCHEMA1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """get tables;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'AUTHTABA_05' )

    stmt = """drop table authtaba_05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop schema authschema1;"""
    output = _dci.cmdexec(stmt)

    stmt = """initialize authorization;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc) 


	
def testa06(desc="""Verify after INITIALIZE AUTHORIZATION is specified, the privilege manager metadata tables are created."""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """initialize authorization,drop;"""
    output = _dci.cmdexec(stmt)

    #time.sleep(60)

    stmt = """get roles;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output,'DB__ROLTROLE')

    stmt = """register component comp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1222')

    stmt = """drop role auth_role1;"""
    output = _dci.cmdexec(stmt)

    stmt = """create role auth_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()  

    stmt = """grant role auth_role1 to "qauser_sqlqab";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')

    stmt = """create schema sch_auth6;"""
    output = _dci.cmdexec(stmt)

    stmt = """set schema sch_auth6;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table authtaba_06;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table authtaba_06 ( a int, b int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from "_PRIVMGR_MD_".OBJECT_PRIVILEGES;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')

        #stmt = 'get components;"""
        #self._odbc.expect_error_msg(stmt, '1222');

    stmt = """initialize authorization;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """get components;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'SQL_OPERATIONS')

    stmt = """get roles;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'DB__ROOTROLE')

    stmt = """showddl TRAFODION."_PRIVMGR_MD_".OBJECT_PRIVILEGES;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'CREATE TABLE TRAFODION."_PRIVMGR_MD_".OBJECT_PRIVILEGES' )

    #time.sleep(10)

    #stmt = """select * from "_PRIVMGR_MD_".OBJECT_PRIVILEGES where OBJECT_NAME='TRAFODION."SCH_AUTH6"."AUTHTABA_06"' ;"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_selected_msg(output, 1)

    stmt = """drop table authtaba_06;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop schema sch_auth6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """set schema TRAFODION."_PRIVMGR_MD_";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """get tables;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'OBJECT_PRIVILEGES' )
    _dci.expect_any_substr(output,'COMPONENTS' )
    _dci.expect_any_substr(output,'ROLE_USAGE' )
    _dci.expect_any_substr(output,'COMPONENT_OPERATIONS' )
    _dci.expect_any_substr(output,'COMPONENT_PRIVILEGES' )

    stmt = """drop role auth_role1;"""
    ooutput = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc) 


def testa07(desc="""Verify create a table will insert a row in the object_privilege table describing owner rights ."""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """initialize authorization;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """set schema sch_auth;""" 
    output = _dci.cmdexec(stmt)

    stmt = """drop table authtaba;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table authtaba2;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table authtaba3;"""
    output = _dci.cmdexec(stmt)

    stmt = """create schema sch_auth;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """set schema sch_auth;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table AUTHTABA( c1 int CONSTRAINT t1pri PRIMARY KEY CONSTRAINT t1ntnul1 NOT NULL NOT DROPPABLE, c2 char(3) CONSTRAINT t1uniq UNIQUE CONSTRAINT t1ntnul2 NOT NULL, c3 char(2));"""	
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from TRAFODION."_PRIVMGR_MD_".OBJECT_PRIVILEGES where OBJECT_NAME = 'TRAFODION.SCH_AUTH.AUTHTABA' and GRANTEE_NAME='DB__ROOT';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)

    stmt = """drop table authtaba;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from TRAFODION."_PRIVMGR_MD_".OBJECT_PRIVILEGES where OBJECT_NAME = 'TRAFODION.SCH_AUTH.AUTHTABA' and GRANTEE_NAME='DB__ROOT';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)

    stmt = """drop schema sch_auth;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """initialize authorization;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()     

    stmt = """create schema sch_auth_2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema sch_auth_2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop table authtabb;"""
    output = mydci.cmdexec(stmt)

    stmt = """create table authtabb( c1 int CONSTRAINT t1pri PRIMARY KEY CONSTRAINT t1ntnul1 NOT NULL NOT DROPPABLE, c2 char(3) CONSTRAINT t1uniq UNIQUE CONSTRAINT t1ntnul2 NOT NULL, c3 char(2));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select * from TRAFODION."_PRIVMGR_MD_".OBJECT_PRIVILEGES where OBJECT_NAME = 'TRAFODION.SCH_AUTH_2.AUTHTABB' ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    stmt = """select * from TRAFODION."_PRIVMGR_MD_".OBJECT_PRIVILEGES where OBJECT_NAME = 'TRAFODION.SCH_AUTH_2.AUTHTABB' and GRANTEE_NAME='PAULLOW99' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    
    mydci = basic_defs.switch_session_qi_user2()     

    stmt = """set schema sch_auth_2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop table authtabb;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """select * from TRAFODION."_PRIVMGR_MD_".OBJECT_PRIVILEGES where OBJECT_NAME = 'TRAFODION.SCH_AUTH_2.AUTHTABB' and GRANTEE_NAME='PAULLOW99' ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0);

    stmt = """drop schema sch_auth_2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc) 
    

def testa08(desc="""Verify grant select/delete will insert/update a row in the object_privileges table with the new privileges and drop will clear ."""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """initialize authorization;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke select, delete on table authtaba1 from qauser80;"""
    output = _dci.cmdexec(stmt)

    stmt = """create schema authschema8;"""
    output = _dci.cmdexec(stmt)

    stmt = """set schema authschema8;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table authtaba1;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table authtaba1( c1 int NOT NULL NOT DROPPABLE, c2 char(3) NOT NULL, c3 char(2));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant select, delete on table authtaba1 to qauser80;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl authtaba1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'GRANT DELETE, SELECT ON TRAFODION.AUTHSCHEMA8.AUTHTABA1 TO PAULLOW80' )

    stmt = """select * from TRAFODION."_PRIVMGR_MD_".OBJECT_PRIVILEGES where OBJECT_NAME = 'TRAFODION.AUTHSCHEMA8.AUTHTABA1' and GRANTOR_NAME = 'DB__ROOT' and GRANTEE_NAME = 'PAULLOW80';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)

    stmt = """initialize authorization,drop;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl authtaba1;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output,'GRANT DELETE, SELECT ON TRAFODION.AUTHSCHEMA8.AUTHTABA1 TO PAULLOW80' )

    stmt = """grant select, delete on table authtaba1 to qauser80;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1222')

    stmt = """revoke select, delete on table authtaba1 from qauser80;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1222')

    stmt = """drop table authtaba1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop schema authschema8;"""
    output = _dci.cmdexec(stmt)

    stmt = """initialize authorization;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc) 
  
  
def testa09(desc="""Verify grant update/insert will insert/update a row in the object_privileges table with the new privileges"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """initialize authorization;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke insert on table authtaba2 from qauser80;"""
    output = _dci.cmdexec(stmt)

    stmt = """create schema authschema9;"""
    output = _dci.cmdexec(stmt)

    stmt = """set schema authschema9;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table authtaba2;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table authtaba2( c1 int, c2 int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant insert on table authtaba2 to qauser80;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    

    stmt = """select * from TRAFODION."_PRIVMGR_MD_".OBJECT_PRIVILEGES where OBJECT_NAME = 'TRAFODION.AUTHSCHEMA9.AUTHTABA2' and GRANTOR_NAME = 'DB__ROOT' and GRANTEE_NAME = 'PAULLOW80';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)

    stmt = """revoke insert on table authtaba2 from qauser80;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

        #stmt = 'drop table authtaba2;"""
    stmt = """drop table TRAFODION.authschema9.AUTHTABA2;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop schema authschema9;""" 
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc) 


def testa10(desc="""Verify grant all_dml will insert/update a row in the object_privileges table with the new privileges. ."""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """initialize authorization;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke all_dml on table authtaba3 from qauser80;"""
    output = _dci.cmdexec(stmt)

        #stmt = 'drop table authtaba;"""
    stmt = """drop table TRAFODION.SOMESCHEMA.AUTHTABA3;""" 
    output = _dci.cmdexec(stmt)

    stmt = """create schema authschema10;""" 
    output = _dci.cmdexec(stmt)

    stmt = """set schema authschema10;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table authtaba3( c1 int, c2 char(3) NOT NULL, c3 char(2));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant all_dml on table authtaba3 to qauser80;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from TRAFODION."_PRIVMGR_MD_".OBJECT_PRIVILEGES where OBJECT_NAME = 'TRAFODION.AUTHSCHEMA10.AUTHTABA3' and GRANTOR_NAME = 'DB__ROOT' and GRANTEE_NAME = 'PAULLOW80';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)

    stmt = """revoke all_dml on table authtaba3 from qauser80;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

        #stmt = 'drop table authtaba3;"""
    stmt = """drop table TRAFODION.AUTHSCHEMA10.AUTHTABA3;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop schema authschema10;""" 
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc) 
    
def testa11(desc="""Verify revoke will update/delete a row from the object_privileges table removing privileges. ."""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """initialize authorization;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke all_dml on table authtaba4 from qauser80;"""
    output = _dci.cmdexec(stmt)

    stmt = """create schema authschema11;""" 
    output = _dci.cmdexec(stmt)

    stmt = """set schema authschema11;"""
    output = _dci.cmdexec(stmt)

        #stmt = 'drop table authtaba4;"""
    stmt = """drop table TRAFODION.AUTHSCHEMA11.AUTHTABA4;""" 
    output = _dci.cmdexec(stmt)

    stmt = """create table authtaba4( c1 int, c2 char(3) NOT NULL, c3 char(2));"""	
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant all_dml on table authtaba4 to qauser80;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke all_dml on table authtaba4 from qauser80;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from TRAFODION."_PRIVMGR_MD_".OBJECT_PRIVILEGES where OBJECT_NAME = 'TRAFODION.AUTHSCHEMA11.AUTHTABA4' and GRANTOR_NAME = 'DB__ROOT\ and GRANTEE_NAME = 'PAULLOW80'; '
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0);

        #stmt = 'drop table authtaba4;"""
    stmt = """drop table TRAFODION.AUTHSCHEMA11.AUTHTABA4;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop SCHEMA authschema11;""" 
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc) 


def testa12(desc="""A showddl (when authorization is enabled) will display grants ."""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """initialize authorization;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke all_dml on table authtaba5 from qauser80;"""
    output = _dci.cmdexec(stmt)

    stmt = """create schema authschema12;"""
    output = _dci.cmdexec(stmt)

    stmt = """set schema authschema12;"""
    output = _dci.cmdexec(stmt)

        #stmt = 'drop table authtaba;"""
    stmt = """drop table TRAFODION.AUTHSCHEMA12.AUTHTABA5;"""       
    output = _dci.cmdexec(stmt)


    stmt = """create table authtaba5( c1 int, c2 char(3) NOT NULL, c3 char(2));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant all_dml on table authtaba5 to qauser80;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl table authtaba5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'-- GRANT DELETE, INSERT, SELECT, UPDATE, REFERENCES ON TRAFODION.AUTHSCHEMA12.AUTHTABA5 TO DB__ROOT WITH GRANT OPTION;' )
    _dci.expect_any_substr(output,'GRANT DELETE, INSERT, SELECT, UPDATE, REFERENCES ON\n  TRAFODION.AUTHSCHEMA12.AUTHTABA5 TO PAULLOW80;')

    stmt = """revoke all_dml on table authtaba5 from qauser80;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

        #stmt = 'drop table authtaba;"""
    stmt = """drop table TRAFODION.AUTHSCHEMA12.AUTHTABA5;"""    
    output = _dci.cmdexec(stmt)    
    _dci.expect_complete_msg(output)

    stmt = """drop schema authschema12;"""   
    output = _dci.cmdexec(stmt)   
    
    _testmgr.testcase_end(desc) 

   