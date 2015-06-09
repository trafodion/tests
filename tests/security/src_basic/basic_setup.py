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
from ...lib import gvars
import basic_defs

_testmgr = None
_testlist = []
_dci = None

# Create work_dir in the result directory.
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    # Set up schema
    # user1
    _dci = basic_defs.switch_session_qi_user1()
    
    stmt = """create schema """ + basic_defs.TestVars.test_schema_full + """;"""
    output = _dci.cmdexec(stmt)
    
    # Set SPJ for testing.
    # super
    _dci = basic_defs.switch_session_super_user()
    
    stmt = """set schema """ + basic_defs.TestVars.test_schema_full + """;"""
    output = _dci.cmdexec(stmt)
    
    # create procedure QIN0001 ()
    #  external name 'QIProcs.QIN0001'
    #  external path '/home/SQFQA/SPJRoot/qi_spjs'
    #  language java
    #  parameter style java
    #  no sql
    #  isolate;
    
    # SPJ is now created using a library.
    # No two libraries can point to the same SPJ file, even if the two libraries
    # are in different schemas. All the tests now create the library in the
    # same schema sch_qi_spjlib, and then the procedure is created in its
    # own schema.  The library creation part really only needs to
    # be done once, so it depends on who gets to do it first on the machine.
    # If someone has done it earlier, you will see errors in the following two
    # create statements.  The errors can be ignored.
    stmt = """create schema """ + gvars.test_catalog + """.sch_qi_spjlib;"""
    output = _dci.cmdexec(stmt)
    stmt = """create library """ + gvars.test_catalog + """.sch_qi_spjlib.QIProcsLib file '/home/SQFQA/SPJRoot/qi_spjs';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create procedure QIN0001 ()
external name 'QIProcs.QIN0001'
library """ + gvars.test_catalog + """.sch_qi_spjlib.QIProcsLib
language java
parameter style java
no sql
isolate;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """grant execute on procedure QIN0001 to \"""" + basic_defs.TestVars.qi_user1 + """\" with grant option;"""
    output = _dci.cmdexec(stmt)
    
    # Set up tables for testing.
    # user1
    _dci = basic_defs.switch_session_qi_user1()
    
    stmt = """set schema """ + basic_defs.TestVars.test_schema_full + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table mytable1
(a int not null not droppable primary key,
b int,
c int,
d char(10),
e varchar(10));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into mytable1 values
(1,1,1,'AAA','AAA'),
(2,2,2,'BBB','BBB'),
(3,3,3,'CCC','CCC'),
(4,4,4,'DDD','DDD'),
(5,5,5,'EEE','EEE');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table mytable2
(a int not null not droppable primary key,
b int,
c int,
d char(10),
e varchar(10));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into mytable2 values
(1,1,1,'AAA','AAA'),
(2,2,2,'BBB','BBB'),
(3,3,3,'CCC','CCC'),
(4,4,4,'DDD','DDD'),
(5,5,5,'EEE','EEE');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view myview1 as select a, b, c, d, e from mytable1;"""
    output = _dci.cmdexec(stmt)
    stmt = """create mv mymv1 refresh on request initialize on create as select a, b, c, d, e from mytable1;"""
    output = _dci.cmdexec(stmt)
    
    # Informational only (turn on if needed)
    # Show all CQD settings
    # cqd showcontrol_unexternalized_attrs 'on';
    # showcontrol all;
    # cqd showcontrol_unexternalized_attrs reset;
    
    # Show errors that would cause auto query retry (AQR) to kick in.
    # get all aqr entries;
    
    # Turn on any needed CQDs here.
    # This newly introduced CQD (by Gayle Schultz) controls whether
    # "REVOKE <privs>" and "REVOKE <privs> ON SCHEMA" will insert the SIKs
    # into the QUERY_USAGE table.  This should be on by default by now.
    # cqd cat_enable_query_invalidation 'on';
    
