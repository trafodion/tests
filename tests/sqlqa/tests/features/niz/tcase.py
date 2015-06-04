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

# ==================   Begin Test Case Header   ==================
#
#  Test case name:     NIZ001
#  Description	: Tests for function NULLIFZERO
#
#	Syntax		: NULLIFZERO(<operand>)
#   	Semantics	:
#		if <operand> is equal to zero, then return NULL.
#		if <operand> is not equal to zero, then return <operand>
#		<operand> must be one of the numeric datatypes
#			(decimal, floats, int, etc..).
#		Same as CASE WHEN <operand> <> 0
#			then <operand>
#			ELSE NULL END
#
#	Examples	:
#		select NULLIFZERO(1) from (values(1)) x(a);
#			-- should return 1
#		select NULLIFZERO(0) from (values(1)) x(a);
#			-- should return NULL (?)
#
#	This is a positive test with these inputs to NULLIFZERO...
#	1) NULLs,
#	2) Simple numeric values &
#	3) Numeric expressions
#
#  Revision History:
#      05/05/06       Created.
#
# =================== End Test Case Header  ===================

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""N01"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """select	smin1,
NULLIFZERO (smin1),
smin2,
NULLIFZERO (smin2)
from niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz000')
    
    stmt = """select	inte1,
NULLIFZERO (inte1),
inte2,
NULLIFZERO (inte2)
from niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz001')
    
    stmt = """select  lint1,
NULLIFZERO (lint1)
from    niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz002')
    
    stmt = """select	lint2,
NULLIFZERO (lint2)
from    niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz003')
    
    stmt = """select  nume1,
NULLIFZERO (nume1),
nume2,
NULLIFZERO (nume2)
from    niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz004')
    
    stmt = """select  nume3,
NULLIFZERO (nume3)
from    niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz005')
    
    stmt = """select	nume4,
NULLIFZERO (nume4)
from    niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz006')
    
    stmt = """select  deci1,
NULLIFZERO (deci1),
deci2,
NULLIFZERO (deci2)
from    niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz007')
    
    stmt = """select	deci3,
NULLIFZERO (deci3)
from    niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz008')
    
    stmt = """select  pict1,
NULLIFZERO (pict1),
pict2,
NULLIFZERO (pict2)
from    niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz009')
    
    stmt = """select	pict3,
NULLIFZERO (pict3),
pict4,
NULLIFZERO (pict4)
from    niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz010')
    
    stmt = """select  real1,
NULLIFZERO (real1),
real2,
NULLIFZERO (real2)
from    niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz011')
    
    stmt = """select  dblp1,
NULLIFZERO (dblp1)
from    niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz012')
    
    stmt = """select	dblp2,
NULLIFZERO (dblp2)
from    niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz013')
    
    # Simple Numeric Expressions (+)
    
    stmt = """select	(smin1 + smin2),
NULLIFZERO (smin1 + smin2)
from niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz014')
    
    stmt = """select	(inte1 + inte2),
NULLIFZERO (inte1 + inte2)
from niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz015')
    
    stmt = """select  (lint1 + lint2),
NULLIFZERO (lint1 + lint2)
from    niz000 
where 	seqno <> 4
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz016')
    
    # mode_1: error 8411
    stmt = """select  (nume1 + nume2 + nume3 + nume4),
NULLIFZERO (nume1 + nume2 + nume3 + nume4)
from    niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz017')
    
    # mode_1: error 8411
    stmt = """select  (deci1 + deci2 + deci3),
NULLIFZERO (deci1 + deci2 + deci3)
from    niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz018')
    
    # mode_1: error 8411
    stmt = """select  (pict1 + pict2 + pict3 + pict4),
NULLIFZERO (pict1 + pict2 + pict3 + pict4)
from    niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz019')
    
    stmt = """select  (real1 + real2),
NULLIFZERO (real1 + real2)
from    niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz020')
    
    stmt = """select  (dblp1 + dblp2),
NULLIFZERO (dblp1 + dblp2)
from    niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz021')
    
    # Simple Numeric Expressions (-)
    
    stmt = """select	(smin1 - smin2),
NULLIFZERO (smin1 - smin2)
from niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz022')
    
    stmt = """select	(inte1 - inte2),
NULLIFZERO (inte1 - inte2)
from niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz023')
    
    stmt = """select  (lint1 - lint2),
NULLIFZERO (lint1 - lint2)
from    niz000 
where 	seqno not in (4, 5)
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz024')
    
    # mode_1: error 8411
    stmt = """select  (nume1 - nume2 - nume3 - nume4),
NULLIFZERO (nume1 - nume2 - nume3 - nume4)
from    niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz025')
    
    # mode_1: error 8411
    stmt = """select  (deci1 - deci2 - deci3),
NULLIFZERO (deci1 - deci2 - deci3)
from    niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz026')
    
    # mode_1: error 8411
    stmt = """select  (pict1 - pict2 - pict3 - pict4),
NULLIFZERO (pict1 - pict2 - pict3 - pict4)
from    niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz027')
    
    stmt = """select  (real1 - real2),
