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

    stmt = """cqd USTAT_AUTOMATION_INTERVAL '0';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _dci.cmdexec("""drop table TBLX;""")
    output = _dci.cmdexec("""drop table TBLY;""")

    stmt = """create table TBLX(
colkey1 int not null,
colkey2 char(15) not null,
cola int,
colb numeric(11,3),
colc char(10),
cold date,
cole int,
colf varchar(13),
colg timestamp,
primary key (colkey1, colkey2))
salt using 8 partitions
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """load into TBLX
select c1+c2*10+c3*100+c4*1000+c5*10000+c6*100000,
cast(c1*10+c2*10+c3*100+c4*1000 as char(15)),
c1*10+c2*10+c3*100+c4*1000,
c1*10+c2*10+c3*100,
cast(c1*10+c2*10+c3*100+c4*1000 as char(10)),
cast(converttimestamp(210614299200000000 + (86400000000 * (c1+c2*10+c3*100)))
as date),
NULL,
cast(c1*10+c2*10+c3*100 as varchar(13)),
converttimestamp(210614299200000000 + (86400000000 *
(c1+c2*10+c3*100+c4*1000)) + (1000000 * (c1+c2*10+c3*100)) +
(60000000 * (c1+c2*10)) + (3600000000 * (c1+c2*10)))
from (values(1)) t
transpose 0,1,2,3,4,5,6,7,8,9 as c1
transpose 0,1,2,3,4,5,6,7,8,9 as c2
transpose 0,1,2,3,4,5,6,7,8,9 as c3
transpose 0,1,2,3,4,5,6,7,8,9 as c4
transpose 0,1,2,3,4,5,6,7,8,9 as c5
transpose 0,1,2,3,4,5,6,7,8,9 as c6
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """select count(*) from TBLX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '1000000')

    stmt = """create table TBLY primary key (colkey1)
number of partitions 8 no load as select * from TBLX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, '0')
    stmt = """load into TBLY select * from TBLX where colkey1 < 90000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """select count(*) from TBLY;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '90000')
    output = _dci.cmdexec("""showddl TBLY;""")

    stmt = """create table TBLZ(
colkey1 int not null,
cola int,
colb int,
colkey2 int not null,
colc int,
cold int)
 primary key (colkey1, colkey2)
salt using 13 partitions;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """load into TBLZ
select c1+c2*10+c3*100+c4*1000+c5*10000+c6*100000+c7*1000000,
c1+c2*10+c3*100+c4*1000+c5*10000+c6*100000+c7*1000000,
c1+c2*10+c3*100+c4*1000+c5*10000,
c1+c2*10+c3*100+c4*1000,
c1+c2*10+c3*100+c4*1000+c5*10000+c6*100000+c7*1000000,
c1+c2*10+c3*100+c4*1000+c5*10000+c6*100000
from (values(1)) t
transpose 0,1,2,3,4,5,6,7,8,9 as c1
transpose 0,1,2,3,4,5,6,7,8,9 as c2
transpose 0,1,2,3,4,5,6,7,8,9 as c3
transpose 0,1,2,3,4,5,6,7,8,9 as c4
transpose 0,1,2,3,4,5,6,7,8,9 as c5
transpose 0,1,2,3,4,5,6,7,8,9 as c6
transpose 0,1,2,3,4 as c7
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """select count(*) from TBLZ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '5000000')

    # do this to create sb_histograms/sb_histogram_intervals for now
    # otherwise prepare show_hist stmt below will fail with
    # ERROR[4082] Object A does not exist or is inaccessible.
    stmt = """update statistics for table TBLY on every key;"""
    output = _dci.cmdexec(stmt)
    stmt = """update statistics for table TBLY clear;"""
    output = _dci.cmdexec(stmt)

    output = _dci.cmdexec("""set param ?t 'TBLX';""")

    stmt = """prepare show_hist from
select substring(b.object_name,1,4)||'.'||substring(c.column_name,1,7)
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

    stmt = """prepare reason_blank from
select case when cnt = 0 then 'PASS' else 'FAIL' end from
(select count(*) as cnt
from """ + gvars.histograms + """ a
,""" + gvars.definition_schema + """.objects b
,""" + gvars.definition_schema + """.columns c
where a.table_uid=b.object_uid
and b.object_type='BT'
and c.object_uid=b.object_uid and c.column_number=a.column_number
and b.catalog_name=UPPER('""" + defs.w_catalog + """')
and b.schema_name=UPPER('""" + defs.w_schema + """')
and b.object_name = ?t
and a.reason != ' '
for read uncommitted access)
;"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_prepared_msg(output)

    stmt = """prepare reason_i from
select case when cnt = 0 then 'PASS' else 'FAIL' end from
(select count(*) as cnt
from """ + gvars.histograms + """ a
,""" + gvars.definition_schema + """.objects b
,""" + gvars.definition_schema + """.columns c
where a.table_uid=b.object_uid
and b.object_type='BT'
and c.object_uid=b.object_uid and c.column_number=a.column_number
and b.catalog_name=UPPER('""" + defs.w_catalog + """')
and b.schema_name=UPPER('""" + defs.w_schema + """')
and b.object_name = ?t
and a.reason != 'I'
for read uncommitted access)
;"""
    output = _dbrootdci.cmdexec(stmt)
    _dbrootdci.expect_prepared_msg(output)

    stmt = """prepare show_sample from
select substring(b.object_name,1,4)||'.'||substring(c.column_name,1,7)
,a.sample_percent
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

    stmt = """cqd USTAT_AUTOMATION_INTERVAL '1440';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """cqd CACHE_HISTOGRAMS 'OFF';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """cqd USTAT_SHOW_MC_INTERVAL_INFO 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


