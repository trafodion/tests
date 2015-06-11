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
import defs
import basic_defs

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
    #_dci.setup_schema(defs.my_schema)   
    #_dci.setup_schema(SECURITY_SECUREJAR)

    #stmt = """control query default SAVE_DROPPED_TABLE_DDL 'OFF';"""
    #output = _dci.cmdexec(stmt)

    stmt = """control query default limit_max_numeric_precision 'SYSTEM';"""
    output = _dci.cmdexec(stmt)

#process user_root

    stmt = """create schema """+defs.my_schema +""";"""
    output = _dci.cmdexec(stmt)

    #stmt = """revoke COMPONENT privilege "CREATE" on sql_operations from "PUBLIC";"""
    #output = _dci.cmdexec(stmt)

    stmt = """grant COMPONENT privilege "CREATE" on sql_operations to  qauser10;"""
    output = _dci.cmdexec(stmt)

    stmt = """grant COMPONENT privilege "DROP" on sql_operations to  qauser10;"""
    output = _dci.cmdexec(stmt)

    stmt = """GRANT COMPONENT privilege manage_library on sql_operations to qauser10;"""
    output = _dci.cmdexec(stmt)
    stmt = """GRANT COMPONENT privilege manage_library on sql_operations to qauser11;"""
    output = _dci.cmdexec(stmt)

    stmt = """GRANT COMPONENT privilege create_library on sql_operations to qauser10;"""
    output = _dci.cmdexec(stmt)
    stmt = """GRANT COMPONENT privilege create_library on sql_operations to qauser11;"""
    output = _dci.cmdexec(stmt)

    stmt = """GRANT COMPONENT privilege drop_library on sql_operations to qauser10;"""
    output = _dci.cmdexec(stmt)
    stmt = """GRANT COMPONENT privilege drop_library on sql_operations to qauser11;"""
    output = _dci.cmdexec(stmt)

    stmt = """GRANT COMPONENT privilege drop_routine on sql_operations to qauser10;"""
    output = _dci.cmdexec(stmt)
    stmt = """GRANT COMPONENT privilege drop_routine on sql_operations to qauser11;"""
    output = _dci.cmdexec(stmt)

    stmt = """GRANT COMPONENT privilege create_routine on sql_operations to qauser10;"""
    output = _dci.cmdexec(stmt)
    stmt = """GRANT COMPONENT privilege create_routine on sql_operations to qauser11;"""
    output = _dci.cmdexec(stmt)
    stmt = """GRANT COMPONENT privilege create_routine on sql_operations to qauser12;"""
    output = _dci.cmdexec(stmt)


