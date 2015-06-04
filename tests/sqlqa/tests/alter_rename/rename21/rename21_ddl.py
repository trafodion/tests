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
    
    stmt = """create table tab_emp_original_01
(
sbin0_10            Numeric(18) signed,
char0_2             Character(8),
udec0_uniq          Decimal(9) unsigned,
ubin0_uniq          PIC 9(9) COMP,
sdec0_500           PIC S9(9),
varchar0_10         varchar(16),
varchar1_20         varchar(8),
sbin1_5000          Numeric(4) signed,
sdec1_4             Decimal(18) signed,
char1_4             Character(8)
)
no partition
location """ + gvars.g_disc1 + """
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table tab_emp_original_02
(
sbin0_10            Numeric(18) signed,
char0_2             Character(8),
udec0_uniq          Decimal(9) unsigned,
ubin0_uniq          PIC 9(9) COMP,
sdec0_500           PIC S9(9),
varchar0_10         varchar(16),
varchar1_20         varchar(8),
sbin1_5000          Numeric(4) signed,
sdec1_4             Decimal(18) signed,
char1_4             Character(8)
)
no partition
location """ + gvars.g_disc1 + """
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table tab_ten_original_03
(
sbin0_10            Numeric(18) signed,
char0_2             Character(8),
udec0_uniq          Decimal(9) unsigned,
ubin0_uniq          PIC 9(9) COMP,
sdec0_500           PIC S9(9),
varchar0_10         varchar(16),
varchar1_20         varchar(8),
sbin1_5000          Numeric(4) signed,
sdec1_4             Decimal(18) signed,
char1_4             Character(8)
)
no partition
location """ + gvars.g_disc1 + """
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table tab_ten_original_04
(
sbin0_10            Numeric(18) signed,
char0_2             Character(8),
udec0_uniq          Decimal(9) unsigned,
ubin0_uniq          PIC 9(9) COMP,
sdec0_500           PIC S9(9),
varchar0_10         varchar(16),
varchar1_20         varchar(8),
sbin1_5000          Numeric(4) signed,
sdec1_4             Decimal(18) signed,
char1_4             Character(8)
)
no partition
location """ + gvars.g_disc1 + """
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table tab_lrg_original_05
(
sbin0_10            Numeric(18) signed,
char0_2             Character(8),
udec0_uniq          Decimal(9) unsigned,
ubin0_uniq          PIC 9(9) COMP,
sdec0_500           PIC S9(9),
varchar0_10         varchar(16),
varchar1_20         varchar(8),
sbin1_5000          Numeric(4) signed,
sdec1_4             Decimal(18) signed,
char1_4             Character(8)
)
no partition
location """ + gvars.g_disc1 + """
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table tab_lrg_original_06
(
sbin0_10            Numeric(18) signed,
char0_2             Character(8),
udec0_uniq          Decimal(9) unsigned,
ubin0_uniq          PIC 9(9) COMP,
sdec0_500           PIC S9(9),
varchar0_10         varchar(16),
varchar1_20         varchar(8),
sbin1_5000          Numeric(4) signed,
sdec1_4             Decimal(18) signed,
char1_4             Character(8)
)
no partition
location """ + gvars.g_disc1 + """
;"""
    output = _dci.cmdexec(stmt)
    
