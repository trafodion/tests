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
from ...lib import gvars
import defs
import setup

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


def test_eqts(desc="""equals & timestamp"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: equals & timestamp"""

    output = _dci.cmdexec("""drop table F00TS cascade;""")

    output = _dci.cmdexec("""cqd COMP_BOOL_226 'ON';""")
    _dci.expect_complete_msg(output)
    stmt = """cqd TRAF_LOAD_PREP_TMP_LOCATION '/bulkload/';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    output = _dci.cmdexec("""cqd TRAF_LOAD_TAKE_SNAPSHOT 'OFF';""")
    _dci.expect_complete_msg(output)

    stmt = """create table F00TS(
colkey int not null primary key,
colts timestamp)
salt using 8 partitions;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """load into F00TS select
c1+c2*10+c3*100+c4*1000+c5*10000+c6*100000, --colkey
converttimestamp(210614299200000000 + (1000000 *
(c1+c2*10+c3*100+c4*1000+c5*10000+c6*100000))) --colts
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

    stmt = """update statistics for table F00TS on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    """showstats for table F00TS on colts detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 1000
--and histogram_id =    and table_uid =
where interval_number between 7 and 17;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 1
--and histogram_id =    and table_uid =
where interval_number in (18,37,46,47);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 5000
--and histogram_id =    and table_uid =
where interval_number between 19 and 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 100
--and histogram_id =    and table_uid =
where interval_number = 21;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 16000
--and histogram_id =    and table_uid =
where interval_number between 38 and 45;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 10000
--and histogram_id =    and table_uid =
where interval_number between 25 and 36;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """showstats for table F00TS on colts detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # workaround for lp bug 1409937
    output = _dci.cmdexec("""cqd CACHE_HISTOGRAMS 'OFF';""")
    _dci.expect_complete_msg(output)
    output = _dci.cmdexec("""cqd CACHE_HISTOGRAMS reset;""")
    _dci.expect_complete_msg(output)

    output = _dci.cmdexec("""cqd COMP_BOOL_226 reset;""")
    _dci.expect_complete_msg(output)
    output = _dci.cmdexec("""cqd TRAF_LOAD_PREP_TMP_LOCATION reset;""")
    _dci.expect_complete_msg(output)
    output = _dci.cmdexec("""cqd TRAF_LOAD_TAKE_SNAPSHOT reset;""")
    _dci.expect_complete_msg(output)

    ## ==================================
    ## EQUAL PREDICATE ON timestamp COLUMN
    ## ==================================
    # showstats for table F00TS on coldate detail;

    #setup.setupHQClog()
    setup.resetHQC()
    output = _dci.cmdexec("""cqd HQC_MAX_VALUES_PER_KEY '1';""")
    _dci.expect_complete_msg(output)

    # exceeds last interval upper boundary
    # expect = Not HQC Cacheable but added to SQC
    stmt = defs.prepXX + """select * from F00TS
where colts = timestamp'1962-01-12 22:33:44';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00TS WHERE COLTS = TIMESTAMP #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '313936322D30312D31322032323A33333A34340A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # preceeds interval 0 upper boundary
    # expect = Not HQC Cacheable but added to SQC
    stmt = defs.prepXX + """select * from F00TS
where colts = timestamp'1961-12-31 23:59:59';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00TS WHERE COLTS = TIMESTAMP #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '313936322D30312D31322032323A33333A34340A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # cqd query_cache '0';"""
    # cqd query_cache reset;
    setup.resetHQC()

    # add plan 1
    # interval 50 ['1962-01-12 08:13:19' - '1962-01-12 13:46:39')
    # rowcount/uec = 20000/20000
    # interval 48 - 50 merged/collapsed
    # interval extension boundaries ['1962-01-11 21:06:39' -
    #     '1962-01-12 13:46:39')
    # expect = HQC::AddEntry(): passed
    # add hqc entry, plan 1, 0 hits
    stmt = defs.prepXX + """select * from F00TS
where colts = timestamp'1962-01-12 13:46:39';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '1962-01-12 13:46:39')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00TS WHERE COLTS = TIMESTAMP #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '313936322D30312D31322031333A34363A33390A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc entry exists, plan 1, 1 hits
    stmt = defs.prepXX + """select * from F00TS
where colts = timestamp'1962-01-11 21:06:40';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '1962-01-11 21:06:40')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00TS WHERE COLTS = TIMESTAMP #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '313936322D30312D31322031333A34363A33390A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    setup.verifyHQCnumEntries('1')

    # replace plan 1
    # interval 47 ['1962-01-11 15:33:19' - '1962-01-11 21:06:39')
    # rowcount/uec = 20000/1
    # expect = HQC performed an interval extension
    # expect = HQC cache entry replaced. Entry has <1> hits
    # expect = HQC::AddEntry(): passed
    # hqc entry exists, plan 1, 0 hits
    stmt = defs.prepXX + """select * from F00TS
where colts = timestamp'1962-01-11 21:06:39';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '1962-01-11 21:06:39')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00TS WHERE COLTS = TIMESTAMP #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '313936322D30312D31312032313A30363A33390A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    setup.verifyHQCnumEntries('1')

    # expect = Found in HQC, HQC backpatch OK
    # hqc entry exists, plan 1, 1 hits
    stmt = defs.prepXX + """select * from F00TS
