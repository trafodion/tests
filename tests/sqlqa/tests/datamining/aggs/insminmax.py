# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2014 Hewlett-Packard Development Company, L.P.
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
    
def test001(desc="""insminmax"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # insminmax.sql
    # jclear
    # 1997-04-28
    # new aggregate tests
    # set up for the minmax table
    
    # create table minmax (
    #     counter  int,
    #     minint   int,
    #     maxint   int,
    #     minsmall smallint,
    #     maxsmall smallint
    #     );
    #
    stmt = """insert into minmax values (1, -2147483648, 2147483647, -32768, 32767),
(2, -2147483648, 2147483647, -32768, 32767),
(3, -2147483648, 2147483647, -32768, 32767),
(4, -2147483648, 2147483647, -32768, 32767),
(5, -2147483648, 2147483647, -32768, 32767),
(6, -2147483648, 2147483647, -32768, 32767),
(7, -2147483648, 2147483647, -32768, 32767),
(8, -2147483648, 2147483647, -32768, 32767),
(9, -2147483648, 2147483647, -32768, 32767),
(10, -2147483648, 2147483647, -32768, 32767);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 10)
    stmt = """insert into minmax values (11, -2147483648, 2147483647, -32768, 32767),
(12, -2147483648, 2147483647, -32768, 32767),
(13, -2147483648, 2147483647, -32768, 32767),
(14, -2147483648, 2147483647, -32768, 32767),
(15, -2147483648, 2147483647, -32768, 32767),
(16, -2147483648, 2147483647, -32768, 32767),
(17, -2147483648, 2147483647, -32768, 32767),
(18, -2147483648, 2147483647, -32768, 32767),
(19, -2147483648, 2147483647, -32768, 32767),
(20, -2147483648, 2147483647, -32768, 32767);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 10)
    stmt = """insert into minmax values (21, -2147483648, 2147483647, -32768, 32767),
(22, -2147483648, 2147483647, -32768, 32767),
(23, -2147483648, 2147483647, -32768, 32767),
(24, -2147483648, 2147483647, -32768, 32767),
(25, -2147483648, 2147483647, -32768, 32767),
(26, -2147483648, 2147483647, -32768, 32767),
(27, -2147483648, 2147483647, -32768, 32767),
(28, -2147483648, 2147483647, -32768, 32767),
(29, -2147483648, 2147483647, -32768, 32767),
(30, -2147483648, 2147483647, -32768, 32767);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 10)
    stmt = """insert into minmax values (31, -2147483648, 2147483647, -32768, 32767),
(32, -2147483648, 2147483647, -32768, 32767),
(33, -2147483648, 2147483647, -32768, 32767),
(34, -2147483648, 2147483647, -32768, 32767),
(35, -2147483648, 2147483647, -32768, 32767),
(36, -2147483648, 2147483647, -32768, 32767),
(37, -2147483648, 2147483647, -32768, 32767),
(38, -2147483648, 2147483647, -32768, 32767),
(39, -2147483648, 2147483647, -32768, 32767),
(40, -2147483648, 2147483647, -32768, 32767);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 10)
    stmt = """insert into minmax values (41, -2147483648, 2147483647, -32768, 32767),
(42, -2147483648, 2147483647, -32768, 32767),
(43, -2147483648, 2147483647, -32768, 32767),
(44, -2147483648, 2147483647, -32768, 32767),
(45, -2147483648, 2147483647, -32768, 32767),
(46, -2147483648, 2147483647, -32768, 32767),
(47, -2147483648, 2147483647, -32768, 32767),
(48, -2147483648, 2147483647, -32768, 32767),
(49, -2147483648, 2147483647, -32768, 32767),
(50, -2147483648, 2147483647, -32768, 32767);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 10)
    stmt = """insert into minmax values (51, -2147483648, 2147483647, -32768, 32767),
(52, -2147483648, 2147483647, -32768, 32767),
(53, -2147483648, 2147483647, -32768, 32767),
(54, -2147483648, 2147483647, -32768, 32767),
(55, -2147483648, 2147483647, -32768, 32767),
(56, -2147483648, 2147483647, -32768, 32767),
(57, -2147483648, 2147483647, -32768, 32767),
(58, -2147483648, 2147483647, -32768, 32767),
(59, -2147483648, 2147483647, -32768, 32767),
(60, -2147483648, 2147483647, -32768, 32767);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 10)
    stmt = """insert into minmax values (61, -2147483648, 2147483647, -32768, 32767),
