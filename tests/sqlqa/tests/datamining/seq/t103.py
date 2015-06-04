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
    
def test001(desc="""test103"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test103
    # "Nested SELECT w/ sequence functions produces internal error in generator"
    #
    #
    #    create table CPW (
    #        account_num int,
    #        wk int,
    #        wkly_ad_clicks int
    #        );
    #
    #    insert into CPW values
    #        (1234,         23,      11),
    #        (1234,         24,      17),
    #        (2345,         23,      14),
    #        (2345,         24,      15),
    #        (2345,         25,      15),
    #        (2345,         26,      11);
    #
    #
    # the workaround
    stmt = """select account_num, wk, diff1 (ad_clicks_mov_avg)
from (
select account_num + 0, wk,
cast (movingavg (wkly_ad_clicks, 3,
rows since (account_num <> OFFSET (account_num,1)))
as dec (10,3))
from CPW 
sequence by account_num, wk
) as T1 ( account_num, wk, ad_clicks_mov_avg)
sequence by account_num, wk
order by 1, 2, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test103.exp""", 's1')
    # expect 6 rows with these values in this order:
    #             1234           23                      ?
    #             1234           24                  3.000
    #             2345           23                   .000
    #             2345           24                  1.000
    #             2345           25                   .000
    #             2345           26                 -1.334
    
    stmt = """select account_num, wk, diff1 (ad_clicks_mov_avg)
from (
select account_num, wk,
cast (movingavg (wkly_ad_clicks, 3,
rows since (account_num <> OFFSET (account_num,1)))
as dec (10,3))
from CPW 
sequence by account_num, wk
) as T1 ( account_num, wk, ad_clicks_mov_avg)
sequence by account_num, wk
order by 1, 2, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test103.exp""", 's2')
    # expect 6 rows with these values in this order:
    #             1234           23                      ?
    #             1234           24                  3.000
    #             2345           23                   .000
    #             2345           24                  1.000
    #             2345           25                   .000
    #             2345           26                 -1.334
    
    _testmgr.testcase_end(desc)

