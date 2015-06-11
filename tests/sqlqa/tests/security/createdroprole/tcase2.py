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

# a45 create role with schema name invalid
# a46 create role with existing schema name
# a47 create role without schema name, role name is used as the schema name
# a48 Create a role1 with different schema name and create another role2 with schema name role1

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
    
def testa45(desc="""create role with schema name invalid"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """ create role c_a45role1 shared schema; 1 2"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001') 
    
    stmt = """ create role c_a45role2 private schema a8_ v;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001') 
    
    stmt = """create role c_a45role3 qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123451281234567;"""  
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """ create role c_a45role4 private schema  $@2^%$;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001') 
    
    stmt = """ create role c_a45role4 shared schema  "LMNOP-./ghij_@klmnop";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001') 
    
    _testmgr.testcase_end(desc)
    
def testa46(desc="""create role with existing schema name"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """create role c_a46role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create shared schema rolecat.myschema46_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create private schema rolecat.myschema46_2 authorization to qauser91"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create shared schema rolecat.myschema46_3 authorization to qauser92"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create shared schema authorization to qauser92;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  
    
    stmt = """grant component privilege manage_roles on sql_operations to qauser92;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    mydci = basic_defs.switch_session_qi_user4()
       
    stmt = """create role a46role1 schema rolecat.myschema46_1"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    stmt = """create role a46role2 shared schema rolecat.myschema46_2"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    stmt = """create role a46role3 private schema rolecat.myschema46_3"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    stmt = """create role a46role10 private schema c_a46role1"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    stmt = """create role c_a46role11 private schema rolecat.myschema46_4"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    stmt = """create role a46role4 schema rolecat.myschema46_1"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1017')
    
    stmt = """create role a46role5 shared schema rolecat.myschema46_2"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1017')
    
    stmt = """create role a46role6 private schema rolecat.myschema46_3"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1017')
    
    stmt = """create role a46role7 private schema qauser92"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1017')
    
    stmt = """create role a46role10 private schema c_a46role1"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1017')
    
    stmt = """create role c_a46role11 private schema rolecat.myschema46_4"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1017')
    
    stmt = """drop schema rolecat.myschema46_1 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop schema rolecat.myschema46_2 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop schema rolecat.myschema46_3 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop schema qauser92 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """revoke component privilege manage_roles on sql_operations from qauser92;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """drop role c_a46role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    _testmgr.testcase_end(desc)
    
def testa47(desc="""create role without schema name, role name is used as the schema name"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """grant component privilege manage_roles on sql_operations to qauser91;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """ create role c_a47role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """ create role c_a47role2 with admin qauser93;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ create role c_a47role3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 
    
    stmt = """ get schemas;"""
    utput = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'C_A47ROLE1' )
    _dci.expect_any_substr(output,'C_A47ROLE2' )    
    _dci.expect_any_substr(output,'C_A47ROLE3' )
    
    stmt = """ grant role c_a47role1 to qauser90;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """grant create on schema c_a47role2 to qauser90;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ grant role c_a47role3 to qauser92;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user6()
    
    stmt = """ set schema c_a47role2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ create table sqsectab1(a int,b int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ insert into table ssqsectab1 values(3,4);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)
    
    mydci = basic_defs.switch_session_qi_user5()
    
    stmt = """ set schema c_a47role1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ create table sqsectab2(a int,b int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from table sqsectab2;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,0) 
    
    stmt = """ insert into table sqsectab2 values(3,4);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1) 
    
    stmt = """ update sqsectab2 set a=a+1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_updated_msg(output,1)
    
    stmt = """ set schema c_a47role2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ create table sqsectab3(a int,b int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from table sqsectab3;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,0) 
    
    stmt = """ insert into table sqsectab3 values(3,4);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1) 
    
    stmt = """ update sqsectab3 set a=a+1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_updated_msg(output,1)
    
    stmt = """ select * from table sqsectab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ insert into table sqsectab1 values(3,4);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ update sqsectab1 set a=a+1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ grant select, insert on table c_a47role2.sqsectab1 to qauser91;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_error_msg(output, '1018')
    
    stmt = """ grant select, insert on table c_a47role2.sqsectab3 to qauser91;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ set schema c_a47role2;"""
    output = mydci.cmdexec(stmt) 
    
    stmt = """ select * from sqsectab1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ insert into table sqsectab1 values(3,4);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ select * from sqsectab3;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,1) 
    
    stmt = """ insert into table sqsectab3 values(3,4);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)
    
    stmt = """ delete from sqsectab3;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_error_msg(output, '4481')
    
    mydci = basic_defs.switch_session_qi_user4()
    
    stmt = """ set schema c_a47role3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ create table sqsectab4(a int,b int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ set schema c_a47role1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ select * from table sqsectab2;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_error_msg(output, '4481') 
    
    stmt = """ insert into table sqsectab2 values(3,4);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ update sqsectab2 set a=a+1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_error_msg(output, '4481')
    
    stmt = """grant component privilege manage_roles on sql_operations to qauser91;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """ drop role c_a47role1 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """ drop role c_a47role2 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ drop role c_a47role3 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    
def testa48(desc="""Create a role1 with different schema name and create another role2 with schema name role1"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
      
     


    
            