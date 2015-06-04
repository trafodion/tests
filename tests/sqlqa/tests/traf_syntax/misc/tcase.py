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
    
def test001(desc="""execute"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create table employee (empnum int, first_name char(10), last_name char(10), deptnum int, jobcode int, salary float);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into employee values (232, 'THOMAS', 'SPINNER', 4000, 450, 45000.00), (75, 'TIM', 'WALKER', 3000, 300, 32000.00), (89, 'PETER', 'SMITH', 3300, 300, 37000.40);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """prepare findemp from
select * from employee
where salary > ?sal and jobcode = ?job;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """set param ?sal 40000.00;"""
    output = _dci.cmdexec(stmt)

    stmt = """set param ?job 450;"""
    output = _dci.cmdexec(stmt)

    stmt = """execute findemp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)

    stmt = """set param ?sal 20000.00;"""
    output = _dci.cmdexec(stmt)

    stmt = """set param ?job 300;"""
    output = _dci.cmdexec(stmt)

    stmt = """execute findemp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)

    stmt = """prepare findemp from
select * from employee
where salary > ? and jobcode = ?;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute findemp using 40000.00,450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)

    stmt = """execute findemp using 20000.00, 300;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)

    stmt = """prepare findemp from
select * from employee
where salary > ? and jobcode = ?;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """set param ?Salary 40000.00;"""
    output = _dci.cmdexec(stmt)

    stmt = """execute findemp using ?Salary, 450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)

    stmt = """drop table employee;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def test002(desc="""explain"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create table region (
