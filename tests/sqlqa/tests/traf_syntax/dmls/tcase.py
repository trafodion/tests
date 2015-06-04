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
    
def test001(desc="""delete"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # [FOR] access-option ACCESS
    stmt = """create table t (a int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into t values (1),(2),(3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)

    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """delete from t where a < 3 for read committed access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)

    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """delete from t where a < 3 read committed access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)

    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # only support read committed for DELETE
    stmt = """delete from t where a < 3 for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3140')

    stmt = """drop table t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #---------------------------------------------------------------------------
    # Examples
    #---------------------------------------------------------------------------
    stmt = """create table job (a int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into job values (1),(2),(3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)

    stmt = """DELETE FROM job;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)

    stmt = """drop table job;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table orders (salesrep int, custnum int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into orders values (220, 1),(220, 2),(220, 1234);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)

    stmt = """DELETE FROM orders
WHERE salesrep = 220 AND custnum <> 1234;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)

    stmt = """drop table orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table partsupp (suppnum int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into partsupp values (1),(2),(3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)

    stmt = """create table supplier (suppnum int, state char(10));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into supplier values (1, 'TEXAS'),(2, 'CALIFORNIA'),(3, 'UTAH');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)

    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """DELETE FROM partsupp
WHERE suppnum IN
(SELECT suppnum FROM supplier
WHERE state <> 'TEXAS');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)

    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """DELETE FROM partsupp
