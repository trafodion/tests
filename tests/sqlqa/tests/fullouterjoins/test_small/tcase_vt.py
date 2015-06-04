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

# Tests
# FROM fullouter2.sql (A201-A249)
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""A201"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A201"""
    stmt = """prepare s1 from
SELECT     a.seqno,
b.seqno
FROM          wm000 a
FULL OUTER JOIN
wm001 b
ON           a.seqno = b.seqno
ORDER BY a.seqno,b.seqno;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test002(desc="""A202"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A202"""
    stmt = """prepare s1 from
SELECT    a.seqno,
b.seqno,
a.smin1,
b.smin1
FROM          vt_wm000 a
FULL OUTER JOIN
vt_wm001 b
ON           a.smin1 = b.smin1
ORDER BY a.seqno,b.seqno,a.smin1,b.smin1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test003(desc="""A203"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A203"""
    stmt = """prepare s1 from
SELECT     a.seqno,
b.seqno,
a.inte1,
b.inte1
FROM          vt_wm000 a
FULL OUTER JOIN
vt_wm001 b
ON           a.inte1 = b.inte1
ORDER BY a.seqno,b.seqno,a.inte1,b.inte1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test004(desc="""A204"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A204"""
    stmt = """prepare s1 from
SELECT     a.seqno,
b.seqno,
a.lint1,
b.lint1
FROM          vt_wm000 a
FULL OUTER JOIN
vt_wm001 b
ON           a.lint1 = b.lint1
ORDER BY a.seqno,b.seqno,a.lint1,b.lint1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test005(desc="""A205"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A205"""
    stmt = """prepare s1 from
SELECT     a.seqno,
b.seqno,
a.nume1,
b.nume1
FROM          vt_wm000 a
FULL OUTER JOIN
vt_wm001 b
ON           a.nume1 = b.nume1
ORDER BY a.seqno,b.seqno,a.nume1, b.nume1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test006(desc="""A206"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A206"""
    stmt = """prepare s1 from
SELECT     a.seqno,
b.seqno,
a.deci1,
b.deci1
FROM          vt_wm000 a
FULL OUTER JOIN
vt_wm001 b
ON           a.deci1 = b.deci1
ORDER BY a.seqno,b.seqno,a.deci1,b.deci1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test007(desc="""A207"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A207"""
    stmt = """prepare s1 from
SELECT     a.seqno,
b.seqno,
a.pict1,
b.pict1
FROM          vt_wm000 a
FULL OUTER JOIN
vt_wm001 b
ON           a.pict1 = b.pict1
ORDER BY a.seqno,b.seqno,a.pict1,b.pict1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test008(desc="""A208"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A208"""
    stmt = """prepare s1 from
SELECT     a.seqno,
b.seqno,
a.flot1,
b.flot1
FROM          vt_wm000 a
FULL OUTER JOIN
vt_wm001 b
ON           a.flot1 = b.flot1
ORDER BY a.seqno,b.seqno,a.flot1, b.flot1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test009(desc="""A209"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A209"""
    stmt = """prepare s1 from
SELECT     a.seqno,
b.seqno,
a.real1,
b.real1
FROM          vt_wm000 a
FULL OUTER JOIN
vt_wm001 b
ON           a.real1 = b.real1
ORDER BY  a.seqno,b.seqno,a.real1,b.real1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test010(desc="""A210"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A210"""
    stmt = """prepare s1 from
SELECT     a.seqno,
b.seqno,
a.dblp1,
b.dblp1
FROM          vt_wm000 a
FULL OUTER JOIN
vt_wm001 b
ON           a.dblp1 = b.dblp1
ORDER BY a.seqno,b.seqno,a.dblp1,b.dblp1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test011(desc="""A211"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A211"""
    stmt = """prepare s1 from
SELECT     a.seqno,
b.seqno,
a.char1,
b.char1
FROM          vt_wm000 a
FULL OUTER JOIN
vt_wm001 b
ON           a.char1 = b.char1
ORDER BY a.seqno,b.seqno,a.char1,b.char1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test012(desc="""A212"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A212"""
    stmt = """prepare s1 from
SELECT     a.seqno,
b.seqno,
a.vchr1,
b.vchr1
FROM          vt_wm000 a
FULL OUTER JOIN
vt_wm001 b
ON           a.vchr1 = b.vchr1
ORDER BY a.seqno,b.seqno,a.vchr1,b.vchr1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test013(desc="""A213"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A213"""
    stmt = """prepare s1 from
SELECT     a.seqno,
b.seqno
FROM          wm000 a
FULL OUTER JOIN
wm001 b
ON           a.seqno = b.seqno
FULL OUTER JOIN
vt_wm000 c
ON           a.seqno = c.seqno
ORDER BY a.seqno,b.seqno;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test014(desc="""A214"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A214"""
    stmt = """prepare s1 from
SELECT     a.seqno,
b.seqno,
a.smin1,
b.smin1
FROM          wm000 a
FULL OUTER JOIN
wm001 b
ON           a.smin1 = b.smin1
FULL OUTER JOIN
vt_wm000 c
ON           a.smin1 = c.smin1
ORDER BY a.seqno,b.seqno,a.smin1,b.smin1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test015(desc="""A215"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A215"""
    stmt = """prepare s1 from
SELECT     a.seqno,
b.seqno,
a.inte1,
b.inte1
FROM          wm000 a
FULL OUTER JOIN
wm001 b
ON           a.inte1 = b.inte1
FULL OUTER JOIN
vt_wm000 c
ON           a.inte1 = c.inte1
ORDER BY a.seqno,b.seqno,a.inte1, b.inte1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test016(desc="""A216"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A216"""
    stmt = """prepare s1 from
SELECT     a.seqno,
b.seqno,
a.lint1,
b.lint1
FROM          wm000 a
FULL OUTER JOIN
wm001 b
ON           a.lint1 = b.lint1
FULL OUTER JOIN
vt_wm000 c
ON           a.lint1 = c.lint1
ORDER BY a.seqno,b.seqno,a.lint1,b.lint1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test017(desc="""A217"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A217"""
    stmt = """prepare s1 from
SELECT     a.seqno,
b.seqno,
a.nume1,
b.nume1
FROM          wm000 a
FULL OUTER JOIN
wm001 b
ON           a.nume1 = b.nume1
FULL OUTER JOIN
vt_wm000 c
ON           a.nume1 = c.nume1
ORDER BY a.seqno,b.seqno,a.nume1,b.nume1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test018(desc="""A218"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A218"""
    stmt = """prepare s1 from
SELECT     a.seqno,
b.seqno,
a.deci1,
b.deci1
FROM          wm000 a
FULL OUTER JOIN
wm001 b
ON           a.deci1 = b.deci1
FULL OUTER JOIN
vt_wm000 c
ON           a.deci1 = c.deci1
ORDER BY a.seqno,b.seqno,a.deci1, b.deci1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test019(desc="""A219"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A219"""
    stmt = """prepare s1 from
SELECT     a.seqno,
b.seqno,
a.pict1,
b.pict1
FROM          wm000 a
FULL OUTER JOIN
wm001 b
ON           a.pict1 = b.pict1
FULL OUTER JOIN
vt_wm000 c
ON           a.pict1 = c.pict1
ORDER BY a.seqno,b.seqno,a.pict1,b.pict1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test020(desc="""A220"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A220"""
    stmt = """prepare s1 from
SELECT     a.seqno,
b.seqno,
a.flot1,
b.flot1
FROM          wm000 a
FULL OUTER JOIN
wm001 b
ON           a.flot1 = b.flot1
FULL OUTER JOIN
vt_wm000 c
ON           a.flot1 = c.flot1
ORDER BY a.seqno,b.seqno,a.flot1,b.flot1  ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test021(desc="""A221"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A221"""
    stmt = """prepare s1 from
SELECT     a.seqno,
b.seqno,
a.real1,
b.real1
FROM          wm000 a
FULL OUTER JOIN
wm001 b
ON           a.real1 = b.real1
FULL OUTER JOIN
vt_wm000 c
ON           a.real1 = c.real1
ORDER BY a.seqno,b.seqno,a.real1,b.real1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test022(desc="""A222"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A222"""
    stmt = """prepare s1 from
SELECT     a.seqno,
b.seqno,
a.dblp1,
b.dblp1
FROM          wm000 a
FULL OUTER JOIN
wm001 b
ON           a.dblp1 = b.dblp1
FULL OUTER JOIN
vt_wm000 c
ON           a.dblp1 = c.dblp1
ORDER BY a.seqno,b.seqno,a.dblp1,b.dblp1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test023(desc="""A223"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A223"""
    stmt = """prepare s1 from
SELECT     a.seqno,
b.seqno,
a.char1,
b.char1
FROM          wm000 a
FULL OUTER JOIN
wm001 b
ON           a.char1 = b.char1
FULL OUTER JOIN
vt_wm000 c
ON           a.char1 = c.char1
ORDER BY a.seqno,b.seqno,a.char1,b.char1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test024(desc="""A224"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A224"""
    stmt = """prepare s1 from
SELECT     a.seqno,
b.seqno,
a.vchr1,
b.vchr1
FROM          wm000 a
FULL OUTER JOIN
wm001 b
ON           a.vchr1 = b.vchr1
FULL OUTER JOIN
vt_wm000 c
ON           a.vchr1 = c.vchr1
ORDER BY a.seqno,b.seqno,a.vchr1,b.vchr1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test025(desc="""A225"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A225"""
    stmt = """prepare s1 from
SELECT     n0sq,
n1sq,
seqno,
n0s1
FROM          wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON           a.n0sq = n1sq
FULL OUTER JOIN
vt_wm000 c
ON           a.n0sq = c.seqno
ORDER BY n0sq,n1sq,seqno,n0s1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test026(desc="""A226"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A226"""
    stmt = """prepare s1 from
SELECT     a.n0sq,
b.n1sq,
a.n0s1,
b.n1s1
FROM          wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON           a.n0s1 = b.n1s1
FULL OUTER JOIN
vt_wm000 c
ON           a.n0s1 = c.smin1
ORDER BY a.n0sq,b.n1sq,a.n0s1, b.n1s1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test027(desc="""A227"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A227"""
    stmt = """prepare s1 from
SELECT     a.n0sq,
b.n1sq,
a.n0i1,
b.n1i1
FROM          wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON           a.n0i1 = b.n1i1
FULL OUTER JOIN
vt_wm000 c
ON           a.n0i1 = c.inte1
ORDER BY a.n0sq,b.n1sq,a.n0i1,b.n1i1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test028(desc="""A228"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A228"""
    stmt = """prepare s1 from
SELECT     a.n0sq,
b.n1sq,
a.n0l1,
b.n1s1
FROM          wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON           a.n0l1 = b.n1l1
FULL OUTER JOIN
vt_wm000 c
ON           a.n0l1 = c.lint1
ORDER BY a.n0sq,b.n1sq,a.n0l1,b.n1s1  ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test029(desc="""A229"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A229"""
    stmt = """prepare s1 from
SELECT     a.n0sq,
b.n1sq,
a.n0n1,
b.n1n1
FROM          wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON           a.n0n1 = b.n1n1
FULL OUTER JOIN
vt_wm000 c
ON           a.n0n1 = c.nume1
ORDER BY  a.n0sq,b.n1sq,a.n0n1,b.n1n1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test030(desc="""A230"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A230"""
    stmt = """prepare s1 from
SELECT     a.n0sq,
b.n1sq,
a.n0d1,
b.n1d1
FROM          wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON           a.n0d1 = b.n1d1
FULL OUTER JOIN
vt_wm000 c
ON           a.n0d1 = c.deci1
ORDER BY a.n0sq,b.n1sq,a.n0d1,b.n1d1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test031(desc="""A231"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A231"""
    stmt = """prepare s1 from
SELECT     a.n0sq,
b.n1sq,
a.n0p1,
b.n1p1
FROM          wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON           a.n0p1 = b.n1p1
FULL OUTER JOIN
vt_wm000 c
ON           a.n0p1 = c.pict1
ORDER BY a.n0sq,b.n1sq,a.n0p1,b.n1p1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test032(desc="""A232"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A232"""
    stmt = """prepare s1 from
SELECT     a.n0sq,
b.n1sq,
a.n0f1,
b.n1f1
FROM          wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON           a.n0f1 = b.n1f1
FULL OUTER JOIN
vt_wm000 c
ON           a.n0f1 = c.flot1
ORDER BY a.n0sq,b.n1sq,a.n0f1,b.n1f1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test033(desc="""A233"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A233"""
    stmt = """prepare s1 from
SELECT     a.n0sq,
b.n1sq,
a.n0r1,
b.n1r1
FROM          wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON           a.n0r1 = b.n1r1
FULL OUTER JOIN
vt_wm000 c
ON           a.n0r1 = c.real1
ORDER BY a.n0sq,b.n1sq,a.n0r1,b.n1r1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test034(desc="""A234"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A234"""
    stmt = """prepare s1 from
SELECT     a.n0sq,
b.n1sq,
a.n0dp1,
b.n1dp1
FROM          wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON           a.n0dp1 = b.n1dp1
FULL OUTER JOIN
vt_wm000 c
ON           a.n0dp1 = c.dblp1
ORDER BY a.n0sq,b.n1sq,a.n0dp1,b.n1dp1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test035(desc="""A235"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A235"""
    stmt = """prepare s1 from
SELECT     a.n0sq,
b.n1sq,
a.n0c1,
b.n1c1
FROM          wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON           a.n0c1 = b.n1c1
FULL OUTER JOIN
vt_wm000 c
ON           a.n0c1 = c.char1
ORDER BY a.n0sq,b.n1sq,a.n0c1,b.n1c1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test036(desc="""A236"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A236"""
    stmt = """prepare s1 from
SELECT     a.n0sq,
b.n1sq,
a.n0v1,
b.n1v1
FROM          wm_vw_000 a
FULL OUTER JOIN
wm_vw_001 b
ON           a.n0v1 = b.n1v1
FULL OUTER JOIN
vt_wm000 c
ON           a.n0v1 = c.vchr1
ORDER BY a.n0sq,b.n1sq,a.n0v1,b.n1v1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test037(desc="""A237"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A237"""
    stmt = """prepare s1 from
SELECT  seqno,smin1,inte1
FROM     ( SELECT seqno  FROM wm000) a(sq)
FULL OUTER JOIN
( SELECT seqno  FROM wm001) b(sq)
ON      a.sq = b.sq
FULL OUTER JOIN
vt_wm000 c
ON      a.sq = c.seqno
ORDER BY seqno,smin1,inte1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test038(desc="""A238"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A238"""
    stmt = """prepare s1 from
SELECT    seqno, smin1,inte1
FROM     ( SELECT smin1  FROM wm000) a(s)
FULL OUTER JOIN
( SELECT smin1  FROM wm001) b(s)
ON      a.s = b.s
FULL OUTER JOIN
vt_wm000 c
ON      a.s = c.smin1
ORDER BY seqno, smin1,inte1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test039(desc="""A239"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A239"""
    stmt = """prepare s1 from
SELECT    seqno, smin1,inte1
FROM     (SELECT inte1  FROM wm000) a(i)
FULL OUTER JOIN
( SELECT inte1  FROM wm001) b(i)
ON      a.i = b.i
FULL OUTER JOIN
vt_wm000 c
ON      a.i = c.inte1
ORDER BY seqno, smin1,inte1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test040(desc="""A240"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A240"""
    stmt = """prepare s1 from
SELECT   seqno, smin1,lint1
FROM     ( SELECT lint1  FROM wm000) a(l)
FULL OUTER JOIN
( SELECT lint1  FROM wm001) b(l)
ON      a.l = b.l
FULL OUTER JOIN
vt_wm000 c
ON      a.l = c.lint1
ORDER BY seqno, smin1,lint1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test041(desc="""A241"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A241"""
    stmt = """prepare s1 from
SELECT     seqno, smin1,nume1
FROM     ( SELECT nume1  FROM wm000) a(n)
FULL OUTER JOIN
( SELECT nume1  FROM wm001) b(n)
ON      a.n = b.n
FULL OUTER JOIN
vt_wm000 c
ON      a.n = c.nume1
ORDER BY seqno, smin1,nume1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test042(desc="""A242"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A242"""
    stmt = """prepare s1 from
SELECT    seqno, smin1,deci1
FROM     ( SELECT deci1  FROM wm000) a(d)
FULL OUTER JOIN
( SELECT deci1  FROM wm001) b(d)
ON      a.d = b.d
FULL OUTER JOIN
vt_wm000 c
ON      a.d = c.deci1
ORDER BY seqno, smin1,deci1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test043(desc="""A243"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A243"""
    stmt = """prepare s1 from
SELECT   seqno, smin1,pict1
FROM     (SELECT pict1  FROM wm000) a(p)
FULL OUTER JOIN
( SELECT pict1  FROM wm001) b(p)
ON      a.p = b.p
FULL OUTER JOIN
vt_wm000 c
ON      a.p = c.pict1
ORDER BY seqno, smin1,pict1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test044(desc="""A244"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A244"""
    stmt = """prepare s1 from
SELECT    seqno, smin1,flot1
FROM     ( SELECT flot1  FROM wm000) a(f)
FULL OUTER JOIN
( SELECT flot1  FROM wm001) b(f)
ON      a.f = b.f
FULL OUTER JOIN
vt_wm000 c
ON      a.f = c.flot1
ORDER BY seqno, smin1,flot1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test045(desc="""A245"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A245"""
    stmt = """prepare s1 from
SELECT  seqno, smin1,real1
FROM     ( SELECT real1  FROM wm000) a(r)
FULL OUTER JOIN
( SELECT real1  FROM wm001) b(r)
ON      a.r = b.r
FULL OUTER JOIN
vt_wm000 c
ON      a.r = c.real1
ORDER BY seqno, smin1,real1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test046(desc="""A246"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A246"""
    stmt = """prepare s1 from
SELECT    seqno, smin1,dblp1
FROM     ( SELECT dblp1  FROM wm000) a(dp)
FULL OUTER JOIN
( SELECT dblp1  FROM wm001) b(dp)
ON      a.dp = b.dp
FULL OUTER JOIN
vt_wm000 c
ON      a.dp = c.dblp1
ORDER BY seqno, smin1,dblp1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test047(desc="""A247"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A247"""
    stmt = """prepare s1 from
SELECT    seqno, smin1,char1
FROM     ( SELECT char1  FROM wm000) a(c)
FULL OUTER JOIN
( SELECT char1  FROM wm001) b(c)
ON      a.c = b.c
FULL OUTER JOIN
vt_wm000 c
ON      a.c = c.char1
ORDER BY seqno, smin1,char1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test048(desc="""A248"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A248"""
    stmt = """prepare s1 from
SELECT  seqno, smin1,vchr1
FROM     ( SELECT vchr1  FROM wm000) a(v)
FULL OUTER JOIN
( SELECT vchr1  FROM wm001) b(v)
ON      a.v = b.v
FULL OUTER JOIN
vt_wm000 c
ON      a.v = c.vchr1
ORDER BY seqno, smin1,vchr1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test049(desc="""A249"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """A249"""
    stmt = """prepare s1 from
