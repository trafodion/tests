# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2014 Hewlett-Packard Development Company, L.P.
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
from ...lib import gvars
import defs

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
    
def test001(desc="""ddls not allowed in TX"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    #-------------------------------------------------------------------------
    # PAGE34-PAGE37 (Syntax Description of CREATE TABLE)
    #-------------------------------------------------------------------------

    stmt = """create table t (a int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # DDL not allowed in TX
    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
 
    stmt = """create table t1 (a int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '20123')

    stmt = """alter table t add column b int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '20123')

    stmt = """create index idx on t (a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '20123')

    stmt = """create volatile index idx on t (a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '20123')

    stmt = """create view v as select * from t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '20123')

    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """SET TRANSACTION AUTOCOMMIT OFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table t1 (a int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '20124')

    stmt = """alter table t add column b int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '20124')

    stmt = """create index idx on t (a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '20124')

    stmt = """create volatile index idx on t (a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '20124')

    stmt = """create view v as select * from t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '20124')

    stmt = """SET TRANSACTION AUTOCOMMIT ON;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
     
    stmt = """drop table t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
 
    _testmgr.testcase_end(desc)

def test002(desc="""begin work/commit work/rollback work"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    #--------------------------------------------------------------------------
    # Command sequences
    #--------------------------------------------------------------------------
    # Double BEGIN WORK
    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8603')

    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # COMMIT WORK without BEGIN WORK
    stmt = """COMMIT WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8605')

    # ROLLBACK WORK without BEGIN WORK
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8609')

    # COMMIT without 'WORK'
    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """COMMIT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # ROLLBACK without 'WORK' 
    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ROLLBACK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
 
    #--------------------------------------------------------------------------
    # BEGIN WORK example
    #--------------------------------------------------------------------------
    stmt = """create table orders (c1 int, c2 date, c3 date, c4 int, c5 int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table odetail (c1 int, c2 int, c3 int, c4 int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table partloc (partnum int, loc_code char(10), qty_on_hand int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into partloc VALUES (4102, 'G45', 10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """INSERT INTO orders VALUES (125, DATE '2008-03-23', DATE '2008-03-30', 75, 7654);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """INSERT INTO odetail VALUES (125, 4102, 25000, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """UPDATE partloc SET qty_on_hand = qty_on_hand - 2 WHERE partnum = 4102 AND loc_code = 'G45';"""    
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """COMMIT WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)

    stmt = """select * from odetail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)

    stmt = """select qty_on_hand from partloc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    _dci.expect_str_token(output, '8')

    stmt = """drop table orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table odetail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table partloc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #--------------------------------------------------------------------------
    # COMMIT WORK example
    #--------------------------------------------------------------------------
    stmt = """create table partsupp (C1 int, C2 int, C3 float, C4 int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table supplier (C1 int, C2 char(20), C3 char(20), C4 char(20), C5 char(20), C6 char(20));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table partloc (partnum int, loc_code char(10), qty_on_hand int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into partloc VALUES (5100, 'G43', 10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """INSERT INTO partsupp VALUES (5100, 17, 800.00, 24);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """INSERT INTO supplier
VALUES (17, 'Super Peripherals','751 Sanborn Way',
'Santa Rosa', 'California', '95405');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """UPDATE partloc
SET qty_on_hand = qty_on_hand + 24
WHERE partnum = 5100 AND loc_code = 'G43';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """COMMIT WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from partsupp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)

    stmt = """select * from supplier;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)

    stmt = """select qty_on_hand from partloc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    _dci.expect_str_token(output, '34')

    stmt = """drop table partsupp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table supplier;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table partloc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #--------------------------------------------------------------------------
    # ROLLBACK WORK example
    #--------------------------------------------------------------------------
    stmt = """create table orders (c1 int, c2 date, c3 date, c4 int, c5 int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table odetail (c1 int, c2 int, c3 int, c4 int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table partloc (partnum int, loc_code char(10), qty_on_hand int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into partloc VALUES (4130, 'K43', 10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """INSERT INTO orders
VALUES (124, DATE '2007-04-10',
DATE '2007-06-10', 75, 7654);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """INSERT INTO odetail
VALUES (124, 4130, 25000, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """UPDATE partloc
SET qty_on_hand = qty_on_hand - 2
WHERE partnum = 4130 AND loc_code = 'K43';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)

    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)

    stmt = """select * from odetail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)

    stmt = """select qty_on_hand from partloc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    _dci.expect_str_token(output, '10')

    stmt = """drop table orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table odetail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table partloc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def test003(desc="""set transaction"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # this is the same as set transaction autocommit on
    stmt = """set transaction autocommit;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # Examples:
    stmt = """create table employee (empnum int, first_name char(20), last_name  char(20), deptnum int, salary float);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into employee values (23, 'CHRIS', 'JONES', 2000, 121000.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """set transaction autocommit on;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table dept(manager int, deptnum int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into dept values (49, 1000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """SET TRANSACTION AUTOCOMMIT OFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """DELETE FROM employee
WHERE empnum = 23;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)

    stmt = """INSERT INTO employee
(empnum, first_name, last_name, deptnum, salary)
VALUES (50, 'JERRY','HOWARD', 1000, 137000.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = """UPDATE dept
SET manager = 50
WHERE deptnum = 1000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)

    stmt = """COMMIT WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from employee;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    _dci.expect_str_token(output, 'JERRY')

    stmt = """select * from dept;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    _dci.expect_str_token(output, '50')
  
    stmt = """set transaction autocommit on;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
 
    stmt = """drop table employee;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table dept;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
 
    _testmgr.testcase_end(desc)

def test004(desc="""TBD"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    _testmgr.testcase_end(desc)