WHERE suppnum NOT IN
(SELECT suppnum FROM supplier
WHERE state = 'TEXAS');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)

    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table partsupp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table supplier;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table table1 (a int, b int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into table1 values (1,1),(2,2),(201,201),(202,202),(203,203);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """delete from table1 where a in
(select a from table1 where b > 200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)

    stmt = """drop table table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def test002(desc="""insert"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create table t0 (a int default 100, b int default 100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table t1 (a int no default, b int default 100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # DEFAULT VALUES
    stmt = """insert into t0 default values;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    # NULL as value
    stmt = """insert into t1 values (1, cast (null as int));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    # query-expr, order-by-clause, and access-clause
    # NOTE: among [(target-col-list)], [order-by-clause], and [access-clause],
    # only able to use  2 of them.  Using all 3 of them returns an error now.
    # But this is the same bahvior as before.  The reference manual needs to 
    # be updated.
    stmt = """insert into t0 select * from t1 where a > 1000 order by a, b asc for read committed access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 0)

    stmt = """insert into t0 (a, b) select * from t1 where a > 1000 order by a, b asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 0)

    stmt = """insert into t0 (a, b) select * from t1 where a > 1000 for read committed access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 0)

    # NOTE: The Trafodion reference manual describes the syntax as 
    #   INSERT INTO table [(target-col-list)] insert-source
    #   target-col-list is:
    #   colname [,colname]...
    #   insert-source is:
    #   query-expr [order-by-clause] [access-clause] | DEFAULT VALUES
    # Among the three options in the syntax: [(target-col-list)], 
    # [order-by-clause], and [access-clause].  Using only 2 out of 3 works
    # fine, but putting all 3 together returns a syntax error now.
    # This is the same behavior as before.  The reference manual needs to
    # be updated.
    stmt = """insert into t0 (a, b) select * from t1 where a > 0 order by a, b asc for read committed access;"""
    output = _dci.cmdexec(stmt)
    # _dci.expect_inserted_msg(output, 0)
    _dci.expect_error_msg(output)

    # should see an error.  Can't specify column list with default values.
    stmt = """insert into t0 (a, b) default values;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
 
    # should see error as colun a as no default
    stmt = """insert into t1 default values;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4024')

    stmt = """drop table t0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # EXAMPLES
    stmt = """create table customer (custnum int, custname char(20), street char(40), city char(20), state char(10), postcode char(10), credit char(20) default 'C1');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create view custlist as select custnum, custname, street, postcode from customer;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table job (id int, title char(20));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table project (c1 int, c2 char(20), c3 date, c4 timestamp, c5 interval DAY);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table supplier (suppnum int, custname char(20), street char(40), postcode char(10));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into supplier values (10, 'CUSTOMER 1', 'University Ave', '95122');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """INSERT INTO customer
VALUES (4777, 'ZYROTECHNIKS', '11211 40TH ST.',
'BURLINGTON', 'MASS.', '01803', 'A2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """SELECT * FROM customer WHERE custnum = 4777;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)

    stmt = """INSERT INTO customer
(custnum, custname, street, city, state, postcode)
VALUES (1120, 'EXPERT MAILERS', '5769 N. 25TH PL',
'PHOENIX', 'ARIZONA', '85016');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """SELECT * FROM customer WHERE custnum = 1120;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    # also make sure that the default value for CREDIT is there.
    _dci.expect_str_token(output, 'C1')

    stmt = """INSERT INTO job
VALUES (100,'MANAGER'),
(200,'PRODUCTION SUPV'),
(250,'ASSEMBLER'),
(300,'SALESREP'),
(400,'SYSTEM ANALYST'),
(420,'ENGINEER'),
(450,'PROGRAMMER'),
(500,'ACCOUNTANT'),
(600,'ADMINISTRATOR'),
(900,'SECRETARY');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """INSERT INTO project
VALUES (1000, 'SALT LAKE CITY', DATE '2007-10-02',
TIMESTAMP '2007-12-21 08:15:00.00', INTERVAL '30' DAY);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """INSERT INTO custlist
(SELECT * FROM supplier
WHERE suppnum = 10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """UPDATE customer
SET credit = 'A4'
WHERE custnum = 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)    

    stmt = """drop view custlist;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table customer;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table job;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table project;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table supplier;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # Self-Referencing inserts
    stmt = """create table table1 (pk int, b int, c int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table table2 (pk int, a int, b int, c int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into table table1 values (1,1,1),(2,2,2),(17,17,17),(18,18,18);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into table table2 values (1,1,1,1),(2,2,2,2),(17,17,17,17),
(20,20,20,20);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """set param ?val 100;"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into table1 select pk+?val, b, c from table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """insert into table1
select a+16, b, c from table2 where table2.b not in
(select b from table1 where a > 16);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """drop table table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table table2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def test003(desc="""merge"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # Examples
    stmt = """create table t (a int primary key not null, b int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into t values (0,0),(10,10),(40,40);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)

    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """MERGE INTO t ON a = 10
WHEN MATCHED THEN UPDATE SET b = 20
WHEN NOT MATCHED THEN INSERT VALUES (10, 30);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from t where b = 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)

    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """MERGE INTO t ON a = 10
WHEN MATCHED THEN UPDATE SET b = 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from t where b = 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)

    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """MERGE INTO t ON a = 100000
WHEN NOT MATCHED THEN INSERT VALUES (80, 80);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from t where b = 80;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)

    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE TABLE t1 (a int not null, b int not null, primary key(a));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # Shuld see error. The key value specified in the on-clause and the 
    # insert-values-list VALUE clause must be the same. This statement is not 
    # allowed
    # NOTE: This example is sited in the Trafodion Reference Manual as 
    # disallowed for the following reason:
    #     "The key value specified in the on-clause and the insert-values-list 
    #     VALUE clause must be the same. This statement is not allowed ...."
    # But it actually works fine in Trafodion.  For now, let's assume that
    # the reference manual is wrong.
    stmt = """MERGE INTO t1 ON a = 10
WHEN NOT MATCHED THEN INSERT VALUES (20, 30);"""
    output = _dci.cmdexec(stmt)
    # _dci.expect_error_msg(output)
    _dci.expect_complete_msg(output)

    # Should see error. On-clause cannot contain a subquery
    stmt = """MERGE INTO t1 ON a = (SELECT a from t)
WHEN NOT MATCHED THEN INSERT VALUES (20, 30);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3241')

    # The optional WHERE predicate in the when-matched clause cannot contain
    # a subquery or an aggregate function. These statements are not allowed:
    stmt = """MERGE INTO t1 ON a = 10
