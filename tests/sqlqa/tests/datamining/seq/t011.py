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
    
def test001(desc="""test011"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test011
    # Sequence function tests: test for RUNNINGCOUNT(*)
    #
    stmt = """select runningcount (*) as runningcount_star,
i1, i2, ts
from vwseqtb2 sequence by ts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 20)
    #
    # expect 20 rows with these values in order
    #
    # RUNNINGCOUNT_STAR     I1           I2           TS
    # --------------------  -----------  -----------  --------------------------
    #
    #                    1            1         6215  1950-03-05 08:32:09.000000
    #                    2            2        28174  1951-02-15 14:35:49.000000
    #                    3            3        19058  1955-05-18 08:40:10.000000
    #                    4            4         4597  1960-09-19 14:40:39.000000
    #                    5            5        11966  1964-05-01 16:41:02.000000
    #                    6            6         2580  1975-02-24 06:52:15.000000
    #                    7            7         1464  1979-07-08 15:15:34.000000
    #                    8            8        13198  1988-11-18 21:40:06.000000
    #                    9            9        29246  1992-08-12 15:17:11.000000
    #                   10           10         1985  1996-10-11 11:34:10.000000
    #                   11           11           61  1997-09-13 17:20:35.000000
    #                   12           12        23453  1997-11-05 09:33:54.000000
    #                   13           13        24998  1999-02-14 09:40:27.000000
    #                   14           14        20119  2004-05-16 04:56:55.000000
    #                   15           15         9235  2009-09-27 11:59:16.000000
    #                   16           16        11798  2013-01-15 20:54:47.000000
    #                   17           17        23727  2024-03-16 11:51:53.000000
    #                   18           18         4818  2027-10-13 18:41:22.000000
    #                   19           19         6516  2032-07-21 16:07:34.000000
    #                   20           20         7447  2039-08-01 09:47:11.000000
    #
    
    # Equivalent standard SQL
    stmt = """select (select count(*) from vwseqtb2 x where x.i1 <= y.i1)
as runningcount_star,
i1, i2, ts
from vwseqtb2 y
order by ts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 20)
    #
    # expect 20 rows with these values in order
    #
    # RUNNINGCOUNT_STAR     I1           I2           TS
    # --------------------  -----------  -----------  --------------------------
    #
    #                    1            1         6215  1950-03-05 08:32:09.000000
    #                    2            2        28174  1951-02-15 14:35:49.000000
    #                    3            3        19058  1955-05-18 08:40:10.000000
    #                    4            4         4597  1960-09-19 14:40:39.000000
    #                    5            5        11966  1964-05-01 16:41:02.000000
    #                    6            6         2580  1975-02-24 06:52:15.000000
    #                    7            7         1464  1979-07-08 15:15:34.000000
    #                    8            8        13198  1988-11-18 21:40:06.000000
    #                    9            9        29246  1992-08-12 15:17:11.000000
    #                   10           10         1985  1996-10-11 11:34:10.000000
    #                   11           11           61  1997-09-13 17:20:35.000000
    #                   12           12        23453  1997-11-05 09:33:54.000000
    #                   13           13        24998  1999-02-14 09:40:27.000000
    #                   14           14        20119  2004-05-16 04:56:55.000000
    #                   15           15         9235  2009-09-27 11:59:16.000000
    #                   16           16        11798  2013-01-15 20:54:47.000000
    #                   17           17        23727  2024-03-16 11:51:53.000000
    #                   18           18         4818  2027-10-13 18:41:22.000000
    #                   19           19         6516  2032-07-21 16:07:34.000000
    #                   20           20         7447  2039-08-01 09:47:11.000000
    #
    
    _testmgr.testcase_end(desc)

