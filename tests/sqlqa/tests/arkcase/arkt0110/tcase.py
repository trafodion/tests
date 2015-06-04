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
import qa03s2
import qn03s0

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
    
def test001(desc="""a01"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0110 : A01
    #  Description:        This test verifies the SQL large number
    #                      of SELECTs in query (normalizer stores totals).
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    #
    #  ---------------------------------
    #  Create the Log file.
    #  ---------------------------------
    #  ---------------------------------
    #  Set up default catalog and schema
    #  ---------------------------------
    # set catalog eval;
    # set schema  eval.gdb;
    #
    #
    
    #  Large (10) number of selects in a query:
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
))))))))) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    
    #  Large (15) number of selects in a query:
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
))))) ))))))))) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    
    #  Large (16) number of selects in a query:
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
)))))) ))))))))) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    
    #  Large (17) number of selects in a query:
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
))))))) ))))))))) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    
    #  Large (20) number of selects in a query:
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
)))))))))) ))))))))) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    
    #  Large (21) number of selects in a query:
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
) )))))))))) ))))))))) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    
    #  Large (25) number of selects in a query:
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
))))) )))))))))) ))))))))) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')
    
    #  Large (26) number of selects in a query:
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
)))))) )))))))))) ))))))))) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s7')
    
    #  Large (27) number of selects in a query:
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
))))))) )))))))))) ))))))))) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s8')
    
    #  Large (28) number of selects in a query:
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
)))))))) )))))))))) ))))))))) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s9')
    
    #  Large (29) number of selects in a query:
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
))))))))) )))))))))) ))))))))) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s10')
    
    #  Large (30) number of selects in a query:
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
)))))))))) )))))))))) ))))))))) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s11')
    
    #  Large (40) number of selects in a query:
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
)))))))))) )))))))))) )))))))))) ))))))))) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s12')
    
    #  Large (100) number of selects in a query:
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
)))))))))) ))))))))))
)))))))))) )))))))))) )))))))))) ))))))))))
)))))))))) )))))))))) )))))))))) ))))))))) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s13')
    
    #  Large (15) number of select levels in a query,
    #  plus large (30) total number of selects in a query:
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from
 """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from
 """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from
 """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from
 """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from
 """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from
 """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from
 """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from
 """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from
 """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
))))) )))))))))
and ( pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from
 """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from
 """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from
 """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
where pic_x_1 in (select pic_x_1 from """ + gvars.g_schema_arkcasedb + """.btsel02 
))))) ))))))))))
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s14')
    
    _testmgr.testcase_end(desc)

def test002(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0110 : A02
    #  Description:        This test verifies the SQL large number
    #                      of TABLEs in parse tree referenced by views
    #                      (normalizer stores totals).
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.svsel19 a
, """ + gvars.g_schema_arkcasedb + """.svsel19 b
where a.data_x3 = b.data_x3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.svsel19 a
, """ + gvars.g_schema_arkcasedb + """.svsel19 b
, """ + gvars.g_schema_arkcasedb + """.svsel19 c
, """ + gvars.g_schema_arkcasedb + """.svsel19 d
where a.data_x3 = b.data_x3
and ( a.data_x3 = c.data_x3 )
and ( a.data_x3 = d.data_x3 )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.svsel19 a
, """ + gvars.g_schema_arkcasedb + """.svsel19 b
, """ + gvars.g_schema_arkcasedb + """.svsel19 c
, """ + gvars.g_schema_arkcasedb + """.svsel19 d
, """ + gvars.g_schema_arkcasedb + """.svsel19 e
, """ + gvars.g_schema_arkcasedb + """.svsel19 f
, """ + gvars.g_schema_arkcasedb + """.svsel19 g
, """ + gvars.g_schema_arkcasedb + """.svsel19 h
, """ + gvars.g_schema_arkcasedb + """.svsel19 i
, """ + gvars.g_schema_arkcasedb + """.svsel19 j
where a.data_x3 = b.data_x3
and ( a.data_x3 = c.data_x3 )
and ( a.data_x3 = d.data_x3 )
and ( a.data_x3 = e.data_x3 )
and ( a.data_x3 = f.data_x3 )
and ( a.data_x3 = g.data_x3 )
and ( a.data_x3 = h.data_x3 )
and ( a.data_x3 = i.data_x3 )
and ( a.data_x3 = j.data_x3 )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    
    stmt = """select count(*) from (
select * from """ + gvars.g_schema_arkcasedb + """.svsel19 a
, """ + gvars.g_schema_arkcasedb + """.svsel19 b
, """ + gvars.g_schema_arkcasedb + """.svsel19 c
, """ + gvars.g_schema_arkcasedb + """.svsel19 d
, """ + gvars.g_schema_arkcasedb + """.svsel19 e
, """ + gvars.g_schema_arkcasedb + """.svsel19 f
, """ + gvars.g_schema_arkcasedb + """.svsel19 g
, """ + gvars.g_schema_arkcasedb + """.svsel19 h
, """ + gvars.g_schema_arkcasedb + """.svsel19 i
, """ + gvars.g_schema_arkcasedb + """.svsel19 j
, """ + gvars.g_schema_arkcasedb + """.svsel19 k
, """ + gvars.g_schema_arkcasedb + """.svsel19 l
, """ + gvars.g_schema_arkcasedb + """.svsel19 m
, """ + gvars.g_schema_arkcasedb + """.svsel19 n
, """ + gvars.g_schema_arkcasedb + """.svsel19 o
, """ + gvars.g_schema_arkcasedb + """.svsel19 p
, """ + gvars.g_schema_arkcasedb + """.svsel19 q
, """ + gvars.g_schema_arkcasedb + """.svsel19 r
, """ + gvars.g_schema_arkcasedb + """.svsel19 s
, """ + gvars.g_schema_arkcasedb + """.svsel19 t
where a.data_x3 = b.data_x3
and ( a.data_x3 = c.data_x3 )
and ( a.data_x3 = d.data_x3 )
and ( a.data_x3 = e.data_x3 )
and ( a.data_x3 = f.data_x3 )
and ( a.data_x3 = g.data_x3 )
and ( a.data_x3 = h.data_x3 )
and ( a.data_x3 = i.data_x3 )
and ( a.data_x3 = j.data_x3 )
and ( a.data_x3 = k.data_x3 )
and ( a.data_x3 = l.data_x3 )
and ( a.data_x3 = m.data_x3 )
and ( a.data_x3 = n.data_x3 )
and ( a.data_x3 = o.data_x3 )
and ( a.data_x3 = p.data_x3 )
and ( a.data_x3 = q.data_x3 )
and ( a.data_x3 = r.data_x3 )
and ( a.data_x3 = s.data_x3 )
and ( a.data_x3 = t.data_x3 ))t
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')

    _testmgr.testcase_end(desc)

def test003(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0110 : A03
    #  Description:        This test verifies the SQL Large number
    #                      of PREDICATEs in parse tree
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    #  The following list has 221 items
    stmt = """SELECT * FROM """ + gvars.g_schema_arkcasedb + """.parts WHERE partname in (
'a','b','c','d','e','f','g'
,'h','i','j','k','l','m'
,'n','o','p','q','r','s','t'
,'a1','b1','c1','d1','e1','f1','g1'
,'h1','i1','j1','k1','l1','m1'
,'n1','o1','p1','q1','r1','s1','t1'
,'a2','b2','c2','d2','e2','f2','g2'
,'h2','i2','j2','k2','l2','m2'
,'n2','o2','p2','q2','r2','s2','t2'
,'a3','b3','c3','d3','e3','f3','g3'
,'h3','i3','j3','k3','l3','m3'
,'n3','o3','p3','q3','r3','s3','t3'
,'a4','b4','c4','d4','e4','f4','g4'
,'h4','i4','j4','k4','l4','m4'
,'n4','o4','p4','q4','r4','s4','t4'
,'a5','b5','c5','d5','e5','f5','g5'
,'h5','i5','j5','k5','l5','m5'
,'n5','o5','p5','q5','r5','s5','t5'
,'a6','b6','c6','d6','e6','f6','g6'
,'h6','i6','j6','k6','l6','m6'
,'n6','o6','p6','q6','r6','s6','t6'
,'a7','b7','c7','d7','e7','f7','g7'
,'h7','i7','j7','k7','l7','m7'
,'n7','o7','p7','q7','r7','s7','t7'
,'a8','b8','c8','d8','e8','f8','g8'
,'h8','i8','j8','k8','l8','m8'
,'n8','o8','p8','q8','r8','s8','t8'
,'a9','b9','c9','d9','e9','f9','g9'
,'h9','i9','j9','k9','l9','m9'
,'n9','o9','p9','q9','r9','s9','t9'
,'a0','b0','c0','d0','e0','f0','g0'
,'h0','i0','j0','k0','l0','m0'
,'n0','o0','p0','q0','r0','s0','t0'
,'DECIMAL ARITH'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s0')
    
    #  The following list has 1301 items
    stmt = """SELECT * FROM """ + gvars.g_schema_arkcasedb + """.parts WHERE partname in (
'a','b','c','d','e','f','g'
,'h','i','j','k','l','m'
,'n','o','p','q','r','s','t'
,'a1','b1','c1','d1','e1','f1','g1'
,'h1','i1','j1','k1','l1','m1'
,'n1','o1','p1','q1','r1','s1','t1'
,'a2','b2','c2','d2','e2','f2','g2'
,'h2','i2','j2','k2','l2','m2'
,'n2','o2','p2','q2','r2','s2','t2'
,'a3','b3','c3','d3','e3','f3','g3'
,'h3','i3','j3','k3','l3','m3'
,'n3','o3','p3','q3','r3','s3','t3'
,'a4','b4','c4','d4','e4','f4','g4'
,'h4','i4','j4','k4','l4','m4'
,'n4','o4','p4','q4','r4','s4','t4'
,'a5','b5','c5','d5','e5','f5','g5'
,'h5','i5','j5','k5','l5','m5'
,'n5','o5','p5','q5','r5','s5','t5'
,'a6','b6','c6','d6','e6','f6','g6'
,'h6','i6','j6','k6','l6','m6'
,'n6','o6','p6','q6','r6','s6','t6'
,'a7','b7','c7','d7','e7','f7','g7'
,'h7','i7','j7','k7','l7','m7'
,'n7','o7','p7','q7','r7','s7','t7'
,'a8','b8','c8','d8','e8','f8','g8'
,'h8','i8','j8','k8','l8','m8'
,'n8','o8','p8','q8','r8','s8','t8'
,'a9','b9','c9','d9','e9','f9','g9'
,'h9','i9','j9','k9','l9','m9'
,'n9','o9','p9','q9','r9','s9','t9'
,'a0','b0','c0','d0','e0','f0','g0'
,'h0','i0','j0','k0','l0','m0'
,'n0','o0','p0','q0','r0','s0','t0'
,'aa','ba','ca','da','ea','fa','ga'
,'ha','ia','ja','ka','la','ma'
,'na','oa','pa','qa','ra','sa','ta'
,'ab','bb','cb','db','eb','fb','gb'
,'hb','ib','jb','kb','lb','mb'
,'nb','ob','pb','qb','rb','sb','tb'
,'ac','cc','cc','dc','ec','fc','gc'
,'hc','ic','jc','kc','lc','mc'
,'nc','oc','pc','qc','rc','sc','tc'
,'ad','bd','cd','dd','ed','fd','gd'
,'hd','id','jd','kd','ld','md'
,'nd','od','pd','qd','rd','sd','td'
,'ae','be','ce','de','ee','fe','ge'
,'he','ie','je','ke','le','me'
,'ne','oe','pe','qe','re','se','te'
,'af','bf','cf','df','ef','ff','gf'
,'hf','if','jf','kf','lf','mf'
,'nf','of','pf','qf','rf','sf','tf'
,'a1','b1','c1','d1','e1','f1','g1'
,'h1','i1','j1','k1','l1','m1'
,'n1','o1','p1','q1','r1','s1','t1'
,'a2','b2','c2','d2','e2','f2','g2'
,'h2','i2','j2','k2','l2','m2'
,'n2','o2','p2','q2','r2','s2','t2'
,'a3','b3','c3','d3','e3','f3','g3'
,'h3','i3','j3','k3','l3','m3'
,'n3','o3','p3','q3','r3','s3','t3'
,'a4','b4','c4','d4','e4','f4','g4'
,'h4','i4','j4','k4','l4','m4'
,'n4','o4','p4','q4','r4','s4','t4'
,'a5','b5','c5','d5','e5','f5','g5'
,'h5','i5','j5','k5','l5','m5'
,'n5','o5','p5','q5','r5','s5','t5'
,'a6','b6','c6','d6','e6','f6','g6'
,'h6','i6','j6','k6','l6','m6'
,'n6','o6','p6','q6','r6','s6','t6'
,'a7','b7','c7','d7','e7','f7','g7'
,'h7','i7','j7','k7','l7','m7'
,'n7','o7','p7','q7','r7','s7','t7'
,'a8','b8','c8','d8','e8','f8','g8'
,'h8','i8','j8','k8','l8','m8'
,'n8','o8','p8','q8','r8','s8','t8'
,'a9','b9','c9','d9','e9','f9','g9'
,'h9','i9','j9','k9','l9','m9'
,'n9','o9','p9','q9','r9','s9','t9'
,'a0','b0','c0','d0','e0','f0','g0'
,'h0','i0','j0','k0','l0','m0'
,'n0','o0','p0','q0','r0','s0','t0'
,'aa','ba','ca','da','ea','fa','ga'
,'ha','ia','ja','ka','la','ma'
,'na','oa','pa','qa','ra','sa','ta'
,'ab','bb','cb','db','eb','fb','gb'
,'hb','ib','jb','kb','lb','mb'
,'nb','ob','pb','qb','rb','sb','tb'
,'ac','cc','cc','dc','ec','fc','gc'
,'hc','ic','jc','kc','lc','mc'
,'nc','oc','pc','qc','rc','sc','tc'
,'ad','bd','cd','dd','ed','fd','gd'
,'hd','id','jd','kd','ld','md'
,'nd','od','pd','qd','rd','sd','td'
,'ae','be','ce','de','ee','fe','ge'
,'he','ie','je','ke','le','me'
,'ne','oe','pe','qe','re','se','te'
,'af','bf','cf','df','ef','ff','gf'
,'hf','if','jf','kf','lf','mf'
,'nf','of','pf','qf','rf','sf','tf'
,'1a1','1b1','1c1','1d1','1e1','1f1','1g1'
,'1h1','1i1','1j1','1k1','1l1','1m1'
,'1n1','1o1','1p1','1q1','1r1','1s1','1t1'
,'1a2','1b2','1c2','1d2','1e2','1f2','1g2'
,'1h2','1i2','1j2','1k2','1l2','1m2'
,'1n2','1o2','1p2','1q2','1r2','1s2','1t2'
,'1a3','1b3','1c3','1d3','1e3','1f3','1g3'
,'1h3','1i3','1j3','1k3','1l3','1m3'
,'1n3','1o3','1p3','1q3','1r3','1s3','1t3'
,'1a4','1b4','1c4','1d4','1e4','1f4','1g4'
,'1h4','1i4','1j4','1k4','1l4','1m4'
,'1n4','1o4','1p4','1q4','1r4','1s4','1t4'
,'1a5','1b5','1c5','1d5','1e5','1f5','1g5'
,'1h5','1i5','1j5','1k5','1l5','1m5'
,'1n5','1o5','1p5','1q5','1r5','1s5','1t5'
,'1a6','1b6','1c6','1d6','1e6','1f6','1g6'
,'1h6','1i6','1j6','1k6','1l6','1m6'
,'1n6','1o6','1p6','1q6','1r6','1s6','1t6'
,'1a7','1b7','1c7','1d7','1e7','1f7','1g7'
,'1h7','1i7','1j7','1k7','1l7','1m7'
,'1n7','1o7','1p7','1q7','1r7','1s7','1t7'
,'1a8','1b8','1c8','1d8','1e8','1f8','1g8'
,'1h8','1i8','1j8','1k8','1l8','1m8'
,'1n8','1o8','1p8','1q8','1r8','1s8','1t8'
,'1a9','1b9','1c9','1d9','1e9','1f9','1g9'
,'1h9','1i9','1j9','1k9','1l9','1m9'
,'1n9','1o9','1p9','1q9','1r9','1s9','1t9'
,'1a0','1b0','1c0','1d0','1e0','1f0','1g0'
,'1h0','1i0','1j0','1k0','1l0','1m0'
,'1n0','1o0','1p0','1q0','1r0','1s0','1t0'
,'1aa','1ba','1ca','1da','1ea','1fa','1ga'
,'1ha','1ia','1ja','1ka','1la','1ma'
,'1na','1oa','1pa','1qa','1ra','1sa','1ta'
,'1ab','1bb','1cb','1db','1eb','1fb','1gb'
,'1hb','1ib','1jb','1kb','1lb','1mb'
,'1nb','1ob','1pb','1qb','1rb','1sb','1tb'
,'1ac','1cc','1cc','1dc','1ec','1fc','1gc'
,'1hc','1ic','1jc','1kc','1lc','1mc'
,'1nc','1oc','1pc','1qc','1rc','1sc','1tc'
,'1ad','1bd','1cd','1dd','1ed','1fd','1gd'
,'1hd','1id','1jd','1kd','1ld','1md'
,'1nd','1od','1pd','1qd','1rd','1sd','1td'
,'1ae','1be','1ce','1de','1ee','1fe','1ge'
,'1he','1ie','1je','1ke','1le','1me'
,'1ne','1oe','1pe','1qe','1re','1se','1te'
,'1af','1bf','1cf','1df','1ef','1ff','1gf'
,'1hf','1if','1jf','1kf','1lf','1mf'
,'1nf','1of','1pf','1qf','1rf','1sf','1tf'
,'2a1','2b1','2c1','2d1','2e1','2f1','2g1'
,'2h1','2i1','2j1','2k1','2l1','2m1'
,'2n1','2o1','2p1','2q1','2r1','2s1','2t1'
,'2a2','2b2','2c2','2d2','2e2','2f2','2g2'
,'2h2','2i2','2j2','2k2','2l2','2m2'
,'2n2','2o2','2p2','2q2','2r2','2s2','2t2'
,'2a3','2b3','2c3','2d3','2e3','2f3','2g3'
,'2h3','2i3','2j3','2k3','2l3','2m3'
,'2n3','2o3','2p3','2q3','2r3','2s3','2t3'
,'2a4','2b4','2c4','2d4','2e4','2f4','2g4'
,'2h4','2i4','2j4','2k4','2l4','2m4'
,'2n4','2o4','2p4','2q4','2r4','2s4','2t4'
,'2a5','2b5','2c5','2d5','2e5','2f5','2g5'
,'2h5','2i5','2j5','2k5','2l5','2m5'
,'2n5','2o5','2p5','2q5','2r5','2s5','2t5'
,'2a6','2b6','2c6','2d6','2e6','2f6','2g6'
,'2h6','2i6','2j6','2k6','2l6','2m6'
,'2n6','2o6','2p6','2q6','2r6','2s6','2t6'
,'2a7','2b7','2c7','2d7','2e7','2f7','2g7'
,'2h7','2i7','2j7','2k7','2l7','2m7'
,'2n7','2o7','2p7','2q7','2r7','2s7','2t7'
,'2a8','2b8','2c8','2d8','2e8','2f8','2g8'
,'2h8','2i8','2j8','2k8','2l8','2m8'
,'2n8','2o8','2p8','2q8','2r8','2s8','2t8'
,'2a9','2b9','2c9','2d9','2e9','2f9','2g9'
,'2h9','2i9','2j9','2k9','2l9','2m9'
,'2n9','2o9','2p9','2q9','2r9','2s9','2t9'
,'2a0','2b0','2c0','2d0','2e0','2f0','2g0'
,'2h0','2i0','2j0','2k0','2l0','2m0'
,'2n0','2o0','2p0','2q0','2r0','2s0','2t0'
,'2aa','2ba','2ca','2da','2ea','2fa','2ga'
,'2ha','2ia','2ja','2ka','2la','2ma'
,'2na','2oa','2pa','2qa','2ra','2sa','2ta'
,'2ab','2bb','2cb','2db','2eb','2fb','2gb'
,'2hb','2ib','2jb','2kb','2lb','2mb'
,'2nb','2ob','2pb','2qb','2rb','2sb','2tb'
,'2ac','2cc','2cc','2dc','2ec','2fc','2gc'
,'2hc','2ic','2jc','2kc','2lc','2mc'
,'2nc','2oc','2pc','2qc','2rc','2sc','2tc'
,'2ad','2bd','2cd','2dd','2ed','2fd','2gd'
,'2hd','2id','2jd','2kd','2ld','2md'
,'2nd','2od','2pd','2qd','2rd','2sd','2td'
,'2ae','2be','2ce','2de','2ee','2fe','2ge'
,'2he','2ie','2je','2ke','2le','2me'
,'2ne','2oe','2pe','2qe','2re','2se','2te'
,'2af','2bf','2cf','2df','2ef','2ff','2gf'
,'2hf','2if','2jf','2kf','2lf','2mf'
,'2nf','2of','2pf','2qf','2rf','2sf','2tf'
,'DECIMAL ARITH'
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    
    qa03s2._init(_testmgr, _testlist)
    
    #    SELECT * FROM parts WHERE partname in (
    # 'a','b','c','d','e','f','g'
    #,'h','i','j','k','l','m'
    #,'n','o','p','q','r','s','t'
    #,'a1','b1','c1','d1','e1','f1','g1'
    #,'h1','i1','j1','k1','l1','m1'
    #,'n1','o1','p1','q1','r1','s1','t1'
    #,'a2','b2','c2','d2','e2','f2','g2'
    #,'h2','i2','j2','k2','l2','m2'
    #,'n2','o2','p2','q2','r2','s2','t2'
    #,'a3','b3','c3','d3','e3','f3','g3'
    #,'h3','i3','j3','k3','l3','m3'
    #,'n3','o3','p3','q3','r3','s3','t3'
    #,'a4','b4','c4','d4','e4','f4','g4'
    #,'h4','i4','j4','k4','l4','m4'
    #,'n4','o4','p4','q4','r4','s4','t4'
    #,'a5','b5','c5','d5','e5','f5','g5'
    #,'h5','i5','j5','k5','l5','m5'
    #,'n5','o5','p5','q5','r5','s5','t5'
    #,'a6','b6','c6','d6','e6','f6','g6'
    #,'h6','i6','j6','k6','l6','m6'
    #,'n6','o6','p6','q6','r6','s6','t6'
    #,'a7','b7','c7','d7','e7','f7','g7'
    #,'h7','i7','j7','k7','l7','m7'
    #,'n7','o7','p7','q7','r7','s7','t7'
    #,'a8','b8','c8','d8','e8','f8','g8'
    #,'h8','i8','j8','k8','l8','m8'
    #,'n8','o8','p8','q8','r8','s8','t8'
    #,'a9','b9','c9','d9','e9','f9','g9'
    #,'h9','i9','j9','k9','l9','m9'
    #,'n9','o9','p9','q9','r9','s9','t9'
    #,'a0','b0','c0','d0','e0','f0','g0'
    #,'h0','i0','j0','k0','l0','m0'
    #,'n0','o0','p0','q0','r0','s0','t0'
    #,'aa','ba','ca','da','ea','fa','ga'
    #,'ha','ia','ja','ka','la','ma'
    #,'na','oa','pa','qa','ra','sa','ta'
    #,'ab','bb','cb','db','eb','fb','gb'
    #,'hb','ib','jb','kb','lb','mb'
    #,'nb','ob','pb','qb','rb','sb','tb'
    #,'ac','cc','cc','dc','ec','fc','gc'
    #,'hc','ic','jc','kc','lc','mc'
    #,'nc','oc','pc','qc','rc','sc','tc'
    #,'ad','bd','cd','dd','ed','fd','gd'
    #,'hd','id','jd','kd','ld','md'
    #,'nd','od','pd','qd','rd','sd','td'
    #,'ae','be','ce','de','ee','fe','ge'
    #,'he','ie','je','ke','le','me'
    #,'ne','oe','pe','qe','re','se','te'
    #,'af','bf','cf','df','ef','ff','gf'
    #,'hf','if','jf','kf','lf','mf'
    #,'nf','of','pf','qf','rf','sf','tf'
    #,'a1','b1','c1','d1','e1','f1','g1'
    #,'h1','i1','j1','k1','l1','m1'
    #,'n1','o1','p1','q1','r1','s1','t1'
    #,'a2','b2','c2','d2','e2','f2','g2'
    #,'h2','i2','j2','k2','l2','m2'
    #,'n2','o2','p2','q2','r2','s2','t2'
    #,'a3','b3','c3','d3','e3','f3','g3'
    #,'h3','i3','j3','k3','l3','m3'
    #,'n3','o3','p3','q3','r3','s3','t3'
    #,'a4','b4','c4','d4','e4','f4','g4'
    #,'h4','i4','j4','k4','l4','m4'
    #,'n4','o4','p4','q4','r4','s4','t4'
    #,'a5','b5','c5','d5','e5','f5','g5'
    #,'h5','i5','j5','k5','l5','m5'
    #,'n5','o5','p5','q5','r5','s5','t5'
    #,'a6','b6','c6','d6','e6','f6','g6'
    #,'h6','i6','j6','k6','l6','m6'
    #,'n6','o6','p6','q6','r6','s6','t6'
    #,'a7','b7','c7','d7','e7','f7','g7'
    #,'h7','i7','j7','k7','l7','m7'
    #,'n7','o7','p7','q7','r7','s7','t7'
    #,'a8','b8','c8','d8','e8','f8','g8'
    #,'h8','i8','j8','k8','l8','m8'
    #,'n8','o8','p8','q8','r8','s8','t8'
    #,'a9','b9','c9','d9','e9','f9','g9'
    #,'h9','i9','j9','k9','l9','m9'
    #,'n9','o9','p9','q9','r9','s9','t9'
    #,'a0','b0','c0','d0','e0','f0','g0'
    #,'h0','i0','j0','k0','l0','m0'
    #,'n0','o0','p0','q0','r0','s0','t0'
    #,'aa','ba','ca','da','ea','fa','ga'
    #,'ha','ia','ja','ka','la','ma'
    #,'na','oa','pa','qa','ra','sa','ta'
    #,'ab','bb','cb','db','eb','fb','gb'
    #,'hb','ib','jb','kb','lb','mb'
    #,'nb','ob','pb','qb','rb','sb','tb'
    #,'ac','cc','cc','dc','ec','fc','gc'
    #,'hc','ic','jc','kc','lc','mc'
    #,'nc','oc','pc','qc','rc','sc','tc'
    #,'ad','bd','cd','dd','ed','fd','gd'
    #,'hd','id','jd','kd','ld','md'
    #,'nd','od','pd','qd','rd','sd','td'
    #,'ae','be','ce','de','ee','fe','ge'
    #,'he','ie','je','ke','le','me'
    #,'ne','oe','pe','qe','re','se','te'
    #,'af','bf','cf','df','ef','ff','gf'
    #,'hf','if','jf','kf','lf','mf'
    #,'nf','of','pf','qf','rf','sf','tf'
    #,'1a1','1b1','1c1','1d1','1e1','1f1','1g1'
    #,'1h1','1i1','1j1','1k1','1l1','1m1'
    #,'1n1','1o1','1p1','1q1','1r1','1s1','1t1'
    #,'1a2','1b2','1c2','1d2','1e2','1f2','1g2'
    #,'1h2','1i2','1j2','1k2','1l2','1m2'
    #,'1n2','1o2','1p2','1q2','1r2','1s2','1t2'
    #,'1a3','1b3','1c3','1d3','1e3','1f3','1g3'
    #,'1h3','1i3','1j3','1k3','1l3','1m3'
    #,'1n3','1o3','1p3','1q3','1r3','1s3','1t3'
    #,'1a4','1b4','1c4','1d4','1e4','1f4','1g4'
    #,'1h4','1i4','1j4','1k4','1l4','1m4'
    #,'1n4','1o4','1p4','1q4','1r4','1s4','1t4'
    #,'1a5','1b5','1c5','1d5','1e5','1f5','1g5'
    #,'1h5','1i5','1j5','1k5','1l5','1m5'
    #,'1n5','1o5','1p5','1q5','1r5','1s5','1t5'
    #,'1a6','1b6','1c6','1d6','1e6','1f6','1g6'
    #,'1h6','1i6','1j6','1k6','1l6','1m6'
    #,'1n6','1o6','1p6','1q6','1r6','1s6','1t6'
    #,'1a7','1b7','1c7','1d7','1e7','1f7','1g7'
    #,'1h7','1i7','1j7','1k7','1l7','1m7'
    #,'1n7','1o7','1p7','1q7','1r7','1s7','1t7'
    #,'1a8','1b8','1c8','1d8','1e8','1f8','1g8'
    #,'1h8','1i8','1j8','1k8','1l8','1m8'
    #,'1n8','1o8','1p8','1q8','1r8','1s8','1t8'
    #,'1a9','1b9','1c9','1d9','1e9','1f9','1g9'
    #,'1h9','1i9','1j9','1k9','1l9','1m9'
    #,'1n9','1o9','1p9','1q9','1r9','1s9','1t9'
    #,'1a0','1b0','1c0','1d0','1e0','1f0','1g0'
    #,'1h0','1i0','1j0','1k0','1l0','1m0'
    #,'1n0','1o0','1p0','1q0','1r0','1s0','1t0'
    #,'1aa','1ba','1ca','1da','1ea','1fa','1ga'
    #,'1ha','1ia','1ja','1ka','1la','1ma'
    #,'1na','1oa','1pa','1qa','1ra','1sa','1ta'
    #,'1ab','1bb','1cb','1db','1eb','1fb','1gb'
    #,'1hb','1ib','1jb','1kb','1lb','1mb'
    #,'1nb','1ob','1pb','1qb','1rb','1sb','1tb'
    #,'1ac','1cc','1cc','1dc','1ec','1fc','1gc'
    #,'1hc','1ic','1jc','1kc','1lc','1mc'
    #,'1nc','1oc','1pc','1qc','1rc','1sc','1tc'
    #,'1ad','1bd','1cd','1dd','1ed','1fd','1gd'
    #,'1hd','1id','1jd','1kd','1ld','1md'
    #,'1nd','1od','1pd','1qd','1rd','1sd','1td'
    #,'1ae','1be','1ce','1de','1ee','1fe','1ge'
    #,'1he','1ie','1je','1ke','1le','1me'
    #,'1ne','1oe','1pe','1qe','1re','1se','1te'
    #,'1af','1bf','1cf','1df','1ef','1ff','1gf'
    #,'1hf','1if','1jf','1kf','1lf','1mf'
    #,'1nf','1of','1pf','1qf','1rf','1sf','1tf'
    #,'2a1','2b1','2c1','2d1','2e1','2f1','2g1'
    #,'2h1','2i1','2j1','2k1','2l1','2m1'
    #,'2n1','2o1','2p1','2q1','2r1','2s1','2t1'
    #,'2a2','2b2','2c2','2d2','2e2','2f2','2g2'
    #,'2h2','2i2','2j2','2k2','2l2','2m2'
    #,'2n2','2o2','2p2','2q2','2r2','2s2','2t2'
    #,'2a3','2b3','2c3','2d3','2e3','2f3','2g3'
    #,'2h3','2i3','2j3','2k3','2l3','2m3'
    #,'2n3','2o3','2p3','2q3','2r3','2s3','2t3'
    #,'2a4','2b4','2c4','2d4','2e4','2f4','2g4'
    #,'2h4','2i4','2j4','2k4','2l4','2m4'
    #,'2n4','2o4','2p4','2q4','2r4','2s4','2t4'
    #,'2a5','2b5','2c5','2d5','2e5','2f5','2g5'
    #,'2h5','2i5','2j5','2k5','2l5','2m5'
    #,'2n5','2o5','2p5','2q5','2r5','2s5','2t5'
    #,'2a6','2b6','2c6','2d6','2e6','2f6','2g6'
    #,'2h6','2i6','2j6','2k6','2l6','2m6'
    #,'2n6','2o6','2p6','2q6','2r6','2s6','2t6'
    #,'2a7','2b7','2c7','2d7','2e7','2f7','2g7'
    #,'2h7','2i7','2j7','2k7','2l7','2m7'
    #,'2n7','2o7','2p7','2q7','2r7','2s7','2t7'
    #,'2a8','2b8','2c8','2d8','2e8','2f8','2g8'
    #,'2h8','2i8','2j8','2k8','2l8','2m8'
    #,'2n8','2o8','2p8','2q8','2r8','2s8','2t8'
    #,'2a9','2b9','2c9','2d9','2e9','2f9','2g9'
    #,'2h9','2i9','2j9','2k9','2l9','2m9'
    #,'2n9','2o9','2p9','2q9','2r9','2s9','2t9'
    #,'2a0','2b0','2c0','2d0','2e0','2f0','2g0'
    #,'2h0','2i0','2j0','2k0','2l0','2m0'
    #,'2n0','2o0','2p0','2q0','2r0','2s0','2t0'
    #,'2aa','2ba','2ca','2da','2ea','2fa','2ga'
    #,'2ha','2ia','2ja','2ka','2la','2ma'
    #,'2na','2oa','2pa','2qa','2ra','2sa','2ta'
    #,'2ab','2bb','2cb','2db','2eb','2fb','2gb'
    #,'2hb','2ib','2jb','2kb','2lb','2mb'
    #,'2nb','2ob','2pb','2qb','2rb','2sb','2tb'
    #,'2ac','2cc','2cc','2dc','2ec','2fc','2gc'
    #,'2hc','2ic','2jc','2kc','2lc','2mc'
    #,'2nc','2oc','2pc','2qc','2rc','2sc','2tc'
    #,'2ad','2bd','2cd','2dd','2ed','2fd','2gd'
    #,'2hd','2id','2jd','2kd','2ld','2md'
    #,'2nd','2od','2pd','2qd','2rd','2sd','2td'
    #,'2ae','2be','2ce','2de','2ee','2fe','2ge'
    #,'2he','2ie','2je','2ke','2le','2me'
    #,'2ne','2oe','2pe','2qe','2re','2se','2te'
    #,'2af','2bf','2cf','2df','2ef','2ff','2gf'
    #,'2hf','2if','2jf','2kf','2lf','2mf'
    #,'2nf','2of','2pf','2qf','2rf','2sf','2tf'
    #,'3a1','3b1','3c1','3d1','3e1','3f1','3g1'
    #,'3h1','3i1','3j1','3k1','3l1','3m1'
    #,'3n1','3o1','3p1','3q1','3r1','3s1','3t1'
    #,'3a2','3b2','3c2','3d2','3e2','3f2','3g2'
    #,'3h2','3i2','3j2','3k2','3l2','3m2'
    #,'3n2','3o2','3p2','3q2','3r2','3s2','3t2'
    #,'3a3','3b3','3c3','3d3','3e3','3f3','3g3'
    #,'3h3','3i3','3j3','3k3','3l3','3m3'
    #,'3n3','3o3','3p3','3q3','3r3','3s3','3t3'
    #,'3a4','3b4','3c4','3d4','3e4','3f4','3g4'
    #,'3h4','3i4','3j4','3k4','3l4','3m4'
    #,'3n4','3o4','3p4','3q4','3r4','3s4','3t4'
    #,'3a5','3b5','3c5','3d5','3e5','3f5','3g5'
    #,'3h5','3i5','3j5','3k5','3l5','3m5'
    #,'3n5','3o5','3p5','3q5','3r5','3s5','3t5'
    #,'3a6','3b6','3c6','3d6','3e6','3f6','3g6'
    #,'3h6','3i6','3j6','3k6','3l6','3m6'
    #,'3n6','3o6','3p6','3q6','3r6','3s6','3t6'
    #,'3a7','3b7','3c7','3d7','3e7','3f7','3g7'
    #,'3h7','3i7','3j7','3k7','3l7','3m7'
    #,'3n7','3o7','3p7','3q7','3r7','3s7','3t7'
    #,'3a8','3b8','3c8','3d8','3e8','3f8','3g8'
    #,'3h8','3i8','3j8','3k8','3l8','3m8'
    #,'3n8','3o8','3p8','3q8','3r8','3s8','3t8'
    #,'3a9','3b9','3c9','3d9','3e9','3f9','3g9'
    #,'3h9','3i9','3j9','3k9','3l9','3m9'
    #,'3n9','3o9','3p9','3q9','3r9','3s9','3t9'
    #,'3a0','3b0','3c0','3d0','3e0','3f0','3g0'
    #,'3h0','3i0','3j0','3k0','3l0','3m0'
    #,'3n0','3o0','3p0','3q0','3r0','3s0','3t0'
    #,'3aa','3ba','3ca','3da','3ea','3fa','3ga'
    #,'3ha','3ia','3ja','3ka','3la','3ma'
    #,'3na','3oa','3pa','3qa','3ra','3sa','3ta'
    #,'3ab','3bb','3cb','3db','3eb','3fb','3gb'
    #,'3hb','3ib','3jb','3kb','3lb','3mb'
    #,'3nb','3ob','3pb','3qb','3rb','3sb','3tb'
    #,'3ac','3cc','3cc','3dc','3ec','3fc','3gc'
    #,'3hc','3ic','3jc','3kc','3lc','3mc'
    #,'3nc','3oc','3pc','3qc','3rc','3sc','3tc'
    #,'3ad','3bd','3cd','3dd','3ed','3fd','3gd'
    #,'3hd','3id','3jd','3kd','3ld','3md'
    #,'3nd','3od','3pd','3qd','3rd','3sd','3td'
    #,'3ae','3be','3ce','3de','3ee','3fe','3ge'
    #,'3he','3ie','3je','3ke','3le','3me'
    #,'3ne','3oe','3pe','3qe','3re','3se','3te'
    #,'3af','3bf','3cf','3df','3ef','3ff','3gf'
    #,'3hf','3if','3jf','3kf','3lf','3mf'
    #,'3nf','3of','3pf','3qf','3rf','3sf','3tf'
    #,'POWER MODULE'
    #,'4a1','4b1','4c1','4d1','4e1','4f1','4g1'
    #,'4h1','4i1','4j1','4k1','4l1','4m1'
    #,'4n1','4o1','4p1','4q1','4r1','4s1','4t1'
    #,'4a2','4b2','4c2','4d2','4e2','4f2','4g2'
    #,'4h2','4i2','4j2','4k2','4l2','4m2'
    #,'4n2','4o2','4p2','4q2','4r2','4s2','4t2'
    #,'4a3','4b3','4c3','4d3','4e3','4f3','4g3'
    #,'4h3','4i3','4j3','4k3','4l3','4m3'
    #,'4n3','4o3','4p3','4q3','4r3','4s3','4t3'
    #,'4a4','4b4','4c4','4d4','4e4','4f4','4g4'
    #,'4h4','4i4','4j4','4k4','4l4','4m4'
    #,'4n4','4o4','4p4','4q4','4r4','4s4','4t4'
    #,'4a5','4b5','4c5','4d5','4e5','4f5','4g5'
    #,'4h5','4i5','4j5','4k5','4l5','4m5'
    #,'4n5','4o5','4p5','4q5','4r5','4s5','4t5'
    #,'4a6','4b6','4c6','4d6','4e6','4f6','4g6'
    #,'4h6','4i6','4j6','4k6','4l6','4m6'
    #,'4n6','4o6','4p6','4q6','4r6','4s6','4t6'
    #,'4a7','4b7','4c7','4d7','4e7','4f7','4g7'
    #,'4h7','4i7','4j7','4k7','4l7','4m7'
    #,'4n7','4o7','4p7','4q7','4r7','4s7','4t7'
    #,'4a8','4b8','4c8','4d8','4e8','4f8','4g8'
    #,'4h8','4i8','4j8','4k8','4l8','4m8'
    #,'4n8','4o8','4p8','4q8','4r8','4s8','4t8'
    #,'4a9','4b9','4c9','4d9','4e9','4f9','4g9'
    #,'4h9','4i9','4j9','4k9','4l9','4m9'
    #,'4n9','4o9','4p9','4q9','4r9','4s9','4t9'
    #,'4a0','4b0','4c0','4d0','4e0','4f0','4g0'
    #,'4h0','4i0','4j0','4k0','4l0','4m0'
    #,'4n0','4o0','4p0','4q0','4r0','4s0','4t0'
    #,'4aa','4ba','4ca','4da','4ea','4fa','4ga'
    #,'4ha','4ia','4ja','4ka','4la','4ma'
    #,'4na','4oa','4pa','4qa','4ra','4sa','4ta'
    #,'4ab','4bb','4cb','4db','4eb','4fb','4gb'
    #,'4hb','4ib','4jb','4kb','4lb','4mb'
    #,'4nb','4ob','4pb','4qb','4rb','4sb','4tb'
    #,'4ac','4cc','4cc','4dc','4ec','4fc','4gc'
    #,'4hc','4ic','4jc','4kc','4lc','4mc'
    #,'4nc','4oc','4pc','4qc','4rc','4sc','4tc'
    #,'4ad','4bd','4cd','4dd','4ed','4fd','4gd'
    #,'4hd','4id','4jd','4kd','4ld','4md'
    #,'4nd','4od','4pd','4qd','4rd','4sd','4td'
    #,'DECIMAL ARITH'
    #)
    #;
    
    _testmgr.testcase_end(desc)

def test004(desc="""a04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt110 : A04
    #  Description:        Large number of PREDICATEs involving more
    #                      than one table
    #  Test case inputs:   --
    #  Test case outputs:  --
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    #
    #  ---------------------------------
    #  Create the Log file.
    #  ---------------------------------
    #  ---------------------------------
    #  Set up default catalog and schema
    #  ---------------------------------
    # set catalog eval;
    # set schema  eval.gdb;
    #
    #
    
    #   Lots of PREDICATEs (16) involving more than one table.
    stmt = """SELECT a.char_1, b.char_10
FROM   """ + gvars.g_schema_arkcasedb + """.btsel01 a
, """ + gvars.g_schema_arkcasedb + """.btsel01 b
--  Join predicates:
WHERE a.char_1             = b.char_1
AND ( a.char_10            = b.char_10            )
AND ( a.pic_x_1            = b.pic_x_1            )
AND ( a.pic_x_7            = b.pic_x_7            )
AND ( a.pic_x_long         = b.pic_x_long         )
AND ( a.var_char           = b.var_char           )
AND ( a.binary_signed      = b.binary_signed      )
AND ( a.binary_32_u        = b.binary_32_u        )
AND ( a.binary_64_s        = b.binary_64_s        )
AND ( a.pic_comp_1         = b.pic_comp_1         )
AND ( a.pic_comp_2         = b.pic_comp_2         )
AND ( a.pic_comp_3         = b.pic_comp_3         )
AND ( a.small_int          = b.small_int          )
AND ( a.medium_int         = b.medium_int         )
AND ( a.large_int          = b.large_int          )
AND ( a.decimal_1          = b.decimal_1          )
AND ( a.decimal_2_signed   = b.decimal_2_signed   )
AND ( a.decimal_3_unsigned = b.decimal_3_unsigned )
AND ( a.pic_decimal_1      = b.pic_decimal_1      )
AND ( a.pic_decimal_2      = b.pic_decimal_2      )
AND ( a.pic_decimal_3      = b.pic_decimal_3      )
--  Add one local predicate:
AND ( a.pic_x_1            = 'Z' )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s0')
    
    stmt = """SELECT a.char_1, b.char_10, c.pic_x_7
FROM    """ + gvars.g_schema_arkcasedb + """.btsel01 a
, """ + gvars.g_schema_arkcasedb + """.btsel01 b
, """ + gvars.g_schema_arkcasedb + """.btsel01 c
--  Join predicates:
WHERE a.char_1             = b.char_1
AND ( a.char_10            = b.char_10            )
AND ( a.pic_x_1            = b.pic_x_1            )
AND ( a.pic_x_7            = b.pic_x_7            )
AND ( a.pic_x_long         = b.pic_x_long         )
AND ( a.var_char           = b.var_char           )
AND ( a.binary_signed      = b.binary_signed      )
AND ( a.binary_32_u        = b.binary_32_u        )
AND ( a.binary_64_s        = b.binary_64_s        )
AND ( a.pic_comp_1         = b.pic_comp_1         )
AND ( a.pic_comp_2         = b.pic_comp_2         )
AND ( a.pic_comp_3         = b.pic_comp_3         )
AND ( a.small_int          = b.small_int          )
AND ( a.medium_int         = b.medium_int         )
AND ( a.large_int          = b.large_int          )
AND ( a.decimal_1          = b.decimal_1          )
AND ( a.decimal_2_signed   = b.decimal_2_signed   )
AND ( a.decimal_3_unsigned = b.decimal_3_unsigned )
AND ( a.pic_decimal_1      = b.pic_decimal_1      )
AND ( a.pic_decimal_2      = b.pic_decimal_2      )
AND ( a.pic_decimal_3      = b.pic_decimal_3      )
--  Add one local predicate:
AND ( a.pic_x_1            = 'Z' )
AND ( c.char_1             = b.char_1             )
AND ( c.char_10            = b.char_10            )
AND ( c.pic_x_1            = b.pic_x_1            )
AND ( c.pic_x_7            = b.pic_x_7            )
AND ( c.pic_x_long         = b.pic_x_long         )
AND ( c.var_char           = b.var_char           )
AND ( c.binary_signed      = b.binary_signed      )
AND ( c.binary_32_u        = b.binary_32_u        )
AND ( c.binary_64_s        = b.binary_64_s        )
AND ( c.pic_comp_1         = b.pic_comp_1         )
AND ( c.pic_comp_2         = b.pic_comp_2         )
AND ( c.pic_comp_3         = b.pic_comp_3         )
AND ( c.small_int          = b.small_int          )
AND ( c.medium_int         = b.medium_int         )
AND ( c.large_int          = b.large_int          )
AND ( c.decimal_1          = b.decimal_1          )
AND ( c.decimal_2_signed   = b.decimal_2_signed   )
AND ( c.decimal_3_unsigned = b.decimal_3_unsigned )
AND ( c.pic_decimal_1      = b.pic_decimal_1      )
AND ( c.pic_decimal_2      = b.pic_decimal_2      )
AND ( c.pic_decimal_3      = b.pic_decimal_3      )
--  Add one local predicate:
AND ( a.pic_x_1            = 'Z' )
AND ( a.pic_x_1            = c.pic_x_1 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s1a')
    
    #   Lots of PREDICATEs (48) involving more than one table.
    stmt = """SELECT a.char_1, b.char_10, c.pic_x_1
FROM   """ + gvars.g_schema_arkcasedb + """.btsel01 a
, """ + gvars.g_schema_arkcasedb + """.btsel01 b
, """ + gvars.g_schema_arkcasedb + """.btsel01 c
--  Compare columns for a and b:
WHERE a.char_1             = b.char_1
AND ( a.char_10            = b.char_10            )
AND ( a.pic_x_1            = b.pic_x_1            )
AND ( a.pic_x_7            = b.pic_x_7            )
AND ( a.pic_x_long         = b.pic_x_long         )
AND ( a.var_char           = b.var_char           )
AND ( a.binary_signed      = b.binary_signed      )
AND ( a.binary_32_u        = b.binary_32_u        )
AND ( a.binary_64_s        = b.binary_64_s        )
AND ( a.pic_comp_1         = b.pic_comp_1         )
AND ( a.pic_comp_2         = b.pic_comp_2         )
AND ( a.pic_comp_3         = b.pic_comp_3         )
AND ( a.small_int          = b.small_int          )
AND ( a.medium_int         = b.medium_int         )
AND ( a.large_int          = b.large_int          )
AND ( a.decimal_1          = b.decimal_1          )
AND ( a.decimal_2_signed   = b.decimal_2_signed   )
AND ( a.decimal_3_unsigned = b.decimal_3_unsigned )
AND ( a.pic_decimal_1      = b.pic_decimal_1      )
AND ( a.pic_decimal_2      = b.pic_decimal_2      )
AND ( a.pic_decimal_3      = b.pic_decimal_3      )
--  Compare columns for a and c:
AND ( a.char_1             = c.char_1             )
AND ( a.char_10            = c.char_10            )
AND ( a.pic_x_1            = c.pic_x_1            )
AND ( a.pic_x_7            = c.pic_x_7            )
AND ( a.pic_x_long         = c.pic_x_long         )
AND ( a.var_char           = c.var_char           )
AND ( a.binary_signed      = c.binary_signed      )
AND ( a.binary_32_u        = c.binary_32_u        )
AND ( a.binary_64_s        = c.binary_64_s        )
AND ( a.pic_comp_1         = c.pic_comp_1         )
AND ( a.pic_comp_2         = c.pic_comp_2         )
AND ( a.pic_comp_3         = c.pic_comp_3         )
AND ( a.small_int          = c.small_int          )
AND ( a.medium_int         = c.medium_int         )
AND ( a.large_int          = c.large_int          )
AND ( a.decimal_1          = c.decimal_1          )
AND ( a.decimal_2_signed   = c.decimal_2_signed   )
AND ( a.decimal_3_unsigned = c.decimal_3_unsigned )
AND ( a.pic_decimal_1      = c.pic_decimal_1      )
AND ( a.pic_decimal_2      = c.pic_decimal_2      )
AND ( a.pic_decimal_3      = c.pic_decimal_3      )
--  Compare columns for b and c:
AND ( b.char_1             = c.char_1             )
AND ( b.char_10            = c.char_10            )
AND ( b.pic_x_1            = c.pic_x_1            )
AND ( b.pic_x_7            = c.pic_x_7            )
AND ( b.pic_x_long         = c.pic_x_long         )
AND ( b.var_char           = c.var_char           )
AND ( b.binary_signed      = c.binary_signed      )
AND ( b.binary_32_u        = c.binary_32_u        )
AND ( b.binary_64_s        = c.binary_64_s        )
AND ( b.pic_comp_1         = c.pic_comp_1         )
AND ( b.pic_comp_2         = c.pic_comp_2         )
AND ( b.pic_comp_3         = c.pic_comp_3         )
AND ( b.small_int          = c.small_int          )
AND ( b.medium_int         = c.medium_int         )
AND ( b.large_int          = c.large_int          )
AND ( b.decimal_1          = c.decimal_1          )
AND ( b.decimal_2_signed   = c.decimal_2_signed   )
AND ( b.decimal_3_unsigned = c.decimal_3_unsigned )
AND ( b.pic_decimal_1      = c.pic_decimal_1      )
AND ( b.pic_decimal_2      = c.pic_decimal_2      )
AND ( b.pic_decimal_3      = c.pic_decimal_3      )
--  Add one local predicate:
AND ( a.pic_x_1            = 'Z' )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s1')
    
    #   Lots of PREDICATEs (160) involving more than one table.
    #   For B41, get SQLCOMP out of space with full extended segment.
    #   Still a problem for C10+, even with segment resized to 4Meg.
    stmt = """SELECT a.char_1, b.char_10, c.char_1, d.char_10, e.pic_x_1
,f.char_1, g.char_10, h.char_1, i.char_10, j.pic_x_1
FROM    """ + gvars.g_schema_arkcasedb + """.btsel01 a
, """ + gvars.g_schema_arkcasedb + """.btsel01 b
, """ + gvars.g_schema_arkcasedb + """.btsel01 c
, """ + gvars.g_schema_arkcasedb + """.btsel01 d
, """ + gvars.g_schema_arkcasedb + """.btsel01 e
, """ + gvars.g_schema_arkcasedb + """.btsel01 f
, """ + gvars.g_schema_arkcasedb + """.btsel01 g
, """ + gvars.g_schema_arkcasedb + """.btsel01 h
, """ + gvars.g_schema_arkcasedb + """.btsel01 i
, """ + gvars.g_schema_arkcasedb + """.btsel01 j
--  Compare columns for a and b:
WHERE a.char_1             = b.char_1
AND ( a.char_10            = b.char_10            )
AND ( a.pic_x_1            = b.pic_x_1            )
AND ( a.pic_x_7            = b.pic_x_7            )
AND ( a.pic_x_long         = b.pic_x_long         )
AND ( a.var_char           = b.var_char           )
AND ( a.binary_signed      = b.binary_signed      )
AND ( a.binary_32_u        = b.binary_32_u        )
AND ( a.binary_64_s        = b.binary_64_s        )
AND ( a.pic_comp_1         = b.pic_comp_1         )
AND ( a.pic_comp_2         = b.pic_comp_2         )
AND ( a.pic_comp_3         = b.pic_comp_3         )
AND ( a.small_int          = b.small_int          )
AND ( a.medium_int         = b.medium_int         )
AND ( a.large_int          = b.large_int          )
AND ( a.decimal_1          = b.decimal_1          )
AND ( a.decimal_2_signed   = b.decimal_2_signed   )
AND ( a.decimal_3_unsigned = b.decimal_3_unsigned )
AND ( a.pic_decimal_1      = b.pic_decimal_1      )
AND ( a.pic_decimal_2      = b.pic_decimal_2      )
AND ( a.pic_decimal_3      = b.pic_decimal_3      )
--  Compare columns for a and c:
AND ( a.char_1             = c.char_1             )
AND ( a.char_10            = c.char_10            )
AND ( a.pic_x_1            = c.pic_x_1            )
AND ( a.pic_x_7            = c.pic_x_7            )
AND ( a.pic_x_long         = c.pic_x_long         )
AND ( a.var_char           = c.var_char           )
AND ( a.binary_signed      = c.binary_signed      )
AND ( a.binary_32_u        = c.binary_32_u        )
AND ( a.binary_64_s        = c.binary_64_s        )
AND ( a.pic_comp_1         = c.pic_comp_1         )
AND ( a.pic_comp_2         = c.pic_comp_2         )
AND ( a.pic_comp_3         = c.pic_comp_3         )
AND ( a.small_int          = c.small_int          )
AND ( a.medium_int         = c.medium_int         )
AND ( a.large_int          = c.large_int          )
AND ( a.decimal_1          = c.decimal_1          )
AND ( a.decimal_2_signed   = c.decimal_2_signed   )
AND ( a.decimal_3_unsigned = c.decimal_3_unsigned )
AND ( a.pic_decimal_1      = c.pic_decimal_1      )
AND ( a.pic_decimal_2      = c.pic_decimal_2      )
AND ( a.pic_decimal_3      = c.pic_decimal_3      )
--  Compare columns for b and c:
AND ( b.char_1             = c.char_1             )
AND ( b.char_10            = c.char_10            )
AND ( b.pic_x_1            = c.pic_x_1            )
AND ( b.pic_x_7            = c.pic_x_7            )
AND ( b.pic_x_long         = c.pic_x_long         )
AND ( b.var_char           = c.var_char           )
AND ( b.binary_signed      = c.binary_signed      )
AND ( b.binary_32_u        = c.binary_32_u        )
AND ( b.binary_64_s        = c.binary_64_s        )
AND ( b.pic_comp_1         = c.pic_comp_1         )
AND ( b.pic_comp_2         = c.pic_comp_2         )
AND ( b.pic_comp_3         = c.pic_comp_3         )
AND ( b.small_int          = c.small_int          )
AND ( b.medium_int         = c.medium_int         )
AND ( b.large_int          = c.large_int          )
AND ( b.decimal_1          = c.decimal_1          )
AND ( b.decimal_2_signed   = c.decimal_2_signed   )
AND ( b.decimal_3_unsigned = c.decimal_3_unsigned )
AND ( b.pic_decimal_1      = c.pic_decimal_1      )
AND ( b.pic_decimal_2      = c.pic_decimal_2      )
--  Compare columns for a and d:
AND ( a.char_1             = d.char_1             )
AND ( a.char_10            = d.char_10            )
AND ( a.pic_x_1            = d.pic_x_1            )
AND ( a.pic_x_7            = d.pic_x_7            )
AND ( a.pic_x_long         = d.pic_x_long         )
AND ( a.var_char           = d.var_char           )
AND ( a.binary_signed      = d.binary_signed      )
AND ( a.binary_32_u        = d.binary_32_u        )
AND ( a.binary_64_s        = d.binary_64_s        )
AND ( a.pic_comp_1         = d.pic_comp_1         )
AND ( a.pic_comp_2         = d.pic_comp_2         )
AND ( a.pic_comp_3         = d.pic_comp_3         )
AND ( a.small_int          = d.small_int          )
AND ( a.medium_int         = d.medium_int         )
AND ( a.large_int          = d.large_int          )
AND ( a.decimal_1          = d.decimal_1          )
AND ( a.decimal_2_signed   = d.decimal_2_signed   )
AND ( a.decimal_3_unsigned = d.decimal_3_unsigned )
AND ( a.pic_decimal_1      = d.pic_decimal_1      )
AND ( a.pic_decimal_2      = d.pic_decimal_2      )
AND ( a.pic_decimal_3      = d.pic_decimal_3      )
--  Compare columns for a and e:
AND ( a.char_1             = e.char_1             )
AND ( a.char_10            = e.char_10            )
AND ( a.pic_x_1            = e.pic_x_1            )
AND ( a.pic_x_7            = e.pic_x_7            )
AND ( a.pic_x_long         = e.pic_x_long         )
AND ( a.var_char           = e.var_char           )
AND ( a.binary_signed      = e.binary_signed      )
AND ( a.binary_32_u        = e.binary_32_u        )
AND ( a.binary_64_s        = e.binary_64_s        )
AND ( a.pic_comp_1         = e.pic_comp_1         )
AND ( a.pic_comp_2         = e.pic_comp_2         )
AND ( a.pic_comp_3         = e.pic_comp_3         )
AND ( a.small_int          = e.small_int          )
AND ( a.medium_int         = e.medium_int         )
AND ( a.large_int          = e.large_int          )
AND ( a.decimal_1          = e.decimal_1          )
AND ( a.decimal_2_signed   = e.decimal_2_signed   )
AND ( a.decimal_3_unsigned = e.decimal_3_unsigned )
AND ( a.pic_decimal_1      = e.pic_decimal_1      )
AND ( a.pic_decimal_2      = e.pic_decimal_2      )
AND ( a.pic_decimal_3      = e.pic_decimal_3      )
--  Compare columns for a and f:
AND ( a.char_1             = f.char_1             )
AND ( a.char_10            = f.char_10            )
AND ( a.pic_x_1            = f.pic_x_1            )
AND ( a.pic_x_7            = f.pic_x_7            )
AND ( a.pic_x_long         = f.pic_x_long         )
AND ( a.var_char           = f.var_char           )
AND ( a.binary_signed      = f.binary_signed      )
AND ( a.binary_32_u        = f.binary_32_u        )
AND ( a.binary_64_s        = f.binary_64_s        )
AND ( a.pic_comp_1         = f.pic_comp_1         )
AND ( a.pic_comp_2         = f.pic_comp_2         )
AND ( a.pic_comp_3         = f.pic_comp_3         )
AND ( a.small_int          = f.small_int          )
AND ( a.medium_int         = f.medium_int         )
AND ( a.large_int          = f.large_int          )
AND ( a.decimal_1          = f.decimal_1          )
AND ( a.decimal_2_signed   = f.decimal_2_signed   )
AND ( a.decimal_3_unsigned = f.decimal_3_unsigned )
AND ( a.pic_decimal_1      = f.pic_decimal_1      )
AND ( a.pic_decimal_2      = f.pic_decimal_2      )
AND ( a.pic_decimal_3      = f.pic_decimal_3      )
--  Compare columns for a and g:
AND ( a.char_1             = g.char_1             )
AND ( a.char_10            = g.char_10            )
AND ( a.pic_x_1            = g.pic_x_1            )
AND ( a.pic_x_7            = g.pic_x_7            )
AND ( a.pic_x_long         = g.pic_x_long         )
AND ( a.var_char           = g.var_char           )
AND ( a.binary_signed      = g.binary_signed      )
AND ( a.binary_32_u        = g.binary_32_u        )
AND ( a.binary_64_s        = g.binary_64_s        )
AND ( a.pic_comp_1         = g.pic_comp_1         )
AND ( a.pic_comp_2         = g.pic_comp_2         )
AND ( a.pic_comp_3         = g.pic_comp_3         )
AND ( a.small_int          = g.small_int          )
AND ( a.medium_int         = g.medium_int         )
AND ( a.large_int          = g.large_int          )
AND ( a.decimal_1          = g.decimal_1          )
AND ( a.decimal_2_signed   = g.decimal_2_signed   )
AND ( a.decimal_3_unsigned = g.decimal_3_unsigned )
AND ( a.pic_decimal_1      = g.pic_decimal_1      )
AND ( a.pic_decimal_2      = g.pic_decimal_2      )
AND ( a.pic_decimal_3      = g.pic_decimal_3      )
--  Compare columns for a and h:
AND ( a.char_1             = h.char_1             )
AND ( a.char_10            = h.char_10            )
AND ( a.pic_x_1            = h.pic_x_1            )
AND ( a.pic_x_7            = h.pic_x_7            )
AND ( a.pic_x_long         = h.pic_x_long         )
AND ( a.var_char           = h.var_char           )
AND ( a.binary_signed      = h.binary_signed      )
AND ( a.binary_32_u        = h.binary_32_u        )
AND ( a.binary_64_s        = h.binary_64_s        )
AND ( a.pic_comp_1         = h.pic_comp_1         )
AND ( a.pic_comp_2         = h.pic_comp_2         )
AND ( a.pic_comp_3         = h.pic_comp_3         )
AND ( a.small_int          = h.small_int          )
AND ( a.medium_int         = h.medium_int         )
AND ( a.large_int          = h.large_int          )
AND ( a.decimal_1          = h.decimal_1          )
AND ( a.decimal_2_signed   = h.decimal_2_signed   )
AND ( a.decimal_3_unsigned = h.decimal_3_unsigned )
AND ( a.pic_decimal_1      = h.pic_decimal_1      )
AND ( a.pic_decimal_2      = h.pic_decimal_2      )
AND ( a.pic_decimal_3      = h.pic_decimal_3      )
--  Compare columns for a and i:
AND ( a.char_1             = i.char_1             )
AND ( a.char_10            = i.char_10            )
AND ( a.pic_x_1            = i.pic_x_1            )
AND ( a.pic_x_7            = i.pic_x_7            )
AND ( a.pic_x_long         = i.pic_x_long         )
AND ( a.var_char           = i.var_char           )
AND ( a.binary_signed      = i.binary_signed      )
AND ( a.binary_32_u        = i.binary_32_u        )
AND ( a.binary_64_s        = i.binary_64_s        )
AND ( a.pic_comp_1         = i.pic_comp_1         )
AND ( a.pic_comp_2         = i.pic_comp_2         )
AND ( a.pic_comp_3         = i.pic_comp_3         )
AND ( a.small_int          = i.small_int          )
AND ( a.medium_int         = i.medium_int         )
AND ( a.large_int          = i.large_int          )
AND ( a.decimal_1          = i.decimal_1          )
AND ( a.decimal_2_signed   = i.decimal_2_signed   )
AND ( a.decimal_3_unsigned = i.decimal_3_unsigned )
AND ( a.pic_decimal_1      = i.pic_decimal_1      )
AND ( a.pic_decimal_2      = i.pic_decimal_2      )
AND ( a.pic_decimal_3      = i.pic_decimal_3      )
--  Compare columns for a and j:
AND ( a.char_1             = j.char_1             )
AND ( a.char_10            = j.char_10            )
AND ( a.pic_x_1            = j.pic_x_1            )
AND ( a.pic_x_7            = j.pic_x_7            )
AND ( a.pic_x_long         = j.pic_x_long         )
AND ( a.var_char           = j.var_char           )
AND ( a.binary_signed      = j.binary_signed      )
AND ( a.binary_32_u        = j.binary_32_u        )
AND ( a.binary_64_s        = j.binary_64_s        )
AND ( a.pic_comp_1         = j.pic_comp_1         )
AND ( a.pic_comp_2         = j.pic_comp_2         )
AND ( a.pic_comp_3         = j.pic_comp_3         )
AND ( a.small_int          = j.small_int          )
AND ( a.medium_int         = j.medium_int         )
AND ( a.large_int          = j.large_int          )
AND ( a.decimal_1          = j.decimal_1          )
AND ( a.decimal_2_signed   = j.decimal_2_signed   )
AND ( a.decimal_3_unsigned = j.decimal_3_unsigned )
AND ( a.pic_decimal_1      = j.pic_decimal_1      )
AND ( a.pic_decimal_2      = j.pic_decimal_2      )
AND ( a.pic_decimal_3      = j.pic_decimal_3      )
--  Add one local predicate:
AND ( a.pic_x_1            = 'Z' )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s2')
    
    _testmgr.testcase_end(desc)

def test005(desc="""a05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt110 : A05
    #  Description:        Large number of COLUMNs referenced
    #                      (normalizer stores totals).
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    #
    #  ---------------------------------
    #  Create the Log file.
    #  ---------------------------------
    #  ---------------------------------
    #  Set up default catalog and schema
    #  ---------------------------------
    # set catalog eval;
    # set schema  eval.gdb;
    #
    #
    
    stmt = """SELECT a.pic_x_1
FROM   """ + gvars.g_schema_arkcasedb + """.btsel01 a
--  Compare columns for all tables:
WHERE
--  Compare columns for a:
( a.char_1             = 'Z' )
OR ( a.char_10            = 'Z' )
OR ( a.pic_x_1            = 'Z' )
OR ( a.pic_x_7            = 'Z' )
OR ( a.pic_x_long         = 'Z' )
OR ( a.var_char           = 'Z' )
--  No numeric fields store the value 42:
OR ( a.binary_signed      = 42  )
OR ( a.binary_32_u        = 42  )
OR ( a.binary_64_s        = 42  )
OR ( a.pic_comp_1         = 42  )
OR ( a.pic_comp_2         = 42  )
OR ( a.pic_comp_3         = 42  )
OR ( a.small_int          = 42  )
OR ( a.medium_int         = 42  )
OR ( a.large_int          = 42  )
OR ( a.decimal_1          = 42  )
OR ( a.decimal_2_signed   = 42  )
OR ( a.decimal_3_unsigned = 42  )
OR ( a.pic_decimal_1      = 42  )
OR ( a.pic_decimal_2      = 42  )
OR ( a.pic_decimal_3      = 42  )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    
    stmt = """SELECT DISTINCT a.pic_x_1, b.pic_x_1
FROM   """ + gvars.g_schema_arkcasedb + """.btsel01 a
,""" + gvars.g_schema_arkcasedb + """.btsel01 b
--  Compare columns for all tables:
WHERE  a.pic_x_1            = b.pic_x_1
AND (
( a.pic_x_1            = 'Z' )
--  Compare columns for a:
OR ( a.char_1             = 'Z' )
OR ( a.char_10            = 'Z' )
--        a.pic_x_1 checked above
OR ( a.pic_x_7            = 'Z' )
OR ( a.pic_x_long         = 'Z' )
OR ( a.var_char           = 'Z' )
--  Note: No numeric fields store the value 42:
OR ( a.binary_signed      = 42  )
OR ( a.binary_32_u        = 42  )
OR ( a.binary_64_s        = 42  )
OR ( a.pic_comp_1         = 42  )
OR ( a.pic_comp_2         = 42  )
OR ( a.pic_comp_3         = 42  )
OR ( a.small_int          = 42  )
OR ( a.medium_int         = 42  )
OR ( a.large_int          = 42  )
OR ( a.decimal_1          = 42  )
OR ( a.decimal_2_signed   = 42  )
OR ( a.decimal_3_unsigned = 42  )
OR ( a.pic_decimal_1      = 42  )
OR ( a.pic_decimal_2      = 42  )
OR ( a.pic_decimal_3      = 42  )
--  Compare columns for b:
AND (b.char_1             = 'Z' )
OR ( b.char_10            = 'Z' )
--   b.pic_x_1 checked above
OR ( b.pic_x_7            = 'Z' )
OR ( b.pic_x_long         = 'Z' )
OR ( b.var_char           = 'Z' )
--  No numeric fields store the value 42:
OR ( b.binary_signed      = 42  )
OR ( b.binary_32_u        = 42  )
OR ( b.binary_64_s        = 42  )
OR ( b.pic_comp_1         = 42  )
OR ( b.pic_comp_2         = 42  )
OR ( b.pic_comp_3         = 42  )
OR ( b.small_int          = 42  )
OR ( b.medium_int         = 42  )
OR ( b.large_int          = 42  )
OR ( b.decimal_1          = 42  )
OR ( b.decimal_2_signed   = 42  )
OR ( b.decimal_3_unsigned = 42  )
OR ( b.pic_decimal_1      = 42  )
OR ( b.pic_decimal_2      = 42  )
OR ( b.pic_decimal_3      = 42  )
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
    
    stmt = """SELECT DISTINCT a.pic_x_1, b.pic_x_1, c.pic_x_1
FROM        """ + gvars.g_schema_arkcasedb + """.btsel01 a
, """ + gvars.g_schema_arkcasedb + """.btsel01 b
, """ + gvars.g_schema_arkcasedb + """.btsel01 c
--  Compare columns for all tables:
WHERE a.pic_x_1            = b.pic_x_1
AND ( a.pic_x_1            = c.pic_x_1 )
AND (
( a.pic_x_1            = 'Z' )
--  Compare columns for a:
OR ( a.char_1             = 'Z' )
OR ( a.char_10            = 'Z' )
--        a.pic_x_1 checked above
OR ( a.pic_x_7            = 'Z' )
OR ( a.pic_x_long         = 'Z' )
OR ( a.var_char           = 'Z' )
--  Note: No numeric fields store the value 42
OR ( a.binary_signed      = 42  )
OR ( a.binary_32_u        = 42  )
OR ( a.binary_64_s        = 42  )
OR ( a.pic_comp_1         = 42  )
OR ( a.pic_comp_2         = 42  )
OR ( a.pic_comp_3         = 42  )
OR ( a.small_int          = 42  )
OR ( a.medium_int         = 42  )
OR ( a.large_int          = 42  )
OR ( a.decimal_1          = 42  )
OR ( a.decimal_2_signed   = 42  )
OR ( a.decimal_3_unsigned = 42  )
OR ( a.pic_decimal_1      = 42  )
OR ( a.pic_decimal_2      = 42  )
OR ( a.pic_decimal_3      = 42  )
--  Compare columns for b:
OR  (b.char_1             = 'Z' )
OR ( b.char_10            = 'Z' )
--        b.pic_x_1 checked above implicitly.
OR ( b.pic_x_7            = 'Z' )
OR ( b.pic_x_long         = 'Z' )
OR ( b.var_char           = 'Z' )
--  No numeric fields store the value 42:
OR ( b.binary_signed      = 42  )
OR ( b.binary_32_u        = 42  )
OR ( b.binary_64_s        = 42  )
OR ( b.pic_comp_1         = 42  )
OR ( b.pic_comp_2         = 42  )
OR ( b.pic_comp_3         = 42  )
OR ( b.small_int          = 42  )
OR ( b.medium_int         = 42  )
OR ( b.large_int          = 42  )
OR ( b.decimal_1          = 42  )
OR ( b.decimal_2_signed   = 42  )
OR ( b.decimal_3_unsigned = 42  )
OR ( b.pic_decimal_1      = 42  )
OR ( b.pic_decimal_2      = 42  )
OR ( b.pic_decimal_3      = 42  )
--  Compare columns for c:
OR  (c.char_1             = 'Z' )
OR ( c.char_10            = 'Z' )
--        c.pic_x_1 checked above implicitly.
OR ( c.pic_x_7            = 'Z' )
OR ( c.pic_x_long         = 'Z' )
OR ( c.var_char           = 'Z' )
--  No numeric fields store the value 42:
OR ( c.binary_signed      = 42  )
OR ( c.binary_32_u        = 42  )
OR ( c.binary_64_s        = 42  )
OR ( c.pic_comp_1         = 42  )
OR ( c.pic_comp_2         = 42  )
OR ( c.pic_comp_3         = 42  )
OR ( c.small_int          = 42  )
OR ( c.medium_int         = 42  )
OR ( c.large_int          = 42  )
OR ( c.decimal_1          = 42  )
OR ( c.decimal_2_signed   = 42  )
OR ( c.decimal_3_unsigned = 42  )
OR ( c.pic_decimal_1      = 42  )
OR ( c.pic_decimal_2      = 42  )
OR ( c.pic_decimal_3      = 42  )
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    
    _testmgr.testcase_end(desc)

def test006(desc="""a06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt110 : A06
    #  Description:        Large number of COLUMNs referenced
    #                      in ORDER BY and GROUP BY clauses
    #                      (normalizer stores totals).
    #  Test case inputs:   --
    #  Test case outputs:  --
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    #
    #  ---------------------------------
    #  Create the Log file.
    #  ---------------------------------
    #  ---------------------------------
    #  Set up default catalog and schema
    #  ---------------------------------
    # set catalog eval;
    # set schema  eval.gdb;
    #
    #
    
    #  So that we can maximize the number of columns that we can see:
    
    stmt = """SELECT a.char_1, a.pic_x_1, a.small_int, a.pic_decimal_3
, b.char_1, b.pic_x_1, b.small_int, b.pic_decimal_3
, c.char_1, c.pic_x_1, c.small_int, c.pic_decimal_3
, d.char_1, d.pic_x_1, d.small_int, d.pic_decimal_3
, e.char_1, e.pic_x_1, e.small_int, e.pic_decimal_3
FROM """ + gvars.g_schema_arkcasedb + """.btsel01 a
, """ + gvars.g_schema_arkcasedb + """.btsel01 b
, """ + gvars.g_schema_arkcasedb + """.btsel01 c
, """ + gvars.g_schema_arkcasedb + """.btsel01 d
, """ + gvars.g_schema_arkcasedb + """.btsel01 e
--  Compare columns for all tables:
WHERE a.pic_x_1            = b.pic_x_1
AND (a.pic_x_1            = c.pic_x_1 )
AND (a.pic_x_1            = d.pic_x_1 )
AND (a.pic_x_1            = e.pic_x_1 )
--  Compare columns for a:
AND (a.pic_x_1            = 'Z' )
--  GROUP BYs for 4 cols for each of 5 tables in the join (i.e. 20
--  cols):
GROUP BY  a.char_1, a.pic_x_1, a.small_int, a.pic_decimal_3
,b.char_1, b.pic_x_1, b.small_int, b.pic_decimal_3
,c.char_1, c.pic_x_1, c.small_int, c.pic_decimal_3
,d.char_1, d.pic_x_1, d.small_int, d.pic_decimal_3
,e.char_1, e.pic_x_1, e.small_int, e.pic_decimal_3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s0')
    
    stmt = """SELECT     a.char_1, a.pic_x_1, a.small_int, a.pic_decimal_3
, b.char_1, b.pic_x_1, b.small_int, b.pic_decimal_3
, c.char_1, c.pic_x_1, c.small_int, c.pic_decimal_3
, d.char_1, d.pic_x_1, d.small_int, d.pic_decimal_3
, e.char_1, e.pic_x_1, e.small_int, e.pic_decimal_3
, f.char_1, f.pic_x_1, f.small_int, f.pic_decimal_3
, g.char_1, g.pic_x_1, g.small_int, g.pic_decimal_3
, h.char_1, h.pic_x_1, h.small_int, h.pic_decimal_3
, i.char_1, i.pic_x_1, i.small_int, i.pic_decimal_3
, j.char_1, j.pic_x_1, j.small_int, j.pic_decimal_3
FROM        """ + gvars.g_schema_arkcasedb + """.btsel01 a
, """ + gvars.g_schema_arkcasedb + """.btsel01 b
, """ + gvars.g_schema_arkcasedb + """.btsel01 c
, """ + gvars.g_schema_arkcasedb + """.btsel01 d
, """ + gvars.g_schema_arkcasedb + """.btsel01 e
, """ + gvars.g_schema_arkcasedb + """.btsel01 f
, """ + gvars.g_schema_arkcasedb + """.btsel01 g
, """ + gvars.g_schema_arkcasedb + """.btsel01 h
, """ + gvars.g_schema_arkcasedb + """.btsel01 i
, """ + gvars.g_schema_arkcasedb + """.btsel01 j
--  Compare columns for all tables:
WHERE     a.pic_x_1            = b.pic_x_1
AND (a.pic_x_1            = c.pic_x_1 )
AND (a.pic_x_1            = d.pic_x_1 )
AND (a.pic_x_1            = e.pic_x_1 )
AND (a.pic_x_1            = f.pic_x_1 )
AND (a.pic_x_1            = g.pic_x_1)
AND (a.pic_x_1            = h.pic_x_1)
AND (a.pic_x_1            = i.pic_x_1)
AND (a.pic_x_1            = j.pic_x_1)
--  Compare columns for a:
AND (a.pic_x_1            = 'Z' )
--  GROUP BYs for 4 cols for each of 10 tables in the join (i.e. 40
--  cols):
GROUP BY	 a.char_1, a.pic_x_1, a.small_int, a.pic_decimal_3
,b.char_1, b.pic_x_1, b.small_int, b.pic_decimal_3
,c.char_1, c.pic_x_1, c.small_int, c.pic_decimal_3
,d.char_1, d.pic_x_1, d.small_int, d.pic_decimal_3
,e.char_1, e.pic_x_1, e.small_int, e.pic_decimal_3
,f.char_1, f.pic_x_1, f.small_int, f.pic_decimal_3
,g.char_1, g.pic_x_1, g.small_int, g.pic_decimal_3
,h.char_1, h.pic_x_1, h.small_int, h.pic_decimal_3
,i.char_1, i.pic_x_1, i.small_int, i.pic_decimal_3
,j.char_1, j.pic_x_1, j.small_int, j.pic_decimal_3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s1')
    
    #   More columns in GROUP BYs:
    stmt = """SELECT     a.char_1, a.pic_x_1, a.small_int, a.pic_decimal_3
, b.char_1, b.pic_x_1, b.small_int, b.pic_decimal_3
, c.char_1, c.pic_x_1, c.small_int, c.pic_decimal_3
, d.char_1, d.pic_x_1, d.small_int, d.pic_decimal_3
, e.char_1, e.pic_x_1, e.small_int, e.pic_decimal_3
, f.char_1, f.pic_x_1, f.small_int, f.pic_decimal_3
, g.char_1, g.pic_x_1, g.small_int, g.pic_decimal_3
, h.char_1, h.pic_x_1, h.small_int, h.pic_decimal_3
, i.char_1, i.pic_x_1, i.small_int, i.pic_decimal_3
, j.char_1, j.pic_x_1, j.small_int, j.pic_decimal_3
, k.char_1, k.pic_x_1, k.small_int, k.pic_decimal_3
, l.char_1, l.pic_x_1, l.small_int, l.pic_decimal_3
FROM        """ + gvars.g_schema_arkcasedb + """.btsel01 a
, """ + gvars.g_schema_arkcasedb + """.btsel01 b
, """ + gvars.g_schema_arkcasedb + """.btsel01 c
, """ + gvars.g_schema_arkcasedb + """.btsel01 d
, """ + gvars.g_schema_arkcasedb + """.btsel01 e
, """ + gvars.g_schema_arkcasedb + """.btsel01 f
, """ + gvars.g_schema_arkcasedb + """.btsel01 g
, """ + gvars.g_schema_arkcasedb + """.btsel01 h
, """ + gvars.g_schema_arkcasedb + """.btsel01 i
, """ + gvars.g_schema_arkcasedb + """.btsel01 j
, """ + gvars.g_schema_arkcasedb + """.btsel01 k
, """ + gvars.g_schema_arkcasedb + """.btsel01 l
--  Compare columns for all tables:
WHERE     a.pic_x_1            = b.pic_x_1
AND (a.pic_x_1            = c.pic_x_1 )
AND (a.pic_x_1            = d.pic_x_1 )
AND (a.pic_x_1            = e.pic_x_1 )
AND (a.pic_x_1            = f.pic_x_1 )
AND (a.pic_x_1            = g.pic_x_1)
AND (a.pic_x_1            = h.pic_x_1)
AND (a.pic_x_1            = i.pic_x_1)
AND (a.pic_x_1            = j.pic_x_1)
AND (a.pic_x_1            = k.pic_x_1)
AND (a.pic_x_1            = l.pic_x_1)
--  Compare columns for a:
AND (a.pic_x_1            = 'Z' )
--  GROUP BYs for 4 cols for each of 12 tables in the join (i.e. 48
--  cols):
GROUP BY	 a.char_1, a.pic_x_1, a.small_int, a.pic_decimal_3
,b.char_1, b.pic_x_1, b.small_int, b.pic_decimal_3
,c.char_1, c.pic_x_1, c.small_int, c.pic_decimal_3
,d.char_1, d.pic_x_1, d.small_int, d.pic_decimal_3
,e.char_1, e.pic_x_1, e.small_int, e.pic_decimal_3
,f.char_1, f.pic_x_1, f.small_int, f.pic_decimal_3
,g.char_1, g.pic_x_1, g.small_int, g.pic_decimal_3
,h.char_1, h.pic_x_1, h.small_int, h.pic_decimal_3
,i.char_1, i.pic_x_1, i.small_int, i.pic_decimal_3
,j.char_1, j.pic_x_1, j.small_int, j.pic_decimal_3
,k.char_1, k.pic_x_1, k.small_int, k.pic_decimal_3
,l.char_1, l.pic_x_1, l.small_int, l.pic_decimal_3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s2')
    
    #   More columns in GROUP BYs:
    #   Since B41, get SQLCOMP out of space with full extended segment.
    stmt = """SELECT     a.char_1, a.pic_x_1, a.small_int, a.pic_decimal_3
, b.char_1, b.pic_x_1, b.small_int, b.pic_decimal_3
, c.char_1, c.pic_x_1, c.small_int, c.pic_decimal_3
, d.char_1, d.pic_x_1, d.small_int, d.pic_decimal_3
, e.char_1, e.pic_x_1, e.small_int, e.pic_decimal_3
, f.char_1, f.pic_x_1, f.small_int, f.pic_decimal_3
, g.char_1, g.pic_x_1, g.small_int, g.pic_decimal_3
, h.char_1, h.pic_x_1, h.small_int, h.pic_decimal_3
, i.char_1, i.pic_x_1, i.small_int, i.pic_decimal_3
, j.char_1, j.pic_x_1, j.small_int, j.pic_decimal_3
, k.char_1, k.pic_x_1, k.small_int, k.pic_decimal_3
, l.char_1, l.pic_x_1, l.small_int, l.pic_decimal_3
, m.char_1, m.pic_x_1, m.small_int, m.pic_decimal_3
, n.char_1, n.pic_x_1, n.small_int, n.pic_decimal_3
, o.char_1, o.pic_x_1, o.small_int, o.pic_decimal_3
, p.char_1, p.pic_x_1, p.small_int, p.pic_decimal_3
FROM        """ + gvars.g_schema_arkcasedb + """.btsel01 a
, """ + gvars.g_schema_arkcasedb + """.btsel01 b
, """ + gvars.g_schema_arkcasedb + """.btsel01 c
, """ + gvars.g_schema_arkcasedb + """.btsel01 d
, """ + gvars.g_schema_arkcasedb + """.btsel01 e
, """ + gvars.g_schema_arkcasedb + """.btsel01 f
, """ + gvars.g_schema_arkcasedb + """.btsel01 g
, """ + gvars.g_schema_arkcasedb + """.btsel01 h
, """ + gvars.g_schema_arkcasedb + """.btsel01 i
, """ + gvars.g_schema_arkcasedb + """.btsel01 j
, """ + gvars.g_schema_arkcasedb + """.btsel01 k
, """ + gvars.g_schema_arkcasedb + """.btsel01 l
, """ + gvars.g_schema_arkcasedb + """.btsel01 m
, """ + gvars.g_schema_arkcasedb + """.btsel01 n
, """ + gvars.g_schema_arkcasedb + """.btsel01 o
, """ + gvars.g_schema_arkcasedb + """.btsel01 p
--  Compare columns for all tables:
WHERE     a.pic_x_1            = b.pic_x_1
AND (a.pic_x_1            = c.pic_x_1 )
AND (a.pic_x_1            = d.pic_x_1 )
AND (a.pic_x_1            = e.pic_x_1 )
AND (a.pic_x_1            = f.pic_x_1 )
AND (a.pic_x_1            = g.pic_x_1)
AND (a.pic_x_1            = h.pic_x_1)
AND (a.pic_x_1            = i.pic_x_1)
AND (a.pic_x_1            = j.pic_x_1)
AND (a.pic_x_1            = k.pic_x_1)
AND (a.pic_x_1            = l.pic_x_1)
AND (a.pic_x_1            = m.pic_x_1)
AND (a.pic_x_1            = n.pic_x_1)
AND (a.pic_x_1            = o.pic_x_1)
AND (a.pic_x_1            = p.pic_x_1)
--  Compare columns for a:
AND (a.pic_x_1            = 'Z' )
--  GROUP BYs for 4 cols for each of 16 tables in the join (i.e. 64
--  cols):
GROUP BY          a.char_1, a.pic_x_1, a.small_int, a.pic_decimal_3
, b.char_1, b.pic_x_1, b.small_int, b.pic_decimal_3
, c.char_1, c.pic_x_1, c.small_int, c.pic_decimal_3
, d.char_1, d.pic_x_1, d.small_int, d.pic_decimal_3
, e.char_1, e.pic_x_1, e.small_int, e.pic_decimal_3
, f.char_1, f.pic_x_1, f.small_int, f.pic_decimal_3
, g.char_1, g.pic_x_1, g.small_int, g.pic_decimal_3
, h.char_1, h.pic_x_1, h.small_int, h.pic_decimal_3
, i.char_1, i.pic_x_1, i.small_int, i.pic_decimal_3
, j.char_1, j.pic_x_1, j.small_int, j.pic_decimal_3
, k.char_1, k.pic_x_1, k.small_int, k.pic_decimal_3
, l.char_1, l.pic_x_1, l.small_int, l.pic_decimal_3
, m.char_1, m.pic_x_1, m.small_int, m.pic_decimal_3
, n.char_1, n.pic_x_1, n.small_int, n.pic_decimal_3
, o.char_1, o.pic_x_1, o.small_int, o.pic_decimal_3
, p.char_1, p.pic_x_1, p.small_int, p.pic_decimal_3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s3')
    
    #   More columns in GROUP BYs:
    #   Since B41, get SQLCOMP out of space with full extended segment.
    stmt = """SELECT     a.char_1, a.pic_x_1, a.small_int, a.pic_decimal_3
, a.binary_signed, a.pic_comp_1, a.decimal_1
, b.char_1, b.pic_x_1, b.small_int, b.pic_decimal_3
, b.binary_signed, b.pic_comp_1, b.decimal_1
, c.char_1, c.pic_x_1, c.small_int, c.pic_decimal_3
, c.binary_signed, c.pic_comp_1, c.decimal_1
, d.char_1, d.pic_x_1, d.small_int, d.pic_decimal_3
, d.binary_signed, d.pic_comp_1, d.decimal_1
, e.char_1, e.pic_x_1, e.small_int, e.pic_decimal_3
, e.binary_signed, e.pic_comp_1, e.decimal_1
, f.char_1, f.pic_x_1, f.small_int, f.pic_decimal_3
, f.binary_signed, f.pic_comp_1, f.decimal_1
, g.char_1, g.pic_x_1, g.small_int, g.pic_decimal_3
, g.binary_signed, g.pic_comp_1, g.decimal_1
, h.char_1, h.pic_x_1, h.small_int, h.pic_decimal_3
, h.binary_signed, h.pic_comp_1, h.decimal_1
, i.char_1, i.pic_x_1, i.small_int, i.pic_decimal_3
, i.binary_signed, i.pic_comp_1, i.decimal_1
, j.char_1, j.pic_x_1, j.small_int, j.pic_decimal_3
, j.binary_signed, j.pic_comp_1, j.decimal_1
, k.char_1, k.pic_x_1, k.small_int, k.pic_decimal_3
, k.binary_signed, k.pic_comp_1, k.decimal_1
, l.char_1, l.pic_x_1, l.small_int, l.pic_decimal_3
, l.binary_signed, l.pic_comp_1, l.decimal_1
, m.char_1, m.pic_x_1, m.small_int, m.pic_decimal_3
, m.binary_signed, m.pic_comp_1, m.decimal_1
, n.char_1, n.pic_x_1, n.small_int, n.pic_decimal_3
, n.binary_signed, n.pic_comp_1, n.decimal_1
, o.char_1, o.pic_x_1, o.small_int, o.pic_decimal_3
, o.binary_signed, o.pic_comp_1, o.decimal_1
, p.char_1, p.pic_x_1, p.small_int, p.pic_decimal_3
, p.binary_signed, p.pic_comp_1, p.decimal_1
FROM        """ + gvars.g_schema_arkcasedb + """.btsel01 a
, """ + gvars.g_schema_arkcasedb + """.btsel01 b
, """ + gvars.g_schema_arkcasedb + """.btsel01 c
, """ + gvars.g_schema_arkcasedb + """.btsel01 d
, """ + gvars.g_schema_arkcasedb + """.btsel01 e
, """ + gvars.g_schema_arkcasedb + """.btsel01 f
, """ + gvars.g_schema_arkcasedb + """.btsel01 g
, """ + gvars.g_schema_arkcasedb + """.btsel01 h
, """ + gvars.g_schema_arkcasedb + """.btsel01 i
, """ + gvars.g_schema_arkcasedb + """.btsel01 j
, """ + gvars.g_schema_arkcasedb + """.btsel01 k
, """ + gvars.g_schema_arkcasedb + """.btsel01 l
, """ + gvars.g_schema_arkcasedb + """.btsel01 m
, """ + gvars.g_schema_arkcasedb + """.btsel01 n
, """ + gvars.g_schema_arkcasedb + """.btsel01 o
, """ + gvars.g_schema_arkcasedb + """.btsel01 p
--  Compare columns for all tables:
WHERE     a.pic_x_1            = b.pic_x_1
AND (a.pic_x_1            = c.pic_x_1)
AND (a.pic_x_1            = d.pic_x_1)
AND (a.pic_x_1            = e.pic_x_1)
AND (a.pic_x_1            = f.pic_x_1)
AND (a.pic_x_1            = g.pic_x_1)
AND (a.pic_x_1            = h.pic_x_1)
AND (a.pic_x_1            = i.pic_x_1)
AND (a.pic_x_1            = j.pic_x_1)
AND (a.pic_x_1            = k.pic_x_1)
AND (a.pic_x_1            = l.pic_x_1)
AND (a.pic_x_1            = m.pic_x_1)
AND (a.pic_x_1            = n.pic_x_1)
AND (a.pic_x_1            = o.pic_x_1)
AND (a.pic_x_1            = p.pic_x_1)
--  Compare columns for a:
AND (a.pic_x_1            = 'Z' )
--  GROUP BYs for 7 cols for each of 16 tables in the join (i.e. 112
--  cols):
GROUP BY 	  a.char_1, a.pic_x_1, a.small_int, a.pic_decimal_3
, a.binary_signed, a.pic_comp_1, a.decimal_1
, b.char_1, b.pic_x_1, b.small_int, b.pic_decimal_3
, b.binary_signed, b.pic_comp_1, b.decimal_1
, c.char_1, c.pic_x_1, c.small_int, c.pic_decimal_3
, c.binary_signed, c.pic_comp_1, c.decimal_1
, d.char_1, d.pic_x_1, d.small_int, d.pic_decimal_3
, d.binary_signed, d.pic_comp_1, d.decimal_1
, e.char_1, e.pic_x_1, e.small_int, e.pic_decimal_3
, e.binary_signed, e.pic_comp_1, e.decimal_1
, f.char_1, f.pic_x_1, f.small_int, f.pic_decimal_3
, f.binary_signed, f.pic_comp_1, f.decimal_1
, g.char_1, g.pic_x_1, g.small_int, g.pic_decimal_3
, g.binary_signed, g.pic_comp_1, g.decimal_1
, h.char_1, h.pic_x_1, h.small_int, h.pic_decimal_3
, h.binary_signed, h.pic_comp_1, h.decimal_1
, i.char_1, i.pic_x_1, i.small_int, i.pic_decimal_3
, i.binary_signed, i.pic_comp_1, i.decimal_1
, j.char_1, j.pic_x_1, j.small_int, j.pic_decimal_3
, j.binary_signed, j.pic_comp_1, j.decimal_1
, k.char_1, k.pic_x_1, k.small_int, k.pic_decimal_3
, k.binary_signed, k.pic_comp_1, k.decimal_1
, l.char_1, l.pic_x_1, l.small_int, l.pic_decimal_3
, l.binary_signed, l.pic_comp_1, l.decimal_1
, m.char_1, m.pic_x_1, m.small_int, m.pic_decimal_3
, m.binary_signed, m.pic_comp_1, m.decimal_1
, n.char_1, n.pic_x_1, n.small_int, n.pic_decimal_3
, n.binary_signed, n.pic_comp_1, n.decimal_1
, o.char_1, o.pic_x_1, o.small_int, o.pic_decimal_3
, o.binary_signed, o.pic_comp_1, o.decimal_1
, p.char_1, p.pic_x_1, p.small_int, p.pic_decimal_3
, p.binary_signed, p.pic_comp_1, p.decimal_1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s4')
    
    #   Lots of columns in ORDER BYs:
    #   Since B41, get SQLCOMP out of space with full extended segment.
    stmt = """SELECT     a.char_1, a.pic_x_1, a.small_int, a.pic_decimal_3
, b.char_1, b.pic_x_1, b.small_int, b.pic_decimal_3
, c.char_1, c.pic_x_1, c.small_int, c.pic_decimal_3
, d.char_1, d.pic_x_1, d.small_int, d.pic_decimal_3
, e.char_1, e.pic_x_1, e.small_int, e.pic_decimal_3
, f.char_1, f.pic_x_1, f.small_int, f.pic_decimal_3
, g.char_1, g.pic_x_1, g.small_int, g.pic_decimal_3
, h.char_1, h.pic_x_1, h.small_int, h.pic_decimal_3
, i.char_1, i.pic_x_1, i.small_int, i.pic_decimal_3
, j.char_1, j.pic_x_1, j.small_int, j.pic_decimal_3
, k.char_1, k.pic_x_1, k.small_int, k.pic_decimal_3
, l.char_1, l.pic_x_1, l.small_int, l.pic_decimal_3
, m.char_1, m.pic_x_1, m.small_int, m.pic_decimal_3
, n.char_1, n.pic_x_1, n.small_int, n.pic_decimal_3
, o.char_1, o.pic_x_1, o.small_int, o.pic_decimal_3
, p.char_1, p.pic_x_1, p.small_int, p.pic_decimal_3
FROM        """ + gvars.g_schema_arkcasedb + """.btsel01 a
, """ + gvars.g_schema_arkcasedb + """.btsel01 b
, """ + gvars.g_schema_arkcasedb + """.btsel01 c
, """ + gvars.g_schema_arkcasedb + """.btsel01 d
, """ + gvars.g_schema_arkcasedb + """.btsel01 e
, """ + gvars.g_schema_arkcasedb + """.btsel01 f
, """ + gvars.g_schema_arkcasedb + """.btsel01 g
, """ + gvars.g_schema_arkcasedb + """.btsel01 h
, """ + gvars.g_schema_arkcasedb + """.btsel01 i
, """ + gvars.g_schema_arkcasedb + """.btsel01 j
, """ + gvars.g_schema_arkcasedb + """.btsel01 k
, """ + gvars.g_schema_arkcasedb + """.btsel01 l
, """ + gvars.g_schema_arkcasedb + """.btsel01 m
, """ + gvars.g_schema_arkcasedb + """.btsel01 n
, """ + gvars.g_schema_arkcasedb + """.btsel01 o
, """ + gvars.g_schema_arkcasedb + """.btsel01 p
--  Compare columns for all tables:
WHERE     a.pic_x_1            = b.pic_x_1
AND (a.pic_x_1            = c.pic_x_1)
AND (a.pic_x_1            = d.pic_x_1)
AND (a.pic_x_1            = e.pic_x_1)
AND (a.pic_x_1            = f.pic_x_1)
AND (a.pic_x_1            = g.pic_x_1)
AND (a.pic_x_1            = h.pic_x_1)
AND (a.pic_x_1            = i.pic_x_1)
AND (a.pic_x_1            = j.pic_x_1)
AND (a.pic_x_1            = k.pic_x_1)
AND (a.pic_x_1            = l.pic_x_1)
AND (a.pic_x_1            = m.pic_x_1)
AND (a.pic_x_1            = n.pic_x_1)
AND (a.pic_x_1            = o.pic_x_1)
AND (a.pic_x_1            = p.pic_x_1)
--  Compare columns for a:
AND (a.pic_x_1            = 'Z' )
--  ORDER BYs for 4 cols for each of 16 tables in the join (i.e. 64
--  cols):
ORDER BY
1,  2,  3,  4,  5,  6,  7,  8,  9
, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19
, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29
, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39
, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49
, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59
, 60, 61, 62, 63, 64
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s5')
    
    #   More columns in ORDER BYs:
    #   Since B41, get SQLCOMP out of space with full extended segment.
    stmt = """SELECT     a.char_1, a.pic_x_1, a.small_int, a.pic_decimal_3
, a.binary_signed, a.pic_comp_1, a.decimal_1
, b.char_1, b.pic_x_1, b.small_int, b.pic_decimal_3
, b.binary_signed, b.pic_comp_1, b.decimal_1
, c.char_1, c.pic_x_1, c.small_int, c.pic_decimal_3
, c.binary_signed, c.pic_comp_1, c.decimal_1
, d.char_1, d.pic_x_1, d.small_int, d.pic_decimal_3
, d.binary_signed, d.pic_comp_1, d.decimal_1
, e.char_1, e.pic_x_1, e.small_int, e.pic_decimal_3
, e.binary_signed, e.pic_comp_1, e.decimal_1
, f.char_1, f.pic_x_1, f.small_int, f.pic_decimal_3
, f.binary_signed, f.pic_comp_1, f.decimal_1
, g.char_1, g.pic_x_1, g.small_int, g.pic_decimal_3
, g.binary_signed, g.pic_comp_1, g.decimal_1
, h.char_1, h.pic_x_1, h.small_int, h.pic_decimal_3
, h.binary_signed, h.pic_comp_1, h.decimal_1
, i.char_1, i.pic_x_1, i.small_int, i.pic_decimal_3
, i.binary_signed, i.pic_comp_1, i.decimal_1
, j.char_1, j.pic_x_1, j.small_int, j.pic_decimal_3
, j.binary_signed, j.pic_comp_1, j.decimal_1
, k.char_1, k.pic_x_1, k.small_int, k.pic_decimal_3
, k.binary_signed, k.pic_comp_1, k.decimal_1
, l.char_1, l.pic_x_1, l.small_int, l.pic_decimal_3
, l.binary_signed, l.pic_comp_1, l.decimal_1
, m.char_1, m.pic_x_1, m.small_int, m.pic_decimal_3
, m.binary_signed, m.pic_comp_1, m.decimal_1
, n.char_1, n.pic_x_1, n.small_int, n.pic_decimal_3
, n.binary_signed, n.pic_comp_1, n.decimal_1
, o.char_1, o.pic_x_1, o.small_int, o.pic_decimal_3
, o.binary_signed, o.pic_comp_1, o.decimal_1
, p.char_1, p.pic_x_1, p.small_int, p.pic_decimal_3
, p.binary_signed, p.pic_comp_1, p.decimal_1
FROM        """ + gvars.g_schema_arkcasedb + """.btsel01 a
, """ + gvars.g_schema_arkcasedb + """.btsel01 b
, """ + gvars.g_schema_arkcasedb + """.btsel01 c
, """ + gvars.g_schema_arkcasedb + """.btsel01 d
, """ + gvars.g_schema_arkcasedb + """.btsel01 e
, """ + gvars.g_schema_arkcasedb + """.btsel01 f
, """ + gvars.g_schema_arkcasedb + """.btsel01 g
, """ + gvars.g_schema_arkcasedb + """.btsel01 h
, """ + gvars.g_schema_arkcasedb + """.btsel01 i
, """ + gvars.g_schema_arkcasedb + """.btsel01 j
, """ + gvars.g_schema_arkcasedb + """.btsel01 k
, """ + gvars.g_schema_arkcasedb + """.btsel01 l
, """ + gvars.g_schema_arkcasedb + """.btsel01 m
, """ + gvars.g_schema_arkcasedb + """.btsel01 n
, """ + gvars.g_schema_arkcasedb + """.btsel01 o
, """ + gvars.g_schema_arkcasedb + """.btsel01 p
WHERE     a.pic_x_1            = b.pic_x_1
AND (a.pic_x_1            = c.pic_x_1)
AND (a.pic_x_1            = d.pic_x_1)
AND (a.pic_x_1            = e.pic_x_1)
AND (a.pic_x_1            = f.pic_x_1)
AND (a.pic_x_1            = g.pic_x_1)
AND (a.pic_x_1            = h.pic_x_1)
AND (a.pic_x_1            = i.pic_x_1)
AND (a.pic_x_1            = j.pic_x_1)
AND (a.pic_x_1            = k.pic_x_1)
AND (a.pic_x_1            = l.pic_x_1)
AND (a.pic_x_1            = m.pic_x_1)
AND (a.pic_x_1            = n.pic_x_1)
AND (a.pic_x_1            = o.pic_x_1)
AND (a.pic_x_1            = p.pic_x_1)
--  Compare columns for a:
AND (a.pic_x_1            = 'Z' )
--  GROUP BYs for 7 cols for each of 16 tables in the join (i.e. 102
--  cols):
ORDER BY
1,  2,  3,  4,  5,  6,  7,  8,  9
, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19
, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29
, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39
, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49
, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59
, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69
, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79
, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89
, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99
,100,101,102,103,104,105,106,107,108,109
,110,111,112
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s6')
    
    #   Lots of columns in ORDER BYs AND GROUP BYs:
    #   Since B41, get SQLCOMP out of space with full extended segment.
    stmt = """SELECT     a.char_1, a.pic_x_1, a.small_int, a.pic_decimal_3
, b.char_1, b.pic_x_1, b.small_int, b.pic_decimal_3
, c.char_1, c.pic_x_1, c.small_int, c.pic_decimal_3
, d.char_1, d.pic_x_1, d.small_int, d.pic_decimal_3
, e.char_1, e.pic_x_1, e.small_int, e.pic_decimal_3
, f.char_1, f.pic_x_1, f.small_int, f.pic_decimal_3
, g.char_1, g.pic_x_1, g.small_int, g.pic_decimal_3
, h.char_1, h.pic_x_1, h.small_int, h.pic_decimal_3
, i.char_1, i.pic_x_1, i.small_int, i.pic_decimal_3
, j.char_1, j.pic_x_1, j.small_int, j.pic_decimal_3
, k.char_1, k.pic_x_1, k.small_int, k.pic_decimal_3
, l.char_1, l.pic_x_1, l.small_int, l.pic_decimal_3
, m.char_1, m.pic_x_1, m.small_int, m.pic_decimal_3
, n.char_1, n.pic_x_1, n.small_int, n.pic_decimal_3
, o.char_1, o.pic_x_1, o.small_int, o.pic_decimal_3
, p.char_1, p.pic_x_1, p.small_int, p.pic_decimal_3
FROM        """ + gvars.g_schema_arkcasedb + """.btsel01 a
, """ + gvars.g_schema_arkcasedb + """.btsel01 b
, """ + gvars.g_schema_arkcasedb + """.btsel01 c
, """ + gvars.g_schema_arkcasedb + """.btsel01 d
, """ + gvars.g_schema_arkcasedb + """.btsel01 e
, """ + gvars.g_schema_arkcasedb + """.btsel01 f
, """ + gvars.g_schema_arkcasedb + """.btsel01 g
, """ + gvars.g_schema_arkcasedb + """.btsel01 h
, """ + gvars.g_schema_arkcasedb + """.btsel01 i
, """ + gvars.g_schema_arkcasedb + """.btsel01 j
, """ + gvars.g_schema_arkcasedb + """.btsel01 k
, """ + gvars.g_schema_arkcasedb + """.btsel01 l
, """ + gvars.g_schema_arkcasedb + """.btsel01 m
, """ + gvars.g_schema_arkcasedb + """.btsel01 n
, """ + gvars.g_schema_arkcasedb + """.btsel01 o
, """ + gvars.g_schema_arkcasedb + """.btsel01 p
--  Compare columns for all tables:
WHERE     a.pic_x_1            = b.pic_x_1
AND (a.pic_x_1            = c.pic_x_1)
AND (a.pic_x_1            = d.pic_x_1)
AND (a.pic_x_1            = e.pic_x_1)
AND (a.pic_x_1            = f.pic_x_1)
AND (a.pic_x_1            = g.pic_x_1)
AND (a.pic_x_1            = h.pic_x_1)
AND (a.pic_x_1            = i.pic_x_1)
AND (a.pic_x_1            = j.pic_x_1)
AND (a.pic_x_1            = k.pic_x_1)
AND (a.pic_x_1            = l.pic_x_1)
AND (a.pic_x_1            = m.pic_x_1)
AND (a.pic_x_1            = n.pic_x_1)
AND (a.pic_x_1            = o.pic_x_1)
AND (a.pic_x_1            = p.pic_x_1)
--  Compare columns for a:
AND (a.pic_x_1            = 'Z' )
--  ORDER and GROUP BYs for 4 cols for each of 16 tables in the join
--  (i.e. 64 cols):
GROUP BY          a.char_1, a.pic_x_1, a.small_int, a.pic_decimal_3
, b.char_1, b.pic_x_1, b.small_int, b.pic_decimal_3
, c.char_1, c.pic_x_1, c.small_int, c.pic_decimal_3
, d.char_1, d.pic_x_1, d.small_int, d.pic_decimal_3
, e.char_1, e.pic_x_1, e.small_int, e.pic_decimal_3
, f.char_1, f.pic_x_1, f.small_int, f.pic_decimal_3
, g.char_1, g.pic_x_1, g.small_int, g.pic_decimal_3
, h.char_1, h.pic_x_1, h.small_int, h.pic_decimal_3
, i.char_1, i.pic_x_1, i.small_int, i.pic_decimal_3
, j.char_1, j.pic_x_1, j.small_int, j.pic_decimal_3
, k.char_1, k.pic_x_1, k.small_int, k.pic_decimal_3
, l.char_1, l.pic_x_1, l.small_int, l.pic_decimal_3
, m.char_1, m.pic_x_1, m.small_int, m.pic_decimal_3
, n.char_1, n.pic_x_1, n.small_int, n.pic_decimal_3
, o.char_1, o.pic_x_1, o.small_int, o.pic_decimal_3
, p.char_1, p.pic_x_1, p.small_int, p.pic_decimal_3
ORDER BY
1,  2,  3,  4,  5,  6,  7,  8,  9
, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19
, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29
, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39
, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49
, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59
, 60, 61, 62, 63, 64
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s7')
    
    #   More columns in GROUP BY and ORDER BY:
    #   Since B41, get SQLCOMP out of space with full extended segment.
    #   Watch for SQLCOMP abend.
    stmt = """SELECT     a.char_1, a.pic_x_1, a.small_int, a.pic_decimal_3
, a.binary_signed, a.pic_comp_1, a.decimal_1
, b.char_1, b.pic_x_1, b.small_int, b.pic_decimal_3
, b.binary_signed, b.pic_comp_1, b.decimal_1
, c.char_1, c.pic_x_1, c.small_int, c.pic_decimal_3
, c.binary_signed, c.pic_comp_1, c.decimal_1
, d.char_1, d.pic_x_1, d.small_int, d.pic_decimal_3
, d.binary_signed, d.pic_comp_1, d.decimal_1
, e.char_1, e.pic_x_1, e.small_int, e.pic_decimal_3
, e.binary_signed, e.pic_comp_1, e.decimal_1
, f.char_1, f.pic_x_1, f.small_int, f.pic_decimal_3
, f.binary_signed, f.pic_comp_1, f.decimal_1
, g.char_1, g.pic_x_1, g.small_int, g.pic_decimal_3
, g.binary_signed, g.pic_comp_1, g.decimal_1
, h.char_1, h.pic_x_1, h.small_int, h.pic_decimal_3
, h.binary_signed, h.pic_comp_1, h.decimal_1
, i.char_1, i.pic_x_1, i.small_int, i.pic_decimal_3
, i.binary_signed, i.pic_comp_1, i.decimal_1
, j.char_1, j.pic_x_1, j.small_int, j.pic_decimal_3
, j.binary_signed, j.pic_comp_1, j.decimal_1
, k.char_1, k.pic_x_1, k.small_int, k.pic_decimal_3
, k.binary_signed, k.pic_comp_1, k.decimal_1
, l.char_1, l.pic_x_1, l.small_int, l.pic_decimal_3
, l.binary_signed, l.pic_comp_1, l.decimal_1
, m.char_1, m.pic_x_1, m.small_int, m.pic_decimal_3
, m.binary_signed, m.pic_comp_1, m.decimal_1
, n.char_1, n.pic_x_1, n.small_int, n.pic_decimal_3
, n.binary_signed, n.pic_comp_1, n.decimal_1
, o.char_1, o.pic_x_1, o.small_int, o.pic_decimal_3
, o.binary_signed, o.pic_comp_1, o.decimal_1
, p.char_1, p.pic_x_1, p.small_int, p.pic_decimal_3
, p.binary_signed, p.pic_comp_1, p.decimal_1
FROM        """ + gvars.g_schema_arkcasedb + """.btsel01 a
, """ + gvars.g_schema_arkcasedb + """.btsel01 b
, """ + gvars.g_schema_arkcasedb + """.btsel01 c
, """ + gvars.g_schema_arkcasedb + """.btsel01 d
, """ + gvars.g_schema_arkcasedb + """.btsel01 e
, """ + gvars.g_schema_arkcasedb + """.btsel01 f
, """ + gvars.g_schema_arkcasedb + """.btsel01 g
, """ + gvars.g_schema_arkcasedb + """.btsel01 h
, """ + gvars.g_schema_arkcasedb + """.btsel01 i
, """ + gvars.g_schema_arkcasedb + """.btsel01 j
, """ + gvars.g_schema_arkcasedb + """.btsel01 k
, """ + gvars.g_schema_arkcasedb + """.btsel01 l
, """ + gvars.g_schema_arkcasedb + """.btsel01 m
, """ + gvars.g_schema_arkcasedb + """.btsel01 n
, """ + gvars.g_schema_arkcasedb + """.btsel01 o
, """ + gvars.g_schema_arkcasedb + """.btsel01 p
--  Compare columns for all tables:
WHERE     a.pic_x_1            = b.pic_x_1
AND (a.pic_x_1            = c.pic_x_1)
AND (a.pic_x_1            = d.pic_x_1)
AND (a.pic_x_1            = e.pic_x_1)
AND (a.pic_x_1            = f.pic_x_1)
AND (a.pic_x_1            = g.pic_x_1)
AND (a.pic_x_1            = h.pic_x_1)
AND (a.pic_x_1            = i.pic_x_1)
AND (a.pic_x_1            = j.pic_x_1)
AND (a.pic_x_1            = k.pic_x_1)
AND (a.pic_x_1            = l.pic_x_1)
AND (a.pic_x_1            = m.pic_x_1)
AND (a.pic_x_1            = n.pic_x_1)
AND (a.pic_x_1            = o.pic_x_1)
AND (a.pic_x_1            = p.pic_x_1)
--  Compare columns for a:
AND (a.pic_x_1            = 'Z' )
--  ORDER and GROUP BYs for 7 cols for each of 16 tables in the join
--  (i.e. 102 cols):
GROUP BY          a.char_1, a.pic_x_1, a.small_int, a.pic_decimal_3
, a.binary_signed, a.pic_comp_1, a.decimal_1
, b.char_1, b.pic_x_1, b.small_int, b.pic_decimal_3
, b.binary_signed, b.pic_comp_1, b.decimal_1
, c.char_1, c.pic_x_1, c.small_int, c.pic_decimal_3
, c.binary_signed, c.pic_comp_1, c.decimal_1
, d.char_1, d.pic_x_1, d.small_int, d.pic_decimal_3
, d.binary_signed, d.pic_comp_1, d.decimal_1
, e.char_1, e.pic_x_1, e.small_int, e.pic_decimal_3
, e.binary_signed, e.pic_comp_1, e.decimal_1
, f.char_1, f.pic_x_1, f.small_int, f.pic_decimal_3
, f.binary_signed, f.pic_comp_1, f.decimal_1
, g.char_1, g.pic_x_1, g.small_int, g.pic_decimal_3
, g.binary_signed, g.pic_comp_1, g.decimal_1
, h.char_1, h.pic_x_1, h.small_int, h.pic_decimal_3
, h.binary_signed, h.pic_comp_1, h.decimal_1
, i.char_1, i.pic_x_1, i.small_int, i.pic_decimal_3
, i.binary_signed, i.pic_comp_1, i.decimal_1
, j.char_1, j.pic_x_1, j.small_int, j.pic_decimal_3
, j.binary_signed, j.pic_comp_1, j.decimal_1
, k.char_1, k.pic_x_1, k.small_int, k.pic_decimal_3
, k.binary_signed, k.pic_comp_1, k.decimal_1
, l.char_1, l.pic_x_1, l.small_int, l.pic_decimal_3
, l.binary_signed, l.pic_comp_1, l.decimal_1
, m.char_1, m.pic_x_1, m.small_int, m.pic_decimal_3
, m.binary_signed, m.pic_comp_1, m.decimal_1
, n.char_1, n.pic_x_1, n.small_int, n.pic_decimal_3
, n.binary_signed, n.pic_comp_1, n.decimal_1
, o.char_1, o.pic_x_1, o.small_int, o.pic_decimal_3
, o.binary_signed, o.pic_comp_1, o.decimal_1
, p.char_1, p.pic_x_1, p.small_int, p.pic_decimal_3
, p.binary_signed, p.pic_comp_1, p.decimal_1
ORDER BY
1,  2,  3,  4,  5,  6,  7,  8,  9
, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19
, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29
, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39
, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49
, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59
, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69
, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79
, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89
, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99
,100,101,102,103,104,105,106,107,108,109
,110,111,112
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s8')
    
    _testmgr.testcase_end(desc)

def test007(desc="""a07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0110 : A07
    #  Description:        This test verifies thefollowing SQL
    #                      feature.
    #                      Large number of access paths in all
    #                      tables referenced created by multiple
    #                      indices (normalizer stores totals).
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    #
    # ---------------------------------
    # Create the Log file.
    # ---------------------------------
    # ---------------------------------
    # Set up default catalog and schema
    # ---------------------------------
    #set catalog eval;
    #set schema  eval.gdb;
    #
    #
    #  Get to the volume where the catalog is, to avoid multiple
    #  volume specifications:
    #  VOLUME <subvol_for_temporary_data>;
    
    # Copy global table to local version and add lots of indices:
    #    DUP btsel01, L6table
    #    CATALOG <subvol_for_temporary_data>;
    
    stmt = """create table L6table (
-- --Fixed length character string
char_1                 char(1)        default ' ' not null
, char_10                char(10)       default ' ' not null
, pic_x_1                pic x(1)       default ' ' not null
, pic_x_7                pic x(7)       default ' ' not null
, pic_x_long             picture x(200) default ' ' not null
--                                pic x(200)     not null
-- --Varying length character string.
, var_char               varchar(253)   default ' ' not null
-- --Binary
, binary_signed          numeric (4,0) signed    default 0 not null
, binary_32_u            numeric (9,2) unsigned  default 0 not null
, binary_64_s            numeric (18,3) signed   default 0 not null
, pic_comp_1             numeric (10,0) signed   default 0 not null
, pic_comp_2             numeric (2,2)  signed   default 0 not null
, pic_comp_3             numeric (8,5)  signed   default 0 not null    

, small_int              smallint                default 0 not null
, medium_int             integer unsigned        default 0 not null
, large_int              largeint signed         default 0 not null
-- --Fixed length character string
, decimal_1              decimal (1,0) unsigned  default 0 not null
, decimal_2_signed       decimal (2,2) signed    default 0 not null
, decimal_3_unsigned     decimal (3,0) unsigned  default 0 not null
, pic_decimal_1          pic s9(1)v9(1)          default 0 not null
--                                numeric (2,1) signed   not null
, pic_decimal_2          picture v9(3)          default 0 not null
--                                numeric (3,3) unsigned not null
, pic_decimal_3          pic s9                 default 0 not null
--                                numeric (1,0) signed   not null
-- --End of columns
, primary key  ( binary_signed )
)
location """ + gvars.g_disc5 + """
store by primary key
attributes
--         audit
blocksize 4096
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # --Index the table with simple, 1-column indexes:
    stmt = """create index L6tablea on L6table ( pic_x_1 )
location """ + gvars.g_disc4 + """
attributes blocksize 4096
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index L6tableb on L6table ( decimal_2_signed )
location """ + gvars.g_disc3 + """
attributes blocksize 4096
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index L6tablec on L6table ( pic_comp_3 )
location """ + gvars.g_disc2 + """
attributes blocksize 4096
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index L6tabled on L6table ( pic_x_long )
location """ + gvars.g_disc1 + """
attributes blocksize 4096
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #
    
    # These indexes are created, but never used, not sure why created
    # Table L6table is similar to btsel01, maybe everything was copied
    
    # -- Make 25 indexes:
    stmt = """CREATE INDEX L6indexa ON L6table ( char_1  );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexb ON L6table ( char_10 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexc ON L6table ( pic_x_1 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexd ON L6table ( pic_x_7 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexe ON L6table ( pic_x_long );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  Var_char is too long to be an index.
    stmt = """CREATE INDEX L6indexf ON L6table ( var_char );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexg ON L6table ( binary_signed );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexh ON L6table ( binary_32_u   );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexi ON L6table ( binary_64_s   );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexj ON L6table ( pic_comp_1    );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexk ON L6table ( pic_comp_2    );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexl ON L6table ( pic_comp_3    );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexm ON L6table ( small_int     );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexn ON L6table ( medium_int    );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexo ON L6table ( large_int     );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexp ON L6table ( decimal_1     );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexq ON L6table ( decimal_2_signed );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexr ON L6table ( decimal_3_unsigned );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexs ON L6table ( pic_decimal_1 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indext ON L6table ( pic_decimal_2 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexu ON L6table ( pic_decimal_3 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexv ON L6table ( pic_decimal_3 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexw ON L6table ( pic_decimal_3 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexx ON L6table ( pic_decimal_3 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexy ON L6table ( pic_decimal_3 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexz ON L6table ( pic_decimal_3 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #DUP btsel01, L6table;
    #
    stmt = """insert into L6table values ('A','steven','C','walter','bob',
'B',50,50,200,50,0.12,100.9,
10,10000,1000000000,4,.5,90,
1.1,0.1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into L6table values ('A','bobby','A','bobby','bop',
'B',60,60,1200,60,0.79,100.99,
1000,8000,-1000,5,.6,100,
2.1,0.2,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into L6table values ('D','steven','B','9','bat','thomas',
8000,70,2000,500,0.10,100.999,
90,10000,1000,7,.7,110,
3.1,0.3,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into L6table values ('D','melissa','C','7','pop','jimmy',
1000,80,1500,500,0.20,100.9999,
80,9000,999,5,.8,120,
4.1,0.4,4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into L6table values ('E','monica','Q','sue','pat',
'christopher',
2000,90,1200,3000,0.30,100.99999,
2000,8000,-1000000,1,.9,80,
5.1,0.5,5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into L6table values ('D','michelle','D','michael','rat',
'thomas',
-5000,90,2000,500,0.40,100.8,
90,8000,200,7,.93,140,
6.1,0.6,6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into L6table values ('C','maureen','E','jimmy','rum',
'marilyn',
3000,80,2000,500,0.50,100.7,
9000,1000,2000,8,.97,150,
7.1, 0.7,7);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into L6table values ('C','marcia','Z','johnny','dum',
'thomas',
4000,40,2000,50,0.60,100.6,
8000,5000,0,9,.99,110,
8.1,0.8,8);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #   Lots of PREDICATEs (21) involving 2 tables.
    stmt = """SELECT a.char_1, b.char_10
FROM L6table a
, L6table b
--  Compare columns for a and b:
WHERE a.char_1             = b.char_1
AND ( a.char_10            = b.char_10            )
AND ( a.pic_x_1            = b.pic_x_1            )
AND ( a.pic_x_7            = b.pic_x_7            )
AND ( a.pic_x_long         = b.pic_x_long         )
AND ( a.var_char           = b.var_char           )
AND ( a.binary_signed      = b.binary_signed      )
AND ( a.binary_32_u        = b.binary_32_u        )
AND ( a.binary_64_s        = b.binary_64_s        )
AND ( a.pic_comp_1         = b.pic_comp_1         )
AND ( a.pic_comp_2         = b.pic_comp_2         )
AND ( a.pic_comp_3         = b.pic_comp_3         )
AND ( a.small_int          = b.small_int          )
AND ( a.medium_int         = b.medium_int         )
AND ( a.large_int          = b.large_int          )
AND ( a.decimal_1          = b.decimal_1          )
AND ( a.decimal_2_signed   = b.decimal_2_signed   )
AND ( a.decimal_3_unsigned = b.decimal_3_unsigned )
AND ( a.pic_decimal_1      = b.pic_decimal_1      )
AND ( a.pic_decimal_2      = b.pic_decimal_2      )
AND ( a.pic_decimal_3      = b.pic_decimal_3      )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s0')
    
    #   Lots of PREDICATEs (63) involving 3 tables:
    stmt = """SELECT a.char_1, b.char_10, c.char_1
FROM L6table a
, L6table b
, L6table c
--  Compare columns for a and b:
WHERE a.char_1             = b.char_1
AND ( a.char_10            = b.char_10            )
AND ( a.pic_x_1            = b.pic_x_1            )
AND ( a.pic_x_7            = b.pic_x_7            )
AND ( a.pic_x_long         = b.pic_x_long         )
AND ( a.var_char           = b.var_char           )
AND ( a.binary_signed      = b.binary_signed      )
AND ( a.binary_32_u        = b.binary_32_u        )
AND ( a.binary_64_s        = b.binary_64_s        )
AND ( a.pic_comp_1         = b.pic_comp_1         )
AND ( a.pic_comp_2         = b.pic_comp_2         )
AND ( a.pic_comp_3         = b.pic_comp_3         )
AND ( a.small_int          = b.small_int          )
AND ( a.medium_int         = b.medium_int         )
AND ( a.large_int          = b.large_int          )
AND ( a.decimal_1          = b.decimal_1          )
AND ( a.decimal_2_signed   = b.decimal_2_signed   )
AND ( a.decimal_3_unsigned = b.decimal_3_unsigned )
AND ( a.pic_decimal_1      = b.pic_decimal_1      )
AND ( a.pic_decimal_2      = b.pic_decimal_2      )
AND ( a.pic_decimal_3      = b.pic_decimal_3      )
--  Compare columns for a and c:
AND ( a.char_1             = c.char_1             )
AND ( a.char_10            = c.char_10            )
AND ( a.pic_x_1            = c.pic_x_1            )
AND ( a.pic_x_7            = c.pic_x_7            )
AND ( a.pic_x_long         = c.pic_x_long         )
AND ( a.var_char           = c.var_char           )
AND ( a.binary_signed      = c.binary_signed      )
AND ( a.binary_32_u        = c.binary_32_u        )
AND ( a.binary_64_s        = c.binary_64_s        )
AND ( a.pic_comp_1         = c.pic_comp_1         )
AND ( a.pic_comp_2         = c.pic_comp_2         )
AND ( a.pic_comp_3         = c.pic_comp_3         )
AND ( a.small_int          = c.small_int          )
AND ( a.medium_int         = c.medium_int         )
AND ( a.large_int          = c.large_int          )
AND ( a.decimal_1          = c.decimal_1          )
AND ( a.decimal_2_signed   = c.decimal_2_signed   )
AND ( a.decimal_3_unsigned = c.decimal_3_unsigned )
AND ( a.pic_decimal_1      = c.pic_decimal_1      )
AND ( a.pic_decimal_2      = c.pic_decimal_2      )
AND ( a.pic_decimal_3      = c.pic_decimal_3      )
--  Compare columns for b and c:
AND ( b.char_1             = c.char_1             )
AND ( b.char_10            = c.char_10            )
AND ( b.pic_x_1            = c.pic_x_1            )
AND ( b.pic_x_7            = c.pic_x_7            )
AND ( b.pic_x_long         = c.pic_x_long         )
AND ( b.var_char           = c.var_char           )
AND ( b.binary_signed      = c.binary_signed      )
AND ( b.binary_32_u        = c.binary_32_u        )
AND ( b.binary_64_s        = c.binary_64_s        )
AND ( b.pic_comp_1         = c.pic_comp_1         )
AND ( b.pic_comp_2         = c.pic_comp_2         )
AND ( b.pic_comp_3         = c.pic_comp_3         )
AND ( b.small_int          = c.small_int          )
AND ( b.medium_int         = c.medium_int         )
AND ( b.large_int          = c.large_int          )
AND ( b.decimal_1          = c.decimal_1          )
AND ( b.decimal_2_signed   = c.decimal_2_signed   )
AND ( b.decimal_3_unsigned = c.decimal_3_unsigned )
AND ( b.pic_decimal_1      = c.pic_decimal_1      )
AND ( b.pic_decimal_2      = c.pic_decimal_2      )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s1')
    
    stmt = """DROP table L6table;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test008(desc="""a08"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0110 : A08
    #  Description:        This test verifies the following SQL
    #                      feature.
    #                      Test over/under flow conditions using
    #                      descending index
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    stmt = """CREATE TABLE mkey1 (a int, b int, c int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into mkey1 values ( 1, 1, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 1, 1, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 1, 1, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 1, 1, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 1, 1, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 1, 1, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 1, 2, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 1, 2, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 1, 2, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 1, 2, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 1, 2, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 1, 2, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 1, 3, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 1, 3, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 1, 3, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 1, 3, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 1, 3, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 1, 3, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 1, 4, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 1, 4, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 1, 4, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 1, 4, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 1, 4, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 1, 4, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 1, 5, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 1, 5, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 1, 5, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 1, 5, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 1, 5, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 1, 5, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 1, null, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 1, null, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 1, null, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 1, null, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 1, null, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 1, null, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into mkey1 values ( 2, 1, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 2, 1, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 2, 1, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 2, 1, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 2, 1, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 2, 1, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 2, 2, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 2, 2, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 2, 2, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 2, 2, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 2, 2, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 2, 2, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 2, 3, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 2, 3, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 2, 3, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 2, 3, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 2, 3, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 2, 3, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 2, 4, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 2, 4, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 2, 4, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 2, 4, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 2, 4, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 2, 4, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 2, 5, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 2, 5, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 2, 5, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 2, 5, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 2, 5, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 2, 5, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 2, null, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 2, null, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 2, null, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 2, null, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 2, null, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 2, null, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into mkey1 values ( 3, 1, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 3, 1, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 3, 1, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 3, 1, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 3, 1, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 3, 1, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 3, 2, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 3, 2, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 3, 2, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 3, 2, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 3, 2, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 3, 2, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 3, 3, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 3, 3, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 3, 3, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 3, 3, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 3, 3, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 3, 3, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 3, 4, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 3, 4, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 3, 4, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 3, 4, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 3, 4, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 3, 4, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 3, 5, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 3, 5, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 3, 5, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 3, 5, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 3, 5, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 3, 5, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 3, null, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 3, null, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 3, null, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 3, null, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 3, null, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 3, null, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into mkey1 values ( 4, 1, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 4, 1, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 4, 1, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 4, 1, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 4, 1, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 4, 1, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 4, 2, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 4, 2, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 4, 2, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 4, 2, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 4, 2, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 4, 2, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 4, 3, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 4, 3, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 4, 3, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 4, 3, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 4, 3, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 4, 3, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 4, 4, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 4, 4, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 4, 4, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 4, 4, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 4, 4, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 4, 4, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 4, 5, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 4, 5, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 4, 5, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 4, 5, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 4, 5, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 4, 5, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 4, null, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 4, null, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 4, null, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 4, null, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 4, null, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 4, null, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into mkey1 values ( 5, 1, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 5, 1, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 5, 1, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 5, 1, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 5, 1, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 5, 1, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 5, 2, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 5, 2, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 5, 2, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 5, 2, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 5, 2, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 5, 2, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 5, 3, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 5, 3, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 5, 3, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 5, 3, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 5, 3, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 5, 3, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 5, 4, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 5, 4, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 5, 4, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 5, 4, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 5, 4, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 5, 4, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 5, 5, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 5, 5, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 5, 5, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 5, 5, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 5, 5, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 5, 5, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 5, null, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 5, null, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 5, null, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 5, null, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 5, null, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( 5, null, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into mkey1 values ( null, 1, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( null, 1, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( null, 1, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( null, 1, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( null, 1, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( null, 1, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( null, 2, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( null, 2, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( null, 2, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( null, 2, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( null, 2, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( null, 2, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( null, 3, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( null, 3, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( null, 3, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( null, 3, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( null, 3, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( null, 3, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( null, 4, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( null, 4, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( null, 4, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( null, 4, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( null, 4, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( null, 4, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( null, 5, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( null, 5, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( null, 5, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( null, 5, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( null, 5, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( null, 5, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( null, null, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( null, null, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( null, null, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( null, null, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( null, null, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into mkey1 values ( null, null, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """prepare pp from
select a,b,c from mkey1 
where a,b,c>4,4,4 and a,b,c<5,1,1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # don't compare plan, numbers change too frequently (kk)
    stmt = """select  SEQ_NUM, OPERATOR, TOTAL_COST
from table (explain (null, 'PP'));"""
    output = _dci.cmdexec(stmt)
    
    #  Execute the select. Every predicate is a DP2 pred.
    #  The last row should not be part of the output.
    #  Note: a pred like (4, ?, 5) > (4, 4, 4) evaluates to null.
    stmt = """select a,b,c from mkey1 
where a,b,c>4,4,4 and a,b,c<5,1,1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s1')
    
    #  Remove the last member of the OR.
    stmt = """select a,b,c from mkey1 where
(a>4 or (a=4 and b>4))
and a,b,c<5,1,1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s2')
    
    #  Doing a select including the last member of the OR should work
    stmt = """select a,b,c from mkey1 where a=4 and b=4 and c>4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s3')
    
    #  So a UNION ALL of the above two queries should produce
    #  the same result as the earlier EXPLAINed select
    stmt = """select a,b,c from mkey1 where
(a>4 or (a=4 and b>4))
and a,b,c<5,1,1
union all
select a,b,c from mkey1 where a=4 and b=4 and c>4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s4')
    
    # To test over/under flow condition you need additional tables that
    # contain some values that are the max or min for their datatype and
    # an index on one that is descending on the column where the first
    # inequality appears.
    
    stmt = """CREATE TABLE mkey10a(a smallint unsigned,
b smallint unsigned,
c smallint unsigned) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into mkey10a select a,b,c-1 from mkey1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 216)
    stmt = """insert into mkey10a select a,b,65536-c from mkey1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 216)
    
    stmt = """drop table mkey10d;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table mkey10d(a smallint unsigned,
b smallint unsigned,
c smallint unsigned) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into mkey10d select a,b,c-1 from mkey1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 216)
    stmt = """insert into mkey10d select a,b,65536-c from mkey1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 216)
    
    # Tables MKEY10A and MKEY10D have the same data but one has a
    # descending index and the other has an ascending index
    # Create indices on these tables
    stmt = """create index mkey10ai on mkey10a(a, b, c);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index mkey10di on mkey10d(a desc, b desc, c desc);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  The DML:
    #  All of the following queries should return 10 rows
    stmt = """select * from mkey10a where a,b=3,3 and c>= -3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s6')
    
    stmt = """select * from mkey10d where a,b=3,3 and c>= -3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s7')
    
    stmt = """select * from mkey10a where a,b=3,3 and c>= -3 order by a desc, b
desc, c desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s8')
    
    stmt = """select * from mkey10d where a,b=3,3 and c>= -3 order by
a, b, c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s9')
    
    stmt = """select * from mkey10a where a,b=3,3 and c<= 65536;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s10')
    
    stmt = """select * from mkey10d where a,b=3,3 and c<= 65536;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s11')
    
    stmt = """select * from mkey10a where a,b=3,3 and c<= 65536
order by a desc, b desc, c desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s12')
    
    stmt = """select * from mkey10d where a,b=3,3 and c<= 65536
order by a, b, c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s13')
    
    stmt = """drop table mkey1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table mkey10a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table mkey10d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test009(desc="""a09"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # ---------------------------------
    # Set up default catalog and schema
    # ---------------------------------
    #  Get to the volume where the catalog is, to avoid multiple
    #  volume specifications:
    #  VOLUME $SUBVOL_FOR_TEMPORARY_DATA;
    #
    # Copy global tables to local versions on which to create views:
    #   DUP btsel01, l8tablea
    #       CATALOG $SUBVOL_FOR_TEMPORARY_DATA;
    #   DUP btsel13, l8tableb
    #       CATALOG $SUBVOL_FOR_TEMPORARY_DATA;
    #   DUP btsel13, l8tablec
    #       CATALOG $SUBVOL_FOR_TEMPORARY_DATA;
    #
    #
    stmt = """CREATE TABLE l8tablea (
-- Fixed length character string
char_1                 CHAR(1)    not null
, char_10                CHAR(10)   not null
, pic_x_1                PIC X(1)   not null
, pic_x_7                PIC X(7)   not null
, pic_x_long             PIC X(200) not null
-- Varying length character string.
, var_char               VARCHAR(253)  not null    

-- Binary
, binary_signed          numeric (4,0) signed not null
, binary_32_u            numeric (9,2) UNSIGNED not null
, binary_64_s            numeric (18,3) SIGNED  not null
, pic_comp_1             numeric(10,0) signed   not null
, pic_comp_2             numeric(2,2) signed    not null
, pic_comp_3             numeric(8,5) signed    not null
, small_int              SMALLINT               not null
, medium_int             INTEGER UNSIGNED       not null
,large_in                LARGEINT               not null
, decimal_1              DECIMAL (1, 0)         not null
, decimal_2_signed       DECIMAL (2,2) SIGNED   not null
, decimal_3_unsigned     DECIMAL (3,0) UNSIGNED not null
, pic_decimal_1          decimal(2,1) not null
, pic_decimal_2          DECIMAL(3,3) signed not null
, pic_decimal_3          DECIMAL(1,0) signed not null
, PRIMARY KEY (binary_signed)
-- End of columns
)
-- Physical specs
attribute
blocksize 4096    

;"""
    output = _dci.cmdexec(stmt)
    
    # Index the table with simple, 1-column indexes:
    stmt = """CREATE INDEX l8tableaa ON l8tablea ( pic_x_1 );"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE INDEX l8tableab ON l8tablea ( decimal_2_signed );"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE INDEX l8tableac ON l8tablea ( pic_comp_3 );"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE INDEX l8tablead ON l8tablea ( pic_x_long );"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into l8tablea values ('A','steven','C','walter','bob',
'B',50,50,200,50,0.12,100.9,
10,10000,1000000000,4,.5,90,
1.1,0.1,1);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into l8tablea values ('A','bobby','A','bobby','bop',
'B',60,60,1200,60,0.79,100.99,
1000,8000,-1000,5,.6,100,
2.1,0.2,2);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into l8tablea values ('D','steven','B','9','bat','thomas',
8000,70,2000,500,0.10,100.999,
90,10000,1000,7,.7,110,
3.1,0.3,3);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into l8tablea values ('D','melissa','C','7','pop','jimmy',
1000,80,1500,500,0.20,100.9999,
80,9000,999,5,.8,120,
4.1,0.4,4);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into l8tablea values ('E','monica','Q','sue','pat',
'christopher',
2000,90,1200,3000,0.30,100.99999,
2000,8000,-1000000,1,.9,80,
5.1,0.5,5);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into l8tablea values ('D','michelle','D','michael','rat',
'thomas',
-5000,90,2000,500,0.40,100.8,
90,8000,200,7,.93,140,
6.1,0.6,6);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into l8tablea values ('C','maureen','E','jimmy','rum',
'marilyn',
3000,80,2000,500,0.50,100.7,
9000,1000,2000,8,.97,150,
7.1, 0.7,7);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into l8tablea values ('C','marcia','Z','johnny','dum',
'thomas',
4000,40,2000,50,0.60,100.6,
8000,5000,0,9,.99,110,
8.1,0.8,8);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from l8tablea;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE l8tableb (
data_93                PIC 9(3)               not null
, PRIMARY KEY ( data_93 )
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into l8tableb values (100);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into l8tableb values (200);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into l8tableb values (250);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into l8tableb values (350);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into l8tableb values (450);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into l8tableb values (550);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into l8tableb values (650);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into l8tableb values (750);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from l8tableb;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE l8tablec (
data_93                PIC 9(3)               not null
, PRIMARY KEY ( data_93 )
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into l8tablec values (100);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into l8tablec values (200);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into l8tablec values (250);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into l8tablec values (350);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into l8tablec values (450);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into l8tablec values (550);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into l8tablec values (650);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into l8tablec values (750);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from l8tablec;"""
    output = _dci.cmdexec(stmt)
    
    #-- DDL-- CREATE one set of VIEWs:
    stmt = """create view l8view21 as select data_93 from l8tableb;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view l8view22 as select v.data_93
from l8view21 v, l8tableb t where t.data_93=v.data_93;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view l8view23 as select v.data_93
from l8view22 v, l8tableb t where t.data_93=v.data_93;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view l8view24 as select v.data_93
from l8view23 v, l8tableb t where t.data_93=v.data_93;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view l8view25 as select v.data_93
from l8view24 v, l8tableb t where t.data_93=v.data_93;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view l8view26 as select v.data_93
from l8view25 v, l8tableb t where t.data_93=v.data_93;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view l8view27 as select v.data_93
from l8view26 v, l8tableb t where t.data_93=v.data_93;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view l8view28 as select v.data_93
from l8view27 v, l8tableb t where t.data_93=v.data_93;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view l8view29 as select v.data_93
from l8view28 v, l8tableb t where t.data_93=v.data_93;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view l8view30 as select v.data_93
from l8view29 v, l8tableb t where t.data_93=v.data_93;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view l8view31 as select v.data_93
from l8view30 v, l8tableb t where t.data_93=v.data_93;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view l8view32 as select v.data_93
from l8view31 v, l8tableb t where t.data_93=v.data_93;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view l8view33 as select v.data_93
from l8view32 v, l8tableb t where t.data_93=v.data_93;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view l8view34 as select v.data_93
from l8view33 v, l8tableb t where t.data_93=v.data_93;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view l8view35 as select v.data_93
from l8view34 v, l8tableb t where t.data_93=v.data_93;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view l8view36 as select v.data_93
from l8view35 v, l8tableb t where t.data_93=v.data_93;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view l8view37 as select v.data_93
from l8view36 v, l8tableb t where t.data_93=v.data_93;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view l8view38 as select v.data_93
from l8view37 v, l8tableb t where t.data_93=v.data_93;"""
    output = _dci.cmdexec(stmt)
    
    #-- DDL -- CREATE another set of VIEWs:
    stmt = """create view l8view01 as select char_1, pic_x_7 from l8tablea;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view l8view02 as select v.char_1,t.pic_x_7
from l8view01 v, l8tablea t where t.pic_x_7=v.pic_x_7;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view l8view03 as select v.char_1,t.pic_x_7
from l8view02 v, l8tablea t where t.pic_x_7=v.pic_x_7;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view l8view04 as select v.char_1,t.pic_x_7
from l8view03 v, l8tablea t where t.pic_x_7=v.pic_x_7;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view l8view05 as select v.char_1,t.pic_x_7
from l8view04 v, l8tablea t where t.pic_x_7=v.pic_x_7;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view l8view06 as select v.char_1,t.pic_x_7
from l8view05 v, l8tablea t where t.pic_x_7=v.pic_x_7;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view l8view07 as select v.char_1,t.pic_x_7
from l8view06 v, l8tablea t where t.pic_x_7=v.pic_x_7;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view l8view08 as select v.char_1,t.pic_x_7
from l8view07 v, l8tablea t where t.pic_x_7=v.pic_x_7;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view l8view09 as select v.char_1,t.pic_x_7
from l8view08 v, l8tablea t where t.pic_x_7=v.pic_x_7;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view l8view10 as select v.char_1,t.pic_x_7
from l8view09 v, l8tablea t where t.pic_x_7=v.pic_x_7;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view l8view11 as select v.char_1,t.pic_x_7
from l8view10 v, l8tablea t where t.pic_x_7=v.pic_x_7;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view l8view12 as select v.char_1,t.pic_x_7
from l8view11 v, l8tablea t where t.pic_x_7=v.pic_x_7;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view l8view13 as select v.char_1,t.pic_x_7
from l8view12 v, l8tablea t where t.pic_x_7=v.pic_x_7;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view l8view14 as select v.char_1,t.pic_x_7
from l8view13 v, l8tablea t where t.pic_x_7=v.pic_x_7;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view l8view15 as select v.char_1,t.pic_x_7
from l8view14 v, l8tablea t where t.pic_x_7=v.pic_x_7;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view l8view16 as select v.char_1,t.pic_x_7
from l8view15 v, l8tablea t where t.pic_x_7=v.pic_x_7;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view l8view17 as select v.char_1,t.pic_x_7
from l8view16 v, l8tablea t where t.pic_x_7=v.pic_x_7;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view l8view18 as select v.char_1,t.pic_x_7
from l8view17 v, l8tablea t where t.pic_x_7=v.pic_x_7;"""
    output = _dci.cmdexec(stmt)
    
    #-- DDL -- CREATE another set of VIEWs:
    stmt = """create view k8view01 as select char_1, pic_x_7 from l8tablea;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view k8view02 as select v.char_1,t.pic_x_7
from k8view01 v, l8tablea t where t.pic_x_7=v.pic_x_7;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view k8view03 as select v.char_1,t.pic_x_7
from k8view02 v, l8tablea t where t.pic_x_7=v.pic_x_7;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view k8view04 as select v.char_1,t.pic_x_7
from k8view03 v, l8tablea t where t.pic_x_7=v.pic_x_7;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view k8view05 as select v.char_1,t.pic_x_7
from k8view04 v, l8tablea t where t.pic_x_7=v.pic_x_7;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view k8view06 as select v.char_1,t.pic_x_7
from k8view05 v, l8tablea t where t.pic_x_7=v.pic_x_7;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view k8view07 as select v.char_1,t.pic_x_7
from k8view06 v, l8tablea t where t.pic_x_7=v.pic_x_7;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view k8view08 as select v.char_1,t.pic_x_7
from k8view07 v, l8tablea t where t.pic_x_7=v.pic_x_7;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view k8view09 as select v.char_1,t.pic_x_7
from k8view08 v, l8tablea t where t.pic_x_7=v.pic_x_7;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view k8view10 as select v.char_1,t.pic_x_7
from k8view09 v, l8tablea t where t.pic_x_7=v.pic_x_7;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view k8view11 as select v.char_1,t.pic_x_7
from k8view10 v, l8tablea t where t.pic_x_7=v.pic_x_7;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view k8view12 as select v.char_1,t.pic_x_7
from k8view11 v, l8tablea t where t.pic_x_7=v.pic_x_7;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view k8view13 as select v.char_1,t.pic_x_7
from k8view12 v, l8tablea t where t.pic_x_7=v.pic_x_7;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view k8view14 as select v.char_1,t.pic_x_7
from k8view13 v, l8tablea t where t.pic_x_7=v.pic_x_7;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view k8view15 as select v.char_1,t.pic_x_7
from k8view14 v, l8tablea t where t.pic_x_7=v.pic_x_7;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view k8view16 as select v.char_1,t.pic_x_7
from k8view15 v, l8tablea t where t.pic_x_7=v.pic_x_7;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view k8view17 as select v.char_1,t.pic_x_7
from k8view16 v, l8tablea t where t.pic_x_7=v.pic_x_7;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view k8view18 as select v.char_1,t.pic_x_7
from k8view17 v, l8tablea t where t.pic_x_7=v.pic_x_7;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """ALTER TABLE l8tablec 
ATTRIBUTE NO AUDIT ;"""
    output = _dci.cmdexec(stmt)
    
    #-- ---------------------------------
    #-- Close the Log file.
    #-- ---------------------------------
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0110 : A09
    #  Description:        This test verifies the following SQL
    #                      feature.
    #                      Views with deep nesting (views on views)
    #                      (Test DML, DCL, DDL)
    #                      Tests limits of view composition.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    #
    #  ---------------------------------
    #  Create the Log file.
    #  ---------------------------------
    #  ---------------------------------
    #  Set up default catalog and schema
    #  ---------------------------------
    # set catalog eval;
    # set schema  eval.gdb;
    #  ---------------------------------
    
    #   Get to the volume where the catalog is, to avoid multiple
    #   volume specifications:
    #   VOLUME <subvol_for_temporary_data>;
    
    #  Copy global tables to local versions on which to create views:
    #     DUP btsel01, l8tablea
    #        CATALOG <subvol_for_temporary_data>;
    #      DUP btsel13, l8tableb
    #        CATALOG <subvol_for_temporary_data>;
    
    #  DDL-- CREATE one set of VIEWs:
    
    stmt = """select * from l8view21;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s0')
    stmt = """select * from l8view22;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s1')
    stmt = """select * from l8view23;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s2')
    stmt = """select * from l8view24;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s3')
    stmt = """select * from l8view25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s4')
    stmt = """select * from l8view26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s5')
    stmt = """select * from l8view27;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s6')
    stmt = """select * from l8view28;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s7')
    stmt = """select * from l8view29;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s8')
    stmt = """select * from l8view30;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s9')
    stmt = """select * from l8view31;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s10')
    stmt = """select * from l8view32;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s11')
    stmt = """select * from l8view33;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s12')
    stmt = """select * from l8view34;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s13')
    stmt = """select * from l8view35;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s14')
    stmt = """select * from l8view36;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s15')
    stmt = """select * from l8view37;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s16')
    stmt = """select * from l8view38;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s17')
    
    #  DDL -- CREATE another set of VIEWs:
    stmt = """select * from l8view10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s18')
    stmt = """select * from l8view11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s19')
    stmt = """select * from l8view12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s20')
    stmt = """select * from l8view13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s21')
    stmt = """select * from l8view14;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s22')
    stmt = """select * from l8view15;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s23')
    stmt = """select * from l8view16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s24')
    stmt = """select * from l8view17;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s25')
    stmt = """select * from l8view18;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s26')
    
    #  DDL --  CREATE a CONSTRAINT:
    #   Tested in other test units; not tested here as CONSTRAINTS not
    #   allowed on shorthand views.
    
    #   DML - DELETE:
    #   Tested in other test units; not tested here as DELETE not
    #   allowed on shorthand views.
    
    #   DML - INSERT:
    #   Tested in other test units; not tested here as INSERT not
    #   allowed on shorthand views.
    
    #   DML - UPDATE:
    #   Tested in other test units; not tested here as UPDATE not
    #   allowed on shorthand views.
    
    #   DCL - CONTROL TABLE statements; set up for later SELECT
    #    CONTROL TABLE * TIMEOUT 100 ;
    #    CONTROL TABLE l8view15 TABLELOCK ON ;
    #    CONTROL TABLE l8view32 TABLELOCK ON ;
    
    #   DML - SELECT:
    #   access what you controlled:
    # 04/09/09 added order by
    stmt = """SELECT * FROM l8view14  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s27')
    stmt = """SELECT * FROM l8view15  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s28')
    stmt = """SELECT * FROM l8view31 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s29')
    stmt = """SELECT * FROM l8view32 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s30')
    
    #  Let's have one unaudited table, Created 18tablec:
    stmt = """ALTER TABLE l8tablea 
ATTRIBUTE NO AUDIT ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3070')
    #  Must be in a transaction to lock audited tables:
    stmt = """BEGIN WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """LOCK TABLE k8view14 in share mode ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """LOCK TABLE k8view16 in share mode ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """LOCK TABLE l8view31 in exclusive mode ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """LOCK TABLE l8view35 in exclusive mode ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """LOCK TABLE l8view37 in exclusive mode ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """SELECT * FROM l8view15 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s36')
    stmt = """SELECT * FROM l8view32 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s37')
    #   DCL - UNLOCK:
    #   Only affects unaudited tables.
    stmt = """UNLOCK TABLE k8view14 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """UNLOCK TABLE k8view16 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """UNLOCK TABLE l8view31 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """UNLOCK TABLE l8view35 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """UNLOCK TABLE l8view37 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """COMMIT WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """ALTER TABLE l8tablea 
ATTRIBUTE AUDIT ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3070')
    
    #-- -- DDL-- DROP one set of VIEWs. Needed only for ARK
    #-- --    -- In MP drop table drops associated views also.
    #-- Note: have to drop in reverse order of how created!
    stmt = """drop view l8view38 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view l8view37 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view l8view36 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view l8view35 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view l8view34 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view l8view33 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view l8view32 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view l8view31 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view l8view30 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view l8view29 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view l8view28 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view l8view27 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view l8view26 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view l8view25 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view l8view24 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view l8view23 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view l8view22 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view l8view21 ;"""
    output = _dci.cmdexec(stmt)
    
    #-- DDL -- Drop another set of VIEWs:
    #--- Note: have to drop in reverse order of how created!
    stmt = """drop view l8view18 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view l8view17 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view l8view16 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view l8view15 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view l8view14 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view l8view13 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view l8view12 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view l8view11 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view l8view10 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view l8view09 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view l8view08 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view l8view07 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view l8view06 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view l8view05 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view l8view04 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view l8view03 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view l8view02 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view l8view01 ;"""
    output = _dci.cmdexec(stmt)
    
    #-- DDL -- Drop another set of VIEWs:
    #-- Note: have to drop in reverse order of how created!
    stmt = """drop view k8view18 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view k8view17 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view k8view16 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view k8view15 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view k8view14 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view k8view13 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view k8view12 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view k8view11 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view k8view10 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view k8view09 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view k8view08 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view k8view07 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view k8view06 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view k8view05 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view k8view04 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view k8view03 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view k8view02 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view k8view01 ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """ALTER TABLE l8tablec 
ATTRIBUTE AUDIT ;"""
    output = _dci.cmdexec(stmt)
    
    #-- Cleanup:
    stmt = """drop table l8tablea;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table l8tableb;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table l8tablec;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test010(desc="""a10"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt110 : A10
    #  Description:        Test transformation of [NOT] IN, ANY/ALL.
    #  Test case inputs:   --
    #  Test case outputs:  --
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    # Find all customers that are in the same state as supplier 15:
    stmt = """select *
from """ + gvars.g_schema_arkcasedb + """.customer 
where state in
(
select state
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum = 15
)
order by custnum
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s0')
    
    # Find all customers that are NOT in the same state as supplier 15:
    stmt = """select *
from """ + gvars.g_schema_arkcasedb + """.customer 
where state NOT in
(
select state
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum = 15
)
order by custnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s1')
    
    # Customers that are in the same state as known suppliers:
    stmt = """select *
from """ + gvars.g_schema_arkcasedb + """.customer 
where state in
(
select state
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum = 1
)
or state in
(
select state
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum = 2
)
or state in
(
select state
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum = 3
)
or state in
(
select state
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum = 4
)
or state in
(
select state
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum = 6
)
or state in
(
select state
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum = 8
)
or state in
(
select state
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum = 10
)
or state in
(
select state
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum = 15
)
order by custnum
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s2')
    
    # Customers that are NOT in the same state as known suppliers:
    stmt = """select *
from """ + gvars.g_schema_arkcasedb + """.customer 
where state not in
(
select state
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum = 1
)
and state not in
(
select state
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum = 2
)
and state not in
(
select state
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum = 3
)
and state not in
(
select state
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum = 4
)
and state not in
(
select state
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum = 6
)
and state not in
(
select state
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum = 8
)
and state not in
(
select state
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum = 10
)
and state not in
(
select state
from """ + gvars.g_schema_arkcasedb + """.supplier 
where suppnum = 15
)
order by custnum
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s3')
    
    stmt = """select regnum
from """ + gvars.g_schema_arkcasedb + """.region A
group by A.regnum
having 1 not in
(select regnum
from """ + gvars.g_schema_arkcasedb + """.branch B
where A.regnum = B.regnum
group by B.regnum
having 2 not in
(select regnum
from """ + gvars.g_schema_arkcasedb + """.region C
where A.regnum = C.regnum
group by C.regnum
having 3 not in
(select regnum
from """ + gvars.g_schema_arkcasedb + """.branch D
where A.regnum = D.regnum
group by D.regnum
having 4 not in
(select regnum
from """ + gvars.g_schema_arkcasedb + """.region E
where A.regnum = E.regnum
group by E.regnum
having 5 not in
(select regnum
from """ + gvars.g_schema_arkcasedb + """.branch F
where A.regnum = F.regnum
group by F.regnum
having 6 not in
(select regnum
from """ + gvars.g_schema_arkcasedb + """.region G
where A.regnum = G.regnum
group by G.regnum
having 7 not in
(select regnum
from """ + gvars.g_schema_arkcasedb + """.branch H
where A.regnum = H.regnum
group by H.regnum
having 8 not in
(select regnum
from """ + gvars.g_schema_arkcasedb + """.region I
where A.regnum = I.regnum
group by I.regnum
having 9 not in
(select regnum
from """ + gvars.g_schema_arkcasedb + """.region J
where A.regnum = J.regnum
))))) ))))
order by regnum
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s4')
    
    # NOT IN.
    # Get employee names who do not work at first branches
    # (eliminate duplicates):
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
group by branchnum, empname
having 1 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
group by branchnum
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s5')
    
    # NOT IN.
    # Get employee names who do not work at various branches:
    # (eliminate duplicates):
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
group by branchnum, empname
having 1 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
group by branchnum
)
and   12 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
group by branchnum
)
and   13 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
group by branchnum
)
and   14 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
group by branchnum
)
and   15 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
group by branchnum
)
and   16 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
group by branchnum
)
and   17 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
group by branchnum
)
and   18 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
group by branchnum
)
and   19 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
group by branchnum
)
and   20 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
group by branchnum
)
order by empname
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s6')
    
    # NOT IN.
    # Get employee names who do not work at various branches:
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
group by branchnum, empname
having 1 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
group by branchnum
)
and   12 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
group by branchnum
)
and   13 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
)
and   14 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
)
and   15 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
)
and   16 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
)
and   17 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
)
and   18 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
)
and   19 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
)
and   20 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
)
and   21 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
)
and   22 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
)
and   23 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
)
and   24 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
)
and   25 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
)
and   26 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
)
and   27 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
)
and   28 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
)
and   29 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
)
and   30 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
)
and   31 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
)
and   32 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
)
and   33 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
)
and   34 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
)
and   35 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
)
and   36 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
)
and   37 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
)
and   38 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
)
and   39 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
)
and   40 not in
(select branchnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.employee.branchnum = """ + gvars.g_schema_arkcasedb + """.branch.branchnum
)
order by empname
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s7')
    
    # NOT IN.
    # Get customer numbers for customers who have not ordered
    # parts stored at various locations:
    # It leaves location F76, with custnums 3333, 3210, and 5635.
    stmt = """select custnum
from """ + gvars.g_schema_arkcasedb + """.customer 
group by custnum
having 'J87' not in
(select col_2
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where custnum = col_12
)
and    'B78' not in
(select col_2
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where custnum = col_12
)
and    'A21' not in
(select col_2
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where custnum = col_12
)
and    'X10' not in
(select col_2
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where custnum = col_12
)
and    'X11' not in
(select col_2
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where custnum = col_12
)
and    'X12' not in
(select col_2
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where custnum = col_12
)
and    'H87' not in
(select col_2
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where custnum = col_12
)
and    'J88' not in
(select col_2
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where custnum = col_12
)
and    'H76' not in
(select col_2
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where custnum = col_12
)
and    'J65' not in
(select col_2
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where custnum = col_12
)
and    'K94' not in
(select col_2
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where custnum = col_12
)
and    'K87' not in
(select col_2
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where custnum = col_12
)
and    'K45' not in
(select col_2
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where custnum = col_12
)
and    'K43' not in
(select col_2
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where custnum = col_12
)
and    'K89' not in
(select col_2
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where custnum = col_12
)
and    'L98' not in
(select col_2
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where custnum = col_12
)
and    'L88' not in
(select col_2
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where custnum = col_12
)
and    'L78' not in
(select col_2
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where custnum = col_12
)
and    'A34' not in
(select col_2
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where custnum = col_12
)
and    'A35' not in
(select col_2
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where custnum = col_12
)
and    'A36' not in
(select col_2
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where custnum = col_12
)
and    'V66' not in
(select col_2
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where custnum = col_12
)
and    'V67' not in
(select col_2
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where custnum = col_12
)
and    'V68' not in
(select col_2
from """ + gvars.g_schema_arkcasedb + """.partsfor 
where custnum = col_12
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # One ANY:
    stmt = """select partnum
from """ + gvars.g_schema_arkcasedb + """.parts A
group by partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts B
where A.partnum = B.partnum
)
order by partnum
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s9')
    
    # Several nested ANY's:
    stmt = """select partnum
from """ + gvars.g_schema_arkcasedb + """.parts A
group by partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts B
where A.partnum = B.partnum
group by B.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts C
where A.partnum = C.partnum
group by C.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts D
where A.partnum = D.partnum
group by D.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts E
where A.partnum = E.partnum
))))
order by partnum
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s10')
    
    # Ten levels of ANY's:
    stmt = """select partnum
from """ + gvars.g_schema_arkcasedb + """.parts A
group by partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts B
where A.partnum = B.partnum
group by B.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts C
where A.partnum = C.partnum
group by C.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts D
where A.partnum = D.partnum
group by D.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts E
where A.partnum = E.partnum
group by E.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts F
where A.partnum = F.partnum
group by F.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts G
where A.partnum = G.partnum
group by G.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts H
where A.partnum = H.partnum
group by H.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts I
where A.partnum = I.partnum
group by I.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts J
where A.partnum = J.partnum
))))) ))))
order by partnum
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s11')
    
    # Sixteen levels of ANY's (the max permitted):
    stmt = """select partnum
from """ + gvars.g_schema_arkcasedb + """.parts A
group by partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts B
where A.partnum = B.partnum
group by B.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts C
where A.partnum = C.partnum
group by C.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts D
where A.partnum = D.partnum
group by D.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts E
where A.partnum = E.partnum
group by E.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts F
where A.partnum = F.partnum
group by F.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts G
where A.partnum = G.partnum
group by G.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts H
where A.partnum = H.partnum
group by H.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts I
where A.partnum = I.partnum
group by I.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts J
where A.partnum = J.partnum
group by J.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts K
where A.partnum = K.partnum
group by K.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts L
where A.partnum = L.partnum
group by L.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts M
where A.partnum = M.partnum
group by M.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts N
where A.partnum = N.partnum
group by N.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts O
where A.partnum = O.partnum
group by O.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts P
where A.partnum = P.partnum
))))) ))))) )))))
order by partnum
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s12')
    
    # Several ANY's with AND's:
    stmt = """select partnum
from """ + gvars.g_schema_arkcasedb + """.parts A
group by partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts B
where A.partnum = B.partnum
group by B.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts C
where A.partnum = C.partnum
group by C.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts D
where A.partnum = D.partnum
)))
and    4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts E
where A.partnum = E.partnum
group by E.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts F
where A.partnum = F.partnum
group by F.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts G
where A.partnum = G.partnum
)))
and    4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts H
where A.partnum = H.partnum
group by H.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts I
where A.partnum = I.partnum
group by I.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts J
where A.partnum = J.partnum
)))
and    4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts K
where A.partnum = K.partnum
group by K.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts L
where A.partnum = L.partnum
group by L.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts M
where A.partnum = M.partnum
)))
and    4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts N
where A.partnum = N.partnum
group by N.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts O
where A.partnum = O.partnum
group by O.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts P
where A.partnum = P.partnum
)))
and    4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts Q
where A.partnum = Q.partnum
group by Q.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts R
where A.partnum = R.partnum
group by R.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts S
where A.partnum = S.partnum
)))
and    4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts T
where A.partnum = T.partnum
group by T.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts U
where A.partnum = U.partnum
group by U.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts V
where A.partnum = V.partnum
)))
and    4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts W
where A.partnum = W.partnum
group by W.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts X
where A.partnum = X.partnum
group by X.partnum
having 4102 =ANY
(select partnum
from """ + gvars.g_schema_arkcasedb + """.parts Y
where A.partnum = Y.partnum
)))
order by partnum
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s13')
    
    # Several ANY/SOME's:
    stmt = """select empname, empnum
from """ + gvars.g_schema_arkcasedb + """.employee E
group by E.empnum, E.empname
having 1 =SOME
(select regnum
from """ + gvars.g_schema_arkcasedb + """.region 
where manager = empnum
group by regnum
having 1 =SOME
(select regnum
from """ + gvars.g_schema_arkcasedb + """.branch 
where """ + gvars.g_schema_arkcasedb + """.region.regnum = """ + gvars.g_schema_arkcasedb + """.branch.regnum
group by regnum
having 1 =SOME
(select regnum
from """ + gvars.g_schema_arkcasedb + """.employee P
where P.regnum = """ + gvars.g_schema_arkcasedb + """.branch.regnum
group by regnum
having 1 <ANY
(select salesman
from """ + gvars.g_schema_arkcasedb + """.orders O
where E.empnum = O.salesman
group by salesman
having 1 <ANY
(select custnum
from """ + gvars.g_schema_arkcasedb + """.customer 
where O.custnum  = """ + gvars.g_schema_arkcasedb + """.customer.custnum
)))))
order by empnum
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4005')
    
    stmt = """select suppnum, partnum, partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup X
