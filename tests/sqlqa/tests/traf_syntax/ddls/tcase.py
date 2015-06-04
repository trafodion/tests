# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2014-2015 Hewlett-Packard Development Company, L.P.
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
   
def test001(desc="""alter table"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create table t (pkey int primary key not null not droppable, c1 int, c2 int, c3 int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # ADD [COLUMN]
    stmt = """alter table t add c4 int default 0 not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'C4')  
 
    stmt = """alter table t add column c5 int default 0 not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """showddl t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'C5')

    stmt = """alter table t add column "sql" date default current_date not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'SQL')

    # ADD IF NOT EXISTS
    stmt = """alter table t add column c1 int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, "1080")

    # column exists
    stmt = """alter table t add if not exists column c1 int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # column does not exist
    stmt = """alter table t add if not exists column c7 int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'C7')

    # column does not exist
    stmt = """alter table t add if not exists column c8 numeric (4) unsigned;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'C8')

    # DROP COLUMN [IF EXISTS] 
    stmt = """alter table t drop column doesnotexist;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1009')

    # primary key can't be dropped
    stmt = """alter table t drop column pkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1420')

    # drop a newly added column
    stmt = """alter table t drop column c4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """alter table t drop column if exists doesnotexist;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """alter table t drop column c1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl t;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, 'C1')

    stmt = """alter table t drop column if exists c2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl t;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, 'C2')

    stmt = """drop table t cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # effect on a view
    stmt = """create table t (c1 int, c2 int, c3 int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into t values (1, 1, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """create view v as select * from t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from v;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """alter table t add column c4 int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # add a column to a table should have no effect on the view.
    stmt = """select * from v;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    _dci.unexpect_any_substr(output, 'C4')

    stmt = """alter table t drop column c3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # drop a column from a table should allows graceful error.
    stmt = """select * from v;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4003')

    stmt = """drop view v;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table t cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def test002(desc="""create index/drop index"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    #-------------------------------------------------------------------------
    # Examples
    #-------------------------------------------------------------------------
    stmt = """create table employee (last_name char(100), first_name char(100), address char(100));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into employee values ('A1','A2','A3'),('B1','B2','B3');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """create index xempname on employee(last_name ASCENDING, first_name ASC, address);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create volatile table employee_v (last_name char(100), first_name char(100), address char(100));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create volatile index xempname_v on employee_v(address, first_name DESC, last_name DESCENDING);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop index xempname;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table employee;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop volatile index xempname_v;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop volatile table employee_v;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # For nonunique indexes, the sum of the lengths of the columns in the 
    # index plus the sum of the length of the clustering key of the underlying 
    # table cannot exceed 2048 bytes. (This limitation might not be true for
    # Trafodion anymore)
    stmt = """create table t (a char(3000) not null not droppable, b char(3000)) store by (a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create index idx on t(a, b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table t cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)
 
def test003(desc="""create table/drop table"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    #-------------------------------------------------------------------------
    # Syntax
    #-------------------------------------------------------------------------
    # VOLATILE table
    stmt = """create volatile table ta1 (a int default 12);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop volatile table ta1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # IF NOT EXISTS
    stmt = """create table tb1 (a int, b int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # Table already exist, but shouldn't see an error.
    stmt = """create table if not exists tb1 ("a" int, "JOIN" int, extra int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # the table should still be the old one.
    stmt = """showddl tb1;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, 'EXTRA')

    stmt = """drop table tb1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # Table does not exist, should be created.
    stmt = """create table if not exists tb1 ("a" int, "JOIN" int, extra int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # now it should be the new table
    stmt = """showddl tb1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'EXTRA')

    stmt = """drop table tb1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # like-spec 
    stmt = """create table tc1 (a int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table tc2 like tc1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table tc3 like tc1 with partitions;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table tc1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table tc2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table tc3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table tc4 (a int not null, b int not null, c int not null, d int) store by (a, b, c) salt using 64 partitions on (c, b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table tc5 like tc4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table tc6 like tc4 with partitions;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table tc4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table tc5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table tc6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # NO PARTITION | SALT USING num PARTITIONS [ON (column[, column]...)]]
    stmt = """create table td1 (a int no default not null primary key desc) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table td1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table td2 (a int not null primary key, b date default current_date, c time default current_time, d timestamp default current_timestamp) salt using 2 partitions;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table td2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table td3 (a largeint not null primary key, b smallint, c float(10), d double precision) salt using 1024 partitions;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table td3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # salt columns using store by columns
    stmt = """create table td4 (a largeint not null, b smallint not null, c float(10) not null, d double precision) store by (a, b, c) salt using 1024 partitions on (b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table td4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # salt columns using primary key.
    stmt = """create table td5 (a largeint not null primary key, b smallint not null, c float(10) not null, d double precision) salt using 1024 partitions on (a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table td5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
 
    # salt number can only be 2-1024
    stmt = """create table td_err (a int primary key) salt using -1 partitions;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """create table td_err (a int primary key) salt using 0 partitions;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1196')

    stmt = """create table td_err (a int primary key) salt using 1 partitions;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1196')

    stmt = """create table td_err (a int primary key) salt using 1025 partitions;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1196')

    stmt = """create table td_err (a int primary key) salt using 0.5 partitions;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """create table td_err (a int primary key) salt using abcd partitions;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    # salt column only allowed primry key columns or store by columns
    stmt = """create table td_err (a int, b int not null) store by (b) salt using 2 partitions on (a, b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1195')

    # salt columns using a combination of primary key AND store by columns is
    # not supported
    stmt = """create table td6 (a int not null primary key, b int not null, c int not null, d int) store by (b, c) salt using 1024 partitions on (a, b, c);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)

    # STORE BY {PRIMARY KEY | (key-column-list)}
    stmt = """create table te1 (a int not null, b int not null) store by (a, b) salt using 2 partitions;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table te1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table te2 (a int not null primary key, b int) store by primary key salt using 2 partitions;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table te2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # It's an error if the store by list is not 'NOT NULL'
    stmt = """create table te_err (a int, b int) store by (a, b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1135')

    # It's an error if store by primary key but did not have a primary key
    stmt = """create table te_err (a int not null, b int not null) store by primary key;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3188')

    # [LOAD IF EXISTS | NO LOAD] [AS select-query]
    stmt = """create table tf1 (a int, b int, c int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into tf1 values (1,1,1),(2,2,2),(3,3,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output) 

    # Do not specify either NO LOAD or LOAD IF EXISTS.  The table does not
    # exist, so it should be created and loaded.
    stmt = """create table tf2 as (select a, b from tf1 where a < 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from tf2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)

    # should be an error.  Without LOAD IF EXISTS and table exists.
    stmt = """create table tf2 as (select a, b from tf1 where a < 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1390')

    # USE LOAD IF EXISTS for a table that does not exist.  This should insert 
    # 2 rows.
    stmt = """create table tf3 load if exists as (select a, b from tf1 where a < 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from tf3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)

    # Use NO LOAD, it should create an empty table.
    stmt = """create table tf4 no load as (select a, b from tf1 where a < 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from tf4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)

    # Use LOAD IF EXISTS for a table that alraedy exists.  Reuse the empty table
    # tf4. This should insert 2 rows.
    stmt = """create table tf4 load if exists as (select a, b from tf1 where a < 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from tf4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)

    stmt = """drop table tf1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table tf2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table tf3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    stmt = """drop table tf4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #-------------------------------------------------------------------------
    # Drop Table
    #-------------------------------------------------------------------------
    # IF EXISTS
    stmt = """create table tg1 (a int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table if exists tg1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # TABLE should be dropped
    stmt = """invoke tg1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')

    # shouldn't return error when the table does not exist.
    stmt = """drop table if exists TABLEDOESNOTEXIST;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    # RESTRICT|CASCADE
    stmt = """create table tg2 (a int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create view tg2v as select * from tg2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # should see error, default is RESTRICT
    stmt = """drop table tg2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1047')

    # should see error with RESTRICT
    stmt = """drop table tg2 RESTRICT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1047')

    # shuld drop the table
    stmt = """drop table tg2 CASCADE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #-------------------------------------------------------------------------
    # Examples
    #-------------------------------------------------------------------------
    stmt = """create table NPTEST
(FIRST_NAME CHAR(12) CHARACTER SET ISO88591 COLLATE DEFAULT NO DEFAULT
NOT NULL
, LAST_NAME CHAR(24) CHARACTER SET ISO88591 COLLATE
DEFAULT NO DEFAULT NOT NULL
, ADDRESS CHAR(128) CHARACTER SET ISO88591 COLLATE
DEFAULT DEFAULT NULL
, ZIP INT DEFAULT 0
, PHONE CHAR(10) CHARACTER SET ISO88591 COLLATE
DEFAULT DEFAULT NULL , SSN LARGEINT NO DEFAULT NOT NULL
, INFO1 CHAR(128) CHARACTER SET ISO88591 COLLATE
DEFAULT DEFAULT NULL , INFO2 CHAR(128) CHARACTER SET ISO88591 COLLATE
DEFAULT DEFAULT NULL , primary key (SSN,first_name,last_name)
)
max table size 512;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table LSCE002 like NPTEST ATTRIBUTE compression type hardware;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table NPTEST;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table LSCE002;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """CREATE TABLE ODETAIL
( ordernum NUMERIC (6) UNSIGNED NO DEFAULT NOT NULL,
partnum NUMERIC (4) UNSIGNED NO DEFAULT NOT NULL,
unit_price NUMERIC (8,2) NO DEFAULT NOT NULL,
qty_ordered NUMERIC (5) UNSIGNED NO DEFAULT NOT NULL,
PRIMARY KEY (ordernum, partnum) );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # CREATE TABLE ... LIKE ... 
    stmt = """CREATE TABLE ODETAIL1
LIKE ODETAIL WITH CONSTRAINTS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """DROP TABLE ODETAIL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """DROP TABLE ODETAIL1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # NOT CASESPECIFIC
    stmt = """CREATE TABLE T (a char(10) NOT CASESPECIFIC,
b char(10)) NO PARTITION;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """INSERT INTO T values ('a', 'A');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """SELECT * from T where a = 'A';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)

    stmt = """SELECT * from T where a = 'A' (not casespecific);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)

    stmt = """SELECT * from T where b = 'A';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)

    stmt = """SELECT * from T where b = 'A' (not casespecific);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)

    stmt = """DROP TABLE T;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # CREATE TABLE AS
    stmt = """CREATE TABLE t1 (a int, b int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)   

    stmt = """create table t0 no partition as select a,b from t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 0)

    stmt = """create table t2 no partition as select a+1 as c from t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """create table t_err no partition as select a+1 from t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)    

    stmt = """create table t3(a int) no partition as select b from t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 0)

    stmt = """create table t_err(a char(10)) no partition as select a+1 b from t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)

    stmt = """create table t4(c,d) no partition as select a,b from t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 0)

    stmt = """create table t_err(a int) no partition as select b,c from t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)

    stmt = """CREATE TABLE t5 (c1 int not null primary key, c2 char(50));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output);

    stmt = """CREATE TABLE t6 (c1 int, c2 char (50) UPSHIFT NOT NULL) no partition AS SELECT * FROM t5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 0)

    stmt = """DROP TABLE t0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """DROP TABLE t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """DROP TABLE t2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """DROP TABLE t3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """DROP TABLE t4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """DROP TABLE t5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """DROP TABLE t6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def test004(desc="""create view/drop view"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create table t (a int, b int default null, c int default null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # should work
    stmt = """create view v1 as select a, b, c from t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop view v1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # should fail, 2 columns with the same name
    stmt = """create view v_err as select a, a from t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1080')

    # should fail, if we give the 2nd column a different name
    stmt = """create view v2 as select a, a as new_a from t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop view v2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # [FIRST/ANY n] is not allowed for a view
    stmt = """create view v_err as select [any 1] * from t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4103')

    stmt = """create view v_err as select [first 1] * from t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4103')

    stmt = """create view v_err as select [last 1] * from t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4103') 

    # ORDER BY column num
    stmt = """create view v3 as select * from t order by 1 asc, 2 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop view v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # ORDER BY column name
    stmt = """create view v4 as select * from t order by c, b, a desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop view v4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # view dose not allow access mode after ORDER BY
    stmt = """create view v_err as select * from t order by 1 asc, 2 desc for read committed access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    # WITH CHECK OPTION
    stmt = """create view v5 as select a from t where a < 10 with check option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # where a < 10 is true, should be allowed
    stmt = """insert into v5 values (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    # where a < 10 is false, should return a check option error
    stmt = """insert into v5 values (11);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8105')

    # should be 1 row
    stmt = """select * from v5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)

    # should be 1 row
    stmt = """select * from t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)

    # should be 1 row deleted
    stmt = """delete from v5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)

    # should be 0 row
    stmt = """select * from v5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)

    # should be 0 row
    stmt = """select * from t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)

    stmt = """drop view v5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    # Drop view
    # RESTRICT|CASCADE
    stmt = """create view v6 as select * from t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create view v7 as select * from v6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # should see error, default is RESTRICT
    stmt = """drop view v6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1047')

    # should see error with RESTRICT
    stmt = """drop view v6 RESTRICT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1047')

    # shuld drop the view
    stmt = """drop view v6 CASCADE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table t cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #-------------------------------------------------------------------------
    # Examples
    #-------------------------------------------------------------------------
    stmt = """create table employee (salary int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # Not allowed, column 1 is unnamed.
    stmt = """create view v_err as select max(salary), avg(salary) as average_slary from employee;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1099')

    stmt = """drop table employee;""";
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table t (a int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into t values (1),(2),(3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)

    stmt = """create table t1 (a int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
  
    stmt = """create view v1 as select a from t order by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from v1 x, v1 y;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 9)

    stmt = """insert into t1 select * from v1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)
 
    # syntax error at that order by.
    stmt = """select * from (select a from t order by a) x, (select a from t order by a) y;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """drop view v1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create view v2 as select * from t order by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from v2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)

    stmt = """drop view v2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """create table t2 (a int, b int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into t2 values (1,1),(2,2),(3,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)

    stmt = """create view v3 as select a,b from t2 order by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from v3 order by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
 
    stmt = """drop view v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create view v4 as select a,b from t2 order by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create view v5 as select a,b from v4 order by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from v5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)

    stmt = """drop view v5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop view v4 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table t cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table t1 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table t2 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #-------------------------------------------------------------------------
    stmt = """create table odetail (ordernum int, qty_ordered int, partnum int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table parts (partnum int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """CREATE VIEW MYVIEW1 AS SELECT ordernum, qty_ordered FROM ODETAIL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """CREATE VIEW MYVIEW2
(v_ordernum, t_partnum) AS
SELECT v.ordernum, t.partnum
FROM MYVIEW1 v, ODETAIL t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """CREATE VIEW MYVIEW4
(v_ordernum, v_partnum) AS
SELECT od.ordernum, p.partnum
FROM ODETAIL OD INNER JOIN PARTS P
ON od.partnum = p.partnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop view MYVIEW2 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop view MYVIEW4 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table odetail cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table parts cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #-------------------------------------------------------------------------
    stmt = """create table vp0(a integer not null, b integer, primary key(a));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table vp1(a integer not null, c integer, primary key(a));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table vp2(a integer not null, d integer, primary key(a));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create view vp(a,b,c,d) as
select vp0.a, b, c, d
from vp0 left outer join vp1 on vp0.a=vp1.a
left outer join vp2 on vp0.a=vp2.a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select a, b from vp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)

    stmt = """select a, c from vp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)

    stmt = """select d from vp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)

    stmt = """drop view vp cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table vp0 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table vp1 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table vp2 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def test005(desc="""invoke"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = 'create table "t0" (a int);'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table t1 (a int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create index i1 on t1 (a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create view v as select * from t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = 'invoke "t0";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """invoke t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # use the full name
    stmt = """invoke """ + defs.my_schema + """.t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """invoke i1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, "4082")

    stmt = """invoke v;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop view v;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = 'drop table "t0";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def test006(desc="""TBD"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    _testmgr.testcase_end(desc)

