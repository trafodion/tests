# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2014-2015 Hewlett-Packard Development Company, L.P.
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

import time
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


# ---------------------------------------------------------
#testcase test001 CREATE SEQUENCE success
# ---------------------------------------------------------
def test001(desc="""CREATE SEQUENCE success"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # create sequence default 
    stmt = """create sequence h_seq_p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl sequence h_seq_p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """CREATE SEQUENCE TRAFODION.SEQUENCE_SEQH01.H_SEQ_P1""")
    _dci.expect_any_substr(output, """START WITH 1 /* NEXT AVAILABLE VALUE 1 */""")
    _dci.expect_any_substr(output, """INCREMENT BY 1""")
    _dci.expect_any_substr(output, """MAXVALUE 9223372036854775806""")
    _dci.expect_any_substr(output, """MINVALUE 1""")
    _dci.expect_any_substr(output, """CACHE 25""")
    _dci.expect_any_substr(output, """NO CYCLE""")
    _dci.expect_any_substr(output, """LARGEINT""")
    _dci.expect_any_substr(output, """;""")

    stmt = """drop sequence h_seq_p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #create sequence specify schema
    stmt = """create schema trafodion.test_seq_sch;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create sequence test_seq_sch.h_seq_p2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """get schemas; """
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'TEST_SEQ_SCH')

    stmt = """showddl sequence test_seq_sch.h_seq_p2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """CREATE SEQUENCE TRAFODION.TEST_SEQ_SCH.H_SEQ_P2""")
    _dci.expect_any_substr(output, """START WITH 1 /* NEXT AVAILABLE VALUE 1 */""")
    _dci.expect_any_substr(output, """INCREMENT BY 1""")
    _dci.expect_any_substr(output, """MAXVALUE 9223372036854775806""")
    _dci.expect_any_substr(output, """MINVALUE 1""")
    _dci.expect_any_substr(output, """CACHE 25""")
    _dci.expect_any_substr(output, """NO CYCLE""")
    _dci.expect_any_substr(output, """LARGEINT""")
    _dci.expect_any_substr(output, """;""")
    
    stmt = """drop sequence test_seq_sch.h_seq_p2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop schema trafodion.test_seq_sch cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """get schemas; """
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output,'TEST_SEQ_SCH')

    # specify parameter 
    stmt = """create sequence h_seq_p3 start with 10 minvalue 1 maxvalue 200 increment by 2 cache 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl sequence h_seq_p3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """CREATE SEQUENCE TRAFODION.SEQUENCE_SEQH01.H_SEQ_P3""")
    _dci.expect_any_substr(output, """START WITH 10 /* NEXT AVAILABLE VALUE 10 */""")
    _dci.expect_any_substr(output, """INCREMENT BY 2""")
    _dci.expect_any_substr(output, """MAXVALUE 200""")
    _dci.expect_any_substr(output, """MINVALUE 1""")
    _dci.expect_any_substr(output, """CACHE 10""")
    _dci.expect_any_substr(output, """NO CYCLE""")
    _dci.expect_any_substr(output, """LARGEINT""")
    _dci.expect_any_substr(output, """;""")
    
    stmt = """drop sequence h_seq_p3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # no cache, no circle
    stmt = """create sequence h_seq_p4 start with 10 minvalue 1 maxvalue 200 increment by 2 no cache;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl sequence h_seq_p4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """CREATE SEQUENCE TRAFODION.SEQUENCE_SEQH01.H_SEQ_P4""")
    _dci.expect_any_substr(output, """START WITH 10 /* NEXT AVAILABLE VALUE 10 */""")
    _dci.expect_any_substr(output, """INCREMENT BY 2""")
    _dci.expect_any_substr(output, """MAXVALUE 200""")
    _dci.expect_any_substr(output, """MINVALUE 1""")
    _dci.expect_any_substr(output, """NO CACHE""")
    _dci.expect_any_substr(output, """NO CYCLE""")
    _dci.expect_any_substr(output, """LARGEINT""")
    _dci.expect_any_substr(output, """;""")    
    stmt = """drop sequence h_seq_p4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #cycle
    stmt = """create sequence h_seq_p5 start with 10 minvalue 1 maxvalue 200 increment by 2 cache 10 cycle;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl sequence h_seq_p5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """CREATE SEQUENCE TRAFODION.SEQUENCE_SEQH01.H_SEQ_P5""")
    _dci.expect_any_substr(output, """START WITH 10 /* NEXT AVAILABLE VALUE 10 */""")
    _dci.expect_any_substr(output, """INCREMENT BY 2""")
    _dci.expect_any_substr(output, """MAXVALUE 200""")
    _dci.expect_any_substr(output, """MINVALUE 1""")
    _dci.expect_any_substr(output, """CACHE 10""")
    _dci.expect_any_substr(output, """CYCLE""")
    _dci.expect_any_substr(output, """LARGEINT""")
    _dci.expect_any_substr(output, """;""")
    
    stmt = """drop sequence h_seq_p5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #start with = boundaries(LONG_MAX - 1)-1
    stmt = """create sequence h_seq_p6 start with 9223372036854775805 cache 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl sequence h_seq_p6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """CREATE SEQUENCE TRAFODION.SEQUENCE_SEQH01.H_SEQ_P6""")
    _dci.expect_any_substr(output, """START WITH 9223372036854775805 /* NEXT AVAILABLE VALUE 9223372036854775805 */""")
    _dci.expect_any_substr(output, """INCREMENT BY 1""")
    _dci.expect_any_substr(output, """MAXVALUE 9223372036854775806""")
    _dci.expect_any_substr(output, """MINVALUE 1""")
    _dci.expect_any_substr(output, """CACHE 2""")
    _dci.expect_any_substr(output, """NO CYCLE""")
    _dci.expect_any_substr(output, """LARGEINT""")
    _dci.expect_any_substr(output, """;""")
    
    stmt = """drop sequence h_seq_p6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #start with = maxvalue-1 & cache =2
    stmt = """create sequence h_seq_p7 start with 9 maxvalue 10 cache 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl sequence h_seq_p7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """CREATE SEQUENCE TRAFODION.SEQUENCE_SEQH01.H_SEQ_P7""")
    _dci.expect_any_substr(output, """START WITH 9 /* NEXT AVAILABLE VALUE 9 */""")
    _dci.expect_any_substr(output, """INCREMENT BY 1""")
    _dci.expect_any_substr(output, """MAXVALUE 10""")
    _dci.expect_any_substr(output, """MINVALUE 1""")
    _dci.expect_any_substr(output, """CACHE 2""")
    _dci.expect_any_substr(output, """NO CYCLE""")
    _dci.expect_any_substr(output, """LARGEINT""")
    _dci.expect_any_substr(output, """;""")
        
    stmt = """drop sequence h_seq_p7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #minvalue =LONG_MAX-2(maxvalue default -1)
    stmt = """create sequence h_seq_p8 minvalue 9223372036854775805;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl sequence h_seq_p8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """CREATE SEQUENCE TRAFODION.SEQUENCE_SEQH01.H_SEQ_P8""")
    _dci.expect_any_substr(output, """START WITH 9223372036854775805 /* NEXT AVAILABLE VALUE 9223372036854775805 */""")
    _dci.expect_any_substr(output, """INCREMENT BY 1""")
    _dci.expect_any_substr(output, """MAXVALUE 9223372036854775806""")
    _dci.expect_any_substr(output, """MINVALUE 9223372036854775805""")
    _dci.expect_any_substr(output, """CACHE 2""")
    _dci.expect_any_substr(output, """NO CYCLE""")
    _dci.expect_any_substr(output, """LARGEINT""")
    _dci.expect_any_substr(output, """;""")
    
    stmt = """drop sequence h_seq_p8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #maxvalue =LONG_MAX(maxvalue default )
    stmt = """create sequence h_seq_p9 maxvalue 9223372036854775806;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl sequence h_seq_p9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """CREATE SEQUENCE TRAFODION.SEQUENCE_SEQH01.H_SEQ_P9""")
    _dci.expect_any_substr(output, """START WITH 1 /* NEXT AVAILABLE VALUE 1 */""")
    _dci.expect_any_substr(output, """INCREMENT BY 1""")
    _dci.expect_any_substr(output, """MAXVALUE 9223372036854775806""")
    _dci.expect_any_substr(output, """MINVALUE 1""")
    _dci.expect_any_substr(output, """CACHE 25""")
    _dci.expect_any_substr(output, """NO CYCLE""")
    _dci.expect_any_substr(output, """LARGEINT""")
    _dci.expect_any_substr(output, """;""")
    
    stmt = """drop sequence h_seq_p9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #increment by =(maxvalue-minvalue)
    stmt = """create sequence h_seq_p10 minvalue 1 maxvalue 10 increment by 9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl sequence h_seq_p10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """CREATE SEQUENCE TRAFODION.SEQUENCE_SEQH01.H_SEQ_P10""")
    _dci.expect_any_substr(output, """START WITH 1 /* NEXT AVAILABLE VALUE 1 */""")
    _dci.expect_any_substr(output, """INCREMENT BY 9""")
    _dci.expect_any_substr(output, """MAXVALUE 10""")
    _dci.expect_any_substr(output, """MINVALUE 1""")
    _dci.expect_any_substr(output, """CACHE 2""")
    _dci.expect_any_substr(output, """NO CYCLE""")
    _dci.expect_any_substr(output, """LARGEINT""")
    _dci.expect_any_substr(output, """;""")
    
    stmt = """drop sequence h_seq_p10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #cache =(maxValue-minValue)/incrementValue
    stmt = """create sequence h_seq_p11 minvalue 1 maxvalue 21 increment by 5 cache 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl sequence h_seq_p11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """CREATE SEQUENCE TRAFODION.SEQUENCE_SEQH01.H_SEQ_P11""")
    _dci.expect_any_substr(output, """START WITH 1 /* NEXT AVAILABLE VALUE 1 */""")
    _dci.expect_any_substr(output, """INCREMENT BY 5""")
    _dci.expect_any_substr(output, """MAXVALUE 21""")
    _dci.expect_any_substr(output, """MINVALUE 1""")
    _dci.expect_any_substr(output, """CACHE 5""")
    _dci.expect_any_substr(output, """NO CYCLE""")
    _dci.expect_any_substr(output, """LARGEINT""")
    _dci.expect_any_substr(output, """;""")

    stmt = """drop sequence h_seq_p11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #increment by =(maxvalue-1)
    stmt = """create sequence h_seq_p12  maxvalue 9223372036854775806 increment by 9223372036854775805;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl sequence h_seq_p12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """CREATE SEQUENCE TRAFODION.SEQUENCE_SEQH01.H_SEQ_P12""")
    _dci.expect_any_substr(output, """START WITH 1 /* NEXT AVAILABLE VALUE 1 */""")
    _dci.expect_any_substr(output, """INCREMENT BY 9223372036854775805""")
    _dci.expect_any_substr(output, """MAXVALUE 9223372036854775806""")
    _dci.expect_any_substr(output, """MINVALUE 1""")
    _dci.expect_any_substr(output, """CACHE 2""")
    _dci.expect_any_substr(output, """NO CYCLE""")
    _dci.expect_any_substr(output, """LARGEINT""")
    _dci.expect_any_substr(output, """;""")
    
    stmt = """drop sequence h_seq_p12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


    _testmgr.testcase_end(desc)
