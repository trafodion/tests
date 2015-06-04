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

#**************************************************************
#			test0001
#**************************************************************
#Modification History: TestR111

def test0001(desc="test0001"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """drop procedure RS262;"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure RS262(out out_param  varchar(150))
        language java
        parameter style java
        external name 'scroll.RS262'
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS262(?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure RS262;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#			test0002
#**************************************************************
#Modification History: TestR112

def test0002(desc="test0002"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS263(out out_param  varchar(150))
        language java
        parameter style java
        external name 'scroll.RS263'
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS263(?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure RS263;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#			test0003
#**************************************************************
#Modification History: TestR113

def test0003(desc="test0003"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS264(out out_param  varchar(150))
        language java
        parameter style java
        external name 'scroll.RS264'
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS264(?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*** ERROR[11220]*""")

    stmt = """drop procedure RS264;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#	 	test0004
#**************************************************************
#Modification History: TestR115

def test0004(desc="test0004"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS235()
        language java
        parameter style java
        external name 'jdbcThread1.RS235'
        dynamic result sets 3
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS235();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure RS235;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#			test0005
#**************************************************************
#Modification History: TestR117

def test0005(desc="test0005"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure N0215(date, out out1 date)
        external name 'Procs.N0215'
        library qa_spjrs
        language java
        parameter style java
        dynamic result sets -2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#		    test0006
#Issue with delimiters.
#**************************************************************
#Modification History: TestR121

def test0006(desc="test0006"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS346()
        language java
        parameter style java
        external name 'RS254.RS346'
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS346();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure RS346;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0007
#**************************************************************
#Modification History: TestR123

def test0007(desc="test0007"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS207()
        language java
        parameter style java
        external name 'spjrs.RS207 '
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS207();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure RS207;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0008
#**************************************************************
#Modification History: TestR124

def test0008(desc="test0008"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS316()
        language java
        parameter style java
        external name 'RS205.RS316'
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS316();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure RS316;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#	                    test0009
#**************************************************************
#Modification History: TestR144

def test0009(desc="test0009"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS213()
        language java
        parameter style java
        external name 'spjrs.RS213'
        dynamic result sets 3
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS213();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure RS213;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#	                    test0010
#**************************************************************
#Modification History: TestR151

def test0010(desc="test0010"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS210()
        language java
        parameter style java
        external name 'RS210.RS210'
        dynamic result sets 25
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS210();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure RS210;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#	                    test0011
#**************************************************************
#Modification History: TestR152

def test0011(desc="test0011"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS348()
        language java
        parameter style java
        external name 'RS210.RS348'
        dynamic result sets 17
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS348();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)

    stmt = """Call RS348();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into testtab values( 'AAA Computers',  1234567890, 'San Francisco', 'programmer',  123456789,  32766,  date '2001-10-30',  time '10:10:10',  timestamp '2001-10-10 10:10:10.00',  123456789987654321,  3.40E+37,  3.0125E+18,  1.78145E+75,  8765432.45678,  8765478.56895,  987654321.0,  123456789.0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*1 row(s) inserted*""")

    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)

    stmt = """Call RS348();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)

    stmt = """delete from testtab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*1 row(s) deleted*""")

    stmt = """drop procedure RS348;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#	 		test0012
#**************************************************************
#Modification History: TestR163

def test0012(desc="test0012"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure N0215(date, out out1 date)
        external name 'Procs.N0215'
        library qa_spjrs
        language java
        parameter style java
        dynamic result sets 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#	                    test0013
#**************************************************************
#Modification History: TestR164

def test0013(desc="test0013"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS350(OUT type varchar(35), OUT conc varchar(35))
        language java
        parameter style java
        external name 'RS320.RS352'
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """call rs350(?,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure RS350;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#	                    test0014
#**************************************************************
#Modification History: TestR165

def test0014(desc="test0014"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS351(OUT type varchar(35), OUT conc varchar(35))
        language java
        parameter style java
        external name 'RS320.RS351'
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

#$err_msg 11242
#Note: No timeout error in Trafodion
    stmt = """Call RS351(?,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure RS351;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#	                    test0015
#**************************************************************
#Modification History: TestR166

def test0015(desc="test0015"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS352()
        external name 'RS205.RS352'
        library qa_spjrs
        language java
        parameter style java
        dynamic result sets 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS352();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure RS352;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0016
#**************************************************************
#Modification History: TestR167

def test0016(desc="test0016"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS216()
        language java
        parameter style java
        external name 'defaultcon.RS216'
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """call RS216();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test162exp""", "verify")

    stmt = """drop procedure RS216;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0017
#**************************************************************
#Modification History: TestR168

def test0017(desc="test0017"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS217()
        language java
        parameter style java
        external name 'defaultcon.RS217'
        dynamic result sets 2
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """call RS217();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test163exp""", "verify")

    stmt = """drop procedure RS217;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0018
#**************************************************************
#Modification History: TestR170

def test0018(desc="test0018"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """drop procedure RS366;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop procedure RS202;"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure RS202()
        language java
        parameter style java
        external name 'spjrs.RS202 '
        dynamic result sets 2
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """create procedure RS366()
        language java
        parameter style java
        external name 'RS500.RS366'
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS366();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure RS366;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop procedure RS202;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0019
#**************************************************************
#Modification History: TestR192

def test0019(desc="test0019"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """set param ?p 10;"""
    output = _dci.cmdexec(stmt)

    stmt = """Call  totalprice(23, 'standard', ?p);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0020
#**************************************************************
#Modification History: TestR193

def test0020(desc="test0020"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """set param ?p 10;"""
    output = _dci.cmdexec(stmt)

    stmt = """Call  totalprice(15, 'nextday', ?p);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0021
#**************************************************************
#Modification History: TestR194

def test0021(desc="test0021"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """set param ?p 10;"""
    output = _dci.cmdexec(stmt)

    stmt = """Call  totalprice(18, 'economy', ?p);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#			test0022
#**************************************************************
#Modification History: TestR196

def test0022(desc="test0022"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure N0215(date, out out1 date)
        external name 'samemethods.N0215'
        library qa_spjrs
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure N0215;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#  		      test0023
#**************************************************************
#Modification History: TestR198

def test0023(desc="test0023"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """delete from testtab;"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into testtab values( 'AAA Computers',  1234567890, 'San Francisco', 'programmer',  123456789,  32766,  date '2001-10-30',  time '10:10:10',  timestamp '2001-10-10 10:10:10.00',  123456789987654321,  3.40E+37,  3.0125E+18,  1.78145E+75,  8765432.45678,  8765478.56895,  987654321.0,  123456789.0);"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure RS786(varchar(100))
        language java
        parameter style java
        external name 'RS205.NS786'
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS786('datetime_interval');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure RS786;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#		    test0025
#**************************************************************
#Modification History: TestR201

def test0025(desc="test0025"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS333()
        language java
        parameter style java
        external name 'RS205.RS333'
        dynamic result sets 2
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS333();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test434exp""", "verify")

    stmt = """drop procedure RS333;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#		    test0026
#**************************************************************
#Modification History: TestR202

def test0026(desc="test0026"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS334()
        language java
        parameter style java
        external name 'RS205.RS334'
        dynamic result sets 3
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS334();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test435exp""", "verify")

    stmt = """drop procedure RS334;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#		    test0027
#need to fix.
#**************************************************************
#Modification History: TestR204

def test0027(desc="test0027"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS336()
        language java
        parameter style java
        external name 'RS205.RS336'
        dynamic result sets 3
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS336();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure RS336;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#		    test0029
#**************************************************************
#Modification History: TestR208

def test0029(desc="test0029"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS786(varchar(100))
        language java
        parameter style java
        external name 'RS205.NS786'
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """call RS786('d4');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure RS786;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#		test0030
#**************************************************************
#Purpose: 		Call statement functionality..
#SPJ:			RS276
#SPJ Parameters:		None.
#SPJ Actions: 		Alter the table name and return RS.
#Modification History: TestR226

def test0030(desc="test0030"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create table btab (a int, b int, c int, d int not null primary key);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into btab values ( 752975,53781,573553,6646464);"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure RS276()
        language java
        parameter style java
        external name 'RS500.RS276'
        dynamic result sets 2
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)

    stmt = """prepare  lorven from call RS276();"""
    output = _dci.cmdexec(stmt)

    stmt = """execute lorven;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """alter table btab add column e int;"""
    output = _dci.cmdexec(stmt)

    stmt = """execute lorven;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop table btab;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop procedure rs276;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#		test0031
#**************************************************************
#Modification History: TestR228

def test0031(desc="test0031"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create table btab (a int, b int, c int, d int not null primary key);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into btab values ( 752975,53781,573553,6646464);"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure RS276()
        language java
        parameter style java
        external name 'RS500.RS276'
        dynamic result sets 2
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)

    stmt = """prepare  lorven from call RS276();"""
    output = _dci.cmdexec(stmt)

    stmt = """execute lorven;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop table btab;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table btab (a int, b int, c int, d int not null primary key);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into btab values ( 752975,53781,573553,6646464);"""
    output = _dci.cmdexec(stmt)

    stmt = """alter table btab add column e int;"""
    output = _dci.cmdexec(stmt)

    stmt = """execute lorven;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop table btab;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop procedure rs276;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#		test0032
#**************************************************************
#Modification History: TestR232

def test0032(desc="test0032"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create table btab (a int, b int, c int, d int not null primary key);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into btab values ( 752975,53781,573553,6646464);"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure RS276()
        language java
        parameter style java
        external name 'RS500.RS276'
        dynamic result sets 2
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)

    stmt = """prepare  lorven from call RS276();"""
    output = _dci.cmdexec(stmt)

    stmt = """execute lorven;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop table btab;"""
    output = _dci.cmdexec(stmt)

    stmt = """control query default automatic_recompilation 'ON';"""
    output = _dci.cmdexec(stmt)

    stmt = """create table btab (c1 int, b2 int, c2 int, d2 int not null primary key);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into btab values ( 752975,53781,573553,6646464);"""
    output = _dci.cmdexec(stmt)

    stmt = """execute lorven;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop table btab;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop procedure rs276;"""
    output = _dci.cmdexec(stmt)

    stmt = """control query default automatic_recompilation reset;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#	                    test0035
#**************************************************************
#Modification History: TestR237

def test0035(desc="test0035"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """drop table sp402;"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure RS266()
        language java  parameter style java
        library qa_spjrs
        dynamic result sets 12
        NO TRANSACTION REQUIRED
        external name 'mxdatatypes.RS266';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS266();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- 6 row(s) selected.*""")
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure RS266;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop table sp402;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#	                    test0036
#**************************************************************
#Modification History: TestR240

def test0036(desc="test0036"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """drop table NS102;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table ns102 (c1 int, c2 int) no partitions;"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into ns102 values(100,2),(200,2),(300,0),(400,2),(500,2);"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure RS275( fetchSize int,consumeNumRows int,isScrollable int,OUT fetchSizeUsed int,
        OUT numRowsConsumed int,OUT type char(20))
        external name 'RS320.RS275'
        library qa_spjrs
        language java
        parameter style java
        dynamic result sets 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """call RS275(4,0,0,?,?,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    stmt = """drop procedure RS275;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#	                    test0037
#**************************************************************
#Modification History: TestR241

def test0037(desc="test0037"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS267 ( )
        external name 'RS205.RS267'
        library qa_spjrs
        language java
        dynamic result sets 1
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """call RS267();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    stmt = """drop procedure RS267;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#	                    test0039
#**************************************************************
#Modification History: TestR243

def test0039(desc="test0039"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS269 ( )
        external name 'RS205.RS269'
        library qa_spjrs
        language java
        dynamic result sets 1
        NO TRANSACTION REQUIRED
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """call RS269();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure RS269;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#	                    test0040
#**************************************************************
#Modification History: TestR106

def test0040(desc="test0040"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS363()
        language java
        parameter style java
        external name 'RS500.RS363'
        dynamic result sets 0
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """create procedure RS200()
        language java
        parameter style java
        external name 'spjrs.RS200A'
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS363();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Drop procedure RS363;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure rs200;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#	                    test0043
#**************************************************************
#SPJ:			RS350a
#SPJ Parameters:		None.
#SPJ Actions: 		rs.next() twice.
#Modification History: TestR249

def test0043(desc="test0043"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS350()
        language java
        parameter style java
        external name 'RS320.RS350a'
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS350();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure RS350;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#	                    test0044
#**************************************************************
#Modification History: TestR253

def test0044(desc="test0044"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """drop table m26;"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure RS281a()
        language java
        parameter style java
        external name 'RS500.RS281a'
        dynamic result sets 2
        NO TRANSACTION REQUIRED
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS281a();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure RS281a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop table m26;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#	                    test0045
#**************************************************************
#Modification History: TestR255

def test0045(desc="test0045"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS279()
        language java
        parameter style java
        external name 'RS500.RS279'
        dynamic result sets 19
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS279();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure RS279;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#	                    test0046
#**************************************************************
#Modification History: TestR256

def test0046(desc="test0046"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """drop table a13;"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure RS288()
        language java  parameter style java
        library qa_spjrs
        dynamic result sets 3
        NO TRANSACTION REQUIRED
        external name 'RS500.RS288';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS288();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure RS288;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop table a13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#	                    test0047
#**************************************************************
#Modification History: TestR257

def test0047(desc="test0047"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS289()
        language java  parameter style java
        library qa_spjrs
        dynamic result sets 3
        NO TRANSACTION REQUIRED
        external name 'RS500.RS289';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS289();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure RS289;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#	                    test0048
#**************************************************************
#Modification History: TestR258

def test0048(desc="test0048"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS289()
        language java  parameter style java
        library qa_spjrs
        dynamic result sets 3
        NO TRANSACTION REQUIRED
        external name 'RS500.RS289';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS289();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure RS289;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#	                    test0049
#**************************************************************
#Modification History: TestR259

def test0049(desc="test0049"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS292()
        language java  parameter style java
        library qa_spjrs
        dynamic result sets 3
        external name 'RS500.RS292';"""
    output = _dci.cmdexec(stmt)

    stmt = """delete from testtab;"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into testtab values( 'AAA Computers',  1234567890, 'San Francisco', 'programmer',  123456789,  32766,  date '2001-10-30',  time '10:10:10',  timestamp '2001-10-10 10:10:10.00',  123456789987654321,  3.40E+37,  3.0125E+18,  1.78145E+75,  8765432.45678,  8765478.56895,  987654321.0,  123456789.0);"""
    output = _dci.cmdexec(stmt)

    stmt = """Call RS292();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure RS292;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """select * from testtab;"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into testtab values( 'AAA Computers',  1234567890, 'San Francisco', 'programmer',  123456789,  32766,  date '2001-10-30',  time '10:10:10',  timestamp '2001-10-10 10:10:10.00',  123456789987654321,  3.40E+37,  3.0125E+18,  1.78145E+75,  8765432.45678,  8765478.56895,  987654321.0,  123456789.0);"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0050
#**************************************************************
#Modification History: TestR263

def test0050(desc="test0050"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """drop procedure RS365;"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure RS365()
        language java
        parameter style java
        external name 'RS500.RS365'
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS365();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure RS365;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0051
#**************************************************************
#Modification History: TestR266

def test0051(desc="test0051"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """insert into testtab values( 'AAA Computers',  1234567890, 'San Francisco', 'programmer',  123456789,  32766,  date '2001-10-30',  time '10:10:10',  timestamp '2001-10-10 10:10:10.00',  123456789987654321,  3.40E+37,  3.0125E+18,  1.78145E+75,  8765432.45678,  8765478.56895,  987654321.0,  123456789.0);"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure RS202()
        language java
        parameter style java
        external name 'spjrs.RS202 '
        dynamic result sets 2
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS202();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test106exp""", "verify")

    stmt = """drop procedure RS202;"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure RS202()
        language java
        parameter style java
        external name 'spjrs.RS202 '
        dynamic result sets 3
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)

    stmt = """Call RS202();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure RS202;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0053
#**************************************************************
#Modification History: TestR271

def test0053(desc="test0053"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS205b(char(20))
        language java
        parameter style java
        external name 'overLoad.RS206'
        dynamic result sets 2
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, "11239")

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0054
#**************************************************************
#Modification History: TestR272

def test0054(desc="test0054"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS205x(largeint)
        language java
        parameter style java
        external name 'overLoad.RS207'
        dynamic result sets 2
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, "11230")

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0055
#**************************************************************
#Modification History: TestR273

def test0055(desc="test0055"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS205ns(largeint)
        language java
        parameter style java
        external name 'overLoad.RS207(long,java.sql.ResultSet[])'
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure RS205ns;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0056
#**************************************************************
#Modification History: TestR274

def test0056(desc="test0056"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS208(largeint)
        language java
        parameter style java
        external name 'overLoad.RS208 '
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, "11239")

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0057
#**************************************************************
#Modification History: TestR275

def test0057(desc="test0057"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS205bc()
        language java
        parameter style java
        external name 'spjrs.RS205'
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure RS205bc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0058
#**************************************************************
#Modification History: TestR277

def test0058(desc="test0058"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """insert into testtab values( 'AAA Computers',  1234567890, 'San Francisco', 'programmer',  123456789,  32766,  date '2001-10-30',  time '10:10:10',  timestamp '2001-10-10 10:10:10.00',  123456789987654321,  3.40E+37,  3.0125E+18,  1.78145E+75,  8765432.45678,  8765478.56895,  987654321.0,  123456789.0);"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure RS208()
        language java
        parameter style java
        external name 'spjrs.RS208 '
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS208();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test119exp""", "verify")

    stmt = """drop procedure RS208;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0059
#**************************************************************
#Modification History: TestR278

def test0059(desc="test0059"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS201()
        language java
        parameter style java
        external name 'spjrs.RS201'
        dynamic result sets 2
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS201();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test120exp""", "verify")

    stmt = """drop procedure RS201;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0060
#**************************************************************
#Modification History: TestR279

def test0060(desc="test0060"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS201b()
        language java
        parameter style java
        external name 'spjrs.RS201b'
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS201b();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test121exp""", "verify")

    stmt = """drop procedure RS201b;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0061
#**************************************************************
#Modification History: TestR280

def test0061(desc="test0061"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS200c()
        language java
        parameter style java
        external name 'spjrs.RS200c '
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS200c();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test122exp""", "verify")

    stmt = """drop procedure RS200c;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0062
#**************************************************************
#Modification History: TestR281

def test0062(desc="test0062"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS200d()
        language java
        parameter style java
        external name 'spjrs.RS200d '
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS200d();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test123exp""", "verify")

    stmt = """drop procedure RS200d;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0063
#**************************************************************
#Modification History: TestR282

def test0063(desc="test0063"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS200e()
        language java
        parameter style java
        external name 'spjrs.RS200e '
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS200e();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test124exp""", "verify")

    stmt = """drop procedure RS200e;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0064
#**************************************************************
#Modification History: TestR283

def test0064(desc="test0064"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS300()
        language java
        parameter style java
        external name 'mxdatatypes.RS300'
        dynamic result sets 31
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS300();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test125exp""", "verify")

    stmt = """drop procedure RS300;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0065
#**************************************************************
#Modification History: TestR284

def test0065(desc="test0065"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS205bc()
        language java
        parameter style java
        external name 'RS205.RS206'
        dynamic result sets 3
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS205bc();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test127exp""", "verify")

    stmt = """drop procedure RS205bc;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0066
#**************************************************************
#Modification History: TestR287

def test0066(desc="test0066"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS310()
        language java
        parameter style java
        external name 'Jdbc_Get_BigDecimal.RS310'
        dynamic result sets 2
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS310();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test130exp""", "verify")

    stmt = """drop procedure RS310;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0067
#**************************************************************
#Modification History: TestR288

def test0067(desc="test0067"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS311()
        language java
        parameter style java
        external name 'Jdbc_Get_VString.RS311'
        dynamic result sets 2
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS311();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test131exp""", "verify")

    stmt = """drop procedure RS311;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0068
#**************************************************************
#Modification History: TestR289

def test0068(desc="test0068"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS312()
        language java
        parameter style java
        external name 'Jdbc_Get_Double.RS312'
        dynamic result sets 2
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS312();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test132exp""", "verify")

    stmt = """drop procedure RS312;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0069
#**************************************************************
#Modification History: TestR290

def test0069(desc="test0069"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """drop procedure RS313;"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure RS313()
        language java
        parameter style java
        external name 'Jdbc_Get_Float.RS313'
        dynamic result sets 2
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS313();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test133exp""", "verify")

    stmt = """drop procedure RS313;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0070
#**************************************************************
#Modification History: TestR291

def test0070(desc="test0070"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS314()
        language java
        parameter style java
        external name 'Jdbc_Get_Int.RS314'
        dynamic result sets 2
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS314();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test134exp""", "verify")

    stmt = """drop procedure RS314;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0071
#**************************************************************
#Modification History: TestR292

def test0071(desc="test0071"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """drop procedure RS315;"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure RS315()
        language java
        parameter style java
        external name 'RS205.RS315'
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS315();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test135exp""", "verify")

    stmt = """drop procedure RS315;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#                         test0072
#**************************************************************
#Modification History: TestR293

def test0072(desc="test0072"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS317()
        language java
        parameter style java
        external name 'RS205.RS317'
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test136exp""", "verify")

    stmt = """Call RS317();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """select count(*)  from b2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test136aexp""", "verify")

    stmt = """drop procedure RS317;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

#purgedata b2;
    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0073
#**************************************************************
#Modification History: TestR295

def test0073(desc="test0073"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS204()
        language java
        parameter style java
        external name 'RS254.RS204 '
        dynamic result sets 13
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS204();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure RS204;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0075
#**************************************************************
#Modification History: TestR298

def test0075(desc="test0075"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS321()
        language java
        parameter style java
        external name 'mxdatatypes.RS321'
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS321();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test142exp""", "verify")

    stmt = """drop procedure RS321;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0077
#**************************************************************
#Modification History: TestR300

def test0077(desc="test0077"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS322()
        language java
        parameter style java
        external name 'RS322.RS322'
        dynamic result sets 7
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS322();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test144exp""", "verify")

    stmt = """drop procedure RS322;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0078
#**************************************************************
#Modification History: TestR301

def test0078(desc="test0078"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS323()
        language java
        parameter style java
        external name 'RS323.RS323'
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS323();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test145exp""", "verify")

    stmt = """drop procedure RS323;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0079
#**************************************************************
#Modification History: TestR302

def test0079(desc="test0079"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS323()
        language java
        parameter style java
        external name 'RS323.RS323a'
        dynamic result sets 13
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS323();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test146exp""", "verify")

    stmt = """drop procedure RS323;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0080
#**************************************************************
#Modification History: TestR303

def test0080(desc="test0080"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS323()
        language java
        parameter style java
        external name 'RS323.RS323b'
        dynamic result sets 27
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS323();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test147exp""", "verify")

    stmt = """drop procedure RS323;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0081
#**************************************************************
#Modification History: TestR304

def test0081(desc="test0081"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS324()
        language java
        parameter style java
        external name 'RS324.RS324'
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS324();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test148exp""", "verify")

    stmt = """drop procedure RS324;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0082
#**************************************************************
#Modification History: TestR305

def test0082(desc="test0082"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS324()
        language java
        parameter style java
        external name 'RS324.RS324a'
        dynamic result sets 8
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS324();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test149exp""", "verify")

    stmt = """drop procedure RS324;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0083
#**************************************************************
#Modification History: TestR306

def test0083(desc="test0083"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS325()
        language java
        parameter style java
        external name 'RS325.RS325'
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS325();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test150exp""", "verify")

    stmt = """drop procedure RS325;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0084
#**************************************************************
#Modification History: TestR307

def test0084(desc="test0084"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS325()
        language java
        parameter style java
        external name 'RS325.RS325a'
        dynamic result sets 10
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS325();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test151exp""", "verify")

    stmt = """drop procedure RS325;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0085
#**************************************************************
#Modification History: TestR308

def test0085(desc="test0085"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS326()
        language java
        parameter style java
        external name 'RS326.RS326'
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS326();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test152exp""", "verify")

    stmt = """drop procedure RS326;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0086
#**************************************************************
#Modification History: TestR309

def test0086(desc="test0086"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS326()
        language java
        parameter style java
        external name 'RS326.RS326a'
        dynamic result sets 11
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS326();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test153exp""", "verify")

    stmt = """drop procedure RS326;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0087
#**************************************************************
#Modification History: TestR314

def test0087(desc="test0087"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure DRS202()
        language java
        parameter style java
        external name 'defaultcon.DRS202'
        dynamic result sets 245
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call  DRS202();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test159exp""", "verify")

    stmt = """drop procedure drs202;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0088
#**************************************************************
#Modification History: TestR315

def test0088(desc="test0088"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """drop procedure RS327;"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure RS327()
        language java
        parameter style java
        external name 'RS320.RS327'
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """call RS327();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test160exp""", "verify")

    stmt = """select count(*)  from b32;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop procedure RS327;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0089
#**************************************************************
#Modification History: TestR316

def test0089(desc="test0089"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS328()
        language java
        parameter style java
        external name 'RS320.RS328'
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """call RS328();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test161exp""", "verify")

    stmt = """select count(*) from b2pns03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- 1 row(s) selected.*""")

    stmt = """drop procedure RS328;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

#purgedata b2;
    _testmgr.testcase_end(desc)

#*********************************************************************
#                            test0090
#*********************************************************************
#Modification History: TestR318

def test0090(desc="test0090"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS261(out out_param  varchar(150))
        language java
        parameter style java
        external name 'scroll.RS261'
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS261(?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*** ERROR[11220]*""")

    stmt = """drop procedure RS261;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#	                    test009
#**************************************************************
#Modification History: TestR333

def test0091(desc="test0091"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS353(fetchSize int, consumeNumRows int, isScrollable int,
        out fetchSizeUsed int, out numRowsConsumed int, out type varchar(50))
        external name 'RS327.RS353'
        library qa_spjrs
        language java
        parameter style java
        dynamic result sets 1;"""
    output = _dci.cmdexec(stmt)

    stmt = """Call RS353(0,0,0,?,?,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")
    _dci.expect_any_substr(output, """*--- 19 row(s) selected.*""")

    stmt = """Call RS353(0,9,0,?,?,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- 10 row(s) selected.*""")
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS353(0,25,0,?,?,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS353(0,19,0,?,?,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- 0 row(s) selected.*""")
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS353(5,9,1,?,?,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- 19 row(s) selected.*""")
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS353(5,25,1,?,?,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- 19 row(s) selected.*""")
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS353(5,19,1,?,?,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- 19 row(s) selected.*""")
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS353(1000,19,1,?,?,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- 19 row(s) selected.*""")
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS353(5,9,2,?,?,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- 19 row(s) selected.*""")
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS353(5,25,2,?,?,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- 19 row(s) selected.*""")
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS353(5,19,2,?,?,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- 19 row(s) selected.*""")
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS353(1000,19,2,?,?,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- 19 row(s) selected.*""")
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure RS353;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#                                test0092
#**************************************************************
#Purpose: 		Verifying the Call functionality for RS
#SPJ:			RS332
#SPJ Parameters:		None
#SPJ Actions: 		Verifying RS functionality.
#Comments:		RS from two tables.
#Modification History: TestR345

def test0092(desc="test0092"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS331()
        language java
        parameter style java
        external name 'RS325.RS331'
        dynamic result sets 2
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call rs331();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test433exp""", "verify")

    stmt = """drop procedure rs331;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#	                    test0093
#**************************************************************
#Modification History: TestR366

def test0093(desc="test0093"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS267 ( )
        external name 'RS205.RS267'
        library qa_spjrs
        language java
        dynamic result sets 1
        parameter style java;"""
    output = _dci.cmdexec(stmt)

    stmt = """call RS267();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    stmt = """drop procedure RS267;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#	                    test0094
#**************************************************************
#Modification History: TestR368

def test0094(desc="test0094"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS269 ( )
        external name 'RS205.RS269'
        library qa_spjrs
        language java
        dynamic result sets 1
        NO TRANSACTION REQUIRED
        parameter style java;"""
    output = _dci.cmdexec(stmt)

    stmt = """call RS269();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure RS269;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    _testmgr.testcase_end(desc)

#*********************************************************************
#                            test0095
#*********************************************************************
#Modification History: TestR373

def test0095(desc="test0095"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS786(varchar(100))
        language java
        parameter style java
        external name 'RS205.NS786'
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS786('str_num');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test340exp""", "verify")

    stmt = """drop procedure RS786;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#*********************************************************************
#                            test0096
#*********************************************************************
#Modification History: TestR374

def test0096(desc="test0096"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS786(varchar(100))
        language java
        parameter style java
        external name 'RS205.NS786'
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS786('nshour');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test341exp""", "verify")

    stmt = """drop procedure RS786;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#*********************************************************************
#                            test0100
#*********************************************************************
#Modification History: TestR382

def test0101(desc="test0100"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS786(varchar(100))
        language java
        parameter style java
        external name 'RS205.NS786'
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS786('trn');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test345exp""", "verify")

    stmt = """drop procedure RS786;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#*********************************************************************
#                            test0102
#*********************************************************************
#Modification History: TestR387

def test0102(desc="test0102"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS786(varchar(100))
        language java
        parameter style java
        external name 'RS205.NS786'
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS786('trs');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test361exp""", "verify")

    stmt = """drop procedure RS786;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#*********************************************************************
#                                        test0103
#*********************************************************************
#Modification History: TestR388

def test0103(desc="test0103"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """call jdbc_get_date(?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#*********************************************************************
#                            test0104
#*********************************************************************
#Modification History: TestR389

def test0104(desc="test0104"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Call jdbc_get_float(?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#*********************************************************************
#                            test0105
#*********************************************************************
#Modification History: TestR390

def test0105(desc="test0105"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Call jdbc_get_long(?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#*********************************************************************
#                            test0106
#*********************************************************************
#Modification History: TestR391

def test0106(desc="test0106"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Call jdbc_get_string(?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#*********************************************************************
#                            test0107
#*********************************************************************
#Modification History: TestR392

def test0107(desc="test0107"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Call jdbc_get_time(?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#*********************************************************************
#                            test0108
#*********************************************************************
#Modification History: TestR393

def test0108(desc="test0108"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure N0217 (IN IN1 Timestamp, OUT OUT1 Timestamp)
        external name 'Procs.N0217'
        library qa_spjrs
        parameter style java
        language java;"""
    output = _dci.cmdexec(stmt)

    stmt = """Call N0217(timestamp'2004-10-13 13:43:14.937025',?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure N0217;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#*********************************************************************
#                            test0109
#*********************************************************************
#Modification History: TestR395

def test0109(desc="test0109"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """set param ?x 3434;"""
    output = _dci.cmdexec(stmt)

    stmt = """Call jdbc_io_float(?x);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#*********************************************************************
#                            test0110
#*********************************************************************
#Modification History: TestR396

def test0110(desc="test0110"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """set param ?x 3434;"""
    output = _dci.cmdexec(stmt)

    stmt = """Call jdbc_io_int(?x);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#*********************************************************************
#                            test0111
#*********************************************************************
#Modification History: TestR397

def test0111(desc="test0111"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """set param ?x 434;"""
    output = _dci.cmdexec(stmt)

    stmt = """Call jdbc_io_short(?x);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#*********************************************************************
#                            test0112
#*********************************************************************
#Modification History: TestR398

def test0112(desc="test0112"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """set param ?x 'Hewlett Packard';"""
    output = _dci.cmdexec(stmt)

    stmt = """Call jdbc_io_vstring(?x);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#*********************************************************************
#                            test0113
#*********************************************************************
#Modification History: TestR399

def test0113(desc="test0113"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """set param ?x '12:10:45';"""
    output = _dci.cmdexec(stmt)

    stmt = """Call jdbc_io_time(?x);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#*********************************************************************
#                            test0114
#*********************************************************************
#Modification History: TestR400

def test0114(desc="test0114"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """set param ?x '2004-10-26 11:50:05.640589';"""
    output = _dci.cmdexec(stmt)

    stmt = """Call jdbc_io_timestamp(?x);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#*********************************************************************
#                            test0115
#DUP command inside SPJ body.
# DUP is not supported on seaquset, the SPJ changed to use create table as
#**************************************************************
#Modification History: TestR401

def test0115(desc="test0115"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """drop procedure RS281a;"""
    output = _dci.cmdexec(stmt)

    stmt = """create procedure RS281a()
        language java
        parameter style java
        external name 'RS500.RS281a'
        NO TRANSACTION REQUIRED
        dynamic result sets 2
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS281a();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure RS281a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#*********************************************************************
#                            test0117
#*********************************************************************
#Modification History: TestR404

def test0117(desc="test0117"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Call  jdbc_set_float(12E3,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*** ERROR[11220]*""")

    _testmgr.testcase_end(desc)

#*********************************************************************
#                            test0119
#*********************************************************************
#Modification History: TestR409

def test0119(desc="test0119"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Call  jdbc_set_time(time '04:04:04',?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#*********************************************************************
#                            test0120
#*********************************************************************
#Modification History: TestR410

def test0120(desc="test0120"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Call  jdbc_set_timestamp(timestamp '1984-05-05 04:04:04.000000',?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#*********************************************************************
#				test0121
#*********************************************************************
#Modification History: TestR412

def test0121(desc="test0121"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure N0200 (IN IN1 VARCHAR(50), OUT OUT1 VARCHAR(50))
        external name 'Procs.N0200'
        library qa_spjrs
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """call N0200(('hello' + 'world'),?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR[4034]*""")

    stmt = """call N0200(('hello'  '+'  'world'),?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure N0200;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***********************************************************************
#				test0122
#***********************************************************************
#Modification History: TestR414

def test0122(desc="test0122"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure N0200 ( character varying(10), out  picture xxxxxxxx)
        external name 'Procs.N0200'
        library qa_spjrs
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """call N0200 ('helloworld',?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """showddl N0200BC;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop procedure N0200;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#                            test0123
#**************************************************************
#Modification History: TestR415

def test0123(desc="test0123"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """call jdbc_get_bigdecimal(?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#                            test0124
#**************************************************************
#Modification History: TestR416

def test0124(desc="test0124"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Call jdbc_get_double(?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#                            test0125
#**************************************************************
#Modification History: TestR417

def test0125(desc="test0125"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Call jdbc_get_int(?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#                            test0126
#**************************************************************
#Modification History: TestR418

def test0126(desc="test0126"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Call jdbc_get_short(?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#                            test0127
#**************************************************************
#Modification History: TestR419

def test0127(desc="test0127"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Call jdbc_get_vstring(?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#                            test0128
#**************************************************************
#Modification History: TestR420

def test0128(desc="test0128"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Call jdbc_get_timestamp(?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#                            test0129
#**************************************************************
#Modification History: TestR421

def test0129(desc="test0129"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """set param ?x 323;"""
    output = _dci.cmdexec(stmt)

    stmt = """Call jdbc_io_double(?x);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#                            test0130
#**************************************************************
#Modification History: TestR422

def test0130(desc="test0130"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """set param ?x 345533454;"""
    output = _dci.cmdexec(stmt)

    stmt = """Call jdbc_io_long(?x);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#                            test0131
#**************************************************************
#Modification History: TestR423

def test0131(desc="test0131"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """set param ?x 'Hewlett Packard';"""
    output = _dci.cmdexec(stmt)

    stmt = """Call jdbc_io_string(?x);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#TestR for cursors.
#**************************************************************
#			test0132
#**************************************************************
#Modification History: TestR428

def test0132(desc="test0132"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS256(out out_param  varchar(150))
        language java
        parameter style java
        external name 'scroll.RS256'
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS256(?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test409exp""", "verify")

    stmt = """drop procedure RS256;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#			test0133
#**************************************************************
#Modification History: TestR429

def test0133(desc="test0133"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS257(out out_param  varchar(150))
        language java
        parameter style java
        external name 'scroll.RS257'
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS257(?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test410exp""", "verify")

    stmt = """drop procedure RS257;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#			test0134
#**************************************************************
#Modification History: TestR430

def test0134(desc="test0134"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS258(out out_param  varchar(150))
        language java
        parameter style java
        external name 'scroll.RS258'
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS258(?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure RS258;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#			test0135
#**************************************************************
#Modification History: TestR431

def test0135(desc="test0135"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS259(out out_param  varchar(150))
        language java
        parameter style java
        external name 'scroll.RS259'
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS259(?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure RS259;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************
#			test0136
#**************************************************************
#Modification History: TestR432

def test0136(desc="test0136"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS260(out out_param  varchar(150))
        language java
        parameter style java
        external name 'scroll.RS260'
        dynamic result sets 1
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS260(?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure RS260;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

#**************************************************************
#		test0140
#**************************************************************
#Modification History: TestR181

def test0140(desc="test0140"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS200()
        language java
        parameter style java
        external name 'spjrs.getobject'
        dynamic result sets 2
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """call RS200();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure RS200;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************
#	                    test0141
#**************************************************************
#Modification History: TestR251

def test0141(desc="test0141"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create procedure RS277()
        language java
        parameter style java
        external name 'RS500.RS277'
        NO TRANSACTION REQUIRED
        dynamic result sets 2
        library qa_spjrs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call RS277();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure RS277;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop table tb2 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop table tb1 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**********************************************************************
#	                    test0142
# comment: Bug #1437102 is opened for this test. Since it will cause
#          session to hang, commented out until the bug is fixed.
#**********************************************************************
#Modification History: TestR252
#
#def test0142(desc="test0142"):
#
#    global _testmgr
#    global _testlist
#    global _dci
#    if not _testmgr.testcase_begin(_testlist):
#        return
#
#    stmt = """drop procedure RS280;"""
#    output = _dci.cmdexec(stmt)
#
#    stmt = """create procedure RS280()
#        language java
#        parameter style java
#        external name 'RS500.RS280'
#        dynamic result sets 2
#        NO TRANSACTION REQUIRED
#        library qa_spjrs;"""
#    output = _dci.cmdexec(stmt)
#    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")
#
#    stmt = """Call RS280();"""
#    output = _dci.cmdexec(stmt)
#    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")
#
#    stmt = """drop procedure RS280;"""
#    output = _dci.cmdexec(stmt)
#    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")
#
#    _testmgr.testcase_end(desc)

#***************************************************************************
#                                test0151
#***************************************************************************
# Purpose: 	  Test SPJ in No TRANSACTION REQUIRED mode
# Caller App:   In auto commit
# SPJ:	         In auto commit mode  (auto commit mode by default)
# Expected:	  SPJ SQL operation complete
#***************************************************************************
def test0151(desc="test0151"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """call InsertAutoCommitNT('txn1');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from txn1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)

    stmt = """delete from txn1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                test0152
#***************************************************************************
# Purpose: 	  Test SPJ in No TRANSACTION REQUIRED mode
# Caller App:   In auto commit
# SPJ:	         "Begin work" & "Commit"
# Expected:	  SPJ SQL operation complete
#***************************************************************************
def test0152(desc="test0152"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """call InsertCommitNT('txn1');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from txn1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)

    stmt = """delete from txn1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                test0153
#***************************************************************************
# Purpose: 	  Test SPJ in No TRANSACTION REQUIRED mode
# Caller App:   In auto commit
# SPJ:	         "Begin work" & "rollback"
# Expected:	  SPJ SQL operation complete
#***************************************************************************
def test0153(desc="test0153"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """call InsertRollbackNT('txn1');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from txn1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                test0154
#***************************************************************************
# Purpose: 	  Test SPJ in TRANSACTION REQUIRED mode
# Caller App:   In auto commit
# SPJ:	         "Begin work" & "Commit"
# Expected:	  SPJ SQL operation complete
#***************************************************************************
def test0154(desc="test0154"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """call InsertCommitT('txn1');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, "8603")

    stmt = """select * from txn1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                test0155
#***************************************************************************
# Purpose: 	  Test SPJ in TRANSACTION REQUIRED mode
# Caller App:   "Begin work" & "Commit"
# SPJ:	         In auto commit mode  (auto commit mode by default)
# Expected:	  SPJ SQL operation complete & commited
#***************************************************************************
def test0155(desc="test0155"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """call InsertAutoCommitT('txn1');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """commit;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from txn1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)

    stmt = """delete from txn1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                test0156
#***************************************************************************
# Purpose: 	  Test SPJ in NO TRANSACTION REQUIRED mode
# Caller App:   "Begin work" & "Commit"
# SPJ:	         In auto commit mode  (auto commit mode by default)
# Expected:	  SPJ SQL operation complete & commited
#***************************************************************************
def test0156(desc="test0156"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """call InsertAutoCommitNT('txn1');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """commit;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from txn1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)

    stmt = """delete from txn1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                test157
#***************************************************************************
# Purpose: 	  Test SPJ in TRANSACTION REQUIRED mode
# Caller App:   "Begin work" & "Commit"
# SPJ:	         "Begin work" & "Commit"
# Expected:	  SPJ "Begin work" failed ERROR 8603
#***************************************************************************
def test0157(desc="test0157"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """call InsertCommitT('txn1');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, "8603")

    stmt = """commit;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from txn1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                test0158
#***************************************************************************
# Purpose: 	  Test SPJ in No TRANSACTION REQUIRED mode
# Caller App:   "Begin work" & "Commit"
# SPJ:	         "Begin work" & "Commit"
# Expected:	  SPJ "Begin work" failed ERROR 8603
#***************************************************************************
def test0158(desc="test0158"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """call InsertCommitNT('txn1');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, "8603")

    stmt = """commit;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from txn1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)

    _testmgr.testcase_end(desc)