WHEN MATCHED THEN UPDATE SET b=4 WHERE b=(SELECT b FROM t)
WHEN NOT MATCHED THEN INSERT VALUES (10,30);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3241')

    stmt = """MERGE INTO t1 ON a=10
WHEN MATCHED THEN UPDATE SET b=4 WHERE b=MAX(b)
WHEN NOT MATCHED THEN INSERT VALUES (10,30);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3241')

    # The UPDATE SET clause in a MERGE statement cannot contain a subquery. T
    # his statement is not allowed:
    stmt = """MERGE INTO t1 ON a = 1 WHEN MATCHED THEN UPDATE SET b = (SELECT a FROM t1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3241')

    # The insert-values-list clause in a MERGE statement cannot contain a 
    # subquery. This statement is not allowed:
    stmt = """MERGE INTO t ON a = 1 WHEN NOT MATCHED THEN INSERT VALUES ((SELECT a FROM t1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3241')

    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # Use of a non-unique on-clause for a MERGE update is allowed only if 
    # no INSERT clause exists.
    stmt = """MERGE INTO t1 USING (SELECT a,b FROM t) x ON t1.a=x.a
WHEN MATCHED THEN UPDATE SET b=x.b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # Use of a non-unique on-clause for a MERGE delete is allowed only if no 
    # INSERT clause exists.
    stmt = """MERGE INTO t1 USING (SELECT a,b FROM t) x ON t1.a=x.a
WHEN MATCHED THEN DELETE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # Merge from one table to another
    stmt = """MERGE INTO t1 USING (SELECT a FROM t) as Z(X) ON a = Z.X
WHEN MATCHED THEN DELETE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # last example
    stmt = """MERGE INTO t USING
(SELECT * FROM t1) z(a,b) on a = z.a
WHEN MATCHED THEN UPDATE SET b = z.b
WHEN NOT MATCHED THEN INSERT VALUES (z.a, z.b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # The column being updated cannot be a clustering key
    stmt = """create table t2 (a int not null primary key, b int) store by (a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into t2 values (1,1),(2,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    # Column being updated cannot be a clustering key.  a is a clustering key
    stmt = """merge into t2 on b = 1 when matched then update set a = 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
 
    stmt = """drop table t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """drop table t2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    _testmgr.testcase_end(desc)

def test004(desc="""select"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create table T (a int, b int, c int, d int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into T values (1,1,1,100),(2,2,2,100),(3,3,3,200),(4,4,4,200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """create table T1 (a int, b int, c int, d int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into T1 values (1,1,1,100),(2,2,2,100),(3,3,3,200),(4,4,4,200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
 
    stmt = """SELECT sum(distinct a), count(distinct b), avg(distinct c)
from T group by d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)

    stmt = """SELECT sum(distinct a), count(distinct a), avg(distinct a)
from T group by d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)

    stmt = """SELECT sum(distinct a), avg(distinct b), sum(c)
from T group by d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)

    stmt = """SELECT A FROM T1 UNION SELECT B FROM T ORDER BY A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    # should see error. This SELECT statement is incorrect because the ORDER 
    # BY clause does not follow the final SELECT statement:
    stmt = """SELECT A FROM T1 ORDER BY A UNION SELECT B FROM T2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    # should see error. the subquery (SELECT B FROM T2...) is processed first, 
    # the ORDER BY clause does not follow the final SELECT.
    stmt = """SELECT A FROM T1 UNION (SELECT B FROM T2 ORDER BY A);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """SELECT a+1 FROM t GROUP BY a+1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4);

    stmt = """SELECT cast(a AS int) FROM t GROUP BY cast(a AS int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4);

    stmt = """SELECT a+1 FROM t GROUP BY 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4);

    # Error, unsupported
    stmt = """SELECT sum(a) FROM t GROUP BY sum(a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197');

    # Error, unsupported
    stmt = """SELECT (SELECT a FROM t1) FROM t GROUP BY (SELECT a FROM t1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output);

    # Error, unsupported
    stmt = """SELECT a+1 FROM t GROUP BY 1+a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197');

    stmt = """drop table T;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table T1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table TABLE1 (a int, b int, c int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into TABLE1 values (1,1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """create table TABLE2 as select * from TABLE1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """create table TABLE3 as select * from TABLE1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """(SELECT * FROM TABLE1 UNION ALL
SELECT * FROM TABLE2) UNION ALL SELECT * FROM TABLE3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)

    stmt = """SELECT * FROM TABLE1 UNION ALL
(SELECT * FROM TABLE2 UNION ALL SELECT * FROM TABLE3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)

    stmt = """drop table TABLE1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table TABLE2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table TABLE3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table employee (jobcode int, empnum int, deptnum int, departmentid int, first_name char(20), last_name char(20), salary float);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into employee values (600,1042,1500,1500,'JONATHAN','MITCHELL',3200.00),(600,1043,1500,1500,'JOIMMY','SCHEIDER',26000.00),(900,1044,2500,2500,'MIRIAM','KING',18000.00),(900,1045,1000,1000,'SUE','CRAMER',19000.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 4)

    stmt = """create table department (departmentid int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into department values (1000),(1500),(2500);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """create table job (jobcode int, jobdesc char(20));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into job values (600, 'SALESREP'),(900,'ENGINEER'),(1200,'SECRETARY');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)

    stmt = """create table job_corporate as select * from job;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """create table dept (deptnum int, deptname char(20), location char(20));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into dept values (1500, 'SOFTWARE', 'CALIFORNIA'),(2000, 'IT', 'CALIFORNIA'),(2500, 'HARDWARE', 'TEXAS'),(3000, 'SALES', 'HAWAII');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 4)

    stmt = """create table odetail (partnum int, price float, ordernum int, qty_ordered int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into odetail values (212, 2450.00, 5567, 3),(244, 2500.00, 4921, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """create table parts (partnum int, qty int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into parts values (212, 3525),(244, 4426);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)

    stmt = """create table orders (custnum int, ordernum int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into orders values (1111, 1111),(2222, 2222);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)

    stmt = """create table customer (custnum int, state char(10));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into customer values (1111,'CALIFORNIA'),(2222,'TEXAS');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)

    stmt = """SELECT jobcode, deptnum, first_name, last_name, salary
FROM employee
WHERE jobcode > 500 AND deptnum <= 3000
ORDER BY jobcode;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)

    stmt = """SELECT jobcode, AVG(salary)
FROM employee
WHERE jobcode > 500 AND deptnum <= 3000
GROUP BY jobcode
ORDER BY jobcode;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)

    stmt = """SELECT jobdesc, first_name, last_name, salary
FROM employee E, job J
WHERE E.jobcode = J.jobcode AND
E.jobcode IN (900, 300, 420);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)

    stmt = """SELECT E.jobcode, E.deptnum, MIN (salary), MAX (salary)
