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
    _dci.setup_schema(defs.my_schema)   

    _dci.setup_schema(defs.aa11 + "." + '"bb"')
    _dci.setup_schema(defs.testcat + "." + defs.testsch1)
    _dci.setup_schema(defs.testcat + "." + defs.testsch2)
    _dci.setup_schema(defs.testcat + "." + defs.testsch3)
    _dci.setup_schema(defs.testcat2 + "." + defs.testsch3)
    _dci.setup_schema(defs.a009_cat1 + "." + defs.a009_cat1_sch1)
    _dci.setup_schema(defs.a013_2_cat1 + "." + defs.a013_2_cat1_sch1)
    _dci.setup_schema(defs.a013_5_cat1 + "." + defs.a013_5_cat1_sch1)
    _dci.setup_schema(defs.a013_6_cat1 + "." + defs.a013_6_cat1_sch1)
    _dci.setup_schema(defs.a013_7_cat1 + "." + defs.a013_7_cat1_sch1)
    _dci.setup_schema(defs.a013_7_cat1 + "." + defs.a013_7_cat1_sch2)
    _dci.setup_schema(defs.catddlA013 + "." + defs.schA013)

    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)

    _dci.showcontrol_showall_on()

