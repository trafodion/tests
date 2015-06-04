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

import abase_ddl
import bbase_ddl
import cbase_ddl
from ...lib import hpdci
from ...lib import gvars
import defs
import table

_testmgr = None
_testlist = []
_dci = None

# Added this for compression

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()

def test001(desc='Create tables'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    prop_template = defs.test_dir + '/../../lib/t4properties.template'
    prop_file = defs.work_dir + '/t4properties'
    hpdci.create_jdbc_propfile(prop_template, prop_file, defs.w_catalog, defs.w_schema)

    # turn off stats warning, so that they don't interfere with expect file
    stmt = """control query default hist_missing_stats_warning_level '0';"""
    output = _dci.cmdexec(stmt)
    stmt = """control query default hist_rowcount_requiring_stats '1000000';"""
    output = _dci.cmdexec(stmt)

    tablelist = [['abase', ['wisc3200', 'wisc3201', 'wisc3202', 'wisc3203', 
                            'wisc3204', 'wisc3205', 'wisc3206', 'wisc3207', 
                            'wisc3208', 'wisc3209', 'wisc3210', 'wisc3211',
                            'wisc3212', 'wisc3213', 'wisc3214', 'wisc3215',
                            'wisc3216', 'wisc3217', 'wisc3218', 'wisc3219',
                            'wisc3220', 'wisc3221', 'wisc3222', 'wisc3223',
                            'wisc3224', 'wisc3225', 'wisc3226', 'wisc3227',
                            'wisc3228', 'wisc3229', 'wisc3230', 'wisc3231']]]

    for items in tablelist:
        table.create_and_load(_testmgr, prop_file, items[0], items[1], '32000000', '\t') 

    bbase_ddl._init(_testmgr)

    stmt = gvars.inscmd + """ bbase (select * from abase);"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)

    stmt = """update statistics for table bbase on every column sample random 5 percent;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select count(*) from bbase;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '32000000')

    cbase_ddl._init(_testmgr)

    stmt = gvars.inscmd + """ cbase (select * from abase);"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)

    stmt = """update statistics for table cbase on every column sample random 5 percent;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select count(*) from cbase;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '32000000')

    _testmgr.testcase_end(desc)
    
def test003(desc='Create Index'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """create unique index ixa4 on abase (UNIQUE3, twentypercent, fiftypercent ASC) hash partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create unique index ixb4 on bbase (UNIQUE3, two, four ASC) hash partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
