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
    
def test001(desc="""test060"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test060
    # jclear
    # 1997-11-03
    # Transpose tests: CREATE VIEW version of test059
    #
    #-------- date test  ----------
    
    stmt = """create view vw060date (num, b, c, d, keycol, iv, countstar) as
select num, b, c, d, keycol, iv, count (*)
from dtxtab 
transpose b, c, d as iv
key by keycol
group by num, b, c, d, keycol, iv;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vw060date 
order by num, keycol, iv;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 75)
    
    #-------- time test  ----------
    stmt = """create view vw060time (num, b, c, d, keycol, iv, countstar) as
select num, b, c, d, keycol, iv, count (*)
from tmxtab 
transpose b, c, d as iv
key by keycol
group by num, b, c, d, keycol, iv;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vw060time 
order by num, keycol, iv;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test060.exp""", 's2')
    
    #-------- eof ----------
    
    _testmgr.testcase_end(desc)

