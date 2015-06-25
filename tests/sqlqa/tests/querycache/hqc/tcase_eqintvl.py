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


def test_eqintvl(desc="""equals & interval"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: equals & interval"""

    output = _dci.cmdexec("""drop table F00INTVL cascade;""")

    output = _dci.cmdexec("""cqd COMP_BOOL_226 'ON';""")
    _dci.expect_complete_msg(output)
    stmt = """cqd TRAF_LOAD_PREP_TMP_LOCATION '/bulkload/';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    output = _dci.cmdexec("""cqd TRAF_LOAD_TAKE_SNAPSHOT 'OFF';""")
    _dci.expect_complete_msg(output)

    stmt = """create table F00INTVL(
colkey int not null primary key,
colintvl interval day(6));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """load into F00INTVL select
c1+c2*10+c3*100+c4*1000+c5*10000+c6*100000, --colkey
cast(cast(mod(c1+c2*10+c3*100+c4*1000+c5*10000+c6*100000,999999)
as integer) as interval day(6)) --colintvl
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

    stmt = """update statistics for table F00INTVL on colintvl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showstats for table F00INTVL on colintvl detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 1
where interval_number between 3 and 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 100
where interval_number between 9 and 13
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 1000
where interval_number between 17 and 21
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 5000
where interval_number between 25 and 27
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 10000
where interval_number between 31 and 34
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 14000
where interval_number between 40 and 44
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 18000
where interval_number between 46 and 50
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """showstats for table F00INTVL on colintvl detail;"""
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
    ## EQUAL PREDICATE ON INTERVAL COLUMN
    ## ==================================
    # showstats for table F00INTVL on colintvl detail;

    #setup.setupHQClog()
    setup.resetHQC()
    output = _dci.cmdexec("""cqd HQC_MAX_VALUES_PER_KEY '3';""")
    _dci.expect_complete_msg(output)

    # add plan 1
    # interval 1 ['1' day - '19998' day), RC/UEC = 20000/20000
    # plan 1, hit 0
    stmt = defs.prepXX + ("""select * from F00INTVL""" +
                          """ where colintvl = interval '19998' day(6);""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output)
    defs.hkey = ("""SELECT * FROM F00INTVL""" +
                 """ WHERE COLINTVL = INTERVAL #NP# DAY ( #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '273139393938270A360A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # plan 1, hit 1
    stmt = defs.prepXX + ("""select * from F00INTVL""" +
                          """ where colintvl = interval '39998' day(6);""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output)
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '273139393938270A360A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add plan 2
    # interval 3 ['39999' day - '59998' day), RC/UEC = 20000/1
    # merge interval 3 & 4, ['39999' day - '79998' day)
    # plan 2, hit 0
    stmt = defs.prepXX + ("""select * from F00INTVL""" +
                          """ where colintvl = interval '39999' day(6);""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output)
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '273139393939270A360A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # plan 2, hit 1
    stmt = defs.prepXX + ("""select * from F00INTVL""" +
                          """ where colintvl = interval '79998' day(6);""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output)
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '273139393938270A360A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add plan 3
    # plan 3, hit 0 ['159999' day - '179998' day), RC/UEC = 20000/100
    # merge interval 9 - 13, ['159999' day - '259998' day)
    # plan 3, hit 0
    stmt = defs.prepXX + ("""select * from F00INTVL""" +
                          """ where colintvl = interval '159999' day(6);""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output)
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '27313539393939270A360A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # plan 3, hit 1
    stmt = defs.prepXX + ("""select * from F00INTVL""" +
                          """ where colintvl = interval '179998' day(6);""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output)
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '27313539393939270A360A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_INTVL00A')

    # replace plan 1
    # interval 21 [ '319998' day - '419998' day), RC/UEC = 20000/1000
    # merge interval 17 - 21
    stmt = defs.prepXX + ("""select * from F00INTVL""" +
                          """ where colintvl = interval '419990' day(6);""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output)
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '27343139393930270A360A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_INTVL00B')

    output = _dci.cmdexec("""drop table F00INTVL cascade;""")
    _dci.expect_complete_msg(output)

    output = _dci.cmdexec("""cqd HQC_MAX_VALUES_PER_KEY reset;""")
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)
