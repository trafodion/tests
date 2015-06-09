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

def testa01(desc="""Test register component, vary ordering of clauses, misspell keywords"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    

    stmt = """reg component comp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """reg component comp1 system;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """reg component comp1 system,;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """component register comp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """component comp1 register;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register component comp1 as;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register component comp1 detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register component aa system detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register component comp1 detail 12w;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register component comp1 detail ''12w;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register component comp1 detail 12w'';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
        
    _testmgr.testcase_end(desc)
    
    
    
def testa02(desc="""Test register component, dir-comp-name exceeds max length,illegal characters"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """unregister component comp1;"""
    output = _dci.cmdexec(stmt)

    stmt = """register component comp,1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register component ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register component comp|1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register component comp)1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register component c%om*p,1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register component comp:;1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register component comp_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456789132;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')

    stmt = """register component comp1 detail \'comp34567120123456789132aqasew32wder544defffasfwrdqweregpfjdigfkgjfkgjldfslkldkfsjfsadasdadad\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3301')

    stmt = """register component comp1 detail \'com\'p)'';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register component compp1 detail ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    _testmgr.testcase_end(desc)

        
def testa03(desc="""Test register component, string exceeds max length,illegal characters"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """register component comp1 detail \'comp34567120123456789132aqasew32wder544dwkdffdkfjgkdghfkgjkfghfkhhhhhhhhhhqqqqqqqqqqqqqqqqqqddefdgfdgdgggggggggg\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3301')

    stmt = """register component comp1 detail \'com\'p)'';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register component comp1 detail ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register component comp1 system detail \'comp34567120123456789132aqasew32wder544...............................................................\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3301')

    stmt = """register component comp1 system detail \'com''p)\'\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15005')

    stmt = """register component comp1 system detail \'\'\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15005')

    _testmgr.testcase_end(desc)
    

def testa04(desc="""Test register component, dir-comp-name avalid with various lengths, max, symbols"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """unregister component a;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister component qa902_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120_____128;"""
    output = _dci.cmdexec(stmt)
    output = _dci.cmdexec(stmt)

    stmt = """register component qa902_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120_____128;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)       

    stmt = """register component a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """unregister component a;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister component qa902_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120_____128;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)
    
        
def testa05(desc="""Test register component, dir-comp-name avalid with various lengths, max, symbols with system"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """unregister component a;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister component qa902_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120_____128;"""
    output = _dci.cmdexec(stmt)

    stmt = """register component qa902_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120_____128 system;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)       

    stmt = """register component a system;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """unregister component a;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister component qa902_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120_____128;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)
    


