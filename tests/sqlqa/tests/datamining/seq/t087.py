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
    
def test001(desc="""test087"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test087
    # JClear
    # 1999-01-20
    # sequence functions: inner join : running functions
    #        runningcount
    #        runningsum
    #        runningmax
    #        runningmin
    #        runningavg
    #        runningvariance
    #        runningstddev
    #
    # check the data first
    stmt = """select seqtb81t1.id, pay, doa
from seqtb81t1 inner join seqtb81t2 
on seqtb81t1.id = seqtb81t2.id
order by id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test087.exp""", 's1')
    # expect 50 rows
    
    # count, sum, max, min, avg
    stmt = """select seqtb81t1.id, doa,
cast (pay as smallint) as pay,
cast (runningcount (pay) as smallint) as rcount,
cast (runningsum (pay) as int) as rsum,
cast (runningmax (pay) as smallint) as rmax,
cast (runningmin (pay) as smallint) as rmin,
cast (runningavg (pay) as smallint) as ravg
from seqtb81t1 inner join seqtb81t2 
on seqtb81t1.id = seqtb81t2.id
sample first 20 rows
sort by seqtb81t1.id
sequence by seqtb81t1.id
order by seqtb81t1.id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test087.exp""", 's2')
    # expect 20 rows
    
    # avg, variance, stddev
    stmt = """select seqtb81t1.id, doa,
cast (pay as smallint) as pay,
cast (runningavg (pay) as dec (15,3)) as ravg,
cast (runningvariance (pay) as dec (15,3)) as rvariance,
cast (runningstddev (pay) as dec (15,3)) as rstddev
from seqtb81t1 inner join seqtb81t2 
on seqtb81t1.id = seqtb81t2.id
sample first 20 rows
sort by seqtb81t1.id
sequence by seqtb81t1.id
order by seqtb81t1.id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test087.exp""", 's3')
    # expect 20 rows
    
    _testmgr.testcase_end(desc)

