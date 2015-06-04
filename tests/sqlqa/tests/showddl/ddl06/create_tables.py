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
    
    stmt = """set schema """ + defs.my_schema + """;"""    
    output = _dci.cmdexec(stmt)

    stmt = """create table b2pwl12 like """ + gvars.g_schema_sqldpop + """.b2pwl12 with partitions;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.b2pwl12
(select * from """ + gvars.g_schema_sqldpop + """.b2pwl12);"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = """create index ix12 on b2pwl12 (sbinneg15_nuniq desc, sdecneg15_100  desc);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table b2pwl28 like """ + gvars.g_schema_sqldpop + """.b2pwl28 with partitions;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.b2pwl28
(select * from """ + gvars.g_schema_sqldpop + """.b2pwl28);"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = """create table b2pwl06 like """ + gvars.g_schema_sqldpop + """.b2pwl06 with partitions;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.b2pwl06
(select * from """ + gvars.g_schema_sqldpop + """.b2pwl06);"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = """set schema """ + defs.my_schema1 + """;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table b2pwl06 like """ + gvars.g_schema_sqldpop + """.b2pwl06 with partitions;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = gvars.inscmd + """ """ + defs.my_schema1 + """.b2pwl06
(select * from """ + gvars.g_schema_sqldpop + """.b2pwl06);"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
