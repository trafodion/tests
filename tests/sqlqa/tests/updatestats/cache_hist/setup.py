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

import time
from ...lib import hpdci
from ...lib import gvars
import defs

_testmgr = None
_testlist = []
_dci = None
_dbrootdci = None

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    global _dbrootdci

    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    _dci.setup_schema(defs.my_schema)   
    _dbrootdci = _testmgr.get_dbroot_dci_proc()
    _dbrootdci.setup_schema(defs.my_schema)

    stmt = """set param ?t 'T_A001';"""
    output = _dbrootdci.cmdexec(stmt)

    # SB_HISTOGRAMS and SB_HISTOGRAM_INTERVAL are not created until the 1st
    # update stats are run for an empty schema.  Need to get them created
    # otherwise the next 2 prepare statements won't work.
    if hpdci.tgtTR():
        stmt = """create table junktable (a int);"""
        output = _dci.cmdexec(stmt)
        _dci.expect_complete_msg(output)

        stmt = """update statistics for table junktable on every column;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_complete_msg(output)

        stmt = """drop table junktable cascade;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_complete_msg(output)

    if hpdci.tgtSQ():
        stmt = """prepare show_hist from
select substring(b.object_name,1,6)||'.'||substring(c.column_name,1,1)
,a.READ_TIME,a.READ_COUNT
,a.REASON
from """ + gvars.histograms + """ a
,""" + gvars.definition_schema + """.objects b
,""" + gvars.definition_schema + """.cols c
,""" + gvars.system_defaults_cat + """.system_schema.catsys d
,""" + gvars.system_defaults_cat + """.system_schema.schemata e
where a.table_uid=b.object_uid
and b.object_name_space='TA' and b.object_type='BT'
and c.object_uid=b.object_uid and c.column_number=a.column_number
and d.cat_name=UPPER('""" + defs.w_catalog + """') and d.cat_uid=e.cat_uid
and e.schema_name=UPPER('""" + defs.w_schema + """')
and e.schema_uid=b.schema_uid
and b.object_name = ?t
for read uncommitted access
;"""
    elif hpdci.tgtTR():
        stmt = """prepare show_hist from
select substring(b.object_name,1,6)||'.'||substring(c.column_name,1,1)
,a.READ_TIME,a.READ_COUNT
,a.REASON
from """ + gvars.histograms + """ a
,""" + gvars.definition_schema + """.objects b
,""" + gvars.definition_schema + """.columns c
where a.table_uid=b.object_uid
and b.object_type='BT'
and c.object_uid=b.object_uid and c.column_number=a.column_number
and b.catalog_name=UPPER('""" + defs.w_catalog + """')
and b.schema_name=UPPER('""" + defs.w_schema + """')
and b.object_name = ?t
for read uncommitted access
;"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_prepared_msg(output)

    if hpdci.tgtSQ():
        stmt = """prepare show_hist_sample from
select substring(b.object_name,1,6)||'.'||substring(c.column_name,1,1)
,a.SAMPLE_SECS,a.COL_SECS,a.SAMPLE_PERCENT,a.CV
from """ + gvars.histograms + """ a
,""" + gvars.definition_schema + """.objects b
,""" + gvars.definition_schema + """.cols c
,""" + gvars.system_defaults_cat + """.system_schema.catsys d
,""" + gvars.system_defaults_cat + """.system_schema.schemata e
where a.table_uid=b.object_uid
and b.object_name_space='TA' and b.object_type='BT'
and c.object_uid=b.object_uid and c.column_number=a.column_number
and d.cat_name=UPPER('""" + defs.w_catalog + """') and d.cat_uid=e.cat_uid
and e.schema_name=UPPER('""" + defs.w_schema + """')
and e.schema_uid=b.schema_uid
and b.object_name = ?t
for read uncommitted access
;"""
    elif hpdci.tgtTR():
        stmt = """prepare show_hist_sample from