group by suppnum, partnum, partcost
having partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where X.suppnum <> Y.suppnum
and X.partnum = Y.partnum
)
order by suppnum, partnum, partcost
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s15')
    
    # One ALL again:
    # The following statements are copied to pretstA10.
    # Need to create a new table for this test, one that allows NULLs:
    
    stmt = """create table p1tab (a int, b int) no partition;"""
    output = _dci.cmdexec(stmt)
    #    catalog <subvol_for_temporary_data>;
    
    stmt = """insert into p1tab values (null,10);"""
    output = _dci.cmdexec(stmt)
    
    # Select should return 0 rows, since the only value in the
    # subselect is null and 'null = all (null)' evaluates to null.
    stmt = """Select * from p1tab t1
where t1.a = ALL
(select a from p1tab t2
where t1.b = t2.b);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # The following statement is copied to psttstA10.
    stmt = """drop table p1tab;"""
    output = _dci.cmdexec(stmt)
    
    # Several ALL's:
    
    stmt = """select suppnum, partnum, partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup X
group by suppnum, partnum, partcost
having partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 1
)
or partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 2
)
or partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 3
)
or partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 4
)
or partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 5
)
or partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 6
)
or partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 7
)
or partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 8
)
or partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 9
)
or partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 10
)
order by suppnum, partnum, partcost
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s17')
    
    stmt = """select suppnum, partnum, partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup X
group by suppnum, partnum, partcost
having partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 1
)
or partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 2
)
or partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 3
)
or partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 4
)
or partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 5
)
or partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 6
)
or partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 7
)
or partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 8
)
or partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 9
)
or partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 10
)
or partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 11
)
or partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 12
)
or partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 13
)
or partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 14
)
or partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 15
)
or partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 16
)
or partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 17
)
or partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 18
)
or partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 19
)
or partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 20
)
or partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 21
)
or partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 22
)
or partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 23
)
or partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 24
)
or partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 25
)
or partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 26
)
or partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 27
)
or partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 28
)
or partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 29
)
or partcost < ALL
(select partcost
from """ + gvars.g_schema_arkcasedb + """.fromsup Y
where Y.suppnum = 30
)
order by suppnum, partnum, partcost
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s18')
    
    _testmgr.testcase_end(desc)

def test011(desc="""a11"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0110 : A11
    #  Description:        Expression reshaping (NOT, BETWEEN, ANDs).
    #  Test case inputs:   --
    #  Test case outputs:  --
    #  Expected Results:   --
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    # The first test was run with optimization level set to 0,
    # in ordre to shorten the running time.
    
    stmt = """select empname, empnum
from """ + gvars.g_schema_arkcasedb + """.employee 
where empnum not between 30 and 251
and empnum not between 30 and 251
and empnum not between 30 and 251
and empnum not between 30 and 251
order by empname
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s0')
    
    stmt = """select empname, empnum
