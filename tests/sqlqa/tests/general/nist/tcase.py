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

import mytest0181
import mytest0180
import mytest0182
import mytest0264
import mytest0267
import mytest0260
import mytest0261
import mytest0262
import mytest0263
import mytest0109
import mytest0108
import mytest0613
import mytest0524
import mytest0105
import mytest0104
import mytest0107
import mytest0106
import mytest0101
import mytest0100
import mytest0103
import mytest0102
import mytest0512
import mytest0069
import mytest0066
import mytest0064
import mytest0065
import mytest0062
import mytest0518
import mytest0061
import mytest0299
import mytest0269
import mytest0151
import mytest0279
import mytest0277
import mytest0237
import mytest0275
import mytest0273
import mytest0229
import mytest0271
import mytest0270
import mytest0509
import mytest0285
import mytest0167
import mytest0691
import mytest0258
import mytest0455
import mytest0071
import mytest0070
import mytest0073
import mytest0072
import mytest0075
import mytest0074
import mytest0077
import mytest0076
import mytest0079
import mytest0078
import mytest0172
import mytest0173
import mytest0174
import mytest0175
import mytest0176
import mytest0177
import mytest0489
import mytest0254
import mytest0487
import mytest0243
import mytest0088
import mytest0089
import mytest0244
import mytest0245
import mytest0084
import mytest0085
import mytest0086
import mytest0087
import mytest0080
import mytest0081
import mytest0082
import mytest0083
import mytest0178
import mytest0179
import mytest0004
import mytest0005
import mytest0169
import mytest0168
import mytest0001
import mytest0002
import mytest0003
import mytest0160
import mytest0008
import mytest0009
import mytest0164
import mytest0493
import mytest0492
import mytest0222
import mytest0272
import mytest0494
import mytest0170
import mytest0257
import mytest0251
import mytest0250
import mytest0099
import mytest0098
import mytest0097
import mytest0096
import mytest0095
import mytest0094
import mytest0093
import mytest0092
import mytest0091
import mytest0090
import mytest0129
import mytest0564
import mytest0284
import mytest0017
import mytest0016
import mytest0396
import mytest0397
import mytest0011
import mytest0159
import mytest0156
import mytest0157
import mytest0155
import mytest0152
import mytest0153
import mytest0019
import mytest0018
import mytest0454
import mytest0253
import mytest0453
import mytest0252
import mytest0611
import mytest0452
import mytest0171
import mytest0305
import mytest0304
import mytest0303
import mytest0302
import mytest0300
import mytest0220
import mytest0221
import mytest0028
import mytest0225
import mytest0226
import mytest0227
import mytest0022
import mytest0023
import mytest0020
import mytest0026
import mytest0027
import mytest0024
import mytest0025
import mytest0412
import mytest0411
import mytest0145
import mytest0149
import mytest0148
import mytest0419
import mytest0418
import mytest0389
import mytest0331
import mytest0839
import mytest0233
import mytest0039
import mytest0038
import mytest0234
import mytest0035
import mytest0034
import mytest0037
import mytest0036
import mytest0031
import mytest0033
import mytest0135
import mytest0130
import mytest0131
import mytest0420
import mytest0246
import mytest0408
import mytest0247
import mytest0417
import mytest0326
import mytest0249
import mytest0442
import mytest0323
import mytest0520
import mytest0248
import mytest0394
import mytest0205
import mytest0395
import mytest0431
import mytest0433
import mytest0432
import mytest0434
import mytest0208
import mytest0436
import mytest0048
import mytest0049
import mytest0125
import mytest0124
import mytest0123
import mytest0122
import mytest0121
import mytest0120
import mytest0040
import mytest0041
import mytest0042
import mytest0043
import mytest0044
import mytest0045
import mytest0046
import mytest0047
import mytest0841
import mytest0844
import mytest0158
import mytest0845
import mytest0393
import mytest0228
import mytest0591
import mytest0219
import mytest0218
import mytest0259
import mytest0678
import mytest0409
import mytest0213
import mytest0215
import mytest0214
import mytest0216
import mytest0118
import mytest0119
import mytest0448
import mytest0112
import mytest0113
import mytest0110
import mytest0111
import mytest0116
import mytest0117
import mytest0114
import mytest0115
import mytest0523
import mytest0059
import mytest0058
import mytest0150
import mytest0297
import mytest0296
import mytest0053
import mytest0052
import mytest0051
import mytest0050
import mytest0057
import mytest0056
import mytest0055
import mytest0054
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
    
