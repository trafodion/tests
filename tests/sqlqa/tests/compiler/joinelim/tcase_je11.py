# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2015 Hewlett-Packard Development Company, L.P.
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

# =================  Begin Test Case Header  ==================
#
#  Description:        Test possible settings of ELIMINATE_REDUNDANT_JOINS CQD.
#
#  Purpose:
#
#
#
# =================== End Test Case Header  ===================

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""ELIMINATE_REDUNDANT_JOINS 'ON'"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """control query default ELIMINATE_REDUNDANT_JOINS 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Conventional RI constraint with eliminated table.
    stmt = """prepare s from select a1 from t1,t2 where fk12=pk2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #unexpect any *_scan*T2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    # Conventional RI constraint with extra-hub table.
    stmt = """prepare s from select a1,a2 from t1,t2 where fk12=pk2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'scan*.T2')
    _dci.expect_selected_msg(output)
    
    # NOT ENFORCED RI constraint with eliminated table.
    stmt = """prepare s from select a1ne from t1ne,t2 where fk1ne2=pk2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #unexpect any *_scan*T2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    # NOT ENFORCED RI constraint with extra-hub table.
    stmt = """prepare s from select a1ne,a2 from t1ne,t2 where fk1ne2=pk2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'scan*.T2')
    _dci.expect_selected_msg(output)
    
    # restore CQD setting
    stmt = """control query default ELIMINATE_REDUNDANT_JOINS reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test002(desc="""ELIMINATE_REDUNDANT_JOINS 'OFF'"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """control query default ELIMINATE_REDUNDANT_JOINS 'OFF';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Conventional RI constraint with redundant table (not eliminated).
    stmt = """prepare s from select a1 from t1,t2 where fk12=pk2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '_scan*T2')
    
    # Conventional RI constraint with extra-hub table (not marked).
    stmt = """prepare s from select a1,a2 from t1,t2 where fk12=pk2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # NOT ENFORCED RI constraint with redundant table (not eliminated).
    stmt = """prepare s from select a1ne from t1ne,t2 where fk1ne2=pk2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '_scan*T2')
    
    # NOT ENFORCED RI constraint with extra-hub table (not marked).
    stmt = """prepare s from select a1ne,a2 from t1ne,t2 where fk1ne2=pk2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # restore CQD setting
    stmt = """control query default ELIMINATE_REDUNDANT_JOINS reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test003(desc="""ELIMINATE_REDUNDANT_JOINS 'MINIMUM'"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """control query default ELIMINATE_REDUNDANT_JOINS 'MINIMUM';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Conventional RI constraint with eliminated table.
    stmt = """prepare s from select a1 from t1,t2 where fk12=pk2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #unexpect any *_scan*T2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    # Conventional RI constraint with extra-hub table.
    stmt = """prepare s from select a1,a2 from t1,t2 where fk12=pk2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'scan*.T2')
    _dci.expect_selected_msg(output)
    
    # NOT ENFORCED RI constraint with redundant table (not eliminated).
    stmt = """prepare s from select a1ne from t1ne,t2 where fk1ne2=pk2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '_scan*T2')
    
    # NOT ENFORCED RI constraint with extra-hub table (not marked).
    stmt = """prepare s from select a1ne,a2 from t1ne,t2 where fk1ne2=pk2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # restore CQD setting
    stmt = """control query default ELIMINATE_REDUNDANT_JOINS reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test004(desc="""ELIMINATE_REDUNDANT_JOINS 'DEBUG'"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """control query default ELIMINATE_REDUNDANT_JOINS 'DEBUG';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Conventional RI constraint with eliminated table.
    stmt = """prepare s from select a1 from t1,t2 where fk12=pk2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #unexpect any *_scan*T2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    # Conventional RI constraint with extra-hub table.
    stmt = """prepare s from select a1,a2 from t1,t2 where fk12=pk2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'scan*.T2')
    _dci.expect_selected_msg(output)
    
    # NOT ENFORCED RI constraint with eliminated table.
    stmt = """prepare s from select a1ne from t1ne,t2 where fk1ne2=pk2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #unexpect any *_scan*T2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    # NOT ENFORCED RI constraint with extra-hub table.
    stmt = """prepare s from select a1ne,a2 from t1ne,t2 where fk1ne2=pk2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'scan*.T2')
    _dci.expect_selected_msg(output)
    
    # restore CQD setting
    stmt = """control query default ELIMINATE_REDUNDANT_JOINS reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

