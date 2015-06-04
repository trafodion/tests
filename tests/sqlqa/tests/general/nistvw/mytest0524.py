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
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """delete from T100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    stmt = """insert into T100 VALUES ('00', '01', '02',
'03', '04', '05', '06', '07', '08', '09', '0a', '0b', '0c',
'0d', '0e', '0f', '10', '11', '12', '13', '14', '15', '16',
'17', '18', '19', '1a', '1b', '1c', '1d', '1e', '1f', '20',
'21', '22', '23', '24', '25', '26', '27', '28', '29', '2a',
'2b', '2c', '2d', '2e', '2f', '30', '31', '32', '33', '34',
'35', '36', '37', '38', '39', '3a', '3b', '3c', '3d', '3e',
'3f', '40', '41', '42', '43', '44', '45', '46', '47', '48',
'49', '4a', '4b', '4c', '4d', '4e', '4f', '50', '51', '52',
'53', '54', '55', '56', '57', '58', '59', '5a', '5b', '5c',
'5d', '5e', '5f', '60', '61', '62', '63');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0524a If 1 row is inserted?
    
    stmt = """SELECT
C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, C13, C14,
C15, C16, C17, C18, C19, C20, C21, C22, C23, C24, C25, C26,
C27, C28, C29, C30, C31, C32, C33, C34, C35, C36, C37, C38,
C39, C40, C41, C42, C43, C44, C45, C46, C47, C48, C49, C50,
C51, C52, C53, C54, C55, C56, C57, C58, C59, C60, C61, C62,
C63, C64, C65, C66, C67, C68, C69, C70, C71, C72, C73, C74,
C75, C76, C77, C78, C79, C80, C81, C82, C83, C84, C85, C86,
C87, C88, C89, C90, C91, C92, C93, C94, C95, C96, C97, C98,
C99, C100
from VWT100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0524.exp""", """s1""")
    # PASS:0524a If 1 row selected?
    # PASS:0524a AND C1 is '00'?
    # PASS:0524a AND C50 is '31'?
    # PASS:0524a AND C67 is '42'?
    # PASS:0524a AND C100 is '63'?
    
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select count (*) from T100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0524.exp""", """s2""")
    # pass if count = 0
    
    # END TEST >>> 0524a <<< END TEST
    
