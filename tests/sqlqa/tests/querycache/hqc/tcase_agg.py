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

# count
# max/maximum
# min
    output = _dci.cmdexec("""drop table F00 cascade;""")
    stmt = """create table F00(
colkey int not null,
colint int, colsint smallint, collint largeint,
colnum numeric(15, 6), coldec decimal(12,5),
colflt float, colreal real, coldp double precision);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into F00 values
(1, -2147483648, -32768, -9223372036854775808,
123456789.987654, 99.99E+4,
6543.21E+2, 12345678.9E-3, 9876.4E+2),
(2, 2147483647, 32767, 9223372036854775807,
1234.1234E-2, 123.456E-2,
12345.6E-4, 99876.45E-3, 100000),
(3, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(4, 555555, 6666, 777777,
3333.33E+5, 555.55,
333.333E+3, 444.444E+5, 100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, '4')
    stmt = """select * from F00 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '1 -2147483648  -32768 -9223372036854775808  123456789.987654 * 999900.00000 * 654321.0 * 12345.679 * 987640.0')
    _dci.expect_any_substr(output, '2  2147483647   32767  9223372036854775807 * 12.341234 * 1.23456 * 1.23456 * 99.87645 * 100000.0')
    _dci.expect_any_substr(output, '3 * NULL * NULL * NULL * NULL * NULL * NULL * NULL * NULL')
    _dci.expect_any_substr(output, '4 * 555555 * 6666 * 777777 * 333333000.000000 * 555.54999 * 333333.0 * 4.44444E7 * 100.0')
    _dci.expect_selected_msg(output, '4')


