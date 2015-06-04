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

# TEST:0246 FIPS sizing - 100 values in INSERT!
# FIPS sizing TEST

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """DELETE FROM T100;"""
    output = _dci.cmdexec(stmt)
    # Making sure the table is empty
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # setup
    stmt = """INSERT INTO T100
VALUES('ZA','ZB','CA','ZC','ZD','AA','ZE','ZF','BA','ZG',
'YA','YB','CB','YC','YD','AB','YE','YF','BB','YG',
'XA','XB','CC','XC','XD','AC','XE','XF','BC','XG',
'UA','UB','CD','UC','UD','AD','UE','UF','BD','UG',
'VA','VB','CE','VC','VD','AE','VE','VF','BE','VG',
'WA','WB','CF','WC','WD','AF','WE','WF','BF','WG',
'LA','LB','CG','LC','LD','AG','LE','LF','BG','LG',
'MA','MB','CH','MC','MD','AH','ME','MF','BH','MG',
'NA','NB','CI','NC','ND','AI','NE','NF','BI','NG',
'OA','OB','CJ','OC','OD','AJ','OE','OF','BJ','OG');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0246 If 1 row is inserted?
    
    stmt = """SELECT C6, C16, C26, C36, C46, C56, C66, C76, C86, C96, C100
FROM VWT100
WHERE C1 = 'ZA' AND C2 = 'ZB';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0246.exp""", """s1""")
    # PASS:0246 If C6  = 'AA', C16 = 'AB', C26  = 'AC', C36 = 'AD' ?
    # PASS:0246 If C46 = 'AE', C56 = 'AF', C66  = 'AG', C76 = 'AH' ?
    # PASS:0246 If C86 = 'AI', C96 = 'AJ', C100 = 'OG' ?
    
    # restore
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select count (*) from VWT100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0246.exp""", """s2""")
    # pass if count = 0
    
    # END TEST >>> 0246 <<< END TEST
    
