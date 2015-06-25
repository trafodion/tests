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

    # for acosine test
    output = _dci.cmdexec("""drop table F00 cascade;""")
    stmt = """create table F00(
colkey int not null, colnum numeric(9,4));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into F00 values ( 1, 0.9397);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    output = _dci.cmdexec("""drop table F01 cascade;""")
    stmt = """create table F01(
colkey int not null, colnum numeric(9,4), cola numeric(12,10),
colb numeric(12,10), colreal real, colc real);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into F01(colkey, colnum, colreal)
values ( 1, 0.9397, 9.397E-1),
( 2, -0.9397, -0.009397E+2),
( 3, 0.6268, 6.268E-1),
( 4, -0.62683, -0.62683E+0),
( 5, 1, 1E+0),
( 6, -1, -1E+0),
( 7, 0.4683219, 4.683219E-1),
( 8, 36.6759311E-2, 36.6759311E-2),
( 9, -234.12328623E-3, -234.12328623E-3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, '9')
    stmt = """update F01 set cola = acos(colnum);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, '9')
    stmt = """update F01 set colb = asin(colnum);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, '9')
    stmt = """select colnum, cola, colb from F01 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.expfile, 'TRIG001')
    stmt = """update F01 set colc = atan(colreal);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, '9')
    stmt = """select colreal, colc from F01 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.expfile, 'TRIG002')


def test_abs(desc="""abs()"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: abs()"""

    ### SQL function: ABS()
    ### ABS() in result-set, constant is positive:
    ###     HQC cacheable & parameterized
    ### ABS() in result-set, constant is negative: Not cacheable
    ### ABS() in where-clause: Not cacheable

    ### ==============================================================
    ### ABS() result-set, no constants: HQC cacheable
    setup.resetHQC()

    defs.qry = """select ABS(colint) from g00;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'ABS001')

    defs.hkey = """SELECT ABS ( COLINT ) FROM G00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    # expect HQC::AddEntry: passed
    setup.verifyHQCEntryExists()

    # prep stmt is skipped by preparser stage, num_hits incremented
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    # prep stmt is skipped by preparser stage, num_hits incremented
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    # prep stmt is skipped by preparser stage, num_hits incremented
    output = _dci.cmdexec(defs.prepXX + defs.qry)

    # expect num_hits = 3
    defs.num_hits = 3
    setup.verifyHQCEntryExists()

    output = _dci.cmdexec("execute XX;")
    _dci.expect_file(output, defs.expfile, 'ABS001')

    ### ==============================================================
    ### ABS in result-set, constant is positive: HQC cacheable & parameterized
    # https://bugs.launchpad.net/trafodion/+bug/1361878
    # expect HQC::AddEntry: passed
    setup.resetHQC()

    defs.qry = """select ABS(25) from g00;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_str_token(output, '25')
    #_dci.expect_file(output, defs.expfile, 'ABS002')

    defs.hkey = """SELECT ABS ( #NP# ) FROM G00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '32350A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # HQC entry found, num_hits incremented
    defs.qry = """select ABS(50) from g00;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_str_token(output, '50')
    #_dci.expect_file(output, defs.expfile, 'ABS003')
    defs.num_hits = 1
    setup.verifyHQCEntryExists()

    # HQC entry found, num_hits incremented
    defs.qry = """select ABS(75) from g00;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_str_token(output, '75')
    #_dci.expect_file(output, defs.expfile, 'ABS004')
    defs.num_hits = 2
    setup.verifyHQCEntryExists()

    # qry captured by preparser stage, hit not counted
    defs.qry = """select ABS(25) from g00;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_str_token(output, '25')
    #_dci.expect_file(output, defs.expfile, 'ABS002')
    setup.verifyHQCEntryExists()

    # new HQC entry; literal type incompatible
    defs.qry = """select ABS(1000) from g00;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_str_token(output, '1000')
    #_dci.expect_file(output, defs.expfile, 'ABS005')

    # verify new HQC Entry added
    defs.hkey = """SELECT ABS ( #NP# ) FROM G00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '313030300A'
    setup.verifyHQCEntryExists()

    # qry captured by preparser stage, hit not counted
    output = _dci.cmdexec(defs.qry)
    _dci.expect_str_token(output, '1000')
    #_dci.expect_file(output, defs.expfile, 'ABS005')
    # verify num_hits has not changed
    setup.verifyHQCEntryExists()

    # different literal but same type, hit counted
    defs.qry = """select ABS(2000) from g00;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_str_token(output, '2000')
    #_dci.expect_file(output, defs.expfile, 'ABS006')
    defs.num_hits = 1
    setup.verifyHQCEntryExists()

    setup.verifyHQCnumEntries('2')

    ### ==============================================================
    ### ABS() in result-set, constant is negative: Not cacheable
    setup.resetHQC()
    qry = """select ABS(-25) from g00;"""
    output = _dci.cmdexec(qry)
    _dci.expect_str_token(output, '25')
    qry = """select ABS(-3000) from g00;"""
    output = _dci.cmdexec(qry)
    _dci.expect_str_token(output, '3000')
    qry = """select ABS(-30 * 100 + 500) from g00;"""
    output = _dci.cmdexec(qry)
    _dci.expect_str_token(output, '2500')
    qry = """select ABS(-100) from g00;"""
    output = _dci.cmdexec(qry)
    _dci.expect_str_token(output, '100')
    setup.verifyHQCempty()

    ### ==============================================================
    ### ABS() in result-set, positive constants in expression:
    ###     HQC cacheable & parameterized
    setup.resetHQC()

    defs.qry = """select ABS(12 + 20) from g00;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_str_token(output, '32')
    #_dci.expect_file(output, defs.expfile, 'ABS007')

    defs.hkey = """SELECT ABS ( #NP# + #NP# ) FROM G00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 2
    defs.pliterals = '31320A32300A'
    defs.num_npliterals = 0
    # HQC entry added
    setup.verifyHQCEntryExists()

    # different literals, same type, hit counted
    defs.qry = """select ABS(24 + 40) from g00;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_str_token(output, '64')
    #_dci.expect_file(output, defs.expfile, 'ABS007')
    defs.num_hits = 1
    setup.verifyHQCEntryExists()

    # qry captured in preparser stage, hit not counted
    defs.qry = """select ABS(12 + 20) from g00;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_str_token(output, '32')
    setup.verifyHQCEntryExists()

    ### ==============================================================
    ### ABS() in result-set, mixed positive/negative constants in expression:
    ###     Not cacheable
    setup.resetHQC()

    # not HQC cacheable
    qry = """select ABS(-12 + 20) from g00;"""
    output = _dci.cmdexec(qry)
    _dci.expect_str_token(output, '8')
    # not HQC cacheable
    qry = """select ABS(12 + -20) from g00;"""
    output = _dci.cmdexec(qry)
    _dci.expect_str_token(output, '8')
    # not HQC cacheable
    qry = """select ABS(-12 + -20) from g00;"""
    output = _dci.cmdexec(qry)
    _dci.expect_str_token(output, '32')
    setup.verifyHQCempty()

    ### ==============================================================
    ### ABS() in where-clause: HQC cacheable, NOT parameterized
    setup.resetHQC()

    # HQC entry added
    defs.qry = """select * from g00 where colint = ABS(colint);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)

    defs.hkey = """SELECT * FROM G00 WHERE COLINT = ABS ( COLINT ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ABS006')

    # HQC entry added
    defs.qry = """select * from g00 where colint = ABS(200);"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'ABS007')
    defs.hkey = """SELECT * FROM G00 WHERE COLINT = ABS ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '3230300A'
    setup.verifyHQCEntryExists()

    # prep stmt skipped by preparser stage, hit counted
    defs.qry = """select * from g00 where colint = ABS(200);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT * FROM G00 WHERE COLINT = ABS ( #NP# ) ;"""
    defs.num_hits = 1
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ABS007')

    # HQC entry added
    defs.qry = """select count(*) from g00 where colint = ABS(-330/3);"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_str_token(output, '1')
    defs.hkey = ("""SELECT COUNT ( * ) FROM G00""" +
                 """ WHERE COLINT = ABS ( - #NP# / #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '3333300A330A'
    setup.verifyHQCEntryExists()

    # HQC entry added, type incompatible
    defs.qry = """select count(*) from g00 where colint = ABS(-4000/20);"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_str_token(output, '1')
    defs.hkey = ("""SELECT COUNT ( * ) FROM G00""" +
                 """ WHERE COLINT = ABS ( - #NP# / #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '343030300A32300A'
    setup.verifyHQCEntryExists()

    # prep stmt, skipped by preparser stage, hit counted
    defs.qry = """select count(*) from g00 where colint = ABS(-330/3);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = ("""SELECT COUNT ( * ) FROM G00""" +
                 """ WHERE COLINT = ABS ( - #NP# / #NP# ) ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '3333300A330A'
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '1')

    _testmgr.testcase_end(desc)


def test_acos(desc="""acos()"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: acos()"""

    ### SQL function: ACOS()
    ### ACOS() in result-set, constant is positive:
    ###         HQC cacheable & parameterized
    ### ACOS() in result-set, constant is negative: Not cacheable
    ### ACOS() in where-clause: HQC cacheable, not parameterized

    ### ==============================================================
    ### ACOS() result-set, no constants: HQC cacheable
    setup.resetHQC()

    defs.qry = """SELECT ACOS(COLNUM) FROM F01 ORDER BY COLKEY;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    defs.hkey = """SELECT ACOS ( COLNUM ) FROM F01 ORDER BY COLKEY ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    # expect HQC::AddEntry: passed
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ACOS001')

    # prep stmt is skipped by preparser stage, num_hits incremented
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    # prep stmt is skipped by preparser stage, num_hits incremented
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    # expect num_hits = 2
    defs.num_hits = 2
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("execute XX;")
    _dci.expect_file(output, defs.expfile, 'ACOS001')

    ### ==============================================================
    ### ACOS in result-set, constant is positive:
    ###     HQC cacheable & parameterized
    setup.resetHQC()

    # new HQC entry
    defs.qry = """SELECT ACOS(0.9397) FROM F00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT ACOS ( #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '302E393339370A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    #_dci.expect_str_token(output, '0.3490442743807244')
    _dci.expect_file(output, defs.expfile, 'ACOS002')

    # HQC entry found, num_hits incremented
    defs.qry = """SELECT ACOS(0.6431) FROM F00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.num_hits = 1
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    #_dci.expect_str_token(output, '0.87225675959934')
    _dci.expect_file(output, defs.expfile, 'ACOS003')

    # new HQC entry
    defs.qry = """SELECT ACOS(0.09397E+1) FROM F00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT ACOS ( #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '302E3039333937452B310A'
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    #_dci.expect_str_token(output, '0.3490442743807244')
    _dci.expect_file(output, defs.expfile, 'ACOS004')

    # HQC entry found, num_hits incremented
    defs.qry = """SELECT ACOS(9.397E-1) FROM F00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.num_hits = 1
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    #_dci.expect_str_token(output, '0.34904427438072405')
    _dci.expect_file(output, defs.expfile, 'ACOS005')

    # new HQC entry; literal type incompatible
    defs.qry = """SELECT ACOS(1.0) FROM F00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT ACOS ( #NP# ) FROM F00 ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '302E393339370A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    #_dci.expect_str_token(output, '0.0')
    _dci.expect_file(output, defs.expfile, 'ACOS006')

    # new HQC entry
    defs.qry = """SELECT ACOS(colnum * 0.1) FROM F01 ORDER BY COLKEY;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT ACOS ( COLNUM * #NP# ) FROM F01 ORDER BY COLKEY ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '302E310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ACOS007')

    # new HQC entry; literal type incompatible
    defs.qry = """SELECT ACOS(colnum * 0.011) FROM F01 ORDER BY COLKEY;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT ACOS ( COLNUM * #NP# ) FROM F01 ORDER BY COLKEY ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '302E3031310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ACOS008')

    # HQC entry found
    defs.qry = """SELECT ACOS(colnum * 0.021) FROM F01 ORDER BY COLKEY;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT ACOS ( COLNUM * #NP# ) FROM F01 ORDER BY COLKEY ;"""
    defs.num_hits = 1
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ACOS009')

    # HQC entry found
    defs.qry = """SELECT ACOS(colnum * 0.1) FROM F01 ORDER BY COLKEY;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT ACOS ( COLNUM * #NP# ) FROM F01 ORDER BY COLKEY ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '302E310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ACOS010')

    # new HQC entry
    defs.qry = """SELECT ACOS(93.97 * 0.01) FROM F00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT ACOS ( #NP# * #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 2
    defs.pliterals = '39332E39370A302E30310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    #_dci.expect_str_token(output, '0.3490442743807244')
    _dci.expect_file(output, defs.expfile, 'ACOS011')

    # new HQC entry
    defs.qry = """SELECT ACOS(6.837 * 0.1) FROM F00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT ACOS ( #NP# * #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 2
    defs.pliterals = '362E3833370A302E310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    #_dci.expect_str_token(output, '0.8179755177225166')
    _dci.expect_file(output, defs.expfile, 'ACOS012')

    setup.verifyHQCnumEntries('6')

    # new HQC entry
    defs.qry = """SELECT ACOS(6.837 / 10) FROM F00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT ACOS ( #NP# / #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 2
    defs.pliterals = '362E3833370A31300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    #_dci.expect_str_token(output, '0.8179755177225166')
    _dci.expect_file(output, defs.expfile, 'ACOS013')

    # new HQC entry
    defs.qry = """SELECT ACOS(COS(0.3491)) FROM F00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT ACOS ( COS ( #NP# ) ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '302E333439310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    #_dci.expect_str_token(output, '0.34909999999999997')
    _dci.expect_file(output, defs.expfile, 'ACOS014')

    setup.verifyHQCnumEntries('8')

    ### ==============================================================
    ### ACOS() in result-set, constant is negative: Not cacheable
    setup.resetHQC()

    qry = """SELECT ACOS(-0.9397) FROM F00;"""
    output = _dci.cmdexec(defs.prepXX + qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    #_dci.expect_str_token(output, '2.792548379209069')
    _dci.expect_file(output, defs.expfile, 'ACOS015')
    qry = """SELECT ACOS(-0.634) FROM F00;"""
    output = _dci.cmdexec(defs.prepXX + qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    #_dci.expect_str_token(output, '2.2575110563881062')
    _dci.expect_file(output, defs.expfile, 'ACOS016')
    qry = """SELECT ACOS(-1) FROM F00;"""
    output = _dci.cmdexec(defs.prepXX + qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    #_dci.expect_str_token(output, '3.141592653589793')
    _dci.expect_file(output, defs.expfile, 'ACOS017')
    qry = """SELECT ACOS(-93.97E-2) FROM F00;"""
    output = _dci.cmdexec(defs.prepXX + qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    #_dci.expect_str_token(output, '2.792548379209069')
    _dci.expect_file(output, defs.expfile, 'ACOS018')
    qry = """SELECT ACOS(-93.97 * 0.01) FROM F00;"""
    output = _dci.cmdexec(defs.prepXX + qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    #_dci.expect_str_token(output, '2.792548379209069')
    _dci.expect_file(output, defs.expfile, 'ACOS019')
    qry = """SELECT ACOS(-93.97 * -0.01) FROM F00;"""
    output = _dci.cmdexec(defs.prepXX + qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    #_dci.expect_str_token(output, '0.3490442743807244')
    _dci.expect_file(output, defs.expfile, 'ACOS020')
    qry = """SELECT ACOS(-93.97 / -100) FROM F00;"""
    output = _dci.cmdexec(defs.prepXX + qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    #_dci.expect_str_token(output, '0.3490442743807244')
    _dci.expect_file(output, defs.expfile, 'ACOS021')
    qry = """SELECT ACOS(-93.97 / 100) FROM F00;"""
    output = _dci.cmdexec(defs.prepXX + qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    #_dci.expect_str_token(output, '2.792548379209069')
    _dci.expect_file(output, defs.expfile, 'ACOS022')

    setup.verifyHQCempty()

    ### ==============================================================
    ### ACOS() in where-clause: HQC cacheable, NOT parameterized
    setup.resetHQC()

    # HQC entry added
    defs.qry = """SELECT * FROM F01 WHERE COLA = ACOS(COLNUM);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT * FROM F01 WHERE COLA = ACOS ( COLNUM ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ACOS023')

    # HQC entry added
    defs.qry = """SELECT * FROM F01 WHERE COLA = ACOS(0.9397);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT * FROM F01 WHERE COLA = ACOS ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E393339370A'
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    #_dci.expect_selected_msg(output, '0')
    _dci.expect_file(output, defs.expfile, 'ACOS024')

    # HQC entry added
    defs.qry = """SELECT * FROM F01 WHERE COLA = CAST(ACOS(0.9397)
AS NUMERIC(12,10));"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = ("""SELECT * FROM F01 WHERE COLA = CAST ( ACOS ( #NP# )""" +
                 """ AS NUMERIC ( #NP# , #NP# ) ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 3
    defs.npliterals = '302E393339370A31320A31300A'
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ACOS025')

    # HQC entry added
    defs.qry = """SELECT * FROM F01 WHERE COLA = CAST(ACOS(0.6268)
AS NUMERIC(12,10));"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = ("""SELECT * FROM F01 WHERE COLA = CAST ( ACOS ( #NP# )""" +
                 """ AS NUMERIC ( #NP# , #NP# ) ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 3
    defs.npliterals = '302E363236380A31320A31300A'
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ACOS026')

    # HQC entry added
    defs.qry = """SELECT * FROM F01 WHERE COLA = ACOS(0.6268);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT * FROM F01 WHERE COLA = ACOS ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E363236380A'
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    #_dci.expect_selected_msg(output, '0')
    _dci.expect_file(output, defs.expfile, 'ACOS027')

    # HQC entry added
    defs.qry = """SELECT * FROM F01 WHERE COLA = ACOS(-0.62683);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT * FROM F01 WHERE COLA = ACOS ( - #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E36323638330A'
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    #_dci.expect_selected_msg(output, '0')
    _dci.expect_file(output, defs.expfile, 'ACOS028')

    # HQC entry added
    defs.qry = """SELECT * FROM F01 WHERE COLA = ACOS(9.397E-001);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT * FROM F01 WHERE COLA = ACOS ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '392E333937452D3030310A'
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    #_dci.expect_selected_msg(output, '0')
    _dci.expect_file(output, defs.expfile, 'ACOS029')

    # HQC entry added
    defs.qry = """SELECT * FROM F01 WHERE COLA = ACOS(626.8E-003);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT * FROM F01 WHERE COLA = ACOS ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '3632362E38452D3030330A'
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    #_dci.expect_selected_msg(output, '0')
    _dci.expect_file(output, defs.expfile, 'ACOS030')

    # HQC entry added
    defs.qry = """SELECT * FROM F01 WHERE COLA = ACOS(-62.683E-002);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT * FROM F01 WHERE COLA = ACOS ( - #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '36322E363833452D3030320A'
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    #_dci.expect_selected_msg(output, '0')
    _dci.expect_file(output, defs.expfile, 'ACOS031')

    # HQC entry added
    defs.qry = """SELECT * FROM F01
WHERE COLA = CAST(ACOS(-62.683 * 0.01) AS NUMERIC(12,10));"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE COLA = CAST ( ACOS ( - #NP# * #NP# )""" +
                 """ AS NUMERIC ( #NP# , #NP# ) ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 4
    defs.npliterals = '36322E3638330A302E30310A31320A31300A'
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    #_dci.expect_selected_msg(output, '0')
    _dci.expect_file(output, defs.expfile, 'ACOS032')

    # HQC entry added
    defs.qry = """SELECT * FROM F01 WHERE COLA = ACOS(0.9397 - 0.111);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT * FROM F01 WHERE COLA = ACOS ( #NP# - #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '302E393339370A302E3131310A'
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    #_dci.expect_selected_msg(output, '0')
    _dci.expect_file(output, defs.expfile, 'ACOS033')

    setup.verifyHQCnumEntries('11')

    _testmgr.testcase_end(desc)


def test_asin(desc="""asin()"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: asin()"""

    ### SQL function: ASIN()
    ### ASIN() in result-set, constant is positive:
    ###         HQC cacheable & parameterized
    ### ASIN() in result-set, constant is negative: Not cacheable
    ### ASIN() in where-clause: HQC cacheable, not parameterized

    ### ==============================================================
    ### ASIN() result-set, no constants: HQC cacheable
    setup.resetHQC()
    defs.qry = """SELECT ASIN(COLNUM) FROM F01 ORDER BY COLKEY;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    defs.hkey = """SELECT ASIN ( COLNUM ) FROM F01 ORDER BY COLKEY ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    # expect HQC::AddEntry: passed
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ASIN001')

    ### ==============================================================
    ### ASIN in result-set, constant is positive:
    ###     HQC cacheable & parameterized
    setup.resetHQC()

    # new HQC entry
    defs.qry = """SELECT ASIN(0.6543892746512) FROM F00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT ASIN ( #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '302E363534333839323734363531320A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ASIN002')

    # HQC entry found
    defs.qry = """SELECT ASIN(0.939712) FROM F00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT ASIN ( #NP# ) FROM F00 ;"""
    defs.num_hits = 1
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ASIN003')

    # new HQC entry
    defs.qry = """SELECT ASIN(0.034916E+1) FROM F00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT ASIN ( #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '302E303334393136452B310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ASIN004')

    # new HQC entry
    defs.qry = """SELECT ASIN(10.18 * 0.01) FROM F00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT ASIN ( #NP# * #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 2
    defs.pliterals = '31302E31380A302E30310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ASIN005')

    ### ==============================================================
    ### ASIN() in result-set, constant is negative: Not cacheable
    setup.resetHQC()

    qry = """SELECT ASIN(-0.3491) FROM F00;"""
    output = _dci.cmdexec(qry)
    _dci.expect_file(output, defs.expfile, 'ASIN006')
    qry = """SELECT ASIN(-6.686431 * 0.1) FROM F00;"""
    output = _dci.cmdexec(qry)
    _dci.expect_file(output, defs.expfile, 'ASIN007')
    qry = """SELECT ASIN(-6.686431E-3 * 10) FROM F00;"""
    output = _dci.cmdexec(qry)
    _dci.expect_file(output, defs.expfile, 'ASIN008')

    setup.verifyHQCempty()

    ### ==============================================================
    ### ASIN() in where-clause - HQC cacheable, not parameterized
    setup.resetHQC()

    # HQC entry added
    defs.qry = """SELECT * FROM F01 WHERE COLB = ASIN(COLNUM);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT * FROM F01 WHERE COLB = ASIN ( COLNUM ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ASIN009')

    # HQC entry added
    defs.qry = """SELECT * FROM F01 WHERE COLB = CAST(ASIN(0.4683219)
 AS NUMERIC(12,10));"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = ("""SELECT * FROM F01 WHERE COLB = CAST ( ASIN ( #NP# )""" +
                 """ AS NUMERIC ( #NP# , #NP# ) ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 3
    defs.npliterals = '302E343638333231390A31320A31300A'
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    #_dci.expect_selected_msg(output, '0')
    _dci.expect_file(output, defs.expfile, 'ASIN010')

    # HQC entry added
    defs.qry = """SELECT * FROM F01 WHERE COLB = ASIN(-0.9397);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT * FROM F01 WHERE COLB = ASIN ( - #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E393339370A'
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    #_dci.expect_selected_msg(output, '0')
    _dci.expect_file(output, defs.expfile, 'ASIN011')

    # HQC entry added
    defs.qry = """SELECT * FROM F01 WHERE COLB = CAST(ASIN(36.6759311E-2)
AS NUMERIC(12,10));"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = ("""SELECT * FROM F01 WHERE COLB = CAST ( ASIN ( #NP# )""" +
                 """ AS NUMERIC ( #NP# , #NP# ) ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 3
    defs.npliterals = '33362E36373539333131452D320A31320A31300A'
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    #_dci.expect_selected_msg(output, '0')
    _dci.expect_file(output, defs.expfile, 'ASIN012')

    _testmgr.testcase_end(desc)


def test_atan(desc="""atan()"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: atan()"""

    ### SQL function: ATAN()
    ### ATAN() in result-set, constant is positive:
    ###         HQC cacheable & parameterized
    ### ATAN() in result-set, constant is negative: Not cacheable
    ### ATAN() in where-clause: HQC cacheable, not parameterized

    ### ==============================================================
    ### ATAN() result-set, no constants: HQC cacheable
    setup.resetHQC()
    defs.qry = """SELECT ATAN(COLREAL) FROM F01 ORDER BY COLKEY;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    defs.hkey = """SELECT ATAN ( COLREAL ) FROM F01 ORDER BY COLKEY ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    # expect HQC::AddEntry: passed
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ATAN')

    ### ==============================================================
    ### ATAN in result-set, constant is positive:
    ###     HQC cacheable & parameterized
    setup.resetHQC()

    # new HQC entry
    defs.qry = """SELECT ATAN(0.6543892746512) FROM F00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT ATAN ( #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '302E363534333839323734363531320A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ATAN002')

    # new HQC entry
    defs.qry = """SELECT ATAN(0.034916E+1) FROM F00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT ATAN ( #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '302E303334393136452B310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ATAN004')

    # new HQC entry
    defs.qry = """SELECT ATAN(10.18 / 100) FROM F00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT ATAN ( #NP# / #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 2
    defs.pliterals = '31302E31380A3130300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ATAN005')

    ### ==============================================================
    ### ATAN() in result-set, constant is negative: Not cacheable
    setup.resetHQC()

    qry = """SELECT ATAN(-0.3491) FROM F00;"""
    output = _dci.cmdexec(qry)
    _dci.expect_file(output, defs.expfile, 'ATAN006')
    qry = """SELECT ATAN(-6.686431 * 0.1) FROM F00;"""
    output = _dci.cmdexec(qry)
    _dci.expect_file(output, defs.expfile, 'ATAN007')
    qry = """SELECT ATAN(-6.686431E-3 * 10) FROM F00;"""
    output = _dci.cmdexec(qry)
    _dci.expect_file(output, defs.expfile, 'ATAN008')

    setup.verifyHQCempty()

    ### ==============================================================
    ### ATAN() in where-clause - HQC cacheable, not parameterized
    setup.resetHQC()

    # HQC entry added
    defs.qry = """SELECT * FROM F01 WHERE COLB = ATAN(COLNUM);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT * FROM F01 WHERE COLB = ATAN ( COLNUM ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ATAN009')

    # HQC entry added
    defs.qry = """SELECT * FROM F01 WHERE COLC = CAST(ATAN(0.4683219)
AS REAL);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = ("""SELECT * FROM F01 WHERE COLC = CAST ( ATAN ( #NP# )""" +
                 """ AS REAL ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E343638333231390A'
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    #_dci.expect_selected_msg(output, '0')
    _dci.expect_file(output, defs.expfile, 'ATAN010')
    output = _dci.cmdexec("""select atan(0.4683219) from F00;""")

    # HQC entry added
    defs.qry = """SELECT * FROM F01 WHERE COLC = CAST(ATAN(-0.009397E+2)
AS REAL);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = ("""SELECT * FROM F01 WHERE COLC = CAST ( ATAN ( - #NP# )""" +
                 """ AS REAL ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E303039333937452B320A'
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    #_dci.expect_selected_msg(output, '0')
    _dci.expect_file(output, defs.expfile, 'ATAN011')
    output = _dci.cmdexec("""select atan(-0.009397E+2) from F00;""")

    # HQC entry added
    defs.qry = """SELECT * FROM F01 WHERE COLC = CAST(ATAN(36.6759311E-2)
AS REAL);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE COLC = CAST ( ATAN ( #NP# ) AS REAL ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '33362E36373539333131452D320A'
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    #_dci.expect_selected_msg(output, '0')
    _dci.expect_file(output, defs.expfile, 'ATAN012')
    #output = _dci.cmdexec("""select colkey, colreal, colc,""" +
    #                        """ cast(atan(colreal) as real)""" +
    #                        """ from f01 order by colkey;""")

    _testmgr.testcase_end(desc)


def test_atan2(desc="""atan2()"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: atan2()"""

    ### SQL function: ATAN2()
    ### ATAN2() in result-set, constant is positive:
    ###         HQC cacheable & parameterized
    ### ATAN2() in result-set, constant is negative: Not cacheable
    ### ATAN2() in where-clause: HQC cacheable, not parameterized

    ### ==============================================================
    ### ATAN2() in result-set, constant is positive:
    ###         HQC cacheable & parameterized
    ### ATAN2() in result-set, constant is negative: Not cacheable
    setup.resetHQC()
    defs.qry = """SELECT ATAN2(COLNUM, COLREAL) FROM F01 ORDER BY COLKEY;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    defs.hkey = ("""SELECT ATAN2 ( COLNUM , COLREAL ) FROM F01""" +
                 """ ORDER BY COLKEY ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    # expect HQC::AddEntry: passed
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ATAN2001')

    defs.qry = """SELECT ATAN2(0.192, COLNUM) FROM F01 ORDER BY COLKEY;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    defs.hkey = """SELECT ATAN2 ( #NP# , COLNUM ) FROM F01 ORDER BY COLKEY ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '302E3139320A'
    defs.num_npliterals = 0
    # expect HQC::AddEntry: passed
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ATAN2002')

    defs.qry = """SELECT ATAN2(COLREAL, 0.34819) FROM F01 ORDER BY COLKEY;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    defs.hkey = ("""SELECT ATAN2 ( COLREAL , #NP# ) FROM F01""" +
                 """ ORDER BY COLKEY ;""")
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '302E33343831390A'
    defs.num_npliterals = 0
    # expect HQC::AddEntry: passed
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ATAN2003')

    defs.qry = """SELECT ATAN2(4.321E-1, 0.34819) FROM F00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    defs.hkey = """SELECT ATAN2 ( #NP# , #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 2
    defs.pliterals = '342E333231452D310A302E33343831390A'
    defs.num_npliterals = 0
    # expect HQC::AddEntry: passed
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ATAN2004')

    ### ==============================================================
    ### ATAN2() in result-set, constant is negative: Not cacheable
    setup.resetHQC()

    qry = """SELECT ATAN2(-10.452E-1, 0.34819) FROM F00 ORDER BY COLKEY;"""
    output = _dci.cmdexec(qry)
    _dci.expect_file(output, defs.expfile, 'ATAN2005')

    qry = """SELECT ATAN2(-1.67943, -0.340819) FROM F00 ORDER BY COLKEY;"""
    output = _dci.cmdexec(qry)
    _dci.expect_file(output, defs.expfile, 'ATAN2006')

    setup.verifyHQCempty()

    ### ==============================================================
    ### ATAN2() in where-clause - HQC cacheable, not parameterized

    output = _dci.cmdexec("""drop table F02;""")

    stmt = """create table F02(
cola numeric(4,3), colb numeric(2,1), colc numeric(9,8));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into F02(cola, colb) values
(1.192, 2.3),
(-1.192, 2.3),
(1.192, -2.3),
(-1.192, -2.3),
(11.92E-1, 2.3E0),
(-119.2E-2, -2.3E0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, '6')

    stmt = """update F02 set colc = atan2(cola, colb);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, '6')

    stmt = """select * from F02 order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.expfile, 'ATAN2007')

    setup.resetHQC()

    defs.qry = """SELECT * FROM F02
WHERE COLC = CAST(ATAN2(1.192, COLB) AS NUMERIC(9,8));"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = ("""SELECT * FROM F02""" +
                 """ WHERE COLC = CAST ( ATAN2 ( #NP# , COLB )""" +
                 """ AS NUMERIC ( #NP# , #NP# ) ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 3
    defs.npliterals = '312E3139320A390A380A'
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ATAN2008')

    defs.qry = """SELECT * FROM F02
WHERE COLC = CAST(ATAN2(COLA, 2.3) AS NUMERIC(9,8));"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = ("""SELECT * FROM F02""" +
                 """ WHERE COLC = CAST ( ATAN2 ( COLA , #NP# )""" +
                 """ AS NUMERIC ( #NP# , #NP# ) ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 3
    defs.npliterals = '322E330A390A380A'
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ATAN2009')

    defs.qry = """SELECT * FROM F02
WHERE COLC = CAST(ATAN2(-1.192, 2.3) AS NUMERIC(9,8));"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = ("""SELECT * FROM F02""" +
                 """ WHERE COLC = CAST ( ATAN2 ( - #NP# , #NP# )""" +
                 """ AS NUMERIC ( #NP# , #NP# ) ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 4
    defs.npliterals = '312E3139320A322E330A390A380A'
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ATAN2010')

    defs.qry = """SELECT * FROM F02
WHERE COLC = CAST(ATAN2(1.192, -2.3) AS NUMERIC(9,8));"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = ("""SELECT * FROM F02""" +
                 """ WHERE COLC = CAST ( ATAN2 ( #NP# , - #NP# )""" +
                 """ AS NUMERIC ( #NP# , #NP# ) ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 4
    defs.npliterals = '312E3139320A322E330A390A380A'
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ATAN2011')

    defs.qry = """SELECT * FROM F02
WHERE COLC = CAST(ATAN2(1.192, 2.3) AS NUMERIC(9,8));"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = ("""SELECT * FROM F02""" +
                 """ WHERE COLC = CAST ( ATAN2 ( #NP# , #NP# )""" +
                 """ AS NUMERIC ( #NP# , #NP# ) ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 4
    defs.npliterals = '312E3139320A322E330A390A380A'
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ATAN2012')

    defs.qry = """SELECT * FROM F02
WHERE COLC = CAST(ATAN2(11.92E-1, 2.3E0) AS NUMERIC(9,8));"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = ("""SELECT * FROM F02""" +
                 """ WHERE COLC = CAST ( ATAN2 ( #NP# , #NP# )""" +
                 """ AS NUMERIC ( #NP# , #NP# ) ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 4
    defs.npliterals = '31312E3932452D310A322E3345300A390A380A'
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ATAN2013')

    output = _dci.cmdexec("""drop table f02;""")
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)


def test_ceiling(desc="""ceiling()"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: ceiling()"""

    ### SQL function: CEILING() - returns smallest integer,
    ### represented as a FLOAT data type, greater than or equal
    ### to a numeric value expression.
    ### CEILING() in result-set, constant is positive:
    ###         HQC cacheable & parameterized
    ### CEILING() in result-set, constant is negative: Not cacheable
    ### CEILING() in where-clause: HQC cacheable, not parameterized

    output = _dci.cmdexec("""drop table F02;""")

    stmt = """create table F02(
colkey int, colb numeric(12,9), colc real, cold decimal(9,6),
colb_ceil float, colc_ceil float, cold_ceil float);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into F02(colkey, colb, colc, cold) values
(1, 123.456781234, 2.34567E+3, 987.654321987),
(2, 0.123456789, -2.345E+3, 9.87654E+2),
(3, 12345.67E-3, 654.321E-2, -987.654);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, '3')

    output = _dci.cmdexec("""update F02 set colb_ceil = ceiling(colb);""")
    _dci.expect_updated_msg(output, '3')
    output = _dci.cmdexec("""update F02 set colc_ceil = ceiling(colc);""")
    _dci.expect_updated_msg(output, '3')
    output = _dci.cmdexec("""update F02 set cold_ceil = ceiling(cold);""")
    _dci.expect_updated_msg(output, '3')
    output = _dci.cmdexec("""select * from F02 order by 1;""")
    _dci.expect_file(output, defs.expfile, 'CEIL001')

    ### ==============================================================
    ### CEILING() in result-set, constant is positive:
    ###         HQC cacheable & parameterized
    setup.resetHQC()

    defs.qry = """SELECT COLKEY, CEILING(COLB), CEILING(COLC),
 CEILING(COLD) FROM F02 ORDER BY 1;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'CEIL002')
    defs.hkey = ("""SELECT COLKEY , CEILING ( COLB ) ,""" +
                 """ CEILING ( COLC ) , CEILING ( COLD )""" +
                 """ FROM F02 ORDER BY #NP# ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '310A'
    setup.verifyHQCEntryExists()

    defs.qry = """SELECT [FIRST 3]COLKEY, CEILING(2.12345),
CEILING(1234567.89123456789) FROM F02 ORDER BY 1;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'CEIL003')
    defs.hkey = ("""SELECT [ FIRST #NP# ] COLKEY , CEILING ( #NP# ) ,""" +
                 """ CEILING ( #NP# ) FROM F02 ORDER BY #NP# ;""")
    defs.num_hits = 0
    defs.num_pliterals = 2
    defs.pliterals = '322E31323334350A313233343536372E38393132333435363738390A'
    defs.num_npliterals = 2
    defs.npliterals = '330A310A'
    setup.verifyHQCEntryExists()

    # oddball case, this query is not SQC or HQC cached
    defs.qry = """SELECT [FIRST 1]
CEILING((1234567.89123456789 / 10000) * 0.50) FROM F02;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'CEIL004')
    defs.hkey = ("""SELECT [ FIRST #NP# ]""" +
                 """ CEILING ( ( #NP# / #NP# ) * #NP# ) FROM F02 ;""")
    #defs.num_hits = 0
    #defs.num_pliterals = 4
    #defs.pliterals = ('310A313233343536372E38393132333435363738390A' +
    #                   '31303030300A302E35300A')
    #defs.num_npliterals = 1
    #defs.npliterals = '310A'
    #setup.verifyHQCEntryExists()
    setup.verifyHQCEntryNOTExists()

    ### ==============================================================
    ### CEILING() in result-set, constant is negative: Not cacheable
    setup.resetHQC()
    qry = """SELECT [FIRST 1]CEILING(2.12345),
CEILING(1234567.89123456789), CEILING(-9.123), CEILING(-1234567.89)
FROM F02 ORDER BY 1;"""
    output = _dci.cmdexec(qry)
    _dci.expect_file(output, defs.expfile, 'CEIL005')

    setup.verifyHQCempty()

    ### ==============================================================
    ### CEILING() in where-clause: HQC cacheable, not parameterized

    defs.qry = """SELECT COLKEY, COLB, COLB_CEIL FROM F02
WHERE COLB_CEIL = CEILING(0.58);"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'CEIL006')
    defs.hkey = ("""SELECT COLKEY , COLB , COLB_CEIL FROM F02""" +
                 """ WHERE COLB_CEIL = CEILING ( #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E35380A'
    setup.verifyHQCEntryExists()

    defs.qry = """SELECT COLKEY, COLC, COLC_CEIL FROM F02
WHERE COLC_CEIL = CEILING(-2345.89);"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'CEIL007')
    defs.hkey = ("""SELECT COLKEY , COLC , COLC_CEIL FROM F02""" +
                 """ WHERE COLC_CEIL = CEILING ( - #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '323334352E38390A'
    setup.verifyHQCEntryExists()

    output = _dci.cmdexec("""drop table F02;""")
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)


def test_cos(desc="""cos()"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: cos()"""

    ### SQL function: COS()
    ### COS() in result-set, constant is positive:
    ###         HQC cacheable & parameterized
    ### COS() in result-set, constant is negative: Not cacheable
    ### COS() in where-clause: HQC cacheable, not parameterized

    setup.resetHQC()

    ### =========================================================
    ### COS() in result-set, constant is negative: Not cacheable
    qry = """select COS(-0.3491) from F00;"""
    output = _dci.cmdexec(qry)
    _dci.expect_file(output, defs.expfile, 'COS001')
    # oddball case, even though constant is negative, HQC cacheable
    # not parameterized. SQC cached. moved case below
    #qry = """select COS(-34.91/1000 * 10) from F00;"""
    #output = _dci.cmdexec(qry)

    setup.verifyHQCempty()

    ### =========================================================
    ### COS() in result-set, constant is positive:
    ###         HQC cacheable & parameterized
    defs.qry = """select COS(colnum) from F00;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'COS002')
    defs.hkey = """SELECT COS ( COLNUM ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    defs.qry = """select COS(0.3491) from F00;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'COS003')
    defs.hkey = """SELECT COS ( #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '302E333439310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    defs.qry = """select COS(0.003491E+2) from F00;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'COS004')
    defs.hkey = """SELECT COS ( #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '302E303033343931452B320A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    defs.qry = """select COS(3491.0 * 0.0001) from F00;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'COS005')
    defs.hkey = """SELECT COS ( #NP# * #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 2
    defs.pliterals = '333439312E300A302E303030310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # con't oddball case, HQC cacheable, not parameterized
    output = _dci.cmdexec("""select COS(-34.91/1000 * 10) from F00;""")
    _dci.expect_file(output, defs.expfile, 'COS005')
    defs.hkey = """SELECT COS ( - #NP# / #NP# * #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 3
    defs.npliterals = '33342E39310A313030300A31300A'
    setup.verifyHQCEntryExists()

    ### =========================================================
    ### COS() in where-clause: HQC cacheable, not parameterized
    output = _dci.cmdexec("""drop table F02;""")
    stmt = """create table F02(
cola real, colacos real,
colb numeric(5,4), colbcos numeric(17,16));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into F02(cola, colb) values
(0.3491, 0.9397),
(-0.9397, -0.3491);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, '2')
    stmt = """update F02
set (colacos, colbcos) = (COS(cola), COS(colb));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, '2')

    defs.qry = """SELECT * FROM F02
WHERE COLACOS = CAST(COS(0.3491) AS REAL);"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'COS006')
    defs.hkey = ("""SELECT * FROM F02""" +
                 """ WHERE COLACOS = CAST ( COS ( #NP# ) AS REAL ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E333439310A'
    setup.verifyHQCEntryExists()

    defs.qry = """SELECT * FROM F02 WHERE COLBCOS = COS(0.9397);"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'COS007')
    defs.hkey = """SELECT * FROM F02 WHERE COLBCOS = COS ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E393339370A'
    setup.verifyHQCEntryExists()

    defs.qry = """SELECT * FROM F02
WHERE COLACOS = CAST(COS(-0.9397) AS REAL);"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'COS008')
    defs.hkey = ("""SELECT * FROM F02""" +
                 """ WHERE COLACOS = CAST ( COS ( - #NP# ) AS REAL ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E393339370A'
    setup.verifyHQCEntryExists()

    defs.qry = """SELECT * FROM F02
WHERE COLBCOS = CAST(COS(9.397E-1) AS NUMERIC(17,16));"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'COS009')
    defs.hkey = ("""SELECT * FROM F02""" +
                 """ WHERE COLBCOS = CAST ( COS ( #NP# )""" +
                 """ AS NUMERIC ( #NP# , #NP# ) ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 3
    defs.npliterals = '392E333937452D310A31370A31360A'
    setup.verifyHQCEntryExists()

    defs.qry = """SELECT * FROM F02
WHERE COLACOS = CAST(COS((-34.91 * 10)/(-1000)) AS REAL);"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'COS010')
    defs.hkey = ("""SELECT * FROM F02""" +
                 """ WHERE COLACOS = CAST ( COS ( ( - #NP# * #NP# ) /""" +
                 """ ( - #NP# ) ) AS REAL ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 3
    defs.npliterals = '33342E39310A31300A313030300A'
    setup.verifyHQCEntryExists()

    output = _dci.cmdexec("""drop table F02;""")
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)


def test_cosh(desc="""cosh()"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: cosh()"""

    ### SQL function: COSH()
    ### COSH() in result-set, constant is positive:
    ###         HQC cacheable & parameterized
    ### COSH() in result-set, constant is negative: Not cacheable
    ### COSH() in where-clause: HQC cacheable, not parameterized

    setup.resetHQC()
    # cosh() in result-set, constant is negative - not cacheable
    qry = """select COSH(-1.25) from F00;"""
    output = _dci.cmdexec(defs.prepXX + qry)
    setup.verifyHQCempty()

    # new entry, cacheable but no literals
    defs.qry = """select COSH(colnum) from F00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    defs.hkey = """SELECT COSH ( COLNUM ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # new entry, parameterized
    defs.qry = """select COSH(0.9657) from F00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    defs.hkey = """SELECT COSH ( #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '302E393635370A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hit
    defs.qry = """select COSH(0.6364) from F00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    defs.hkey = """SELECT COSH ( #NP# ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '302E393635370A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # new entry, parameterized
    defs.qry = """select COSH(0.03491E+1) from F00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    defs.hkey = """SELECT COSH ( #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '302E3033343931452B310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # new entry, parameterized
    defs.qry = """select COSH(34.91 / 100) from F00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    defs.hkey = """SELECT COSH ( #NP# / #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 2
    defs.pliterals = '33342E39310A3130300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # new entry, parameterized
    defs.qry = """select COSH(acos(1)) from F00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    defs.hkey = """SELECT COSH ( ACOS ( #NP# ) ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # new entry, non-parameterized
    defs.qry = """select * from F00 where colnum = COSH(0.45);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    defs.hkey = """SELECT * FROM F00 WHERE COLNUM = COSH ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E34350A'
    setup.verifyHQCEntryExists()

    # new entry, non-parameterized
    defs.qry = """select * from F00 where colnum = COSH(0.36);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    defs.hkey = """SELECT * FROM F00 WHERE COLNUM = COSH ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E33360A'
    setup.verifyHQCEntryExists()

    # new entry, non-parameterized
    defs.qry = """select * from F00 where colnum = COSH(-0.9397);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    defs.hkey = """SELECT * FROM F00 WHERE COLNUM = COSH ( - #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E393339370A'
    setup.verifyHQCEntryExists()

    # new entry, non-parameterized
    defs.qry = """select * from F00 where colnum = COSH(-0.4563);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    defs.hkey = """SELECT * FROM F00 WHERE COLNUM = COSH ( - #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E343536330A'
    setup.verifyHQCEntryExists()

    # new entry, non-parameterized
    defs.qry = """select * from F00 where colnum = COSH(9.397E-1);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    defs.hkey = """SELECT * FROM F00 WHERE COLNUM = COSH ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '392E333937452D310A'
    setup.verifyHQCEntryExists()

    # new entry, non-parameterized
    defs.qry = """select * from F00 where colnum = COSH(4.563E-1);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    defs.hkey = """SELECT * FROM F00 WHERE COLNUM = COSH ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '342E353633452D310A'
    setup.verifyHQCEntryExists()

    # new entry, non-parameterized
    defs.qry = """select * from F00 where colnum = COSH(cos(0.93));"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    defs.hkey = """SELECT * FROM F00 WHERE COLNUM = COSH ( COS ( #NP# ) ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E39330A'
    setup.verifyHQCEntryExists()

    # new entry, non-parameterized
    defs.qry = """select * from F00 where colnum = COSH(939.7 * 0.001);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    defs.hkey = """SELECT * FROM F00 WHERE COLNUM = COSH ( #NP# * #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '3933392E370A302E3030310A'
    setup.verifyHQCEntryExists()

    # new entry, non-parameterized
    defs.qry = """select * from F00 where colnum = COSH(676.7 * 0.005);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    defs.hkey = """SELECT * FROM F00 WHERE COLNUM = COSH ( #NP# * #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '3637362E370A302E3030350A'
    setup.verifyHQCEntryExists()

    # increase hit
    defs.qry = """select COSH(0.5647) from F00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    defs.hkey = """SELECT COSH ( #NP# ) FROM F00 ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '302E393635370A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    _testmgr.testcase_end(desc)


def test_degrad(desc="""degrees() and radians()"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: degrees() and radians()"""

    ### SQL function: DEGREES()/RADIANS()
    ### in result-set, constant is positive: cacheable & parameterized
    ### in result-set, constant is negative: Not cacheable
    ### in where-clause: HQC cacheable, not parameterized

    setup.resetHQC()
    ### =====================================================
    # in result-set, constant is negative - not cacheable
    qry = """select DEGREES(-0.78540) from F00;"""
    output = _dci.cmdexec(qry)
    qry = """select radians(-180 - 90) from F00;"""
    output = _dci.cmdexec(qry)
    _dci.expect_file(output, defs.expfile, 'RADIANS004')
    qry = """select radians(-270 - 60) from F00;"""
    output = _dci.cmdexec(qry)
    _dci.expect_file(output, defs.expfile, 'RADIANS005')
    setup.verifyHQCempty()

    ### =====================================================
    ### in result-set, constant is positive: cacheable & parameterized

    # add entry1
    defs.qry = """select DEGREES(0.78540) from F00;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'DEGREES001')
    defs.hkey = """SELECT DEGREES ( #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '302E37383534300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry2
    defs.qry = """select DEGREES(colnum) from F00;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'DEGREES002')
    defs.hkey = """SELECT DEGREES ( COLNUM ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry3; type incompatible
    defs.qry = """select DEGREES(3.1415926) from F00;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'DEGREES003')
    defs.hkey = """SELECT DEGREES ( #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '332E313431353932360A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry1
    defs.qry = """select DEGREES(0.14719) from F00;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'DEGREES004')
    defs.hkey = """SELECT DEGREES ( #NP# ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '302E37383534300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    #add entry4
    defs.qry = """select radians(45) from F00;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'RADIANS001')
    defs.hkey = """SELECT RADIANS ( #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '34350A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    #add entry5
    defs.qry = """select radians(180) from F00;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'RADIANS002')
    defs.hkey = """SELECT RADIANS ( #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '3138300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    #increase hits, entry 4
    defs.qry = """select radians(60) from F00;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'RADIANS003')
    defs.hkey = """SELECT RADIANS ( #NP# ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '34350A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    #add entry6
    defs.qry = """select degrees(radians(180)) from F00;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'DEGREES005')
    defs.hkey = """SELECT DEGREES ( RADIANS ( #NP# ) ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '3138300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    #add entry7
    defs.qry = """select radians(degrees(0.3491)) from F00;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'RADIANS006')
    defs.hkey = """SELECT RADIANS ( DEGREES ( #NP# ) ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '302E333439310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    ### =====================================================
    ### in where-clause: HQC cacheable, not parameterized
    # add entry8
    defs.qry = """select * from F00 where colnum = DEGREES(2.25);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT * FROM F00 WHERE COLNUM = DEGREES ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '322E32350A'
    setup.verifyHQCEntryExists()

    # add entry9
    defs.qry = """select * from F00 where colnum = RADIANS(45);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT * FROM F00 WHERE COLNUM = RADIANS ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '34350A'
    setup.verifyHQCEntryExists()

    # add entry10, non parameterized
    defs.qry = """select * from F00 where colnum = RADIANS(90);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT * FROM F00 WHERE COLNUM = RADIANS ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '39300A'
    setup.verifyHQCEntryExists()

    # add entry11
    defs.qry = """select * from F00 where colnum = RADIANS(degrees(270));"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = ("""SELECT * FROM F00 WHERE""" +
                 """ COLNUM = RADIANS ( DEGREES ( #NP# ) ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '3237300A'
    setup.verifyHQCEntryExists()

    # add entry12
    defs.qry = """select * from F00 where colnum = RADIANS(-45);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT * FROM F00 WHERE COLNUM = RADIANS ( - #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '34350A'
    setup.verifyHQCEntryExists()

    # increase hits, entry12
    defs.qry = """select * from F00 where colnum = RADIANS(-45);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT * FROM F00 WHERE COLNUM = RADIANS ( - #NP# ) ;"""
    defs.num_hits = 1
    setup.verifyHQCEntryExists()

    # add entry13
    defs.qry = """select * from F00 where colnum = RADIANS(60);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT * FROM F00 WHERE COLNUM = RADIANS ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '36300A'
    setup.verifyHQCEntryExists()

    # increase hits, entry9
    defs.qry = """select * from F00 where colnum = RADIANS(45);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT * FROM F00 WHERE COLNUM = RADIANS ( #NP# ) ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '34350A'
    setup.verifyHQCEntryExists()

    _testmgr.testcase_end(desc)


def test_exploglog10(desc="""exp(),log(),log10()"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: exp(),log(),log10()"""

    ### SQL function: EXP()/LOG()/LOG10()
    ### in result-set, constant is positive: cacheable & parameterized
    ### in result-set, constant is negative: Not cacheable
    ### in where-clause: HQC cacheable, not parameterized

    setup.resetHQC()
    ### =====================================================
    # in result-set, constant is negative - not cacheable
    qry = """select EXP(-0.78540) from F00;"""
    output = _dci.cmdexec(qry)
    _dci.expect_file(output, defs.expfile, 'EXP001')
    qry = """select EXP(-744.44) from F00;"""
    output = _dci.cmdexec(qry)
    _dci.expect_file(output, defs.expfile, 'EXP002')
    setup.verifyHQCempty()

    ### =====================================================
    ### in result-set, constant is positive: cacheable & parameterized
    # add entry1
    defs.qry = """select EXP(1.25) from F00;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'EXP003')
    defs.hkey = """SELECT EXP ( #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '312E32350A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry2
    defs.qry = """select EXP(709.7827128) from F00;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'EXP004')
    defs.hkey = """SELECT EXP ( #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '3730392E373832373132380A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry1
    defs.qry = """select EXP(4.97) from F00;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'EXP005')
    defs.hkey = """SELECT EXP ( #NP# ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '312E32350A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry3
    defs.qry = """select EXP(log(2.0)) from F00;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'EXP006')
    defs.hkey = """SELECT EXP ( LOG ( #NP# ) ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '322E300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry4
    defs.qry = """select LOG(4.7463822) from F00;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'LOG002')
    defs.hkey = """SELECT LOG ( #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '342E373436333832320A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry3
    defs.qry = """select EXP(log(1.5)) from F00;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'EXP007')
    defs.hkey = """SELECT EXP ( LOG ( #NP# ) ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '322E300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry4
    defs.qry = """select LOG(6.1111222) from F00;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'LOG003')
    defs.hkey = """SELECT LOG ( #NP# ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '342E373436333832320A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry5
    defs.qry = """select LOG10(6.1111222) from F00;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'LOG10_001')
    defs.hkey = """SELECT LOG10 ( #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '362E313131313232320A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    ### =====================================================
    ### in where-clause: HQC cacheable, not parameterized
    # add entry5
    defs.qry = """select * from F00 where colnum = EXP(2.25);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT * FROM F00 WHERE COLNUM = EXP ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '322E32350A'
    setup.verifyHQCEntryExists()

    # add entry6
    defs.qry = """select * from F00
where colnum = EXP(300.1234 + 234.987) ;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT * FROM F00 WHERE COLNUM = EXP ( #NP# + #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '3330302E313233340A3233342E3938370A'
    setup.verifyHQCEntryExists()

    # add entry7
    defs.qry = """select * from F00 where EXP(colnum) = EXP(0.9397);"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'EXP008')
    defs.hkey = """SELECT * FROM F00 WHERE EXP ( COLNUM ) = EXP ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E393339370A'
    setup.verifyHQCEntryExists()

    # add entry8
    defs.qry = """select * from F00 where colnum = LOG(3.14);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT * FROM F00 WHERE COLNUM = LOG ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '332E31340A'
    setup.verifyHQCEntryExists()

    # increase hits, entry5
    defs.qry = """select * from F00 where colnum = EXP(2.25);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT * FROM F00 WHERE COLNUM = EXP ( #NP# ) ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '322E32350A'
    setup.verifyHQCEntryExists()

    # add entry9
    defs.qry = """select * from F00 where colnum = LOG(5.75);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT * FROM F00 WHERE COLNUM = LOG ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '352E37350A'
    setup.verifyHQCEntryExists()

    # add entry10
    defs.qry = """select * from F00 where colnum = LOG(10.0/3.33);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT * FROM F00 WHERE COLNUM = LOG ( #NP# / #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '31302E300A332E33330A'
    setup.verifyHQCEntryExists()

    # add entry11
    defs.qry = """select * from F00 where colnum = LOG10(EXP(485.6) * 50);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = ("""SELECT * FROM F00""" +
                 """ WHERE COLNUM = LOG10 ( EXP ( #NP# ) * #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '3438352E360A35300A'
    setup.verifyHQCEntryExists()

    # increase hits, entry6
    defs.qry = """select * from F00 where colnum = EXP(300.1234 + 234.987) ;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    defs.hkey = """SELECT * FROM F00 WHERE COLNUM = EXP ( #NP# + #NP# ) ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '3330302E313233340A3233342E3938370A'
    setup.verifyHQCEntryExists()

    _testmgr.testcase_end(desc)


def test_floor(desc="""floor()"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: floor()"""

    ### SQL function: FLOOR()
    ### in result-set, constant is positive: cacheable & parameterized
    ### in result-set, constant is negative: Not cacheable
    ### in where-clause: HQC cacheable, not parameterized

    setup.resetHQC()
    ### =====================================================
    # in result-set, constant is negative - not cacheable
    qry = """select FLOOR(-0.78540) from F00;"""
    output = _dci.cmdexec(qry)
    _dci.expect_file(output, defs.expfile, 'FLOOR1')
    qry = """select FLOOR(-744.44/100 * 2.2) from F00;"""
    output = _dci.cmdexec(qry)
    _dci.expect_file(output, defs.expfile, 'FLOOR2')
    qry = """select FLOOR(EXP(-702.2)/100) from F00;"""
    output = _dci.cmdexec(qry)
    _dci.expect_file(output, defs.expfile, 'FLOOR3')
    setup.verifyHQCempty()

    ### =====================================================
    ### in result-set, constant is positive: cacheable & parameterized

    # add entry1
    defs.qry = """select FLOOR(222.995) from F00;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'FLOOR004')

    # increase hits, entry1
    defs.qry = """select FLOOR(2.596) from F00;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'FLOOR005')

    # increase hits, entry1
    defs.qry = """select FLOOR(495.958) from F00;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'FLOOR006')
    defs.hkey = """SELECT FLOOR ( #NP# ) FROM F00 ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '3232322E3939350A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry1
    defs.qry = """select FLOOR(100.11) from F00;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'FLOOR007')

    # add entry2
    defs.qry = """select FLOOR(cast(colnum as float)) from F00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT FLOOR ( CAST ( COLNUM AS FLOAT ) ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry1
    defs.qry = """select FLOOR(9.013) from F00;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'FLOOR008')
    defs.hkey = """SELECT FLOOR ( #NP# ) FROM F00 ;"""
    defs.num_hits = 4
    defs.num_pliterals = 1
    defs.pliterals = '3232322E3939350A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry2
    defs.qry = """select FLOOR(cast(colnum as float)) from F00;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'FLOOR009')
    defs.hkey = """SELECT FLOOR ( CAST ( COLNUM AS FLOAT ) ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry3
    defs.qry = """select FLOOR(2048 / 89.12 * colnum) from F00;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'FLOOR010')
    defs.hkey = """SELECT FLOOR ( #NP# / #NP# * COLNUM ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 2
    defs.pliterals = '323034380A38392E31320A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    ### =====================================================
    ### in where-clause: HQC cacheable, not parameterized
    setup.resetHQC()

    output = _dci.cmdexec("""drop table F02;""")
    stmt = """create table F02 (colval numeric(11,5), colflr float);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # add entry
    defs.qry = """insert into F02(colval) values
(-123456.78901),(0.0),(1.17),(2.25),(117.56412),(987654.32109);"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_inserted_msg(output, '6')
    defs.hkey = ("""INSERT INTO F02 ( COLVAL ) VALUES ( - #NP# ) ,"""
                 + """ ( #NP# ) , ( #NP# ) , ( #NP# ) , ( #NP# ) ,"""
                 + """ ( #NP# ) ;""")
    #defs.num_hits = 0
    #defs.num_pliterals = 6
    #defs.pliterals = ('3132333435362E37383930310A302E300A' +
    #                   '312E31370A322E32350A3131372E35363431320A' +
    #                   '3938373635342E33323130390A')
    #defs.num_npliterals = 0
    #setup.verifyHQCEntryExists()
    setup.verifyHQCEntryNOTExists()

    # add entry
    defs.qry = """update F02 set colflr = FLOOR(colval);"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_updated_msg(output, '6')
    defs.hkey = """UPDATE F02 SET COLFLR = FLOOR ( COLVAL ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    output = _dci.cmdexec("""select * from F02 order by 1;""")
    _dci.expect_file(output, defs.expfile, 'FLOOR011')
    # add entry
    defs.qry = """SELECT * FROM F02 WHERE COLFLR = FLOOR(COLVAL);"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'FLOOR012')
    defs.hkey = """SELECT * FROM F02 WHERE COLFLR = FLOOR ( COLVAL ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry
    defs.qry = """SELECT * FROM F02 WHERE COLFLR = FLOOR(89754.223);"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM F02 WHERE COLFLR = FLOOR ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '38393735342E3232330A'
    setup.verifyHQCEntryExists()

    # add entry
    defs.qry = """select * from F02 where colflr = FLOOR(2.25);"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'FLOOR013')
    defs.hkey = """SELECT * FROM F02 WHERE COLFLR = FLOOR ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '322E32350A'
    setup.verifyHQCEntryExists()

    # add entry
    defs.qry = """select * from F02 where colflr = FLOOR(-123456.78901);"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'FLOOR014')
    defs.hkey = """SELECT * FROM F02 WHERE COLFLR = FLOOR ( - #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '3132333435362E37383930310A'
    setup.verifyHQCEntryExists()

    # add entry
    defs.qry = """select * from F02
where colflr = FLOOR(-123000.00901 + -456.78);"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'FLOOR015')
    defs.hkey = ("""SELECT * FROM F02""" +
                 """ WHERE COLFLR = FLOOR ( - #NP# + - #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '3132333030302E30303930310A3435362E37380A'
    setup.verifyHQCEntryExists()

    output = _dci.cmdexec("""drop table F02;""")
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)


def test_mod(desc="""mod()"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: mod()"""

    ### SQL function: MOD()
    ### in result-set, constant is positive: cacheable & parameterized
    ### in result-set, constant is negative: Not cacheable
    ### in where-clause: HQC cacheable, not parameterized

    setup.resetHQC()
    ### =====================================================
    # in result-set, constant is negative - not cacheable
    qry = """select MOD(-64586, 2048) from F00;"""
    output = _dci.cmdexec(qry)
    _dci.expect_file(output, defs.expfile, 'MOD001')
    qry = """select MOD(-10000000, -10) from F00;"""
    output = _dci.cmdexec(qry)
    _dci.expect_file(output, defs.expfile, 'MOD002')
    qry = """select MOD(1000000, -colsint) as modsint,
colsint from F02 order by colsint;"""
    output = _dci.cmdexec(qry)
    setup.verifyHQCempty()

    ### =====================================================
    ### in result-set, constant is positive: cacheable & parameterized
    output = _dci.cmdexec("""drop table F02;""")
    stmt = """create table F02 (
colsint smallint, colint int, collint largeint, myint int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # add entry
    defs.qry = """insert into F02 values
(-8192, -2147483647, 288230376151711744, 7),
(2048, 2147483647, -288230376151711744, 49),
(16384, 8192, 1024, 0);"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_inserted_msg(output, '3')
    defs.hkey = ("""INSERT INTO F02 VALUES ( - #NP# , - #NP# ,"""
                 + """ #NP# , #NP# ) , ( #NP# , #NP# , - #NP# ,"""
                 + """ #NP# ) , ( #NP# , #NP# , #NP# , #NP# ) ;""")
    #defs.num_hits = 0
    #defs.num_pliterals = 12
    #defs.pliterals = ('383139320A323134373438333634370A' +
    #                   '3238383233303337363135313731313734340A' +
    #                   '370A323034380A323134373438333634370A' +
    #                   '3238383233303337363135313731313734340A' +
    #                   '34390A31363338340A383139320A313032340A300A')
    ##defs.num_npliterals = 0
    #setup.verifyHQCEntryExists()
    setup.verifyHQCEntryNOTExists()

    # add entry1
    defs.qry = """select MOD(colint,colsint) from F02;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'MOD003')
    defs.hkey = """SELECT MOD ( COLINT , COLSINT ) FROM F02 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry2
    defs.qry = """select colint, MOD(colint, 100) from F02 order by colint;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'MOD004')
    defs.hkey = ("""SELECT COLINT , MOD ( COLINT , #NP# ) FROM F02""" +
                 """ ORDER BY COLINT ;""")
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '3130300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry3
    defs.qry = """select MOD(collint, 8000) as modlint, collint from F02
order by collint;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'MOD005')
    defs.hkey = ("""SELECT MOD ( COLLINT , #NP# ) AS MODLINT , COLLINT""" +
                 """ FROM F02 ORDER BY COLLINT ;""")
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '383030300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry4
    defs.qry = """select MOD(10017,10) from F00;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'MOD006')
    defs.hkey = """SELECT MOD ( #NP# , #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 2
    defs.pliterals = '31303031370A31300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    ### =====================================================
    ### in where-clause: HQC cacheable, not parameterized
    defs.qry = """select * from F02 where colsint = MOD(1008192, -1000000);"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'MOD007')
    defs.hkey = """SELECT * FROM F02 WHERE COLSINT = MOD ( #NP# , - #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '313030383139320A313030303030300A'
    setup.verifyHQCEntryExists()

    defs.qry = """select * from F02 where myint = MOD(colsint, 1999);"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'MOD008')
    defs.hkey = """SELECT * FROM F02 WHERE MYINT = MOD ( COLSINT , #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '313939390A'
    setup.verifyHQCEntryExists()

    defs.qry = """select colsint, collint, MOD(colsint, collint) from F02
where MOD(colsint, collint) = 0;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'MOD009')
    defs.hkey = ("""SELECT COLSINT , COLLINT , MOD ( COLSINT , COLLINT )""" +
                 """ FROM F02 WHERE MOD ( COLSINT , COLLINT ) = #NP# ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '300A'
    setup.verifyHQCEntryExists()

    defs.qry = """select * from F02 where myint = MOD(1047, 10);"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'MOD010')
    defs.hkey = """SELECT * FROM F02 WHERE MYINT = MOD ( #NP# , #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '313034370A31300A'
    setup.verifyHQCEntryExists()

    output = _dci.cmdexec("""drop table F02;""")
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)


def test_pi(desc="""pi()"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: pi()"""

    ### SQL function: PI()
    ### in result-set: cacheable
    ### in where-clause: HQC cacheable

    setup.resetHQC()
    output = _dci.cmdexec("""drop table F02;""")
    stmt = """create table F02 (cola varchar(3), colb float);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    defs.qry = """insert into F02 values ('PI', pi());"""
    output = _dci.cmdexec(defs.qry)
    defs.hkey = """INSERT INTO F02 VALUES ( #NP# , PI ( ) ) ;"""
    #defs.num_hits = 0
    #defs.num_pliterals = 1
    #defs.pliterals = '275049270A'
    #defs.num_npliterals = 0
    #setup.verifyHQCEntryExists()
    setup.verifyHQCEntryNOTExists()

    output = _dci.cmdexec("""select * from F02;""")
    _dci.expect_file(output, defs.expfile, 'PI001')

    # add entry1
    defs.qry = """select PI() from F02;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '3.1415926')
    defs.hkey = """SELECT PI ( ) FROM F02 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry2
    defs.qry = """select * from F02 where colb = PI();"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'PI002')
    defs.hkey = """SELECT * FROM F02 WHERE COLB = PI ( ) ;"""
    setup.verifyHQCEntryExists()

    # increase hits, entry1
    defs.qry = """select PI() from F02;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_str_token(output, '3.1415926')
    defs.hkey = """SELECT PI ( ) FROM F02 ;"""
    defs.num_hits = 1
    setup.verifyHQCEntryExists()

    # increase hits, entry2
    defs.qry = """select * from F02 where colb = PI();"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'PI002')
    defs.hkey = """SELECT * FROM F02 WHERE COLB = PI ( ) ;"""
    defs.num_hits = 1
    setup.verifyHQCEntryExists()

    output = _dci.cmdexec("""drop table F02;""")
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)


def test_power(desc="""power()"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: power()"""

    ### SQL function: POWER()
    ### in result-set, constant is positive: cacheable & parameterized
    ### in result-set, constant is negative: Not cacheable
    ### in where-clause: HQC cacheable, not parameterized

    setup.resetHQC()

    ### ======================================================
    ### in result-set, constant is negative: Not cacheable
    output = _dci.cmdexec("""select POWER(-2, -10) from F00;""")
    _dci.expect_file(output, defs.expfile, 'POWER002')
    output = _dci.cmdexec("""select POWER(-2, 10) from F00;""")
    _dci.expect_file(output, defs.expfile, 'POWER003')
    output = _dci.cmdexec("""select POWER(2, -10) from F00;""")
    _dci.expect_file(output, defs.expfile, 'POWER004')

    setup.verifyHQCempty()

    output = _dci.cmdexec("""drop table F02;""")
    stmt = """create table F02 (
colbase numeric(5,2), colexp int, colpow numeric(9,3));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    defs.qry = """insert into F02 values (3, 5, POWER(3,5)),
(10, 2, POWER(10,2)),
(2.5, 3, POWER(2.5,3));"""
    output = _dci.cmdexec(defs.qry)
    defs.hkey = ("""INSERT INTO F02 VALUES ( #NP# , #NP# ,"""
                 + """ POWER ( #NP# , #NP# ) ) , ( #NP# , #NP# ,"""
                 + """ POWER ( #NP# , #NP# ) ) , ( #NP# , #NP# ,"""
                 + """ POWER ( #NP# , #NP# ) ) ;""")
    #defs.num_hits = 0
    #defs.num_pliterals = 12
    #defs.pliterals = ('330A350A330A350A31300A320A31300A320A' +
    #                   '322E350A330A322E350A330A')
    #defs.num_npliterals = 0
    #setup.verifyHQCEntryExists()
    setup.verifyHQCEntryNOTExists()

    output = _dci.cmdexec("""select * from F02;""")
    _dci.expect_file(output, defs.expfile, 'POWER001')

    ### ======================================================
    ### in result-set, constant is positive: cacheable & parameterized
    # add entry1
    defs.qry = """select POWER(colbase, 5) from F02;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'POWER005')
    defs.hkey = """SELECT POWER ( COLBASE , #NP# ) FROM F02 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '350A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry2
    defs.qry = """select POWER(100/2, colexp) from F02;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'POWER006')
    defs.hkey = """SELECT POWER ( #NP# / #NP# , COLEXP ) FROM F02 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 2
    defs.pliterals = '3130300A320A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry3
    defs.qry = """select POWER(colbase + 3, colexp * 2) from F02;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'POWER007')
    defs.hkey = ("""SELECT POWER ( COLBASE + #NP# , COLEXP * #NP# )""" +
                 """ FROM F02 ;""")
    defs.num_hits = 0
    defs.num_pliterals = 2
    defs.pliterals = '330A320A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry3
    defs.qry = """select POWER(colbase + 3, colexp * 2) from F02;"""
    output = _dci.cmdexec(defs.qry)
    _dci.expect_file(output, defs.expfile, 'POWER007')
    defs.hkey = ("""SELECT POWER ( COLBASE + #NP# , COLEXP * #NP# )""" +
                 """ FROM F02 ;""")
    defs.num_hits = 1
    defs.num_pliterals = 2
    defs.pliterals = '330A320A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    ### ======================================================
    ### in where-clause: HQC cacheable, not parameterized
    # add entry4
    defs.qry = """select * from F02 where colpow = POWER(2.5, 3);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'POWER008')
    defs.hkey = """SELECT * FROM F02 WHERE COLPOW = POWER ( #NP# , #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '322E350A330A'
    setup.verifyHQCEntryExists()

    # add entry5
    defs.qry = """select * from F02 where colpow = POWER(-2.5, -3);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'POWER009')
    defs.hkey = ("""SELECT * FROM F02""" +
                 """ WHERE COLPOW = POWER ( - #NP# , - #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '322E350A330A'
    setup.verifyHQCEntryExists()

    # add entry6
    defs.qry = """select * from F02 where POWER(colbase, colexp) = 243;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'POWER010')
    defs.hkey = ("""SELECT * FROM F02""" +
                 """ WHERE POWER ( COLBASE , COLEXP ) = #NP# ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '3234330A'
    setup.verifyHQCEntryExists()

    # increase hits, entry4
    defs.qry = """select * from F02 where colpow = POWER(2.5, 3);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'POWER008')
    defs.hkey = """SELECT * FROM F02 WHERE COLPOW = POWER ( #NP# , #NP# ) ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '322E350A330A'
    setup.verifyHQCEntryExists()

    # increase hits, entry5
    defs.qry = """select * from F02 where colpow = POWER(-2.5, -3);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'POWER009')
    defs.hkey = ("""SELECT * FROM F02""" +
                 """ WHERE COLPOW = POWER ( - #NP# , - #NP# ) ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '322E350A330A'
    setup.verifyHQCEntryExists()

    # increase hits, entry6
    defs.qry = """select * from F02 where POWER(colbase, colexp) = 243;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'POWER010')
    defs.hkey = ("""SELECT * FROM F02""" +
                 """ WHERE POWER ( COLBASE , COLEXP ) = #NP# ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '3234330A'
    setup.verifyHQCEntryExists()

    output = _dci.cmdexec("""drop table F02;""")
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)


def test_round(desc="""round()"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: round()"""

    ### SQL function: ROUND()
    ### in result-set, constant is positive: cacheable & parameterized
    ### in result-set, constant is negative: Not cacheable
    ### in where-clause: HQC cacheable, not parameterized

    setup.resetHQC()

    ### ======================================================
    ### in result-set, constant is negative: Not cacheable
    # oddball cases - SQC cached, HQC cacheable, NOT parameterized
    output = _dci.cmdexec(defs.prepXX + """select
ROUND(-123.4567) from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ROUND001')
    defs.hkey = """SELECT ROUND ( - #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '3132332E343536370A'
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec(defs.prepXX + """select
ROUND(-123.4567, colkey) from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ROUND002')
    defs.hkey = """SELECT ROUND ( - #NP# , COLKEY ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '3132332E343536370A'
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec(defs.prepXX + """select
ROUND(colnum, -2) from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ROUND003')
    defs.hkey = """SELECT ROUND ( COLNUM , - #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '320A'
    setup.verifyHQCEntryExists()

    #setup.verifyHQCempty()

    output = _dci.cmdexec("""drop table F02;""")
    stmt = """create table F02 (
colival int, colrnd4 int,
collval largeint, colrnd12 int,
colsval smallint, colrnd3 int,
colnval1 numeric(9,3), colrnd2 int, colrnd_2 int,
colnval2 numeric(18,15), colrnd_9 float,
colnval3 numeric(27,20), colrnd7 int,
colrval real,  colrnd6 int, colrnd_6 float,
colfval float, colrnd5 int, colrnd_5 float,
coldval double precision, colrnd1 int, colrnd_1 float
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    defs.qry = """insert into F02(colival, collval, colsval, colnval1,
colnval2, colnval3, colrval, colfval, coldval) values
(2147483647, 9223372036854775807, 32767,
123456.123, 987.123456789012345,
9876543.21098765432109876543,
3.40282347E+8, 1.7976931348623157E+10,
1.7976931348623157E+10),
(-2147483648, -9223372036854775808, -32768,
-123456.123, -987.123456789012345,
-9876543.21098765432109876543,
-1.17549435E-8, -2.2250738585072014E-5,
-2.2250738585072014E-5);"""
    output = _dci.cmdexec(defs.qry)
    defs.hkey = ("""INSERT INTO F02 ( COLIVAL , COLLVAL , COLSVAL ,"""
                 + """ COLNVAL1 , COLNVAL2 , COLNVAL3 , COLRVAL , COLFVAL ,"""
                 + """ COLDVAL ) VALUES ( #NP# , #NP# , #NP# , #NP# ,"""
                 + """ #NP# , #NP# , #NP# , #NP# , #NP# ) , ( - #NP# ,"""
                 + """ - #NP# , - #NP# , - #NP# , - #NP# , - #NP# ,"""
                 + """ - #NP# , - #NP# , - #NP# ) ;""")
    #defs.num_hits = 0
    #defs.num_pliterals = 18
    #defs.pliterals = ('323134373438333634370A' +
    #                   '393232333337323033363835343737353830370A' +
    #                   '33323736370A3132333435362E3132330A' +
    #                   '3938372E3132333435363738393031323334350A' +
    #                   '393837363534332E32313039383736353433323130' +
    #                   '393837363534330A332E3430323832333437452B380A' +
    #                   '312E37393736393331333438363233313537452B31300A' +
    #                   '312E37393736393331333438363233313537452B31300A' +
    #                   '323134373438333634380A' +
    #                   '393232333337323033363835343737353830380A' +
    #                   '33323736380A3132333435362E3132330A' +
    #                   '3938372E3132333435363738393031323334350A' +
    #                   '393837363534332E32313039383736353433323130393837' +
    #                   '363534330A312E3137353439343335452D380A' +
    #                   '322E32323530373338353835303732303134452D350A' +
    #                   '322E32323530373338353835303732303134452D350A')
    #defs.num_npliterals = 0
    #setup.verifyHQCEntryExists()
    setup.verifyHQCEntryNOTExists()

    defs.qry = """update F02 set (colrnd4, colrnd12, colrnd3,
colrnd2, colrnd_2, colrnd_9, colrnd7, colrnd6, colrnd_6, colrnd5,
colrnd_5, colrnd1, colrnd_1) = (ROUND(colival, 4), ROUND(collval, 12),
ROUND(colsval, 3), ROUND(colnval1, 2), ROUND(colnval1, -2),
ROUND(colnval2, -9), ROUND(colnval3, 7), ROUND(colrval, 6),
ROUND(colrval, -6), ROUND(colfval, 5), ROUND(colfval, -5),
ROUND(coldval, 1), ROUND(coldval, -1));"""
    defs.hkey = ("""UPDATE F02 SET ( COLRND4 , COLRND12 , COLRND3 ,""" +
                 """ COLRND2, COLRND_2 , COLRND_9 , COLRND7 , COLRND6,""" +
                 """ COLRND_6 , COLRND5, COLRND_5 , COLRND1 ,""" +
                 """ COLRND_1 ) = ( ROUND ( COLIVAL , #NP# ) ,""" +
                 """ ROUND ( COLLVAL , #NP# ) ,""" +
                 """ ROUND ( COLSVAL , #NP# ) ,""" +
                 """ ROUND ( COLNVAL1 , #NP# ) ,""" +
                 """ ROUND ( COLNVAL1 , - #NP# ) ,""" +
                 """ ROUND ( COLNVAL2 , - #NP# ) ,""" +
                 """ ROUND ( COLNVAL3 , #NP# ) ,""" +
                 """ ROUND ( COLRVAL , #NP# ) ,""" +
                 """ ROUND ( COLRVAL , - #NP# ) ,""" +
                 """ ROUND ( COLFVAL , #NP# ) ,""" +
                 """ ROUND ( COLFVAL , - #NP# ) ,""" +
                 """ ROUND ( COLDVAL , #NP# ) ,""" +
                 """ ROUND ( COLDVAL , - #NP# ) ) ;""")
    #defs.num_hits = 0
    #defs.num_pliterals = 13
    #defs.pliterals = ('340A31320A330A320A320A390A370A360A360A' +
    #                   '350A350A310A310A')
    #defs.num_npliterals = 0
    #setup.verifyHQCEntryExists()
    setup.verifyHQCEntryNOTExists()

    output = _dci.cmdexec("""select * from F02;""")
    _dci.expect_file(output, defs.expfile, 'ROUND004')

    output = _dci.cmdexec("""drop table F02;""")
    _dci.expect_complete_msg(output)

    stmt = """create table F02 (colrval real, colrnd int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into F02 values (-9223372036854775808, -17),
(9223372036854775807, -17),
(9.223372036854775807, 16);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, '3')

    stmt = """create table F03(rndval numeric(18,6));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into F03 values
(678900000.000000),
(678917321.300000),
(-80000.000000),
(-76543.880000),
(998000.000000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, '5')

    ### ======================================================
    ### in result-set, constant is positive: cacheable & parameterized

    setup.resetHQC()

    # oddball case - SQC cached, but not HQC cached
    # add entry1
    defs.qry = """select ROUND(123.4567) from F00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ROUND005')
    #defs.hkey = """SELECT ROUND ( #NP# ) FROM F00 ;"""
    #defs.num_hits = 0
    #defs.num_pliterals = 1
    #defs.pliterals = '3132332E343536370A'
    #defs.num_npliterals = 0
    #setup.verifyHQCEntryExists()
    # increase hits, entry1
    defs.qry = """select ROUND(345.6789) from F00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ROUND006')
    #defs.hkey = """SELECT ROUND ( #NP# ) FROM F00 ;"""
    #defs.num_hits = 1
    #defs.num_pliterals = 1
    #defs.pliterals = '3132332E343536370A'
    #defs.num_npliterals = 0
    #setup.verifyHQCEntryExists()
    # add entry2
    defs.qry = """select ROUND(12.345) from F00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ROUND007')
    #defs.hkey = """SELECT ROUND ( #NP# ) FROM F00 ;"""
    #defs.num_hits = 0
    #defs.num_pliterals = 1
    #defs.pliterals = '31322E3334350A'
    #defs.num_npliterals = 0
    #setup.verifyHQCEntryExists()
    # add entry3
    defs.qry = """select ROUND(345.678912345) from F00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ROUND008')
    #defs.hkey = """SELECT ROUND ( #NP# ) FROM F00 ;"""
    #defs.num_hits = 0
    #defs.num_pliterals = 1
    #defs.pliterals = '3334352E3637383931323334350A'
    #defs.num_npliterals = 0
    #setup.verifyHQCEntryExists()
    setup.verifyHQCempty()

    # add entry4
    defs.qry = """select ROUND(3.45678912345E+4, 5) from F00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ROUND009')
    defs.hkey = """SELECT ROUND ( #NP# , #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 2
    defs.pliterals = '332E3435363738393132333435452B340A350A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry5
    defs.qry = """select ROUND(9.1234 * 9.1234, 3) from F00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ROUND010')
    defs.hkey = """SELECT ROUND ( #NP# * #NP# , #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    # oddball case - literals are non-parameterized
    defs.num_pliterals = 0
    defs.num_npliterals = 3
    defs.npliterals = '392E313233340A392E313233340A330A'
    setup.verifyHQCEntryExists()

    # add entry6
    defs.qry = """select ROUND(55555.5555555, colkey + 2) from F00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ROUND011')
    defs.hkey = """SELECT ROUND ( #NP# , COLKEY + #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    # oddball case - literals are non-parameterized
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '35353535352E353535353535350A320A'
    setup.verifyHQCEntryExists()

    # add entry7
    defs.qry = """select ROUND(55555.5555555, colkey - 3) from F00;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ROUND012')
    defs.hkey = """SELECT ROUND ( #NP# , COLKEY - #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    # oddball case - literals are non-parameterized
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '35353535352E353535353535350A330A'
    setup.verifyHQCEntryExists()

    # add entry8
    defs.qry = """select ROUND(colrval, 12) from F02;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ROUND013')
    defs.hkey = """SELECT ROUND ( COLRVAL , #NP# ) FROM F02 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '31320A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry9
    defs.qry = """select ROUND(-9223372036854775808, colrnd) from F02;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ROUND014')
    defs.hkey = """SELECT ROUND ( - #NP# , COLRND ) FROM F02 ;"""
    defs.num_hits = 0
    # oddball case - literals are non-parameterized
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '393232333337323033363835343737353830380A'
    setup.verifyHQCEntryExists()

    # add entry9a
    defs.qry = """select ROUND(-9223372036854775809, colrnd) from F02;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ROUND014a')
    defs.hkey = """SELECT ROUND ( - #NP# , COLRND ) FROM F02 ;"""
    defs.num_hits = 0
    # oddball case - literals are non-parameterized
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '393232333337323033363835343737353830390A'
    setup.verifyHQCEntryExists()

    # increase hits, entry9
    defs.qry = """select ROUND(-9223372036854775808, colrnd) from F02;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ROUND014')
    defs.hkey = """SELECT ROUND ( - #NP# , COLRND ) FROM F02 ;"""
    defs.num_hits = 1
    # oddball case - literals are non-parameterized
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '393232333337323033363835343737353830380A'
    setup.verifyHQCEntryExists()

    # add entry10
    defs.qry = """select * from F03
where rndval = ROUND(678917321.345678, -5);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ROUND015')
    defs.hkey = ("""SELECT * FROM F03""" +
                 """ WHERE RNDVAL = ROUND ( #NP# , - #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '3637383931373332312E3334353637380A350A'
    setup.verifyHQCEntryExists()

    # add entry11
    defs.qry = """select * from F03
where rndval = ROUND(678917321.345678, 1);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ROUND016')
    defs.hkey = """SELECT * FROM F03 WHERE RNDVAL = ROUND ( #NP# , #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '3637383931373332312E3334353637380A310A'
    setup.verifyHQCEntryExists()

    # add entry12
    defs.qry = """select * from F03
where rndval = ROUND(-76543.876543, -4);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ROUND017')
    defs.hkey = ("""SELECT * FROM F03""" +
                 """ WHERE RNDVAL = ROUND ( - #NP# , - #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '37363534332E3837363534330A340A'
    setup.verifyHQCEntryExists()

    # add entry13
    defs.qry = """select * from F03 where rndval = ROUND(-76543.876543, 2);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ROUND018')
    defs.hkey = ("""SELECT * FROM F03""" +
                 """ WHERE RNDVAL = ROUND ( - #NP# , #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '37363534332E3837363534330A320A'
    setup.verifyHQCEntryExists()

    # add entry14
    defs.qry = """select * from F03
where rndval = ROUND(999.123 * 999.123, -3);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ROUND019')
    defs.hkey = ("""SELECT * FROM F03""" +
                 """ WHERE RNDVAL = ROUND ( #NP# * #NP# , - #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 3
    defs.npliterals = '3939392E3132330A3939392E3132330A330A'
    setup.verifyHQCEntryExists()

    # add entry15
    defs.qry = """select * from F03
where rndval = ROUND(999.123E+3 * 999.123E+3, -3);"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ROUND020')
    defs.hkey = ("""SELECT * FROM F03""" +
                 """ WHERE RNDVAL = ROUND ( #NP# * #NP# , - #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 3
    defs.npliterals = '3939392E313233452B330A3939392E313233452B330A330A'
    setup.verifyHQCEntryExists()

    # add entry16
    defs.qry = """select * from F02
where ROUND(colrval, colrnd) = 9200000000000000000;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ROUND021')
    defs.hkey = ("""SELECT * FROM F02""" +
                 """ WHERE ROUND ( COLRVAL , COLRND ) = #NP# ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '393230303030303030303030303030303030300A'
    setup.verifyHQCEntryExists()

    # add entry17
    defs.qry = """select * from F02
where ROUND(colrval, colrnd) = -9200000000000000000;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ROUND022')
    defs.hkey = ("""SELECT * FROM F02""" +
                 """ WHERE ROUND ( COLRVAL , COLRND ) = - #NP# ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '393230303030303030303030303030303030300A'
    setup.verifyHQCEntryExists()

    # add entry18
    defs.qry = """select * from F02
where ROUND(colrval, colrnd) = 9.223372036854775800;"""
    output = _dci.cmdexec(defs.prepXX + defs.qry)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'ROUND023')
    defs.hkey = ("""SELECT * FROM F02""" +
                 """ WHERE ROUND ( COLRVAL , COLRND ) = #NP# ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '392E3232333337323033363835343737353830300A'
    setup.verifyHQCEntryExists()

    output = _dci.cmdexec("""drop table F02;""")
    _dci.expect_complete_msg(output)
    output = _dci.cmdexec("""drop table F03;""")
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)


def test_sin(desc="""sin()"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: sin()"""

    ### SQL function: SIN()
    ### in result-set, constant is positive: cacheable & parameterized
    ### in result-set, constant is negative: Not cacheable
    ### in where-clause: HQC cacheable, not parameterized

    setup.resetHQC()
    ### =====================================================
    # in result-set, constant is negative - not cacheable

    output = _dci.cmdexec("""select SIN(-0.3491) from F00;""")
    _dci.expect_file(output, defs.expfile, 'SIN001')
    output = _dci.cmdexec("""select SIN(-34.91E-2) from F00;""")
    _dci.expect_file(output, defs.expfile, 'SIN002')
    output = _dci.cmdexec("""select SIN(34.91 * -0.01) from F00;""")
    _dci.expect_file(output, defs.expfile, 'SIN003')
    output = _dci.cmdexec("""select SIN(-colnum) from F00;""")
    _dci.expect_file(output, defs.expfile, 'SIN004')

    setup.verifyHQCempty()

    ### =====================================================
    ### in result-set, constant is positive: cacheable & parameterized

    # add entry1
    output = _dci.cmdexec("""select SIN(colnum) from F00;""")
    _dci.expect_file(output, defs.expfile, 'SIN005')
    defs.hkey = """SELECT SIN ( COLNUM ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry2
    output = _dci.cmdexec("""select SIN(0.3491) from F00;""")
    _dci.expect_file(output, defs.expfile, 'SIN006')
    defs.hkey = """SELECT SIN ( #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '302E333439310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry2
    output = _dci.cmdexec("""select SIN(0.9397) from F00;""")
    _dci.expect_file(output, defs.expfile, 'SIN007')
    defs.hkey = """SELECT SIN ( #NP# ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '302E333439310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry2
    output = _dci.cmdexec("""select SIN(1) from F00;""")
    _dci.expect_file(output, defs.expfile, 'SIN008')
    defs.hkey = """SELECT SIN ( #NP# ) FROM F00 ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '302E333439310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry3
    output = _dci.cmdexec("""select SIN(0.03491E+1) from F00;""")
    _dci.expect_file(output, defs.expfile, 'SIN009')
    defs.hkey = """SELECT SIN ( #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '302E3033343931452B310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry3
    output = _dci.cmdexec("""select SIN(3.491E-1) from F00;""")
    _dci.expect_file(output, defs.expfile, 'SIN010')
    defs.hkey = """SELECT SIN ( #NP# ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '302E3033343931452B310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry4
    output = _dci.cmdexec("""select SIN(34.91 * 0.01) from F00;""")
    _dci.expect_file(output, defs.expfile, 'SIN011')
    defs.hkey = """SELECT SIN ( #NP# * #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 2
    defs.pliterals = '33342E39310A302E30310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # entry1
    output = _dci.cmdexec("""select SIN(colnum) from F00;""")
    _dci.expect_file(output, defs.expfile, 'SIN012')
    defs.hkey = """SELECT SIN ( COLNUM ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry2
    output = _dci.cmdexec("""select SIN(0) from F00;""")
    _dci.expect_file(output, defs.expfile, 'SIN013')
    defs.hkey = """SELECT SIN ( #NP# ) FROM F00 ;"""
    defs.num_hits = 3
    defs.num_pliterals = 1
    defs.pliterals = '302E333439310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry4
    output = _dci.cmdexec("""select SIN(93.97 * 0.01) from F00;""")
    _dci.expect_file(output, defs.expfile, 'SIN014')
    defs.hkey = """SELECT SIN ( #NP# * #NP# ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 2
    defs.pliterals = '33342E39310A302E30310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry2
    output = _dci.cmdexec("""select SIN(0.681) from F00;""")
    _dci.expect_file(output, defs.expfile, 'SIN015')
    defs.hkey = """SELECT SIN ( #NP# ) FROM F00 ;"""
    defs.num_hits = 4
    defs.num_pliterals = 1
    defs.pliterals = '302E333439310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry3
    output = _dci.cmdexec("""select SIN(9.397E-1) from F00;""")
    _dci.expect_file(output, defs.expfile, 'SIN016')
    defs.hkey = """SELECT SIN ( #NP# ) FROM F00 ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '302E3033343931452B310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    output = _dci.cmdexec("""drop table F02;""")
    output = _dci.cmdexec("""create table F02
(val numeric(5,4), sinval numeric(18,17));""")
    _dci.expect_complete_msg(output)
    output = _dci.cmdexec("""insert into F02 values
(0.3491, 0.34205223325441986),
(-0.3491, -0.34205223325441986);""")
    _dci.expect_inserted_msg(output, '2')
    output = _dci.cmdexec("""select * from F02 order by 1;""")
    _dci.expect_file(output, defs.expfile, 'SIN017')

    setup.resetHQC()

    # add entry1
    output = _dci.cmdexec(defs.prepXX + """select * from F02
where sinval = SIN(0.3491);""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SIN018')
    defs.hkey = """SELECT * FROM F02 WHERE SINVAL = SIN ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E333439310A'
    setup.verifyHQCEntryExists()

    # add entry2
    output = _dci.cmdexec(defs.prepXX + """select * from F02
where sinval = SIN(-0.3491);""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SIN019')
    defs.hkey = """SELECT * FROM F02 WHERE SINVAL = SIN ( - #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E333439310A'
    setup.verifyHQCEntryExists()

    # add entry3
    output = _dci.cmdexec(defs.prepXX + """select * from F02
where sinval = SIN(3.491E-1);""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SIN020')
    defs.hkey = """SELECT * FROM F02 WHERE SINVAL = SIN ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '332E343931452D310A'
    setup.verifyHQCEntryExists()

    # add entry4
    output = _dci.cmdexec(defs.prepXX + """select * from F02
where sinval = SIN(0.03491E+1);""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SIN021')
    defs.hkey = """SELECT * FROM F02 WHERE SINVAL = SIN ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E3033343931452B310A'
    setup.verifyHQCEntryExists()

    # add entry5
    output = _dci.cmdexec(defs.prepXX + """select * from F02
where sinval = SIN(34.91 / 100);""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SIN022')
    defs.hkey = """SELECT * FROM F02 WHERE SINVAL = SIN ( #NP# / #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '33342E39310A3130300A'
    setup.verifyHQCEntryExists()

    # add entry6, constant changed
    output = _dci.cmdexec("""select * from F02
where sinval = SIN(-0.6147);""")
    _dci.expect_file(output, defs.expfile, 'SIN023')
    defs.hkey = """SELECT * FROM F02 WHERE SINVAL = SIN ( - #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E333439310A'
    setup.verifyHQCEntryExists()

    # add entry7, constant changed
    output = _dci.cmdexec("""select * from F02
where sinval = SIN(0.06147E+1);""")
    _dci.expect_file(output, defs.expfile, 'SIN024')
    defs.hkey = """SELECT * FROM F02 WHERE SINVAL = SIN ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E3033343931452B310A'
    setup.verifyHQCEntryExists()

    # add entry8, constant changed
    output = _dci.cmdexec("""select * from F02
where sinval = SIN(61.47 / 100);""")
    _dci.expect_file(output, defs.expfile, 'SIN025')
    defs.hkey = """SELECT * FROM F02 WHERE SINVAL = SIN ( #NP# / #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '33342E39310A3130300A'
    setup.verifyHQCEntryExists()

    # increase hits, entry1
    output = _dci.cmdexec(defs.prepXX + """select * from F02
where sinval = SIN(0.3491);""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SIN018')
    defs.hkey = """SELECT * FROM F02 WHERE SINVAL = SIN ( #NP# ) ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E333439310A'
    setup.verifyHQCEntryExists()

    # increase hits, entry2
    output = _dci.cmdexec(defs.prepXX + """select * from F02
where sinval = SIN(-0.3491);""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SIN019')
    defs.hkey = """SELECT * FROM F02 WHERE SINVAL = SIN ( - #NP# ) ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E333439310A'
    setup.verifyHQCEntryExists()

    # increase hits, entry3
    output = _dci.cmdexec(defs.prepXX + """select * from F02
where sinval = SIN(3.491E-1);""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SIN020')
    defs.hkey = """SELECT * FROM F02 WHERE SINVAL = SIN ( #NP# ) ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '332E343931452D310A'
    setup.verifyHQCEntryExists()

    # increase hits, entry4
    output = _dci.cmdexec(defs.prepXX + """select * from F02
where sinval = SIN(0.03491E+1);""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SIN021')
    defs.hkey = """SELECT * FROM F02 WHERE SINVAL = SIN ( #NP# ) ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E3033343931452B310A'
    setup.verifyHQCEntryExists()

    # increase hits, entry5
    output = _dci.cmdexec(defs.prepXX + """select * from F02
where sinval = SIN(34.91 / 100);""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SIN022')
    defs.hkey = """SELECT * FROM F02 WHERE SINVAL = SIN ( #NP# / #NP# ) ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '33342E39310A3130300A'
    setup.verifyHQCEntryExists()

    output = _dci.cmdexec("""drop table F02;""")
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)


def test_sinh(desc="""sinh()"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: sinh()"""

    ### SQL function: SINH()
    ### in result-set, constant is positive: cacheable & parameterized
    ### in result-set, constant is negative: Not cacheable
    ### in where-clause: HQC cacheable, not parameterized

    setup.resetHQC()
    ### =====================================================
    # in result-set, constant is negative - not cacheable

    output = _dci.cmdexec("""select SINH(-1.2345) from F00;""")
    _dci.expect_file(output, defs.expfile, 'SINH001')
    output = _dci.cmdexec("""select SINH(-0.0125E-2) from F00;""")
    _dci.expect_file(output, defs.expfile, 'SINH002')
    # oddball case - SQC cached, HQC cached, not parameterized
    # moved case below
    #output = _dci.cmdexec("""select SINH(-0.000125 * 10000) from F00;""")
    #_dci.expect_file(output, defs.expfile, 'SINH003')
    output = _dci.cmdexec("""select SINH(-colnum) from F00;""")
    _dci.expect_file(output, defs.expfile, 'SINH004')
    output = _dci.cmdexec("""select SINH(12345/-10000) from F00;""")
    _dci.expect_file(output, defs.expfile, 'SINH005')
    output = _dci.cmdexec("""select SINH(-12345/10000) from F00;""")
    _dci.expect_file(output, defs.expfile, 'SINH005')
    output = _dci.cmdexec("""select SINH(-12345/-10000) from F00;""")
    _dci.expect_file(output, defs.expfile, 'SINH005a')

    setup.verifyHQCempty()

    ### =====================================================
    ### in result-set, constant is positive: cacheable & parameterized

    # add entry1
    output = _dci.cmdexec(defs.prepXX + """select SINH(colnum) from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SINH006')
    defs.hkey = """SELECT SINH ( COLNUM ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry2
    output = _dci.cmdexec(defs.prepXX + """select SINH(1.2345) from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SINH007')
    defs.hkey = """SELECT SINH ( #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '312E323334350A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry2
    output = _dci.cmdexec(defs.prepXX + """select SINH(0.9397) from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SINH008')
    defs.hkey = """SELECT SINH ( #NP# ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '312E323334350A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry2
    output = _dci.cmdexec(defs.prepXX + """select SINH(1) from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SINH009')
    defs.hkey = """SELECT SINH ( #NP# ) FROM F00 ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '312E323334350A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry3
    output = _dci.cmdexec(defs.prepXX + """select SINH(0.09397E+1)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SINH010')
    defs.hkey = """SELECT SINH ( #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '302E3039333937452B310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry3
    output = _dci.cmdexec(defs.prepXX + """select SINH(9.397E-1) from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SINH011')
    defs.hkey = """SELECT SINH ( #NP# ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '302E3039333937452B310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry3
    output = _dci.cmdexec(defs.prepXX + """select SINH(0.012345E+2)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SINH012')
    defs.hkey = """SELECT SINH ( #NP# ) FROM F00 ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '302E3039333937452B310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # con't oddball case - SQC cached, HQC cached, not parameterized
    output = _dci.cmdexec(defs.prepXX + """select SINH(-0.000125 * 10000)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SINH003')
    defs.hkey = """SELECT SINH ( - #NP# * #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '302E3030303132350A31303030300A'
    setup.verifyHQCEntryExists()
    # this will be a new entry, since HQC for prior query is not parameterized
    output = _dci.cmdexec(defs.prepXX + """select SINH(-0.000222 * 20000)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SINH003a')
    defs.hkey = """SELECT SINH ( - #NP# * #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '302E3030303232320A32303030300A'
    setup.verifyHQCEntryExists()
    # verify that hits increased for non-parameterized entry
    output = _dci.cmdexec(defs.prepXX + """select SINH(-0.000125 * 10000)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SINH003')
    defs.hkey = """SELECT SINH ( - #NP# * #NP# ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '302E3030303132350A31303030300A'
    setup.verifyHQCEntryExists()

    output = _dci.cmdexec("""drop table F02;""")
    output = _dci.cmdexec("""create table F02
(val numeric(8,7), sinhval numeric(18,17));""")
    _dci.expect_complete_msg(output)
    output = _dci.cmdexec("""insert into F02(val) values
(0.7475), (-0.7475), (1.5432475), (-1.5432475);""")
    _dci.expect_inserted_msg(output, '4')
    output = _dci.cmdexec("""update F02 set sinhval = SINH(val);""")
    _dci.expect_updated_msg(output, '4')
    defs.hkey = """UPDATE F02 SET SINHVAL = SINH ( VAL ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""select * from F02 order by 1;""")
    _dci.expect_file(output, defs.expfile, 'SINH013')

    ### =====================================================
    ### in where-clause: cacheable, not parameterized
    setup.resetHQC()
    # add entry1
    output = _dci.cmdexec(defs.prepXX + """select * from F02
where sinhval = SINH(val);""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SINH014')
    defs.hkey = """SELECT * FROM F02 WHERE SINHVAL = SINH ( VAL ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry2
    output = _dci.cmdexec(defs.prepXX + """select * from F02
where sinhval = SINH(0.7475);""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SINH015')
    defs.hkey = """SELECT * FROM F02 WHERE SINHVAL = SINH ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E373437350A'
    setup.verifyHQCEntryExists()

    # add entry3
    output = _dci.cmdexec(defs.prepXX + """select * from F02
where sinhval = SINH(-0.7475);""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SINH016')
    defs.hkey = """SELECT * FROM F02 WHERE SINHVAL = SINH ( - #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E373437350A'
    setup.verifyHQCEntryExists()

    # add entry4
    output = _dci.cmdexec(defs.prepXX + """select * from F02
where sinhval = SINH(74.75E-2);""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SINH017')
    defs.hkey = """SELECT * FROM F02 WHERE SINHVAL = SINH ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '37342E3735452D320A'
    setup.verifyHQCEntryExists()

    # increase hits, entry4
    output = _dci.cmdexec(defs.prepXX + """select * from F02
where sinhval = SINH(0.0015E+3);""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SINH018')
    defs.hkey = """SELECT * FROM F02 WHERE SINHVAL = SINH ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '37342E3735452D320A'
    setup.verifyHQCEntryExists()

    # add entry5
    output = _dci.cmdexec(defs.prepXX + """select * from F02
where sinhval = SINH(1.0 + 0.5400075 + 0.00324);""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SINH019')
    defs.hkey = ("""SELECT * FROM F02""" +
                 """ WHERE SINHVAL = SINH ( #NP# + #NP# + #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 3
    defs.npliterals = '312E300A302E353430303037350A302E30303332340A'
    setup.verifyHQCEntryExists()

    # add entry6
    output = _dci.cmdexec(defs.prepXX + """select * from F02
where SINH(val) = -0.81908259009369152;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SINH020')
    defs.hkey = """SELECT * FROM F02 WHERE SINH ( VAL ) = - #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E38313930383235393030393336393135320A'
    setup.verifyHQCEntryExists()

    # add entry7
    output = _dci.cmdexec(defs.prepXX + """select * from F02
where SINH(val) = 2.23303856174339712;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SINH021')
    defs.hkey = """SELECT * FROM F02 WHERE SINH ( VAL ) = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '322E32333330333835363137343333393731320A'
    setup.verifyHQCEntryExists()

    # add entry8
    output = _dci.cmdexec(defs.prepXX + """select * from F02
where sinhval = SINH(0.4444);""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SINH022')
    defs.hkey = """SELECT * FROM F02 WHERE SINHVAL = SINH ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E343434340A'
    setup.verifyHQCEntryExists()

    # increase hits,entry2
    output = _dci.cmdexec(defs.prepXX + """select * from F02
where sinhval = SINH(0.7475);""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SINH015')
    defs.hkey = """SELECT * FROM F02 WHERE SINHVAL = SINH ( #NP# ) ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E373437350A'
    setup.verifyHQCEntryExists()

    # add entry9
    output = _dci.cmdexec(defs.prepXX + """select * from F02
where sinhval = SINH(0.6768);""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SINH023')
    defs.hkey = """SELECT * FROM F02 WHERE SINHVAL = SINH ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E363736380A'
    setup.verifyHQCEntryExists()

    # increase hits, add entry3
    output = _dci.cmdexec(defs.prepXX + """select * from F02
where sinhval = SINH(-0.7475);""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SINH016')
    defs.hkey = """SELECT * FROM F02 WHERE SINHVAL = SINH ( - #NP# ) ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E373437350A'
    setup.verifyHQCEntryExists()

    # increase hits, entry7
    output = _dci.cmdexec(defs.prepXX + """select * from F02
where SINH(val) = 2.23303856174339712;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SINH021')
    defs.hkey = """SELECT * FROM F02 WHERE SINH ( VAL ) = #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '322E32333330333835363137343333393731320A'
    setup.verifyHQCEntryExists()

    # increase hits, entry8
    output = _dci.cmdexec(defs.prepXX + """select * from F02
where sinhval = SINH(0.4444);""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SINH022')
    defs.hkey = """SELECT * FROM F02 WHERE SINHVAL = SINH ( #NP# ) ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E343434340A'
    setup.verifyHQCEntryExists()

    # add entry10
    output = _dci.cmdexec(defs.prepXX + """select * from F02
where SINH(val) = -2.23303856174339712;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SINH023')
    defs.hkey = """SELECT * FROM F02 WHERE SINH ( VAL ) = - #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '322E32333330333835363137343333393731320A'
    setup.verifyHQCEntryExists()

    output = _dci.cmdexec("""drop table F02;""")
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)


def test_sqrt(desc="""sqrt()"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: sqrt()"""

    ### SQL function: SQRT()
    ### in result-set, constant is positive: cacheable & parameterized
    ### in result-set, constant is negative: Not cacheable
    ### in where-clause: HQC cacheable, not parameterized

    setup.resetHQC()

    # add entry1
    stmt = defs.prepXX + """select SQRT(25) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '5.0')
    defs.hkey = """SELECT SQRT ( #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '32350A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry2
    stmt = defs.prepXX + """select SQRT(144) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '12.0')
    defs.hkey = """SELECT SQRT ( #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '3134340A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry3
    stmt = defs.prepXX + """select SQRT(14641) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '121.0')
    defs.hkey = """SELECT SQRT ( #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '31343634310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry4
    stmt = defs.prepXX + """select SQRT(0.1296) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '0.36')
    defs.hkey = """SELECT SQRT ( #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '302E313239360A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry5
    stmt = defs.prepXX + """select SQRT(0.0081E4) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '9.0')
    defs.hkey = """SELECT SQRT ( #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '302E3030383145340A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry3
    stmt = defs.prepXX + """select SQRT(14641) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '121.0')
    defs.hkey = """SELECT SQRT ( #NP# ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '31343634310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry4
    stmt = defs.prepXX + """select SQRT(0.1296) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '0.36')
    defs.hkey = """SELECT SQRT ( #NP# ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '302E313239360A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry5
    stmt = defs.prepXX + """select SQRT(0.0081E4) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '9.0')
    defs.hkey = """SELECT SQRT ( #NP# ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '302E3030383145340A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry6
    stmt = defs.prepXX + """select SQRT(8100E-2) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '9.0')
    defs.hkey = """SELECT SQRT ( #NP# ) FROM F00 ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '302E3030383145340A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry7
    stmt = defs.prepXX + """select * from F01
where colnum = SQRT(0.39287824);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SQRT007')
    defs.hkey = """SELECT * FROM F01 WHERE COLNUM = SQRT ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E33393238373832340A'
    setup.verifyHQCEntryExists()

    #add entry8
    stmt = defs.prepXX + """select * from F01
where colnum = SQRT(0.88303609);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SQRT008')
    defs.hkey = """SELECT * FROM F01 WHERE COLNUM = SQRT ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E38383330333630390A'
    setup.verifyHQCEntryExists()

    # increase hits, entry7
    stmt = defs.prepXX + """select * from F01
where colnum = SQRT(0.39287824);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SQRT007')
    defs.hkey = """SELECT * FROM F01 WHERE COLNUM = SQRT ( #NP# ) ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E33393238373832340A'
    setup.verifyHQCEntryExists()

    _testmgr.testcase_end(desc)


def test_tanh(desc="""tanh()"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: tanh()"""

    ### SQL function: TANH()
    ### in result-set, constant is positive: cacheable & parameterized
    ### in result-set, constant is negative: Not cacheable
    ### in where-clause: HQC cacheable, not parameterized

    setup.resetHQC()
    ### =====================================================
    # in result-set, constant is negative - not cacheable

    output = _dci.cmdexec("""select TANH(-1.2345) from F00;""")
    _dci.expect_file(output, defs.expfile, 'TANH001')
    output = _dci.cmdexec("""select TANH(-0.0125E-2) from F00;""")
    _dci.expect_file(output, defs.expfile, 'TANH002')
    # oddball case - SQC cached, HQC cacheable, not parameterized
    #output = _dci.cmdexec("""select TANH(-0.000125 * 10000) from F00;""")
    #_dci.expect_file(output, defs.expfile, 'TANH003')
    # oddball case - SQC cached, HQC cacheable, not parameterized
    #output = _dci.cmdexec("""select TANH(0.000125 * -10000) from F00;""")
    #_dci.expect_file(output, defs.expfile, 'TANH003')
    output = _dci.cmdexec("""select TANH(-0.000125 * -10000) from F00;""")
    _dci.expect_file(output, defs.expfile, 'TANH003a')
    output = _dci.cmdexec("""select TANH(-colnum) from F00;""")
    _dci.expect_file(output, defs.expfile, 'TANH004')
    output = _dci.cmdexec("""select TANH(12345/-10000) from F00;""")
    _dci.expect_file(output, defs.expfile, 'TANH005')
    output = _dci.cmdexec("""select TANH(-12345/10000) from F00;""")
    _dci.expect_file(output, defs.expfile, 'TANH005')
    output = _dci.cmdexec("""select TANH(-12345/-10000) from F00;""")
    _dci.expect_file(output, defs.expfile, 'TANH005a')
    # oddball case - SQC cached, HQC cacheable, not parameterized
    #output = _dci.cmdexec("""select TANH((125 / 100) - 0.27) from F00;""")
    #_dci.expect_file(output, defs.expfile, 'TANH006')
    output = _dci.cmdexec("""select TANH((125 / 100) + -0.27) from F00;""")
    _dci.expect_file(output, defs.expfile, 'TANH006')

    setup.verifyHQCempty()

    ### =====================================================
    ### in result-set, constant is positive: cacheable & parameterized

    # add entry1
    output = _dci.cmdexec(defs.prepXX + """select TANH(colnum) from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TANH007')
    defs.hkey = """SELECT TANH ( COLNUM ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry1
    output = _dci.cmdexec(defs.prepXX + """select TANH(colnum) from F00;""")
    _dci.expect_prepared_msg(output)
    defs.hkey = """SELECT TANH ( COLNUM ) FROM F00 ;"""
    defs.num_hits = 1
    setup.verifyHQCEntryExists()

    # add entry2
    output = _dci.cmdexec(defs.prepXX + """select TANH(1.2345) from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TANH008')
    defs.hkey = """SELECT TANH ( #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '312E323334350A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry2
    output = _dci.cmdexec(defs.prepXX + """select TANH(0.9397) from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TANH009')
    defs.hkey = """SELECT TANH ( #NP# ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '312E323334350A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry2
    output = _dci.cmdexec(defs.prepXX + """select TANH(1) from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TANH010')
    defs.hkey = """SELECT TANH ( #NP# ) FROM F00 ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '312E323334350A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry3
    output = _dci.cmdexec(defs.prepXX + """select TANH(0.09397E+1)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TANH011')
    defs.hkey = """SELECT TANH ( #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '302E3039333937452B310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry3
    output = _dci.cmdexec(defs.prepXX + """select TANH(9.397E-1) from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TANH012')
    defs.hkey = """SELECT TANH ( #NP# ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '302E3039333937452B310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry3
    output = _dci.cmdexec(defs.prepXX + """select TANH(0.012345E+2)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TANH013')
    defs.hkey = """SELECT TANH ( #NP# ) FROM F00 ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '302E3039333937452B310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # con't oddball case - SQC cached, HQC cacheable, not parameterized
    # add entry4
    output = _dci.cmdexec(defs.prepXX + """select TANH(-0.000125 * 10000)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TANH003')
    defs.hkey = """SELECT TANH ( - #NP# * #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '302E3030303132350A31303030300A'
    setup.verifyHQCEntryExists()
    # con't oddball case - SQC cached, HQC cacheable, not parameterized
    # add entry5
    output = _dci.cmdexec(defs.prepXX + """select TANH(0.000125 * -10000)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TANH003')
    defs.hkey = """SELECT TANH ( #NP# * - #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '302E3030303132350A31303030300A'
    setup.verifyHQCEntryExists()
    # increase hits, entry4
    output = _dci.cmdexec(defs.prepXX + """select TANH(-0.000125 * 10000)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TANH003')
    defs.hkey = """SELECT TANH ( - #NP# * #NP# ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '302E3030303132350A31303030300A'
    setup.verifyHQCEntryExists()
    # increase hits, entry5
    output = _dci.cmdexec(defs.prepXX + """select TANH(0.000125 * -10000)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TANH003')
    defs.hkey = """SELECT TANH ( #NP# * - #NP# ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '302E3030303132350A31303030300A'
    setup.verifyHQCEntryExists()
    # literals different, add entry6
    output = _dci.cmdexec(defs.prepXX + """select TANH(-0.000111 * 10000)
from F00;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TANH003b')
    defs.hkey = """SELECT TANH ( - #NP# * #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '302E3030303131310A31303030300A'
    setup.verifyHQCEntryExists()

    output = _dci.cmdexec("""drop table F02;""")
    output = _dci.cmdexec("""create table F02
(val numeric(8,7), tanhval numeric(18,17));""")
    _dci.expect_complete_msg(output)
    output = _dci.cmdexec("""insert into F02(val) values
(0.7475), (-0.7475), (1.5432475), (-1.5432475);""")
    _dci.expect_inserted_msg(output, '4')
    output = _dci.cmdexec("""update F02 set tanhval = TANH(val);""")
    _dci.expect_updated_msg(output, '4')
    defs.hkey = """UPDATE F02 SET TANHVAL = TANH ( VAL ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""select * from F02 order by 1;""")
    _dci.expect_file(output, defs.expfile, 'TANH014')

    ### =====================================================
    ### in where-clause: cacheable, not parameterized
    setup.resetHQC()
    # add entry1
    output = _dci.cmdexec(defs.prepXX + """select * from F02
where tanhval = TANH(val);""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TANH015')
    defs.hkey = """SELECT * FROM F02 WHERE TANHVAL = TANH ( VAL ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry2
    output = _dci.cmdexec(defs.prepXX + """select * from F02
where tanhval = TANH(0.7475);""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TANH016')
    defs.hkey = """SELECT * FROM F02 WHERE TANHVAL = TANH ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E373437350A'
    setup.verifyHQCEntryExists()

    # add entry3
    output = _dci.cmdexec(defs.prepXX + """select * from F02
where tanhval = TANH(-0.7475);""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TANH017')
    defs.hkey = """SELECT * FROM F02 WHERE TANHVAL = TANH ( - #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E373437350A'
    setup.verifyHQCEntryExists()

    # add entry4
    output = _dci.cmdexec(defs.prepXX + """select * from F02
where tanhval = TANH(74.75E-2);""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TANH018')
    defs.hkey = """SELECT * FROM F02 WHERE TANHVAL = TANH ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '37342E3735452D320A'
    setup.verifyHQCEntryExists()

    # increase hits, entry4
    output = _dci.cmdexec(defs.prepXX + """select * from F02
where tanhval = TANH(0.0015E+3);""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TANH019')
    defs.hkey = """SELECT * FROM F02 WHERE TANHVAL = TANH ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '37342E3735452D320A'
    setup.verifyHQCEntryExists()

    # add entry5
    output = _dci.cmdexec(defs.prepXX + """select * from F02
where tanhval = TANH(1.0 + 0.5400075 + 0.00324);""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TANH020')
    defs.hkey = ("""SELECT * FROM F02""" +
                 """ WHERE TANHVAL = TANH ( #NP# + #NP# + #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 3
    defs.npliterals = '312E300A302E353430303037350A302E30303332340A'
    setup.verifyHQCEntryExists()

    # add entry6
    output = _dci.cmdexec(defs.prepXX + """select * from F02
where TANH(val) = -0.81908259009369152;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TANH021')
    defs.hkey = """SELECT * FROM F02 WHERE TANH ( VAL ) = - #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E38313930383235393030393336393135320A'
    setup.verifyHQCEntryExists()

    # add entry7
    output = _dci.cmdexec(defs.prepXX + """select * from F02
where TANH(val) = 2.23303856174339712;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TANH022')
    defs.hkey = """SELECT * FROM F02 WHERE TANH ( VAL ) = #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '322E32333330333835363137343333393731320A'
    setup.verifyHQCEntryExists()

    # add entry8
    output = _dci.cmdexec(defs.prepXX + """select * from F02
where tanhval = TANH(0.4444);""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TANH023')
    defs.hkey = """SELECT * FROM F02 WHERE TANHVAL = TANH ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E343434340A'
    setup.verifyHQCEntryExists()

    # increase hits,entry2
    output = _dci.cmdexec(defs.prepXX + """select * from F02
where tanhval = TANH(0.7475);""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TANH016')
    defs.hkey = """SELECT * FROM F02 WHERE TANHVAL = TANH ( #NP# ) ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E373437350A'
    setup.verifyHQCEntryExists()

    # add entry9
    output = _dci.cmdexec(defs.prepXX + """select * from F02
where tanhval = TANH(0.6768);""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TANH024')
    defs.hkey = """SELECT * FROM F02 WHERE TANHVAL = TANH ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E363736380A'
    setup.verifyHQCEntryExists()

    # increase hits, add entry3
    output = _dci.cmdexec(defs.prepXX + """select * from F02
where tanhval = TANH(-0.7475);""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TANH017')
    defs.hkey = """SELECT * FROM F02 WHERE TANHVAL = TANH ( - #NP# ) ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E373437350A'
    setup.verifyHQCEntryExists()

    # increase hits, entry7
    output = _dci.cmdexec(defs.prepXX + """select * from F02
where TANH(val) = 2.23303856174339712;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TANH022')
    defs.hkey = """SELECT * FROM F02 WHERE TANH ( VAL ) = #NP# ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '322E32333330333835363137343333393731320A'
    setup.verifyHQCEntryExists()

    # increase hits, entry8
    output = _dci.cmdexec(defs.prepXX + """select * from F02
where tanhval = TANH(0.4444);""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TANH023')
    defs.hkey = """SELECT * FROM F02 WHERE TANHVAL = TANH ( #NP# ) ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E343434340A'
    setup.verifyHQCEntryExists()

    # add entry10
    output = _dci.cmdexec(defs.prepXX + """select * from F02
where TANH(val) = -2.23303856174339712;""")
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TANH024')
    defs.hkey = """SELECT * FROM F02 WHERE TANH ( VAL ) = - #NP# ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '322E32333330333835363137343333393731320A'
    setup.verifyHQCEntryExists()

    output = _dci.cmdexec("""drop table F02;""")
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)
