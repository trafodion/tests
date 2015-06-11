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


def testa01(desc="""udf function - syntax checking"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """ set schema SECURITY_UDF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop function GETMXV;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop function ADD2;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop library sec_udflib1 cascade;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create library """+ defs.sec_udflib1 +""" file '"""+ defs.spjpath +"""';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


    #different characteristics. ADD2: Adds two integers
    stmt = """create function ADD2(int,int) returns (ADD2 int)
            language c parameter style sql external name 'add2'
            library sec_udflib1
            not deterministic no sql final call state area 1024
            no parallelism fast execution mode;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    # verify state area size
    stmt = """create function ADD2(int,int) returns (ADD2 int)
            language c parameter style sql external name 'add2'
            library sec_udflib1
            not deterministic no sql final call state area size 16001;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3272')
    
    #illegal state area size
    stmt = """create function ADD2(int,int) returns (ADD2 int)
            language c parameter style sql external name 'add2'
            library sec_udflib1
            not deterministic no sql final call state area size -1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    #not exist library
    stmt = """create function ADD2(int,int) returns (ADD2 int)
            language c parameter style sql external name 'add2'
            library sec_udflib1TMP
            not deterministic no sql final call state area size 16000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1389')
    
    
    #missing external name
    stmt = """create function ADD2(int) returns (ADD2 int)
        language c parameter style sql library sec_udflib1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3205')
    
    #wrong language
    stmt = """create function ADD2(int,int) returns (ADD2 int)
            language c++ parameter style sql external name 'add2'
            library sec_udflib1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3205')
    _dci.expect_error_msg(output, '15001')

    #missing library clause
    stmt = """create function ADD2(int,int) returns (ADD2 int)
            language c parameter style sql external name 'add2';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1389')

     
    #return no values
    stmt = """create function ADD2(int,int) returns (ADD2)
            language c parameter style sql external name 'add2'
            library sec_udflib1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    #return no values
    stmt = """create function ADD2(int,int) returns ()
            language c parameter style sql external name 'add2'
            library sec_udflib1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """drop function add2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop function GETMXV;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop library sec_udflib1 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    _testmgr.testcase_end(desc)
    
def testa02(desc="""create udf function"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """ set schema SECURITY_UDF;"""
    output = _dci.cmdexec(stmt)    
    
    stmt = """drop function ADD2;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop library sec_udflib1 cascade;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create library """+ defs.sec_udflib1 +""" file '"""+ defs.spjpath +"""';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ grant usage on library sec_udflib1 to qauser13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """create function ADD2(int,int) returns (ADD2 int)
            language c parameter style sql external name 'add2'
            library sec_udflib1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ drop function ADD2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1389')
    
    mydci = basic_defs.switch_session_qi_user4()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """create function ADD2(int,int) returns (ADD2 int)
            language c parameter style sql external name 'add2'
            library sec_udflib1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    stmt = """ set schema SECURITY_UDF;"""
    output = _dci.cmdexec(stmt)

    stmt = """ drop function ADD2;"""
    output = _dci.cmdexec(stmt)
    
    mydci = basic_defs.switch_session_qi_user5()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """create function ADD2(int,int) returns (ADD2 int)
            language c parameter style sql external name 'add2'
            library sec_udflib1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    stmt = """ drop function ADD2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1389')
    
    stmt = """ set schema SECURITY_UDF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """ revoke usage on library sec_udflib1 from qauser13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop library sec_udflib1 cascade;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)
    
def testa03(desc="""grant usage/all privilege on library"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return     
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """create library """+ defs.sec_udflib1 +""" file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant usage on library sec_udflib1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """create function ADD2(int, int) returns (ADD2 int)
            language c parameter style sql external name 'add2'
            library sec_udflib1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop function add2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user4()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """create function ADD2(int, int) returns (ADD2 int)
            language c parameter style sql external name 'add2'
            library sec_udflib1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ revoke usage on library sec_udflib1 from qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant all on library sec_udflib1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """create function ADD2(int, int) returns (ADD2 int)
            language c parameter style sql external name 'add2'
            library sec_udflib1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop function add2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ revoke all on library sec_udflib1 from qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop library sec_udflib1 cascade;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)
    
def testa04(desc="""revoke usage/all privilege on library"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return    

    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """create library """+ defs.sec_udflib1 +""" file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant usage on library sec_udflib1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """create function ADD2(int, int) returns (ADD2 int)
            language c parameter style sql external name 'add2'
            library sec_udflib1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop function add2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ revoke usage on library sec_udflib1 from qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """create function ADD2(int, int) returns (ADD2 int)
            language c parameter style sql external name 'add2'
            library sec_udflib1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
       
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """grant all on library sec_udflib1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """create function ADD2(int, int) returns (ADD2 int)
            language c parameter style sql external name 'add2'
            library sec_udflib1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop function add2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """drop library sec_udflib1 cascade;"""
    output = mydci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

  
def testa05(desc="""drop library/cascade with an existing function"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return     

    stmt = """ set schema SECURITY_UDF;"""
    output = _dci.cmdexec(stmt)    
    
    stmt = """drop function ADD2;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop library sec_udflib1 cascade;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create library """+ defs.sec_udflib1 +""" file '"""+ defs.spjpath +"""';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create function ADD2(int, int) returns (ADD2 int)
            language c parameter style sql external name 'add2'
            library sec_udflib1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user4()

    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt) 
    
    stmt = """ drop library sec_udflib1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    stmt = """ drop library sec_udflib1 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    mydci = basic_defs.switch_session_qi_user2()

    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt) 
    
    stmt = """ drop library sec_udflib1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1366')
    
    stmt = """ drop library sec_udflib1 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    
def testa06(desc="""verify execute privilege on udf function"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return    

    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """create library """+ defs.sec_udflib1 +""" file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ create function myudf (INVAL int)
                returns (OUTVAL int)
                language c
                parameter style sql
                external name 'myudf'
                library sec_udflib1
                deterministic
                state area size 1024
                allow any parallelism
                no sql;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)            

    stmt = """create table mytable (a int, b int);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into mytable values (1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt = """ grant execute on function myudf to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select on table mytable to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select on table mytable to qauser12;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ select myudf(a) from mytable;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)
    
    mydci = basic_defs.switch_session_qi_user4()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
  
    stmt = """ select myudf(a) from mytable;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4482')
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)

    stmt = """ drop function myudf cascade;"""
    output = mydci.cmdexec(stmt)	
    
    stmt = """ drop library sec_udflib1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """ drop table mytable cascade;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)
    
def testa07(desc="""verify drop udf function"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return    
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """create library """+ defs.sec_udflib1 +""" file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """ create function myudf (INVAL int)
                returns (OUTVAL int)
                language c
                parameter style sql
                external name 'myudf'
                library sec_udflib1
                deterministic
                state area size 1024
                allow any parallelism
                no sql;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)            

    stmt = """create table mytable (a int, b int);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into mytable values (1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt = """ create view myview as select myudf(a) from mytable;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user4()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ drop function myudf;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ select myudf(a) from mytable;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,1)
    
    stmt = """ drop function myudf restrict;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1047')
    
    stmt = """ select * from myview;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,1)
    
    stmt = """select myudf(a) from mytable;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,1)
        
    stmt = """ drop function myudf;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1047')
    
    stmt = """ select * from myview;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,1)
    
    stmt = """select myudf(a) from mytable;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,1)
    
    stmt = """ drop function myudf cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from myview;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_error_msg(output, '4082')
    
    stmt = """select myudf(a) from mytable;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_error_msg(output, '4450')

    stmt = """ drop table mytable cascade;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ drop library sec_udflib1 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    
    
def testa08(desc="""create view and execute privilege on UDF"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return    

    stmt = """GRANT COMPONENT privilege create_view on sql_operations to qauser11;"""
    output = _dci.cmdexec(stmt)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ create schema SECURITY_UDF2;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ set schema SECURITY_UDF2;"""
    output = mydci.cmdexec(stmt)

    stmt = """create library sec_udflib1 file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """ create function myudf (INVAL int)
                returns (OUTVAL int)
                language c
                parameter style sql
                external name 'myudf'
                library sec_udflib1
                deterministic
                state area size 1024
                allow any parallelism
                no sql;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)            

    stmt = """create table mytable (a int, b int);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into mytable values (1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)

    stmt = """grant select on  mytable to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    #CREATE VIEW should only work if the user has EXECUTE privilege on the UDF. 
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """ set schema SECURITY_UDF2;"""
    output = mydci.cmdexec(stmt)    
    
    stmt = """ create view myview as select myudf(a) from mytable;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4482')    
    
    mydci = basic_defs.switch_session_qi_user4()
    
    stmt = """ set schema SECURITY_UDF2;"""
    output = mydci.cmdexec(stmt)    
    
    stmt = """ create view myview as select myudf(a) from mytable;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  
    mydci.expect_error_msg(output, '4482')
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ grant execute on function myudf to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """ set schema SECURITY_UDF2;"""
    output = mydci.cmdexec(stmt)    
    
    stmt = """ create view myview as select myudf(a) from mytable;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from myview;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,1) 
    
    stmt = """ drop view myview;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')  
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ set schema SECURITY_UDF2;"""
    output = mydci.cmdexec(stmt) 

    stmt = """ drop table mytable cascade;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ drop function myudf;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop library sec_udflib1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """ drop schema SECURITY_UDF2 cascade;"""
    output = mydci.cmdexec(stmt)

    stmt = """revoke COMPONENT privilege create_view on sql_operations from qauser11;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)    
    
def testa09(desc="""other user create view and drop UDF/restrict"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return    

    stmt = """GRANT COMPONENT privilege create_view on sql_operations to qauser11;"""
    output = _dci.cmdexec(stmt)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """create library """+ defs.sec_udflib1 +""" file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """ create function myudf (INVAL int)
                returns (OUTVAL int)
                language c
                parameter style sql
                external name 'myudf'
                library sec_udflib1
                deterministic
                state area size 1024
                allow any parallelism
                no sql;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)            

    stmt = """create table mytable (a int, b int);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into mytable values (1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)  

    stmt = """grant select on  mytable to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant execute on function myudf to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ create view myview as select myudf(a) from mytable;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop function myudf restrict;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1047')
    
    stmt = """ select * from myview;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,1)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)

    stmt = """ select * from myview;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,1)
    
    stmt = """ drop view myview;"""
    output = mydci.cmdexec(stmt)

    stmt = """ drop table mytable cascade;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ drop function myudf restrict;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ drop library sec_udflib1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """revoke COMPONENT privilege create_view on sql_operations from qauser11;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)
    
    