# ---------------------------------------------------------
#testcase test002 CREATE SEQUENCE negative tests
# ---------------------------------------------------------
def test002(desc="""CREATE SEQUENCE negative tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # repeatedly  create sequence   
    stmt = """drop sequence h_seq_f1;"""
    output = _dci.cmdexec(stmt)

    stmt = """create sequence h_seq_f1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create sequence h_seq_f1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1390')

    stmt = """drop sequence h_seq_f1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #start with = -1
    stmt = """create sequence h_seq_f2 start with -1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1572')
    stmt = """drop sequence h_seq_f2;"""
    output = _dci.cmdexec(stmt)

    #start with = 0
    stmt = """create sequence h_seq_f3 start with 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1573')
    stmt = """drop sequence h_seq_f3;"""
    output = _dci.cmdexec(stmt)
    
    #start with <minvalue
    stmt = """create sequence h_seq_f4 start with 4 minvalue 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1573')
    stmt = """drop sequence h_seq_f4;"""
    output = _dci.cmdexec(stmt)
    
    #start with >maxvalue
    stmt = """create sequence h_seq_f5 start with 10 maxvalue 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1573')
    stmt = """drop sequence h_seq_f5;"""
    output = _dci.cmdexec(stmt)

    #start with =LONG_MAX
    stmt = """create sequence h_seq_f6 start with 9223372036854775807;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1573')
    stmt = """drop sequence h_seq_f6;"""
    output = _dci.cmdexec(stmt)

    #start with = boundaries(LONG_MAX - 1), cache not defined
    stmt = """create sequence h_seq_f start with 9223372036854775806 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1577')

    #start with = maxvalue, cache not defined
    stmt = """create sequence h_seq_f start with 10 maxvalue 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1577')

    #minvalue = -1
    stmt = """create sequence h_seq_f7 minvalue -1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1572')
    stmt = """drop sequence h_seq_f7;"""
    output = _dci.cmdexec(stmt)

    #minvalue = 0
    stmt = """create sequence h_seq_f8 minvalue 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1571')
    stmt = """drop sequence h_seq_f8;"""
    output = _dci.cmdexec(stmt)

    #minvalue >maxvalue
    stmt = """create sequence h_seq_f9 minvalue 10 maxvalue 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1570')
    stmt = """drop sequence h_seq_f9;"""
    output = _dci.cmdexec(stmt)

    #minvalue =LONG_MAX-1(maxvalue default)
    stmt = """create sequence h_seq_f10 minvalue 9223372036854775806;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1570')
    stmt = """drop sequence h_seq_f10;"""
    output = _dci.cmdexec(stmt)

    #maxvalue = -1
    stmt = """create sequence h_seq_f11 maxvalue -1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1572')
    stmt = """drop sequence h_seq_f11;"""
    output = _dci.cmdexec(stmt)

    #maxvalue = 0
    stmt = """create sequence h_seq_f12 maxvalue 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1571')
    stmt = """drop sequence h_seq_f12;"""
    output = _dci.cmdexec(stmt)

    #maxvalue =?(maximum )
    stmt = """create sequence h_seq_f13 maxvalue 9223372036854775807;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1576')
    stmt = """drop sequence h_seq_f13;"""
    output = _dci.cmdexec(stmt)

    #increment by >(maxvalue-minvalue)
    stmt = """create sequence h_seq_f14 minvalue 1 maxvalue 10 increment by 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1575')
    stmt = """drop sequence h_seq_f14;"""
    output = _dci.cmdexec(stmt)

    #cache =0
    stmt = """create sequence h_seq_f15 cache 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1577')
    stmt = """drop sequence h_seq_f15;"""
    output = _dci.cmdexec(stmt)

    #cache = -1
    stmt = """create sequence h_seq_f16 cache -1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'15001')
    stmt = """drop sequence h_seq_f16;"""
    output = _dci.cmdexec(stmt)

    #cache >(maxValue-minValue)/incrementValue
    stmt = """create sequence h_seq_f17 minvalue 1 maxvalue 21 increment by 5 cache 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1577')
 
    stmt = """drop sequence h_seq_f17;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)