def clear_stats(tblname):
    global _testmgr
    global _testlist
    global _dci

    stmt = ("""update statistics for table """ + tblname + """ clear;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


def run_each_test(cqdval='4'):
    global _testmgr
    global _testlist
    global _dci

    stmt = """cqd USTAT_AUTO_MISSING_STATS_LEVEL '""" + cqdval + """';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """cqd HIST_MISSING_STATS_WARNING_LEVEL '""" + cqdval + """';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # ==========================
    # single key column stats to be generated
    qryid = 'Q1'
    stmt = """prepare XX from select *
from TBLX where colkey1 = 40000;"""
    output = _dci.cmdexec(stmt)
    if cqdval == '0':
        _dci.unexpect_warning_msg(output)
    else:
        _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY1)*TBLX""")
        _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY2)*TBLX""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLA)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLB)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLC)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLD)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLE)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLF)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLG)*""")
        _dci.unexpect_warning_msg(output, '6013')
    _dci.expect_prepared_msg(output)
    output = _dbrootdci.cmdexec("""set param ?t 'TBLX';""")
    output = _dbrootdci.cmdexec("""execute show_hist;""")
    if cqdval == '0':
        _dbrootdci.expect_selected_msg(output, '0')
        _dbrootdci.unexpect_warning_msg(output)
    else:
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY1 * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY2 * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX._SALT_ * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_selected_msg(output, '3')
        output = _dbrootdci.cmdexec("""execute reason_blank;""")
        _dbrootdci.expect_str_token(output, 'PASS')

    stmt = """update statistics for table TBLX on necessary columns;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _dbrootdci.cmdexec("""execute show_hist;""")
    if cqdval == '0':
        _dbrootdci.expect_selected_msg(output, '0')
        _dbrootdci.unexpect_warning_msg(output)
    else:
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY1 * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY2 * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX._SALT_ * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_selected_msg(output, '3')
        output = _dbrootdci.cmdexec("""execute reason_i;""")
        _dbrootdci.expect_str_token(output, 'PASS')

    stmt = ("""showstats for table TBLX on existing column;""")
    output = _dci.cmdexec(stmt)
    if cqdval == '0':
        _dci.expect_any_substr(output, """No Histograms exist for the""" +
                               """ requested columns or groups""")
    else:
        _dci.expect_any_substr(output, """1000000 * 1000000 COLKEY""")
        _dci.expect_any_substr(output, """1000000 * 1009 COLKEY2""")
        _dci.expect_any_substr(output, """1000000 * 8 \"_SALT_\"""")
        _dci.unexpect_any_substr(output, """COLA""")
        _dci.unexpect_any_substr(output, """COLB""")
        _dci.unexpect_any_substr(output, """COLC""")
        _dci.unexpect_any_substr(output, """COLD""")
        _dci.unexpect_any_substr(output, """COLE""")
        _dci.unexpect_any_substr(output, """COLF""")
        _dci.unexpect_any_substr(output, """COLG""")
    _dci.expect_complete_msg(output)
    clear_stats("TBLX")

    # ==========================
    qryid = 'Q1a'
    stmt = """prepare XX from select *
from TBLX where "_SALT_" = 2;"""
    output = _dci.cmdexec(stmt)
    if cqdval == '0':
        _dci.unexpect_warning_msg(output)
    else:
        _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY1)*TBLX""")
        _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY2)*TBLX""")
        _dci.unexpect_any_substr(output, """(COLA)""")
        _dci.unexpect_any_substr(output, """(COLB)""")
        _dci.unexpect_any_substr(output, """(COLC)""")
        _dci.unexpect_any_substr(output, """(COLD)""")
        _dci.unexpect_any_substr(output, """(COLE)""")
        _dci.unexpect_any_substr(output, """(COLF)""")
        _dci.unexpect_any_substr(output, """(COLG)""")
        _dci.unexpect_warning_msg(output, '6013')
    _dci.expect_prepared_msg(output)
    output = _dbrootdci.cmdexec("""set param ?t 'TBLX';""")
    output = _dbrootdci.cmdexec("""execute show_hist;""")
    if cqdval == '0':
        _dbrootdci.expect_selected_msg(output, '0')
        _dbrootdci.unexpect_warning_msg(output)
    else:
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY1 * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY2 * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX._SALT_ * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_selected_msg(output, '3')
        output = _dbrootdci.cmdexec("""execute reason_blank;""")
        _dbrootdci.expect_str_token(output, 'PASS')

    stmt = """update statistics for table TBLX on necessary columns;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _dbrootdci.cmdexec("""execute show_hist;""")
    if cqdval == '0':
        _dbrootdci.expect_selected_msg(output, '0')
        _dbrootdci.unexpect_warning_msg(output)
    else:
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY1 * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY2 * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX._SALT_ * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_selected_msg(output, '3')
        output = _dbrootdci.cmdexec("""execute reason_i;""")
        _dbrootdci.expect_str_token(output, 'PASS')

    stmt = ("""showstats for table TBLX on existing column;""")
    output = _dci.cmdexec(stmt)
    if cqdval == '0':
        _dci.expect_any_substr(output, """No Histograms exist for the""" +
                               """ requested columns or groups""")
    else:
        _dci.expect_any_substr(output, """1000000 * 1000000 COLKEY""")
        _dci.expect_any_substr(output, """1000000 * 1009 COLKEY2""")
        _dci.expect_any_substr(output, """1000000 * 8 \"_SALT_\"""")
        _dci.unexpect_any_substr(output, """COLA""")
        _dci.unexpect_any_substr(output, """COLB""")
        _dci.unexpect_any_substr(output, """COLC""")
        _dci.unexpect_any_substr(output, """COLD""")
        _dci.unexpect_any_substr(output, """COLE""")
        _dci.unexpect_any_substr(output, """COLF""")
        _dci.unexpect_any_substr(output, """COLG""")
    _dci.expect_complete_msg(output)
    clear_stats("TBLX")

    # ==========================
    # _salt_ histograms should be requested by optimizer
    qryid = 'Q2'
    stmt = """prepare XX from select *
from TBLX where cola = 1000;"""
    output = _dci.cmdexec(stmt)
    if cqdval == '0':
        _dci.unexpect_warning_msg(output)
    else:
        _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY1)*TBLX""")
        _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY2)*TBLX""")
        _dci.expect_any_substr(output, """WARNING[6011]*(COLA)*TBLX""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLB)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLC)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLD)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLE)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLF)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLG)*""")
        _dci.unexpect_warning_msg(output, '6013')
    _dci.expect_prepared_msg(output)
    output = _dbrootdci.cmdexec("""set param ?t 'TBLX';""")
    output = _dbrootdci.cmdexec("""execute show_hist;""")
    if cqdval == '0':
        _dbrootdci.expect_selected_msg(output, '0')
        _dbrootdci.unexpect_warning_msg(output)
    else:
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY1 * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY2 * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLA * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX._SALT_ * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_selected_msg(output, '4')
        output = _dbrootdci.cmdexec("""execute reason_blank;""")
        _dbrootdci.expect_str_token(output, 'PASS')

    stmt = """update statistics for table TBLX on necessary columns;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _dbrootdci.cmdexec("""execute show_hist;""")
    if cqdval == '0':
        _dbrootdci.expect_selected_msg(output, '0')
        _dbrootdci.unexpect_warning_msg(output)
    else:
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY1 * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY2 * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLA * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX._SALT_ * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_selected_msg(output, '4')
        output = _dbrootdci.cmdexec("""execute reason_i;""")
        _dbrootdci.expect_str_token(output, 'PASS')

    stmt = ("""showstats for table TBLX on existing column;""")
    output = _dci.cmdexec(stmt)
    if cqdval == '0':
        _dci.expect_any_substr(output, """No Histograms exist for the""" +
                               """ requested columns or groups""")
    else:
        _dci.expect_any_substr(output, """1000000 * 1000000 COLKEY""")
        _dci.expect_any_substr(output, """1000000 * 1009 COLKEY2""")
        _dci.expect_any_substr(output, """1000000 * 1009 COLA""")
        _dci.expect_any_substr(output, """1000000 * 8 \"_SALT_\"""")
        _dci.unexpect_any_substr(output, """COLB""")
        _dci.unexpect_any_substr(output, """COLC""")
        _dci.unexpect_any_substr(output, """COLD""")
        _dci.unexpect_any_substr(output, """COLE""")
        _dci.unexpect_any_substr(output, """COLF""")
        _dci.unexpect_any_substr(output, """COLG""")
    _dci.expect_complete_msg(output)
    clear_stats("TBLX")

    # ==========================
    qryid = 'Q2a'
    stmt = """prepare XX from select *
from TBLX where colkey1 = 40000 and colf = 'bogus data';"""
    output = _dci.cmdexec(stmt)
    if cqdval == '0':
        _dci.unexpect_warning_msg(output)
    else:
        _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY1)*TBLX""")
        _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY2)*TBLX""")
        _dci.expect_any_substr(output, """WARNING[6011]*(COLF)*TBLX""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLA)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLB)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLC)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLD)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLE)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLG)*""")
        if cqdval == '2' or cqdval == '3' or cqdval == '4':
            _dci.expect_any_substr(output,
                                   """WARNING[6010]*(COLKEY1, COLF)*TBLX""")
        else:
            _dci.unexpect_warning_msg(output, '6010')
    _dci.expect_prepared_msg(output)
    output = _dbrootdci.cmdexec("""set param ?t 'TBLX';""")
    output = _dbrootdci.cmdexec("""execute show_hist;""")
    if cqdval == '0':
        _dbrootdci.expect_selected_msg(output, '0')
        _dbrootdci.unexpect_warning_msg(output)
    else:
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY1 * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY2 * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLF * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX._SALT_ * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.unexpect_any_substr(output, """COLA""")
        _dbrootdci.unexpect_any_substr(output, """COLB""")
        _dbrootdci.unexpect_any_substr(output, """COLC""")
        _dbrootdci.unexpect_any_substr(output, """COLD""")
        _dbrootdci.unexpect_any_substr(output, """COLE""")
        _dbrootdci.unexpect_any_substr(output, """COLG""")
        if cqdval == '2' or cqdval == '3' or cqdval == '4':
            _dbrootdci.expect_selected_msg(output, '6')
        else:
            _dbrootdci.expect_selected_msg(output, '4')
        output = _dbrootdci.cmdexec("""execute reason_blank;""")
        _dbrootdci.expect_str_token(output, 'PASS')

    stmt = """update statistics for table TBLX on necessary columns;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _dbrootdci.cmdexec("""execute show_hist;""")
    if cqdval == '0':
        _dbrootdci.expect_selected_msg(output, '0')
        _dbrootdci.unexpect_warning_msg(output)
    else:
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY1 * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY2 * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLF * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX._SALT_ * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.unexpect_any_substr(output, """COLA""")
        _dbrootdci.unexpect_any_substr(output, """COLB""")
        _dbrootdci.unexpect_any_substr(output, """COLC""")
        _dbrootdci.unexpect_any_substr(output, """COLD""")
        _dbrootdci.unexpect_any_substr(output, """COLE""")
        _dbrootdci.unexpect_any_substr(output, """COLG""")
        if cqdval == '2' or cqdval == '3' or cqdval == '4':
            _dbrootdci.expect_selected_msg(output, '6')
        else:
            _dbrootdci.expect_selected_msg(output, '4')
        output = _dbrootdci.cmdexec("""execute reason_i;""")
        _dbrootdci.expect_str_token(output, 'PASS')

    stmt = ("""showstats for table TBLX on existing column;""")
    output = _dci.cmdexec(stmt)
    if cqdval == '0':
        _dci.expect_any_substr(output, """No Histograms exist for the""" +
                               """ requested columns or groups""")
    else:
        _dci.expect_any_substr(output, """1000000 * 1000000 COLKEY""")
        _dci.expect_any_substr(output, """1000000 * 1009 COLKEY2""")
        _dci.expect_any_substr(output, """1000000 * 109 COLF""")
        _dci.expect_any_substr(output, """1000000 * 8 \"_SALT_\"""")
        _dci.unexpect_any_substr(output, """COLA""")
        _dci.unexpect_any_substr(output, """COLB""")
        _dci.unexpect_any_substr(output, """COLC""")
        _dci.unexpect_any_substr(output, """COLD""")
        _dci.unexpect_any_substr(output, """COLE""")
        _dci.unexpect_any_substr(output, """COLG""")
    _dci.expect_complete_msg(output)
    clear_stats("TBLX")

    # ==========================
    qryid = 'Q2b'
    stmt = """prepare XX from select *
from TBLX where colkey1 < 40000;"""
    output = _dci.cmdexec(stmt)
    if cqdval == '0':
        _dci.unexpect_warning_msg(output)
    else:
        _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY1)*TBLX""")
        _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY2)*TBLX""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLA)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLB)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLC)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLD)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLE)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLF)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLG)*""")
        _dci.unexpect_warning_msg(output, '6010')
    _dci.expect_prepared_msg(output)
    output = _dbrootdci.cmdexec("""set param ?t 'TBLX';""")
    output = _dbrootdci.cmdexec("""execute show_hist;""")
    if cqdval == '0':
        _dbrootdci.expect_selected_msg(output, '0')
        _dbrootdci.unexpect_warning_msg(output)
    else:
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY1 * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY2 * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX._SALT_ * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_selected_msg(output, '3')
        output = _dbrootdci.cmdexec("""execute reason_blank;""")
        _dbrootdci.expect_str_token(output, 'PASS')

    stmt = """update statistics for table TBLX on necessary columns;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _dbrootdci.cmdexec("""execute show_hist;""")
    if cqdval == '0':
        _dbrootdci.expect_selected_msg(output, '0')
        _dbrootdci.unexpect_warning_msg(output)
    else:
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY1 * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY2 * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX._SALT_ * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_selected_msg(output, '3')
        output = _dbrootdci.cmdexec("""execute reason_i;""")
        _dbrootdci.expect_str_token(output, 'PASS')

    stmt = ("""showstats for table TBLX on existing column;""")
    output = _dci.cmdexec(stmt)
    if cqdval == '0':
        _dci.expect_any_substr(output, """No Histograms exist for the""" +
                               """ requested columns or groups""")
    else:
        _dci.expect_any_substr(output, """1000000 * 1000000 COLKEY""")
        _dci.expect_any_substr(output, """1000000 * 1009 COLKEY2""")
        _dci.expect_any_substr(output, """1000000 * 8 \"_SALT_\"""")
        _dci.unexpect_any_substr(output, """COLA""")
        _dci.unexpect_any_substr(output, """COLB""")
        _dci.unexpect_any_substr(output, """COLC""")
        _dci.unexpect_any_substr(output, """COLD""")
        _dci.unexpect_any_substr(output, """COLE""")
        _dci.unexpect_any_substr(output, """COLF""")
        _dci.unexpect_any_substr(output, """COLG""")
    _dci.expect_complete_msg(output)
    clear_stats("TBLX")

    # ==========================
    qryid = 'Q2c'
    stmt = """prepare XX from select *
from TBLX where colg < timestamp'2015-05-05 12:34:56';"""
    output = _dci.cmdexec(stmt)
    if cqdval == '0':
        _dci.unexpect_warning_msg(output)
    else:
        _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY1)*TBLX""")
        _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY2)*TBLX""")
        _dci.expect_any_substr(output, """WARNING[6011]*(COLG)*TBLX""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLA)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLB)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLC)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLD)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLE)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLF)*""")
        _dci.unexpect_warning_msg(output, '6010')
    _dci.expect_prepared_msg(output)
    output = _dbrootdci.cmdexec("""set param ?t 'TBLX';""")
    output = _dbrootdci.cmdexec("""execute show_hist;""")
    if cqdval == '0':
        _dbrootdci.expect_selected_msg(output, '0')
        _dbrootdci.unexpect_warning_msg(output)
    else:
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY1 * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY2 * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLG * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX._SALT_ * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_selected_msg(output, '4')
        output = _dbrootdci.cmdexec("""execute reason_blank;""")
        _dbrootdci.expect_str_token(output, 'PASS')

    stmt = """update statistics for table TBLX on necessary columns;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _dbrootdci.cmdexec("""execute show_hist;""")
    if cqdval == '0':
        _dbrootdci.expect_selected_msg(output, '0')
        _dbrootdci.unexpect_warning_msg(output)
    else:
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY1 * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY2 * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLG * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX._SALT_ * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_selected_msg(output, '4')
        output = _dbrootdci.cmdexec("""execute reason_i;""")
        _dbrootdci.expect_str_token(output, 'PASS')

    stmt = ("""showstats for table TBLX on existing column;""")
    output = _dci.cmdexec(stmt)
    if cqdval == '0':
        _dci.expect_any_substr(output, """No Histograms exist for the""" +
                               """ requested columns or groups""")
    else:
        _dci.expect_any_substr(output, """1000000 * 1000000 COLKEY""")
        _dci.expect_any_substr(output, """1000000 * 1009 COLKEY2""")
        _dci.expect_any_substr(output, """1000000 * 10000 COLG""")
        _dci.expect_any_substr(output, """1000000 * 8 \"_SALT_\"""")
        _dci.unexpect_any_substr(output, """COLA""")
        _dci.unexpect_any_substr(output, """COLB""")
        _dci.unexpect_any_substr(output, """COLC""")
        _dci.unexpect_any_substr(output, """COLD""")
        _dci.unexpect_any_substr(output, """COLE""")
        _dci.unexpect_any_substr(output, """COLF""")
    _dci.expect_complete_msg(output)
    clear_stats("TBLX")

    # ==========================
    qryid = 'Q2d'
    stmt = """prepare XX from select *
from TBLX where "_SALT_" < 2;"""
    output = _dci.cmdexec(stmt)
    if cqdval == '0':
        _dci.unexpect_warning_msg(output)
    else:
        _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY1)*TBLX""")
        _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY2)*TBLX""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLA)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLB)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLC)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLD)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLE)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLF)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLG)*""")
        _dci.unexpect_warning_msg(output, '6010')
    _dci.expect_prepared_msg(output)
    output = _dbrootdci.cmdexec("""set param ?t 'TBLX';""")
    output = _dbrootdci.cmdexec("""execute show_hist;""")
    if cqdval == '0':
        _dbrootdci.expect_selected_msg(output, '0')
        _dbrootdci.unexpect_warning_msg(output)
    else:
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY1 * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY2 * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX._SALT_ * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_selected_msg(output, '3')
        output = _dbrootdci.cmdexec("""execute reason_blank;""")
        _dbrootdci.expect_str_token(output, 'PASS')

    stmt = """update statistics for table TBLX on necessary columns;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _dbrootdci.cmdexec("""execute show_hist;""")
    if cqdval == '0':
        _dbrootdci.expect_selected_msg(output, '0')
        _dbrootdci.unexpect_warning_msg(output)
    else:
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY1 * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY2 * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX._SALT_ * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_selected_msg(output, '3')
        output = _dbrootdci.cmdexec("""execute reason_i;""")
        _dbrootdci.expect_str_token(output, 'PASS')

    stmt = ("""showstats for table TBLX on existing column;""")
    output = _dci.cmdexec(stmt)
    if cqdval == '0':
        _dci.expect_any_substr(output, """No Histograms exist for the""" +
                               """ requested columns or groups""")
    else:
        _dci.expect_any_substr(output, """1000000 * 1000000 COLKEY""")
        _dci.expect_any_substr(output, """1000000 * 1009 COLKEY2""")
        _dci.expect_any_substr(output, """1000000 * 8 \"_SALT_\"""")
        _dci.unexpect_any_substr(output, """COLA""")
        _dci.unexpect_any_substr(output, """COLB""")
        _dci.unexpect_any_substr(output, """COLC""")
        _dci.unexpect_any_substr(output, """COLD""")
        _dci.unexpect_any_substr(output, """COLE""")
        _dci.unexpect_any_substr(output, """COLF""")
        _dci.unexpect_any_substr(output, """COLG""")
    _dci.expect_complete_msg(output)
    clear_stats("TBLX")

    # ==========================
    # key and non-key column stats to be generated
    qryid = 'Q3'
    stmt = """prepare XX from select *
from TBLX where (colkey1 between 500000 and 550000)
and colf like '9%';"""
    output = _dci.cmdexec(stmt)
    if cqdval == '0':
        _dci.unexpect_warning_msg(output)
    else:
        _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY1)*TBLX""")
        _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY2)*TBLX""")
        _dci.expect_any_substr(output, """WARNING[6011]*(COLF)*TBLX""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLA)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLB)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLC)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLD)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLE)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLG)*""")
        _dci.unexpect_warning_msg(output, '6010')
    _dci.expect_prepared_msg(output)
    output = _dbrootdci.cmdexec("""set param ?t 'TBLX';""")
    output = _dbrootdci.cmdexec("""execute show_hist;""")
    if cqdval == '0':
        _dbrootdci.expect_selected_msg(output, '0')
        _dbrootdci.unexpect_warning_msg(output)
    else:
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY1 * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY2 * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLF * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX._SALT_ * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_selected_msg(output, '4')
        output = _dbrootdci.cmdexec("""execute reason_blank;""")
        _dbrootdci.expect_str_token(output, 'PASS')

    stmt = """update statistics for table TBLX on necessary columns;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _dbrootdci.cmdexec("""execute show_hist;""")
    if cqdval == '0':
        _dbrootdci.expect_selected_msg(output, '0')
        _dbrootdci.unexpect_warning_msg(output)
    else:
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY1 * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY2 * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLF * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX._SALT_ * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_selected_msg(output, '4')
        output = _dbrootdci.cmdexec("""execute reason_i;""")
        _dbrootdci.expect_str_token(output, 'PASS')

    stmt = ("""showstats for table TBLX on existing column;""")
    output = _dci.cmdexec(stmt)
    if cqdval == '0':
        _dci.expect_any_substr(output, """No Histograms exist for the""" +
                               """ requested columns or groups""")
    else:
        _dci.expect_any_substr(output, """1000000 * 1000000 COLKEY""")
        _dci.expect_any_substr(output, """1000000 * 1009 COLKEY2""")
        _dci.expect_any_substr(output, """1000000 * 109 COLF""")
        _dci.expect_any_substr(output, """1000000 * 8 \"_SALT_\"""")
        _dci.unexpect_any_substr(output, """COLA""")
        _dci.unexpect_any_substr(output, """COLB""")
        _dci.unexpect_any_substr(output, """COLC""")
        _dci.unexpect_any_substr(output, """COLD""")
        _dci.unexpect_any_substr(output, """COLE""")
        _dci.unexpect_any_substr(output, """COLG""")
    _dci.expect_complete_msg(output)
    clear_stats("TBLX")

    # ==========================
    # multi-columns to be generated
    qryid = 'Q4'
    stmt = """prepare XX from select cole, colb
from TBLX where colkey1 between 100000 and 500000
group by colb, cole;"""
    output = _dci.cmdexec(stmt)
    if cqdval == '0':
        _dci.unexpect_warning_msg(output)
    else:
        _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY1)*TBLX""")
        _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY2)*TBLX""")
        _dci.expect_any_substr(output, """WARNING[6011]*(COLB)*TBLX""")
        _dci.expect_any_substr(output, """WARNING[6011]*(COLE)*TBLX""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLA)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLC)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLD)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLF)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLG)*""")
        if cqdval == '4':
            _dci.expect_any_substr(output,
                                   """WARNING[6010]*(COLB, COLE)*TBLX""")
        else:
            _dci.unexpect_warning_msg(output, '6010')
        _dci.expect_prepared_msg(output)
    output = _dbrootdci.cmdexec("""set param ?t 'TBLX';""")
    output = _dbrootdci.cmdexec("""execute show_hist;""")
    if cqdval == '0':
        _dbrootdci.expect_selected_msg(output, '0')
        _dbrootdci.unexpect_warning_msg(output)
    else:
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY1 * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY2 * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLB * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLE * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX._SALT_ * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.unexpect_any_substr(output, """COLA""")
        _dbrootdci.unexpect_any_substr(output, """COLC""")
        _dbrootdci.unexpect_any_substr(output, """COLD""")
        _dbrootdci.unexpect_any_substr(output, """COLF""")
        _dbrootdci.unexpect_any_substr(output, """COLG""")
        if cqdval == '4':
            _dbrootdci.expect_selected_msg(output, '7')
        else:
            _dbrootdci.expect_selected_msg(output, '5')
        output = _dbrootdci.cmdexec("""execute reason_blank;""")
        _dbrootdci.expect_str_token(output, 'PASS')

    stmt = """update statistics for table TBLX on necessary columns;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _dbrootdci.cmdexec("""execute show_hist;""")
    if cqdval == '0':
        _dbrootdci.expect_selected_msg(output, '0')
        _dbrootdci.unexpect_warning_msg(output)
    else:
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY1 * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY2 * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLB * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLE * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX._SALT_ * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.unexpect_any_substr(output, """COLA""")
        _dbrootdci.unexpect_any_substr(output, """COLC""")
        _dbrootdci.unexpect_any_substr(output, """COLD""")
        _dbrootdci.unexpect_any_substr(output, """COLF""")
        _dbrootdci.unexpect_any_substr(output, """COLG""")
        if cqdval == '4':
            _dbrootdci.expect_selected_msg(output, '7')
        else:
            _dbrootdci.expect_selected_msg(output, '5')
        output = _dbrootdci.cmdexec("""execute reason_i;""")
        _dbrootdci.expect_str_token(output, 'PASS')

    stmt = ("""showstats for table TBLX on existing column;""")
    output = _dci.cmdexec(stmt)
    if cqdval == '0':
        _dci.expect_any_substr(output, """No Histograms exist for the""" +
                               """ requested columns or groups""")
    else:
        _dci.expect_any_substr(output, """1000000 * 1000000 COLKEY""")
        _dci.expect_any_substr(output, """1000000 * 1009 COLKEY2""")
        _dci.expect_any_substr(output, """1000000 * 109 COLB""")
        _dci.expect_any_substr(output, """1000000 * 1 COLE""")
        _dci.expect_any_substr(output, """1000000 * 8 \"_SALT_\"""")
        if cqdval == '4':
            _dci.expect_any_substr(output, """1000000 * 109 COLB, COLE""")
        _dci.unexpect_any_substr(output, """COLA""")
        _dci.unexpect_any_substr(output, """COLC""")
        _dci.unexpect_any_substr(output, """COLD""")
        _dci.unexpect_any_substr(output, """COLF""")
        _dci.unexpect_any_substr(output, """COLG""")
    _dci.expect_complete_msg(output)
    clear_stats("TBLX")

    # ==========================
    qryid = 'Q5'
    stmt = """prepare XX from select *
from TBLY where colkey1 < 4000 and colkey1 > 40;"""
    output = _dci.cmdexec(stmt)
    if cqdval == '0':
        _dci.unexpect_warning_msg(output)
        _dci.expect_prepared_msg(output)
    else:
        _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY1)*TBLY""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLKEY2)""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLA)""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLB)""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLC)""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLD)""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLE)""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLF)""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLG)""")
        _dci.unexpect_warning_msg(output, '6010')
    output = _dbrootdci.cmdexec("""set param ?t 'TBLY';""")
    output = _dbrootdci.cmdexec("""execute show_hist;""")
    if cqdval == '0':
        _dbrootdci.expect_selected_msg(output, '0')
        _dbrootdci.unexpect_warning_msg(output)
    else:
        _dbrootdci.expect_any_substr(output, """TBLY.COLKEY1 * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_selected_msg(output, '1')
        output = _dbrootdci.cmdexec("""execute reason_blank;""")
        _dbrootdci.expect_str_token(output, 'PASS')

    stmt = """update statistics for table TBLY on necessary columns;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _dbrootdci.cmdexec("""execute show_hist;""")
    if cqdval == '0':
        _dbrootdci.expect_selected_msg(output, '0')
        _dbrootdci.unexpect_warning_msg(output)
    else:
        _dbrootdci.expect_any_substr(output, """TBLY.COLKEY1 * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_selected_msg(output, '1')
        output = _dbrootdci.cmdexec("""execute reason_i;""")
        _dbrootdci.expect_str_token(output, 'PASS')

    stmt = ("""showstats for table TBLY on existing column;""")
    output = _dci.cmdexec(stmt)
    if cqdval == '0':
        _dci.expect_any_substr(output, """No Histograms exist for the""" +
                               """ requested columns or groups""")
    else:
        _dci.expect_any_substr(output, """90000 * 90000 COLKEY""")
        _dci.unexpect_any_substr(output, """COLKEY2""")
        _dci.unexpect_any_substr(output, """_SALT_""")
        _dci.unexpect_any_substr(output, """COLA""")
        _dci.unexpect_any_substr(output, """COLB""")
        _dci.unexpect_any_substr(output, """COLC""")
        _dci.unexpect_any_substr(output, """COLD""")
        _dci.unexpect_any_substr(output, """COLE""")
        _dci.unexpect_any_substr(output, """COLF""")
        _dci.unexpect_any_substr(output, """COLG""")
    clear_stats("TBLY")

    # ==========================
    # single columns stats for join
    qryid = 'Q6'
    stmt = """prepare XX from select *
from TBLX, TBLY where TBLX.colkey1 = TBLY.colkey1;"""
    output = _dci.cmdexec(stmt)
    if cqdval == '0':
        _dci.unexpect_warning_msg(output)
        _dci.expect_prepared_msg(output)
    else:
        _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY1)*TBLX""")
        _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY2)*TBLX""")
        _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY1)*TBLY""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLKEY2)*TBLY""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLA)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLB)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLC)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLD)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLE)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLF)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLG)*""")
        _dci.unexpect_warning_msg(output, '6010')
    output = _dbrootdci.cmdexec("""set param ?t 'TBLX';""")
    output = _dbrootdci.cmdexec("""execute show_hist;""")
    if cqdval == '0':
        _dbrootdci.expect_selected_msg(output, '0')
        _dbrootdci.unexpect_warning_msg(output)
    else:
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY1 * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY2 * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX._SALT_ * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_selected_msg(output, '3')
        output = _dbrootdci.cmdexec("""execute reason_blank;""")
        _dbrootdci.expect_str_token(output, 'PASS')

    stmt = """update statistics for table TBLX on necessary columns;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _dbrootdci.cmdexec("""execute show_hist;""")
    if cqdval == '0':
        _dbrootdci.expect_selected_msg(output, '0')
        _dbrootdci.unexpect_warning_msg(output)
    else:
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY1 * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY2 * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX._SALT_ * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_selected_msg(output, '3')
        output = _dbrootdci.cmdexec("""execute reason_i;""")
        _dbrootdci.expect_str_token(output, 'PASS')

    stmt = ("""showstats for table TBLX on existing column;""")
    output = _dci.cmdexec(stmt)
    if cqdval == '0':
        _dci.expect_any_substr(output, """No Histograms exist for the""" +
                               """ requested columns or groups""")
    else:
        _dci.expect_any_substr(output, """1000000 * 1000000 COLKEY""")
        _dci.expect_any_substr(output, """1000000 * 1009 COLKEY2""")
        _dci.expect_any_substr(output, """1000000 * 8 \"_SALT_\"""")
        _dci.unexpect_any_substr(output, """COLA""")
        _dci.unexpect_any_substr(output, """COLB""")
        _dci.unexpect_any_substr(output, """COLC""")
        _dci.unexpect_any_substr(output, """COLD""")
        _dci.unexpect_any_substr(output, """COLE""")
        _dci.unexpect_any_substr(output, """COLF""")
        _dci.unexpect_any_substr(output, """COLG""")
    clear_stats("TBLX")

    output = _dbrootdci.cmdexec("""set param ?t 'TBLY';""")
    output = _dbrootdci.cmdexec("""execute show_hist;""")
    if cqdval == '0':
        _dbrootdci.expect_selected_msg(output, '0')
        _dbrootdci.unexpect_warning_msg(output)
    else:
        _dbrootdci.expect_any_substr(output, """TBLY.COLKEY1 * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_selected_msg(output, '1')
        output = _dbrootdci.cmdexec("""execute reason_blank;""")
        _dbrootdci.expect_str_token(output, 'PASS')

    stmt = """update statistics for table TBLY on necessary columns;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _dbrootdci.cmdexec("""execute show_hist;""")
    if cqdval == '0':
        _dbrootdci.expect_selected_msg(output, '0')
        _dbrootdci.unexpect_warning_msg(output)
    else:
        _dbrootdci.expect_any_substr(output, """TBLY.COLKEY1 * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_selected_msg(output, '1')
        output = _dbrootdci.cmdexec("""execute reason_i;""")
        _dbrootdci.expect_str_token(output, 'PASS')

    stmt = ("""showstats for table TBLY on existing column;""")
    output = _dci.cmdexec(stmt)
    if cqdval == '0':
        _dci.expect_any_substr(output, """No Histograms exist for the""" +
                               """ requested columns or groups""")
    else:
        _dci.expect_any_substr(output, """90000 * 90000 COLKEY""")
        _dci.unexpect_any_substr(output, """COLKEY2""")
        _dci.unexpect_any_substr(output, """\"_SALT_\"""")
        _dci.unexpect_any_substr(output, """COLA""")
        _dci.unexpect_any_substr(output, """COLB""")
        _dci.unexpect_any_substr(output, """COLC""")
        _dci.unexpect_any_substr(output, """COLD""")
        _dci.unexpect_any_substr(output, """COLE""")
        _dci.unexpect_any_substr(output, """COLF""")
        _dci.unexpect_any_substr(output, """COLG""")
    clear_stats("TBLY")

    # ==========================
    # single columns stats for join
    qryid = 'Q7'
    stmt = """prepare XX from select *
from TBLX, TBLY where TBLX.cold between date'1996-06-04' and date '1997-01-05'
and TBLY.colc like '50%';"""
    output = _dci.cmdexec(stmt)
    if cqdval == '0':
        _dci.unexpect_warning_msg(output)
    else:
        _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY1)*TBLX""")
        _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY2)*TBLX""")
        _dci.expect_any_substr(output, """WARNING[6011]*(COLD)*TBLX""")
        _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY1)*TBLY""")
        _dci.expect_any_substr(output, """WARNING[6011]*(COLC)*TBLY""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLKEY2)*TBLY""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLA)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLB)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLC)*TBLX""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLD)*TBLY""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLE)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLF)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLG)*""")
        _dci.unexpect_warning_msg(output, '6010')
    _dci.expect_prepared_msg(output)
    output = _dbrootdci.cmdexec("""set param ?t 'TBLX';""")
    output = _dbrootdci.cmdexec("""execute show_hist;""")
    if cqdval == '0':
        _dbrootdci.expect_selected_msg(output, '0')
        _dbrootdci.unexpect_warning_msg(output)
    else:
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY1 * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY2 * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLD * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX._SALT_ * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_selected_msg(output, '4')
        output = _dbrootdci.cmdexec("""execute reason_blank;""")
        _dbrootdci.expect_str_token(output, 'PASS')

    stmt = """update statistics for table TBLX on necessary columns;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _dbrootdci.cmdexec("""execute show_hist;""")
    if cqdval == '0':
        _dbrootdci.expect_selected_msg(output, '0')
        _dbrootdci.unexpect_warning_msg(output)
    else:
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY1 * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY2 * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLD * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX._SALT_ * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_selected_msg(output, '4')
        output = _dbrootdci.cmdexec("""execute reason_i;""")
        _dbrootdci.expect_str_token(output, 'PASS')

    stmt = ("""showstats for table TBLX on existing column;""")
    output = _dci.cmdexec(stmt)
    if cqdval == '0':
        _dci.expect_any_substr(output, """No Histograms exist for the""" +
                               """ requested columns or groups""")
    else:
        _dci.expect_any_substr(output, """1000000 * 1000000 COLKEY""")
        _dci.expect_any_substr(output, """1000000 * 1009 COLKEY2""")
        _dci.expect_any_substr(output, """1000000 * 1000 COLD""")
        _dci.expect_any_substr(output, """1000000 * 8 \"_SALT_\"""")
        _dci.unexpect_any_substr(output, """COLA""")
        _dci.unexpect_any_substr(output, """COLB""")
        _dci.unexpect_any_substr(output, """COLC""")
        _dci.unexpect_any_substr(output, """COLE""")
        _dci.unexpect_any_substr(output, """COLF""")
        _dci.unexpect_any_substr(output, """COLG""")
    clear_stats("TBLX")

    output = _dbrootdci.cmdexec("""set param ?t 'TBLY';""")
    output = _dbrootdci.cmdexec("""execute show_hist;""")
    if cqdval == '0':
        _dbrootdci.expect_selected_msg(output, '0')
        _dbrootdci.unexpect_warning_msg(output)
    else:
        _dbrootdci.expect_any_substr(output, """TBLY.COLKEY1 * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLY.COLC * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_selected_msg(output, '2')
        output = _dbrootdci.cmdexec("""execute reason_blank;""")
        _dbrootdci.expect_str_token(output, 'PASS')

    stmt = """update statistics for table TBLY on necessary columns;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _dbrootdci.cmdexec("""execute show_hist;""")
    if cqdval == '0':
        _dbrootdci.expect_selected_msg(output, '0')
        _dbrootdci.unexpect_warning_msg(output)
    else:
        _dbrootdci.expect_any_substr(output, """TBLY.COLKEY1 * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLY.COLC * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_selected_msg(output, '2')
        output = _dbrootdci.cmdexec("""execute reason_i;""")
        _dbrootdci.expect_str_token(output, 'PASS')

    stmt = ("""showstats for table TBLY on existing column;""")
    output = _dci.cmdexec(stmt)
    if cqdval == '0':
        _dci.expect_any_substr(output, """No Histograms exist for the""" +
                               """ requested columns or groups""")
    else:
        _dci.expect_any_substr(output, """90000 * 90000 COLKEY""")
        _dci.expect_any_substr(output, """90000 * 1009 COLC""")
        _dci.unexpect_any_substr(output, """COLA""")
        _dci.unexpect_any_substr(output, """COLB""")
        _dci.unexpect_any_substr(output, """COLD""")
        _dci.unexpect_any_substr(output, """COLE""")
        _dci.unexpect_any_substr(output, """COLF""")
        _dci.unexpect_any_substr(output, """COLG""")
    clear_stats("TBLY")

    # ==========================
    # multi-column stats for join
    qryid = 'Q8'
    stmt = """prepare XX from select * from TBLX join TBLY
on TBLX.cold = TBLY.cold and TBLX.colf = TBLY.colf;"""
    output = _dci.cmdexec(stmt)
    if cqdval == '0':
        _dci.unexpect_warning_msg(output)
        _dci.expect_prepared_msg(output)
    else:
        _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY1)*TBLX""")
        _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY2)*TBLX""")
        _dci.expect_any_substr(output, """WARNING[6011]*(COLD)*TBLX""")
        _dci.expect_any_substr(output, """WARNING[6011]*(COLF)*TBLX""")
        _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY1)*TBLY""")
        _dci.expect_any_substr(output, """WARNING[6011]*(COLD)*TBLY""")
        _dci.expect_any_substr(output, """WARNING[6011]*(COLF)*TBLY""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLKEY2)*TBLY""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLA)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLB)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLC)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLE)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLG)*""")
        if cqdval == '3' or cqdval == '4':
            _dci.expect_any_substr(output,
                                   """WARNING[6010]*(COLD, COLF)*TBLX""")
            _dci.expect_any_substr(output,
                                   """WARNING[6010]*(COLD, COLF)*TBLY""")
        else:
            _dci.unexpect_warning_msg(output, '6010')
    output = _dbrootdci.cmdexec("""set param ?t 'TBLX';""")
    output = _dbrootdci.cmdexec("""execute show_hist;""")
    if cqdval == '0':
        _dbrootdci.expect_selected_msg(output, '0')
        _dbrootdci.unexpect_warning_msg(output)
    else:
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY1 * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY2 * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLD * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLF * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX._SALT_ * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.unexpect_any_substr(output, """COLA""")
        _dbrootdci.unexpect_any_substr(output, """COLB""")
        _dbrootdci.unexpect_any_substr(output, """COLC""")
        _dbrootdci.unexpect_any_substr(output, """COLE""")
        _dbrootdci.unexpect_any_substr(output, """COLG""")
        if cqdval == '3' or cqdval == '4':
            _dbrootdci.expect_selected_msg(output, '7')
        else:
            _dbrootdci.expect_selected_msg(output, '5')
        output = _dbrootdci.cmdexec("""execute reason_blank;""")
        _dbrootdci.expect_str_token(output, 'PASS')

    stmt = """update statistics for table TBLX on necessary columns;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _dbrootdci.cmdexec("""execute show_hist;""")
    if cqdval == '0':
        _dbrootdci.expect_selected_msg(output, '0')
        _dbrootdci.unexpect_warning_msg(output)
    else:
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY1 * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY2 * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLD * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLF * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX._SALT_ * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.unexpect_any_substr(output, """COLA""")
        _dbrootdci.unexpect_any_substr(output, """COLB""")
        _dbrootdci.unexpect_any_substr(output, """COLC""")
        _dbrootdci.unexpect_any_substr(output, """COLE""")
        _dbrootdci.unexpect_any_substr(output, """COLG""")
        if cqdval == '3' or cqdval == '4':
            _dbrootdci.expect_selected_msg(output, '7')
        else:
            _dbrootdci.expect_selected_msg(output, '5')
        output = _dbrootdci.cmdexec("""execute reason_i;""")
        _dbrootdci.expect_str_token(output, 'PASS')

    stmt = ("""showstats for table TBLX on existing column;""")
    output = _dci.cmdexec(stmt)
    if cqdval == '0':
        _dci.expect_any_substr(output, """No Histograms exist for the""" +
                               """ requested columns or groups""")
    else:
        _dci.expect_any_substr(output, """1000000 * 1000000 COLKEY""")
        _dci.expect_any_substr(output, """1000000 * 1009 COLKEY2""")
        _dci.expect_any_substr(output, """1000000 * 1000 COLD""")
        _dci.expect_any_substr(output, """1000000 * 109 COLF""")
        _dci.expect_any_substr(output, """1000000 * 8 \"_SALT_\"""")
        _dci.unexpect_any_substr(output, """COLA""")
        _dci.unexpect_any_substr(output, """COLB""")
        _dci.unexpect_any_substr(output, """COLC""")
        _dci.unexpect_any_substr(output, """COLE""")
        _dci.unexpect_any_substr(output, """COLG""")
    clear_stats("TBLX")

    output = _dbrootdci.cmdexec("""set param ?t 'TBLY';""")
    output = _dbrootdci.cmdexec("""execute show_hist;""")
    if cqdval == '0':
        _dbrootdci.expect_selected_msg(output, '0')
        _dbrootdci.unexpect_warning_msg(output)
    else:
        _dbrootdci.expect_any_substr(output, """TBLY.COLKEY1 * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLY.COLD * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLY.COLF * 0001-01-01 00:00:00 * 0""")
        if cqdval == '3' or cqdval == '4':
            _dbrootdci.expect_selected_msg(output, '5')
        else:
            _dbrootdci.expect_selected_msg(output, '3')
        output = _dbrootdci.cmdexec("""execute reason_blank;""")
        _dbrootdci.expect_str_token(output, 'PASS')

    stmt = """update statistics for table TBLY on necessary columns;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _dbrootdci.cmdexec("""execute show_hist;""")
    if cqdval == '0':
        _dbrootdci.expect_selected_msg(output, '0')
        _dbrootdci.unexpect_warning_msg(output)
    else:
        _dbrootdci.expect_any_substr(output, """TBLY.COLKEY1 * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLY.COLD * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLY.COLF * 0001-01-01 00:00:00 * 0 I""")
        if cqdval == '3' or cqdval == '4':
            _dbrootdci.expect_selected_msg(output, '5')
        else:
            _dbrootdci.expect_selected_msg(output, '3')
        output = _dbrootdci.cmdexec("""execute reason_i;""")
        _dbrootdci.expect_str_token(output, 'PASS')

    stmt = ("""showstats for table TBLY on existing column;""")
    output = _dci.cmdexec(stmt)
    if cqdval == '0':
        _dci.expect_any_substr(output, """No Histograms exist for the""" +
                               """ requested columns or groups""")
    else:
        _dci.expect_any_substr(output, """90000 * 90000 COLKEY""")
        _dci.expect_any_substr(output, """90000 * 1000 COLD""")
        _dci.expect_any_substr(output, """90000 * 109 COLF""")
        _dci.unexpect_any_substr(output, """_SALT_""")
        _dci.unexpect_any_substr(output, """COLA""")
        _dci.unexpect_any_substr(output, """COLB""")
        _dci.unexpect_any_substr(output, """COLC""")
        _dci.unexpect_any_substr(output, """COLE""")
        _dci.unexpect_any_substr(output, """COLG""")
    clear_stats("TBLY")

    # ==========================
    # multi-column stats for join
    qryid = 'Q9'
    stmt = """prepare XX from select * from TBLX, TBLY