def testa10(desc="""other user create view and drop UDF/cascade"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return      

    stmt = """GRANT COMPONENT privilege create_view on sql_operations to qauser11;"""
    output = _dci.cmdexec(stmt)

    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """create library """+ defs.sec_udflib1 +""" file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """ create function myudf (INVAL int)
                returns (OUTVAL int)
                language c
                parameter style sql
                external name 'myudf'
                library sec_udflib1
                deterministic
                state area size 1024
                allow any parallelism
                no sql;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)            

    stmt = """create table mytable (a int, b int);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into mytable values (1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)   

    stmt = """grant select on  mytable to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant execute on function myudf to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ create view myview as select myudf(a) from mytable;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop function myudf cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from myview;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_error_msg(output, '4082')
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ drop view myview;"""
    output = mydci.cmdexec(stmt)

    stmt = """ drop table mytable cascade;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ drop function myudf restrict;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ drop library sec_udflib1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """revoke COMPONENT privilege create_view on sql_operations from qauser11;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)
    
    
def testa11(desc="""db_root create view references to undefined UDFs """):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return      
    
    stmt = """ set schema SECURITY_UDF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table mytable (a int, b int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into mytable values (1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,1) 
   
    stmt = """ create view myview as select GETA(a) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4450')
    
    stmt = """ drop table mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    
    
def testa12(desc="""other user create view references to undefined UDFs """):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return      
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """create table mytable (a int, b int);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into mytable values (1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)   
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
   
    stmt = """ create view myview as select GETA(a) from mytable;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4450')
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ drop table mytable;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    
    
def testa13(desc="""revoke EXECUTE from a UDF """):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return  


    stmt = """GRANT COMPONENT privilege create_view on sql_operations to qauser11;"""
    output = _dci.cmdexec(stmt)    
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """create library """+ defs.sec_udflib1 +""" file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """ create function myudf (INVAL int)
                returns (OUTVAL int)
                language c
                parameter style sql
                external name 'myudf'
                library sec_udflib1
                deterministic
                state area size 1024
                allow any parallelism
                no sql;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)            

    stmt = """create table mytable (a int, b int);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into mytable values (1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)   

    stmt = """grant select on  mytable to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant execute on function myudf to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ create view myview as select myudf(a) from mytable;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from myview;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,1)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ revoke execute on function myudf from qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ create view myview1 as select myudf(a) from mytable;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4482')
    
    stmt = """ select * from myview;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,1)
    
    stmt = """create view myview as select myudf(a) from mytable;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4482')
    
    stmt = """ drop view myview;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ drop table mytable cascade;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ drop function myudf cascade;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ drop library sec_udflib1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """revoke COMPONENT privilege create_view on sql_operations from qauser11;"""
    output = _dci.cmdexec(stmt) 
   
    _testmgr.testcase_end(desc)
    
    
