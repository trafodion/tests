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
import setup
import cleanup
# Import you own test modules, one line for each.
import cr8seq
import t001
import t002
import t003
import t010
import t011
import t012
import t013
import t014
import t015
import t016
import t017
import t018
import t020
import t026
import t027
import t028
import t029
import t030
import t031
import t032
import t040
import t041
import t042
import t043
import t044
import t045
import t046
import t047
import t048
import t049
import t050
import t051
import t052
import t053
import t061
import t062
import t068
import t069
import t070
import t071
import t072
import t075
import t078
import t079
import t080
import t081
import t082
import t083
import t084
import t085
import t086
import t087
import t088
import t089
import t090
import t091
import t092
import t093
import t094
import t095
import t096
import t097
import t098
import t099
import t100
import t101
import t102
import t103
import t104
import t105
import t106
import t107
import t108
import t109
import t110

def sq_testunit(hptestmgr, testlist=[]):

    cleanup._init(hptestmgr, testlist)
    setup._init(hptestmgr, testlist)

    # Auto execute your test modules, one line for each.
    hpdci.auto_execute_module_tests(cr8seq, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t001, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t002, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t003, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t010, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t011, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t012, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t013, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t014, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t015, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t016, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t017, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t018, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t020, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t026, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t027, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t028, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t029, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t030, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t031, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t032, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t040, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t041, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t042, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t043, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t044, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t045, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t046, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t047, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t048, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t049, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t050, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t051, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t052, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t053, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t061, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t062, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t068, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t069, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t070, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t071, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t072, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t075, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t078, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t079, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t080, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t081, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t082, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t083, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t084, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t085, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t086, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t087, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t088, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t089, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t090, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t091, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t092, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t093, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t094, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t095, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t096, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t097, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t098, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t099, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t100, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t101, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t102, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t103, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t104, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t105, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t106, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t107, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t108, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t109, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t110, hptestmgr, testlist)

    cleanup._init(hptestmgr, testlist)
   