def test_avgA(desc="""avg() part A"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: avg() part A"""

    ### SQL function: AVG() - HQC cacheable & parameterized

    setup.resetHQC()
    defs.num_pliterals = 0
    defs.num_npliterals = 0

    output = _dci.cmdexec(defs.prepXX + """select AVG(colflt) from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec(defs.prepXX + """select AVG(colint) from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec(defs.prepXX + """select AVG(colflt) from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec(defs.prepXX + """select AVG(colint) from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec(defs.prepXX + """select AVG(colsint) from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec(defs.prepXX + """select AVG(colnum) from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec(defs.prepXX + """select AVG(coldec) from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec(defs.prepXX + """select AVG(colnum) from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec(defs.prepXX + """select AVG(colflt) from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec(defs.prepXX + """select AVG(colreal) from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec(defs.prepXX + """select AVG(coldp) from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec(defs.prepXX + """select AVG(colnum) from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec(defs.prepXX + """select AVG(colflt) from F00;""")
    _dci.expect_prepared_msg(output)

    # entry1, increase hits to 2
    output = _dci.cmdexec(defs.prepXX + """select AVG(colint) from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '185184')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT AVG ( COLINT ) FROM F00 ;"""
    defs.num_hits = 2
    setup.verifyHQCEntryExists()

    # add entry2, increase hits to 1
    output = _dci.cmdexec(defs.prepXX + """select AVG(colsint) from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2221')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT AVG ( COLSINT ) FROM F00 ;"""
    defs.num_hits = 1
    setup.verifyHQCEntryExists()

    # add entry3, hits 0
    output = _dci.cmdexec(defs.prepXX + """select AVG(collint) from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '259258')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT AVG ( COLLINT ) FROM F00 ;"""
    defs.num_hits = 0
    setup.verifyHQCEntryExists()

    # add entry4, increase hits to 3
    output = _dci.cmdexec(defs.prepXX + """select AVG(colnum) from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '152263267.442962')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT AVG ( COLNUM ) FROM F00 ;"""
    defs.num_hits = 3
    setup.verifyHQCEntryExists()

    # add entry5, increase hits to 1
    output = _dci.cmdexec(defs.prepXX + """select AVG(coldec) from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '333485.59485')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT AVG ( COLDEC ) FROM F00 ;"""
    defs.num_hits = 1
    setup.verifyHQCEntryExists()

    # add entry6, increase hits to 4
    output = _dci.cmdexec(defs.prepXX + """select AVG(colflt) from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '329218.41152')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT AVG ( COLFLT ) FROM F00 ;"""
    defs.num_hits = 4
    setup.verifyHQCEntryExists()

    # add entry7, increase hits to 1
    output = _dci.cmdexec(defs.prepXX + """select AVG(colreal) from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '1.481894851838684E7')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT AVG ( COLREAL ) FROM F00 ;"""
    defs.num_hits = 1
    setup.verifyHQCEntryExists()

    # add entry8, increase hits to 1
    output = _dci.cmdexec(defs.prepXX + """select AVG(coldp) from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '362580.0')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT AVG ( COLDP ) FROM F00 ;"""
    defs.num_hits = 1
    setup.verifyHQCEntryExists()

    # clear HQC cache
    setup.resetHQC()

    # add entry1
    output = _dci.cmdexec(defs.prepXX + """select AVG(colint + 10)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '185194')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT AVG ( COLINT + #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '31300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    output = _dci.cmdexec(defs.prepXX + """select AVG(colint + -10)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '185174')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT AVG ( COLINT + - #NP# ) FROM F00 ;"""
    #defs.num_hits = 0
    #defs.num_pliterals = 1
    #defs.pliterals = '31300A'
    #defs.num_npliterals = 0
    #setup.verifyHQCEntryExists()
    setup.verifyHQCEntryNOTExists()

    output = _dci.cmdexec(defs.prepXX + """select AVG(-coldec)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '-333485.59485')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT AVG ( - COLDEC ) FROM F00 ;"""
    setup.verifyHQCEntryNOTExists()

    # add entry2
    output = _dci.cmdexec(defs.prepXX + """select AVG(colint - 10)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '185174')
    _dci.expect_selected_msg(output, '1')

    defs.hkey = """SELECT AVG ( COLINT - #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '31300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry1
    output = _dci.cmdexec(defs.prepXX + """select AVG(colint + 10)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '185194')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT AVG ( COLINT + #NP# ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '31300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry1
    output = _dci.cmdexec(defs.prepXX + """select AVG(colint + 99)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '185283')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT AVG ( COLINT + #NP# ) FROM F00 ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '31300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # new entry3
    output = _dci.cmdexec(defs.prepXX + """select AVG(colint + 999)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '186183')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT AVG ( COLINT + #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '3939390A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry2
    output = _dci.cmdexec(defs.prepXX + """select AVG(colint - 99)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '185085')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT AVG ( COLINT - #NP# ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '31300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry2
    output = _dci.cmdexec(defs.prepXX + """select AVG(colint - 10)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '185174')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT AVG ( COLINT - #NP# ) FROM F00 ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '31300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # new entry4
    output = _dci.cmdexec(defs.prepXX + """select AVG(colint - 999)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '184185')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT AVG ( COLINT - #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '3939390A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry5
    output = _dci.cmdexec(defs.prepXX + """select AVG(colreal * 333.33E+3)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '4.939600109633886E12')
    _dci.expect_selected_msg(output, '1')

    # add entry6
    output = _dci.cmdexec(defs.prepXX + """select AVG(colreal / 4.1234567)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '3593816.934802987')
    _dci.expect_selected_msg(output, '1')

    # increase hits, entry 5
    output = _dci.cmdexec(defs.prepXX + """select AVG(colreal * 333.33E+3)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '4.939600109633886E12')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT AVG ( COLREAL * #NP# ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '3333332E3333452B330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry6
    output = _dci.cmdexec(defs.prepXX + """select AVG(colreal / 4.1234567)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '3593816.934802987')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT AVG ( COLREAL / #NP# ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '342E313233343536370A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry7
    output = _dci.cmdexec(defs.prepXX + """select AVG(mod(colint,4))
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2')
    _dci.expect_selected_msg(output, '1')

    # increase hits, entry6
    output = _dci.cmdexec(defs.prepXX + """select AVG(colreal / 7.8901234)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '1878164.3539804257')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT AVG ( COLREAL / #NP# ) FROM F00 ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '342E313233343536370A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry7
    output = _dci.cmdexec(defs.prepXX + """select AVG(mod(colint,4))
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT AVG ( MOD ( COLINT , #NP# ) ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '340A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry7
    output = _dci.cmdexec(defs.prepXX + """select AVG(mod(colint,6))
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '0')
    _dci.expect_selected_msg(output, '1')

    defs.hkey = """SELECT AVG ( MOD ( COLINT , #NP# ) ) FROM F00 ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '340A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry7
    output = _dci.cmdexec(defs.prepXX + """select AVG(mod(colint,11))
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '0')
    _dci.expect_selected_msg(output, '1')

    defs.hkey = """SELECT AVG ( MOD ( COLINT , #NP# ) ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '31310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    _testmgr.testcase_end(desc)


def test_avgB(desc="""avg() part B"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: avg() part B"""

    ### SQL function: AVG()
    ### AVG() in result-set, constant is positive:
    ###        HQC cacheable & parameterized
    ### AVG() in result-set, constant is negative: Not cacheable

    ### ==============================================================
    ### AVG() result-set, no constants: HQC cacheable
    ###
    setup.resetHQC()

    # new HQC entry
    defs.qry = """SELECT AVG(COLINT) FROM G00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT AVG ( COLINT ) FROM G00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    # expect HQC::AddEntry: passed
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")

    # found in HQC
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.num_hits = 1
    setup.verifyHQCEntryExists()

    ### ==============================================================
    ### AVG() in result-set, constant is positive:
    ###        HQC cacheable & parameterized
    ###
    # new HQC entry
    defs.qry = """SELECT AVG(COLNUM * 1.1) FROM G00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT AVG ( COLNUM * #NP# ) FROM G00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '312E310A'
    defs.num_npliterals = 0
    # expect HQC::AddEntry: passed
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '5256.34015')
    _dci.expect_selected_msg(output, '1')

    # found in HQC
    defs.qry = """SELECT AVG(COLNUM * 2.0) FROM G00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT AVG ( COLNUM * #NP# ) FROM G00 ;"""
    defs.num_hits = 1
    # expect HQC::AddEntry: passed
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '9556.98210')
    _dci.expect_selected_msg(output, '1')

    # new HQC entry; type incompatible
    defs.qry = """SELECT AVG(COLNUM * 0.557) FROM G00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT AVG ( COLNUM * #NP# ) FROM G00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '302E3535370A'
    defs.num_npliterals = 0
    # expect HQC::AddEntry: passed
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2661.6195148')
    _dci.expect_selected_msg(output, '1')

    # new HQC entry, interval constant non-parameterized
    defs.qry = """SELECT AVG(COLINTVL + interval '4' day) FROM G00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT AVG ( COLINTVL + INTERVAL #NP# DAY ) FROM G00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2734270A'
    # expect HQC::AddEntry: passed
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '24')
    _dci.expect_selected_msg(output, '1')

    # new HQC entry, interval constant non-parameterized
    defs.qry = """SELECT AVG(COLINTVL + interval '44' day) FROM G00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT AVG ( COLINTVL + INTERVAL #NP# DAY ) FROM G00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '273434270A'
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '64')
    _dci.expect_selected_msg(output, '1')

    # new HQC entry, interval constant non-parameterized
    defs.qry = """SELECT AVG(COLINTVL + interval '99' day) FROM G00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT AVG ( COLINTVL + INTERVAL #NP# DAY ) FROM G00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '273939270A'
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '119')
    _dci.expect_selected_msg(output, '1')

    setup.verifyHQCnumEntries('6')

    # new HQC entry
    defs.qry = """SELECT AVG(COLLINT * 111) FROM G00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT AVG ( COLLINT * #NP# ) FROM G00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '3131310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '20442')
    _dci.expect_selected_msg(output, '1')

    # found in HQC
    defs.qry = """SELECT AVG(COLLINT * 222) FROM G00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT AVG ( COLLINT * #NP# ) FROM G00 ;"""
    defs.num_hits = 1
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '40885')
    _dci.expect_selected_msg(output, '1')

    # new HQC entry
    defs.qry = """SELECT AVG(COLLINT * 55) FROM G00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT AVG ( COLLINT * #NP# ) FROM G00 ;"""
    defs.num_hits = 2
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '10129')
    _dci.expect_selected_msg(output, '1')

    # new HQC entry
    defs.qry = """SELECT AVG(COLSINT * 111) FROM G00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT AVG ( COLSINT * #NP# ) FROM G00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '3131310A'
    defs.num_npliterals = 0
    # expect HQC::AddEntry: passed
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '-322029')
    _dci.expect_selected_msg(output, '1')

    # new HQC entry
    defs.qry = """SELECT AVG(COLDEC) FROM G00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT AVG ( COLDEC ) FROM G00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    # expect HQC::AddEntry: passed
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '-164')
    _dci.expect_selected_msg(output, '1')

    # new HQC entry
    defs.qry = """SELECT AVG(COLFLT) FROM G00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT AVG ( COLFLT ) FROM G00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    # expect HQC::AddEntry: passed
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '74.31666666666666')
    _dci.expect_selected_msg(output, '1')

    setup.verifyHQCnumEntries('10')
    setup.dumpHQCEntries()

    ### ==============================================================
    ### AVG() in result-set, constant is negative: Not cacheable
    setup.resetHQC()

    defs.qry = """SELECT AVG(COLNUM * -1.1) FROM G00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '-5256.34015')
    _dci.expect_selected_msg(output, '1')

    defs.qry = """SELECT AVG(COLINT * -0.557) FROM G00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '80.393')
    _dci.expect_selected_msg(output, '1')

    defs.qry = """SELECT AVG(COLINT * -22) FROM G00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '3175')
    _dci.expect_selected_msg(output, '1')

    setup.verifyHQCempty()

    _testmgr.testcase_end(desc)


def test_stddev(desc="""stddev()"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: stddev()"""

    ### ================================================
    ### STDDEV: HQC cacheable & parameterized
    setup.resetHQC()

    output = _dci.cmdexec(defs.prepXX + """select STDDEV(colint + 495)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2.147483671453765E9')
    _dci.expect_selected_msg(output, '1')

    output = _dci.cmdexec(defs.prepXX + """select STDDEV(colint + 95)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2.147483671453765E9')
    _dci.expect_selected_msg(output, '1')

    output = _dci.cmdexec(defs.prepXX + """select STDDEV(colsint + 495)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '32992.773910863165')
    _dci.expect_selected_msg(output, '1')

    output = _dci.cmdexec(defs.prepXX + """select STDDEV(colint)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2.147483671453765E9')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT STDDEV ( COLINT ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    output = _dci.cmdexec(defs.prepXX + """select STDDEV(colint + 495)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2.147483671453765E9')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT STDDEV ( COLINT + #NP# ) FROM F00 ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '3439350A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    output = _dci.cmdexec(defs.prepXX + """select STDDEV(colsint)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '32992.773910863165')
    _dci.expect_selected_msg(output, '1')

    output = _dci.cmdexec(defs.prepXX + """select STDDEV(colsint)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '32992.773910863165')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT STDDEV ( COLSINT ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    output = _dci.cmdexec(defs.prepXX + """select STDDEV(colsint + 9)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '32992.773910863165')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT STDDEV ( COLSINT + #NP# ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '3439350A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    output = _dci.cmdexec(defs.prepXX + """select STDDEV(colsint + 495)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '32992.773910863165')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT STDDEV ( COLSINT + #NP# ) FROM F00 ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '3439350A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    output = _dci.cmdexec(defs.prepXX + """select STDDEV(colsint * 1.1)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '36292.05130194948')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT STDDEV ( COLSINT * #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '312E310A'
    setup.verifyHQCEntryExists()

    output = _dci.cmdexec(defs.prepXX + """select STDDEV(colnum)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '1.6852323288768575E8')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT STDDEV ( COLNUM ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    output = _dci.cmdexec(defs.prepXX + """select STDDEV(coldec * 1.1)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '634845.0579437191')
    _dci.expect_selected_msg(output, '1')

    output = _dci.cmdexec(defs.prepXX + """select STDDEV(coldec * 1.1)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '634845.0579437191')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT STDDEV ( COLDEC * #NP# ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '312E310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    output = _dci.cmdexec(defs.prepXX + """select STDDEV(colflt)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '327179.2876086962')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT STDDEV ( COLFLT ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    output = _dci.cmdexec(defs.prepXX + """select STDDEV(colflt/1000
+ 54321.54321987) from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '327.17928760791693')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT STDDEV ( COLFLT / #NP# + #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 2
    defs.pliterals = '313030300A35343332312E35343332313938370A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    output = _dci.cmdexec(defs.prepXX + """select STDDEV(colflt/1.111E1 +
5.432154321987E4) from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '29449.080792861907')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT STDDEV ( COLFLT / #NP# + #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 2
    defs.pliterals = '312E31313145310A352E34333231353433323139383745340A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    output = _dci.cmdexec(defs.prepXX + """select STDDEV(colreal/0.01)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2.5656394312275834E9')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT STDDEV ( COLREAL / #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '302E30310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    output = _dci.cmdexec(defs.prepXX + """select
STDDEV(colreal * 1.23456789012) from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '3.167456059419314E7')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT STDDEV ( COLREAL * #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '312E32333435363738393031320A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    output = _dci.cmdexec(defs.prepXX + """select
STDDEV(colreal * 1.23456789111E+2) from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '3.167456061959297E9')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT STDDEV ( COLREAL * #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '312E3233343536373839313131452B320A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    output = _dci.cmdexec(defs.prepXX + """select
STDDEV(coldec * 8.9) from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '5136473.650635545')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT STDDEV ( COLDEC * #NP# ) FROM F00 ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '312E310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    output = _dci.cmdexec(defs.prepXX + """select
STDDEV(coldec * 1.1) from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '634845.0579437191')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT STDDEV ( COLDEC * #NP# ) FROM F00 ;"""
    defs.num_hits = 3
    defs.num_pliterals = 1
    defs.pliterals = '312E310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    _testmgr.testcase_end(desc)


def test_sum(desc="""sum()"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: sum()"""

    ### ================================================
    ### SUM: HQC cacheable & parameterized
    setup.resetHQC()

    stmt = defs.prepXX + """select SUM(-colint) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = defs.prepXX + """select SUM(coldec + -123.123) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    stmt = defs.prepXX + """select SUM(colreal * -123.123) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)

    setup.verifyHQCempty()

    stmt = defs.prepXX + """select SUM(colint) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '555554')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT SUM ( COLINT ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select SUM(coldec) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '1000456.78455')
    _dci.expect_selected_msg(output, '1')
    stmt = defs.prepXX + """select SUM(colflt) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '987655.23456')
    _dci.expect_selected_msg(output, '1')

    stmt = defs.prepXX + """select SUM(colsint) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '6665')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT SUM ( COLSINT ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select SUM(collint) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '777776')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT SUM ( COLLINT ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select SUM(colnum) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '456789802.328888')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT SUM ( COLNUM ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select SUM(coldec) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '1000456.78455')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT SUM ( COLDEC ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select SUM(colflt) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '987655.23456')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT SUM ( COLFLT ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select SUM(colreal) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '4.445684555516052E7')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT SUM ( COLREAL ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select SUM(coldp) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '1087740.0')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT SUM ( COLDP ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select SUM(colreal) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '4.445684555516052E7')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT SUM ( COLREAL ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select SUM(coldp) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '1087740.0')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT SUM ( COLDP ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    setup.resetHQC()

    stmt = defs.prepXX + """select SUM(colint * 123.45) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '68583141.30')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT SUM ( COLINT * #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '3132332E34350A'
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select SUM((coldec + 1.23E2)/45) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '22240.57299')
    _dci.expect_selected_msg(output, '1')
    stmt = defs.prepXX + """select SUM(colflt**2) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '5.392468599315241E11')
    _dci.expect_selected_msg(output, '1')

    stmt = defs.prepXX + """select SUM(MOD(colsint,10)) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '5')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT SUM ( MOD ( COLSINT , #NP# ) ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '31300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select SUM(collint/(2**24)) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '0.046359121799468994')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT SUM ( COLLINT / ( #NP# ** #NP# ) ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 2
    defs.pliterals = '320A32340A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select SUM(colnum * 12345E-2) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '5.639070109750122E10')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT SUM ( COLNUM * #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '3132333435452D320A'
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select SUM((coldec + 2.34E1)/19) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '52659.314976315785')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT SUM ( ( COLDEC + #NP# ) / #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '322E333445310A31390A'
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select SUM((coldec + 1.23E2)/45) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '22240.57299')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT SUM ( ( COLDEC + #NP# ) / #NP# ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '312E323345320A34350A'
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select SUM(colflt**3) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '3.171752826335552E17')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT SUM ( COLFLT ** #NP# ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '320A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select SUM(colreal + 123.456789E7) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '3.7481605155551605E9')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT SUM ( COLREAL + #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '3132332E34353637383945370A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select SUM(coldp - 123.456789E7) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '-3.70261593E9')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT SUM ( COLDP - #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '3132332E34353637383945370A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select SUM(colreal + 123.45E7) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '3.7479568455551605E9')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT SUM ( COLREAL + #NP# ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '3132332E34353637383945370A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select SUM(coldp - 123.45E7) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '-3.70241226E9')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT SUM ( COLDP - #NP# ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '3132332E34353637383945370A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    _testmgr.testcase_end(desc)


def test_variance(desc="""variance()"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: variance()"""

    ### ================================================
    ### VARIANCE: HQC cacheable & parameterized
    setup.resetHQC()

    stmt = defs.prepXX + """select VARIANCE(colint) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '4.6116861191605422E18')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT VARIANCE ( COLINT ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select VARIANCE(all colsint) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '1.0885231303333333E9')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT VARIANCE ( ALL COLSINT ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select VARIANCE(distinct coldec) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '3.330811963599703E11')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT VARIANCE ( DISTINCT COLDEC ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select VARIANCE(colint * colnum) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2.344617150830292E34')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT VARIANCE ( COLINT * COLNUM ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select VARIANCE(colint * 1.1) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '5.5801402041842565E18')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT VARIANCE ( COLINT * #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '312E310A'
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select VARIANCE(colnum / 3147E-2) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2.867649563196321E13')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT VARIANCE ( COLNUM / #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '33313437452D320A'
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select VARIANCE(coldec * 123.456E2) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '5.07661839558451E19')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = """SELECT VARIANCE ( COLDEC * #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '3132332E34353645320A'
    setup.verifyHQCEntryExists()

    _testmgr.testcase_end(desc)
