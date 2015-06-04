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

# cr8vals
# JClear
# 1999-04-06
# Setup for the VALUES tests.
#
# test002
# following CQD is added for Highlander R1 QCD-2 build
#control query default POS_NUM_OF_PARTNS '0';

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """CREATE table anywhere (its char (15) not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT into anywhere values ('experimental');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE OK (OK CHAR (5) not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO OK (OK) VALUES ('OK OK');"""
    output = _dci.cmdexec(stmt)
    
    # test003
    stmt = """create table valtb003 (fname char (10) not null not droppable primary key, minit char, lname char (10));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into valtb003 values ('Dolores', 'D', 'Cabeza');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """control query default POS_NUM_OF_PARTNS reset;"""
    output = _dci.cmdexec(stmt)
