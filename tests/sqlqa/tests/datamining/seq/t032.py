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
    
def test001(desc="""test032"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test032
    # Sequence function tests: LASTNOTNULL(column)
    #
    stmt = """select * from vwseqtb3 order by i1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 16)
    # expect 16 rows with the following values in order
    
    # I1           I2           TS
    # -----------  -----------  --------------------------
    #
    #           1         6215  1950-03-05 08:32:09.000000
    #           2        28174                           ?
    #           3            ?  1955-05-18 08:40:10.000000
    #           5        11966                           ?
    #           6         2580  1975-02-24 06:52:15.000000
    #           7         1464  1979-07-08 15:15:34.000000
    #           9        29246                           ?
    #          10         1985  1996-10-11 11:34:10.000000
    #          12            ?  1997-11-05 09:33:54.000000
    #          13            ?  1999-02-14 09:40:27.000000
    #          15         9235  2009-09-27 11:59:16.000000
    #          16        11798  2013-01-15 20:54:47.000000
    #          17        23727  2024-03-16 11:51:53.000000
    #          18         4818                           ?
    #          19            ?  2032-07-21 16:07:34.000000
    #          20         7447  2039-08-01 09:47:11.000000
    
    stmt = """select i1, ts, lastnotnull (ts) as lastnotnull_ts
from vwseqtb3 
where i1 < 10
sequence by i1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test032.exp""", 's2')
    # expect 7 rows in order with the following values
    
    # I1           TS                          LASTNOTNULL_TS
    # -----------  --------------------------  --------------------------
    #
    #           1  1950-03-05 08:32:09.000000  1950-03-05 08:32:09.000000
    #           2                           ?  1950-03-05 08:32:09.000000
    #           3  1955-05-18 08:40:10.000000  1955-05-18 08:40:10.000000
    #           5                           ?  1955-05-18 08:40:10.000000
    #           6  1975-02-24 06:52:15.000000  1975-02-24 06:52:15.000000
    #           7  1979-07-08 15:15:34.000000  1979-07-08 15:15:34.000000
    #           9                           ?  1979-07-08 15:15:34.000000
    
    _testmgr.testcase_end(desc)

