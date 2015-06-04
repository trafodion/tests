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
    if not _testmgr.testcase_begin(_testlist): return
    # ================================
    # Create tables.
    # ================================
    stmt = """create table depart 
( prof     varchar(15)   not null,
namelen  int,
cname    varchar(21)   not null,
clen     int,
cnum     varchar(5)    not null,
prereq   varchar(5),
semester varchar(10)   not null,
credits  int
) no partition;"""
    output = _dci.cmdexec(stmt)
    
    # Note that empA01 differs from empA01 in that two columns
    # in empA02 are varchar while they are char in empA01.
    
    stmt = """create table empA01 
( last_name   varchar(15) not null,
first_name  char(13)   ,
job         varchar(15),
gender      char(8)    ,
salary      int,
dept_num    int
) no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table empA02 
( last_name   varchar(15) not null,
first_name  varchar(13),
job         varchar(15),
gender      varchar(8) ,
salary      int,
dept_num    int
) no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table empA07 
( first_name  varchar(13),
last_name   varchar(15) not null,
job         varchar(15),
gender      varchar(8) ,
salary      int,
dept_num    int,
str         varchar(2)
) no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table emp 
( first_name  varchar(13),
last_name   varchar(15) not null,
job         varchar(15),
gender      varchar(8) ,
salary      int,
dept_num    int,
str         varchar(2)
) no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table emptabl 
( first_name  varchar(13),
last_name   varchar(15),
job         varchar(15),
gender      varchar(8) ,
dept_name   varchar(20),
emp_num     int
) no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table tab1 
( v1 varchar(20)  not null ,
v2 varchar(20),
c1 char(20) not null,
c2 char(20),
i1 int
) no partition ;"""
    output = _dci.cmdexec(stmt)
    
    # Populate table emp used in several test cases with these
    # values.
    
    stmt = """insert into emp values
('shanti', 'aradhyula', 'salesrep', 'female', 60000, 12, 'A');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into emp values
('sulu', 'kapoor', 'manager', 'female', 90000, 13, 'B');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into emp values
('BHAVESH', 'MEHTA', 'ENGINEER', 'MALE', 50000, 14 , 'C');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into emp values
('YUGAL', 'AGGARWAL', 'SYSADMIN', 'MALE', 80000, 14, 'D');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into emp values
('ANANDHI', 'RAMASWAMY', 'PROGRAMMER', 'FEMALE', 50000, 13, 'E');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into emp values
('Kathy', 'Baxter', 'secretary', 'female', 36000, 15, 'F');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into emp values
('steve', 'martin', 'director', 'male', 120000, 13, 'H');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into emp values
('MARIA', 'JOYCE', 'HAIRDRESSER', 'FEMALE', 40000, 16, 'I');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into emp values
(NULL, 'HAUSMANN', 'PROGRAMMER', 'MALE', 52000, 14, 'J');"""
    output = _dci.cmdexec(stmt)
    _testmgr.testcase_end(desc)