# ---------------------------------------------------------
#testcase test003 alter SEQUENCE success
# ---------------------------------------------------------
def test003(desc="""alter SEQUENCE success"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop sequence h_seq_alter_p1;"""
    output = _dci.cmdexec(stmt)

    # create sequence default 
    stmt = """create sequence h_seq_alter_p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl sequence h_seq_alter_p1;"""
    output = _dci.cmdexec(stmt)
    
    _dci.expect_any_substr(output, """CREATE SEQUENCE TRAFODION.SEQUENCE_SEQH01.H_SEQ_ALTER_P1""")
    _dci.expect_any_substr(output, """START WITH 1 /* NEXT AVAILABLE VALUE 1 */""")
    _dci.expect_any_substr(output, """INCREMENT BY 1""")
    _dci.expect_any_substr(output, """MAXVALUE 9223372036854775806""")
    _dci.expect_any_substr(output, """MINVALUE 1""")
    _dci.expect_any_substr(output, """CACHE 25""")
    _dci.expect_any_substr(output, """NO CYCLE""")
    _dci.expect_any_substr(output, """LARGEINT""")
    _dci.expect_any_substr(output, """;""")    
    
    # alter increment by 
    stmt = """alter sequence h_seq_alter_p1 increment by 20; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl sequence h_seq_alter_p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """CREATE SEQUENCE TRAFODION.SEQUENCE_SEQH01.H_SEQ_ALTER_P1""")
    _dci.expect_any_substr(output, """START WITH 1 /* NEXT AVAILABLE VALUE 1 */""")
    _dci.expect_any_substr(output, """INCREMENT BY 20""")
    _dci.expect_any_substr(output, """MAXVALUE 9223372036854775806""")
    _dci.expect_any_substr(output, """MINVALUE 1""")
    _dci.expect_any_substr(output, """CACHE 25""")
    _dci.expect_any_substr(output, """NO CYCLE""")
    _dci.expect_any_substr(output, """LARGEINT""")
    _dci.expect_any_substr(output, """;""")

    # alter increment by = maxvalue
    stmt = """alter sequence h_seq_alter_p1 increment by 9223372036854775805; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl sequence h_seq_alter_p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """CREATE SEQUENCE TRAFODION.SEQUENCE_SEQH01.H_SEQ_ALTER_P1""")
    _dci.expect_any_substr(output, """START WITH 1 /* NEXT AVAILABLE VALUE 1 */""")
    _dci.expect_any_substr(output, """INCREMENT BY 9223372036854775805""")
    _dci.expect_any_substr(output, """MAXVALUE 9223372036854775806""")
    _dci.expect_any_substr(output, """MINVALUE 1""")
    _dci.expect_any_substr(output, """CACHE 25""")
    _dci.expect_any_substr(output, """NO CYCLE""")
    _dci.expect_any_substr(output, """LARGEINT""")
    _dci.expect_any_substr(output, """;""")
    # alter maxvalue
    stmt = """alter sequence h_seq_alter_p1 maxvalue 100 increment by 10; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl sequence h_seq_alter_p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """CREATE SEQUENCE TRAFODION.SEQUENCE_SEQH01.H_SEQ_ALTER_P1""")
    _dci.expect_any_substr(output, """START WITH 1 /* NEXT AVAILABLE VALUE 1 */""")
    _dci.expect_any_substr(output, """INCREMENT BY 10""")
    _dci.expect_any_substr(output, """MAXVALUE 100""")
    _dci.expect_any_substr(output, """MINVALUE 1""")
    _dci.expect_any_substr(output, """CACHE 25""")
    _dci.expect_any_substr(output, """NO CYCLE""")
    _dci.expect_any_substr(output, """LARGEINT""")
    _dci.expect_any_substr(output, """;""")
    
    # alter maxvalue= max
    stmt = """alter sequence h_seq_alter_p1 maxvalue 9223372036854775806 increment by 9223372036854775805;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl sequence h_seq_alter_p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """CREATE SEQUENCE TRAFODION.SEQUENCE_SEQH01.H_SEQ_ALTER_P1""")
    _dci.expect_any_substr(output, """START WITH 1 /* NEXT AVAILABLE VALUE 1 */""")
    _dci.expect_any_substr(output, """INCREMENT BY 9223372036854775805""")
    _dci.expect_any_substr(output, """MAXVALUE 9223372036854775806""")
    _dci.expect_any_substr(output, """MINVALUE 1""")
    _dci.expect_any_substr(output, """CACHE 25""")
    _dci.expect_any_substr(output, """NO CYCLE""")
    _dci.expect_any_substr(output, """LARGEINT""")
    _dci.expect_any_substr(output, """;""")

    # alter maxvalue= max
    stmt = """alter sequence h_seq_alter_p1 maxvalue 11 increment by 10; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl sequence h_seq_alter_p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """CREATE SEQUENCE TRAFODION.SEQUENCE_SEQH01.H_SEQ_ALTER_P1""")
    _dci.expect_any_substr(output, """START WITH 1 /* NEXT AVAILABLE VALUE 1 */""")
    _dci.expect_any_substr(output, """INCREMENT BY 10""")
    _dci.expect_any_substr(output, """MAXVALUE 11""")
    _dci.expect_any_substr(output, """MINVALUE 1""")
    _dci.expect_any_substr(output, """CACHE 25""")
    _dci.expect_any_substr(output, """NO CYCLE""")
    _dci.expect_any_substr(output, """LARGEINT""")
    _dci.expect_any_substr(output, """;""")

    # alter cycle
    stmt = """alter sequence h_seq_alter_p1 cycle; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl sequence h_seq_alter_p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """CREATE SEQUENCE TRAFODION.SEQUENCE_SEQH01.H_SEQ_ALTER_P1""")
    _dci.expect_any_substr(output, """START WITH 1 /* NEXT AVAILABLE VALUE 1 */""")
    _dci.expect_any_substr(output, """INCREMENT BY 10""")
    _dci.expect_any_substr(output, """MAXVALUE 11""")
    _dci.expect_any_substr(output, """MINVALUE 1""")
    _dci.expect_any_substr(output, """CACHE 25""")
    _dci.expect_any_substr(output, """CYCLE""")
    _dci.expect_any_substr(output, """LARGEINT""")
    _dci.expect_any_substr(output, """;""")

    stmt = """drop sequence h_seq_alter_p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)
# ---------------------------------------------------------
#testcase test004 alter SEQUENCE negative tests
# ---------------------------------------------------------
def test004(desc="""alter SEQUENCE negative tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # create sequence   
    stmt = """drop sequence h_seq_alter_f1;"""
    output = _dci.cmdexec(stmt)

    stmt = """create sequence h_seq_alter_f1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # alter start with = -1 , is an issue
    stmt = """alter sequence h_seq_alter_f1 start with -1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1592')

    #start with = 0
    stmt = """alter sequence h_seq_alter_f1 start with 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1592')
    
    #start with <minvalue
    stmt = """alter sequence h_seq_alter_f1 start with 4 minvalue 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1592')
    
    #start with >maxvalue
    stmt = """alter sequence h_seq_alter_f1 start with 10 maxvalue 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1592')
    
    #start with =LONG_MAX
    stmt = """alter sequence h_seq_alter_f1 start with 9223372036854775807;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1592')
    
    #minvalue = -1
    stmt = """alter sequence h_seq_alter_f1 minvalue -1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1592')
    
    #minvalue = 0
    stmt = """alter sequence h_seq_alter_f1 minvalue 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1592')
    
    #minvalue >maxvalue
    stmt = """alter sequence h_seq_alter_f1 minvalue 10 maxvalue 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1592')
    
    #minvalue =LONG_MAX-1(maxvalue default)
    stmt = """alter sequence h_seq_alter_f1 minvalue 9223372036854775806;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1592')

    #maxvalue = -1
    stmt = """alter sequence h_seq_alter_f1 maxvalue -1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1572')
    
    #maxvalue = 0
    stmt = """alter sequence h_seq_alter_f1 maxvalue 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1571')
    
    #maxvalue =maximum+1(maximum 9223372036854775806)
    stmt = """alter sequence h_seq_alter_f1 maxvalue 9223372036854775807;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1576')

    #increment by >(maxvalue-minvalue)
    stmt = """alter sequence h_seq_alter_f1 minvalue 1 maxvalue 10 increment by 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1592')
    
    #cache =0
    stmt = """alter sequence h_seq_alter_f1 cache 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1577')

    #cache = -1
    stmt = """alter sequence h_seq_alter_f1 cache -1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'15001')
    
    #cache >(maxValue-minValue)/incrementValue
    stmt = """alter sequence h_seq_alter_f1 minvalue 1 maxvalue 21 increment by 5 cache 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1592')

    stmt = """alter sequence h_seq_alter_f1 minvalue 1 maxvalue 21 increment by 5 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1592')

    stmt = """showddl  sequence h_seq_alter_f1 ;"""
    output = _dci.cmdexec(stmt)
    stmt = """alter sequence h_seq_alter_f1 cache 6 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop sequence h_seq_alter_f1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


    _testmgr.testcase_end(desc)
# ---------------------------------------------------------
#testcase test005 drop SEQUENCE 
# ---------------------------------------------------------
def test005(desc="""drop SEQUENCE """):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # drop default sequence  
    stmt = """drop sequence h_seq_drop_p1;"""
    output = _dci.cmdexec(stmt)

    stmt = """create sequence h_seq_drop_p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """get sequences;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'H_SEQ_DROP_P1')

    stmt = """drop sequence h_seq_drop_p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """get sequences;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, 'H_SEQ_DROP_P1')

    #create sequence specify schema

    stmt = """create schema test_seq_drop_sch;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create sequence test_seq_drop_sch.h_seq_drop_p2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get sequences;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'TEST_SEQ_DROP_SCH.H_SEQ_DROP_P2')
    
    stmt = """create sequence test_seq_drop_sch.h_seq_drop_p3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """get sequences;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'TEST_SEQ_DROP_SCH.H_SEQ_DROP_P3')

    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # can't drop sequence not in own schema
    stmt = """drop sequence h_seq_drop_p2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1389')
    stmt = """get sequences;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'H_SEQ_DROP_P2')

    # drop schema.sequence success
    stmt = """drop sequence test_seq_drop_sch.h_seq_drop_p2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get sequences;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, 'TEST_SEQ_DROP_SCH.H_SEQ_DROP_P2')
    
    # drop catalog.schema.sequence success
    stmt = """drop sequence trafodion.test_seq_drop_sch.h_seq_drop_p3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
    stmt = """get sequences;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, 'H_SEQ_DROP_P3')
    

    # drop sequence in specify schema
    stmt = """create sequence h_seq_drop_p4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get sequences in schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'H_SEQ_DROP_P4')

    #the sequence  not exist
    stmt = """drop sequence h_seq_drop_not_exit;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1389')
   
   #sequence name is empty
    stmt = """drop sequence """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1389')
    
    #schema.*
    stmt = """drop sequence """ + defs.my_schema + """.*;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'15001')
    
    #wrong schema name
    stmt = """drop sequence trafodion.seabase.h_seq_drop_p4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1389')
    
    #wrong catalog name
    stmt = """drop sequence traf.SEQUENCE_SEQH01.h_seq_drop_p4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1389')
    
    # A syntax error
    stmt = """drop sequences h_seq_drop_exit;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'15001')

    stmt = """drop sequence h_seq_drop_p4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get sequences;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, 'H_SEQ_DROP_P4')
   
    #stmt = """get schemas;"""
    #output = _dci.cmdexec(stmt)
    #_dci.unexpect_any_substr(output, 'SEQUENCE_SEQH01')

    stmt = """drop schema test_seq_drop_sch cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """get schemas;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, 'TEST_SEQ_DROP_SCH')

    _testmgr.testcase_end(desc)