NULLIFZERO (real1 - real2)
from    niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz028')
    
    stmt = """select  (dblp1 - dblp2),
NULLIFZERO (dblp1 - dblp2)
from    niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz029')
    
    # Simple Numeric Expressions (*)
    
    stmt = """select	(smin1 * smin2),
NULLIFZERO (smin1 * smin2)
from niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz030')
    
    stmt = """select	(inte1 * inte2),
NULLIFZERO (inte1 * inte2)
from niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz031')
    
    stmt = """select  (lint1 * lint2),
NULLIFZERO (lint1 * lint2)
from    niz000 
where 	seqno not in (4, 5, 6)
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz032')
    
    # mode_1: error 8411
    stmt = """select  (nume1 * nume2 * nume3 * nume4),
NULLIFZERO (nume1 * nume2 * nume3 * nume4)
from    niz000 
where	seqno not in (4, 5)
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz033')
    
    stmt = """select  (deci1 * deci2 * deci3),
NULLIFZERO (deci1 * deci2 * deci3)
from    niz000 
where	seqno not in (4, 5, 6)
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz034')
    
    #SAP
    
    # mode_1: error 8411
    stmt = """select	pict1,
pict2,
(pict1 * pict2),
NULLIFZERO (pict1 * pict2)
from    niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz035')
    
    # mode_1: error 8411
    stmt = """select  (pict3 * pict4),
NULLIFZERO (pict3 * pict4)
from    niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz036')
    
    stmt = """select  (real1 * real2),
NULLIFZERO (real1 * real2)
from    niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz037')
    
    stmt = """select  (dblp1 *
(
case 	when dblp2 = 9 then dblp2 * 0.1
else dblp2
end
)
),
NULLIFZERO
(dblp1 *
(
case 	when dblp2 = 9 then dblp2 * 0.1
else dblp2
end
)
)
from    niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz038')
    
    # Simple Numeric Expressions (/)
    
    stmt = """select	(smin1 / NULLIFZERO (smin2)),
NULLIFZERO (smin1 / NULLIFZERO (smin2))
from niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz039')
    
    stmt = """select	(inte1 / NULLIFZERO (inte2)),
NULLIFZERO (inte1 / NULLIFZERO (inte2))
from niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz040')
    
    stmt = """select  (lint1 / NULLIFZERO (lint2)),
NULLIFZERO (lint1 / NULLIFZERO (lint2))
from    niz000 
where 	seqno not in (4, 5)
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz041')
    
    #SAP
    
    # mode_1: error 8411
    stmt = """select  ((nume1 * nume2) / NULLIFZERO (nume3 * nume4)),
NULLIFZERO ((nume1 * nume2) / NULLIFZERO (nume3 * nume4))
from    niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz042')
    
    # mode_1: error 8411
    stmt = """select  ((deci1 * deci2) / NULLIFZERO (deci3)),
NULLIFZERO ((deci1 * deci2) / NULLIFZERO (deci3))
from    niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz043')
    
    #SAP
    
    # mode_1: error 8411
    stmt = """select  ((pict1 * pict2) / NULLIFZERO (pict3 * pict4)),
NULLIFZERO ((pict1 * pict2) / NULLIFZERO (pict3 * pict4))
from    niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz044')
    
    stmt = """select  (real1 / NULLIFZERO (real2)),
NULLIFZERO (real1 / NULLIFZERO (real2))
from    niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz045')
    
    stmt = """select  (dblp1 / NULLIFZERO (dblp2)),
NULLIFZERO (dblp1 / NULLIFZERO (dblp2))
from    niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz046')
    
    #SAP
    # Simple Numeric Expressions (**)
    
    stmt = """select	(smin1 ** -2),
NULLIFZERO (smin1 ** -2)
from niz000 
where	smin1 is not null and
smin1 <> 0
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz047')
    
    stmt = """select	(inte1 ** 3),
NULLIFZERO (inte1 ** 3)
from niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz048')
    
    stmt = """select  (lint1 ** 0),
NULLIFZERO (lint1 ** 0)
from    niz000 
where 	lint1 is not null and
lint1 <> 0
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz049')
    
    # mode_1: error 8411
    stmt = """select  ((nume1 * nume2 * nume3 * nume4) ** 1),
NULLIFZERO ((nume1 * nume2 * nume3 * nume4) ** 1)
from    niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz050')
    
    # mode_1: error 8411
    stmt = """select  ((deci1 * deci2 / NULLIFZERO (deci3)) ** 2),
NULLIFZERO ((deci1 * deci2 / NULLIFZERO (deci3)) ** 2)
from    niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz051')
    
    #SAP
    #Change Query. This is same as niz044
    # mode_1: error 8411
    stmt = """select  ((pict1 * pict2) / NULLIFZERO (pict3 * pict4)),
NULLIFZERO ((pict1 * pict2) / NULLIFZERO (pict3 * pict4))
from    niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz052')
    
    stmt = """select  ((real1 + real2) ** -1),
NULLIFZERO ((real1 + real2) ** -1)
from    niz000 
where	(real1 + real2) <> 0
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz053')
    
    stmt = """select  ((dblp1 / NULLIFZERO (dblp2)) ** 3),
