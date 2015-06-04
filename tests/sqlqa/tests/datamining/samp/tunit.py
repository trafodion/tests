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
import cr8samp
import t001
import t002
import t003
import t004
import t005
import t006
import t007
import t008
import t009
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
import t021
import t022
import t023
import t024
import t025
import t026
import t027
import t028
import t029
import t030
import t031
import t032
import t033
import t050
import t051
import t052
import t053
import t054
import t055
import t056
import t056b
import t057
import t058
import t059
import t060
import t061
import t062
import t063
import t064
import t065
import t066
import t067
import t068
import t069
import t070
import t071
import t072
import t072b
import t073
import t074
import t075
import t076
import t077
import t078
import t078b
import t079
import t080
import t081
import t082
import t083
import t084
import t085
import t086
import t100
import t101
import t102

def sq_testunit(hptestmgr, testlist=[]):

    cleanup._init(hptestmgr, testlist)
    setup._init(hptestmgr, testlist)

    # Auto execute your test modules, one line for each.
    hpdci.auto_execute_module_tests(cr8samp, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t001, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t002, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t003, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t004, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t005, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t008, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t009, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t010, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t011, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t012, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t013, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t014, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t020, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t021, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t022, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t023, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t024, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t025, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t026, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t027, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t028, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t029, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t030, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t031, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t032, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t050, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t051, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t052, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t053, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t054, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t055, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t056, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t056b, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t057, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t058, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t059, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t060, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t061, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t062, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t063, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t064, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t065, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t066, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t067, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t068, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t069, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t070, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t071, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t072b, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t073, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t074, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t075, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t076, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t077, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t078, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t078b, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t079, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t080, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t081, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t082, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t083, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t084, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t085, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t086, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t100, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t101, hptestmgr, testlist)
    hpdci.auto_execute_module_tests(t102, hptestmgr, testlist)

    cleanup._init(hptestmgr, testlist)
   
