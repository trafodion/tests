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

# Tests on uniqual FOJ with small tables
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""U001"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U001"""
    stmt = """prepare s1 from
select [first 10]  10618,
ZEROIFNULL(t2.store_count),
ZEROIFNULL(t1.store_count)
FROM  ( select     cash01a.item_nbr,
COUNT(DISTINCT( cash01a.store_nbr ))
FROM     cash01a
GROUP     BY 1
) t1 (item_nbr, store_count )
FULL OUTER JOIN
( select     cash01a.item_nbr,
COUNT(DISTINCT( cash01a.store_nbr ))
FROM     cash01a
WHERE     cash01a.ON_hand_qty > 0
GROUP BY 1
) t2 (item_nbr, store_count )
ON       t1.item_nbr > t2.item_nbr
ORDER BY t1.item_nbr ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test002(desc="""U002"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U002"""
    stmt = """prepare s1 from
select [first 10]  t1.item_nbr,
10618,
ZEROIFNULL(t1.store_count)
FROM  ( select     cash01a.item_nbr,
COUNT(DISTINCT( cash01a.store_nbr ))
FROM     cash01a
GROUP     BY 1
) t1 (item_nbr, store_count )
FULL OUTER JOIN
( select      cash01a.item_nbr,
COUNT(DISTINCT( cash01a.store_nbr ))
FROM     cash01a
WHERE     cash01a.ON_hand_qty > 0 GROUP BY 1
)  t2 (item_nbr, store_count )
ON       t1.item_nbr < t2.item_nbr
ORDER BY t1.item_nbr ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test003(desc="""U003"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U003"""
    stmt = """prepare s1 from
select [first 10]  t1.item_nbr,
10618,
ZEROIFNULL(t2.store_count),
ZEROIFNULL(t1.store_count)
FROM  ( select   cash01a.item_nbr,
COUNT(DISTINCT( cash01a.store_nbr ))
FROM     cash01a
GROUP     BY 1
) t1 (item_nbr, store_count )
FULL OUTER JOIN
( select     cash01a.item_nbr,
COUNT( DISTINCT( cash01a.store_nbr ))
FROM     cash01a
WHERE     cash01a.ON_hand_qty > 0
GROUP BY 1
) t2 (item_nbr, store_count )
ON       t1.item_nbr >= t2.item_nbr
ORDER BY t1.item_nbr ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test004(desc="""U004"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U004"""
    stmt = """prepare s1 from
select [first 10]  t1.item_nbr,
10618,
t1.store_nbr,
ZEROIFNULL(t1.store_count)
FROM  ( select       cash01a.item_nbr,
COUNT( DISTINCT( cash01a.store_nbr )),
cash01a.store_nbr
FROM      cash01a
GROUP BY 1, 3
) t1 (item_nbr, store_count , store_nbr)
FULL OUTER JOIN
( select      cash01a.item_nbr,
COUNT( DISTINCT( cash01a.store_nbr )),
cash01a.store_nbr
FROM      cash01a
WHERE      cash01a.ON_hand_qty > 0
GROUP BY 1, 3
) t2 (item_nbr, store_count , store_nbr)
ON       t1.item_nbr  > t2.item_nbr and
t1.store_nbr = t2.store_nbr
ORDER BY t1.item_nbr ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test005(desc="""U005"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U005"""
    stmt = """prepare s1 from
select [first 10] t1.item_nbr,
ZEROIFNULL(t1.store_count)
FROM ( select     cash01a.item_nbr,
COUNT( DISTINCT( cash01a.store_nbr ))
FROM         cash01a
GROUP     BY 1
) t1 (item_nbr, store_count )
FULL OUTER JOIN
( select     cash01a.item_nbr,
COUNT( DISTINCT( cash01a.store_nbr ))
FROM         cash01a
WHERE     cash01a.ON_hand_qty > 0
GROUP BY 1
) t2 (item_nbr, store_count )
ON        t1.item_nbr < t2.item_nbr
ORDER BY t1.item_nbr ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test006(desc="""U006"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U006"""
    stmt = """prepare s1 from
select [first 10]  t1.item_nbr,
ZEROIFNULL(t1.store_count),
ZEROIFNULL(t2.store_count)
FROM  ( select     cash01a.item_nbr,
COUNT(DISTINCT( cash01a.store_nbr ))
FROM     cash01a
GROUP     BY 1
) t1 (item_nbr, store_count )
FULL OUTER JOIN
( select     cash01a.item_nbr,
COUNT(DISTINCT( cash01a.store_nbr ))
FROM     cash01a
WHERE     cash01a.ON_hand_qty > 0
GROUP BY 1
)  t2 (item_nbr, store_count )
ON       t1.item_nbr > t2.item_nbr
ORDER BY t1.item_nbr;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test007(desc="""U007"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U007"""
    stmt = """prepare s1 from
select [first 10]  t1.item_nbr,
ZEROIFNULL(t2.store_count),
ZEROIFNULL(t1.store_count)
FROM  ( select      cash01a.item_nbr,
COUNT( DISTINCT( cash01a.store_nbr ))
FROM     cash01a
GROUP     BY 1
)  t1 (item_nbr, store_count )
FULL OUTER JOIN
( select      cash01a.item_nbr,
COUNT(DISTINCT( cash01a.store_nbr ))
FROM     cash01a
WHERE     cash01a.ON_hand_qty > 0
GROUP BY 1
) t2 (item_nbr, store_count )
ON       t1.item_nbr < t2.item_nbr
ORDER BY t1.item_nbr ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test008(desc="""U008"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U008"""
    stmt = """prepare s1 from
select [first 10]  t1.item_nbr,
t1.store_nbr,
10618,
ZEROIFNULL(t1.store_count)
FROM  ( select     cash01a.item_nbr,
COUNT( DISTINCT( cash01a.store_nbr )),
cash01a.store_nbr
FROM     cash01a
GROUP     BY 1 , 3
) t1 (item_nbr, store_count , store_nbr)
FULL OUTER JOIN
( select      cash01a.item_nbr,
COUNT( DISTINCT( cash01a.store_nbr )),
cash01a.store_nbr
FROM     cash01a
WHERE     cash01a.ON_hand_qty > 0
GROUP BY 1 , 3
) t2 (item_nbr, store_count , store_nbr)
ON       t1.item_nbr >= t2.item_nbr and
t1.store_nbr = t2.store_nbr
ORDER BY t1.item_nbr;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test009(desc="""U009"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U009"""
    stmt = """prepare s1 from
select [first 10]  t1.item_nbr,
t1.store_nbr,
10618,
ZEROIFNULL(t1.store_count),
ZEROIFNULL(t2.store_count)
FROM  ( select     cash01a.item_nbr,
COUNT( DISTINCT( cash01a.store_nbr )),
cash01a.store_nbr
FROM     cash01a
GROUP     BY 1 , 3
) t1 (item_nbr, store_count , store_nbr)
FULL OUTER JOIN
( select     cash01a.item_nbr,
COUNT( DISTINCT( cash01a.store_nbr )),
cash01a.store_nbr
FROM     cash01a
WHERE     cash01a.ON_hand_qty > 0
GROUP BY 1 , 3
) t2 (item_nbr, store_count , store_nbr)
ON       t1.item_nbr > t2.item_nbr and
t1.store_nbr < t2.store_nbr
ORDER BY t1.item_nbr ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test010(desc="""U010"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U010"""
    stmt = """prepare s1 from
select [first 10]  t1.item_nbr,
t1.store_nbr,
ZEROIFNULL(t1.store_count)
FROM  ( select     cash01a.item_nbr,
COUNT( DISTINCT( cash01a.store_nbr )),
cash01a.store_nbr
FROM     cash01a
GROUP     BY 1 , 3
) t1 (item_nbr, store_count , store_nbr)
FULL OUTER JOIN
( select      cash01a.item_nbr,
COUNT( DISTINCT( cash01a.store_nbr )),
cash01a.store_nbr
FROM     cash01a
WHERE     cash01a.ON_hand_qty > 0
GROUP BY 1 , 3
) t2 (item_nbr, store_count , store_nbr)
ON       t1.item_nbr > t2.item_nbr and
t1.store_nbr > t2.store_nbr
ORDER BY t1.item_nbr ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test011(desc="""U011"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U011"""
    stmt = """prepare s1 from
select [first 10]  t1.item_nbr,
t1.store_nbr,
ZEROIFNULL(t1.store_count),
ZEROIFNULL(t2.store_count)
FROM  ( select     cash01a.item_nbr,
COUNT( DISTINCT( cash01a.store_nbr )),
cash01a.store_nbr
FROM     cash01a
GROUP     BY 1 , 3
) t1 (item_nbr, store_count , store_nbr)
FULL OUTER JOIN
( select    cash01a.item_nbr,
COUNT(DISTINCT( cash01a.store_nbr )),
cash01a.store_nbr
FROM     cash01a
WHERE     cash01a.ON_hand_qty > 0
GROUP BY 1 , 3
) t2 (item_nbr, store_count , store_nbr)
ON       t1.item_nbr < t2.item_nbr and
t1.store_nbr < t2.store_nbr
ORDER BY t1.item_nbr ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test012(desc="""U012"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U012"""
    stmt = """prepare s1 from
select [first 10] t1.item_nbr,
t1.store_nbr,
ZEROIFNULL(t2.store_count),
ZEROIFNULL(t1.store_count)
FROM ( select      cash01a.item_nbr,
COUNT( DISTINCT( cash01a.store_nbr )),
cash01a.store_nbr
FROM         cash01a
GROUP     BY 1 , 3
) t1 (item_nbr, store_count , store_nbr)
FULL OUTER JOIN
( select     cash01a.item_nbr,
COUNT( DISTINCT( cash01a.store_nbr )),
cash01a.store_nbr
FROM         cash01a
WHERE     cash01a.ON_hand_qty > 0
GROUP BY 1 , 3
) t2 (item_nbr, store_count , store_nbr)
ON      t1.item_nbr >= t2.item_nbr and
t1.store_nbr <= t2.store_nbr
ORDER BY t1.item_nbr ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test013(desc="""U013"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U013"""
    stmt = """prepare s1 from
select [first 10]  t1.store_nbr,
ZEROIFNULL(t1.store_count)
FROM  ( select      cash01a.item_nbr,
COUNT( DISTINCT( cash01a.store_nbr )),
cash01a.store_nbr
FROM     cash01a
GROUP     BY 1 , 3
) t1 (item_nbr, store_count , store_nbr)
FULL OUTER JOIN
( select     cash01a.item_nbr,
COUNT( DISTINCT( cash01a.store_nbr )),
cash01a.store_nbr
FROM     cash01a
WHERE     cash01a.ON_hand_qty > 0
GROUP BY 1 , 3
) t2 (item_nbr, store_count , store_nbr)
ON       t1.item_nbr > t2.item_nbr and
t1.store_nbr < t2.store_nbr
ORDER BY t1.item_nbr ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test014(desc="""U014"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U014"""
    stmt = """prepare s1 from
select [first 10]  t1.store_nbr,
ZEROIFNULL( t2.store_count),
ZEROIFNULL( t1.store_count)
FROM  ( select     cash01a.item_nbr,
COUNT( DISTINCT( cash01a.store_nbr )),
cash01a.store_nbr
FROM     cash01a
GROUP     BY 1 , 3
)  t1 (item_nbr, store_count , store_nbr)
FULL OUTER JOIN
( select      cash01a.item_nbr,
COUNT( DISTINCT( cash01a.store_nbr )),
cash01a.store_nbr
FROM     cash01a
WHERE     cash01a.on_hand_qty > 0
GROUP BY 1 , 3
) t2 (item_nbr, store_count , store_nbr)
ON       t1.item_nbr = t2.item_nbr and
t1.store_nbr < t2.store_nbr
ORDER BY t1.item_nbr ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test015(desc="""U015"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U015"""
    stmt = """prepare s1 from
select [first 10]  t1.store_nbr,
t1.item_nbr,
ZEROIFNULL( t1.store_count)
FROM  ( select     cash01a.item_nbr,
COUNT( DISTINCT( cash01a.store_nbr )),
cash01a.store_nbr
FROM     cash01a
GROUP     BY 1 , 3
) t1 (item_nbr, store_count , store_nbr)
FULL OUTER JOIN
( select    cash01a.item_nbr,
COUNT(DISTINCT( cash01a.store_nbr )),
cash01a.store_nbr
FROM     cash01a
WHERE     cash01a.ON_hand_qty > 0
GROUP BY 1 , 3
) t2 (item_nbr, store_count , store_nbr)
ON       t1.item_nbr > t2.item_nbr and
t1.store_nbr = t2.store_nbr
ORDER BY t1.item_nbr;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    # Tests
    # FROM fullouter.sql  (U101-U136)
    _testmgr.testcase_end(desc)

def test016(desc="""U101"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U101"""
    stmt = """prepare s1 from
select [first 10]   a.seqno,
b.seqno
FROM      wm000 a
FULL OUTER JOIN
wm001 b
ON       a.seqno < b.seqno
ORDER BY a.seqno, b.seqno ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test017(desc="""U102"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U102"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno,
a.smin1,
b.smin1
FROM     wm000 a
FULL OUTER JOIN
wm001 b
ON      a.smin1 > b.smin1
ORDER BY a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test018(desc="""U103"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U103"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno,
a.inte1,
b.inte1
FROM     wm000 a
FULL OUTER JOIN
wm001 b
ON      a.inte1 >= b.inte1
ORDER BY a.seqno, b.seqno, a.inte1, b.inte1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test019(desc="""U104"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U104"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno,
a.lint1,
b.lint1
FROM     wm000 a
FULL OUTER JOIN
wm001 b
ON      a.lint1 <= b.lint1
ORDER BY a.seqno, b.seqno, a.lint1, b.lint1      ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test020(desc="""U105"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U105"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno,
a.nume1,
b.nume1
FROM     wm000 a
FULL OUTER JOIN
wm001 b
ON      a.nume1 <> b.nume1
ORDER BY a.seqno, b.seqno, a.nume1, b.nume1      ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test021(desc="""U106"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U106"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno,
a.deci1,
b.deci1
FROM     wm000 a
FULL OUTER JOIN
wm001 b
ON      a.deci1 > b.deci1
ORDER BY a.seqno, b.seqno, a.deci1, b.deci1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test022(desc="""U107"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U107"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno,
a.pict1,
b.pict1
FROM     wm000 a
FULL OUTER JOIN
wm001 b
ON      a.pict1 < b.pict1
ORDER BY a.seqno, b.seqno, a.pict1, b.pict1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test023(desc="""U108"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U108"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno,
a.flot1,
b.flot1
FROM     wm000 a
FULL OUTER JOIN
wm001 b
ON      a.flot1 <> b.flot1
ORDER BY a.seqno, b.seqno, a.flot1, b.flot1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test024(desc="""U109"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U109"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno,
a.real1,
b.real1
FROM     wm000 a
FULL OUTER JOIN
wm001 b
ON      a.real1 < b.real1
ORDER BY a.seqno, b.seqno, a.real1, b.real1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test025(desc="""U110"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U110"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno,
a.dblp1,
b.dblp1
FROM     wm000 a
FULL OUTER JOIN
wm001 b
ON      a.dblp1 > b.dblp1
ORDER BY a.seqno, b.seqno, a.dblp1, b.dblp1  ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test026(desc="""U111"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U111"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno,
a.char1,
b.char1
FROM     wm000 a
FULL OUTER JOIN
wm001 b
ON      a.char1 > b.char1
ORDER BY a.seqno, b.seqno, a.char1, b.char1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test027(desc="""U112"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U112"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno,
a.vchr1,
b.vchr1
FROM     wm000 a
FULL OUTER JOIN
wm001 b
ON      a.vchr1 < b.vchr1
ORDER BY a.seqno, b.seqno, a.vchr1, b.vchr1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test028(desc="""U113"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U113"""
    stmt = """prepare s1 from
select [first 10]     a.n0sq,
b.n1sq,
a.n0sq,
b.n1sq
FROM     wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON      a.n0sq > n1sq
ORDER BY a.n0sq, b.n1sq, a.n0sq, b.n1sq ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test029(desc="""U114"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U114"""
    stmt = """prepare s1 from
select [first 10]     a.n0sq,
b.n1sq,
a.n0s1,
b.n1s1
FROM     wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON      a.n0s1 >= b.n1s1
ORDER BY a.n0sq, b.n1sq, a.n0s1, b.n1s1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test030(desc="""U115"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U115"""
    stmt = """prepare s1 from
select [first 10]     a.n0sq,
b.n1sq,
a.n0i1,
b.n1i1
FROM     wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON      a.n0i1 <= b.n1i1
ORDER BY a.n0sq, b.n1sq, a.n0i1, b.n1i1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test031(desc="""U116"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U116"""
    stmt = """prepare s1 from
select [first 10]     a.n0sq,
b.n1sq,
a.n0l1,
b.n1s1
FROM     wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON      a.n0l1 > b.n1l1
ORDER BY a.n0sq, b.n1sq, a.n0l1, b.n1s1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test032(desc="""U117"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U117"""
    stmt = """prepare s1 from
select [first 10]     a.n0sq,
b.n1sq,
a.n0n1,
b.n1n1
FROM     wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON      a.n0n1 > b.n1n1
ORDER BY a.n0sq, b.n1sq, a.n0n1, b.n1n1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test033(desc="""U118"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U118"""
    stmt = """prepare s1 from
select [first 10]     a.n0sq,
b.n1sq,
a.n0d1,
b.n1d1
FROM     wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON      a.n0d1 < b.n1d1
ORDER BY a.n0sq, b.n1sq, a.n0d1, b.n1d1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test034(desc="""U119"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U119"""
    stmt = """prepare s1 from
select [first 10]     a.n0sq,
b.n1sq,
a.n0p1,
b.n1p1
FROM     wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON      a.n0p1 > b.n1p1
ORDER BY a.n0sq, b.n1sq, a.n0p1, b.n1p1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test035(desc="""U120"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U120"""
    stmt = """prepare s1 from
select [first 10]     a.n0sq,
b.n1sq,
a.n0f1,
b.n1f1
FROM     wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON      a.n0f1 > b.n1f1
ORDER BY a.n0sq, b.n1sq, a.n0f1, b.n1f1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test036(desc="""U121"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U121"""
    stmt = """prepare s1 from
select [first 10]     a.n0sq,
b.n1sq,
a.n0r1,
b.n1r1
FROM     wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON      a.n0r1 < b.n1r1
ORDER BY a.n0sq, b.n1sq, a.n0r1, b.n1r1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test037(desc="""U122"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U122"""
    stmt = """prepare s1 from
select [first 10]     a.n0sq,
b.n1sq,
a.n0dp1,
b.n1dp1
FROM     wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON      a.n0dp1 > b.n1dp1
ORDER BY a.n0sq, b.n1sq, a.n0dp1, b.n1dp1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test038(desc="""U123"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U123"""
    stmt = """prepare s1 from
select [first 10]     a.n0sq,
b.n1sq,
a.n0c1,
b.n1c1
FROM     wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON      a.n0c1 < b.n1c1
ORDER BY a.n0sq, b.n1sq, a.n0c1, b.n1c1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test039(desc="""U124"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U124"""
    stmt = """prepare s1 from
select [first 10]     a.n0sq,
b.n1sq,
a.n0v1,
b.n1v1
FROM     wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON      a.n0v1 >= b.n1v1
ORDER BY a.n0sq, b.n1sq, a.n0v1, b.n1v1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test040(desc="""U125"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U125"""
    stmt = """prepare s1 from
select [first 10]     *
FROM
( select  seqno FROM wm000) a(sq)
FULL OUTER JOIN
( select  seqno FROM wm001) b(sq)
ON  a.sq >= b.sq
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test041(desc="""U126"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U126"""
    stmt = """prepare s1 from
select [first 10]     *
FROM
( select  smin1 FROM wm000) a(s)
FULL OUTER JOIN
( select  smin1 FROM wm001) b(s)
ON  a.s <= b.s
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test042(desc="""U127"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U127"""
    stmt = """prepare s1 from
select [first 10]     *
FROM
( select  inte1 FROM wm000) a(i)
FULL OUTER JOIN
( select  inte1 FROM wm001) b(i)
ON  a.i <> b.i
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test043(desc="""U128"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U128"""
    stmt = """prepare s1 from
select [first 10]     *
FROM
(select  lint1 FROM wm000) a(l)
FULL OUTER JOIN
(select  lint1 FROM wm001) b(l)
ON  a.l < b.l
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test044(desc="""U129"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U129"""
    stmt = """prepare s1 from
select [first 10]     *
FROM
( select  nume1 FROM wm000) a(n)
FULL OUTER JOIN
( select  nume1 FROM wm001) b(n)
ON  a.n > b.n
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test045(desc="""U130"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U130"""
    stmt = """prepare s1 from
select [first 10]     *
FROM
( select  deci1 FROM wm000) a(d)
FULL OUTER JOIN
( select  deci1 FROM wm001) b(d)
ON  a.d > b.d
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test046(desc="""U131"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U131"""
    stmt = """prepare s1 from
select [first 10]     *
FROM
( select  pict1 FROM wm000) a(p)
FULL OUTER JOIN
( select  pict1 FROM wm001) b(p)
ON  a.p < b.p
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test047(desc="""U132"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U132"""
    stmt = """prepare s1 from
select [first 10]     *
FROM
( select  flot1 FROM wm000) a(f)
FULL OUTER JOIN
( select  flot1 FROM wm001) b(f)
ON  a.f > b.f
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test048(desc="""U133"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U133"""
    stmt = """prepare s1 from
select [first 10]     *
FROM
( select  real1 FROM wm000) a(r)
FULL OUTER JOIN
( select  real1 FROM wm001) b(r)
ON  a.r > b.r
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test049(desc="""U134"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U134"""
    stmt = """prepare s1 from
select [first 10]     *
FROM
( select  dblp1 FROM wm000) a(dp)
FULL OUTER JOIN
( select  dblp1 FROM wm001) b(dp)
ON  a.dp > b.dp
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test050(desc="""U135"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U135"""
    stmt = """prepare s1 from
select [first 10]     *
FROM
( select  char1 FROM wm000) a(c)
FULL OUTER JOIN
( select  char1 FROM wm001) b(c)
ON  a.c < b.c
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test051(desc="""U136"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """U136"""
    stmt = """prepare s1 from
select [first 10]     *
FROM
( select  vchr1 FROM wm000) a(v)
FULL OUTER JOIN
( select  vchr1 FROM wm001) b(v)
ON  a.v > b.v
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    # Elena Krotkova 5/24/07
    #  tables FOJ + where
    _testmgr.testcase_end(desc)

def test052(desc="""UW101"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """UW101"""
    stmt = """prepare s1 from
select [first 10] a.seqno,
b.seqno,
a.smin1,
b.smin1
FROM   wm000 a
FULL OUTER JOIN
wm001 b
ON        a.seqno < b.seqno
where (a.seqno > 3 and a.smin1 < 123) or
a.seqno <5
ORDER BY a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test053(desc="""UW102"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """UW102"""
    stmt = """prepare s1 from
select [first 10]      a.seqno,
b.seqno,
a.smin1,
b.smin1
FROM           wm000 a
FULL OUTER JOIN
wm001 b
ON             a.smin1 > b.smin1
where (a.seqno > 3 and a.smin1 < 123) or b.smin1 = 1
ORDER BY a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test054(desc="""UW103"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """UW103"""
    stmt = """prepare s1 from
select [first 10]      a.seqno,
b.seqno,
a.inte1,
b.inte1
FROM           wm000 a
FULL OUTER JOIN
wm001 b
ON             a.inte1 > b.inte1
where (a.inte1 > 3 and a.smin1 < 123) or
b.inte1 = 2
ORDER BY a.seqno, b.seqno, a.inte1, b.inte1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test055(desc="""UW104"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """UW104"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno,
a.lint1,
b.lint1
FROM           wm000 a
FULL OUTER JOIN
wm001 b
ON             a.lint1 <> b.lint1
where(a.lint1 > 3 and a.smin1 < 123) or
b.lint1 = 2
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test056(desc="""UW105"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """UW105"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno,
a.nume1,
b.nume1
FROM           wm000 a
FULL OUTER JOIN
wm001 b
ON            a.nume1 <= b.nume1
where (a.nume1  > 3 and a.smin1 < 1230) or
b.nume1  = 0 or b.nume1  <> 763.463
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test057(desc="""UW106"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """UW106"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno,
a.deci1,
b.deci1
FROM           wm000 a
FULL OUTER JOIN
wm001 b
ON             a.deci1 >= b.deci1
where (a.deci1  > 3 and a.smin1 < 1230) or
(b.deci1 <= 1 or a.deci1 <> -1000000 )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test058(desc="""UW107"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """UW107"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno,
a.pict1,
b.pict1
FROM           wm000 a
FULL OUTER JOIN
wm001 b
ON             a.pict1 <> b.pict1
where (a.pict1  > 3 and a.smin1 < 1230) or
( b.pict1  > 1 or a.pict1  < 1 )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test059(desc="""UW108"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """UW108"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno,
a.flot1,
b.flot1
FROM           wm000 a
FULL OUTER JOIN
wm001 b
ON             a.flot1 > b.flot1
where (a.flot1   < 3 and a.smin1 > 1230) or
( b.flot1   > 1 or a.flot1  <> 0 )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test060(desc="""UW109"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """UW109"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno,
a.real1,
b.real1
FROM           wm000 a
FULL OUTER JOIN
wm001 b
ON             a.real1 < b.real1
where (a.real1   < 3 and a.smin1 < 123) or
( b.real1   < 4 and a.real1  > 1 )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test061(desc="""UW110"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """UW110"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno,
a.dblp1,
b.dblp1
FROM           wm000 a
FULL OUTER JOIN
wm001 b
ON             a.dblp1 > b.dblp1
where (a.dblp1   > 8 and a.smin1 < 123) or
( b.dblp1   < 1 or a.dblp1  <> 0 )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test062(desc="""UW111"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """UW111"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno,
a.char1,
b.char1
FROM           wm000 a
FULL OUTER JOIN
wm001 b
ON             a.char1 < b.char1
where (a.char1   >'8' and a.smin1 < 1023) or
( b.char1   <= '1' or a.char1  <> '0' )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test063(desc="""UW112"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """UW112"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno,
a.vchr1,
b.vchr1
FROM           wm000 a
FULL OUTER JOIN
wm001 b
ON             a.vchr1 > b.vchr1
where (a.vchr1  > '8' and a.smin1 < 35000) or
( b.vchr1   >= '1' or a.vchr1  <> '112345' )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    # views FOJ + where clause
    # ---------------------1------------------------------------------
    _testmgr.testcase_end(desc)

def test064(desc="""UW113"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """UW113"""
    stmt = """prepare s1 from
select [first 10]     a.n0sq,
b.n1sq,
a.n0sq,
b.n1sq
FROM           wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON             a.n0sq < n1sq
where (a.n0sq > 3 and n0s1 < 123) or
n0sq <5
ORDER BY       a.n0sq, b.n1sq, a.n0sq,     b.n1sq ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    # ----------------------2-----------------------------------------
    _testmgr.testcase_end(desc)

def test065(desc="""UW114"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """UW114"""
    stmt = """prepare s1 from
select [first 10]     a.n0sq,
b.n1sq,
a.n0s1,
b.n1s1
FROM           wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON             a.n0s1 > b.n1s1
where (a.n0sq > 3 and n0s1 < 123) or n0s1 = 1
ORDER BY       a.n0sq, b.n1sq, a.n0sq,     b.n1sq      ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    # -----------------------3----------------------------------------
    _testmgr.testcase_end(desc)

def test066(desc="""UW115"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """UW115"""
    stmt = """prepare s1 from
select [first 10]     a.n0sq,
b.n1sq,
a.n0i1,
b.n1i1
FROM           wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON             a.n0i1 >= b.n1i1
where (a.n0i1 > 3 and a.n0s1 < 123) or
b.n1i1 = 2
ORDER BY       a.n0sq, b.n1sq, a.n0sq,     b.n1sq      ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    # ------------------------4---------------------------------------
    _testmgr.testcase_end(desc)

def test067(desc="""UW116"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """UW116"""
    stmt = """prepare s1 from
select [first 10]     a.n0sq,
b.n1sq,
a.n0l1,
b.n1s1
FROM           wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON             a.n0l1 <= b.n1l1
where (a.n0l1 > 3 and a.n0s1 < 123) or
b.n1l1 = 2
ORDER BY       a.n0sq, b.n1sq, a.n0sq,     b.n1sq      ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    # -------------------------5--------------------------------------
    _testmgr.testcase_end(desc)

def test068(desc="""UW117"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """UW117"""
    stmt = """prepare s1 from
select [first 10]     a.n0sq,
b.n1sq,
a.n0n1,
b.n1n1
FROM           wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON             a.n0n1 <> b.n1n1
where (a.n0n1  > 3 and a.n0s1 < 1230) or
b.n1n1  = 0 or
b.n1n1  <> 9
ORDER BY       a.n0sq, b.n1sq, a.n0sq,     b.n1sq      ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    # --------------------------6-------------------------------------
    _testmgr.testcase_end(desc)

def test069(desc="""UW118"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """UW118"""
    stmt = """prepare s1 from
select [first 10]     a.n0sq,
b.n1sq,
a.n0d1,
b.n1d1
FROM           wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON             a.n0d1 > b.n1d1
where (a.n0d1 > 3 and a.n0s1 < 1230) or
(b.n1d1<= 1 or a.n0d1 = 10000 )
ORDER BY       a.n0sq, b.n1sq, a.n0sq,     b.n1sq       ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    # ---------------------------7------------------------------------
    _testmgr.testcase_end(desc)

def test070(desc="""UW119"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """UW119"""
    stmt = """prepare s1 from
select [first 10]     a.n0sq,
b.n1sq,
a.n0p1,
b.n1p1
FROM           wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON             a.n0p1 < b.n1p1
where (a.n0p1  > 3 and a.n0s1 < 1230) or
( b.n1p1  > 1 or a.n0p1  = 0 )
ORDER BY       a.n0sq, b.n1sq, a.n0sq,     b.n1sq      ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    # ----------------------------8-----------------------------------
    _testmgr.testcase_end(desc)

def test071(desc="""UW120"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """UW120"""
    stmt = """prepare s1 from
select [first 10]     a.n0sq,
b.n1sq,
a.n0f1,
b.n1f1
FROM           wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON             a.n0f1 >= b.n1f1
where (a.n0f1  < 3 and a.n0s1 < 1230) or
( b.n1f1  > 1 or a.n0f1 = 0 )
ORDER BY       a.n0sq, b.n1sq, a.n0sq,     b.n1sq      ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    # -----------------------------9----------------------------------
    _testmgr.testcase_end(desc)

def test072(desc="""UW121"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """UW121"""
    stmt = """prepare s1 from
select [first 10]     a.n0sq,
b.n1sq,
a.n0r1,
b.n1r1
FROM           wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON             a.n0r1 <= b.n1r1
where (a.n0r1  < 3 and a.n0s1 < 123) or
( b.n1r1  < 1 or a.n0r1 = 0 )
ORDER BY       a.n0sq, b.n1sq, a.n0sq,     b.n1sq      ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    # ----------------------------10-----------------------------------
    _testmgr.testcase_end(desc)

def test073(desc="""UW122"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """UW122"""
    stmt = """prepare s1 from
select [first 10]     a.n0sq,
b.n1sq,
a.n0dp1,
b.n1dp1
FROM           wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON             a.n0dp1 >= b.n1dp1
where (a.n0dp1   > 8 and a.n0s1 < 123) or
( b.n1dp1   < 1 and a.n0dp1  >1 )
ORDER BY       a.n0sq, b.n1sq, a.n0sq,     b.n1sq      ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test074(desc="""UW123"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """UW123"""
    stmt = """prepare s1 from
select [first 10]     a.n0sq,
b.n1sq,
a.n0c1,
b.n1c1
FROM           wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON             a.n0c1 > b.n1c1
where (a.n0c1   > '8' and a.n0s1 < 1023) or
( b.n1c1   <= '10' or a.n0c1  <> '1' )
ORDER BY       a.n0sq, b.n1sq, a.n0sq,     b.n1sq      ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test075(desc="""UW124"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """UW124"""
    stmt = """prepare s1 from
select [first 10]     a.n0sq,
b.n1sq,
a.n0v1,
b.n1v1
FROM           wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON             a.n0v1 < b.n1v1
where (a.n0v1  > '8' and a.n0s1 < 35000) or
( b.n1v1    >= '1' or a.n0v1  <> '11' )
ORDER BY       a.n0sq, b.n1sq, a.n0sq,     b.n1sq      ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test076(desc="""UW125"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """UW125"""
    stmt = """prepare s1 from
select [first 10]     a.n0sq,
b.n1sq,
a.n0v1,
b.n1v1
FROM           wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON             a.n0v1 > b.n1v1
where (b.n1v1  > '8' and b.n1s1 < 35000) or
( b.n1v1    >= '1' or b.n1v1  <> '11' )
ORDER BY       a.n0sq, b.n1sq, a.n0sq,     b.n1sq      ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    # ---------------------------rest------------------------------------
    # Multi Joins
    _testmgr.testcase_end(desc)

def test077(desc="""UM001"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """UM001"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno
FROM       wm000 a
FULL OUTER JOIN
wm001 b
ON         a.seqno < b.seqno
FULL OUTER JOIN
vt_wm000 c
ON         a.seqno > c.seqno
FULL OUTER JOIN
wm003 d
ON         b.seqno >= d.seqno
FULL OUTER JOIN
wm005 e
ON         b.seqno = e.seqno
FULL OUTER JOIN
tab006 f
ON         b.seqno <= f.a
FULL OUTER JOIN
vt_wm001 g
ON         b.seqno >= g.seqno
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test078(desc="""UM002"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """UM002"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno
FROM       wm000 a
FULL OUTER JOIN
wm000 b
ON         a.seqno >= b.seqno
FULL OUTER JOIN
vt_wm000 c
ON         a.seqno >= c.seqno
FULL OUTER JOIN
vt_wm001 d
ON         b.seqno <= d.seqno
FULL OUTER JOIN
wm_vw_003 e
ON         b.seqno <> e.n0sq
FULL OUTER JOIN
wm_vw_001  f
ON         b.seqno < f.n1sq
FULL OUTER JOIN
vt_wm001 g
ON         b.seqno > g.seqno
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    #--------------------------
    # nested FOJ
    # mixed veiws tables ant vt tables
    # some tables have no values(empty)
    #--------------------------
    _testmgr.testcase_end(desc)

def test079(desc="""UM003"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """UM003"""
    stmt = """prepare s1 from
select [first 10] 			v.flot1,
w.seqno
from
(	select  x.flot1,
y.seqno
from
(  select      b.seqno,
c.flot1
from       wm000 b
FULL OUTER JOIN
vt_wm000 c
ON         b.seqno < c.seqno
) as x    

FULL OUTER JOIN
( select      d.seqno,
e.n0sq
from
vt_wm001 d
FULL OUTER JOIN
wm_vw_003 e
ON         d.seqno > e.n0sq
) as y
ON       x.seqno = y.seqno
)   as v
FULL OUTER JOIN
(    select     a.n1sq,
b.seqno
from
( select     f.n1sq,
g.seqno
from
wm_vw_001  f
FULL OUTER JOIN
vt_wm001 g
ON        f.n1sq < g.seqno
) as a
FULL OUTER JOIN
( select     g.seqno,
f.smin1
from
wm004  f
FULL OUTER JOIN
wm004 g
ON        f.seqno > g.seqno
) as b    

ON      a.seqno = b.seqno
)   as w
ON          v.seqno  = w.seqno
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    # FOJ on same tables
    # Scenario: Everything matches on various datatypes.
    _testmgr.testcase_end(desc)

def test080(desc="""US101"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """US101"""
    stmt = """prepare s1 from
select [first 10]   a.seqno,
b.seqno
FROM      wm000 a
FULL OUTER JOIN
wm000 b
ON       a.seqno >= b.seqno
ORDER BY a.seqno, b.seqno ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test081(desc="""US102"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """US102"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno,
a.smin1,
b.smin1
FROM     wm000 a
FULL OUTER JOIN
wm000 b
ON      a.smin1 <> b.smin1
ORDER BY a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test082(desc="""US103"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """US103"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno,
a.inte1,
b.inte1
FROM     wm000 a
FULL OUTER JOIN
wm000 b
ON      a.inte1 > b.inte1
ORDER BY a.seqno, b.seqno, a.inte1, b.inte1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test083(desc="""US104"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """US104"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno,
a.lint1,
b.lint1
FROM     wm000 a
FULL OUTER JOIN
wm000 b
ON      a.lint1 < b.lint1
ORDER BY a.seqno, b.seqno, a.lint1, b.lint1      ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test084(desc="""US105"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """US105"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno,
a.nume1,
b.nume1
FROM     wm000 a
FULL OUTER JOIN
wm000 b
ON      a.nume1 > b.nume1
ORDER BY a.seqno, b.seqno, a.nume1, b.nume1      ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test085(desc="""US106"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """US106"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno,
a.deci1,
b.deci1
FROM     wm000 a
FULL OUTER JOIN
wm000 b
ON      a.deci1 >= b.deci1
ORDER BY a.seqno, b.seqno, a.deci1, b.deci1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test086(desc="""US107"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """US107"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno,
a.pict1,
b.pict1
FROM     wm000 a
FULL OUTER JOIN
wm000 b
ON      a.pict1 > b.pict1
ORDER BY a.seqno, b.seqno, a.pict1, b.pict1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test087(desc="""US108"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """US108"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno,
a.flot1,
b.flot1
FROM     wm000 a
FULL OUTER JOIN
wm000 b
ON      a.flot1 < b.flot1
ORDER BY a.seqno, b.seqno, a.flot1, b.flot1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test088(desc="""US109"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """US109"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno,
a.real1,
b.real1
FROM     wm000 a
FULL OUTER JOIN
wm000 b
ON      a.real1 >= b.real1
ORDER BY a.seqno, b.seqno, a.real1, b.real1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test089(desc="""US110"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """US110"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno,
a.dblp1,
b.dblp1
FROM     wm000 a
FULL OUTER JOIN
wm000 b
ON      a.dblp1 >= b.dblp1
ORDER BY a.seqno, b.seqno, a.dblp1, b.dblp1  ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test090(desc="""US111"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """US111"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno,
a.char1,
b.char1
FROM     wm000 a
FULL OUTER JOIN
wm000 b
ON      a.char1 < b.char1
ORDER BY a.seqno, b.seqno, a.char1, b.char1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test091(desc="""US112"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """US112"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno,
a.vchr1,
b.vchr1
FROM     wm000 a
FULL OUTER JOIN
wm000 b
ON      a.vchr1 > b.vchr1
ORDER BY a.seqno, b.seqno, a.vchr1, b.vchr1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test092(desc="""USW104"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """USW104"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno,
a.lint1,
b.lint1
FROM           wm000 a
FULL OUTER JOIN
wm000 b
ON             a.lint1 >= b.lint1
where(a.lint1 > 3 and a.smin1 < 123) or
b.lint1 = 2
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test093(desc="""USW105"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """USW105"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno,
a.nume1,
b.nume1
FROM           wm000 a
FULL OUTER JOIN
wm000 b
ON            a.nume1 <= b.nume1
where (a.nume1  > 3 and a.smin1 < 1230) or
b.nume1  = 0 or b.nume1  <> 763.463
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test094(desc="""USW106"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """USW106"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno,
a.deci1,
b.deci1
FROM           wm000 a
FULL OUTER JOIN
wm000 b
ON             a.deci1 <> b.deci1
where (a.deci1  > 3 and a.smin1 < 1230) or
(b.deci1 <= 1 or a.deci1 <> -1000000 )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test095(desc="""USW107"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """USW107"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno,
a.pict1,
b.pict1
FROM           wm000 a
FULL OUTER JOIN
wm000 b
ON             a.pict1 <> b.pict1
where (a.pict1  > 3 and a.smin1 < 1230) or
( b.pict1  > 1 or a.pict1  < 1 )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test096(desc="""USW108"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """USW108"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno,
a.flot1,
b.flot1
FROM           wm000 a
FULL OUTER JOIN
wm000 b
ON             a.flot1 >= b.flot1
where (a.flot1   < 3 and a.smin1 > 1230) or
( b.flot1   > 1 or a.flot1  <> 0 )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test097(desc="""USW109"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """USW109"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno,
a.real1,
b.real1
FROM           wm000 a
FULL OUTER JOIN
wm000 b
ON             a.real1 >= b.real1
where (a.real1   < 3 and a.smin1 < 123) or
( b.real1   < 4 and a.real1  > 1 )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test098(desc="""USW110"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """USW110"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno,
a.dblp1,
b.dblp1
FROM           wm000 a
FULL OUTER JOIN
wm000 b
ON             a.dblp1 <= b.dblp1
where (a.dblp1   > 8 and a.smin1 < 123) or
( b.dblp1   < 1 or a.dblp1  <> 0 )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test099(desc="""USW111"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """USW111"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno,
a.char1,
b.char1
FROM           wm000 a
FULL OUTER JOIN
wm000 b
ON             a.char1 >= b.char1
where (a.char1   > '8' and a.smin1 < 1023) or
( b.char1   <= '1' or a.char1  <> '0' )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test100(desc="""USW112"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """USW112"""
    stmt = """prepare s1 from
select [first 10]     a.seqno,
b.seqno,
a.vchr1,
b.vchr1
FROM           wm000 a
FULL OUTER JOIN
wm000 b
ON             a.vchr1 > b.vchr1
where (a.vchr1  > '8' and a.smin1 < 35000) or
( b.vchr1   >= '1' or a.vchr1  <> '112345' )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test101(desc="""USW125"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """USW125"""
    stmt = """prepare s1 from
select [first 10]     a.n0sq,
b.n0sq,
a.n0v1,
b.n0v1
FROM           wm_vw_000 a
FULL OUTER JOIN
wm_vw_000 b
ON             a.n0v1 > b.n0v1
where (b.n0v1  > '8' and b.n0s1 < 35000) or
( b.n0v1    >= '1' or b.n0v1  <> '11' )
ORDER BY       a.n0sq, b.n0sq, a.n0sq,     b.n0sq      ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

