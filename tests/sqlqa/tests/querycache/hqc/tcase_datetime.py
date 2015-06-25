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

#add_months
#converttimestamp
#current
#current_date
#current_time
#date_add
#date_part
#date_sub
#date_trunc
#dateadd
#datediff
#dateformat
#day
#dayname
#dayofmonth
#dayofyear
#hour
#minute
#month
#monthname
#quarter
#second
#timestampadd
#timestampdfif
#week
#year

    output = _dci.cmdexec("""drop table F00 cascade;""")
    output = _dci.cmdexec("""drop table F01 cascade;""")
    output = _dci.cmdexec("""drop table TBL1R cascade;""")

    stmt = """create table TBL1R(colts timestamp);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    setup.resetHQC()
    stmt = """insert into TBL1R values (current_timestamp);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, '1')
    setup.verifyHQCempty()

    stmt = """create table F00(colkey int not null primary key,
coldate date,
colts timestamp,
colyr int,
colmon int,
colday int,
colhr int,
colmin int,
colsec int,
coljdt largeint,
coljts largeint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into F00 values
(1, date '2015-03-21', timestamp '2015-03-21 14:48:32.123456', 2015,
3, 21, 14, 48, 32, 212293656000000000, 212293709312123456),
(2, date '1975-12-25', timestamp '1975-12-25 17:52:45.987', 1975,
12, 25, 17, 52, 45, 211055457600000000, 211055521965987000),
(3, date '1998-07-04', timestamp '1998-07-04 23:59:59.5673', 1998,
7, 4, 23, 59, 59, 211766270400000000, 211766356799567300),
(4, date '1986-10-21', timestamp '1986-10-21 16:17:18.00001', 1971,
1, 1, 0, 0, 0, 211396996800000000, 211397055438000010),
(5, date '2004-11-27', timestamp '2004-11-27 00:00:00.123456', 2004,
11, 27, 0, 0, 0, 211968273600000000, 211968273600123456),
(6, date '2010-05-31', timestamp '2010-05-31 01:02:03.45', 2010,
5, 31, 1, 2, 3, 212142024000000000, 212142027723450000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, '6')

    stmt = """create table KEYTBL(colkey int not null primary key,
colday varchar(10) character set utf8);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into KEYTBL values
(1, 'SUNDAY'),
(2, 'MONDAY'),
(3, 'TUESDAY'),
(4, 'WEDNESDAY'),
(5, 'THURSDAY'),
(6, 'FRIDAY'),
(7, 'SATURDAY');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, '7')


