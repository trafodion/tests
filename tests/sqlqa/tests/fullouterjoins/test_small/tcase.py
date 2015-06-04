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

# Tests  FROM foj2.sql (A001-A015)
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""A001"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A001"""
    stmt = """prepare s1 from
SELECT  10618,
ZEROIFNULL(t2.store_count),
ZEROIFNULL(t1.store_count)
FROM  ( SELECT     cash01a.item_nbr,
COUNT(DISTINCT( cash01a.store_nbr ))
FROM     cash01a
GROUP     BY 1
) t1 (item_nbr, store_count )
FULL OUTER JOIN
( SELECT     cash01a.item_nbr,
COUNT(DISTINCT( cash01a.store_nbr ))
FROM     cash01a
WHERE     cash01a.ON_hand_qty > 0
GROUP BY 1
) t2 (item_nbr, store_count )
ON       t1.item_nbr = t2.item_nbr
ORDER BY t1.item_nbr ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test002(desc="""A002"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A002"""
    stmt = """prepare s1 from
SELECT  t1.item_nbr,
10618,
ZEROIFNULL(t1.store_count)
FROM  ( SELECT     cash01a.item_nbr,
COUNT(DISTINCT( cash01a.store_nbr ))
FROM     cash01a
GROUP     BY 1
) t1 (item_nbr, store_count )
FULL OUTER JOIN
( SELECT     cash01a.item_nbr,
COUNT(DISTINCT( cash01a.store_nbr ))
FROM     cash01a
WHERE     cash01a.ON_hand_qty > 0 GROUP BY 1
)  t2 (item_nbr, store_count )
ON       t1.item_nbr = t2.item_nbr
ORDER BY t1.item_nbr ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test003(desc="""A003"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A003"""
    stmt = """prepare s1 from
SELECT  t1.item_nbr,
10618,
ZEROIFNULL(t2.store_count),
ZEROIFNULL(t1.store_count)
FROM  ( SELECT     cash01a.item_nbr,
COUNT(DISTINCT( cash01a.store_nbr ))
FROM     cash01a
GROUP     BY 1
) t1 (item_nbr, store_count )
FULL OUTER JOIN
( SELECT     cash01a.item_nbr,
COUNT( DISTINCT( cash01a.store_nbr ))
FROM     cash01a
WHERE     cash01a.ON_hand_qty > 0
GROUP BY 1
) t2 (item_nbr, store_count )
ON       t1.item_nbr = t2.item_nbr
ORDER BY t1.item_nbr ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test004(desc="""A004"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A004"""
    stmt = """prepare s1 from
SELECT  t1.item_nbr,
10618,
t1.store_nbr,
ZEROIFNULL(t1.store_count)
FROM  ( SELECT      cash01a.item_nbr,
COUNT( DISTINCT( cash01a.store_nbr )),
cash01a.store_nbr
FROM      cash01a
GROUP BY 1, 3
) t1 (item_nbr, store_count , store_nbr)
FULL OUTER JOIN
( SELECT      cash01a.item_nbr,
COUNT( DISTINCT( cash01a.store_nbr )),
cash01a.store_nbr
FROM      cash01a
WHERE      cash01a.ON_hand_qty > 0
GROUP BY 1, 3
) t2 (item_nbr, store_count , store_nbr)
ON       t1.item_nbr  = t2.item_nbr and
t1.store_nbr = t2.store_nbr
ORDER BY t1.item_nbr ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test005(desc="""A005"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A005"""
    stmt = """prepare s1 from
SELECT t1.item_nbr,
ZEROIFNULL(t1.store_count)
FROM ( SELECT     cash01a.item_nbr,
COUNT( DISTINCT( cash01a.store_nbr ))
FROM         cash01a
GROUP     BY 1
) t1 (item_nbr, store_count )
FULL OUTER JOIN
( SELECT     cash01a.item_nbr,
COUNT( DISTINCT( cash01a.store_nbr ))
FROM         cash01a
WHERE     cash01a.ON_hand_qty > 0
GROUP BY 1
) t2 (item_nbr, store_count )
ON        t1.item_nbr = t2.item_nbr
ORDER BY t1.item_nbr ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test006(desc="""A006"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A006"""
    stmt = """prepare s1 from
SELECT  t1.item_nbr,
ZEROIFNULL(t1.store_count),
ZEROIFNULL(t2.store_count)
FROM  ( SELECT     cash01a.item_nbr,
COUNT(DISTINCT( cash01a.store_nbr ))
FROM     cash01a
GROUP     BY 1
) t1 (item_nbr, store_count )
FULL OUTER JOIN
( SELECT     cash01a.item_nbr,
COUNT(DISTINCT( cash01a.store_nbr ))
FROM     cash01a
WHERE     cash01a.ON_hand_qty > 0
GROUP BY 1
)  t2 (item_nbr, store_count )
ON       t1.item_nbr = t2.item_nbr
ORDER BY t1.item_nbr;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test007(desc="""A007"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A007"""
    stmt = """prepare s1 from
SELECT  t1.item_nbr,
ZEROIFNULL(t2.store_count),
ZEROIFNULL(t1.store_count)
FROM  ( SELECT     cash01a.item_nbr,
COUNT( DISTINCT( cash01a.store_nbr ))
FROM     cash01a
GROUP     BY 1
)  t1 (item_nbr, store_count )
FULL OUTER JOIN
( SELECT     cash01a.item_nbr,
COUNT(DISTINCT( cash01a.store_nbr ))
FROM     cash01a
WHERE     cash01a.ON_hand_qty > 0
GROUP BY 1
) t2 (item_nbr, store_count )
ON       t1.item_nbr = t2.item_nbr
ORDER BY t1.item_nbr ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test008(desc="""A008"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A008"""
    stmt = """prepare s1 from
SELECT  t1.item_nbr,
t1.store_nbr,
10618,
ZEROIFNULL(t1.store_count)
FROM  ( SELECT     cash01a.item_nbr,
COUNT( DISTINCT( cash01a.store_nbr )),
cash01a.store_nbr
FROM     cash01a
GROUP     BY 1 , 3
) t1 (item_nbr, store_count , store_nbr)
FULL OUTER JOIN
( SELECT     cash01a.item_nbr,
COUNT( DISTINCT( cash01a.store_nbr )),
cash01a.store_nbr
FROM     cash01a
WHERE     cash01a.ON_hand_qty > 0
GROUP BY 1 , 3
) t2 (item_nbr, store_count , store_nbr)
ON       t1.item_nbr = t2.item_nbr and
t1.store_nbr = t2.store_nbr
ORDER BY t1.item_nbr;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test009(desc="""A009"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A009"""
    stmt = """prepare s1 from
SELECT  t1.item_nbr,
t1.store_nbr,
10618,
ZEROIFNULL(t1.store_count),
ZEROIFNULL(t2.store_count)
FROM  ( SELECT     cash01a.item_nbr,
COUNT( DISTINCT( cash01a.store_nbr )),
cash01a.store_nbr
FROM     cash01a
GROUP     BY 1 , 3
) t1 (item_nbr, store_count , store_nbr)
FULL OUTER JOIN
( SELECT     cash01a.item_nbr,
COUNT( DISTINCT( cash01a.store_nbr )),
cash01a.store_nbr
FROM     cash01a
WHERE     cash01a.ON_hand_qty > 0
GROUP BY 1 , 3
) t2 (item_nbr, store_count , store_nbr)
ON       t1.item_nbr = t2.item_nbr and
t1.store_nbr = t2.store_nbr
ORDER BY t1.item_nbr ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test010(desc="""A010"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A010"""
    stmt = """prepare s1 from
SELECT  t1.item_nbr,
t1.store_nbr,
ZEROIFNULL(t1.store_count)
FROM  ( SELECT     cash01a.item_nbr,
COUNT( DISTINCT( cash01a.store_nbr )),
cash01a.store_nbr
FROM     cash01a
GROUP     BY 1 , 3
) t1 (item_nbr, store_count , store_nbr)
FULL OUTER JOIN
( SELECT     cash01a.item_nbr,
COUNT( DISTINCT( cash01a.store_nbr )),
cash01a.store_nbr
FROM     cash01a
WHERE     cash01a.ON_hand_qty > 0
GROUP BY 1 , 3
) t2 (item_nbr, store_count , store_nbr)
ON       t1.item_nbr = t2.item_nbr and
t1.store_nbr = t2.store_nbr
ORDER BY t1.item_nbr ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test011(desc="""A011"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A011"""
    stmt = """prepare s1 from
SELECT  t1.item_nbr,
t1.store_nbr,
ZEROIFNULL(t1.store_count),
ZEROIFNULL(t2.store_count)
FROM  ( SELECT     cash01a.item_nbr,
COUNT( DISTINCT( cash01a.store_nbr )),
cash01a.store_nbr
FROM     cash01a
GROUP     BY 1 , 3
) t1 (item_nbr, store_count , store_nbr)
FULL OUTER JOIN
( SELECT     cash01a.item_nbr,
COUNT(DISTINCT( cash01a.store_nbr )),
cash01a.store_nbr
FROM     cash01a
WHERE     cash01a.ON_hand_qty > 0
GROUP BY 1 , 3
) t2 (item_nbr, store_count , store_nbr)
ON       t1.item_nbr = t2.item_nbr and
t1.store_nbr = t2.store_nbr
ORDER BY t1.item_nbr ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test012(desc="""A012"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A012"""
    stmt = """prepare s1 from
SELECT t1.item_nbr,
t1.store_nbr,
ZEROIFNULL(t2.store_count),
ZEROIFNULL(t1.store_count)
FROM ( SELECT     cash01a.item_nbr,
COUNT( DISTINCT( cash01a.store_nbr )),
cash01a.store_nbr
FROM         cash01a
GROUP     BY 1 , 3
) t1 (item_nbr, store_count , store_nbr)
FULL OUTER JOIN
( SELECT     cash01a.item_nbr,
COUNT( DISTINCT( cash01a.store_nbr )),
cash01a.store_nbr
FROM         cash01a
WHERE     cash01a.ON_hand_qty > 0
GROUP BY 1 , 3
) t2 (item_nbr, store_count , store_nbr)
ON      t1.item_nbr = t2.item_nbr and
t1.store_nbr = t2.store_nbr
ORDER BY t1.item_nbr ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test013(desc="""A013"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A013"""
    stmt = """prepare s1 from
SELECT  t1.store_nbr,
ZEROIFNULL(t1.store_count)
FROM  ( SELECT     cash01a.item_nbr,
COUNT( DISTINCT( cash01a.store_nbr )),
cash01a.store_nbr
FROM     cash01a
GROUP     BY 1 , 3
) t1 (item_nbr, store_count , store_nbr)
FULL OUTER JOIN
( SELECT     cash01a.item_nbr,
COUNT( DISTINCT( cash01a.store_nbr )),
cash01a.store_nbr
FROM     cash01a
WHERE     cash01a.ON_hand_qty > 0
GROUP BY 1 , 3
) t2 (item_nbr, store_count , store_nbr)
ON       t1.item_nbr = t2.item_nbr and
t1.store_nbr = t2.store_nbr
ORDER BY t1.item_nbr ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test014(desc="""A014"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A014"""
    stmt = """prepare s1 from
SELECT  t1.store_nbr,
ZEROIFNULL( t2.store_count),
ZEROIFNULL( t1.store_count)
FROM  ( SELECT     cash01a.item_nbr,
COUNT( DISTINCT( cash01a.store_nbr )),
cash01a.store_nbr
FROM     cash01a
GROUP     BY 1 , 3
)  t1 (item_nbr, store_count , store_nbr)
FULL OUTER JOIN
( SELECT     cash01a.item_nbr,
COUNT( DISTINCT( cash01a.store_nbr )),
cash01a.store_nbr
FROM     cash01a
WHERE     cash01a.on_hand_qty > 0
GROUP BY 1 , 3
) t2 (item_nbr, store_count , store_nbr)
ON       t1.item_nbr = t2.item_nbr and
t1.store_nbr = t2.store_nbr
ORDER BY t1.item_nbr ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test015(desc="""A015"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A015"""
    stmt = """prepare s1 from
SELECT  t1.store_nbr,
t1.item_nbr,
ZEROIFNULL( t1.store_count)
FROM  ( SELECT     cash01a.item_nbr,
COUNT( DISTINCT( cash01a.store_nbr )),
cash01a.store_nbr
FROM     cash01a
GROUP     BY 1 , 3
) t1 (item_nbr, store_count , store_nbr)
FULL OUTER JOIN
( SELECT     cash01a.item_nbr,
COUNT(DISTINCT( cash01a.store_nbr )),
cash01a.store_nbr
FROM     cash01a
WHERE     cash01a.ON_hand_qty > 0
GROUP BY 1 , 3
) t2 (item_nbr, store_count , store_nbr)
ON       t1.item_nbr = t2.item_nbr and
t1.store_nbr = t2.store_nbr
ORDER BY t1.item_nbr;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    # Tests
    # FROM fullouter.sql  (A101-A136)
    _testmgr.testcase_end(desc)

def test016(desc="""A101"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A101"""
    stmt = """prepare s1 from
select   a.seqno,
b.seqno
FROM      wm000 a
FULL OUTER JOIN
wm001 b
ON       a.seqno = b.seqno
ORDER BY a.seqno, b.seqno ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test017(desc="""A102"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A102"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.smin1,
b.smin1
FROM     wm000 a
FULL OUTER JOIN
wm001 b
ON      a.smin1 = b.smin1
ORDER BY a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test018(desc="""A103"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A103"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.inte1,
b.inte1
FROM     wm000 a
FULL OUTER JOIN
wm001 b
ON      a.inte1 = b.inte1
ORDER BY a.seqno, b.seqno, a.inte1, b.inte1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test019(desc="""A104"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A104"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.lint1,
b.lint1
FROM     wm000 a
FULL OUTER JOIN
wm001 b
ON      a.lint1 = b.lint1
ORDER BY a.seqno, b.seqno, a.lint1, b.lint1      ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test020(desc="""A105"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A105"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.nume1,
b.nume1
FROM     wm000 a
FULL OUTER JOIN
wm001 b
ON      a.nume1 = b.nume1
ORDER BY a.seqno, b.seqno, a.nume1, b.nume1      ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test021(desc="""A106"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A106"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.deci1,
b.deci1
FROM     wm000 a
FULL OUTER JOIN
wm001 b
ON      a.deci1 = b.deci1
ORDER BY a.seqno, b.seqno, a.deci1, b.deci1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test022(desc="""A107"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A107"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.pict1,
b.pict1
FROM     wm000 a
FULL OUTER JOIN
wm001 b
ON      a.pict1 = b.pict1
ORDER BY a.seqno, b.seqno, a.pict1, b.pict1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test023(desc="""A108"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A108"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.flot1,
b.flot1
FROM     wm000 a
FULL OUTER JOIN
wm001 b
ON      a.flot1 = b.flot1
ORDER BY a.seqno, b.seqno, a.flot1, b.flot1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test024(desc="""A109"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A109"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.real1,
b.real1
FROM     wm000 a
FULL OUTER JOIN
wm001 b
ON      a.real1 = b.real1
ORDER BY a.seqno, b.seqno, a.real1, b.real1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test025(desc="""A110"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A110"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.dblp1,
b.dblp1
FROM     wm000 a
FULL OUTER JOIN
wm001 b
ON      a.dblp1 = b.dblp1
ORDER BY a.seqno, b.seqno, a.dblp1, b.dblp1  ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test026(desc="""A111"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A111"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.char1,
b.char1
FROM     wm000 a
FULL OUTER JOIN
wm001 b
ON      a.char1 = b.char1
ORDER BY a.seqno, b.seqno, a.char1, b.char1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test027(desc="""A112"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A112"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.vchr1,
b.vchr1
FROM     wm000 a
FULL OUTER JOIN
wm001 b
ON      a.vchr1 = b.vchr1
ORDER BY a.seqno, b.seqno, a.vchr1, b.vchr1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test028(desc="""A113"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A113"""
    stmt = """prepare s1 from
select     a.n0sq,
b.n1sq,
a.n0sq,
b.n1sq
FROM     wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON      a.n0sq = n1sq
ORDER BY a.n0sq, b.n1sq, a.n0sq, b.n1sq ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test029(desc="""A114"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A114"""
    stmt = """prepare s1 from
select     a.n0sq,
b.n1sq,
a.n0s1,
b.n1s1
FROM     wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON      a.n0s1 = b.n1s1
ORDER BY a.n0sq, b.n1sq, a.n0s1, b.n1s1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test030(desc="""A115"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A115"""
    stmt = """prepare s1 from
select     a.n0sq,
b.n1sq,
a.n0i1,
b.n1i1
FROM     wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON      a.n0i1 = b.n1i1
ORDER BY a.n0sq, b.n1sq, a.n0i1, b.n1i1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test031(desc="""A116"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A116"""
    stmt = """prepare s1 from
select     a.n0sq,
b.n1sq,
a.n0l1,
b.n1s1
FROM     wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON      a.n0l1 = b.n1l1
ORDER BY a.n0sq, b.n1sq, a.n0l1, b.n1s1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test032(desc="""A117"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A117"""
    stmt = """prepare s1 from
select     a.n0sq,
b.n1sq,
a.n0n1,
b.n1n1
FROM     wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON      a.n0n1 = b.n1n1
ORDER BY a.n0sq, b.n1sq, a.n0n1, b.n1n1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test033(desc="""A118"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A118"""
    stmt = """prepare s1 from
select     a.n0sq,
b.n1sq,
a.n0d1,
b.n1d1
FROM     wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON      a.n0d1 = b.n1d1
ORDER BY a.n0sq, b.n1sq, a.n0d1, b.n1d1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test034(desc="""A119"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A119"""
    stmt = """prepare s1 from
select     a.n0sq,
b.n1sq,
a.n0p1,
b.n1p1
FROM     wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON      a.n0p1 = b.n1p1
ORDER BY a.n0sq, b.n1sq, a.n0p1, b.n1p1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test035(desc="""A120"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A120"""
    stmt = """prepare s1 from
select     a.n0sq,
b.n1sq,
a.n0f1,
b.n1f1
FROM     wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON      a.n0f1 = b.n1f1
ORDER BY a.n0sq, b.n1sq, a.n0f1, b.n1f1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test036(desc="""A121"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A121"""
    stmt = """prepare s1 from
select     a.n0sq,
b.n1sq,
a.n0r1,
b.n1r1
FROM     wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON      a.n0r1 = b.n1r1
ORDER BY a.n0sq, b.n1sq, a.n0r1, b.n1r1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test037(desc="""A122"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A122"""
    stmt = """prepare s1 from
select     a.n0sq,
b.n1sq,
a.n0dp1,
b.n1dp1
FROM     wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON      a.n0dp1 = b.n1dp1
ORDER BY a.n0sq, b.n1sq, a.n0dp1, b.n1dp1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test038(desc="""A123"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A123"""
    stmt = """prepare s1 from
select     a.n0sq,
b.n1sq,
a.n0c1,
b.n1c1
FROM     wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON      a.n0c1 = b.n1c1
ORDER BY a.n0sq, b.n1sq, a.n0c1, b.n1c1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test039(desc="""A124"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A124"""
    stmt = """prepare s1 from
select     a.n0sq,
b.n1sq,
a.n0v1,
b.n1v1
FROM     wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON      a.n0v1 = b.n1v1
ORDER BY a.n0sq, b.n1sq, a.n0v1, b.n1v1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test040(desc="""A125"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A125"""
    stmt = """prepare s1 from
select     *
FROM
( select seqno FROM wm000) a(sq)
FULL OUTER JOIN
( select seqno FROM wm001) b(sq)
ON  a.sq = b.sq
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test041(desc="""A126"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A126"""
    stmt = """prepare s1 from
select     *
FROM
( select smin1 FROM wm000) a(s)
FULL OUTER JOIN
( select smin1 FROM wm001) b(s)
ON  a.s = b.s
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test042(desc="""A127"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A127"""
    stmt = """prepare s1 from
select     *
FROM
( select inte1 FROM wm000) a(i)
FULL OUTER JOIN
( select inte1 FROM wm001) b(i)
ON  a.i = b.i
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test043(desc="""A128"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A128"""
    stmt = """prepare s1 from
select     *
FROM
(select lint1 FROM wm000) a(l)
FULL OUTER JOIN
(select lint1 FROM wm001) b(l)
ON  a.l = b.l
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test044(desc="""A129"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A129"""
    stmt = """prepare s1 from
select     *
FROM
( select nume1 FROM wm000) a(n)
FULL OUTER JOIN
( select nume1 FROM wm001) b(n)
ON  a.n = b.n
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test045(desc="""A130"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A130"""
    stmt = """prepare s1 from
select     *
FROM
( select deci1 FROM wm000) a(d)
FULL OUTER JOIN
( select deci1 FROM wm001) b(d)
ON  a.d = b.d
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test046(desc="""A131"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A131"""
    stmt = """prepare s1 from
select     *
FROM
( select pict1 FROM wm000) a(p)
FULL OUTER JOIN
( select pict1 FROM wm001) b(p)
ON  a.p = b.p
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test047(desc="""A132"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A132"""
    stmt = """prepare s1 from
select     *
FROM
( select flot1 FROM wm000) a(f)
FULL OUTER JOIN
( select flot1 FROM wm001) b(f)
ON  a.f = b.f
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test048(desc="""A133"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A133"""
    stmt = """prepare s1 from
select     *
FROM
( select real1 FROM wm000) a(r)
FULL OUTER JOIN
( select real1 FROM wm001) b(r)
ON  a.r = b.r
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test049(desc="""A134"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A134"""
    stmt = """prepare s1 from
select     *
FROM
( select dblp1 FROM wm000) a(dp)
FULL OUTER JOIN
( select dblp1 FROM wm001) b(dp)
ON  a.dp = b.dp
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test050(desc="""A135"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A135"""
    stmt = """prepare s1 from
select     *
FROM
( select char1 FROM wm000) a(c)
FULL OUTER JOIN
( select char1 FROM wm001) b(c)
ON  a.c = b.c
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test051(desc="""A136"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A136"""
    stmt = """prepare s1 from
select     *
FROM
( select vchr1 FROM wm000) a(v)
FULL OUTER JOIN
( select vchr1 FROM wm001) b(v)
ON  a.v = b.v
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    # Elena Krotkova 5/24/07
    #  tables FOJ + where
    _testmgr.testcase_end(desc)

def test052(desc="""W101"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """W101"""
    stmt = """prepare s1 from
select a.seqno,
b.seqno,
a.smin1,
b.smin1
FROM   wm000 a
FULL OUTER JOIN
wm001 b
ON        a.seqno = b.seqno
where (a.seqno > 3 and a.smin1 < 123) or
a.seqno <5
ORDER BY a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test053(desc="""W102"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """W102"""
    stmt = """prepare s1 from
select      a.seqno,
b.seqno,
a.smin1,
b.smin1
FROM           wm000 a
FULL OUTER JOIN
wm001 b
ON             a.smin1 = b.smin1
where (a.seqno > 3 and a.smin1 < 123) or b.smin1 = 1
ORDER BY a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test054(desc="""W103"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """W103"""
    stmt = """prepare s1 from
select      a.seqno,
b.seqno,
a.inte1,
b.inte1
FROM           wm000 a
FULL OUTER JOIN
wm001 b
ON             a.inte1 = b.inte1
where (a.inte1 > 3 and a.smin1 < 123) or
b.inte1 = 2
ORDER BY a.seqno, b.seqno, a.inte1, b.inte1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test055(desc="""W104"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """W104"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.lint1,
b.lint1
FROM           wm000 a
FULL OUTER JOIN
wm001 b
ON             a.lint1 = b.lint1
where(a.lint1 > 3 and a.smin1 < 123) or
b.lint1 = 2
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test056(desc="""W105"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """W105"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.nume1,
b.nume1
FROM           wm000 a
FULL OUTER JOIN
wm001 b
ON            a.nume1 = b.nume1
where (a.nume1  > 3 and a.smin1 < 1230) or
b.nume1  = 0 or b.nume1  <> 763.463
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test057(desc="""W106"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """W106"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.deci1,
b.deci1
FROM           wm000 a
FULL OUTER JOIN
wm001 b
ON             a.deci1 = b.deci1
where (a.deci1  > 3 and a.smin1 < 1230) or
(b.deci1 <= 1 or a.deci1 <> -1000000 )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test058(desc="""W107"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """W107"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.pict1,
b.pict1
FROM           wm000 a
FULL OUTER JOIN
wm001 b
ON             a.pict1 = b.pict1
where (a.pict1  > 3 and a.smin1 < 1230) or
( b.pict1  > 1 or a.pict1  < 1 )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test059(desc="""W108"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """W108"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.flot1,
b.flot1
FROM           wm000 a
FULL OUTER JOIN
wm001 b
ON             a.flot1 = b.flot1
where (a.flot1   < 3 and a.smin1 > 1230) or
( b.flot1   > 1 or a.flot1  <> 0 )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test060(desc="""W109"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """W109"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.real1,
b.real1
FROM           wm000 a
FULL OUTER JOIN
wm001 b
ON             a.real1 = b.real1
where (a.real1   < 3 and a.smin1 < 123) or
( b.real1   < 4 and a.real1  > 1 )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test061(desc="""W110"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """W110"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.dblp1,
b.dblp1
FROM           wm000 a
FULL OUTER JOIN
wm001 b
ON             a.dblp1 = b.dblp1
where (a.dblp1   > 8 and a.smin1 < 123) or
( b.dblp1   < 1 or a.dblp1  <> 0 )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test062(desc="""W111"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """W111"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.char1,
b.char1
FROM           wm000 a
FULL OUTER JOIN
wm001 b
ON             a.char1 = b.char1
where (a.char1   >'8' and a.smin1 < 1023) or
( b.char1   <= '1' or a.char1  <> '0' )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test063(desc="""W112"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """W112"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.vchr1,
b.vchr1
FROM           wm000 a
FULL OUTER JOIN
wm001 b
ON             a.vchr1 = b.vchr1
where (a.vchr1  > '8' and a.smin1 < 35000) or
( b.vchr1   >= '1' or a.vchr1  <> '112345' )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    # views FOJ + where clause
    # ---------------------1------------------------------------------
    _testmgr.testcase_end(desc)

def test064(desc="""W113"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """W113"""
    stmt = """prepare s1 from
select     a.n0sq,
b.n1sq,
a.n0sq,
b.n1sq
FROM           wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON             a.n0sq = n1sq
where (a.n0sq > 3 and n0s1 < 123) or
n0sq <5
ORDER BY       a.n0sq, b.n1sq, a.n0sq,     b.n1sq ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    # ----------------------2-----------------------------------------
    _testmgr.testcase_end(desc)

def test065(desc="""W114"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """W114"""
    stmt = """prepare s1 from
select     a.n0sq,
b.n1sq,
a.n0s1,
b.n1s1
FROM           wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON             a.n0s1 = b.n1s1
where (a.n0sq > 3 and n0s1 < 123) or n0s1 = 1
ORDER BY       a.n0sq, b.n1sq, a.n0sq,     b.n1sq      ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    # -----------------------3----------------------------------------
    _testmgr.testcase_end(desc)

def test066(desc="""W115"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """W115"""
    stmt = """prepare s1 from
select     a.n0sq,
b.n1sq,
a.n0i1,
b.n1i1
FROM           wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON             a.n0i1 = b.n1i1
where (a.n0i1 > 3 and a.n0s1 < 123) or
b.n1i1 = 2
ORDER BY       a.n0sq, b.n1sq, a.n0sq,     b.n1sq      ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    # ------------------------4---------------------------------------
    _testmgr.testcase_end(desc)

def test067(desc="""W116"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """W116"""
    stmt = """prepare s1 from
select     a.n0sq,
b.n1sq,
a.n0l1,
b.n1s1
FROM           wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON             a.n0l1 = b.n1l1
where (a.n0l1 > 3 and a.n0s1 < 123) or
b.n1l1 = 2
ORDER BY       a.n0sq, b.n1sq, a.n0sq,     b.n1sq      ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    # -------------------------5--------------------------------------
    _testmgr.testcase_end(desc)

def test068(desc="""W117"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """W117"""
    stmt = """prepare s1 from
select     a.n0sq,
b.n1sq,
a.n0n1,
b.n1n1
FROM           wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON             a.n0n1 = b.n1n1
where (a.n0n1  > 3 and a.n0s1 < 1230) or
b.n1n1  = 0 or
b.n1n1  <> 9
ORDER BY       a.n0sq, b.n1sq, a.n0sq,     b.n1sq      ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    # --------------------------6-------------------------------------
    _testmgr.testcase_end(desc)

def test069(desc="""W118"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """W118"""
    stmt = """prepare s1 from
select     a.n0sq,
b.n1sq,
a.n0d1,
b.n1d1
FROM           wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON             a.n0d1 = b.n1d1
where (a.n0d1 > 3 and a.n0s1 < 1230) or
(b.n1d1<= 1 or a.n0d1 = 10000 )
ORDER BY       a.n0sq, b.n1sq, a.n0sq,     b.n1sq       ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    # ---------------------------7------------------------------------
    _testmgr.testcase_end(desc)

def test070(desc="""W119"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """W119"""
    stmt = """prepare s1 from
select     a.n0sq,
b.n1sq,
a.n0p1,
b.n1p1
FROM           wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON             a.n0p1 = b.n1p1
where (a.n0p1  > 3 and a.n0s1 < 1230) or
( b.n1p1  > 1 or a.n0p1  = 0 )
ORDER BY       a.n0sq, b.n1sq, a.n0sq,     b.n1sq      ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    # ----------------------------8-----------------------------------
    _testmgr.testcase_end(desc)

def test071(desc="""W120"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """W120"""
    stmt = """prepare s1 from
select     a.n0sq,
b.n1sq,
a.n0f1,
b.n1f1
FROM           wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON             a.n0f1 = b.n1f1
where (a.n0f1  < 3 and a.n0s1 < 1230) or
( b.n1f1  > 1 or a.n0f1 = 0 )
ORDER BY       a.n0sq, b.n1sq, a.n0sq,     b.n1sq      ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    # -----------------------------9----------------------------------
    _testmgr.testcase_end(desc)

def test072(desc="""W121"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """W121"""
    stmt = """prepare s1 from
select     a.n0sq,
b.n1sq,
a.n0r1,
b.n1r1
FROM           wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON             a.n0r1 = b.n1r1
where (a.n0r1  < 3 and a.n0s1 < 123) or
( b.n1r1  < 1 or a.n0r1 = 0 )
ORDER BY       a.n0sq, b.n1sq, a.n0sq,     b.n1sq      ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    # ----------------------------10-----------------------------------
    _testmgr.testcase_end(desc)

def test073(desc="""W122"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """W122"""
    stmt = """prepare s1 from
select     a.n0sq,
b.n1sq,
a.n0dp1,
b.n1dp1
FROM           wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON             a.n0dp1 = b.n1dp1
where (a.n0dp1   > 8 and a.n0s1 < 123) or
( b.n1dp1   < 1 and a.n0dp1  >1 )
ORDER BY       a.n0sq, b.n1sq, a.n0sq,     b.n1sq      ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test074(desc="""W123"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """W123"""
    stmt = """prepare s1 from
select     a.n0sq,
b.n1sq,
a.n0c1,
b.n1c1
FROM           wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON             a.n0c1 = b.n1c1
where (a.n0c1   > '8' and a.n0s1 < 1023) or
( b.n1c1   <= '10' or a.n0c1  <> '1' )
ORDER BY       a.n0sq, b.n1sq, a.n0sq,     b.n1sq      ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test075(desc="""W124"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """W124"""
    stmt = """prepare s1 from
select     a.n0sq,
b.n1sq,
a.n0v1,
b.n1v1
FROM           wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON             a.n0v1 = b.n1v1
where (a.n0v1  > '8' and a.n0s1 < 35000) or
( b.n1v1    >= '1' or a.n0v1  <> '11' )
ORDER BY       a.n0sq, b.n1sq, a.n0sq,     b.n1sq      ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test076(desc="""W125"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """W125"""
    stmt = """prepare s1 from
select     a.n0sq,
b.n1sq,
a.n0v1,
b.n1v1
FROM           wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON             a.n0v1 = b.n1v1
where (b.n1v1  > '8' and b.n1s1 < 35000) or
( b.n1v1    >= '1' or b.n1v1  <> '11' )
ORDER BY       a.n0sq, b.n1sq, a.n0sq,     b.n1sq      ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    # ---------------------------rest------------------------------------
    # Multi Joins
    #--------------------------
    # some of FOJ do not have equality match
    #--------------------------
    _testmgr.testcase_end(desc)

def test077(desc="""M001"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """M001"""
    stmt = """prepare s1 from
SELECT     a.seqno,
b.seqno
FROM       wm000 a
FULL OUTER JOIN
wm001 b
ON         a.seqno = b.seqno
FULL OUTER JOIN
vt_wm000 c
ON         a.seqno = c.seqno
FULL OUTER JOIN
wm003 d
ON         b.seqno = d.seqno
FULL OUTER JOIN
wm005 e
ON         b.seqno = e.seqno
FULL OUTER JOIN
tab006 f
ON         b.seqno = f.a
FULL OUTER JOIN
vt_wm001 g
ON         b.seqno = g.seqno
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test078(desc="""M002"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """M002"""
    stmt = """prepare s1 from
SELECT     a.seqno,
b.seqno
FROM       wm000 a
FULL OUTER JOIN
wm000 b
ON         a.seqno = b.seqno
FULL OUTER JOIN
vt_wm000 c
ON         a.seqno = c.seqno
FULL OUTER JOIN
vt_wm001 d
ON         b.seqno = d.seqno
FULL OUTER JOIN
wm_vw_003 e
ON         b.seqno = e.n0sq
FULL OUTER JOIN
wm_vw_001  f
ON         b.seqno = f.n1sq
FULL OUTER JOIN
vt_wm001 g
ON         b.seqno = g.seqno
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    
    #--------------------------
    # nested FOJ
    # mixed veiws tables ant vt tables
    # some tables have no values(empty)
    #--------------------------
    _testmgr.testcase_end(desc)

def test079(desc="""M003"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """M003"""
    stmt = """prepare s1 from select   v.flot1,
w.seqno
from
(select x.flot1,
y.seqno
from
(select b.seqno,
c.flot1
from wm000 b
FULL OUTER JOIN
vt_wm000 c
ON   b.seqno = c.seqno
) as x
FULL OUTER JOIN
( SELECT  d.seqno,
e.n0sq
from
vt_wm001 d
FULL OUTER JOIN
wm_vw_003 e
ON d.seqno = e.n0sq
) as y
ON x.seqno = y.seqno
)   as v
FULL OUTER JOIN
( SELECT  a.n1sq,
b.seqno
from
( select f.n1sq,
g.seqno
from
wm_vw_001  f
FULL OUTER JOIN
vt_wm001 g
ON f.n1sq = g.seqno
) as a
FULL OUTER JOIN
( select g.seqno,
f.smin1
from
wm004  f
FULL OUTER JOIN
wm004 g
ON f.seqno = g.seqno
) as b
ON a.seqno = b.seqno
) as w
ON v.seqno  = w.seqno
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    # FOJ on same tables
    # Scenario: Everything matches on various datatypes.
    _testmgr.testcase_end(desc)

def test080(desc="""SS101"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """SS101"""
    stmt = """prepare s1 from
select   a.seqno,
b.seqno
FROM      wm000 a
FULL OUTER JOIN
wm000 b
ON       a.seqno = b.seqno
ORDER BY a.seqno, b.seqno ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test081(desc="""SS102"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """SS102"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.smin1,
b.smin1
FROM     wm000 a
FULL OUTER JOIN
wm000 b
ON      a.smin1 = b.smin1
ORDER BY a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test082(desc="""SS103"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """SS103"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.inte1,
b.inte1
FROM     wm000 a
FULL OUTER JOIN
wm000 b
ON      a.inte1 = b.inte1
ORDER BY a.seqno, b.seqno, a.inte1, b.inte1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test083(desc="""SS104"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """SS104"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.lint1,
b.lint1
FROM     wm000 a
FULL OUTER JOIN
wm000 b
ON      a.lint1 = b.lint1
ORDER BY a.seqno, b.seqno, a.lint1, b.lint1      ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test084(desc="""SS105"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """SS105"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.nume1,
b.nume1
FROM     wm000 a
FULL OUTER JOIN
wm000 b
ON      a.nume1 = b.nume1
ORDER BY a.seqno, b.seqno, a.nume1, b.nume1      ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test085(desc="""SS106"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """SS106"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.deci1,
b.deci1
FROM     wm000 a
FULL OUTER JOIN
wm000 b
ON      a.deci1 = b.deci1
ORDER BY a.seqno, b.seqno, a.deci1, b.deci1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test086(desc="""SS107"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """SS107"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.pict1,
b.pict1
FROM     wm000 a
FULL OUTER JOIN
wm000 b
ON      a.pict1 = b.pict1
ORDER BY a.seqno, b.seqno, a.pict1, b.pict1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test087(desc="""SS108"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """SS108"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.flot1,
b.flot1
FROM     wm000 a
FULL OUTER JOIN
wm000 b
ON      a.flot1 = b.flot1
ORDER BY a.seqno, b.seqno, a.flot1, b.flot1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test088(desc="""SS109"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """SS109"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.real1,
b.real1
FROM     wm000 a
FULL OUTER JOIN
wm000 b
ON      a.real1 = b.real1
ORDER BY a.seqno, b.seqno, a.real1, b.real1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test089(desc="""SS110"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """SS110"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.dblp1,
b.dblp1
FROM     wm000 a
FULL OUTER JOIN
wm000 b
ON      a.dblp1 = b.dblp1
ORDER BY a.seqno, b.seqno, a.dblp1, b.dblp1  ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test090(desc="""SS111"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """SS111"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.char1,
b.char1
FROM     wm000 a
FULL OUTER JOIN
wm000 b
ON      a.char1 = b.char1
ORDER BY a.seqno, b.seqno, a.char1, b.char1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test091(desc="""SS112"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """SS112"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.vchr1,
b.vchr1
FROM     wm000 a
FULL OUTER JOIN
wm000 b
ON      a.vchr1 = b.vchr1
ORDER BY a.seqno, b.seqno, a.vchr1, b.vchr1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test092(desc="""SSW104"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """SSW104"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.lint1,
b.lint1
FROM           wm000 a
FULL OUTER JOIN
wm000 b
ON             a.lint1 = b.lint1
where(a.lint1 > 3 and a.smin1 < 123) or
b.lint1 = 2
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test093(desc="""SSW105"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """SSW105"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.nume1,
b.nume1
FROM           wm000 a
FULL OUTER JOIN
wm000 b
ON            a.nume1 = b.nume1
where (a.nume1  > 3 and a.smin1 < 1230) or
b.nume1  = 0 or b.nume1  <> 763.463
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test094(desc="""SSW106"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """SSW106"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.deci1,
b.deci1
FROM           wm000 a
FULL OUTER JOIN
wm000 b
ON             a.deci1 = b.deci1
where (a.deci1  > 3 and a.smin1 < 1230) or
(b.deci1 <= 1 or a.deci1 <> -1000000 )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test095(desc="""SSW107"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """SSW107"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.pict1,
b.pict1
FROM           wm000 a
FULL OUTER JOIN
wm000 b
ON             a.pict1 = b.pict1
where (a.pict1  > 3 and a.smin1 < 1230) or
( b.pict1  > 1 or a.pict1  < 1 )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test096(desc="""SSW108"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """SSW108"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.flot1,
b.flot1
FROM           wm000 a
FULL OUTER JOIN
wm000 b
ON             a.flot1 = b.flot1
where (a.flot1   < 3 and a.smin1 > 1230) or
( b.flot1   > 1 or a.flot1  <> 0 )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test097(desc="""SSW109"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """SSW109"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.real1,
b.real1
FROM           wm000 a
FULL OUTER JOIN
wm000 b
ON             a.real1 = b.real1
where (a.real1   < 3 and a.smin1 < 123) or
( b.real1   < 4 and a.real1  > 1 )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test098(desc="""SSW110"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """SSW110"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.dblp1,
b.dblp1
FROM           wm000 a
FULL OUTER JOIN
wm000 b
ON             a.dblp1 = b.dblp1
where (a.dblp1   > 8 and a.smin1 < 123) or
( b.dblp1   < 1 or a.dblp1  <> 0 )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test099(desc="""SSW111"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """SSW111"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.char1,
b.char1
FROM           wm000 a
FULL OUTER JOIN
wm000 b
ON             a.char1 = b.char1
where (a.char1   > '8' and a.smin1 < 1023) or
( b.char1   <= '1' or a.char1  <> '0' )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test100(desc="""SSW112"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """SSW112"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.vchr1,
b.vchr1
FROM           wm000 a
FULL OUTER JOIN
wm000 b
ON             a.vchr1 = b.vchr1
where (a.vchr1  > '8' and a.smin1 < 35000) or
( b.vchr1   >= '1' or a.vchr1  <> '112345' )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test101(desc="""SSW125"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """SSW125"""
    stmt = """prepare s1 from
select     a.n0sq,
b.n0sq,
a.n0v1,
b.n0v1
FROM           wm_vw_000 a
FULL OUTER JOIN
wm_vw_000 b
ON             a.n0v1 = b.n0v1
where (b.n0v1  > '8' and b.n0s1 < 35000) or
( b.n0v1    >= '1' or b.n0v1  <> '11' )
ORDER BY       a.n0sq, b.n0sq, a.n0sq,     b.n0sq      ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

