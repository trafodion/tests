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

#ascii
#char
#insert
#lcase
#left
#locate
#lpad
#ltrim
#octet_length
#position
#repeat
#right
#rpad
#rtrim
#space
#ucase
#upshift

    setup.resetHQC()
    output = _dci.cmdexec("""drop table F00 cascade;""")
    output = _dci.cmdexec("""drop table F01 cascade;""")

    stmt = """create table F00(
colkey int not null,
collen int,
cval smallint,
colchriso char(25) character set iso88591,
colchrutf8 char(30) character set utf8,
colvchriso varchar(35) character set iso88591,
colvchrutf8 varchar(40) character set utf8)
primary key (colkey)
salt using 8 partitions;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into F00 values (1, NULL, NULL,
'Pennsylvannia', 'New Hampshire', 'South Dakota', 'California');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, '1')

    stmt = """create table F01 like F00 with partitions;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into F01 (colkey, collen, colchriso, colchrutf8,
colvchriso, colvchrutf8) values
(1, 8, 'New York', 'New York', 'New York', 'New York'),
(2, 7, 'chicago', 'chicago', 'chicago', 'chicago'),
(3, 7, 'seattle', 'seattle', 'seattle', 'seattle'),
(4, 11, 'ALBUQUERQUE', 'ALBUQUERQUE', 'ALBUQUERQUE', 'ALBUQUERQUE'),
(5, 12, 'JACKSONVILLE', 'JACKSONVILLE', 'JACKSONVILLE', 'JACKSONVILLE'),
(6, 6, 'BOSTON', 'BOSTON', 'BOSTON', 'BOSTON'),
(7, 7, 'houston', 'HOUSTON', 'HOUSTON', 'houston'),
(8, 6, 'dallas', 'dallas', 'dallas', 'dallas'),
(9, 11, 'TALLAHASSEE', 'TALLAHASSEE', 'TALLAHASSEE', 'TALLAHASSEE'),
(10, 8, 'Portland', 'Portland', 'Portland', 'Portland'),
(11, 11,'Los Angeles', 'Los Angeles', 'Los Angeles', 'LOS ANGELES'),
(12, 13, 'San Francisco', 'San Francisco', 'San Francisco', 'San Francisco'),
(13, 10, 'SACRAMENTO', 'sacramento', 'sacramento', 'SACRAMENTO'),
(14, 9, 'St. Louis', 'St. Louis', 'St. Louis', 'St. Louis'),
(15, 24, 'WINCHESTER-ON-THE-SEVERN', 'Winchester-On-The-Severn',
'Winchester-On-The-Severn', 'WINCHESTER-ON-THE-SEVERN'),
(16, 17, 'mooseLOOKmegUNTIC', 'MOOSElookMEGuntic', 'mooseLOOKMEGuntic',
'MOOSElookmegUNTIC'),
(17, NULL,'1234567890123456789012345', '123456789012345678901234567890',
'12345678901234567890123456789012345',
'1234567890123456789012345678901234567890');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, '17')
    stmt = """update F01 set cval = CODE_VALUE(colchriso);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, '17')
    #setup.verifyHQCempty()
    stmt = """select * from F01 order by colkey;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table F02_CISO(
cola char(11) character set iso88591,
colb char(11) character set iso88591,
colc char(22) character set iso88591);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into F02_CISO values
('BOOT', 'leg', 'BOOTleg'),
('fire', 'place', 'fireplace'),
('through', 'put', 'throughput'),
('cccccc', 'aaaa', 'bbbbb'),
('table', 'spoon', 'tablespoon'),
('side', 'STEP', 'sideSTEP');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, '6')

    stmt = """create table F02_CUTF8(
cola char(11) character set utf8,
colb char(11) character set utf8,
colc char(22) character set utf8);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into F02_CUTF8 values
('BOOT', 'leg', 'BOOTleg'),
('fire', 'place', 'fireplace'),
('through', 'put', 'throughput'),
('cccccc', 'aaaa', 'bbbbb'),
('table', 'spoon', 'tablespoon'),
('side', 'STEP', 'sideSTEP');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, '6')

    stmt = """create table F02_VISO(
cola varchar(11) character set iso88591,
colb varchar(11) character set iso88591,
colc varchar(22) character set iso88591);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into F02_VISO values
('BOOT', 'leg', 'BOOTleg'),
('fire', 'place', 'fireplace'),
('through', 'put', 'throughput'),
('cccccc', 'aaaa', 'bbbbb'),
('table', 'spoon', 'tablespoon'),
('side', 'STEP', 'sideSTEP');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, '6')

    stmt = """create table F02_VUTF8(
cola varchar(11) character set utf8,
colb varchar(11) character set utf8,
colc varchar(22) character set utf8);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into F02_VUTF8 values
('BOOT', 'leg', 'BOOTleg'),
('fire', 'place', 'fireplace'),
('through', 'put', 'throughput'),
('cccccc', 'aaaa', 'bbbbb'),
('table', 'spoon', 'tablespoon'),
('side', 'STEP', 'sideSTEP');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, '6')


def test_charlen(desc="""char_length()"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: char_length()"""

    ### function: CHAR_LENGTH, CHARACTER_LENGTH
    ### in result set: HQC CACHEABLE & PARAMETERIZED
    ### in where clause: HQC CACHEABLE & NOT PARAMETERIZED

    setup.resetHQC()
    # HQC::AddEntry(): passed
    stmt = defs.prepXX + """select CHAR_LENGTH(colchrutf8) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '30')
    defs.hkey = ("""SELECT CHAR_LENGTH ( COLCHRUTF8 ) FROM F00 ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # HQC::AddEntry(): passed
    stmt = defs.prepXX + """select CHAR_LENGTH('Mississippi') from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '11')
    defs.hkey = """SELECT CHAR_LENGTH ( #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '274D69737369737369707069270A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # Found in HQC, HQC backpatch OK
    stmt = defs.prepXX + """select CHAR_LENGTH('Louisiana') from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '9')
    defs.hkey = """SELECT CHAR_LENGTH ( #NP# ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '274D69737369737369707069270A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # Found in HQC, HQC backpatch OK
    stmt = defs.prepXX + """select CHAR_LENGTH(colchrutf8) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '30')
    defs.hkey = ("""SELECT CHAR_LENGTH ( COLCHRUTF8 ) FROM F00 ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # Found in HQC, HQC backpatch OK
    stmt = defs.prepXX + """select CHAR_LENGTH('KENTUCKY') from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '8')
    defs.hkey = """SELECT CHAR_LENGTH ( #NP# ) FROM F00 ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '274D69737369737369707069270A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # Found in HQC, HQC backpatch OK
    stmt = defs.prepXX + """select CHAR_LENGTH('IDAHO') from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '5')
    defs.hkey = """SELECT CHAR_LENGTH ( #NP# ) FROM F00 ;"""
    defs.num_hits = 3
    defs.num_pliterals = 1
    defs.pliterals = '274D69737369737369707069270A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # HQC::AddEntry(): passed
    stmt = defs.prepXX + """select CHAR_LENGTH(colvchriso) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '12')
    defs.hkey = ("""SELECT CHAR_LENGTH ( COLVCHRISO ) FROM F00 ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # HQC::AddEntry(): passed
    stmt = defs.prepXX + """select CHAR_LENGTH(colvchrutf8) from F00 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '10')
    defs.hkey = ("""SELECT CHAR_LENGTH ( COLVCHRUTF8 ) FROM F00 ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # HQC::AddEntry(): passed
    stmt = defs.prepXX + """select CHAR_LENGTH(colchriso) from F00 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '25')
    defs.hkey = ("""SELECT CHAR_LENGTH ( COLCHRISO ) FROM F00 ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    setup.resetHQC()

    # CHAR_LENGTH in where-clause
    # HQC Cacheable but not parameterized
    # add HQC entry1
    stmt = defs.prepXX + """select * from F01
where collen = CHAR_LENGTH(colvchrutf8) order by collen, colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CHRLEN001')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE COLLEN = CHAR_LENGTH ( COLVCHRUTF8 )""" +
                 """ ORDER BY COLLEN , COLKEY ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add HQC entry2, not parameterized
    stmt = defs.prepXX + """select * from F01
where collen = CHAR_LENGTH('CHICAGO');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '2 * 7 * 99 chicago*')
    _dci.expect_any_substr(output, '3 * 7 * 115 seattle*')
    _dci.expect_any_substr(output, '7 * 7 * 104 houston*')     
    _dci.expect_selected_msg(output, '3')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE COLLEN = CHAR_LENGTH ( #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '274348494341474F270A'
    setup.verifyHQCEntryExists()

    # Add HQC entry3, not parameterized
    stmt = defs.prepXX + """select * from F01
where collen = CHAR_LENGTH('new york');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '1 * 8 * 78 New York * New York * New York * New York')
    _dci.expect_any_substr(output, '10 * 8 * 80 Portland * Portland * Portland * Portland')
    _dci.expect_selected_msg(output, '2')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE COLLEN = CHAR_LENGTH ( #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '276E657720796F726B270A'
    setup.verifyHQCEntryExists()

    # Seattle has same # of letters as Chicago
    # Add HQC entry4, not parameterized
    stmt = defs.prepXX + """select * from F01
where collen = CHAR_LENGTH('Seattle');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '2 * 7 * 99 chicago*')
    _dci.expect_any_substr(output, '3 * 7 * 115 seattle*')
    _dci.expect_any_substr(output, '7 * 7 * 104 houston*')
    _dci.expect_selected_msg(output, '3')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE COLLEN = CHAR_LENGTH ( #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2753656174746C65270A'
    setup.verifyHQCEntryExists()

    #San Jose has same # of letters as New York
    # Add HQC entry5, not parameterized
    stmt = defs.prepXX + """select * from F01
where collen = CHAR_LENGTH('San Jose');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '1 * 8 * 78 New York*')
    _dci.expect_any_substr(output, '10 * 8 * 80 Portland*')
    _dci.expect_selected_msg(output, '2')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE COLLEN = CHAR_LENGTH ( #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2753616E204A6F7365270A'
    setup.verifyHQCEntryExists()

    # should have been cached previously
    # increase num hits, entry2
    stmt = defs.prepXX + """select * from F01
where collen = CHAR_LENGTH('CHICAGO');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '2 * 7 * 99 chicago*')
    _dci.expect_any_substr(output, '3 * 7 * 115 seattle*')
    _dci.expect_any_substr(output, '7 * 7 * 104 houston*')     
    _dci.expect_selected_msg(output, '3')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE COLLEN = CHAR_LENGTH ( #NP# ) ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '274348494341474F270A'
    setup.verifyHQCEntryExists()

    # Add HQC entry6, not parameterized
    stmt = defs.prepXX + """select * from F01
where collen = CHAR_LENGTH('chicago');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '2 * 7 * 99 chicago*')
    _dci.expect_any_substr(output, '3 * 7 * 115 seattle*')
    _dci.expect_any_substr(output, '7 * 7 * 104 houston*')     
    _dci.expect_selected_msg(output, '3')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE COLLEN = CHAR_LENGTH ( #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '276368696361676F270A'
    setup.verifyHQCEntryExists()

    # Add HQC entry7, not parameterized
    stmt = defs.prepXX + """select * from F01
where collen = CHAR_LENGTH('NEW York');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '1 * 8 * 78 New York*')
    _dci.expect_any_substr(output, '10 * 8 * 80 Portland*')
    _dci.expect_selected_msg(output, '2')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE COLLEN = CHAR_LENGTH ( #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '274E455720596F726B270A'
    setup.verifyHQCEntryExists()

    # Add HQC entry8, not parameterized
    stmt = defs.prepXX + """select * from F01
where CHAR_LENGTH(colchrutf8) = 30;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '17')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE CHAR_LENGTH ( COLCHRUTF8 ) = #NP# ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '33300A'
    setup.verifyHQCEntryExists()

    # Add HQC entry9, not parameterized
    stmt = defs.prepXX + """select * from F01
where CHAR_LENGTH(colchrutf8) = 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE CHAR_LENGTH ( COLCHRUTF8 ) = #NP# ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '32350A'
    setup.verifyHQCEntryExists()

    # increase hits, entry8, not parameterized
    stmt = defs.prepXX + """select * from F01
where CHAR_LENGTH(colchrutf8) = 30;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '17')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE CHAR_LENGTH ( COLCHRUTF8 ) = #NP# ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '33300A'
    setup.verifyHQCEntryExists()

    # increase hits, entry9, not parameterized
    stmt = defs.prepXX + """select * from F01
where CHAR_LENGTH(colchrutf8) = 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE CHAR_LENGTH ( COLCHRUTF8 ) = #NP# ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '32350A'
    setup.verifyHQCEntryExists()

    # Add HQC entry10, not parameterized
    stmt = defs.prepXX + """select * from F01
where CHAR_LENGTH(colvchrutf8) = 11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '4 * 11 * 65 ALBUQUERQUE')
    _dci.expect_any_substr(output, '9 * 11 * 84 TALLAHASSEE')
    _dci.expect_any_substr(output, '11 * 11 * 76 Los Angeles')
    _dci.expect_selected_msg(output, '3')
    # increase hits, entry10
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '4 * 11 * 65 ALBUQUERQUE')
    _dci.expect_any_substr(output, '9 * 11 * 84 TALLAHASSEE')
    _dci.expect_any_substr(output, '11 * 11 * 76 Los Angeles')
    _dci.expect_selected_msg(output, '3')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE CHAR_LENGTH ( COLVCHRUTF8 ) = #NP# ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '31310A'
    setup.verifyHQCEntryExists()

    # Add HQC entry11, not parameterized
    stmt = defs.prepXX + """select * from F01
where CHAR_LENGTH(colvchrutf8) = 24;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, '15 * 24 * 87 WINCHESTER-ON-THE-SEVERN')
    _dci.expect_selected_msg(output, '1')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE CHAR_LENGTH ( COLVCHRUTF8 ) = #NP# ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '32340A'
    setup.verifyHQCEntryExists()

    setup.resetHQC()

    # hqc cache key constructed uses the text of the query as entered by
    # the user, so CHAR_LENGTH and CHARACTER_LENGTH are different and do NOT
    # match. But SQC uses a common name for them. If you intermingle queries
    # ith CHAR_LENGTH and CHARACTER_LENGTH, you may not see queries in hqc
    # log because hqc does not match the query, but then the query is picked
    # up by SQC, so we do not get to the code that will attempt to insert the
    # new query to the hqc cache.

    # HQC::AddEntry(): passed
    stmt = defs.prepXX + """select CHARACTER_LENGTH(colchrutf8) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '30')
    defs.hkey = ("""SELECT CHARACTER_LENGTH ( COLCHRUTF8 ) FROM F00 ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # HQC::AddEntry(): passed
    stmt = defs.prepXX + """select CHARACTER_LENGTH('Mississippi') from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '11')
    defs.hkey = """SELECT CHARACTER_LENGTH ( #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '274D69737369737369707069270A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # Found in HQC, HQC backpatch OK
    stmt = defs.prepXX + """select CHARACTER_LENGTH('Louisiana') from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '9')
    defs.hkey = """SELECT CHARACTER_LENGTH ( #NP# ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '274D69737369737369707069270A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # Found in HQC, HQC backpatch OK
    stmt = defs.prepXX + """select CHARACTER_LENGTH(colchrutf8) from F00 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '30')
    defs.hkey = ("""SELECT CHARACTER_LENGTH ( COLCHRUTF8 ) FROM F00 ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # Found in HQC, HQC backpatch OK
    stmt = defs.prepXX + """select CHARACTER_LENGTH('KENTUCKY') from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '8')
    defs.hkey = """SELECT CHARACTER_LENGTH ( #NP# ) FROM F00 ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '274D69737369737369707069270A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # Found in HQC, HQC backpatch OK
    stmt = defs.prepXX + """select CHARACTER_LENGTH('IDAHO') from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '5')
    defs.hkey = """SELECT CHARACTER_LENGTH ( #NP# ) FROM F00 ;"""
    defs.num_hits = 3
    defs.num_pliterals = 1
    defs.pliterals = '274D69737369737369707069270A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # HQC::AddEntry(): passed
    stmt = defs.prepXX + """select CHARACTER_LENGTH(colvchriso) from F00 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '12')
    defs.hkey = ("""SELECT CHARACTER_LENGTH ( COLVCHRISO ) FROM F00 ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # HQC::AddEntry(): passed
    stmt = defs.prepXX + """select CHARACTER_LENGTH(colvchrutf8) from F00 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '10')
    defs.hkey = ("""SELECT CHARACTER_LENGTH ( COLVCHRUTF8 ) FROM F00 ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # HQC::AddEntry(): passed
    stmt = defs.prepXX + """select CHARACTER_LENGTH(colchriso) from F00 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '25')
    defs.hkey = ("""SELECT CHARACTER_LENGTH ( COLCHRISO ) FROM F00 ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    setup.resetHQC()

    # CHARACTER_LENGTH in where-clause
    # HQC Cacheable but not parameterized
    # add HQC entry1
    stmt = defs.prepXX + """select * from F01
where collen = CHARACTER_LENGTH(colvchrutf8) order by collen, colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CHRLEN001')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE COLLEN = CHARACTER_LENGTH ( COLVCHRUTF8 )""" +
                 """ ORDER BY COLLEN , COLKEY ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add HQC entry2, not parameterized
    stmt = defs.prepXX + """select * from F01
where collen = CHARACTER_LENGTH('CHICAGO');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CHRLEN002')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE COLLEN = CHARACTER_LENGTH ( #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '274348494341474F270A'
    setup.verifyHQCEntryExists()

    # Add HQC entry3, not parameterized
    stmt = defs.prepXX + """select * from F01
where collen = CHARACTER_LENGTH('new york');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CHRLEN003')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE COLLEN = CHARACTER_LENGTH ( #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '276E657720796F726B270A'
    setup.verifyHQCEntryExists()

    # Seattle has same # of letters as Chicago
    # Add HQC entry4, not parameterized
    stmt = defs.prepXX + """select * from F01
where collen = CHARACTER_LENGTH('Seattle');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CHRLEN004')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE COLLEN = CHARACTER_LENGTH ( #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2753656174746C65270A'
    setup.verifyHQCEntryExists()

    #San Jose has same # of letters as New York
    # Add HQC entry5, not parameterized
    stmt = defs.prepXX + """select * from F01
where collen = CHARACTER_LENGTH('San Jose');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CHRLEN005')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE COLLEN = CHARACTER_LENGTH ( #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2753616E204A6F7365270A'
    setup.verifyHQCEntryExists()

    # should have been cached previously
    # increase num hits, entry2
    stmt = defs.prepXX + """select * from F01
where collen = CHARACTER_LENGTH('CHICAGO');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CHRLEN002')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE COLLEN = CHARACTER_LENGTH ( #NP# ) ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '274348494341474F270A'
    setup.verifyHQCEntryExists()

    # Add HQC entry6, not parameterized
    stmt = defs.prepXX + """select * from F01
where collen = CHARACTER_LENGTH('chicago');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CHRLEN002')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE COLLEN = CHARACTER_LENGTH ( #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '276368696361676F270A'
    setup.verifyHQCEntryExists()

    # Add HQC entry7, not parameterized
    stmt = defs.prepXX + """select * from F01
where collen = CHARACTER_LENGTH('NEW York');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CHRLEN006')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE COLLEN = CHARACTER_LENGTH ( #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '274E455720596F726B270A'
    setup.verifyHQCEntryExists()

    # Add HQC entry8, not parameterized
    stmt = defs.prepXX + """select * from F01
where CHARACTER_LENGTH(colchrutf8) = 30;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CHRLEN007')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE CHARACTER_LENGTH ( COLCHRUTF8 ) = #NP# ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '33300A'
    setup.verifyHQCEntryExists()

    # Add HQC entry9, not parameterized
    stmt = defs.prepXX + """select * from F01
where CHARACTER_LENGTH(colchrutf8) = 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE CHARACTER_LENGTH ( COLCHRUTF8 ) = #NP# ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '32350A'
    setup.verifyHQCEntryExists()

    # increase hits, entry8, not parameterized
    stmt = defs.prepXX + """select * from F01
where CHARACTER_LENGTH(colchrutf8) = 30;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CHRLEN007')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE CHARACTER_LENGTH ( COLCHRUTF8 ) = #NP# ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '33300A'
    setup.verifyHQCEntryExists()

    # increase hits, entry9, not parameterized
    stmt = defs.prepXX + """select * from F01
where CHARACTER_LENGTH(colchrutf8) = 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_selected_msg(output, '0')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE CHARACTER_LENGTH ( COLCHRUTF8 ) = #NP# ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '32350A'
    setup.verifyHQCEntryExists()

    # Add HQC entry10, not parameterized
    stmt = defs.prepXX + """select * from F01
where CHARACTER_LENGTH(colvchrutf8) = 11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CHRLEN008')
    # increase hits, entry10
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CHRLEN008')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE CHARACTER_LENGTH ( COLVCHRUTF8 ) = #NP# ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '31310A'
    setup.verifyHQCEntryExists()

    # Add HQC entry11, not parameterized
    stmt = defs.prepXX + """select * from F01
where CHARACTER_LENGTH(colvchrutf8) = 24;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CHRLEN009')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE CHARACTER_LENGTH ( COLVCHRUTF8 ) = #NP# ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '32340A'
    setup.verifyHQCEntryExists()

    _testmgr.testcase_end(desc)


def test_codeval(desc="""code_value()"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: code_value()"""

    ### function: CODE_VALUE()
    ### in result set: HQC CACHEABLE & PARAMETERIZED
    ### in where clause: HQC CACHEABLE & NOT PARAMETERIZED

    setup.resetHQC()
    # HQC::AddEntry(): passed
    stmt = defs.prepXX + """select colkey, CODE_VALUE(colchriso), COLCHRISO
from F01 order by 1,2,3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CODEVAL001')
    defs.hkey = ("""SELECT COLKEY , CODE_VALUE ( COLCHRISO ) , COLCHRISO"""
                 + """ FROM F01 ORDER BY #NP# , #NP# , #NP# ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 3
    defs.npliterals = '310A320A330A'
    setup.verifyHQCEntryExists()

    # HQC::AddEntry(): passed
    stmt = defs.prepXX + """select colchrutf8, CODE_VALUE(colchrutf8) from F01
order by colchrutf8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CODEVAL002')
    defs.hkey = ("""SELECT COLCHRUTF8 , CODE_VALUE ( COLCHRUTF8 )""" +
                 """ FROM F01 ORDER BY COLCHRUTF8 ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # HQC::AddEntry(): passed
    stmt = defs.prepXX + """select colvchriso, CODE_VALUE(colvchriso) from F01
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CODEVAL003')
    defs.hkey = ("""SELECT COLVCHRISO , CODE_VALUE ( COLVCHRISO )"""
                 + """ FROM F01 ORDER BY #NP# ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '310A'
    setup.verifyHQCEntryExists()

    # HQC::AddEntry(): passed
    stmt = defs.prepXX + """select colvchrutf8, CODE_VALUE(colvchrutf8)
from F01 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CODEVAL004')
    defs.hkey = ("""SELECT COLVCHRUTF8 , CODE_VALUE ( COLVCHRUTF8 )"""
                 + """ FROM F01 ORDER BY #NP# ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.pliterals = '310A'
    setup.verifyHQCEntryExists()

    # HQC::AddEntry(): passed
    stmt = defs.prepXX + """select CODE_VALUE('Mississippi') from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '77')
    defs.hkey = """SELECT CODE_VALUE ( #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = '274D69737369737369707069270A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # Found in HQC, HQC backpatch OK
    stmt = defs.prepXX + """select CODE_VALUE('Louisiana') from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '76')
    defs.hkey = """SELECT CODE_VALUE ( #NP# ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = '274D69737369737369707069270A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # Found in HQC, HQC backpatch OK
    stmt = defs.prepXX + """select colvchrutf8, CODE_VALUE(colvchrutf8)
from F01 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CODEVAL004')
    defs.hkey = ("""SELECT COLVCHRUTF8 , CODE_VALUE ( COLVCHRUTF8 )"""
                 + """ FROM F01 ORDER BY #NP# ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '310A'
    setup.verifyHQCEntryExists()

    # Found in HQC, HQC backpatch OK
    stmt = (defs.prepXX + """select CODE_VALUE('KENTUCKY') from F00 ;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '75')
    defs.hkey = """SELECT CODE_VALUE ( #NP# ) FROM F00 ;"""
    defs.num_hits = 2
    defs.num_pliterals = 1
    defs.pliterals = '274D69737369737369707069270A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # Found in HQC, HQC backpatch OK
    stmt = defs.prepXX + """select CODE_VALUE('IDAHO') from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, '73')
    defs.hkey = """SELECT CODE_VALUE ( #NP# ) FROM F00 ;"""
    defs.num_hits = 3
    defs.num_pliterals = 1
    defs.pliterals = '274D69737369737369707069270A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    setup.resetHQC()

    # CODE_VALUE in where-clause
    # HQC Cacheable but not parameterized
    # add HQC entry1
    stmt = defs.prepXX + """select colchrutf8 from F01
where CODE_VALUE(colvchrutf8)  = 83 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CODEVAL005')
    defs.hkey = ("""SELECT COLCHRUTF8 FROM F01""" +
                 """ WHERE CODE_VALUE ( COLVCHRUTF8 ) = #NP#""" +
                 """ ORDER BY #NP# ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '38330A310A'
    setup.verifyHQCEntryExists()

    # add HQC entry2, not parameterized
    stmt = defs.prepXX + """select * from F01
where cval = CODE_VALUE('Washington') order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CODEVAL006')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE CVAL = CODE_VALUE ( #NP# )""" +
                 """ ORDER BY COLKEY ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2757617368696E67746F6E270A'
    setup.verifyHQCEntryExists()

    # Add HQC entry3, not parameterized
    stmt = defs.prepXX + """select * from F01
where cval = CODE_VALUE('Madison') order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CODEVAL007')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE CVAL = CODE_VALUE ( #NP# )""" +
                 """ ORDER BY COLKEY ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '274D616469736F6E270A'
    setup.verifyHQCEntryExists()

    # should have been cached previously
    # increase hits, entry1
    stmt = defs.prepXX + """select colchrutf8 from F01
where CODE_VALUE(colvchrutf8)  = 83 order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CODEVAL005')
    defs.hkey = ("""SELECT COLCHRUTF8 FROM F01""" +
                 """ WHERE CODE_VALUE ( COLVCHRUTF8 ) = #NP#""" +
                 """ ORDER BY #NP# ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '38330A310A'
    setup.verifyHQCEntryExists()

    # increase num hits, entry2
    stmt = defs.prepXX + """select * from F01
where cval = CODE_VALUE('Washington') order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CODEVAL006')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE CVAL = CODE_VALUE ( #NP# )""" +
                 """ ORDER BY COLKEY ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2757617368696E67746F6E270A'
    setup.verifyHQCEntryExists()

    # increase hits, entry3
    stmt = defs.prepXX + """select * from F01
where cval = CODE_VALUE('Madison') order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CODEVAL007')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE CVAL = CODE_VALUE ( #NP# )""" +
                 """ ORDER BY COLKEY ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '274D616469736F6E270A'
    setup.verifyHQCEntryExists()

    # Add HQC entry4, not parameterized
    stmt = defs.prepXX + """select * from F01
where CODE_VALUE(colvchrutf8) = 84;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CODEVAL008')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE CODE_VALUE ( COLVCHRUTF8 ) = #NP# ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '38340A'
    setup.verifyHQCEntryExists()

    # Add HQC entry5, not parameterized
    stmt = defs.prepXX + """select * from F01
where CODE_VALUE(colvchrutf8) = 72;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CODEVAL011')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE CODE_VALUE ( COLVCHRUTF8 ) = #NP# ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '37320A'
    setup.verifyHQCEntryExists()

    # increase hits, entry4, not parameterized
    stmt = defs.prepXX + """select * from F01
where CODE_VALUE(colvchrutf8) = 84;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CODEVAL008')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE CODE_VALUE ( COLVCHRUTF8 ) = #NP# ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '38340A'
    setup.verifyHQCEntryExists()

    # increase hits, entry9, not parameterized
    stmt = defs.prepXX + """select * from F01
where CODE_VALUE(colvchrutf8) = 72;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CODEVAL011')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE CODE_VALUE ( COLVCHRUTF8 ) = #NP# ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '37320A'
    setup.verifyHQCEntryExists()

    # Add HQC entry10, not parameterized
    stmt = defs.prepXX + """select * from F01
where CODE_VALUE(colchrutf8) = 80;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CODEVAL009')
    # increase hits, entry10
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CODEVAL009')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE CODE_VALUE ( COLCHRUTF8 ) = #NP# ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '38300A'
    setup.verifyHQCEntryExists()

    # Add HQC entry11, not parameterized
    stmt = defs.prepXX + """select * from F01
where CODE_VALUE(colvchriso) = 77;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CODEVAL010')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE CODE_VALUE ( COLVCHRISO ) = #NP# ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '37370A'
    setup.verifyHQCEntryExists()

    _testmgr.testcase_end(desc)


def test_concat(desc="""concat()"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: concat()"""

    ### function: CONCAT()
    ### HQC CACHEABLE, NOT PARAMETERIZED

    setup.resetHQC()

    # add entry1
    stmt = defs.prepXX + """select CONCAT('a1b2c3', colchriso) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT001')
    defs.hkey = """SELECT CONCAT ( #NP# , COLCHRISO ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27613162326333270A'
    setup.verifyHQCEntryExists()

    # add entry2
    stmt = defs.prepXX + """select CONCAT('a1b2c3d4e5', colchriso) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT002')
    defs.hkey = """SELECT CONCAT ( #NP# , COLCHRISO ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27613162326333270A'
    setup.verifyHQCEntryExists()

    # add entry3
    stmt = defs.prepXX + """select CONCAT('AB DE_', colchrutf8) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT003')
    defs.hkey = """SELECT CONCAT ( #NP# , COLCHRUTF8 ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2741422044455F270A'
    setup.verifyHQCEntryExists()

    # add entry4
    stmt = defs.prepXX + """select CONCAT('aaaaa', colchrutf8) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT004')
    defs.hkey = """SELECT CONCAT ( #NP# , COLCHRUTF8 ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2741422044455F270A'
    setup.verifyHQCEntryExists()

    # add entry5
    stmt = defs.prepXX + """select colkey, CONCAT('112233', colvchriso)
from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT005')
    defs.hkey = """SELECT COLKEY , CONCAT ( #NP# , COLVCHRISO ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27313132323333270A'
    setup.verifyHQCEntryExists()

    # add entry6
    stmt = defs.prepXX + """select colkey, CONCAT('a1b2c3d4e5', colvchriso)
from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT006')
    defs.hkey = """SELECT COLKEY , CONCAT ( #NP# , COLVCHRISO ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27313132323333270A'
    setup.verifyHQCEntryExists()

    # add entry7
    stmt = defs.prepXX + """select colkey, CONCAT('AB12  ', colvchrutf8)
from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT007')
    defs.hkey = """SELECT COLKEY , CONCAT ( #NP# , COLVCHRUTF8 ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27414231322020270A'
    setup.verifyHQCEntryExists()

    # add entry8
    stmt = defs.prepXX + """select colkey,CONCAT('aaaaa', colvchrutf8)
from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT008')
    defs.hkey = """SELECT COLKEY , CONCAT ( #NP# , COLVCHRUTF8 ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27414231322020270A'
    setup.verifyHQCEntryExists()

    # add entry9
    stmt = defs.prepXX + """select CONCAT(colchriso, '- XYZxyz') from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT009')
    defs.hkey = """SELECT CONCAT ( COLCHRISO , #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '272D2058595A78797A270A'
    setup.verifyHQCEntryExists()

    # add entry10
    stmt = defs.prepXX + """select CONCAT(colchrutf8, 'xyz') from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT010')
    defs.hkey = """SELECT CONCAT ( COLCHRUTF8 , #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2778797A270A'
    setup.verifyHQCEntryExists()

    # add entry11
    stmt = defs.prepXX + """select colkey, CONCAT(colvchriso, 'x1y2z3')
from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT011')
    defs.hkey = """SELECT COLKEY , CONCAT ( COLVCHRISO , #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27783179327A33270A'
    setup.verifyHQCEntryExists()

    # add entry12
    stmt = defs.prepXX + """select colkey, CONCAT(colvchrutf8, '=7890123')
from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT012')
    defs.hkey = """SELECT COLKEY , CONCAT ( COLVCHRUTF8 , #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '273D37383930313233270A'
    setup.verifyHQCEntryExists()

   # add entry13
    stmt = defs.prepXX + """select colkey, CONCAT('happy ', 'birthday!')
from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT013')
    defs.hkey = """SELECT COLKEY , CONCAT ( #NP# , #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '27686170707920270A27626972746864617921270A'
    setup.verifyHQCEntryExists()

    # add entry14
    stmt = defs.prepXX + """select colkey, CONCAT('iggie ', 'biggie pop')
from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT014')
    defs.hkey = """SELECT COLKEY , CONCAT ( #NP# , #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '27696767696520270A2762696767696520706F70270A'
    setup.verifyHQCEntryExists()

    # add entry15
    # increase hits, entry15
    stmt = defs.prepXX + """select * from F01
where colchriso = CONCAT('JACKSON', 'VILLE');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT015')
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT015')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE COLCHRISO = CONCAT ( #NP# , #NP# ) ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '274A41434B534F4E270A2756494C4C45270A'
    setup.verifyHQCEntryExists()

    # add entry16
    # increase hits, entry16
    stmt = defs.prepXX + """select * from F01
where colchrutf8 = CONCAT('PORT', 'LAND');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT016')
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT016')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE COLCHRUTF8 = CONCAT ( #NP# , #NP# ) ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '27504F5254270A274C414E44270A'
    setup.verifyHQCEntryExists()

    # add entry17
    # increase hits, entry17
    stmt = defs.prepXX + """select * from F01
where colvchriso = CONCAT('BOS', 'TON');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT017')
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT017')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE COLVCHRISO = CONCAT ( #NP# , #NP# ) ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '27424F53270A27544F4E270A'
    setup.verifyHQCEntryExists()

    # add entry18
    stmt = defs.prepXX + """select * from F01
where colvchrutf8 = CONCAT('JACKSON', 'VILLE');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT018')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE COLVCHRUTF8 = CONCAT ( #NP# , #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '274A41434B534F4E270A2756494C4C45270A'
    setup.verifyHQCEntryExists()

    # add entry19
    stmt = defs.prepXX + """select * from F02_CISO
where colc = CONCAT('through', colb);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT019')
    defs.hkey = ("""SELECT * FROM F02_CISO""" +
                 """ WHERE COLC = CONCAT ( #NP# , COLB ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '277468726F756768270A'
    setup.verifyHQCEntryExists()

    # add entry20
    stmt = defs.prepXX + """select * from F02_CISO
where colc = CONCAT(cola, 'leg');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT020')
    defs.hkey = ("""SELECT * FROM F02_CISO""" +
                 """ WHERE COLC = CONCAT ( COLA , #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '276C6567270A'
    setup.verifyHQCEntryExists()

    # add entry21
    stmt = defs.prepXX + """select * from F02_CISO
where colc = CONCAT(cola, colb);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT021')
    defs.hkey = ("""SELECT * FROM F02_CISO""" +
                 """ WHERE COLC = CONCAT ( COLA , COLB ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry22
    stmt = defs.prepXX + """select * from F02_CUTF8
where colc = CONCAT('through', colb);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT022')
    defs.hkey = ("""SELECT * FROM F02_CUTF8""" +
                 """ WHERE COLC = CONCAT ( #NP# , COLB ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '277468726F756768270A'
    setup.verifyHQCEntryExists()

    # add entry23
    stmt = defs.prepXX + """select * from F02_CUTF8
where colc = CONCAT(cola, 'leg');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT023')
    defs.hkey = ("""SELECT * FROM F02_CUTF8""" +
                 """ WHERE COLC = CONCAT ( COLA , #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '276C6567270A'
    setup.verifyHQCEntryExists()

    # add entry24
    stmt = defs.prepXX + """select * from F02_CUTF8
where colc = CONCAT(cola, colb);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT024')
    defs.hkey = ("""SELECT * FROM F02_CUTF8""" +
                 """ WHERE COLC = CONCAT ( COLA , COLB ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry25
    stmt = defs.prepXX + """select * from F02_VISO
where colc = CONCAT('table', colb);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT025')
    defs.hkey = ("""SELECT * FROM F02_VISO""" +
                 """ WHERE COLC = CONCAT ( #NP# , COLB ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '277461626C65270A'
    setup.verifyHQCEntryExists()

    # add entry26
    stmt = defs.prepXX + """select * from F02_VISO
where colc = CONCAT(cola, 'place');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT026')
    defs.hkey = ("""SELECT * FROM F02_VISO""" +
                 """ WHERE COLC = CONCAT ( COLA , #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27706C616365270A'
    setup.verifyHQCEntryExists()

    # add entry27
    stmt = defs.prepXX + """select * from F02_VISO
where colc = CONCAT(cola, colb);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT027')
    defs.hkey = ("""SELECT * FROM F02_VISO""" +
                 """ WHERE COLC = CONCAT ( COLA , COLB ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry28
    stmt = defs.prepXX + """select * from F02_VUTF8
where colc = CONCAT('table', colb);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT028')
    defs.hkey = ("""SELECT * FROM F02_VUTF8""" +
                 """ WHERE COLC = CONCAT ( #NP# , COLB ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '277461626C65270A'
    setup.verifyHQCEntryExists()

    # add entry29
    stmt = defs.prepXX + """select * from F02_VUTF8
where colc = CONCAT(cola, 'place');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT029')
    defs.hkey = ("""SELECT * FROM F02_VUTF8""" +
                 """ WHERE COLC = CONCAT ( COLA , #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27706C616365270A'
    setup.verifyHQCEntryExists()

    # add entry30
    stmt = defs.prepXX + """select * from F02_VUTF8
where colc = CONCAT(cola, colb);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT030')
    defs.hkey = ("""SELECT * FROM F02_VUTF8""" +
                 """ WHERE COLC = CONCAT ( COLA , COLB ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    setup.resetHQC()

    # https://bugs.launchpad.net/bugs/1359971
    # concat function is HQC cached, but concat operator (||) is not
    # add entry1
    stmt = defs.prepXX + """select 'a1b2c3' || colchriso from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT001')
    defs.hkey = """SELECT #NP# || COLCHRISO FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27613162326333270A'
    setup.verifyHQCEntryExists()

    # add entry2
    stmt = defs.prepXX + """select 'a1b2c3d4e5' || colchriso from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT002')
    defs.hkey = """SELECT #NP# || COLCHRISO FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27613162326333270A'
    setup.verifyHQCEntryExists()

    # add entry3
    stmt = defs.prepXX + """select 'AB DE_' || colchrutf8 from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT003')
    defs.hkey = """SELECT #NP# || COLCHRUTF8 FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2741422044455F270A'
    setup.verifyHQCEntryExists()

    # add entry4
    stmt = defs.prepXX + """select 'aaaaa' || colchrutf8 from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT004')
    defs.hkey = """SELECT #NP# || COLCHRUTF8 FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2741422044455F270A'
    setup.verifyHQCEntryExists()

    # add entry5
    stmt = defs.prepXX + """select colkey, '112233' || colvchriso
from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT005')
    defs.hkey = """SELECT COLKEY , #NP# || COLVCHRISO FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27313132323333270A'
    setup.verifyHQCEntryExists()

    # add entry6
    stmt = defs.prepXX + """select colkey, 'a1b2c3d4e5' || colvchriso
from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT006')
    defs.hkey = """SELECT COLKEY , #NP# || COLVCHRISO FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27313132323333270A'
    setup.verifyHQCEntryExists()

    # add entry7
    stmt = defs.prepXX + """select colkey, 'AB12  ' || colvchrutf8
from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT007')
    defs.hkey = """SELECT COLKEY , #NP# || COLVCHRUTF8 FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27414231322020270A'
    setup.verifyHQCEntryExists()

    # add entry8
    stmt = defs.prepXX + """select colkey, 'aaaaa' || colvchrutf8 from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT008')
    defs.hkey = """SELECT COLKEY , #NP# || COLVCHRUTF8 FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27414231322020270A'
    setup.verifyHQCEntryExists()

    # add entry9
    stmt = defs.prepXX + """select colchriso || '- XYZxyz' from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT009')
    defs.hkey = """SELECT COLCHRISO || #NP# FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '272D2058595A78797A270A'
    setup.verifyHQCEntryExists()

    # add entry10
    stmt = defs.prepXX + """select (colchrutf8 || 'xyz') from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT010')
    defs.hkey = """SELECT ( COLCHRUTF8 || #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2778797A270A'
    setup.verifyHQCEntryExists()

    # add entry11
    stmt = defs.prepXX + """select colkey, (colvchriso || 'x1y2z3')
from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT011')
    defs.hkey = """SELECT COLKEY , ( COLVCHRISO || #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27783179327A33270A'
    setup.verifyHQCEntryExists()

    # add entry12
    stmt = defs.prepXX + """select colkey, (colvchrutf8 || '=7890123')
from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT012')
    defs.hkey = """SELECT COLKEY , ( COLVCHRUTF8 || #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '273D37383930313233270A'
    setup.verifyHQCEntryExists()

   # add entry13
    stmt = defs.prepXX + """select colkey, 'happy ' || 'birthday!'
from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT013')
    defs.hkey = """SELECT COLKEY , #NP# || #NP# FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '27686170707920270A27626972746864617921270A'
    setup.verifyHQCEntryExists()

    # add entry14
    stmt = defs.prepXX + """select colkey, ('iggie ' || 'biggie pop')
from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT014')
    defs.hkey = """SELECT COLKEY , ( #NP# || #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '27696767696520270A2762696767696520706F70270A'
    setup.verifyHQCEntryExists()

    # add entry15
    # increase hits, entry15
    stmt = defs.prepXX + """select * from F01
where colchriso = ('JACKSON' || 'VILLE');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT015')
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT015')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE COLCHRISO = ( #NP# || #NP# ) ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '274A41434B534F4E270A2756494C4C45270A'
    setup.verifyHQCEntryExists()

    # add entry16
    # increase hits, entry16
    stmt = defs.prepXX + """select * from F01
where colchrutf8 = 'PORT' || 'LAND';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT016')
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT016')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE COLCHRUTF8 = #NP# || #NP# ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '27504F5254270A274C414E44270A'
    setup.verifyHQCEntryExists()

    # add entry17
    # increase hits, entry17
    stmt = defs.prepXX + """select * from F01
where colvchriso = 'BOS' || 'TON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT017')
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT017')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE COLVCHRISO = #NP# || #NP# ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '27424F53270A27544F4E270A'
    setup.verifyHQCEntryExists()

    # add entry18
    stmt = defs.prepXX + """select * from F01
where colvchrutf8 = ('JACKSON' || 'VILLE');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT018')
    defs.hkey = ("""SELECT * FROM F01""" +
                 """ WHERE COLVCHRUTF8 = ( #NP# || #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '274A41434B534F4E270A2756494C4C45270A'
    setup.verifyHQCEntryExists()

    # add entry19
    stmt = defs.prepXX + """select * from F02_CISO
where colc = ('through' || colb);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT019')
    defs.hkey = ("""SELECT * FROM F02_CISO""" +
                 """ WHERE COLC = ( #NP# || COLB ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '277468726F756768270A'
    setup.verifyHQCEntryExists()

    # add entry20
    stmt = defs.prepXX + """select * from F02_CISO
where colc = (cola || 'leg');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT020')
    defs.hkey = ("""SELECT * FROM F02_CISO""" +
                 """ WHERE COLC = ( COLA || #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '276C6567270A'
    setup.verifyHQCEntryExists()

    # add entry21
    stmt = defs.prepXX + """select * from F02_CISO
where colc = (cola || colb);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT021')
    defs.hkey = ("""SELECT * FROM F02_CISO""" +
                 """ WHERE COLC = ( COLA || COLB ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry22
    stmt = defs.prepXX + """select * from F02_CUTF8
where colc = ('through' || colb);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT022')
    defs.hkey = ("""SELECT * FROM F02_CUTF8""" +
                 """ WHERE COLC = ( #NP# || COLB ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '277468726F756768270A'
    setup.verifyHQCEntryExists()

    # add entry23
    stmt = defs.prepXX + """select * from F02_CUTF8
where colc = (cola || 'leg');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT023')
    defs.hkey = ("""SELECT * FROM F02_CUTF8""" +
                 """ WHERE COLC = ( COLA || #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '276C6567270A'
    setup.verifyHQCEntryExists()

    # add entry24
    stmt = defs.prepXX + """select * from F02_CUTF8
where colc = (cola || colb);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT024')
    defs.hkey = ("""SELECT * FROM F02_CUTF8""" +
                 """ WHERE COLC = ( COLA || COLB ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry25
    stmt = defs.prepXX + """select * from F02_VISO
where colc = ('table' || colb);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT025')
    defs.hkey = ("""SELECT * FROM F02_VISO""" +
                 """ WHERE COLC = ( #NP# || COLB ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '277461626C65270A'
    setup.verifyHQCEntryExists()

    # add entry26
    stmt = defs.prepXX + """select * from F02_VISO
where colc = (cola || 'place');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT026')
    defs.hkey = ("""SELECT * FROM F02_VISO""" +
                 """ WHERE COLC = ( COLA || #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27706C616365270A'
    setup.verifyHQCEntryExists()

    # add entry27
    stmt = defs.prepXX + """select * from F02_VISO
where colc = (cola || colb);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT027')
    defs.hkey = ("""SELECT * FROM F02_VISO""" +
                 """ WHERE COLC = ( COLA || COLB ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry28
    stmt = defs.prepXX + """select * from F02_VUTF8
where colc = ('table' || colb);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT028')
    defs.hkey = ("""SELECT * FROM F02_VUTF8""" +
                 """ WHERE COLC = ( #NP# || COLB ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '277461626C65270A'
    setup.verifyHQCEntryExists()

    # add entry29
    stmt = defs.prepXX + """select * from F02_VUTF8
where colc = (cola || 'place');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT029')
    defs.hkey = ("""SELECT * FROM F02_VUTF8""" +
                 """ WHERE COLC = ( COLA || #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27706C616365270A'
    setup.verifyHQCEntryExists()

    # add entry30
    stmt = defs.prepXX + """select * from F02_VUTF8
where colc = (cola || colb);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'CONCAT030')
    defs.hkey = ("""SELECT * FROM F02_VUTF8""" +
                 """ WHERE COLC = ( COLA || COLB ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    _testmgr.testcase_end(desc)


def test_lower(desc="""lower()"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: lower()"""

    ### function: LOWER()
    ### HQC CACHEABLE, NOT PARAMETERIZED
    setup.resetHQC()

    # add entry1, expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select colkey, LOWER(colchriso)
from F01 order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'LOWER001')
    defs.hkey = ("""SELECT COLKEY , LOWER ( COLCHRISO ) FROM F01""" +
                 """ ORDER BY COLKEY ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry2, expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select colkey, LOWER(colchrutf8)
from F01 order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'LOWER002')
    defs.hkey = ("""SELECT COLKEY , LOWER ( COLCHRUTF8 ) FROM F01""" +
                 """ ORDER BY COLKEY ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry3, expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select colkey, LOWER(colvchriso)
from F01 order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'LOWER003')
    defs.hkey = ("""SELECT COLKEY , LOWER ( COLVCHRISO ) FROM F01""" +
                 """ ORDER BY COLKEY ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry4, expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select colkey, LOWER(colvchrutf8)
from F01 order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'LOWER004')
    defs.hkey = ("""SELECT COLKEY , LOWER ( COLVCHRUTF8 ) FROM F01""" +
                 """ ORDER BY COLKEY ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry5, expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select LOWER('DEMOINE') from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, 'demoine')
    defs.hkey = """SELECT LOWER ( #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2744454D4F494E45270A'
    setup.verifyHQCEntryExists()

    # add entry6
    stmt = defs.prepXX + """select LOWER('SAVANNAH') from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, 'savannah')
    defs.hkey = """SELECT LOWER ( #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27534156414E4E4148270A'
    setup.verifyHQCEntryExists()

    # increase hits entry1
    stmt = defs.prepXX + """select colkey, LOWER(colchriso)
from F01 order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'LOWER001')
    defs.hkey = ("""SELECT COLKEY , LOWER ( COLCHRISO ) FROM F01""" +
                 """ ORDER BY COLKEY ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry2
    stmt = defs.prepXX + """select colkey, LOWER(colchrutf8)
from F01 order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'LOWER002')
    defs.hkey = ("""SELECT COLKEY , LOWER ( COLCHRUTF8 ) FROM F01""" +
                 """ ORDER BY COLKEY ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry3
    stmt = defs.prepXX + """select colkey, LOWER(colvchriso)
from F01 order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'LOWER003')
    defs.hkey = ("""SELECT COLKEY , LOWER ( COLVCHRISO ) FROM F01""" +
                 """ ORDER BY COLKEY ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits,  entry4
    stmt = defs.prepXX + """select colkey, LOWER(colvchrutf8)
from F01 order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'LOWER004')
    defs.hkey = ("""SELECT COLKEY , LOWER ( COLVCHRUTF8 ) FROM F01""" +
                 """ ORDER BY COLKEY ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry5
    stmt = defs.prepXX + """select LOWER('DEMOINE') from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, 'demoine')
    defs.hkey = """SELECT LOWER ( #NP# ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2744454D4F494E45270A'
    setup.verifyHQCEntryExists()

    # increase hits, entry6
    stmt = defs.prepXX + """select LOWER('SAVANNAH') from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, 'savannah')
    defs.hkey = """SELECT LOWER ( #NP# ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27534156414E4E4148270A'
    setup.verifyHQCEntryExists()

    # add entry7
    stmt = defs.prepXX + """select * from F01
where colchriso = LOWER('HOUSTON');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'LOWER007')
    defs.hkey = """SELECT * FROM F01 WHERE COLCHRISO = LOWER ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27484F5553544F4E270A'
    setup.verifyHQCEntryExists()

    # add entry8
    stmt = defs.prepXX + """select * from F01
where colchrutf8 = LOWER('SAcrameNTO');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'LOWER008')
    defs.hkey = """SELECT * FROM F01 WHERE COLCHRUTF8 = LOWER ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2753416372616D654E544F270A'
    setup.verifyHQCEntryExists()

    # add entry9
    stmt = defs.prepXX + """select * from F01
where colvchriso = LOWER('CHICago');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'LOWER009')
    defs.hkey = """SELECT * FROM F01 WHERE COLVCHRISO = LOWER ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '274348494361676F270A'
    setup.verifyHQCEntryExists()

    # add entry10
    stmt = defs.prepXX + """select * from F01
where colvchrutf8 = LOWER('Winchester-On-The-Severn');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'LOWER010')
    defs.hkey = """SELECT * FROM F01 WHERE COLVCHRUTF8 = LOWER ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2757696E636865737465722D4F6E2D5468652D53657665726E270A'
    setup.verifyHQCEntryExists()

    # increase hits, entry7
    stmt = defs.prepXX + """select * from F01
where colchriso = LOWER('HOUSTON');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'LOWER007')
    defs.hkey = """SELECT * FROM F01 WHERE COLCHRISO = LOWER ( #NP# ) ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27484F5553544F4E270A'
    setup.verifyHQCEntryExists()

    # increase hits, add entry8
    stmt = defs.prepXX + """select * from F01
where colchrutf8 = LOWER('SAcrameNTO');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'LOWER008')
    defs.hkey = """SELECT * FROM F01 WHERE COLCHRUTF8 = LOWER ( #NP# ) ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2753416372616D654E544F270A'
    setup.verifyHQCEntryExists()

    # increase hits, add entry9
    stmt = defs.prepXX + """select * from F01
where colvchriso = LOWER('CHICago');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'LOWER009')
    defs.hkey = """SELECT * FROM F01 WHERE COLVCHRISO = LOWER ( #NP# ) ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '274348494361676F270A'
    setup.verifyHQCEntryExists()

    # increase hits, add entry10
    stmt = defs.prepXX + """select * from F01
where colvchrutf8 = LOWER('Winchester-On-The-Severn');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'LOWER010')
    defs.hkey = """SELECT * FROM F01 WHERE COLVCHRUTF8 = LOWER ( #NP# ) ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2757696E636865737465722D4F6E2D5468652D53657665726E270A'
    setup.verifyHQCEntryExists()

    _testmgr.testcase_end(desc)


def test_replace(desc="""replace()"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: replace()"""

    ### function: REPLACE()
    ### HQC CACHEABLE, PARAMETERIZED
    setup.resetHQC()

    # add entry1
    stmt = defs.prepXX + """select colkey,
REPLACE(colchriso, 'Francisco', 'Luis Obispo')
from F01 order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, 'San Luis Obispo')
    _dci.expect_file(output, defs.expfile, 'REPLACE001')
    defs.hkey = ("""SELECT COLKEY , REPLACE ( COLCHRISO , #NP# , #NP# )"""
                 + """ FROM F01 ORDER BY COLKEY ;""")
    defs.num_hits = 0
    defs.num_pliterals = 2
    defs.pliterals = '274672616E636973636F270A274C756973204F626973706F270A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry2
    stmt = defs.prepXX + """select colkey,
REPLACE(colchrutf8, 'MEGuntic', 'AT me!')
from F01 order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.unexpect_any_substr(output, 'MOOSElookMEGuntic')
    _dci.expect_any_substr(output, 'MOOSElookAT me!')
    _dci.expect_file(output, defs.expfile, 'REPLACE002')

    # increase hits, entry1
    stmt = defs.prepXX + """select colkey,
REPLACE(colchriso, 'Louis', 'Tropez')
from F01 order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.unexpect_any_substr(output, 'St. Louis')
    _dci.expect_any_substr(output, 'St. Tropez')
    _dci.expect_file(output, defs.expfile, 'REPLACE001a')
    defs.hkey = ("""SELECT COLKEY , REPLACE ( COLCHRISO , #NP# , #NP# )"""
                 + """ FROM F01 ORDER BY COLKEY ;""")
    defs.num_hits = 1
    defs.num_pliterals = 2
    defs.pliterals = '274672616E636973636F270A274C756973204F626973706F270A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry2
    stmt = defs.prepXX + """select colkey,
REPLACE(colchrutf8, 'MEGuntic', 'AT me!')
from F01 order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.unexpect_any_substr(output, 'MOOSElookMEGuntic')
    _dci.expect_any_substr(output, 'MOOSElookAT me!')
    _dci.expect_file(output, defs.expfile, 'REPLACE002')
    defs.hkey = ("""SELECT COLKEY , REPLACE ( COLCHRUTF8 , #NP# , #NP# )"""
                 + """ FROM F01 ORDER BY COLKEY ;""")
    defs.num_hits = 0
    defs.num_pliterals = 2
    defs.pliterals = '274D4547756E746963270A274154206D6521270A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry2
    stmt = defs.prepXX + """select colkey,
REPLACE(colchrutf8, 'MEGuntic', ' here.')
from F01 order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.unexpect_any_substr(output, 'MOOSElookMEGuntic')
    _dci.expect_any_substr(output, 'MOOSElook here.')
    _dci.expect_file(output, defs.expfile, 'REPLACE002a')
    defs.hkey = ("""SELECT COLKEY , REPLACE ( COLCHRUTF8 , #NP# , #NP# )"""
                 + """ FROM F01 ORDER BY COLKEY ;""")
    defs.num_hits = 0
    defs.num_pliterals = 2
    defs.pliterals = '274D4547756E746963270A274154206D6521270A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry3
    stmt = defs.prepXX + """select colkey,
REPLACE(colvchriso, 'ON', '#OFF#')
from F01 order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'REPLACE003')
    # increase hits, entry3
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'REPLACE003')
    defs.hkey = ("""SELECT COLKEY , REPLACE ( COLVCHRISO , #NP# , #NP# )"""
                 + """ FROM F01 ORDER BY COLKEY ;""")
    defs.num_hits = 1
    defs.num_pliterals = 2
    defs.pliterals = '274F4E270A27234F464623270A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # DEBUG
    setup.resetHQC()
    # add entry4
    stmt = defs.prepXX + """select colkey,
REPLACE(colvchrutf8, 'York', 'Jersey')
from F01 order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.unexpect_any_substr(output, 'New York')
    _dci.expect_any_substr(output, 'New Jersey')
    _dci.expect_file(output, defs.expfile, 'REPLACE004')
    defs.hkey = ("""SELECT COLKEY , REPLACE ( COLVCHRUTF8 , #NP# , #NP# )"""
                 + """ FROM F01 ORDER BY COLKEY ;""")
    defs.num_hits = 0
    defs.num_pliterals = 2
    defs.pliterals = '27596F726B270A274A6572736579270A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry4
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.unexpect_any_substr(output, 'New York')
    _dci.expect_any_substr(output, 'New Jersey')
    _dci.expect_file(output, defs.expfile, 'REPLACE004')
    defs.hkey = ("""SELECT COLKEY , REPLACE ( COLVCHRUTF8 , #NP# , #NP# )"""
                 + """ FROM F01 ORDER BY COLKEY ;""")
    defs.num_hits = 0
    defs.num_pliterals = 2
    defs.pliterals = '27596F726B270A274A6572736579270A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry4
    stmt = defs.prepXX + """select colkey,
REPLACE(colvchrutf8, 'York', 'Mexico')
from F01 order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.unexpect_any_substr(output, 'New York')
    _dci.expect_any_substr(output, 'New Mexico')
    _dci.expect_file(output, defs.expfile, 'REPLACE004a')
    defs.hkey = ("""SELECT COLKEY , REPLACE ( COLVCHRUTF8 , #NP# , #NP# )"""
                 + """ FROM F01 ORDER BY COLKEY ;""")
    defs.num_hits = 0
    defs.num_pliterals = 2
    defs.pliterals = '27596F726B270A274A6572736579270A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    setup.resetHQC()
    # add entry5
    stmt = defs.prepXX + """select
REPLACE('the cat in the hat', 'cat', 'mouse') from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, 'the mouse in the hat')
    # increase hits, entry5
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, 'the mouse in the hat')
    defs.hkey = ("""SELECT REPLACE ( #NP# , #NP# , #NP# ) FROM F00 ;""")
    defs.num_hits = 1
    defs.num_pliterals = 3
    defs.pliterals = ('277468652063617420696E2074686520686174270A' +
                      '27636174270A276D6F757365270A')
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry5
    stmt = defs.prepXX + """select
REPLACE('green eggs and ham', 'green', 'purple') from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, 'purple eggs and ham')
    defs.hkey = ("""SELECT REPLACE ( #NP# , #NP# , #NP# ) FROM F00 ;""")
    defs.num_hits = 1
    defs.num_pliterals = 3
    defs.pliterals = ('277468652063617420696E2074686520686174270A' +
                      '27636174270A276D6F757365270A')
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry6
    stmt = defs.prepXX + """select
REPLACE('Pennsylvannia            Dutch', colchriso, 'New England ')
from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, 'New England Dutch')
    defs.hkey = ("""SELECT REPLACE ( #NP# , COLCHRISO , #NP# ) FROM F00 ;""")
    defs.num_hits = 0
    defs.num_pliterals = 2
    defs.pliterals = ('2750656E6E73796C76616E6E6961' +
                      '2020202020202020202020204475746368270A' +
                      '274E657720456E676C616E6420270A')
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry7
    stmt = defs.prepXX + """select
REPLACE('Ohio primaries', 'Ohio', colchrutf8) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'REPLACE007')
    defs.hkey = ("""SELECT REPLACE ( #NP# , #NP# , COLCHRUTF8 ) FROM F00 ;""")
    defs.num_hits = 0
    defs.num_pliterals = 2
    defs.pliterals = '274F68696F207072696D6172696573270A274F68696F270A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry8
    stmt = defs.prepXX + """select
REPLACE('Ohio', 'Ohio', colvchrutf8) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, 'California')
    defs.hkey = ("""SELECT REPLACE ( #NP# , #NP# , COLVCHRUTF8 ) FROM F00 ;""")
    defs.num_hits = 0
    defs.num_pliterals = 2
    defs.pliterals = '274F68696F2270A274F68696F270A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryNOTExists()

    output = _dci.cmdexec("""drop table mytbl;""")
    output = _dci.cmdexec("""create table mytbl like F01 with partitions;""")
    _dci.expect_complete_msg(output)
    output = _dci.cmdexec("""load into mytbl select * from F01;""")
    _dci.expect_complete_msg(output)

    # add entry9
    stmt = """update mytbl
set colvchriso = REPLACE(colvchriso, 'Francisco', 'Fernando');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, '17')
    defs.hkey = ("""UPDATE MYTBL SET COLVCHRISO =""" +
                 """ REPLACE ( COLVCHRISO , #NP# , #NP# ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 2
    defs.pliterals = '274672616E636973636F270A274665726E616E646F270A'
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()
    output = _dci.cmdexec("""select [first 20]colkey, colvchriso from mytbl
order by 2,1;""")
    _dci.expect_file(output, defs.expfile, 'REPLACE009')
    defs.hkey = ("""SELECT [ FIRST #NP# ] COLKEY , COLVCHRISO FROM MYTBL""" +
                 """ ORDER BY #NP# , #NP# ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 3
    defs.npliterals = '32300A320A310A'
    setup.verifyHQCEntryExists()

    output = _dci.cmdexec("""drop table mytbl cascade;""")
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)


def test_substr(desc="""substring/substr()"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: substring/substr()"""

    ### function: SUBSTRING()/SUBSTR()
    ### HQC CACHEABLE, NOT PARAMETERIZED
    setup.resetHQC()

    # add entry1
    stmt = defs.prepXX + """select SUBSTRING(colchriso FROM 5) from F01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SUBSTRING001')
    defs.hkey = """SELECT SUBSTRING ( COLCHRISO FROM #NP# ) FROM F01 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '350A'
    setup.verifyHQCEntryExists()

    # add entry2
    stmt = defs.prepXX + """select SUBSTRING(colchrutf8, 4) from F01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SUBSTRING002')
    defs.hkey = """SELECT SUBSTRING ( COLCHRUTF8 , #NP# ) FROM F01 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '340A'
    setup.verifyHQCEntryExists()

    # add entry3
    stmt = defs.prepXX + """select SUBSTRING(colvchriso from 4 for 6)
from F01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SUBSTRING003')
    defs.hkey = ("""SELECT SUBSTRING ( COLVCHRISO FROM #NP# FOR #NP# )""" +
                 """ FROM F01 ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '340A360A'
    setup.verifyHQCEntryExists()

    # add entry4
    stmt = defs.prepXX + """select SUBSTRING(colvchrutf8, 5, 10)
from F01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SUBSTRING004')
    defs.hkey = ("""SELECT SUBSTRING ( COLVCHRUTF8 , #NP# , #NP# )""" +
                 """ FROM F01 ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '350A31300A'
    setup.verifyHQCEntryExists()

    # add entry5
    stmt = (defs.prepXX + """select SUBSTRING('the snow glows""" +
            """ white on the mountain tonight', 16, 22) from F00;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, 'white on the mountain')
    defs.hkey = ("""SELECT SUBSTRING ( #NP# , #NP# , #NP# )""" +
                 """ FROM F00 ;""")
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = ('2774686520736E6F7720676C6F7773207768697465206F6E20' +
                      '746865206D6F756E7461696E20746F6E69676874270A')
    defs.num_npliterals = 2
    defs.npliterals = '31360A32320A'
    setup.verifyHQCEntryExists()

    #output = _dci.cmdexec("""drop table mytbl;""")
    #output = _dci.cmdexec("""create table mytbl like F01 with partitions;""")
    #_dci.expect_complete_msg(output)
    #output = _dci.cmdexec("""load into mytbl select * from F01;""")
    #_dci.expect_complete_msg(output)

    # add entry6
    #stmt = defs.prepXX + """update mytbl
#set (colchriso, colchrutf8, colvchriso, colvchrutf8) = (
#SUBSTRING(colchriso, 3),
#SUBSTRING(colchrutf8, 4, 9),
#SUBSTRING(colvchriso from 5),
#SUBSTRING(colvchrutf8 from 6 for 12));"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_prepared_msg(output)
    #defs.hkey = ("""UPDATE MYTBL""" +
                 #""" SET ( COLCHRISO , COLCHRUTF8 , COLVCHRISO ,""" +
                 #""" COLVCHRUTF8 ) = ( SUBSTRING ( COLCHRISO , #NP# ) ,""" +
                 #""" SUBSTRING ( COLCHRUTF8 , #NP# , #NP# ) ,""" +
                 #""" SUBSTRING ( COLVCHRISO FROM #NP# ) ,""" +
                 #""" SUBSTRING (COLVCHRUTF8 FROM #NP# FOR #NP# ) ) ;""")
    #defs.num_hits = 0
    #defs.num_pliterals = 0
    #defs.num_npliterals = 6
    #defs.npliterals = '330A340A390A350A360A31320A'
    #setup.verifyHQCEntryExists()
    #output = _dci.cmdexec("""select * from mytbl order by colkey;""")
    #_dci.expect_file(output, defs.expfile, 'SUBSTRING006')

    # increase hits, entry1
    stmt = defs.prepXX + """select SUBSTRING(colchriso FROM 5) from F01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SUBSTRING001')
    defs.hkey = """SELECT SUBSTRING ( COLCHRISO FROM #NP# ) FROM F01 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '350A'
    setup.verifyHQCEntryExists()

    # add new entry6
    stmt = defs.prepXX + """select SUBSTRING(colchriso FROM 2) from F01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SUBSTRING001a')
    defs.hkey = """SELECT SUBSTRING ( COLCHRISO FROM #NP# ) FROM F01 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '320A'
    setup.verifyHQCEntryExists()

    # increase hits, entry2
    stmt = defs.prepXX + """select SUBSTRING(colchrutf8, 4) from F01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SUBSTRING002')
    defs.hkey = """SELECT SUBSTRING ( COLCHRUTF8 , #NP# ) FROM F01 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '340A'
    setup.verifyHQCEntryExists()

    # add new entry7
    stmt = defs.prepXX + """select SUBSTRING(colchrutf8, 7) from F01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SUBSTRING002a')
    defs.hkey = """SELECT SUBSTRING ( COLCHRUTF8 , #NP# ) FROM F01 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '370A'
    setup.verifyHQCEntryExists()

    # increase hits, entry3
    stmt = defs.prepXX + """select SUBSTRING(colvchriso from 4 for 6)
from F01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SUBSTRING003')
    defs.hkey = ("""SELECT SUBSTRING ( COLVCHRISO FROM #NP# FOR #NP# )""" +
                 """ FROM F01 ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '340A360A'
    setup.verifyHQCEntryExists()

    # add new entry8
    stmt = defs.prepXX + """select SUBSTRING(colvchriso from 6 for 7)
from F01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SUBSTRING003a')
    defs.hkey = ("""SELECT SUBSTRING ( COLVCHRISO FROM #NP# FOR #NP# )""" +
                 """ FROM F01 ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '360A370A'
    setup.verifyHQCEntryExists()

    # increase hits, entry4
    stmt = defs.prepXX + """select SUBSTRING(colvchrutf8, 5, 10)
from F01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SUBSTRING004')
    defs.hkey = ("""SELECT SUBSTRING ( COLVCHRUTF8 , #NP# , #NP# )""" +
                 """ FROM F01 ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '350A31300A'
    setup.verifyHQCEntryExists()

    # increase hits, entry4
    stmt = defs.prepXX + """select SUBSTRING(colvchrutf8, 5, 10)
from F01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SUBSTRING004')
    defs.num_hits = 2
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '350A31300A'
    setup.verifyHQCEntryExists()

    # add new entry10
    stmt = defs.prepXX + """select SUBSTRING(colvchrutf8, 2, 9)
from F01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'SUBSTRING004a')
    defs.hkey = ("""SELECT SUBSTRING ( COLVCHRUTF8 , #NP# , #NP# )""" +
                 """ FROM F01 ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = '320A390A'
    setup.verifyHQCEntryExists()

    # add new entry11
    stmt = defs.prepXX + ("""select SUBSTRING('the snow glows white""" +
                          """ on the mountain tonight', 5, 15) from F00;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, 'snow glows whit')
    defs.hkey = ("""SELECT SUBSTRING ( #NP# , #NP# , #NP# )""" +
                 """ FROM F00 ;""")
    defs.num_hits = 0
    defs.num_pliterals = 1
    defs.pliterals = ('2774686520736E6F7720676C6F7773207768697465206F6E20' +
                      '746865206D6F756E7461696E20746F6E69676874270A')
    defs.num_npliterals = 2
    defs.npliterals = '350A31350A'
    setup.verifyHQCEntryExists()

    # increas hits, entry11
    stmt = defs.prepXX + ("""select SUBSTRING('not a footprint to""" +
                          """ be seen', 5, 15) from F00;""")
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, 'a footprint to ')
    defs.hkey = ("""SELECT SUBSTRING ( #NP# , #NP# , #NP# )""" +
                 """ FROM F00 ;""")
    defs.num_hits = 1
    defs.num_pliterals = 1
    defs.pliterals = ('2774686520736E6F7720676C6F7773207768697465206F6E20' +
                      '746865206D6F756E7461696E20746F6E69676874270A')
    defs.num_npliterals = 2
    defs.npliterals = '350A31350A'
    setup.verifyHQCEntryExists()

    # increase hits, entry6
    #stmt = defs.prepXX + """update mytbl
#set (colchriso, colchrutf8, colvchriso, colvchrutf8) = (
#SUBSTRING(colchriso, 3),
#SUBSTRING(colchrutf8, 2, 3),
#SUBSTRING(colvchriso from 5),
#SUBSTRING(colvchrutf8 from 2 for 7));"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_updated_msg(output, '17')
    #defs.hkey = ("""UPDATE MYTBL""" +
                 #""" SET ( COLCHRISO , COLCHRUTF8 , COLVCHRISO ,""" +
                 #""" COLVCHRUTF8 ) = ( SUBSTRING ( COLCHRISO , #NP# ) ,""" +
                 #""" SUBSTRING ( COLCHRUTF8 , #NP# , #NP# ) ,""" +
                 #""" SUBSTRING ( COLVCHRISO FROM #NP# ) ,""" +
                 #""" SUBSTRING (COLVCHRUTF8 FROM #NP# FOR #NP# ) ) ;""")
    #defs.num_hits = 1
    #defs.num_pliterals = 6
    #defs.pliterals = '330A340A390A350A360A31320A'
    #defs.num_npliterals = 0
    #setup.verifyHQCEntryExists()
    #output = _dci.cmdexec("""select * from mytbl order by colkey;""")
    #_dci.expect_file(output, defs.expfile, 'SUBSTRING006a')

    #output = _dci.cmdexec("""drop table mytbl;""")

    _testmgr.testcase_end(desc)


def test_translate(desc="""translate()"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: translate()"""

    ### function: TRANSLATE()
    ### HQC CACHEABLE, NOT PARAMETERIZED
    setup.resetHQC()

    # add entry1
    stmt = defs.prepXX + """select colkey,
TRANSLATE(colchriso USING iso88591toutf8)
from F01 order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRANSLATE001')
    defs.hkey = ("""SELECT COLKEY ,""" +
                 """ TRANSLATE ( COLCHRISO USING ISO88591TOUTF8 )""" +
                 """ FROM F01 ORDER BY COLKEY ; """)
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry2
    stmt = defs.prepXX + """select colkey,
TRANSLATE(colvchriso USING iso88591toutf8)
from F01 order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRANSLATE002')
    defs.hkey = ("""SELECT COLKEY ,""" +
                 """ TRANSLATE ( COLVCHRISO USING ISO88591TOUTF8 )""" +
                 """ FROM F01 ORDER BY COLKEY ; """)
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry3
    stmt = defs.prepXX + """select colkey,
TRANSLATE(colchrutf8 USING utf8toiso88591)
from F01 order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRANSLATE003')
    defs.hkey = ("""SELECT COLKEY ,""" +
                 """ TRANSLATE ( COLCHRUTF8 USING UTF8TOISO88591 )""" +
                 """ FROM F01 ORDER BY COLKEY ; """)
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry4
    stmt = defs.prepXX + """select colkey,
TRANSLATE(colvchrutf8 USING utf8toiso88591)
from F01 order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRANSLATE004')
    defs.hkey = ("""SELECT COLKEY ,""" +
                 """ TRANSLATE ( COLVCHRUTF8 USING UTF8TOISO88591 )""" +
                 """ FROM F01 ORDER BY COLKEY ; """)
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry5
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select
TRANSLATE('MiSSiSSiPPi' USING ISO88591TOUTF8) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRANSLATE005')

    # add entry6
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select
TRANSLATE('KENTUCKY' USING UTF8TOISO88591) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRANSLATE006')

    # increase hits, entry5
    stmt = defs.prepXX + """select
TRANSLATE('MiSSiSSiPPi' USING ISO88591TOUTF8) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRANSLATE005')
    defs.hkey = ("""SELECT TRANSLATE ( #NP# USING ISO88591TOUTF8 )""" +
                 """ FROM F00 ; """)
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '274D69535369535369505069270A'
    setup.verifyHQCEntryExists()

    # increase hits, entry6
    stmt = defs.prepXX + """select
TRANSLATE('KENTUCKY' USING UTF8TOISO88591) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRANSLATE006')
    defs.hkey = ("""SELECT TRANSLATE ( #NP# USING UTF8TOISO88591 )""" +
                 """ FROM F00 ; """)
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '274B454E5455434B59270A'
    setup.verifyHQCEntryExists()

    # add entry7
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select
TRANSLATE('!@ #${ + = }^!' USING ISO88591TOUTF8) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRANSLATE007')

    # add entry8
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select
TRANSLATE('()@&^!$z' USING UTF8TOISO88591)
from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRANSLATE008')

    # increase hits, entry7
    stmt = defs.prepXX + """select
TRANSLATE('!@ #${ + = }^!' USING ISO88591TOUTF8) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRANSLATE007')

    # increase hits, entry8
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select
TRANSLATE('()@&^!$z' USING UTF8TOISO88591)
from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRANSLATE008')

    # verify entry7
    defs.hkey = ("""SELECT TRANSLATE ( #NP# USING ISO88591TOUTF8 )""" +
                 """ FROM F00 ; """)
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2721402023247B202B203D207D5E21270A'
    setup.verifyHQCEntryExists()

    # verify entry8
    defs.hkey = ("""SELECT TRANSLATE ( #NP# USING UTF8TOISO88591 )""" +
                 """ FROM F00 ; """)
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27282940265E21247A270A'
    setup.verifyHQCEntryExists()

    # add entry9
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select * from F01
where colchrutf8 = TRANSLATE(colchriso using iso88591toutf8)
order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRANSLATE009')
    defs.hkey = ("""SELECT * FROM F01 WHERE COLCHRUTF8 =""" +
                 """ TRANSLATE ( COLCHRISO USING ISO88591TOUTF8 )""" +
                 """ ORDER BY COLKEY ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry10
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select * from F01
where colvchriso = TRANSLATE(colvchrutf8 using utf8toiso88591)
order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRANSLATE010')
    defs.hkey = ("""SELECT * FROM F01 WHERE COLVCHRISO =""" +
                 """ TRANSLATE ( COLVCHRUTF8 USING UTF8TOISO88591 )""" +
                 """ ORDER BY COLKEY ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry11
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select * from F01
where colchrutf8 = TRANSLATE('sacramento' USING ISO88591TOUTF8);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRANSLATE011')
    defs.hkey = ("""SELECT * FROM F01 WHERE COLCHRUTF8 =""" +
                 """ TRANSLATE ( #NP# USING ISO88591TOUTF8 ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2773616372616D656E746F270A'
    setup.verifyHQCEntryExists()

    # add entry12
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select * from F01
where colvchrutf8 = TRANSLATE('houston' USING ISO88591TOUTF8);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRANSLATE012')
    defs.hkey = ("""SELECT * FROM F01 WHERE COLVCHRUTF8 =""" +
                 """ TRANSLATE ( #NP# USING ISO88591TOUTF8 ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27686F7573746F6E270A'
    setup.verifyHQCEntryExists()

    # add entry13
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select * from F01
where colchriso = TRANSLATE('Houston' USING UTF8TOISO88591);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRANSLATE013')
    defs.hkey = ("""SELECT * FROM F01 WHERE COLCHRISO =""" +
                 """ TRANSLATE ( #NP# USING UTF8TOISO88591 ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27486F7573746F6E270A'
    setup.verifyHQCEntryExists()

    # add entry14
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select * from F01
where colvchriso = TRANSLATE('Tallahassee' USING UTF8TOISO88591);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRANSLATE014')
    defs.hkey = ("""SELECT * FROM F01 WHERE COLVCHRISO =""" +
                 """ TRANSLATE ( #NP# USING UTF8TOISO88591 ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2754616C6C61686173736565270A'
    setup.verifyHQCEntryExists()

    # increase hits, entry11
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select * from F01
where colchrutf8 = TRANSLATE('sacramento' USING ISO88591TOUTF8);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRANSLATE011')
    defs.hkey = ("""SELECT * FROM F01 WHERE COLCHRUTF8 =""" +
                 """ TRANSLATE ( #NP# USING ISO88591TOUTF8 ) ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2773616372616D656E746F270A'
    setup.verifyHQCEntryExists()

    # increase hits, entry12
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select * from F01
where colvchrutf8 = TRANSLATE('houston' USING ISO88591TOUTF8);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRANSLATE012')
    defs.hkey = ("""SELECT * FROM F01 WHERE COLVCHRUTF8 =""" +
                 """ TRANSLATE ( #NP# USING ISO88591TOUTF8 ) ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27686F7573746F6E270A'
    setup.verifyHQCEntryExists()

    # add entry15
    # same hkey as entry13, but differing literals
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select * from F01
where colchriso = TRANSLATE('St. Louis' USING UTF8TOISO88591);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRANSLATE015')
    defs.hkey = ("""SELECT * FROM F01 WHERE COLCHRISO =""" +
                 """ TRANSLATE ( #NP# USING UTF8TOISO88591 ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2753742E204C6F756973270A'
    setup.verifyHQCEntryExists()

    # add entry16
    # same hkey as entry14, but differing literals
    # expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select * from F01
where colvchriso = TRANSLATE('dallas' USING UTF8TOISO88591);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRANSLATE016')
    defs.hkey = ("""SELECT * FROM F01 WHERE COLVCHRISO =""" +
                 """ TRANSLATE ( #NP# USING UTF8TOISO88591 ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2764616C6C6173270A'
    setup.verifyHQCEntryExists()

    _testmgr.testcase_end(desc)


def test_trim(desc="""trim()"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: trim()"""

    ### function: TRIM()
    ### HQC CACHEABLE, NOT PARAMETERIZED
    setup.resetHQC()

    ### trim leading in result set
    # add entry1
    stmt = defs.prepXX + """select
trim(leading 'P' from colchriso) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRIM001')
    # increase hits, entry1
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRIM001')
    # change literal, add entry2
    stmt = defs.prepXX + """select
trim(leading 'N' from colchriso) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRIM002')
    # verify entry2 with differing literal
    defs.hkey = ("""SELECT TRIM ( LEADING #NP# FROM COLCHRISO )""" +
                 """ FROM F00 ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '274E270A'
    setup.verifyHQCEntryExists()
    # verify entry1
    defs.hkey = ("""SELECT TRIM ( LEADING #NP# FROM COLCHRISO )""" +
                 """ FROM F00 ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2750270A'
    setup.verifyHQCEntryExists()

    # add entry3
    stmt = defs.prepXX + """select
trim(leading 'N' from colchrutf8) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRIM003')
    defs.hkey = ("""SELECT TRIM ( LEADING #NP# FROM COLCHRUTF8 )""" +
                 """ FROM F00 ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '274E270A'
    setup.verifyHQCEntryExists()

    # add entry4
    stmt = defs.prepXX + """select
trim(leading 'S' from colvchriso) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRIM004')
    defs.hkey = ("""SELECT TRIM ( LEADING #NP# FROM COLVCHRISO )""" +
                 """ FROM F00 ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2753270A'
    setup.verifyHQCEntryExists()

    # add entry5
    stmt = defs.prepXX + """select
trim(leading 'C' from colvchrutf8) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRIM005')
    # change literal, add entry6
    stmt = defs.prepXX + """select
trim(leading 'M' from colvchrutf8) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRIM006')
    # verify entry5
    defs.hkey = ("""SELECT TRIM ( LEADING #NP# FROM COLVCHRUTF8 )""" +
                 """ FROM F00 ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2743270A'
    setup.verifyHQCEntryExists()
    # increase hits, entry6
    stmt = defs.prepXX + """select
trim(leading 'M' from colvchrutf8) from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRIM006')
    # verify entry6
    defs.hkey = ("""SELECT TRIM ( LEADING #NP# FROM COLVCHRUTF8 )""" +
                 """ FROM F00 ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '274D270A'
    setup.verifyHQCEntryExists()

    # add entry7
    stmt = defs.prepXX + """select
trim(leading 'o'
from 'oo once upon a time in a far off landooo') from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRIM007')
    # change literal, add entry8
    stmt = defs.prepXX + """select
trim(leading 'n'
from 'once upon a time in a far off land') from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRIM008')
    # verify entry7
    defs.hkey = ("""SELECT TRIM ( LEADING #NP# FROM #NP# )""" +
                 """ FROM F00 ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = ('276F270A' +
                       '276F6F206F6E63652075706F6E20612074696D6520' +
                       '696E206120666172206F6666206C616E646F6F6F270A')
    setup.verifyHQCEntryExists()
    # increase hits, entry8
    stmt = defs.prepXX + """select
trim(leading 'n'
from 'once upon a time in a far off land') from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRIM008')
    # verify entry8
    defs.hkey = ("""SELECT TRIM ( LEADING #NP# FROM #NP# )""" +
                 """ FROM F00 ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = ('276E270A' +
                       '276F6E63652075706F6E20612074696D6520' +
                       '696E206120666172206F6666206C616E64270A')
    setup.verifyHQCEntryExists()

    setup.resetHQC()
    ### trim trailing in result set
    # add entry9
    stmt = defs.prepXX + """select
trim(trailing 'a' from colchriso)  from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRIM009')
    defs.hkey = ("""SELECT TRIM ( TRAILING #NP# FROM COLCHRISO )""" +
                 """ FROM F00 ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2761270A'
    setup.verifyHQCEntryExists()

    # add entry10
    stmt = defs.prepXX + """select
trim(trailing 'e' from colchrutf8)  from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRIM010')
    defs.hkey = ("""SELECT TRIM ( TRAILING #NP# FROM COLCHRUTF8 )""" +
                 """ FROM F00 ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2765270A'
    setup.verifyHQCEntryExists()

    # add entry11
    stmt = defs.prepXX + """select
trim(trailing 'a' from colvchriso)  from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRIM011')
    defs.hkey = ("""SELECT TRIM ( TRAILING #NP# FROM COLVCHRISO )""" +
                 """ FROM F00 ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2761270A'
    setup.verifyHQCEntryExists()

    # add entry12
    stmt = defs.prepXX + """select
trim(trailing 'a' from colvchrutf8)  from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRIM012')
    defs.hkey = ("""SELECT TRIM ( TRAILING #NP# FROM COLVCHRUTF8 )""" +
                 """ FROM F00 ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2761270A'
    setup.verifyHQCEntryExists()

    # add entry13
    stmt = defs.prepXX + """select
trim(trailing '.' from 'some data here.') from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRIM013')
    defs.hkey = ("""SELECT TRIM ( TRAILING #NP# FROM #NP# )""" +
                 """ FROM F00 ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = ('272E270A' +
                       '27736F6D65206461746120686572652E270A')
    setup.verifyHQCEntryExists()

    # add entry14
    stmt = defs.prepXX + """select
trim('   some data here.   ')  from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRIM014')
    defs.hkey = ("""SELECT TRIM ( #NP# )""" +
                 """ FROM F00 ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27202020736F6D65206461746120686572652E202020270A'
    setup.verifyHQCEntryExists()

    # add entry15
    stmt = defs.prepXX + """select
trim('a' from 'aaasome data here.aaa') from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRIM015')
    defs.hkey = ("""SELECT TRIM ( #NP# FROM #NP# )""" +
                 """ FROM F00 ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 2
    defs.npliterals = ('2761270A' +
                       '27616161736F6D65206461746120686572652E616161270A')
    setup.verifyHQCEntryExists()

    ### trim leading in where predicate
    ### trim trailing in where predicate
    output = _dci.cmdexec("""drop table mytbl cascade;""")
    output = _dci.cmdexec("""create table mytbl like F01;""")
    _dci.expect_complete_msg(output)
    output = _dci.cmdexec("""load into mytbl select * from F01;""")
    _dci.expect_complete_msg(output)

    setup.resetHQC()
    # add entry16
    stmt = defs.prepXX + """update mytbl
set colchriso = trim(leading 'N' from colchriso);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRIM016')
    defs.hkey = ("""UPDATE MYTBL SET COLCHRISO =""" +
                 """ TRIM ( LEADING #NP# FROM COLCHRISO ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '274E270A'
    setup.verifyHQCEntryExists()

    # add entry17
    stmt = defs.prepXX + """update mytbl
set colvchriso = trim(trailing 'a' from colvchriso);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRIM017')
    defs.hkey = ("""UPDATE MYTBL SET COLVCHRISO =""" +
                 """ TRIM ( TRAILING #NP# FROM COLVCHRISO ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2761270A'
    setup.verifyHQCEntryExists()

    # add entry18
    stmt = defs.prepXX + """update mytbl
set colvchrutf8 = trim(leading 'M' from colvchrutf8);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRIM018')
    defs.hkey = ("""UPDATE MYTBL SET COLVCHRUTF8 =""" +
                 """ TRIM ( LEADING #NP# FROM COLVCHRUTF8 ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '274D270A'
    setup.verifyHQCEntryExists()

    # add entry19
    stmt = defs.prepXX + """update mytbl
set colvchrutf8 = trim(trailing 'N' from colvchrutf8);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRIM019')
    defs.hkey = ("""UPDATE MYTBL SET COLVCHRUTF8 =""" +
                 """ TRIM ( TRAILING #NP# FROM COLVCHRUTF8 ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '274E270A'
    setup.verifyHQCEntryExists()

    # add entry20
    stmt = defs.prepXX + """update mytbl
set colvchriso = trim('1' from colvchriso);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'TRIM020')
    defs.hkey = ("""UPDATE MYTBL SET COLVCHRISO =""" +
                 """ TRIM ( #NP# FROM COLVCHRISO ) ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2731270A'
    setup.verifyHQCEntryExists()

    _testmgr.testcase_end(desc)


def test_upper(desc="""upper()"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return
    defs.testid = """HQC: upper()"""

    ### function: UPPER()
    ### HQC CACHEABLE, NOT PARAMETERIZED
    setup.resetHQC()

    # add entry1, expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select colkey, UPPER(colchriso)
from F01 order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'UPPER001')
    defs.hkey = ("""SELECT COLKEY , UPPER ( COLCHRISO ) FROM F01""" +
                 """ ORDER BY COLKEY ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry2, expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select colkey, UPPER(colchrutf8)
from F01 order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'UPPER002')
    defs.hkey = ("""SELECT COLKEY , UPPER ( COLCHRUTF8 ) FROM F01""" +
                 """ ORDER BY COLKEY ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry3, expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select colkey, UPPER(colvchriso)
from F01 order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'UPPER003')
    defs.hkey = ("""SELECT COLKEY , UPPER ( COLVCHRISO ) FROM F01""" +
                 """ ORDER BY COLKEY ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry4, expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select colkey, UPPER(colvchrutf8)
from F01 order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'UPPER004')
    defs.hkey = ("""SELECT COLKEY , UPPER ( COLVCHRUTF8 ) FROM F01""" +
                 """ ORDER BY COLKEY ;""")
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # add entry5, expect = HQC::AddEntry(): passed
    stmt = defs.prepXX + """select UPPER('huntington') from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, 'HUNTINGTON')
    defs.hkey = """SELECT UPPER ( #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2768756E74696E67746F6E270A'
    setup.verifyHQCEntryExists()

    # add entry6
    stmt = defs.prepXX + """select UPPER('port jefferson') from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, 'PORT JEFFERSON')
    defs.hkey = """SELECT UPPER ( #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27706F7274206A6566666572736F6E270A'
    setup.verifyHQCEntryExists()

    # increase hits entry1
    stmt = defs.prepXX + """select colkey, UPPER(colchriso)
from F01 order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'UPPER001')
    defs.hkey = ("""SELECT COLKEY , UPPER ( COLCHRISO ) FROM F01""" +
                 """ ORDER BY COLKEY ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry2
    stmt = defs.prepXX + """select colkey, UPPER(colchrutf8)
from F01 order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'UPPER002')
    defs.hkey = ("""SELECT COLKEY , UPPER ( COLCHRUTF8 ) FROM F01""" +
                 """ ORDER BY COLKEY ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry3
    stmt = defs.prepXX + """select colkey, UPPER(colvchriso)
from F01 order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'UPPER003')
    defs.hkey = ("""SELECT COLKEY , UPPER ( COLVCHRISO ) FROM F01""" +
                 """ ORDER BY COLKEY ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits,  entry4
    stmt = defs.prepXX + """select colkey, UPPER(colvchrutf8)
from F01 order by colkey;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'UPPER004')
    defs.hkey = ("""SELECT COLKEY , UPPER ( COLVCHRUTF8 ) FROM F01""" +
                 """ ORDER BY COLKEY ;""")
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 0
    setup.verifyHQCEntryExists()

    # increase hits, entry5
    stmt = defs.prepXX + """select UPPER('huntington') from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_str_token(output, 'HUNTINGTON')
    defs.hkey = """SELECT UPPER ( #NP# ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2768756E74696E67746F6E270A'
    setup.verifyHQCEntryExists()

    # increase hits, entry6
    stmt = defs.prepXX + """select UPPER('port jefferson') from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, 'PORT JEFFERSON')
    defs.hkey = """SELECT UPPER ( #NP# ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27706F7274206A6566666572736F6E270A'
    setup.verifyHQCEntryExists()

    # add entry7
    stmt = defs.prepXX + """select UPPER('Cold Spring Harbor') from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, 'COLD SPRING HARBOR')
    defs.hkey = """SELECT UPPER ( #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27436F6C6420537072696E6720486172626F72270A'
    setup.verifyHQCEntryExists()

    # add entry8
    stmt = defs.prepXX + """select * from F01
where colchriso = UPPER('albuQUERque');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'UPPER008')
    defs.hkey = """SELECT * FROM F01 WHERE COLCHRISO = UPPER ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27616C627551554552717565270A'
    setup.verifyHQCEntryExists()

    # add entry9
    stmt = defs.prepXX + """select * from F01
where colchrutf8 = UPPER('boston');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'UPPER009')
    defs.hkey = """SELECT * FROM F01 WHERE COLCHRUTF8 = UPPER ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27626F73746F6E270A'
    setup.verifyHQCEntryExists()

    # add entry10
    stmt = defs.prepXX + """select * from F01
where colvchriso = UPPER('st. Louis');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'UPPER010')
    defs.hkey = """SELECT * FROM F01 WHERE COLVCHRISO = UPPER ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2773742E204C6F756973270A'
    setup.verifyHQCEntryExists()

    # add entry11
    stmt = defs.prepXX + """select * from F01
where colvchrutf8 = UPPER('los angeles');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'UPPER011')
    defs.hkey = """SELECT * FROM F01 WHERE COLVCHRUTF8 = UPPER ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '276C6F7320616E67656C6573270A'
    setup.verifyHQCEntryExists()

    # increase hits, entry7
    stmt = defs.prepXX + """select UPPER('Cold Spring Harbor') from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, 'COLD SPRING HARBOR')
    defs.hkey = """SELECT UPPER ( #NP# ) FROM F00 ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27436F6C6420537072696E6720486172626F72270A'
    setup.verifyHQCEntryExists()

    # add entry12
    stmt = defs.prepXX + """select UPPER('Cold SPring Harbor') from F00;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_any_substr(output, 'COLD SPRING HARBOR')
    defs.hkey = """SELECT UPPER ( #NP# ) FROM F00 ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27436F6C6420535072696E6720486172626F72270A'
    setup.verifyHQCEntryExists()

    # increase hits, entry8
    stmt = defs.prepXX + """select * from F01
where colchriso = UPPER('albuQUERque');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'UPPER008')
    defs.hkey = """SELECT * FROM F01 WHERE COLCHRISO = UPPER ( #NP# ) ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27616C627551554552717565270A'
    setup.verifyHQCEntryExists()

    # add entry13
    stmt = defs.prepXX + """select * from F01
where colchriso = UPPER('albUQUERque');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'UPPER008')
    defs.hkey = """SELECT * FROM F01 WHERE COLCHRISO = UPPER ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27616C625551554552717565270A'
    setup.verifyHQCEntryExists()

    # increase hits, entry9
    stmt = defs.prepXX + """select * from F01
where colchrutf8 = UPPER('boston');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'UPPER009')
    defs.hkey = """SELECT * FROM F01 WHERE COLCHRUTF8 = UPPER ( #NP# ) ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '27626F73746F6E270A'
    setup.verifyHQCEntryExists()

    # increase hits,  entry10
    stmt = defs.prepXX + """select * from F01
where colvchriso = UPPER('st. Louis');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'UPPER010')
    defs.hkey = """SELECT * FROM F01 WHERE COLVCHRISO = UPPER ( #NP# ) ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '2773742E204C6F756973270A'
    setup.verifyHQCEntryExists()

    # increase hits,  entry11
    stmt = defs.prepXX + """select * from F01
where colvchrutf8 = UPPER('los angeles');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'UPPER011')
    defs.hkey = """SELECT * FROM F01 WHERE COLVCHRUTF8 = UPPER ( #NP# ) ;"""
    defs.num_hits = 1
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '276C6F7320616E67656C6573270A'
    setup.verifyHQCEntryExists()

    # add entry14
    stmt = defs.prepXX + """select * from F01
where colvchrutf8 = UPPER('Los Angeles');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    output = _dci.cmdexec("""execute XX;""")
    _dci.expect_file(output, defs.expfile, 'UPPER011')
    defs.hkey = """SELECT * FROM F01 WHERE COLVCHRUTF8 = UPPER ( #NP# ) ;"""
    defs.num_hits = 0
    defs.num_pliterals = 0
    defs.num_npliterals = 1
    defs.npliterals = '274C6F7320416E67656C6573270A'
    setup.verifyHQCEntryExists()

    _testmgr.testcase_end(desc)
