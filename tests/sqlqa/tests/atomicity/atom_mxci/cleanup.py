# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2014-2015 Hewlett-Packard Development Company, L.P.
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
    _dci.cleanup_schema(defs.my_schema)

    stmt = """control query default SHOWDDL_DISPLAY_FORMAT reset;"""
    output = _dci.cmdexec(stmt)
    stmt = """control query default QUERY_CACHE reset;"""
    output = _dci.cmdexec(stmt)
    stmt = """control query default QUERY_CACHE_STATEMENT_PINNING reset;"""
    output = _dci.cmdexec(stmt)
    stmt = """control query default UPD_SAVEPOINT_ON_ERROR reset;"""
    output = _dci.cmdexec(stmt)
    stmt = """control query default UPD_ABORT_ON_ERROR reset;"""
    output = _dci.cmdexec(stmt)
    stmt = """control query default UPDATE_CLUSTERING_OR_UNIQUE_INDEX_KEY reset;"""
    output = _dci.cmdexec(stmt)
    stmt = """control query default TABLELOCK reset;"""
    output = _dci.cmdexec(stmt)
    stmt = """control query default ISOLATION_LEVEL reset;"""
    output = _dci.cmdexec(stmt)
    stmt = """control query default SIMILARITY_CHECK reset;"""
    output = _dci.cmdexec(stmt)
    stmt = """control query default POS_TABLE_SIZE reset;"""
    output = _dci.cmdexec(stmt)
    stmt = """control query default POS reset;"""
    output = _dci.cmdexec(stmt)

