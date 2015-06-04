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

#-------------------------
# testunit ddl04
# data in /g_data/sqldopt
#-------------------------

#------------------------------------
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    

def test001(desc="""showddl negative tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # n01.1 showddl on non-existing table <tablename>
    
    stmt = """showddl nonexistingtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    # n01.2 showddl on non-existing table, where index with same name exists
    
    stmt = """create table n1a12 ( a int , b int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index ixn1a12 on n1a12 (a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl ixn1a12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
 
    # n01.3 showddl on non-existing table <catalog>.<schema>.<tablename>
    
    stmt = """showddl """ + defs.my_schema + """.nonexistingtable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    stmt = """showddl \NSK.$DB0014.ZSDVGH8J.DNJ8J200;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
   
    _testmgr.testcase_end(desc)
