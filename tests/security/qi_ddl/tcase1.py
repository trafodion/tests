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

def testa01(desc="""DDL operations drop tables"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """create schema qi_schema1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema qi_schema1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a01tab1(a int not null primary key, b int);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ insert into a01tab1 values(11,10), (1,4);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,2)
    
    stmt = """grant select,insert on a01tab1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into a01tab1 values(3,4);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    stmt = """ select * from a01tab1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,3) 
    
    stmt = """ delete  from a01tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop table a01tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ insert into a01tab1 values(1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into a01tab1 values(3,4);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')
    
    stmt = """ select * from a01tab1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_error_msg(output, '4082') 
    
    stmt = """ delete  from a01tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """drop schema qi_schema1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    
def testa02(desc="""DDL operations,alter table add column/drop column"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """create schema qi_schema2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema qi_schema2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a02tab1(a int, b int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ insert into a02tab1 values(1,3),(9,8);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,2)
    
    stmt = """ grant insert on a02tab1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from a02tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ delete from a02tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ insert into a02tab1 values(11,34),(34,55);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,2)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table a02tab1 add column c int;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from a02tab1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,4) 
    
    stmt = """ insert into a02tab1 values (11,22,33);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from a02tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ delete from a02tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ insert into a02tab1 values(11,34),(34,55);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_error_msg(output, '4023')
    
    stmt = """ insert into a02tab1 values(11,34,77);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table a02tab1 add column d int;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select on a02tab1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ insert into a02tab1 values(11,34,79,1);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table a02tab1 drop column b;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from a02tab1 where(b>0);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4001')
    
    stmt = """ insert into a02tab1 values(1,2,3,4);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4023')
  
    stmt = """ insert into a02tab1 values(1,2,3);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table a02tab1 drop column d;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from a02tab1 where(d>0);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4001')
    
    stmt = """ insert into a02tab1 values(2,3,4);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4023')
  
    stmt = """ insert into a02tab1 values(2,3);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop table a02tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from a02tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')
    
    stmt = """ insert into a02tab1 values(2,3);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """drop schema qi_schema2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    
def testa03(desc="""DDL operations,alter table add/drop check constraint"""):
    global _testmgr
    global _testlist
    global mydci
    if not _testmgr.testcase_begin(_testlist): return 
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """create schema qi_schema3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema qi_schema3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a03tab1(a int, b int, constraint c1 check (a>b));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into a03tab1 values (13,1);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)
    
    stmt = """insert into a03tab1 values (12,14);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '8101')
    
    stmt = """grant insert on a03tab1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
     
    stmt = """set schema qi_schema3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
 
    stmt = """insert into a03tab1 values (23,11);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)
    
    stmt = """insert into a03tab1 values (22,24);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '8101')
    
    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema qi_schema3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
 
    stmt = """alter table a03tab1 add constraint c2 check (a > 2*b);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into a03tab1 values (33,11);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)
    
    stmt = """insert into a03tab1 values (32,31);""" 
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '8101')
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
 
    stmt = """insert into a03tab1 values (43,11);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)
    
    stmt = """insert into a03tab1 values (42,34);""" 
    output = mydci.cmdexec(stmt)    
    mydci.expect_error_msg(output, '8101')
 
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
 
    stmt = """alter table a03tab1 drop constraint c2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into a03tab1 values (53,41);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)
    
    stmt = """insert into a03tab1 values (52,54);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_error_msg(output, '8101')
 
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
 
    stmt = """insert into a03tab1 values (63,51); """
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)
    
    stmt = """insert into a03tab1 values (54,62);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_error_msg(output, '8101')
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
 
    stmt = """alter table a03tab1 drop constraint c1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into a03tab1 values (53,70);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)

    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into a03tab1 values (1,70);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop table a03tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop schema qi_schema3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    
def testa04(desc="""DDL operations,alter table add/drop unique constraint"""):
    global _testmgr
    global _testlist
    global mydci
    if not _testmgr.testcase_begin(_testlist): return 
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """create schema qi_schema4;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema qi_schema4;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a04tab1( a int not null primary key, b int, c int,constraint cons4_1 unique(b));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into a04tab1 values(1,2,3);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)
    
    stmt = """insert into a04tab1 values(1,2,3);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_error_msg(output, '8102')
    
    stmt = """ grant insert on a04tab1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema4;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into a04tab1 values(2,1,4);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_error_msg(output, '4481')

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema qi_schema4;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """ grant select on a04tab1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user3()

    stmt = """insert into a04tab1 values(2,1,4);"""
    output = mydci.cmdexec(stmt)  
    mydci.expect_inserted_msg(output,1)
    
    stmt = """insert into a04tab1 values(3,4,5);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema4;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table a04tab1 add constraint cons42 unique(c);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into a04tab1 values(11,7,6);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)
    
    stmt = """insert into a04tab1 values(11,1,5);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_error_msg(output, '8102')
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema4;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into a04tab1 values(15,8,9);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)
    
    stmt = """insert into a04tab1 values(11,1,6);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_error_msg(output, '8102')
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema4;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table a04tab1 drop constraint cons42;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into a04tab1 values(100,99,98);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)
    
    stmt = """insert into a04tab1 values(100,99,98);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_error_msg(output, '8102')
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema4;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into a04tab1 values(87,98,98);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)
    
    stmt = """insert into a04tab1 values(86,99,98);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_error_msg(output, '8102')
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema4;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """alter table a04tab1 drop constraint cons4_1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop table a04tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop schema qi_schema4 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    
def testa05(desc="""DDL operations,alter table add/drop primary key"""):
    global _testmgr
    global _testlist
    global mydci
    if not _testmgr.testcase_begin(_testlist): return 
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """create schema qi_schema5;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema qi_schema5;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a05tab1(a int, b int) no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ insert into a05tab1 values(9,1);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)
    
    stmt = """grant insert,select on a05tab1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema5;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ insert into a05tab1 values(9,1),(8,2);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,2)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema5;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """alter table a05tab1 add constraint cons51 primary key(a);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '8110')    

    stmt = """delete from a05tab1 where a =9 ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,2)

    stmt = """alter table a05tab1 add constraint cons51 primary key(a);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ insert into a05tab1 values(8,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '8102')
    
    stmt = """ insert into a05tab1 values(7,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema5;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ insert into a05tab1 values(8,9);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '8102')
    
    stmt = """ insert into a05tab1 values(6,3);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema5;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table a05tab1 drop constraint cons51;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ insert into a05tab1 values(9,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema5;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ insert into a05tab1 values(9,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """drop table a05tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop schema qi_schema5;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    
def testa06(desc="""DDL operations,alter table add/drop foreign key (RI)"""):
    global _testmgr
    global _testlist
    global mydci
    if not _testmgr.testcase_begin(_testlist): return 
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """create schema qi_schema6;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema qi_schema6;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a06tab1( a int not null primary key, b int);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ create table a06tab2(c int, d int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ insert into a06tab1 values(1,1);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)
    
    stmt = """ insert into a06tab2 values(1,1);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)
    
    stmt= """ grant insert,select on a06tab2 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema6;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into a06tab1 values(1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ insert into a06tab2 values(1,1);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema6;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """alter table a06tab2 add constraint c61 foreign key(d) references a06tab1(a);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ insert into a06tab1 values(2,2);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)
    
    stmt = """insert into a06tab2 values(1,3);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '8103')
    
    stmt = """insert into a06tab2 values(1,2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema6;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ insert into a06tab2 values(1,3);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_error_msg(output, '8103')
    
    stmt = """ insert into a06tab2 values(1,2);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema6;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ alter table a06tab2 drop constraint c61;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into a06tab2 values(1,3);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema6;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ insert into a06tab2 values(1,3);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)
    
    stmt = """ insert into a06tab2 values(1,2);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """drop table a06tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop table a06tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop schema qi_schema6;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    
def testa07(desc="""DDL operations,create/drop index"""):
    global _testmgr
    global _testlist
    global mydci
    if not _testmgr.testcase_begin(_testlist): return 
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """create schema qi_schema7;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema qi_schema7;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a07tab1( a int not null primary key, b int);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create index index1 on a07tab1(b desc);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant select, delete, insert on a07tab1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """populate index index1 on a07tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema7;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ populate index index1 on a07tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """revoke select, delete, insert on a07tab1 from qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema7;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ populate index index1 on a07tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
   
    
    stmt = """grant component privilege "ALTER" on sql_operations to  qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema qi_schema7;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant update on a07tab1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema7;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ populate index index1 on a07tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema qi_schema7;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """revoke update on a07tab1 from qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema7;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ populate index index1 on a07tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 

    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """drop table a07tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop schema qi_schema7;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """revoke component privilege "ALTER" on sql_operations from  qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    
    
def testa08(desc="""create view depends on one table, drop view"""):
    global _testmgr
    global _testlist
    global mydci
    if not _testmgr.testcase_begin(_testlist): return 
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """create schema qi_schema8;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema qi_schema8;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a08tab1( a int not null primary key, b int);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create view a08view1 as select * from a08tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """grant select on a08tab1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select on a08view1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema8;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from a08tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt = """ select * from a08view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema8;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop view a08view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema8;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from a08tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt = """select * from a08view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema8;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop table a08tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop schema qi_schema8;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    
def testa09(desc="""create view depends on one table, drop table"""):
    global _testmgr
    global _testlist
    global mydci
    if not _testmgr.testcase_begin(_testlist): return 
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """create schema qi_schema9;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema qi_schema9;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a09tab1( a int not null primary key, b int);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create view a09view1 as select * from a09tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """grant select on a09tab1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select on a09view1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema9;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from a09tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt = """ select * from a09view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema9;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop table a09tab1 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema9;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from a09tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')
    
    stmt = """select * from a09view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')
    
    mydci = basic_defs.switch_session_qi_user2()
    
    
    stmt = """drop schema qi_schema9;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    
def testa10(desc="""create view depends on mixed tables, drop table"""):
    global _testmgr
    global _testlist
    global mydci
    if not _testmgr.testcase_begin(_testlist): return 
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """create schema qi_schema10;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema qi_schema10;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a10tab1( a1 int not null primary key, b1 int,c1 varchar(10));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a10tab2( a2 int not null primary key, b2 int,c2 varchar(10));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create view a10view1 as select * from a10tab1,a10tab2 where a1=a2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select on a10view1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema10;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from a10view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema10;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop table a10tab1 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema10;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from a10view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema10;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop table a10tab2 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop schema qi_schema10;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    
def testa11(desc="""create view depends on mixed table and view, drop table"""):
    global _testmgr
    global _testlist
    global mydci
    if not _testmgr.testcase_begin(_testlist): return 
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """create schema qi_schema11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema qi_schema11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a11tab1( a1 int not null primary key, b1 int,c1 varchar(10));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a11tab2( a2 int not null primary key, b2 int,c2 varchar(10));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a11tab3( a3 int not null primary key, b3 int,c3 varchar(10));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create view a11view1 as select a1,c2 from a11tab1, a11tab2 where a1>a2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ create view a11view2 as select a1,b2 from a11tab2,a11view1 where a2=a1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select on a11view2 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select on a11view1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select on a11tab1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select on a11tab2 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select on a11tab3 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from a11view2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt = """select * from a11view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop table a11tab1 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from a11view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082') 
    
    stmt = """select * from a11view2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082') 
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop table a11tab2 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop table a11tab3 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop schema qi_schema11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    
    
def testa12(desc="""create view depends on mixed table and view, drop view"""):
    global _testmgr
    global _testlist
    global mydci
    if not _testmgr.testcase_begin(_testlist): return 
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """create schema qi_schema12;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema qi_schema12;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a12tab1( a1 int not null primary key, b1 int,c1 varchar(10));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a12tab2( a2 int not null primary key, b2 int,c2 varchar(10));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a12tab3( a3 int not null primary key, b3 int,c3 varchar(10));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create view a12view1 as select a1,c2 from a12tab1, a12tab2 where a1>a2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ create view a12view2 as select a1,b2 from a12tab2,a12view1 where a2=a1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select on a12view2 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select on a12view1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select on a12tab1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select on a12tab2 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select on a12tab3 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema12;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from a12view2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt = """select * from a12view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema12;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop view a12view1 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema12;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from a12view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082') 
    
    stmt = """select * from a12view2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082') 
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema12;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop table a12tab1 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop table a12tab2 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop table a12tab3 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop schema qi_schema12;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    
def testa13(desc="""create view depends on an view, drop view"""):
    global _testmgr
    global _testlist
    global mydci
    if not _testmgr.testcase_begin(_testlist): return 
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """create schema qi_schema13;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema qi_schema13;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a13tab1( a1 int not null primary key, b1 int,c1 varchar(10));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ create view a13view1 as select a1,b1 from a13tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ create view a13view2 as select b1 from a13view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select on a13tab1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select on a13view1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """ grant select on a13view2 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
     
    stmt = """set schema qi_schema13;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from a13view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt = """ select * from a13view2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema13;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop view a13view1 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
     
    stmt = """set schema qi_schema13;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from a13view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082') 
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema13;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop table a13tab1 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop schema qi_schema13;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    
def testa14(desc="""create view depends on an view, drop table"""):
    global _testmgr
    global _testlist
    global mydci
    if not _testmgr.testcase_begin(_testlist): return 
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """create schema qi_schema14;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema qi_schema14;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a14tab1( a1 int not null primary key, b1 int,c1 varchar(10));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ create view a14view1 as select a1,b1 from a14tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ create view a14view2 as select b1 from a14view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select on a14tab1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select on a14view1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """ grant select on a14view2 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
     
    stmt = """set schema qi_schema14;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from a14view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt = """ select * from a14view2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema14;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop table a14tab1 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
     
    stmt = """set schema qi_schema14;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from a14view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082') 
    
    stmt = """ select * from a14view2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082') 
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """ drop schema qi_schema14;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
 
def testa15(desc="""create view depends on mixed views, drop table"""):
    global _testmgr
    global _testlist
    global mydci
    if not _testmgr.testcase_begin(_testlist): return 
 
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """create schema qi_schema15;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema qi_schema15;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a15tab1( a1 int not null primary key, b1 int,c1 varchar(10));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a15tab2( a2 int not null primary key, b2 int,c2 varchar(10));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ create view a15view1 as select a1 from a15tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ create view a15view2 as select b2 from a15tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ create view a15view3 as select * from a15view1, a15view2 where a1>b2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select on a15tab1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select on a15tab2 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select on a15view1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """ grant select on a15view2 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select on a15view3 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
     
    stmt = """set schema qi_schema15;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from a15view3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt = """ select * from a15view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt = """ select * from a15view2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    mydci = basic_defs.switch_session_qi_user2()
     
    stmt = """set schema qi_schema15;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop table a15tab1 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
     
    stmt = """set schema qi_schema15;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from a15view3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')
    
    stmt = """ select * from a15view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')
    
    stmt = """ select * from a15view2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    mydci = basic_defs.switch_session_qi_user2()
     
    stmt = """set schema qi_schema15;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop table a15tab2 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop schema qi_schema15;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    
    
def testa16(desc="""DDL operations,load/unload"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """create shared schema qi_schema16;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema qi_schema16;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a16tab1(a int, b int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a16tab2(a int, b int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into a16tab1 values(1,2),(3,4);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,2)

    stmt = """ grant insert,select on a16tab1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema16;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into a16tab1 values(2,13);"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_inserted_msg(output,1)
    
    stmt = """load into a16tab2 select * from a16tab1;"""
    output = mydci.cmdexec(stmt) 
    mydci.expect_error_msg(output, '4481')  

    stmt = """unload with purgedata from target into '/bulkload/4security' 
            select * from a16tab2;"""
    output = mydci.cmdexec(stmt) 
    mydci.expect_error_msg(output, '4481')  


    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema16;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)      

    stmt = """ grant insert,select on a16tab2 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)  

    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema16;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """select * from a16tab2;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,0)
    
    stmt = """load into a16tab2 select * from a16tab1;"""
    output = mydci.cmdexec(stmt) 
    mydci.expect_any_substr(output,'Rows Processed: 3' );   

    stmt = """unload with purgedata from target into '/bulkload/4security' 
            select * from a16tab2;"""
    output = mydci.cmdexec(stmt) 
    mydci.expect_any_substr(output,'Rows Processed: 3' );  
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema16;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """ revoke insert,select on a16tab1 from qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema16;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """load into a16tab2 select * from a16tab1;"""
    output = mydci.cmdexec(stmt) 
    mydci.expect_error_msg(output, '4481')  
    
    stmt = """unload with purgedata from target into '/bulkload/4security' 
            select * from a16tab2;"""
    output = mydci.cmdexec(stmt) 
    #mydci.expect_error_msg(output, '4481')
    mydci.expect_any_substr(output,'5 row(s) unloaded' );  
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema16;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop table a16tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop table a16tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop schema qi_schema16;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

    
def testa17(desc="""DDL operations,upsert"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """create shared schema qi_schema17;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema qi_schema17;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a17tab1(a int, b int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema17;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ upsert into a17tab1 values(1,2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema17;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant insert on a17tab1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema17;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ upsert into a17tab1 values(1,2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema17;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ revoke insert on a17tab1 from qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema17;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ upsert into a17tab1 values(1,2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema17;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop table a17tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop schema qi_schema17;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    
    
def testa18(desc="""DDL operations,merge"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """create shared schema qi_schema18;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema qi_schema18;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a18tab1(a int not null, b int, primary key (a));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema18;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ merge into a18tab1 on a= 10 when not matched then insert values(10,20);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema18;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant insert,update, select on a18tab1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema18;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ merge into a18tab1 on a= 10 when not matched then insert values(10,20);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema18;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ revoke insert on a18tab1 from qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema18;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ merge into a18tab1 on a= 10 when not matched then insert values(10,20);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema18;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop table a18tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop schema qi_schema18;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    
    
def testa19(desc="""DDL operations,create table as"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """create shared schema qi_schema19;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema qi_schema19;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a19tab1(a int, b int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema19;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a19tab2 as select * from a19tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema19;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select on a19tab1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema19;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a19tab2 as select * from a19tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,0)
    
    stmt = """ insert into a19tab2 values(1,2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema19;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ revoke select on a19tab1 from qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema19;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
        
    stmt = """create table a19tab3 as select * from a19tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')   
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema19;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop table a19tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop table a19tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop schema qi_schema19;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
   
    
     
    

    
    