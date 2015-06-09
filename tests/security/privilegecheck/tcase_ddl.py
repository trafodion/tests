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
 

def testa12(desc="""privilege checks for DDL operations: db__root"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """create shared schema ddl_schema1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set schema ddl_schema1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ddl1_table1( a int not null primary key, b int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ddl1_table2(c int, d int, f varchar(10), constraint cons1 foreign key(c) references ddl1_table1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ddl1_table3(a int, b int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table1 add column c int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table1 add constraint cons2 check(a>0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table1 add constraint cons3 unique(b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table2 add constraint cons4 foreign key(d) references ddl1_table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table2 add constraint cons5 primary key(c);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table1 drop constraint cons2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table3 drop column b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index ddl1_index1 on ddl1_table3(a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table3 disable index ddl1_index1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table3 enable index ddl1_index1;""";
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table3 rename to ddl1_table3_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ drop index ddl1_index1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view ddl1_view1 as select * from ddl1_table3_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop view ddl1_view1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table ddl1_table3_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table ddl1_table2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table ddl1_table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create role ddl1_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop role ddl1_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ alter user qauser11 set online;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    stmt = """register component ddl1_comp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create component privilege aa as 'sa' on ddl1_comp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop component privilege aa on ddl1_comp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ unregister component ddl1_comp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE SEQUENCE seq1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop SEQUENCE seq1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop schema ddl_schema1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def testa13(desc="""privilege checks for DDL operation alter table: table owner"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """create shared schema ddl_sch13;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """set schema ddl_sch13;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table ddl1_table1( a int not null primary key, b int);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table ddl1_table2(c int, d int, f varchar(10), constraint cons1 foreign key(c) references ddl1_table1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table ddl1_table3(a int, b int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table1 add column c int;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table1 add constraint cons2 check(a>0);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table1 add constraint cons3 unique(b);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table2 add constraint cons4 foreign key(d) references ddl1_table1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table2 add constraint cons5 primary key(c);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table1 drop constraint cons2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table3 drop column b;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create index ddl1_index1 on ddl1_table3(a);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """alter table ddl1_table3 disable index ddl1_index1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table3 enable index ddl1_index1;""";
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table3 rename to ddl1_table3_1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop index ddl1_index1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create view ddl1_view1 as select * from ddl1_table3_1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop view ddl1_view1 ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop table ddl1_table3_1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop table ddl1_table2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop table ddl1_table1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop schema ddl_sch13 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def testa14(desc="""privilege checks for DDL other user alter table on private schema: alter component privilege"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return


    stmt = """create schema ddl_sch14;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set schema ddl_sch14;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ddl1_table1( a int not null primary key, b int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ddl1_table2(c int, d int, f varchar(10), constraint cons1 foreign key(c) references ddl1_table1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ddl1_table3(a int, b int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema ddl_sch14;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """alter table ddl1_table1 add column c int;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    stmt = """alter table ddl1_table1 add constraint cons2 check(a>0);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    stmt = """alter table ddl1_table1 add constraint cons3 unique(b);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    stmt = """alter table ddl1_table2 add constraint cons4 foreign key(d) references ddl1_table1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    stmt = """alter table ddl1_table2 add constraint cons5 primary key(c);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    stmt = """alter table ddl1_table1 drop constraint cons2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    stmt = """alter table ddl1_table3 drop column b;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 

    stmt = """ grant component privilege "ALTER" on SQL_OPERATIONS to qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """set schema ddl_sch14;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ grant references on  ddl1_table1 to qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema ddl_sch14;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table1 add column c int;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table1 add constraint cons2 check(a>0);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table1 add constraint cons3 unique(b);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table2 add constraint cons4 foreign key(d) references ddl1_table1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table2 add constraint cons5 primary key(c);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table1 drop constraint cons2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table3 drop column b;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema ddl_sch14;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop view ddl1_view1 ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table ddl1_table3_1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table ddl1_table2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table ddl1_table1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop schema ddl_sch14 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ revoke component privilege "ALTER" on SQL_OPERATIONS from qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)


def testa15(desc="""privilege checks for DDL other user alter table on shared schema: user has alter component privilege"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return


    stmt = """create shared schema ddl_sch15;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set schema ddl_sch15;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ddl1_table1( a int not null primary key, b int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ddl1_table2(c int, d int, f varchar(10), constraint cons1 foreign key(c) references ddl1_table1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ddl1_table3(a int, b int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema ddl_sch15;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """alter table ddl1_table1 add column c int;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    stmt = """alter table ddl1_table1 add constraint cons2 check(a>0);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    stmt = """alter table ddl1_table1 add constraint cons3 unique(b);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    stmt = """alter table ddl1_table2 add constraint cons4 foreign key(d) references ddl1_table1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    stmt = """alter table ddl1_table2 add constraint cons5 primary key(c);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    stmt = """alter table ddl1_table1 drop constraint cons2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    stmt = """alter table ddl1_table3 drop column b;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 

    stmt = """ grant component privilege "ALTER" on SQL_OPERATIONS to qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """set schema ddl_sch15;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ grant references on  ddl1_table1 to qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema ddl_sch15;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table1 add column c int;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table1 add constraint cons2 check(a>0);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table1 add constraint cons3 unique(b);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table2 add constraint cons4 foreign key(d) references ddl1_table1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table2 add constraint cons5 primary key(c);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table1 drop constraint cons2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table3 drop column b;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema ddl_sch15;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop view ddl1_view1 ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table ddl1_table3_1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table ddl1_table2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table ddl1_table1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop schema ddl_sch15 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ revoke component privilege "ALTER" on SQL_OPERATIONS from qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)


def testa16(desc="""privilege checks for DDL other user alter table on shared schema: user has alter component privilege"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return


    stmt = """create shared schema ddl_sch16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set schema ddl_sch16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ddl1_table1( a int not null primary key, b int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ddl1_table2(c int, d int, f varchar(10), constraint cons1 foreign key(c) references ddl1_table1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ddl1_table3(a int, b int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema ddl_sch16;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """alter table ddl1_table1 add column c int;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    stmt = """alter table ddl1_table1 add constraint cons2 check(a>0);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    stmt = """alter table ddl1_table1 add constraint cons3 unique(b);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    stmt = """alter table ddl1_table2 add constraint cons4 foreign key(d) references ddl1_table1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    stmt = """alter table ddl1_table2 add constraint cons5 primary key(c);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    stmt = """alter table ddl1_table1 drop constraint cons2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    stmt = """alter table ddl1_table3 drop column b;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 

    stmt = """ grant component privilege "ALTER_TABLE" on SQL_OPERATIONS to qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """set schema ddl_sch16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ grant references on  ddl1_table1 to qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema ddl_sch16;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table1 add column c int;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table1 add constraint cons2 check(a>0);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table1 add constraint cons3 unique(b);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table2 add constraint cons4 foreign key(d) references ddl1_table1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table2 add constraint cons5 primary key(c);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table1 drop constraint cons2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table3 drop column b;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema ddl_sch16;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop view ddl1_view1 ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table ddl1_table3_1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table ddl1_table2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table ddl1_table1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop schema ddl_sch16 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ revoke component privilege "ALTER_TABLE" on SQL_OPERATIONS from qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)


def testa17(desc="""privilege checks for DDL other user alter table on private schema: user has alter component privilege"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return


    stmt = """create schema ddl_sch17;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set schema ddl_sch17;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ddl1_table1( a int not null primary key, b int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ddl1_table2(c int, d int, f varchar(10), constraint cons1 foreign key(c) references ddl1_table1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ddl1_table3(a int, b int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema ddl_sch17;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """alter table ddl1_table1 add column c int;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    stmt = """alter table ddl1_table1 add constraint cons2 check(a>0);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    stmt = """alter table ddl1_table1 add constraint cons3 unique(b);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    stmt = """alter table ddl1_table2 add constraint cons4 foreign key(d) references ddl1_table1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    stmt = """alter table ddl1_table2 add constraint cons5 primary key(c);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    stmt = """alter table ddl1_table1 drop constraint cons2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    stmt = """alter table ddl1_table3 drop column b;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 

    stmt = """ grant component privilege "ALTER_TABLE" on SQL_OPERATIONS to qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """set schema ddl_sch17;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ grant references on  ddl1_table1 to qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema ddl_sch17;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table1 add column c int;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table1 add constraint cons2 check(a>0);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table1 add constraint cons3 unique(b);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table2 add constraint cons4 foreign key(d) references ddl1_table1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table2 add constraint cons5 primary key(c);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table1 drop constraint cons2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table3 drop column b;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema ddl_sch17;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop table ddl1_table2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table ddl1_table1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop schema ddl_sch17 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ revoke component privilege "ALTER_TABLE" on SQL_OPERATIONS from qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def testa18(desc="""privilege checks for DDL operation alter table on shared schema:role has alter component privilege"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create role ddl_role18;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant role ddl_role18 to qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create shared schema ddl_sch18;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set schema ddl_sch18;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ddl1_table1( a int not null primary key, b int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ddl1_table2(c int, d int, f varchar(10), constraint cons1 foreign key(c) references ddl1_table1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ddl1_table3(a int, b int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema ddl_sch18;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """alter table ddl1_table1 add column c int;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    stmt = """alter table ddl1_table1 add constraint cons2 check(a>0);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    stmt = """alter table ddl1_table1 add constraint cons3 unique(b);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    stmt = """alter table ddl1_table2 add constraint cons4 foreign key(d) references ddl1_table1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    stmt = """alter table ddl1_table2 add constraint cons5 primary key(c);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    stmt = """alter table ddl1_table1 drop constraint cons2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    stmt = """alter table ddl1_table3 drop column b;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 

    stmt = """ grant component privilege "ALTER" on SQL_OPERATIONS to ddl_role18;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """set schema ddl_sch18;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ grant references on  ddl1_table1 to qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema ddl_sch18;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table1 add column c int;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table1 add constraint cons2 check(a>0);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table1 add constraint cons3 unique(b);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table2 add constraint cons4 foreign key(d) references ddl1_table1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table2 add constraint cons5 primary key(c);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table1 drop constraint cons2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table3 drop column b;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema ddl_sch18;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop table ddl1_table2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table ddl1_table1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop schema ddl_sch18 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ revoke component privilege "ALTER" on SQL_OPERATIONS from ddl_role18;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke role ddl_role18 from qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role ddl_role18;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def testa19(desc="""privilege checks for DDL operation alter table on private schema:role has alter component privilege"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create role ddl_role19;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant role ddl_role19 to qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create schema ddl_sch19;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set schema ddl_sch19;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ddl1_table1( a int not null primary key, b int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ddl1_table2(c int, d int, f varchar(10), constraint cons1 foreign key(c) references ddl1_table1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ddl1_table3(a int, b int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ grant component privilege "ALTER" on SQL_OPERATIONS to ddl_role19;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """set schema ddl_sch19;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ grant references on  ddl1_table1 to qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema ddl_sch19;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table1 add column c int;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table1 add constraint cons2 check(a>0);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table1 add constraint cons3 unique(b);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table2 add constraint cons4 foreign key(d) references ddl1_table1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table2 add constraint cons5 primary key(c);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table1 drop constraint cons2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table3 drop column b;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema ddl_sch19;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop table ddl1_table2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table ddl1_table1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop schema ddl_sch19 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ revoke component privilege "ALTER" on SQL_OPERATIONS from ddl_role19;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke role ddl_role19 from qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role ddl_role19;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def testa20(desc="""privilege checks for DDL operation alter table  on shared schema:  role has alter_table  privilege"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create role ddl_role20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant role ddl_role20 to qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create shared schema ddl_sch20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set schema ddl_sch20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ddl1_table1( a int not null primary key, b int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ddl1_table2(c int, d int, f varchar(10), constraint cons1 foreign key(c) references ddl1_table1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ddl1_table3(a int, b int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ grant component privilege "ALTER_TABLE" on SQL_OPERATIONS to ddl_role20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """set schema ddl_sch20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ grant references on  ddl1_table1 to qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema ddl_sch20;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table1 add column c int;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table1 add constraint cons2 check(a>0);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table1 add constraint cons3 unique(b);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table2 add constraint cons4 foreign key(d) references ddl1_table1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table2 add constraint cons5 primary key(c);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table1 drop constraint cons2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table3 drop column b;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema ddl_sch20;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop table ddl1_table2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table ddl1_table1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop schema ddl_sch20 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ revoke component privilege "ALTER_TABLE" on SQL_OPERATIONS from ddl_role20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke role ddl_role20 from qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role ddl_role20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def testa21(desc="""privilege checks for DDL operation alter table on private schema:  role has alter_table  privilege"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create role ddl_role21;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant role ddl_role21 to qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create schema ddl_sch21;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set schema ddl_sch21;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ddl1_table1( a int not null primary key, b int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ddl1_table2(c int, d int, f varchar(10), constraint cons1 foreign key(c) references ddl1_table1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ddl1_table3(a int, b int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ grant component privilege "ALTER_TABLE" on SQL_OPERATIONS to ddl_role21;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """set schema ddl_sch21;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ grant references on  ddl1_table1 to qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema ddl_sch21;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table1 add column c int;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table1 add constraint cons2 check(a>0);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table1 add constraint cons3 unique(b);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table2 add constraint cons4 foreign key(d) references ddl1_table1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table2 add constraint cons5 primary key(c);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table1 drop constraint cons2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl1_table3 drop column b;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema ddl_sch21;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop table ddl1_table2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table ddl1_table1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop schema ddl_sch21 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ revoke component privilege "ALTER_TABLE" on SQL_OPERATIONS from ddl_role21;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke role ddl_role21 from qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role ddl_role21;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def testa22(desc="""privilege checks for DDL operations: role has component privilege_1"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """create role ddl2_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant role ddl2_role1 to qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    #CREATE TABLE
    stmt = """create schema ddl2_schema2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set schema ddl2_schema2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ddl2_table11( a int not null primary key, b int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ddl2_table22(c int, d int, f varchar(10), constraint cons1 foreign key(c) references ddl2_table11);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ddl2_table33( a int not null primary key, b int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema ddl2_schema2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create view ddl2_view11 as select * from ddl2_table33;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
    
    stmt = """drop table ddl2_table22;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    stmt = """drop table ddl2_table11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    
    stmt = """ unregister user qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    stmt = """ register user qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')   
    
    stmt = """ alter user qauser11 set online;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')  
    
    stmt = """register component ddl1_comp1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')

    stmt = """create component privilege aa as 'sa' on ddl1_comp1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    stmt = """drop component privilege aa on ddl1_comp1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    stmt = """ unregister component ddl1_comp1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    stmt = """CREATE SEQUENCE seq1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    stmt = """drop SEQUENCE seq1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1389')
    
    stmt = """create role ddl2_role2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    stmt = """drop role ddl2_role2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1338') 
    
    stmt = """set schema ddl2_schema2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ grant component privilege "ALTER_TABLE" on SQL_OPERATIONS to ddl2_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ grant component privilege "MANAGE_USERS" on SQL_OPERATIONS to ddl2_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ grant component privilege "MANAGE_ROLES" on SQL_OPERATIONS to ddl2_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ grant component privilege "MANAGE_COMPONENTS" on SQL_OPERATIONS to ddl2_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ grant component privilege "CREATE_SEQUENCE" on SQL_OPERATIONS to ddl2_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ grant component privilege "DROP" on SQL_OPERATIONS to ddl2_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema ddl2_schema2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    
    stmt = """create index ddl2_index22 on ddl2_table33(a);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """alter table ddl2_table33 disable index ddl2_index22;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl2_table33 enable index ddl2_index22;""";
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
   
    
    stmt = """alter table ddl2_table33 rename to ddl2_table3_11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop index ddl2_index22;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop table ddl2_table3_11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop table ddl2_table22;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop table ddl2_table11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    
    stmt = """ alter user qauser11 set online;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 
    
    stmt = """register component ddl1_comp1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 

    stmt = """create component privilege aa as 'sa' on ddl1_comp1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 
    
    stmt = """drop component privilege aa on ddl1_comp1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 
    
    stmt = """ unregister component ddl1_comp1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 
    
    stmt = """CREATE SEQUENCE seq1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop SEQUENCE seq1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create role ddl2_role2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop role ddl2_role2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop schema ddl2_schema2 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ revoke component privilege "ALTER_TABLE" on SQL_OPERATIONS from ddl2_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ revoke component privilege "MANAGE_USERS" on SQL_OPERATIONS from ddl2_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ revoke component privilege "MANAGE_ROLES" on SQL_OPERATIONS from ddl2_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ revoke component privilege "MANAGE_COMPONENTS" on SQL_OPERATIONS from ddl2_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ revoke component privilege "CREATE_SEQUENCE" on SQL_OPERATIONS from ddl2_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ revoke component privilege "DROP" on SQL_OPERATIONS from ddl2_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke role ddl2_role1 from qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop role ddl2_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)    

   
def testa23(desc="""privilege checks for DDL operations: role has component privilege_2"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """create role ddl2_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant role ddl2_role1 to qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    #CREATE TABLE
    stmt = """create schema ddl2_schema2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set schema ddl2_schema2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ddl2_table11( a int not null primary key, b int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ddl2_table22(c int, d int, f varchar(10), constraint cons1 foreign key(c) references ddl2_table11);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ddl2_table33( a int not null primary key, b int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema ddl2_schema2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create view ddl2_view11 as select * from ddl2_table33;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
    
    stmt = """drop table ddl2_table22;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    stmt = """drop table ddl2_table11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    
    stmt = """ unregister user qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    stmt = """ register user qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')   
    
    stmt = """ alter user qauser11 set online;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')  
    
    stmt = """register component ddl1_comp1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')

    stmt = """create component privilege aa as 'sa' on ddl1_comp1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    stmt = """drop component privilege aa on ddl1_comp1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    stmt = """ unregister component ddl1_comp1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    stmt = """CREATE SEQUENCE seq1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    stmt = """drop SEQUENCE seq1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1389')
    
    stmt = """create role ddl2_role2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    stmt = """drop role ddl2_role2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1338') 
    
    stmt = """set schema ddl2_schema2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ grant component privilege "ALTER" on SQL_OPERATIONS to ddl2_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ grant component privilege "MANAGE_USERS" on SQL_OPERATIONS to ddl2_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ grant component privilege "MANAGE_ROLES" on SQL_OPERATIONS to ddl2_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ grant component privilege "MANAGE_COMPONENTS" on SQL_OPERATIONS to ddl2_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ grant component privilege "CREATE" on SQL_OPERATIONS to ddl2_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ grant component privilege "DROP" on SQL_OPERATIONS to ddl2_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema ddl2_schema2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    
    stmt = """create index ddl2_index22 on ddl2_table33(a);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """alter table ddl2_table33 disable index ddl2_index22;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl2_table33 enable index ddl2_index22;""";
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
     
    stmt = """alter table ddl2_table33 rename to ddl2_table3_11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop index ddl2_index22;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop table ddl2_table3_11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop table ddl2_table22;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop table ddl2_table11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    
    stmt = """ alter user qauser11 set online;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 
    
    stmt = """register component ddl1_comp1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 

    stmt = """create component privilege aa as 'sa' on ddl1_comp1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 
    
    stmt = """drop component privilege aa on ddl1_comp1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 
    
    stmt = """ unregister component ddl1_comp1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 
    
    stmt = """CREATE SEQUENCE seq1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop SEQUENCE seq1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create role ddl2_role2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop role ddl2_role2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop schema ddl2_schema2 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ revoke component privilege "ALTER" on SQL_OPERATIONS from ddl2_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ revoke component privilege "MANAGE_USERS" on SQL_OPERATIONS from ddl2_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ revoke component privilege "MANAGE_ROLES" on SQL_OPERATIONS from ddl2_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ revoke component privilege "MANAGE_COMPONENTS" on SQL_OPERATIONS from ddl2_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ revoke component privilege "CREATE" on SQL_OPERATIONS from ddl2_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ revoke component privilege "DROP" on SQL_OPERATIONS from ddl2_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke role ddl2_role1 from qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop role ddl2_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc) 
    
def testa24(desc="""privilege checks for DDL operations: user has component privilege"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
      
    #CREATE TABLE
    stmt = """create shared schema ddl3_schema2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set schema ddl3_schema2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ddl3_table11( a int not null primary key, b int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ddl3_table22(c int, d int, f varchar(10), constraint cons1 foreign key(c) references ddl3_table11);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ddl3_table33( a int not null primary key, b int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema ddl3_schema2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view ddl3_view11 as select * from ddl3_table33;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
    
    stmt = """drop table ddl3_table22;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    stmt = """drop table ddl3_table11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    
    stmt = """ unregister user qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    stmt = """ register user qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')   
    
    stmt = """ alter user qauser11 set online;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')  
    
    stmt = """register component ddl1_comp1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')

    stmt = """create component privilege aa as 'sa' on ddl1_comp1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    stmt = """drop component privilege aa on ddl1_comp1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    stmt = """ unregister component ddl1_comp1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    stmt = """CREATE SEQUENCE seq1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop SEQUENCE seq1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create role ddl3_role2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
   
    
    stmt = """drop schema ddl3_schema2 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 


    stmt = """set schema ddl3_schema2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop index ddl3_index11;"""
    output = _dci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1389') 
    
    stmt = """ grant component privilege "ALTER_TABLE" on SQL_OPERATIONS to qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ grant component privilege "MANAGE_USERS" on SQL_OPERATIONS to qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ grant component privilege "MANAGE_ROLES" on SQL_OPERATIONS to qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ grant component privilege "MANAGE_COMPONENTS" on SQL_OPERATIONS to qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ grant component privilege "CREATE_SEQUENCE" on SQL_OPERATIONS to qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ grant component privilege "DROP" on SQL_OPERATIONS to qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema ddl3_schema2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create index ddl3_index11 on ddl3_table33(a);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    
    stmt = """alter table ddl3_table33 disable index ddl3_index11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table ddl3_table33 enable index ddl3_index11;""";
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    
    stmt = """alter table ddl3_table33 rename to ddl3_table3_11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop index ddl3_index11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create view ddl3_view11 as select * from ddl3_table3_11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
    
    stmt = """drop table ddl3_table3_11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop table ddl3_table22;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop table ddl3_table11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    
    stmt = """ alter user qauser11 set online;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 
    
    stmt = """register component ddl1_comp1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 

    stmt = """create component privilege aa as 'sa' on ddl1_comp1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 
    
    stmt = """drop component privilege aa on ddl1_comp1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 
    
    stmt = """ unregister component ddl1_comp1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 
    
    stmt = """CREATE SEQUENCE seq1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop SEQUENCE seq1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create role ddl3_role2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop role ddl3_role2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop schema ddl3_schema2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ revoke component privilege "ALTER_TABLE" on SQL_OPERATIONS from qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ revoke component privilege "MANAGE_USERS" on SQL_OPERATIONS from qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ revoke component privilege "MANAGE_ROLES" on SQL_OPERATIONS from qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ revoke component privilege "MANAGE_COMPONENTS" on SQL_OPERATIONS from qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ revoke component privilege "CREATE_SEQUENCE" on SQL_OPERATIONS from qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ revoke component privilege "DROP" on SQL_OPERATIONS from qauser10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)  
    

  
def testa25(desc="""Privilege checks for utility operations: db__root"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """create shared schema ddl4_schema1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set schema ddl4_schema1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CONTROL QUERY DEFAULT SCHEMA 'ddl4_schema1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ddl4_tab1(a int, b int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ddl4_tab2(c int, d int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into ddl4_tab1 values(1,2),(4,5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,2)
    
    stmt = """load into ddl4_tab2 select * from ddl4_tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from ddl4_tab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output,2)

    stmt = """unload with purgedata from target into '/bulkload/4security' 
            select * from ddl4_tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'5 row(s) unloaded' );
    
    stmt = """drop table ddl4_tab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table ddl4_tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table ddl4_tab3 (a int not null primary key,b int) not droppable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index ddl4_index1 on ddl4_tab3(b) no populate hash partition by (b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """populate index ddl4_index1 on ddl4_tab3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update statistics for table ddl4_tab3 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showstats for table ddl4_tab3 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """purgedata DDL4_SCHEMA1.ddl4_tab3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set catalog trafodion;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set PARSERFLAGS 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop index ddl4_index1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table ddl4_tab3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop schema ddl4_schema1 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc) 

def testa26(desc="""Privilege checks for utility operations: other users"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
        
   
    #stmt = """set schema ddl4_schema1;"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_complete_msg(output)
    
    stmt = """CREATE COMPONENT PRIVILEGE MANAGE_LOAD AS 'MT' ON SQL_OPERATIONS SYSTEM DETAIL 'Allow grantee to perform load and unload requests';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE COMPONENT PRIVILEGE MANAGE_STATISTICS AS 'MS' ON SQL_OPERATIONS SYSTEM DETAIL 'Allow grantee to perform statistic requests';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """ grant component privilege MANAGE_LOAD on SQL_OPERATIONS to qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ grant component privilege SHOW on SQL_OPERATIONS to qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ grant component privilege MANAGE_STATISTICS on SQL_OPERATIONS to qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()

    stmt = """create schema ddl4_schema1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """set schema ddl4_schema1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    #stmt = """CONTROL QUERY DEFAULT SCHEMA 'ddl4_schema1';"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    
    stmt = """create table ddl4_tab1(a int, b int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table ddl4_tab2(c int, d int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select, insert,delete on ddl4_tab2 to qauser12;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """ grant select, insert,delete on ddl4_tab1 to qauser12;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    #stmt = """insert into ddl4_tab1 values(1,2),(4,5);"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_inserted_msg(output,2)
    
    stmt = """create table ddl4_tab3 (a int not null primary key,b int) not droppable;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """ grant select on ddl4_tab3 to qauser12;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """ grant insert on ddl4_tab3 to qauser12;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """ grant delete on ddl4_tab3 to qauser12;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    
    stmt = """create index ddl4_index1 on ddl4_tab3 (b) no populate hash partition by (b);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """populate index ddl4_index1 on ddl4_tab3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """update statistics for table ddl4_tab3 on every column;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """showstats for table ddl4_tab3 on every column;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """purgedata DDL4_SCHEMA1.ddl4_tab3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
   
    stmt = """set catalog trafodion;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """set PARSERFLAGS 2;"""
    output =mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema ddl4_schema1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """update statistics for table ddl4_tab3 on every column;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """CONTROL QUERY DEFAULT SCHEMA 'ddl4_schema1';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """load into ddl4_tab2 select * from ddl4_tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """select * from ddl4_tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
    
    stmt = """unload with purgedata from target into '/bulkload/4security' 
            select * from ddl4_tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_any_substr(output,'5 row(s) unloaded' );
    
    stmt = """populate index ddl4_index1 on ddl4_tab3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """update statistics for table ddl4_tab3 on every column;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """showstats for table ddl4_tab3 on every column;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """purgedata DDL4_SCHEMA1.ddl4_tab3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
    
    stmt = """set catalog trafodion;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """set PARSERFLAGS 2;"""
    output =mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    mydci = basic_defs.switch_session_qi_user4()
    
    stmt = """set schema ddl4_schema1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """CONTROL QUERY DEFAULT SCHEMA 'ddl4_schema1';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """load into ddl4_tab2 select * from ddl4_tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """select * from ddl4_tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt = """unload with purgedata from target into '/bulkload/4security' 
            select * from ddl4_tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_any_substr(output,'5 row(s) unloaded' );
    
    stmt = """populate index ddl4_index1 on ddl4_tab3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """update statistics for table ddl4_tab3 on every column;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '9241') 
    
    stmt = """showstats for table ddl4_tab3 on every column;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """purgedata DDL4_SCHEMA1.ddl4_tab3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """set catalog trafodion;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """set PARSERFLAGS 2;"""
    output =mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    mydci = basic_defs.switch_session_qi_user5()
    
    stmt = """set schema ddl4_schema1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    
    stmt = """load into ddl4_tab2 select * from ddl4_tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt = """select * from ddl4_tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt = """unload with purgedata from target into '/bulkload/4security' 
            select * from ddl4_tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    stmt = """CONTROL QUERY DEFAULT SCHEMA 'ddl4_schema1';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """populate index ddl4_index1 on ddl4_tab3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt = """update statistics for table ddl4_tab3 on every column;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '9241')
    
    stmt = """showstats for table ddl4_tab3 on every column;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """purgedata DDL4_SCHEMA1.ddl4_tab3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt = """set catalog trafodion;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """set PARSERFLAGS 2;"""
    output =mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')

    stmt = """drop index DDL4_INDEX1;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table DDL4_TAB3;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop schema ddl4_schema1 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ revoke component privilege MANAGE_LOAD on SQL_OPERATIONS from qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ revoke component privilege SHOW on SQL_OPERATIONS from qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ revoke component privilege MANAGE_STATISTICS on SQL_OPERATIONS from qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc) 


def testa27(desc="""Privilege checks for utility operations: role has/no component privilege"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
        
   
    stmt = """create shared schema ddl5_schema1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create role ddl5_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create role ddl5_role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ grant role ddl5_role1 to qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ grant role ddl5_role2 to qauser12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set schema ddl5_schema1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE COMPONENT PRIVILEGE MANAGE_LOAD AS 'MT' ON SQL_OPERATIONS SYSTEM DETAIL 'Allow grantee to perform load and unload requests';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE COMPONENT PRIVILEGE MANAGE_STATISTICS AS 'MS' ON SQL_OPERATIONS SYSTEM DETAIL 'Allow grantee to perform statistic requests';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """ grant component privilege MANAGE_LOAD on SQL_OPERATIONS to ddl5_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ grant component privilege SHOW on SQL_OPERATIONS to ddl5_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ grant component privilege MANAGE_STATISTICS on SQL_OPERATIONS to ddl5_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema ddl5_schema1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table ddl4_tab1(a int, b int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table ddl4_tab2(c int, d int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into ddl4_tab1 values(1,2),(4,5);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,2)
    
    stmt = """create table ddl4_tab3 (a int not null primary key,b int) not droppable;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select on ddl4_tab3 to ddl5_role2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """ grant insert on ddl4_tab3 to ddl5_role2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """ grant delete on ddl4_tab3 to ddl5_role2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)


    stmt = """create index ddl4_index1 on ddl4_tab3 (b) no populate hash partition by (b);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema ddl5_schema1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """CONTROL QUERY DEFAULT SCHEMA 'ddl5_schema1';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """load into ddl4_tab2 select * from ddl4_tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    #mydci.expect_error_msg(output, '4481') 
    
    stmt = """select * from ddl4_tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
    
    stmt = """unload with purgedata from target into '/bulkload/4security' 
            select * from ddl4_tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_any_substr(output,'5 row(s) unloaded' );
    
    stmt = """populate index ddl4_index1 on ddl4_tab3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    stmt = """set schema ddl5_schema1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """update statistics for table ddl4_tab3 on every column;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """showstats for table ddl4_tab3 on every column;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """purgedata DDL5_SCHEMA1.ddl4_tab3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
    
    stmt = """set catalog trafodion;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """set PARSERFLAGS 2;"""
    output =mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    mydci = basic_defs.switch_session_qi_user4()
    
    stmt = """set schema ddl5_schema1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """CONTROL QUERY DEFAULT SCHEMA 'ddl5_schema1';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """load into ddl4_tab2 select * from ddl4_tab1;"""
    output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '4481') 
    mydci.expect_complete_msg(output)
    
    stmt = """select * from ddl4_tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
    
    stmt = """unload with purgedata from target into '/bulkload/4security' 
            select * from ddl4_tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
    
    stmt = """populate index ddl4_index1 on ddl4_tab3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """update statistics for table ddl4_tab3 on every column;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '9241') 
    
    stmt = """showstats for table ddl4_tab3 on every column;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """purgedata DDL5_SCHEMA1.ddl4_tab3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """set catalog trafodion;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """set PARSERFLAGS 2;"""
    output =mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    
    stmt = """drop schema ddl5_schema1 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ revoke component privilege MANAGE_LOAD on SQL_OPERATIONS from ddl5_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ revoke component privilege SHOW on SQL_OPERATIONS from ddl5_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ revoke component privilege MANAGE_STATISTICS on SQL_OPERATIONS from ddl5_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ revoke role ddl5_role1 from qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ revoke role ddl5_role2 from qauser12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop role ddl5_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop role ddl5_role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)    
 

  

    
     
    
    
    
    
    