where TBLX.cola = TBLY.cola
and TBLX.cold = TBLY.cold
and TBLX.colb = TBLY.cole;"""
    output = _dci.cmdexec(stmt)
    if cqdval == '0':
        _dci.unexpect_warning_msg(output)
        _dci.expect_prepared_msg(output)
    else:
        _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY1)*TBLX""")
        _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY2)*TBLX""")
        _dci.expect_any_substr(output, """WARNING[6011]*(COLA)*TBLX""")
        _dci.expect_any_substr(output, """WARNING[6011]*(COLB)*TBLX""")
        _dci.expect_any_substr(output, """WARNING[6011]*(COLD)*TBLX""")
        _dci.expect_any_substr(output, """WARNING[6011]*(COLA)*TBLY""")
        _dci.expect_any_substr(output, """WARNING[6011]*(COLD)*TBLY""")
        _dci.expect_any_substr(output, """WARNING[6011]*(COLE)*TBLY""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLE)*TBLX""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLKEY2)*TBLY""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLB)*TBLY""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLC)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLF)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLG)*""")
        if cqdval == '3' or cqdval == '4':
            _dci.expect_any_substr(output,
                                   """WARNING[6010]*(COLA, COLB, COLD)*TBLX""")
            _dci.expect_any_substr(output,
                                   """WARNING[6010]*(COLA, COLD, COLE)*TBLY""")
        else:
            _dci.unexpect_warning_msg(output, '6010')
    output = _dbrootdci.cmdexec("""set param ?t 'TBLX';""")
    output = _dbrootdci.cmdexec("""execute show_hist;""")
    if cqdval == '0':
        _dbrootdci.expect_selected_msg(output, '0')
        _dbrootdci.unexpect_warning_msg(output)
    else:
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY1 * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY2 * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLA * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLB * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLD * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX._SALT_ * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.unexpect_any_substr(output, """COLC""")
        _dbrootdci.unexpect_any_substr(output, """COLE""")
        _dbrootdci.unexpect_any_substr(output, """COLF""")
        _dbrootdci.unexpect_any_substr(output, """COLG""")
        if cqdval == '3' or cqdval == '4':
            _dbrootdci.expect_selected_msg(output, '9')
        else:
            _dbrootdci.expect_selected_msg(output, '6')
        output = _dbrootdci.cmdexec("""execute reason_blank;""")
        _dbrootdci.expect_str_token(output, 'PASS')

    stmt = """update statistics for table TBLX on necessary columns;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _dbrootdci.cmdexec("""execute show_hist;""")
    if cqdval == '0':
        _dbrootdci.expect_selected_msg(output, '0')
        _dbrootdci.unexpect_warning_msg(output)
    else:
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY1 * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY2 * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLA * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLB * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLD * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX._SALT_ * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.unexpect_any_substr(output, """COLC""")
        _dbrootdci.unexpect_any_substr(output, """COLE""")
        _dbrootdci.unexpect_any_substr(output, """COLF""")
        _dbrootdci.unexpect_any_substr(output, """COLG""")
        if cqdval == '3' or cqdval == '4':
            _dbrootdci.expect_selected_msg(output, '9')
        else:
            _dbrootdci.expect_selected_msg(output, '6')
        output = _dbrootdci.cmdexec("""execute reason_i;""")
        _dbrootdci.expect_str_token(output, 'PASS')

    stmt = ("""showstats for table TBLX on existing column;""")
    output = _dci.cmdexec(stmt)
    if cqdval == '0':
        _dci.expect_any_substr(output, """No Histograms exist for the""" +
                               """ requested columns or groups""")
    else:
        _dci.expect_any_substr(output, """1000000 * 1000000 COLKEY""")
        _dci.expect_any_substr(output, """1000000 * 1009 COLKEY2""")
        _dci.expect_any_substr(output, """1000000 * 1009 COLA""")
        _dci.expect_any_substr(output, """1000000 * 109 COLB""")
        _dci.expect_any_substr(output, """1000000 * 1000 COLD""")
        _dci.expect_any_substr(output, """1000000 * 8 \"_SALT_\"""")
        _dci.unexpect_any_substr(output, """COLC""")
        _dci.unexpect_any_substr(output, """COLE""")
        _dci.unexpect_any_substr(output, """COLG""")
    clear_stats("TBLX")

    output = _dbrootdci.cmdexec("""set param ?t 'TBLY';""")
    output = _dbrootdci.cmdexec("""execute show_hist;""")
    if cqdval == '0':
        _dbrootdci.expect_selected_msg(output, '0')
        _dbrootdci.unexpect_warning_msg(output)
    else:
        _dbrootdci.expect_any_substr(output, """TBLY.COLKEY1 * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLY.COLA * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLY.COLD * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLY.COLE * 0001-01-01 00:00:00 * 0""")
        if cqdval == '3' or cqdval == '4':
            _dbrootdci.expect_selected_msg(output, '7')
        else:
            _dbrootdci.expect_selected_msg(output, '4')
        output = _dbrootdci.cmdexec("""execute reason_blank;""")
        _dbrootdci.expect_str_token(output, 'PASS')

    stmt = """update statistics for table TBLY on necessary columns;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _dbrootdci.cmdexec("""execute show_hist;""")
    if cqdval == '0':
        _dbrootdci.expect_selected_msg(output, '0')
        _dbrootdci.unexpect_warning_msg(output)
    else:
        _dbrootdci.expect_any_substr(output, """TBLY.COLKEY1 * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLY.COLA * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLY.COLD * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLY.COLE * 0001-01-01 00:00:00 * 0 I""")
        if cqdval == '3' or cqdval == '4':
            _dbrootdci.expect_selected_msg(output, '7')
        else:
            _dbrootdci.expect_selected_msg(output, '4')
        output = _dbrootdci.cmdexec("""execute reason_i;""")
        _dbrootdci.expect_str_token(output, 'PASS')

    stmt = ("""showstats for table TBLY on existing column;""")
    output = _dci.cmdexec(stmt)
    if cqdval == '0':
        _dci.expect_any_substr(output, """No Histograms exist for the""" +
                               """ requested columns or groups""")
    else:
        _dci.expect_any_substr(output, """90000 * 90000 COLKEY""")
        _dci.expect_any_substr(output, """90000 * 1009 COLA""")
        _dci.expect_any_substr(output, """90000 * 1000 COLD""")
        _dci.expect_any_substr(output, """90000 * 1 COLE""")
        _dci.unexpect_any_substr(output, """_SALT_""")
        _dci.unexpect_any_substr(output, """COLB""")
        _dci.unexpect_any_substr(output, """COLC""")
        _dci.unexpect_any_substr(output, """COLF""")
        _dci.unexpect_any_substr(output, """COLG""")
    clear_stats("TBLY")

    # ==========================
    # single column stats
    qryid = 'Q10'
    stmt = """prepare XX from select * from TBLX