# ---------------------------------------------------------
#testcase test006  get sequences
# ---------------------------------------------------------
def test006(desc="""get sequences """):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create schema test_seq_get_sch;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create sequence test_seq_get_sch.h_seq_get_p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create sequence h_seq_get_p2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """get sequences;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'TEST_SEQ_GET_SCH.H_SEQ_GET_P1')
    _dci.expect_any_substr(output, 'SEQUENCE_SEQH01.H_SEQ_GET_P2')

    stmt = """get sequences in schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'H_SEQ_GET_P2')

    #wrong schema name ???
    stmt = """get sequences in schema wrong_name;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # A syntax error
    stmt = """get sequence ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'15001')
    
    stmt = """get sequences in wrong ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'15001')
    
    stmt = """get sequences in schema trafodion.dd';;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'15005')

    stmt = """drop sequence test_seq_get_sch.h_seq_get_p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop sequence h_seq_get_p2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop schema test_seq_get_sch cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)
# ---------------------------------------------------------
#testcase test007  showddl sequence
# ---------------------------------------------------------
def test007(desc="""showddl sequence """):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create schema test_seq_show_sch;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create sequence test_seq_show_sch.h_seq_show_p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # in owner schema
    stmt = """set schema test_seq_show_sch;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl sequence h_seq_show_p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """CREATE SEQUENCE TRAFODION.TEST_SEQ_SHOW_SCH.H_SEQ_SHOW_P1""")
    _dci.expect_any_substr(output, """START WITH 1 /* NEXT AVAILABLE VALUE 1 */""")
    _dci.expect_any_substr(output, """INCREMENT BY 1""")
    _dci.expect_any_substr(output, """MAXVALUE 9223372036854775806""")
    _dci.expect_any_substr(output, """MINVALUE 1""")
    _dci.expect_any_substr(output, """CACHE 25""")
    _dci.expect_any_substr(output, """NO CYCLE""")
    _dci.expect_any_substr(output, """LARGEINT""")
    _dci.expect_any_substr(output, """;""")

    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # not in default schema
    stmt = """showddl sequence h_seq_show_p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1389')
    
    #showddl sequence schema.sequence
    stmt = """showddl sequence test_seq_show_sch.h_seq_show_p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """CREATE SEQUENCE TRAFODION.TEST_SEQ_SHOW_SCH.H_SEQ_SHOW_P1""")
    _dci.expect_any_substr(output, """START WITH 1 /* NEXT AVAILABLE VALUE 1 */""")
    _dci.expect_any_substr(output, """INCREMENT BY 1""")
    _dci.expect_any_substr(output, """MAXVALUE 9223372036854775806""")
    _dci.expect_any_substr(output, """MINVALUE 1""")
    _dci.expect_any_substr(output, """CACHE 25""")
    _dci.expect_any_substr(output, """NO CYCLE""")
    _dci.expect_any_substr(output, """LARGEINT""")
    _dci.expect_any_substr(output, """;""")
    
    #showddl sequence catalog.schema.sequence
    stmt = """showddl sequence trafodion.test_seq_show_sch.h_seq_show_p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """CREATE SEQUENCE TRAFODION.TEST_SEQ_SHOW_SCH.H_SEQ_SHOW_P1""")
    _dci.expect_any_substr(output, """START WITH 1 /* NEXT AVAILABLE VALUE 1 */""")
    _dci.expect_any_substr(output, """INCREMENT BY 1""")
    _dci.expect_any_substr(output, """MAXVALUE 9223372036854775806""")
    _dci.expect_any_substr(output, """MINVALUE 1""")
    _dci.expect_any_substr(output, """CACHE 25""")
    _dci.expect_any_substr(output, """NO CYCLE""")
    _dci.expect_any_substr(output, """LARGEINT""")
    _dci.expect_any_substr(output, """;""")

    stmt = """create sequence h_seq_show_p2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl sequence h_seq_show_p2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """CREATE SEQUENCE TRAFODION.SEQUENCE_SEQH01.H_SEQ_SHOW_P2""")
    _dci.expect_any_substr(output, """START WITH 1 /* NEXT AVAILABLE VALUE 1 */""")
    _dci.expect_any_substr(output, """INCREMENT BY 1""")
    _dci.expect_any_substr(output, """MAXVALUE 9223372036854775806""")
    _dci.expect_any_substr(output, """MINVALUE 1""")
    _dci.expect_any_substr(output, """CACHE 25""")
    _dci.expect_any_substr(output, """NO CYCLE""")
    _dci.expect_any_substr(output, """LARGEINT""")
    _dci.expect_any_substr(output, """;""")
    #wrong sequence name
    stmt = """showddl sequence wrong_name;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1389')

    #wrong catalog.schema name
    stmt = """showddl sequence trafodion.wrong.h_seq_show_p2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1389')
    
    #wrong catalog name
    stmt = """showddl sequence tafodio.SEQUENCE_SEQH01.h_seq_show_p2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1002')

    stmt = """showddl sequence ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'15001')
    
    stmt = """showddl sequence in schema dd ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'15001')
    
    stmt = """showddl sequence ';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'15005')

    stmt = """drop sequence test_seq_show_sch.h_seq_show_p1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    time.sleep(10);

    stmt = """drop sequence h_seq_show_p2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop schema test_seq_show_sch cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    time.sleep(10);
    _testmgr.testcase_end(desc)
