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


def testa01(desc="""get/showddl users"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """unregister user qauser43;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user qauser44;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user qauser45;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user sqlchen;"""
    output = _dci.cmdexec(stmt)

    stmt = """register user qauser43;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """register user qauser44 as sqlchen;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
  

    stmt = """get users;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'DB__ROOT')
    _dci.expect_any_substr(output,'SQLUSER_ADMIN' )
    _dci.expect_any_substr(output,'SQLCHEN' )
    _dci.expect_any_substr(output,'PAULLOW43' )


    stmt = """unregister user sqlchen;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """unregister user qauser44;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """register user qauser44;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """register user qauser45;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)    


def testa02(desc="""get/showddl roles"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """drop role getrole1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role getrole2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role getrole3;"""
    output = _dci.cmdexec(stmt)

    stmt = """create role getrole1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
        
    stmt = """create role getrole2 with admin qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role getrole3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant role getrole1 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant role getrole2 to qauser_sqlqab by qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """get roles;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'GETROLE1' )
    _dci.expect_any_substr(output,'GETROLE2' )
    _dci.expect_any_substr(output,'GETROLE3' )

    mydci = basic_defs.switch_session_qi_user2()
    
    #mydci = _testmgr.get_dci_proc('qi_mxci2')

    stmt = """get roles;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_any_substr(output,'GETROLE1' )
    mydci.expect_any_substr(output,'GETROLE2' )
    mydci.expect_any_substr(output,'GETROLE3' )

    stmt = """showddl role getrole1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'CREATE ROLE "GETROLE1"' )

    stmt = """showddl role getrole1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'GRANT ROLE\n  "GETROLE1" TO "QAUSER_SQLQAA"' )

    stmt = """showddl role getrole2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'CREATE ROLE "GETROLE2" WITH ADMIN "QAUSER_SQLQAA"' )

    stmt = """showddl role getrole2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'GRANT ROLE\n  "GETROLE2" TO "QAUSER_SQLQAB"' )

    stmt = """showddl role getrole3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'CREATE ROLE "GETROLE3";' )

    stmt = """revoke role getrole1 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """revoke role getrole2 from qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role getrole1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop role getrole2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop role getrole3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)   


  
def testa03(desc="""get/showddl component"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return    

    stmt = """unregister component get_comp1;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister component get_comp2;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister component get_comp3;"""
    output = _dci.cmdexec(stmt)

    stmt = """register component get_comp1;"""
    output = _dci.cmdexec(stmt)

    stmt = """register component get_comp2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """register component get_comp3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """get components;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'GET_COMP1' )
    _dci.expect_any_substr(output,'GET_COMP2' )
    _dci.expect_any_substr(output,'GET_COMP3' )
        
    stmt = """showddl component get_comp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'REGISTER COMPONENT GET_COMP1' )

    stmt = """showddl component get_comp2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'REGISTER COMPONENT GET_COMP2' )

    stmt = """showddl component get_comp3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'REGISTER COMPONENT GET_COMP3' )

    stmt = """unregister component get_comp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """unregister component get_comp2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """unregister component get_comp3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

      
