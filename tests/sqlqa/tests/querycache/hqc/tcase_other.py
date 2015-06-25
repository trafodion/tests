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

#authname, bitand, case, cast, coalesce, converttohex, current_user,
#decode, explain, isnull, nullif, nvl, user

    output = _dci.cmdexec("""drop table F00 cascade;""")
    output = _dci.cmdexec("""drop table F01 cascade;""")
    output = _dci.cmdexec("""drop table F02 cascade;""")
    output = _dci.cmdexec("""drop table TBL1R cascade;""")

    stmt = """create table TBL1R(colts timestamp);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    setup.resetHQC()
    stmt = """insert into TBL1R values (current_timestamp);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, '1')
    setup.verifyHQCempty()

    stmt = """create table F00(colint int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """upsert using load into F00 select (c1 + c2 * 10  - 25)
from (values(1)) t
transpose 0,1,2,3,4,5,6,7,8,9 as c1
transpose 0,1,2,3,4 as c2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table F01(colint int, colnum numeric(9,3),
colreal real, colchr char(25), colvchr varchar(25), coldate date);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into F01 values
(100, 1.11111E3, 1.11E4, 'one hundred', 'one hundred one', date '1996-03-27'),
(200, 2.22222E3, 2.22E4, 'two hundred', 'two hundred two', date '1887-12-28'),
(300, 3.33333E3, 3.33E4, 'three hundred', 'three hundred three',
date '2001-06-04'),
(400, 4.44444E3, 4.44E4, 'four hundred', 'four hundred four',
date '2015-02-15'),
(500, 5.55555E3, 5.55E4, 'five hundred', 'five hundred five',
date '1975-11-09'),
(600, 6.66666E3, 6.66E4, 'six hundred', 'six hundred six',
date '1984-01-31'),
(700, 7.77777E3, 7.77E4, 'seven hundred', 'seven hundred seven',
date '2000-01-01'),
(800, 8.88888E3, 8.88E4, 'eight hundred', 'eight hundred eight',
date '1967-11-27'),
(900, 9.99999E3, 9.99E4, 'nine hundred', 'nine hundred nine',
date '1775-04-29'),
(1000, 10.10101E3, 10.1010E4, 'one thousand', 'one thousand one',
date '2021-10-31');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, '10')

    stmt = """create table F02(colint int, coldate date,
colchar char(10), colnum numeric(7,3), colintvl interval day(18));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into F02 values
(1, date'2014-08-02', '2015-09-03', 111.222, interval '8' day),
(2, date'1970-09-14', '1971-10-15', 3.33344E2, interval '33' day);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, '2')


def test_bitand(desc="""bitand"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: bitand"""

    setup.resetHQC()

    # function: BITAND
    # HQC CACHEABLE, NOT PARAMETERIZED

    stmt = defs.prepXX + """select BITAND(-1, 3) from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '3')

    stmt = defs.prepXX + """select BITAND(1, -3) from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '1')

    stmt = defs.prepXX + """select BITAND(-1, -3) from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '-3')

    setup.verifyHQCempty()

    stmt = defs.prepXX + """select BITAND(1, 3) from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '1')
    defs.hkey = """SELECT BITAND ( #NP# , #NP# ) FROM TBL1R ;"""
    defs.num_hits = 0
    defs.num_pliterals = 2
    defs.pliterals = '310A330A'

    stmt = defs.prepXX + """select BITAND(9, 8) from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '8')
    defs.hkey = """SELECT BITAND ( #NP# , #NP# ) FROM TBL1R ;"""
    defs.num_hits = 1
    defs.num_pliterals = 2
    defs.pliterals = '310A330A'

    stmt = defs.prepXX + """select BITAND(99, 11) from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '3')
    defs.hkey = """SELECT BITAND ( #NP# , #NP# ) FROM TBL1R ;"""
    defs.num_hits = 0
    defs.num_pliterals = 2
    defs.pliterals = '39390A31310A'

    stmt = defs.prepXX + """select BITAND(8, 40) from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '8')
    defs.hkey = """SELECT BITAND ( #NP# , #NP# ) FROM TBL1R ;"""
    defs.num_hits = 1
    defs.num_pliterals = 2
    defs.pliterals = '39390A31310A'

    stmt = defs.prepXX + """select BITAND(7, 2) from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2')
    defs.hkey = """SELECT BITAND ( #NP# , #NP# ) FROM TBL1R ;"""
    defs.num_hits = 2
    defs.num_pliterals = 2
    defs.pliterals = '310A330A'

    stmt = defs.prepXX + """select * from F00 where colint = BITAND(8, 9);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '8')

    stmt = defs.prepXX + """select * from F00 where colint = BITAND(-8, 9);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '8')

    stmt = defs.prepXX + """select * from F00 where colint = BITAND(8, -9);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '0')

    stmt = defs.prepXX + """select * from F00 where colint = BITAND(-8, -9);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '-16')

    stmt = defs.prepXX + """select * from F00 where colint = BITAND(8, 9);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '8')
    defs.hkey = """SELECT * FROM F00 WHERE COLINT = BITAND ( #NP# , #NP# ) ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '380A390A'
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select * from F00 where colint = BITAND(-8, 9);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '8')
    defs.hkey = ("""SELECT * FROM""" +
                 """ F00 WHERE COLINT = BITAND ( - #NP# , #NP# ) ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '380A390A'
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select * from F00 where colint = BITAND(8, -9);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '0')
    defs.hkey = ("""SELECT * FROM""" +
                 """ F00 WHERE COLINT = BITAND ( #NP# , - #NP# ) ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '380A390A'
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select * from F00 where colint = BITAND(-8, -9);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '-16')
    defs.hkey = ("""SELECT * FROM""" +
                 """ F00 WHERE COLINT = BITAND ( - #NP# , - #NP# ) ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '380A390A'
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select * from F00 where colint = BITAND(31, 13);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '13')
    defs.hkey = """SELECT * FROM F00 WHERE COLINT = BITAND ( #NP# , #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '33310A31330A'
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select * from F00 where colint = BITAND(-7, 9);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '9')
    defs.hkey = ("""SELECT * FROM""" +
                 """ F00 WHERE COLINT = BITAND ( - #NP# , #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '370A390A'
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select * from F00 where colint = BITAND(8, -11);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '0')
    defs.hkey = ("""SELECT * FROM""" +
                 """ F00 WHERE COLINT = BITAND ( #NP# , - #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '380A31310A'
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select * from F00 where colint = BITAND(-7, -5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '-7')
    defs.hkey = ("""SELECT * FROM""" +
                 """ F00 WHERE COLINT = BITAND ( - #NP# , - #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '370A350A'
    setup.verifyHQCEntryExists()

    _testmgr.testcase_end(desc)


def test_case(desc="""case"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: case"""

    setup.resetHQC()

    # function: CASE
    # HQC CACHEABLE AND ALL ARGUMENTS ARE NOT PARAMETERIZED

    stmt = defs.prepXX + """select CASE colint
  WHEN 100 THEN 'one hundred'
  WHEN 200 THEN 'two hundred'
  WHEN 300 THEN 'three hundred'
  WHEN 400 THEN 'four hundred'
  WHEN 500 THEN 'five hundred'
  ELSE 'other'
END from F01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CASE001')
    # increase hits
    # expect = Found in HQC, backpatch OK
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    defs.hkey = ("""SELECT CASE COLINT WHEN #NP# THEN #NP#""" +
                 """ WHEN #NP# THEN #NP# WHEN #NP# THEN #NP#""" +
                 """ WHEN #NP# THEN #NP# WHEN #NP# THEN #NP#""" +
                 """ ELSE #NP# END FROM F01 ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 11
    defs.npliterals = ('3130300A276F6E652068756E64726564270A' +
                       '3230300A2774776F2068756E64726564270A' +
                       '3330300A2774687265652068756E64726564270A' +
                       '3430300A27666F75722068756E64726564270A' +
                       '3530300A27666976652068756E64726564270A' +
                       '276F74686572270A')
    setup.verifyHQCEntryExists()

    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select CASE colint
  WHEN 100 THEN 'one hundred'
  WHEN 200 THEN 'two hundred'
  WHEN 300 THEN 'three hundred'
  WHEN 900 THEN 'nine hundred'
  WHEN 500 THEN 'five hundred'
  ELSE 'whatever'
END from F01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CASE002')
    defs.hkey = ("""SELECT CASE COLINT WHEN #NP# THEN #NP#""" +
                 """ WHEN #NP# THEN #NP# WHEN #NP# THEN #NP#""" +
                 """ WHEN #NP# THEN #NP# WHEN #NP# THEN #NP#""" +
                 """ ELSE #NP# END FROM F01 ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 11
    defs.npliterals = ('3130300A276F6E652068756E64726564270A' +
                       '3230300A2774776F2068756E64726564270A' +
                       '3330300A2774687265652068756E64726564270A' +
                       '3930300A276E696E652068756E64726564270A' +
                       '3530300A27666976652068756E64726564270A' +
                       '277768617465766572270A')
    setup.verifyHQCEntryExists()

    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select CASE colvchr
  WHEN 'six hundred six' THEN 6.06E2
  WHEN 'seven hundred seven' THEN 7.077777E4
  WHEN 'eight hundred eight' THEN 808.808808
  WHEN 'nine hundred nine' THEN 9.09E-2
  WHEN 'one thousand one' THEN 1E3
  WHEN 'two' THEN 2.0
  ELSE 0
END
from F01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CASE003')
    defs.hkey = ("""SELECT CASE COLVCHR WHEN #NP# THEN #NP#""" +
                 """ WHEN #NP# THEN #NP# WHEN #NP# THEN #NP#""" +
                 """ WHEN #NP# THEN #NP# WHEN #NP# THEN #NP#""" +
                 """ WHEN #NP# THEN #NP# ELSE #NP# END FROM F01 ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 13
    defs.npliterals = ('277369782068756E6472656420736978270A' +
                       '362E303645320A' +
                       '27736576656E2068756E6472656420736576656E270A' +
                       '372E30373737373745340A' +
                       '2765696768742068756E64726564206569676874270A' +
                       '3830382E3830383830380A'
                       '276E696E652068756E64726564206E696E65270A' +
                       '392E3039452D320A' +
                       '276F6E652074686F7573616E64206F6E65270A3145330A' +
                       '2774776F270A322E300A300A')
    setup.verifyHQCEntryExists()

    # search CASE
    stmt = defs.prepXX + """select CASE
when colreal < 30000 then 'cold'
when colreal between 30001 and 50000 then 'lukewarm'
when colreal > 50001 and colreal <= 77700 then 'hot'
when colreal >= 77701 and colreal < 90000 then 'very hot'
else 'off the scale'
end from F01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CASE004')
    defs.hkey = ("""SELECT CASE WHEN COLREAL < #NP# THEN #NP#""" +
                 """ WHEN COLREAL BETWEEN #NP# AND #NP# THEN #NP#""" +
                 """ WHEN COLREAL > #NP# AND COLREAL <= #NP# THEN #NP#""" +
                 """ WHEN COLREAL >= #NP# AND COLREAL < #NP# THEN #NP#""" +
                 """ ELSE #NP# END FROM F01 ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 12
    defs.npliterals = ('33303030300A27636F6C64270A' +
                       '33303030310A35303030300A276C756B657761726D270A' +
                       '35303030310A37373730300A27686F74270A' +
                       '37373730310A39303030300A277665727920686F74270A' +
                       '276F666620746865207363616C65270A')
    setup.verifyHQCEntryExists()

    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select coldate, CASE
WHEN coldate < date'1800-01-01' THEN '18th century'
WHEN coldate >= date'1800-01-01'
    and coldate < date'1900-01-01' THEN '19th century'
WHEN coldate >= date'1900-01-01'
    and coldate < date'2000-01-01' THEN '20th century'
WHEN coldate >= date'2000-01-01'
    and coldate < date'2100-01-01' THEN '21st century'
ELSE 'beyond'
END from F01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CASE005')
    defs.hkey = ("""SELECT COLDATE , CASE""" +
                 """ WHEN COLDATE < DATE #NP# THEN #NP#""" +
                 """ WHEN COLDATE >= DATE #NP# AND COLDATE < DATE #NP#""" +
                 """ THEN #NP#""" +
                 """ WHEN COLDATE >= DATE #NP# AND COLDATE < DATE #NP#""" +
                 """ THEN #NP#""" +
                 """ WHEN COLDATE >= DATE #NP# AND COLDATE < DATE #NP#""" +
                 """ THEN #NP#""" +
                 """ ELSE #NP# END FROM F01 ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 12
    defs.npliterals = ('27313830302D30312D3031270A' +
                       '27313874682063656E74757279270A' +
                       '27313830302D30312D3031270A' +
                       '27313930302D30312D3031270A' +
                       '27313974682063656E74757279270A' +
                       '27313930302D30312D3031270A' +
                       '27323030302D30312D3031270A' +
                       '27323074682063656E74757279270A' +
                       '27323030302D30312D3031270A' +
                       '27323130302D30312D3031270A' +
                       '27323173742063656E74757279270A' +
                       '276265796F6E64270A')
    setup.verifyHQCEntryExists()

    _testmgr.testcase_end(desc)


def test_cast(desc="""cast"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: cast"""

    setup.resetHQC()

    # function: CAST
    # HQC CACHEABLE AND PARAMETERIZED

    # expect = HQC::AddEntry: passed
    # 1112utt: 'some data here ' is parameterized literal
    #    whereas 17 of char() is non-parameterized literal
    stmt = defs.prepXX + """select cast('some data here' as char(17))
from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, 'some data here')
    defs.hkey = """SELECT CAST ( #NP# AS CHAR ( #NP# ) ) FROM TBL1R ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '27736F6D6520646174612068657265270A'
    defs.num_npliterals = 1
    defs.npliterals = '31370A'
    setup.verifyHQCEntryExists()

    # expect = HQC::AddEntry: passed
    stmt = defs.prepXX + """select cast('Snow White Sleeps' as char(17))
from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, 'Snow White Sleeps')
    defs.hkey = """SELECT CAST ( #NP# AS CHAR ( #NP# ) ) FROM TBL1R ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '27536E6F7720576869746520536C65657073270A'
    defs.num_npliterals = 1
    defs.npliterals = '31370A'
    setup.verifyHQCEntryExists()

    # expect = HQC::AddEntry: passed
    stmt = defs.prepXX + """select cast('dwarfs' as char(15)) from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, 'dwarfs')
    defs.hkey = """SELECT CAST ( #NP# AS CHAR ( #NP# ) ) FROM TBL1R ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '27647761726673270A'
    defs.num_npliterals = 1
    defs.npliterals = '31350A'
    setup.verifyHQCEntryExists()

    # expect = HQC::AddEntry: passed
    stmt = defs.prepXX + """select cast('aaaaa' as char(5)) from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, 'aaaaa')
    defs.hkey = """SELECT CAST ( #NP# AS CHAR ( #NP# ) ) FROM TBL1R ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '276161616161270A'
    defs.num_npliterals = 1
    defs.npliterals = '350A'
    setup.verifyHQCEntryExists()

    # expect = HQC::AddEntry: passed
    stmt = defs.prepXX + """select cast(date'1971-01-01' as char(10))
from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '1971-01-01')
    defs.hkey = """SELECT CAST ( DATE #NP# AS CHAR ( #NP# ) ) FROM TBL1R ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '313937312D30312D30310A'
    defs.num_npliterals = 1
    defs.npliterals = '31300A'
    setup.verifyHQCEntryExists()

    # expect = Found in HQC, backpatch OK
    stmt = defs.prepXX + """select cast(date'1999-12-31' as char(10))
from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '1999-12-31')
    defs.hkey = """SELECT CAST ( DATE #NP# AS CHAR ( #NP# ) ) FROM TBL1R ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '313937312D30312D30310A'
    defs.num_npliterals = 1
    defs.npliterals = '31300A'
    setup.verifyHQCEntryExists()

    # 1112utt timestamp is parameterized
    # 1112utt HQC::AddEntry()
    stmt = defs.prepXX + """select
cast(timestamp'2014-08-20 11:22:33' as date) from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2014-08-20')
    defs.hkey = """SELECT CAST ( TIMESTAMP #NP# AS DATE ) FROM TBL1R ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '323031342D30382D32302031313A32323A33330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # 1112utt: Found in HQC, backpatch OK
    stmt = defs.prepXX + """select
cast(timestamp'1999-12-31 22:33:44' as date) from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '1999-12-31')
    defs.hkey = """SELECT CAST ( TIMESTAMP #NP# AS DATE ) FROM TBL1R ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '323031342D30382D32302031313A32323A33330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # 1112utt timestamp is parameterized but # of char() is not parameterized
    # 1112utt HQC::AddEntry()
    stmt = defs.prepXX + """select
cast(timestamp'2014-08-20 11:22:33' as char(19)) from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '2014-08-20 11:22:33')
    # increase hits
    stmt = defs.prepXX + """select
cast(timestamp'2014-08-20 11:22:33' as char(19)) from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '2014-08-20 11:22:33')
    defs.hkey = ("""SELECT CAST ( TIMESTAMP #NP# AS CHAR ( #NP# ) )""" +
                 """ FROM TBL1R ;""")
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '323031342D30382D32302031313A32323A33330A'
    defs.num_npliterals = 1
    defs.npliterals = '31390A'
    setup.verifyHQCEntryExists()

    # 1112utt: Found in HQC, backpatch OK
    stmt = defs.prepXX + """select
cast(timestamp'1999-12-31 22:33:44' as char(19)) from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '1999-12-31 22:33:44')
    defs.hkey = ("""SELECT CAST ( TIMESTAMP #NP# AS CHAR ( #NP# ) )""" +
                 """ FROM TBL1R ;""")
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '323031342D30382D32302031313A32323A33330A'
    defs.num_npliterals = 1
    defs.npliterals = '31390A'
    setup.verifyHQCEntryExists()

    # expect = HQC::AddEntry: passed
    #stmt = defs.prepXX + """select cast('2014-08-26' as date) from g00;"""
    # expect = Found in HQC, HQC backpatch OK
    #stmt = defs.prepXX + """select cast('1974-12-28' as date) from g00;"""
    #stmt = defs.prepXX + """select cast('1974-12-28 22:33:44' as date)
#from g00;"""

    # 1112utt HQC::AddEntry()
    #stmt = defs.prepXX + """select cast(cast('1974-12-28 22:33:44'
#as timestamp) as date) from g00;"""

    # expect = HQC::AddEntry: passed
    stmt = defs.prepXX + """select cast(cos(0.3457) as numeric(6,3))
from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '0.940')
    defs.hkey = ("""SELECT CAST ( COS ( #NP# ) AS NUMERIC ( #NP# , """ +
                 """#NP# ) ) FROM TBL1R ;""")
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '302E333435370A'
    defs.num_npliterals = 2
    defs.npliterals = '360A330A'
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select cast(cos(0.647352) as numeric(6,3))
from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '0.797')
    defs.hkey = ("""SELECT CAST ( COS ( #NP# ) AS NUMERIC""" +
                 """ ( #NP# , #NP# ) ) FROM TBL1R ;""")
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '302E3634373335320A'
    defs.num_npliterals = 2
    defs.npliterals = '360A330A'
    setup.verifyHQCEntryExists()

    # expect = ERROR[8411]
    #stmt = defs.prepXX + """select cast(100 as numeric(2)) from g00;"""
    # expect = ERROR[8411]
    #stmt = defs.prepXX + """select cast(cast(100 as smallint)
#as numeric(2)) from g00;"""
    # expect = 100.789
    #stmt = defs.prepXX + """select cast(100.789 as numeric(6,3))
#from TBL1R;"""
    #stmt = defs.prepXX + """select cast(111.222 as numeric(6,3))
#from TBL1R;"""
    # expect = 123.456
    #stmt = defs.prepXX + """select cast(123.456789 as numeric(6,3))
#from TBL1R;"""
    #stmt = defs.prepXX + """select cast(987.654321 as numeric(6,3))
#from TBL1R;"""
    # expect = 456.789
    #stmt = defs.prepXX + """select cast(cast(456.789 as decimal(7,4))
#as numeric(6,3)) from TBL1R;"""
    # expect = 123.67
    #stmt = defs.prepXX + """select cast(cast(123.4567 as decimal(7,4))
#as numeric(6,2)) from TBL1R;"""

    # expect = HQC::AddEntry: passed
#insert into g00 values (cast(1.00E+02 as int), cast(123.123 as int),
#cast('1986-12-31' as date), cast(16384.0 as smallint),
#cast('49.1' as numeric(9,4)), cast(date'2014-08-20' as char(26)),
#cast(3.147E+10 as largeint), cast('2014-08-26 22:33:44' as timestamp),
#cast(timestamp'2026-07-04 23:34:45' as varchar(75)), cast(3.147 as float),
#cast(6.294 as decimal(9)), cast(123.123 as interval day(18)));"""

#update g00 set (colint,colchar,colnum,colintvl) = (cast(789.789 as int),
#cast(date'2014-09-02' as char(10)), cast(555 as numeric(6,2)),
#cast(111.222 as interval day(18)));"""

    # expect = Found in HQC, HQC backpatch OK
#insert into g00 values (cast(9.00E+02 as int), cast(456.456 as int),
#cast('1996-01-15' as date), cast(8192.0 as smallint),
#cast('99.9' as numeric(9,4)), cast(date'2004-08-26' as char(26)),
#cast(1.876E+11 as largeint), cast('1996-12-26 22:22:22' as timestamp),
#cast(timestamp'2016-11-27 11:11:11' as varchar(75)),
#cast(3.147 as float), cast(6.294 as decimal(9)),
#cast(123.123 as interval day(18)));"""

    #stmt = defs.prepXX + """select * from g00
#where colint = (cast(789.789 as int));"""
    #stmt = defs.prepXX + """select * from g00
#where colint = (cast(123.456 as int));"""
    #stmt = defs.prepXX + """select * from g00
#where colint = (cast(12345.4567 as int));"""

    setup.resetHQC()

    stmt = defs.prepXX + """select * from F02
where colchar = (cast(date'2014-09-03' as char(10)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CAST001')
    defs.hkey = ("""SELECT * FROM F02 WHERE COLCHAR =""" +
                 """ ( CAST ( DATE #NP# AS CHAR ( #NP# ) ) ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '27323031342D30392D3033270A31300A'
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select * from F02
where colchar = (cast(date'1971-10-15' as char(10)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CAST002')
    defs.hkey = ("""SELECT * FROM F02 WHERE COLCHAR = ( CAST (""" +
                 """ DATE #NP# AS CHAR ( #NP# ) ) ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '27313937312D31302D3135270A31300A'
    setup.verifyHQCEntryExists()

    setup.resetHQC()

    stmt = defs.prepXX + """select * from F02
where colnum = (cast(1.11222E2 as numeric(9,4)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CAST003')
    defs.hkey = ("""SELECT * FROM F02 WHERE COLNUM = ( CAST (""" +
                 """ #NP# AS NUMERIC ( #NP# , #NP# ) ) ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 3
    defs.npliterals = '312E313132323245320A390A340A'
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select * from F02
where colnum = (cast(333.344 as numeric(9,4)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CAST004')
    defs.hkey = ("""SELECT * FROM F02 WHERE COLNUM = ( CAST (""" +
                 """ #NP# AS NUMERIC ( #NP# , #NP# ) ) ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 3
    defs.npliterals = '3333332E3334340A390A340A'
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select * from F02
where colintvl = (cast(8.222 as interval day(18)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CAST005')
    defs.hkey = ("""SELECT * FROM F02 WHERE COLINTVL = ( CAST (""" +
                 """ #NP# AS INTERVAL DAY ( #NP# ) ) ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '382E3232320A31380A'
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select * from F02
where colintvl = (cast(33.0 as interval day(18)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CAST006')
    defs.hkey = ("""SELECT * FROM F02 WHERE COLINTVL = ( CAST (""" +
                 """ #NP# AS INTERVAL DAY ( #NP# ) ) ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '33332E300A31380A'
    setup.verifyHQCEntryExists()

    #stmt = defs.prepXX + """select * from g00
#where coldate = (cast('2014-08-20' as date));"""
    #stmt = defs.prepXX + """select * from g00
#where coldate = (cast('1970-01-31' as date));"""
    #stmt = defs.prepXX + """select * from g00
#where coldate = (cast('2014-08-20 11:22:33' as date));"""

    #stmt = defs.prepXX + """select * from g00
#where colnum = (cast(555 as numeric(2)));"""
    #stmt = defs.prepXX + """select * from g00
#where colnum = (cast(666 as numeric(2)));"""
    #stmt = defs.prepXX + """select * from g00
#where colnum = (cast(555 as numeric(3)));"""

    #stmt = defs.prepXX + """select * from g00
#where colnum = (cast(cast(555 as smallint) as numeric(2)));"""
    #stmt = defs.prepXX + """select * from g00
#where colnum = (cast(cast(666 as smallint) as numeric(2)));"""
    #stmt = defs.prepXX + """select * from g00
#where colnum = (cast(cast(666 as smallint) as numeric(4)));"""

    _testmgr.testcase_end(desc)


def test_converttohex(desc="""converttohex"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: converttohex"""

    setup.resetHQC()

    # function: CONVERTTOHEX()
    # HQC CACHEABLE, NOT PARAMETERIZED

    stmt = defs.prepXX + """select CONVERTTOHEX(269488144) from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '10101010')
    # increase hits
    stmt = defs.prepXX + """select CONVERTTOHEX(269488144) from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '10101010')
    defs.hkey = """SELECT CONVERTTOHEX ( #NP# ) FROM TBL1R ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '3236393438383134340A'
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select CONVERTTOHEX(11259375) from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, 'EFCDAB00')
    defs.hkey = """SELECT CONVERTTOHEX ( #NP# ) FROM TBL1R ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '31313235393337350A'
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + ("""select CONVERTTOHEX(""" +
                          """timestamp'2014-08-20 12:23:34') from TBL1R;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, 'DE0708140C1722')
    defs.hkey = """SELECT CONVERTTOHEX ( TIMESTAMP #NP# ) FROM TBL1R ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27323031342D30382D32302031323A32333A3334270A'
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + ("""select CONVERTTOHEX('some data here')""" +
                          """ from TBL1R;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '736F6D6520646174612068657265')
    defs.hkey = """SELECT CONVERTTOHEX ( #NP# ) FROM TBL1R ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27736F6D6520646174612068657265270A'
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + ("""select""" +
                          """ CONVERTTOHEX(interval '31:14:59:58' day""" +
                          """ to second) from TBL1R;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '80B79C2F7C020000')
    defs.hkey = ("""SELECT""" +
                 """ CONVERTTOHEX ( INTERVAL #NP# DAY TO SECOND )""" +
                 """ FROM TBL1R ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2733313A31343A35393A3538270A'
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select CONVERTTOHEX(1.234567E+3) from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '54E3A59B444A9340')
    defs.hkey = """SELECT CONVERTTOHEX ( #NP# ) FROM TBL1R ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '312E323334353637452B330A'
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select CONVERTTOHEX(0.987654E-3) from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, 'EC0B4E68852E503F')
    defs.hkey = """SELECT CONVERTTOHEX ( #NP# ) FROM TBL1R ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E393837363534452D330A'
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select CONVERTTOHEX(0.56789124) from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '84886203')
    defs.hkey = """SELECT CONVERTTOHEX ( #NP# ) FROM TBL1R ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '302E35363738393132340A'
    setup.verifyHQCEntryExists()

    _testmgr.testcase_end(desc)


def test_AND_bitwise(desc="""bitwise AND"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: bitwise AND"""

    bitwise_oper("""&""")

    _testmgr.testcase_end(desc)


def test_OR_bitwise(desc="""bitwise OR"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: bitwise OR"""

    bitwise_oper("""|""")

    _testmgr.testcase_end(desc)


def test_XOR_bitwise(desc="""bitwise XOR"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: bitwise XOR"""

    bitwise_oper("""^""")

    _testmgr.testcase_end(desc)


def bitwise_oper(oper=None):
    global _testmgr
    global _testlist
    global _dci

    setup.resetHQC()

    # HQC CACHEABLE, NOT PARAMETERIZED

    if oper == """&""":
        sect = 'BO_AND'
    elif oper == """|""":
        sect = 'BO_OR'
    elif oper == """^""":
        sect = 'BO_XOR'

    stmt = defs.prepXX + """select -1 """ + oper + """ 3 from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, sect + '-001')

    stmt = defs.prepXX + """select 1 """ + oper + """ -3 from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, sect + '-002')

    stmt = defs.prepXX + """select -1 """ + oper + """ -3 from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, sect + '-003')

    setup.verifyHQCempty()

    stmt = defs.prepXX + """select 1 """ + oper + """ 3 from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, sect + '-004')
    defs.hkey = """SELECT #NP# """ + oper + """ #NP# FROM TBL1R ;"""
    defs.num_hits = 0
    defs.num_pliterals = 2
    defs.pliterals = '310A330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select 9 """ + oper + """ 8 from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, sect + '-005')
    defs.hkey = """SELECT #NP# """ + oper + """ #NP# FROM TBL1R ;"""
    defs.num_hits = 1
    defs.num_pliterals = 2
    defs.pliterals = '310A330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select 99 """ + oper + """ 11 from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, sect + '-006')
    defs.hkey = """SELECT #NP# """ + oper + """ #NP# FROM TBL1R ;"""
    defs.num_hits = 0
    defs.num_pliterals = 2
    defs.pliterals = '39390A31310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select 8 """ + oper + """ 40 from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, sect + '-007')
    defs.hkey = """SELECT #NP# """ + oper + """ #NP# FROM TBL1R ;"""
    defs.num_hits = 1
    defs.num_pliterals = 2
    defs.pliterals = '39390A31310A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    stmt = defs.prepXX + """select 7 """ + oper + """ 2 from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, sect + '-008')
    defs.hkey = """SELECT #NP# """ + oper + """ #NP# FROM TBL1R ;"""
    defs.num_hits = 2
    defs.num_pliterals = 2
    defs.pliterals = '310A330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    stmt = (defs.prepXX +
            """select * from F00 where colint = 8 """ + oper + """ 9;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, sect + '-009')
    defs.hkey = ("""SELECT * FROM F00 WHERE COLINT = #NP# """ +
                 oper + """ #NP# ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '380A390A'
    setup.verifyHQCEntryExists()

    stmt = (defs.prepXX +
            """select * from F00 where colint = -8 """ + oper + """ 9;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, sect + '-010')
    defs.hkey = ("""SELECT * FROM F00 WHERE COLINT = - #NP# """ +
                 oper + """ #NP# ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '380A390A'
    setup.verifyHQCEntryExists()

    stmt = (defs.prepXX + """select * from F00 where colint = 8 """ +
            oper + """ -9;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, sect + '-011')
    defs.hkey = ("""SELECT * FROM F00 WHERE COLINT = #NP# """ + oper +
                 """ - #NP# ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '380A390A'
    setup.verifyHQCEntryExists()

    stmt = (defs.prepXX + """select * from F00 where colint = -8 """ +
            oper + """ -9;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, sect + '-012')
    defs.hkey = ("""SELECT * FROM F00 WHERE COLINT = - #NP# """ + oper +
                 """ - #NP# ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '380A390A'
    setup.verifyHQCEntryExists()

    stmt = (defs.prepXX + """select * from F00 where colint = 8 """ +
            oper + """ 9;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, sect + '-013')
    defs.hkey = ("""SELECT * FROM F00 WHERE COLINT = #NP# """ + oper +
                 """ #NP# ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '380A390A'
    setup.verifyHQCEntryExists()

    stmt = (defs.prepXX + """select * from F00 where colint = -8 """ +
            oper + """ 9;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, sect + '-014')
    defs.hkey = ("""SELECT * FROM""" +
                 """ F00 WHERE COLINT = - #NP# """ + oper + """ #NP# ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '380A390A'
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute show_entries;""")

    stmt = (defs.prepXX + """select * from F00 where colint = 8 """ +
            oper + """ -9;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, sect + '-015')
    defs.hkey = ("""SELECT * FROM""" +
                 """ F00 WHERE COLINT = #NP# """ + oper + """ - #NP# ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '380A390A'
    #setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute show_entries;""")

    stmt = (defs.prepXX + """select * from F00 where colint = -8 """ +
            oper + """ -9;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, sect + '-016')
    defs.hkey = ("""SELECT * FROM""" +
                 """ F00 WHERE COLINT = - #NP# """ + oper + """ - #NP# ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '380A390A'
    #setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""execute show_entries;""")

    stmt = (defs.prepXX + """select * from F00 where colint = 31 """ +
            oper + """ 13;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, sect + '-017')
    defs.hkey = ("""SELECT * FROM F00 WHERE COLINT = #NP# """ +
                 oper + """ #NP# ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '33310A31330A'
    setup.verifyHQCEntryExists()

    stmt = (defs.prepXX + """select * from F00 where colint = -7 """ +
            oper + """ 9;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, sect + '-018')
    defs.hkey = ("""SELECT * FROM""" +
                 """ F00 WHERE COLINT = - #NP# """ + oper + """ #NP# ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '370A390A'
    setup.verifyHQCEntryExists()

    stmt = (defs.prepXX + """select * from F00 where colint = 8 """ +
            oper + """ -11;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, sect + '-019')
    defs.hkey = ("""SELECT * FROM""" +
                 """ F00 WHERE COLINT = #NP# """ + oper + """ - #NP# ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '380A31310A'
    setup.verifyHQCEntryExists()

    stmt = (defs.prepXX + """select * from F00 where colint = -7 """ +
            oper + """ -5;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, sect + '-020')
    defs.hkey = ("""SELECT * FROM""" +
                 """ F00 WHERE COLINT = - #NP# """ + oper + """ - #NP# ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '370A350A'
    setup.verifyHQCEntryExists()