# ---------------------------------------------------------
#testcase test008  seqnum value in select,where,insert
# ---------------------------------------------------------
def test008(desc="""seqnum value in select,where,insert"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create sequence h_seq_num_select;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # next seqnum value in select
    stmt = """select seqnum(h_seq_num_select, next) from (values(1)) x(a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/h08exp""", 'h08s1')
    
    stmt = """select seqnum(h_seq_num_select, next) from (values(1)) x(a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/h08exp""", 'h08s2')
    
    #current seqnum value in select
    stmt = """select seqnum(h_seq_num_select, current) from (values(1)) x(a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/h08exp""", 'h08s3')

    stmt = """drop sequence h_seq_num_select;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # seqnum in the where predicate
    stmt = """create table t (a int not null primary key, b int not null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into t values (1,1), (2,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,'2')
    
    stmt = """create sequence h_seq_num_where;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #current 1
    stmt = """select * from t where a < seqnum(h_seq_num_where);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/h08exp""", 'h08s4')
    
    # current 2
    stmt = """select * from t where a < seqnum(h_seq_num_where);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/h08exp""", 'h08s5')
    
    #current 3
    stmt = """select * from t where a < seqnum(h_seq_num_where);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/h08exp""", 'h08s6')
    
    stmt = """drop table t cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop sequence h_seq_num_where;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #next seqnum value in insert
    stmt = """create table seq_insert11 (a int not null primary key, b int not null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create sequence h_seq_num_insert start with 10 increment by 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into seq_insert11 values (seqnum(h_seq_num_insert), 10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,'1')

    stmt = """insert into seq_insert11 values (seqnum(h_seq_num_insert), 11);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,'1')

    stmt = """insert into seq_insert11 values (seqnum(h_seq_num_insert), 12);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,'1')

    stmt = """select * from seq_insert11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output,'3')
    
    stmt = """insert into seq_insert11 values (seqnum(h_seq_num_insert, current), 12);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'8102')

    # multiple seqnum values in insert
    stmt = """create table seq_insert2 (z largeint not null primary key, b int not null, c int not null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into seq_insert2 select seqnum(h_seq_num_insert), a, b from seq_insert11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,'3')
    
    stmt = """drop table seq_insert11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table seq_insert2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop sequence h_seq_num_insert;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # seqnum with cycle option
    stmt = """create sequence h_seq_num_cycle maxvalue 4 increment by 2 cycle;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl sequence h_seq_num_cycle;"""
    output = _dci.cmdexec(stmt)

    _dci.expect_any_substr(output, """CREATE SEQUENCE TRAFODION.SEQUENCE_SEQH01.H_SEQ_NUM_CYCLE""")
    _dci.expect_any_substr(output, """START WITH 1 /* NEXT AVAILABLE VALUE 1 */""")
    _dci.expect_any_substr(output, """INCREMENT BY 2""")
    _dci.expect_any_substr(output, """MAXVALUE 4""")
    _dci.expect_any_substr(output, """MINVALUE 1""")
    _dci.expect_any_substr(output, """CACHE 2""")
    _dci.expect_any_substr(output, """CYCLE""")
    _dci.expect_any_substr(output, """LARGEINT""")
    _dci.expect_any_substr(output, """;""")
    
    stmt = """select seqnum(h_seq_num_cycle) from (values (1)) x(a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/h08exp""", 'h08s8')
    
    stmt = """select seqnum(h_seq_num_cycle) from (values (1)) x(a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/h08exp""", 'h08s9')
    
    stmt = """select seqnum(h_seq_num_cycle) from (values (1)) x(a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/h08exp""", 'h08s10')
    
    stmt = """select seqnum(h_seq_num_cycle) from (values (1)) x(a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/h08exp""", 'h08s11')
    
    stmt = """drop sequence h_seq_num_cycle;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # seqnum with  no cycle option
    stmt = """create sequence h_seq_num_no_cycle maxvalue 4 increment by 2 no cycle;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl sequence h_seq_num_no_cycle;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """CREATE SEQUENCE TRAFODION.SEQUENCE_SEQH01.H_SEQ_NUM_NO_CYCLE""")
    _dci.expect_any_substr(output, """START WITH 1 /* NEXT AVAILABLE VALUE 1 */""")
    _dci.expect_any_substr(output, """INCREMENT BY 2""")
    _dci.expect_any_substr(output, """MAXVALUE 4""")
    _dci.expect_any_substr(output, """MINVALUE 1""")
    _dci.expect_any_substr(output, """CACHE 2""")
    _dci.expect_any_substr(output, """NO CYCLE""")
    _dci.expect_any_substr(output, """LARGEINT""")
    _dci.expect_any_substr(output, """;""")

    stmt = """select seqnum(h_seq_num_no_cycle) from (values (1)) x(a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/h08exp""", 'h08s13')
    
    stmt = """select seqnum(h_seq_num_no_cycle) from (values (1)) x(a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/h08exp""", 'h08s14')
    
    stmt = """select seqnum(h_seq_num_no_cycle) from (values (1)) x(a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1579')
    
    stmt = """drop sequence h_seq_num_no_cycle;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)
    