def testa04(desc="""get component privileges on component-name | for authid"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return   
    
    stmt = """unregister component get_comp4;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister component get_comp5;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister component get_comp6;"""
    output = _dci.cmdexec(stmt)

    stmt = """register component get_comp4;"""
    output = _dci.cmdexec(stmt)

    stmt = """register component get_comp5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """register component get_comp6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create component privilege cre as \'ca\' on get_comp4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create component privilege upd as \'up\' on get_comp5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create component privilege aaa as \'as\' on get_comp5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create component privilege bbb as \'bs\' on get_comp6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant component privilege cre on get_comp4 to qauser_sqlqaa with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """grant component privilege upd,aaa  on get_comp5 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant component privilege bbb  on get_comp6 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant component privilege manage_roles on sql_operations to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """get component privileges on get_comp4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'CRE' )

    stmt = """get component privileges on get_comp5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'UPD' )
    _dci.expect_any_substr(output,'AAA' )

    stmt = """get component privileges on get_comp6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'BBB' )

    stmt = """get component privileges on get_comp4 for qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'CRE' )

    stmt = """get component privileges on get_comp5 for qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'UPD' )
    _dci.expect_any_substr(output,'AAA' )

    stmt = """get component privileges on get_comp6 for qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'BBB' )

    stmt = """get component privileges on sql_operations for qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'MANAGE_ROLES' )
    _dci.unexpect_any_substr(output,'CREATE_VIEW' )

    stmt = """revoke component privilege manage_roles on sql_operations from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """unregister component get_comp4 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister component get_comp5 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister component get_comp6 cascade;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)
    
    
def testa05(desc="""gshowddl [procedure] object-name[,privileges]"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return           
        

    stmt = """drop role getrole5;"""
    output = _dci.cmdexec(stmt)

    stmt = """create role getrole5;"""
    output = _dci.cmdexec(stmt)

    stmt = """grant role getrole5 to qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create schema get_schema1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """set schema get_schema1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table t1;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table t1 (c1 int not null primary key, c2 int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ grant select on table t1 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ grant select on table t1 to getrole5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ grant select on table t1 to qauser_tsang granted by qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    #_dci.expect_complete_msg(output)
    _dci.expect_error_msg(output, '1229')

    stmt = """ grant select on table t1 to qauser_tsang granted by getrole5;"""
    output = _dci.cmdexec(stmt)
    #_dci.expect_complete_msg(output)
    _dci.expect_error_msg(output, '1229')
    
    #mydci = _testmgr.get_dci_proc('qi_mxci1')

    #stmt = """set schema get_schema1;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
         
    #stmt = """ grant select on table t1 to qauser_teg;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    stmt = """set schema get_schema1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl procedure t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'-- GRANT DELETE, INSERT, SELECT, UPDATE, REFERENCES ON TRAFODION.GET_SCHEMA1.T1 TO DB__ROOT WITH GRANT OPTION;')
    #_dci.expect_any_substr(output,'GRANT SELECT ON\n  TRAFODION.GET_SCHEMA1.T1 TO QAUSER_TSANG;' )
    _dci.expect_any_substr(output,'GRANT SELECT ON TRAFODION.GET_SCHEMA1.T1 TO QAUSER_SQLQAA;' )
    _dci.expect_any_substr(output,'GRANT SELECT ON\n  TRAFODION.GET_SCHEMA1.T1 TO GETROLE5;' )


    stmt = """showddl t1, privileges;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'-- GRANT DELETE, INSERT, SELECT, UPDATE, REFERENCES ON TRAFODION.GET_SCHEMA1.T1 TO DB__ROOT WITH GRANT OPTION;')
    #_dci.expect_any_substr(output,'GRANT SELECT ON\n  TRAFODION.GET_SCHEMA1.T1 TO QAUSER_TSANG;' )
    _dci.expect_any_substr(output,'GRANT SELECT ON TRAFODION.GET_SCHEMA1.T1 TO QAUSER_SQLQAA;' )
    _dci.expect_any_substr(output,'GRANT SELECT ON\n  TRAFODION.GET_SCHEMA1.T1 TO GETROLE5;' )


    stmt = """create view v1 as select * from t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl procedure v1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'CREATE VIEW TRAFODION.GET_SCHEMA1.V1')


    stmt = """drop view v1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

        #stmt='revoke select on table t1 from qauser_teg by qauser_sqlqab;"""
        #_dci.expect_complete_msg(output)

        #stmt='revoke select on table t1 from qauser_tsang by getrole5;"""
        #_dci.expect_complete_msg(output)

        #stmt='revoke select on table t1 from qauser_tsang by qauser_sqlqaa;"""
        #_dci.expect_complete_msg(output)

        #stmt='revoke select on table t1 from qauser_sqlqaa;"""
        #_dci.expect_complete_msg(output)

        #stmt='revoke select on table t1 from getrole5;"""
        #_dci.expect_complete_msg(output)

    stmt = """drop table t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop schema get_schema1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke role getrole5 from qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop role getrole5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    





        