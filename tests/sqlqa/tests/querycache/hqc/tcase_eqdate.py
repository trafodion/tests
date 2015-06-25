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


def test_eqdate(desc="""equals & date"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: equals & date"""

    output = _dci.cmdexec("""drop table F00DATE cascade;""")

    output = _dci.cmdexec("""cqd COMP_BOOL_226 'ON';""")
    _dci.expect_complete_msg(output)
    stmt = """cqd TRAF_LOAD_PREP_TMP_LOCATION '/bulkload/';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    output = _dci.cmdexec("""cqd TRAF_LOAD_TAKE_SNAPSHOT 'OFF';""")
    _dci.expect_complete_msg(output)

    stmt = """create table F00DATE(
colkey int not null primary key,
coldate date)
salt using 8 partitions;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """load into F00DATE select
c1+c2*10+c3*100+c4*1000+c5*10000+c6*100000, --colkey
cast(converttimestamp(210614299200000000 +
(8640000000 * (c1+c2*10+c3*100+c4*1000+c5*10000+c6*100000))) as date) --coldate
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

    output = _dci.cmdexec("""update statistics for table F00DATE
on every column;""")
    _dci.expect_complete_msg(output)

    output = _dci.cmdexec("""showstats for table F00DATE
on coldate detail;""")
    _dci.expect_complete_msg(output)

    # update sb_histogram_intervals
    # set (interval_rowcount, interval_uec) = (30000,500)
    # and histogram_id =    and table_uid =
    # where interval_number = 3;
    # update sb_histogram_intervals
    # set (interval_rowcount, interval_uec) = (40000,500)
    # and histogram_id =    and table_uid =
    # where interval_number = 4;
    # update sb_histogram_intervals
    # set (interval_rowcount, interval_uec) = (10000,500)
    # and histogram_id =    and table_uid =
    # where interval_number = 5;

    stmt = """update sb_histogram_intervals set interval_uec = 1000
--and histogram_id =    and table_uid =
where interval_number between 7 and 17;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 1
--and histogram_id =    and table_uid =
where interval_number = 18;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 1500
--and histogram_id =    and table_uid =
where interval_number between 19 and 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    stmt = """update sb_histogram_intervals set interval_uec = 800
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

    stmt = """update sb_histogram_intervals
set (interval_rowcount, interval_uec) = (3000,50)
--and histogram_id =    and table_uid =
where interval_number in (24,37,46,47);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)

    output = _dci.cmdexec("""showstats for table F00DATE
on coldate detail;""")
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
    ## EQUAL PREDICATE ON DATE COLUMN
    ## ==================================
    # showstats for table F00DATE on coldate detail;

    #setup.setupHQClog()
    setup.resetHQC()
    output = _dci.cmdexec("""cqd HQC_MAX_VALUES_PER_KEY '2';""")
    _dci.expect_complete_msg(output)

    # add plan 1
    # interval 21 ['2071-07-07' - '2076-12-27') rowcount/uec = 20000/800
    # expect = HQC::AddEntry: passed
    # add hqc entry, plan 1, 0 hits
    stmt = defs.prepXX + """select * from F00DATE
where coldate = date'2076-12-20';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2076-12-20')
    defs.hkey = """SELECT * FROM F00DATE WHERE COLDATE = DATE #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '323037362D31322D32300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc entry exists, plan 1, 1 hits
    stmt = defs.prepXX + """select * from F00DATE
where coldate = date'2076-12-27';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2076-12-27')
    defs.hkey = """SELECT * FROM F00DATE WHERE COLDATE = DATE #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '323037362D31322D32300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc entry exists, plan 1, 2 hits
    stmt = defs.prepXX + """select * from F00DATE
where coldate = date'2071-07-08';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2071-07-08')
    defs.hkey = """SELECT * FROM F00DATE WHERE COLDATE = DATE #NP# ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '323037362D31322D32300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add plan 2
    # interval 19 [2060-07-24 - 2066-01-14) rowcount/uec = 20000/1500
    # intervals 19 - 20 merged/collapsed
    # expect = HQC::AddEntry: passed
    # hqc entry exists, plan 2, 0 hits
    stmt = defs.prepXX + """select * from F00DATE
where coldate = date'2060-07-25';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2060-07-25')
    defs.hkey = """SELECT * FROM F00DATE WHERE COLDATE = DATE #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '323036302D30372D32350A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc entry exists, plan 2, 1 hits
    stmt = defs.prepXX + """select * from F00DATE
where coldate = date'2066-01-14';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2066-01-14')
    defs.hkey = """SELECT * FROM F00DATE WHERE COLDATE = DATE #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '323036302D30372D32350A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # status:
    # plan 1 (date'2076-12-20'): 2 hits
    # plan 2 (date'2060-07-25'): 1 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_DATE00A')

    # expect = Found in HQC, HQC backpatch OK
    # hqc entry exists, plan 1, 3 hits
    stmt = defs.prepXX + """select * from F00DATE
where coldate = date'2071-07-09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2071-07-09')
    defs.hkey = """SELECT * FROM F00DATE WHERE COLDATE = DATE #NP# ;"""
    defs.num_hits = 3
    defs.num_pliterals = 1
    defs.pliterals = '323037362D31322D32300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc entry exists, plan 2, 2 hits
    stmt = defs.prepXX + """select * from F00DATE
where coldate = date'2063-06-04';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2063-06-04')
    defs.hkey = """SELECT * FROM F00DATE WHERE COLDATE = DATE #NP# ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '323036302D30372D32350A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc entry exists, plan 1, 4 hits
    stmt = defs.prepXX + """select * from F00DATE
where coldate = date'2074-06-04';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2074-06-04')
    defs.hkey = """SELECT * FROM F00DATE WHERE COLDATE = DATE #NP# ;"""
    defs.num_hits = 4
    defs.num_pliterals = 1
    defs.pliterals = '323037362D31322D32300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc entry exists, plan 2, 3 hits
    stmt = defs.prepXX + """select * from F00DATE
where coldate = date'2065-11-25';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2065-11-25')
    defs.hkey = """SELECT * FROM F00DATE WHERE COLDATE = DATE #NP# ;"""
    defs.num_hits = 3
    defs.num_pliterals = 1
    defs.pliterals = '323036302D30372D32350A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc entry exists, plan 1, 5 hits
    stmt = defs.prepXX + """select * from F00DATE
where coldate = date'2074-06-04';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2074-06-04')
    defs.hkey = """SELECT * FROM F00DATE WHERE COLDATE = DATE #NP# ;"""
    defs.num_hits = 5
    defs.num_pliterals = 1
    defs.pliterals = '323037362D31322D32300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # status:
    # plan 1 (date'2076-12-20'): 5 hits
    # plan 2 (date'2060-07-25'): 3 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_DATE00B')

    # replace plan 2
    # interval 18 ['2055-02-01' - '2060-07-24') rowcount/uec = 20000/1
    # expect = HQC performed an interval extension
    # expect = HQC cache entry replaced. Entry has <3> hits
    # expect = HQC::AddEntry(): passed
    # hqc entry exists, plan 2, 0 hits
    stmt = defs.prepXX + """select * from F00DATE
where coldate = date'2060-07-24';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2060-07-24')
    defs.hkey = """SELECT * FROM F00DATE WHERE COLDATE = DATE #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '323036302D30372D32340A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # verify plan 1 is still intact
    defs.hkey = """SELECT * FROM F00DATE WHERE COLDATE = DATE #NP# ;"""
    defs.num_hits = 5
    defs.num_pliterals = 1
    defs.pliterals = '323037362D31322D32300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc entry exists, plan 2, 1 hits
    stmt = defs.prepXX + """select * from F00DATE
where coldate = date'2055-02-02';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2055-02-02')
    defs.hkey = """SELECT * FROM F00DATE WHERE COLDATE = DATE #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '323036302D30372D32340A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # replace plan 2
    # interval 17 ['2049-08-11' - '2055-02-01') rowcount/uec = 20000/1000
    # intervals 7 - 17 merged/collapsed
    # interval extension boundaries ['1994-11-08' - '2055-02-01')
    # expect = HQC performed an interval extension
    # expect = HQC cache entry replaced. Entry has <1> hits
    # expect = HQC::AddEntry(): passed
    # hqc entry exists, plan 2, 0 hits
    stmt = defs.prepXX + """select * from F00DATE
where coldate = date'2055-02-01';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2055-02-01')
    defs.hkey = """SELECT * FROM F00DATE WHERE COLDATE = DATE #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '323035352D30322D30310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # status:
    # plan 1 (date'2076-12-20'): 5 hits
    # plan 2 (date'2055-02-01'): 0 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_DATE00C')

    # again interval 18
    # expect = nothing in hqc log; SQC hit
    stmt = defs.prepXX + """select * from F00DATE
where coldate = date'2058-12-24';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2058-12-24')

    # expect = nothing in hqc log; SQC hit
    stmt = defs.prepXX + """select * from F00DATE
