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

# Null and empty tables
# FROM fullouter.sql  (NUL101-NUL136)
# FOJ on tables on NULL tables that have all NULL values except primary key
# which is integer
# NO check on integer null join
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""NN101"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NN101"""
    stmt = """prepare s1 from
select   a.seqno,
b.seqno
FROM      tbl_null_000 a
FULL OUTER JOIN
tbl_null_001 b
ON       a.seqno = b.seqno
ORDER BY a.seqno, b.seqno ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test002(desc="""NN102"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NN102"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.smin1,
b.smin1
FROM     tbl_null_000 a
FULL OUTER JOIN
tbl_null_001 b
ON      a.smin1 = b.smin1
ORDER BY a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test003(desc="""NN103"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NN103"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.inte1,
b.inte1
FROM     tbl_null_000 a
FULL OUTER JOIN
tbl_null_001 b
ON      a.inte1 = b.inte1
ORDER BY a.seqno, b.seqno, a.inte1, b.inte1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test004(desc="""NN104"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NN104"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.lint1,
b.lint1
FROM     tbl_null_000 a
FULL OUTER JOIN
tbl_null_001 b
ON      a.lint1 = b.lint1
ORDER BY a.seqno, b.seqno, a.lint1, b.lint1      ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test005(desc="""NN105"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NN105"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.nume1,
b.nume1
FROM     tbl_null_000 a
FULL OUTER JOIN
tbl_null_001 b
ON      a.nume1 = b.nume1
ORDER BY a.seqno, b.seqno, a.nume1, b.nume1      ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test006(desc="""NN106"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NN106"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.deci1,
b.deci1
FROM     tbl_null_000 a
FULL OUTER JOIN
tbl_null_001 b
ON      a.deci1 = b.deci1
ORDER BY a.seqno, b.seqno, a.deci1, b.deci1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test007(desc="""NN107"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NN107"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.pict1,
b.pict1
FROM     tbl_null_000 a
FULL OUTER JOIN
tbl_null_001 b
ON      a.pict1 = b.pict1
ORDER BY a.seqno, b.seqno, a.pict1, b.pict1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test008(desc="""NN108"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NN108"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.flot1,
b.flot1
FROM     tbl_null_000 a
FULL OUTER JOIN
tbl_null_001 b
ON      a.flot1 = b.flot1
ORDER BY a.seqno, b.seqno, a.flot1, b.flot1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test009(desc="""NN109"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NN109"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.real1,
b.real1
FROM     tbl_null_000 a
FULL OUTER JOIN
tbl_null_001 b
ON      a.real1 = b.real1
ORDER BY a.seqno, b.seqno, a.real1, b.real1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test010(desc="""NN110"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NN110"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.dblp1,
b.dblp1
FROM     tbl_null_000 a
FULL OUTER JOIN
tbl_null_001 b
ON      a.dblp1 = b.dblp1
ORDER BY a.seqno, b.seqno, a.dblp1, b.dblp1  ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test011(desc="""NN111"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NN111"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.char1,
b.char1
FROM     tbl_null_000 a
FULL OUTER JOIN
tbl_null_001 b
ON      a.char1 = b.char1
ORDER BY a.seqno, b.seqno, a.char1, b.char1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test012(desc="""NN112"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NN112"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.vchr1,
b.vchr1
FROM     tbl_null_000 a
FULL OUTER JOIN
tbl_null_001 b
ON      a.vchr1 = b.vchr1
ORDER BY a.seqno, b.seqno, a.vchr1, b.vchr1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test013(desc="""NN113"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NN113"""
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

def test014(desc="""NN114"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NN114"""
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

def test015(desc="""NN115"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NN115"""
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

def test016(desc="""NN116"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NN116"""
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

def test017(desc="""NN117"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NN117"""
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

def test018(desc="""NN118"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NN118"""
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

def test019(desc="""NN119"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NN119"""
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

def test020(desc="""NN120"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NN120"""
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

def test021(desc="""NN121"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NN121"""
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

def test022(desc="""NN122"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NN122"""
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

def test023(desc="""NN123"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NN123"""
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

def test024(desc="""NN124"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NN124"""
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

def test025(desc="""NN125"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NN125"""
    stmt = """prepare s1 from
select     *
FROM
( select seqno FROM tbl_null_000) a(sq)
FULL OUTER JOIN
( select seqno FROM tbl_null_001) b(sq)
ON  a.sq = b.sq
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test026(desc="""NN126"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NN126"""
    stmt = """prepare s1 from
select     *
FROM
( select smin1 FROM tbl_null_000) a(s)
FULL OUTER JOIN
( select smin1 FROM tbl_null_001) b(s)
ON  a.s = b.s
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test027(desc="""NN127"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NN127"""
    stmt = """prepare s1 from
select     *
FROM
( select inte1 FROM tbl_null_000) a(i)
FULL OUTER JOIN
( select inte1 FROM tbl_null_001) b(i)
ON  a.i = b.i
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test028(desc="""NN128"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NN128"""
    stmt = """prepare s1 from
select     *
FROM
(select lint1 FROM tbl_null_000) a(l)
FULL OUTER JOIN
(select lint1 FROM tbl_null_001) b(l)
ON  a.l = b.l
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test029(desc="""NN129"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NN129"""
    stmt = """prepare s1 from
select     *
FROM
( select nume1 FROM tbl_null_000) a(n)
FULL OUTER JOIN
( select nume1 FROM tbl_null_001) b(n)
ON  a.n = b.n
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test030(desc="""NN130"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NN130"""
    stmt = """prepare s1 from
select     *
FROM
( select deci1 FROM tbl_null_000) a(d)
FULL OUTER JOIN
( select deci1 FROM tbl_null_001) b(d)
ON  a.d = b.d
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test031(desc="""NN131"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NN131"""
    stmt = """prepare s1 from
select     *
FROM
( select pict1 FROM tbl_null_000) a(p)
FULL OUTER JOIN
( select pict1 FROM tbl_null_001) b(p)
ON  a.p = b.p
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test032(desc="""NN132"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NN132"""
    stmt = """prepare s1 from
select     *
FROM
( select flot1 FROM tbl_null_000) a(f)
FULL OUTER JOIN
( select flot1 FROM tbl_null_001) b(f)
ON  a.f = b.f
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test033(desc="""NN133"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NN133"""
    stmt = """prepare s1 from
select     *
FROM
( select real1 FROM tbl_null_000) a(r)
FULL OUTER JOIN
( select real1 FROM tbl_null_001) b(r)
ON  a.r = b.r
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test034(desc="""NN134"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NN134"""
    stmt = """prepare s1 from
select     *
FROM
( select dblp1 FROM tbl_null_000) a(dp)
FULL OUTER JOIN
( select dblp1 FROM tbl_null_001) b(dp)
ON  a.dp = b.dp
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test035(desc="""NN135"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NN135"""
    stmt = """prepare s1 from
select     *
FROM
( select char1 FROM tbl_null_000) a(c)
FULL OUTER JOIN
( select char1 FROM tbl_null_001) b(c)
ON  a.c = b.c
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test036(desc="""NN136"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NN136"""
    stmt = """prepare s1 from
select     *
FROM
( select vchr1 FROM tbl_null_000) a(v)
FULL OUTER JOIN
( select vchr1 FROM tbl_null_001) b(v)
ON  a.v = b.v
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    # Elena Krotkova 5/24/07
    #  tables FOJ + where
    _testmgr.testcase_end(desc)

def test037(desc="""NNW101"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NNW101"""
    stmt = """prepare s1 from
select a.seqno,
b.seqno,
a.smin1,
b.smin1
FROM   tbl_null_000 a
FULL OUTER JOIN
tbl_null_001 b
ON        a.seqno = b.seqno
where (a.seqno > 3 and a.smin1 < 123) or
a.seqno <5
ORDER BY a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test038(desc="""NNW102"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NNW102"""
    stmt = """prepare s1 from
select      a.seqno,
b.seqno,
a.smin1,
b.smin1
FROM           tbl_null_000 a
FULL OUTER JOIN
tbl_null_001 b
ON             a.smin1 = b.smin1
where (a.seqno > 3 and a.smin1 < 123) or b.smin1 = 1
ORDER BY a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test039(desc="""NNW103"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NNW103"""
    stmt = """prepare s1 from
select      a.seqno,
b.seqno,
a.inte1,
b.inte1
FROM           tbl_null_000 a
FULL OUTER JOIN
tbl_null_001 b
ON             a.inte1 = b.inte1
where (a.inte1 > 3 and a.smin1 < 123) or
b.inte1 = 2
ORDER BY a.seqno, b.seqno, a.inte1, b.inte1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test040(desc="""NNW104"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NNW104"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.lint1,
b.lint1
FROM           tbl_null_000 a
FULL OUTER JOIN
tbl_null_001 b
ON             a.lint1 = b.lint1
where(a.lint1 > 3 and a.smin1 < 123) or
b.lint1 = 2
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test041(desc="""NNW105"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NNW105"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.nume1,
b.nume1
FROM           tbl_null_000 a
FULL OUTER JOIN
tbl_null_001 b
ON            a.nume1 = b.nume1
where (a.nume1  > 3 and a.smin1 < 1230) or
b.nume1  = 0 or b.nume1  <> 763.463
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test042(desc="""NNW106"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NNW106"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.deci1,
b.deci1
FROM           tbl_null_000 a
FULL OUTER JOIN
tbl_null_001 b
ON             a.deci1 = b.deci1
where (a.deci1  > 3 and a.smin1 < 1230) or
(b.deci1 <= 1 or a.deci1 <> -1000000 )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test043(desc="""NNW107"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NNW107"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.pict1,
b.pict1
FROM           tbl_null_000 a
FULL OUTER JOIN
tbl_null_001 b
ON             a.pict1 = b.pict1
where (a.pict1  > 3 and a.smin1 < 1230) or
( b.pict1  > 1 or a.pict1  < 1 )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test044(desc="""NNW108"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NNW108"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.flot1,
b.flot1
FROM           tbl_null_000 a
FULL OUTER JOIN
tbl_null_001 b
ON             a.flot1 = b.flot1
where (a.flot1   < 3 and a.smin1 > 1230) or
( b.flot1   > 1 or a.flot1  <> 0 )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test045(desc="""NNW109"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NNW109"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.real1,
b.real1
FROM           tbl_null_000 a
FULL OUTER JOIN
tbl_null_001 b
ON             a.real1 = b.real1
where (a.real1   < 3 and a.smin1 < 123) or
( b.real1   < 4 and a.real1  > 1 )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test046(desc="""NNW110"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NNW110"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.dblp1,
b.dblp1
FROM           tbl_null_000 a
FULL OUTER JOIN
tbl_null_001 b
ON             a.dblp1 = b.dblp1
where (a.dblp1   > 8 and a.smin1 < 123) or
( b.dblp1   < 1 or a.dblp1  <> 0 )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test047(desc="""NNW111"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NNW111"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.char1,
b.char1
FROM           tbl_null_000 a
FULL OUTER JOIN
tbl_null_001 b
ON             a.char1 = b.char1
where (a.char1   > '8' and a.smin1 < 1023) or
( b.char1   <= '1' or a.char1  <> '0' )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test048(desc="""NNW112"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NNW112"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.vchr1,
b.vchr1
FROM           tbl_null_000 a
FULL OUTER JOIN
tbl_null_001 b
ON             a.vchr1 = b.vchr1
where (a.vchr1  > '8' and a.smin1 < 35000) or
( b.vchr1   >= '1' or a.vchr1  <> '112345' )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    # views FOJ + where clause
    # ---------------------1------------------------------------------
    _testmgr.testcase_end(desc)

def test049(desc="""NNW113"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NNW113"""
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

def test050(desc="""NNW114"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NNW114"""
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

def test051(desc="""NNW115"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NNW115"""
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

def test052(desc="""NNW116"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NNW116"""
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

def test053(desc="""NNW117"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NNW117"""
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

def test054(desc="""NNW118"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NNW118"""
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

def test055(desc="""NNW119"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NNW119"""
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

def test056(desc="""NNW120"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NNW120"""
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

def test057(desc="""NNW121"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NNW121"""
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

def test058(desc="""NNW122"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NNW122"""
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

def test059(desc="""NNW123"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NNW123"""
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

def test060(desc="""NNW124"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NNW124"""
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
    # ---------------------------rest------------------------------------
    # Multi Joins
    #--------------------------
    # some of FOJ do not have equality match
    #--------------------------
    _testmgr.testcase_end(desc)

def test061(desc="""NNM001"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NNM001"""
    stmt = """prepare s1 from
SELECT     a.seqno,
b.seqno
FROM       tbl_null_000 a
FULL OUTER JOIN
tbl_null_001 b
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

def test062(desc="""NNM002"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NNM002"""
    stmt = """prepare s1 from
SELECT     a.seqno,
b.seqno
FROM       tbl_null_000 a
FULL OUTER JOIN
tbl_null_000 b
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

def test063(desc="""NNM003"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NNM003"""
    stmt = """prepare s1 from
select 			v.flot1,
w.seqno
from
(	select x.flot1,
y.seqno
from
(  select     b.seqno,
c.flot1
from       tbl_null_000 b
FULL OUTER JOIN
vt_wm000 c
ON         b.seqno = c.seqno
) as x    

FULL OUTER JOIN
( SELECT     d.seqno,
e.n0sq
from
vt_wm001 d
FULL OUTER JOIN
wm_vw_003 e
ON         d.seqno = e.n0sq
) as y
ON       x.seqno = y.seqno
)   as v
FULL OUTER JOIN
(    SELECT     a.n1sq,
b.seqno
from
( select    f.n1sq,
g.seqno
from
wm_vw_001  f
FULL OUTER JOIN
vt_wm001 g
ON        f.n1sq = g.seqno
) as a
FULL OUTER JOIN
( select    g.seqno,
f.smin1
from
wm004  f
FULL OUTER JOIN
wm004 g
ON        f.seqno = g.seqno
) as b    

ON      a.seqno = b.seqno
)   as w
ON          v.seqno  = w.seqno
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    # Combination of NNEMPEMPL tables and empty table
    # tbl_NNEMPEMPl_001 is table with 2 rows of NNEMPEMPLs of different data types.
    # wm004 is empty table
    _testmgr.testcase_end(desc)

def test064(desc="""NE101"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NE101"""
    stmt = """prepare s1 from
select   a.seqno,
b.seqno
FROM      wm004 a
FULL OUTER JOIN
tbl_null_001 b
ON       a.seqno = b.seqno
ORDER BY a.seqno, b.seqno ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test065(desc="""NE102"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NE102"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.smin1,
b.smin1
FROM     wm004 a
FULL OUTER JOIN
tbl_null_001 b
ON      a.smin1 = b.smin1
ORDER BY a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test066(desc="""NE103"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NE103"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.inte1,
b.inte1
FROM     wm004 a
FULL OUTER JOIN
tbl_null_001 b
ON      a.inte1 = b.inte1
ORDER BY a.seqno, b.seqno, a.inte1, b.inte1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test067(desc="""NE104"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NE104"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.lint1,
b.lint1
FROM     wm004 a
FULL OUTER JOIN
tbl_null_001 b
ON      a.lint1 = b.lint1
ORDER BY a.seqno, b.seqno, a.lint1, b.lint1      ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test068(desc="""NE105"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NE105"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.nume1,
b.nume1
FROM     wm004 a
FULL OUTER JOIN
tbl_null_001 b
ON      a.nume1 = b.nume1
ORDER BY a.seqno, b.seqno, a.nume1, b.nume1      ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test069(desc="""NE106"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NE106"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.deci1,
b.deci1
FROM     wm004 a
FULL OUTER JOIN
tbl_null_001 b
ON      a.deci1 = b.deci1
ORDER BY a.seqno, b.seqno, a.deci1, b.deci1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test070(desc="""NE107"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NE107"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.pict1,
b.pict1
FROM     wm004 a
FULL OUTER JOIN
tbl_null_001 b
ON      a.pict1 = b.pict1
ORDER BY a.seqno, b.seqno, a.pict1, b.pict1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test071(desc="""NE108"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NE108"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.flot1,
b.flot1
FROM     wm004 a
FULL OUTER JOIN
tbl_null_001 b
ON      a.flot1 = b.flot1
ORDER BY a.seqno, b.seqno, a.flot1, b.flot1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test072(desc="""NE109"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NE109"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.real1,
b.real1
FROM     wm004 a
FULL OUTER JOIN
tbl_null_001 b
ON      a.real1 = b.real1
ORDER BY a.seqno, b.seqno, a.real1, b.real1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test073(desc="""NE110"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NE110"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.dblp1,
b.dblp1
FROM     wm004 a
FULL OUTER JOIN
tbl_null_001 b
ON      a.dblp1 = b.dblp1
ORDER BY a.seqno, b.seqno, a.dblp1, b.dblp1  ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test074(desc="""NE111"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NE111"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.char1,
b.char1
FROM     wm004 a
FULL OUTER JOIN
tbl_null_001 b
ON      a.char1 = b.char1
ORDER BY a.seqno, b.seqno, a.char1, b.char1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test075(desc="""NE112"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NE112"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.vchr1,
b.vchr1
FROM     wm004 a
FULL OUTER JOIN
tbl_null_001 b
ON      a.vchr1 = b.vchr1
ORDER BY a.seqno, b.seqno, a.vchr1, b.vchr1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test076(desc="""NE113"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NE113"""
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

def test077(desc="""NE114"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NE114"""
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

def test078(desc="""NE115"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NE115"""
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

def test079(desc="""NE116"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NE116"""
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

def test080(desc="""NE117"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NE117"""
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

def test081(desc="""NE118"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NE118"""
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

def test082(desc="""NE119"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NE119"""
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

def test083(desc="""NE120"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NE120"""
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

def test084(desc="""NE121"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NE121"""
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

def test085(desc="""NE122"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NE122"""
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

def test086(desc="""NE123"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NE123"""
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

def test087(desc="""NE124"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NE124"""
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

def test088(desc="""NE125"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NE125"""
    stmt = """prepare s1 from
select     *
FROM
( select seqno FROM wm004) a(sq)
FULL OUTER JOIN
( select seqno FROM tbl_null_001) b(sq)
ON  a.sq = b.sq
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test089(desc="""NE126"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NE126"""
    stmt = """prepare s1 from
select     *
FROM
( select smin1 FROM wm004) a(s)
FULL OUTER JOIN
( select smin1 FROM tbl_null_001) b(s)
ON  a.s = b.s
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test090(desc="""NE127"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NE127"""
    stmt = """prepare s1 from
select     *
FROM
( select inte1 FROM wm004) a(i)
FULL OUTER JOIN
( select inte1 FROM tbl_null_001) b(i)
ON  a.i = b.i
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test091(desc="""NE128"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NE128"""
    stmt = """prepare s1 from
select     *
FROM
(select lint1 FROM wm004) a(l)
FULL OUTER JOIN
(select lint1 FROM tbl_null_001) b(l)
ON  a.l = b.l
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test092(desc="""NE129"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NE129"""
    stmt = """prepare s1 from
select     *
FROM
( select nume1 FROM wm004) a(n)
FULL OUTER JOIN
( select nume1 FROM tbl_null_001) b(n)
ON  a.n = b.n
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test093(desc="""NE130"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NE130"""
    stmt = """prepare s1 from
select     *
FROM
( select deci1 FROM wm004) a(d)
FULL OUTER JOIN
( select deci1 FROM tbl_null_001) b(d)
ON  a.d = b.d
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test094(desc="""NE131"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NE131"""
    stmt = """prepare s1 from
select     *
FROM
( select pict1 FROM wm004) a(p)
FULL OUTER JOIN
( select pict1 FROM tbl_null_001) b(p)
ON  a.p = b.p
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test095(desc="""NE132"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NE132"""
    stmt = """prepare s1 from
select     *
FROM
( select flot1 FROM wm004) a(f)
FULL OUTER JOIN
( select flot1 FROM tbl_null_001) b(f)
ON  a.f = b.f
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test096(desc="""NE133"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NE133"""
    stmt = """prepare s1 from
select     *
FROM
( select real1 FROM wm004) a(r)
FULL OUTER JOIN
( select real1 FROM tbl_null_001) b(r)
ON  a.r = b.r
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test097(desc="""NE134"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NE134"""
    stmt = """prepare s1 from
select     *
FROM
( select dblp1 FROM wm004) a(dp)
FULL OUTER JOIN
( select dblp1 FROM tbl_null_001) b(dp)
ON  a.dp = b.dp
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test098(desc="""NE135"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NE135"""
    stmt = """prepare s1 from
select     *
FROM
( select char1 FROM wm004) a(c)
FULL OUTER JOIN
( select char1 FROM tbl_null_001) b(c)
ON  a.c = b.c
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test099(desc="""NE136"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NE136"""
    stmt = """prepare s1 from
select     *
FROM
( select vchr1 FROM wm004) a(v)
FULL OUTER JOIN
( select vchr1 FROM tbl_null_001) b(v)
ON  a.v = b.v
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    # Elena Krotkova 5/24/07
    #  tables FOJ + where
    _testmgr.testcase_end(desc)

def test100(desc="""NEW101"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NEW101"""
    stmt = """prepare s1 from
select a.seqno,
b.seqno,
a.smin1,
b.smin1
FROM   wm004 a
FULL OUTER JOIN
tbl_null_001 b
ON        a.seqno = b.seqno
where (a.seqno > 3 and a.smin1 < 123) or
a.seqno <5
ORDER BY a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test101(desc="""NEW102"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NEW102"""
    stmt = """prepare s1 from
select      a.seqno,
b.seqno,
a.smin1,
b.smin1
FROM           wm004 a
FULL OUTER JOIN
tbl_null_001 b
ON             a.smin1 = b.smin1
where (a.seqno > 3 and a.smin1 < 123) or b.smin1 = 1
ORDER BY a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test102(desc="""NEW103"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NEW103"""
    stmt = """prepare s1 from
select      a.seqno,
b.seqno,
a.inte1,
b.inte1
FROM           wm004 a
FULL OUTER JOIN
tbl_null_001 b
ON             a.inte1 = b.inte1
where (a.inte1 > 3 and a.smin1 < 123) or
b.inte1 = 2
ORDER BY a.seqno, b.seqno, a.inte1, b.inte1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test103(desc="""NEW104"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NEW104"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.lint1,
b.lint1
FROM           wm004 a
FULL OUTER JOIN
tbl_null_001 b
ON             a.lint1 = b.lint1
where(a.lint1 > 3 and a.smin1 < 123) or
b.lint1 = 2
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test104(desc="""NEW105"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NEW105"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.nume1,
b.nume1
FROM           wm004 a
FULL OUTER JOIN
tbl_null_001 b
ON            a.nume1 = b.nume1
where (a.nume1  > 3 and a.smin1 < 1230) or
b.nume1  = 0 or b.nume1  <> 763.463
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test105(desc="""NEW106"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NEW106"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.deci1,
b.deci1
FROM           wm004 a
FULL OUTER JOIN
tbl_null_001 b
ON             a.deci1 = b.deci1
where (a.deci1  > 3 and a.smin1 < 1230) or
(b.deci1 <= 1 or a.deci1 <> -1000000 )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test106(desc="""NEW107"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NEW107"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.pict1,
b.pict1
FROM           wm004 a
FULL OUTER JOIN
tbl_null_001 b
ON             a.pict1 = b.pict1
where (a.pict1  > 3 and a.smin1 < 1230) or
( b.pict1  > 1 or a.pict1  < 1 )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test107(desc="""NEW108"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NEW108"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.flot1,
b.flot1
FROM           wm004 a
FULL OUTER JOIN
tbl_null_001 b
ON             a.flot1 = b.flot1
where (a.flot1   < 3 and a.smin1 > 1230) or
( b.flot1   > 1 or a.flot1  <> 0 )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test108(desc="""NEW109"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NEW109"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.real1,
b.real1
FROM           wm004 a
FULL OUTER JOIN
tbl_null_001 b
ON             a.real1 = b.real1
where (a.real1   < 3 and a.smin1 < 123) or
( b.real1   < 4 and a.real1  > 1 )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test109(desc="""NEW110"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NEW110"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.dblp1,
b.dblp1
FROM           wm004 a
FULL OUTER JOIN
tbl_null_001 b
ON             a.dblp1 = b.dblp1
where (a.dblp1   > 8 and a.smin1 < 123) or
( b.dblp1   < 1 or a.dblp1  <> 0 )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test110(desc="""NEW111"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NEW111"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.char1,
b.char1
FROM           wm004 a
FULL OUTER JOIN
tbl_null_001 b
ON             a.char1 = b.char1
where (a.char1   > '8' and a.smin1 < 1023) or
( b.char1   <= '1' or a.char1  <> '0' )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test111(desc="""NEW112"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NEW112"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.vchr1,
b.vchr1
FROM           wm004 a
FULL OUTER JOIN
tbl_null_001 b
ON             a.vchr1 = b.vchr1
where (a.vchr1  > '8' and a.smin1 < 35000) or
( b.vchr1   >= '1' or a.vchr1  <> '112345' )
ORDER BY       a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    # views FOJ + where clause
    # ---------------------1------------------------------------------
    _testmgr.testcase_end(desc)

def test112(desc="""NEW113"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NEW113"""
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

def test113(desc="""NEW114"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NEW114"""
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

def test114(desc="""NEW115"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NEW115"""
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

def test115(desc="""NEW116"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NEW116"""
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

def test116(desc="""NEW117"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NEW117"""
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

def test117(desc="""NEW118"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NEW118"""
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

def test118(desc="""NEW119"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NEW119"""
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

def test119(desc="""NEW120"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NEW120"""
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

def test120(desc="""NEW121"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NEW121"""
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

def test121(desc="""NEW122"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NEW122"""
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

def test122(desc="""NEW123"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NEW123"""
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

def test123(desc="""NEW124"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NEW124"""
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
    # ---------------------------rest------------------------------------
    # Multi Joins
    #--------------------------
    # some of FOJ do not have equality match
    #--------------------------
    _testmgr.testcase_end(desc)

def test124(desc="""NEM001"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NEM001"""
    stmt = """prepare s1 from
SELECT     a.seqno,
b.seqno
FROM       wm004 a
FULL OUTER JOIN
tbl_null_001 b
ON         a.seqno = b.seqno
FULL OUTER JOIN
vt_wm004 c
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
vt_tbl_null_001 g
ON         b.seqno = g.seqno
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test125(desc="""NEM002"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NEM002"""
    stmt = """prepare s1 from
SELECT     a.seqno,
b.seqno
FROM       wm004 a
FULL OUTER JOIN
wm004 b
ON         a.seqno = b.seqno
FULL OUTER JOIN
vt_wm004 c
ON         a.seqno = c.seqno
FULL OUTER JOIN
vt_tbl_null_001 d
ON         b.seqno = d.seqno
FULL OUTER JOIN
wm_vw_003 e
ON         b.seqno = e.n0sq
FULL OUTER JOIN
wm_vw_001  f
ON         b.seqno = f.n1sq
FULL OUTER JOIN
vt_tbl_null_001 g
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

def test126(desc="""NEM003"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """NEM003"""
    stmt = """prepare s1 from
select 			v.flot1,
w.seqno
from
(	select x.flot1,
y.seqno
from
(  select     b.seqno,
c.flot1
from       wm004 b
FULL OUTER JOIN
vt_wm004 c
ON         b.seqno = c.seqno
) as x    

FULL OUTER JOIN
( SELECT     d.seqno,
e.n0sq
from
vt_tbl_null_001 d
FULL OUTER JOIN
wm_vw_003 e
ON         d.seqno = e.n0sq
) as y
ON       x.seqno = y.seqno
)   as v
FULL OUTER JOIN
(    SELECT     a.n1sq,
b.seqno
from
( select    f.n1sq,
g.seqno
from
wm_vw_001  f
FULL OUTER JOIN
vt_tbl_null_001 g
ON        f.n1sq = g.seqno
) as a
FULL OUTER JOIN
( select    g.seqno,
f.smin1
from
wm004  f
FULL OUTER JOIN
wm004 g
ON        f.seqno = g.seqno
) as b    

ON      a.seqno = b.seqno
)   as w
ON          v.seqno  = w.seqno
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    #--------------------------
    # FOJ with 3 empty tables
    #--------------------------
    _testmgr.testcase_end(desc)

def test127(desc="""EEM001"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """EEM001"""
    stmt = """prepare s1 from
SELECT     a.seqno,
b.seqno
FROM       wm004 a
FULL OUTER JOIN
emp01 b
ON         a.seqno = b.seqno
FULL OUTER JOIN
emp00 c
ON         a.seqno = c.seqno
FULL OUTER JOIN
wm004 d
ON         b.seqno = d.seqno
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    #--------------------------
    _testmgr.testcase_end(desc)

def test128(desc="""EEM002"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """EEM002"""
    stmt = """prepare s1 from
SELECT     a.seqno,
b.seqno
FROM       wm004 a
FULL OUTER JOIN
emp01 b
ON         a.seqno = b.seqno
FULL OUTER JOIN
emp00 c
ON         a.seqno = c.seqno
FULL OUTER JOIN
wm004 d
ON         b.seqno = d.seqno
where (a.seqno > 3 and a.smin1 < 123) or
a.seqno <>5
ORDER BY 1,2;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    #--------------------------
    _testmgr.testcase_end(desc)

