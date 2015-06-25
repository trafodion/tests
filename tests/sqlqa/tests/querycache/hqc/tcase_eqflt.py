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


def test_eqflt(desc="""equals & float"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: equals & float"""

    output = _dci.cmdexec("""drop table F00FLT cascade;""")

    output = _dci.cmdexec("""cqd COMP_BOOL_226 'ON';""")
    _dci.expect_complete_msg(output)
    stmt = """cqd TRAF_LOAD_PREP_TMP_LOCATION '/bulkload/';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    output = _dci.cmdexec("""cqd TRAF_LOAD_TAKE_SNAPSHOT 'OFF';""")
    _dci.expect_complete_msg(output)

    stmt = """create table F00FLT(
colkey int not null primary key,
colflt float(5))
salt using 8 partitions;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """load into F00FLT select
c1+c2*10+c3*100+c4*1000+c5*10000+c6*100000, --colkey
cast(-1000.33333+c1+c2*10+c3*100+c4*1000+c5*10000+c6*100000 as float) --colflt
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

    stmt = """update statistics for table F00FLT on colflt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showstats for table F00FLT on colflt detail;"""
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

    stmt = """showstats for table F00FLT on colflt detail;"""
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
    ## EQUAL PREDICATE ON FLOAT COLUMN
    ## ==================================
    # showstats for table F00FLT on coldate detail;

    #setup.setupHQClog()
    setup.resetHQC()
    output = _dci.cmdexec("""cqd HQC_MAX_VALUES_PER_KEY '1';""")
    _dci.expect_complete_msg(output)

    # exceeds last interval upper boundary
    # expect = Not HQC Cacheable but added to SQC
    stmt = defs.prepXX + """select * from F00FLT
where colflt = 1002000.66660;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00FLT WHERE COLFLT = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '313030323030302E36363636300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # negative constants are not parameterized
    # HQC cacheable but not parameterized
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select * from F00FLT where colflt = -999.888;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00FLT WHERE COLFLT = - #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '3939392E3838380A'
    setup.verifyHQCEntryExists()

    # negative constants are not parameterized
    # HQC cacheable but not parameterized
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select * from F00FLT where colflt = -1100.333;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00FLT WHERE COLFLT = - #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '313130302E3333330A'
    setup.verifyHQCEntryExists()

    # cqd query_cache '0';
    # cqd query_cache reset;
    setup.resetHQC()

    # add plan 1
    # interval 22 [4.36491666670000000E+005 - 4.57324666670000000E+005)
    #    rowcount/uec = 20833/1
    # expect = HQC::AddEntry(): passed
    # add entry to cache, plan 1, 0 hits
    stmt = defs.prepXX + """select * from F00FLT where colflt = 457324.000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00FLT WHERE COLFLT = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '3435373332342E3030300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # add entry to cache, plan 1, 1 hits
    stmt = defs.prepXX + """select * from F00FLT where colflt = 436492.12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00FLT WHERE COLFLT = #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '3435373332342E3030300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    setup.verifyHQCnumEntries('1')

    # replace plan 1
    # interval 27 [5.40656666670000000E+005 - 5.61489666670000000E+005)
    #     rowcount/uec = 20833/20833
    # intervals 27 - 29 merged/collapsed
    # interval extension boundaries [5.40656666670000000E+005 -
    #     6.03155666670000000E+005)
    # expect = HQC performed interval extension
    # expect = HQC cache entry replaced. Entry has <1> hits
    # expect = HQC::AddEntry(): passed
    # hqc key exists, plan 1, 0 hits
    stmt = defs.prepXX + """select * from F00FLT where colflt = 561489.00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00FLT WHERE COLFLT = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '3536313438392E30300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    setup.verifyHQCnumEntries('1')

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 1, 1 hits
    stmt = defs.prepXX + """select * from F00FLT where colflt = 540657.1111;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00FLT WHERE COLFLT = #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '3536313438392E30300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    setup.verifyHQCnumEntries('1')

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 1, 2 hits
    stmt = defs.prepXX + """select * from F00FLT where colflt = 603155.0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00FLT WHERE COLFLT = #NP# ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '3536313438392E30300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    setup.verifyHQCnumEntries('1')

    # replace plan 1
    # interval 31 [6.23988666670000000E+005 - 6.44821666670000000E+005)
    #     rowcount/uec = 20833/200
    # intervals 30 - 31 merged/collapsed
    # interval extension boundaries [6.03155666670000000E+005 -
    #     6.44821666670000000E+005)
    # expect = HQC performed interval extension
    # expect = HQC cache entry replaced. Entry has <2> hits
    # expect = HQC::AddEntry(): passed
    # hqc key exists, plan 1, 0 hits
    stmt = defs.prepXX + """select * from F00FLT where colflt = 623990.123;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00FLT WHERE COLFLT = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '3632333939302E3132330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    setup.verifyHQCnumEntries('1')

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 1, 1 hits
    stmt = defs.prepXX + """select * from F00FLT where colflt = 644820.000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00FLT WHERE COLFLT = #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '3632333939302E3132330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    setup.verifyHQCnumEntries('1')

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 1, 2 hits
    stmt = defs.prepXX + """select * from F00FLT where colflt = 603156.000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00FLT WHERE COLFLT = #NP# ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '3632333939302E3132330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    setup.verifyHQCnumEntries('1')

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 1, 3 hits
    stmt = defs.prepXX + """select * from F00FLT where colflt = 623991.000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00FLT WHERE COLFLT = #NP# ;"""
    defs.num_hits = 3
    defs.num_pliterals = 1
    defs.pliterals = '3632333939302E3132330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    setup.verifyHQCnumEntries('1')

    # replace plan 1
    # interval 44 [8.94828666670000000E+005 - 9.15662666670000000E+005)
    #     rowcount/uec = 20834/10
    # expect = HQC cache entry replaced. Entry has <3> hits
    # expect = HQC::AddEntry(): passed
    # hqc key exists, plan 1, 0 hits
    stmt = defs.prepXX + """select * from F00FLT where colflt = 915662.123;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00FLT WHERE COLFLT = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '3931353636322E3132330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    setup.verifyHQCnumEntries('1')

    output = _dci.cmdexec("""drop table F00FLT cascade;""")
    _dci.expect_complete_msg(output)

    output = _dci.cmdexec("""cqd HQC_MAX_VALUES_PER_KEY reset;""")
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)
