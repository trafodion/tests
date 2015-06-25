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


def test_eqsint(desc="""equals & small int"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: equals & small int"""

    output = _dci.cmdexec("""drop table F00SINT cascade;""")

    output = _dci.cmdexec("""cqd COMP_BOOL_226 'ON';""")
    _dci.expect_complete_msg(output)
    stmt = """cqd TRAF_LOAD_PREP_TMP_LOCATION '/bulkload/';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    output = _dci.cmdexec("""cqd TRAF_LOAD_TAKE_SNAPSHOT 'OFF';""")
    _dci.expect_complete_msg(output)

    stmt = """create table F00SINT(
colkey int not null primary key,
colsint smallint)
salt using 8 partitions;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """load into F00SINT select
c1+c2*10+c3*100+c4*1000+c5*10000+c6*100000, --colkey
mod(1000+c1+c2+c3*100+c4*1000+c5*10000+c6*100000, 32767) --colsint
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

    stmt = """update statistics for table F00SINT on colsint;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showstats for table F00SINT on colsint detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 297
where interval_number between 15 and 18
--and histogram_id =    and table_uid =
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 421
where interval_number between 24 and 27
--and histogram_id =    and table_uid =
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 99
where interval_number between 32 and 40
--and histogram_id =    and table_uid =
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 1
where interval_number = 44
--and histogram_id =    and table_uid =
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 570
where interval_number between 47 and 51
--and histogram_id =    and table_uid =
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """showstats for table F00SINT on colsint detail;"""
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
    ## EQUAL PREDICATE ON SMALLINT COLUMN
    ## ==================================
    # showstats for table F00SINT on colsint detail;

    #setup.setupHQClog()
    setup.resetHQC()
    output = _dci.cmdexec("""cqd HQC_MAX_VALUES_PER_KEY '4';""")
    _dci.expect_complete_msg(output)

    # add plan 1
    # interval 44 [24513 - 25269), rowcount/uec = 22460/1
    # expect = HQC::AddEntry(): passed
    # hqc entry added, plan 1, 0 hits
    stmt = defs.prepXX + """select * from F00SINT where colsint = 25269;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '73')
    defs.hkey = """SELECT * FROM F00SINT WHERE COLSINT = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '32353236390A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add plan 2
    # interval 8 [317 - 324), rowcount/uec = 1/1
    # expect = HQC::AddEntry(): passed
    # hqc entry added, plan 2, 0 hits
    stmt = defs.prepXX + """select * from F00SINT where colsint = 324;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00SINT WHERE COLSINT = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '3332340A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add plan 3
    # interval 5 [124 - 217), rowcount/uec = 2999/83
    # expect = HQC::AddEntry(): passed
    # hqc entry added, plan 3, 0 hits
    stmt = defs.prepXX + """select * from F00SINT where colsint = 210;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '36')
    defs.hkey = """SELECT * FROM F00SINT WHERE COLSINT = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '3231300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = found in HQC, HQC backpatch OK
    # hqc entry exists, plan 3, 1 hits
    stmt = defs.prepXX + """select * from F00SINT where colsint = 125;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '3')
    defs.hkey = """SELECT * FROM F00SINT WHERE COLSINT = #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '3231300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add plan 4
    # interval 51 [29765 - 30506), rowcount/uec = 22483/570
    # intervals 45 - 51 merged/collapsed
    # interval extension boundaries [25269 - 30506)
    # expect = HQC::AddEntry(): passed
    # add hqc key, plan 4, 0 hits
    stmt = defs.prepXX + """select * from F00SINT where colsint = 30500;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '55')
    defs.hkey = """SELECT * FROM F00SINT WHERE COLSINT = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '33303530300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 4, 1 hits
    stmt = defs.prepXX + """select * from F00SINT where colsint = 30506;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '73')
    defs.hkey = """SELECT * FROM F00SINT WHERE COLSINT = #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '33303530300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 4, 2 hits
    stmt = defs.prepXX + """select * from F00SINT where colsint = 26769;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '73')
    defs.hkey = """SELECT * FROM F00SINT WHERE COLSINT = #NP# ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '33303530300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 4, 3 hits
    stmt = defs.prepXX + """select * from F00SINT where colsint = 27000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '55')
    defs.hkey = """SELECT * FROM F00SINT WHERE COLSINT = #NP# ;"""
    defs.num_hits = 3
    defs.num_pliterals = 1
    defs.pliterals = '33303530300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 4, 4 hits
    stmt = defs.prepXX + """select * from F00SINT where colsint = 30000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '55')
    defs.hkey = """SELECT * FROM F00SINT WHERE COLSINT = #NP# ;"""
    defs.num_hits = 4
    defs.num_pliterals = 1
    defs.pliterals = '33303530300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 4, 5 hits
    stmt = defs.prepXX + """select * from F00SINT where colsint = 30506;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '73')
    defs.hkey = """SELECT * FROM F00SINT WHERE COLSINT = #NP# ;"""
    defs.num_hits = 5
    defs.num_pliterals = 1
    defs.pliterals = '33303530300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 4, 6 hits
    stmt = defs.prepXX + """select * from F00SINT where colsint = 26769;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '73')
    defs.hkey = """SELECT * FROM F00SINT WHERE COLSINT = #NP# ;"""
    defs.num_hits = 6
    defs.num_pliterals = 1
    defs.pliterals = '33303530300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # status:
    # plan 1: 0 hits
    # plan 2: 0 hits
    # plan 3: 1 hits
    # plan 4: 6 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_SINT00A')

    # replace plan 1
    # interval 43 [23770 - 24513) rowcount/uec = 22465/625
    # intervals 41 - 43 merged/collapsed
    # interval extension boundaries [22272 - 24513)
    # expect = HQC performed an interval extension
    # expect = HQC cache entry replaced. Entry has 0 hits.
    # expect = HQC::AddEntry(): passed
    # hqc key exists, replace plan 1, 0 hits
    stmt = defs.prepXX + """select * from F00SINT where colsint = 24513;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '21')
    defs.hkey = """SELECT * FROM F00SINT WHERE COLSINT = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '32343531330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 1, 1 hits
    stmt = defs.prepXX + """select * from F00SINT where colsint = 22273;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '69')
    defs.hkey = """SELECT * FROM F00SINT WHERE COLSINT = #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '32343531330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 1, 2 hits
    stmt = defs.prepXX + """select * from F00SINT where colsint = 24500;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '55')
    defs.hkey = """SELECT * FROM F00SINT WHERE COLSINT = #NP# ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '32343531330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # status:
    # plan 1: 2 hits
    # plan 2: 0 hits
    # plan 3: 1 hits
    # plan 4: 6 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_SINT00B')

    # replace plan 2
    # interval 24 [9838 - 10567) rowcount/uec = 22408/421
    # intervals 24 - 27 merged/collapsed
    # interval extension boundaries [9838 - 12735)
    # expect = HQC performed an interval extension
    # expect = HQC cache entry replaced. Entry has 0 hits.
    # expect = HQC::AddEntry(): passed
    # hqc key exists, replace plan 2, 0 hits
    stmt = defs.prepXX + """select * from F00SINT where colsint = 9839;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '73')
    defs.hkey = """SELECT * FROM F00SINT WHERE COLSINT = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '393833390A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 2, 1 hits
    stmt = defs.prepXX + """select * from F00SINT where colsint = 12735;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '69')
    defs.hkey = """SELECT * FROM F00SINT WHERE COLSINT = #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '393833390A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 2, 2 hits
    stmt = defs.prepXX + """select * from F00SINT where colsint = 12734;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '63')
    defs.hkey = """SELECT * FROM F00SINT WHERE COLSINT = #NP# ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '393833390A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 2, 3 hits
    stmt = defs.prepXX + """select * from F00SINT where colsint = 9840;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '69')
    defs.hkey = """SELECT * FROM F00SINT WHERE COLSINT = #NP# ;"""
    defs.num_hits = 3
    defs.num_pliterals = 1
    defs.pliterals = '393833390A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # status:
    # plan 1: 2 hits
    # plan 2: 3 hits
    # plan 3: 1 hits
    # plan 4: 6 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_SINT00C')

    # increase hits on plan 1
    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 1, 3 hits
    stmt = defs.prepXX + """select * from F00SINT where colsint = 22274;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '63')
    defs.hkey = """SELECT * FROM F00SINT WHERE COLSINT = #NP# ;"""
    defs.num_hits = 3
    defs.num_pliterals = 1
    defs.pliterals = '32343531330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 1, 4 hits
    stmt = defs.prepXX + """select * from F00SINT where colsint = 24512;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '28')
    defs.hkey = """SELECT * FROM F00SINT WHERE COLSINT = #NP# ;"""
    defs.num_hits = 4
    defs.num_pliterals = 1
    defs.pliterals = '32343531330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # status:
    # plan 1: 4 hits
    # plan 2: 3 hits
    # plan 3: 1 hits
    # plan 4: 6 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_SINT00D')

    # replace plan 3
    # interval 1 [0 - 17), rowcount/uec = 780/18
    # expect = HQC performed an interval extension
    # expect = HQC cache entry replaced. Entry has 1 hits
    # expect = HQC::AddEntry(): passed
    # hqc entry exists, replace plan 3, 0 hits
    stmt = defs.prepXX + """select * from F00SINT where colsint = 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '36')
    defs.hkey = """SELECT * FROM F00SINT WHERE COLSINT = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '31300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 3, 1 hits
    stmt = defs.prepXX + """select * from F00SINT where colsint = 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '69')
    defs.hkey = """SELECT * FROM F00SINT WHERE COLSINT = #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '31300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 3, 2 hits
    stmt = defs.prepXX + """select * from F00SINT where colsint = 17;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00SINT WHERE COLSINT = #NP# ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '31300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # status:
    # plan 1: 4 hits
    # plan 2: 3 hits
    # plan 3: 2 hits
    # plan 4: 6 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_SINT00E')

    # increase hits on plan 3
    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 3, 3 hits
    stmt = defs.prepXX + """select * from F00SINT where colsint = 16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '3')
    defs.hkey = """SELECT * FROM F00SINT WHERE COLSINT = #NP# ;"""
    defs.num_hits = 3
    defs.num_pliterals = 1
    defs.pliterals = '31300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 3, 4 hits
    stmt = defs.prepXX + """select * from F00SINT where colsint = 15;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '6')
    defs.hkey = """SELECT * FROM F00SINT WHERE COLSINT = #NP# ;"""
    defs.num_hits = 4
    defs.num_pliterals = 1
    defs.pliterals = '31300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 3, 5 hits
    stmt = defs.prepXX + """select * from F00SINT where colsint = 14;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '10')
    defs.hkey = """SELECT * FROM F00SINT WHERE COLSINT = #NP# ;"""
    defs.num_hits = 5
    defs.num_pliterals = 1
    defs.pliterals = '31300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # status:
    # plan 1: 4 hits
    # plan 2: 3 hits
    # plan 3: 5 hits
    # plan 4: 6 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_SINT00F')

    # increase hits on plan 1
    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 1, 5 hits
    stmt = defs.prepXX + """select * from F00SINT where colsint = 22275;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '55')
    defs.hkey = """SELECT * FROM F00SINT WHERE COLSINT = #NP# ;"""
    defs.num_hits = 5
    defs.num_pliterals = 1
    defs.pliterals = '32343531330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 1, 6 hits
    stmt = defs.prepXX + """select * from F00SINT where colsint = 24511;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '36')
    defs.hkey = """SELECT * FROM F00SINT WHERE COLSINT = #NP# ;"""
    defs.num_hits = 6
    defs.num_pliterals = 1
    defs.pliterals = '32343531330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 1, 7 hits
    stmt = defs.prepXX + """select * from F00SINT where colsint = 24510;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '45')
    defs.hkey = """SELECT * FROM F00SINT WHERE COLSINT = #NP# ;"""
    defs.num_hits = 7
    defs.num_pliterals = 1
    defs.pliterals = '32343531330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits on plan 3
    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 3, 6 hits
    stmt = defs.prepXX + """select * from F00SINT where colsint = 13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '15')
    defs.hkey = """SELECT * FROM F00SINT WHERE COLSINT = #NP# ;"""
    defs.num_hits = 6
    defs.num_pliterals = 1
    defs.pliterals = '31300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 3, 7 hits
    stmt = defs.prepXX + """select * from F00SINT where colsint = 12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '21')
    defs.hkey = """SELECT * FROM F00SINT WHERE COLSINT = #NP# ;"""
    defs.num_hits = 7
    defs.num_pliterals = 1
    defs.pliterals = '31300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 3, 8 hits
    stmt = defs.prepXX + """select * from F00SINT where colsint = 11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '28')
    defs.hkey = """SELECT * FROM F00SINT WHERE COLSINT = #NP# ;"""
    defs.num_hits = 8
    defs.num_pliterals = 1
    defs.pliterals = '31300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits on plan 2
    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 2, 4 hits
    stmt = defs.prepXX + """select * from F00SINT where colsint = 12733;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '55')
    defs.hkey = """SELECT * FROM F00SINT WHERE COLSINT = #NP# ;"""
    defs.num_hits = 4
    defs.num_pliterals = 1
    defs.pliterals = '393833390A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 2, 5 hits
    stmt = defs.prepXX + """select * from F00SINT where colsint = 12732;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '45')
    defs.hkey = """SELECT * FROM F00SINT WHERE COLSINT = #NP# ;"""
    defs.num_hits = 5
    defs.num_pliterals = 1
    defs.pliterals = '393833390A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 2, 6 hits
    stmt = defs.prepXX + """select * from F00SINT where colsint = 12731;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '36')
    defs.hkey = """SELECT * FROM F00SINT WHERE COLSINT = #NP# ;"""
    defs.num_hits = 6
    defs.num_pliterals = 1
    defs.pliterals = '393833390A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 2, 7 hits
    stmt = defs.prepXX + """select * from F00SINT where colsint = 12730;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '28')
    defs.hkey = """SELECT * FROM F00SINT WHERE COLSINT = #NP# ;"""
    defs.num_hits = 7
    defs.num_pliterals = 1
    defs.pliterals = '393833390A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # status:
    # plan 1: 7 hits
    # plan 2: 7 hits
    # plan 3: 8 hits
    # plan 4: 6 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_SINT00G')

    # replace plan 4
    # interval 32 [15631 - 16342) rowcount/uec = 22415/99
    # intervals 32 - 40 merged/collapsed
    # interval extension boundaries [15631 - 22272)
    # expect = HQC performed an interval extension
    # expect = HQC cache entry replaced. Entry has 6 hits.
    # expect = HQC::AddEntry(): passed
    # hqc key exists, replace plan 4, 0 hits
    stmt = defs.prepXX + """select * from F00SINT where colsint = 15632;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '45')
    defs.hkey = """SELECT * FROM F00SINT WHERE COLSINT = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '31353633320A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 4, 1 hits
    stmt = defs.prepXX + """select * from F00SINT where colsint = 22272;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '73')
    defs.hkey = """SELECT * FROM F00SINT WHERE COLSINT = #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '31353633320A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 4, 2 hits
    stmt = defs.prepXX + """select * from F00SINT where colsint = 15633;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '55')
    defs.hkey = """SELECT * FROM F00SINT WHERE COLSINT = #NP# ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '31353633320A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 4, 3 hits
    stmt = defs.prepXX + """select * from F00SINT where colsint = 15634;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '63')
    defs.hkey = """SELECT * FROM F00SINT WHERE COLSINT = #NP# ;"""
    defs.num_hits = 3
    defs.num_pliterals = 1
    defs.pliterals = '31353633320A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # status:
    # plan 1: 7 hits
    # plan 2: 7 hits
    # plan 3: 8 hits
    # plan 4: 3 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_SINT00H')

    output = _dci.cmdexec("""drop table F00SINT cascade;""")
    _dci.expect_complete_msg(output)

    output = _dci.cmdexec("""cqd HQC_MAX_VALUES_PER_KEY reset;""")
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)
