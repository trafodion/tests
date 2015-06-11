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

def testa20(desc="""create view depends on mixed views, drop view"""):
    global _testmgr
    global _testlist
    global mydci
    if not _testmgr.testcase_begin(_testlist): return 
 
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """create schema qi_schema16;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema qi_schema16;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a16tab1( a1 int not null primary key, b1 int,c1 varchar(10));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a16tab2( a2 int not null primary key, b2 int,c2 varchar(10));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ create view a16view1 as select a1 from a16tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ create view a16view2 as select b2 from a16tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ create view a16view3 as select * from a16view1, a16view2 where a1>b2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select on a16tab1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select on a16tab2 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select on a16view1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """ grant select on a16view2 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select on a16view3 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
     
    stmt = """set schema qi_schema16;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from a16view3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt = """ select * from a16view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt = """ select * from a16view2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    mydci = basic_defs.switch_session_qi_user2()
     
    stmt = """set schema qi_schema16;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop view a16view1 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
     
    stmt = """set schema qi_schema16;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from a16view3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')
    
    stmt = """ select * from a16view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')
    
    stmt = """ select * from a16view2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    mydci = basic_defs.switch_session_qi_user2()
     
    stmt = """set schema qi_schema16;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop table a16tab1 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop table a16tab2 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop schema qi_schema16;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    
def testa21(desc="""create view depends on one table, alter view"""):
    global _testmgr
    global _testlist
    global mydci
    if not _testmgr.testcase_begin(_testlist): return 
 
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """create schema qi_schema17;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema qi_schema17;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a17tab1( a1 int not null primary key, b1 int,c1 varchar(10));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ create view a17view1 as select  * from a17tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select on a17tab1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """ grant select on a17view1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema17;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from a17view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema17;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ alter view a17view1 rename to a17view1_1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema17;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from a17view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')  
    
    stmt = """ select * from a17view1_1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0) 
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema17;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop table a17tab1 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema17;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from a17view1_1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """drop schema qi_schema17;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    
def testa22(desc="""create view depends on view, alter view"""):
    global _testmgr
    global _testlist
    global mydci
    if not _testmgr.testcase_begin(_testlist): return 
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """create schema qi_schema18;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema qi_schema18;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a18tab1( a1 int not null primary key, b1 int,c1 varchar(10));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ create view a18view1 as select  * from a18tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ create view a18view2 as select * from a18view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select on a18tab1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select on a18view1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
  
    stmt = """ grant select on a18view2 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema18;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from a18view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt = """ select * from a18view2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema18;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ alter view a18view1 rename to a18view1_1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema18;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from a18view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ select * from a18view2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt = """ select * from a18view1_1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema18;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop table a18tab1 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop schema qi_schema18;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    
def testa23(desc="""create view depends on view, alter view2"""):
    global _testmgr
    global _testlist
    global mydci
    if not _testmgr.testcase_begin(_testlist): return 
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """create schema qi_schema19;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema qi_schema19;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a19tab1( a1 int not null primary key, b1 int,c1 varchar(10));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ create view a19view1 as select  * from a19tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ create view a19view2 as select * from a19view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select on a19tab1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select on a19view1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
  
    stmt = """ grant select on a19view2 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema19;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from a19view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt = """ select * from a19view2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema19;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ alter view a19view2 rename to a19view2_1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema19;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from a19view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt = """ select * from a19view2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ select * from a19view2_1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema19;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop table a19tab1 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop schema qi_schema19;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)


