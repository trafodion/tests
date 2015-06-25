# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2015 Hewlett-Packard Development Company, L.P.
#
#  Licensed under the Apache License, Version 2.0 (the "License");"""
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


def test_eqvchr(desc="""equals & varchar"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: equals & varchar"""

    output = _dci.cmdexec("""drop table F00VCHR cascade;""")

    output = _dci.cmdexec("""cqd COMP_BOOL_226 'ON';""")
    _dci.expect_complete_msg(output)
    stmt = """cqd TRAF_LOAD_PREP_TMP_LOCATION '/bulkload/';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    output = _dci.cmdexec("""cqd TRAF_LOAD_TAKE_SNAPSHOT 'OFF';""")
    _dci.expect_complete_msg(output)

    stmt = """create table F00VCHR(
colvchr varchar(75) not null primary key)
salt using 8 partitions;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """load into F00VCHR select
c1 || c2 || c3 || c4 || c5 || c6  || '789'
from (values(1)) t
transpose 'a','b','c','d','e','f','g','h','i','j','k','l','m' as c1
transpose 'n','o','p','q','r','s','t','u','v','w','x','y','z' as c2
transpose 'A','B','C','D','E','F','G','H','I','J','K','L','M' as c3
transpose 'N','O','P','Q','R','S','T','U','V','W','X','Y','Z' as c4
transpose '1','2','3','4','5','6','7','8','9','0','!','@','#' as c5
transpose '$','^','&','?','/','{','}','[',']','+','-','<','>' as c6
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    output = _dci.cmdexec("""update statistics for table F00VCHR
on every column;""")
    _dci.expect_complete_msg(output)

    output = _dci.cmdexec("""showstats for table F00VCHR
on existing columns detail;""")
    _dci.expect_complete_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 1000
--and histogram_id =    and table_uid =
where interval_number between 7 and 17
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 1
--and histogram_id =    and table_uid =
where interval_number in (18,37,46,47)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 5000
--and histogram_id =    and table_uid =
where interval_number between 19 and 20
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 35000
--and histogram_id =    and table_uid =
where interval_number = 21
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 16000
--and histogram_id =    and table_uid =
where interval_number between 38 and 45
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 50000
--and histogram_id =    and table_uid =
where interval_number between 25 and 36
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 65000
--and histogram_id =    and table_uid =
where interval_number between 42 and 46
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 500
--and histogram_id =    and table_uid =
where interval_number in (39,41,47,51)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 72000
--and histogram_id =    and table_uid =
where interval_number between 55 and 58
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 12500
--and histogram_id =    and table_uid =
where interval_number in (53,54,60,61)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """showstats for table F00VCHR on colvchr detail;"""
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
    ## EQUAL PREDICATE ON VARCHAR COLUMN
    ## ==================================
    # showstats for table F00VCHR on colvchr detail;"""

    #setup.setupHQClog()
    setup.resetHQC()
    output = _dci.cmdexec("""cqd HQC_MAX_VALUES_PER_KEY '2';""")
    _dci.expect_complete_msg(output)

    # beyond last interval upper boundary
    # expect = Not HQC cacheable but added to SQC
    stmt = defs.prepXX + ("""select * from F00VCHR""" +
                          """ where colvchr = 'aaaaaaaaa';""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')

    # beyond first interval upper boundary
    stmt = defs.prepXX + ("""select * from F00VCHR""" +
                          """ where colvchr = 'zzzzzzzzz';""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00VCHR WHERE COLVCHR = #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '27616161616161616161270A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    setup.verifyHQCnumEntries('1')

    # cqd query_cache '0';
    # cqd query_cache reset;
    setup.resetHQC()

    # add plan 1
    # interval 62 [mxDU2/789 - mzMZ@}789) rowcount/uec = 77852/77852
    # expect = HQC::AddEntry: passed
    # add entry to cache, plan 1, 0 hits
    stmt = defs.prepXX + ("""select * from F00VCHR""" +
                          """ where colvchr = 'mzMZ@}789';""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00VCHR WHERE COLVCHR = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '276D7A4D5A407D373839270A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    setup.verifyHQCnumEntries('1')

    # add plan 2
    # interval 60 [mrKW!&789 - muHO6]789) rowcount/uec = 77852/12500
    # intervals 60 - 61 merged/collapsed
    # interval extension boundaries [mrKW!&789 - mxDU2/789)
    # expect = HQC::AddEntry(): passed
    # hqc key exists, plan 2, 0 hits
    stmt = defs.prepXX + ("""select * from F00VCHR""" +
                          """ where colvchr = 'msKW!&789';""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00VCHR WHERE COLVCHR = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '276D734B572126373839270A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 2, 1 hits
    stmt = defs.prepXX + ("""select * from F00VCHR""" +
                          """ where colvchr = 'mxDU2/789';""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00VCHR WHERE COLVCHR = #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '276D734B572126373839270A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 2, 2 hits
    stmt = defs.prepXX + ("""select * from F00VCHR""" +
                          """ where colvchr = 'muHO6]789';""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00VCHR WHERE COLVCHR = #NP# ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '276D734B572126373839270A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    setup.verifyHQCnumEntries('2')

    # status:
    # plan 1 ('mzMZ@}789'): 0 hits
    # plan 2 ('msKW!&789'): 2 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_VCHR00A')

    # replace plan 1
    # interval 7 [bqEU@+789 - btBN5]789) rowcount/uec = 77851/1000
    # intervals 7 - 17 merged/collapsed
    # interval extension boundaries [bqEU@+789 - duES0-789)
    # expect = HQC performed an interval extension
    # expect = HQC cache entry replaced. Entry has <0> hits
    # expect = HQC::AddEntry(): passed
    # hqc key exists, should push out plan 1 which had 0 hits
    # hqc key exists, plan 1, 0 hits
    stmt = defs.prepXX + ("""select * from F00VCHR""" +
                          """ where colvchr = 'btBN5]789';""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00VCHR WHERE COLVCHR = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '276274424E355D373839270A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # status:
    # plan 1, replace ('btBN5]789'): 0 hits
    # plan 2 ('msKW!&789'): 2 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_VCHR00B')

    # again interval 62 which has been replaced in HQC already
    # expect = nothing in hqc log; SQC hit
    stmt = defs.prepXX + ("""select * from F00VCHR""" +
                          """ where colvchr = 'mzMZ@}789';""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '1')

    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_VCHR00B')

    # increase plan 2 to 3 hits
    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 2, 2 hits
    stmt = defs.prepXX + ("""select * from F00VCHR""" +
                          """ where colvchr = 'mvHO6]789';""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00VCHR WHERE COLVCHR = #NP# ;"""
    defs.num_hits = 3
    defs.num_pliterals = 1
    defs.pliterals = '276D734B572126373839270A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase plan 1 to 1 hits
    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 1, 1 hits
    stmt = defs.prepXX + ("""select * from F00VCHR""" +
                          """ where colvchr = 'coDR5/789';""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00VCHR WHERE COLVCHR = #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '276274424E355D373839270A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 1, 2 hits
    stmt = defs.prepXX + ("""select * from F00VCHR""" +
                          """ where colvchr = 'duES0-789';""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00VCHR WHERE COLVCHR = #NP# ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '276274424E355D373839270A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 1, 3 hits
    stmt = defs.prepXX + ("""select * from F00VCHR""" +
                          """ where colvchr = 'doLT9$789';""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00VCHR WHERE COLVCHR = #NP# ;"""
    defs.num_hits = 3
    defs.num_pliterals = 1
    defs.pliterals = '276274424E355D373839270A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 1, 4 hits
    stmt = defs.prepXX + ("""select * from F00VCHR""" +
                          """ where colvchr = 'cqMX0{789';""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00VCHR WHERE COLVCHR = #NP# ;"""
    defs.num_hits = 4
    defs.num_pliterals = 1
    defs.pliterals = '276274424E355D373839270A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 1, 5 hits
    stmt = defs.prepXX + ("""select * from F00VCHR""" +
                          """ where colvchr = 'brEU@+789';""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00VCHR WHERE COLVCHR = #NP# ;"""
    defs.num_hits = 5
    defs.num_pliterals = 1
    defs.pliterals = '276274424E355D373839270A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # status:
    # plan 1 ('btBN5]789'): 5 hits
    # plan 2 ('msKW!&789'): 3 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_VCHR00C')

    # replace plan 2
    # interval 18 [duES0-789 - dxAX8{789) rowcount/uec = 77852/1
    # expect = HQC performed an interval extension
    # expect = HQC cache entry replace. Entry has <3> hits
    # expect = HQC::AddEntry(): passed
    # hqc key exists, plan 2, 0 hits
    stmt = defs.prepXX + ("""select * from F00VCHR""" +
                          """ where colvchr = 'dvES0-789';""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00VCHR WHERE COLVCHR = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '2764764553302D373839270A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 2, 1 hits
    stmt = defs.prepXX + ("""select * from F00VCHR""" +
                          """ where colvchr = 'dxAX8{789';""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00VCHR WHERE COLVCHR = #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '2764764553302D373839270A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # status:
    # plan 1 ('btBN5]789'): 5 hits
    # plan 2 ('dvES0-789'): 1 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_VCHR00D')

    # replace plan 2
    # interval 58 [lzEX6{789 - mpBQ2>789)
    # intervals 55 - 58 merged/collapsed
    # interval extension boundaries [lrCT7$789 - mpBQ2>789)
    # expect = HQC performed an interval extension
    # expect = HQC cache entry replaced. Entry has <1> hits
    # expect = HQC::AddEntry(): passed
    # hqc key exists, plan 2, 0 hits
    stmt = defs.prepXX + ("""select * from F00VCHR""" +
                          """ where colvchr = 'mpBQ2>789';""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00VCHR WHERE COLVCHR = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '276D704251323E373839270A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # status:
    # plan 1 ('btBN5]789'): 5 hits
    # plan 2 ('mpBQ2>789'): 0 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_VCHR00E')

    # replace plan 2
    # interval 51 [ktDX!?789 - kwAP7+789)
    # expect = HQC performed an interval extension
    # expect = HQC cache entry replace. Entry has <0> hits
    # expect = HQC::AddEntry(): passed
    # hqc key exists, plan 2, 0 hits
    stmt = defs.prepXX + ("""select * from F00VCHR""" +
                          """ where colvchr = 'kuDX!?789';""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00VCHR WHERE COLVCHR = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '276B754458213F373839270A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 2, 1 hits
    stmt = defs.prepXX + ("""select * from F00VCHR""" +
                          """ where colvchr = 'kwAP7+789';""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00VCHR WHERE COLVCHR = #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '276B754458213F373839270A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # interval 47, same selectivity as interval 51
    # interval 47 [jvFN3&789 - jyBT!]789)
    # expect = nothing in hqc log; SQC hit
    stmt = defs.prepXX + ("""select * from F00VCHR""" +
                          """ where colvchr = 'jyBT!]789';""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '1')
    setup.dumpHQCEntries()

    # status:
    # plan 1 ('btBN5]789'): 5 hits
    # plan 2 ('kuDX!?789'): 1 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_VCHR00F')

    output = _dci.cmdexec("""drop table F00VCHR cascade;""")
    _dci.expect_complete_msg(output)

    output = _dci.cmdexec("""cqd HQC_MAX_VALUES_PER_KEY reset;""")
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)
