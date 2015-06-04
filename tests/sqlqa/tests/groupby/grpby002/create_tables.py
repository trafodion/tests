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

#control query default POS 'OFF';

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """create table emp1(
last_name char(15) default null,
job_code character varying (25),
responsible varchar(25),
salary numeric(8,2) not null
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Insert into emp1 values('CLARK','Programmer', 'Programming',80000.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert into emp1 values('CRINAR','Analyst', 'Analyse problems',50000.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert into emp1 values('GREEN','Intern', 'Help out',35000.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert into emp1 values('HOWARD','Architect', 'Design',90000.00);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create table emp2(
employee_id smallint not null,
marital_status int,
bonus largeint,
vacation dec,
tax float,
retire real,
code char(1)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Insert into emp2 values(10, 1,1000, 10, 400, 300, 'a');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert into emp2 values(20, 2,1500, 15, 300, 250, 'b');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert into emp2 values(30, 1,1300, 12, 200, 150, 'c');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert into emp2 values(40, 2,1200, 11, 350, 200, 'd');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create table emp3(
employee_id smallint not null,
col1 double precision,
hire_date date,
start_time time,
end_time timestamp,
experience interval year to month,
primary key(employee_id)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Insert into emp3 values(10, 30.00,  DATE '1998-04-03', TIME '08:30:30', TIMESTAMP '2007-06-01:16:30:30', INTERVAL '9-03'  YEAR TO MONTH);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert into emp3 values(20, 25.00,  DATE '1999-05-06', TIME '08:45:00', TIMESTAMP '2007-06-01:16:45:00', INTERVAL '8-01'  YEAR TO MONTH);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert into emp3 values(30, 65.00,  DATE '2000-01-02', TIME '09:00:00', TIMESTAMP '2007-06-01:17:00:00', INTERVAL '7-05'  YEAR TO MONTH);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """Insert into emp3 values(40, 58.00,  DATE '2002-12-11', TIME '09:15:30', TIMESTAMP '2007-06-01:17:15:30', INTERVAL '4-06'  YEAR TO MONTH);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