select substring(b.object_name,1,6)||'.'||substring(c.column_name,1,1)
,a.SAMPLE_SECS,a.COL_SECS,a.SAMPLE_PERCENT,a.CV
from """ + gvars.histograms + """ a
,""" + gvars.definition_schema + """.objects b
,""" + gvars.definition_schema + """.columns c
where a.table_uid=b.object_uid
and b.object_type='BT'
and c.object_uid=b.object_uid and c.column_number=a.column_number
and b.catalog_name=UPPER('""" + defs.w_catalog + """')
and b.schema_name=('""" + defs.w_schema + """')
and b.object_name = ?t
for read uncommitted access
;"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_prepared_msg(output)

    stmt = """control query default USTAT_AUTOMATION_INTERVAL '1440';"""
    output = _dci.cmdexec(stmt)
    stmt = """control query default QUERY_CACHE '0';"""
    output = _dci.cmdexec(stmt)

def cr8tbl():
    global _testmgr
    global _testlist
    global _dci
    global _dbrootdci

    stmt = """drop table """ + defs.tblname + """;"""
    output = _dci.cmdexec(stmt)
    ##expect any * SQL operation complete.
    stmt = """create table """ + defs.tblname + """ (
a int not null
,b int not null
,c int
,d int
,e int
,primary key (a)
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    ##sh SQL_inserted_msg 60000
    stmt = gvars.inscmd + """ """ + defs.tblname + """
select c1+c2*10+c3*100+c4*1000+c5*10000
,c1*10+c2
,c1*10
,NULL
,c3
from (values(1)) t
transpose 0,1,2,3,4,5,6,7,8,9 as c1
transpose 0,1,2,3,4,5,6,7,8,9 as c2
transpose 0,1,2,3,4,5,6,7,8,9 as c3
transpose 0,1,2,3,4,5,6,7,8,9 as c4
transpose 0,1,2,3,4,5 as c5
;"""
    output = _dci.cmdexec(stmt)

    stmt = """select count(*) from """ + defs.tblname + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '60000')

def run_each_test():
    global _testmgr
    global _testlist
    global _dci
    global _dbrootdci

    # show current CQD
    stmt = """showcontrol default CACHE_HISTOGRAMS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showcontrol default CACHE_HISTOGRAMS_REFRESH_INTERVAL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """set param ?t """ + defs.tblname + """;"""
    output = _dbrootdci.cmdexec(stmt)

    # clear the histogram
    stmt = """update statistics for table """ + defs.tblname + """ clear;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # show current histogram
    stmt = """execute show_hist;"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_selected_msg(output)

    stmt = """update statistics for table """ + defs.tblname + """ on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """execute show_hist;"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_selected_msg(output)

    # this should update read_time and read_count
    stmt = """select count(*) from """ + defs.tblname + """ where a > 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/""" + defs.testid + """exp""", """v03b1""")

    stmt = """execute show_hist;"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_selected_msg(output)

    time.sleep(defs.SLEEP_TIME)

    # Run series of queries
    stmt = """select count(*) from """ + defs.tblname + """ where a > 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/""" + defs.testid + """exp""", """v03c1""")

    stmt = """execute show_hist;"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_selected_msg(output)

    time.sleep(defs.SLEEP_TIME)

    stmt = """select count(*) from """ + defs.tblname + """ where a =100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/""" + defs.testid + """exp""", """v03d1""")

    stmt = """execute show_hist;"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_selected_msg(output)

    time.sleep(defs.SLEEP_TIME)

    stmt = """select count(*) from """ + defs.tblname + """ where a is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/""" + defs.testid + """exp""", """v03e1""")

    stmt = """execute show_hist;"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_selected_msg(output)

    time.sleep(defs.SLEEP_TIME)

    stmt = """select count(*) from """ + defs.tblname + """ where a > 10 and b < 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/""" + defs.testid + """exp""", """v03f1""")

    stmt = """execute show_hist;"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_selected_msg(output)

    time.sleep(defs.SLEEP_TIME)

    stmt = """select count(*) from """ + defs.tblname + """ where b<10;"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_file(output, defs.test_dir + """/""" + defs.testid + """exp""", """v03g1""")

    stmt = """execute show_hist;"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_selected_msg(output)

