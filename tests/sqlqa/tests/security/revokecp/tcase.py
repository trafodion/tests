# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2015 Hewlett-Packard Development Company, L.P.
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
import defs
import basic_defs
import unittest
import time

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


def testa01(desc="""priv_name below max"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """unregister user qa902_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120_____128;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """unregister user qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127;"""
    output = _dci.cmdexec(stmt)

    stmt='register component users1;'
    output = _dci.cmdexec(stmt)	

    stmt = """create component privilege created as \'cr\' on users1;"""
    output = _dci.cmdexec(stmt)

    stmt = """create component privilege qa902_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120_____128 as \'qa\' on users1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create component privilege qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127 as \'pa\' on users1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant component privilege created  on users1 to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant component privilege qa902_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120_____128 on users1 to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt = """grant component privilege qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127 on users1 to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt = """revoke component privilege  created  on users1 from qauser_tsang cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)	
	
    stmt = """revoke component privilege qa902_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120_____128 on users1 from qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)	

    stmt = """revoke component privilege qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127 on users1 from qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)		
	
    stmt="""unregister component users1 cascade;"""
    output = _dci.cmdexec(stmt)
	
    _testmgr.testcase_end(desc)  


def testa02(desc="""priv_name blank, out of max"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return    
    
    stmt = """register component users2;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234567130;"""
    output = _dci.cmdexec(stmt)
 
    stmt = """unregister user qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456129;"""
    output = _dci.cmdexec(stmt)
 
    #blank
    stmt = """create component privilege as \'cr\' on users2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
	
    #max+n
    stmt = """create component privilege qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234567130 as \'pa\' on users2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')
	
    stmt = """create component privilege  qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456129 as \'p1\' on users2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')	
	
    stmt = """grant component privilege  on users2 to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """grant component privilege  qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234567130 on users2 to qauser_tsang;;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')
	
    stmt = """grant component privilege  qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456129 on users2 to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')	

    stmt = """revoke component privilege  on users2 from qauser_tsang cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')		
	
    stmt = """revoke component privilege qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234567130 on users2 from qauser_tsang cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')	
	
    stmt = """revoke component privilege qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456129 on users2 to qauser_tsang cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')	
	
	 
    stmt = """unregister component users2 cascade;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)  
                

def testa03(desc="""priv_name valid chars"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return    
    
    stmt = """register component users3;"""
    output = _dci.cmdexec(stmt)

    stmt = """create component privilege created as \'cr\' on users3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create component privilege updated as \'up\' on users3 detail \'update users\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create component privilege deleted as \'de\' on users3 detail \'delete users\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create component privilege adcd as \'ad\' on users3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt = """grant component privilege created on users3  to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """grant component privilege updated on users3  to qauser_sqlqaa with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """grant component privilege deleted,adcd on users3 to qauser_sqlqab ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke  component privilege created on users3 from qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)	
	
	
    stmt = """revoke component privilege updated  on users3 from qauser_sqlqaa cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)	
	
    stmt = """revoke component privilege deleted, adcd on users3 from qauser_sqlqab ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)	
    
    stmt = """unregister component users3 cascade;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)  



def testa04(desc="""priv_name invalid chars"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return  
    
    stmt = """register component users4;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create component privilege "test" as \'t\' on user4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1220')
    
    stmt = """create  component privilege  "1289-_@" as \'1\' on user4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1220')
    
    stmt = """create  component privilege  "_asdf" as \'as\' on user4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1004')
    

    stmt = """create component privilege "/test" as \'/t\' on user4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1004')
	
    stmt = """grant component privilege "1289-_@" on users4 to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1004')	
	
    stmt = """grant component privilege "_asdf"  on users4 to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1004')	

    stmt = """grant component privilege "/test"  on users4 to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1004')	

    stmt = """grant component privilege "test"  on users4 to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1004')		
	
    stmt = """revoke component privilege "test" on users4 from qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1004')		

    stmt = """revoke component privilege "1289-_@" on users4 from qauser_tsang cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1004')	

    stmt = """revoke component privilege  "_asdf"  on users4 from qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1004')	

    stmt = """revoke component privilege "/test"  on users4 from qauser_tsang cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1004')		
	
    stmt = """unregister component users4 cascade;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)  


def testa05(desc="""name below max"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return  
    
    stmt = """unregister user qa902_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120_____128;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """unregister user qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """unregister user qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345681201234127;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """register component qa902_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120_____128;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """register component qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """create component privilege created as \'cr\' on qa902_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120_____128 ;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """create component privilege updated as \'up\' on qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127 ;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """create component privilege  qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345681201234127 as \'pa\' on qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127;"""
    output = _dci.cmdexec(stmt)
	
    stmt="""grant component privilege created on qa902_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120_____128 to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt="""grant component privilege updated on qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127  to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt="""grant component privilege qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345681201234127 on qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127 to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt="""revoke component privilege created on qa902_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120_____128 from qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
		
    stmt="""revoke component privilege updated on qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127  from qauser_tsang cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt="""revoke component privilege qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345681201234127 on qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127 from qauser_tsang cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt="""unregister component qa902_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120_____128 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt="""unregister component qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127 cascade;"""
    output = _dci.cmdexec(stmt)	
	
    _testmgr.testcase_end(desc)  


def testa06(desc="""name blank, out of max"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return  
    
    stmt = """unregister user qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456129;"""
    output = _dci.cmdexec(stmt)

    stmt="""unregister user qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456789132;"""
    output = _dci.cmdexec(stmt)
	
    stmt="""register component qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456129;"""
    output = _dci.cmdexec(stmt)
	
    stmt="""register component qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456789132;"""
    output = _dci.cmdexec(stmt)	
	
    stmt = """create component privilege created as \'cr\' on ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """create component privilege updated as \'up\' on qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456129;"""
    output = _dci.cmdexec(stmt)

    stmt = """create component privilege deleted as \'de\' on qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456789132;"""
    output = _dci.cmdexec(stmt)

    
    stmt = """grant component privilege created on to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """grant component privilege updated on qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456129 to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'3118')

    stmt = """grant component privilege deleted on qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456789132 to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'3118')
	
    stmt = """revoke component privilege created on from qauser_tsang cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """revoke component privilege updated on qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456129 from qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')

    stmt = """revoke component privilege deleted on qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456789132 from qauser_tsang cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')	
	
    stmt = """unregister component  qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456129 cascade;"""
    output = _dci.cmdexec(stmt)
	
    stmt="""unregister component qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456789132;"""
    output = _dci.cmdexec(stmt)	

    _testmgr.testcase_end(desc)             
  