def testa06(desc="""Test register component, detail string  valid with various lengths, max, symbols"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """unregister component comp1;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister component comp2;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister component comp3;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister component comp4;"""
    output = _dci.cmdexec(stmt)

    stmt = """register component comp1 detail \'abcdefg\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """register component comp2 detail \'abcdefg%_01\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """register component comp3 detail \'pabcdefg%_01fdsfdghghhhhhhtrrrrrrfrqwertyuioplkjhgfdsazxcvbnmlkjhgfdsa\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """register component comp4 detail \'abcdefg@.coms(8&)\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """unregister component comp1;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister component comp2;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister component comp3;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister component comp4;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)


def testa07(desc="""Test register component, detail string  valid with various lengths, max, symbols with system"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """unregister component comp1;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister component comp2;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister component comp3;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister component comp4;"""
    output = _dci.cmdexec(stmt)

    stmt = """register component comp1 system detail \'abcdefg\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """register component comp2 system detail \'abcdefg%_01\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """register component comp3 system detail \'abcdefg%_01fdsfdghghhhhhhtrrrrrrfrqwertyuioplkjhgfdsazxcvbnmlkjhgfdsa\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """register component comp4 system detail \'abcdefg@.coms(8&)\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """unregister component comp1;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister component comp2;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister component comp3;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister component comp4;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)


def testa08(desc="""Test register component, that is the same name as an existing component name(predefined)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """unregister component comp1;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister component comp2;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister component comp3;"""
    output = _dci.cmdexec(stmt)

    stmt = """register component comp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """register component comp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1055')

    stmt = """register component comp2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()

    stmt = """register component comp2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')

    stmt = """register component comp3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """register component comp3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')

    stmt = """unregister component comp1;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister component comp2;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister component comp3;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)


def testa09(desc="""Test in the initial release, other users cannot register component"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """unregister component comp1;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister component comp2;"""
    output = _dci.cmdexec(stmt)
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """register component comp2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')    
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """register component comp1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')   
    
    _testmgr.testcase_end(desc)

        
def testa10(desc="""Test unregister component, vary ordering of clauses, misspell keywords"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """unregister component comp1;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister component comp1;"""
    output = _dci.cmdexec(stmt)

    stmt = """unreg component comp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """component unregister comp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """component comp1 unregister;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """unregister component comp1 as;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """unregister component comp1 detail;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """unregiste component comp1 restrict;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """unregiste component comp1 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """unregister component comp1,cascade\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15005')
    
    _testmgr.testcase_end(desc)


def testa11(desc="""Test unregister component, dir-comp-name exceeds max length,illegal characters"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """unregister component comp,1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """unregister component comp|1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """unregister component comp)1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """unregister component c%om*p,1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """unregister component comp:;1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """unregister component comp_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456789132;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')

    stmt = """unregister component comp1 detail \'comp34567120123456789132aqasew32wder544dwkdffdkfjgkdghfkgjkfghfkhhhhhhhhhhqqqqqqqqqqqqqqqqqqddefdgfdgdgggggggggg\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """unregister component comp1 detail \'comp34567120123456789132aqasew32wder544...............................................................\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """unregister component comp1 detail \'com\'p)\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15005')
    
    _testmgr.testcase_end(desc)
    
    
def testa12(desc="""Test unregister component, dir-comp-name exist or not exits"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """unregister component comp1;"""
    output = _dci.cmdexec(stmt)

    stmt = """register component comp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """unregister component comp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()

    stmt = """unregister component comp2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')

    stmt = """unregister component comp1 restrict;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1004')

    stmt = """unregister component comp_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456789132  cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')
    
    _testmgr.testcase_end(desc)


def testa13(desc="""Test in the initial release,other users cannot unregister component"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """unregister component comp1;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister component comp2;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister component comp3;"""
    output = _dci.cmdexec(stmt)

    stmt = """register component comp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """register component comp2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """register component comp3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()

    stmt = """unregister component comp1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
        
    mydci = basic_defs.switch_session_qi_user3()

    stmt = """unregister component comp2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 

    stmt = """unregister component comp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """unregister component comp2 restrict;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """unregister component comp3 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)


def testa14(desc="""Test in the initial release,other users cannot unregister component"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """register component comp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """unregister component comp2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1004')

    stmt = """unregister component comp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """unregister component comp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1004')

    stmt = """unregister component comp1 restrict;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1004')

    stmt = """unregister component comp1 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1004')
    
    mydci = basic_defs.switch_session_qi_user3()

    stmt = """unregister component comp1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 

    stmt = """unregister component comp2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    _testmgr.testcase_end(desc)
    

def testa15(desc="""Test in the initial release,other users cannot unregister component"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """unregister component comp1 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister component comp2 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister component comp3 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """register component comp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """register component comp2 system;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """register component comp3 system detail \'system\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt="""create component privilege cde as \'cr\' on comp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt="""create component privilege aaa as \'cs\' on comp2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt="""create component privilege ccs as \'cq\' on comp3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """unregister component comp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1025')

    stmt = """unregister component comp2 restrict;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1025')

    stmt = """unregister component comp2 restrict;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1025')

    stmt="""drop component privilege cde on comp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt="""drop component privilege aaa on comp2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """ drop component privilege ccs on comp3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """unregister component comp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """unregister component comp2 restrict;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """unregister component comp3 restrict;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)



def testa16(desc="""create privs on component, then register component casacde"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """unregister component comp1 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister component comp2 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister component comp3 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """register component comp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """register component comp2 system;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """register component comp3 system detail \'system\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create component privilege cde as \'cr\' on comp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create component privilege aaa as \'cs\' on comp2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create component privilege ccs as \'cd\' on comp3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """unregister component comp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1025')

    stmt = """unregister component comp1 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """unregister component comp2 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """unregister component comp3 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)


def testa17(desc="""ordinary user unregister component"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """unregister component comp1 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister component comp2 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister component comp3 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """register component comp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """register component comp2 system;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """register component comp3 system detail \'system\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create component privilege cde as \'cr\' on comp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create component privilege aaa as \'cs\' on comp2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create component privilege ccs as \'cd\' on comp3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()

    stmt = """unregister component comp1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 

    stmt = """unregister component comp2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 

    stmt = """unregister component comp3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 

    stmt = """unregister component comp1 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """unregister component comp2 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """unregister component comp3 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)


def testa18(desc="""ordinary user with admin unregister component"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """unregister component comp1 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister component comp2 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister component comp3 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """grant role db__rootrole to qauser99;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """register component comp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """register component comp2 system;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """register component comp3 system detail \'system\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()

    stmt = """unregister component comp1;"""
    output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '1017') 
    mydci.expect_complete_msg(output)

    stmt = """unregister component comp2 restrict;"""
    output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '1017') 
    mydci.expect_complete_msg(output)

    stmt = """unregister component comp3 cascade;"""
    output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '1017') 
    mydci.expect_complete_msg(output)

    stmt = """unregister component comp1 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister component comp2 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister component comp3 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """revoke role db__rootrole from qauser99;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)


def testa19(desc="""grant privs on component to users, then unregister component restrict"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """unregister component comp1 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister component comp2 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """register component comp1;"""
    output = _dci.cmdexec(stmt)

    stmt = """register component comp2;"""
    output = _dci.cmdexec(stmt)

    stmt="""create role cp_role1;"""
    output = _dci.cmdexec(stmt)

    stmt = """create component privilege cwe as \'ca\' on comp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create component privilege upd as \'up\' on comp2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant component privilege cwe on comp1 to qauser_tsang with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #mydci = basic_defs.switch_session_qi_user2()

    #stmt = """grant component privilege upd  on comp2 to qauser_sqlqaa;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    stmt="""grant component privilege cwe on comp1 to cp_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """unregister component comp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1025')

    stmt = """unregister component comp1 restrict;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1025')

    stmt = """unregister component comp2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1025')

    stmt = """unregister component comp2 restrict;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1025')

    stmt = """drop component privilege cwe on comp1 cascade;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop component privilege upd on comp2 cascade;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """unregister component comp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """unregister component comp2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role cp_role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
    
    
def testa20(desc="""grant privs on component to users/roles, then unregister component cascade"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """unregister component comp1 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister component comp2 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """register component comp1;"""
    output = _dci.cmdexec(stmt)

    stmt = """register component comp2;"""
    output = _dci.cmdexec(stmt)

    stmt="""create role cp_role2;"""
    output = _dci.cmdexec(stmt)

    stmt = """create component privilege cre as \'ca\' on comp1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create component privilege upd as \'up\' on comp2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant component privilege cre on comp1 to qauser_tsang with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #mydci = basic_defs.switch_session_qi_user2()
    
    #stmt = """grant component privilege upd  on comp2 to qauser_sqlqaa;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    stmt="""grant component privilege cre on comp1 to cp_role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """unregister component comp1 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """unregister component comp2 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role cp_role2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)



