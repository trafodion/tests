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
    
def test001(desc="""n12"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     N12
    #  Description:        NULL in arithmetic expressions
    #                      Negative - SQLCI select.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    #  Notes:
    #  This test case incorporates features detailed in the "Title"
    #  by Ima Programmer (Version 1.1, <date>).
    #
    # =================== End Test Case Header  ===================
    
    # 06/09/98 EL
    
    stmt = """create table btre201 (
ordering            smallint   not null
, alwaysnull          smallint                default null
, char_1              char(1)                 default null
, pic_x_8             pic x(8)                default null
, var_char_2          varchar(2)              default null
, var_char_3          varchar(3)              default null
, binary_signed       numeric (4) signed      default null
, binary_32_u         numeric (9,2) unsigned  default null
, binary_64_s         numeric (18,3) signed   default null
, pic_comp_1          pic s9(10) comp         default null
, pic_comp_2          pic sv9(2) comp         default null
, pic_comp_3          pic s9(3)v9(5) comp     default null
, small_int           smallint                default null
, medium_int          integer unsigned        default null
, large_int           largeint signed         default null
, decimal_1           decimal (1)             default null
, decimal_2_signed    decimal (2,2) signed    default null
, decimal_3_unsigned  decimal (3,0) unsigned  default null
, pic_decimal_1       pic s9(1)v9(1)          default null
, pic_decimal_2       picture v999 display    default null
, pic_decimal_3       pic s9                  default null
, float_basic         float (4)               default null
, float_real          real                    default null
, float_double_p      double precision        default null
, y_to_d              date                    default null
, y_to_d_2            date                    default null
, h_to_f              time(3)                 default null
, time1               time                    default null
, iy_to_mo            interval year(4) to month  default null
, ih_to_s             interval hour to second default null
, primary key (ordering)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # 1/25/99 For now the only blocksize supported is 4096
    #    blocksize 2048
    
    stmt = """create index btre201a 
on btre201 (ordering)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #      ATTRIBUTES
    # 1/25/99 For now the only blocksize supported is 4096
    #      blocksize 512
    
    stmt = """create index btre201b 
on btre201 (char_1, alwaysnull, binary_signed)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index btre201c 
on btre201 (var_char_3, large_int)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # 1/25/99 For now the only blocksize supported is 4096
    #      ATTRIBUTES
    #      blocksize 512
    
    stmt = """create index btre201d 
on btre201 (decimal_3_unsigned, pic_decimal_1)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # 1/25/99 For now the only blocksize supported is 4096
    #      ATTRIBUTES
    #      blocksize 512
    
    stmt = """create index btre201e 
on btre201 (pic_x_8, iy_to_mo, y_to_d, medium_int)
ATTRIBUTES
auditcompress,
--      no buffered,
clearonpurge
--      no dcompress,
--      no icompress,
--      maxsize 320
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index btre201f 
on btre201 (ih_to_s)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index btre201g 
on btre201 (time1 DESC, float_real ASC, pic_comp_3)
ATTRIBUTES
no auditcompress,
--      buffered,
no clearonpurge
--      icompress,
--      no dcompress,
--      maxsize 6
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index btre201h 
on btre201 (y_to_d_2 DESC)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index btre201i 
on btre201 (float_double_p ASC)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index btre201j 
on btre201 (h_to_f)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index btre201k 
on btre201 (decimal_1, pic_decimal_3 DESC)
-- 1/25/99 For now the only blocksize supported is 4096
ATTRIBUTES
blocksize 4096
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index btre201l 
on btre201 (decimal_2_signed ASC, small_int DESC,
var_char_2, binary_32_u, pic_comp_1,
float_basic DESC)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index btre201m 
on btre201 (pic_comp_2, binary_64_s)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into btre201 (ordering , pic_comp_2 ,
pic_comp_3 , char_1 , pic_x_8 , var_char_2, var_char_3
, small_int , large_int , decimal_2_signed
, decimal_1
)
values ( 1, .1, 1
, 'a' , 'Abcdefgh' , 'aB' , 'AbC'
, NULL , 1 , .1
, 1
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into btre201 (ordering , pic_comp_2 ,
pic_comp_3 , var_char_2, var_char_3
, small_int , large_int , decimal_2_signed
, decimal_1
)
values ( 2, null, 2
, 'az' , 'zz'
, NULL , NULL , .2
, 1
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into btre201 (ordering , pic_comp_2 ,
pic_comp_3 , var_char_2, var_char_3
, small_int , large_int , decimal_2_signed
)
values ( 3, null, 2
, 'zy' , 'zy'
, NULL , 10 , NULL
) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  Attempt to use NULL literal in select list and where clause:
    
    stmt = """select decimal_2_signed , NULL , ordering
from btre201 
order by ordering ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n12exp""", 'n12s2')
    
    stmt = """select ( decimal_2_signed + NULL ) , ordering
from btre201 
order by ordering ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4098')
    
    stmt = """select decimal_2_signed , ordering
from btre201 
where decimal_2_signed + null = 0
order by ordering ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4098')
    
    stmt = """drop table btre201;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #             End of test case ARKT0139
    _testmgr.testcase_end(desc)

