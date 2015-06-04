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
    
    stmt = """CREATE TABLE emp
(
LAST_NAME                      CHAR(10) DEFAULT NULL
, FIRST_NAME                     CHAR(10) DEFAULT NULL
, DEPT_NUM                       NUMERIC( 4, 0) DEFAULT NULL
, SALARY                         NUMERIC( 8, 2) DEFAULT NULL
, MARITAL_STATUS                 NUMERIC( 1, 0) DEFAULT NULL
, HIRE_DATE			   DATE
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO emp
values
( 'CLARK' , 'DINAH',9000, 37000.00, 3, DATE '1998-04-03');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO emp
values ( 'CRINAR', 'JESSICA', 3500, 39500.00, 2, DATE '1999-05-06');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO emp
values ('GREEN','ROGER',  9000, 175500.00, 2, DATE '2000-01-02');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO emp
values ('HOWARD', 'JERRY', 1000, 65000.00, 1, DATE '2002-12-11');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