where coldate = date'2060-02-14';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2060-02-14')

    # expect = nothing in hqc log; SQC hit
    # status:
    # plan 1 (date'2076-12-20'): 5 hits
    # plan 2 (date'2055-02-01'): 0 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_DATE00C')

    # increase plan 2 hits
    # expect = Found in HQC, HQC backpatch OK
    # hqc entry exists, plan 2, 1 hits
    stmt = defs.prepXX + """select * from F00DATE
where coldate = date'2049-08-12';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2049-08-12')
    defs.hkey = """SELECT * FROM F00DATE WHERE COLDATE = DATE #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '323035352D30322D30310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc entry exists, plan 2, 2 hits
    stmt = defs.prepXX + """select * from F00DATE
where coldate = date'2049-08-13';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2049-08-13')
    defs.hkey = """SELECT * FROM F00DATE WHERE COLDATE = DATE #NP# ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '323035352D30322D30310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc entry exists, plan 2, 3 hits
    stmt = defs.prepXX + """select * from F00DATE
where coldate = date'2049-08-14';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2049-08-14')
    defs.hkey = """SELECT * FROM F00DATE WHERE COLDATE = DATE #NP# ;"""
    defs.num_hits = 3
    defs.num_pliterals = 1
    defs.pliterals = '323035352D30322D30310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc entry exists, plan 2, 4 hits
    stmt = defs.prepXX + """select * from F00DATE
where coldate = date'2055-02-01';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2055-02-01')
    defs.hkey = """SELECT * FROM F00DATE WHERE COLDATE = DATE #NP# ;"""
    defs.num_hits = 4
    defs.num_pliterals = 1
    defs.pliterals = '323035352D30322D30310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc entry exists, plan 2, 5 hits
    stmt = defs.prepXX + """select * from F00DATE
where coldate = date'2055-01-31';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2055-01-31')
    defs.hkey = """SELECT * FROM F00DATE WHERE COLDATE = DATE #NP# ;"""
    defs.num_hits = 5
    defs.num_pliterals = 1
    defs.pliterals = '323035352D30322D30310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, HQC backpatch OK
    # hqc entry exists, plan 2, 6 hits
    stmt = defs.prepXX + """select * from F00DATE
where coldate = date'2055-01-30';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2055-01-30')
    defs.hkey = """SELECT * FROM F00DATE WHERE COLDATE = DATE #NP# ;"""
    defs.num_hits = 6
    defs.num_pliterals = 1
    defs.pliterals = '323035352D30322D30310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # status:
    # plan 1 (date'2076-12-20'): 5 hits
    # plan 2 (date'2055-02-01'): 6 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_DATE00D')

    # replace plan 1
    # interval 41 ['2181-01-11' - '2186-07-04') rowcount = 20000/16000
    # intervals 39 - 45 merged/collapsed
    # expect = HQC performed an interval extension
    # expect = HQC cache entry replace. Entry has <5> hits
    # expect = HQC::AddEntry(): passed
    # hqc entry exists, plan 1, 0 hits
    stmt = defs.prepXX + """select * from F00DATE
where coldate = date'2181-01-12';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2181-01-12')
    defs.hkey = """SELECT * FROM F00DATE WHERE COLDATE = DATE #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '323138312D30312D31320A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # verify plan 2 still intact
    defs.hkey = """SELECT * FROM F00DATE WHERE COLDATE = DATE #NP# ;"""
    defs.num_hits = 6
    defs.num_pliterals = 1
    defs.pliterals = '323035352D30322D30310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    setup.verifyHQCnumEntries('2')

    # replace plan 1
    # interval 24 ['2087-12-10' - '2093-06-01') rowcount = 3000/50
    # expect = HQC performed an interval extension
    # expect = HQC cache entry replace. Entry has <0> hits
    # expect = HQC::AddEntry(): passed
    # hqc entry exists, plan 1, 0 hits
    stmt = defs.prepXX + """select * from F00DATE
where coldate = date'2093-06-01';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2093-06-01')
    defs.hkey = """SELECT * FROM F00DATE WHERE COLDATE = DATE #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '323039332D30362D30310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # verify plan 2 still intact
    defs.hkey = """SELECT * FROM F00DATE WHERE COLDATE = DATE #NP# ;"""
    defs.num_hits = 6
    defs.num_pliterals = 1
    defs.pliterals = '323035352D30322D30310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    setup.verifyHQCnumEntries('2')

    # status:
    # plan 1 (date'2093-06-01'): 0 hits
    # plan 2 (date'2055-02-01'): 6 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_DATE00E')

    # interval 46, same selectivity as interval 24
    # expect = interval extension boundaries info in hqc log; SQC hit
    stmt = defs.prepXX + """select * from F00DATE
where coldate = date'2213-11-20';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2213-11-20')

    # status: unchanged
    # plan 1 (date'2093-06-01'): 0 hits
    # plan 2 (date'2055-02-01'): 6 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_DATE00E')

    # replace plan 1
    # interval 23 ['2082-06-19' - '2087-12-10') rowcount = 20000/2000
    # intervals 22 - 23 merged/collapsed
    # interval extension boundaries ['2076-12-27' - '2087-12-10')
    # expect = HQC performed an interval extension
    # expect = HQC cache entry replace. Entry has <0> hits
    # expect = HQC::AddEntry(): passed
    # hqc entry exists, plan 1, 1 hits
    stmt = defs.prepXX + """select * from F00DATE
