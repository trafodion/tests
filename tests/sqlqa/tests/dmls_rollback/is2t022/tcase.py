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
    
def test001(desc="""t01"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # AUTOABORT syntax test
    # SET TRANSACTION ... AUTOABORT [ timeout | 0 | RESET ]
    #   timeout is integer {HOUR[S] | MINUTE[S] | SECOND[S]}
    # Expected error -3235/-15001
    #   3235 : Invalid <value> specified for AUTOABORT timeout interval.
    #   15001: Syntax error at or before:
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """set param ?p 10;"""
    output = _dci.cmdexec(stmt)
    
    # t01.1: -1 seconds
    stmt = """SET TRANSACTION AUTOABORT RESET;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.2:
    stmt = """SHOWTRANSACTION;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _dci = _testmgr.get_dci_proc('mymxci')
    stmt = """env;"""
    output = _dci.cmdexec(stmt)
    
    # t01.3:
    stmt = """SHOWTRANSACTION;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.4:
    stmt = """SET TRANSACTION AUTOABORT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.5:
    # #expect any *3235*
    stmt = """SET TRANSACTION AUTOABORT 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.6:
    stmt = """SET TRANSACTION AUTOABORT SECOND;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.7: expect error 3235
    # 19 seconds is less than minimum 20 seconds
    ##expectfile $test_dir/t01exp t01s7
    stmt = """SET TRANSACTION AUTOABORT 19 SECOND;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3235')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.8: expect error 3235
    ##expectfile $test_dir/t01exp t01s8
    stmt = """SET TRANSACTION AUTOABORT 19 SECONDS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3235')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.9: expect error 3235
    ##expectfile $test_dir/t01exp t01s9
    stmt = """SET TRANSACTION AUTOABORT 0 SECOND;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3235')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.10: expect error 3235
    ##expectfile $test_dir/t01exp t01s10
    stmt = """SET TRANSACTION AUTOABORT 10 SECONDS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3235')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.11: expect error 3235
    # 1 seconds is an illegal values. Minimum interval is 20 seconds.
    ##expectfile $test_dir/t01exp t01s11
    stmt = """SET TRANSACTION AUTOABORT 1 SECONDS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3235')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.12:
    stmt = """SET TRANSACTION AUTOABORT 20 secondss;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.13:
    stmt = """SET TRANSACTION AUTOABORT -1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.14:
    stmt = """SET TRANSACTION AUTOABORT -1 SECOND;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.15:
    # #expect any *3235*
    ##expectfile $test_dir/t01exp t01s150
    stmt = """SET TRANSACTION AUTOABORT 21474837 SECONDS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3235')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.15.1:
    # #expect any *3235*
    # #expectfile $test_dir/t01exp t01s151
    stmt = """SET TRANSACTION AUTOABORT 999999999999999999 SECONDS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3235')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.16:
    stmt = """SET TRANSACTION AUTOABORT 0 MINUTE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3235')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.17: expected error 3235
    # The followings are out of range intervals
    # #expectfile $test_dir/t01exp t01s171
    stmt = """SET TRANSACTION AUTOABORT 999999999999 minutes;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3235')
    
    ##expectfile $test_dir/t01exp t01s172
    stmt = """set transaction autoabort 10000000000000 hours;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3235')
    
    ##expectfile $test_dir/t01exp t01s173
    stmt = """set transaction autoabort 99999999999999999 hour;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3235')
    
    ##expectfile $test_dir/t01exp t01s174
    stmt = """set transaction autoabort 99999999999999999 minutes;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3235')
    
    ##expectfile $test_dir/t01exp t01s175
    stmt = """SET TRANSACTION AUTOABORT 123456789012345678 HOUR;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3235')
    
    ##expectfile $test_dir/t01exp t01s176
    stmt = """set transaction autoabort 99999999999999999 minutes;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3235')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.18: expect error 3235
    ##expectfile $test_dir/t01exp t01s18
    stmt = """SET TRANSACTION AUTOABORT 357914 minutes;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3235')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.19: expect error 3235
    ##expectfile $test_dir/t01exp t01s19
    stmt = """SET TRANSACTION AUTOABORT 21474835 minute;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3235')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.20:
    stmt = """SET TRANSACTION AUTOABORT minuteS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.21:
    stmt = """SET TRANSACTION AUTOABORT 71 minute 20 SECONDS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.22:
    ##expect any *3235*
    stmt = """SET TRANSACTION AUTOABORT 0 hours;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3235')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.23:
    # #expect any *3235*
    ##expectfile $test_dir/t01exp t01s23
    stmt = """SET TRANSACTION AUTOABORT 5966 hour;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3235')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.24:
    stmt = """SET TRANSACTION AUTOABORT 1 hours 20 minutes 300 seconds;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.25:
    stmt = """SET TRANSACTION AUTOABORT 1 hour and 20 miuntes;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.26:
    stmt = """SET TRANSACTION AUTOABORT 21 seconds 0 minutes;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.27:
    stmt = """SET TRANSACTION AUTOABORT 21 seconds 99 hours;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.28:
    stmt = """SET TRANSACTION AUTOABORT 20-20 seconds;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.29:
    stmt = """SET TRANSACTION AUTOABORT -20 seconds;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.30:
    stmt = """SET TRANSACTION AUTOABORT hour 20 seconds;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.31:
    stmt = """SET TRANSACTION AUTOABORT 1 hour, 20 seconds;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.32:
    stmt = """SET TRANSACTION AUTOABORT 10,24,36;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.33:
    stmt = """SET TRANSACTION AUTOABORT 10:24:36;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.34:
    # #expect any *3235*
    ##expectfile $test_dir/t01exp t01s34
    stmt = """SET TRANSACTION AUTOABORT 357913 hours;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3235')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.35:
    stmt = """SET TRANSACTION AUTOABORT 10 hours RESET;;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.36:
    stmt = """SET TRANSACTION AUTOABORT RESET 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.37:
    stmt = """SET TRANSACTION AUTOABORT RESET/u #;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.38:
    stmt = """SET TRANSACTION AUTOABORT 0 RESET;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.39:
    stmt = """SET TRANSACTION AUTOABORT RESET 20 seconds;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.40:
    stmt = """SET TRANSACTION AUTOABORT 2006/10/10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.41:
    ##expect any *3238*
    stmt = """SET TRANSACTION AUTOABORT RESET, AUTOABORT 20 SECONDS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3238')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SET TRANSACTION AUTOABORT RESET;"""
    output = _dci.cmdexec(stmt)
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    
    # t01.42:
    stmt = """SET TRANSACTION AUTOABORT 0, AUTOABORT RESET;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3238')
    
    # t01.43:
    stmt = """SHOWTRANSACTION;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.44: expected error 3238
    ##expectfile $test_dir/t01exp t01s44
    stmt = """SET TRANSACTION AUTOABORT 1 HOUR, AUTOABORT 0, AUTOABORT RESET;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3238')
    
    # t01.45:
    stmt = """SHOWTRANSACTION;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.46:
    
    stmt = """set param ?p 120;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SET TRANSACTION AUTOABORT ?p seconds;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.47:
    stmt = """SET TRANSACTION AUTOABORT 20p seconds;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.48:
    stmt = """SET TRANSACTION READ ONLY, AUTOABORT 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.49:
    stmt = """SET TRANSACTION AUTOABORT 20 S;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.50:
    stmt = """SET TRANSACTION AUTOABORT 20, isolation level read committed;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.51:
    stmt = """SET TRANSACTION DIAGNOSTICS Size 12, AUTOABORT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.52:
    stmt = """SET TRANSACTION AUTOABORT 20 SECONDS, AUTOCOMMIT ON;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.53:
    # #expect any *3235*
    ##expectfile $test_dir/t01exp t01s53
    stmt = """SET TRANSACTION AUTOABORT 999999999999999999 SECONDS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3235')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.54: expect error 3235
    ##expectfile $test_dir/t01exp t01s54
    stmt = """SET TRANSACTION AUTOABORT 123456789012345678 HOUR;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3235')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.55:
    stmt = """SET TRANSACTION AUTOABORT 1+99 MINUTES;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.56:
    stmt = """SET TRANSACTION AUTOABORT 1.375 HOUR;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.57:
    stmt = """SET TRANSACTION AUTOABORT 6*60*60 SECONDS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.58:
    stmt = """SET TRANSACTION AUTOABORT 30**2 SECONDS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.59: 5964 hours
    stmt = """SET TRANSACTION AUTOABORT 357840/60 HOURS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.60:
    stmt = """SET TRANSACTION AUTOABORT +999 MINUTES;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.61:
    stmt = """SET TRANSACTION AUTOABORT 1999+ MINUTES;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.62:
    stmt = """SET TRANSACTION AUTOABORT 1999- MINUTES;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.63:
    stmt = """SET TRANSACTION AUTOABORT 9999%3 MINUTES;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t01.64:
    stmt = """SHOWTRANSACTION;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _dci = _testmgr.get_default_dci_proc()
    
    # t01.65:
    stmt = """SHOWTRANSACTION;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.66:
    stmt = """SET TRANSACTION AUTOABORT 2(2000) MINUTES;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.67:
    stmt = """SET TRANSACTION AUTOABORT 2 MINUTE[S];"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.68:
    stmt = """SET TRANSACTION AUTOABORT RESET -1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.69:
    stmt = """SET TRANSACTION AUTOABORT RESET ON, READ ONLY;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t01.70:
    stmt = """SHOWTRANSACTION;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.71:
    stmt = """SET TRANSACTION AUTOABORT 0000000000000000.00000000000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """SHOWTRANSACTION;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

