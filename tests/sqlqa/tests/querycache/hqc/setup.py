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


def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci

    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    _dci.setup_schema(defs.my_schema)

    output = _dci.cmdexec("""drop table g00 cascade;""")

    stmt = """create table g00(
colkey int not null, colint int, coldate date,
colsint smallint, colnum numeric(9,4), colchar char(26),
collint largeint, colts timestamp,
colvchr varchar(75), colflt float, coldec decimal(9),
colintvl interval day(18));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into g00 values (
100, 200, date'2014-08-22',
16384, 32768.1230, '   defghijklmno0123456789',
1099511627776, timestamp'1972-02-08 00:11:22',
'q  ABCDEFGHIJKLMNOPQRSTUWXYZ9876543210zyxwutsrq  ', 0.0, 1.1,
interval '3' day);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into g00 values (
-300, -400, date'1972-02-08',
-16383, -0.9397, '9876543210defghijklmno   ',
-1099511626667, timestamp'2014-08-22 22:11:00',
'q  qrstuwxyz0123456789ABCDEFGHIJKLMNOPQRSTUWXYZ  ', -99.88, -77.66,
interval '97' day);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into g00 values (
-500, -600, date'1996-09-30',
-8192, -0.6431, 'apples bananas grapes',
-1, timestamp'2014-06-12 22:11:00',
'mangoes pears pineapple blueberries', 555.88, 4.66,
interval '14' day);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into g00 values (
-77, -88, date'1996-09-30',
-4096, -0.137, 'kiwi cantelope',
-1, timestamp'2000-01-01 11:11:11',
'honeydew strawberries watermelon', -10.10, -1000.0,
interval '1' day);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into g00 values (
-99, -11, date'1996-10-31',
-1024, 0.6431, 'lettuce tomato',
-1, timestamp'2000-01-01 11:11:11',
'bacon cheese onion', 1.1, 89.6,
interval '1' day);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into g00 values (
66, 33, date'1985-09-30',
-4096, -4096.1000, 'lemon merengue cherry pie',
-1, timestamp'2010-10-10 10:10:10',
'key-lime chocolate mousse banana bread', -1.1, -1.0,
interval '6' day);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """prepare get_hkey from
select left(hkey,100) as hkey
from table(HybridQueryCacheEntries('USER', 'LOCAL'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """prepare get_num_hits from
select num_hits
from table(HybridQueryCacheEntries('USER', 'LOCAL'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """prepare get_num_pliterals from
select num_pliterals
from table(HybridQueryCacheEntries('USER', 'LOCAL'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """prepare get_pliterals from
select converttohex(left(pliterals,10)) as pliterals
from table(HybridQueryCacheEntries('USER', 'LOCAL'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """prepare get_num_npliterals from
select num_npliterals
from table(HybridQueryCacheEntries('USER', 'LOCAL'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """prepare get_npliterals from
select left(npliterals,10) as npliterals
from table(HybridQueryCacheEntries('USER', 'LOCAL'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """prepare dump_entries from
select left(hkey,300) as hkey, num_hits,
num_pliterals, converttohex(left(pliterals, 500)),
num_npliterals, converttohex(left(npliterals, 500))
from table(HybridQueryCacheEntries('USER', 'LOCAL'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """prepare show_entries from
select left(hkey,150) as hkey, num_hits,
num_pliterals, left(pliterals, 25),
num_npliterals, left(npliterals, 25)
from table(HybridQueryCacheEntries('USER', 'LOCAL'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    output = _dci.cmdexec("set param ?exp_key 'dummy';")
    output = _dci.cmdexec("set param ?exp_num_hits 0;")
    output = _dci.cmdexec("set param ?exp_num_pliterals 0;")
    output = _dci.cmdexec("set param ?exp_num_npliterals 0;")
    output = _dci.cmdexec("set param ?exp_pliterals '20202020';")
    output = _dci.cmdexec("set param ?exp_npliterals '20202020';")
    stmt = """prepare chk_entry_nolit from
select case cnt when 1 then 'PASS' else 'FAIL' end
from (select count(*) as cnt
from table(HybridQueryCacheEntries('USER', 'LOCAL'))
where hkey = ?exp_hkey
and num_hits = ?exp_num_hits
and num_pliterals = 0
and num_npliterals = 0) aa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """prepare chk_entry_plit from
select case cnt when 1 then 'PASS' else 'FAIL' end
from (select count(*) as cnt
from table(HybridQueryCacheEntries('USER', 'LOCAL'))
where hkey = ?exp_hkey
and num_hits = ?exp_num_hits
and num_pliterals = ?exp_num_pliterals
and converttohex(pliterals) = ?exp_pliterals
and num_npliterals = 0) bb;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """prepare chk_entry_nplit from
select case cnt when 1 then 'PASS' else 'FAIL' end
from (select count(*) as cnt
from table(HybridQueryCacheEntries('USER', 'LOCAL'))
where hkey = ?exp_hkey
and num_hits = ?exp_num_hits
and num_pliterals = 0
and num_npliterals = ?exp_num_npliterals
and converttohex(npliterals) = ?exp_npliterals) cc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """prepare chk_entry_bothlit from
select case cnt when 1 then 'PASS' else 'FAIL' end
from (select count(*) as cnt
from table(HybridQueryCacheEntries('USER', 'LOCAL'))
where hkey = ?exp_hkey
and num_hits = ?exp_num_hits
and num_pliterals = ?exp_num_pliterals
and converttohex(pliterals) = ?exp_pliterals
and num_npliterals = ?exp_num_npliterals
and converttohex(npliterals) = ?exp_npliterals) dd;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = """prepare chk_entry_exists from
select case when cnt = 0 then 'DOES NOT EXIST' else 'EXISTS' end
from (select count(*) as cnt
from table(HybridQueryCacheEntries('USER', 'LOCAL'))
where hkey = ?exp_hkey) ee;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    output = _dci.cmdexec("""cqd HQC_MAX_VALUES_PER_KEY reset;""")
    _dci.expect_complete_msg(output)


def resetHQC():
    global _testmgr
    global _testlist
    global _dci

    output = _dci.cmdexec("cqd HYBRID_QUERY_CACHE 'OFF';")
    _dci.expect_complete_msg(output)
    output = _dci.cmdexec("cqd QUERY_CACHE '0';")
    _dci.expect_complete_msg(output)
    output = _dci.cmdexec("cqd QUERY_CACHE reset;")
    _dci.expect_complete_msg(output)
    if defs.genexp == 0:
        output = _dci.cmdexec("cqd HYBRID_QUERY_CACHE 'ON';")
        _dci.expect_complete_msg(output)
        stmt = """cqd QUERY_CACHE_USE_CONVDOIT_FOR_BACKPATCH 'ON';"""
        output = _dci.cmdexec(stmt)
        _dci.expect_complete_msg(output)
        output = _dci.cmdexec("""cqd DYNAMIC_HISTOGRAM_COMPRESSION 'OFF';""")
        _dci.expect_complete_msg(output)
        verifyHQCempty()
    else:
        output = _dci.cmdexec("""cqd SHOWCONTROL_SHOW_ALL 'ON';""")
        output = _dci.cmdexec("""showcontrol default HYBRID_QUERY_CACHE;""")


def setupHQClog(hqc_log=None):
    global _testmgr
    global _testlist
    global _dci

    output = _dci.cmdexec("""cqd HQC_LOG 'ON';""")
    _dci.expect_complete_msg(output)
    if hqc_log is None:
        hqc_log = 'hqc.log'
    output = _dci.cmdexec("""cqd HQC_LOG_FILE '""" + hqc_log + """';""")
    _dci.expect_complete_msg(output)
    resetHQC()


def verifyHQCEntryExists():
    global _testmgr
    global _testlist
    global _dci

    if defs.genexp == 0:
        stmt = """set param ?exp_hkey '""" + defs.hkey + """';"""
        output = _dci.cmdexec(stmt)
        stmt = """set param ?exp_num_hits """ + str(defs.num_hits) + """;"""
        output = _dci.cmdexec(stmt)
        stmt = ("""set param ?exp_num_pliterals """
                + str(defs.num_pliterals) + """;""")
        output = _dci.cmdexec(stmt)
        stmt = ("""set param ?exp_num_npliterals """
                + str(defs.num_npliterals) + """;""")
        output = _dci.cmdexec(stmt)

        if defs.num_pliterals == 0 and defs.num_npliterals == 0:
            # no literals
            output = _dci.cmdexec("""execute chk_entry_nolit;""")
        elif defs.num_pliterals != 0 and defs.num_npliterals == 0:
            # parameterized literals
            stmt = """set param ?exp_pliterals '""" + defs.pliterals + "';"
            output = _dci.cmdexec(stmt)
            output = _dci.cmdexec("execute chk_entry_plit;")
        elif defs.num_pliterals == 0 and defs.num_npliterals != 0:
            # non-parameterized literals
            stmt = """set param ?exp_npliterals '""" + defs.npliterals + "';"
            output = _dci.cmdexec(stmt)
            output = _dci.cmdexec("execute chk_entry_nplit;")
        elif defs.num_pliterals != 0 and defs.num_npliterals != 0:
            # both parameterized and non-parameterized literals present
            stmt = """set param ?exp_pliterals '""" + defs.pliterals + "';"
            output = _dci.cmdexec(stmt)
            stmt = """set param ?exp_npliterals '""" + defs.npliterals + "';"
            output = _dci.cmdexec(stmt)
            output = _dci.cmdexec("execute chk_entry_bothlit;")
        _dci.expect_str_token(output, 'PASS')
        # DEBUG
        dumpHQCEntries()
    else:
        output = _dci.cmdexec("""select *
from table(HybridQueryCacheEntries('USER', 'LOCAL'));""")
        _dci.expect_selected_msg(output, '0')


def dumpHQCEntries():
    global _testmgr
    global _testlist
    global _dci

    output = _dci.cmdexec("""execute dump_entries;""")


def verifyHQCnumEntries(exp_num):
    global _testmgr
    global _testlist
    global _dci

    if defs.genexp == 0:
        stmt = """select count(*)
from table(HybridQueryCacheEntries('USER', 'LOCAL'));"""
        output = _dci.cmdexec(stmt)
        _dci.expect_str_token(output, exp_num)


def verifyHQCempty():
    global _testmgr
    global _testlist
    global _dci

    if defs.genexp == 0:
        stmt = """execute get_hkey;"""
        output = _dci.cmdexec(stmt)
        _dci.expect_selected_msg(output, '0')


def getEntryNumHits():
    global _testmgr
    global _testlist
    global _dci

    if defs.genexp == 0:
        stmt = """set param ?exp_hkey '""" + defs.hkey + """';"""
        output = _dci.cmdexec(stmt)
        stmt = """set param ?exp_num_hits """ + str(defs.num_hits) + """;"""
        output = _dci.cmdexec(stmt)
        stmt = ("""set param ?exp_num_pliterals """
                + str(defs.num_pliterals) + """;""")
        output = _dci.cmdexec(stmt)
        stmt = ("""set param ?exp_num_npliterals """
                + str(defs.num_npliterals) + """;""")
        output = _dci.cmdexec(stmt)

        if defs.num_pliterals == 0 and defs.num_npliterals == 0:
            # no literals
            stmt = """select num_hits
from table(HybridQueryCacheEntries('USER', 'LOCAL'))
where hkey = ?exp_hkey
and num_pliterals = 0
and num_npliterals = 0;"""
        elif defs.num_pliterals != 0 and defs.num_npliterals == 0:
            # parameterized literals
            stmt = """set param ?exp_pliterals '""" + defs.pliterals + "';"
            output = _dci.cmdexec(stmt)
            stmt = """select num_hits
from table(HybridQueryCacheEntries('USER', 'LOCAL'))
where hkey = ?exp_hkey
and num_pliterals = ?exp_num_pliterals
and converttohex(pliterals) = ?exp_pliterals
and num_npliterals = 0;"""
        elif defs.num_pliterals == 0 and defs.num_npliterals != 0:
            # non-parameterized literals
            stmt = """set param ?exp_npliterals '""" + defs.npliterals + "';"
            output = _dci.cmdexec(stmt)
            stmt = """select num_hits
from table(HybridQueryCacheEntries('USER', 'LOCAL'))
where hkey = ?exp_hkey
and num_pliterals = 0
and num_npliterals = ?exp_num_npliterals
and converttohex(npliterals) = ?exp_npliterals;"""
        _output = _dci.cmdexec(stmt)


def verifyHQCEntryNOTExists():
    global _testmgr
    global _testlist
    global _dci

    if defs.genexp == 0:
        stmt = """set param ?exp_hkey '""" + defs.hkey + """';"""
        output = _dci.cmdexec(stmt)
        output = _dci.cmdexec("""execute chk_entry_exists;""")
        _dci.expect_any_substr(output, 'DOES NOT EXIST')
        # DEBUG
        dumpHQCEntries()


def prepexec():
    global _testmgr
    global _testlist
    global _dci

    output = _dci.cmdexec(defs.qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_complete_msg(output)