where cola between 700 and 1000 and cold between date'1999-01-30'
and date'1999-06-01' order by cold;"""
    output = _dci.cmdexec(stmt)
    if cqdval == '0':
        _dci.unexpect_warning_msg(output)
        _dci.expect_prepared_msg(output)
    else:
        _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY1)*TBLX""")
        _dci.expect_any_substr(output, """WARNING[6011]*(COLKEY2)*TBLX""")
        _dci.expect_any_substr(output, """WARNING[6011]*(COLA)*TBLX""")
        _dci.expect_any_substr(output, """WARNING[6011]*(COLD)*TBLX""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLB)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLC)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLE)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLF)*""")
        _dci.unexpect_any_substr(output, """WARNING[6011]*(COLG)*""")
        _dci.unexpect_warning_msg(output, '6010')
    output = _dbrootdci.cmdexec("""set param ?t 'TBLX';""")
    output = _dbrootdci.cmdexec("""execute show_hist;""")
    if cqdval == '0':
        _dbrootdci.expect_selected_msg(output, '0')
        _dbrootdci.unexpect_warning_msg(output)
    else:
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY1 * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY2 * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLA * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLD * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_any_substr(output, """TBLX._SALT_ * 0001-01-01 00:00:00 * 0""")
        _dbrootdci.expect_selected_msg(output, '5')
        output = _dbrootdci.cmdexec("""execute reason_blank;""")
        _dbrootdci.expect_str_token(output, 'PASS')

    stmt = """update statistics for table TBLX on necessary columns;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _dbrootdci.cmdexec("""execute show_hist;""")
    if cqdval == '0':
        _dbrootdci.expect_selected_msg(output, '0')
        _dbrootdci.unexpect_warning_msg(output)
    else:
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY1 * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLKEY2 * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLA * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX.COLD * 0001-01-01 00:00:00 * 0 I""")
        _dbrootdci.expect_any_substr(output, """TBLX._SALT_ * 0001-01-01 00:00:00 * 0 I""")
        _dci.expect_selected_msg(output, '5')
        output = _dbrootdci.cmdexec("""execute reason_i;""")
        _dbrootdci.expect_str_token(output, 'PASS')

    stmt = ("""showstats for table TBLX on existing column;""")
    output = _dci.cmdexec(stmt)
    if cqdval == '0':
        _dci.expect_any_substr(output, """No Histograms exist for the""" +
                               """ requested columns or groups""")
    else:
        _dci.expect_any_substr(output, """1000000 * 1000000 COLKEY""")
        _dci.expect_any_substr(output, """1000000 * 1009 COLKEY2""")
        _dci.expect_any_substr(output, """1000000 * 1009 COLA""")
        _dci.expect_any_substr(output, """1000000 * 1000 COLD""")
        _dci.expect_any_substr(output, """1000000 * 8 \"_SALT_\"""")
        _dci.unexpect_any_substr(output, """COLB""")
        _dci.unexpect_any_substr(output, """COLC""")
        _dci.unexpect_any_substr(output, """COLE""")
        _dci.unexpect_any_substr(output, """COLF""")
        _dci.unexpect_any_substr(output, """COLG""")
    clear_stats("TBLX")

    output = _dci.cmdexec("""cqd USTAT_AUTO_MISSING_STATS_LEVEL reset;""")
    _dci.expect_complete_msg(output)
    output = _dci.cmdexec("""cqd HIST_MISSING_STATS_WARNING_LEVEL reset;""")
    _dci.expect_complete_msg(output)
    return
