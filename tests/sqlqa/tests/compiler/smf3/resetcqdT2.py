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

# reset CQDs set in cqdT2.sql
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    _dci.showcontrol_showall_reset() 
    stmt = """control query default query_cache reset;"""
    output = _dci.cmdexec(stmt)
    stmt = """control query default cache_histograms reset;"""
    output = _dci.cmdexec(stmt)
    stmt = """Control query default EXE_DIAGNOSTIC_EVENTS reset;"""
    output = _dci.cmdexec(stmt)
    stmt = """control query default detailed_statistics reset;"""
    output = _dci.cmdexec(stmt)
    stmt = """control query default sort_merge_buffer_unit_56kb reset;"""
    output = _dci.cmdexec(stmt)
    stmt = """control query default scratch_max_opens_sort reset;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """control query default gen_sort_max_num_buffers reset;"""
    output = _dci.cmdexec(stmt)
    stmt = """control query default gen_sort_max_buffer_size reset;"""
    output = _dci.cmdexec(stmt)
    
