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
    
def test001(desc="""test003"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test003
    # JClear
    # 1999-06-01
    # CJDate tests (5th ed. p148): simple queries
    #--------------------------------------------
    #
    stmt = """select * from s 
order by snum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test003.exp""", 's1')
    # expect 5 rows with the following values in order:
    #    s1, Smith, 20, London
    #    s2, Jones, 10, Paris
    #    s3, Blake, 30, Paris
    #    s4, Clark, 20, London
    #    s5, Adams, 30, Athens
    
    stmt = """select s.* from s 
order by snum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test003.exp""", 's2')
    # expect the same 5 rows
    
    #- select * from vps
    #-   order by snum;
    # expect 5 rows with the following values in order:
    #    s1, Smith, 20, London
    #    s2, Jones, 10, Paris
    #    s3, Blake, 30, Paris
    #    s4, Clark, 20, London
    #    s5, Adams, 30, Athens
    
    #- select vps.* from vps
    #-   order by snum;
    # expect the same 5 rows
    
    stmt = """select * from hps 
order by snum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test003.exp""", 's3')
    # expect 5 rows with the following values in order:
    #    s1, Smith, 20, London
    #    s2, Jones, 10, Paris
    #    s3, Blake, 30, Paris
    #    s4, Clark, 20, London
    #    s5, Adams, 30, Athens
    
    stmt = """select hps.* from hps 
order by snum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test003.exp""", 's4')
    # expect the same 5 rows
    
    _testmgr.testcase_end(desc)