def testa07(desc="""name valid chars"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return  
    
    stmt = """register component AAA;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """register component abcd;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """register component A1B2;"""
    output = _dci.cmdexec(stmt)

    stmt = """create component privilege created as \'cr\' on AAA;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create component privilege updated as \'up\' on abcd; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create component privilege deleted as \'up\' on A1B2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """grant component privilege created on AAA to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """grant component privilege updated on abcd to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt = """grant component privilege deleted on A1B2 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt = """revoke component privilege created on AAA from qauser_tsang cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt = """revoke component privilege updated on abcd from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke component privilege deleted on A1B2 from  qauser_sqlqaa cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
	
        
    stmt = """unregister component AAA cascade;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """unregister component abcd cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister component A1B2 cascade;"""
    output = _dci.cmdexec(stmt)	
	
    _testmgr.testcase_end(desc)  


def testa08(desc="""name  invalid chars"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return  
    
    stmt = """register component "LMNOP-./ghij_@klmnop";"""
    output = _dci.cmdexec(stmt)
	
    stmt = """register component test;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """register component "/test/";"""
    output = _dci.cmdexec(stmt)		

    stmt = """create component privilege created as \'cr\' on "LMNOP-./ghij_@klmnop";"""
    output = _dci.cmdexec(stmt)

    stmt = """create component privilege updated as \'up\' on test;"""
    output = _dci.cmdexec(stmt)

    stmt = """create component privilege deleted as \'de\' on "/test/";"""
    output = _dci.cmdexec(stmt)
    
    stmt = """grant component privilege created on "LMNOP-./ghij_@klmnop" to qauser_sqlqaa; """
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    
    stmt = """grant component privilege updated on test to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
	
    stmt = """grant component privilege deleted on "/test/" to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')   

    stmt = """revoke component privilege created on "LMNOP-./ghij_@klmnop" from qauser_sqlqaa cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')  

    stmt = """revoke component privilege updated on test from qauser_sqlqaa cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')  

    stmt = """revoke component privilege deleted on "/test/" from qauser_tsang cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')  
    
    stmt = """unregister component "LMNOP-./ghij_@klmnop" cascade;"""
    output = _dci.cmdexec(stmt)    
    
    stmt = """unregister component test cascade;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """unregister component "/test/"  cascade;"""
    output = _dci.cmdexec(stmt)	
    
    _testmgr.testcase_end(desc)  


def testa09(desc="""grantee below max"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """unregister user qauser1;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """unregister user qauser2;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """unregister user qauser3;"""
    output = _dci.cmdexec(stmt)
	
    stmt="""unregister user qa902_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120_____128 ;"""
    output = _dci.cmdexec(stmt)
		
    stmt="""unregister user qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127 ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """register user qauser1;"""
    output = _dci.cmdexec(stmt)
	
    stmt="""register user qauser2 as qa902_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120_____128;"""
    output = _dci.cmdexec(stmt)
			
    stmt="""register user qauser3 as qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """register component users9;"""
    output = _dci.cmdexec(stmt)
	
    stmt="""create component privilege created as \'cr\'on users9 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt="""create component privilege updated as \'up\' on users9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt="""grant component privilege created on users9 to qauser1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


    stmt="""grant component privilege  updated on users9 to qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


    stmt="""grant component privilege created on users9 to qa902_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120_____128;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt="""revoke component privilege created on users9 from  qauser1 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt="""revoke component privilege  updated on users9 from  qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt="""revoke component privilege created on users9 from  qa902_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120_____128 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)		
    
    stmt = """unregister component users9 cascade;"""
    output = _dci.cmdexec(stmt)
	
    stmt="""unregister user qauser1;"""
    output = _dci.cmdexec(stmt)

    stmt="""unregister user qa902_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120_____128;"""
    output = _dci.cmdexec(stmt)
	
    stmt="""unregister user qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127;"""
    output = _dci.cmdexec(stmt)
	
    _testmgr.testcase_end(desc)  

def testa10(desc=""" grantee  blank, out of max"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """unregister user qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456129;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """unregister user qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456789132;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """unregister  user qauser4;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """unregister  user qauser5;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """unregister  user qauser6;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """register user qauser5 as qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456129;"""
    output = _dci.cmdexec(stmt)	

    stmt = """register user qauser6 as qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456789132;"""
    output = _dci.cmdexec(stmt)		

    stmt = """register component users10;"""
    output = _dci.cmdexec(stmt)		

    stmt = """create component privilege created as \'cr\' on users10 ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create component privilege updated as \'up\' on users10 ; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant component privilege created on users10 to qauser4; """
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1008')
	
    stmt = """grant component privilege created on users10 to qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456789132;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')	
	
    stmt = """grant component privilege updated on users10 to qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456129;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')	
	
    stmt = """revoke component privilege created on users10 from qauser4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1008')

    stmt = """revoke component privilege created on users10 from qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456789132;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')

    stmt = """revoke component privilege updated on users10 from qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456129;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')	
	

    stmt = """unregister component users10 cascade;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)  

def testa11(desc="""grantee  valid chars"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
	
    stmt = """unregister  user qauser7;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """unregister  user qauser8;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """unregister  user qauser9;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """unregister  user qauser10;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """register  user qauser11;"""
    output = _dci.cmdexec(stmt)
   
    stmt = """register component users11;"""
    output = _dci.cmdexec(stmt)

    stmt = """register user qauser7 as T;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """register user qauser8 as "123456789-_@./";"""
    output = _dci.cmdexec(stmt)
	
    stmt = """register user qauser9 as "LMNOP-./ghij_@klmnop";"""
    output = _dci.cmdexec(stmt)
	
    stmt = """create component privilege created as \'cr\' on users11;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """create component privilege qauser10 as \'pa\' on users11;"""
    output = _dci.cmdexec(stmt)

    stmt = """create component privilege qauser11 as \'p1\' on users11;"""
    output = _dci.cmdexec(stmt)	
	
    stmt = """grant component privilege created on users11 to T;"""
    output = _dci.cmdexec(stmt)	
    _dci.expect_complete_msg(output)	
	
    stmt = """grant component privilege qauser10  on users11 to "123456789-_@./" with grant option;"""
    output = _dci.cmdexec(stmt)	
    _dci.expect_complete_msg(output)	

    stmt = """grant component privilege qauser11 on users11 to "LMNOP-./ghij_@klmnop";"""
    output = _dci.cmdexec(stmt)	
    _dci.expect_complete_msg(output)	

    stmt = """revoke component privilege created on users11 from T;"""
    output = _dci.cmdexec(stmt)	
    _dci.expect_complete_msg(output)		
	
    stmt = """revoke component privilege qauser10  on users11 from "123456789-_@./" cascade;"""
    output = _dci.cmdexec(stmt)	
    _dci.expect_complete_msg(output)		
	
    stmt = """revoke component privilege qauser11 on users11 from "LMNOP-./ghij_@klmnop";"""
    output = _dci.cmdexec(stmt)	
    _dci.expect_complete_msg(output)		
	
    stmt="""unregister component users11 cascade;"""
    output = _dci.cmdexec(stmt)	

    stmt="""unregister user T;"""
    output = _dci.cmdexec(stmt)	

    stmt="""unregister user "123456789-_@./";"""
    output = _dci.cmdexec(stmt)	

    stmt="""unregister user "LMNOP-./ghij_@klmnop";"""
    output = _dci.cmdexec(stmt)		

    stmt="""unregister user qauser10;"""
    output = _dci.cmdexec(stmt)	

    stmt="""unregister user qauser11;"""
    output = _dci.cmdexec(stmt)			
	
    _testmgr.testcase_end(desc)  


def testa12(desc="""grantee  invalid chars"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
	
    stmt = """unregister  user qauser12;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """unregister  user qauser13;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """unregister  user qauser14;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """register user qauser12 as _W1245wereqwr;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """register user qauser13 as "@test1";"""
    output = _dci.cmdexec(stmt)
	
    stmt = """register user qauser14 as \"^testa**$\";"""
    output = _dci.cmdexec(stmt)		
    
    stmt = """register component users12;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """create component privilege created as \'cr\' on users12;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """create component privilege qauser10 as \'pa\' on users12;"""
    output = _dci.cmdexec(stmt)

    stmt = """create component privilege qauser11 as \'p1\' on users12;"""
    output = _dci.cmdexec(stmt)	

    stmt = """grant component privilege created on users12 to _W1245wereqwr;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
	
    stmt = """grant component privilege qauser10 on users12 to  "@test1";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """grant component privilege qauser11 on users12 to  \"^testa**$\";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')	
	
    stmt = """revoke component privilege created on users12 from _W1245wereqwr;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
	
    stmt = """revoke component privilege qauser10 on users12 from "@test1";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')	
	
    stmt = """revoke component privilege qauser11 on users12 from \"^testa**$\" cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')	
           
           
    stmt = """unregister component users12 cascade;"""
    output = _dci.cmdexec(stmt)
	
    _testmgr.testcase_end(desc)  
           

def testa13(desc="""missing, invaild keywords"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """register component users13;"""
    output = _dci.cmdexec(stmt)

    stmt = """create component privilege created as \'cr\' on users13 detail \'create users\'; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt = """create component privilege updated as \'up\' on users13; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   	
    stmt = """grant component privilege created, updated on users13 to qauser_sqlqaa with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)	
	
    stmt = """revoke component privilege created, updated on users13 from qauser_sqlqaa with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
	
    stmt = """revoke privilege created, updated on users13 from qauser_sqlqaa ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
	
    stmt = """revoke component privilge updated created on users13 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """revoke with grant option component privilege created, updated on users13 from qauser_sqlqaa ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
	
    stmt = """revoke component privilege created, updated on users13 from qauser_sqlqaa grant option for ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
	
    stmt = """revoke component privilege created, updated on users13 from qauser_sqlqaa restrict;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)   
	
    stmt = """revoke component privilege created, updated on users13 from qauser_sqlqaa cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1004')
    
  
    stmt = """unregister component users13 cascade;"""
    output = _dci.cmdexec(stmt)
	
    _testmgr.testcase_end(desc)  


def testa14(desc="""not all of priv_name_list exist(exist in other components)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
 
    stmt = """register component users141;"""
    output = _dci.cmdexec(stmt)

    stmt = """register component users142;"""
    output = _dci.cmdexec(stmt)
 
    stmt="""create component privilege created as \'ca\' on users141;"""
    output = _dci.cmdexec(stmt)
	
    stmt="""create component privilege updated as \'up\' on users141;"""
    output = _dci.cmdexec(stmt)
	
    stmt="""create component privilege deleted as \'de\' on users141;"""
    output = _dci.cmdexec(stmt)
	
    stmt="""create component privilege updated as \'up\' on users142;"""
    output = _dci.cmdexec(stmt)
	
    stmt="""grant component privilege created on users141 to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt="""grant component privilege updated on users141 to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt="""grant component privilege created ,updated ,deleted on users142 to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1004')
	
    stmt="""revoke component privilege created, updated on user142 from  qauser_tsang cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1004')
	
    stmt="""revoke component privilege updated,deleted on users141 from  qauser_tsang cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1018')
	
    stmt="""revoke component privilege created ,updated ,deleted on users142 from qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1004')
	
    stmt="""revoke component privilege created ,updated ,deleted on users141 from qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1018')

	
    stmt="""unregister component users141 cascade;"""
    output = _dci.cmdexec(stmt)	

    stmt="""unregister component users142 cascade;"""
    output = _dci.cmdexec(stmt)	
			
    _testmgr.testcase_end(desc) 

def testa15(desc="""revoke privilege from non-existing grantee"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
	
    stmt = """unregister user qauser16;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser17;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """unregister user qauser18;"""
    output = _dci.cmdexec(stmt)
	
    stmt='unregister user qauser19;'
    output = _dci.cmdexec(stmt)


    stmt = """register user qauser17 as qauser17test;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """register user qauser18;"""
    output = _dci.cmdexec(stmt)	
	
    stmt="""alter user qauser18 set offline;"""
    output = _dci.cmdexec(stmt)	

    stmt="""create role a15role1;"""
    output = _dci.cmdexec(stmt)	
	
    stmt="""create role a15role2;"""
    output = _dci.cmdexec(stmt)		
	
    stmt="""drop role a15role2;"""
    output = _dci.cmdexec(stmt)	
	
    stmt="""register component users15;"""
    output = _dci.cmdexec(stmt)		
	
    stmt="""create component privilege created as \'ca\' on users15;"""
    output = _dci.cmdexec(stmt)			
	
    stmt="""create component privilege updated as \'up\' on users15;"""
    output = _dci.cmdexec(stmt)	

    stmt="""create component privilege deleted as \'de\' on users15;"""
    output = _dci.cmdexec(stmt)		
	
    stmt="""grant component privilege created ,updated on users15 to qauser16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1008')	
	
    stmt="""grant component privilege created ,updated on users15 to qauser17test;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt="""alter user qauser17test set external name qauser19;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)	
	
    stmt="""grant component privilege created ,updated on users15 to qauser18;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt = """unregister user qauser18;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1227')	
	
    stmt="""grant component privilege deleted on users15 to a15role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt="""drop role a15role1;"""
    output = _dci.cmdexec(stmt)	
    _dci.expect_error_msg(output, '1228')	
	
    stmt="""grant component privilege deleted on users15 to a15role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1008')
	
    stmt="""revoke component privilege created ,updated on users15 from qauser16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1008')
	
    stmt="""revoke component privilege created ,updated on users15 from qauser17test ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt="""revoke component privilege created ,updated on users15 from qauser18;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt="""revoke component privilege deleted on users15 from a15role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt="""revoke component privilege created ,updated on users15  from qauser16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1008')

    stmt = """unregister component users15 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser16;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser17test;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """unregister user qauser18;"""
    output = _dci.cmdexec(stmt)
	
    stmt="""drop role a15role1;"""
    output = _dci.cmdexec(stmt)	
	
    _testmgr.testcase_end(desc)   
	
def testa16(desc="""revoke privilege on non-existing name"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 	
	
    stmt = """register component users161;"""
    output = _dci.cmdexec(stmt)	
	
    stmt = """register component users162;"""
    output = _dci.cmdexec(stmt)	
	
    stmt = """unregister component users162;"""
    output = _dci.cmdexec(stmt)	

    stmt = """create component privilege created as \'ca\' on users161;"""
    output = _dci.cmdexec(stmt)	
	
    stmt = """create component privilege updated as \'up\' on users161;"""
    output = _dci.cmdexec(stmt)	
	
    stmt = """create component privilege deleted as \'de\' on users161;"""
    output = _dci.cmdexec(stmt)	
	
    stmt="""grant component privilege created, updated , deleted on users162 to qauser_tsang with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1004')
		
    stmt="""grant component privilege created, updated , deleted on users16 to qauser_tsang with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1004')	
	
    stmt="""revoke component privilege created, updated,deleted on users162 from qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1004')
	
    stmt="""revoke component privilege created, updated , deleted on users from qauser_tsang ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1004')	
   
    stmt="""unregister component users161 cascade;"""
    output = _dci.cmdexec(stmt)
	
    stmt="""grant component privilege created, updated , deleted on users161 to qauser_tsang with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1004')		
	
    stmt="""revoke grant option for component privilege created, updated , deleted on users161 from qauser_tsang ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1004')	

    _testmgr.testcase_end(desc)

def testa17(desc="""revoke privilege from grantee lists"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 	
		
	
    stmt = """create role a17role1;"""
    output = _dci.cmdexec(stmt)
	
    stmt="""register component users17;"""
    output = _dci.cmdexec(stmt)
	
    stmt="""create component privilege created as \'ca\' on users17;"""
    output = _dci.cmdexec(stmt)
	
    stmt="""create component privilege updated as \'up\' on users17;"""
    output = _dci.cmdexec(stmt)
	
    stmt="""create component privilege deleted as \'de\' on users17;"""
    output = _dci.cmdexec(stmt)
	
    stmt="""grant component privilege created on users17 to qauser_tsang with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt="""grant component privilege updated, deleted on users17 to qauser_tsang,a17role1 with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
	
    stmt="""revoke component privilege created,updated, deleted on users17 from qauser_tsang, a17role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt="""revoke component privilege updated ,deleted on users17 from qauser_tsang, a17role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt="""revoke component privilege created on users17 from qauser_tsang;"""
    output = _dci.cmdexec(stmt)	
    _dci.expect_complete_msg(output)
	
    stmt="""unregister component users17 cascade;"""
    output = _dci.cmdexec(stmt)	
	
    stmt="""drop role a17role1;"""
    output = _dci.cmdexec(stmt)	
	

    _testmgr.testcase_end(desc)   	
	

def testa18(desc="""grant privlege separately ,revoke privilege together"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 	
			
    stmt="""create role a18role1;"""
    output = _dci.cmdexec(stmt)		

    stmt="""register component users18;"""
    output = _dci.cmdexec(stmt)	
	
    stmt="""create component privilege created as \'ca\' on users18;"""
    output = _dci.cmdexec(stmt)		

	
    stmt="""create component privilege updated as \'up\' on users18;"""
    output = _dci.cmdexec(stmt)		
	
	
    stmt="""create component privilege deleted as \'de\' on users18;;"""
    output = _dci.cmdexec(stmt)				

    stmt = """grant component privilege created on users18 to qauser_tsang with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt = """grant component privilege updated on users18 to qauser_tsang with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant component privilege deleted on users18 to qauser_tsang with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt = """grant component privilege created on users18 to a18role1 by qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt = """grant component privilege deleted on users18 to a18role1 by qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt = """revoke component privilege deleted ,created, updated on users18 from a18role1 by qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1018')
	
    stmt = """revoke component privilege deleted ,created on users18 from a18role1 by qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt = """revoke component privilege created, updated,deleted on users18 from qauser_tsang cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt="""unregister component users18 cascade;"""
    output = _dci.cmdexec(stmt)
	
    stmt="""drop role a18role1;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)   	
	
def testa19(desc=""" ordinary user revoke privilege"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 		
	
    stmt="""register component users19;"""
    output = _dci.cmdexec(stmt)			
	
    stmt="""create component privilege created as \'ca\' on users19;"""
    output = _dci.cmdexec(stmt)		

    stmt="""create component privilege updated as \'up\' on users19;"""
    output = _dci.cmdexec(stmt)			

    stmt="""grant component privilege created on users19 to qauser_tsang with grant option;"""
    output = _dci.cmdexec(stmt)	
    _dci.expect_complete_msg(output)		

    mydci = basic_defs.switch_session_qi_user3()  

    stmt="""grant component privilege updated on users19 to qauser_tsang;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')	

    stmt="""grant component privilege updated on users19 to qauser_tsang with grant option ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt="""revoke component privilege created ,updated on users19 from qauser_tsang;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1018')		

    stmt="""revoke component privilege created ,updated on users19 from qauser_tsang cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1018')		

    stmt="""unregister component users19 cascade;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)   

def testa20(desc=""" ordinary user with admin privilge revoke privilege"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 	
	
    stmt="""register component users20;"""
    output = _dci.cmdexec(stmt)	

    stmt="""create component privilege created as \'ca\' on users20;"""
    output = _dci.cmdexec(stmt)	
	
    stmt="""create component privilege updated as \'up\' on users20;"""
    output = _dci.cmdexec(stmt)	

    stmt="""grant role db__rootrole to qauser_tsang;"""
    output = _dci.cmdexec(stmt)		
	
    stmt="""grant component privilege created on users20 to qauser_sqlqaa with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    mydci = basic_defs.switch_session_qi_user2()  
	
    stmt="""grant component privilege updated on users20 to qauser_sqlqaa;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')

    stmt="""revoke component privilege created ,updated on users20 from qauser_sqlqaa cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1018')

    stmt="""revoke component privilege created on users20 from qauser_sqlqaa cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1018')
	
    stmt="""revoke component privilege created on users20 from qauser_sqlqaa cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1018')
	
    stmt="""revoke role db__rootrole from qauser_tsang;"""
    output = mydci.cmdexec(stmt)

    stmt="""unregister component users20 cascade;"""
    output = _dci.cmdexec(stmt)	  

    _testmgr.testcase_end(desc)   	
 	
def testa21(desc="""one excutes grant ,another excute revoke """):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 	
	
    stmt="""register component users21;"""
    output = _dci.cmdexec(stmt)	  
	
    stmt="""create component privilege created as \'cr\' on users21 ;"""
    output = _dci.cmdexec(stmt)	  
	
    stmt="""create component privilege updated as \'up\' on users21;"""
    output = _dci.cmdexec(stmt)	  

    stmt="""grant role DB__rootrole to qauser_tsang;"""
    output = _dci.cmdexec(stmt)	  

    stmt="""grant component privilege created ,updated on users21 to qauser_sqlqaa with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    mydci = basic_defs.switch_session_qi_user2()  

    stmt="""revoke component privilege created ,updated on users21 from qauser_sqlqaa cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output,'1018')
	
    stmt="""revoke component privilege created, updated on users21 from qauser_sqlqaa cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output,'1018')
   	
	
    stmt="""unregister component users21 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt="""revoke role db__rootrole from qauser_tsang;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)   	
	
def testa22(desc=""" revoke by an ordinary user  """):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 	
	
    stmt="""register component users22;"""
    output = _dci.cmdexec(stmt)	

	
    stmt="""create component privilege created as \'ca\' on users22;"""
    output = _dci.cmdexec(stmt)		
	
    stmt="""create component privilege updated as \'up\' on users22;"""
    output = _dci.cmdexec(stmt)
	
	
    stmt="""grant component privilege created ,updated on users22 to qauser_sqlqaa with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt="""grant component privilege created ,updated on users22 to qauser_sqlqaa with grant option by qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1017')
	
    stmt="""revoke component privilege created,updated on users22  from qauser_sqlqaa by qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1018')
	
    mydci = basic_defs.switch_session_qi_user2()  
	
    stmt="""revoke component privilege created,updated on users22  from qauser_sqlqaa by db__root;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output,'1017')
	
    stmt="""revoke component privilege created,updated on users22  from qauser_sqlqaa by db__root;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt="""unregister component users22 cascade;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)   	
	
def testa23(desc="""revoke by an ordinary user with admin privilege"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 	

    stmt="""register component users23;"""
    output = _dci.cmdexec(stmt)
	
    stmt="""create component privilege created as \'cr\' on users23 ;"""
    output = _dci.cmdexec(stmt)
	
    stmt="""create component privilege updated  as \'up\' on users23 ;"""
    output = _dci.cmdexec(stmt)

	
    stmt="""grant role db__rootrole  to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt="""grant component privilege created on users23 to qauser_sqlqaa with grant option;"""	
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt="""grant component privilege updated on users23 to qauser_sqlqaa ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt="""grant component privilege created on users23 to qauser_sqlqab by qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)	
	
	
    mydci = basic_defs.switch_session_qi_user2()  

    stmt="""grant component privilege created on users23 to qauser_sqlqab by qauser_sqlqaa;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output,'1017')
	
    stmt="""revoke component privilege updated on users23 from qauser_sqlqaa cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output,'1018')
	
    stmt="""revoke component privilege updated on users23 from qauser_sqlqaa by qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1018')
	
    stmt="""revoke component privilege updated on users23  from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)	
	
    stmt="""revoke component privilege created on users23 from qauser_sqlqab by qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1018')
	
    stmt="""revoke component privilege created on users23 from qauser_sqlqab by qauser_tsang;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output,'1017')

    stmt="""revoke component privilege created on users23 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1014')	

    stmt="""revoke component privilege created on users23 from qauser_sqlqab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1014')	

    stmt="""revoke component privilege created on users23 from qauser_sqlqab by qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)	

    stmt="""revoke component privilege created on users23 from qauser_sqlqaa  cascade by qauser_tsang;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output,'1017')	

    stmt="""revoke component privilege created on users23 from qauser_sqlqaa  cascade by qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1350')	

    stmt="""revoke component privilege created on  users23 from qauser_sqlqaa cascade by db__root;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1014')	

    stmt="""revoke role db__rootrole from qauser_tsang;"""
    output = _dci.cmdexec(stmt)
	
    stmt="""unregister component users23 cascade;"""
    output = _dci.cmdexec(stmt)
	
    _testmgr.testcase_end(desc)   	
	
def testa24(desc="""grant privielge by different roles/users ,revoke one time"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 	

    stmt="""register component users24;"""
    output = _dci.cmdexec(stmt)
	
    stmt="""create role a24role1;"""
    output = _dci.cmdexec(stmt)	
	
    stmt="""create component privilege created as \'ca\' on users24;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)	
	
    stmt="""create component privilege updated as \'up\' on users24;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)	

    stmt="""grant component privilege created , updated on users24 to qauser_tsang with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt="""grant component privilege created ,updated on users24 to a24role1 with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)	

    stmt="""grant component privilege created, updated on users24 to qauser_sqlqaa with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)	

    stmt="""grant component privilege created ,updated on users24 to qauser_sqlqaa by qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)	

    stmt="""grant component privilege created ,updated on users24 to qauser_sqlqaa by a24role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)	

    stmt="""revoke component privilege created ,updated on users24 from qauser_sqlqaa by  qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)	
	
    stmt="""revoke component privilege created ,updated on users24 from qauser_sqlqaa by db__root;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1004')		
	
    stmt="""revoke component privilege created ,updated on users24 from qauser_sqlqaa by a24role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1004')	
	
    stmt="""revoke component privilege created, updated on users24 from qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)	
	
    stmt="""revoke  component privilege created, updated on users24 from a24role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)	
	
    stmt="""unregister component users24 cascade;"""
    output = _dci.cmdexec(stmt)
	
    stmt="""drop role a24role1;"""
    output = _dci.cmdexec(stmt)	
	
    _testmgr.testcase_end(desc)   


