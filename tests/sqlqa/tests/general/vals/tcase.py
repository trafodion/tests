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

import mytest0031
import mytest0033
import mytest0035
import mytest0034
import mytest0039
import mytest003
import mytest002
import mytest001
import mytest1109
import mytest007
import mytest006
import mytest005
import mytest004
import mytest0040
import mytest0042
import mytest0022
import mytest0023
import mytest0020
import mytest0027
import mytest0024
import mytest0025
import mytest0028
import mytest0008
import mytest0009
import mytest1097
import mytest103
import mytest100
import mytest1111
import mytest1110
import mytest1112
import mytest1115
import mytest1114
import mytest1116
import mytest0019
import mytest0018
import mytest102
import mytest1145
import mytest0011
import mytest101
import mytest0017
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
    
def test001(desc="""test001"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest001._init(_testmgr)
    _testmgr.testcase_end(desc)

def test002(desc="""test002"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest002._init(_testmgr)
    _testmgr.testcase_end(desc)

def test003(desc="""test003"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest003._init(_testmgr)
    _testmgr.testcase_end(desc)

def test004(desc="""test004"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest004._init(_testmgr)
    _testmgr.testcase_end(desc)

def test005(desc="""test005"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest005._init(_testmgr)
    _testmgr.testcase_end(desc)

def test006(desc="""test006"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest006._init(_testmgr)
    _testmgr.testcase_end(desc)

def test007(desc="""test007"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest007._init(_testmgr)
    _testmgr.testcase_end(desc)

def test008(desc="""test0008"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0008._init(_testmgr)
    _testmgr.testcase_end(desc)

def test009(desc="""test0009"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0009._init(_testmgr)
    _testmgr.testcase_end(desc)

def test010(desc="""test0011"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0011._init(_testmgr)
    _testmgr.testcase_end(desc)

def test011(desc="""test0017"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0017._init(_testmgr)
    _testmgr.testcase_end(desc)

def test012(desc="""test0018"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0018._init(_testmgr)
    _testmgr.testcase_end(desc)

def test013(desc="""test0019"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0019._init(_testmgr)
    _testmgr.testcase_end(desc)

def test014(desc="""test0020"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0020._init(_testmgr)
    _testmgr.testcase_end(desc)

def test015(desc="""test0022"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0022._init(_testmgr)
    _testmgr.testcase_end(desc)

def test016(desc="""test0023"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0023._init(_testmgr)
    _testmgr.testcase_end(desc)

def test017(desc="""test0024"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0024._init(_testmgr)
    _testmgr.testcase_end(desc)

def test018(desc="""test0025"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0025._init(_testmgr)
    _testmgr.testcase_end(desc)

def test019(desc="""test0027"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0027._init(_testmgr)
    _testmgr.testcase_end(desc)

def test020(desc="""test0028"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0028._init(_testmgr)
    _testmgr.testcase_end(desc)

def test021(desc="""test0031"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0031._init(_testmgr)
    _testmgr.testcase_end(desc)

def test022(desc="""test0033"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0033._init(_testmgr)
    _testmgr.testcase_end(desc)

def test023(desc="""test0034"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0034._init(_testmgr)
    _testmgr.testcase_end(desc)

def test024(desc="""test0035"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0035._init(_testmgr)
    _testmgr.testcase_end(desc)

def test025(desc="""test0039"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0039._init(_testmgr)
    _testmgr.testcase_end(desc)

def test026(desc="""test0040"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0040._init(_testmgr)
    _testmgr.testcase_end(desc)

def test027(desc="""test0042"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0042._init(_testmgr)
    _testmgr.testcase_end(desc)

def test028(desc="""test1097"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest1097._init(_testmgr)
    _testmgr.testcase_end(desc)

def test029(desc="""test1109"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest1109._init(_testmgr)
    _testmgr.testcase_end(desc)

def test030(desc="""test1110"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest1110._init(_testmgr)
    _testmgr.testcase_end(desc)

def test031(desc="""test1111"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest1111._init(_testmgr)
    _testmgr.testcase_end(desc)

def test032(desc="""test1112"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest1112._init(_testmgr)
    _testmgr.testcase_end(desc)

def test033(desc="""test1114"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest1114._init(_testmgr)
    _testmgr.testcase_end(desc)

def test034(desc="""test1115"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest1115._init(_testmgr)
    _testmgr.testcase_end(desc)

def test035(desc="""test1116"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest1116._init(_testmgr)
    _testmgr.testcase_end(desc)

def test036(desc="""test1145"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest1145._init(_testmgr)
    _testmgr.testcase_end(desc)

def test037(desc="""test100"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest100._init(_testmgr)
    _testmgr.testcase_end(desc)

def test038(desc="""test101"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest101._init(_testmgr)
    _testmgr.testcase_end(desc)

def test039(desc="""test102"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest102._init(_testmgr)
    _testmgr.testcase_end(desc)

def test040(desc="""test103"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest103._init(_testmgr)
    _testmgr.testcase_end(desc)