FROM employee E,
dept D, job J
WHERE E.deptnum = D.deptnum AND E.jobcode = J.jobcode
AND E.jobcode IN (900, 300, 420)
GROUP BY E.jobcode, E.deptnum
ORDER BY 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)

    stmt = """SELECT OD.*, P.*
FROM odetail OD INNER JOIN parts P
ON OD.partnum = P.partnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """SELECT empnum, first_name, last_name, deptname, location, jobdesc
FROM employee e LEFT JOIN dept d ON e.deptnum = d.deptnum
LEFT JOIN job j ON e.jobcode = j.jobcode
ORDER BY empnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """SELECT * FROM job UNION SELECT * FROM job_corporate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """SELECT *
FROM employee
FULL OUTER JOIN
department
ON employee.DepartmentID = department.DepartmentID;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """SELECT OD.ordernum, SUM (qty_ordered * price)
FROM parts P, odetail OD
WHERE OD.partnum = P.partnum AND OD.ordernum IN
(SELECT O.ordernum
FROM orders O, customer C
WHERE O.custnum = C.custnum AND state = 'CALIFORNIA')
GROUP BY OD.ordernum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """SELECT OD.ordernum, SUM (qty_ordered * price)
FROM parts P, odetail OD
WHERE OD.partnum = P.partnum AND OD.ordernum IN
(SELECT O.ordernum
FROM orders O
WHERE custnum IN
(SELECT custnum
FROM customer
WHERE state = 'CALIFORNIA'))
GROUP BY OD.ordernum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """SELECT empnum, first_name, last_name, salary,
CAST(salary * 100 / (SELECT SUM(salary) FROM employee)
AS NUMERIC(4,2))
FROM employee
ORDER BY salary, empnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """drop table employee;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    stmt = """drop table job;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table job_corporate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """drop table dept;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table odetail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table parts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table customer;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table department;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
 
    _testmgr.testcase_end(desc)

