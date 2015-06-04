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

# Description: This test verifies 
#              HLDR- Select statement gets Error 8838 saveabend created for MXCMP
#  Test case inputs:  .
#  Test case outputs:
#  History:  Created on 07/01/2006
#

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""Select gets error 8838"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # got rid of expect plan.  plan quality is not the issue here (kk)
    
    stmt = """create table s(
GL_KY                            LARGEINT NO DEFAULT NOT NULL NOT DROPPABLE
, ACCTG_DOC_DT_DAY_KY              LARGEINT DEFAULT NULL
, REV_RECGN_DT_DAY_KY              LARGEINT DEFAULT NULL
, ACCTG_POST_DT_DAY_KY             LARGEINT NO DEFAULT NOT NULL NOT DROPPABLE
, GL_SRC_SYS_KY                    LARGEINT DEFAULT NULL
, GL_LEGL_CO_KY                    LARGEINT NO DEFAULT NOT NULL NOT DROPPABLE
, GL_ACCT_KY                       LARGEINT NO DEFAULT NOT NULL NOT DROPPABLE
, ACCTG_DOC_ID                     CHAR(20) CHARACTER SET ISO88591 COLLATE
DEFAULT DEFAULT NULL
, ACCTG_DOC_ITM_ID                 CHAR(20) CHARACTER SET ISO88591 COLLATE
DEFAULT DEFAULT NULL
, SO_ID                            CHAR(20) CHARACTER SET ISO88591 COLLATE
DEFAULT DEFAULT NULL
, SO_LN_ITM_ID                     CHAR(12) CHARACTER SET ISO88591 COLLATE
DEFAULT DEFAULT NULL
, SO_SRC_SYS_KY                    LARGEINT DEFAULT NULL
, MISC_CHRG_CD_KY                  LARGEINT DEFAULT NULL
, BILL_DOC_ID                      CHAR(20) CHARACTER SET ISO88591 COLLATE
DEFAULT DEFAULT NULL
, BILL_DOC_DTL_LEGL_CO_KY          LARGEINT DEFAULT NULL
, BILL_DOC_DTL_SRC_SYS_KY          LARGEINT DEFAULT NULL
, BILL_DOC_LN_ITM_ID               CHAR(12) CHARACTER SET ISO88591 COLLATE
DEFAULT DEFAULT NULL
, BILL_DOC_DTL_EFF_FRM_GMT_TS      TIMESTAMP(6) DEFAULT NULL
, POST_TYPE_KY                     LARGEINT DEFAULT NULL
, PRFT_CTR_KY                      LARGEINT DEFAULT NULL
, FIN_TXN_GEO_CTRY_KY              LARGEINT DEFAULT NULL
, LC_KY                            LARGEINT DEFAULT NULL
, DOC_CRNCY_KY                     LARGEINT DEFAULT NULL
, ACCTG_DOC_TYPE_KY                LARGEINT DEFAULT NULL
, SLS_ORG_KY                       LARGEINT DEFAULT NULL
, BUS_AREA_KY                      LARGEINT DEFAULT NULL
, CST_CTR_KY                       LARGEINT DEFAULT NULL
, PROJ_KY                          LARGEINT DEFAULT NULL
, WBS_KY                           LARGEINT DEFAULT NULL
, INVN_CLS_KY                      LARGEINT DEFAULT NULL
, VNDR_KY                          LARGEINT DEFAULT NULL
, PROD_KY                          LARGEINT DEFAULT NULL
, PROD_BASE_KY                     LARGEINT DEFAULT NULL
, SRVC_GDS_PROD_KY                 LARGEINT DEFAULT NULL
, BOOK_TYPE_CD                     CHAR(6) CHARACTER SET ISO88591 COLLATE
DEFAULT DEFAULT NULL
, BOOK_ENT_ID                      CHAR(2) CHARACTER SET ISO88591 COLLATE
DEFAULT DEFAULT NULL
, BOOK_SUB_ENT_ID                  CHAR(4) CHARACTER SET ISO88591 COLLATE
DEFAULT DEFAULT NULL
, REF_DOC_ID                       CHAR(50) CHARACTER SET ISO88591 COLLATE
DEFAULT DEFAULT NULL
, PKG_NR_TX                        CHAR(20) CHARACTER SET UCS2 COLLATE
DEFAULT DEFAULT NULL
, GL_TXN_DN                        VARCHAR(100) CHARACTER SET UCS2 COLLATE
DEFAULT DEFAULT NULL
, ACTL_BILLD_QT                    NUMERIC(13, 3) DEFAULT NULL
, LCL_GL_AM                        NUMERIC(17, 3) DEFAULT NULL
, US_GL_AM                         NUMERIC(17, 3) DEFAULT NULL
, DOC_GL_AM                        NUMERIC(17, 3) DEFAULT NULL
, LEG_SO_ID                        CHAR(20) CHARACTER SET ISO88591 COLLATE
DEFAULT DEFAULT NULL
, LEG_SO_LN_ITM_ID                 CHAR(12) CHARACTER SET ISO88591 COLLATE
DEFAULT DEFAULT NULL
, LEG_BILL_DOC_ID                  CHAR(20) CHARACTER SET ISO88591 COLLATE
DEFAULT DEFAULT NULL
, LEG_BILL_DOC_LN_ITM_ID           CHAR(12) CHARACTER SET ISO88591 COLLATE
DEFAULT DEFAULT NULL
, INS_GMT_TS                       TIMESTAMP(6) DEFAULT NULL
, UPD_GMT_TS                       TIMESTAMP(6) DEFAULT NULL
, BILL_DOC_NF_KY                   LARGEINT DEFAULT NULL
, BILL_DOC_DTL_NF_KY               LARGEINT DEFAULT NULL
, GL_NF_KY                         LARGEINT DEFAULT NULL
, LOAD_JOB_NR                      NUMERIC(15, 0) DEFAULT NULL
, LGCL_DEL_FG                      CHAR(1) CHARACTER SET ISO88591 COLLATE
DEFAULT DEFAULT NULL
, REC_ST_NR                        SMALLINT DEFAULT NULL
, MGMT_PNL_KY                      LARGEINT DEFAULT NULL
, MGMT_GEO_KY                      LARGEINT DEFAULT NULL
, FUNC_AREA_KY                     LARGEINT DEFAULT NULL
, EXT_INV_QT                       NUMERIC(13, 3) DEFAULT NULL
, SLDT_CUST_MSTR_SRC_SYS_KY        LARGEINT DEFAULT NULL
, SLDT_CUST_KY                     LARGEINT DEFAULT NULL
, BILT_CUST_MSTR_SRC_SYS_KY        LARGEINT DEFAULT NULL
, BILT_CUST_KY                     LARGEINT DEFAULT NULL
, SHPT_CUST_MSTR_SRC_SYS_KY        LARGEINT DEFAULT NULL
, SHPT_CUST_KY                     LARGEINT DEFAULT NULL
, END_USER_CUST_MSTR_SRC_SYS_KY    LARGEINT DEFAULT NULL
, END_USER_CUST_KY                 LARGEINT DEFAULT NULL
, SO_TYPE_KY                       LARGEINT DEFAULT NULL
, QTA_PROD_LN_KY                   LARGEINT DEFAULT NULL
, SRC_PROD_LN_KY                   LARGEINT DEFAULT NULL
, RTE_TO_MKT_KY                    LARGEINT DEFAULT NULL
, primary key (GL_KY)) attributes extent (16,64);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """prepare xx from select * from S where SO_ID =?;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xy from select count(*) from s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' xy;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from s where SO_ID='abc';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select count (*) from s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '0')
    
    stmt = """create view sv1(v1,v2,v3,v4,v5) as select BUS_AREA_KY,SRC_PROD_LN_KY,RTE_TO_MKT_KY ,FUNC_AREA_KY,PROD_BASE_KY from s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select count(*) from sv1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '0')
    
    stmt = """select (select v1 from sv1 group by v1) from s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    _testmgr.testcase_end(desc)

