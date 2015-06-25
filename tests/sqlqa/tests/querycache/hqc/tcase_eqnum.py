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
import time

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


def test_eqnum(desc="""equals & numeric"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: equals & numeric"""

    output = _dci.cmdexec("""drop table F00NUM cascade;""")

    output = _dci.cmdexec("""cqd COMP_BOOL_226 'ON';""")
    _dci.expect_complete_msg(output)
    stmt = """cqd TRAF_LOAD_PREP_TMP_LOCATION '/bulkload/';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    output = _dci.cmdexec("""cqd TRAF_LOAD_TAKE_SNAPSHOT 'OFF';""")
    _dci.expect_complete_msg(output)

    stmt = """create table F00NUM(
colkey int not null primary key,
colnum numeric(11,3))
salt using 8 partitions;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """load into F00NUM select
c1+c2*10+c3*100+c4*1000+c5*10000+c6*100000, --colkey
cast((c1+c2*10+c3*100+c4*1000+c5*10000+c6*100000)-99999.211
as numeric(11,3)) --colnum
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

    stmt = """update statistics for table F00NUM on colnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showstats for table F00NUM on colnum detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

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

    stmt = """showstats for table F00NUM on colnum detail;"""
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
    ## EQUAL PREDICATE ON NUMERIC COLUMN
    ## ==================================
    # showstats for table F00NUM on colnum detail;

    #setup.setupHQClog()
    setup.resetHQC()
    output = _dci.cmdexec("""cqd HQC_MAX_VALUES_PER_KEY '4';""")
    _dci.expect_complete_msg(output)

    # exceeds last interval upper boundary
    # expect = Not HQC Cacheable but added to SQC
    stmt = defs.prepXX + """select * from F00NUM where colnum = 999999.999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '3939393939392E3939390A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    stmt = (defs.prepXX + """select * from F00NUM""" +
            """ where colnum = 99.9999999E4;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '39392E3939393939393945340A'
    setup.verifyHQCEntryExists()

    stmt = (defs.prepXX + """select * from F00NUM""" +
            """ where colnum = 999999999.0E-3;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '3939393939393939392E30452D330A'
    setup.verifyHQCEntryExists()

    # cqd query_cache '0';"""
    # cqd query_cache reset;"""
    setup.resetHQC()

    # add plan 1
    # interval 36 [629157.789 - 649991.789) rowcount/uec = 20834/10000
    # intervals 32 - 36 merged/collapsed
    # interval extension boundaries [545822.789 - 649991.789)
    # extension boundaries are encoded values and thus do not
    # necessary reflect showstats output.
    # expect = HQC::AddEntry(): passed
    # add entry to cache, plan 1, 0 hits
    stmt = defs.prepXX + """select * from F00NUM where colnum = 649991.789;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '649991.789')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '3634393939312E3738390A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # hqc key exists, plan 1, 1 hits
    stmt = (defs.prepXX + """select * from F00NUM""" +
            """ where colnum = 54.5823789E4;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '545823.789')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '3634393939312E3738390A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add plan 2
    # interval 16 [212494.789 - 358325.789) rowcount/uec = 20834/8000
    # intervals 16 - 17 merged/collapsed
    # interval extension boundaries [212494.789 - 254160.789)
    # expect = HQC::AddEntry(): passed
    # hqc key exists, plan 2, 0 hits
    stmt = defs.prepXX + """select * from F00NUM where colnum = 212494.790;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '3231323439342E3739300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 2, 1 hits
    stmt = defs.prepXX + """select * from F00NUM where colnum = 212494.8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '3231323439342E3739300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # hqc key exists, plan 2, 2 hits
    stmt = (defs.prepXX + """select * from F00NUM""" +
            """ where colnum = 254.160789E3;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '254160.789')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = #NP# ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '3231323439342E3739300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # status:
    # plan 1 (649991.789): 1 hits
    # plan 2 (212494.790): 2 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_NUM00A')

    # negative constant, not parameterized
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select * from F00NUM where colnum = -37501.211;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = - #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '33373530312E3231310A'
    setup.verifyHQCEntryExists()

    # negative constant, not parameterized
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select * from F00NUM where colnum = -12345.211;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = - #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '31323334352E3231310A'
    setup.verifyHQCEntryExists()

    # negative constant, not parameterized
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + ("""select * from F00NUM""" +
                          """ where colnum = -1000000.789;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = - #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '313030303030302E3738390A'
    setup.verifyHQCEntryExists()

    # status:
    # 3 non-parameterized plans
    # plan 1 (649991.789): 1 hits
    # plan 2 (212494.790): 2 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_NUM00B')

    # add plan 3
    # interval 6 [4164.789 - 24997.789) rowcount/uec = 20833/20833
    # intervals 5 - 8 merged/collapsed
    # interval extension boundaries [-99999.211 - 66663.789)
    # expect = HQC::AddEntry(): passed
    # add entry to cache, plan 3, 0 hits
    stmt = defs.prepXX + """select * from F00NUM where colnum = 20000.123;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '32303030302E3132330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # hqc key exists, plan 3, 1 hits
    stmt = (defs.prepXX + """select * from F00NUM""" +
            """ where colnum = 30000123.0E-3;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '32303030302E3132330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # status:
    # 3 non-parameterized plans
    # plan 1 (649991.789): 1 hits
    # plan 2 (212494.790): 2 hits
    # plan 3 (20000.123): 1 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_NUM00C')

    # negative constant, not parameterized
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select * from F00NUM where colnum = -16668.211;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = - #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '31363636382E3231310A'
    setup.verifyHQCEntryExists()

    # status:
    # 4 non-parameterized plans
    # plan 1 (649991.789): 1 hits
    # plan 2 (212494.790): 2 hits
    # plan 3 (20000.123): 1 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_NUM00D')

    # add plan 4
    # interval 31 [524989.789 - 545822.789) rowcount/uec = 20833/200
    # intervals 30 - 31 merged/collapsed
    # interval extension boundaries [504156.789 - 545822.789)
    # expect = HQC::AddEntry(): passed
    # hqc key exists, plan 4, 0 hits
    stmt = defs.prepXX + """select * from F00NUM where colnum = 545822.789;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '545822.789')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '3534353832322E3738390A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # status:
    # 4 non-parameterized plans
    # plan 1 (649991.789): 1 hits
    # plan 2 (212494.790): 2 hits
    # plan 3 (20000.123): 1 hits
    # plan 4 (545822.789): 0 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_NUM00E')

    # increase plan 1 to 4 hits
    # expect = Found in HQC, HQC backpatch OK
    # entry exists, plan 1, 2 hits
    stmt = defs.prepXX + """select * from F00NUM where colnum = 649991.789;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '649991.789')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = #NP# ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '3634393939312E3738390A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # entry exists, plan 1, 3 hits
    stmt = defs.prepXX + """select * from F00NUM where colnum = 545822.790;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = #NP# ;"""
    defs.num_hits = 3
    defs.num_pliterals = 1
    defs.pliterals = '3634393939312E3738390A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # entry exists, plan 1, 4 hits
    stmt = defs.prepXX + """select * from F00NUM where colnum = 545822.791;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = #NP# ;"""
    defs.num_hits = 4
    defs.num_pliterals = 1
    defs.pliterals = '3634393939312E3738390A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # entry exists, plan 1, 5 hits
    stmt = defs.prepXX + """select * from F00NUM where colnum = 545822.792;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = #NP# ;"""
    defs.num_hits = 5
    defs.num_pliterals = 1
    defs.pliterals = '3634393939312E3738390A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase plan 2 to 6 hits
    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 2, 3 hits
    stmt = defs.prepXX + """select * from F00NUM where colnum = 212494.801;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = #NP# ;"""
    defs.num_hits = 3
    defs.num_pliterals = 1
    defs.pliterals = '3231323439342E3739300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 2, 4 hits
    stmt = defs.prepXX + """select * from F00NUM where colnum = 254160.789;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = #NP# ;"""
    defs.num_hits = 4
    defs.num_pliterals = 1
    defs.pliterals = '3231323439342E3739300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 2, 5 hits
    stmt = defs.prepXX + """select * from F00NUM where colnum = 254160.788;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = #NP# ;"""
    defs.num_hits = 5
    defs.num_pliterals = 1
    defs.pliterals = '3231323439342E3739300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 2, 6 hits
    stmt = defs.prepXX + """select * from F00NUM where colnum = 254160.787;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = #NP# ;"""
    defs.num_hits = 6
    defs.num_pliterals = 1
    defs.pliterals = '3231323439342E3739300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase plan 3 to 4 hits
    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 3, 2 hits
    stmt = defs.prepXX + """select * from F00NUM where colnum = 66663.789;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = #NP# ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '32303030302E3132330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 3, 3 hits
    stmt = defs.prepXX + """select * from F00NUM where colnum = 0.000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = #NP# ;"""
    defs.num_hits = 3
    defs.num_pliterals = 1
    defs.pliterals = '32303030302E3132330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 3, 4 hits
    stmt = defs.prepXX + """select * from F00NUM where colnum = 1.111;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = #NP# ;"""
    defs.num_hits = 4
    defs.num_pliterals = 1
    defs.pliterals = '32303030302E3132330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase plan 4 to 5 hits
    # hqc key exists, plan 4, 1 hits
    stmt = defs.prepXX + """select * from F00NUM where colnum = 504157.001;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '3534353832322E3738390A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 4, 2 hits
    stmt = defs.prepXX + """select * from F00NUM where colnum = 504157.002;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = #NP# ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '3534353832322E3738390A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 4, 3 hits
    stmt = defs.prepXX + """select * from F00NUM where colnum = 545822.788;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = #NP# ;"""
    defs.num_hits = 3
    defs.num_pliterals = 1
    defs.pliterals = '3534353832322E3738390A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 4, 4 hits
    stmt = defs.prepXX + """select * from F00NUM where colnum = 545822.787;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = #NP# ;"""
    defs.num_hits = 4
    defs.num_pliterals = 1
    defs.pliterals = '3534353832322E3738390A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 4, 5 hits
    stmt = defs.prepXX + """select * from F00NUM where colnum = 545822.786;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = #NP# ;"""
    defs.num_hits = 5
    defs.num_pliterals = 1
    defs.pliterals = '3534353832322E3738390A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # status:
    # 4 non-parameterized plans
    # plan 1 (649991.789): 5 hits
    # plan 2 (212494.790): 6 hits
    # plan 3 (20000.123): 3 hits
    # plan 4 (545822.789): 5 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_NUM00F')

    # replace plan 3
    # interval 24 [379158.789 - 399991.789)
    # intervals 23 - 26 merged/collapsed
    # interval extension boundaries [358325.789 - 441657.789)
    # expect = HQC performed an interval extension
    # expect = HQC cache entry replace. Entry has <3> hits
    # expect = HQC::AddEntry(): passed
    # hqc key exists, replace plan 3, 0 hits
    stmt = defs.prepXX + """select * from F00NUM where colnum = 399990.123;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '3339393939302E3132330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, replace plan 3, 1 hits
    stmt = defs.prepXX + """select * from F00NUM where colnum = 441657.789;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '441657.789')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '3339393939302E3132330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, replace plan 3, 2 hits
    stmt = defs.prepXX + """select * from F00NUM where colnum = 358325.999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = #NP# ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '3339393939302E3132330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, replace plan 3, 3 hits
    stmt = defs.prepXX + """select * from F00NUM where colnum = 399990.123;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = #NP# ;"""
    defs.num_hits = 3
    defs.num_pliterals = 1
    defs.pliterals = '3339393939302E3132330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, replace plan 3, 4 hits
    stmt = defs.prepXX + """select * from F00NUM where colnum = 370000.000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = #NP# ;"""
    defs.num_hits = 4
    defs.num_pliterals = 1
    defs.pliterals = '3339393939302E3132330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, replace plan 3, 5 hits
    stmt = defs.prepXX + """select * from F00NUM where colnum = 358325.8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = #NP# ;"""
    defs.num_hits = 5
    defs.num_pliterals = 1
    defs.pliterals = '3339393939302E3132330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, replace plan 3, 6 hits
    stmt = defs.prepXX + """select * from F00NUM where colnum = 441657.788;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = #NP# ;"""
    defs.num_hits = 6
    defs.num_pliterals = 1
    defs.pliterals = '3339393939302E3132330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, replace plan 3, 7 hits
    stmt = defs.prepXX + """select * from F00NUM where colnum = 399990.123;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = #NP# ;"""
    defs.num_hits = 7
    defs.num_pliterals = 1
    defs.pliterals = '3339393939302E3132330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # status:
    # 4 non-parameterized plans
    # plan 1 (649991.789): 5 hits
    # plan 2 (212494.790): 6 hits
    # plan 3 (399990.123): 7 hits
    # plan 4 (545822.789): 5 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_NUM00G')

    # replace plan 1
    # interval 37 [649991.789 - 670825.789)
    # expect = HQC performed an interval extension
    # expect = HQC cache entry replaced. Entry has <4> hits
    # expect = HQC::AddEntry(): passed
    # hqc key exists, replace plan 1, 0 hits
    stmt = defs.prepXX + """select * from F00NUM where colnum = 670825.000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '3637303832352E3030300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # status:
    # 4 non-parameterized plans
    # plan 1, replaced (670825.000): 0 hits
    # plan 2 (212494.790): 6 hits
    # plan 3 (399990.123): 7 hits
    # plan 4 (545822.789): 5 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_NUM00H')

    # replace plan 1
    # interval 22 [337492.789 - 358325.789) rowcount/uec = 20834/1
    # expect = HQC::AddEntry(): passed
    # hqc key exists, plan 1, 0 hits
    stmt = (defs.prepXX + """select * from F00NUM""" +
            """ where colnum = 33.7492790E4;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '33332E3734393237393045340A'
    setup.verifyHQCEntryExists()

    # status:
    # 4 non-parameterized plans
    # plan 1, replaced (33.7492790E4): 0 hits
    # plan 2 (212494.790): 6 hits
    # plan 3 (399990.123): 7 hits
    # plan 4 (545822.789): 5 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_NUM00I')

    # replace plan 1
    # interval 41 [733327.789 - 754161.789), rowcount/uec = 20834/14000
    # intervals 40 - 42 merged/collapsed
    # interval extension boundaries [712493.789 - 774995.789)
    # hqc key exists, plan 4, 0 hits
    stmt = (defs.prepXX + """select * from F00NUM""" +
            """ where colnum = 754.161789E+3;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '754161.789')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = #NP# ;"""
    defs.num_hits = 6
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '3735342E313631373839452B330A'
    setup.verifyHQCEntryExists()

    # status:
    # 4 non-parameterized plans
    # plan 1, replaced (754.161789E+3): 6 hits
    # plan 2 (212494.790): 6 hits
    # plan 3 (399990.123): 7 hits
    # plan 4 (545822.789): 5 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_NUM00J')

    # replace plan 4
    # interval 48 [879165.789 - 899999.789) rowcount/uec = 20834/18000
    # intervals 46 - 48 merged/collapsed
    # interval extension boundaries [837497.789 - 899999.789)
    # hqc key exists, plan 2, 0 hits
    stmt = (defs.prepXX + """select * from F00NUM""" +
            """ where colnum = 89999978.9E-2;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00NUM WHERE COLNUM = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '38393939393937382E39452D320A'
    setup.verifyHQCEntryExists()

    # status:
    # 4 non-parameterized plans
    # plan 1 (754.161789E+3): 6 hits
    # plan 2 (212494.790): 6 hits
    # plan 3 (399990.123): 7 hits
    # plan 4 (89999978.9E-2): 0 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_NUM00K')

    output = _dci.cmdexec("""drop table F00NUM cascade;""")
    _dci.expect_complete_msg(output)

    output = _dci.cmdexec("""cqd HQC_MAX_VALUES_PER_KEY reset;""")
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)
