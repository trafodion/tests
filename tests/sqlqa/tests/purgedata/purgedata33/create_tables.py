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

import pd33004_ddl
import pd33008_ddl
import pd33001_ddl
import pd33016_ddl
import pd33002_ddl
import pd33064_ddl
import pd33128_ddl
import pd33210_ddl
import pd33032_ddl
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
    
    pd33001_ddl._init(_testmgr)
    pd33002_ddl._init(_testmgr)
    pd33004_ddl._init(_testmgr)
    pd33008_ddl._init(_testmgr)
    pd33016_ddl._init(_testmgr)
    pd33032_ddl._init(_testmgr)
    pd33064_ddl._init(_testmgr)
    pd33128_ddl._init(_testmgr)
    pd33210_ddl._init(_testmgr)
    
    ##sh import ${my_schema}.pd33001 -I ${qagdata1}/dat10500 -C 50
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.pd33001 select * from """ + gvars.g_schema_cmureg + """.dat50;"""
    output = _dci.cmdexec(stmt)
  
    stmt = """select count(*) from """ + defs.my_schema + """.pd33001;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '50')
    
    ##sh import ${my_schema}.pd33002 -I ${qagdata1}/dat10500 -C 100
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.pd33002 select * from """ + gvars.g_schema_cmureg + """.dat100;"""
    output = _dci.cmdexec(stmt)

    stmt = """select count(*) from """ + defs.my_schema + """.pd33002;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '100')
    
    ##sh import ${my_schema}.pd33004 -I ${qagdata1}/dat10500 -C 200
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.pd33004 select * from """ + gvars.g_schema_cmureg + """.dat200;"""
    output = _dci.cmdexec(stmt)

    stmt = """select count(*) from """ + defs.my_schema + """.pd33004;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '200')
    
    ##sh import ${my_schema}.pd33008 -I ${qagdata1}/dat10500 -C 400
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.pd33008 select * from """ + gvars.g_schema_cmureg + """.dat400;"""
    output = _dci.cmdexec(stmt)

    stmt = """select count(*) from """ + defs.my_schema + """.pd33008;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '400')
    
    ##sh import ${my_schema}.pd33016 -I ${qagdata1}/dat10500 -C 800
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.pd33016 select * from """ + gvars.g_schema_cmureg + """.dat800;"""
    output = _dci.cmdexec(stmt)

    stmt = """select count(*) from """ + defs.my_schema + """.pd33016;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '800')
    
    ##sh import ${my_schema}.pd33032 -I ${qagdata1}/dat10500 -C 1600
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.pd33032 select * from """ + gvars.g_schema_cmureg + """.dat1600;"""
    output = _dci.cmdexec(stmt)

    stmt = """select count(*) from """ + defs.my_schema + """.pd33032;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '1600')
    
    ##sh import ${my_schema}.pd33064 -I ${qagdata1}/dat10500 -C 3200
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.pd33064 select * from """ + gvars.g_schema_cmureg + """.dat3200;"""
    output = _dci.cmdexec(stmt)

    stmt = """select count(*) from """ + defs.my_schema + """.pd33064;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '3200')
    
    ##sh import ${my_schema}.pd33128 -I ${qagdata1}/dat10500 -C 6400
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.pd33128 select * from """ + gvars.g_schema_cmureg + """.dat6400;"""
    output = _dci.cmdexec(stmt)

    stmt = """select count(*) from """ + defs.my_schema + """.pd33128;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '6400')
    
    ##sh import ${my_schema}.pd33210 -I ${qagdata1}/dat10500
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.pd33210 select * from """ + gvars.g_schema_cmureg + """.dat10500;"""
    output = _dci.cmdexec(stmt)

    stmt = """select count(*) from """ + defs.my_schema + """.pd33210;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '10500')
