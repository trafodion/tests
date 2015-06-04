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
    
def test001(desc="""test026"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test026
    # JClear
    # 1999-06-03
    # CJDate tests (5th ed. p174): Join subquery with IN & NOT IN.
    # Exercise 6.21
    # "Get project names for projects supplied by supplier S1."
    #  added "not supplied" too
    #
    stmt = """select jname
from j 
where jnum in
(select jnum
from spj 
where snum = 's1')
order by jname;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test026.exp""", 's1')
    # expect 2 ordered rows with values 'console' and 'sorter'
    
    stmt = """select jname
from j 
where jnum not in
(select jnum
from spj 
where snum = 's1')
order by jname;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test026.exp""", 's2')
    # expect 5 ordered rows with the following values:
    #      collator
    #      punch
    #      reader
    #      tape
    #      terminal
    
    #- select jname
    #-   from vpj
    #-     where jnum in
    #-       (select jnum
    #-          from vpspj
    #- 	   where snum = 's1')
    #- 	     order by jname;
    # expect 2 ordered rows with values 'console' and 'sorter'
    
    #- select jname
    #-   from vpj
    #-     where jnum not in
    #-       (select jnum
    #-          from vpspj
    #- 	   where snum = 's1')
    #- 	     order by jname;
    # expect 5 ordered rows with the following values:
    #      collator
    #      punch
    #      reader
    #      tape
    #      terminal
    
    stmt = """select jname
from hpj 
where jnum in
(select jnum
from hpspj 
where snum = 's1')
order by jname;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test026.exp""", 's3')
    # expect 2 ordered rows with values 'console' and 'sorter'
    
    stmt = """select jname
from hpj 
where jnum not in
(select jnum
from hpspj 
where snum = 's1')
order by jname;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test026.exp""", 's4')
    # expect 5 ordered rows with the following values:
    #      collator
    #      punch
    #      reader
    #      tape
    #      terminal
    
    _testmgr.testcase_end(desc)

