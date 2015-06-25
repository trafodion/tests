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


def test_eqint(desc="""equals & int"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: equals & int"""

    output = _dci.cmdexec("""drop table F00INT cascade;""")

    output = _dci.cmdexec("""cqd COMP_BOOL_226 'ON';""")
    _dci.expect_complete_msg(output)
    stmt = """cqd TRAF_LOAD_PREP_TMP_LOCATION '/bulkload/';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    output = _dci.cmdexec("""cqd TRAF_LOAD_TAKE_SNAPSHOT 'OFF';""")
    _dci.expect_complete_msg(output)

    stmt = """create table F00INT(
colkey int not null primary key,
colint int)
salt using 8 partitions;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """load into F00INT select
c1+c2*10+c3*100+c4*1000+c5*10000+c6*100000, --colkey
c1+c2*10+c3*100+c4*1000+c5*10000+c6*100000  --colint
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

    stmt = """update statistics for table F00INT on colint;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showstats for table F00INT on colint detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 2000
where interval_number between 3 and 5
--and histogram_id =    and table_uid =
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 6000
where interval_number between 9 and 13
--and histogram_id =    and table_uid =
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 8000
where interval_number between 16 and 17
--and histogram_id =    and table_uid =
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 4000
where interval_number between 23 and 26
--and histogram_id =    and table_uid =
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 10000
where interval_number between 31 and 36
--and histogram_id =    and table_uid =
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 500
where interval_number = 37
--and histogram_id =    and table_uid =
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 14000
where interval_number between 40 and 42
--and histogram_id =    and table_uid =
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 10
where interval_number = 44
--and histogram_id =    and table_uid =
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 1
where interval_number = 22
--and histogram_id =    and table_uid =
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 100
where interval_number = 2
--and histogram_id =    and table_uid =
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 18000
where interval_number between 46 and 48
--and histogram_id =    and table_uid =
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 200
where interval_number between 30 and 31
--and histogram_id =    and table_uid =
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """showstats for table F00INT on colint detail;"""
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
    ## EQUAL PREDICATE ON INT COLUMN
    ## ==================================
    # showstats for table F00INT on colint detail;

    #setup.setupHQClog()
    setup.resetHQC()
    output = _dci.cmdexec("""cqd HQC_MAX_VALUES_PER_KEY '10';""")
    _dci.expect_complete_msg(output)

    # negative constant, not parameterized
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select * from F00INT where colint = -99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = - #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '39393939390A'
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select * from F00INT where colint = -3737;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = - #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '333733370A'
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select * from F00INT where colint = -99999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = - #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '39393939390A'
    setup.verifyHQCEntryExists()

    # constant exceeds upper boundary of last interval
    # expect = Not HQC Cacheable but added to SQC
    stmt = defs.prepXX + """select * from F00INT where colint = 1001000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '313030313030300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    setup.verifyHQCnumEntries('3')

    # cqd query_cache '0';"""
    # cqd query_cache reset;"""
    setup.resetHQC()

    # add plan 1, 0 hits
    # interval 47 [958331 - 979165) rowcount/uec = 20834/18000
    # intervals 46 - 48 merged/collapsed
    # interval extension boundaries [937497 - 999999)
    # expect = HQC::AddEntry(): passed
    # add key entry to cache, plan 1, 0 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 979160;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '979160')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '3937393136300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add plan 2, 0 hits
    # interval 22 [437492 - 458325) rowcount/uec = 20833/1
    # expect = HQC::AddEntry(): passed
    # hqc key exists, plan 2, 0 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 458325;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '458325')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '3435383332350A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add plan 3, 1 hits
    # interval 26 [520824 - 541657) rowcount/uec = 20833/4000
    # intervals 23 - 26 merged/collapsed
    # interval extension boundaries [458325 - 541657)
    # expect = HQC::AddEntry(): passed
    # hqc key exists, plan 3, 0 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 541657;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '541657')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '3534313635370A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 3, 1 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 458326;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '458326')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '3534313635370A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Not HQC Cacheable but added to SQC
    #stmt = defs.prepXX + """select * from F00INT where colint = 1000000;"""

    # add plan 4, 2 hits
    # interval 44 [895829 - 916663) rowcount/uec = 20834/10
    # expect = HQC::AddEntry(): passed
    # hqc key exists, plan 4, 0 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 916663;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '916663')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '3931363636330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 4, 1 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 895830;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '895830')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '3931363636330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 4, 2 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 916662;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '916662')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '3931363636330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add plan 5, 2 hits
    # interval 30 [604156 - 624989) rowcount/uec = 20833/200
    # intervals 30 -31 merged/collapsed
    # interval extension boundaries [604156 - 645822)
    # expect = HQC::AddEntry(): passed
    # hqc key exists, plan 5, 0 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 604157;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '604157')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '3630343135370A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 5, 1 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 604158;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '604158')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '3630343135370A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 5, 2 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 604159;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '604159')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '3630343135370A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add plan 6, 1 hits
    # interval 37 [749991 - 770825) rowcount/uec = 20834/500
    # expect = HQC::AddEntry(): passed
    # hqc key exists, plan 6, 0 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 770000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '770000')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '3737303030300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 6, 1 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 749992;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '749992')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '3737303030300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add plan 7, 2 hits
    # interval 34 [687489 - 708323) rowcount/uec = 20834/10000
    # intervals 32 - 36 merged/collapsed
    # interval extension boundaries [645822 - 749991)
    # expect = HQC::AddEntry(): passed
    # hqc key exists, plan 7, 0 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 700000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '700000')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '3730303030300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 7, 1 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 645823;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '645823')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '3730303030300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 7, 2 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 749991;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '749991')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '3730303030300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add plan 8, 1 hits
    # interval 3 [41665 - 62498) rowcount/uec = 20833/2000
    # intervals 3 - 5 merged/collapsed
    # interval extension boundaries [41665 - 104164)
    # expect = HQC::AddEntry(): passed
    # hqc key exists, plan 8, 0 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 41666;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '41666')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '34313636360A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 8, 1 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 104164;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '104164')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '34313636360A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # HQC cacheable but NOT parameterized
    # interval 0
    # expect = HQC::AddEntry(): passed
    # different hqc key
    #stmt = defs.prepXX + """select * from F00INT where colint = -1;"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_prepared_msg(output)
    #output = _dci.cmdexec("""execute XX;""")
    #_dci.expect_selected_msg(output, '0')
    #defs.hkey = """SELECT * FROM F00INT WHERE COLINT = - #NP# ;"""
    #defs.num_hits = 0
    #defs.num_pliterals = 0
    #defs.num_npliterals = 0
    #defs.pliterals = '310A'
    #setup.verifyHQCEntryExists()

    # HQC cacheable but NOT parameterized
    # interval 0
    # expect = HQC::AddEntry(): passed
    # different hqc key
    # stmt = defs.prepXX + """select * from F00INT where colint = -100;"""

    # add plan 9, 0 hits
    # interval 2 [20832 - 41665) rowcount/uec = 20833/100
    # expect = HQC::AddEntry(): passed
    # hqc key exists, plan 9, 0 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 41665;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '41665')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '34313636350A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add plan 10, 0 hits
    # interval 16 [312494 - 333327) rowcount/uec = 20833/8000
    # intervals 16 - 17 merged/collapsed
    # interval extension boundaries [312494 - 354160)
    # expect = HQC::AddEntry(): passed
    # hqc key exists, plan 10, 0 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 312495;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '312495')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '3331323439350A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits for plan 9 to 1 hits
    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 9, 1 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 20833;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '20833')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '34313636350A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits for plan 10 to 1 hits
    # expect = HQC::AddEntry(): passed
    # hqc key exists, plan 10, 1 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 354160;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '354160')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '3331323439350A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits for plan 1 to 3 hits
    # expect = Found in HQC, HQC backpatch OK
    # entry exists, plan 1, 1 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 937498;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '937498')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '3937393136300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    # expect = Found in HQC, HQC backpatch OK
    # entry exists, plan 1, 2 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 999999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '999999')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '3937393136300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    # expect = Found in HQC, HQC backpatch OK
    # entry exists, plan 1, 3 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 999998;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '999998')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 3
    defs.num_pliterals = 1
    defs.pliterals = '3937393136300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Not HQC Cacheable but added to SQC
    #stmt = defs.prepXX + """select * from F00INT where colint = 1001000;"""

    # increase hits for plan 8 to 5 hits
    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 8, 2 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 41667;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '41667')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '34313636360A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 8, 3 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 41668;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '41668')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 3
    defs.num_pliterals = 1
    defs.pliterals = '34313636360A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 8, 4 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 41669;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '41669')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 4
    defs.num_pliterals = 1
    defs.pliterals = '34313636360A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 8, 5 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 41670;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '41670')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 5
    defs.num_pliterals = 1
    defs.pliterals = '34313636360A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # status:
    # plan 1 (979160): 3 hits
    # plan 2 (458325): 0 hits
    # plan 3 (541657): 1 hits
    # plan 4 (916663): 2 hits
    # plan 5 (604157): 2 hits
    # plan 6 (770000): 1 hits
    # plan 7 (700000): 2 hits
    # plan 8 (41666) : 5 hits
    # plan 9 (41665) : 1 hits
    # plan 10(312495): 1 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_INT00A')

    # replace plan 2
    # interval 21 [416659 - 437492) rowcount/uec = 20833/20833
    # intervals 18 - 21 merged/collapsed
    # interval extension boundaries [354160 - 437492)
    # expect = HQC performed an interval extension
    # expect = HQC cache entry replaced. Entry has <0> hits
    # expect = HQC::AddEntry(): passed
    # hqc key exists, plan 2, 0 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 437492;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '437492')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '3433373439320A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits for plan 2 to 3 hits
    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 2, 1 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 354161;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '354161')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '3433373439320A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 2, 2 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 354162;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '354162')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '3433373439320A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 2, 3 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 354163;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '354163')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 3
    defs.num_pliterals = 1
    defs.pliterals = '3433373439320A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits for plan 3 to 3 hits
    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 3, 2 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 458326;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '458326')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '3534313635370A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 3, 3 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 458326;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '458326')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 3
    defs.num_pliterals = 1
    defs.pliterals = '3534313635370A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits for plan 5 to 4 hits
    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 5, 3 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 604159;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '604159')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 3
    defs.num_pliterals = 1
    defs.pliterals = '3630343135370A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 5, 4 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 604159;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '604159')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 4
    defs.num_pliterals = 1
    defs.pliterals = '3630343135370A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits for plan 9 to 2 hits
    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 9, 2 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 41665;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '41665')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '34313636350A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits for plan 10 to 2 hits
    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 10, 2 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 354160;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '354160')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '3331323439350A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # status:
    # plan 1 (979160): 3 hits
    # plan2, replaced (437492): 3 hits
    # plan 3 (541657): 3 hits
    # plan 4 (916663): 2 hits
    # plan 5 (604157): 4 hits
    # plan 6 (770000): 1 hits
    # plan 7 (700000): 2 hits
    # plan 8 (41666) : 5 hits
    # plan 9 (41665) : 2 hits
    # plan 10(312495): 2 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_INT00B')

    # replace plan 6
    # interval 9 [166663 - 187496) rowcount/uec = 20833/6000
    # intervals 9 - 13 merged/collapsed
    # interval extension boundaries [166663 - 270828)
    # expect = HQC performed an interval extension
    # expect = HQC cache entry replaced. Entry has <1> hits
    # expect = HQC::AddEntry(): passed
    # hqc key exists, plan 6, 0 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 166664;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '166664')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '3136363636340A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 6, 1 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 270828;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '270828')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '3136363636340A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 6, 2 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 270828;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '270828')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '3136363636340A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # status:
    # plan 1 (979160): 3 hits
    # plan2, replaced (437492): 3 hits
    # plan 3 (541657): 3 hits
    # plan 4 (916663): 2 hits
    # plan 5 (604157): 4 hits
    # plan 6,replaced (166664): 2 hits
    # plan 7 (700000): 2 hits
    # plan 8 (41666) : 5 hits
    # plan 9 (41665) : 2 hits
    # plan 10(312495): 2 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_INT00C')

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 4, 3 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 9.16663E5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '916663')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 3
    defs.num_pliterals = 1
    defs.pliterals = '3931363636330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 4, 4 hits
    stmt = defs.prepXX + """select * from F00INT where colint = 8958.31E2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '895831')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 4
    defs.num_pliterals = 1
    defs.pliterals = '3931363636330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # status:
    # plan 1 (979160): 3 hits
    # plan2, replaced (437492): 3 hits
    # plan 3 (541657): 3 hits
    # plan 4 (916663): 4 hits
    # plan 5 (604157): 4 hits
    # plan 6,replaced (166664): 2 hits
    # plan 7 (700000): 2 hits
    # plan 8 (41666) : 5 hits
    # plan 9 (41665) : 2 hits
    # plan 10(312495): 2 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_INT00D')

    stmt = defs.prepXX + """select * from F00INT where colint = 8958.30E2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '895829')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00INT WHERE COLINT = #NP# ;"""
    defs.num_hits = 5
    defs.num_pliterals = 1
    defs.pliterals = '3931363636330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # status:
    # plan 1 (979160): 3 hits
    # plan2, replaced (437492): 3 hits
    # plan 3 (541657): 3 hits
    # plan 4 (916663): 4 hits
    # plan 5 (604157): 4 hits
    # plan 6, replaced (166664): 2 hits
    # plan 7, replaced (8958.30E2): 0 hits
    # plan 8 (41666) : 5 hits
    # plan 9 (41665) : 2 hits
    # plan 10(312495): 2 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_INT00E')

    output = _dci.cmdexec("""drop table F00INT cascade;""")
    _dci.expect_complete_msg(output)

    output = _dci.cmdexec("""cqd HQC_MAX_VALUES_PER_KEY reset;""")
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)
