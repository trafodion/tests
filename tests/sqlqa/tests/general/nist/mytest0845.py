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
    
    stmt = """select ADD_MONTHS( cast('2005-03-31' as DATE), 0) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845a""")
    stmt = """select ADD_MONTHS( cast('2005-03-31' as date), 1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845b""")
    stmt = """select ADD_MONTHS( cast('2005-03-31' as date), 1, 0) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845c""")
    stmt = """select ADD_MONTHS( cast('2005-03-31' as date), 1, 1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845d""")
    stmt = """select ADD_MONTHS( cast('2005-03-31' as date), 0, 1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845e""")
    
    stmt = """select ADD_MONTHS( DATE'2005-03-31','13') from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845f""")
    stmt = """select ADD_MONTHS( DATE'2005-03-31','13',0) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845g""")
    stmt = """select ADD_MONTHS( DATE'2005-03-31','13',1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845h""")
    stmt = """select ADD_MONTHS( DATE'2005-03-31','12') from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845i""")
    stmt = """select ADD_MONTHS( DATE'2005-03-31','12',0) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845j""")
    stmt = """select ADD_MONTHS( DATE'2005-03-31','12',1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845k""")
    stmt = """select ADD_MONTHS(DATE'2001-02-28', 0)  from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845l""")
    stmt = """select ADD_MONTHS(DATE'2001-02-28', 1)  from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845m""")
    stmt = """select ADD_MONTHS(DATE '2001-02-28', 1, 0)  from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845n""")
    stmt = """select ADD_MONTHS(DATE '2000-02-28', 1, 1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845o""")
    stmt = """select ADD_MONTHS( DATE'2001-02-28','13') from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845p""")
    stmt = """select ADD_MONTHS( DATE'2001-02-28','13',0) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845q""")
    stmt = """select ADD_MONTHS( DATE'2001-02-28','13',1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845r""")
    stmt = """select ADD_MONTHS( DATE'2001-02-28','12') from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845s""")
    stmt = """select ADD_MONTHS( DATE'2001-02-28','12',0) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845t""")
    stmt = """select ADD_MONTHS( DATE'2001-02-28','12',1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845u""")
    stmt = """select ADD_MONTHS( DATE'2004-02-29','0') from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845v""")
    stmt = """select ADD_MONTHS( DATE'2004-02-29','1') from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845w""")
    stmt = """select ADD_MONTHS( DATE'2004-02-29','1',0) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845x""")
    stmt = """select ADD_MONTHS( DATE'2004-02-29','1',1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845y""")
    stmt = """select ADD_MONTHS( DATE'2004-02-29','12') from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z""")
    stmt = """select ADD_MONTHS( DATE'2004-02-29','12',1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z1""")
    stmt = """select ADD_MONTHS( DATE'2004-02-29','12',0) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z2""")
    stmt = """select ADD_MONTHS( DATE'2004-02-29','13') from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z3""")
    stmt = """select ADD_MONTHS( DATE'2004-02-29','13',0) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z4""")
    stmt = """select ADD_MONTHS( DATE'2004-02-29','13',1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z5""")
    stmt = """select ADD_MONTHS( DATE'2004-02-29',65535,0) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z6""")
    
    # TIMESTAMT--
    
    stmt = """select ADD_MONTHS( cast('1906-03-31 10:53:07.012650' as timestamp), 0) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z7""")
    stmt = """select ADD_MONTHS( cast('1906-03-31 10:53:07.012650' as timestamp), 1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z8""")
    stmt = """select ADD_MONTHS( cast('1906-03-31 10:53:07.012650' as timestamp), 1, 0) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z9""")
    stmt = """select ADD_MONTHS( cast('1906-03-31 10:53:07.012650' as timestamp), 1, 1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z10""")
    stmt = """select ADD_MONTHS( cast('1906-03-31 10:53:07.012650' as timestamp), 0, 1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z11""")
    
    stmt = """select ADD_MONTHS( timestamp'1906-03-31 10:53:07.012650' ,'13') from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z12""")
    stmt = """select ADD_MONTHS( timestamp'1906-03-31 10:53:07.012650' ,'13',0) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z13""")
    stmt = """select ADD_MONTHS( timestamp'1906-03-31 10:53:07.012650' ,'13',1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z14""")
    
    stmt = """select ADD_MONTHS( timestamp'1906-03-31 10:53:07.012650','12') from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z15""")
    stmt = """select ADD_MONTHS( timestamp'1906-03-31 10:53:07.012650','12',0) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z16""")
    stmt = """select ADD_MONTHS( timestamp'1906-03-31 10:53:07.012650','12',1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z17""")
    stmt = """select ADD_MONTHS( timestamp'2001-02-28 10:53:07.012650', 0)  from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z18""")
    stmt = """select ADD_MONTHS( timestamp'2001-02-28 10:53:07.012650', 1)  from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z19""")
    stmt = """select ADD_MONTHS( timestamp'2001-02-28 10:53:07.012650', 1, 0)  from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z20""")
    stmt = """select ADD_MONTHS( timestamp'2001-02-28 10:53:07.012650', 1, 1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z21""")
    stmt = """select ADD_MONTHS( timestamp'2001-02-28 10:53:07.012650','13') from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z22""")
    stmt = """select ADD_MONTHS( timestamp'2001-02-28 10:53:07.012650','13',0) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z23""")
    stmt = """select ADD_MONTHS( timestamp'2001-02-28 10:53:07.012650','13',1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z24""")
    stmt = """select ADD_MONTHS( timestamp'2001-02-28 10:53:07.012650','12') from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z25""")
    stmt = """select ADD_MONTHS( timestamp'2001-02-28 10:53:07.012650','12',0) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z26""")
    stmt = """select ADD_MONTHS( timestamp'2001-02-28 10:53:07.012650','12',1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z27""")
    stmt = """select ADD_MONTHS( timestamp'2004-02-29 10:53:07.012650','0') from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z28""")
    stmt = """select ADD_MONTHS( timestamp'2004-02-29 10:53:07.012650','1') from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z29""")
    stmt = """select ADD_MONTHS( timestamp'2004-02-29 10:53:07.012650','1',0) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z30""")
    stmt = """select ADD_MONTHS( timestamp'2004-02-29 10:53:07.012650','1',1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z31""")
    stmt = """select ADD_MONTHS( timestamp'2004-02-29 10:53:07.012650','12') from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z32""")
    stmt = """select ADD_MONTHS( timestamp'2004-02-29 10:53:07.012650','12',1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z33""")
    stmt = """select ADD_MONTHS( timestamp'2004-02-29 10:53:07.012650','12',0) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z34""")
    stmt = """select ADD_MONTHS( timestamp'2004-02-29 10:53:07.012650','13') from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z35""")
    stmt = """select ADD_MONTHS( timestamp'2004-02-29 10:53:07.012650','13',0) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z36""")
    stmt = """select ADD_MONTHS( timestamp'2004-02-29 10:53:07.012650','13',1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z37""")
    stmt = """select ADD_MONTHS( timestamp'2004-02-29 10:53:07.012650',65535,0) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z38""")
    
    #--Tables Values select update tables---
    stmt = """UPDATE dt_mth_d
SET CLDR_MTH_STRT_DT = ADD_MONTHS ( CLDR_MTH_STRT_DT, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select CLDR_MTH_STRT_DT from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z40""")
    
    stmt = """UPDATE dt_mth_d
SET CLDR_MTH_STRT_DT = ADD_MONTHS ( CLDR_MTH_STRT_DT, -1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select CLDR_MTH_STRT_DT from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z42""")
    stmt = """UPDATE dt_mth_d
SET CLDR_MTH_STRT_DT = ADD_MONTHS ( CLDR_MTH_STRT_DT, -13);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select CLDR_MTH_STRT_DT from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z44""")
    stmt = """UPDATE dt_mth_d
SET CLDR_MTH_STRT_DT = ADD_MONTHS ( CLDR_MTH_STRT_DT, -12);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select CLDR_MTH_STRT_DT from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z46""")
    
    #NEgatives values
    
    # zero--
    stmt = """select ADD_MONTHS( cast('2005-03-31' as date), -0) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z47""")
    stmt = """select ADD_MONTHS( cast('2005-03-31' as date), -1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z48""")
    stmt = """select ADD_MONTHS( cast('2005-03-31' as date), -1, 0) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z49""")
    stmt = """select ADD_MONTHS( cast('2005-03-31' as date), -1, 1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z50""")
    stmt = """select ADD_MONTHS( cast('2005-03-31' as date), -0, 1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z51""")
    stmt = """select ADD_MONTHS( DATE'2005-03-31',-13) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z52""")
    stmt = """select ADD_MONTHS( DATE'2005-03-31',-13,0) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z53""")
    stmt = """select ADD_MONTHS( DATE'2005-03-31',-13,1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z54""")
    stmt = """select ADD_MONTHS( DATE'2005-03-31',-12) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z55""")
    stmt = """select ADD_MONTHS( DATE'2005-03-31',-12,0) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z56""")
    stmt = """select ADD_MONTHS( DATE'2005-03-31',-12,1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z57""")
    stmt = """select ADD_MONTHS( DATE'2001-02-28', -0)  from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z58""")
    stmt = """select ADD_MONTHS( DATE'2001-02-28', -1)  from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z59""")
    stmt = """select ADD_MONTHS( DATE '2001-02-28', -1, 0)  from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z60""")
    stmt = """select ADD_MONTHS( DATE '2000-02-28', -1, 1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z61""")
    stmt = """select ADD_MONTHS( DATE'2001-02-28',-13) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z62""")
    stmt = """select ADD_MONTHS( DATE'2001-02-28',-13,0) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z63""")
    stmt = """select ADD_MONTHS( DATE'2001-02-28',-13,1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z64""")
    stmt = """select ADD_MONTHS( DATE'2001-02-28',-12) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z65""")
    stmt = """select ADD_MONTHS( DATE'2001-02-28',-12,0) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z66""")
    stmt = """select ADD_MONTHS( DATE'2001-02-28',-12,1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z67""")
    stmt = """select ADD_MONTHS( DATE'2004-02-29',-0) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z68""")
    stmt = """select ADD_MONTHS( DATE'2004-02-29',-1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z69""")
    stmt = """select ADD_MONTHS( DATE'2004-02-29',-1,0) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z70""")
    stmt = """select ADD_MONTHS( DATE'2004-02-29',-1,1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z71""")
    stmt = """select ADD_MONTHS( DATE'2004-02-29',-12) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z72""")
    stmt = """select ADD_MONTHS( DATE'2004-02-29',-12,1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z73""")
    stmt = """select ADD_MONTHS( DATE'2004-02-29',-12,0) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z74""")
    stmt = """select ADD_MONTHS( DATE'2004-02-29',-13) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z75""")
    stmt = """select ADD_MONTHS( DATE'2004-02-29',-13,0) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z76""")
    stmt = """select ADD_MONTHS( DATE'2004-02-29',-13,1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z77""")
    stmt = """select ADD_MONTHS( DATE'2004-02-29',-65535,0) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8416')
    
    # TIMESTAMT--
    stmt = """select ADD_MONTHS( timestamp'1906-03-31 10:53:07.012650',-13) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z79""")
    stmt = """select ADD_MONTHS( timestamp'1906-03-31 10:53:07.012650',-13,0) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z80""")
    stmt = """select ADD_MONTHS( timestamp'1906-03-31 10:53:07.012650',-13,1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z81""")
    stmt = """select ADD_MONTHS( timestamp'1906-03-31 10:53:07.012650',-12) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z82""")
    stmt = """select ADD_MONTHS( timestamp'1906-03-31 10:53:07.012650',-12,0) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z83""")
    stmt = """select ADD_MONTHS( timestamp'1906-03-31 10:53:07.012650',-12,1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z84""")
    stmt = """select ADD_MONTHS(timestamp'2001-02-28 10:53:07.012650', -0)  from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z85""")
    stmt = """select ADD_MONTHS(timestamp'2001-02-28 10:53:07.012650', -1)  from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z86""")
    stmt = """select ADD_MONTHS(timestamp'2001-02-28 10:53:07.012650', -1, 0)  from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z87""")
    stmt = """select ADD_MONTHS(timestamp'2001-02-28 10:53:07.012650', -1, 1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z88""")
    
    stmt = """select ADD_MONTHS( timestamp'2001-02-28 10:53:07.012650',-13) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z89""")
    stmt = """select ADD_MONTHS( timestamp'2001-02-28 10:53:07.012650',-13,0) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z90""")
    stmt = """select ADD_MONTHS( timestamp'2001-02-28 10:53:07.012650',-13,1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z91""")
    stmt = """select ADD_MONTHS( timestamp'2001-02-28 10:53:07.012650',-12) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z92""")
    stmt = """select ADD_MONTHS( timestamp'2001-02-28 10:53:07.012650',-12,0) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z93""")
    stmt = """select ADD_MONTHS( timestamp'2001-02-28 10:53:07.012650',-12,1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z94""")
    stmt = """select ADD_MONTHS( timestamp'2004-02-29 10:53:07.012650',-0) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z95""")
    stmt = """select ADD_MONTHS( timestamp'2004-02-29 10:53:07.012650',-1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z96""")
    stmt = """select ADD_MONTHS( timestamp'2004-02-29 10:53:07.012650',-1,0) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z97""")
    stmt = """select ADD_MONTHS( timestamp'2004-02-29 10:53:07.012650',-1,1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z98""")
    stmt = """select ADD_MONTHS( timestamp'2004-02-29 10:53:07.012650',-12) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z99""")
    stmt = """select ADD_MONTHS( timestamp'2004-02-29 10:53:07.012650',-12,1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z100""")
    stmt = """select ADD_MONTHS( timestamp'2004-02-29 10:53:07.012650',-12,0) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z101""")
    stmt = """select ADD_MONTHS( timestamp'2004-02-29 10:53:07.012650',-13) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z102""")
    
    stmt = """select ADD_MONTHS( timestamp'2004-02-29 10:53:07.012650',-13,0) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z103""")
    stmt = """select ADD_MONTHS( timestamp'2004-02-29 10:53:07.012650',-13,1) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0845.exp""", """test0845z104""")
    stmt = """select ADD_MONTHS( timestamp'2004-02-29 10:53:07.012650',-65535,0) from dt_mth_d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8416')
    
    # END TEST >>> 0845 <<< END TEST