def test_currts(desc="""current_timestamp"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: current_timestamp"""

    setup.resetHQC()

    # function: CURRENT_TIMESTAMP
    # HQC CACHEABLE, NOT PARAMETERIZED

    # add entry1
    stmt = defs.prepXX + """select CURRENT_TIMESTAMP from tbl1r;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CURRTS001')
    defs.hkey = """SELECT CURRENT_TIMESTAMP FROM TBL1R ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry2
    stmt = defs.prepXX + """select CURRENT_TIMESTAMP(3) from tbl1r;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CURRTS002')
    defs.hkey = """SELECT CURRENT_TIMESTAMP ( #NP# ) FROM TBL1R ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '330A'
    setup.verifyHQCEntryExists()

    # add entry3
    stmt = defs.prepXX + """select CURRENT_TIMESTAMP(5) from tbl1r;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CURRTS003')
    defs.hkey = """SELECT CURRENT_TIMESTAMP ( #NP# ) FROM TBL1R ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '350A'
    setup.verifyHQCEntryExists()

    # increase hits, entry1
    stmt = defs.prepXX + """select CURRENT_TIMESTAMP from tbl1r;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CURRTS001')
    defs.hkey = """SELECT CURRENT_TIMESTAMP FROM TBL1R ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry2
    stmt = defs.prepXX + """select CURRENT_TIMESTAMP(3) from tbl1r;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CURRTS002')
    defs.hkey = """SELECT CURRENT_TIMESTAMP ( #NP# ) FROM TBL1R ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '330A'
    setup.verifyHQCEntryExists()

    # add entry4
    stmt = defs.prepXX + """select CURRENT_TIMESTAMP(2) from tbl1r;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CURRTS004')
    defs.hkey = """SELECT CURRENT_TIMESTAMP ( #NP# ) FROM TBL1R ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '320A'
    setup.verifyHQCEntryExists()

    # add entry5
    stmt = defs.prepXX + """select * from tbl1r
where colts = CURRENT_TIMESTAMP;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = """SELECT * FROM TBL1R WHERE COLTS = CURRENT_TIMESTAMP ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry6
    stmt = defs.prepXX + """select * from tbl1r
where colts = CURRENT_TIMESTAMP(2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = ("""SELECT * FROM TBL1R""" +
                 """ WHERE COLTS = CURRENT_TIMESTAMP ( #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '320A'
    setup.verifyHQCEntryExists()

    # add entry7
    stmt = defs.prepXX + """select * from tbl1r
where colts = CURRENT_TIMESTAMP(4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = ("""SELECT * FROM TBL1R""" +
                 """ WHERE COLTS = CURRENT_TIMESTAMP ( #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '340A'
    setup.verifyHQCEntryExists()

    # increase hits, entry6
    stmt = defs.prepXX + """select * from tbl1r
where colts = CURRENT_TIMESTAMP(2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = ("""SELECT * FROM TBL1R""" +
                 """ WHERE COLTS = CURRENT_TIMESTAMP ( #NP# ) ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '320A'
    setup.verifyHQCEntryExists()

    # increase hits, entry7
    stmt = defs.prepXX + """select * from tbl1r
where colts = CURRENT_TIMESTAMP(4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = ("""SELECT * FROM TBL1R""" +
                 """ WHERE COLTS = CURRENT_TIMESTAMP ( #NP# ) ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '340A'
    setup.verifyHQCEntryExists()

    # add entry8
    stmt = defs.prepXX + """update tbl1r set colts = CURRENT_TIMESTAMP;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_updated_msg(output, '1')
    defs.hkey = ("""UPDATE TBL1R SET""" +
                 """ COLTS = CURRENT_TIMESTAMP ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry9
    stmt = defs.prepXX + """update tbl1r set colts = CURRENT_TIMESTAMP(3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_updated_msg(output, '1')
    defs.hkey = ("""UPDATE TBL1R SET""" +
                 """ COLTS = CURRENT_TIMESTAMP ( #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '330A'
    setup.verifyHQCEntryExists()

    # add entry10
    stmt = defs.prepXX + """update tbl1r set colts = CURRENT_TIMESTAMP(1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_updated_msg(output, '1')
    defs.hkey = ("""UPDATE TBL1R SET""" +
                 """ COLTS = CURRENT_TIMESTAMP ( #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '310A'
    setup.verifyHQCEntryExists()

    # add entry11
    stmt = defs.prepXX + """update tbl1r set colts = CURRENT_TIMESTAMP(5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_updated_msg(output, '1')
    defs.hkey = ("""UPDATE TBL1R SET""" +
                 """ COLTS = CURRENT_TIMESTAMP ( #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '350A'
    setup.verifyHQCEntryExists()

    # increase hits, entry8
    stmt = defs.prepXX + """update tbl1r set colts = CURRENT_TIMESTAMP;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_updated_msg(output, '1')
    defs.hkey = ("""UPDATE TBL1R SET""" +
                 """ COLTS = CURRENT_TIMESTAMP ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry9
    stmt = defs.prepXX + """update tbl1r set colts = CURRENT_TIMESTAMP(3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_updated_msg(output, '1')
    defs.hkey = ("""UPDATE TBL1R SET""" +
                 """ COLTS = CURRENT_TIMESTAMP ( #NP# ) ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '330A'
    setup.verifyHQCEntryExists()

    # increase hits, entry10
    stmt = defs.prepXX + """update tbl1r set colts = CURRENT_TIMESTAMP(1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_updated_msg(output, '1')
    defs.hkey = ("""UPDATE TBL1R SET""" +
                 """ COLTS = CURRENT_TIMESTAMP ( #NP# ) ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '310A'
    setup.verifyHQCEntryExists()

    _testmgr.testcase_end(desc)


def test_dayofweek(desc="""dayofweek"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: dayofweek()"""

    setup.resetHQC()

    # function: DAYOFWEEK()
    # HQC CACHEABLE, PARAMETERIZED

    # add entry1
    stmt = defs.prepXX + """select colkey,
DAYOFWEEK(coldate) from F00 order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'DAYOFWK001')
    defs.hkey = ("""SELECT COLKEY , DAYOFWEEK ( COLDATE )""" +
                 """ FROM F00 ORDER BY COLKEY ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry2
    stmt = defs.prepXX + """select colkey,
DAYOFWEEK(colts) from F00 order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'DAYOFWK002')
    defs.hkey = ("""SELECT COLKEY , DAYOFWEEK ( COLTS )""" +
                 """ FROM F00 ORDER BY COLKEY ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry3
    stmt = defs.prepXX + """select
DAYOFWEEK(date'2014-09-03') from TBL1R ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'DAYOFWK003')
    defs.hkey = ("""SELECT DAYOFWEEK ( DATE #NP# ) FROM TBL1R ;""")
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '323031342D30392D30330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry3
    stmt = defs.prepXX + """select
DAYOFWEEK(date'1976-09-03') from TBL1R ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'DAYOFWK003a')
    defs.hkey = ("""SELECT DAYOFWEEK ( DATE #NP# ) FROM TBL1R ;""")
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '323031342D30392D30330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry2
    stmt = defs.prepXX + """select colkey,
DAYOFWEEK(colts) from F00 order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'DAYOFWK002')
    defs.hkey = ("""SELECT COLKEY , DAYOFWEEK ( COLTS )""" +
                 """ FROM F00 ORDER BY COLKEY ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry4
    stmt = defs.prepXX + """select
DAYOFWEEK(timestamp'2014-09-04 11:22:33') from TBL1R ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'DAYOFWK004')
    defs.hkey = ("""SELECT DAYOFWEEK ( TIMESTAMP #NP# )""" +
                 """ FROM TBL1R ;""")
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '323031342D30392D30342031313A32323A33330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry3
    stmt = defs.prepXX + """select
DAYOFWEEK(date'2021-01-30') from TBL1R ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'DAYOFWK003b')
    defs.hkey = ("""SELECT DAYOFWEEK ( DATE #NP# )""" +
                 """ FROM TBL1R ;""")
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '323031342D30392D30330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry4
    stmt = defs.prepXX + """select
DAYOFWEEK(timestamp'1976-09-04 22:33:44') from TBL1R ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'DAYOFWK004a')
    defs.hkey = ("""SELECT DAYOFWEEK ( TIMESTAMP #NP# )""" +
                 """ FROM TBL1R ;""")
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '323031342D30392D30342031313A32323A33330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry5
    stmt = defs.prepXX + """select colday from KEYTBL
where colkey = DAYOFWEEK(date'2014-08-20');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, 'WEDNESDAY')
    defs.hkey = ("""SELECT COLDAY FROM KEYTBL""" +
                 """ WHERE COLKEY = DAYOFWEEK ( DATE #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27323031342D30382D3230270A'
    setup.verifyHQCEntryExists()

    # add entry6
    stmt = defs.prepXX + """select colday from KEYTBL
where colkey = DAYOFWEEK(timestamp'1978-11-27 23:59:59');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, 'MONDAY')
    defs.hkey = ("""SELECT COLDAY FROM KEYTBL""" +
                 """ WHERE COLKEY = DAYOFWEEK ( TIMESTAMP #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27313937382D31312D32372032333A35393A3539270A'
    setup.verifyHQCEntryExists()

    # increase hits, entry5
    stmt = defs.prepXX + """select colday from KEYTBL
where colkey = DAYOFWEEK(date'2014-08-20');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, 'WEDNESDAY')
    defs.hkey = ("""SELECT COLDAY FROM KEYTBL""" +
                 """ WHERE COLKEY = DAYOFWEEK ( DATE #NP# ) ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27323031342D30382D3230270A'
    setup.verifyHQCEntryExists()

    # add entry7
    stmt = defs.prepXX + """select colday from KEYTBL
where colkey = DAYOFWEEK(date'1984-11-02');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, 'FRIDAY')
    defs.hkey = ("""SELECT COLDAY FROM KEYTBL""" +
                 """ WHERE COLKEY = DAYOFWEEK ( DATE #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27313938342D31312D3032270A'
    setup.verifyHQCEntryExists()

    # increase hits, entry6
    stmt = defs.prepXX + """select colday from KEYTBL
where colkey = DAYOFWEEK(timestamp'1978-11-27 23:59:59');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, 'MONDAY')
    defs.hkey = ("""SELECT COLDAY FROM KEYTBL""" +
                 """ WHERE COLKEY = DAYOFWEEK ( TIMESTAMP #NP# ) ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27313937382D31312D32372032333A35393A3539270A'
    setup.verifyHQCEntryExists()

    # add entry8
    stmt = defs.prepXX + """select colday from KEYTBL
where colkey = DAYOFWEEK(timestamp'2015-03-23 00:22:33');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, 'MONDAY')
    defs.hkey = ("""SELECT COLDAY FROM KEYTBL""" +
                 """ WHERE COLKEY = DAYOFWEEK ( TIMESTAMP #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27323031352D30332D32332030303A32323A3333270A'
    setup.verifyHQCEntryExists()

    _testmgr.testcase_end(desc)


def test_extract(desc="""extract"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: extract()"""

    # function: EXTRACT()
    # in result-set: HQC CACHEABLE, PARAMETERIZED
    # in where-clause: HQC CACHEABLE, NOT PARAMETERIZED

    setup.resetHQC()

    # expect = HQC::AddEntry(): passed
    stmt1 = defs.prepXX + """select colkey,
EXTRACT(YEAR FROM coldate) from F00 order by 1;"""
    output = _dci.cmdexec(stmt1)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'EXTRACT001')

    # expect = HQC::AddEntry(): passed
    stmt2 = defs.prepXX + """select colkey,
EXTRACT(MONTH FROM coldate) from F00 order by colkey;"""
    output = _dci.cmdexec(stmt2)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'EXTRACT002')

    # expect = HQC::AddEntry(): passed
    stmt3 = defs.prepXX + """select colkey,
EXTRACT(DAY FROM coldate) from F00 order by colkey;"""
    output = _dci.cmdexec(stmt3)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'EXTRACT003')

    # expect = HQC::AddEntry(): passed
    stmt4 = defs.prepXX + """select colkey,
EXTRACT(HOUR FROM colts) from F00 order by colkey;"""
    output = _dci.cmdexec(stmt4)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'EXTRACT004')

    # expect = HQC::AddEntry(): passed
    stmt5 = defs.prepXX + """select colkey,
EXTRACT(MINUTE FROM colts) from F00 order by colkey;"""
    output = _dci.cmdexec(stmt5)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'EXTRACT005')

    # expect = HQC::AddEntry(): passed
    stmt6 = defs.prepXX + """select colkey,
EXTRACT(SECOND FROM colts) from F00 order by colkey;"""
    output = _dci.cmdexec(stmt6)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'EXTRACT006')

    # expect = HQC::AddEntry(): passed
    stmt7 = defs.prepXX + """select colkey,
EXTRACT(YEAR FROM colts) from F00 order by colkey;"""
    output = _dci.cmdexec(stmt7)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'EXTRACT007')

    # expect = HQC::AddEntry(): passed
    stmt8 = defs.prepXX + """select colkey,
EXTRACT(MONTH FROM colts) from F00 order by colkey;"""
    output = _dci.cmdexec(stmt8)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'EXTRACT008')

    # expect = HQC::AddEntry(): passed
    stmt9 = defs.prepXX + """select colkey,
EXTRACT(DAY FROM colts) from F00 order by colkey;"""
    output = _dci.cmdexec(stmt9)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'EXTRACT009')

    output = _dci.cmdexec(stmt1)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'EXTRACT001')

    output = _dci.cmdexec(stmt2)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'EXTRACT002')

    output = _dci.cmdexec(stmt3)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'EXTRACT003')

    output = _dci.cmdexec(stmt4)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'EXTRACT004')

    output = _dci.cmdexec(stmt5)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'EXTRACT005')

    output = _dci.cmdexec(stmt6)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'EXTRACT006')

    # expect 9 HQC entries
    # expect num_hits = 1 for queries involving
    #    extract([year|month|day] from coldate)
    #    extract([hour|minute|sec] from colts)
    # expect num_hits = 0 for queries involing
    #    extract([year|month|day] from colts)
    if defs.genexp == 0:
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EXTRACT_a1')

    # add entry10
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select
EXTRACT(YEAR FROM date'1980-01-30') from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '1980')
    defs.hkey = """SELECT EXTRACT ( YEAR FROM DATE #NP# ) FROM TBL1R ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '313938302D30312D33300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry11
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select
EXTRACT(MONTH FROM date'1990-03-28') from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '3')
    defs.hkey = """SELECT EXTRACT ( MONTH FROM DATE #NP# ) FROM TBL1R ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '313939302D30332D32380A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry12
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select
EXTRACT(DAY FROM date'2000-05-15') from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '15')
    defs.hkey = """SELECT EXTRACT ( DAY FROM DATE #NP# ) FROM TBL1R ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '323030302D30352D31350A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry 10
    # expect = Found in HQC, HQC backpatch OK
    stmt = defs.prepXX + """select
EXTRACT(YEAR FROM date'2013-12-25') from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2013')
    defs.hkey = """SELECT EXTRACT ( YEAR FROM DATE #NP# ) FROM TBL1R ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '313938302D30312D33300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry 11
    # expect = Found in HQC, HQC backpatch OK
    stmt = defs.prepXX + """select
EXTRACT(MONTH FROM date'1996-12-14') from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '12')
    defs.hkey = """SELECT EXTRACT ( MONTH FROM DATE #NP# ) FROM TBL1R ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '313939302D30332D32380A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry 12
    # expect = Found in HQC, HQC backpatch OK
    stmt = defs.prepXX + """select
EXTRACT(DAY FROM date'2006-07-04') from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '4')
    defs.hkey = """SELECT EXTRACT ( DAY FROM DATE #NP# ) FROM TBL1R ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '323030302D30352D31350A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry13
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select
EXTRACT(HOUR FROM timestamp'1985-11-27 12:23:34') from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '12')

    # add entry14
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select
EXTRACT(MINUTE FROM timestamp'1995-01-21 23:34:45') from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '34')

    # add entry15
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select
EXTRACT(SECOND FROM timestamp'2005-09-02 00:45:56') from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '56')

    # add entry16
    stmt = defs.prepXX + """select
EXTRACT(DAY FROM timestamp'1975-11-27 16:17:18') from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '27')
    defs.hkey = """SELECT EXTRACT ( DAY FROM TIMESTAMP #NP# ) FROM TBL1R ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '313937352D31312D32372031363A31373A31380A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry17
    stmt = defs.prepXX + """select
EXTRACT(MONTH FROM timestamp'1993-11-01 13:43:13') from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '11')
    defs.hkey = """SELECT EXTRACT ( MONTH FROM TIMESTAMP #NP# ) FROM TBL1R ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '313939332D31312D30312031333A34333A31330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry18
    stmt = defs.prepXX + """select
EXTRACT(YEAR FROM timestamp'2015-09-18 00:37:23') from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '2015')
    defs.hkey = """SELECT EXTRACT ( YEAR FROM TIMESTAMP #NP# ) FROM TBL1R ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '323031352D30392D31382030303A33373A32330A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry13
    # expect = Found in HQC, HQC backpatch OK
    stmt = defs.prepXX + """select
EXTRACT(HOUR FROM timestamp'1975-11-27 16:17:18') from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '16')
    defs.hkey = """SELECT EXTRACT ( HOUR FROM TIMESTAMP #NP# ) FROM TBL1R ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '313938352D31312D32372031323A32333A33340A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry14
    # expect = Found in HQC, HQC backpatch OK
    stmt = defs.prepXX + """select
EXTRACT(MINUTE FROM timestamp'1993-11-01 13:43:13') from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '43')
    defs.hkey = ("""SELECT EXTRACT ( MINUTE FROM TIMESTAMP #NP# )""" +
                 """ FROM TBL1R ;""")
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '313939352D30312D32312032333A33343A34350A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry15
    # expect = Found in HQC, HQC backpatch OK
    stmt = defs.prepXX + """select
EXTRACT(SECOND FROM timestamp'2015-09-18 00:37:23') from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '23')
    defs.hkey = ("""SELECT EXTRACT ( SECOND FROM TIMESTAMP #NP# )""" +
                 """ FROM TBL1R ;""")
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '323030352D30392D30322030303A34353A35360A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    if defs.genexp == 0:
        # expect 18 HQC entries
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_selected_msg(output, '18')

    setup.resetHQC()

    # add entry19
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select colyr, coldate from F00
where colyr = EXTRACT(YEAR FROM coldate) order by coldate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'EXTRACT019')

    # add entry20
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select colmon, coldate from F00
where colmon = EXTRACT(MONTH FROM coldate) order by coldate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'EXTRACT020')

    # add entry21
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select colday, coldate from F00
where colday = EXTRACT(DAY FROM coldate) order by coldate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'EXTRACT021')

    # add entry22
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select colhr, colts from F00
where colhr = EXTRACT(HOUR FROM colts) order by colts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'EXTRACT022')

    # add entry23
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select colmin, colts from F00
where colmin = EXTRACT(MINUTE FROM colts) order by colts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'EXTRACT023')

    # add entry24
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select colsec, colts from F00
where colsec = EXTRACT(SECOND FROM colts) order by colts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'EXTRACT024')

    if defs.genexp == 0:
        # expect 6 HQC entries
        # expect num_hits = num_pliterals = num_npliterals = 0
        output = _dci.cmdexec("""execute show_entries;""")
        _dci.expect_file(output, defs.expfile, 'EXTRACTa2')

    setup.resetHQC()

    # add entry25
    stmt = defs.prepXX + """select colyr, coldate from F00
where colyr = EXTRACT(YEAR FROM date'1975-01-30');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'EXTRACT025')
    defs.hkey = ("""SELECT COLYR , COLDATE FROM F00""" +
                 """ WHERE COLYR = EXTRACT ( YEAR FROM DATE #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27313937352D30312D3330270A'
    setup.verifyHQCEntryExists()

    # add entry26
    stmt = defs.prepXX + """select colmon, coldate from F00
where colmon = EXTRACT(MONTH FROM date'1990-03-28');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'EXTRACT026')
    defs.hkey = ("""SELECT COLMON , COLDATE FROM F00""" +
                 """ WHERE COLMON = EXTRACT ( MONTH FROM DATE #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27313939302D30332D3238270A'
    setup.verifyHQCEntryExists()

    # add entry27
    stmt = defs.prepXX + """select colday, coldate from F00
where colday = EXTRACT(DAY FROM date'2000-05-21');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'EXTRACT027')
    defs.hkey = ("""SELECT COLDAY , COLDATE FROM F00""" +
                 """ WHERE COLDAY = EXTRACT ( DAY FROM DATE #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27323030302D30352D3231270A'
    setup.verifyHQCEntryExists()

    # add entry28
    stmt = defs.prepXX + """select colhr, colts from F00
where colhr = EXTRACT(HOUR FROM timestamp'1985-11-27 01:23:34');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'EXTRACT028')
    defs.hkey = ("""SELECT COLHR , COLTS FROM F00""" +
                 """ WHERE COLHR = EXTRACT ( HOUR FROM TIMESTAMP #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27313938352D31312D32372030313A32333A3334270A'
    setup.verifyHQCEntryExists()

    # add entry29
    stmt = defs.prepXX + """select colmin, colts from F00
where colmin = EXTRACT(MINUTE FROM timestamp'1995-01-21 23:52:45');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'EXTRACT029')
    defs.hkey = ("""SELECT COLMIN , COLTS FROM F00""" +
                 """ WHERE COLMIN =""" +
                 """ EXTRACT ( MINUTE FROM TIMESTAMP #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27313939352D30312D32312032333A35323A3435270A'
    setup.verifyHQCEntryExists()

    # add entry30
    stmt = defs.prepXX + """select colsec, colts from F00
where colsec = EXTRACT(SECOND FROM timestamp'2005-09-02 00:45:59');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'EXTRACT030')
    defs.hkey = ("""SELECT COLSEC , COLTS FROM F00""" +
                 """ WHERE COLSEC =""" +
                 """ EXTRACT ( SECOND FROM TIMESTAMP #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27323030352D30392D30322030303A34353A3539270A'
    setup.verifyHQCEntryExists()

    # increase hits, entry25
    stmt = defs.prepXX + """select colyr, coldate from F00
where colyr = EXTRACT(YEAR FROM date'1975-01-30');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'EXTRACT025')
    defs.hkey = ("""SELECT COLYR , COLDATE FROM F00""" +
                 """ WHERE COLYR = EXTRACT ( YEAR FROM DATE #NP# ) ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27313937352D30312D3330270A'
    setup.verifyHQCEntryExists()

    # increase hits, entry27
    stmt = defs.prepXX + """select colday, coldate from F00
where colday = EXTRACT(DAY FROM date'2000-05-21');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'EXTRACT027')
    defs.hkey = ("""SELECT COLDAY , COLDATE FROM F00""" +
                 """ WHERE COLDAY = EXTRACT ( DAY FROM DATE #NP# ) ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27323030302D30352D3231270A'
    setup.verifyHQCEntryExists()

    # increase hits, entry29
    stmt = defs.prepXX + """select colmin, colts from F00
where colmin = EXTRACT(MINUTE FROM timestamp'1995-01-21 23:52:45');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'EXTRACT029')
    defs.hkey = ("""SELECT COLMIN , COLTS FROM F00""" +
                 """ WHERE COLMIN =""" +
                 """ EXTRACT ( MINUTE FROM TIMESTAMP #NP# ) ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27313939352D30312D32312032333A35323A3435270A'
    setup.verifyHQCEntryExists()

    # add entry31
    # similar to entry27 hkey, but literals differ
    stmt = defs.prepXX + """select colday, coldate from F00
where colday = EXTRACT(DAY FROM date'2001-05-21');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'EXTRACT031')
    defs.hkey = ("""SELECT COLDAY , COLDATE FROM F00""" +
                 """ WHERE COLDAY = EXTRACT ( DAY FROM DATE #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27323030312D30352D3231270A'
    setup.verifyHQCEntryExists()

    # add entry32
    # similar to entry29 hkey, but literals differ
    stmt = defs.prepXX + """select colmin, colts from F00
where colmin = EXTRACT(MINUTE FROM timestamp'1995-01-21 22:52:43');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'EXTRACT032')
    defs.hkey = ("""SELECT COLMIN , COLTS FROM F00""" +
                 """ WHERE COLMIN =""" +
                 """ EXTRACT ( MINUTE FROM TIMESTAMP #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27313939352D30312D32312032323A35323A3433270A'
    setup.verifyHQCEntryExists()

    _testmgr.testcase_end(desc)


def test_juliants(desc="""juliantimestamp"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: juliantimestamp()"""

    # function: JULIANTIMESTAMP()
    # in result-set: HQC CACHEABLE, PARAMETERIZED
    # in where-clause: HQC CACHEABLE, NOT PARAMETERIZED

    setup.resetHQC()

    # add entry1
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select colkey,
JULIANTIMESTAMP(coldate) from F00 order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'JULIANTS001')
    defs.hkey = ("""SELECT COLKEY , JULIANTIMESTAMP ( COLDATE )""" +
                 """ FROM F00 ORDER BY COLKEY ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry2
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select colkey,
JULIANTIMESTAMP(colts) from F00 order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'JULIANTS002')
    defs.hkey = ("""SELECT COLKEY , JULIANTIMESTAMP ( COLTS )""" +
                 """ FROM F00 ORDER BY COLKEY ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry3
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select
JULIANTIMESTAMP(date'1980-01-30') from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'JULIANTS003')
    defs.hkey = ("""SELECT JULIANTIMESTAMP ( DATE #NP# ) FROM TBL1R ;""")
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '313938302D30312D33300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry3
    # expect = Found in HQC, HQC backpatch OK
    stmt = defs.prepXX + """select
JULIANTIMESTAMP(date'1986-12-25') from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'JULIANTS003a')
    defs.hkey = ("""SELECT JULIANTIMESTAMP ( DATE #NP# ) FROM TBL1R ;""")
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '313938302D30312D33300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry3
    # expect = Found in HQC, HQC backpatch OK
    stmt = defs.prepXX + """select
JULIANTIMESTAMP(date'1996-02-14') from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'JULIANTS003b')
    defs.hkey = ("""SELECT JULIANTIMESTAMP ( DATE #NP# ) FROM TBL1R ;""")
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '313938302D30312D33300A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry4
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select
JULIANTIMESTAMP(timestamp'1985-11-27 12:23:34') from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'JULIANTS004')
    defs.hkey = ("""SELECT JULIANTIMESTAMP ( TIMESTAMP #NP# )""" +
                 """ FROM TBL1R ;""")
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '313938352D31312D32372031323A32333A33340A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry4
    # expect = Found in HQC, HQC backpatch OK
    stmt = defs.prepXX + """select
JULIANTIMESTAMP(timestamp'2005-09-02 00:45:56') from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'JULIANTS004a')
    defs.hkey = ("""SELECT JULIANTIMESTAMP ( TIMESTAMP #NP# )""" +
                 """ FROM TBL1R ;""")
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '313938352D31312D32372031323A32333A33340A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry4
    # expect = Found in HQC, HQC backpatch OK
    stmt = defs.prepXX + """select
JULIANTIMESTAMP(timestamp'1993-11-01 13:43:13') from TBL1R;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'JULIANTS004b')
    defs.hkey = ("""SELECT JULIANTIMESTAMP ( TIMESTAMP #NP# )""" +
                 """ FROM TBL1R ;""")
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '313938352D31312D32372031323A32333A33340A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry5
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select * from F00
where coljdt = JULIANTIMESTAMP(coldate) order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'JULIANTS005')

    # add entry6
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select * from F00
where coljts = JULIANTIMESTAMP(colts) order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'JULIANTS006')

    # increase hits, entry5
    stmt = defs.prepXX + """select * from F00
where coljdt = JULIANTIMESTAMP(coldate) order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'JULIANTS005')
    defs.hkey = ("""SELECT * FROM F00""" +
                 """ WHERE COLJDT = JULIANTIMESTAMP ( COLDATE )""" +
                 """ ORDER BY COLKEY ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry6
    stmt = defs.prepXX + """select * from F00
where coljts = JULIANTIMESTAMP(colts) order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'JULIANTS006')
    defs.hkey = ("""SELECT * FROM F00""" +
                 """ WHERE COLJTS = JULIANTIMESTAMP ( COLTS )""" +
                 """ ORDER BY COLKEY ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry7
    stmt = defs.prepXX + """select * from F00
where coljdt = JULIANTIMESTAMP(date'1998-07-04');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'JULIANTS007')
    defs.hkey = ("""SELECT * FROM F00""" +
                 """ WHERE COLJDT = JULIANTIMESTAMP ( DATE #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27313939382D30372D3034270A'
    setup.verifyHQCEntryExists()

    # add entry8
    stmt = defs.prepXX + """select * from F00
where coljts = JULIANTIMESTAMP(timestamp'2004-11-27 00:00:00.123456');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'JULIANTS008')
    defs.hkey = ("""SELECT * FROM F00""" +
                 """ WHERE COLJTS = JULIANTIMESTAMP ( TIMESTAMP #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = ('27323030342D31312D323720' +
                       '30303A30303A30302E313233343536270A')
    setup.verifyHQCEntryExists()

    # add entry9
    stmt = defs.prepXX + """select * from F00
where coljdt = JULIANTIMESTAMP(date'1986-10-21');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'JULIANTS009')
    defs.hkey = ("""SELECT * FROM F00""" +
                 """ WHERE COLJDT = JULIANTIMESTAMP ( DATE #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27313938362D31302D3231270A'
    setup.verifyHQCEntryExists()

    # increase hits, entry7
    stmt = defs.prepXX + """select * from F00
where coljdt = JULIANTIMESTAMP(date'1998-07-04');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'JULIANTS007')
    defs.hkey = ("""SELECT * FROM F00""" +
                 """ WHERE COLJDT = JULIANTIMESTAMP ( DATE #NP# ) ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27313939382D30372D3034270A'
    setup.verifyHQCEntryExists()

    # increase hits, entry8
    stmt = defs.prepXX + """select * from F00
where coljts = JULIANTIMESTAMP(timestamp'2004-11-27 00:00:00.123456');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'JULIANTS008')
    defs.hkey = ("""SELECT * FROM F00""" +
                 """ WHERE COLJTS = JULIANTIMESTAMP ( TIMESTAMP #NP# ) ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = ('27323030342D31312D323720' +
                       '30303A30303A30302E313233343536270A')
    setup.verifyHQCEntryExists()

    # add entry10
    stmt = defs.prepXX + """select * from F00
where coljts = JULIANTIMESTAMP(timestamp'1975-12-25 17:52:45.987');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'JULIANTS010')
    defs.hkey = ("""SELECT * FROM F00""" +
                 """ WHERE COLJTS = JULIANTIMESTAMP ( TIMESTAMP #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27313937352D31322D32352031373A35323A34352E393837270A'
    setup.verifyHQCEntryExists()

    _testmgr.testcase_end(desc)