def testa25(desc="""revoke privilege more than one time """):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 	
	
    stmt="""register component users25;"""
    output = _dci.cmdexec(stmt)
	
	
    stmt="""create component privilege created as \'ca\' on users25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)	
	
    stmt="""create component privilege updated as \'up\' on users25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)	
	
    stmt="""grant component privilege created , updated on users25 to qauser_tsang with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)	
	
    stmt="""grant component privilege created on users25 to qauser_tsang ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)	
	
    stmt="""grant component privilege created on users25 to qauser_sqlqaa by qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt="""revoke component privilege updated on users25 from qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)	
	
    stmt="""revoke component privilege created on users25 from qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1004')	
	
    stmt="""revoke component privilege created on users25 from qauser_tsang cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)	
	
    stmt="""revoke component privilege created on users25 from qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1004')	
	
    stmt="""unregister component users25 cascade;"""
    output = _dci.cmdexec(stmt)
	
    _testmgr.testcase_end(desc)   

	
def testa26(desc="""revoke privilege ,then drop component privileg ,unregister component """):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 	
	
    stmt="""register component users26;"""
    output = _dci.cmdexec(stmt)
	
    stmt="""create component privilege created as \'ca\' on users26;"""
    output = _dci.cmdexec(stmt)
	
    stmt="""create component privilege updated as \'up\' on users26;"""
    output = _dci.cmdexec(stmt)
	
    stmt="""grant component privilege created ,updated on users26 to qauser_tsang with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)	

    stmt="""unregister component users26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1025')	
	
    stmt="""revoke  component privilege created ,updated on users26 from qauser_tsang  cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)		
	
    stmt="""unregister component users26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1025')	
	
    stmt="""drop component privilege created on users26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)		
	
    stmt="""drop component privilege updated on users26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt="""unregister component users26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)	

    _testmgr.testcase_end(desc)  
	
def testa27(desc=""" revoke grant option for"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 	

    stmt="""register component users27;"""
    output = _dci.cmdexec(stmt)	
	
    stmt="""create component privilege created as \'ca\' on users27;"""
    output = _dci.cmdexec(stmt)	
	
    stmt="""create component privilege updated as \'up\' on users27;"""
    output = _dci.cmdexec(stmt)		
	
    stmt="""grant component privilege created on users27 to qauser_tsang with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt="""grant component privilege updated on users27 to qauser_tsang;"""
    output = _dci.cmdexec(stmt)		
    _dci.expect_complete_msg(output)	
	
    stmt="""grant component privilege created on users27 to qauser_sqlqaa with grant option by qauser_tsang;"""
    output = _dci.cmdexec(stmt)		
    _dci.expect_complete_msg(output)	
	
    stmt="""grant component privilege updated on users27 to qauser_sqlqaa by qauser_tsang;"""
    output = _dci.cmdexec(stmt)		
    _dci.expect_error_msg(output,'1017')	
	
    stmt="""revoke grant option for component privilege created on users27 from qauser_tsang;"""
    output = _dci.cmdexec(stmt)		
    _dci.expect_complete_msg(output)	

    stmt="""get component privilege on users27;"""
    output = _dci.cmdexec(stmt)		
    _dci.unexpect_any_substr(output,'grant component privilege create on qauser_sqlqaa')
    _dci.expect_any_substr(output,'grant component privilege create on qauser_tsang')
	
    stmt="""grant component privilege created on users27 to qauser_sqlqab by qauser_tsang;"""
    output = _dci.cmdexec(stmt)		
    _dci.expect_error_msg(output,'1017')	
	
    stmt="""grant component privilege created on users27 to qauser_sqlqab by qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)		
    _dci.expect_error_msg(output,'1017')

    stmt="""unregister component users27 cascade;"""
    output = _dci.cmdexec(stmt)		
	
    _testmgr.testcase_end(desc)  
	
