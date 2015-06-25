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


def test_eqreal(desc="""equals & real"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: equals & real"""

    output = _dci.cmdexec("""drop table F00REAL cascade;""")

    output = _dci.cmdexec("""cqd COMP_BOOL_226 'ON';""")
    _dci.expect_complete_msg(output)
    stmt = """cqd TRAF_LOAD_PREP_TMP_LOCATION '/bulkload/';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    output = _dci.cmdexec("""cqd TRAF_LOAD_TAKE_SNAPSHOT 'OFF';""")
    _dci.expect_complete_msg(output)

    stmt = """create table F00REAL(
colkey int not null primary key,
colreal real)
salt using 8 partitions;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """load into F00REAL select
c1+c2*10+c3*100+c4*1000+c5*10000+c6*100000, --colkey
cast((c1+c2*10+c3*100+c4*1000+c5*10000+c6*100000)-99999.211
as real) --colreal
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

    stmt = """update statistics for table F00REAL on colreal;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showstats for table F00REAL on colreal detail;"""
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

    stmt = """showstats for table F00REAL on colreal detail;"""
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
    ## EQUAL PREDICATE ON REALERIC COLUMN
    ## ==================================
    # showstats for table F00REAL on colreal detail;

    #setup.setupHQClog()
    setup.resetHQC()
    output = _dci.cmdexec("""cqd HQC_MAX_VALUES_PER_KEY '4';""")
    _dci.expect_complete_msg(output)

    # negative constant, not parameterized
    stmt = (defs.prepXX + """select * from F00REAL""" +
            """ where colreal = -9.9999211E4;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00REAL WHERE COLREAL = - #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '392E3939393932313145340A'
    setup.verifyHQCEntryExists()

    # add plan 1
    # interval 8 [4.5830789E+004 - 6.6663789E+004) rowcount/uec = 20833/20833
    # intervals 1- 8 merged/collapsed
    # interval extension boundaries [-9.9999210E4 - 6.6663789E+004)
    # add entry to cache, plan 1, 0 hits
    stmt = (defs.prepXX + """select * from F00REAL""" +
            """ where colreal = 6.6663789E4;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '66663.79')
    defs.hkey = """SELECT * FROM F00REAL WHERE COLREAL = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '362E3636363337383945340A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # JULWORK hqc key exists, plan 1, 1 hits

    # add plan 2
    # interval 13 [1.4999579E+005 - 1.7082878E+005) rowcount/uec = 20834/6000
    # intervals 9 - 13 merged/collapsed
    # interval extension boundaries [6.6663789E+004 - 1.7082878E+005)
    # expect = HQC::AddEntry(): passed
    # hqc key exists, plan 2, 0 hits
    stmt = (defs.prepXX + """select * from F00REAL""" +
            """ where colreal = 1.6000E+5;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00REAL WHERE COLREAL = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '312E36303030452B350A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 2, 1 hits
    stmt = (defs.prepXX + """select * from F00REAL""" +
            """ where colreal = 1.2000E+5;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00REAL WHERE COLREAL = #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '312E36303030452B350A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 2, 2 hits
    stmt = (defs.prepXX + """select * from F00REAL""" +
            """ where colreal = 6.667E4;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00REAL WHERE COLREAL = #NP# ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '312E36303030452B350A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc key exists, plan 1, 1 hits
    # interval 8 [4.5830789E+004 - 6.6663789E+004) rowcount/uec = 20833/20833
    # intervals 1- 8 merged/collapsed
    # interval extension boundaries [-9.9999210E4 - 6.6663789E+004)
    # add entry to cache, plan 1, 0 hits
    stmt = (defs.prepXX + """select * from F00REAL""" +
            """ where colreal = 11.113789E+3;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '11113.789')
    defs.hkey = """SELECT * FROM F00REAL WHERE COLREAL = #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '362E3636363337383945340A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add plan 3
    # interval 25 [3.9999178E+005 - 4.2082481E+005) rowcount/uec = 20833/4000
    # intervals 23 - 26 merged/collapsed
    # interval extension boundaries [3.5832578E+005 - 4.4165778E+005)
    # expect = HQC::AddEntry(): passed
    # hqc key exists, plan 3, 0 hits
    stmt = (defs.prepXX + """select * from F00REAL""" +
            """ where colreal = 420824.81;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00REAL WHERE COLREAL = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '3432303832342E38310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # status:
    # 1 non-parameterized plan
    # plan 1 (6.6663789E4): 1 hits
    # plan 2 (1.6000E+5): 2 hits
    # plan 3 (420824.81): 0 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_REAL00A')

    # negative constant, not parameterized
    # expect = HQC::AddEntry(): passed
    stmt = (defs.prepXX + """select * from F00REAL""" +
            """ where colreal = -37501.211;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00REAL WHERE COLREAL = - #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '33373530312E3231310A'
    setup.verifyHQCEntryExists()

    # negative constant, not parameterized
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + ("""select * from F00REAL""" +
                          """ where colreal = -1000000.789;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00REAL WHERE COLREAL = - #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '313030303030302E3738390A'
    setup.verifyHQCEntryExists()

    # status:
    # 3 non-parameterized plan
    # plan 1 (6.6663789E4): 1 hits
    # plan 2 (1.6000E+5): 2 hits
    # plan 3 (420824.81): 0 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_REAL00B')

    # add plan 4
    # interval 22 [3.3749281E+005 - 3.5832578E+005) rowcount/uec = 20833/1
    # expect = HQC::AddEntry(): passed
    # hqc key exists, plan 4, 0 hits
    stmt = (defs.prepXX + """select * from F00REAL""" +
            """ where colreal = 358325.78;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00REAL WHERE COLREAL = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '3335383332352E37380A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # replace plan 3
    # interval 17 [2.3332779E+005 - 2.5416078E+005) rowcount/uec = 20833/8000
    # intervals 16 - 17 merged/collapsed
    # interval extension boundaries [2.1249478E+005 - 2.5416078E+005)
    # expect = HQC::AddEntry(): passed
    # hqc key exists, plan 3, 0 hits
    stmt = (defs.prepXX + """select * from F00REAL""" +
            """ where colreal = 254160.78;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00REAL WHERE COLREAL = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '3235343136302E37380A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # hqc key exists, plan 3, 1 hits
    stmt = (defs.prepXX + """select * from F00REAL""" +
            """ where colreal = 254159.789;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00REAL WHERE COLREAL = #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '3235343136302E37380A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # hqc key exists, plan 3, 2 hits
    stmt = (defs.prepXX + """select * from F00REAL""" +
            """ where colreal = 2.5416078E5;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '254160.78')
    defs.hkey = """SELECT * FROM F00REAL WHERE COLREAL = #NP# ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '3235343136302E37380A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # status:
    # 3 non-parameterized plan
    # plan 1 (6.6663789E4): 1 hits
    # plan 2 (1.6000E+5): 2 hits
    # plan 3 (254160.78): 2 hits
    # plan 4 (358325.78): 0 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_REAL00C')

    # replace plan 4
    # interval 30 [5.0415681E+005 - 5.2498981E+005) rowcount/uec = 20833/200
    # interval 30 - 31 merged/collapsed
    # interval extension boundaries [5.0415681E+005 - 5.4582281E+005)
    # expect = HQC::AddEntry(): passed
    # hqc key exists, plan 4, 0 hits
    stmt = (defs.prepXX + """select * from F00REAL""" +
            """ where colreal = 504.15690E3;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00REAL WHERE COLREAL = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '3530342E313536393045330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # hqc key exists, plan 4, 1 hits
    stmt = (defs.prepXX + """select * from F00REAL""" +
            """ where colreal = 545.82190E3;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00REAL WHERE COLREAL = #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '3530342E313536393045330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # hqc key exists, plan 4, 2 hits
    stmt = (defs.prepXX + """select * from F00REAL""" +
            """ where colreal = 504156.81000;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00REAL WHERE COLREAL = #NP# ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '3530342E313536393045330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # hqc key exists, plan 1, 2 hits
    stmt = (defs.prepXX + """select * from F00REAL""" +
            """ where colreal = 66663.789;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00REAL WHERE COLREAL = #NP# ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '362E3636363337383945340A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # hqc key exists, plan 2, 3 hits
    stmt = (defs.prepXX + """select * from F00REAL""" +
            """ where colreal = 160.828789E3;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '160828.78')
    defs.hkey = """SELECT * FROM F00REAL WHERE COLREAL = #NP# ;"""
    defs.num_hits = 3
    defs.num_pliterals = 1
    defs.pliterals = '312E36303030452B350A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # hqc key exists, plan 2, 4 hits
    stmt = (defs.prepXX + """select * from F00REAL""" +
            """ where colreal = 160828.789;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00REAL WHERE COLREAL = #NP# ;"""
    defs.num_hits = 4
    defs.num_pliterals = 1
    defs.pliterals = '312E36303030452B350A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # hqc key exists, plan 2, 5 hits
    stmt = (defs.prepXX + """select * from F00REAL""" +
            """ where colreal = 160828.78;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F00REAL WHERE COLREAL = #NP# ;"""
    defs.num_hits = 5
    defs.num_pliterals = 1
    defs.pliterals = '312E36303030452B350A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # status:
    # 3 non-parameterized plan
    # plan 1 (6.6663789E4): 2 hits
    # plan 2 (1.6000E+5): 5 hits
    # plan 3 (254160.78): 2 hits
    # plan 4 (504.15690E3): 2 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_REAL00D')

    output = _dci.cmdexec("""drop table F00REAL cascade;""")
    _dci.expect_complete_msg(output)

    output = _dci.cmdexec("""cqd HQC_MAX_VALUES_PER_KEY reset;""")
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)
