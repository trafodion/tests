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
    
    stmt = """drop table aa cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table basetable1 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table bb cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table cc cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table character18table18 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table cpref cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table cpbase cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table dd cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table dec15 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table ee cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table ff cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table four_types cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table flo15 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table gg cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table hh cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table ii cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table int10 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table jj cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table jj_20 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table kk cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table ll cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table longint cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table mm2 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table mm cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table nn cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table oo cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table p12 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table p15 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table p15_15 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table p15_7 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table p1 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table p7 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table pp cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table pp_15 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table pp_7 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table proj1 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table works3 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table proj3 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table qq cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table rr cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table shorttable cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table siz1_f cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table siz1_p cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table ss cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table staff1 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table staff3 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table staff4 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table staff5 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table staff6 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table staff7 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table staff8 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table staff9 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table staff cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table sv cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table t100 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table t118 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table t12 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table t2000 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table t240 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table t4 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table t8 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table tablefghijklmnopq19 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table temp_observ cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table temp_s cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table text1024 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table text132 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table text240 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table text256 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table text512 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table text80 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table tmp cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table u_sig cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table upuniq cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table usig cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table vtable cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table works1 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table works cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table proj cascade;"""
    output = _dci.cmdexec(stmt)
    
