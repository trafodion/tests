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
    
    stmt = """set param ?CFTMLOW1    'a';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?CFTMLOW2    'b';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?CFTMLOW3  'c';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?CFTMHIGH1   'd';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?CFTMHIGH2   'e';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?CFTMHIGH3 'f';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?SDNO1LOW11  'a';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?SDNO1LOW12  'b';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?SDNO1HIGH11 'd';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?SDNO1HIGH12 'e';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?SDNO2LOW11  'a';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?SDNO2LOW12  'b';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?SDNO2HIGH11 'd';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?SDNO2HIGH12 'e';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?CFDAYLOW  '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?ORNLOW    '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?PNLOW     '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?RDGTLOW   '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?SPNLOW    '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?CCSLOW    '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?CIDLOW    '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?CLNLOW    '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?CLTLOW    '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?CNLOW     '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?CN0LOW    '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?CN1LOW    '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?ISRTALOW  '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?OSRTALOW  '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?NNPLOW    '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?ORCLOW    '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?OSCLOW    '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?PFXCLOW   '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?RDCLOW    '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?SCSLOW    '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?SPCLOW    '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?SSCLOW    '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?TN0LOW    '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?TN1LOW    '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?ANDAYLOW  '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?ANTMLOW   '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?CBTMLOW   '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?CCLSLOW   '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?CGFLOW    '%x';"""
    output = _dci.cmdexec(stmt)
    #set param                    ?CHGCLOW   '%x';
    stmt = """set param                    ?CHKLOW    '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?CLR1LOW   '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?CLR2LOW   '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?CPILOW    '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?DCCLOW    '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?FLTLOW    '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?FSCLOW    '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?GWLOW     '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?ICILOW    '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?IDSTALOW  '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?IDSTNLOW  '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?IOLOW     '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?IRTALOW   '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?ISGLOW    '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?ISRTNLOW  '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?ISTNLOW   '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?MALOW     '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?ODSTALOW  '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?ODSTNLOW  '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?OGTMLOW   '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?ORTALOW   '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?ORDAYLOW  '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?ORTMLOW   '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?OSGLOW    '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?OSTNLOW   '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?RAILOW    '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?SUBLOW    '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?TMRLOW    '%x';"""
    output = _dci.cmdexec(stmt)
    #set param                    ?UUIRLOW   '%x';
    #set param                    ?UUISLOW   '%x';
    stmt = """set param                    ?VDLOW     '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?VDTLOW    '%x';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param                    ?VRTALOW   '%x';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
SELECT  SDNO1   ,
SDNO2   ,
CFDAY   ,
CFTM1   ,
CFTM2   ,
CFTM3   ,
ORN     ,
PN      ,
RDGT    ,
SPN     ,
CCS     ,
CID     ,
CLN     ,
CLT     ,
CN      ,
CN0     ,
CN1     ,
ISRTA   ,
NNP     ,
ORC     ,
OSC     ,
OSRTA   ,
PFXC    ,
RDC     ,
SCS     ,
SPC     ,
SSC     ,
TN0     ,
TN1     ,
ANDAY   ,
ANTM    ,
CBTM    ,
CCLS    ,
CGF     ,
CHGC    ,
CHK     ,
CLR1    ,
CLR2    ,
CPI     ,
DCC     ,
FLT     ,
FSC     ,
GW      ,
ICI     ,
IDSTA   ,
IDSTN   ,
IO      ,
IRTA    ,
ISG     ,
ISRTN   ,
ISTN    ,
MA      ,
ODSTA   ,
ODSTN   ,
OGTM   ,
ORTA    ,
ORDAY   ,
ORTM    ,
OSG     ,
OSTN    ,
RAI     ,
SUB     ,
TMR     ,
UUIR    ,
UUIS    ,
VD      ,
VDT     ,
VRTA
FROM   s0804ta 
WHERE  (CFTM1,CFTM2,CFTM3)
BETWEEN (?CFTMLOW1,?CFTMLOW2,?CFTMLOW3)    AND
(?CFTMHIGH1,?CFTMHIGH2,?CFTMHIGH3) AND
((SDNO1,SDNO2)
BETWEEN (?SDNO1LOW11,?SDNO2LOW12)
AND (?SDNO1HIGH11,?SDNO2HIGH12)
AND
CFDAY  LIKE     ?CFDAYLOW                     AND
ORN    LIKE     ?ORNLOW                       AND
PN     LIKE     ?PNLOW                        AND
RDGT   LIKE     ?RDGTLOW                      AND
SPN    LIKE     ?SPNLOW                       AND
CCS    LIKE     ?CCSLOW                       AND
CID    LIKE     ?CIDLOW                       AND
CLN    LIKE     ?CLNLOW                       AND
CLT    LIKE     ?CLTLOW                       AND
CN     LIKE     ?CNLOW                        AND
(CN0    LIKE     ?CN0LOW                       OR
CN1    LIKE     ?CN1LOW)                      AND
(ISRTA  LIKE     ?ISRTALOW                     OR
OSRTA  LIKE     ?OSRTALOW)                    AND
NNP    LIKE     ?NNPLOW                       AND
ORC    LIKE     ?ORCLOW                       AND
OSC    LIKE     ?OSCLOW                       AND
PFXC   LIKE     ?PFXCLOW                      AND
RDC    LIKE     ?RDCLOW                       AND
SCS    LIKE     ?SCSLOW                       AND
SPC    LIKE     ?SPCLOW                       AND
SSC    LIKE     ?SSCLOW                       AND
(TN0    LIKE     ?TN0LOW                       OR
TN1    LIKE     ?TN1LOW)                      AND
ANDAY  LIKE     ?ANDAYLOW                     AND
ANTM   LIKE     ?ANTMLOW                      AND
CBTM   LIKE     ?CBTMLOW                      AND
CCLS   LIKE     ?CCLSLOW                      AND
CGF    LIKE     ?CGFLOW                       AND
--             CHGC   LIKE     ?CHGCLOW                      AND
CHK    LIKE     ?CHKLOW                       AND
CLR1   LIKE     ?CLR1LOW                      AND
CLR2   LIKE     ?CLR2LOW                      AND
CPI    LIKE     ?CPILOW                       AND
DCC    LIKE     ?DCCLOW                       AND
FLT    LIKE     ?FLTLOW                       AND
FSC    LIKE     ?FSCLOW                       AND
GW     LIKE     ?GWLOW                        AND
ICI    LIKE     ?ICILOW                       AND
IDSTA  LIKE     ?IDSTALOW                     AND
IDSTN  LIKE     ?IDSTNLOW                     AND
IO     LIKE     ?IOLOW                        AND
IRTA   LIKE     ?IRTALOW                      AND
ISG    LIKE     ?ISGLOW                       AND
ISRTN  LIKE     ?ISRTNLOW                     AND
ISTN   LIKE     ?ISTNLOW                      AND
MA     LIKE     ?MALOW                        AND
ODSTA  LIKE     ?ODSTALOW                     AND
ODSTN  LIKE     ?ODSTNLOW                     AND
OGTM   LIKE     ?OGTMLOW                      AND
ORTA   LIKE     ?ORTALOW                      AND
ORDAY  LIKE     ?ORDAYLOW                     AND
ORTM   LIKE     ?ORTMLOW                      AND
OSG    LIKE     ?OSGLOW                       AND
OSTN   LIKE     ?OSTNLOW                      AND
RAI    LIKE     ?RAILOW                       AND
SUB    LIKE     ?SUBLOW                       AND
TMR    LIKE     ?TMRLOW                       AND
--             UUIR   LIKE     ?UUIRLOW                      AND
--             UUIS   LIKE     ?UUISLOW                      AND
VD     LIKE     ?VDLOW                        AND
VDT    LIKE     ?VDTLOW                       AND
VRTA   LIKE     ?VRTALOW)                     OR
--
((SDNO1,SDNO2)
BETWEEN (?SDNO1LOW11,?SDNO2LOW12)
AND (?SDNO1HIGH11,?SDNO2HIGH12)
AND
CFDAY  LIKE     ?CFDAYLOW                     AND
ORN    LIKE     ?ORNLOW                       AND
PN     LIKE     ?PNLOW                        AND
RDGT   LIKE     ?RDGTLOW                      AND
SPN    LIKE     ?SPNLOW                       AND
CCS    LIKE     ?CCSLOW                       AND
CID    LIKE     ?CIDLOW                       AND
CLN    LIKE     ?CLNLOW                       AND
CLT    LIKE     ?CLTLOW                       AND
CN     LIKE     ?CNLOW                        AND
(CN0    LIKE     ?CN0LOW                       OR
CN1    LIKE     ?CN1LOW)                      AND
(ISRTA  LIKE     ?ISRTALOW                     OR
OSRTA  LIKE     ?OSRTALOW)                    AND
NNP    LIKE     ?NNPLOW                       AND
ORC    LIKE     ?ORCLOW                       AND
OSC    LIKE     ?OSCLOW                       AND
PFXC   LIKE     ?PFXCLOW                      AND
RDC    LIKE     ?RDCLOW                       AND
SCS    LIKE     ?SCSLOW                       AND
SPC    LIKE     ?SPCLOW                       AND
SSC    LIKE     ?SSCLOW                       AND
(TN0    LIKE     ?TN0LOW                       OR
TN1    LIKE     ?TN1LOW)                      AND
ANDAY  LIKE     ?ANDAYLOW                     AND
ANTM   LIKE     ?ANTMLOW                      AND
CBTM   LIKE     ?CBTMLOW                      AND
CCLS   LIKE     ?CCLSLOW                      AND
CGF    LIKE     ?CGFLOW                       AND
--             CHGC   LIKE     ?CHGCLOW                      AND
CHK    LIKE     ?CHKLOW                       AND
CLR1   LIKE     ?CLR1LOW                      AND
CLR2   LIKE     ?CLR2LOW                      AND
CPI    LIKE     ?CPILOW                       AND
DCC    LIKE     ?DCCLOW                       AND
FLT    LIKE     ?FLTLOW                       AND
FSC    LIKE     ?FSCLOW                       AND
GW     LIKE     ?GWLOW                        AND
ICI    LIKE     ?ICILOW                       AND
IDSTA  LIKE     ?IDSTALOW                     AND
IDSTN  LIKE     ?IDSTNLOW                     AND
IO     LIKE     ?IOLOW                        AND
IRTA   LIKE     ?IRTALOW                      AND
ISG    LIKE     ?ISGLOW                       AND
ISRTN  LIKE     ?ISRTNLOW                     AND
ISTN   LIKE     ?ISTNLOW                      AND
MA     LIKE     ?MALOW                        AND
ODSTA  LIKE     ?ODSTALOW                     AND
ODSTN  LIKE     ?ODSTNLOW                     AND
OGTM   LIKE     ?OGTMLOW                      AND
ORTA   LIKE     ?ORTALOW                      AND
ORDAY  LIKE     ?ORDAYLOW                     AND
ORTM   LIKE     ?ORTMLOW                      AND
OSG    LIKE     ?OSGLOW                       AND
OSTN   LIKE     ?OSTNLOW                      AND
RAI    LIKE     ?RAILOW                       AND
SUB    LIKE     ?SUBLOW                       AND
TMR    LIKE     ?TMRLOW                       AND
--             UUIR   LIKE     ?UUIRLOW                      AND
--             UUIS   LIKE     ?UUISLOW                      AND
VD     LIKE     ?VDLOW                        AND
VDT    LIKE     ?VDTLOW                       AND
VRTA   LIKE     ?VRTALOW)                     OR
--
((SDNO1,SDNO2)
BETWEEN (?SDNO1LOW11,?SDNO2LOW12)
AND (?SDNO1HIGH11,?SDNO2HIGH12)
AND
CFDAY  LIKE     ?CFDAYLOW                     AND
ORN    LIKE     ?ORNLOW                       AND
PN     LIKE     ?PNLOW                        AND
RDGT   LIKE     ?RDGTLOW                      AND
SPN    LIKE     ?SPNLOW                       AND
CCS    LIKE     ?CCSLOW                       AND
CID    LIKE     ?CIDLOW                       AND
CLN    LIKE     ?CLNLOW                       AND
CLT    LIKE     ?CLTLOW                       AND
CN     LIKE     ?CNLOW                        AND
(CN0    LIKE     ?CN0LOW                       OR
CN1    LIKE     ?CN1LOW)                      AND
(ISRTA  LIKE     ?ISRTALOW                     OR
OSRTA  LIKE     ?OSRTALOW)                    AND
NNP    LIKE     ?NNPLOW                       AND
ORC    LIKE     ?ORCLOW                       AND
OSC    LIKE     ?OSCLOW                       AND
PFXC   LIKE     ?PFXCLOW                      AND
RDC    LIKE     ?RDCLOW                       AND
SCS    LIKE     ?SCSLOW                       AND
SPC    LIKE     ?SPCLOW                       AND
SSC    LIKE     ?SSCLOW                       AND
(TN0    LIKE     ?TN0LOW                       OR
TN1    LIKE     ?TN1LOW)                      AND
ANDAY  LIKE     ?ANDAYLOW                     AND
ANTM   LIKE     ?ANTMLOW                      AND
CBTM   LIKE     ?CBTMLOW                      AND
CCLS   LIKE     ?CCLSLOW                      AND
CGF    LIKE     ?CGFLOW                       AND
--             CHGC   LIKE     ?CHGCLOW                      AND
CHK    LIKE     ?CHKLOW                       AND
CLR1   LIKE     ?CLR1LOW                      AND
CLR2   LIKE     ?CLR2LOW                      AND
CPI    LIKE     ?CPILOW                       AND
DCC    LIKE     ?DCCLOW                       AND
FLT    LIKE     ?FLTLOW                       AND
FSC    LIKE     ?FSCLOW                       AND
GW     LIKE     ?GWLOW                        AND
ICI    LIKE     ?ICILOW                       AND
IDSTA  LIKE     ?IDSTALOW                     AND
IDSTN  LIKE     ?IDSTNLOW                     AND
IO     LIKE     ?IOLOW                        AND
IRTA   LIKE     ?IRTALOW                      AND
ISG    LIKE     ?ISGLOW                       AND
ISRTN  LIKE     ?ISRTNLOW                     AND
ISTN   LIKE     ?ISTNLOW                      AND
MA     LIKE     ?MALOW                        AND
ODSTA  LIKE     ?ODSTALOW                     AND
ODSTN  LIKE     ?ODSTNLOW                     AND
OGTM   LIKE     ?OGTMLOW                      AND
ORTA   LIKE     ?ORTALOW                      AND
ORDAY  LIKE     ?ORDAYLOW                     AND
ORTM   LIKE     ?ORTMLOW                      AND
OSG    LIKE     ?OSGLOW                       AND
OSTN   LIKE     ?OSTNLOW                      AND
RAI    LIKE     ?RAILOW                       AND
SUB    LIKE     ?SUBLOW                       AND
TMR    LIKE     ?TMRLOW                       AND
--             UUIR   LIKE     ?UUIRLOW                      AND
--             UUIS   LIKE     ?UUISLOW                      AND
VD     LIKE     ?VDLOW                        AND
VDT    LIKE     ?VDTLOW                       AND
VRTA   LIKE     ?VRTALOW)                     OR
--
((SDNO1,SDNO2)
BETWEEN (?SDNO1LOW11,?SDNO2LOW12)
AND (?SDNO1HIGH11,?SDNO2HIGH12)
AND
CFDAY  LIKE     ?CFDAYLOW                     AND
ORN    LIKE     ?ORNLOW                       AND
PN     LIKE     ?PNLOW                        AND
RDGT   LIKE     ?RDGTLOW                      AND
SPN    LIKE     ?SPNLOW                       AND
CCS    LIKE     ?CCSLOW                       AND
CID    LIKE     ?CIDLOW                       AND
CLN    LIKE     ?CLNLOW                       AND
CLT    LIKE     ?CLTLOW                       AND
CN     LIKE     ?CNLOW                        AND
(CN0    LIKE     ?CN0LOW                       OR
CN1    LIKE     ?CN1LOW)                      AND
(ISRTA  LIKE     ?ISRTALOW                     OR
OSRTA  LIKE     ?OSRTALOW)                    AND
NNP    LIKE     ?NNPLOW                       AND
ORC    LIKE     ?ORCLOW                       AND
OSC    LIKE     ?OSCLOW                       AND
PFXC   LIKE     ?PFXCLOW                      AND
RDC    LIKE     ?RDCLOW                       AND
SCS    LIKE     ?SCSLOW                       AND
SPC    LIKE     ?SPCLOW                       AND
SSC    LIKE     ?SSCLOW                       AND
(TN0    LIKE     ?TN0LOW                       OR
TN1    LIKE     ?TN1LOW)                      AND
ANDAY  LIKE     ?ANDAYLOW                     AND
ANTM   LIKE     ?ANTMLOW                      AND
CBTM   LIKE     ?CBTMLOW                      AND
CCLS   LIKE     ?CCLSLOW                      AND
CGF    LIKE     ?CGFLOW                       AND
--             CHGC   LIKE     ?CHGCLOW                      AND
CHK    LIKE     ?CHKLOW                       AND
CLR1   LIKE     ?CLR1LOW                      AND
CLR2   LIKE     ?CLR2LOW                      AND
CPI    LIKE     ?CPILOW                       AND
DCC    LIKE     ?DCCLOW                       AND
FLT    LIKE     ?FLTLOW                       AND
FSC    LIKE     ?FSCLOW                       AND
GW     LIKE     ?GWLOW                        AND
ICI    LIKE     ?ICILOW                       AND
IDSTA  LIKE     ?IDSTALOW                     AND
IDSTN  LIKE     ?IDSTNLOW                     AND
IO     LIKE     ?IOLOW                        AND
IRTA   LIKE     ?IRTALOW                      AND
ISG    LIKE     ?ISGLOW                       AND
ISRTN  LIKE     ?ISRTNLOW                     AND
ISTN   LIKE     ?ISTNLOW                      AND
MA     LIKE     ?MALOW                        AND
ODSTA  LIKE     ?ODSTALOW                     AND
ODSTN  LIKE     ?ODSTNLOW                     AND
OGTM   LIKE     ?OGTMLOW                      AND
ORTA   LIKE     ?ORTALOW                      AND
ORDAY  LIKE     ?ORDAYLOW                     AND
ORTM   LIKE     ?ORTMLOW                      AND
OSG    LIKE     ?OSGLOW                       AND
OSTN   LIKE     ?OSTNLOW                      AND
RAI    LIKE     ?RAILOW                       AND
SUB    LIKE     ?SUBLOW                       AND
TMR    LIKE     ?TMRLOW                       AND
--             UUIR   LIKE     ?UUIRLOW                      AND
--             UUIS   LIKE     ?UUISLOW                      AND
VD     LIKE     ?VDLOW                        AND
VDT    LIKE     ?VDTLOW                       AND
VRTA   LIKE     ?VRTALOW)                     OR
--
((SDNO1,SDNO2)
BETWEEN (?SDNO1LOW11,?SDNO2LOW12)
AND (?SDNO1HIGH11,?SDNO2HIGH12)
AND
CFDAY  LIKE     ?CFDAYLOW                     AND
ORN    LIKE     ?ORNLOW                       AND
PN     LIKE     ?PNLOW                        AND
RDGT   LIKE     ?RDGTLOW                      AND
SPN    LIKE     ?SPNLOW                       AND
CCS    LIKE     ?CCSLOW                       AND
CID    LIKE     ?CIDLOW                       AND
CLN    LIKE     ?CLNLOW                       AND
CLT    LIKE     ?CLTLOW                       AND
CN     LIKE     ?CNLOW                        AND
(CN0    LIKE     ?CN0LOW                       OR
CN1    LIKE     ?CN1LOW)                      AND
(ISRTA  LIKE     ?ISRTALOW                     OR
OSRTA  LIKE     ?OSRTALOW)                    AND
NNP    LIKE     ?NNPLOW                       AND
ORC    LIKE     ?ORCLOW                       AND
OSC    LIKE     ?OSCLOW                       AND
PFXC   LIKE     ?PFXCLOW                      AND
RDC    LIKE     ?RDCLOW                       AND
SCS    LIKE     ?SCSLOW                       AND
SPC    LIKE     ?SPCLOW                       AND
SSC    LIKE     ?SSCLOW                       AND
(TN0    LIKE     ?TN0LOW                       OR
TN1    LIKE     ?TN1LOW)                      AND
ANDAY  LIKE     ?ANDAYLOW                     AND
ANTM   LIKE     ?ANTMLOW                      AND
CBTM   LIKE     ?CBTMLOW                      AND
CCLS   LIKE     ?CCLSLOW                      AND
CGF    LIKE     ?CGFLOW                       AND
--             CHGC   LIKE     ?CHGCLOW                      AND
CHK    LIKE     ?CHKLOW                       AND
CLR1   LIKE     ?CLR1LOW                      AND
CLR2   LIKE     ?CLR2LOW                      AND
CPI    LIKE     ?CPILOW                       AND
DCC    LIKE     ?DCCLOW                       AND
FLT    LIKE     ?FLTLOW                       AND
FSC    LIKE     ?FSCLOW                       AND
GW     LIKE     ?GWLOW                        AND
ICI    LIKE     ?ICILOW                       AND
IDSTA  LIKE     ?IDSTALOW                     AND
IDSTN  LIKE     ?IDSTNLOW                     AND
IO     LIKE     ?IOLOW                        AND
IRTA   LIKE     ?IRTALOW                      AND
ISG    LIKE     ?ISGLOW                       AND
ISRTN  LIKE     ?ISRTNLOW                     AND
ISTN   LIKE     ?ISTNLOW                      AND
MA     LIKE     ?MALOW                        AND
ODSTA  LIKE     ?ODSTALOW                     AND
ODSTN  LIKE     ?ODSTNLOW                     AND
OGTM   LIKE     ?OGTMLOW                      AND
ORTA   LIKE     ?ORTALOW                      AND
ORDAY  LIKE     ?ORDAYLOW                     AND
ORTM   LIKE     ?ORTMLOW                      AND
OSG    LIKE     ?OSGLOW                       AND
OSTN   LIKE     ?OSTNLOW                      AND
RAI    LIKE     ?RAILOW                       AND
SUB    LIKE     ?SUBLOW                       AND
TMR    LIKE     ?TMRLOW                       AND
--             UUIR   LIKE     ?UUIRLOW                      AND
--             UUIS   LIKE     ?UUISLOW                      AND
VD     LIKE     ?VDLOW                        AND
VDT    LIKE     ?VDTLOW                       AND
VRTA   LIKE     ?VRTALOW)                     OR
--
((SDNO1,SDNO2)
BETWEEN (?SDNO1LOW11,?SDNO2LOW12)
AND (?SDNO1HIGH11,?SDNO2HIGH12)
AND
CFDAY  LIKE     ?CFDAYLOW                     AND
ORN    LIKE     ?ORNLOW                       AND
PN     LIKE     ?PNLOW                        AND
RDGT   LIKE     ?RDGTLOW                      AND
SPN    LIKE     ?SPNLOW                       AND
CCS    LIKE     ?CCSLOW                       AND
CID    LIKE     ?CIDLOW                       AND
CLN    LIKE     ?CLNLOW                       AND
CLT    LIKE     ?CLTLOW                       AND
CN     LIKE     ?CNLOW                        AND
(CN0    LIKE     ?CN0LOW                       OR
CN1    LIKE     ?CN1LOW)                      AND
(ISRTA  LIKE     ?ISRTALOW                     OR
OSRTA  LIKE     ?OSRTALOW)                    AND
NNP    LIKE     ?NNPLOW                       AND
ORC    LIKE     ?ORCLOW                       AND
OSC    LIKE     ?OSCLOW                       AND
PFXC   LIKE     ?PFXCLOW                      AND
RDC    LIKE     ?RDCLOW                       AND
SCS    LIKE     ?SCSLOW                       AND
SPC    LIKE     ?SPCLOW                       AND
SSC    LIKE     ?SSCLOW                       AND
(TN0    LIKE     ?TN0LOW                       OR
TN1    LIKE     ?TN1LOW)                      AND
ANDAY  LIKE     ?ANDAYLOW                     AND
ANTM   LIKE     ?ANTMLOW                      AND
CBTM   LIKE     ?CBTMLOW                      AND
CCLS   LIKE     ?CCLSLOW                      AND
CGF    LIKE     ?CGFLOW                       AND
--             CHGC   LIKE     ?CHGCLOW                      AND
CHK    LIKE     ?CHKLOW                       AND
CLR1   LIKE     ?CLR1LOW                      AND
CLR2   LIKE     ?CLR2LOW                      AND
CPI    LIKE     ?CPILOW                       AND
DCC    LIKE     ?DCCLOW                       AND
FLT    LIKE     ?FLTLOW                       AND
FSC    LIKE     ?FSCLOW                       AND
GW     LIKE     ?GWLOW                        AND
ICI    LIKE     ?ICILOW                       AND
IDSTA  LIKE     ?IDSTALOW                     AND
IDSTN  LIKE     ?IDSTNLOW                     AND
IO     LIKE     ?IOLOW                        AND
IRTA   LIKE     ?IRTALOW                      AND
ISG    LIKE     ?ISGLOW                       AND
ISRTN  LIKE     ?ISRTNLOW                     AND
ISTN   LIKE     ?ISTNLOW                      AND
MA     LIKE     ?MALOW                        AND
ODSTA  LIKE     ?ODSTALOW                     AND
ODSTN  LIKE     ?ODSTNLOW                     AND
OGTM   LIKE     ?OGTMLOW                      AND
ORTA   LIKE     ?ORTALOW                      AND
ORDAY  LIKE     ?ORDAYLOW                     AND
ORTM   LIKE     ?ORTMLOW                      AND
OSG    LIKE     ?OSGLOW                       AND
OSTN   LIKE     ?OSTNLOW                      AND
RAI    LIKE     ?RAILOW                       AND
SUB    LIKE     ?SUBLOW                       AND
TMR    LIKE     ?TMRLOW                       AND
--             UUIR   LIKE     ?UUIRLOW                      AND
--             UUIS   LIKE     ?UUISLOW                      AND
VD     LIKE     ?VDLOW                        AND
VDT    LIKE     ?VDTLOW                       AND
VRTA   LIKE     ?VRTALOW)
read uncommitted access
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
