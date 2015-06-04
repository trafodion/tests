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
    
def test001(desc="""test076"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test076
    # DDunn
    # 1999-01-18
    # Test balance with periodic sampling & balance
    #
    # check the data first
    stmt = """select gender, name, salary
from samptb075 
order by name;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test076.exp""", 's1')
    # expect 14 rows with the following data in order
    #      F       Abbie                       90000
    #      M       Chris                        2000
    #      M       David                      300000
    #      F       Debbie                     500000
    #      F       Donna                      100000
    #      F       Ellie                      100000
    #      F       Elory                        2000
    #      F       Hema                       100000
    #      F       Iris                       100000
    #      F       Jane                        70000
    #      M       Larry                       80000
    #      F       Melody                      90000
    #      F       Nikki                       60000
    #      F       Sydney                     500000
    
    stmt = """select gender, name, salary
from samptb075 
sample periodic
balance when gender = 'F' THEN 2 rows
when gender = 'M' THEN 1 rows
end
every 3 rows
sort by name
order by name;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test076.exp""", 's2')
    # expect 9 rows with the following names in order
    #      Abbie
    #      Chris
    #      Debbie
    #      Ellie
    #      Elory
    #      Iris
    #      Jane
    #      Nikki
    #      Sydney
    
    _testmgr.testcase_end(desc)