def test005(desc="""update"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create table t (a int, b int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into table t values (1,1),(2,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """update t set (a, b) = (3, 3) where a = 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)

    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """update t set (a, b) = (null, null) where a = 1 for read committed access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)

    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """update t set b = null where a = 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)

    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #-------------------------------------------------------------------------
    # Examples
    stmt = """create table mytable (a int, b int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into mytable values (11, 12);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = """update mytable set b = 20 where a > 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)

    stmt = """select * from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    _dci.expect_str_token(output, '11')
    _dci.expect_str_token(output, '20')

    stmt = """drop table mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #-------------------------------------------------------------------------
    stmt = """create table t (a int, b int, c int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table x (r int, t int, s int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table t1 (a int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table z (x int, y int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table a (x int, y int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # Error, mismatched number of columns
    stmt = """UPDATE t SET (a,b)=(10,20,30);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4023')

    # Error, mismatched number of columns
    stmt = """UPDATE t set (b,c)=(SELECT r,t,s FROM x);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4023')

    # Error, If multi-column update syntax is specified and the right side 
    # contains a subquery, only one element, the subquery, is not allowed.
    stmt = """UPDATE t SET (a,b)=(10, (SELECT a FROM t1));"""
    output = _dci.cmdexec(stmt)
    # _dci.expect_error_msg(output, '3242')
    _dci.expect_updated_msg(output, '0')

    # Error, More than one subquery is not allowed if multiple-column syntax is used.
    stmt = """UPDATE t SET (a,b)=(SELECT x,y FROM z), (c,d)=(SELECT x,y FROM a));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """drop table t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table z;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #-------------------------------------------------------------------------
    stmt = """create table orders(ordernum int, deliv_date date);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into orders values (200300, date '1999-12-12');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = """create table customer (custnum int, credit char(10));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into customer values (21, 'C1');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = """create table employee (deptnum int, salary float);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
  
    stmt = """insert into employee values (1000, 110000.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = """create table dept (deptnum int, location char(20));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into dept values (1000, 'CHICAGO');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = """UPDATE orders
SET deliv_date = DATE '2008-05-02'
WHERE ordernum = 200300;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)

    stmt = """UPDATE customer
SET credit = 'A1'
WHERE custnum IN (21, 3333, 324);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)

    stmt = """UPDATE customer
SET credit = 'C1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)

    stmt = """UPDATE employee
SET salary = salary * 1.1
WHERE deptnum IN
(SELECT deptnum FROM dept
WHERE location = 'CHICAGO');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)

    stmt = """drop table orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table customer;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table employee;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table dept;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #-------------------------------------------------------------------------
    # Self-referencing update.
    stmt = """create table table3 (a int, b int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into table3 values (1,1),(201,201);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)

    stmt = """UPDATE table3 SET b = b + 2000 WHERE a, b =
(SELECT a, b FROM table3 WHERE b > 200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)

    stmt = """drop table table3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def test006(desc="""upsert"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # update vs insert
    stmt = """create table t0 (a int not null primary key, b int, c int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into t0 values (1,1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = """create table t1 (a int, b int, c int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into t1 values (1,1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    # a is a primary key (the value 1 already exists), so this should be an 
    # update
    stmt = """upsert into t0 values (1,2,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from t0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)

    # a is not a primary key, (the row (1,2,2) does not exist) so this should 
    # be an insert.
    stmt = """upsert into t1 values (1,2,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)

    stmt = """drop table t0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #-------------------------------------------------------------------------
    # Examples
    stmt = """create table parts (partnum int not null primary key, price int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into parts values (244,10000),(245,20000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """create table odetail (partnum int, unit_price int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into odetail values (244, 90000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """UPSERT INTO parts (partnum, price) SELECT partnum, unit_price
FROM odetail WHERE partnum = 244;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # partnum is a primary key, this should be an update, remain 2 rows.
    # (244, 10000) should be updated to (244,90000)
    stmt = """select * from parts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)
    _dci.unexpect_any_substr(output, '10000')
    _dci.expect_str_token(output, '90000')

    stmt = """drop table parts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table odetail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #-------------------------------------------------------------------------
    stmt = """create table employee (l_n char(30), f_n char(10));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table employee_europe (last_name char(20), first_name char(20));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """upsert into employee_europe values ('Jones','Mary');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """UPSERT INTO employee SELECT * FROM employee_europe;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from employee;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)

    stmt = """drop table employee;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table employee_europe;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
 
    #--------------------------------------------------------------------------
    stmt = """create table dept (deptnum int, deptname char(20), manager int, id int, location char(20));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """UPSERT INTO dept VALUES (3500,'CHINA SALES',111,3000,'HONG KONG');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from dept;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)

    stmt = """UPSERT INTO dept (deptnum, deptname, manager)
VALUES (3600,'JAPAN SALES', 996);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from dept;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)

    stmt = """drop table dept;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def test007(desc="""TBD"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    _testmgr.testcase_end(desc)
