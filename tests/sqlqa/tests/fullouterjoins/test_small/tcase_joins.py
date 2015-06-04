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
import setup

_testmgr = None
_testlist = []
_dci = None

# ----------------------
# Small data (tests) for tables
# ----------------------
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""J001"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """J001"""
    stmt = """prepare s1 from SELECT seqno, smin1 ,inte1, lint1 ,  deci1
FROM
wm000  t1
FULL OUTER JOIN
(select *
from wm_vw_000 natural join wm_vw_001
) as t2
on t1.seqno = t2.n1sq
order by seqno, smin1 ,inte1, lint1 ,  deci1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    
    #--------------------------
    _testmgr.testcase_end(desc)

def test002(desc="""J002"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """J002"""
    stmt = """prepare s1 from SELECT seqno, smin1 ,inte1, lint1 ,  deci1
FROM
wm000  t1
FULL OUTER JOIN
(select *
from wm_vw_000 natural join wm_vw_001
) as t2
on t1.seqno = t2.n1sq
where t1.seqno < 4
order by seqno, smin1 ,inte1, lint1 ,  deci1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    
    # -----inner join---------
    _testmgr.testcase_end(desc)

def test003(desc="""J003"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """J003"""
    stmt = """prepare s1 from SELECT seqno, smin1 ,inte1, lint1 ,  deci1
FROM
wm000  t1
FULL OUTER JOIN
(select *
from wm_vw_000 INNER JOIN  wm_vw_001
ON wm_vw_000.n0sq = wm_vw_001.n1sq
) as t2
on t1.seqno = t2.n1sq
order by seqno, smin1 ,inte1, lint1 ,  deci1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    
    #--------------------------
    _testmgr.testcase_end(desc)

def test004(desc="""J004"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """J004"""
    stmt = """prepare s1 from SELECT seqno, smin1 ,inte1, lint1 ,  deci1
FROM
wm000  t1
FULL OUTER JOIN
(select *
from wm_vw_000 INNER JOIN  wm_vw_001
ON wm_vw_000.n0sq = wm_vw_001.n1sq
) as t2
on t1.seqno = t2.n1sq
where t1.seqno < 4
order by seqno, smin1 ,inte1, lint1 ,  deci1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    
    # -----cross join---------
    _testmgr.testcase_end(desc)

def test005(desc="""J005"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """J005"""
    stmt = """prepare s1 from SELECT seqno, smin1 ,inte1, lint1 ,  deci1
FROM
wm000  t1
FULL OUTER JOIN
(select *
from wm_vw_000 CROSS JOIN  wm_vw_001
) as t2
on t1.seqno = t2.n1sq
order by seqno, smin1 ,inte1, lint1 ,  deci1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    
    #--------------------------
    _testmgr.testcase_end(desc)

def test006(desc="""J006"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """J006"""
    stmt = """prepare s1 from SELECT    seqno, smin1 ,inte1, lint1 ,  deci1
FROM
wm000  t1
FULL OUTER JOIN
(select *
from wm_vw_000 CROSS JOIN  wm_vw_001
) as t2
on t1.seqno = t2.n1sq
where t1.seqno < 4
order by seqno, smin1 ,inte1, lint1 ,  deci1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    
    # -----LEFT OUTER join---------
    ##testcase J007 J007
    ##sh testid=J007
    #prepare s1 from SELECT     seqno, smin1 ,inte1, lint1 ,  deci1
    stmt = """FROM
wm000  t1
FULL OUTER JOIN
(select *
from wm_vw_000 LEFT OUTER JOIN wm_vw_001
ON wm_vw_000.n0sq = wm_vw_001.n1sq
) as t2
on t1.seqno = t2.n1sq
order by seqno, smin1 ,inte1, lint1 ,  deci1 ;"""
    output = _dci.cmdexec(stmt)
    ##call setup.atest()
    ##endtestcase
    
    #--------------------------
    _testmgr.testcase_end(desc)

def test007(desc="""J008"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """J008"""
    stmt = """prepare s1 from SELECT   seqno, smin1 ,inte1, lint1 ,  deci1
FROM
wm000  t1
FULL OUTER JOIN
(select *
from wm_vw_000 LEFT OUTER JOIN wm_vw_001
ON wm_vw_000.n0sq = wm_vw_001.n1sq
) as t2
on t1.seqno = t2.n1sq
where t1.seqno < 4
order by seqno, smin1 ,inte1, lint1 ,  deci1  ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    
    # -----Right outer join---------
    _testmgr.testcase_end(desc)

def test008(desc="""J010"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """J010"""
    stmt = """prepare s1 from SELECT     seqno, smin1 ,inte1, lint1 ,  deci1
FROM
wm000  t1
FULL OUTER JOIN
(select *
from wm_vw_000 RIGHT OUTER  JOIN  wm_vw_001
ON wm_vw_000.n0sq = wm_vw_001.n1sq
) as t2
on t1.seqno = t2.n1sq
order by seqno, smin1 ,inte1, lint1 ,  deci1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    
    #--------------------------
    _testmgr.testcase_end(desc)

def test009(desc="""J011"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """J011"""
    stmt = """prepare s1 from SELECT    seqno, smin1 ,inte1, lint1 ,  deci1
FROM
wm000  t1
FULL OUTER JOIN
(select *
from wm_vw_000 RIGHT OUTER  JOIN  wm_vw_001
ON wm_vw_000.n0sq = wm_vw_001.n1sq
) as t2
on t1.seqno = t2.n1sq
where t1.seqno < 4
order by seqno, smin1 ,inte1, lint1 ,  deci1  ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    
    # -----FULL OUTER JOIN---------
    _testmgr.testcase_end(desc)

def test010(desc="""J012"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """J012"""
    stmt = """prepare s1 from SELECT  seqno, smin1 ,inte1, lint1 ,  deci1
FROM
wm000  t1
FULL OUTER JOIN
(select *
from wm_vw_000 FULL OUTER JOIN  wm_vw_001
on wm_vw_000.n0sq= wm_vw_001.n1sq
) as t2
on t1.seqno = t2.n1sq
order by seqno, smin1 ,inte1, lint1 ,  deci1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    
    #--------------------------
    _testmgr.testcase_end(desc)

def test011(desc="""J013"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """J013"""
    stmt = """prepare s1 from SELECT   seqno, smin1 ,inte1, lint1 ,  deci1
FROM
wm000  t1
FULL OUTER JOIN
(select *
from wm_vw_000 FULL OUTER JOIN  wm_vw_001
on wm_vw_000.n0sq= wm_vw_001.n1sq
) as t2
on t1.seqno = t2.n1sq
where t1.seqno < 4
order by seqno, smin1 ,inte1, lint1 ,  deci1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    
    # -----LEFT join---------
    _testmgr.testcase_end(desc)

def test012(desc="""J014"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """J014"""
    stmt = """prepare s1 from SELECT  seqno, smin1 ,inte1, lint1 ,  deci1
FROM
wm000  t1
FULL OUTER JOIN
(select *
from wm_vw_000 LEFT JOIN wm_vw_001
ON wm_vw_000.n0sq = wm_vw_001.n1sq
) as t2
on t1.seqno = t2.n1sq
order by seqno, smin1 ,inte1, lint1 ,  deci1  ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    
    #--------------------------
    _testmgr.testcase_end(desc)

def test013(desc="""J015"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """J015"""
    stmt = """prepare s1 from SELECT  seqno, smin1 ,inte1, lint1 ,  deci1
FROM
wm000  t1
FULL OUTER JOIN
(select *
from wm_vw_000 LEFT JOIN wm_vw_001
ON wm_vw_000.n0sq = wm_vw_001.n1sq
) as t2
on t1.seqno = t2.n1sq
where t1.seqno < 4
order by seqno, smin1 ,inte1, lint1 ,  deci1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    
    # -----Right join---------
    _testmgr.testcase_end(desc)

def test014(desc="""J016"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """J016"""
    stmt = """prepare s1 from SELECT     seqno, smin1 ,inte1, lint1 ,  deci1
FROM
wm000  t1
FULL OUTER JOIN
(select *
from wm_vw_000 RIGHT JOIN  wm_vw_001
ON wm_vw_000.n0sq = wm_vw_001.n1sq
) as t2
on t1.seqno = t2.n1sq
order by seqno, smin1 ,inte1, lint1 ,  deci1  ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    
    #--------------------------
    _testmgr.testcase_end(desc)

def test015(desc="""J017"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """J017"""
    stmt = """prepare s1 from SELECT   seqno, smin1 ,inte1, lint1 ,  deci1
FROM
wm000  t1
FULL OUTER JOIN
(select *
from wm_vw_000 RIGHT JOIN  wm_vw_001
ON wm_vw_000.n0sq = wm_vw_001.n1sq
) as t2
on t1.seqno = t2.n1sq
where t1.seqno < 4
order by seqno, smin1 ,inte1, lint1 ,  deci1  ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    
    # -----Union---------
    _testmgr.testcase_end(desc)

def test016(desc="""J018"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """J018"""
    stmt = """prepare s1 from SELECT  seqno, smin1 ,inte1, lint1 ,  deci1
FROM
wm000  t1
FULL OUTER JOIN
(
SELECT *
from wm_vw_000
UNION
SELECT *
from wm_vw_001
) as t2
on t1.seqno = t2.n0sq
order by seqno, smin1 ,inte1, lint1 ,  deci1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    
    #--------------------------
    _testmgr.testcase_end(desc)

def test017(desc="""J019"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """J019"""
    stmt = """prepare s1 from SELECT     seqno, smin1 ,inte1, lint1 ,  deci1
FROM
wm000  t1
FULL OUTER JOIN
(select *
from wm_vw_000
UNION
SELECT  *
from wm_vw_001
) as t2
on t1.seqno = t2.n0sq
where t1.seqno < 4
order by  seqno, smin1 ,inte1, lint1 ,  deci1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    
    # -----Union All---------
    _testmgr.testcase_end(desc)

def test018(desc="""J020"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """J020"""
    stmt = """prepare s1 from SELECT  seqno, smin1 ,inte1, lint1 ,  deci1
FROM
wm000  t1
FULL OUTER JOIN
(
SELECT *
from wm_vw_000
UNION  ALL
SELECT *
from wm_vw_001
) as t2
on t1.seqno = t2.n0sq
order by  seqno, smin1 ,inte1, lint1 ,  deci1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    
    #--------------------------
    _testmgr.testcase_end(desc)

def test019(desc="""J021"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """J021"""
    stmt = """prepare s1 from SELECT  [ first 5]  seqno, smin1 ,inte1, lint1 ,  deci1
FROM
wm000  t1
FULL OUTER JOIN
(
SELECT *
from wm_vw_000
UNION  ALL
SELECT *
from wm_vw_001
) as t2
on t1.seqno = t2.n0sq
where t1.seqno < 4
order by seqno, smin1 ,inte1, lint1 ,  deci1  ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