def testa24(desc="""create table in shared schema, then drop schema cascade"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """create shared schema qi_schema20;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema qi_schema20;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a20tab1(a int, b int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema20;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """ select * from a20tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ insert into a20tab1 values(1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema20;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select, insert on a20tab1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema20;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from a20tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt = """ insert into a20tab1 values(1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """drop schema qi_schema20 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema20;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """ select * from a20tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')
    
    stmt = """ insert into a20tab1 values(1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')
    
    _testmgr.testcase_end(desc)
    
def testa25(desc="""create table in private schema, then drop schema cascade"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """ grant component privilege create_table on sql_operations to qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """create schema qi_schema21;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema qi_schema21;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a21tab1(a int, b int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema21;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """ select * from a21tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    stmt = """ insert into a21tab1 values(1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema21;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select, insert on a21tab1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema21;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from a21tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt = """ insert into a21tab1 values(1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """drop schema qi_schema21 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema21;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """ select * from a21tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')
    
    stmt = """ insert into a21tab1 values(1,1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')

    stmt = """ revoke component privilege create_table on sql_operations from qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    
def testa26(desc="""create view in shared schema, then drop schema cascade"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """create shared schema qi_schema22;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema qi_schema22;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a22tab1(a int, b int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ create view a22view1 as select * from a22tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema22;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """select * from a22view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema22;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select on a22view1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select on a22tab1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema22;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from a22tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt = """ select * from a22view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt = """ create view a22view2 as select * from a22tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """drop schema qi_schema22 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema22;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from a22tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')
    
    stmt = """ select * from a22view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')
    
    stmt = """ select * from a22view2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')
    
    _testmgr.testcase_end(desc)
    
    
def testa27(desc="""create view in private schema, then drop schema cascade"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """ grant component privilege create_view on sql_operations to qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """create schema qi_schema23;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema qi_schema23;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a23tab1(a int, b int)no partition;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ create view a23view1 as select * from a23tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema23;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """select * from a23view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481') 
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema qi_schema23;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select on a23view1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select on a23tab1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema23;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from a23tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt = """ select * from a23view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)
    
    stmt = """ create view a23view2 as select * from a23tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """drop schema qi_schema23 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema qi_schema23;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ select * from a23tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')
    
    stmt = """ select * from a23view1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')
    
    stmt = """ select * from a23view2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4082')

    stmt = """ revoke component privilege create_view on sql_operations from qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def testa28(desc="""without qi ddl"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    _testmgr.create_dci_proc('qi_mxci6', _dci._target, _dci._dsn, 'trafodion', 'traf123','')
    mydci = _testmgr.get_dci_proc('qi_mxci6')
    
    stmt = """create schema a28schema1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """set schema a28schema1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a28tab_up(c1 int not null primary key, c2 int);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into a28tab_up values (1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,7)

    stmt = """create table a28tab_me(c1 int not null primary key, c2 int);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into a28tab_me values (1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,7)
   
    stmt = """create table a28tab_cas(c1 int not null primary key, c2 int);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into a28tab_cas values (1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,7)

    stmt = """create table a28tab_load1(c1 int not null primary key, c2 int);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into a28tab_load1 values (1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,7)
    
    stmt = """create table a28tab_load2(c1 int not null primary key, c2 int);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into a28tab_load2 values (1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (8,8);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,7)

    stmt = """create table a28tab_index(c1 int not null primary key, c2 int);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create index a28index on a28tab_index(c2 desc);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """insert into a28tab_index values (1,1),(3,3),(5,5), (6,6), (7,7),(2,2),(4,4);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,7)
    
    _dci = _testmgr.delete_dci_proc('qi_mxci6')
    _dci = _testmgr.get_default_dci_proc()
    

    #stmt = """obey /"""+defs.test_dir +"""/sample.sql(create_table);"""
    #output = _dci.cmdexec(stmt)  
    
    
    stmt = """set schema a28schema1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from a28tab_up;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output,7)
    
    stmt = """select * from a28tab_load1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output,7)
    
    stmt = """select * from a28tab_load2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output,7)
    
    stmt = """select * from a28tab_index;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test""", 's1')
    
    #stmt = """sh """+"""sqlci """+"""-i """+defs.test_dir +"""/sample.sql(table_operation1);"""
    #output = _dci.cmdexec(stmt)
    
    _testmgr.create_dci_proc('qi_mxci6', _dci._target, _dci._dsn, 'trafodion', 'traf123','')
    mydci = _testmgr.get_dci_proc('qi_mxci6')
    
    stmt = """set schema a28schema1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """upsert into a28tab_up values (1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7),(8,8);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """merge into a28tab_me on c1= 0 when not matched then insert values(10,20);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a28tab_cas2 as select * from a28tab_cas;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,7)
    
    stmt = """load into a28tab_load2 select * from a28tab_load1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """populate index a28index on a28tab_index;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    _dci = _testmgr.delete_dci_proc('qi_mxci6')
    _dci = _testmgr.get_default_dci_proc()
    
    #stmt="""control query default AUTO_QUERY_RETRY_WARNINGS 'ON';"""
    #output = _dci.cmdexec(stmt)
    
    stmt = """set schema a28schema1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from a28tab_up;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output,8)
    
    stmt = """select * from a28tab_me;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output,8)
    
    stmt = """select * from a28tab_cas2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output,7)
    
    stmt = """select * from a28tab_load2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output,8)
    
    stmt = """select * from a28tab_load1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output,7)
    
    stmt = """populate index a28index on a28tab_index;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    

    stmt = """select * from a28tab_index;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test""", 's1')
    
    #stmt = """sh """+"""sqlci """+"""-i """+defs.test_dir +"""/sample.sql(table_operation2);"""
    #output = _dci.cmdexec(stmt)
    
    _testmgr.create_dci_proc('qi_mxci6', _dci._target, _dci._dsn, 'trafodion', 'traf123','')
    mydci = _testmgr.get_dci_proc('qi_mxci6')
    
    stmt = """set schema a28schema1;"""
    output = mydci.cmdexec(stmt)
    
    stmt = """unload with purgedata from target into '/bulkload/4security' 
            select * from a28tab_load2;"""
    output = mydci.cmdexec(stmt)

    stmt = """unload with purgedata from target into '/bulkload/4security' 
            select * from a28tab_load1;"""
    output = mydci.cmdexec(stmt)
    
    _dci = _testmgr.delete_dci_proc('qi_mxci6')
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """set schema a28schema1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from a28tab_load2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output,8)
    
    stmt = """select * from a28tab_load1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output,7)

    #stmt = """obey """+defs.test_dir +"""/sample.sql(drop_table);"""
    #output = _dci.cmdexec(stmt)
    
    stmt = """set schema a28schema1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a28tab_up cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a28tab_me cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a28tab_cas cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a28tab_load1 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a28tab_load2 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a28tab_index cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop schema a28schema1 cascade;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def testa29(desc="""veriry bug 1409113 disable index error displays incorrect schema name """):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    mydci = basic_defs.switch_session_qi_user3()

    stmt = """create schema a29schema1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """set schema a29schema1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a29tab1(c1 int not null , c2 int);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a29tab1 values (1,1), (2,2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,2)

    stmt = """alter table a29tab1 add constraint t1_pk primary key (c1);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """alter table a29tab1 disable all indexes;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop table a29tab1 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop schema a29schema1 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create schema a29schema1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set schema a29schema1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table a29tab1(c1 int not null, c2 int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into a29tab1 values (1,1), (2,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,2)

    stmt = """alter table a29tab1 add constraint t1_pk primary key (c1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """alter table a29tab1 disable all indexes;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table a29tab1 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop schema a29schema1 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)


def testa30(desc="""create view depends on a different schema , drop table cascade"""):
    global _testmgr
    global _testlist
    global mydci
    if not _testmgr.testcase_begin(_testlist): return 
 
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """create schema qi_schema30;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema qi_schema30;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a30tab1( a1 int not null primary key, b1 int,c1 varchar(10));"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ create view a30view1 as select a1 from a30tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
  
    stmt = """ grant select on a30tab1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ grant select on a30view1 to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()

    stmt = """create schema qi_schema30_1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
     
    stmt = """set schema qi_schema30_1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create view a30view2 as select * from qi_schema30.a30tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()
     
    stmt = """set schema qi_schema30;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """ drop table a30tab1 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user3()
     
    stmt = """drop  schema qi_schema30_1 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """drop schema qi_schema30 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def testa31(desc="""create table like, drop schema cascade"""):
    global _testmgr
    global _testlist
    global mydci
    if not _testmgr.testcase_begin(_testlist): return 

    stmt = """grant component privilege "CREATE_TABLE" on sql_operations to qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
 
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """create schema qi_schema31;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema qi_schema31;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a31tab1( a1 int not null primary key, b1 int);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create shared schema qi_schema31_1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema qi_schema31_1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create table a31tab2( a1 int not null primary key, b1 int);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user3()

    stmt = """set schema qi_schema31;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a31tab33( a1 int not null primary key, b1 int);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a31tab1_1 like a31tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a31tab1_1 values (1,1);"""
    output = mydci.cmdexec(stmt)  
    mydci.expect_inserted_msg(output,1)   

    stmt = """select * from a31tab1_1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,1)   

    stmt = """delete from a31tab1_1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_deleted_msg(output,1)   

    stmt = """select * from a31tab1;"""
    output = mydci.cmdexec(stmt) 
    mydci.expect_error_msg(output, '4481')

    stmt = """set schema qi_schema31_1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a31tab2_1 like a31tab2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a31tab2_1 values (1,1);"""
    output = mydci.cmdexec(stmt)  
    mydci.expect_inserted_msg(output,1)   

    stmt = """select * from a31tab2_1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,1)   

    stmt = """delete from a31tab2_1;"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_deleted_msg(output,1)   

    stmt = """select * from a31tab2;"""
    output = mydci.cmdexec(stmt) 
    mydci.expect_error_msg(output, '4481')

    stmt = """create schema qi_schema31_3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema qi_schema31_3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create table a31tab3 like qi_schema31.a31tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant select on  a31tab3 to qauser12;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a31tab3 values (1,1);"""
    output = mydci.cmdexec(stmt)  
    mydci.expect_inserted_msg(output,1)  

    stmt = """drop schema qi_schema31_3 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema qi_schema31;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a31tab1_1 values (2,1);"""
    output = mydci.cmdexec(stmt)  
    mydci.expect_inserted_msg(output,1)   

    stmt = """set schema qi_schema31_1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """insert into a31tab2_1 values (2,1);"""
    output = mydci.cmdexec(stmt)  
    mydci.expect_error_msg(output, '4481')

    stmt = """set schema qi_schema31;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant select on  a31tab1_1 to qauser12 by qauser10;"""
    output = _dci.cmdexec(stmt) 
    #_dci.expect_error_msg(output, '4481')

    stmt = """grant select on  a31tab1_1 to qauser12 by qauser11;"""
    output = _dci.cmdexec(stmt) 
    #_dci.expect_error_msg(output, '4481')


    stmt = """set schema qi_schema31_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant select on  a31tab2_1 to qauser12 by qauser10;"""
    output = _dci.cmdexec(stmt) 
    #_dci.expect_error_msg(output, '4481')

    stmt = """grant select on  a31tab2_1 to qauser12 by qauser11;"""
    output = _dci.cmdexec(stmt) 
    #_dci.expect_error_msg(output, '4481')

    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """drop schema qi_schema31 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop schema qi_schema31_1 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """revoke component privilege "CREATE_TABLE" on sql_operations from qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)



