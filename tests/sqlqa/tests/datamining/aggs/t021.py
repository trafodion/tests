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
    
def test001(desc="""test021"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test021
    # interval.sql
    # jclear
    # 1997-05-01
    # test the new aggregates with the interval data types
    #
    
    #- select
    #-     avg (iyr), avg (imon), avg (idy), avg (ihr), avg (imin), avg (isec)
    #-         from intrval;
    # expect 1 row with the following values:
    # 	Avgiyr	45.6315789473684
    # 	Avgimon	49.0315789473684
    # 	Avgidy	47.4736842105263
    # 	Avgihr	38.3263157894737
    # 	Avgimin	42.1578947368421
    # 	Avgisec	42.7052631578947
    
    #- select
    #-     sum (iyr), sum (imon), sum (idy), sum (ihr), sum (imin), sum (isec)
    #- 	from intrval;
    # expect 1 row with the following values:
    # 	Sumiyr	4335
    # 	Sumimon	4658
    # 	Sumidy	4510
    # 	Sumihr	3641
    # 	Sumimin	4005
    # 	Sumisec	4057
    #
    stmt = """select
min (iyr), min (imon), min (idy), min (ihr), min (imin), min (isec)
from intrval;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test021exp""", 'test021a')
    # expect 1 row with the following values:
    #	Miniyr	-79
    #	Minimon	-71
    #	Minidy	-92
    #	Minihr	-85
    #	Minimin	-99
    #	Minisec	-95
    
    stmt = """select
max (iyr), max (imon), max (idy), max (ihr), max (imin), max (isec)
from intrval;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test021exp""", 'test021b')
    # expect 1 row with the following values:
    # 	Maxiyr	99
    # 	Maximon	99
    # 	Maxidy	99
    # 	Maxihr	93
    # 	Maximax	99
    # 	Maxisec	99
    
    #- select
    #-     Variance (iyr),
    #-     Variance (imon),
    #-     Variance (idy),
    #-     Variance (ihr),
    #-     Variance (imin),
    #-     Variance (isec)
    #-         from intrval;
    #- 	from intrval;
    # expect 1 row with the following values:
    # 	PVarIyr		1373.07479224377
    # 	PVarImon	1252.76742382271
    # 	PVarIdy		1334.48088642659
    # 	PVarIhr		1041.60930747922
    # 	PVarImin	1473.39612188366
    # 	PVarIsec	1558.56576177285
    
    #- select
    #-     StdDev (iyr),
    #-     StdDev (imon),
    #-     StdDev (idy),
    #-     StdDev (ihr),
    #-     StdDev (imin),
    #-     StdDev (isec)
    #-         from intrval;
    #- 	from intrval;
    # expect 1 row with the following values:
    # 	PStDevIyr	37.0550238462178
    # 	PStDevImon	35.3944547044126
    # 	PStDevIdy	36.5305473053251
    # 	PStDevIhr	32.2739726014512
    # 	PStDevImin	38.3848423454318
    # 	PStDevIsec	39.478674772247
    #
    #-------- eof ----------
    
    _testmgr.testcase_end(desc)

