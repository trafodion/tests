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

import pd29_ddl
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
    
    pd29_ddl._init(_testmgr)
    
    ##sh import ${my_schema}.pd29 -I ${qagdata1}/wisc8m.8p0 -FD \\t
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.pd29 select * from """ + gvars.g_schema_cmureg + """.wisc8m8p0;"""
    output = _dci.cmdexec(stmt)
    ##sh import ${my_schema}.pd29 -I ${qagdata1}/wisc8m.8p1 -FD \\t
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.pd29 select * from """ + gvars.g_schema_cmureg + """.wisc8m8p1;"""
    output = _dci.cmdexec(stmt)
    ##sh import ${my_schema}.pd29 -I ${qagdata1}/wisc8m.8p2 -FD \\t
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.pd29 select * from """ + gvars.g_schema_cmureg + """.wisc8m8p2;"""
    output = _dci.cmdexec(stmt)
    ##sh import ${my_schema}.pd29 -I ${qagdata1}/wisc8m.8p3 -FD \\t
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.pd29 select * from """ + gvars.g_schema_cmureg + """.wisc8m8p3;"""
    output = _dci.cmdexec(stmt)
    ##sh import ${my_schema}.pd29 -I ${qagdata1}/wisc8m.8p4 -FD \\t
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.pd29 select * from """ + gvars.g_schema_cmureg + """.wisc8m8p4;"""
    output = _dci.cmdexec(stmt)
    ##sh import ${my_schema}.pd29 -I ${qagdata1}/wisc8m.8p5 -FD \\t
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.pd29 select * from """ + gvars.g_schema_cmureg + """.wisc8m8p5;"""
    output = _dci.cmdexec(stmt)
    ##sh import ${my_schema}.pd29 -I ${qagdata1}/wisc8m.8p6 -FD \\t
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.pd29 select * from """ + gvars.g_schema_cmureg + """.wisc8m8p6;"""
    output = _dci.cmdexec(stmt)
    ##sh import ${my_schema}.pd29 -I ${qagdata1}/wisc8m.8p7 -FD \\t
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.pd29 select * from """ + gvars.g_schema_cmureg + """.wisc8m8p7;"""
    output = _dci.cmdexec(stmt)

    stmt = """select count(*) from """ + defs.my_schema + """.pd29;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '8000000')
