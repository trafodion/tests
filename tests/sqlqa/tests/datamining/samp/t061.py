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
    
def test001(desc="""test061"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test061
    # DDunn
    # 1999-01-18
    # Testing periodic sampling.
    # Testing to make sure that an error is returned when PERIODIC sample
    # size and the sample size is somthing other than number of rows.
    # It is currently a rule that the sample size must be specified
    # in rows rather than percent.
    #
    #an error should be returned
    stmt = """select empid, salary
from samptb051 
sample periodic 10 percent every 12 rows;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4113')
    
    #an error should be returned
    stmt = """select empid, salary
from samptb051 
sample periodic 10 percent every 12 percent;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4113')
    
    #an error should be returned
    stmt = """select empid, salary
from samptb051 
sample periodic 10 rows every 12 percent;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4113')
    
    _testmgr.testcase_end(desc)