def testa14(desc="""create view with sequence generator """):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return     

    stmt = """GRANT COMPONENT privilege create_view on sql_operations to qauser11;"""
    output = _dci.cmdexec(stmt)   
    
    #mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table mytable (a int, b int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into mytable values (1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,1)  
    
    stmt = """ create sequence myseq; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create view myview as select seqnum(myseq) as a from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop view myview;"""
    output = _dci.cmdexec(stmt)

    stmt = """grant select on  mytable to qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """create view myview as select seqnum(myseq) as a from mytable;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4491')
    
    stmt = """create view myview1 as select a from mytable where b < seqnum(myseq);;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4491')
    
    #mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """grant usage on sequence myseq to qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """create view myview as select seqnum(myseq) as a from mytable;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create view myview1 as select a from mytable where b < seqnum(myseq);;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
 
    #mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = _dci.cmdexec(stmt)
    
    stmt=""" drop sequence myseq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ select * from myview;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4481')
    
    stmt = """ select * from myview1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4481')
    
    stmt =""" drop table mytable cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke COMPONENT privilege create_view on sql_operations from qauser11;"""
    output = _dci.cmdexec(stmt) 
    
    _testmgr.testcase_end(desc)
    
    
def testa15(desc="""create multi-level view with sequence generator and drop sq"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return    
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """create table mytable (a int, b int);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into mytable values (1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt = """ create sequence myseq; """
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ create view myview1 as select seqnum(myseq) from mytable;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create view myview2 as select a from myview1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
 
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt=""" drop sequence myseq;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from myview1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ select * from myview2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt =""" drop table mytable cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    
    
def testa16(desc="""other user create multi-level view with sequence generator and drop sq"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return   

    stmt = """GRANT COMPONENT privilege create_view on sql_operations to qauser11;"""
    output = _dci.cmdexec(stmt)   
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """create table mytable (a int, b int);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into mytable values (1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 
    
    stmt = """ create sequence myseq; """
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """grant usage on sequence myseq to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant select on  mytable to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ create view myview1 as select seqnum(myseq) from mytable;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create view myview2 as select a from myview1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
 
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt=""" drop sequence myseq;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from myview1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ select * from myview2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt =""" drop table mytable cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """revoke COMPONENT privilege create_view on sql_operations from qauser11;"""
    output = _dci.cmdexec(stmt) 
    
    _testmgr.testcase_end(desc)    

