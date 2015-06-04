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

# TEST:0247 FIPS sizing - 20 values in update SET clause!
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
    _dci.expect_deleted_msg(output)
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
'MA','MB','CH','MC','MD','AH','AE','AF','BH','BG',
'NA','NB','CI','NC','ND','AI','NE','NF','BI','NG',
'OA','OB','CJ','OC','OD','AJ','OE','OF','BJ','OG');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0247 If 1 row is inserted?
    
    stmt = """UPDATE T100
SET C5 = 'BA', C10 = 'ZP', C15 = 'BB', C20 = 'YP', C25 = 'BC',
C30 = 'XP', C35 = 'BD', C40 = 'UP', C45 = 'BE', C50 = 'VP',
C55 = 'BF', C60 = 'WP', C65 = 'BG', C70 = 'LP', C75 = 'BH',
C80 = 'MP', C85 = 'BI', C90 = 'NP', C95 = 'BJ', C100 = 'OP';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    # PASS:0247 If 1 row is updated ?
    
    stmt = """SELECT C5, C20, C35, C40, C55, C60, C75, C80, C90, C95, C100
FROM VWT100
WHERE C1 = 'ZA' AND C2 = 'ZB';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0247.exp""", """s1""")
    # PASS:0247 If C5  = 'BA', C35  = 'BD', C55 = 'BF', C75 = 'BH' ?
    # PASS:0247 If C90 = 'NP', C100 = 'OP'?
    
    # restore
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select count (*) from VWT100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0247.exp""", """s2""")
    # pass if count = 0
    
    # END TEST >>> 0247 <<< END TEST
    