from """ + gvars.g_schema_arkcasedb + """.employee 
where empnum not between 30 and 251
and empnum not between 30 and 251
and empnum not between 30 and 251
and empnum not between 30 and 251
and empnum not between 30 and 251
and empnum not between 30 and 251
and empnum not between 30 and 251
and empnum not between 30 and 251
and empnum not between 30 and 251
and empnum not between 30 and 251
and empnum not between 30 and 251
order by empname
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s1')
    
    stmt = """select empname, empnum
from """ + gvars.g_schema_arkcasedb + """.employee 
where not empnum > 30
and not empnum > 39
and not empnum > 35
and not empnum > 33
and not empnum > 40
and not empnum > 42
and empnum <= 42
and empnum <= 45
and empnum <= 43
and empnum <= 50
and empnum <= 57
and empnum <= 54
order by empname
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s2')
    
    stmt = """select empname, empnum
from """ + gvars.g_schema_arkcasedb + """.employee 
where not empnum between 30 and 251
or not empnum between 30 and 251
or not empnum between 30 and 251
or not empnum between 30 and 251
or not empnum between 30 and 251
or not empnum between 30 and 251
or not empnum between 30 and 251
or not empnum between 30 and 251
or not empnum between 30 and 251
or not empnum between 30 and 251
or not empnum between 30 and 251
or empnum not between 30 and 251
order by empname
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s3')
    
    #  multiple OR'd NOT's: should get empnum 1, 23, and 29:
    stmt = """select empname, empnum
from """ + gvars.g_schema_arkcasedb + """.employee 
where not empnum > 30
or not empnum > 30
or not empnum > 30
or not empnum > 30
or not empnum > 30
or not empnum > 30
or not empnum > 30
or not empnum > 30
or not empnum > 30
or not empnum > 30
or not empnum > 30
order by empname
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s4')
    
    #  Lots of ANDed BETWEENs.
    stmt = """select empname, empnum