def testa17(desc="""create multi-level view with UDF and drop UDF"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return    
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """create library """+ defs.sec_udflib1 +""" file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """ create function myudf (INVAL int)
                returns (OUTVAL int)
                language c
                parameter style sql
                external name 'myudf'
                library sec_udflib1
                deterministic
                state area size 1024
                allow any parallelism
                no sql;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)            

    stmt = """create table mytable (a int, b int);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into mytable values (1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1) 

    stmt = """ create view myview1 as select myudf(a) from mytable;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ create view myview2 as select * from myview1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop function myudf restrict;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ select * from myview1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,1)
    
    stmt = """ select * from myview2;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,1)
    
    stmt = """ drop function myudf cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from myview1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ select * from myview2;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_error_msg(output, '4481')

    
    stmt = """ drop table mytable cascade;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ drop function myudf restrict;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ drop library sec_udflib1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)    
    
def testa18(desc="""other user create multi-level view with UDF and drop UDF"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return  

    stmt = """GRANT COMPONENT privilege create_view on sql_operations to qauser11;"""
    output = _dci.cmdexec(stmt)     
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """create library """+ defs.sec_udflib1 +""" file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """ create function myudf (INVAL int)
                returns (OUTVAL int)
                language c
                parameter style sql
                external name 'myudf'
                library sec_udflib1
                deterministic
                state area size 1024
                allow any parallelism
                no sql;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)            

    stmt = """create table mytable (a int, b int);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into mytable values (1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)    
    
    stmt = """grant select on  mytable to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """ grant execute on function myudf to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ create view myview1 as select myudf(a) from mytable;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ create view myview2 as select * from myview1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    
    stmt = """ drop function myudf restrict;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ select * from myview1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,1)
    
    stmt = """ select * from myview2;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,1)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ drop function myudf cascade;"""
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from myview1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ select * from myview2;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_error_msg(output, '4481')

    stmt = """ drop table mytable cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """ drop function myudf cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop library sec_udflib1 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """revoke COMPONENT privilege create_view on sql_operations from qauser11;"""
    output = _dci.cmdexec(stmt) 
    
    _testmgr.testcase_end(desc)    
    

def testa19(desc="""db_root grant execute to none user"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return    
      
    stmt = """ set schema SECURITY_UDF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table mytable (a int, b int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into mytable values (1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,1)  
    
    stmt = """create library """+ defs.sec_udflib1 +""" file '"""+ defs.spjpath +"""';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ create function myudf (INVAL int)
                returns (OUTVAL int)
                language c
                parameter style sql
                external name 'myudf'
                library sec_udflib1
                deterministic
                state area size 1024
                allow any parallelism
                no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)   
    
    stmt = """select myudf(a) from mytable ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output,1) 
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """select myudf(a) from mytable ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
    mydci.expect_error_msg(output, '4482') 
    
    stmt = """ set schema SECURITY_UDF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """ drop table mytable cascade;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """ drop function myudf ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ drop library sec_udflib1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)    
    
def testa20(desc="""db_root grant execute to  user1, verify privilege"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return    
      
    stmt = """ set schema SECURITY_UDF;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table mytable (a int, b int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into mytable values (1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,1)  
    
    stmt = """create library """+ defs.sec_udflib1 +""" file '"""+ defs.spjpath +"""';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ create function myudf (INVAL int)
                returns (OUTVAL int)
                language c
                parameter style sql
                external name 'myudf'
                library sec_udflib1
                deterministic
                state area size 1024
                allow any parallelism
                no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)   
    
    stmt = """ grant execute on function myudf to qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ grant select on mytable to qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select myudf(a) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output,1) 
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """select myudf(a) from mytable;;"""
    output = mydci.cmdexec(stmt)
    _dci.expect_selected_msg(output,1) 
    
    mydci = basic_defs.switch_session_qi_user4()
    
    stmt = """ set schema SECURITY_UDF;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """select myudf(a) from mytable;;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    mydci.expect_error_msg(output, '4482')
    
    stmt = """ set schema SECURITY_UDF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """ drop table mytable cascade;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """ drop function myudf ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ drop library sec_udflib1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)  
    