NULLIFZERO ((dblp1 / NULLIFZERO (dblp2)) ** 3)
from    niz000 
where	(dblp1 / NULLIFZERO (dblp2)) is not null
and seqno not in (4, 5)
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz054')
    
    # ==================   Begin Test Case Header   ==================
    #
    #  Test case name:     NIZ002
    #  Description	: Tests for function NULLIFZERO
    #
    #	Syntax		: NULLIFZERO(<operand>)
    #   	Semantics	:
    #		if <operand> is equal to zero, then return NULL.
    #		if <operand> is not equal to zero, then return <operand>
    #		<operand> must be one of the numeric datatypes
    #			(decimal, floats, int, etc..).
    #		Same as CASE WHEN <operand> <> 0
    #			then <operand>
    #			ELSE NULL END
    #
    #	Examples	:
    #		select NULLIFZERO(1) from (values(1)) x(a);
    #			-- should return 1
    #		select NULLIFZERO(0) from (values(1)) x(a);
    #			-- should return NULL (?)
    #
    #	This is a positive test involving casts to other numeric data types
    #
    #  Revision History:
    #      05/05/06       Created.
    #
    # =================== End Test Case Header  ===================
    
    _testmgr.testcase_end(desc)

def test002(desc="""N02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """select	smin1,
NULLIFZERO (cast (smin1 as int)),
smin2,
NULLIFZERO (cast (smin2 as double precision))
from niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz055')
    
    stmt = """select	inte1,
NULLIFZERO (cast (inte1 as largeint)),
inte2,
NULLIFZERO (cast (inte2 as decimal(12)))
from niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz056')
    
    stmt = """select	lint1,
NULLIFZERO (cast (lint1 as double precision)),
lint2,
NULLIFZERO (cast (lint2 as float(52)))
from niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz057')
    
    stmt = """select	nume1,
NULLIFZERO (cast (nume1 as real)),
nume2,
NULLIFZERO (cast (nume2 as float(12)))
from niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz058')
    
    stmt = """select	nume3,
NULLIFZERO (cast (nume3 as real))
from niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz059')
    
    stmt = """select	nume4,
NULLIFZERO (cast (nume4 as double precision))
from niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz060')
    
    stmt = """select	deci1,
NULLIFZERO (cast (deci1 as smallint))
from niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz061')
    
    stmt = """select	deci2,
NULLIFZERO (cast (deci2 as double precision))
from niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz062')
    
    stmt = """select	deci3,
NULLIFZERO (cast (deci3 as float (52)))
from niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz063')
    
    # mode_1: error 8411
    stmt = """select	(((pict1 * pict2) / NULLIFZERO (pict3)) - pict4),
NULLIFZERO
(cast ((((pict1 * pict2) / NULLIFZERO (pict3)) - pict4)
as integer))
from niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz064')
    
    stmt = """select	(flot1 * flot2),
NULLIFZERO ((cast (flot1 as double precision)) * flot2)
from niz000 
where	seqno <> 5
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz065')
    
    stmt = """select	(real1 / NULLIFZERO (real2)),
NULLIFZERO ((cast (real1 as float)) / NULLIFZERO (real2))
from niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz066')
    
    stmt = """select	(dblp1 / NULLIFZERO (dblp2)),
NULLIFZERO ((cast (dblp1 as float)) / NULLIFZERO (dblp2))
from niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz067')
    
    # mode_1: error 8411
    stmt = """select	smin1 +
smin2 -    

inte1 +
cast (inte2 as largeint) /    

NULLIFZERO (lint1) +
lint2 -    

nume1 +
nume2 -
cast (nume3 as double precision) +
nume4 -    

deci1 +
deci2 -    

pict1 +
pict2 -
pict3 +
pict4 -    

flot1 +
flot2 -    

real1 +
real2 -    

dblp1 +
dblp2,    

NULLIFZERO
(
smin1 +
smin2 -    

inte1 +
inte2 -    

NULLIFZERO (lint1) +
lint2 -    

nume1 +
nume2 -
nume3 +
nume4 -    

deci1 +
deci2 -    

pict1 +
pict2 -
pict3 +
pict4 -    

flot1 +
flot2 -    

real1 +
real2 -    

dblp1 +
dblp2
)    

from niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz068')
    
    # ==================   Begin Test Case Header   ==================
    #
    #  Test case name:     NIZ003
    #  Description	: Tests for function NULLIFZERO
    #
    #	Syntax		: NULLIFZERO(<operand>)
    #   	Semantics	:
    #		if <operand> is equal to zero, then return NULL.
    #		if <operand> is not equal to zero, then return <operand>
    #		<operand> must be one of the numeric datatypes
    #			(decimal, floats, int, etc..).
    #		Same as CASE WHEN <operand> <> 0
    #			then <operand>
    #			ELSE NULL END
    #
    #	Examples	:
    #		select NULLIFZERO(1) from (values(1)) x(a);
    #			-- should return 1
    #		select NULLIFZERO(0) from (values(1)) x(a);
    #			-- should return NULL (?)
    #
    #	This is a positive test involving functions within NULLIFZERO
    #
    #  Revision History:
    #      05/05/06       Created.
    #
    # =================== End Test Case Header  ===================
    
    _testmgr.testcase_end(desc)

def test003(desc="""N03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # mode_1: error 8411
    stmt = """select	NULLIFZERO
(
avg (NULLIFZERO (smin1)) +
avg (NULLIFZERO (inte1)) +
avg (NULLIFZERO (lint1)) +
avg (NULLIFZERO (nume1)) +
avg (NULLIFZERO (deci1)) +
avg (NULLIFZERO (pict1)) +
avg (NULLIFZERO (flot1)) +
avg (NULLIFZERO (real1)) +
avg (NULLIFZERO (dblp1))
)
from niz000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz069')
    
    stmt = """select	NULLIFZERO
(
count (NULLIFZERO (smin2)) +
count (NULLIFZERO (inte2)) +
count (NULLIFZERO (lint2)) +
count (NULLIFZERO (nume2)) +
count (NULLIFZERO (deci2)) +
count (NULLIFZERO (pict2)) +
count (NULLIFZERO (flot2)) +
count (NULLIFZERO (real2)) +
count (NULLIFZERO (dblp2))
)
from niz000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz070')
    
    # mode_1: error 8411
    stmt = """select	NULLIFZERO
(
max (NULLIFZERO (smin1)) +
max (NULLIFZERO (inte1)) +
max (NULLIFZERO (lint1)) +
max (NULLIFZERO (nume3)) +
max (NULLIFZERO (deci3)) +
max (NULLIFZERO (pict3)) +
max (NULLIFZERO (flot1)) +
max (NULLIFZERO (real1)) +
max (NULLIFZERO (dblp1))
)
from niz000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz071')
    
    # mode_1: error 8411
    stmt = """select	NULLIFZERO
(
min (NULLIFZERO (smin2)) +
min (NULLIFZERO (inte2)) +
min (NULLIFZERO (lint2)) +
min (NULLIFZERO (nume4)) +
min (NULLIFZERO (deci2)) +
min (NULLIFZERO (pict4)) +
min (NULLIFZERO (flot2)) +
min (NULLIFZERO (real2)) +
min (NULLIFZERO (dblp2))
)
from niz000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz072')
    
    stmt = """select	NULLIFZERO
(
stddev (NULLIFZERO (smin1)) +
stddev (NULLIFZERO (inte2)) +
stddev (NULLIFZERO (lint1)) +
stddev (NULLIFZERO (nume2)) +
stddev (NULLIFZERO (deci1)) +
stddev (NULLIFZERO (pict2)) +
stddev (NULLIFZERO (flot1)) +
stddev (NULLIFZERO (real2)) +
stddev (NULLIFZERO (dblp1))
)
from niz000 
where seqno not in (4, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz073')
    
    stmt = """select	NULLIFZERO
(
sum (NULLIFZERO (smin2)) +
sum (NULLIFZERO (inte1)) +
sum (NULLIFZERO (lint2)) +
sum (NULLIFZERO (nume1)) +
sum (NULLIFZERO (deci2)) +
sum (NULLIFZERO (pict1)) +
sum (NULLIFZERO (flot2)) +
sum (NULLIFZERO (real1)) +
sum (NULLIFZERO (dblp2))
)
from niz000 
where seqno not in (4, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz074')
    
    stmt = """select	NULLIFZERO
(
variance (NULLIFZERO (smin1)) +
variance (NULLIFZERO (inte2)) +
variance (NULLIFZERO (lint1)) +
variance (NULLIFZERO (nume2)) +
variance (NULLIFZERO (deci1)) +
variance (NULLIFZERO (pict2)) +
variance (NULLIFZERO (flot1)) +
variance (NULLIFZERO (real2)) +
variance (NULLIFZERO (dblp1))
)
from niz000 
where seqno not in (4, 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz075')
    
    stmt = """select	ascii (char1),
NULLIFZERO (ascii (char1))
from niz002 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz076')
    
    stmt = """select	char_length (char1),
NULLIFZERO (char_length (char1)),
char_length (char2),
NULLIFZERO (char_length (char2))
from niz002 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz077')
    
    stmt = """select	code_value (char1),
NULLIFZERO (code_value (char1)),
code_value (char2),
NULLIFZERO (code_value (char2))
from niz002 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz078')
    
    stmt = """select	octet_length (char1),
NULLIFZERO (octet_length (char1)),
octet_length (char2),
NULLIFZERO (octet_length (char2))
from niz002 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz079')
    
    stmt = """select	position ('A' IN upper (char1)),
NULLIFZERO (position ('A' IN upper (char1))),
position (_ucs2'A' IN upper(char2)),
NULLIFZERO (position (_ucs2'A' IN upper (char2)))
from niz002 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz080')
    
    stmt = """select	date1,
NULLIFZERO (day (date1) - 7),
tims1,
NULLIFZERO (day (tims1) - 5)
from niz002 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz081')
    
    stmt = """select	date1,
NULLIFZERO (dayofmonth (date1) - 7),
tims1,
NULLIFZERO (dayofmonth (tims1) - 5)
from niz002 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz082')
    
    stmt = """select	date1,
NULLIFZERO (dayofweek (date1) - 1),
tims1,
NULLIFZERO (dayofweek (tims1) - 1)
from niz002 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz083')
    
    stmt = """select	date1,
cast ((NULLIFZERO (dayofyear (date1) - 71)) as smallint),
tims1,
cast ((NULLIFZERO (dayofyear (tims1) - 121)) as smallint)
from niz002 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz084')
    
    stmt = """select	date1,
NULLIFZERO (extract (year from date1) - 2005),
tims1,
NULLIFZERO (extract (year from tims1) - 2005)
from niz002 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz085')
    
    stmt = """select	tims1,
NULLIFZERO (extract (hour from tims1)),
NULLIFZERO (extract (minute from tims1)),
NULLIFZERO (extract (second from tims1))
from niz002 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz086')
    
    stmt = """select	tims1,
NULLIFZERO (hour (tims1))
from niz002 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz087')
    
    stmt = """select	date1,
NULLIFZERO (juliantimestamp (date1) - 212013720000000000)
from niz002 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz088')
    
    stmt = """select	tims1,
NULLIFZERO (juliantimestamp (tims1) - 212013693600000000)
from niz002 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz089')
    
    stmt = """select	tims1,
NULLIFZERO (minute (tims1))
from niz002 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz090')
    
    stmt = """select	date1,
NULLIFZERO (month (date1) - 3),
tims1,
NULLIFZERO (month (tims1) - 1)
from niz002 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz091')
    
    stmt = """select	date1,
NULLIFZERO (quarter (date1) - 3),
tims1,
NULLIFZERO (quarter (tims1) - 1)
from niz002 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz092')
    
    stmt = """select	tims1,
NULLIFZERO (second (tims1))
from niz002 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz093')
    
    stmt = """select	date1,
cast ((NULLIFZERO (week (date1) - 11)) as smallint),
tims1,
cast ((NULLIFZERO (week (tims1) - 2)) as smallint)
from niz002 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz094')
    
    stmt = """select	date1,
NULLIFZERO (year (date1) - 2001),
tims1,
NULLIFZERO (year (tims1) - 2001)
from niz002 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz095')
    
    # ==================   Begin Test Case Header   ==================
    #
    #  Test case name:     NIZ004
    #  Description	: Tests for function NULLIFZERO
    #
    #	Syntax		: NULLIFZERO(<operand>)
    #   	Semantics	:
    #		if <operand> is equal to zero, then return NULL.
    #		if <operand> is not equal to zero, then return <operand>
    #		<operand> must be one of the numeric datatypes
    #			(decimal, floats, int, etc..).
    #		Same as CASE WHEN <operand> <> 0
    #			then <operand>
    #			ELSE NULL END
    #
    #	Examples	:
    #		select NULLIFZERO(1) from (values(1)) x(a);
    #			-- should return 1
    #		select NULLIFZERO(0) from (values(1)) x(a);
    #			-- should return NULL (?)
    #
    #	This is a positive test involving interaction with other features
    #
    #  Revision History:
    #      05/05/06       Created.
    #
    # =================== End Test Case Header  ===================
    
    _testmgr.testcase_end(desc)

def test004(desc="""N04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """select	inte2,
NULLIFZERO (inte2 - (	select	seqno
from niz002 
where	char1 in ('HP')))
from niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz096')
    
    stmt = """select	o.seqno,
NULLIFZERO ((	select	inte1
from niz001 i
where	o.seqno = i.seqno))
from niz000 o
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz097')
    
    stmt = """select	inte1
from niz000 
where	NULLIFZERO (inte1) is NULL
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz098')
    
    stmt = """select	inte1
from niz000 
where	NULLIFZERO (inte1) is not NULL
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz099')
    
    stmt = """select	NULLIFZERO (cnt)
from niz_vw_001;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz100')
    
    stmt = """select	niz_avg
from niz_vw_001;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz101')
    
    stmt = """select	count (*)
from niz_vw_003;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz102')
    
    stmt = """select	n0sq,
n0s1 + n1f2 + n0dp1,
NULLIFZERO (n0s1 + n1f2 + n0dp1)
from niz_vw_003 
order by n0sq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz103')
    
    stmt = """select	a.seqno,
count (*)
from niz000 a
cross join
 niz001 b
group by a.seqno
having NULLIFZERO (a.seqno) > 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz104')
    
    stmt = """select	a.seqno,
NULLIFZERO (count (a.inte1))
from niz000 a
join
 niz000 b
on a.seqno = b.seqno
join
 niz002 c
on b.seqno = c.seqno
group by a.seqno
having count (*) >= 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz105')
    
    stmt = """select	a.seqno
from niz000 a
join
 niz001 b
on a.seqno = NULLIFZERO (b.seqno)
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz106')
    
    # Modify query. Same as niz106
    stmt = """select	a.seqno,
b.inte1
from niz000 a
join
 niz001 b
on a.seqno = NULLIFZERO (b.seqno)
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz107')
    
    stmt = """select	seqno,
inte1
from niz000 
where	seqno in (	select	NULLIFZERO (inte1)
from niz000 
where	seqno <= 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz108')
    
    stmt = """select	seqno,
inte1
from niz000 
where	seqno in (	select	inte1
from niz000 
where	NULLIFZERO (inte1) is not NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz109')
    
    stmt = """select	seqno,
inte1
from niz000 a
where	exists (select	inte1
from niz001 b
where	NULLIFZERO (a.seqno) = b.seqno)
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz110')
    
    stmt = """select	seqno,
NULLIFZERO (inte1)
from niz000     

union    

select	seqno,
NULLIFZERO (inte2)
from niz001 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz111')
    
    stmt = """set param ?val_z 0;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?val_nz 1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select	a.inte1
from niz000 a
left outer join
 niz001 b
on a.seqno = b.seqno
where	a.inte1 in (NULLIFZERO (?val_z), NULLIFZERO (?val_nz));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz112')
    
    stmt = """select	seqno,
inte1
from niz000 
where	seqno = (	select	NULLIFZERO (inte1)
from niz000 
where	seqno = 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz113')
    
    stmt = """select	inte1,
NULLIFZERO (smin1)
from niz000 
where	inte1 between smin1 and 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz114')
    
    stmt = """insert
into niz000 (seqno, inte1, smin1, lint1,
nume1, deci1, pict1, flot1,
real1, dblp1)
values	(NULLIFZERO (8), NULLIFZERO (0),
NULLIFZERO (33), NULLIFZERO (12345),
12, 71, 4366, NULLIFZERO (0.7209),
NULLIFZERO (3.1415), 3.0000089);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update niz000 
set	inte1 = (	select	NULLIFZERO (inte1)
from niz001 
where	seqno = 3),
inte2 = 39393939,
dblp1 = dblp1 - (	select	NULLIFZERO (smin1)
from niz001 
where seqno = 5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 8)
    
    stmt = """delete
from niz000 
where	seqno = (	select	NULLIFZERO (max (seqno)) + 3
from niz001);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select	count (*)
from niz000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz115')
    
    stmt = """begin 	work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert
into niz000 values
(
8,    

NULLIFZERO (5 + 5 - 10),
5058,    

-1073218,
1074,    

462348416,
-255116,    

4834915,
59962.443,
4957958598,
NULLIFZERO (381.731740490000250),    

68,
61965178354,
300380.231001835,    

4197117958,
0.29,
-54427822.44480,
426.843503,    

-3.31318885280000000E-001,
1.95643640470999968E-002,    

4.61149992608438720E+018,
-4.15749993640929472E-001,    

1.55610634902000000E+002,
NULLIFZERO (5.00000204380000128E+001)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into niz000 (seqno) values (9);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select	count (*)
from niz000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz116')
    
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select	count (*)
from niz000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz117')
    
    stmt = """delete
from niz000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 7)
    
    stmt = """insert into niz000 
(
seqno,
smin1,
smin2,
inte1,
inte2,
lint1,
lint2,
nume1,
nume2,
nume3,
nume4,
deci1,
deci2,
deci3,
pict1,
pict2,
pict3,
pict4,
flot1,
flot2,
real1,
real2,
dblp1,
dblp2
)
(
select	seqno,
smin1,
smin2,
inte1,
inte2,
lint1,
lint2,
nume1,
nume2,
nume3,
nume4,
deci1,
deci2,
deci3,
pict1,
pict2,
pict3,
pict4,
flot1,
flot2,
real1,
real2,
dblp1,
dblp2
from    temp_niz000 
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 7)
    
    # mode_1: error 8411
    stmt = """select	abs (smin1 + smin2) +
abs (inte1 + inte2) +
abs (lint1 + lint2) +
abs (nume1 + nume2 + nume3 + nume4) +
abs (deci1 + deci2 + deci3) +
abs (pict1 + pict2 + pict3 + pict4) +
abs (flot1 + flot2) +
abs (real1 + real2) +
abs (dblp1 + dblp2),    

NULLIFZERO
(
abs (smin1 + smin2) +
abs (inte1 + inte2) +
abs (lint1 + lint2) +
abs (nume1 + nume2 + nume3 + nume4) +
abs (deci1 + deci2 + deci3) +
abs (pict1 + pict2 + pict3 + pict4) +
abs (flot1 + flot2) +
abs (real1 + real2) +
abs (dblp1 + dblp2)
)
from niz000 
where	seqno <> 5
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz118')
    
    # mode_1: error 8411
    stmt = """select  floor (smin1 + smin2) +
floor (inte1 + inte2) +
floor (lint1 + lint2) +
floor (nume1 + nume2 + nume3 + nume4) +
floor (deci1 + deci2 + deci3) +
floor (pict1 + pict2 + pict3 + pict4) +
floor (flot1 + flot2) +
floor (real1 + real2) +
floor (dblp1 + dblp2),    

NULLIFZERO
(
floor (smin1 + smin2) +
floor (inte1 + inte2) +
floor (lint1 + lint2) +
floor (nume1 + nume2 + nume3 + nume4) +
floor (deci1 + deci2 + deci3) +
floor (pict1 + pict2 + pict3 + pict4) +
floor (flot1 + flot2) +
floor (real1 + real2) +
floor (dblp1 + dblp2)
)
from    niz000 
where   seqno not in (5)
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz119')
    
    # mode_1: error 8411
    stmt = """select  ceiling (smin1 + smin2) +
ceiling (inte1 + inte2) +
ceiling (lint1 + lint2) +
ceiling (nume1 + nume2 + nume3 + nume4) +
ceiling (deci1 + deci2 + deci3) +
ceiling (pict1 + pict2 + pict3 + pict4) +
ceiling (flot1 + flot2) +
ceiling (real1 + real2) +
ceiling (dblp1 + dblp2),    

NULLIFZERO
(
ceiling (smin1 + smin2) +
ceiling (inte1 + inte2) +
ceiling (lint1 + lint2) +
ceiling (nume1 + nume2 + nume3 + nume4) +
ceiling (deci1 + deci2 + deci3) +
ceiling (pict1 + pict2 + pict3 + pict4) +
ceiling (flot1 + flot2) +
ceiling (real1 + real2) +
ceiling (dblp1 + dblp2)
)
from    niz000 
where   seqno not in (5)
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz120')
    
    # mode_1: error 8411
    stmt = """select  sqrt (smin1 + smin2) +
sqrt (inte1 + inte2) +
sqrt (lint1 + lint2) +
sqrt (nume1 + nume2 + nume3 + nume4) +
sqrt (deci1 + deci2 + deci3) +
sqrt (pict1 + pict2 + pict3 + pict4) +
sqrt (flot1 + flot2) +
sqrt (real1 + real2) +
sqrt (dblp1 + dblp2),    

NULLIFZERO
(
sqrt (smin1 + smin2) +
sqrt (inte1 + inte2) +
sqrt (lint1 + lint2) +
sqrt (nume1 + nume2 + nume3 + nume4) +
sqrt (deci1 + deci2 + deci3) +
sqrt (pict1 + pict2 + pict3 + pict4) +
sqrt (flot1 + flot2) +
sqrt (real1 + real2) +
sqrt (dblp1 + dblp2)
)
from    niz000 
where   seqno not in (4, 6, 7)
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz121')
    
    stmt = """select  exp (smin1 + smin2) +
exp (inte1 + inte2) +
exp (lint1 + lint2) +
exp (nume1 + nume2 + nume3 + nume4) +
exp (deci1 + deci2 + deci3) +
exp (pict1 + pict2 + pict3 + pict4) +
exp (flot1 + flot2) +
exp (real1 + real2) +
exp (dblp1 + dblp2),    

NULLIFZERO
(
exp (smin1 + smin2) +
exp (inte1 + inte2) +
exp (lint1 + lint2) +
exp (nume1 + nume2 + nume3 + nume4) +
exp (deci1 + deci2 + deci3) +
exp (pict1 + pict2 + pict3 + pict4) +
exp (flot1 + flot2) +
exp (real1 + real2) +
exp (dblp1 + dblp2)
)
from    niz000 
where	seqno not in (4, 5, 6, 7)
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz122')
    
    # mode_1: error 8411
    stmt = """select  diff1 (smin1 + smin2) +
diff1 (inte1 + inte2) +
diff1 (lint1 + lint2) +
diff1 (nume1 + nume2 + nume3 + nume4) +
diff1 (deci1 + deci2 + deci3) +
diff1 (pict1 + pict2 + pict3 + pict4) +
diff1 (flot1 + flot2) +
diff1 (real1 + real2) +
diff1 (dblp1 + dblp2),    

NULLIFZERO
(
diff1 (smin1 + smin2) +
diff1 (inte1 + inte2) +
diff1 (lint1 + lint2) +
diff1 (nume1 + nume2 + nume3 + nume4) +
diff1 (deci1 + deci2 + deci3) +
diff1 (pict1 + pict2 + pict3 + pict4) +
diff1 (flot1 + flot2) +
diff1 (real1 + real2) +
diff1 (dblp1 + dblp2)
)
from    niz000 
where	seqno <> 5
sequence by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz123')
    
    # mode_1: error 8411
    stmt = """select  diff2 (smin1 + smin2) +
diff2 (inte1 + inte2) +
diff2 (lint1 + lint2) +
diff2 (nume1 + nume2 + nume3 + nume4) +
diff2 (deci1 + deci2 + deci3) +
diff2 (pict1 + pict2 + pict3 + pict4) +
diff2 (flot1 + flot2) +
diff2 (real1 + real2) +
diff2 (dblp1 + dblp2),    

NULLIFZERO
(
diff2 (smin1 + smin2) +
diff2 (inte1 + inte2) +
diff2 (lint1 + lint2) +
diff2 (nume1 + nume2 + nume3 + nume4) +
diff2 (deci1 + deci2 + deci3) +
diff2 (pict1 + pict2 + pict3 + pict4) +
diff2 (flot1 + flot2) +
diff2 (real1 + real2) +
diff2 (dblp1 + dblp2)
)
from    niz000 
where	seqno <> 5
sequence by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz124')
    
    #SAP
    
    stmt = """select	inte1,
movingavg (inte1, 3),
NULLIFZERO (movingavg (inte1, 3))
from niz000 
sequence by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz125')
    
    stmt = """select	inte1,
movingcount (NULLIFZERO (inte1), 3),
NULLIFZERO (movingcount (NULLIFZERO (inte1), 3))
from niz000 
sequence by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz126')
    
    stmt = """select	inte1,
movingmax (inte1, 8),
NULLIFZERO (movingmax (inte1, 8))
from niz000 
sequence by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz127')
    
    stmt = """insert into niz000 (seqno, inte1) values (8, 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into niz000 (seqno, inte1) values (9, 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into niz000 (seqno, inte1) values (10, 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select	inte1,
movingmin (inte1, 2),
NULLIFZERO (movingmin (inte1, 2))
from niz000 
sequence by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz128')
    
    stmt = """select	inte1,
movingstddev (inte1, 2),
NULLIFZERO (movingstddev (inte1, 2))
from niz000 
sequence by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz129')
    
    stmt = """select	nume3,
movingsum (nume3, 2),
NULLIFZERO (movingsum (nume3, 2))
from niz000 
sequence by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz130')
    
    stmt = """select	flot1,
movingvariance (flot1, 2),
NULLIFZERO (movingvariance (flot1, 2))
from niz000 
sequence by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz131')
    
    stmt = """select	dblp1,
offset (dblp1, 1),
NULLIFZERO (offset (dblp1, 1))
from niz000 
sequence by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz132')
    
    stmt = """select	real1,
runningavg (real1),
NULLIFZERO (runningavg (real1))
from niz000 
sequence by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz133')
    
    #SAP
    
    # mode_1: error 8411
    stmt = """select	lint1,
runningavg (lint1),
NULLIFZERO (runningavg (lint1))
from niz000 
sequence by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz134')
    
    stmt = """select	pict3,
runningcount (pict3),
NULLIFZERO (runningcount (pict3))
from niz000 
sequence by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz135')
    
    stmt = """select	pict1,
runningmax (pict1),
NULLIFZERO (runningmax (pict1))
from niz000 
sequence by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz136')
    
    stmt = """select	flot2,
runningmin (flot2),
NULLIFZERO (runningmin (flot2))
from niz000 
sequence by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz137')
    
    stmt = """select	dblp2,
runningstddev (dblp2),
NULLIFZERO (runningstddev (dblp2))
from niz000 
sequence by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz138')
    
    stmt = """select	smin2,
runningsum (smin2),
NULLIFZERO (runningsum (smin2))
from niz000 
sequence by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz139')
    
    stmt = """select	lint2,
runningvariance (lint2),
NULLIFZERO (runningvariance (lint2))
from niz000 
sequence by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz140')
    
    stmt = """select	inte1,
runningvariance (inte1),
NULLIFZERO (runningvariance (inte1))
from niz000 
sequence by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz141')
    
    stmt = """select	inte1,
rows since (inte1 = 1),
NULLIFZERO (rows since (inte1 = 1))
from niz000 
sequence by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz142')
    
    stmt = """select	inte1,
NULLIFZERO (NVL (inte1, 3))
from niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz143')
    
    stmt = """select	inte1,
inte2,
NULLIFZERO (NULLIFZERO (NULLIFZERO (NULLIFZERO (NULLIFZERO (inte1))))),
NVL (NULLIFZERO (inte1), inte2)
from niz000 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'niz144')
    
    # ==================   Begin Test Case Header   ==================
    #
    #  Test case name:     NIZ005
    #  Description	: Tests for function NULLIFZERO
    #
    #	Syntax		: NULLIFZERO(<operand>)
    #   	Semantics	:
    #		if <operand> is equal to zero, then return NULL.
    #		if <operand> is not equal to zero, then return <operand>
    #		<operand> must be one of the numeric datatypes
    #			(decimal, floats, int, etc..).
    #		Same as CASE WHEN <operand> <> 0
    #			then <operand>
    #			ELSE NULL END
    #
    #	Examples	:
    #		select NULLIFZERO(1) from (values(1)) x(a);
    #			-- should return 1
    #		select NULLIFZERO(0) from (values(1)) x(a);
    #			-- should return NULL (?)
    #
    #	This is a negative test
    #
    #  Revision History:
    #      05/05/06       Created.
    #
    # =================== End Test Case Header  ===================
    
    _testmgr.testcase_end(desc)

def test005(desc="""N05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """select	NULLIZERO (seqno),
char1
from niz002 
group by NULLIFZERO (seqno), char1
having upper(char1) in ('HP', 'TANDEM', 'RTSD');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """select	char1,
NULLIFZERO (trim(char1))
from niz002 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select	seqno,
NULLIFZERO (inte1)
from niz000     

intersect    

select	seqno,
NULLIFZERO (inte2)
from niz001 
order by seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3022')
    
    stmt = """select	a.inte1
from niz000 a
right outer join
 niz001 b
on a.seqno = b.seqno
where	a.inte1 = any (NULLIFZERO (?val_z), 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select	NULLIFZERO (inte1, inte2)
from niz000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """showcontrol all;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

