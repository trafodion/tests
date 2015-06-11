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
 
def testa01(desc="""dbroot create referenced and referencing tables with RI constraints"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """create shared schema prv_schema1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set schema prv_schema1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table prv1_table1( a int not null primary key, b int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #table column list is different
    stmt = """create table prv1_table2(c int, d int, f varchar(10), constraint cons1 foreign key(c) references prv1_table1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Referenced and referencing column lists do not match
    stmt = """create table prv1_table3(c int, d int, f varchar(10), constraint cons1 foreign key(f) references prv1_table1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1046')
    
    #other tables create same constraint
    stmt = """create table prv1_table4(c int, d int,constraint cons1 foreign key(c) references prv1_table1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    
    # column list is same
    stmt = """create table prv1_table4(c int, d int,constraint cons2 foreign key(c) references prv1_table1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #foreign keys that is more than one column
    stmt = """create table prv1_table5(c int, d int,f int, constraint cons3 foreign key (c) references prv1_table1, constraint cons4 foreign key(d) references prv1_table1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table prv1_table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1059')
    
    stmt = """drop table prv1_table2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table prv1_table4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table prv1_table5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop schema prv_schema1 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    
def testa02(desc="""dbrootrole create referenced and referencing tables with RI constraints"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
     
    stmt = """grant role db__rootrole to qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """create shared schema prv_schema2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """set schema prv_schema2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table prv2_table1( a int not null primary key, b int);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table prv2_table2(c int, d int, f varchar(10), constraint cons1 foreign key(c) references prv2_table1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table prv2_table3(c int, d int, f varchar(10), constraint cons1 foreign key(f) references prv2_table1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1046')

    stmt = """create table prv2_table4(c int, d int,constraint cons1 foreign key(c) references prv2_table1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '8102')
    
    stmt = """create table prv2_table4(c int, d int,constraint cons2 foreign key(c) references prv2_table1);"""
    output = mydci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table prv2_table5(c int, d int,f int, constraint cons3 foreign key (c) references prv2_table1, constraint cons4 foreign key(d) references prv2_table1);"""
    output = mydci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table prv2_table1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1059')
    
    stmt = """drop table prv2_table2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop table prv2_table4;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop table prv2_table5;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop table prv2_table1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop schema prv_schema2 cascade ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """revoke role db__rootrole from qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    
    _testmgr.testcase_end(desc)
    
def testa03(desc="""user1 create referenced tab, user2/role2 create referencing table with/with out references/all privileges"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return   
       
    stmt = """create role prv3_role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ grant role prv3_role2 to qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """grant component privilege "CREATE" on SQL_OPERATIONS to qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """grant component privilege "DROP" on SQL_OPERATIONS to qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """create shared schema prv_schema3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """set schema prv_schema3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table prv3_table1 (a int not null primary key, b int);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table prv3_table2 (c int, b int not null, constraint fk2 foreign key (b) references prv3_table1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop table prv3_table2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema prv_schema3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table prv3_table3 (c int, b int not null, constraint fk3 foreign key (b) references prv3_table1) no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')  

    stmt = """set schema prv_schema3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table prv3_table4(c int, b int not null, constraint fk4 foreign key (b) references prv3_table1) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table prv3_table4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema prv_schema3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """grant REFERENCES on prv3_table1 to prv3_role2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema prv_schema3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table prv3_table5 (c int, b int not null, constraint fk5 foreign key (b) references prv3_table1) no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema prv_schema3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """REVOKE REFERENCES on prv3_table1 from qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """REVOKE REFERENCES on prv3_table1 from prv3_role2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1025') 

    mydci = basic_defs.switch_session_qi_user3()

    stmt = """set schema prv_schema3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop table prv3_table5;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema prv_schema3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """REVOKE REFERENCES on prv3_table1 from qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 
    
    stmt = """REVOKE REFERENCES on prv3_table1 from prv3_role2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user3()

    stmt = """set schema prv_schema3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table prv3_table6 (c int, b int not null, constraint fk6 foreign key (b) references prv3_table1) no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema prv_schema3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """grant ALL on prv3_table1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user3()

    stmt = """set schema prv_schema3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table prv3_table6 (c int, b int not null, constraint fk6 foreign key (b) references prv3_table1) no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema prv_schema3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """revoke ALL on prv3_table1 from qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1025')

    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema prv_schema3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt= """drop table prv3_table6;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema prv_schema3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """revoke ALL on prv3_table1 from qauser11;"""
    output = mydci.cmdexec(stmt)  
    mydci.expect_complete_msg(output)
    
    stmt = """drop schema prv_schema3 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """revoke component privilege "DROP" on SQL_OPERATIONS from qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke component privilege "CREATE" on SQL_OPERATIONS from qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ revoke role prv3_role2 from qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop role prv3_role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    
    
def testa04(desc="""user has create_table component privilege create RI constraints"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return   
     
    stmt = """revoke component privilege "CREATE" on SQL_OPERATIONS from qauser10;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """grant component privilege "CREATE_TABLE" on SQL_OPERATIONS to qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ create shared schema prv_schema4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ set schema prv_schema4;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table prv4_table1( a int not null primary key, b int);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table prv4_table2(c int, d int, f varchar(10), constraint cons1 foreign key(c));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001') 

    stmt = """create table prv4_table2(c int, d int, f varchar(10), constraint cons1 foreign key(c) references prv4_table1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    #Referenced and referencing column lists do not match
    stmt = """create table prv4_table3(c int, d int, f varchar(10), constraint cons1 foreign key(f) references prv4_table1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1046')
    
    #other tables create same constraint
    stmt = """create table prv4_table4(c int, d int,constraint cons1 foreign key(c) references prv4_table1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '8102')
    
    # column list is same
    stmt = """create table prv4_table4(c int, d int,constraint cons2 foreign key(c) references prv4_table1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    #foreign keys that is more than one column
    stmt = """create table prv4_table5(c int, d int,f int, constraint cons3 foreign key (c) references prv4_table1, constraint cons4 foreign key(d) references prv4_table1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """revoke component privilege "CREATE_TABLE" on SQL_OPERATIONS from qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ set schema prv_schema4;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table prv4_table6(c int, d int, f varchar(10), constraint cons6 foreign key(c) references prv4_table1);"""
    output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '4481') 
    mydci.expect_complete_msg(output)
    
    stmt = """ drop table prv4_table1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1059')
    
    stmt = """ drop table prv4_table2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop table prv4_table4;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop table prv4_table5;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop schema prv_schema4 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """revoke component privilege "CREATE" on SQL_OPERATIONS from qauser10;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)
    
    
def testa05(desc="""role has create_table component privilege create RI constraints"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return   
    
    stmt = """ create role prv5_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ grant role prv5_role1 to qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """grant component privilege "CREATE_TABLE" on SQL_OPERATIONS to prv5_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ create shared schema prv_schema5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ set schema prv_schema5;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table prv5_table1( a int not null primary key, b int);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table prv5_table2(c int, d int, f varchar(10), constraint cons1 foreign key(c));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001') 

    stmt = """create table prv5_table2(c int, d int, f varchar(10), constraint cons1 foreign key(c) references prv5_table1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    #Referenced and referencing column lists do not match
    stmt = """create table prv5_table3(c int, d int, f varchar(10), constraint cons1 foreign key(f) references prv5_table1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1046')
    
    #other tables create same constraint
    stmt = """create table prv5_table4(c int, d int,constraint cons1 foreign key(c) references prv5_table1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '8102')
    
    # column list is same
    stmt = """create table prv5_table4(c int, d int,constraint cons2 foreign key(c) references prv5_table1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    #foreign keys that is more than one column
    stmt = """create table prv5_table5(c int, d int,f int, constraint cons3 foreign key (c) references prv5_table1, constraint cons4 foreign key(d) references prv5_table1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """revoke component privilege "CREATE_TABLE" on SQL_OPERATIONS from prv5_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ set schema prv_schema5;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table prv5_table6(c int, d int, f varchar(10), constraint cons6 foreign key(c) references prv5_table1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop table prv5_table1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1059')
    
    stmt = """ drop table prv5_table2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop table prv5_table4;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop table prv5_table5;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop table prv5_table6;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop table prv5_table1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop schema prv_schema5 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ revoke role prv5_role1 from qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ drop role prv5_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    
    _testmgr.testcase_end(desc)
     
def testa06(desc="""verify privileges on referenced and referencing tables"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return   
      
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """create shared schema prv_schema6;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """set schema prv_schema6;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table prv6_table1( a int not null primary key, b int);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table prv6_table2(c int, d int,constraint cons2 foreign key(c) references prv6_table1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table prv6_table3(c int, d int,f int,constraint cons3 foreign key(c) references prv6_table1, constraint cons4 foreign key(f) references prv6_table1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    
    stmt = """insert into prv6_table1 values (7,8);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt = """insert into prv6_table2 values(1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '8103')
    
    stmt = """insert into prv6_table3 values(1,2,3);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '8103')
    
    stmt = """insert into prv6_table2 values(7,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt = """insert into prv6_table3 values(7,1,2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '8103')
    
    stmt = """insert into prv6_table3 values(2,1,7);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '8103')
    
    stmt = """insert into prv6_table3 values(7,1,7);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt = """drop table prv6_table1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1059')
    
    stmt = """drop table prv6_table2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop table prv6_table3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop table prv6_table1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop schema prv_schema6;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)    
    
     


    
def testa07(desc="""db_root create/alter/use sequence generator"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return   
       
    stmt = """create shared schema prv_schema7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set schema prv_schema7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table prv7_table1( a int not null primary key, b int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
    
    stmt = """ insert into prv7_table1 values (1,1), (2,2),(3,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,3) 
    
    stmt = """CREATE TABLE prv7_table2 (z int not null primary key, a int not null, b int not null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  
    
    stmt ="""CREATE SEQUENCE seq1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE SEQUENCE seq2 maxvalue 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SELECT * from prv7_table1 where a < seqnum(seq2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output,0)
    
    stmt = """insert into prv7_table2 select seqnum(seq2),a, b from prv7_table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1579')
    
    stmt = """SELECT * from prv7_table1 where a < seqnum(seq2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1579')
    
    stmt = """insert into prv7_table2 select seqnum(seq2) from prv7_table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4023')
    
    stmt = """ insert into prv7_table1 values (1,1), (2,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    
    stmt = """SELECT * from prv7_table1 where a < seqnum(seq1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output,0)
    
    stmt = """alter SEQUENCE seq2 no maxvalue;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SELECT * from prv7_table1 where a < seqnum(seq1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output,1)
    
    stmt = """SELECT * from prv7_table1 where a < seqnum(seq2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output,2)
    
    stmt = """SELECT * from prv7_table1 where a < seqnum(seq2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output,3)
    
    stmt = """SELECT * from prv7_table1 where a < seqnum(seq2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output,3)
    
    stmt = """SELECT * from prv7_table1 where a < seqnum(seq2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output,3)
    
    stmt = """SELECT * from prv7_table1 where a < seqnum(seq1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output,3)
    
    stmt = """ drop sequence seq1; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """ drop sequence seq2; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """SELECT * from prv7_table1 where a < seqnum(seq1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1389')
    
    stmt = """ drop table prv7_table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ drop table prv7_table2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop schema prv_schema7 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    
def testa08(desc="""the owner of sequence create/alter/use sequence generator"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return   
    
    mydci = basic_defs.switch_session_qi_user2()
           
    stmt = """create shared schema prv_schema8;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """set schema prv_schema8;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table prv8_table1( a int not null primary key, b int);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt = """CREATE TABLE prv8_table2 (z int not null primary key, a int not null, b int not null);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 
    
    stmt = """ create sequence seq1; """
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 
    
    stmt = """insert into prv8_table1 values(2,2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt = """insert into prv8_table1 values(seqnum(seq1), 1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt = """select * from prv8_table1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)
    
    stmt = """insert into prv8_table1 values(seqnum(seq1), 2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '8102')
    
    stmt = """insert into prv8_table1 values(seqnum(seq1), 4);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt = """insert into prv8_table1 values(3,seqnum(seq1));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '8102')

    stmt = """insert into prv8_table1 values(5,seqnum(seq1));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
   
    stmt = """select * from prv8_table1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_any_substr(output,'5           5' );
    mydci.expect_selected_msg(output,4)
    
    stmt = """insert into prv8_table2 values(3,seqnum(seq1), 9);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt = """select * from prv8_table2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_any_substr(output,'3           6           9' );
    mydci.expect_selected_msg(output,1)
    
    stmt = """insert into prv8_table2 values(seqnum(seq1),3, 9);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt = """select * from prv8_table2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_any_substr(output,'7           3           9' )
    mydci.expect_selected_msg(output,2)
    
    stmt = """insert into prv8_table2 values(3, 9, seqnum(seq1));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '8102')
    
    stmt = """insert into prv8_table2 values(3, 2, 4);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '8102')
    
    stmt = """alter sequence seq1 maxvalue 2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 
    
    stmt = """delete from prv8_table1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,4)
    
    stmt = """insert into prv8_table1 values( seqnum(seq1),seqnum(seq1));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt = """drop sequence seq1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop table prv8_table1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop table prv8_table2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop schema prv_schema8 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
        
    
def testa09(desc="""the role has pri create/alter/drop/use/ sequence"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return   
    
    stmt = """create shared schema prv_schema9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set schema prv_schema9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create role prv9_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """grant component privilege create_sequence on SQL_OPERATIONS to prv9_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """grant role prv9_role1 to qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """revoke component privilege "CREATE" on SQL_OPERATIONS from qauser10;"""
    output = _dci.cmdexec(stmt)
    
    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema prv_schema9;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table prv9_table1( a int not null primary key, b int);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt = """ insert into prv9_table1 values (1,1), (2,2),(3,3);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,3) 
    
    stmt = """CREATE TABLE prv9_table2 (z int not null primary key, a int not null, b int not null);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)  
    
    stmt ="""CREATE SEQUENCE seq1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """CREATE SEQUENCE seq2 maxvalue 3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """SELECT * from prv9_table1 where a < seqnum(seq2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt = """insert into prv9_table2 select seqnum(seq2),a, b from prv9_table1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1579')
    
    stmt = """SELECT * from prv9_table1 where a < seqnum(seq2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1579')
    
    stmt = """insert into prv9_table2 select seqnum(seq2) from prv9_table1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4023')
    
    stmt = """ insert into prv9_table1 values (1,1), (2,2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '8102')
    
    stmt = """SELECT * from prv9_table1 where a < seqnum(seq1);"""
    output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '1579')
    mydci.expect_selected_msg(output,0)
    
    stmt = """alter SEQUENCE seq2 no maxvalue;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """SELECT * from prv9_table1 where a < seqnum(seq1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)
    
    stmt = """SELECT * from prv9_table1 where a < seqnum(seq2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)
    
    stmt = """SELECT * from prv9_table1 where a < seqnum(seq2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,3)
    
    stmt = """SELECT * from prv9_table1 where a < seqnum(seq2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,3)
    
    stmt = """SELECT * from prv9_table1 where a < seqnum(seq2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,3)
    
    stmt = """SELECT * from prv9_table1 where a < seqnum(seq1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,3)
    
    stmt = """ drop sequence seq1; """
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 
    
    stmt = """ drop sequence seq2; """
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 
    
    stmt = """SELECT * from prv9_table1 where a < seqnum(seq1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1389')
    
    stmt = """ drop table prv9_table1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop table prv9_table2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """revoke component privilege create_sequence on SQL_OPERATIONS from prv9_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt ="""CREATE SEQUENCE seq1;"""
    output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '1389')
    mydci.expect_complete_msg(output)
    
    stmt = """revoke role prv9_role1 from qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """revoke component privilege "CREATE" on SQL_OPERATIONS from qauser10;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop schema prv_schema9 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt ="""drop SEQUENCE seq1;"""
    output = _dci.cmdexec(stmt)

    stmt ="""drop SEQUENCE prv_schema9.seq1;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop role prv9_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    
def testa10(desc="""usage: grant/revoke usage/all prv(n/p)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return   

    #stmt = """unregister user qauser11;"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_complete_msg(output)

    #stmt = """unregister user qauser12;"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_complete_msg(output)

    #stmt = """register user qauser11;"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_complete_msg(output)

    #stmt = """register user qauser12;"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_complete_msg(output)
    
    stmt = """create role prv10_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create role prv10_role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """grant role prv10_role1 to qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """grant role prv10_role2 to qauser12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create shared schema prv_schema10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set schema prv_schema10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table prv10_tab1 (a int, b int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create sequence seq11 maxvalue 3 cycle;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into prv10_tab1 values (seqnum(seq11), seqnum(seq11));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,1)
    
    stmt = """select * from prv10_tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output,1)

    stmt = """grant insert on prv10_tab1 to qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant select on prv10_tab1 to qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """grant all on prv10_tab1 to prv10_role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema prv_schema10;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """select * from prv10_tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)
    
    #-- should fail
    stmt = """insert into prv10_tab1 values (seqnum(seq11), seqnum(seq11));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4491')    
    
    mydci = basic_defs.switch_session_qi_user4()
    
    stmt = """set schema prv_schema10;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """select * from prv10_tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)
    
    stmt = """insert into prv10_tab1 values (seqnum(seq11), seqnum(seq11));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4491') 
    
    stmt = """set schema prv_schema10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """grant USAGE on sequence seq11 to prv10_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """grant USAGE on sequence seq11 to qauser12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema prv_schema10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from prv10_tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)
    
    stmt = """insert into prv10_tab1 values (seqnum(seq11), seqnum(seq11));"""
    output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '4491') 
    mydci.expect_inserted_msg(output,1)
    
    mydci = basic_defs.switch_session_qi_user4()
    
    stmt = """set schema prv_schema10;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """select * from prv10_tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)
    
    stmt = """insert into prv10_tab1 values (seqnum(seq11), seqnum(seq11));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    #    -- should fail"""
    stmt = """create sequence seq13 maxvalue 3 cycle; """
    output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '4481')
    mydci.expect_complete_msg(output) 

    #-- should fail
    stmt = """insert into prv10_tab1 values (seqnum(seq13), seqnum(seq13)); """
    output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '4481')
    mydci.expect_inserted_msg(output,1)

    stmt = """set schema prv_schema10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """grant component privilege "CREATE" on SQL_OPERATIONS to prv10_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """grant component privilege CREATE_SEQUENCE on SQL_OPERATIONS to qauser12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema prv_schema10;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create sequence seq12 maxvalue 3 cycle;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user4()
    
    stmt = """set schema prv_schema10;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create sequence seq14 maxvalue 3 cycle;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    # -- should fail
    stmt = """drop sequence seq12;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    #-- should fail
    stmt = """alter sequence seq12 maxvalue 4;""" 
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    #-- should fail
    stmt = """insert into prv10_tab1 values (seqnum(seq12), seqnum(seq12)); """
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4491') 
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema prv_schema10;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    # -- should fail
    stmt = """drop sequence seq13;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    ## -- should fail
    stmt = """alter sequence seq13 maxvalue 4; """
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    ## -- should fail
    stmt = """insert into prv10_tab1 values (seqnum(seq13), seqnum(seq13)); """
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4491')

    stmt = """set schema prv_schema10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """grant component privilege "DROP" on SQL_OPERATIONS to qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """grant component privilege DROP_SEQUENCE on SQL_OPERATIONS to prv10_role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """grant component privilege "ALTER" on SQL_OPERATIONS to qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """grant component privilege ALTER_SEQUENCE on SQL_OPERATIONS to prv10_role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema prv_schema10;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """grant ALL on sequence seq12 to prv10_role2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user4()
    
    stmt = """set schema prv_schema10;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """grant USAGE on sequence seq13 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into prv10_tab1 values (seqnum(seq12), seqnum(seq12));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt = """alter sequence seq12 maxvalue 4;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop sequence seq12;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop sequence seq14;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema prv_schema10;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into prv10_tab1 values (seqnum(seq13), seqnum(seq13));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt = """alter sequence seq13 maxvalue 4;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop sequence seq13;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop sequence seq11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """revoke component privilege "DROP" on SQL_OPERATIONS from qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """revoke component privilege DROP_SEQUENCE on SQL_OPERATIONS from prv10_role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """revoke component privilege "ALTER" on SQL_OPERATIONS from qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """revoke component privilege ALTER_SEQUENCE on SQL_OPERATIONS from prv10_role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke component privilege "CREATE" on SQL_OPERATIONS from prv10_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """revoke component privilege CREATE_SEQUENCE on SQL_OPERATIONS from qauser12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop schema prv_schema10 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """revoke role prv10_role1 from qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """revoke role prv10_role2 from qauser12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop role prv10_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop role prv10_role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
 
    
    _testmgr.testcase_end(desc)
    
    
def testa11(desc="""usage: create table with idetity column, veriry privilege"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return   
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """create shared schema prv_schema11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """set schema prv_schema11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table prv11_table1( a int not null primary key, INDENTITY int);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
    
    stmt = """ insert into prv11_table1 values (1,1), (2,2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,2)
    
    stmt = """CREATE TABLE prv11_table2 (z int not null primary key, a int not null, INDENTITY int not null);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)  
   
    stmt = """ create sequence seq1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into prv11_table2 values(3,4,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt = """insert into prv11_table2 values(3,4,1);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_error_msg(output, '8102')
    
    stmt = """ insert into prv11_table1 values(1, INDENTITY);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_error_msg(output, '4001')
    
    stmt = """ insert into prv11_table1 values(1,seqnum(seq1));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '8102')
    
    stmt = """ insert into prv11_table1 values(seqnum(seq1),3);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '8102')
    
    stmt = """select * from prv11_table1;"""
    output = mydci.cmdexec(stmt)
    _dci.expect_any_substr(output,'2           2' );
    
    stmt = """insert into prv11_table2 values(4,5,5);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt = """insert into prv11_table2 values(seqnum(seq1),5,5);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '8102')
    
    stmt = """insert into prv11_table2 values(seqnum(seq1),6,7);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '8102')
    
    stmt = """ select * from prv11_table1 where indentity < seqnum(seq1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2)
    
    stmt = """ grant all on table prv11_table1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()

    stmt = """set schema prv_schema11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into prv11_table2 values(6,7,9);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
    
    stmt = """insert into prv11_table2 values(seqnum(seq1),8,9);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
    
    stmt = """insert into prv11_table2 values(seqnum(seq1),8,9);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
    
    stmt = """drop sequence seq1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """drop sequence seq1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ revoke all on table prv11_table1 from qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop table prv11_table2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop table prv11_table1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop schema prv_schema11 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)    
    
  