def testa21(desc="""other user grant execute to none user"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return    
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ create schema security_udf1;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ set schema SECURITY_UDF1;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """create table mytable (a int, b int);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into mytable values (1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)  

    stmt = """ drop library sec_udflib1 cascade;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """create library sec_udflib1 file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ create function myudf (INVAL int)
                returns (OUTVAL int)
                language c
                parameter style sql
                external name 'myudf'
                library sec_udflib1
                deterministic
                state area size 1024
                allow any parallelism
                no sql;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)   
    
    stmt = """select myudf(a) from mytable;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1) 
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """ set schema SECURITY_UDF1;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """select myudf(a) from mytable;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4482') 
    
    stmt = """ set schema SECURITY_UDF1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """ drop table mytable cascade;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """ drop function myudf ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ drop library sec_udflib1 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ drop schema security_udf1 cascade;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)     
    
def testa22(desc="""other user grant execute to db_root"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return    
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ create schema security_udf1;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ set schema SECURITY_UDF1;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """create table mytable (a int, b int);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into mytable values (1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)  
    
    stmt = """create library sec_udflib1 file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ create function myudf (INVAL int)
                returns (OUTVAL int)
                language c
                parameter style sql
                external name 'myudf'
                library sec_udflib1
                deterministic
                state area size 1024
                allow any parallelism
                no sql;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)   
    
    stmt = """ grant execute on function myudf to db__root;"""
    output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    mydci.expect_error_msg(output, '1223')
    
    stmt = """select myudf(a) from mytable;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1) 
    
    stmt = """ set schema SECURITY_UDF1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select myudf(a) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output,1)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """ set schema SECURITY_UDF1;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """select myudf(a) from mytable;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4482')
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ set schema SECURITY_UDF1;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ drop table mytable cascade;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ drop function myudf ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop library sec_udflib1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """ drop schema security_udf1 cascade;"""
    output = mydci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)      
    
def testa23(desc="""other user1  grant execute to  user2, verify privilege"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return    
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ create schema security_udf1;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ set schema SECURITY_UDF1;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """create table mytable (a int, b int);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into mytable values (1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)  
    
    stmt = """create library sec_udflib1  file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ create function myudf (INVAL int)
                returns (OUTVAL int)
                language c
                parameter style sql
                external name 'myudf'
                library sec_udflib1
                deterministic
                state area size 1024
                allow any parallelism
                no sql;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)   
    
    stmt = """ grant execute on function myudf to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """ grant select on mytable to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """select myudf(a) from mytable;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1) 
    
    
    stmt = """ set schema SECURITY_UDF1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select myudf(a) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output,1)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """ set schema SECURITY_UDF1;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """select myudf(a) from mytable;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)
    
    mydci = basic_defs.switch_session_qi_user4()
    
    stmt = """ set schema SECURITY_UDF1;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """select myudf(a) from mytable;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    mydci.expect_error_msg(output, '4482')
    
    mydci = basic_defs.switch_session_qi_user4()
    
    stmt = """ set schema SECURITY_UDF1;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ drop  function myudf;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """ set schema SECURITY_UDF1;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ drop  function myudf;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ set schema SECURITY_UDF1;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ drop table mytable cascade;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ drop function myudf ;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ drop library sec_udflib1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """ drop schema security_udf1 cascade;"""
    output = mydci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)
    