(62, -2147483648, 2147483647, -32768, 32767),
(63, -2147483648, 2147483647, -32768, 32767),
(64, -2147483648, 2147483647, -32768, 32767),
(65, -2147483648, 2147483647, -32768, 32767),
(66, -2147483648, 2147483647, -32768, 32767),
(67, -2147483648, 2147483647, -32768, 32767),
(68, -2147483648, 2147483647, -32768, 32767),
(69, -2147483648, 2147483647, -32768, 32767),
(70, -2147483648, 2147483647, -32768, 32767);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 10)
    stmt = """insert into minmax values (71, -2147483648, 2147483647, -32768, 32767),
(72, -2147483648, 2147483647, -32768, 32767),
(73, -2147483648, 2147483647, -32768, 32767),
(74, -2147483648, 2147483647, -32768, 32767),
(75, -2147483648, 2147483647, -32768, 32767),
(76, -2147483648, 2147483647, -32768, 32767),
(77, -2147483648, 2147483647, -32768, 32767),
(78, -2147483648, 2147483647, -32768, 32767),
(79, -2147483648, 2147483647, -32768, 32767),
(80, -2147483648, 2147483647, -32768, 32767);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 10)
    stmt = """insert into minmax values (81, -2147483648, 2147483647, -32768, 32767),
(82, -2147483648, 2147483647, -32768, 32767),
(83, -2147483648, 2147483647, -32768, 32767),
(84, -2147483648, 2147483647, -32768, 32767),
(85, -2147483648, 2147483647, -32768, 32767),
(86, -2147483648, 2147483647, -32768, 32767),
(87, -2147483648, 2147483647, -32768, 32767),
(88, -2147483648, 2147483647, -32768, 32767),
(89, -2147483648, 2147483647, -32768, 32767),
(90, -2147483648, 2147483647, -32768, 32767);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 10)
    stmt = """insert into minmax values (91, -2147483648, 2147483647, -32768, 32767),
(92, -2147483648, 2147483647, -32768, 32767),
(93, -2147483648, 2147483647, -32768, 32767),
(94, -2147483648, 2147483647, -32768, 32767),
(95, -2147483648, 2147483647, -32768, 32767),
(96, -2147483648, 2147483647, -32768, 32767),
(97, -2147483648, 2147483647, -32768, 32767),
(98, -2147483648, 2147483647, -32768, 32767),
(99, -2147483648, 2147483647, -32768, 32767),
(100, -2147483648, 2147483647, -32768, 32767);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 10)
    
    stmt = """update minmax 
set minint = -1, maxint = 1, minsmall = -1, maxsmall = 1
where counter = 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """update minmax 
set minint = -10, maxint = 10, minsmall = -10, maxsmall = 10
where counter = 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """update minmax 
set minint = -20, maxint = 20, minsmall = -20, maxsmall = 20
where counter = 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """update minmax 
set minint = -30, maxint = 30, minsmall = -30, maxsmall = 30
where counter = 30;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """update minmax 
set minint = -40, maxint = 40, minsmall = -40, maxsmall = 40
where counter = 40;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """update minmax 
set minint = -50, maxint = 50, minsmall = -50, maxsmall = 50
where counter = 50;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """update minmax 
set minint = -60, maxint = 60, minsmall = -60, maxsmall = 60
where counter = 60;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """update minmax 
set minint = -70, maxint = 70, minsmall = -70, maxsmall = 70
where counter = 70;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """update minmax 
set minint = -80, maxint = 80, minsmall = -80, maxsmall = 80
where counter = 80;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """update minmax 
set minint = -90, maxint = 90, minsmall = -90, maxsmall = 90
where counter = 90;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """update minmax 
set minint = -100, maxint = 100, minsmall = -100, maxsmall = 100
where counter = 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select count (*) as CountStar
from minmax;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/insminmaxexp""", 'insminmaxs1')
    # expect count = 100
    
    stmt = """select
sum (maxint) as SumMaxint,
sum (minint) as SumMinint,
avg (maxint) as AvgMaxint,
avg (minint) as AvgMinint
from minmax;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/insminmaxexp""", 'insminmaxs2')
    # expect SumMax = 191126045134, SumMin = -191126045223,
    # AvgMax = 1911260451.34, AvgMin = -1911260452.23
    
    stmt = """select
max (maxint) as MaxMaxint,
max (minint) as MaxMinint,
min (maxint) as MinMaxint,
min (minint) as MinMinint
from minmax;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/insminmaxexp""", 'insminmaxs3')
    # expect MaxMax = 2147483647, MaxMin = -1,
    #        MinMax = 1, MinMin = -2147483648
    
    stmt = """select
sum (maxsmall) as SumMaxsmall,
sum (minsmall) as SumMinsmall,
avg (maxsmall) as AvgMaxsmall,
avg (minsmall) as AvgMinsmall
from minmax;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/insminmaxexp""", 'insminmaxs4')
    # expect SumMax = 2916814, SumMin = -2916903,
    #        AvgMax = 29168.14, AvgMin = -29169.03
    
    stmt = """select
max (maxsmall) as MaxMaxsmall,
max (minsmall) as MaxMinsmall,
min (maxsmall) as MinMaxsmall,
min (minsmall) as MinMinsmall
from minmax;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/insminmaxexp""", 'insminmaxs5')
    # expect MaxMax = 32767, MaxMin = -1, MinMax = 1, MinMin = -32768
    
    _testmgr.testcase_end(desc)