def test001(desc="""test0001"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0001._init(_testmgr)
    _testmgr.testcase_end(desc)

def test002(desc="""test0002"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0002._init(_testmgr)
    _testmgr.testcase_end(desc)

def test003(desc="""test0003"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0003._init(_testmgr)
    _testmgr.testcase_end(desc)

def test004(desc="""test0004"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0004._init(_testmgr)
    _testmgr.testcase_end(desc)

def test005(desc="""test0005"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0005._init(_testmgr)
    _testmgr.testcase_end(desc)

def test006(desc="""test0008"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0008._init(_testmgr)
    _testmgr.testcase_end(desc)

def test007(desc="""test0009"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0009._init(_testmgr)
    _testmgr.testcase_end(desc)

def test008(desc="""test0011"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0011._init(_testmgr)
    _testmgr.testcase_end(desc)

def test009(desc="""test0016"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0016._init(_testmgr)
    _testmgr.testcase_end(desc)

def test010(desc="""test0017"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0017._init(_testmgr)
    _testmgr.testcase_end(desc)

def test011(desc="""test0018"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0018._init(_testmgr)
    _testmgr.testcase_end(desc)

def test012(desc="""test0019"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0019._init(_testmgr)
    _testmgr.testcase_end(desc)

def test013(desc="""test0020"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0020._init(_testmgr)
    _testmgr.testcase_end(desc)

def test014(desc="""test0022"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0022._init(_testmgr)
    _testmgr.testcase_end(desc)

def test015(desc="""test0023"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0023._init(_testmgr)
    _testmgr.testcase_end(desc)

def test016(desc="""test0024"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0024._init(_testmgr)
    _testmgr.testcase_end(desc)

def test017(desc="""test0025"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0025._init(_testmgr)
    _testmgr.testcase_end(desc)

def test018(desc="""test0026"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0026._init(_testmgr)
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

def test025(desc="""test0036"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0036._init(_testmgr)
    _testmgr.testcase_end(desc)

def test026(desc="""test0037"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0037._init(_testmgr)
    _testmgr.testcase_end(desc)

def test027(desc="""test0038"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0038._init(_testmgr)
    _testmgr.testcase_end(desc)

def test028(desc="""test0039"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0039._init(_testmgr)
    _testmgr.testcase_end(desc)

def test029(desc="""test0040"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0040._init(_testmgr)
    _testmgr.testcase_end(desc)

def test030(desc="""test0041"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0041._init(_testmgr)
    _testmgr.testcase_end(desc)

def test031(desc="""test0042"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0042._init(_testmgr)
    _testmgr.testcase_end(desc)

def test032(desc="""test0043"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0043._init(_testmgr)
    _testmgr.testcase_end(desc)

def test033(desc="""test0044"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0044._init(_testmgr)
    _testmgr.testcase_end(desc)

def test034(desc="""test0045"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0045._init(_testmgr)
    _testmgr.testcase_end(desc)

def test035(desc="""test0046"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0046._init(_testmgr)
    _testmgr.testcase_end(desc)

def test036(desc="""test0047"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0047._init(_testmgr)
    _testmgr.testcase_end(desc)

def test037(desc="""test0048"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0048._init(_testmgr)
    _testmgr.testcase_end(desc)

def test038(desc="""test0049"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0049._init(_testmgr)
    _testmgr.testcase_end(desc)

def test039(desc="""test0050"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0050._init(_testmgr)
    _testmgr.testcase_end(desc)

def test040(desc="""test0051"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0051._init(_testmgr)
    _testmgr.testcase_end(desc)

def test041(desc="""test0052"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0052._init(_testmgr)
    _testmgr.testcase_end(desc)

def test042(desc="""test0053"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0053._init(_testmgr)
    _testmgr.testcase_end(desc)

def test043(desc="""test0054"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0054._init(_testmgr)
    _testmgr.testcase_end(desc)

def test044(desc="""test0055"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0055._init(_testmgr)
    _testmgr.testcase_end(desc)

def test045(desc="""test0056"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0056._init(_testmgr)
    _testmgr.testcase_end(desc)

def test046(desc="""test0057"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0057._init(_testmgr)
    _testmgr.testcase_end(desc)

def test047(desc="""test0058"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0058._init(_testmgr)
    _testmgr.testcase_end(desc)

def test048(desc="""test0059"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0059._init(_testmgr)
    _testmgr.testcase_end(desc)

def test049(desc="""test0061"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0061._init(_testmgr)
    _testmgr.testcase_end(desc)

def test050(desc="""test0062"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0062._init(_testmgr)
    _testmgr.testcase_end(desc)

def test051(desc="""test0064"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0064._init(_testmgr)
    _testmgr.testcase_end(desc)

def test052(desc="""test0065"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0065._init(_testmgr)
    _testmgr.testcase_end(desc)

def test053(desc="""test0066"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0066._init(_testmgr)
    _testmgr.testcase_end(desc)

def test054(desc="""test0069"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0069._init(_testmgr)
    _testmgr.testcase_end(desc)

def test055(desc="""test0070"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0070._init(_testmgr)
    _testmgr.testcase_end(desc)

def test056(desc="""test0071"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0071._init(_testmgr)
    _testmgr.testcase_end(desc)

def test057(desc="""test0072"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0072._init(_testmgr)
    _testmgr.testcase_end(desc)

def test058(desc="""test0073"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0073._init(_testmgr)
    _testmgr.testcase_end(desc)

def test059(desc="""test0074"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0074._init(_testmgr)
    _testmgr.testcase_end(desc)

def test060(desc="""test0075"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0075._init(_testmgr)
    _testmgr.testcase_end(desc)

def test061(desc="""test0076"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0076._init(_testmgr)
    _testmgr.testcase_end(desc)

def test062(desc="""test0077"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0077._init(_testmgr)
    _testmgr.testcase_end(desc)

def test063(desc="""test0078"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0078._init(_testmgr)
    _testmgr.testcase_end(desc)

def test064(desc="""test0079"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0079._init(_testmgr)
    _testmgr.testcase_end(desc)

def test065(desc="""test0080"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0080._init(_testmgr)
    _testmgr.testcase_end(desc)

def test066(desc="""test0081"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0081._init(_testmgr)
    _testmgr.testcase_end(desc)

def test067(desc="""test0082"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0082._init(_testmgr)
    _testmgr.testcase_end(desc)

def test068(desc="""test0083"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0083._init(_testmgr)
    _testmgr.testcase_end(desc)

def test069(desc="""test0084"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """drop table seven_types;"""
    output = _dci.cmdexec(stmt)
    mytest0084._init(_testmgr)
    _testmgr.testcase_end(desc)

def test070(desc="""test0085"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0085._init(_testmgr)
    _testmgr.testcase_end(desc)

def test071(desc="""test0086"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0086._init(_testmgr)
    _testmgr.testcase_end(desc)

def test072(desc="""test0087"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0087._init(_testmgr)
    _testmgr.testcase_end(desc)

def test073(desc="""test0088"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0088._init(_testmgr)
    _testmgr.testcase_end(desc)

def test074(desc="""test0089"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0089._init(_testmgr)
    _testmgr.testcase_end(desc)

def test075(desc="""test0090"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0090._init(_testmgr)
    _testmgr.testcase_end(desc)

def test076(desc="""test0091"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0091._init(_testmgr)
    _testmgr.testcase_end(desc)

def test077(desc="""test0092"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0092._init(_testmgr)
    _testmgr.testcase_end(desc)

def test078(desc="""test0093"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0093._init(_testmgr)
    _testmgr.testcase_end(desc)

def test079(desc="""test0094"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0094._init(_testmgr)
    _testmgr.testcase_end(desc)

def test080(desc="""test0095"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0095._init(_testmgr)
    _testmgr.testcase_end(desc)

def test081(desc="""test0096"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0096._init(_testmgr)
    _testmgr.testcase_end(desc)

def test082(desc="""test0097"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0097._init(_testmgr)
    _testmgr.testcase_end(desc)

def test083(desc="""test0098"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0098._init(_testmgr)
    _testmgr.testcase_end(desc)

def test084(desc="""test0099"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0099._init(_testmgr)
    _testmgr.testcase_end(desc)

def test085(desc="""test0100"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0100._init(_testmgr)
    _testmgr.testcase_end(desc)

def test086(desc="""test0101"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0101._init(_testmgr)
    _testmgr.testcase_end(desc)

def test087(desc="""test0102"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0102._init(_testmgr)
    _testmgr.testcase_end(desc)

def test088(desc="""test0104"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0104._init(_testmgr)
    _testmgr.testcase_end(desc)

def test089(desc="""test0103"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0103._init(_testmgr)
    _testmgr.testcase_end(desc)

def test090(desc="""test0105"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0105._init(_testmgr)
    _testmgr.testcase_end(desc)

def test091(desc="""test0106"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0106._init(_testmgr)
    _testmgr.testcase_end(desc)

def test092(desc="""test0107"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0107._init(_testmgr)
    _testmgr.testcase_end(desc)

def test093(desc="""test0108"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0108._init(_testmgr)
    _testmgr.testcase_end(desc)

def test094(desc="""test0109"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0109._init(_testmgr)
    _testmgr.testcase_end(desc)

def test095(desc="""test0110"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0110._init(_testmgr)
    _testmgr.testcase_end(desc)

def test096(desc="""test0111"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0111._init(_testmgr)
    _testmgr.testcase_end(desc)

def test097(desc="""test0112"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0112._init(_testmgr)
    _testmgr.testcase_end(desc)

def test098(desc="""test0113"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0113._init(_testmgr)
    _testmgr.testcase_end(desc)

def test099(desc="""test0114"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0114._init(_testmgr)
    _testmgr.testcase_end(desc)

def test100(desc="""test0115"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0115._init(_testmgr)
    _testmgr.testcase_end(desc)

def test101(desc="""test0116"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0116._init(_testmgr)
    _testmgr.testcase_end(desc)

def test102(desc="""test0117"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0117._init(_testmgr)
    _testmgr.testcase_end(desc)

def test103(desc="""test0118"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0118._init(_testmgr)
    _testmgr.testcase_end(desc)

def test104(desc="""test0119"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0119._init(_testmgr)
    _testmgr.testcase_end(desc)

def test105(desc="""test0120"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0120._init(_testmgr)
    _testmgr.testcase_end(desc)

def test106(desc="""test0121"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0121._init(_testmgr)
    _testmgr.testcase_end(desc)

def test107(desc="""test0122"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0122._init(_testmgr)
    _testmgr.testcase_end(desc)

def test108(desc="""test0123"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0123._init(_testmgr)
    _testmgr.testcase_end(desc)

def test109(desc="""test0124"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0124._init(_testmgr)
    _testmgr.testcase_end(desc)

def test110(desc="""test0125"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0125._init(_testmgr)
    _testmgr.testcase_end(desc)

def test111(desc="""test0129"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0129._init(_testmgr)
    _testmgr.testcase_end(desc)

def test112(desc="""test0130"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0130._init(_testmgr)
    _testmgr.testcase_end(desc)

def test113(desc="""test0131"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0131._init(_testmgr)
    _testmgr.testcase_end(desc)

def test114(desc="""test0135"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0135._init(_testmgr)
    _testmgr.testcase_end(desc)

def test115(desc="""test0145"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0145._init(_testmgr)
    _testmgr.testcase_end(desc)

def test116(desc="""test0148"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0148._init(_testmgr)
    _testmgr.testcase_end(desc)

def test117(desc="""test0149"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0149._init(_testmgr)
    _testmgr.testcase_end(desc)

def test118(desc="""test0150"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0150._init(_testmgr)
    _testmgr.testcase_end(desc)

def test119(desc="""test0151"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0151._init(_testmgr)
    _testmgr.testcase_end(desc)

def test120(desc="""test0152"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0152._init(_testmgr)
    _testmgr.testcase_end(desc)

def test121(desc="""test0153"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0153._init(_testmgr)
    _testmgr.testcase_end(desc)

def test122(desc="""test0155"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0155._init(_testmgr)
    _testmgr.testcase_end(desc)

def test123(desc="""test0156"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0156._init(_testmgr)
    _testmgr.testcase_end(desc)

def test124(desc="""test0157"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0157._init(_testmgr)
    _testmgr.testcase_end(desc)

def test125(desc="""test0158"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0158._init(_testmgr)
    _testmgr.testcase_end(desc)

def test126(desc="""test0159"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0159._init(_testmgr)
    _testmgr.testcase_end(desc)

def test127(desc="""test0160"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0160._init(_testmgr)
    _testmgr.testcase_end(desc)

def test128(desc="""test0164"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0164._init(_testmgr)
    _testmgr.testcase_end(desc)

def test129(desc="""test0167"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0167._init(_testmgr)
    _testmgr.testcase_end(desc)

def test130(desc="""test0168"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0168._init(_testmgr)
    _testmgr.testcase_end(desc)

def test131(desc="""test0169"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0169._init(_testmgr)
    _testmgr.testcase_end(desc)

def test132(desc="""test0170"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0170._init(_testmgr)
    _testmgr.testcase_end(desc)

def test133(desc="""test0171"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0171._init(_testmgr)
    _testmgr.testcase_end(desc)

def test134(desc="""test0172"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0172._init(_testmgr)
    _testmgr.testcase_end(desc)

def test135(desc="""test0173"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0173._init(_testmgr)
    _testmgr.testcase_end(desc)

def test136(desc="""test0174"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0174._init(_testmgr)
    _testmgr.testcase_end(desc)

def test137(desc="""test0175"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0175._init(_testmgr)
    _testmgr.testcase_end(desc)

def test138(desc="""test0176"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0176._init(_testmgr)
    _testmgr.testcase_end(desc)

def test139(desc="""test0177"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0177._init(_testmgr)
    _testmgr.testcase_end(desc)

def test140(desc="""test0178"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0178._init(_testmgr)
    _testmgr.testcase_end(desc)

def test141(desc="""test0179"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0179._init(_testmgr)
    _testmgr.testcase_end(desc)

def test142(desc="""test0180"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0180._init(_testmgr)
    _testmgr.testcase_end(desc)

def test143(desc="""test0181"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0181._init(_testmgr)
    _testmgr.testcase_end(desc)

def test144(desc="""test0182"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0182._init(_testmgr)
    _testmgr.testcase_end(desc)

def test145(desc="""test0205"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0205._init(_testmgr)
    _testmgr.testcase_end(desc)

def test146(desc="""test0208"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0208._init(_testmgr)
    _testmgr.testcase_end(desc)

def test147(desc="""test0213"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0213._init(_testmgr)
    _testmgr.testcase_end(desc)

def test148(desc="""test0214"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0214._init(_testmgr)
    _testmgr.testcase_end(desc)

def test149(desc="""test0215"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0215._init(_testmgr)
    _testmgr.testcase_end(desc)

def test150(desc="""test0216"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0216._init(_testmgr)
    _testmgr.testcase_end(desc)

def test151(desc="""test0218"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0218._init(_testmgr)
    _testmgr.testcase_end(desc)

def test152(desc="""test0219"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0219._init(_testmgr)
    _testmgr.testcase_end(desc)

def test153(desc="""test0220"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0220._init(_testmgr)
    _testmgr.testcase_end(desc)

def test154(desc="""test0221"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0221._init(_testmgr)
    _testmgr.testcase_end(desc)

def test155(desc="""test0222"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0222._init(_testmgr)
    _testmgr.testcase_end(desc)

def test156(desc="""test0225"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0225._init(_testmgr)
    _testmgr.testcase_end(desc)

def test157(desc="""test0226"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0226._init(_testmgr)
    _testmgr.testcase_end(desc)

def test158(desc="""test0227"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0227._init(_testmgr)
    _testmgr.testcase_end(desc)

def test159(desc="""test0228"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0228._init(_testmgr)
    _testmgr.testcase_end(desc)

def test160(desc="""test0229"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0229._init(_testmgr)
    _testmgr.testcase_end(desc)

def test161(desc="""test0233"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0233._init(_testmgr)
    _testmgr.testcase_end(desc)

def test162(desc="""test0234"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0234._init(_testmgr)
    _testmgr.testcase_end(desc)

def test163(desc="""test0237"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0237._init(_testmgr)
    _testmgr.testcase_end(desc)

def test164(desc="""test0243"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0243._init(_testmgr)
    _testmgr.testcase_end(desc)

def test165(desc="""test0244"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0244._init(_testmgr)
    _testmgr.testcase_end(desc)

def test166(desc="""test0245"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0245._init(_testmgr)
    _testmgr.testcase_end(desc)

def test167(desc="""test0246"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0246._init(_testmgr)
    _testmgr.testcase_end(desc)

def test168(desc="""test0247"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0247._init(_testmgr)
    _testmgr.testcase_end(desc)

def test169(desc="""test0248"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0248._init(_testmgr)
    _testmgr.testcase_end(desc)

def test170(desc="""test0249"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0249._init(_testmgr)
    _testmgr.testcase_end(desc)

def test171(desc="""test0250"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0250._init(_testmgr)
    _testmgr.testcase_end(desc)

def test172(desc="""test0251"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0251._init(_testmgr)
    _testmgr.testcase_end(desc)

def test173(desc="""test0252"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0252._init(_testmgr)
    _testmgr.testcase_end(desc)

def test174(desc="""test0253"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0253._init(_testmgr)
    _testmgr.testcase_end(desc)

def test175(desc="""test0254"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0254._init(_testmgr)
    _testmgr.testcase_end(desc)

def test176(desc="""test0257"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0257._init(_testmgr)
    _testmgr.testcase_end(desc)

def test177(desc="""test0258"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0258._init(_testmgr)
    _testmgr.testcase_end(desc)

def test178(desc="""test0259"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0259._init(_testmgr)
    _testmgr.testcase_end(desc)

def test179(desc="""test0260"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0260._init(_testmgr)
    _testmgr.testcase_end(desc)

def test180(desc="""test0261"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0261._init(_testmgr)
    _testmgr.testcase_end(desc)

def test181(desc="""test0262"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0262._init(_testmgr)
    _testmgr.testcase_end(desc)

def test182(desc="""test0263"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0263._init(_testmgr)
    _testmgr.testcase_end(desc)

def test183(desc="""test0264"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0264._init(_testmgr)
    _testmgr.testcase_end(desc)

def test184(desc="""test0267"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0267._init(_testmgr)
    _testmgr.testcase_end(desc)

def test185(desc="""test0269"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0269._init(_testmgr)
    _testmgr.testcase_end(desc)

def test186(desc="""test0270"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0270._init(_testmgr)
    _testmgr.testcase_end(desc)

def test187(desc="""test0271"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0271._init(_testmgr)
    _testmgr.testcase_end(desc)

def test188(desc="""test0272"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0272._init(_testmgr)
    _testmgr.testcase_end(desc)

def test189(desc="""test0273"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0273._init(_testmgr)
    _testmgr.testcase_end(desc)

def test190(desc="""test0275"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0275._init(_testmgr)
    _testmgr.testcase_end(desc)

def test191(desc="""test0277"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0277._init(_testmgr)
    _testmgr.testcase_end(desc)

def test192(desc="""test0279"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0279._init(_testmgr)
    _testmgr.testcase_end(desc)

def test193(desc="""test0284"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0284._init(_testmgr)
    _testmgr.testcase_end(desc)

def test194(desc="""test0285"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0285._init(_testmgr)
    _testmgr.testcase_end(desc)

def test195(desc="""test0296"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0296._init(_testmgr)
    _testmgr.testcase_end(desc)

def test196(desc="""test0297"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0297._init(_testmgr)
    _testmgr.testcase_end(desc)

def test197(desc="""test0299"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0299._init(_testmgr)
    _testmgr.testcase_end(desc)

def test198(desc="""test0300"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0300._init(_testmgr)
    _testmgr.testcase_end(desc)

def test199(desc="""test0302"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0302._init(_testmgr)
    _testmgr.testcase_end(desc)

def test200(desc="""test0303"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0303._init(_testmgr)
    _testmgr.testcase_end(desc)

def test201(desc="""test0304"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0304._init(_testmgr)
    _testmgr.testcase_end(desc)

def test202(desc="""test0305"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0305._init(_testmgr)
    _testmgr.testcase_end(desc)

def test203(desc="""test0323"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0323._init(_testmgr)
    _testmgr.testcase_end(desc)

def test204(desc="""test0326"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0326._init(_testmgr)
    _testmgr.testcase_end(desc)

def test205(desc="""test0331"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0331._init(_testmgr)
    _testmgr.testcase_end(desc)

def test206(desc="""test0389"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0389._init(_testmgr)
    _testmgr.testcase_end(desc)

def test207(desc="""test0393"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0393._init(_testmgr)
    _testmgr.testcase_end(desc)

def test208(desc="""test0394"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0394._init(_testmgr)
    _testmgr.testcase_end(desc)

def test209(desc="""test0395"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0395._init(_testmgr)
    _testmgr.testcase_end(desc)

def test210(desc="""test0396"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0396._init(_testmgr)
    _testmgr.testcase_end(desc)

def test211(desc="""test0397"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0397._init(_testmgr)
    _testmgr.testcase_end(desc)

def test212(desc="""test0408"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0408._init(_testmgr)
    _testmgr.testcase_end(desc)

def test213(desc="""test0409"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0409._init(_testmgr)
    _testmgr.testcase_end(desc)

def test214(desc="""test0411"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0411._init(_testmgr)
    _testmgr.testcase_end(desc)

def test215(desc="""test0412"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0412._init(_testmgr)
    _testmgr.testcase_end(desc)

def test216(desc="""test0417"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0417._init(_testmgr)
    _testmgr.testcase_end(desc)

def test217(desc="""test0418"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0418._init(_testmgr)
    _testmgr.testcase_end(desc)

def test218(desc="""test0419"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0419._init(_testmgr)
    _testmgr.testcase_end(desc)

def test219(desc="""test0420"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0420._init(_testmgr)
    _testmgr.testcase_end(desc)

def test220(desc="""test0431"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0431._init(_testmgr)
    _testmgr.testcase_end(desc)

def test221(desc="""test0432"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0432._init(_testmgr)
    _testmgr.testcase_end(desc)

def test222(desc="""test0433"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0433._init(_testmgr)
    _testmgr.testcase_end(desc)

def test223(desc="""test0434"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0434._init(_testmgr)
    _testmgr.testcase_end(desc)

def test224(desc="""test0436"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0436._init(_testmgr)
    _testmgr.testcase_end(desc)

def test225(desc="""test0442"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0442._init(_testmgr)
    _testmgr.testcase_end(desc)

def test226(desc="""test0448"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0448._init(_testmgr)
    _testmgr.testcase_end(desc)

def test227(desc="""test0452"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0452._init(_testmgr)
    _testmgr.testcase_end(desc)

def test228(desc="""test0453"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0453._init(_testmgr)
    _testmgr.testcase_end(desc)

def test229(desc="""test0454"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0454._init(_testmgr)
    _testmgr.testcase_end(desc)

def test230(desc="""test0455"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0455._init(_testmgr)
    _testmgr.testcase_end(desc)

def test231(desc="""test0487"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0487._init(_testmgr)
    _testmgr.testcase_end(desc)

def test232(desc="""test0489"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0489._init(_testmgr)
    _testmgr.testcase_end(desc)

def test233(desc="""test0492"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0492._init(_testmgr)
    _testmgr.testcase_end(desc)

def test234(desc="""test0493"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0493._init(_testmgr)
    _testmgr.testcase_end(desc)

def test235(desc="""test0494"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0494._init(_testmgr)
    _testmgr.testcase_end(desc)

def test236(desc="""test0509"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0509._init(_testmgr)
    _testmgr.testcase_end(desc)

def test237(desc="""test0512"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0512._init(_testmgr)
    _testmgr.testcase_end(desc)

def test238(desc="""test0518"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0518._init(_testmgr)
    _testmgr.testcase_end(desc)

def test239(desc="""test0520"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0520._init(_testmgr)
    _testmgr.testcase_end(desc)

def test240(desc="""test0523"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0523._init(_testmgr)
    _testmgr.testcase_end(desc)

def test241(desc="""test0524"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0524._init(_testmgr)
    _testmgr.testcase_end(desc)

def test242(desc="""test0564"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0564._init(_testmgr)
    _testmgr.testcase_end(desc)

def test243(desc="""test0591"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """drop table groups1 cascade;"""
    mytest0591._init(_testmgr)
    _testmgr.testcase_end(desc)

def test244(desc="""test0611"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0611._init(_testmgr)
    _testmgr.testcase_end(desc)

def test245(desc="""test0613"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0613._init(_testmgr)
    _testmgr.testcase_end(desc)

def test246(desc="""test0678"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0678._init(_testmgr)
    _testmgr.testcase_end(desc)

def test247(desc="""test0691"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0691._init(_testmgr)
    _testmgr.testcase_end(desc)

def test248(desc="""test0839"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0839._init(_testmgr)
    _testmgr.testcase_end(desc)

def test249(desc="""test0841"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0841._init(_testmgr)
    _testmgr.testcase_end(desc)

def test250(desc="""test0845"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    mytest0845._init(_testmgr)
    _testmgr.testcase_end(desc)

def test251(desc="""test0844"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """drop table seven_types cascade;"""
    output = _dci.cmdexec(stmt)
    mytest0844._init(_testmgr)
    _testmgr.testcase_end(desc)