def testa28(desc="""revoke privilege cascade ,then drop component privilege ,unregister component"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 	
    _testmgr.testcase_end(desc)  
	
def testa29(desc="""user create object based on granted privilege ,then revoke component privilege"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 	
    _testmgr.testcase_end(desc)  
	
def testa30(desc="""user create object based on granted privilege ,then revoke component privilege cascade"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 	
    _testmgr.testcase_end(desc)  
		
	
def testa31(desc="""cleanup"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 	
	
    stmt="""unregister component users1 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt="""unregister component users2 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt="""unregister component users3 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt="""unregister component users4 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt="""unregister component qa902_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120_____128 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt="""unregister component qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt="""unregister component  qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456129;"""
    output = _dci.cmdexec(stmt)
    stmt="""unregister component qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456789132;"""
    output = _dci.cmdexec(stmt)
    stmt="""unregister component AAA cascade;"""
    output = _dci.cmdexec(stmt)
    stmt="""unregister component abcd cascade;"""
    output = _dci.cmdexec(stmt)
    stmt="""unregister component A1B2 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt="""unregister component "LMNOP-./ghij_@klmnop" cascade;"""
    output = _dci.cmdexec(stmt)
    stmt="""unregister component test cascade;"""
    output = _dci.cmdexec(stmt)
    stmt="""unregister component "/test/" cascade;"""
    output = _dci.cmdexec(stmt)
    stmt="""unregister component users9 cascade;"""
    output = _dci.cmdexec(stmt)
    #stmt="""unregister user qauser1;"""
    #output = _dci.cmdexec(stmt)
    stmt="""unregister component users10 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt="""unregister user qa902_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120_____128 ;"""
    output = _dci.cmdexec(stmt)
    stmt="""unregister user qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127 ;"""
    output = _dci.cmdexec(stmt)
    #stmt="""unregister user qauser4;"""
    #output = _dci.cmdexec(stmt)
    #stmt="""unregister user qauser5;"""
    #output = _dci.cmdexec(stmt)
    #stmt="""unregister user qauser6;"""
    #output = _dci.cmdexec(stmt)
    stmt="""unregister component users11 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt="""unregister user T;"""
    output = _dci.cmdexec(stmt)
    stmt="""unregister user "123456789-_@./";"""
    output = _dci.cmdexec(stmt)
    stmt="""unregister user "LMNOP-./ghij_@klmnop";"""
    output = _dci.cmdexec(stmt)
    #stmt="""unregister user qauser10;"""
    #output = _dci.cmdexec(stmt)
    #stmt="""unregister user qauser11;"""
    #output = _dci.cmdexec(stmt)
    #stmt="""unregister user qauser12;"""
    #output = _dci.cmdexec(stmt)
    #stmt="""unregister user qauser13;"""
    #output = _dci.cmdexec(stmt)
    #stmt="""unregister user qauser14;"""
    #output = _dci.cmdexec(stmt)
    stmt="""unregister component users12 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt="""unregister component users13 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt="""unregister component users141 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt="""unregister component users142 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt="""unregister component users15 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt="""drop role a15role1;"""
    output = _dci.cmdexec(stmt)
    #stmt="""unregister user qauser16;"""
    #output = _dci.cmdexec(stmt)
    #stmt="""unregister user qauser17;"""
    #output = _dci.cmdexec(stmt)
    #stmt="""unregister user qauser18;"""
    #output = _dci.cmdexec(stmt)	
    #stmt="""unregister user qauser19;"""
    #output = _dci.cmdexec(stmt)
    stmt="""unregister user qauser17test;"""
    output = _dci.cmdexec(stmt)	
    stmt="""unregister component users162 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt="""unregister component users161 cascade;"""
    output = _dci.cmdexec(stmt)		
    stmt="""unregister component users17 cascade;"""
    output = _dci.cmdexec(stmt)		
    stmt="""drop role a17role1;"""
    output = _dci.cmdexec(stmt)
    stmt="""unregister component users18 cascade;"""
    output = _dci.cmdexec(stmt)		
    stmt="""drop role a18role1;"""
    output = _dci.cmdexec(stmt)		
    stmt="""unregister component users19 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt="""unregister component users20 cascade;"""
    output = _dci.cmdexec(stmt)		
    stmt="""unregister  component users21 cascade;"""
    output = _dci.cmdexec(stmt)					
    stmt="""unregister component users22 cascade;"""
    output = _dci.cmdexec(stmt)		
    stmt="""unregister component  users23 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt="""unregister component users24 cascade;"""
    output = _dci.cmdexec(stmt)		
    stmt="""drop role a24role1;"""
    output = _dci.cmdexec(stmt)			
    stmt="""unregister component users25 cascade;"""
    output = _dci.cmdexec(stmt)		
    stmt="""unregister component users26 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt="""unregister component users27 cascade;"""
    output = _dci.cmdexec(stmt)		

    _testmgr.testcase_end(desc)   		
	
	
	
	
	
	
	
	
	
	
	
	