where coldate = date'2087-12-10';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2087-12-10')
    defs.hkey = """SELECT * FROM F00DATE WHERE COLDATE = DATE #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '323038372D31322D31300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # status:
    # plan 1 (date'2087-12-10'): 0 hits
    # plan 2 (date'2055-02-01'): 6 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_DATE00F')

    # interval 41, extension intervals 38 - 45
    # expect = interval extension boundaries info in hqc log; SQC hit
    stmt = defs.prepXX + """select * from F00DATE
where coldate = date'2181-01-12';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2181-01-12')

    # expect = interval extension boundaries info in hqc log; SQC hit
    stmt = defs.prepXX + """select * from F00DATE
where coldate = date'2181-01-12';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2181-01-12')

    # interval 18
    # expect = nothing in hqc log; SQC hit
    stmt = defs.prepXX + """select * from F00DATE
where coldate = date'2060-07-24';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2060-07-24')

    # expect = nothing in hqc log; SQC hit
    stmt = defs.prepXX + """select * from F00DATE
where coldate = date'2055-02-02';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2055-02-02')

    # again interval 24
    # expect = nothing in hqc log; SQC hit
    stmt = defs.prepXX + """select * from F00DATE
where coldate = date'2093-06-01';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2093-06-01')

    # interval 37, same selectivity as interval 24
    # expect = nothing in hqc log; SQC hit
    stmt = defs.prepXX + """select * from F00DATE
where coldate = date'2164-08-08';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2164-08-08')

    # status: unchanged
    # plan 1 (date'2087-12-10'): 0 hits
    # plan 2 (date'2055-02-01'): 6 hits
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EQUAL_DATE00F')

    output = _dci.cmdexec("""drop table F00DATE cascade;""")
    _dci.expect_complete_msg(output)

    output = _dci.cmdexec("""cqd HQC_MAX_VALUES_PER_KEY reset;""")
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)