where colts = timestamp'1962-01-11 15:33:20';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '1962-01-11 15:33:20')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00TS WHERE COLTS = TIMESTAMP #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '313936322D30312D31312032313A30363A33390A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc entry exists, plan 1, 2 hits
    stmt = defs.prepXX + """select * from F00TS
where colts = timestamp'1962-01-11 17:44:33';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '1962-01-11 17:44:33')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00TS WHERE COLTS = TIMESTAMP #NP# ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '313936322D30312D31312032313A30363A33390A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc entry exists, plan 1, 3 hits
    stmt = defs.prepXX + """select * from F00TS
where colts = timestamp'1962-01-11 16:33:44';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '1962-01-11 16:33:44')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00TS WHERE COLTS = TIMESTAMP #NP# ;"""
    defs.num_hits = 3
    defs.num_pliterals = 1
    defs.pliterals = '313936322D30312D31312032313A30363A33390A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    setup.verifyHQCnumEntries('1')

    # replace plan 1
    # interval 43 ['1962-01-10 17:19:59' - '1962-01-10 22:53:19')
    # rowcount/uec = 20000/16000
    # intervals 38 - 45 merged/collapsed
    # interval extension boundaries ['1962-01-09 13:33:19' -
    #     '1962-01-11 09:59:59'
    # expect = HQC performed an interval extension
    # expect = HQC cache entry replaced. Entry has <3> hits
    # expect = HQC::AddEntry(): passed
    # hqc entry exists, plan 1, 0 hits
    stmt = defs.prepXX + """select * from F00TS
where colts = timestamp'1962-01-10 22:53:19';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '1962-01-10 22:53:19')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00TS WHERE COLTS = TIMESTAMP #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '313936322D30312D31302032323A35333A31390A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc entry exists, plan 1, 1 hits
    stmt = defs.prepXX + """select * from F00TS
where colts = timestamp'1962-01-09 13:33:20';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '1962-01-09 13:33:20')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00TS WHERE COLTS = TIMESTAMP #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '313936322D30312D31302032323A35333A31390A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    setup.verifyHQCnumEntries('1')

    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_TS00A')

    # interval 37, same selectivity as interval 46, 47
    # expect = nothing in hqc log; SQC hit
    stmt = defs.prepXX + """select * from F00TS
where colts = timestamp'1962-01-09 13:33:19';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '1962-01-09 13:33:19')
    _dci.expect_selected_msg(output, '1')

    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_TS00A')

    # replace plan 1
    # interval 28 ['1962-01-07 05:59:59' - '1962-01-07 11:33:19')
    # rowcount/uec = 20000/10000
    # intervals 25 - 36 merged/collapsed
    # interval extension boundaries ['1962-01-06 13:19:59' -
    #     '1962-01-09 07:59:59'
    # expect = HQC performed an interval extension
    # expect = HQC cache entry replaced. Entry has <1> hits
    # expect = HQC::AddEntry(): passed
    # hqc entry exists, plan 1, 0 hits
    stmt = defs.prepXX + """select * from F00TS
where colts = timestamp'1962-01-07 11:33:19';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '1962-01-07 11:33:19')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00TS WHERE COLTS = TIMESTAMP #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '313936322D30312D30372031313A33333A31390A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    setup.verifyHQCnumEntries('1')

    # expect = Found in HQC, HQC backpatch OK
    # hqc entry exists, plan 1, 1 hits
    stmt = defs.prepXX + """select * from F00TS
where colts = timestamp'1962-01-09 07:59:59';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '1962-01-09 07:59:59')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00TS WHERE COLTS = TIMESTAMP #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '313936322D30312D30372031313A33333A31390A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc entry exists, plan 1, 2 hits
    stmt = defs.prepXX + """select * from F00TS