from """ + gvars.g_schema_arkcasedb + """.employee 
where empnum between 1 and 251
and empnum between 1 and 252
and empnum between 1 and 253
and empnum between 1 and 254
and empnum between 1 and 255
and empnum between 1 and 256
and empnum between 1 and 257
and empnum between 1 and 258
and empnum between 1 and 259
and empnum between 1 and 260
and empnum between 1 and 261
and empnum between 1 and 262
and empnum between 1 and 263
and empnum between 1 and 264
and empnum between 1 and 265
and empnum between 1 and 266
and empnum between 1 and 267
and empnum between 1 and 268
and empnum between 1 and 269
and empnum between 1 and 270
and empnum between 1 and 271
and empnum between 1 and 272
and empnum between 1 and 273
and empnum between 1 and 274
and empnum between 1 and 275
and empnum between 1 and 276
and empnum between 1 and 277
and empnum between 1 and 278
and empnum between 1 and 279
and empnum between 1 and 280
and empnum between 1 and 281
and empnum between 1 and 282
and empnum between 1 and 283
and empnum between 1 and 284
and empnum between 1 and 285
and empnum between 1 and 286
and empnum between 1 and 287
and empnum between 1 and 288
and empnum between 1 and 289
and empnum between 1 and 290
and empnum between 1 and 291
and empnum between 1 and 292
and empnum between 1 and 293
and empnum between 1 and 294
and empnum between 1 and 295
and empnum between 1 and 296
and empnum between 1 and 297
and empnum between 1 and 298
and empnum between 1 and 299
and empnum between 1 and 300
and empnum between 1 and 201
and empnum between 2 and 202
and empnum between 3 and 203
and empnum between 4 and 204
and empnum between 5 and 205
and empnum between 6 and 206
and empnum between 7 and 207
and empnum between 8 and 208
and empnum between 9 and 209
and empnum between 10 and 210
and empnum between 11 and 211
and empnum between 12 and 212
and empnum between 13 and 213
and empnum between 14 and 214
and empnum between 15 and 215
and empnum between 16 and 216
and empnum between 17 and 217
and empnum between 18 and 218
and empnum between 19 and 219
and empnum between 20 and 220
and empnum between 21 and 221
and empnum between 22 and 222
and empnum between 23 and 223
and empnum between 24 and 224
and empnum between 25 and 225
and empnum between 26 and 226
and empnum between 27 and 227
and empnum between 28 and 228
and empnum between 29 and 229
and empnum between 30 and 230
and empnum between 31 and 231
and empnum between 32 and 232
and empnum between 33 and 233
and empnum between 34 and 234
and empnum between 35 and 235
and empnum between 36 and 236
and empnum between 37 and 237
and empnum between 38 and 238
and empnum between 39 and 239
and empnum between 40 and 240
and empnum between 41 and 241
and empnum between 42 and 242
and empnum between 43 and 243
and empnum between 44 and 244
and empnum between 45 and 245
and empnum between 46 and 246
and empnum between 47 and 247
and empnum between 48 and 248
and empnum between 49 and 249
and empnum between 50 and 250
order by empname
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s5')
    
    stmt = """select empname, empnum
from """ + gvars.g_schema_arkcasedb + """.employee 
where empnum between 1 and 251
and empnum between 1 and 252
and empnum between 1 and 253
and empnum between 1 and 254
and empnum between 1 and 255
and empnum between 1 and 256
and empnum between 1 and 257
and empnum between 1 and 258
and empnum between 1 and 259
and empnum between 1 and 260
and empnum between 1 and 261
and empnum between 1 and 262
and empnum between 1 and 263
and empnum between 1 and 264
and empnum between 1 and 265
and empnum between 1 and 266
and empnum between 1 and 267
and empnum between 1 and 268
and empnum between 1 and 269
and empnum between 1 and 270
and empnum between 1 and 271
and empnum between 1 and 272
and empnum between 1 and 273
and empnum between 1 and 274
and empnum between 1 and 275
and empnum between 1 and 276
and empnum between 1 and 277
and empnum between 1 and 278
and empnum between 1 and 279
and empnum between 1 and 280
and empnum between 1 and 281
and empnum between 1 and 282
and empnum between 1 and 283
and empnum between 1 and 284
and empnum between 1 and 285
and empnum between 1 and 286
and empnum between 1 and 287
and empnum between 1 and 288
and empnum between 1 and 289
and empnum between 1 and 290
and empnum between 1 and 291
and empnum between 1 and 292
and empnum between 1 and 293
and empnum between 1 and 294
and empnum between 1 and 295
and empnum between 1 and 296
and empnum between 1 and 297
and empnum between 1 and 298
and empnum between 1 and 299
and empnum between 1 and 300
and empnum between 7 and 251
and empnum between 7 and 252
and empnum between 7 and 253
and empnum between 7 and 254
and empnum between 7 and 255
and empnum between 7 and 256
and empnum between 7 and 257
and empnum between 7 and 258
and empnum between 7 and 259
and empnum between 7 and 260
and empnum between 7 and 261
and empnum between 7 and 262
and empnum between 7 and 263
and empnum between 7 and 264
and empnum between 7 and 265
and empnum between 7 and 266
and empnum between 7 and 267
and empnum between 7 and 268
and empnum between 7 and 269
and empnum between 7 and 270
and empnum between 7 and 271
and empnum between 7 and 272
and empnum between 7 and 273
and empnum between 7 and 274
and empnum between 7 and 275
and empnum between 7 and 276
and empnum between 7 and 277
and empnum between 7 and 278
and empnum between 7 and 279
and empnum between 7 and 280
and empnum between 7 and 281
and empnum between 7 and 282
and empnum between 7 and 283
and empnum between 7 and 284
and empnum between 7 and 285
and empnum between 7 and 286
and empnum between 7 and 287
and empnum between 7 and 288
and empnum between 7 and 289
and empnum between 7 and 290
and empnum between 7 and 291
and empnum between 7 and 292
and empnum between 7 and 293
and empnum between 7 and 294
and empnum between 7 and 295
and empnum between 7 and 296
and empnum between 7 and 297
and empnum between 7 and 298
and empnum between 7 and 299
and empnum between 7 and 300
and empnum between 1 and 201
and empnum between 2 and 202
and empnum between 3 and 203
and empnum between 4 and 204
and empnum between 5 and 205
and empnum between 6 and 206
and empnum between 7 and 207
and empnum between 8 and 208
and empnum between 9 and 209
and empnum between 10 and 210
and empnum between 11 and 211
and empnum between 12 and 212
and empnum between 13 and 213
and empnum between 14 and 214
and empnum between 15 and 215
and empnum between 16 and 216
and empnum between 17 and 217
and empnum between 18 and 218
and empnum between 19 and 219
and empnum between 20 and 220
and empnum between 21 and 221
and empnum between 22 and 222
and empnum between 23 and 223
and empnum between 24 and 224
and empnum between 25 and 225
and empnum between 26 and 226
and empnum between 27 and 227
and empnum between 28 and 228
and empnum between 29 and 229
and empnum between 30 and 230
and empnum between 31 and 231
and empnum between 32 and 232
and empnum between 33 and 233
and empnum between 34 and 234
and empnum between 35 and 235
and empnum between 36 and 236
and empnum between 37 and 237
and empnum between 38 and 238
and empnum between 39 and 239
and empnum between 40 and 240
and empnum between 41 and 241
and empnum between 42 and 242
and empnum between 43 and 243
and empnum between 44 and 244
and empnum between 45 and 245
and empnum between 46 and 246
and empnum between 47 and 247
and empnum between 48 and 248
and empnum between 49 and 249
and empnum between 50 and 250
order by empname
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s6')
    
    stmt = """select empname, empnum, custname, partname