SELECT  a.s, b.s, seqm
FROM    ( SELECT smin1  FROM wm000) a(s)
FULL OUTER JOIN
( SELECT l.smin1, m.seqno
FROM wm001 l
left outer join wm001 m
ON l.smin1 = m.smin1
) b(s, seqm)
ON        a.s = b.s
ORDER BY a.s, b.s, seqm ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    #  Elena Krotkova
    #  05/25/07
    #  violatile tables - FOJ + WHERE
    _testmgr.testcase_end(desc)

def test050(desc="""VT101"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """VT101"""
    stmt = """prepare s1 from
select  a.seqno,
b.seqno,
a.smin1,
b.smin1
FROM    vt_wm000 a
FULL OUTER JOIN
vt_wm001 b
ON      a.seqno = b.seqno
WHERE (a.seqno > 3 and b.smin1 < 123) or
a.seqno <5
ORDER BY a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test051(desc="""VT102"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """VT102"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.smin1,
b.smin1
FROM    vt_wm000 a
FULL OUTER JOIN
vt_wm001 b
ON      a.smin1 = b.smin1
WHERE ( a.seqno > 3 and a.smin1 < 123) or
b.smin1 = 1
ORDER BY a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test052(desc="""VT103"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """VT103"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.inte1,
b.inte1
FROM     vt_wm000 a
FULL OUTER JOIN vt_wm001 b
ON a.inte1 = b.inte1
WHERE (a.inte1 > 3 and a.smin1 < 123) or b.inte1 = 2
ORDER BY a.seqno, b.seqno, a.inte1, b.inte1;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test053(desc="""VT104"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """VT104"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.lint1,
b.lint1
FROM     vt_wm000 a
FULL OUTER JOIN
vt_wm001 b
ON      a.lint1 = b.lint1
WHERE (a.lint1 > 3 and a.smin1 < 123) or
b.lint1 = 2
ORDER BY a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test054(desc="""VT105"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """VT105"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.nume1,
b.nume1
FROM     vt_wm000 a
FULL OUTER JOIN
vt_wm001 b
ON      a.nume1 = b.nume1
WHERE (a.nume1  > 3 and a.smin1 < 1230) or
b.nume1  = 0 or b.nume1  <> 763.463
ORDER BY a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test055(desc="""VT106"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """VT106"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.deci1,
b.deci1
FROM     vt_wm000 a
FULL OUTER JOIN
vt_wm001 b
ON      a.deci1 = b.deci1
WHERE (a.deci1  > 3 and a.smin1 < 1230) or
(b.deci1 <= 1 or a.deci1 <> -1000000 )
ORDER BY a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test056(desc="""VT107"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """VT107"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.pict1,
b.pict1
FROM     vt_wm000 a
FULL OUTER JOIN
vt_wm001 b
ON      a.pict1 = b.pict1
WHERE (a.pict1  > 3 and a.smin1 < 1230) or
(b.pict1  > 1 or a.pict1  < 1 )
ORDER BY a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test057(desc="""VT108"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """VT108"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.flot1,
b.flot1
FROM     vt_wm000 a
FULL OUTER JOIN
vt_wm001 b
ON      a.flot1 = b.flot1
WHERE (a.flot1   < 3 and a.smin1 < 1230) or
( b.flot1   > 1 or a.flot1  <> 0 )
ORDER BY a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test058(desc="""VT109"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """VT109"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.real1,
b.real1
FROM     vt_wm000 a
FULL OUTER JOIN
vt_wm001 b
ON      a.real1 = b.real1
WHERE (a.real1   < 3 and a.smin1 < 123) or
( b.real1   < 4 and a.real1  > 1 )
ORDER BY a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test059(desc="""VT110"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """VT110"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.dblp1,
b.dblp1
FROM     vt_wm000 a
FULL OUTER JOIN
vt_wm001 b
ON      a.dblp1 = b.dblp1
WHERE (a.dblp1   > 8 and a.smin1 < 123) or
(b.dblp1   < 1 or a.dblp1  <> 0 )
ORDER BY a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test060(desc="""VT111"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """VT111"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.char1,
b.char1
FROM          vt_wm000 a
FULL OUTER JOIN
vt_wm001 b
ON           a.char1 = b.char1
WHERE (a.char1   > '8' and a.smin1 < 1023) or
( b.char1   <= '1' or a.char1  <> '0' )
ORDER BY a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    _testmgr.testcase_end(desc)

def test061(desc="""VT112"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    defs.testid = """VT112"""
    stmt = """prepare s1 from
select     a.seqno,
b.seqno,
a.vchr1,
b.vchr1
FROM          vt_wm000 a
FULL OUTER JOIN
vt_wm001 b
ON           a.vchr1 = b.vchr1
WHERE (a.vchr1  > '8' and a.smin1 < 35000) or
( b.vchr1   >= '1' or a.vchr1  <> '112345' )
ORDER BY      a.seqno, b.seqno, a.smin1, b.smin1 ;"""
    output = _dci.cmdexec(stmt)
    setup.atest()
    
    _testmgr.testcase_end(desc)

