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


def test001(desc="""create tables"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = "drop table emp;"
    output = _dci.cmdexec(stmt)

    stmt = "drop table employee;"
    output = _dci.cmdexec(stmt)

    stmt = "drop table testtab;"
    output = _dci.cmdexec(stmt)

    stmt = "drop table timetab;"
    output = _dci.cmdexec(stmt)

    stmt = "drop table atable;"
    output = _dci.cmdexec(stmt)

    stmt = "drop table dtime;"
    output = _dci.cmdexec(stmt)

    stmt = "drop table testtime;"
    output = _dci.cmdexec(stmt)

    stmt = "create table emp(ename varchar(50) not null not droppable ,primary key (ename)) no partitions;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "create table employee(empnum int not null not droppable ,primary key (empnum),empname varchar(50), title varchar(20),salary numeric(7,2) ) no partitions;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table testtab( e_name varchar(20) not null, e_num int not null, e_city char(15),
      e_title varchar(20), e_salary numeric(11,2), e_code smallint, e_date date,
      e_time time,  e_tstamp timestamp, e_long largeint , e_float float,  e_real real,
      e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),
      e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))   attributes extent (1064, 1064), maxextents 755 no partitions;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "create table timetab(e_date date , e_time time, e_tstamp timestamp) no partitions;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table atable(index int not null not droppable , department smallint,pin largeint,name varchar(35),
      id integer,systemcode real, salary float(10),rate  decimal(9,0),hiredate date,
      hiretime time,payday timestamp, primary key (index)) no partitions;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "create table dtime(number integer ,  salary float, monthname varchar(35),hiredate date, hiretime time,payday timestamp) no partitions;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "create table testtime(number integer not null not droppable, primary key (number),salary float, monthname varchar(35),hiredate date, hiretime time,payday timestamp) no partitions;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "insert into emp values('Rajani');"
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = "insert into employee values(5500,'karunappa', 'analyst', 90000);"
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = """insert into testtab values('AAA Computers',
      1234567890,
      'San Francisco',
      'programmer',
      123456789,
      32766,
      date '2001-10-30',
      time '10:10:10',
      timestamp '2001-10-10 10:10:10.00',
      123456789987654321,
      3.40E+37,
      3.0125E+18,
      1.78145E+75,
      8765432.45678,
      8765478.56895,
      987654321.0,
      123456789.0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = "insert into atable values(1,-9,1234567890,'Joe Henrickson',1234567,1.201227E13,65000.5,7784785.0,date '1999-12-10',time '11:59:59',timestamp '2001-01-10 10:45:59');"
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = "insert into atable values(2,null,3214567890,'Rose Smith',9074567,1.209827E13,45456.50,1788323.1,date '1998-12-20',time '11:34:55',timestamp '2000-01-10 10:45:34');"
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = "insert into atable values(3,1,null,'Srinivas Henrickson',1239027,1.201876E13,65111.0,1.23232,date '1999-12-04',time '09:12:22',timestamp '2000-01-01 11:45:22');"
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = "insert into atable values(4,4,9874561230,'Justin',null,1.200227E12,6845670,4333297.2,date '2000-12-04',time '09:59:59',timestamp '2000-12-12 11:33:12');"
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = "insert into atable values(5,-2,3216549870,'Mary Hou',8907667,1.001227E11,75456.00,2.22011,date '1999-12-04',time '10:22:59',timestamp '2001-12-12 11:59:12');  "
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = "insert into atable values(6,3,3698521470,null,8903217,1.101227E11,121212.00,3.3243,date '1999-12-04',time '10:22:59',timestamp '2001-12-12 11:59:12');"
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = "insert into atable values(7,5,7418529630,'Henry Leon',123233,1.211227E13,null,2.3321,date '1999-01-01',time'10:23:24',timestamp '2001-05-12 09:54:59');"
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = "insert into atable values(8,5,9517537893,'Hong Vo',123203,1.211127E11,56000.34,null,date '1999-01-01',time '10:23:24',timestamp '2001-05-12 09:54:59');"
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = "insert into atable values(9,4,9632589630,'Kathy Rose',127833,1.201578E13,63000.97,6.9043,null,time '10:23:24',timestamp '2001-05-12 09:54:59');"
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = "insert into atable values(10,7,1236549630,'Jessica Beth',130833,null,63930.97,2.899343,date '2001-01-01',null, timestamp '2001-05-12 09:54:59');"
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = "insert into atable values(11,2,9874563690,'Louise Parker',9907667,1.205557E11,75456.00,2.22011,date '1999-12-04',time '10:22:59',null);  "
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = "insert into dtime values(1,53429.43,'December',date '1999-12-10',time '11:59:59',timestamp '2001-01-10 10:23:57');"
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = "insert into testtime values(20,98429.43,'August',date '2009-12-12',time '11:42:59',timestamp '2002-01-11 05:59:57');"
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = "insert into testtime values(23,36219.32,'January',date '2009-05-12',time '09:33:59',timestamp '2001-01-25 07:33:57');"
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = "insert into testtime values(53,90469.53,'April',date '2004-03-12',time '11:11:59',timestamp '2006-01-21 11:39:57');"
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = "insert into testtime values(91,15783.72,'October',date '2007-12-02',time '11:42:44',timestamp '2009-01-12 08:59:22');"
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    _testmgr.testcase_end(desc)