from """ + gvars.g_schema_arkcasedb + """.employee 
, """ + gvars.g_schema_arkcasedb + """.region 
, """ + gvars.g_schema_arkcasedb + """.branch 
, """ + gvars.g_schema_arkcasedb + """.orders 
, """ + gvars.g_schema_arkcasedb + """.customer 
, """ + gvars.g_schema_arkcasedb + """.odetail 
, """ + gvars.g_schema_arkcasedb + """.fromsup 
, """ + gvars.g_schema_arkcasedb + """.parts 
, """ + gvars.g_schema_arkcasedb + """.supplier 
where """ + gvars.g_schema_arkcasedb + """.region.regnum   = """ + gvars.g_schema_arkcasedb + """.branch.regnum
and   """ + gvars.g_schema_arkcasedb + """.employee.regnum = """ + gvars.g_schema_arkcasedb + """.branch.regnum
and   """ + gvars.g_schema_arkcasedb + """.employee.empnum = """ + gvars.g_schema_arkcasedb + """.orders.salesman
and   """ + gvars.g_schema_arkcasedb + """.orders.custnum  = """ + gvars.g_schema_arkcasedb + """.customer.custnum
and   """ + gvars.g_schema_arkcasedb + """.orders.ordernum = """ + gvars.g_schema_arkcasedb + """.odetail.ordernum
and   """ + gvars.g_schema_arkcasedb + """.parts.partnum   = """ + gvars.g_schema_arkcasedb + """.odetail.partnum
and   """ + gvars.g_schema_arkcasedb + """.parts.partnum   = """ + gvars.g_schema_arkcasedb + """.supplier.suppnum
and   """ + gvars.g_schema_arkcasedb + """.supplier.suppnum = """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum
and """ + gvars.g_schema_arkcasedb + """.employee.empnum    between 1 and 1000
and """ + gvars.g_schema_arkcasedb + """.employee.empname   between 'A' and 'Z'
and """ + gvars.g_schema_arkcasedb + """.employee.regnum    between 1 and 1000
and """ + gvars.g_schema_arkcasedb + """.employee.branchnum between 1 and 1000
and """ + gvars.g_schema_arkcasedb + """.employee.job       between 'A' and 'Z'
and """ + gvars.g_schema_arkcasedb + """.employee.age       between 1 and 1000
and """ + gvars.g_schema_arkcasedb + """.employee.salary    between 1 and 300000
and """ + gvars.g_schema_arkcasedb + """.employee.vacation  between 1 and 1000
and """ + gvars.g_schema_arkcasedb + """.region.regnum   between 1 and 1000
and """ + gvars.g_schema_arkcasedb + """.region.regname  between 'A' and 'Z'
and """ + gvars.g_schema_arkcasedb + """.region.location between 'A' and 'Z'
and """ + gvars.g_schema_arkcasedb + """.region.manager  between 1 and 300000
and """ + gvars.g_schema_arkcasedb + """.branch.regnum     between 1 and 1000
and """ + gvars.g_schema_arkcasedb + """.branch.branchnum  between 1 and 1000
and """ + gvars.g_schema_arkcasedb + """.branch.branchname between 'A' and 'Z'
and """ + gvars.g_schema_arkcasedb + """.branch.manager    between 1 and 300000
and """ + gvars.g_schema_arkcasedb + """.orders.ordernum between 1 and 1000
and """ + gvars.g_schema_arkcasedb + """.orders.omonth   between 1 and 1000
and """ + gvars.g_schema_arkcasedb + """.orders.oday     between 1 and 1000
and """ + gvars.g_schema_arkcasedb + """.orders.oyear    between 1 and 1000
and """ + gvars.g_schema_arkcasedb + """.orders.dmonth   between 1 and 1000
and """ + gvars.g_schema_arkcasedb + """.orders.dday     between 1 and 1000
and """ + gvars.g_schema_arkcasedb + """.orders.dyear    between 1 and 1000
and """ + gvars.g_schema_arkcasedb + """.orders.salesman between 1 and 300000
and """ + gvars.g_schema_arkcasedb + """.orders.custnum  between 1 and 300000
and """ + gvars.g_schema_arkcasedb + """.customer.custnum  between 1 and 1000
and """ + gvars.g_schema_arkcasedb + """.customer.custname between 'B' and 'C'
and """ + gvars.g_schema_arkcasedb + """.customer.address  between 'A' and 'Z'
and """ + gvars.g_schema_arkcasedb + """.customer.city     between 'A' and 'Z'
and """ + gvars.g_schema_arkcasedb + """.customer.state    between 'A' and 'Z'
and """ + gvars.g_schema_arkcasedb + """.fromsup.partnum   between 1 and 1000
and """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum   between 1 and 1000
and """ + gvars.g_schema_arkcasedb + """.fromsup.partcost  between 1 and 300000
and """ + gvars.g_schema_arkcasedb + """.odetail.ordernum  between 1 and 1000
and """ + gvars.g_schema_arkcasedb + """.odetail.partnum   between 1 and 300000
and """ + gvars.g_schema_arkcasedb + """.odetail.quantity  between 1 and 1000
and """ + gvars.g_schema_arkcasedb + """.parts.partnum     between 1 and 300000
and """ + gvars.g_schema_arkcasedb + """.parts.partname    between 'P' and 'Q'
and """ + gvars.g_schema_arkcasedb + """.parts.inventory   between 1 and 1000
and """ + gvars.g_schema_arkcasedb + """.parts.location    between 'A' and 'Z'
and """ + gvars.g_schema_arkcasedb + """.parts.price       between 1 and 300000
order by empname
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    _testmgr.testcase_end(desc)