def testa24(desc="""the view and UDF are defined in different schemas"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return  
    
    stmt = """ set schema SECURITY_UDF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create library """+ defs.sec_udflib1 +""" file '"""+ defs.spjpath +"""';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ create function myudf (INVAL int)
                returns (OUTVAL int)
                language c
                parameter style sql
                external name 'myudf'
                library sec_udflib1
                deterministic
                state area size 1024
                allow any parallelism
                no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)            

    stmt = """create table mytable (a int, b int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into mytable values (1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,1)  
    
    stmt = """ grant select on mytable to qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #CREATE VIEW should only work if the user has EXECUTE privilege on the UDF. 
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """ create schema security_udf2;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ set schema SECURITY_UDF2;"""
    output = mydci.cmdexec(stmt)    
    
    stmt = """ create view myview as select security_udf.myudf(a) from security_udf.mytable;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4482')  

    stmt = """ set schema SECURITY_UDF;"""
    output = _dci.cmdexec(stmt) 

    stmt = """ grant execute on function myudf to qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """ set schema SECURITY_UDF2;"""
    output = mydci.cmdexec(stmt)    
    
    stmt = """ create view myview as select security_udf.myudf(a) from security_udf.mytable;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)   
    
    stmt = """ select * from myview;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)
    
    mydci = basic_defs.switch_session_qi_user4()
    
    stmt = """ set schema SECURITY_UDF2;"""
    output = mydci.cmdexec(stmt)    
    
    stmt = """ create view myview as select security_udf.myudf(a) from security_udf.mytable;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    mydci.expect_error_msg(output, '4482')
    
    stmt = """ set schema SECURITY_UDF;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """ drop function myudf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1047')
    
    stmt = """drop function myudf cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """ set schema SECURITY_UDF2;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ select * from myview;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')
    
    stmt = """ drop schema SECURITY_UDF2 cascade;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ set schema SECURITY_UDF;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """ drop table mytable cascade;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """ drop function myudf;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """ drop library sec_udflib1 cascade;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)
    
def testa25(desc="""the view and UDF are defined in different schemas_2"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return  
    
    stmt = """ set schema SECURITY_UDF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create library """+ defs.sec_udflib1 +""" file '"""+ defs.spjpath +"""';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ create function myudf (INVAL int)
                returns (OUTVAL int)
                language c
                parameter style sql
                external name 'myudf'
                library sec_udflib1
                deterministic
                state area size 1024
                allow any parallelism
                no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)            

    stmt = """create table mytable (a int, b int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into mytable values (1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,1)  
    
    stmt = """ grant select on mytable to qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #CREATE VIEW should only work if the user has EXECUTE privilege on the UDF. 
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """ create shared schema security_udf2;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ set schema SECURITY_UDF2;"""
    output = mydci.cmdexec(stmt)    
    
    stmt = """ create view myview as select security_udf.myudf(a) from security_udf.mytable;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4482')  

    stmt = """ set schema SECURITY_UDF;"""
    output = _dci.cmdexec(stmt) 

    stmt = """ grant execute on function myudf to qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """ set schema SECURITY_UDF2;"""
    output = mydci.cmdexec(stmt)    
    
    stmt = """ create view myview as select security_udf.myudf(a) from security_udf.mytable;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)   
    
    stmt = """ select * from myview;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)
    
    mydci = basic_defs.switch_session_qi_user4()
    
    stmt = """ set schema SECURITY_UDF2;"""
    output = mydci.cmdexec(stmt)    
    
    stmt = """ create view myview as select security_udf.myudf(a) from security_udf.mytable;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ set schema SECURITY_UDF;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """ drop function myudf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1047')
    
    stmt = """drop function myudf cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """ set schema SECURITY_UDF2;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ select * from myview;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')
    
    stmt = """ drop schema SECURITY_UDF2 cascade;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """ set schema SECURITY_UDF;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """ drop table mytable cascade;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """ drop function myudf;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """ drop library sec_udflib1 cascade;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)     


def testa26(desc="""drop schema cascade after create UDF"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return    

    stmt = """GRANT COMPONENT privilege create_view on sql_operations to qauser11;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """ create schema SECURITY_UDF2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """ set schema SECURITY_UDF2;"""
    output = _dci.cmdexec(stmt)

    stmt = """create library sec_udflib1 file '"""+ defs.spjpath +"""';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ create function myudf (INVAL int)
                returns (OUTVAL int)
                language c
                parameter style sql
                external name 'myudf'
                library sec_udflib1
                deterministic
                state area size 1024
                allow any parallelism
                no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)            

    stmt = """create table mytable (a int, b int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into mytable values (1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,1)

    stmt = """grant select on  mytable to qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    
    stmt = """ grant execute on function myudf to qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """ set schema SECURITY_UDF2;"""
    output = mydci.cmdexec(stmt)    
    
    stmt = """ create view myview as select myudf(a) from mytable;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from myview;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,1) 
      

    stmt = """ drop schema SECURITY_UDF2 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """revoke COMPONENT privilege create_view on sql_operations from qauser11;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)    

