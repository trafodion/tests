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
    
def test001(desc="""test057"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test057
    # JClear
    # 2000-10-03
    # UNION ALL of test020 complicated EXISTS query
    #              test021 complicated EXISTS-EXISTS-EXISTS query
    # CJDate tests 5th ed. pp 171
    #
    stmt = """select distinct jnum
from spj x
where exists
(select *
from spj y
where y.jnum = x.jnum
and exists
(select *
from spj z
where z.pnum = y.pnum
and z.snum = 's1'))
union all
select distinct jnum
from spj x
where exists
(select *
from spj y
where exists
(select *
from spj a
where a.snum = 's1'
and a.pnum = y.pnum)
and exists
(select *
from spj b
where b.snum = 's1'
and b.pnum = y.pnum
and b.jnum = x.jnum))
order by jnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test057.exp""", 's1')
    # expect 2 rows with values j1 j4 in that order
    
    # VP tables
    #- select distinct jnum
    #-   from vpspj x
    #-     where exists
    #-       (select *
    #-          from vpspj y
    #-            where y.jnum = x.jnum
    #-              and exists
    #-                (select *
    #-                   from vpspj z
    #-                     where z.pnum = y.pnum
    #-                       and z.snum = 's1'))
    #- union all
    #- select distinct jnum
    #-   from vpspj x
    #-     where exists
    #-       (select *
    #-          from vpspj y
    #-            where exists
    #-              (select *
    #-                 from vpspj a
    #-                   where a.snum = 's1'
    #-                     and a.pnum = y.pnum)
    #-       and exists
    #-         (select *
    #-            from vpspj b
    #-              where b.snum = 's1'
    #-                and b.pnum = y.pnum
    #-                and b.jnum = x.jnum))
    #-       order by jnum;
    # expect 2 rows with values j1 j4 in that order
    
    # HP tables
    stmt = """select distinct jnum
from hpspj x
where exists
(select *
from hpspj y
where y.jnum = x.jnum
and exists
(select *
from hpspj z
where z.pnum = y.pnum
and z.snum = 's1'))
union all
select distinct jnum
from hpspj x
where exists
(select *
from hpspj y
where exists
(select *
from hpspj a
where a.snum = 's1'
and a.pnum = y.pnum)
and exists
(select *
from hpspj b
where b.snum = 's1'
and b.pnum = y.pnum
and b.jnum = x.jnum))
order by jnum;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test057.exp""", 's2')
    # expect 2 rows with values j1 j4 in that order
    
    _testmgr.testcase_end(desc)

