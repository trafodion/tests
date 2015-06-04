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
    
def test001(desc="""control query default"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    #---------------------------------------------------------------------------
    # CQD examples: set schema does not affect a prepared statement.
    #---------------------------------------------------------------------------
    stmt = """create schema myschema1;""";
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    stmt = """create schema MYSCHEMA2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create schema MYSCHEMA3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # use default schema
    stmt = """create table t (a int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # use default schema
    stmt = """PREPARE x FROM SELECT * FROM t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """CONTROL QUERY DEFAULT SCHEMA 'myschema1';""";
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # use MYSCHEMA1
    stmt = """create table t3 (a int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # use default schema
    stmt = """EXECUTE x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    # use MYSCHEMA1, shuld see error.
    stmt = """SELECT * FROM t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)

    # use MYSCHEMA1
    stmt = """PREPARE y FROM SELECT * FROM t3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """CONTROL QUERY DEFAULT SCHEMA 'MYSCHEMA2';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # use MYSCHEMA1
    stmt = """EXECUTE y;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    stmt = """drop table """ + defs.my_schema + """.t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table myschema1.t3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # Restore the default schema
    _dci.setup_schema(defs.my_schema)

    stmt = """CONTROL QUERY DEFAULT HBASE_MAX_COLUMN_NAME_LENGTH '200';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """CONTROL QUERY DEFAULT HBASE_MAX_COLUMN_NAME_LENGTH RESET;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """CONTROL QUERY DEFAULT SCHEMA 'MYSCHEMA3';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table t (a int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """CONTROL QUERY DEFAULT * RESET;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # schema should have been reset to SEABASE, make sure the error shows it.
    stmt = """select * from t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    _dci.expect_any_substr(output, 'SEABASE')

    stmt = """drop table myschema3.t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop schema myschema1 cascade;""";
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop schema MYSCHEMA2 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop schema MYSCHEMA3 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # Restore the default schema
    _dci.setup_schema(defs.my_schema)

    _testmgr.testcase_end(desc)

def test002(desc="""TBD"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    _testmgr.testcase_end(desc)


