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

def testa01(desc="""create table"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    

    stmt = """create schema schema1;"""
    output = _dci.cmdexec(stmt)

    stmt = """set schema schema1;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table test_tab1 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table test_tab2 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table test_tab3 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 

    stmt = """create table test_tab4 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt)    
    
    stmt = """create table test_tab5 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table test_tab6 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt)    
    
    stmt = """create table test_tab7 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab8 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab9 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab10 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab11 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab12 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab13 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab14 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab15 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab16 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab17 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab18 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab19 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab20 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab21 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab22 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab23 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab24 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab25 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab26 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab27 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab28 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab29 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab30 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab31 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab32 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab33 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab34 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab35 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab36 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab37 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab38 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab39 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab40 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab41 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab42 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab43 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab44 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab45 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab46 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab47 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab48 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab49 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab50 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab51 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab52 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab53 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab54 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab55 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab56 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab57 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab58 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab59 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab60 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab61 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab62 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab63 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab64 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab65 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab66 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab67 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab68 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab69 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab70 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab71 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab72 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab73 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab74 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab75 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab76 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab77 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab78 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab79 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab80 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab81 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab82 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab83 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab84 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab85 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab86 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab87 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab88 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab89 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab90 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab91 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab92 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab93 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab94 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab95 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab96 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab97 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab98 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab99 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """create table test_tab100 (a int not null primary key,b int) ;"""
    output = _dci.cmdexec(stmt) 
    
    _testmgr.testcase_end(desc)

def testa02(desc="""update statistics"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    

    stmt = """set schema schema1;"""
    output = _dci.cmdexec(stmt)    
    
    stmt = """update statistics for table test_tab1 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab2 on every column;"""
    output = _dci.cmdexec(stmt) 
    stmt = """update statistics for table test_tab3 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab4 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab5 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab6 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab7 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab8 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab9 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab10 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab11 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab12 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab13 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab14 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab15 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab16 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab17 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab18 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab19 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab20 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab21 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab22 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab23 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab24 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab25 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab26 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab27 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab28 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab29 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab30 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab31 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab32 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab33 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab34 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab35 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab36 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab37 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab38 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab39 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab40 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab41 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab42 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab43 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab44 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab45 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab46 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab47 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab48 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab49 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab50 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab51 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab52 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab53 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab54 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab55 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab56 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab57 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab58 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab59 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab60 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab61 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab62 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab63 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab64 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab65 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab66 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab67 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab68 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab69 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab70 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab71 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab72 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab73 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab74 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab75 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab76 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab77 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab78 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab79 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab80 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab81 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab82 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab83 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab84 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab85 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab86 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab87 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab88 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab89 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab90 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab91 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab92 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab93 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab94 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab95 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab96 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab97 on every column;"""
    output = _dci.cmdexec(stmt) 
    stmt = """update statistics for table test_tab98 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab99 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """update statistics for table test_tab100 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    _testmgr.testcase_end(desc)
    
def testa03(desc="""showstats"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    

    stmt = """set schema schema1;"""
    output = _dci.cmdexec(stmt)    
    
    stmt = """showstats for table test_tab1 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab2 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab3 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab4 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab5 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab6 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab7 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab8 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab9 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab10 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab11 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab12 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab13 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab14 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab15 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab16 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab17 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab18 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab19 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab20 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab21 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab22 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab23 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab24 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab25 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab26 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab27 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab28 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab29 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab30 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab31 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab32 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab33 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab34 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab35 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab36 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab37 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab38 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab39 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab40 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab41 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab42 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab43 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab44 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab45 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab46 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab47 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab48 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab49 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab50 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab51 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab52 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab53 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab54 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab55 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab56 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab57 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab58 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab59 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab60 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab61 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab62 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab63 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab64 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab65 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab66 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab67 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab68 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab69 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab70 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab71 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab72 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab73 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab74 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab75 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab76 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab77 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab78 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab79 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab80 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab81 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab82 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab83 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab84 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab85 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab86 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab87 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab88 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab89 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab90 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab91 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab92 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab93 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab94 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab95 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab96 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab97 on every column;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """showstats for table test_tab98 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab99 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """showstats for table test_tab100 on every column;"""
    output = _dci.cmdexec(stmt) 
    
    _testmgr.testcase_end(desc)
    
    
def testa04(desc="""drop table"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    

    stmt = """set schema schema1;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table test_tab1 cascade ;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table test_tab2 cascade ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table test_tab3 cascade ;"""
    output = _dci.cmdexec(stmt) 

    stmt = """drop table test_tab4 cascade ;"""
    output = _dci.cmdexec(stmt)    
    
    stmt = """drop table test_tab5 cascade ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table test_tab6 cascade ;"""
    output = _dci.cmdexec(stmt)    
    
    stmt = """drop table test_tab7 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab8 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab9 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab10 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab11 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab12 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab13 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab14 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab15 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab16 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab17 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab18 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab19 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab20 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab21 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab22 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab23 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab24 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab25 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab26 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab27 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab28 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab29 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab30 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab31 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab32 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab33 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab34 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab35 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab36 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab37 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab38 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab39 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab40 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab41 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab42 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab43 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab44 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab45 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab46 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab47 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab48 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab49 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab50 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab51 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab52 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab53 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab54 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab55 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab56 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab57 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab58 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab59 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab60 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab61 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab62 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab63 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab64 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab65 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab66 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab67 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab68 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab69 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab70 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab71 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab72 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab73 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab74 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab75 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab76 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab77 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab78 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab79 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab80 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab81 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab82 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab83 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab84 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab85 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab86 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab87 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab88 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab89 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab90 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab91 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab92 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab93 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab94 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab95 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab96 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab97 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab98 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab99 cascade ;"""
    output = _dci.cmdexec(stmt) 
    
    stmt = """drop table test_tab100 cascade ;"""
    output = _dci.cmdexec(stmt) 

    stmt = """drop schema schema1 cascade;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)