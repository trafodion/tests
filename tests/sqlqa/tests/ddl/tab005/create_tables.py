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

import btpns13_ddl
import btpnl21_ddl
import b2pns09_ddl
import b2pwl28_ddl
import b2uns01_ddl
import b2pns01_ddl
import b2pns03_ddl
import btpwl10_ddl
import b2pwl30_ddl
import b2pwl34_ddl
import b2uwl16_ddl
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
    
    stmt = """create catalog """ + defs.w_catalog + """;"""
    output = _dci.cmdexec(stmt)
    stmt = """create schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    btpns13_ddl._init(_testmgr)
    btpwl10_ddl._init(_testmgr)
    btpnl21_ddl._init(_testmgr)
    b2pns01_ddl._init(_testmgr)
    b2pwl28_ddl._init(_testmgr)
    b2pns03_ddl._init(_testmgr)
    b2pwl30_ddl._init(_testmgr)
    b2pwl34_ddl._init(_testmgr)
    b2pns09_ddl._init(_testmgr)
    b2uns01_ddl._init(_testmgr)
    b2uwl16_ddl._init(_testmgr)
    
    stmt = """create table """ + defs.my_schema + """.b2empty like """ + defs.my_schema + """.b2pwl28
with partitions with constraints;"""
    output = _dci.cmdexec(stmt)
    
    # R2.5 NCI #sh import $my_schema.btpns13 -I $popdatadir/btpns13.dat
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.btpns13
(select * from """ + gvars.g_schema_sqldpop + """.btpns13);"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    # R2.5 NCI #sh import $my_schema.btpwl10 -I $popdatadir/btpwl10.dat
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.btpwl10
(select * from """ + gvars.g_schema_sqldpop + """.btpwl10);"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    # R2.5 NCI #sh import $my_schema.btpnl21 -I $popdatadir/btpnl21.dat
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.btpnl21
(select * from """ + gvars.g_schema_sqldpop + """.btpnl21);"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    # R2.5 NCI #sh import $my_schema.b2pns01 -I $popdatadir/b2pns01.dat
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.b2pns01
(select * from """ + gvars.g_schema_sqldpop + """.b2pns01);"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    # R2.5 NCI #sh import $my_schema.b2pwl28 -I $popdatadir/b2pwl28.dat
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.b2pwl28
(select * from """ + gvars.g_schema_sqldpop + """.b2pwl28);"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    # R2.5 NCI #sh import $my_schema.b2pns03 -I $popdatadir/b2pns03.dat
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.b2pns03
(select * from """ + gvars.g_schema_sqldpop + """.b2pns03);"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    # R2.5 NCI #sh import $my_schema.b2pwl30 -I $popdatadir/b2pwl30.dat
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.b2pwl30
(select * from """ + gvars.g_schema_sqldpop + """.b2pwl30);"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    # R2.5 NCI #sh import $my_schema.b2pwl34 -I $popdatadir/b2pwl34.dat
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.b2pwl34
(select * from """ + gvars.g_schema_sqldpop + """.b2pwl34);"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    # R2.5 NCI #sh import $my_schema.b2pns09 -I $popdatadir/b2pns09.dat
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.b2pns09
(select * from """ + gvars.g_schema_sqldpop + """.b2pns09);"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    # R2.5 NCI #sh import $my_schema.b2uns01 -I $optdatadir/b2uns01.dat
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.b2uns01
(select * from """ + gvars.g_schema_sqldopt + """.b2uns01);"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    # R2.5 NCI #sh import $my_schema.b2uwl16 -I $optdatadir/b2uwl16.dat
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.b2uwl16
(select * from """ + gvars.g_schema_sqldopt + """.b2uwl16);"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