r_regionkey         int                not null not droppable,
r_name              char(25)           not null not droppable,
r_comment           varchar(152)       not null not droppable,
primary key (r_regionkey)  not droppable)
store by primary key;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """explain options 'f' select * from region;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """PREPARE q FROM SELECT * FROM REGION;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """EXPLAIN options 'f' q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # options 'n'
    stmt = """explain options 'n' select * from region;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # options 'e'
    stmt = """explain options 'e' select * from region;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # no options
    stmt = """explain select * from region;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from region;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)

    qid = _dci.get_current_qid()
  
    # FOR QID
    # The document is a bit vague on if this feature is supported.  It says:
    # "Trafodion SQL provides the ability to capture an EXPLAIN plan for a 
    # query at any time while the query is running with the FOR QID option. 
    # By default, this behavior is disabled for a Trafodion database session."
    # The following statement cores mxssmp right now.  Skip it until it is
    # fully supported.
    # stmt = """explain for qid """ + qid + """;"""
    # output = _dci.cmdexec(stmt)
    # only want to make sure that this is not a syntax error
    # _dci.unexpect_error_msg(output, '15001')
    # _dci.expect_complete_msg(output)

    stmt = """drop table region;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def test003(desc="""get"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create table mytable (a int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create view myview as select * from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """get schemas;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _dci.expect_any_substr(output, defs.w_schema, True);

    stmt = """get schemas in catalog """ + defs.w_catalog + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _dci.expect_any_substr(output, defs.w_schema, True);

    stmt = """get schemas in catalog doesnotexist;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1002')

    stmt = """get tables;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _dci.expect_any_substr(output, 'mytable', True);

    stmt = """get tables in schema """ + defs.w_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _dci.expect_any_substr(output, 'mytable', True);

    stmt = """get tables in schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _dci.expect_any_substr(output, 'mytable', True);

    # No error message even if the schema does not exist.
    stmt = """get tables in schema doesnotexist;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """get views;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _dci.expect_any_substr(output, 'myview', True);

    stmt = """get views in schema """ + defs.w_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _dci.expect_any_substr(output, 'myview', True);

    stmt = """get views in schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _dci.expect_any_substr(output, 'myview', True);

    # No error message even if the schema does not exist.
    stmt = """get views in schema doesnotexist;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """get views on table """ + defs.w_schema + """.mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _dci.expect_any_substr(output, 'myview', True);

    stmt = """get views on table """ + defs.w_catalog + """.""" + defs.w_schema + """.mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _dci.expect_any_substr(output, 'myview', True);

    # No error message even if the schema does not exist.
    stmt = """get views on table doesnotexist;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop view MYVIEW;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table MYTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def test004(desc="""prepare"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # Examples
    stmt = """create table employee (jobcode int, salary float);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into employee values (450,32000.00),(450,33000.50),(450,40000.00),(450,32000.00),(450,45000.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)

    # table does not exist
    stmt = """prepare empsal from
select salary from doesnotexist
where jobcode = 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')

    stmt = """prepare findsal from
select salary from employee
where jobcode = ?;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """execute findsal using 450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 5)

    stmt = """prepare findsal from
select salary from employee
where jobcode = ?job;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """set param ?job 450;"""
    output = _dci.cmdexec(stmt)

    stmt = """execute findsal;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 5)

    stmt = """drop table employee;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def test005(desc="""set schema"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = 'create schema "myschema";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = 'set schema "myschema";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table t (a int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """invoke t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _dci.expect_any_substr(output, 'myschema', True) 

    stmt = """drop table t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = 'drop schema "myschema" cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # Spaces actually are not allowed in Trafodion.  You will get an error
    # at the table creation time.  This is different from SQ.
    stmt = 'create schema "my schema";'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1422')

    stmt = 'set schema "my schema";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table t (a int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)

    # reset the schema
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def test006(desc="""table"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create table job (code int, description char(20));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
 
    stmt = """insert into job values (100,'MANAGER'),(200,'PRODUCTION SUPV'),(250,'ASSEMBLER'),(300,'SALESREP'),(400,'SYSTEM ANALYST'),(420,'ENGINEER'),(450,'PROGRAMMER'),(500,'ACCOUNTANT'),(600,'ADMINISTRATOR'),(900,'SECRETARY');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 10)
 
    stmt = """create view v as select * from job;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """table job;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
 
    stmt = """table """ + defs.w_schema + """.job;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """table """ + defs.w_catalog + """.""" + defs.w_schema + """.job;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """table v;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """table """ + defs.w_schema + """.v;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """table """ + defs.w_catalog + """.""" + defs.w_schema + """.v;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # Error, table doe not exist
    stmt = """table doesnotexist;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')

    stmt = """drop view v;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table job;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def test007(desc="""update statistics"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create table t (a int, b int, c int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into t values (1,1,1),(2,2,2),(3,3,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)

    # CLEAR
    stmt = """update statistics for table t clear;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # I don't think this is supported.  Comment the entire section out for now.
    # [CREATE|REMOVE SAMPLE persistent-sample-option]
    # r rows
    # invalid sample, must r>0
    ## stmt = """update statistics for table t create sample -1 rows;"""
    ## output = _dci.cmdexec(stmt)
    ## _dci.expect_error_msg(output, '9204')

    # invalid sample, must r rows be > 0
    ## stmt = """update statistics for table t create sample -1 rows;"""
    ## output = _dci.cmdexec(stmt)
    ## _dci.expect_error_msg(output, '9204')

    # invalid sample, must r rows be > 0
    ## stmt = """update statistics for table t remove sample -1 rows;"""
    ## output = _dci.cmdexec(stmt)
    ## _dci.expect_error_msg(output, '9204')

    # invalid sample, must r rows be > 0
    ## stmt = """update statistics for table t create sample 0 rows;"""
    ## output = _dci.cmdexec(stmt)
    ## _dci.expect_error_msg(output, '9204')

    # invalid sample, must r rows be > 0
    ## stmt = """update statistics for table t remove sample 0 rows;"""
    ## output = _dci.cmdexec(stmt)
    ## _dci.expect_error_msg(output, '9204')

    # TODO: Does TR supports persistent sample table feature at all?  This
    # fails on TR now.
    ## stmt = """update statistics for table t create sample 1 rows;"""
    ## output = _dci.cmdexec(stmt)
    ## _dci.expect_complete_msg(output)

    # TODO: Does TR supports persistent sample table feature at all?  This
    # fails on TR now.
    ## stmt = """update statistics for table t remove sample 1 rows;"""
    ## output = _dci.cmdexec(stmt)
    ## _dci.expect_complete_msg(output)

    # TODO: Does TR supports persistent sample table feature at all?  This
    # fails on TR now.
    ## jstmt = """update statistics for table t create sample 3 rows;"""
    ## output = _dci.cmdexec(stmt)
    ## _dci.expect_complete_msg(output)

    # TODO: Does TR supports persistent sample table feature at all?  This
    # fails on TR now.
    ## stmt = """update statistics for table t remove sample 3 rows;"""
    ## output = _dci.cmdexec(stmt)
    ## _dci.expect_complete_msg(output)

    # invalid sample n rows, table only has 3 rows
    ## stmt = """update statistics for table t create sample 4 rows;"""
    ## output = _dci.cmdexec(stmt)
    ## _dci.expect_error_msg(output, '9204')

    # invalid sample n rows, table only has 3 rows
    ## stmt = """update statistics for table t remove sample 4 rows;"""
    ## output = _dci.cmdexec(stmt)
    ## _dci.expect_error_msg(output, '9204')

    # ALL
    ## stmt = """update statistics for table t create sample all;"""
    ## output = _dci.cmdexec(stmt)
    ## _dci.expect_complete_msg(output)

    ## stmt = """update statistics for table t remove sample all;"""
    ## output = _dci.cmdexec(stmt)
    ## _dci.expect_complete_msg(output)

    # RANDOM percent PERCENT
    # Invalid sample, 0 < perent <= 100
    ## stmt = """update statistics for table t create sample random -1 percent;"""
    ## output = _dci.cmdexec(stmt)
    ## _dci.expect_error_msg(output, '9204')

    # Invalid sample, 0 < perent <= 100
    ## stmt = """update statistics for table t remove sample random -1 percent;"""
    ## output = _dci.cmdexec(stmt)
    ## _dci.expect_error_msg(output, '9204')

    # Invalid sample, 0 < perent <= 100
    ## stmt = """update statistics for table t create sample random 0 percent;"""
    ## output = _dci.cmdexec(stmt)
    ## _dci.expect_error_msg(output, '9204')

    # Invalid sample, 0 < perent <= 100
    ## stmt = """update statistics for table t remove sample random 0 percent;"""
    ## output = _dci.cmdexec(stmt)
    ## _dci.expect_error_msg(output, '9204')

    # TODO: Does TR supports persistent sample table feature at all?  This
    # fails on TR now.
    ## stmt = """update statistics for table t create sample random 99.9 percent;"""
    ## output = _dci.cmdexec(stmt)
    ## _dci.expect_complete_msg(output)

    # TODO: Does TR supports persistent sample table feature at all?  This
    # fails on TR now.
    ## stmt = """update statistics for table t remove sample random 99.9 percent;"""
    ## output = _dci.cmdexec(stmt)
    ## _dci.expect_complete_msg(output)

    # TODO: Does TR supports persistent sample table feature at all?  This
    # fails on TR now.
    ## stmt = """update statistics for table t create sample random 100 percent;"""
    ## output = _dci.cmdexec(stmt)
    ## _dci.expect_complete_msg(output)

    # TODO: Does TR supports persistent sample table feature at all?  This
    # fails on TR now.
    ## stmt = """update statistics for table t remove sample random 100 percent;"""
    ## output = _dci.cmdexec(stmt)
    ## _dci.expect_complete_msg(output)

    # Invalid sample, 0 < perent <= 100
    ## stmt = """update statistics for table t create sample random 101 percent;"""
    ## output = _dci.cmdexec(stmt)
    ## _dci.expect_error_msg(output, '9204')

    # Invalid sample, 0 < perent <= 100
    ## stmt = """update statistics for table t remove sample random 101 percent;"""
    ## output = _dci.cmdexec(stmt)
    ## _dci.expect_error_msg(output, '9204')

    # on-clause clear 
    stmt = """update statistics for table t on a clear;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # on-clause histogram-option
    # invalid niterval, must be 0-10000
    stmt = """update statistics for table t on a generate -1 intervals;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '9204')

    # invalid niterval, must be 0-10000
    stmt = """update statistics for table t on a generate 0 intervals;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '9204')

    stmt = """update statistics for table t on a generate 1 intervals;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """update statistics for table t on a generate 10000 intervals;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # invalid niterval, must be 0-10000
    stmt = """update statistics for table t on a generate 10001 intervals;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '9204')

    # invalid sample, r > 0
    stmt = """update statistics for table t on a sample -1 rows;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '9204')

    # invalid sample, r > 0
    stmt = """update statistics for table t on a sample 0 rows;"""
    output = _dci.cmdexec(stmt)
    # TODO: This actually works?
    # _dci.expect_error_msg(output, '9204')

    stmt = """update statistics for table t on a sample 1000000 rows;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # Invalid sample, 0 < perent <= 100
    stmt = """update statistics for table t on a sample random -1 percent;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '9204')

    # Invalid sample, 0 < perent <= 100
    stmt = """update statistics for table t on a sample random 0 percent;"""
    output = _dci.cmdexec(stmt)
    # TODO: This actually works?
    # _dci.expect_error_msg(output, '9204')

    stmt = """update statistics for table t on a sample random 99.9 percent;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """update statistics for table t on a sample random 100 percent;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # Invalid sample, 0 < perent <= 100
    stmt = """update statistics for table t on a sample random 101 percent;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '9204')

    # column-list
    stmt = """update statistics for table t on a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """update statistics for table t on (a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """update statistics for table t on a to c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """update statistics for table t on (a) to (c);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # column-group-list
    stmt = """update statistics for table t on (a),(a,c),(b,c);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """update statistics for table t on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """update statistics for table t on every column, (a,b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """update statistics for table t on every key;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """update statistics for table t on every key, a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """update statistics for table t on existing column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """update statistics for table t on existing columns;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """update statistics for table t on existing columns, c, b, a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #--------------------------------------------------------------------------
    # Examples
    stmt = """create table employee (jobcode int , empnum int, deptnum int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into employee values (1,1,1),(2,2,2),(3,3,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)

    stmt = """create table dept (a int, b int, c int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into dept values (1,1,1),(2,2,2),(3,3,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)

    stmt = """create table address (number int, street char(10), city char(10), zip int, state char(10), type int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into address values (1, '1st Ave', 'San Jose', 95132, 'CA', 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = """create table demolition_sites(zip int, type int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into demolition_sites values (95132, 1);""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = """UPDATE STATISTICS FOR TABLE employee
ON (jobcode),(empnum, deptnum)
GENERATE 10 INTERVALS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """UPDATE STATISTICS FOR TABLE dept ON EVERY COLUMN;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """UPDATE STATISTICS FOR TABLE address
ON (street), (city), (state), (zip, type);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """UPDATE STATISTICS FOR TABLE demolition_sites
ON (zip, type);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """SELECT COUNT(AD.number), AD.street,
AD.city, AD.zip, AD.state
FROM address AD, demolition_sites DS
WHERE AD.zip = DS.zip AND AD.type = DS.type
GROUP BY AD.street, AD.city, AD.zip, AD.state;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """UPDATE STATISTICS FOR TABLE demolition_sites CLEAR;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """UPDATE STATISTICS FOR TABLE address ON street CLEAR;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table employee;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table dept;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table address;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table demolition_sites;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def test008(desc="""values"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create table t (a int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into t values (1),(2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)

    # An error, rows must have the same number of values
    stmt = """values (1,2,3),(4,5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4126') 

    # An error, subquery can only return 1 row.
    stmt = """values ((select * from t), 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8401')

    stmt = """values ((select * from t where a=1), 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)

    stmt = """values ((select sum(a) from t),1,null),(null,(select count(*) from t),null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)

    # examples
    stmt = """VALUES (1,2,3), (4,5,6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)

    stmt = """VALUES (1+2, 3+4), (5, (select count (*) from t));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    
    stmt = """drop table t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def test009(desc="""language elements"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    #-----------------------------------------------------------------------------
    # support iso88591 & utf8
    stmt = """create table t (a char(10) character set iso88591, b char(10) character set utf8);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into t values ('a','a'),('b','b');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)

    stmt = """drop table t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #-----------------------------------------------------------------------------
    # derived column name, constraints
    stmt = """create table employee (salary float not null primary key);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into employee values (49441.52);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = """SELECT AVG (salary) AS "AVERAGE SALARY" FROM employee;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    _dci.expect_any_substr(output, 'AVERAGE SALARY')

    stmt = """drop table employee;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #-----------------------------------------------------------------------------
    # Correlation names
    stmt = """create table orders (custnum int, ordernum int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into orders values (543, 10000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = """create table customer (custnum int, custname char(20));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into customer values (543, 'HP');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = """SELECT ordernum, custname
FROM orders, customer c
WHERE orders.custnum = c.custnum
AND orders.custnum = 543;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)

    stmt = """drop table orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table customer;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #-----------------------------------------------------------------------------
    # Metadata schema
    stmt = """get tables in schema TRAFODION."_MD_";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def test010(desc="""TBD"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    _testmgr.testcase_end(desc)