def test012(desc="""a12"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0110 : A12
    #  Description:        Moves expressions between HAVING tree and
    #                      WHERE tree.
    #  Test case inputs:   --
    #  Test case outputs:  --
    #  Expected Results:   --
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    #
    # =================== End Test Case Header  ===================
    #
    #  ---------------------------------
    #  Create the Log file.
    #  ---------------------------------
    #  ---------------------------------
    #  Set up default catalog and schema
    #  ---------------------------------
    # set catalog eval;
    # set schema  eval.gdb;
    
    #  HAVING clause does not contain a function of a native column:
    stmt = """select regnum
from """ + gvars.g_schema_arkcasedb + """.region 
group by regnum
having regnum = 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s0')
    
    stmt = """select regnum
from """ + gvars.g_schema_arkcasedb + """.region 
group by regnum
having regnum = 0
or regnum = 1
or regnum = 2
or regnum = 3
or regnum = 4
or regnum = 5
or regnum = 6
or regnum = 7
or regnum = 8
or regnum = 9
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s1')
    
    stmt = """set param ?wanted 2;"""
    output = _dci.cmdexec(stmt)
    #   Should return 4, 1 and 5, 1:
    stmt = """select regnum, count (distinct branchnum)
from """ + gvars.g_schema_arkcasedb + """.branch 
where regnum > 0
group by regnum, branchnum
having ( regnum > 3 )
and ( branchnum = ?wanted)
and ( count(distinct branchnum) > 0 )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s2')
    stmt = """select regnum, count (distinct branchnum)
from """ + gvars.g_schema_arkcasedb + """.branch 
where regnum > 0
group by regnum, branchnum
having ( regnum > 3 )
and ( branchnum = ?wanted)
and ( count(distinct branchnum) > 0 )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s3')
    
    #  ---------------------------------
    #  Since Region A is used in the Having clauses,
    #  they are evaluated for each row in Region A
    #  Note: The expected results for this match what
    #  MP use to produce (The second have duplicates
    #  the first have, which doesn't have 1 in it)
    #  ---------------------------------
    
    stmt = """select regnum
from """ + gvars.g_schema_arkcasedb + """.region A
where    1 not in
(select regnum from """ + gvars.g_schema_arkcasedb + """.branch B
where A.regnum = B.regnum group by regnum having 2 not in
(select regnum from """ + gvars.g_schema_arkcasedb + """.region C
where A.regnum = C.regnum group by regnum having 3 not in
(select regnum from """ + gvars.g_schema_arkcasedb + """.branch D
where A.regnum = D.regnum group by regnum having 4 not in
(select regnum from """ + gvars.g_schema_arkcasedb + """.region E
where A.regnum = E.regnum group by regnum having 5 not in
(select regnum from """ + gvars.g_schema_arkcasedb + """.branch F
where A.regnum = F.regnum group by regnum having 6 not in
(select regnum from """ + gvars.g_schema_arkcasedb + """.region G
where A.regnum = G.regnum group by regnum having 7 not in
(select regnum from """ + gvars.g_schema_arkcasedb + """.branch H
where A.regnum = H.regnum group by regnum having 8 not in
(select regnum from """ + gvars.g_schema_arkcasedb + """.region I
where A.regnum = I.regnum group by regnum having 9 not in
(select regnum from """ + gvars.g_schema_arkcasedb + """.region J
where A.regnum = J.regnum
))))) ))))
group by regnum
having 1 not in
(select regnum from """ + gvars.g_schema_arkcasedb + """.branch B
where A.regnum = B.regnum group by regnum having 2 not in
(select regnum from """ + gvars.g_schema_arkcasedb + """.region C
where A.regnum = C.regnum group by regnum having 3 not in
(select regnum from """ + gvars.g_schema_arkcasedb + """.branch D
where A.regnum = D.regnum group by regnum having 4 not in
(select regnum from """ + gvars.g_schema_arkcasedb + """.region E
where A.regnum = E.regnum group by regnum having 5 not in
(select regnum from """ + gvars.g_schema_arkcasedb + """.branch F
where A.regnum = F.regnum group by regnum having 6 not in
(select regnum from """ + gvars.g_schema_arkcasedb + """.region G
where A.regnum = G.regnum group by regnum having 7 not in
(select regnum from """ + gvars.g_schema_arkcasedb + """.branch H
where A.regnum = H.regnum group by regnum having 8 not in
(select regnum from """ + gvars.g_schema_arkcasedb + """.region I
where A.regnum = I.regnum group by regnum having 9 not in
(select regnum from """ + gvars.g_schema_arkcasedb + """.region J
where A.regnum = J.regnum
))))) ))));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s4')
    
    #  ---------------------------------
    #  the second Having is missing "Group by" (or an aggregate function)
    #  So we should get an error, this is what this test had before Dec 98
    #  for the above query.  It appears that SQL processes the Having
    #  clauses differently, ie MP didn't require a group by clause, while
    #  MP does require it.
    #  ---------------------------------
    
    stmt = """select regnum from """ + gvars.g_schema_arkcasedb + """.region A
where    1 not in
(select regnum from """ + gvars.g_schema_arkcasedb + """.branch B
where A.regnum = B.regnum group by regnum having 2 not in
(select regnum from """ + gvars.g_schema_arkcasedb + """.region C
where A.regnum = C.regnum  having 3 not in
(select regnum from """ + gvars.g_schema_arkcasedb + """.region I
where A.regnum = I.regnum
)))    

group by regnum
having 1 not in
(select regnum from """ + gvars.g_schema_arkcasedb + """.branch B
where A.regnum = B.regnum group by regnum having 2 not in
(select regnum from """ + gvars.g_schema_arkcasedb + """.region C
where A.regnum = C.regnum group by regnum having 3 not in
(select regnum from """ + gvars.g_schema_arkcasedb + """.region I
where A.regnum = I.regnum
)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4005')
    
    #  WHERE clause contains a function of a native column and no
    #  nongroup columns:
    stmt = """select 1, 2, max(branchnum)
from """ + gvars.g_schema_arkcasedb + """.branch 
group by regnum, branchnum
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s6')
    
    _testmgr.testcase_end(desc)

def test013(desc="""a13"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0110 : A13
    #  Description:        This test verifies the following SQL
    #                      feature.
    #                      Test LIKE handling
    #                      Purpose: [NOT] LIKE comparisons.
    #                      Positive and negative tests
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    #
    # ---------------------------------
    # Create the Log file.
    # ---------------------------------
    # ---------------------------------
    # Set up default catalog and schema
    # ---------------------------------
    #set catalog eval;
    #set schema  eval.gdb;
    
    #  Get to the volume where the catalog is, to avoid multiple
    #  volume specifications:
    #  VOLUME $SUBVOL_FOR_TEMPORARY_DATA;
    
    # Initialize:
    stmt = """create table p4table (i1 int NOT NULL,
c2 char(6),
PRIMARY KEY (i1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into p4table values (1,'abcd');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p4table values (2,'abcef');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p4table values (3,'xycd');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p4table values (4,'abcf');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p4table values (5,'a%c_f');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from p4table;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s0')
    
    #  Positive tests.
    #  Adds start and stop keys, checks for escape char at end
    #  of pattern or preceding a regular character.
    
    #  should see 1,2,4
    stmt = """select * from p4table where c2 like 'ab%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s1')
    #  should see 2,4
    stmt = """select * from p4table where c2 like 'ab%f%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s2')
    #  should see 1,3
    stmt = """select * from p4table where c2 like '%cd%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s3')
    #  should see 1,2,4
    stmt = """select * from p4table where c2 like 'abc_%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s4')
    
    #  Positive tests.
    #  should see 1,2,4,5
    stmt = """select * from p4table where c2 like 'a_c_%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s5')
    #  should see 1,2,4,5
    stmt = """select * from p4table where c2 like 'a%%%%%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s6')
    #  should see 1,2,4
    stmt = """select * from p4table where c2 like '_b__%%%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s7')
    #  should see 2
    stmt = """select * from p4table where c2 like 'abcef_';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s8')
    
    #  Positive tests.
    #  should see 3,5
    stmt = """select * from p4table where c2 not like 'ab__%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s9')
    #  should see 3,5
    stmt = """select * from p4table where not c2 like 'ab__%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s10')
    #  should see 1,2,4
    stmt = """select * from p4table where not c2 not like 'ab__%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s11')
    
    #  Positive tests; ESCAPE.
    #  should see 5
    stmt = """select * from p4table where c2 like 'a/%c%'  escape '/';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s12')
    #  should see 5
    stmt = """select * from p4table where c2 like 'a%c/_%'  escape '/';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s13')
    #  should see 1,2,3,4
    stmt = """select * from p4table where c2 not like '%/%%'  escape '/';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s14')
    
    # Positive tests; ESCAPE with params.
    # should see 1,2,3,4
    stmt = """set param ?paramlike '%/%%';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?paramesc  '/';"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from p4table where c2 not like
?paramlike escape ?paramesc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s15')
    
    #  Negative tests.
    #  Error -8416
    stmt = """select * from p4table where c2 like 'a/' escape '/';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8410')
    #  Error -8416
    stmt = """select * from p4table where c2 like 'ab/c%' escape '/';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8410')
    #  Error -8416
    stmt = """select * from p4table where c2 like 'ab/c%' escape '%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8410')
    
    #  Check tree for start and stop keys
    #  should see 1
    stmt = """select * from p4table where c2 like 'abcd  ';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s19')
    #  should see 2,4,5
    stmt = """select * from p4table where c2 like 'a%f%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s20')
    #  should see 1,2,4,5
    stmt = """select * from p4table where c2 like 'a_c%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s21')
    
    #-- ---------------------------------
    #-- Set up default catalog and schema
    #-- ---------------------------------
    
    #--  Get to the volume where the catalog is, to avoid multiple
    #--  volume specifications:
    #-- VOLUME $SUBVOL_FOR_TEMPORARY_DATA;
    
    #-- Cleanup:
    stmt = """drop table p4table;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test014(desc="""a14"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #--  Get to the volume where the catalog is, to avoid multiple
    #--  volume specifications:
    
    stmt = """create table p5table (
i1 int
, c2 char(6)
, i3 int
, c4 char(6)
, key i1
) no partition
;"""
    output = _dci.cmdexec(stmt)
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0110 : A14
    #  Description:        This test verifies create table with big
    #                      constraints.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    #
    # ---------------------------------
    # Create the Log file.
    # ---------------------------------
    # ---------------------------------
    # Set up default catalog and schema
    # ---------------------------------
    #set catalog eval;
    #set schema  eval.gdb;
    
    #  Get to the volume where the catalog is, to avoid multiple
    #  volume specifications:
    #  VOLUME $SUBVOL_FOR_TEMPORARY_DATA;
    #
    stmt = """drop table p5table;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table p5table (
i1 int	not null
, c2 char(6)
, i3 int
, c4 char(6),
--   , key i1
PRIMARY KEY (i1)
)
--    catalog <subvol_for_temporary_data>
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into p5table values (1,'abcde',0,'abcdc');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p5table values (2,'abcef',0,'abcde');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p5table values (3,'abcfg',0,'abcde');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p5table values (4,'abcyz',0,'abcde');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p5table values (5,'xyzzz',0,'abcde');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from p5table;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s0')
    
    _testmgr.testcase_end(desc)

def test015(desc="""a14_2"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """create constraint p5con0 on p5table 
check i1 > -1
and i1 < 20
and i1 between 0 and 10
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create constraint p5con1 on p5table 
check i1 = 0
or i1 = 1
or i1 = 2
or i1 = 3
or i1 = 4
or i1 = 5
or i1 = 6
or i1 = 7
or i1 = 8
or i1 = 9
or c2 not in ( "a", "b", "c", "d")
or i3 = 0
or i3 = 1
or i3 = 2
or i3 = 3
or i3 = 4
or i3 = 5
or i3 = 6
or i3 = 7
or i3 = 8
or i3 = 9
or c4 between "aaaaa" and "zzzzz"
or c4 not in ( "a", "b", "c", "d")
;"""
    output = _dci.cmdexec(stmt)
    
    #  constraint too big for file label
    stmt = """create constraint p5con2 on p5table 
check i1 = 0
or i1 = 1
or i1 = 2
or i1 = 3
or i1 = 4
or i1 = 5
or i1 = 6
or i1 = 7
or i1 = 8
or i1 = 9
or i1 between -1 and 11
or c2 between "aaaaa" and "zzzzz"
or i3 = 0
or i3 = 1
or i3 = 2
or i3 = 3
or i3 = 4
or i3 = 5
or i3 = 6
or i3 = 7
or i3 = 8
or i3 = 9
or i3 between -1 and 11
or i3 < i1
or c4 between "aaaaa" and "zzzzz"
or c4 <> c2
;"""
    output = _dci.cmdexec(stmt)
    
    #--  Constraint too big for file label
    stmt = """create constraint p5con3 on p5table 
check i1 = 0
or i1 = 1
or i1 = 2
or i1 = 3
or i1 = 4
or i1 = 5
or i1 = 6
or i1 = 7
or i1 = 8
or i1 = 9
or i1 between -1 and 11
or c2 between "aaaaa" and "zzzzz"
or c2 not in ( "a", "b", "c", "d")
or c2 not in ( "e", "f", "g", "h")
or c2 not in ( "i", "j", "k", "l")
or c2 not in ( "m", "n", "o", "p")
or c2 not in ( "q", "r", "s", "t")
or c2 not in ( "y", "z")
or i3 = 0
or i3 = 1
or i3 = 2
or i3 = 3
or i3 = 4
or i3 = 5
or i3 = 6
or i3 = 7
or i3 = 8
or i3 = 9
or i3 between -1 and 11
or i3 < i1
or c4 between "aaaaa" and "zzzzz"
or c4 <> c2
;"""
    output = _dci.cmdexec(stmt)
    
    #--  Constraint too big for file label
    stmt = """create constraint p5con4 on p5table 
check i1 = 0
or i1 = 1
or i1 = 2
or i1 = 3
or i1 = 4
or i1 = 5
or i1 = 6
or i1 = 7
or i1 = 8
or i1 = 9
or i1 between -1 and 11
or c2 between "aaaaa" and "zzzzz"
or c2 not in ( "a", "b", "c", "d")
or c2 not in ( "e", "f", "g", "h")
or c2 not in ( "i", "j", "k", "l")
or c2 not in ( "m", "n", "o", "p")
or c2 not in ( "q", "r", "s", "t")
or c2 not in ( "y", "z")
or i3 = 0
or i3 = 1
or i3 = 2
or i3 = 3
or i3 = 4
or i3 = 5
or i3 = 6
or i3 = 7
or i3 = 8
or i3 = 9
or i3 between -1 and 11
or i3 < i1
or c4 between "aaaaa" and "zzzzz"
or c4 not in ( "a", "b", "c", "d")
or c4 not in ( "e", "f", "g", "h")
or c4 not in ( "i", "j", "k", "l")
or c4 not in ( "m", "n", "o", "p")
or c4 not in ( "q", "r", "s", "t")
or c4 not in ( "u", "v", "w", "x")
or c4 not in ( "y", "z")
or c4 <> c2
;"""
    output = _dci.cmdexec(stmt)
    
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0110 : A14
    #  Description:        This test verifies the SQL <specify>
    #                      feature.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    #
    # ---------------------------------
    # Create the Log file.
    # ---------------------------------
    # ---------------------------------
    # Set up default catalog and schema
    # ---------------------------------
    #set catalog eval;
    #set schema  eval.gdb;
    
    #  Get to the volume where the catalog is, to avoid multiple
    #  volume specifications:
    #  VOLUME $SUBVOL_FOR_TEMPORARY_DATA;
    
    stmt = """insert into p5table values (6,'abcde',7,'abcdc');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into p5table values (7,'abcde',7,'abcdc');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from p5table;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14_2exp""", 'a14_2s0')
    
    stmt = """drop table p5table;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test016(desc="""a15"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0110 : A15
    #  Description:        This test verifies the following SQL
    #                      feature.
    #                      SELECT DISTINCT and ORDER BY transformed
    #                      to GROUP BY.
    #                      Purpose: The NORMALIZER makes this  transform
    #
    #                      SELECT DISTINCT X,Y
    #                      becomes:
    #                      SELECT X, Y GROUP BY X, Y
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    #
    #  ---------------------------------
    #  Create the Log file.
    #  ---------------------------------
    #  ---------------------------------
    #  Set up default catalog and schema
    #  ---------------------------------
    # set catalog eval;
    # set schema  eval.gdb;
    
    #  HAVING clause does not contain a function of a native column:
    stmt = """select regnum
from """ + gvars.g_schema_arkcasedb + """.region 
having regnum = 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4005')
    
    stmt = """select regnum
from """ + gvars.g_schema_arkcasedb + """.region 
group by regnum
having regnum = 0
or regnum = 1
or regnum = 2
or regnum = 3
or regnum = 4
or regnum = 5
or regnum = 6
or regnum = 7
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s1')
    
    _testmgr.testcase_end(desc)

def test017(desc="""a16"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0110 : A16
    #  Description:        Union of two SELECTs where one select list
    #                      contains an aggregate on an empty table
    #  Test case inputs:   --
    #  Test case outputs:  --
    #  Expected Results:   __
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    # ---------------------------------
    #
    # ---------------------------------
    # Create the Log file.
    # ---------------------------------
    # ---------------------------------
    # Set up default catalog and schema
    # ---------------------------------
    #set catalog eval;
    #set schema  eval.gdb;
    
    # Following statements are copied to pretstA16
    
    # VOLUME <subvol_for_temporary_data>;
    
    stmt = """create table empty (a int, b int, c int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  1 row with a 0
    stmt = """select count(*) from empty;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s0')
    
    # no rows returned
    stmt = """select count(*) from empty group by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    #  1 row with a NULL
    stmt = """select sum(a) from empty;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s1')
    
    # no rows returned
    stmt = """select sum(a) from empty group by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    #  Only sums
    #  return 2 rows both with NULL
    stmt = """select sum(a) from empty union all select sum(a) from empty;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s2')
    
    #  1 row with a NULL
    stmt = """select sum(a) from empty union select sum(a) from empty;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s3')
    
    #  2 rows both with NULL
    stmt = """select sum(a) from empty union all select sum(a) from empty 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s4')
    
    #  1 row with a NULL
    stmt = """select sum(a) from empty union select sum(a) from empty 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s5')
    
    #  Only counts
    #  2 rows both with 0
    stmt = """select count(*) from empty union all select count(*) from empty;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s6')
    
    #  1 row with 0
    stmt = """select count(*) from empty union select count(*) from empty;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s7')
    
    #  2 rows with 0
    stmt = """select count(*) from empty union all select count(*) from empty 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s8')
    
    #  1 row with 0
    stmt = """select count(*) from empty union select count(*) from empty 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s9')
    
    #  Mix up aggregates
    #  2 rows, one NULL, the other 0
    stmt = """select sum(a) from empty union all select count(*) from empty;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s10')
    
    #  2 rows, one NULL, the other 0
    stmt = """select sum(a) from empty union select count(*) from empty;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s11')
    
    #  2 rows, one 0, the other NULL
    stmt = """select count(*) from empty union all select sum(a) from empty;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s12')
    
    #  2 rows, one 0, the other NULL
    stmt = """select count(*) from empty union select sum(a) from empty;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s13')
    
    #  2 rows, one 0, the other NULL
    stmt = """select sum(a) from empty union all select count(*) from empty 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s14')
    
    #  2 rows, one 0, the other NULL
    stmt = """select sum(a) from empty union select count(*) from empty 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s15')
    
    #  2 rows, one 0, the other NULL
    stmt = """select count(*) from empty union all select sum(a) from empty 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s16')
    
    #  2 rows, one 0, the other NULL
    stmt = """select count(*) from empty union all select sum(a) from empty 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s17')
    
    #  Now repeat the whole series adding GROUP BY
    #  Only sums
    #  1 row with a NULL
    stmt = """select sum(a) from empty group by b union all select sum(a) from empty;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s18')
    
    #  1 row with a NULL
    stmt = """select sum(a) from empty union all select sum(a) from empty 
group by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s19')
    
    #  1 row with a NULL
    stmt = """select sum(a) from empty group by b union select sum(a) from empty;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s20')
    
    #  1 row with a NULL
    stmt = """select sum(a) from empty union select sum(a) from empty 
group by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s21')
    
    #  1 row with a NULL
    stmt = """select sum(a) from empty group by b union all select sum(a) from empty 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s22')
    
    #  1 row with a NULL
    stmt = """select sum(a) from empty union all select sum(a) from empty 
group by b order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s23')
    
    #  1 row with a NULL
    stmt = """select sum(a) from empty group by b union select sum(a) from empty 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s24')
    
    #  1 row with a NULL
    stmt = """select sum(a) from empty union select sum(a) from empty 
group by b order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s25')
    
    #  Only counts
    #  1 row with a 0
    stmt = """select count(*) from empty group by b union all select count(*) from empty;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s26')
    
    #  1 row with 0
    stmt = """select count(*) from empty union all select count(*) from empty 
group by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s27')
    
    # 0 rows
    stmt = """select count(*) from empty group by b union select count(*) from empty 
group by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    #  1 row with 0
    stmt = """select count(*) from empty union select count(*) from empty 
group by b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s28')
    
    #  1 row with 0
    stmt = """select count(*) from empty group by b union all select count(*) from empty 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s29')
    
    #  1 row with 0
    stmt = """select count(*) from empty union all select count(*) from empty 
group by b order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s30')
    
    #  1 row with 0
    stmt = """select count(*) from empty group by b union select count(*) from empty 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s31')
    
    #  1 row with 0
    stmt = """select count(*) from empty union select count(*) from empty 
group by b order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s32')
    
    #  Mix up aggregates
    #  1 row with a 0
    stmt = """select sum(a) from empty group by b union all select count(*) from empty;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s33')
    
    #  1 row with a 0
    stmt = """select sum(a) from empty group by b union select count(*) from empty;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s34')
    
    #  1 row with a NULL
    stmt = """select count(*) from empty group by b union all select sum(a) from empty;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s35')
    
    #  1 row with a NULL
    stmt = """select count(*) from empty group by b union select sum(a) from empty;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s36')
    
    #  1 row with a 0
    stmt = """select sum(a) from empty group by b union all select count(*) from empty 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s37')
    
    #  1 row with a 0
    stmt = """select sum(a) from empty group by b union select count(*) from empty 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s38')
    
    #  1 row with a NULL
    stmt = """select count(*) from empty group by b union all select sum(a) from empty 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s39')
    
    #  1 row with a NULL
    stmt = """select count(*) from empty group by b union all select sum(a) from empty 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s40')
    
    #  Unions of an agg over an empty table with a non-agg
    #  1 row with a 0
    stmt = """select count(*) from empty union select a from empty;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s41')
    
    #  1 row with a 0
    stmt = """select a from empty union select count(*) from empty;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s42')
    
    #  1 row with a NULL
    stmt = """select sum(a) from empty union select a from empty;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s43')
    
    #  1 row with a NULL
    stmt = """select a from empty union select sum(a) from empty;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s44')
    
    #  1 row with a 0
    stmt = """select count(*) from empty union all select a from empty;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s45')
    
    #  1 row with a 0
    stmt = """select a from empty union all select count(*) from empty;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s46')
    
    #  1 row with a NULL
    stmt = """select sum(a) from empty union all select a from empty;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s47')
    
    #  1 row with a NULL
    stmt = """select a from empty union all select sum(a) from empty;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s48')
    
    #  1 row with a 0
    stmt = """select count(*) from empty union select 9 from empty;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s49')
    
    #  1 row with a 0
    stmt = """select 8 from empty union select count(*) from empty;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s50')
    
    #  1 row with a NULL
    stmt = """select sum(a) from empty union select 7 from empty;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s51')
    
    #  1 row with a NULL
    stmt = """select 6 from empty union select sum(a) from empty;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s52')
    
    _testmgr.testcase_end(desc)

def test018(desc="""a17"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0110 : A17
    #  Description:        Aggregated select on an empty table
    #  Test case inputs:   --
    #  Test case outputs:  --
    #  Expected Results:   --
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    #
    #  ---------------------------------
    #  Create the Log file.
    #  ---------------------------------
    #  ---------------------------------
    #  Set up default catalog and schema
    #  ---------------------------------
    # set catalog eval;
    # set schema  eval.gdb;
    
    #  return 1 row, since there is 1 group
    stmt = """select sum(a), count(*) from empty;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s0')
    
    #  return 1 row, since there is also one group
    stmt = """select sum(a), 7 from empty;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s1')
    
    #  return 1 row, since there is also one group
    stmt = """select count(*), 7 from empty;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s2')
    
    #  return 1 row, since there is also one group
    stmt = """select avg(a), 7 from empty;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s3')
    
    #  return 1 row, since there is also one group
    stmt = """select min(a), 7 from empty;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s4')
    
    #  return 1 row, since there is also one group
    stmt = """select max(a), 7 from empty;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s5')
    
    stmt = """drop table empty;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test019(desc="""a18"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """CREATE TABLE d1 ( i1 INT UNSIGNED not null
,i2 INT UNSIGNED
,i3 INT UNSIGNED,
PRIMARY KEY (i1) );"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE d2 ( i1 INT UNSIGNED not null
, i2 INT UNSIGNED
, i3 INT UNSIGNED,
PRIMARY KEY (i1) );"""
    output = _dci.cmdexec(stmt)
    
    #-- Create a view:
    stmt = """CREATE VIEW d3 (i1,i2,i3) AS    

SELECT i1,i2,i3 FROM   d1;"""
    output = _dci.cmdexec(stmt)
    
    #-- Create a view for error tests.  Must have function,
    #-- group col, and expression in select list.
    stmt = """CREATE VIEW vs1 (i1,i2,i3) AS
SELECT avg(i1),i2,i2*2
FROM   d1 
WHERE  i1>3
GROUP BY i2;"""
    output = _dci.cmdexec(stmt)
    
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt110 : A18
    #  Description:        Test Normalizer error messages
    #  Test case inputs:   --
    #  Test case outputs:  --
    #  Expected Results:   --
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    #
    # ---------------------------------
    # Create the Log file.
    # ---------------------------------
    # ---------------------------------
    # Set up default catalog and schema
    # ---------------------------------
    #set catalog eval;
    #set schema  eval.gdb;
    
    # Fill tables with values:
    # - - - - - - - - -  - - <KEY> - - - -  - - -
    stmt = """INSERT INTO d1 VALUES (  11 ,  21 ,  61);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO d1 VALUES (  31 ,  41 ,  51);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO d1 VALUES (  51 ,  61 ,   1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # - - - - - - - - -  - - <KEY> - - - -  - - -
    stmt = """INSERT INTO d2 VALUES (  31 ,   10,  88);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO d2 VALUES (  51 ,   8 ,  66);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO d2 VALUES (  71 ,   6 ,  44);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # * ERROR from SQL [-5001]: Aggregate function in argument of
    # * aggregate function.
    stmt = """select avg(col_1)
from """ + gvars.g_schema_arkcasedb + """.svsel12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s0')
    stmt = """select avg(i1 + max(i2) )
from d1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4009')
    stmt = """select max( max(partnum) )
from """ + gvars.g_schema_arkcasedb + """.parts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4009')
    stmt = """select max( min(partnum) )
from """ + gvars.g_schema_arkcasedb + """.parts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4009')
    
    # * ERROR from SQL [-5002]: Part of PREPROCESSOR normalizer.
    # * Cursor could not be used for update because of one of these
    # * reasons: 1)It involves a join; 2) It has a GROUP BY clause,
    # * ORDER BY clause, or aggregate functions; 3) It specificies
    # * DISTINCT.
    # * Test not yet implemented
    
    # * ERROR from SQL [-5003]: A subquery can have only one entry in the
    # * select list;
    # * D30 - dlh - we now receive SQL [-5018]
    stmt = """select empname
from """ + gvars.g_schema_arkcasedb + """.employee 
where empnum in
(select *
from """ + gvars.g_schema_arkcasedb + """.orders 
where custnum = 1234
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4042')
    stmt = """select i1,i2 from d2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s5')
    stmt = """select *
from d1 
where i1 >= all (select i1,i2 from d2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4042')
    
    # * ERROR from SQL [-5004]: Select statement is grouped, either
    # * because it has a GROUP BY clause or because it contains an
    # * aggregate function.  A column in the select list that is not
    # * a GROUP BY column can only appear in the argument of an
    # * aggregate function.
    stmt = """select binary_32_u
from """ + gvars.g_schema_arkcasedb + """.btsel01 
where max(binary_32_u) > 50;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4015')
    stmt = """select binary_64_s, avg(binary_64_s)
from """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4021')
    stmt = """select binary_32_u, avg(pic_comp_1) from
 """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4021')
    stmt = """select i1, avg(i2) from d1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4021')
    
    # * ERROR from SQL [-5005]: error shown in binder; dormant in
    # * normalizer.
    #  +++ unused
    
    # * ERROR from SQL [-5006]: error shown in binder; dormant in
    # * normalizer.
    #  +++ unused
    
    # Values is selected from and inserted into the same table.
    stmt = """insert into d1 
(select * from d1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    stmt = """update d1 set i2 = i2
where i1 > ANY (select i3 from d1)
and 2 > 3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 0)
    stmt = """delete from d1 
where i1 > ANY (select i3 from d1)
and 2 > 3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    # * ERROR from SQL [-5008]: View must be a protection view
    # * (Cannot update a shorthand view).
    #   +++ USELESS - binder gives 4039
    stmt = """insert into vs1 values (1,2,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4027')
    stmt = """update vs1 
set i2 = i2
where i1 > 21 and 3 < 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4028')
    stmt = """delete from vs1 
where i1 > 10 and 5>7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4028')
    
    # * ERROR from SQL [-5009]: A view column to be inserted into is
    # * not a column of a base table.
    #   +++  NOTE: can't happen now.
    
    # * ERROR from SQL [-5010]: Column list or value list is empty.
    #   +++ USELESS - parser gives 3015
    stmt = """update d1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # * ERROR from SQL [-5011]: Column list and value list are not the
    # * same length.
    #   +++ D30 - binder gives 4062
    stmt = """insert into d1 values (1,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4023')
    
    # * ERROR from SQL [-5012]: Column appears more than once in the
    # * column list.
    stmt = """update d1 
set i2 = i2,
i2 = i2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4022')
    
    # * ERROR from SQL [-5013]: Item must be a column name or a column
    # * number.
    #   CH 3310
    #   +++ should not happen.
    
    # * ERROR from SQL [-5014]: A FROM clause that refers to a grouped
    # * view cannot refer to any additional tables or views.
    stmt = """select * from """ + gvars.g_schema_arkcasedb + """.svsel14,
 """ + gvars.g_schema_arkcasedb + """.btsel01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s18')
    stmt = """select T0.i1,T1.i1
from d1 T0, vs1 T1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s19')
    
    # * ERROR from SQL [-5015]: An aggregate function cannot appear
    # * in an update set expression.
    stmt = """update d1 
set i2 = max(i3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4015')
    
    # * ERROR from SQL [-5016]: An entry in a GROUP BY or ORDER BY
    # * list must be a constant or a column from the current query.
    stmt = """select i1
from d1 T0
where i1 > ANY (select avg(i1)
from d1 
group by T0.i2) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s21')
    
    # * ERROR from SQL [-5017]: A column number in an ORDER BY list
    # * is out of range.
    #   +++ D30 - binder gives 4012
    stmt = """select i1,i2
from d1 
where i1 > 4
order by 99;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4007')
    
    stmt = """select i1,i2
from d1 
where i1 > 4
group by 99;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4007')
    
    # * ERROR from SQL [-5018]: A select list of a subquery must
    # * contain exactly one expression.
    #   +++ USELESS - parser gives 3015
    stmt = """select i1,i2 from d2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s24')
    stmt = """select *
from d1 
where exists (select i1,i2
from d2 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s25')
    
    # * ERROR from SQL [-5019]: A select statement that is GROUPed cannot
    # * refer to a VIEW that is grouped.
    #   se^norm^view^groupby^groupby    grouped view in grouped select
    stmt = """select i1
from vs1 
where i1 > 4
group by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s26')
    stmt = """select i1,i2
from vs1 
where i1 > 4
group by i3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4005')
    
    # * ERROR from SQL [-5020]: A select involves a view that could
    # * not be composed.  The GROUP BY or ORDER BY list of the
    # * statement indexes a view column that represents an expression,
    # * but the view column does not appear in the select list of the
    # * statement.
    #   se^norm^view^list^index   gb/ob ix refers to absent view col expr
    #   CO 4520
    #   CO 6690
    stmt = """select i1,i2
from vs1 
where i1 > 4
order by i3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s28')
    
    # * ERROR from SQL [-5021]: A select statement that refers to a
    # * grouped view in the FROM clause cannot include a HAVING clause.
    stmt = """select count(*)
from vs1 
having i1 > 33;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4005')
    
    # * ERROR from SQL [-5022]: A select statement that refers to a
    # * grouped view in the FROM clause cannot include any function
    # * on columns of that view in the select list.
    stmt = """select max(pic_X_7)
from """ + gvars.g_schema_arkcasedb + """.svsel14;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    stmt = """select max(i3)
from vs1 
where i2 > 33;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s31')
    
    # * ERROR from SQL [-5023]: A GROUP BY list cannot refer to a select
    # * list item that is an expression containing an aggregate function
    # * whose argument contains a column from the FROM clause result
    # * table. i.e., only a function with an argument that is a correlated
    # * reference to a column to a column from an outer table is allowed.
    stmt = """select max(i1) ,i2
from d1 
where i1 > 4
group by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4185')
    
    # * ERROR from SQL [-5024]:  The argument of an aggregate function
    # * cannot contain both a column from a subquery and a correlation
    # * column from a select statement where the select statement is a
    # * grouped query and a correlation column is not a grouping column of
    # * the select column.
    #   CH 7640
    #   and a correlation column C from Select S where S
    #   is a grouped query and C in not a grouping column of S.
    stmt = """select sum(i3)
from d1 T0
where i1 > ANY (select avg(T1.i1 + T0.i1)
from d1 T1
group by T1.i3 )
group by i2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4006')
    
    # * ERROR from SQL [-5025]: For a grouped select statement, an
    # * expression cannot contain both an aggregate function whose
    # * argument contains a column from the select statement and the
    # * column that is not a grouping column of the select statement.
    stmt = """select regnum, branchnum
from """ + gvars.g_schema_arkcasedb + """.employee X
where X.salary >ALL
(select avg(Y.salary)
from """ + gvars.g_schema_arkcasedb + """.employee Y
where Y.salary >= min(X.salary)
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4015')
    stmt = """select regnum, branchnum
from """ + gvars.g_schema_arkcasedb + """.employee X
where X.salary >ALL
(select avg(Y.salary)
from """ + gvars.g_schema_arkcasedb + """.employee Y
where Y.salary >= min(Y.salary)
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4015')
    stmt = """select sum(i3)
from d1 T0
where i1 > min(i1)
group by i2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4015')
    
    stmt = """DROP VIEW d3;"""
    output = _dci.cmdexec(stmt)
    stmt = """DROP VIEW vs1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """DROP TABLE d1;"""
    output = _dci.cmdexec(stmt)
    stmt = """DROP TABLE d2;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test020(desc="""a19"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0110 : A19
    #  Description:        Negative: Normalizer error messages
    #                      provoked.
    #  Test case inputs:   --
    #  Test case outputs:  --
    #  Expected Results:   --
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    #
    #  ---------------------------------
    #  Create the Log file.
    #  ---------------------------------
    #  ---------------------------------
    #  Set up default catalog and schema
    #  ---------------------------------
    # set catalog eval;
    # set schema  eval.gdb;
    
    #  Correlated subquery works; but correlated column
    #  should fail (check with Slutz):
    #  06NOV89 Does not fail because not ambiguous.
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having 4102 in
(select partnum
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where """ + gvars.g_schema_arkcasedb + """.supplier.suppnum = suppnum);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s0')
    
    stmt = """select suppnum
from """ + gvars.g_schema_arkcasedb + """.supplier 
group by suppnum
having 4102 <
(select max (partnum + avg (""" + gvars.g_schema_arkcasedb + """.supplier.suppnum))
from """ + gvars.g_schema_arkcasedb + """.fromsup 
where """ + gvars.g_schema_arkcasedb + """.supplier.suppnum = """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4009')
    
    stmt = """select max (partnum) , avg (""" + gvars.g_schema_arkcasedb + """.supplier.suppnum)
from """ + gvars.g_schema_arkcasedb + """.supplier 
, """ + gvars.g_schema_arkcasedb + """.fromsup 
where """ + gvars.g_schema_arkcasedb + """.supplier.suppnum = """ + gvars.g_schema_arkcasedb + """.fromsup.suppnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s2')
    
    #  Should get error where function has only constants.
    stmt = """select max(partnum) , avg (3)
from """ + gvars.g_schema_arkcasedb + """.parts 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s3')
    stmt = """set param ?j 5;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select max(partnum) , max(partnum+?j) , max(?j)
from """ + gvars.g_schema_arkcasedb + """.parts 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s4')
    stmt = """select max(partnum) , max(6 - ?j)
from """ + gvars.g_schema_arkcasedb + """.parts 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s5')
    stmt = """select max(partnum) , max(?j)
from """ + gvars.g_schema_arkcasedb + """.parts 
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s6')
    
    _testmgr.testcase_end(desc)

def test021(desc="""n03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0110 : N03
    #  Description:        This test verifies the SQL Large number
    #                      of PREDICATEs in parse tree
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    qn03s0._init(_testmgr, _testlist)

    #    SELECT * FROM parts WHERE partname in (
    # 'a','b','c','d','e','f','g'
    #,'h','i','j','k','l','m'
    #,'n','o','p','q','r','s','t'
    #,'a1','b1','c1','d1','e1','f1','g1'
    #,'h1','i1','j1','k1','l1','m1'
    #,'n1','o1','p1','q1','r1','s1','t1'
    #,'a2','b2','c2','d2','e2','f2','g2'
    #,'h2','i2','j2','k2','l2','m2'
    #,'n2','o2','p2','q2','r2','s2','t2'
    #,'a3','b3','c3','d3','e3','f3','g3'
    #,'h3','i3','j3','k3','l3','m3'
    #,'n3','o3','p3','q3','r3','s3','t3'
    #,'a4','b4','c4','d4','e4','f4','g4'
    #,'h4','i4','j4','k4','l4','m4'
    #,'n4','o4','p4','q4','r4','s4','t4'
    #,'a5','b5','c5','d5','e5','f5','g5'
    #,'h5','i5','j5','k5','l5','m5'
    #,'n5','o5','p5','q5','r5','s5','t5'
    #,'a6','b6','c6','d6','e6','f6','g6'
    #,'h6','i6','j6','k6','l6','m6'
    #,'n6','o6','p6','q6','r6','s6','t6'
    #,'a7','b7','c7','d7','e7','f7','g7'
    #,'h7','i7','j7','k7','l7','m7'
    #,'n7','o7','p7','q7','r7','s7','t7'
    #,'a8','b8','c8','d8','e8','f8','g8'
    #,'h8','i8','j8','k8','l8','m8'
    #,'n8','o8','p8','q8','r8','s8','t8'
    #,'a9','b9','c9','d9','e9','f9','g9'
    #,'h9','i9','j9','k9','l9','m9'
    #,'n9','o9','p9','q9','r9','s9','t9'
    #,'a0','b0','c0','d0','e0','f0','g0'
    #,'h0','i0','j0','k0','l0','m0'
    #,'n0','o0','p0','q0','r0','s0','t0'
    #,'aa','ba','ca','da','ea','fa','ga'
    #,'ha','ia','ja','ka','la','ma'
    #,'na','oa','pa','qa','ra','sa','ta'
    #,'ab','bb','cb','db','eb','fb','gb'
    #,'hb','ib','jb','kb','lb','mb'
    #,'nb','ob','pb','qb','rb','sb','tb'
    #,'ac','cc','cc','dc','ec','fc','gc'
    #,'hc','ic','jc','kc','lc','mc'
    #,'nc','oc','pc','qc','rc','sc','tc'
    #,'ad','bd','cd','dd','ed','fd','gd'
    #,'hd','id','jd','kd','ld','md'
    #,'nd','od','pd','qd','rd','sd','td'
    #,'ae','be','ce','de','ee','fe','ge'
    #,'he','ie','je','ke','le','me'
    #,'ne','oe','pe','qe','re','se','te'
    #,'af','bf','cf','df','ef','ff','gf'
    #,'hf','if','jf','kf','lf','mf'
    #,'nf','of','pf','qf','rf','sf','tf'
    #,'a1','b1','c1','d1','e1','f1','g1'
    #,'h1','i1','j1','k1','l1','m1'
    #,'n1','o1','p1','q1','r1','s1','t1'
    #,'a2','b2','c2','d2','e2','f2','g2'
    #,'h2','i2','j2','k2','l2','m2'
    #,'n2','o2','p2','q2','r2','s2','t2'
    #,'a3','b3','c3','d3','e3','f3','g3'
    #,'h3','i3','j3','k3','l3','m3'
    #,'n3','o3','p3','q3','r3','s3','t3'
    #,'a4','b4','c4','d4','e4','f4','g4'
    #,'h4','i4','j4','k4','l4','m4'
    #,'n4','o4','p4','q4','r4','s4','t4'
    #,'a5','b5','c5','d5','e5','f5','g5'
    #,'h5','i5','j5','k5','l5','m5'
    #,'n5','o5','p5','q5','r5','s5','t5'
    #,'a6','b6','c6','d6','e6','f6','g6'
    #,'h6','i6','j6','k6','l6','m6'
    #,'n6','o6','p6','q6','r6','s6','t6'
    #,'a7','b7','c7','d7','e7','f7','g7'
    #,'h7','i7','j7','k7','l7','m7'
    #,'n7','o7','p7','q7','r7','s7','t7'
    #,'a8','b8','c8','d8','e8','f8','g8'
    #,'h8','i8','j8','k8','l8','m8'
    #,'n8','o8','p8','q8','r8','s8','t8'
    #,'a9','b9','c9','d9','e9','f9','g9'
    #,'h9','i9','j9','k9','l9','m9'
    #,'n9','o9','p9','q9','r9','s9','t9'
    #,'a0','b0','c0','d0','e0','f0','g0'
    #,'h0','i0','j0','k0','l0','m0'
    #,'n0','o0','p0','q0','r0','s0','t0'
    #,'aa','ba','ca','da','ea','fa','ga'
    #,'ha','ia','ja','ka','la','ma'
    #,'na','oa','pa','qa','ra','sa','ta'
    #,'ab','bb','cb','db','eb','fb','gb'
    #,'hb','ib','jb','kb','lb','mb'
    #,'nb','ob','pb','qb','rb','sb','tb'
    #,'ac','cc','cc','dc','ec','fc','gc'
    #,'hc','ic','jc','kc','lc','mc'
    #,'nc','oc','pc','qc','rc','sc','tc'
    #,'ad','bd','cd','dd','ed','fd','gd'
    #,'hd','id','jd','kd','ld','md'
    #,'nd','od','pd','qd','rd','sd','td'
    #,'ae','be','ce','de','ee','fe','ge'
    #,'he','ie','je','ke','le','me'
    #,'ne','oe','pe','qe','re','se','te'
    #,'af','bf','cf','df','ef','ff','gf'
    #,'hf','if','jf','kf','lf','mf'
    #,'nf','of','pf','qf','rf','sf','tf'
    #,'1a1','1b1','1c1','1d1','1e1','1f1','1g1'
    #,'1h1','1i1','1j1','1k1','1l1','1m1'
    #,'1n1','1o1','1p1','1q1','1r1','1s1','1t1'
    #,'1a2','1b2','1c2','1d2','1e2','1f2','1g2'
    #,'1h2','1i2','1j2','1k2','1l2','1m2'
    #,'1n2','1o2','1p2','1q2','1r2','1s2','1t2'
    #,'1a3','1b3','1c3','1d3','1e3','1f3','1g3'
    #,'1h3','1i3','1j3','1k3','1l3','1m3'
    #,'1n3','1o3','1p3','1q3','1r3','1s3','1t3'
    #,'1a4','1b4','1c4','1d4','1e4','1f4','1g4'
    #,'1h4','1i4','1j4','1k4','1l4','1m4'
    #,'1n4','1o4','1p4','1q4','1r4','1s4','1t4'
    #,'1a5','1b5','1c5','1d5','1e5','1f5','1g5'
    #,'1h5','1i5','1j5','1k5','1l5','1m5'
    #,'1n5','1o5','1p5','1q5','1r5','1s5','1t5'
    #,'1a6','1b6','1c6','1d6','1e6','1f6','1g6'
    #,'1h6','1i6','1j6','1k6','1l6','1m6'
    #,'1n6','1o6','1p6','1q6','1r6','1s6','1t6'
    #,'1a7','1b7','1c7','1d7','1e7','1f7','1g7'
    #,'1h7','1i7','1j7','1k7','1l7','1m7'
    #,'1n7','1o7','1p7','1q7','1r7','1s7','1t7'
    #,'1a8','1b8','1c8','1d8','1e8','1f8','1g8'
    #,'1h8','1i8','1j8','1k8','1l8','1m8'
    #,'1n8','1o8','1p8','1q8','1r8','1s8','1t8'
    #,'1a9','1b9','1c9','1d9','1e9','1f9','1g9'
    #,'1h9','1i9','1j9','1k9','1l9','1m9'
    #,'1n9','1o9','1p9','1q9','1r9','1s9','1t9'
    #,'1a0','1b0','1c0','1d0','1e0','1f0','1g0'
    #,'1h0','1i0','1j0','1k0','1l0','1m0'
    #,'1n0','1o0','1p0','1q0','1r0','1s0','1t0'
    #,'1aa','1ba','1ca','1da','1ea','1fa','1ga'
    #,'1ha','1ia','1ja','1ka','1la','1ma'
    #,'1na','1oa','1pa','1qa','1ra','1sa','1ta'
    #,'1ab','1bb','1cb','1db','1eb','1fb','1gb'
    #,'1hb','1ib','1jb','1kb','1lb','1mb'
    #,'1nb','1ob','1pb','1qb','1rb','1sb','1tb'
    #,'1ac','1cc','1cc','1dc','1ec','1fc','1gc'
    #,'1hc','1ic','1jc','1kc','1lc','1mc'
    #,'1nc','1oc','1pc','1qc','1rc','1sc','1tc'
    #,'1ad','1bd','1cd','1dd','1ed','1fd','1gd'
    #,'1hd','1id','1jd','1kd','1ld','1md'
    #,'1nd','1od','1pd','1qd','1rd','1sd','1td'
    #,'1ae','1be','1ce','1de','1ee','1fe','1ge'
    #,'1he','1ie','1je','1ke','1le','1me'
    #,'1ne','1oe','1pe','1qe','1re','1se','1te'
    #,'1af','1bf','1cf','1df','1ef','1ff','1gf'
    #,'1hf','1if','1jf','1kf','1lf','1mf'
    #,'1nf','1of','1pf','1qf','1rf','1sf','1tf'
    #,'2a1','2b1','2c1','2d1','2e1','2f1','2g1'
    #,'2h1','2i1','2j1','2k1','2l1','2m1'
    #,'2n1','2o1','2p1','2q1','2r1','2s1','2t1'
    #,'2a2','2b2','2c2','2d2','2e2','2f2','2g2'
    #,'2h2','2i2','2j2','2k2','2l2','2m2'
    #,'2n2','2o2','2p2','2q2','2r2','2s2','2t2'
    #,'2a3','2b3','2c3','2d3','2e3','2f3','2g3'
    #,'2h3','2i3','2j3','2k3','2l3','2m3'
    #,'2n3','2o3','2p3','2q3','2r3','2s3','2t3'
    #,'2a4','2b4','2c4','2d4','2e4','2f4','2g4'
    #,'2h4','2i4','2j4','2k4','2l4','2m4'
    #,'2n4','2o4','2p4','2q4','2r4','2s4','2t4'
    #,'2a5','2b5','2c5','2d5','2e5','2f5','2g5'
    #,'2h5','2i5','2j5','2k5','2l5','2m5'
    #,'2n5','2o5','2p5','2q5','2r5','2s5','2t5'
    #,'2a6','2b6','2c6','2d6','2e6','2f6','2g6'
    #,'2h6','2i6','2j6','2k6','2l6','2m6'
    #,'2n6','2o6','2p6','2q6','2r6','2s6','2t6'
    #,'2a7','2b7','2c7','2d7','2e7','2f7','2g7'
    #,'2h7','2i7','2j7','2k7','2l7','2m7'
    #,'2n7','2o7','2p7','2q7','2r7','2s7','2t7'
    #,'2a8','2b8','2c8','2d8','2e8','2f8','2g8'
    #,'2h8','2i8','2j8','2k8','2l8','2m8'
    #,'2n8','2o8','2p8','2q8','2r8','2s8','2t8'
    #,'2a9','2b9','2c9','2d9','2e9','2f9','2g9'
    #,'2h9','2i9','2j9','2k9','2l9','2m9'
    #,'2n9','2o9','2p9','2q9','2r9','2s9','2t9'
    #,'2a0','2b0','2c0','2d0','2e0','2f0','2g0'
    #,'2h0','2i0','2j0','2k0','2l0','2m0'
    #,'2n0','2o0','2p0','2q0','2r0','2s0','2t0'
    #,'2aa','2ba','2ca','2da','2ea','2fa','2ga'
    #,'2ha','2ia','2ja','2ka','2la','2ma'
    #,'2na','2oa','2pa','2qa','2ra','2sa','2ta'
    #,'2ab','2bb','2cb','2db','2eb','2fb','2gb'
    #,'2hb','2ib','2jb','2kb','2lb','2mb'
    #,'2nb','2ob','2pb','2qb','2rb','2sb','2tb'
    #,'2ac','2cc','2cc','2dc','2ec','2fc','2gc'
    #,'2hc','2ic','2jc','2kc','2lc','2mc'
    #,'2nc','2oc','2pc','2qc','2rc','2sc','2tc'
    #,'2ad','2bd','2cd','2dd','2ed','2fd','2gd'
    #,'2hd','2id','2jd','2kd','2ld','2md'
    #,'2nd','2od','2pd','2qd','2rd','2sd','2td'
    #,'2ae','2be','2ce','2de','2ee','2fe','2ge'
    #,'2he','2ie','2je','2ke','2le','2me'
    #,'2ne','2oe','2pe','2qe','2re','2se','2te'
    #,'2af','2bf','2cf','2df','2ef','2ff','2gf'
    #,'2hf','2if','2jf','2kf','2lf','2mf'
    #,'2nf','2of','2pf','2qf','2rf','2sf','2tf'
    #,'3a1','3b1','3c1','3d1','3e1','3f1','3g1'
    #,'3h1','3i1','3j1','3k1','3l1','3m1'
    #,'3n1','3o1','3p1','3q1','3r1','3s1','3t1'
    #,'3a2','3b2','3c2','3d2','3e2','3f2','3g2'
    #,'3h2','3i2','3j2','3k2','3l2','3m2'
    #,'3n2','3o2','3p2','3q2','3r2','3s2','3t2'
    #,'3a3','3b3','3c3','3d3','3e3','3f3','3g3'
    #,'3h3','3i3','3j3','3k3','3l3','3m3'
    #,'3n3','3o3','3p3','3q3','3r3','3s3','3t3'
    #,'3a4','3b4','3c4','3d4','3e4','3f4','3g4'
    #,'3h4','3i4','3j4','3k4','3l4','3m4'
    #,'3n4','3o4','3p4','3q4','3r4','3s4','3t4'
    #,'3a5','3b5','3c5','3d5','3e5','3f5','3g5'
    #,'3h5','3i5','3j5','3k5','3l5','3m5'
    #,'3n5','3o5','3p5','3q5','3r5','3s5','3t5'
    #,'3a6','3b6','3c6','3d6','3e6','3f6','3g6'
    #,'3h6','3i6','3j6','3k6','3l6','3m6'
    #,'3n6','3o6','3p6','3q6','3r6','3s6','3t6'
    #,'3a7','3b7','3c7','3d7','3e7','3f7','3g7'
    #,'3h7','3i7','3j7','3k7','3l7','3m7'
    #,'3n7','3o7','3p7','3q7','3r7','3s7','3t7'
    #,'3a8','3b8','3c8','3d8','3e8','3f8','3g8'
    #,'3h8','3i8','3j8','3k8','3l8','3m8'
    #,'3n8','3o8','3p8','3q8','3r8','3s8','3t8'
    #,'3a9','3b9','3c9','3d9','3e9','3f9','3g9'
    #,'3h9','3i9','3j9','3k9','3l9','3m9'
    #,'3n9','3o9','3p9','3q9','3r9','3s9','3t9'
    #,'3a0','3b0','3c0','3d0','3e0','3f0','3g0'
    #,'3h0','3i0','3j0','3k0','3l0','3m0'
    #,'3n0','3o0','3p0','3q0','3r0','3s0','3t0'
    #,'3aa','3ba','3ca','3da','3ea','3fa','3ga'
    #,'3ha','3ia','3ja','3ka','3la','3ma'
    #,'3na','3oa','3pa','3qa','3ra','3sa','3ta'
    #,'3ab','3bb','3cb','3db','3eb','3fb','3gb'
    #,'3hb','3ib','3jb','3kb','3lb','3mb'
    #,'3nb','3ob','3pb','3qb','3rb','3sb','3tb'
    #,'3ac','3cc','3cc','3dc','3ec','3fc','3gc'
    #,'3hc','3ic','3jc','3kc','3lc','3mc'
    #,'3nc','3oc','3pc','3qc','3rc','3sc','3tc'
    #,'3ad','3bd','3cd','3dd','3ed','3fd','3gd'
    #,'3hd','3id','3jd','3kd','3ld','3md'
    #,'3nd','3od','3pd','3qd','3rd','3sd','3td'
    #,'3ae','3be','3ce','3de','3ee','3fe','3ge'
    #,'3he','3ie','3je','3ke','3le','3me'
    #,'3ne','3oe','3pe','3qe','3re','3se','3te'
    #,'3af','3bf','3cf','3df','3ef','3ff','3gf'
    #,'3hf','3if','3jf','3kf','3lf','3mf'
    #,'3nf','3of','3pf','3qf','3rf','3sf','3tf'
    #,'4a1','4b1','4c1','4d1','4e1','4f1','4g1'
    #,'4h1','4i1','4j1','4k1','4l1','4m1'
    #,'4n1','4o1','4p1','4q1','4r1','4s1','4t1'
    #,'4a2','4b2','4c2','4d2','4e2','4f2','4g2'
    #,'4h2','4i2','4j2','4k2','4l2','4m2'
    #,'4n2','4o2','4p2','4q2','4r2','4s2','4t2'
    #,'4a3','4b3','4c3','4d3','4e3','4f3','4g3'
    #,'4h3','4i3','4j3','4k3','4l3','4m3'
    #,'4n3','4o3','4p3','4q3','4r3','4s3','4t3'
    #,'4a4','4b4','4c4','4d4','4e4','4f4','4g4'
    #,'4h4','4i4','4j4','4k4','4l4','4m4'
    #,'4n4','4o4','4p4','4q4','4r4','4s4','4t4'
    #,'4a5','4b5','4c5','4d5','4e5','4f5','4g5'
    #,'4h5','4i5','4j5','4k5','4l5','4m5'
    #,'4n5','4o5','4p5','4q5','4r5','4s5','4t5'
    #,'4a6','4b6','4c6','4d6','4e6','4f6','4g6'
    #,'4h6','4i6','4j6','4k6','4l6','4m6'
    #,'4n6','4o6','4p6','4q6','4r6','4s6','4t6'
    #,'4a7','4b7','4c7','4d7','4e7','4f7','4g7'
    #,'4h7','4i7','4j7','4k7','4l7','4m7'
    #,'4n7','4o7','4p7','4q7','4r7','4s7','4t7'
    #,'4a8','4b8','4c8','4d8','4e8','4f8','4g8'
    #,'4h8','4i8','4j8','4k8','4l8','4m8'
    #,'4n8','4o8','4p8','4q8','4r8','4s8','4t8'
    #,'4a9','4b9','4c9','4d9','4e9','4f9','4g9'
    #,'4h9','4i9','4j9','4k9','4l9','4m9'
    #,'4n9','4o9','4p9','4q9','4r9','4s9','4t9'
    #,'4a0','4b0','4c0','4d0','4e0','4f0','4g0'
    #,'4h0','4i0','4j0','4k0','4l0','4m0'
    #,'4n0','4o0','4p0','4q0','4r0','4s0','4t0'
    #,'4aa','4ba','4ca','4da','4ea','4fa','4ga'
    #,'4ha','4ia','4ja','4ka','4la','4ma'
    #,'4na','4oa','4pa','4qa','4ra','4sa','4ta'
    #,'4ab','4bb','4cb','4db','4eb','4fb','4gb'
    #,'4hb','4ib','4jb','4kb','4lb','4mb'
    #,'4nb','4ob','4pb','4qb','4rb','4sb','4tb'
    #,'4ac','4cc','4cc','4dc','4ec','4fc','4gc'
    #,'4hc','4ic','4jc','4kc','4lc','4mc'
    #,'4nc','4oc','4pc','4qc','4rc','4sc','4tc'
    #,'4ad','4bd','4cd','4dd','4ed','4fd','4gd'
    #,'4hd','4id','4jd','4kd','4ld','4md'
    #,'4nd','4od','4pd','4qd','4rd','4sd','4td'
    #,'4ae','4be','4ce','4de','4ee','4fe','4ge'
    #,'4he','4ie','4je','4ke','4le','4me'
    #,'4ne','4oe','4pe','4qe','4re','4se','4te'
    #,'4af','4bf','4cf','4df','4ef','4ff','4gf'
    #,'4hf','4if','4jf','4kf','4lf','4mf'
    #,'4nf','4of','4pf','4qf','4rf','4sf','4tf'
    #,'5a1','5b1','5c1','5d1','5e1','5f1','5g1'
    #,'5h1','5i1','5j1','5k1','5l1','5m1'
    #,'5n1','5o1','5p1','5q1','5r1','5s1','5t1'
    #,'5a2','5b2','5c2','5d2','5e2','5f2','5g2'
    #,'5h2','5i2','5j2','5k2','5l2','5m2'
    #,'5n2','5o2','5p2','5q2','5r2','5s2','5t2'
    #,'5a3','5b3','5c3','5d3','5e3','5f3','5g3'
    #,'5h3','5i3','5j3','5k3','5l3','5m3'
    #,'5n3','5o3','5p3','5q3','5r3','5s3','5t3'
    #,'5a4','5b4','5c4','5d4','5e4','5f4','5g4'
    #,'5h4','5i4','5j4','5k4','5l4','5m4'
    #,'5n4','5o4','5p4','5q4','5r4','5s4','5t4'
    #,'5a5','5b5','5c5','5d5','5e5','5f5','5g5'
    #,'5h5','5i5','5j5','5k5','5l5','5m5'
    #,'5n5','5o5','5p5','5q5','5r5','5s5','5t5'
    #,'5a6','5b6','5c6','5d6','5e6','5f6','5g6'
    #,'5h6','5i6','5j6','5k6','5l6','5m6'
    #,'5n6','5o6','5p6','5q6','5r6','5s6','5t6'
    #,'5a7','5b7','5c7','5d7','5e7','5f7','5g7'
    #,'5h7','5i7','5j7','5k7','5l7','5m7'
    #,'5n7','5o7','5p7','5q7','5r7','5s7','5t7'
    #,'5a8','5b8','5c8','5d8','5e8','5f8','5g8'
    #,'5h8','5i8','5j8','5k8','5l8','5m8'
    #,'5n8','5o8','5p8','5q8','5r8','5s8','5t8'
    #,'5a9','5b9','5c9','5d9','5e9','5f9','5g9'
    #,'5h9','5i9','5j9','5k9','5l9','5m9'
    #,'5n9','5o9','5p9','5q9','5r9','5s9','5t9'
    #,'5a0','5b0','5c0','5d0','5e0','5f0','5g0'
    #,'5h0','5i0','5j0','5k0','5l0','5m0'
    #,'5n0','5o0','5p0','5q0','5r0','5s0','5t0'
    #,'5aa','5ba','5ca','5da','5ea','5fa','5ga'
    #,'5ha','5ia','5ja','5ka','5la','5ma'
    #,'5na','5oa','5pa','5qa','5ra','5sa','5ta'
    #,'5ab','5bb','5cb','5db','5eb','5fb','5gb'
    #,'5hb','5ib','5jb','5kb','5lb','5mb'
    #,'5nb','5ob','5pb','5qb','5rb','5sb','5tb'
    #,'5ac','5cc','5cc','5dc','5ec','5fc','5gc'
    #,'5hc','5ic','5jc','5kc','5lc','5mc'
    #,'5nc','5oc','5pc','5qc','5rc','5sc','5tc'
    #,'5ad','5bd','5cd','5dd','5ed','5fd','5gd'
    #,'5hd','5id','5jd','5kd','5ld','5md'
    #,'5nd','5od','5pd','5qd','5rd','5sd','5td'
    #,'5ae','5be','5ce','5de','5ee','5fe','5ge'
    #,'5he','5ie','5je','5ke','5le','5me'
    #,'5ne','5oe','5pe','5qe','5re','5se','5te'
    #,'5af','5bf','5cf','5df','5ef','5ff','5gf'
    #,'5hf','5if','5jf','5kf','5lf','5mf'
    #,'5nf','5of','5pf','5qf','5rf','5sf','5tf'
    #,'POWER MODULE'
    #,'6a1','6b1','6c1','6d1','6e1','6f1','6g1'
    #,'6h1','6i1','6j1','6k1','6l1','6m1'
    #,'6n1','6o1','6p1','6q1','6r1','6s1','6t1'
    #,'6a2','6b2','6c2','6d2','6e2','6f2','6g2'
    #,'6h2','6i2','6j2','6k2','6l2','6m2'
    #,'6n2','6o2','6p2','6q2','6r2','6s2','6t2'
    #,'6a3','6b3','6c3','6d3','6e3','6f3','6g3'
    #,'6h3','6i3','6j3','6k3','6l3','6m3'
    #,'6n3','6o3','6p3','6q3','6r3','6s3','6t3'
    #,'6a4','6b4','6c4','6d4','6e4','6f4','6g4'
    #,'6h4','6i4','6j4','6k4','6l4','6m4'
    #,'6n4','6o4','6p4','6q4','6r4','6s4','6t4'
    #,'6a5','6b5','6c5','6d5','6e5','6f5','6g5'
    #,'6h5','6i5','6j5','6k5','6l5','6m5'
    #,'6n5','6o5','6p5','6q5','6r5','6s5','6t5'
    #,'6a6','6b6','6c6','6d6','6e6','6f6','6g6'
    #,'6h6','6i6','6j6','6k6','6l6','6m6'
    #,'6n6','6o6','6p6','6q6','6r6','6s6','6t6'
    #,'6a7','6b7','6c7','6d7','6e7','6f7','6g7'
    #,'6h7','6i7','6j7','6k7','6l7','6m7'
    #,'6n7','6o7','6p7','6q7','6r7','6s7','6t7'
    #,'6a8','6b8','6c8','6d8','6e8','6f8','6g8'
    #,'6h8','6i8','6j8','6k8','6l8','6m8'
    #,'6n8','6o8','6p8','6q8','6r8','6s8','6t8'
    #,'6a9','6b9','6c9','6d9','6e9','6f9','6g9'
    #,'6h9','6i9','6j9','6k9','6l9','6m9'
    #,'6n9','6o9','6p9','6q9','6r9','6s9','6t9'
    #,'6a0','6b0','6c0','6d0','6e0','6f0','6g0'
    #,'6h0','6i0','6j0','6k0','6l0','6m0'
    #,'6n0','6o0','6p0','6q0','6r0','6s0','6t0'
    #,'6aa','6ba','6ca','6da','6ea','6fa','6ga'
    #,'6ha','6ia','6ja','6ka','6la','6ma'
    #,'6na','6oa','6pa','6qa','6ra','6sa','6ta'
    #,'6ab','6bb','6cb','6db','6eb','6fb','6gb'
    #,'6hb','6ib','6jb','6kb','6lb','6mb'
    #,'6nb','6ob','6pb','6qb','6rb','6sb','6tb'
    #,'6ac','6cc','6cc','6dc','6ec','6fc','6gc'
    #,'6hc','6ic','6jc','6kc','6lc','6mc'
    #,'6nc','6oc','6pc','6qc','6rc','6sc','6tc'
    #,'6ad','6bd','6cd','6dd','6ed','6fd','6gd'
    #,'6hd','6id','6jd','6kd','6ld','6md'
    #,'6nd','6od','6pd','6qd','6rd','6sd','6td'
    #,'6ae','6be','6ce','6de','6ee','6fe','6ge'
    #,'6he','6ie','6je','6ke','6le','6me'
    #,'6ne','6oe','6pe','6qe','6re','6se','6te'
    #,'6af','6bf','6cf','6df','6ef','6ff','6gf'
    #,'6hf','6if','6jf','6kf','6lf','6mf'
    #,'6nf','6of','6pf','6qf','6rf','6sf','6tf'
    #,'7a1','7b1','7c1','7d1','7e1','7f1','7g1'
    #,'7h1','7i1','7j1','7k1','7l1','7m1'
    #,'7n1','7o1','7p1','7q1','7r1','7s1','7t1'
    #,'7a2','7b2','7c2','7d2','7e2','7f2','7g2'
    #,'7h2','7i2','7j2','7k2','7l2','7m2'
    #,'7n2','7o2','7p2','7q2','7r2','7s2','7t2'
    #,'7a3','7b3','7c3','7d3','7e3','7f3','7g3'
    #,'7h3','7i3','7j3','7k3','7l3','7m3'
    #,'7n3','7o3','7p3','7q3','7r3','7s3','7t3'
    #,'7a4','7b4','7c4','7d4','7e4','7f4','7g4'
    #,'7h4','7i4','7j4','7k4','7l4','7m4'
    #,'7n4','7o4','7p4','7q4','7r4','7s4','7t4'
    #,'7a5','7b5','7c5','7d5','7e5','7f5','7g5'
    #,'7h5','7i5','7j5','7k5','7l5','7m5'
    #,'7n5','7o5','7p5','7q5','7r5','7s5','7t5'
    #,'7a6','7b6','7c6','7d6','7e6','7f6','7g6'
    #,'7h6','7i6','7j6','7k6','7l6','7m6'
    #,'7n6','7o6','7p6','7q6','7r6','7s6','7t6'
    #,'7a7','7b7','7c7','7d7','7e7','7f7','7g7'
    #,'7h7','7i7','7j7','7k7','7l7','7m7'
    #,'7n7','7o7','7p7','7q7','7r7','7s7','7t7'
    #,'7a8','7b8','7c8','7d8','7e8','7f8','7g8'
    #,'7h8','7i8','7j8','7k8','7l8','7m8'
    #,'7n8','7o8','7p8','7q8','7r8','7s8','7t8'
    #,'7a9','7b9','7c9','7d9','7e9','7f9','7g9'
    #,'7h9','7i9','7j9','7k9','7l9','7m9'
    #,'7n9','7o9','7p9','7q9','7r9','7s9','7t9'
    #,'7a0','7b0','7c0','7d0','7e0','7f0','7g0'
    #,'7h0','7i0','7j0','7k0','7l0','7m0'
    #,'7n0','7o0','7p0','7q0','7r0','7s0','7t0'
    #,'7aa','7ba','7ca','7da','7ea','7fa','7ga'
    #,'7ha','7ia','7ja','7ka','7la','7ma'
    #,'7na','7oa','7pa','7qa','7ra','7sa','7ta'
    #,'7ab','7bb','7cb','7db','7eb','7fb','7gb'
    #,'7hb','7ib','7jb','7kb','7lb','7mb'
    #,'7nb','7ob','7pb','7qb','7rb','7sb','7tb'
    #,'7ac','7cc','7cc','7dc','7ec','7fc','7gc'
    #,'7hc','7ic','7jc','7kc','7lc','7mc'
    #,'7nc','7oc','7pc','7qc','7rc','7sc','7tc'
    #,'7ad','7bd','7cd','7dd','7ed','7fd','7gd'
    #,'7hd','7id','7jd','7kd','7ld','7md'
    #,'7nd','7od','7pd','7qd','7rd','7sd','7td'
    #,'7ae','7be','7ce','7de','7ee','7fe','7ge'
    #,'7he','7ie','7je','7ke','7le','7me'
    #,'7ne','7oe','7pe','7qe','7re','7se','7te'
    #,'7af','7bf','7cf','7df','7ef','7ff','7gf'
    #,'7hf','7if','7jf','7kf','7lf','7mf'
    #,'7nf','7of','7pf','7qf','7rf','7sf','7tf'
    #,'8a1','8b1','8c1','8d1','8e1','8f1','8g1'
    #,'8h1','8i1','8j1','8k1','8l1','8m1'
    #,'8n1','8o1','8p1','8q1','8r1','8s1','8t1'
    #,'8a2','8b2','8c2','8d2','8e2','8f2','8g2'
    #,'8h2','8i2','8j2','8k2','8l2','8m2'
    #,'8n2','8o2','8p2','8q2','8r2','8s2','8t2'
    #,'8a3','8b3','8c3','8d3','8e3','8f3','8g3'
    #,'8h3','8i3','8j3','8k3','8l3','8m3'
    #,'8n3','8o3','8p3','8q3','8r3','8s3','8t3'
    #,'8a4','8b4','8c4','8d4','8e4','8f4','8g4'
    #,'8h4','8i4','8j4','8k4','8l4','8m4'
    #,'8n4','8o4','8p4','8q4','8r4','8s4','8t4'
    #,'8a5','8b5','8c5','8d5','8e5','8f5','8g5'
    #,'8h5','8i5','8j5','8k5','8l5','8m5'
    #,'8n5','8o5','8p5','8q5','8r5','8s5','8t5'
    #,'8a6','8b6','8c6','8d6','8e6','8f6','8g6'
    #,'8h6','8i6','8j6','8k6','8l6','8m6'
    #,'8n6','8o6','8p6','8q6','8r6','8s6','8t6'
    #,'8a7','8b7','8c7','8d7','8e7','8f7','8g7'
    #,'8h7','8i7','8j7','8k7','8l7','8m7'
    #,'8n7','8o7','8p7','8q7','8r7','8s7','8t7'
    #,'8a8','8b8','8c8','8d8','8e8','8f8','8g8'
    #,'8h8','8i8','8j8','8k8','8l8','8m8'
    #,'8n8','8o8','8p8','8q8','8r8','8s8','8t8'
    #,'8a9','8b9','8c9','8d9','8e9','8f9','8g9'
    #,'8h9','8i9','8j9','8k9','8l9','8m9'
    #,'8n9','8o9','8p9','8q9','8r9','8s9','8t9'
    #,'8a0','8b0','8c0','8d0','8e0','8f0','8g0'
    #,'8h0','8i0','8j0','8k0','8l0','8m0'
    #,'8n0','8o0','8p0','8q0','8r0','8s0','8t0'
    #,'8aa','8ba','8ca','8da','8ea','8fa','8ga'
    #,'8ha','8ia','8ja','8ka','8la','8ma'
    #,'8na','8oa','8pa','8qa','8ra','8sa','8ta'
    #,'8ab','8bb','8cb','8db','8eb','8fb','8gb'
    #,'8hb','8ib','8jb','8kb','8lb','8mb'
    #,'8nb','8ob','8pb','8qb','8rb','8sb','8tb'
    #,'8ac','8cc','8cc','8dc','8ec','8fc','8gc'
    #,'8hc','8ic','8jc','8kc','8lc','8mc'
    #,'8nc','8oc','8pc','8qc','8rc','8sc','8tc'
    #,'8ad','8bd','8cd','8dd','8ed','8fd','8gd'
    #,'8hd','8id','8jd','8kd','8ld','8md'
    #,'8nd','8od','8pd','8qd','8rd','8sd','8td'
    #,'8ae','8be','8ce','8de','8ee','8fe','8ge'
    #,'8he','8ie','8je','8ke','8le','8me'
    #,'8ne','8oe','8pe','8qe','8re','8se','8te'
    #,'8af','8bf','8cf','8df','8ef','8ff','8gf'
    #,'8hf','8if','8jf','8kf','8lf','8mf'
    #,'8nf','8of','8pf','8qf','8rf','8sf','8tf'
    #,'9a1','9b1','9c1','9d1','9e1','9f1','9g1'
    #,'9h1','9i1','9j1','9k1','9l1','9m1'
    #,'9n1','9o1','9p1','9q1','9r1','9s1','9t1'
    #,'9a2','9b2','9c2','9d2','9e2','9f2','9g2'
    #,'9h2','9i2','9j2','9k2','9l2','9m2'
    #,'9n2','9o2','9p2','9q2','9r2','9s2','9t2'
    #,'9a3','9b3','9c3','9d3','9e3','9f3','9g3'
    #,'9h3','9i3','9j3','9k3','9l3','9m3'
    #,'9n3','9o3','9p3','9q3','9r3','9s3','9t3'
    #,'9a4','9b4','9c4','9d4','9e4','9f4','9g4'
    #,'9h4','9i4','9j4','9k4','9l4','9m4'
    #,'9n4','9o4','9p4','9q4','9r4','9s4','9t4'
    #,'9a5','9b5','9c5','9d5','9e5','9f5','9g5'
    #,'9h5','9i5','9j5','9k5','9l5','9m5'
    #,'9n5','9o5','9p5','9q5','9r5','9s5','9t5'
    #,'9a6','9b6','9c6','9d6','9e6','9f6','9g6'
    #,'9h6','9i6','9j6','9k6','9l6','9m6'
    #,'9n6','9o6','9p6','9q6','9r6','9s6','9t6'
    #,'9a7','9b7','9c7','9d7','9e7','9f7','9g7'
    #,'9h7','9i7','9j7','9k7','9l7','9m7'
    #,'9n7','9o7','9p7','9q7','9r7','9s7','9t7'
    #,'9a8','9b8','9c8','9d8','9e8','9f8','9g8'
    #,'9h8','9i8','9j8','9k8','9l8','9m8'
    #,'9n8','9o8','9p8','9q8','9r8','9s8','9t8'
    #,'9a9','9b9','9c9','9d9','9e9','9f9','9g9'
    #,'9h9','9i9','9j9','9k9','9l9','9m9'
    #,'9n9','9o9','9p9','9q9','9r9','9s9','9t9'
    #,'9a0','9b0','9c0','9d0','9e0','9f0','9g0'
    #,'9h0','9i0','9j0','9k0','9l0','9m0'
    #,'9n0','9o0','9p0','9q0','9r0','9s0','9t0'
    #,'9aa','9ba','9ca','9da','9ea','9fa','9ga'
    #,'9ha','9ia','9ja','9ka','9la','9ma'
    #,'9na','9oa','9pa','9qa','9ra','9sa','9ta'
    #,'9ab','9bb','9cb','9db','9eb','9fb','9gb'
    #,'9hb','9ib','9jb','9kb','9lb','9mb'
    #,'9nb','9ob','9pb','9qb','9rb','9sb','9tb'
    #,'9ac','9cc','9cc','9dc','9ec','9fc','9gc'
    #,'9hc','9ic','9jc','9kc','9lc','9mc'
    #,'9nc','9oc','9pc','9qc','9rc','9sc','9tc'
    #,'9ad','9bd','9cd','9dd','9ed','9fd','9gd'
    #,'9hd','9id','9jd','9kd','9ld','9md'
    #,'9nd','9od','9pd','9qd','9rd','9sd','9td'
    #,'9ae','9be','9ce','9de','9ee','9fe','9ge'
    #,'9he','9ie','9je','9ke','9le','9me'
    #,'9ne','9oe','9pe','9qe','9re','9se','9te'
    #,'9af','9bf','9cf','9df','9ef','9ff','9gf'
    #,'9hf','9if','9jf','9kf','9lf','9mf'
    #,'9nf','9of','9pf','9qf','9rf','9sf','9tf'
    #,'DECIMAL ARITH'
    #)
    #;
    
    _testmgr.testcase_end(desc)

def test022(desc="""n05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt110 : A05
    #  Description:        Large number of COLUMNs referenced
    #                      (normalizer stores totals).
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    #
    #  ---------------------------------
    #  Create the Log file.
    #  ---------------------------------
    #  ---------------------------------
    #  Set up default catalog and schema
    #  ---------------------------------
    # set catalog eval;
    # set schema  eval.gdb;
    #
    #
    
    stmt = """SELECT a.pic_x_1
FROM   """ + gvars.g_schema_arkcasedb + """.btsel01 a
--  Compare columns for all tables:
WHERE
--  Compare columns for a:
( a.char_1             = 'Z' )
OR ( a.char_10            = 'Z' )
OR ( a.pic_x_1            = 'Z' )
OR ( a.pic_x_7            = 'Z' )
OR ( a.pic_x_long         = 'Z' )
OR ( a.var_char           = 'Z' )
--  No numeric fields store the value 42:
OR ( a.binary_signed      = 42  )
OR ( a.binary_32_u        = 42  )
OR ( a.binary_64_s        = 42  )
OR ( a.pic_comp_1         = 42  )
OR ( a.pic_comp_2         = 42  )
OR ( a.pic_comp_3         = 42  )
OR ( a.small_int          = 42  )
OR ( a.medium_int         = 42  )
OR ( a.large_int          = 42  )
OR ( a.decimal_1          = 42  )
OR ( a.decimal_2_signed   = 42  )
OR ( a.decimal_3_unsigned = 42  )
OR ( a.pic_decimal_1      = 42  )
OR ( a.pic_decimal_2      = 42  )
OR ( a.pic_decimal_3      = 42  )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n05exp""", 'n05s0')
    
    stmt = """SELECT DISTINCT a.pic_x_1, b.pic_x_1
FROM   """ + gvars.g_schema_arkcasedb + """.btsel01 a
,""" + gvars.g_schema_arkcasedb + """.btsel01 b
--  Compare columns for all tables:
WHERE  a.pic_x_1            = b.pic_x_1
AND (
( a.pic_x_1            = 'Z' )
--  Compare columns for a:
OR ( a.char_1             = 'Z' )
OR ( a.char_10            = 'Z' )
--        a.pic_x_1 checked above
OR ( a.pic_x_7            = 'Z' )
OR ( a.pic_x_long         = 'Z' )
OR ( a.var_char           = 'Z' )
--  Note: No numeric fields store the value 42:
OR ( a.binary_signed      = 42  )
OR ( a.binary_32_u        = 42  )
OR ( a.binary_64_s        = 42  )
OR ( a.pic_comp_1         = 42  )
OR ( a.pic_comp_2         = 42  )
OR ( a.pic_comp_3         = 42  )
OR ( a.small_int          = 42  )
OR ( a.medium_int         = 42  )
OR ( a.large_int          = 42  )
OR ( a.decimal_1          = 42  )
OR ( a.decimal_2_signed   = 42  )
OR ( a.decimal_3_unsigned = 42  )
OR ( a.pic_decimal_1      = 42  )
OR ( a.pic_decimal_2      = 42  )
OR ( a.pic_decimal_3      = 42  )
--  Compare columns for b:
AND (b.char_1             = 'Z' )
OR ( b.char_10            = 'Z' )
--   b.pic_x_1 checked above
OR ( b.pic_x_7            = 'Z' )
OR ( b.pic_x_long         = 'Z' )
OR ( b.var_char           = 'Z' )
--  No numeric fields store the value 42:
OR ( b.binary_signed      = 42  )
OR ( b.binary_32_u        = 42  )
OR ( b.binary_64_s        = 42  )
OR ( b.pic_comp_1         = 42  )
OR ( b.pic_comp_2         = 42  )
OR ( b.pic_comp_3         = 42  )
OR ( b.small_int          = 42  )
OR ( b.medium_int         = 42  )
OR ( b.large_int          = 42  )
OR ( b.decimal_1          = 42  )
OR ( b.decimal_2_signed   = 42  )
OR ( b.decimal_3_unsigned = 42  )
OR ( b.pic_decimal_1      = 42  )
OR ( b.pic_decimal_2      = 42  )
OR ( b.pic_decimal_3      = 42  )
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n05exp""", 'n05s1')
    
    stmt = """SELECT DISTINCT a.pic_x_1, b.pic_x_1, c.pic_x_1
FROM        """ + gvars.g_schema_arkcasedb + """.btsel01 a
, """ + gvars.g_schema_arkcasedb + """.btsel01 b
, """ + gvars.g_schema_arkcasedb + """.btsel01 c
-- Compare columns for all tables:
WHERE a.pic_x_1            = b.pic_x_1
AND ( a.pic_x_1            = c.pic_x_1 )
AND (
( a.pic_x_1            = 'Z' )
-- Compare columns for a:
OR ( a.char_1             = 'Z' )
OR ( a.char_10            = 'Z' )
--       a.pic_x_1 checked above
OR ( a.pic_x_7            = 'Z' )
OR ( a.pic_x_long         = 'Z' )
OR ( a.var_char           = 'Z' )
-- Note: No numeric fields store the value 42
OR ( a.binary_signed      = 42  )
OR ( a.binary_32_u        = 42  )
OR ( a.binary_64_s        = 42  )
OR ( a.pic_comp_1         = 42  )
OR ( a.pic_comp_2         = 42  )
OR ( a.pic_comp_3         = 42  )
OR ( a.small_int          = 42  )
OR ( a.medium_int         = 42  )
OR ( a.large_int          = 42  )
OR ( a.decimal_1          = 42  )
OR ( a.decimal_2_signed   = 42  )
OR ( a.decimal_3_unsigned = 42  )
OR ( a.pic_decimal_1      = 42  )
OR ( a.pic_decimal_2      = 42  )
OR ( a.pic_decimal_3      = 42  )
-- Compare columns for b:
OR  (b.char_1             = 'Z' )
OR ( b.char_10            = 'Z' )
--       b.pic_x_1 checked above implicitly.
OR ( b.pic_x_7            = 'Z' )
OR ( b.pic_x_long         = 'Z' )
OR ( b.var_char           = 'Z' )
-- No numeric fields store the value 42:
OR ( b.binary_signed      = 42  )
OR ( b.binary_32_u        = 42  )
OR ( b.binary_64_s        = 42  )
OR ( b.pic_comp_1         = 42  )
OR ( b.pic_comp_2         = 42  )
OR ( b.pic_comp_3         = 42  )
OR ( b.small_int          = 42  )
OR ( b.medium_int         = 42  )
OR ( b.large_int          = 42  )
OR ( b.decimal_1          = 42  )
OR ( b.decimal_2_signed   = 42  )
OR ( b.decimal_3_unsigned = 42  )
OR ( b.pic_decimal_1      = 42  )
OR ( b.pic_decimal_2      = 42  )
OR ( b.pic_decimal_3      = 42  )
-- Compare columns for c:
OR  (c.char_1             = 'Z' )
OR ( c.char_10            = 'Z' )
--       c.pic_x_1 checked above implicitly.
OR ( c.pic_x_7            = 'Z' )
OR ( c.pic_x_long         = 'Z' )
OR ( c.var_char           = 'Z' )
-- No numeric fields store the value 42:
OR ( c.binary_signed      = 42  )
OR ( c.binary_32_u        = 42  )
OR ( c.binary_64_s        = 42  )
OR ( c.pic_comp_1         = 42  )
OR ( c.pic_comp_2         = 42  )
OR ( c.pic_comp_3         = 42  )
OR ( c.small_int          = 42  )
OR ( c.medium_int         = 42  )
OR ( c.large_int          = 42  )
OR ( c.decimal_1          = 42  )
OR ( c.decimal_2_signed   = 42  )
OR ( c.decimal_3_unsigned = 42  )
OR ( c.pic_decimal_1      = 42  )
OR ( c.pic_decimal_2      = 42  )
OR ( c.pic_decimal_3      = 42  )
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n05exp""", 'n05s2')
    
    _testmgr.testcase_end(desc)

def test023(desc="""n07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     arkt0110 : N07
    #  Description:        Stuff split off from testa07, never finishes
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    #
    # ---------------------------------
    # Create the Log file.
    # ---------------------------------
    # ---------------------------------
    # Set up default catalog and schema
    # ---------------------------------
    #set catalog eval;
    #set schema  eval.gdb;
    #
    #
    #  Get to the volume where the catalog is, to avoid multiple
    #  volume specifications:
    #  VOLUME <subvol_for_temporary_data>;
    
    # Copy global table to local version and add lots of indices:
    #    DUP btsel01, L6table
    #    CATALOG <subvol_for_temporary_data>;
    
    stmt = """create table L6table (
-- --Fixed length character string
char_1                 char(1)        default ' ' not null
, char_10                char(10)       default ' ' not null
, pic_x_1                pic x(1)       default ' ' not null
, pic_x_7                pic x(7)       default ' ' not null
, pic_x_long             picture x(200) default ' ' not null
--                                pic x(200)     not null
-- --Varying length character string.
, var_char               varchar(253)   default ' ' not null
-- --Binary
, binary_signed          numeric (4,0) signed    default 0 not null
, binary_32_u            numeric (9,2) unsigned  default 0 not null
, binary_64_s            numeric (18,3) signed   default 0 not null
, pic_comp_1             numeric (10,0) signed   default 0 not null
, pic_comp_2             numeric (2,2)  signed   default 0 not null
, pic_comp_3             numeric (8,5)  signed   default 0 not null    

, small_int              smallint                default 0 not null
, medium_int             integer unsigned        default 0 not null
, large_int              largeint signed         default 0 not null
-- --Fixed length character string
, decimal_1              decimal (1,0) unsigned  default 0 not null
, decimal_2_signed       decimal (2,2) signed    default 0 not null
, decimal_3_unsigned     decimal (3,0) unsigned  default 0 not null
, pic_decimal_1          pic s9(1)v9(1)          default 0 not null
--                                numeric (2,1) signed   not null
, pic_decimal_2          picture v9(3)          default 0 not null
--                                numeric (3,3) unsigned not null
, pic_decimal_3          pic s9                 default 0 not null
--                                numeric (1,0) signed   not null
-- --End of columns
, primary key  ( binary_signed )
)
store by primary key
location """ + gvars.g_disc6 + """
attributes
--         audit
blocksize 4096
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # --Index the table with simple, 1-column indexes:
    stmt = """create index L6tablea on L6table ( pic_x_1 )
location """ + gvars.g_disc9 + """
attributes blocksize 4096
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index L6tableb on L6table ( decimal_2_signed )
location """ + gvars.g_disc4 + """
attributes blocksize 4096
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index L6tablec on L6table ( pic_comp_3 )
location """ + gvars.g_disc3 + """
attributes blocksize 4096
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index L6tabled on L6table ( pic_x_long )
location """ + gvars.g_disc2 + """
attributes blocksize 4096
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #
    
    # These indexes are created, but never used, not sure why created
    # Table L6table is similar to btsel01, maybe everything was copied
    
    # -- Make 25 indexes:
    stmt = """CREATE INDEX L6indexa ON L6table ( char_1  );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexb ON L6table ( char_10 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexc ON L6table ( pic_x_1 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexd ON L6table ( pic_x_7 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexe ON L6table ( pic_x_long );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #  Var_char is too long to be an index.
    stmt = """CREATE INDEX L6indexf ON L6table ( var_char );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexg ON L6table ( binary_signed );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexh ON L6table ( binary_32_u   );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexi ON L6table ( binary_64_s   );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexj ON L6table ( pic_comp_1    );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexk ON L6table ( pic_comp_2    );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexl ON L6table ( pic_comp_3    );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexm ON L6table ( small_int     );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexn ON L6table ( medium_int    );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexo ON L6table ( large_int     );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexp ON L6table ( decimal_1     );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexq ON L6table ( decimal_2_signed );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexr ON L6table ( decimal_3_unsigned );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexs ON L6table ( pic_decimal_1 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indext ON L6table ( pic_decimal_2 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexu ON L6table ( pic_decimal_3 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexv ON L6table ( pic_decimal_3 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexw ON L6table ( pic_decimal_3 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexx ON L6table ( pic_decimal_3 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexy ON L6table ( pic_decimal_3 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """CREATE INDEX L6indexz ON L6table ( pic_decimal_3 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #DUP btsel01, L6table;
    #
    stmt = """insert into L6table values ('A','steven','C','walter','bob',
'B',50,50,200,50,0.12,100.9,
10,10000,1000000000,4,.5,90,
1.1,0.1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into L6table values ('A','bobby','A','bobby','bop',
'B',60,60,1200,60,0.79,100.99,
1000,8000,-1000,5,.6,100,
2.1,0.2,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into L6table values ('D','steven','B','9','bat','thomas',
8000,70,2000,500,0.10,100.999,
90,10000,1000,7,.7,110,
3.1,0.3,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into L6table values ('D','melissa','C','7','pop','jimmy',
1000,80,1500,500,0.20,100.9999,
80,9000,999,5,.8,120,
4.1,0.4,4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into L6table values ('E','monica','Q','sue','pat',
'christopher',
2000,90,1200,3000,0.30,100.99999,
2000,8000,-1000000,1,.9,80,
5.1,0.5,5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into L6table values ('D','michelle','D','michael','rat',
'thomas',
-5000,90,2000,500,0.40,100.8,
90,8000,200,7,.93,140,
6.1,0.6,6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into L6table values ('C','maureen','E','jimmy','rum',
'marilyn',
3000,80,2000,500,0.50,100.7,
9000,1000,2000,8,.97,150,
7.1, 0.7,7);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into L6table values ('C','marcia','Z','johnny','dum',
'thomas',
4000,40,2000,50,0.60,100.6,
8000,5000,0,9,.99,110,
8.1,0.8,8);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #   Lots of PREDICATEs (105) involving more than one table.
    stmt = """SELECT a.char_1, b.char_10, c.char_1, d.char_10, e.pic_x_1
FROM L6table a
, L6table b
, L6table c
, L6table d
, L6table e
--  Compare columns for a and b:
WHERE a.char_1             = b.char_1
AND ( a.char_10            = b.char_10            )
AND ( a.pic_x_1            = b.pic_x_1            )
AND ( a.pic_x_7            = b.pic_x_7            )
AND ( a.pic_x_long         = b.pic_x_long         )
AND ( a.var_char           = b.var_char           )
AND ( a.binary_signed      = b.binary_signed      )
AND ( a.binary_32_u        = b.binary_32_u        )
AND ( a.binary_64_s        = b.binary_64_s        )
AND ( a.pic_comp_1         = b.pic_comp_1         )
AND ( a.pic_comp_2         = b.pic_comp_2         )
AND ( a.pic_comp_3         = b.pic_comp_3         )
AND ( a.small_int          = b.small_int          )
AND ( a.medium_int         = b.medium_int         )
AND ( a.large_int          = b.large_int          )
AND ( a.decimal_1          = b.decimal_1          )
AND ( a.decimal_2_signed   = b.decimal_2_signed   )
AND ( a.decimal_3_unsigned = b.decimal_3_unsigned )
AND ( a.pic_decimal_1      = b.pic_decimal_1      )
AND ( a.pic_decimal_2      = b.pic_decimal_2      )
AND ( a.pic_decimal_3      = b.pic_decimal_3      )
--  Compare columns for a and c:
AND ( a.char_1             = c.char_1             )
AND ( a.char_10            = c.char_10            )
AND ( a.pic_x_1            = c.pic_x_1            )
AND ( a.pic_x_7            = c.pic_x_7            )
AND ( a.pic_x_long         = c.pic_x_long         )
AND ( a.var_char           = c.var_char           )
AND ( a.binary_signed      = c.binary_signed      )
AND ( a.binary_32_u        = c.binary_32_u        )
AND ( a.binary_64_s        = c.binary_64_s        )
AND ( a.pic_comp_1         = c.pic_comp_1         )
AND ( a.pic_comp_2         = c.pic_comp_2         )
AND ( a.pic_comp_3         = c.pic_comp_3         )
AND ( a.small_int          = c.small_int          )
AND ( a.medium_int         = c.medium_int         )
AND ( a.large_int          = c.large_int          )
AND ( a.decimal_1          = c.decimal_1          )
AND ( a.decimal_2_signed   = c.decimal_2_signed   )
AND ( a.decimal_3_unsigned = c.decimal_3_unsigned )
AND ( a.pic_decimal_1      = c.pic_decimal_1      )
AND ( a.pic_decimal_2      = c.pic_decimal_2      )
AND ( a.pic_decimal_3      = c.pic_decimal_3      )
--  Compare columns for b and c:
AND ( b.char_1             = c.char_1             )
AND ( b.char_10            = c.char_10            )
AND ( b.pic_x_1            = c.pic_x_1            )
AND ( b.pic_x_7            = c.pic_x_7            )
AND ( b.pic_x_long         = c.pic_x_long         )
AND ( b.var_char           = c.var_char           )
AND ( b.binary_signed      = c.binary_signed      )
AND ( b.binary_32_u        = c.binary_32_u        )
AND ( b.binary_64_s        = c.binary_64_s        )
AND ( b.pic_comp_1         = c.pic_comp_1         )
AND ( b.pic_comp_2         = c.pic_comp_2         )
AND ( b.pic_comp_3         = c.pic_comp_3         )
AND ( b.small_int          = c.small_int          )
AND ( b.medium_int         = c.medium_int         )
AND ( b.large_int          = c.large_int          )
AND ( b.decimal_1          = c.decimal_1          )
AND ( b.decimal_2_signed   = c.decimal_2_signed   )
AND ( b.decimal_3_unsigned = c.decimal_3_unsigned )
AND ( b.pic_decimal_1      = c.pic_decimal_1      )
AND ( b.pic_decimal_2      = c.pic_decimal_2      )
--  Compare columns for a and d:
AND ( a.char_1             = d.char_1             )
AND ( a.char_10            = d.char_10            )
AND ( a.pic_x_1            = d.pic_x_1            )
AND ( a.pic_x_7            = d.pic_x_7            )
AND ( a.pic_x_long         = d.pic_x_long         )
AND ( a.var_char           = d.var_char           )
AND ( a.binary_signed      = d.binary_signed      )
AND ( a.binary_32_u        = d.binary_32_u        )
AND ( a.binary_64_s        = d.binary_64_s        )
AND ( a.pic_comp_1         = d.pic_comp_1         )
AND ( a.pic_comp_2         = d.pic_comp_2         )
AND ( a.pic_comp_3         = d.pic_comp_3         )
AND ( a.small_int          = d.small_int          )
AND ( a.medium_int         = d.medium_int         )
AND ( a.large_int          = d.large_int          )
AND ( a.decimal_1          = d.decimal_1          )
AND ( a.decimal_2_signed   = d.decimal_2_signed   )
AND ( a.decimal_3_unsigned = d.decimal_3_unsigned )
AND ( a.pic_decimal_1      = d.pic_decimal_1      )
AND ( a.pic_decimal_2      = d.pic_decimal_2      )
AND ( a.pic_decimal_3      = d.pic_decimal_3      )
--  Compare columns for a and e:
AND ( a.char_1             = e.char_1             )
AND ( a.char_10            = e.char_10            )
AND ( a.pic_x_1            = e.pic_x_1            )
AND ( a.pic_x_7            = e.pic_x_7            )
AND ( a.pic_x_long         = e.pic_x_long         )
AND ( a.var_char           = e.var_char           )
AND ( a.binary_signed      = e.binary_signed      )
AND ( a.binary_32_u        = e.binary_32_u        )
AND ( a.binary_64_s        = e.binary_64_s        )
AND ( a.pic_comp_1         = e.pic_comp_1         )
AND ( a.pic_comp_2         = e.pic_comp_2         )
AND ( a.pic_comp_3         = e.pic_comp_3         )
AND ( a.small_int          = e.small_int          )
AND ( a.medium_int         = e.medium_int         )
AND ( a.large_int          = e.large_int          )
AND ( a.decimal_1          = e.decimal_1          )
AND ( a.decimal_2_signed   = e.decimal_2_signed   )
AND ( a.decimal_3_unsigned = e.decimal_3_unsigned )
AND ( a.pic_decimal_1      = e.pic_decimal_1      )
AND ( a.pic_decimal_2      = e.pic_decimal_2      )
AND ( a.pic_decimal_3      = e.pic_decimal_3      )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n07exp""", 'n07s0')
    
    #   Lots of PREDICATEs (210) involving more than one table.
    #   Since B41 get SQLCOMP out of space with full extended segment.
    stmt = """SELECT a.char_1, b.char_10, c.char_1, d.char_10, e.pic_x_1
, f.char_1, g.char_10, h.char_1, i.char_10, j.pic_x_1
FROM L6table a
, L6table b
, L6table c
, L6table d
, L6table e
, L6table f
, L6table g
, L6table h
, L6table i
, L6table j
--  Compare columns for a and b:
WHERE a.char_1             = b.char_1
AND ( a.char_10            = b.char_10            )
AND ( a.pic_x_1            = b.pic_x_1            )
AND ( a.pic_x_7            = b.pic_x_7            )
AND ( a.pic_x_long         = b.pic_x_long         )
AND ( a.var_char           = b.var_char           )
AND ( a.binary_signed      = b.binary_signed      )
AND ( a.binary_32_u        = b.binary_32_u        )
AND ( a.binary_64_s        = b.binary_64_s        )
AND ( a.pic_comp_1         = b.pic_comp_1         )
AND ( a.pic_comp_2         = b.pic_comp_2         )
AND ( a.pic_comp_3         = b.pic_comp_3         )
AND ( a.small_int          = b.small_int          )
AND ( a.medium_int         = b.medium_int         )
AND ( a.large_int          = b.large_int          )
AND ( a.decimal_1          = b.decimal_1          )
AND ( a.decimal_2_signed   = b.decimal_2_signed   )
AND ( a.decimal_3_unsigned = b.decimal_3_unsigned )
AND ( a.pic_decimal_1      = b.pic_decimal_1      )
AND ( a.pic_decimal_2      = b.pic_decimal_2      )
AND ( a.pic_decimal_3      = b.pic_decimal_3      )
--  Compare columns for a and c:
AND ( a.char_1             = c.char_1             )
AND ( a.char_10            = c.char_10            )
AND ( a.pic_x_1            = c.pic_x_1            )
AND ( a.pic_x_7            = c.pic_x_7            )
AND ( a.pic_x_long         = c.pic_x_long         )
AND ( a.var_char           = c.var_char           )
AND ( a.binary_signed      = c.binary_signed      )
AND ( a.binary_32_u        = c.binary_32_u        )
AND ( a.binary_64_s        = c.binary_64_s        )
AND ( a.pic_comp_1         = c.pic_comp_1         )
AND ( a.pic_comp_2         = c.pic_comp_2         )
AND ( a.pic_comp_3         = c.pic_comp_3         )
AND ( a.small_int          = c.small_int          )
AND ( a.medium_int         = c.medium_int         )
AND ( a.large_int          = c.large_int          )
AND ( a.decimal_1          = c.decimal_1          )
AND ( a.decimal_2_signed   = c.decimal_2_signed   )
AND ( a.decimal_3_unsigned = c.decimal_3_unsigned )
AND ( a.pic_decimal_1      = c.pic_decimal_1      )
AND ( a.pic_decimal_2      = c.pic_decimal_2      )
AND ( a.pic_decimal_3      = c.pic_decimal_3      )
--  Compare columns for b and c:
AND ( b.char_1             = c.char_1             )
AND ( b.char_10            = c.char_10            )
AND ( b.pic_x_1            = c.pic_x_1            )
AND ( b.pic_x_7            = c.pic_x_7            )
AND ( b.pic_x_long         = c.pic_x_long         )
AND ( b.var_char           = c.var_char           )
AND ( b.binary_signed      = c.binary_signed      )
AND ( b.binary_32_u        = c.binary_32_u        )
AND ( b.binary_64_s        = c.binary_64_s        )
AND ( b.pic_comp_1         = c.pic_comp_1         )
AND ( b.pic_comp_2         = c.pic_comp_2         )
AND ( b.pic_comp_3         = c.pic_comp_3         )
AND ( b.small_int          = c.small_int          )
AND ( b.medium_int         = c.medium_int         )
AND ( b.large_int          = c.large_int          )
AND ( b.decimal_1          = c.decimal_1          )
AND ( b.decimal_2_signed   = c.decimal_2_signed   )
AND ( b.decimal_3_unsigned = c.decimal_3_unsigned )
AND ( b.pic_decimal_1      = c.pic_decimal_1      )
AND ( b.pic_decimal_2      = c.pic_decimal_2      )
--  Compare columns for a and d:
AND ( a.char_1             = d.char_1             )
AND ( a.char_10            = d.char_10            )
AND ( a.pic_x_1            = d.pic_x_1            )
AND ( a.pic_x_7            = d.pic_x_7            )
AND ( a.pic_x_long         = d.pic_x_long         )
AND ( a.var_char           = d.var_char           )
AND ( a.binary_signed      = d.binary_signed      )
AND ( a.binary_32_u        = d.binary_32_u        )
AND ( a.binary_64_s        = d.binary_64_s        )
AND ( a.pic_comp_1         = d.pic_comp_1         )
AND ( a.pic_comp_2         = d.pic_comp_2         )
AND ( a.pic_comp_3         = d.pic_comp_3         )
AND ( a.small_int          = d.small_int          )
AND ( a.medium_int         = d.medium_int         )
AND ( a.large_int          = d.large_int          )
AND ( a.decimal_1          = d.decimal_1          )
AND ( a.decimal_2_signed   = d.decimal_2_signed   )
AND ( a.decimal_3_unsigned = d.decimal_3_unsigned )
AND ( a.pic_decimal_1      = d.pic_decimal_1      )
AND ( a.pic_decimal_2      = d.pic_decimal_2      )
AND ( a.pic_decimal_3      = d.pic_decimal_3      )
--  Compare columns for a and e:
AND ( a.char_1             = e.char_1             )
AND ( a.char_10            = e.char_10            )
AND ( a.pic_x_1            = e.pic_x_1            )
AND ( a.pic_x_7            = e.pic_x_7            )
AND ( a.pic_x_long         = e.pic_x_long         )
AND ( a.var_char           = e.var_char           )
AND ( a.binary_signed      = e.binary_signed      )
AND ( a.binary_32_u        = e.binary_32_u        )
AND ( a.binary_64_s        = e.binary_64_s        )
AND ( a.pic_comp_1         = e.pic_comp_1         )
AND ( a.pic_comp_2         = e.pic_comp_2         )
AND ( a.pic_comp_3         = e.pic_comp_3         )
AND ( a.small_int          = e.small_int          )
AND ( a.medium_int         = e.medium_int         )
AND ( a.large_int          = e.large_int          )
AND ( a.decimal_1          = e.decimal_1          )
AND ( a.decimal_2_signed   = e.decimal_2_signed   )
AND ( a.decimal_3_unsigned = e.decimal_3_unsigned )
AND ( a.pic_decimal_1      = e.pic_decimal_1      )
AND ( a.pic_decimal_2      = e.pic_decimal_2      )
AND ( a.pic_decimal_3      = e.pic_decimal_3      )
--  Compare columns for a and f:
AND ( a.char_1             = f.char_1             )
AND ( a.char_10            = f.char_10            )
AND ( a.pic_x_1            = f.pic_x_1            )
AND ( a.pic_x_7            = f.pic_x_7            )
AND ( a.pic_x_long         = f.pic_x_long         )
AND ( a.var_char           = f.var_char           )
AND ( a.binary_signed      = f.binary_signed      )
AND ( a.binary_32_u        = f.binary_32_u        )
AND ( a.binary_64_s        = f.binary_64_s        )
AND ( a.pic_comp_1         = f.pic_comp_1         )
AND ( a.pic_comp_2         = f.pic_comp_2         )
AND ( a.pic_comp_3         = f.pic_comp_3         )
AND ( a.small_int          = f.small_int          )
AND ( a.medium_int         = f.medium_int         )
AND ( a.large_int          = f.large_int          )
AND ( a.decimal_1          = f.decimal_1          )
AND ( a.decimal_2_signed   = f.decimal_2_signed   )
AND ( a.decimal_3_unsigned = f.decimal_3_unsigned )
AND ( a.pic_decimal_1      = f.pic_decimal_1      )
AND ( a.pic_decimal_2      = f.pic_decimal_2      )
AND ( a.pic_decimal_3      = f.pic_decimal_3      )
--  Compare columns for a and g:
AND ( a.char_1             = g.char_1             )
AND ( a.char_10            = g.char_10            )
AND ( a.pic_x_1            = g.pic_x_1            )
AND ( a.pic_x_7            = g.pic_x_7            )
AND ( a.pic_x_long         = g.pic_x_long         )
AND ( a.var_char           = g.var_char           )
AND ( a.binary_signed      = g.binary_signed      )
AND ( a.binary_32_u        = g.binary_32_u        )
AND ( a.binary_64_s        = g.binary_64_s        )
AND ( a.pic_comp_1         = g.pic_comp_1         )
AND ( a.pic_comp_2         = g.pic_comp_2         )
AND ( a.pic_comp_3         = g.pic_comp_3         )
AND ( a.small_int          = g.small_int          )
AND ( a.medium_int         = g.medium_int         )
AND ( a.large_int          = g.large_int          )
AND ( a.decimal_1          = g.decimal_1          )
AND ( a.decimal_2_signed   = g.decimal_2_signed   )
AND ( a.decimal_3_unsigned = g.decimal_3_unsigned )
AND ( a.pic_decimal_1      = g.pic_decimal_1      )
AND ( a.pic_decimal_2      = g.pic_decimal_2      )
AND ( a.pic_decimal_3      = g.pic_decimal_3      )
--  Compare columns for a and h:
AND ( a.char_1             = h.char_1             )
AND ( a.char_10            = h.char_10            )
AND ( a.pic_x_1            = h.pic_x_1            )
AND ( a.pic_x_7            = h.pic_x_7            )
AND ( a.pic_x_long         = h.pic_x_long         )
AND ( a.var_char           = h.var_char           )
AND ( a.binary_signed      = h.binary_signed      )
AND ( a.binary_32_u        = h.binary_32_u        )
AND ( a.binary_64_s        = h.binary_64_s        )
AND ( a.pic_comp_1         = h.pic_comp_1         )
AND ( a.pic_comp_2         = h.pic_comp_2         )
AND ( a.pic_comp_3         = h.pic_comp_3         )
AND ( a.small_int          = h.small_int          )
AND ( a.medium_int         = h.medium_int         )
AND ( a.large_int          = h.large_int          )
AND ( a.decimal_1          = h.decimal_1          )
AND ( a.decimal_2_signed   = h.decimal_2_signed   )
AND ( a.decimal_3_unsigned = h.decimal_3_unsigned )
AND ( a.pic_decimal_1      = h.pic_decimal_1      )
AND ( a.pic_decimal_2      = h.pic_decimal_2      )
AND ( a.pic_decimal_3      = h.pic_decimal_3      )
--  Compare columns for a and i:
AND ( a.char_1             = i.char_1             )
AND ( a.char_10            = i.char_10            )
AND ( a.pic_x_1            = i.pic_x_1            )
AND ( a.pic_x_7            = i.pic_x_7            )
AND ( a.pic_x_long         = i.pic_x_long         )
AND ( a.var_char           = i.var_char           )
AND ( a.binary_signed      = i.binary_signed      )
AND ( a.binary_32_u        = i.binary_32_u        )
AND ( a.binary_64_s        = i.binary_64_s        )
AND ( a.pic_comp_1         = i.pic_comp_1         )
AND ( a.pic_comp_2         = i.pic_comp_2         )
AND ( a.pic_comp_3         = i.pic_comp_3         )
AND ( a.small_int          = i.small_int          )
AND ( a.medium_int         = i.medium_int         )
AND ( a.large_int          = i.large_int          )
AND ( a.decimal_1          = i.decimal_1          )
AND ( a.decimal_2_signed   = i.decimal_2_signed   )
AND ( a.decimal_3_unsigned = i.decimal_3_unsigned )
AND ( a.pic_decimal_1      = i.pic_decimal_1      )
AND ( a.pic_decimal_2      = i.pic_decimal_2      )
AND ( a.pic_decimal_3      = i.pic_decimal_3      )
--  Compare columns for a and j:
AND ( a.char_1             = j.char_1             )
AND ( a.char_10            = j.char_10            )
AND ( a.pic_x_1            = j.pic_x_1            )
AND ( a.pic_x_7            = j.pic_x_7            )
AND ( a.pic_x_long         = j.pic_x_long         )
AND ( a.var_char           = j.var_char           )
AND ( a.binary_signed      = j.binary_signed      )
AND ( a.binary_32_u        = j.binary_32_u        )
AND ( a.binary_64_s        = j.binary_64_s        )
AND ( a.pic_comp_1         = j.pic_comp_1         )
AND ( a.pic_comp_2         = j.pic_comp_2         )
AND ( a.pic_comp_3         = j.pic_comp_3         )
AND ( a.small_int          = j.small_int          )
AND ( a.medium_int         = j.medium_int         )
AND ( a.large_int          = j.large_int          )
AND ( a.decimal_1          = j.decimal_1          )
AND ( a.decimal_2_signed   = j.decimal_2_signed   )
AND ( a.decimal_3_unsigned = j.decimal_3_unsigned )
AND ( a.pic_decimal_1      = j.pic_decimal_1      )
AND ( a.pic_decimal_2      = j.pic_decimal_2      )
AND ( a.pic_decimal_3      = j.pic_decimal_3      )
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n07exp""", 'n07s1')
    
    stmt = """DROP table L6table;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

