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

work_dir = None


class TestVars():


    # register user sqluser_admin;
    # register user qauser99;

    qi_user2 = "qauser99"
    qi_pw2 = "QAPassword"
    qi_role2 = ""

    qi_user3 = "sqluser_admin"
    qi_pw3 = "traf123"
    qi_role3 = ""

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci

    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()

    #_testmgr.clone_dci_proc_with_id('supermxci', _dci, TestVars.super_user, TestVars.super_pw, TestVars.super_role)
    # Use the users/pws/roles defined in testunit.
    _testmgr.clone_dci_proc_with_id('qi_mxci2', _dci, TestVars.qi_user2, TestVars.qi_pw2, TestVars.qi_role2)
    _testmgr.clone_dci_proc_with_id('qi_mxci3', _dci, TestVars.qi_user3, TestVars.qi_pw3, TestVars.qi_role3)

    mydci = switch_session_qi_user2()
    mydci = switch_session_qi_user3()


def switch_session_qi_user2():
    global _testmgr
    mydci = _testmgr.get_dci_proc('qi_mxci2')
    return mydci

def switch_session_qi_user3():
    global _testmgr
    mydci = _testmgr.get_dci_proc('qi_mxci3')
    return mydci