where colts = timestamp'1962-01-06 13:20:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '1962-01-06 13:20:00')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00TS WHERE COLTS = TIMESTAMP #NP# ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '313936322D30312D30372031313A33333A31390A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc entry exists, plan 1, 3 hits
    stmt = defs.prepXX + """select * from F00TS
where colts = timestamp'1962-01-07 05:59:59';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '1962-01-07 05:59:59')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00TS WHERE COLTS = TIMESTAMP #NP# ;"""
    defs.num_hits = 3
    defs.num_pliterals = 1
    defs.pliterals = '313936322D30312D30372031313A33333A31390A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    setup.verifyHQCnumEntries('1')

    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_TS00B')

    # interval 23, same selectivity as interval 48 - 50
    # expect = nothing in hqc log; SQC hit
    stmt = defs.prepXX + """select * from F00TS
where colts = timestamp'1962-01-06 07:46:38';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '1962-01-06 07:46:38')
    _dci.expect_selected_msg(output, '1')

    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_TS00B')

    # replace plan 1
    # interval 21 ['1962-01-05 15:06:39' - '1962-01-05 20:39:59')
    # expect = HQC performed an interval extension
    # expect = HQC cache entry replaced. Entry has <3> hits
    # expect = HQC::AddEntry(): passed
    # hqc entry exists, plan 1, 0 hits
    stmt = defs.prepXX + """select * from F00TS
where colts = timestamp'1962-01-05 20:39:59';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '1962-01-05 20:39:59')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00TS WHERE COLTS = TIMESTAMP #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '313936322D30312D30352032303A33393A35390A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    setup.verifyHQCnumEntries('1')

    # replace plan 1
    # interval 19 ['1962-01-05 03:59:59' - '1962-01-05 09:33:19')
    # intervals 19 - 20 merged/collapsed
    # interval extension boundaries ['1962-01-05 03:59:59' -
    #     '1962-01-05 15:06:39')
    # expect = HQC performed an interval extension
    # expect = HQC cache entry replaced. Entry has <0> hits
    # expect = HQC::AddEntry(): passed
    # hqc entry exists, plan 1, 0 hits
    stmt = defs.prepXX + """select * from F00TS
where colts = timestamp'1962-01-05 04:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '1962-01-05 04:00:00')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00TS WHERE COLTS = TIMESTAMP #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '313936322D30312D30352030343A30303A30300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    setup.verifyHQCnumEntries('1')

    # expect = Found in HQC, HQC backpatch OK
    # hqc entry exists, plan 1, 1 hits
    stmt = defs.prepXX + """select * from F00TS
where colts = timestamp'1962-01-05 15:06:39';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '1962-01-05 15:06:39')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00TS WHERE COLTS = TIMESTAMP #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '313936322D30312D30352030343A30303A30300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    setup.verifyHQCnumEntries('1')

    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_TS00C')

    # interval 18, same selectivity as interval 37, 46, 47
    # expect = nothing in hqc log; SQC hit
    stmt = defs.prepXX + """select * from F00TS
where colts = timestamp'1962-01-05 03:59:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '1962-01-05 03:59:00')
    _dci.expect_selected_msg(output, '1')

    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_TS00C')

    # replace plan 1
    # interval 13 ['1962-01-03 18:39:59' - '1962-01-04 00:13:19')
    # intervals 7 - 17 merged/collapsed
    # interval extension boundaries ['1962-01-02 09:19:59' -
    #     '1962-01-04 22:26:39')
    # expect = HQC performed an interval extension
    # expect = HQC cache entry replaced. Entry has <1> hits
    # expect = HQC::AddEntry(): passed
    # hqc entry exists, plan 1, 0 hits
    stmt = defs.prepXX + """select * from F00TS
where colts = timestamp'1962-01-04 00:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '1962-01-04 00:00:00')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00TS WHERE COLTS = TIMESTAMP #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '313936322D30312D30342030303A30303A30300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    setup.verifyHQCnumEntries('1')

    # expect = Found in HQC, HQC backpatch OK
    # hqc entry exists, plan 1, 1 hits
    stmt = defs.prepXX + """select * from F00TS
where colts = timestamp'1962-01-04 00:13:19';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '1962-01-04 00:13:19')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00TS WHERE COLTS = TIMESTAMP #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '313936322D30312D30342030303A30303A30300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc entry exists, plan 1, 2 hits
    stmt = defs.prepXX + """select * from F00TS
where colts = timestamp'1962-01-02 09:20:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '1962-01-02 09:20:00')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00TS WHERE COLTS = TIMESTAMP #NP# ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '313936322D30312D30342030303A30303A30300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc entry exists, plan 1, 3 hits
    stmt = defs.prepXX + """select * from F00TS
where colts = timestamp'1962-01-04 22:26:39';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '1962-01-04 22:26:39')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00TS WHERE COLTS = TIMESTAMP #NP# ;"""
    defs.num_hits = 3
    defs.num_pliterals = 1
    defs.pliterals = '313936322D30312D30342030303A30303A30300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    setup.verifyHQCnumEntries('1')

    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_TS00D')

    # interval 0
    # expect = nothing in hqc log; SQC hit
    stmt = defs.prepXX + """select * from F00TS
where colts = timestamp'1962-01-01 00:00:00';"""

    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_TS00D')

    output = _dci.cmdexec("""drop table F00TS cascade;""")
    _dci.expect_complete_msg(output)

    output = _dci.cmdexec("""cqd HQC_MAX_VALUES_PER_KEY reset;""")
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)
