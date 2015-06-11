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

    _dci = _testmgr.delete_dci_proc('qi_mxci2')
    _dci = _testmgr.get_default_dci_proc()
    _dci = _testmgr.delete_dci_proc('qi_mxci3')
    _dci = _testmgr.get_default_dci_proc()
    _dci = _testmgr.delete_dci_proc('qi_mxci4')
    _dci = _testmgr.get_default_dci_proc()
    #_dci = _testmgr.delete_dci_proc('qi_mxci5')
    #_dci = _testmgr.get_default_dci_proc()
    #_dci = _testmgr.delete_dci_proc('qi_mxci6')
    #_dci = _testmgr.get_default_dci_proc()
    #_dci = _testmgr.delete_dci_proc('qi_mxci7')
    #_dci = _testmgr.get_default_dci_proc()
    #_dci = _testmgr.delete_dci_proc('qi_mxci8')
    #_dci = _testmgr.get_default_dci_proc()	
    #_dci = _testmgr.delete_dci_proc('qi_mxci9')
    #_dci = _testmgr.get_default_dci_proc()
    #_dci = _testmgr.delete_dci_proc('qi_mxci10')
    #_dci = _testmgr.get_default_dci_proc()