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
import setup

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
#  -------------------------------------------------------------------
#testcase a01 a01
# --------------------------------------------------------------------
# 
#   In this test case a01, these options are used:
# 
#   CQD UPD_PARTIAL_ON_ERROR is set ON for some BEGIN/ROLLBACK/COMMIT 
#   fram,
#   The target tables have primary keys, but no any index and constraints,
#   The INSERT statement with a single VALUES clause,
#   The UPDATE statement with an equality predicate on primary keys,
#   The DELETE statement with an equality predicate on primary keys.    
def test001(desc="""a01"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default TABLELOCK 'OFF';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default SIMILARITY_CHECK 'OFF';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default QUERY_CACHE '0';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO receiver1 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2, 
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I1a', 'picx8   ', 1234567.83, '333',
                       -7291, 382, 'c2', 10, .823, 1.27839E18, 3.7289112E23,
                       date '2003-07-31', interval '4444-01' year(4) to month,
                       interval '23:09:12.666666' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO receiver2 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)   
               VALUES ('I2a', 'picx8   ', -1273, 'r2a', 
                       -8219, 79, 'R2', 12, .72, 2.3787E13, 4.237423E52, 
                       date '2003-08-01', interval '4291-09' year(4) to month, 
                       interval '02:04:59.888888' hour to second),
                      ('I2b', 'picx82  ', 22273.111, 'r2b',
                       8219, 709, 'r2', 7333, .172, 5.3787E13, 9.237423E52,
                       date '2003-08-02', interval '0291-10' year(4) to month,
                       interval '12:14:57.888888' hour to second),
                       ('I2c', 'picx83  ', 38223242.333, 'r2c',
                        6839, 333, 'Rr', 7812, .436, 8.1937E16, 9.22323E2,
                       date '2003-08-03', interval '7291-09' year(4) to month,
                       interval '05:27:33.888888' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)
    
    stmt = """INSERT INTO receiver3 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I3a', 'picx8   ', 1234567.83, '333',
                       -7291, 382, 'c2', 10, .823, 1.27839E18, 3.7289112E23,
                       date '2003-07-31', interval '4444-01' year(4) to month,
                       interval '23:09:12.666666' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from receiver1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    
    stmt = """select * from receiver2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    
    stmt = """select * from receiver3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    
    stmt = """INSERT INTO receiver1 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I1a', 'picx888', 1234567.83, '333',
                       -7291, 382, 'c2', 10, null, 1.27839E8, 3.7289112E59,
                       date '2003-07-31', interval '4444-01' year(4) to month,
                       interval '23:09:12.666666' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4122')
    
    stmt = """UPDATE receiver1 SET  pic_x_8 = 'PRIMKEY'
       WHERE pic_x_8 = 'PICX88888';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """UPDATE receiver1 SET  pic_x_8 = 'PRIMKEY'
       WHERE pic_x_8 = 'PICX8';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4033')
    
    stmt = """INSERT INTO View_R1 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('IV1', 'ViewR1', 22273.111, 'r2b',
                       8219, 709, 'r2', 7333, .172, 5.3787E13, 9.3E52,
                       date '2003-08-02', interval '0291-10' year(4) to month,
                       interval '12:14:57.888888' hour to second),
                      ('IV2', 'VR1', 38223242.333, 'r2c',
                       6839, 333, 'Rr', 7812, .906, 8.1937E16, 3.22323E12,
                       date '2003-08-03', interval '7291-09' year(4) to month,
                       interval '05:27:33.888888' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)

    stmt = """UPDATE receiver1 SET char_3 = 'UPD'
       WHERE pic_x_8 = 'PICX8   ';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)

    #stmt = """ UPDATE receiver1 SET char_3 = 'UPD4'
    #         WHERE pic_x_8 = 'PICX8   ';"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_error_msg(output,'8402')
 
    stmt = """select small_int from View_R1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """UPDATE View_R1 set small_int = 1014;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    
    stmt = """DROP TABLE receiver1 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'20123')
    
    stmt = """UPDATE View_R3 set small_int = 1014;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """INSERT INTO receiver2 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsiged, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I2a', 'picx88888', -1273, 'r2a',
                       -8219, 79, 'R2', 12, .72, 2.3787E13, 4.237423E52,
                       date '2003-08-01', interval '4291:09' year(4) to month,
                       interval '02:04:59.888888' hour to second),
                      ('I2b', 'picx88882', 22273.111, 'r2b',
                       8219, 709, 'r2', 7333, .172, 5.3787E13, 9.237423E52,
                       date '2003-08-02', interval '0291-10' year(4) to month,
                       interval '12:14:57.888888' hour to second),
                       ('I2c', 'picx88883', 38223242.333, 'r2c',
                        6839, 333, 'Rr', 7812, .436, 8.1937E16, 9.22323E2,
                       date '2003-08-03', interval '7291-09' year(4) to month,
                       interval '05:27:33.888888' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'3044')
    
    stmt = """INSERT INTO receiver3 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('eee', 'picx88888', 1234567.83, '333',
                       -7291, 382, 'c2', 10, .823, 1.27839E18, 3.7289112E23,
                       date '22003-07-31', interval '4444-01' year(4) to month,
                       interval '23:09:12.666666' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'3045')

    stmt = """INSERT INTO View_R3 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('IV3', 'ViewR3', 22273.111, 'r2b',
                       8219, 709, 'r2', 7333, .172, 5.3787E13, 9.3E52,
                       date '2003-08-02', interval '0291-10' year(4) to month,
                       interval '12:14:57.888888' hour to second),
                      ('IV4', 'VR1', 38223242.333, 'r2c',
                       6839, 333, 'Rr', 7812, .906, 8.1937E16, 3.22323E12,
                       date '2003-08-03', interval '7291-09' year(4) to month,
                       interval '05:27:33.888888' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    stmt = """COMMIT WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO receiver1 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('Ia', 'cx88888', 1234567.83, 'M333',
                       -7291, 382, 'c2', 10, .823, 1.27839E18, 3.7289112E23,
                       date '2003-07-31', interval '4444-01' year(4) to month,
                       interval '23:09:12.666666' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'8402')
    
    stmt = """select * from receiver1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    
    stmt = """select * from receiver2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    
    stmt = """select * from receiver3; """
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')
    
    stmt = """control query default TABLELOCK reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default SIMILARITY_CHECK reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default QUERY_CACHE reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """delete from receiver1;"""
    output = _dci.cmdexec(stmt)

    stmt = """delete from receiver2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """delete from receiver3;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO receiver1 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I1a', 'picx8   ', 1234567.83, '333',
                       -7291, 382, 'c2', 10, .823, 1.27839E18, 3.7289112E23,
                       date '2003-07-31', interval '4444-01' year(4) to month,
                       interval '23:09:12.666666' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = """INSERT INTO receiver2 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I2a', 'picx8   ', -1273, 'r2a',
                       -8219, 79, 'R2', 12, .72, 2.3787E13, 4.237423E52,
                       date '2003-08-01', interval '4291-09' year(4) to month,
                       interval '02:04:59.888888' hour to second),
                      ('I2b', 'picx82  ', 22273.111, 'r2b',
                       8219, 709, 'r2', 7333, .172, 5.3787E13, 9.237423E52,
                       date '2003-08-02', interval '0291-10' year(4) to month,
                       interval '12:14:57.888888' hour to second),
                       ('I2c', 'picx83  ', 38223242.333, 'r2c',
                        6839, 333, 'Rr', 7812, .436, 8.1937E16, 9.22323E2,
                       date '2003-08-03', interval '7291-09' year(4) to month,
                       interval '05:27:33.888888' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)

    stmt = """INSERT INTO receiver3 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I3a', 'picx8   ', 1234567.83, '333',
                       -7291, 382, 'c2', 10, .823, 1.27839E18, 3.7289112E23,
                       date '2003-07-31', interval '4444-01' year(4) to month,
                       interval '23:09:12.666666' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default TABLELOCK 'OFF';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default QUERY_CACHE_STATEMENT_PINNING 'OFF';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default QUERY_CACHE '0';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO receiver2 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I2d', 'picx82  ', 22273.111, 'r2b',
                       8219, 709, 'r2', 7333, 9.172, 5.3787E13, 9.3E52,
                       date '2003-08-02', interval '0291-10' year(4) to month,
                       interval '12:14:57.888888' hour to second),
                       ('I2d', 'picx8888r', 38223242.333, 'r2c',
                        6839, 333, 'Rr', 7812, .906, 8.1937E16, 3.22323E12,
                       date '2003-08-03', interval '7291-09' year(4) to month,
                       interval '05:27:33.888888' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'8402')
    
    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    
    stmt = """INSERT INTO receiver2 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ((select char_3 from receiver1), 
                       'pic28882', 21273.111, 'I2b',
                       7259, 19, 'i2', 3333, .122, 7.1287E3, 8.23E5,
                       (select y_to_d from receiver1),
                       (select iy_to_mo from receiver1),
                       interval '12:14:57.123987' hour to second),
                       ('I22', 'picr888r', 82242.333,
                        (select var_char_3 from receiver1),
                        16839, 23, 'ir', 33812, .96, 3.4732E6, 6.83E12,
                        (select y_to_d from receiver1),
                        interval '7291-09' year(4) to month,
                        interval '06:27:33.888888' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    stmt = """INSERT INTO receiver1 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I1a', 'picx8   ', 1234567.83, '333',
                       -7291, 382, 'c2', 72, .823, 1.27839E18, 3.7289112E23,
                       date '2003-07-31', interval '4444-01' year(4) to month,
                       interval '13:09:12.666666' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'8102')
    
    stmt = """DROP VIEW view_r1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'20123')
    
    stmt = """DROP TABLE receiver1 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'20123')
  
    stmt = """SHOWcontrol query default TABLELOCK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6a')
    
    stmt = """SHOWcontrol query default QUERY_CACHE_STATEMENT_PINNING;"""
    output = _dci.cmdexec(stmt)
    #_dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6b')
     
    stmt = """SHOWcontrol query default QUERY_CACHE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6c')
    
    stmt = """INSERT INTO receiver3 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I3b', 'picx2801', 1357.16, 'bbb',
                       12721, 618, 'c3', 35, .472, 6.39E7, 2.9112E2,
                       date '2003-07-31', interval '2831-01' year(4) to month,
                       interval '02:19:27.228836' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO receiver3 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I3c', 'picC8801', 7.16, 'ccc',
                       11, 392, 'c4', 5, .0, 0, 0,
                       date '2003-12-11', interval '1234-11' year(4) to month,
                       interval '12:19:27.228836' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  Copy into the expect file, and then delete
    stmt = """SHOWcontrol query default TABLELOCK;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SHOWcontrol query default QUERY_CACHE_STATEMENT_PINNING;"""
    output = _dci.cmdexec(stmt)

    stmt = """SHOWcontrol query default QUERY_CACHE;"""
    output = _dci.cmdexec(stmt)

    stmt = """select * from receiver1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from receiver2;"""
    output = _dci.cmdexec(stmt)

    stmt = """select * from receiver3;"""
    output = _dci.cmdexec(stmt)

    stmt = """SHOWcontrol query default TABLELOCK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6d')

    stmt = """SHOWcontrol query default QUERY_CACHE_STATEMENT_PINNING;"""
    output = _dci.cmdexec(stmt)
    #_dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6e')

    stmt = """SHOWcontrol query default QUERY_CACHE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6f')

    stmt = """select * from receiver1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')

    stmt = """select * from receiver2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    
    stmt = """select * from receiver3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    
    #  #expect any *--- SQL operation complete.*
    #  BEGIN WORK;
    stmt = """control query default UPD_ABORT_ON_ERROR 'OFF';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """UPDATE receiver3 SET medium_int = 3993
        WHERE pic_x_8 = 'PICX8   ';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)    

    stmt = """UPDATE receiver2 SET medium_int = 2992
        WHERE pic_x_8 = 'PICX8   ';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)      

    stmt = """INSERT INTO receiver3 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('T', 'T8801', 7.16, 'ccc',
                       11, 392, 'c4', 5, .95, 0, 0,
                       date '2003-12-11', interval '1234-11' year(4) to month,
                       interval '12:19:27.228836' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)    

    stmt = """DELETE FROM receiver2 
      WHERE char_3 = 123123123123123123123123123.9 and 
            pic_x_8 = 'PICX82  ';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4041')    

    stmt = """UPDATE receiver2 SET medium_int = 1991
        WHERE pic_x_8 = 'PICX82  ';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)       

    stmt = """UPDATE receiver2 SET medium_int = 1991
        WHERE pic_x_8 = 'PICX83  ';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)          

    stmt = """DELETE FROM receiver1
      WHERE pic_x_8 = 'PICX8888' or 
            pic_decimal_2 = 99.99;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)    

    stmt = """DELETE FROM receiver2
      WHERE pic_decimal_2 = .72 and 
            float_double_p = '1.2E12' and
            pic_x_8 = upshift ('picx88882');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4041')      

    stmt = """UPDATE receiver1 SET medium_int = '9999'
    WHERE pic_x_8 = 'PICX8   ';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4039')      

    stmt = """UPDATE receiver1 SET medium_int = 9999
        WHERE pic_x_8 = 'PICX8   ';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)       

    stmt = """UPDATE receiver1 SET medium_int = 9999 + 123456789E5
        WHERE pic_x_8 = 'PICX8   ';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'8411')      

    stmt = """UPDATE receiver1 SET medium_int = 1110 
        WHERE pic_x_8 = 'PICX8   ';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)   

    stmt = """UPDATE receiver2 SET medium_int = 9999
        WHERE pic_x_8 < 'PICX82  ' and float_basic > 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)   

    stmt = """select * from receiver3
    WHERE char_3 = 'T' and
          pic_decimal_2 = .950 and
          ih_to_s = interval '12:19:27.228836' hour to second;"""
    output = _dci.cmdexec(stmt)

    stmt = """UPDATE receiver3 SET binary_64_s = 555555555555555.333,
                     small_int   = 12283,
                     var_char_2  = 'CC',
                     y_to_d      = date '2005-03-31',
                     float_basic = 3.369E12,
                     float_double_p = 3.369E12
               WHERE char_3 = 'T' and
                     pic_decimal_2 = .950 and
                     ih_to_s = interval '12:19:27.228836' hour to second;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)  

    stmt = """DELETE FROM receiver3
      WHERE char_3 = I3e and pic_decimal_2 = 3.99 and 
            cast(ih_to_s as varchar(16)) = ' 12:19:27.228836'; """
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4001') 

    # #expect any *--- SQL operation complete.*
    # COMMIT WORK;

    stmt = """control query default UPD_ABORT_ON_ERROR 'OFF';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # Copy into the expect file
    stmt = """select * from receiver1;"""
    output = _dci.cmdexec(stmt)

    stmt = """select * from receiver2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from receiver3;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from receiver1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s7')

    stmt = """select * from receiver2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s8')
    
    stmt = """select * from receiver3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s9')

    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """control query default QUERY_CACHE '0';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """control query default QUERY_CACHE_STATEMENT_PINNING 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """DELETE FROM receiver2
      WHERE pic_decimal_2 <> (select pic_decimal_2 from receiver3
                               where char_3 >= 'T');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)

    stmt = """DELETE FROM receiver3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    
    stmt = """DELETE FROM receiver1
      WHERE float_double_p is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output,1)

    stmt = """INSERT INTO receiver3 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I3y', 'picC8801', 7.16, 'ccc',
                       11, 392, 'c4', 5, .101, 0, 0,
                       date '2003-12-11', interval '1234-11' year(4) to month,
                       interval '10:10:20.000000' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = """UPDATE receiver2 SET medium_int = (select distinct(medium_int) from receiver1)
        WHERE pic_x_8 = (select pic_x_8 from receiver1
                          where pic_x_8 = 'PICX8   ') and 
                        float_basic > 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 0)  

    stmt = """UPDATE View_R3 set small_int = 906;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)  

    stmt = """DELETE FROM receiver1 
      WHERE pic_x_8 = 'PICX8   ' and y_to_d = date '2003-07-31';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)

    stmt = """ALTER TABLE receiver1 add column new_col interval day(5) to second(4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'20123')    

    stmt = """DELETE FROM receiver2
      WHERE (pic_decimal_2 is null or 
             pic_x_8 = 'XXXYYYY')  and
            float_double_p = '-99';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4041') 

    stmt = """invoke receiver1;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output,'NEW_COL') 

    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # When we went to NCI, there were a few formatting issues
    # Since this test isn't focused on ShowDDL, not going to worry about it
    # #expectfile ${test_dir}/a01exp a01s9a
    stmt = """showddl receiver1;"""
    output = _dci.cmdexec(stmt)
    
    # Think fixed these three
    stmt = """select * from receiver1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s7')

    stmt = """select * from receiver2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s8')
    
    stmt = """select * from receiver3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s9')
    
    # #expect any *--- SQL operation complete.*
    # BEGIN WORK;

    stmt = """INSERT INTO receiver1 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I1a', 'picx8   ', 1234567.83, '333',
                       -7291, 382, 'c2', 10, .823, 1.27839E18, 3.7289112E23,
                       date '2003-07-31', interval '4444-01' year(4) to month,
                       interval '23:09:12.666666' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'8102') 

    stmt = """INSERT INTO receiver2 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I2a', 'picx8   ', -1273, 'r2a',
                       -8219, 79, 'R2', 12, .72, 2.3787E13, 4.237423E52,
                       date '2003-08-01', interval '4291-09' year(4) to month,
                       interval '02:04:59.888888' hour to second),
                      ('I2b', 'picx82  ', 22273.111, 'r2b',
                       8219, 709, 'r2', 7333, .172, 5.3787E13, 9.237423E52,
                       date '2003-08-02', interval '0291-10' year(4) to month,
                       interval '12:14:57.888888' hour to second),
                       ('I2c', 'picx83  ', 38223242.333 'r2c',
                        6839, 333, 'Rr', 7812, .436, 8.1937E16, 9.22323E2,
                       date '2003-08-03', interval '7291-09' year(4) to month,
                       interval '05:27:33.888888' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'15001') 

    stmt = """INSERT INTO receiver3 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I3a', 'picx88888', 1234567.83, '333',
                       -7291, 382, 'c2', 10, .823, 1.27839E18, 3.7289112E23,
                       date '2003-07-31', interval '4444-01' year(4) to month,
                       interval '23:09:12.666666' hour to second),
                       ('I3b', 'picx33399', 38273,2, 'bbb',
                        -83721, 720, 'C2', 6223, .520, 0, 0,
                       date '2103-07-31', interval '8232-05' year(4) to month,
                       interval '99:39:19.999999' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4126') 

    stmt = """UPDATE receiver2 SET char_3 = 'UpU',
                     var_char_3 = '3vv',
                     medium_int = 79,
                     y_to_d = NULL
               WHERE pic_x_8 is not null and
                     pic_decimal_2 = .999 and
                     float_double_p = 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 0) 

    stmt = """INSERT INTO receiver2 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s) 
               VALUES ('3cc', 'picx88882', +2273, 23.285, +29, 79,
                       .109, 81.82322872342, 24.230847392),
                      ('3bb', 'picx8888r', 173, 123.3821, 83, 23774329,
                       .43, 3.2342, 34.872); """
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4023') 

    stmt = """INSERT INTO receiver1 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I1p', 'pic8888r', 167.81, '533',
                       1, 32, 'P2', 0, .3, 8.839E1, 8.72E3,
                       date '2003-08-01', interval '8444-01' year(4) to month,
                       interval '03:29:52.123456' hour to second),
                      ('I1P', 'pic888r2', 567.13, '633',
                       7, 82, '12', 47, .275, 7.9E8, 6.89E2,
                       date '2093-07-31', interval '9446-11' year(4) to month,
                       interval '63:27:00.000000' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)

    stmt = """INSERT INTO receiver3 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I3a', 'picx88888', 1234567.83, '333',
                       -7291, 382, 'c2', 10, .823, 1.27839E18, 3.7289112E23,
                       date '2003-07-31', interval '4444-01' year(4) to month,
                       interval '23:09:12.666666' hour to second),
                       ('I3b', 'picx33399', 38273,2, 'bbb',
                        -83721, 720, 'C2', 6223, .520, 0, 0,
                       date '2103-07-31', interval '8232-05' year(4) to month,
                       interval '99:39:19.999999' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4126')

    stmt = """INSERT INTO receiver2 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('E2e', 'year2003', 8932, 'RIA',
                       6714, 574, 'RI', 8012, .478, 5.7E8, 8.3E5,
                       date '9993-08-21', interval '0302-11' year(4) to month,
                       interval '99:14:00.123456' hour to second),
                       ('R2R', 'year9023', 3, 'RIB',
                        76, 330, 'RJ', 5851, .228, 4.7E08, 6.93E10,
                       date '1280-02-28', interval '9999-09' year(4) to month,
                       interval '00:04:00.123456' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    stmt = """DELETE FROM receiver2
      WHERE pic_x_8 is not null and
            pic_decimal_2 = .999 and
            float_double_p = 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)

    stmt = """UPDATE receiver3 SET y_to_d = date '9191-08-01',
                     iy_to_mo = iy_to_mo + interval - '9220' year(4)
               WHERE cast(ih_to_s as varchar(16)) =  ' 12:19:27.228836';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 0)

    stmt = """UPDATE receiver3 SET y_to_d = date '9191-08',
                     iy_to_mo = iy_to_mo + interval - '922012' year(6),
                     ih_to_s = ih_to_s - interval '99.999999' second
               WHERE cast(ih_to_s as varchar(16)) =  '99:39:19.999999' or 
                     (char_3 = 'I3a' and
                     pic_decimal_2 = .823);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'3045')

    stmt = """INSERT INTO receiver1 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_double_p,
                       ih_to_s)
               VALUES (NULL, 'Isagain', NULL, NULL,
                       NULL, NULL, null, null, .823, 9.11111E18,
                       interval '78:00:02.999999' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = """INSERT INTO receiver1 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_double_p,
                       ih_to_s)
               VALUES (NULL, null, NULL, NULL,
                       NULL, NULL, null, null, .823, 9.11111E18,
                       interval '78:00:02.999999' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4122')
    
    stmt = """INSERT INTO receiver1 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUE ('I1a', 'WrongRow', 1234567.83, '333',
                       -7291, 382, 'c2', 10, .823, 1.27839E18, 3.7289112E23,
                       date '2003-07-31', interval '4444-01' year(4) to month,
                       interval '23:09:12.666666' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'15001')
    
    stmt = """UPDATE receiver3 SET y_to_d = date '9191-08',
                     iy_to_mo = iy_to_mo + interval - '9220' year(4),
                     ih_to_s = ih_to_s - interval '99.999999' second,
                     pic_x_8 = NULL
               WHERE cast(ih_to_s as varchar(16)) =  '99:39:19.999999' and
                     char_3 = 'I1a' and
                     pic_decimal_2 = .823;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'3045')

    stmt = """select * from receiver1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s10')

    stmt = """select * from receiver2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s11')
    
    stmt = """select * from receiver3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s12')
    
    stmt = """delete from receiver2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output,5)

    stmt = """showcontrol ALL;"""
    output = _dci.cmdexec(stmt)
    stmt = """delete from receiver2;"""
    output = _dci.cmdexec(stmt)

    
    stmt = """INSERT INTO receiver2 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I2a', 'picx8888', -1273, 'r2a',
                       -8219, 79, 'R2', 12, .72, 2.3787E13, 4.237423E52,
                       date '2003-08-01', interval '4291-09' year(4) to month,
                       interval '02:04:59.888888' hour to second),
                      ('I2b', 'picx8882', 22273.111, 'r2b',
                       8219, 709, 'r2', 7333, .172, 5.3787E13, 9.237423E52,
                       date '2003-08-02', interval '0291-10' year(4) to month,
                       interval '12:14:57.888888' hour to second),
                       ('I2c', 'picx8883', 38223242.333, 'r2c',
                        6839, 333, 'Rr', 7812, .436, 8.1937E16, 9.22323E2,
                       date '2003-08-03', interval '7291-09' year(4) to month,
                       interval '05:27:33.888888' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)

    stmt = """control query default ISOLATION_LEVEL 'READ UNCOMMITTED';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """control query default QUERY_CACHE '0';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """control query default ISOLATION_LEVEL 'READ COMMITTED';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP VIEW VIEW_R1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE receiver1 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """  CREATE TABLE receiver1 (
        char_3                 char(3),
        pic_x_8                char(8) upshift not null,
        binary_64_s            numeric(18, 3) signed,
        var_char_3             varchar(3) upshift,
        small_int              smallint signed,
        decimal_3_unsigned     decimal(3, 0) unsigned,
        var_char_2             varchar(2),
        medium_int             integer unsigned,
        pic_decimal_2          decimal(3,3) not null,
        float_basic            float (4),
        float_double_p         double precision not null,
        y_to_d                 date,
        iy_to_mo               interval year(4) to month,
        ih_to_s                interval hour to second not null,
        PRIMARY KEY (pic_x_8));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """Create view View_R1 as (select * from receiver1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """INSERT INTO receiver1 (pic_x_8, pic_decimal_2, float_double_p, ih_to_s)
               VALUES (NULL, 0.982, 1.283E12,
                       interval '99:00.982312' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'3044')
    
    stmt = """INSERT INTO receiver1 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I1a', 'picx8888', 1234567.83, '333',
                       -7291, 382, 'c2', 10, .823, 1.27839E18, 3.7289112E23,
                       date '2003-07-31', interval '4444-01' year(4) to month,
                       interval '23:09:12.666666' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO receiver3 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I3a', 'picx8888', 1234567.83, '333',
                       -7291, 382, 'c2', 10, .823, 1.27839E18, 3.7289112E23,
                       date '2003-07-31', interval '4444-01' year(4) to month,
                       interval '23:09:12.666666' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'8102')
    # #expect any *--- SQL operation complete.*
    # COMMIT WORK;
    
    #  12/30/03 EL  These queries on table pic8 are for the bug reported in
    stmt = """create table pic8 (a pic x(8));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into pic8 values ('123456789');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'8402')
    
    stmt = """insert into pic8 values ('123456789'), ('picx88888'), ('picx88883');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'8402')

    stmt = """showcontrol default ISOLATION_LEVEL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s12a')
    
    stmt = """showcontrol default QUERY_CACHE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s12b')
    
    # Think fixed these 
    stmt = """select * from receiver1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s13')
    
    stmt = """select * from receiver2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s14')

    stmt = """select * from receiver3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s15')

    stmt = """delete from receiver1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    stmt = """delete from receiver2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    stmt = """delete from receiver3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    stmt = """control query default ISOLATION_LEVEL reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default QUERY_CACHE reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
# -------------------------------------------------------------------
#testcase a02 a02
# --------------------------------------------------------------------

# 
#  In this test case a02, these options are used:
# 
#  CQD UPD_PARTIAL_ON_ERROR is set ON to some BEGIN/ROLLBACK/COMMIT WORK
#  frames,
#  The target tables have primary keys, but no any index and constraints,
#  The main focus is on INSERT/SELECT statement only on one row, and
#      multiple rows.
#      and also mixed in some INSERT statement with a single VALUES clause.
#  The UPDATE statement with an equality predicate on primary keys,
#  The DELETE statement with an equality predicate on primary keys.
# 
def test002(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    setup._init2(_testmgr, _testlist)

    stmt = """set transaction READ WRITE;"""
    output = _dci.cmdexec(stmt)
    stmt = """control query default UPD_SAVEPOINT_ON_ERROR 'OFF';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """control query default UPD_ABORT_ON_ERROR 'OFF';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from receiver1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default UPD_ABORT_ON_ERROR 'OFF';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """control query default QUERY_CACHE_STATEMENT_PINNING 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default TABLELOCK 'OFF';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


    stmt = """INSERT INTO receiver1 (SELECT * FROM Target_Rows
                               WHERE pic_x_8 > 'AAA' and
                                     pic_x_8 < 'TROWC   ' and
                                     pic_x_8 is not null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)

    stmt = """INSERT INTO receiver1 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES (null, 'picx8888', 1234567.83, '333',
                       -7291, 382, 'c2', 10, .823, 1.27839E18, 3.7289112E23,
                       date '2003-07-31', interval '4444-01' year(4) to month,
                       interval '23:09:12.666666' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO receiver2 (SELECT * FROM Target_Row1 T1 
                          left join Target_Row1 T2 on 
                T1.pic_x_8 = T2.pic_decimal_2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4041')
    
    stmt = """select * from receiver1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    
    stmt = """INSERT INTO receiver2 (SELECT * from Target_Row1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)
    
    stmt = """UPDATE receiver2 SET pic_decimal_2 = NULL,
                     float_basic = 3.3333E7,
                     y_to_d = current_date,
                     iy_to_mo = iy_to_mo + interval '23' year,
                     ih_to_s = ih_to_s + interval '24' hour
               WHERE pic_x_8 = 'CXX' and
                     pic_decimal_2 = 0.123 or
                     float_double_p = 3.72001E76;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4033')
    
    stmt = """DELETE receiver1 WHERE pic_x_8 is null; """
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'15001')
    
    stmt = """SELECT * FROM Target_Rows where pic_x_8 > 'TROWB';"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO receiver1 (SELECT * FROM Target_Rows where pic_x_8 > 'TROWB');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    stmt = """UPDATE receiver2 SET float_basic = 3.3333E7,
                     y_to_d = current_date,
                     iy_to_mo = iy_to_mo + interval - '23' year,
                     ih_to_s = ih_to_s + interval - '24' hour
               WHERE pic_x_8 = 'TARGROWS' and
                     pic_decimal_2 = 0.123 and 
                     (float_double_p >= 1.72000999999999968E+077 or
                      float_double_p <= 1.72000999999999968E+077);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """UPDATE receiver2 SET pic_decimal_2 = NULL,
                     float_basic = 3.3333E7,
                     y_to_d = current_date,
                     iy_to_mo = iy_to_mo + interval '23' year,
                     ih_to_s = ih_to_s + interval '24' hour
               WHERE pic_x_8 = 'TARGROWS' and
                     pic_decimal_2 = 0.123 and 
                     float_double_p = 1.72000999999999968E+077;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4033')

    stmt = """COMMIT WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default UPD_ABORT_ON_ERROR 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """control query default QUERY_CACHE_STATEMENT_PINNING reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """control query default TABLELOCK reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from receiver1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    
    stmt = """select * from receiver2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    
    stmt = """select * from receiver3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')

    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default TABLELOCK 'OFF';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default QUERY_CACHE '0';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default SIMILARITY_CHECK 'OFF';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """INSERT INTO receiver3 (SELECT * FROM receiver1
                        WHERE char_3 is not null and
                              pic_decimal_2 is not null and
                              ih_to_s is not null
                       UNION 
                       SELECT * FROM receiver2
                        WHERE char_3 is not null and
                              pic_decimal_2 is not null and
                              ih_to_s is not null );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 8)

    stmt = """INSERT INTO receiver3 (SELECT * FROM receiver1 Ra
                               right join receiver2 R2 on
                                     R1.char_3 <> R2.char_3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4002')

    stmt = """INSERT INTO receiver3 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I3a', 'pic88888', 1234567.83, '333',
                       -7291, 382, 'c2', 10, .823, 1.27839E18, 3.7289112E23,
                       date '2003-07-31', interval '4444-01' year(4) to month,
                       interval '23:09:12.666666' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = """INSERT INTO receiver2 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I2a', 'pic88888', -1273, 'r2a',
                       -8219, 79, 'R2', 12, .72, 2.3787E13, 4.237423E52,
                       date '2003-08-01', interval '4291-09' year(4) to month,
                       interval '02:04:59.888888' hour to second),
                      ('I2b', 'pic88882', 22273.111, 'r2b',
                       8219, 709, 'r2', 7333, .172, 5.3787E13, 9.237423E52,
                       date '2003-08-02', interval '0291-10' year(4) to month,
                       interval '12:14:57.888888' hour to second),
                       ('I2c', 'pic88883', 38223242.333, 'r2c',
                        6839, 333, 'Rr', 7812, .436, 8.1937E16, 9.22323E2,
                       date '2003-08-03', interval '7291-09' year(4) to month,
                       interval '05:27:33.888888' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)

    stmt = """INSERT INTO receiver3 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I3a', 'pic1    ', 1234567.83, '333',
                       -7291, 382, 'c2', 10, .23, 1.27839E11118, 3.7289112E23,
                       date '2003-07-31', interval '4444-01' year(4) to month,
                       interval '23:09:12.666656' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'3166')

    stmt = """UPDATE receiver2 SET pic_x_8 = null, pic_decimal_2 = null, float_double_p = null
               WHERE (pic_x_8 = 'I2c' and pic_decimal_2 = 0.436) or  
                     float_double_p = 9.22323E2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4033')
    
    stmt = """delete from receiver2 where pic_x_8 like 'T%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)  

    stmt = """INSERT INTO receiver2 (SELECT * FROM Target_Rows);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)

    stmt = """DELETE FROM receiver2 WHERE SET (pic_x_8 = 'I2c' and pic_decimal_2 = 0.436) or
                                 float_double_p = 9.22323E2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'15001')
    
    stmt = """UPDATE receiver3 SET var_char3_3 = 'PoP',var_char_2 = 'V2'
               WHERE char_3 = 'I3a' and
                     pic_decimal_2 = .823 and
                     ih_to_s = interval '23:09:12.666666' hour to second;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4001')
    
    stmt = """COMMIT WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP TABLE Target_Rows cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # #expect any *--- SQL operation complete.*
    # BEGIN WORK;
    stmt = """DELETE FROM receiver3 WHERE var_char3_3 = 'PoP';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4001')
    
    stmt = """INSERT INTO receiver1 (SELECT * FROM reciever3 WHERE var_char3_3 = 'PoP');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4082')
    
    stmt = """INSERT INTO receiver3 (SELECT * FROM Target_Rows);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4082')
    
    stmt = """UPDATE receiver3 SET var_char_3 = 'PoP',
                     var_char_2 = 'V2'
              WHERE pic_x_8 = upper('TargRows');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)

    stmt = """CREATE TABLE target_rows (
        char_3                 char(3),
        pic_x_8                char(8) upshift not null,
        binary_64_s            numeric(18, 3) signed,
        var_char_3             varchar(3) upshift,
        small_int              smallint signed,
        decimal_3_unsigned     decimal(3, 0) unsigned,
        var_char_2             varchar(2),
        medium_int             integer unsigned,
        pic_decimal_2          decimal(3,3) not null,
        float_basic            float (4),
        float_double_p         double precision not null,
        y_to_d                 date,
        iy_to_mo               interval year(4) to month,
        ih_to_s                interval hour to second not null,
        PRIMARY KEY (pic_x_8, ih_to_s));"""
        # PRIMARY KEY (pic_x_8, pic_decimal_2, float_double_p, ih_to_s));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """UPDATE receiver1 SET pic_decimal_2 = 3.6 * 12.6724
                     y_to_d        = date '3333-12-31'
              WHERE pic_x_8 = 'DXX';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'15001')

    stmt = """INSERT INTO target_rows (char_3, pic_x_8, binary_64_s, var_char_3,
                           small_int, decimal_3_unsigned, var_char_2,
                           medium_int, pic_decimal_2, float_basic,
                           float_double_p, y_to_d,
                           iy_to_mo,
                           ih_to_s)
                   VALUES ('AXX', 'TRowA', 13579135.13, 'Vc1',
                           32765, 123, 'v1',
                           217483640,  .123, 2.72001E76,
                           2.72001E76, date '2003-08-01',
                           interval '9999-11' year(4) to month,
                           interval '19:59:59.999999' hour to second),

                          ('BXX', 'TRowB', 123456789012345.123, 'Vc2',
                           -32765, 321, 'v2',
                           27860,  .223, 1.72001E76,
                           1.72001E76, date '2023-08-01',
                           interval '2999-11' year(4) to month,
                           interval '29:29:29.222222' hour to second),

                          ('CXX', 'TRowC', 2468024.2, 'Vc3',
                           265, 123, 'vc',
                           217483640, 0.123, 3.72001E76,
                           3.72001E76, date '3003-08-01',
                           interval '9999-11' year(4) to month,
                           interval '39:59:59.333333' hour to second),

                          ('DXX', 'TRowD', 456012.123, 'Vc4',
                           65, 0, 'v4',
                           483, 0.3, 1.72001E76,
                           4.72001E76, date '2003-08-01',
                           interval '4999-11' year(4) to month,
                           interval '49:59:59.999999' hour to second),

                          ('EXX', 'TargRows', 123456789012345.123, 'Vc3',
                           32765, 123, 'vc',
                           217483640, 0.123, 1.72001E76,
                           1.72001E76, date '2003-08-01',
                           interval '9999-11' year(4) to month,
                           interval '59:59:59.999999' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)

    stmt = """select pic_x_8, pic_decimal_2, float_double_p, ih_to_s from target_rows;"""
    output = _dci.cmdexec(stmt)
    stmt = """select pic_x_8, pic_decimal_2, float_double_p, ih_to_s from target_row1;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO Target_rows (SELECT * FROM Target_row1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """DELETE FROM Target_rows WHERE (pic_x_8 = upper('TargRows') and char_3 = 'XXX') or
                              char_3 = '123' or
                              char_3 = '333';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)
    
    stmt = """UPDATE receiver1 SET pic_decimal_2 = 3.6 * 12
                     ih_to_s       = interval '16-22:123456' hour to second 
              WHERE pic_x_8 = 'DXX';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'15001')

    stmt = """UPDATE receiver1 SET pic_decimal_2 = .36 * 1.2,
                     ih_to_s       = interval - '16:22:11.123456' hour to second
              WHERE char_3 = 'DXX';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)

    stmt = """INSERT INTO Target_rows (SELECT * FROM Target_row1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)

    stmt = """select * from Target_rows;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s4')
    
    stmt = """DELETE FROM Target_rows WHERE pic_x_8 like '%ROWS';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    
    stmt = """select * from target_rows where pic_x_8 like '%ROWS';"""
    output = _dci.cmdexec(stmt)

    stmt = """UPDATE receiver1 SET pic_decimal_2 = '3.6 * 12',
                     ih_to_s       = interval '-16:22.123456' hour to second
              WHERE pic_x_8 = (SELECT pic_x_8 
                                 FROM Target_Rows
                                WHERE pic_x_8 = 'DXX');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'3044')

    stmt = """INSERT INTO Target_rows VALUES ('XXX', 'TargRows', 123456789012345.123, 'Vc3',
                                32765, 123, 'vc',
                                217483640,  .123, 1.72001E76,
                                1.72001E76, date '2003-08-01',
                                interval '9999-11' year(4) to month,
                                interval '99:59:59.999999' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """control query default TABLELOCK reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default QUERY_CACHE reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default SIMILARITY_CHECK reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from receiver1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')

    stmt = """select * from receiver2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5a')

    stmt = """select * from receiver3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s6')

    stmt = """select * from Target_rows;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s6a')

    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default UPD_ABORT_ON_ERROR 'OFF';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """INSERT INTO receiver3 (SELECT * FROM receiver1 R1
                               right join receiver2 R2 on
                                     R1.char_3 <> R2.char_3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4023')
    
    stmt = """INSERT INTO receiver3 (SELECT * FROM receiver1 Ra
                               right join receiver2 R2 on
                                     Ra.char_3 <> R1.char_3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4002')

    stmt = """INSERT INTO receiver3 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I3y', 'picx8888', 1234567.83, '333',
                       -7291, 382, 'c2', 10, .923, 1.27839E18, 3.7289112E23,
                       date '2003-07-31', interval '4444-01' year(4) to month,
                       interval '23:09:12.666616' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = """INSERT INTO receiver2 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I2q', 'picx8888', -1273, 'r2a',
                       -8219, 79, 'R2', 12, .72, 2.3787E13, 4.237423E52,
                       date '2003-08-01', interval '4291-09' year(4) to month,
                       interval '02:04:59.888888' hour to second),
                      ('I2o', 'picx8882', 22273.111, 'r2b',
                       8219, 709, 'r2', 7333, .172, 5.3787E13, 9.237423E52,
                       date '2003-08-02', interval '0291-10' year(4) to month,
                       interval '12:14:57.888888' hour to second),
                       ('I2z', 'picx8883', 38223242.333,'r2c',
                        6839, 333, 'Rr', 7812, .436, 8.1937E16, 9.22323E2,
                       date '2003-08-03', interval '7291-09' year(4) to month,
                       interval '05:27:33.888888' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)
    
    stmt = """INSERT INTO receiver3 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I3a', 'picx88888', 1234567.83, '333',
                       -7291, 382, 'c2', 10, .823, 1.27839E18, 3.7289112E23,
                       date '2003-07-31', interval '4444-01' year(4) to month,
                       interval '23:09:12.666666' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'8402')
    
    stmt = """UPDATE receiver2 SET pic_x_8 = null, pic_decimal_2 = null, float_double_p = null
               WHERE (pic_x_8 = 'I2c' and pic_decimal_2 = 0.436) or
                     float_double_p = 9.22323E2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4033')
    
    stmt = """DELETE FROM receiver2 WHERE SET (pic_x_8 = 'I2c' and pic_decimal_2 = 0.436) or
                                 float_double_p = 9.22323E2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'15001')
    
    stmt = """UPDATE receiver3 SET var_char3 = 'PoP',
                     var_char_2 = 'V2'
               WHERE char_3 = 'I3a' and
                     pic_decimal_2 = .823 and
                     ih_to_s = interval '23:09:12.666666' hour to second
               ORDER BY 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'15001')
    
    stmt = """DELETE FROM receiver3 WHERE var_char3_3 = 'PoP';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4001')
    
    stmt = """INSERT INTO receiver1 (SELECT * FROM reciever3 WHERE var_char3_3 = 'PoP');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4082')

    stmt = """DELETE FROM receiver3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output,10)
    
    stmt = """INSERT INTO receiver3 (SELECT * FROM Target_Rows);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 7)

    stmt = """UPDATE receiver3 SET var_char_3 = 'PoP',
                     var_char_2 = 'V2'
              WHERE pic_x_8 = upper('TargRows');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)

    stmt = """UPDATE receiver3 SET var_char_3 = 'PoP',var_char_2 = 'V2',
                      binary_64_s = binary_64_s +1.283E24
              WHERE pic_x_8 = upper('TargRows') and
                    char_3  = 'EXX' and
                    ih_to_s = interval '59:59:59.999999' hour to second;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 0)

    stmt = """UPDATE receiver1 SET pic_decimal_2 = 3.6 * 12.6724
                     y_to_d        = date '3333-12-31'
              WHERE pic_x_8 = 'DXX';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'15001')
    
    stmt = """UPDATE receiver1 SET pic_decimal_2 = 3.6 * 12
                     ih_to_s       = interval '16-22:123456' hour to second
              WHERE pic_x_8 = 'DXX';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'15001')
 
    stmt = """UPDATE receiver1 SET pic_decimal_2 = .36 * 1.2,
                     ih_to_s       = interval - '33:16:22.123456' hour to second
              WHERE char_3 = 'DXX';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """UPDATE receiver1 SET pic_decimal_2 = '3.6 * 12',
                     ih_to_s       = interval '00:16:22.123456' hour to second
              WHERE pic_x_8 = (SELECT pic_x_8
                                 FROM Target_Rows
                                WHERE pic_x_8 = 'DXX');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4039')

    stmt = """ROLLBACK; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from receiver1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')

    stmt = """select * from receiver2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5a')

    stmt = """select * from receiver3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s6')

    stmt = """delete from receiver1;"""
    output = _dci.cmdexec(stmt)
    stmt = """delete from receiver2;"""
    output = _dci.cmdexec(stmt)
    stmt = """delete from receiver3;"""
    output = _dci.cmdexec(stmt)
    stmt = """delete from target_rows;"""
    output = _dci.cmdexec(stmt)
    stmt = """delete from target_row1;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO target_rows (char_3, pic_x_8, binary_64_s, var_char_3,
                           small_int, decimal_3_unsigned, var_char_2,
                           medium_int, pic_decimal_2, float_basic,
                           float_double_p, y_to_d,
                           iy_to_mo,
                           ih_to_s)
                   VALUES ('AXX', 'TRowA', 13579135.13, 'Vc1',
                           32765, 123, 'v1',
                           217483640,  .123, 2.72001E76,
                           2.72001E76, date '2003-08-01',
                           interval '9999-11' year(4) to month,
                           interval '19:59:59.999999' hour to second),

                          ('BXX', 'TRowB', 123456789012345.123, 'Vc2',
                           -32765, 321, 'v2',
                           27860,  .223, 1.72001E76,
                           1.72001E76, date '2023-08-01',
                           interval '2999-11' year(4) to month,
                           interval '29:29:29.222222' hour to second),

                          ('CXX', 'TRowC', 2468024.2, 'Vc3',
                           265, 123, 'vc',
                           217483640, 0.123, 3.72001E76,
                           3.72001E76, date '3003-08-01',
                           interval '9999-11' year(4) to month,
                           interval '39:59:59.333333' hour to second),

                          ('DXX', 'TRowD', 456012.123, 'Vc4',
                           65, 0, 'v4',
                           483, 0.3, 1.72001E76,
                           4.72001E76, date '2003-08-01',
                           interval '4999-11' year(4) to month,
                           interval '49:59:59.999999' hour to second),

                          ('EXX', 'TargRows', 123456789012345.123, 'Vc3',
                           32765, 123, 'vc',
                           217483640, 0.123, 1.72001E76,
                           1.72001E76, date '2003-08-01',
                           interval '9999-11' year(4) to month,
                           interval '59:59:59.999999' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
 
    stmt = """INSERT INTO target_row1 (char_3, pic_x_8, binary_64_s, var_char_3,
                           small_int, decimal_3_unsigned, var_char_2,
                           medium_int, pic_decimal_2, float_basic,
                           float_double_p, y_to_d,
                           iy_to_mo,
                           ih_to_s)
                   VALUES ('XXX', 'TargRows', 123456789012345.123, 'Vc3',
                           32765, 123, 'vc',
                           217483640,  .123, 1.72001E76,
                           1.72001E76, date '2003-08-01',
                           interval '9999-11' year(4) to month,
                           interval '99:59:59.999999' hour to second),

                          ('123', 'TargRow2', 6789012345.12, 'V32',
                           25, 23, 'v2',
                           4830,  .23, 1.22001E76,
                           1.22001E76, date '2003-02-01',
                           interval '2222-11' year(4) to month,
                           interval '22:22:29.222222' hour to second),

                          ('333', 'TargRow3', 12345.13, 'Vc3',
                           5, 3, 'v3',
                           217,  .3, 1.32001E76,
                           1.32001E76, date '2003-03-01',
                           interval '3333-11' year(4) to month,
                           interval '39:39:39.333333' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)

    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """  INSERT INTO target_row1 (char_3, pic_x_8, binary_64_s, var_char_3,
                           small_int, decimal_3_unsigned, var_char_2,
                           medium_int, pic_decimal_2, float_basic,
                           float_double_p, y_to_d,
                           iy_to_mo,
                           ih_to_s)
                   VALUES ('AXX', 'TRowA', 13579135.13, 'Vc1',
                           32765, 123, 'v1',
                           217483640,  .123, 2.72001E76,
                           2.72001E76, date '2003-08-01',
                           interval '9999-11' year(4) to month,
                           interval '19:59:59.999999' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO receiver1 (char_3, pic_x_8, binary_64_s, var_char_3,
                         small_int, decimal_3_unsigned, var_char_2,
                         medium_int, pic_decimal_2, float_basic,
                         float_double_p, y_to_d,
                         iy_to_mo,
                         ih_to_s)
                 VALUES ('AXX', 'TRowA', 13579135.13, 'Vc1',
                         32765, 123, 'v1',
                         217483640,  .123, 2.72001E76,
                         2.72001E76, date '2003-08-01',
                         interval '9999-11' year(4) to month,
                         interval '19:59:59.999999' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO receiver3 (SELECT * FROM Target_rows t1
                        WHERE t1.pic_x_8 = (select max(t2.pic_x_8)
                                              from target_row1 t2 ) or
                      t1.decimal_3_unsigned = (select max(t2.decimal_3_unsigned)
                                               from target_row1 t2));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)

    stmt = """INSERT INTO receiver3 (char_3, pic_x_8, binary_64_s, var_char_3,
                           small_int, decimal_3_unsigned, var_char_2,
                           medium_int, pic_decimal_2, float_basic) 
            (SELECT * FROM Target_rows t1
                            left join Target_row1 t2 on
                                 t1.pic_x_8 = t2.pic_x_8 and
                                 t1.decimal_3_unsigned = t2.decimal_3_unsigned);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4023')

    stmt = """UPDATE receiver3 SET decimal_3_unsigned = 804,
                     var_char_3 = 'Upd',
                     medium_int = 20030804,
                     y_to_d = date current_date
               WHERE char_3 = 'AXX' and 
                     pic_decimal_2 = .123 and
                     ih_to_s = '19:59:59.999999';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'15001')
    
    stmt = """DELETE FROM receiver3 WHERE char_3 = (select char_3 from receiver1) and 
                            pic_decimal_2 = .123 and
                            ih_to_s = interval '19:59:59.999999' hour to second;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)

    stmt = """COMMIT WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from receiver1;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from receiver3;"""
    output = _dci.cmdexec(stmt)

    stmt = """select * from receiver1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s7')
 
    stmt = """select * from receiver2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output,0)
    
    stmt = """select * from receiver3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s8')

    stmt = """control query default UPD_ABORT_ON_ERROR 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)
# --------------------------------------------------------------------
#testcase a03 a03
# --------------------------------------------------------------------

# 
#  In this test case a03, these options are used:
# 
#  CQD UPD_PARTIAL_ON_ERROR is set ON for some BEGIN/ROLLBACK/COMMIT
#  WORK frames, 
#  The target tables have primary keys, with indexes and constraints, 
#  The main focus is on INSERT statement with a single VALUES clause,
#  The UPDATE statement with an equality predicate on primary keys,
#  The DELETE statement with an equality predicate on primary keys.
# 
#  This is the same test case as a01, except there are indexes and
#  constraints are added to the tables;
# 

def test003(desc="""a03 """):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    setup._init2(_testmgr, _testlist)

    stmt = """control query default UPD_SAVEPOINT_ON_ERROR 'OFF';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index receiver1a
      on receiver1 (char_3)
      ATTRIBUTES
      blocksize 4096;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create unique index receiver1b
      on receiver1 (medium_int)
      ATTRIBUTES
      blocksize 4096;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index receiver1c
      on receiver1 (pic_decimal_2, binary_64_s)
      ATTRIBUTES
      blocksize 4096;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index receiver1d 
      on receiver1 (pic_decimal_2, binary_64_s)
      ATTRIBUTES
      blocksize 4096;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index receiver1e
      on receiver1 (float_double_p ASC)
      ATTRIBUTES
      blocksize 4096;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """alter table receiver1 add constraint r1c1
           check (y_to_d > date '0001-05-08');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index receiver2a
      on receiver2 (var_char_3)
      ATTRIBUTES
      blocksize 4096;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index receiver2b
      on receiver2 (y_to_d)
      ATTRIBUTES
      blocksize 4096;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index receiver2c
      on receiver2 (float_double_p ASC)
      ATTRIBUTES
      blocksize 4096;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index receiver2d
      on receiver2 (pic_decimal_2, binary_64_s)
      ATTRIBUTES
      blocksize 4096;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create index receiver2e
      on receiver2 (float_double_p ASC)
      ATTRIBUTES
      blocksize 4096;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table receiver2 add constraint r2c1
       check (iy_to_mo is not null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """alter table receiver2 add constraint r2c2
           check (small_int < 999989888999);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index receiver3a
      on receiver3 (iy_to_mo, y_to_d, medium_int)
      ATTRIBUTES
      auditcompress,
      blocksize 4096,
      clearonpurge,
      extent (32,128),
      maxextents 320;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create unique index receiver3b
      on  receiver3 (small_int)
      ATTRIBUTES
      blocksize 4096;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index receiver3c
      on receiver3 (y_to_d DESC)
      ATTRIBUTES
      blocksize 4096;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index receiver3d
      on receiver3 (pic_decimal_2, binary_64_s)
      ATTRIBUTES
      blocksize 4096;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index receiver3e 
      on receiver3 (float_double_p ASC)
      ATTRIBUTES
      blocksize 4096;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """alter table receiver3 add constraint r3c1
           check (float_basic is not null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """alter table receiver3 add constraint r3c2 unique (char_3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table receiver3 add constraint r3c3
          check (iy_to_mo is not null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default UPD_ABORT_ON_ERROR 'OFF';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """INSERT INTO receiver1 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I1a', 'pica8888', 1234567.83, '333',
                       -7291, 382, 'c2', 10, .823, 1.27839E18, 3.7289112E23,
                       date '2003-07-31', interval '4444-01' year(4) to month,
                       interval '23:09:12.666666' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = """INSERT INTO receiver2 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I2a', 'pica8888', -1273, 'r2a',
                       -8219, 79, 'R2', 12, .72, 2.3787E13, 4.237423E52,
                       date '2003-08-01', interval '4291-09' year(4) to month,
                       interval '02:04:59.888888' hour to second),
                      ('I2b', 'picb8882', 22273.111, 'r2b',
                       8219, 709, 'r2', 7333, .172, 5.3787E13, 9.237423E52,
                       date '2003-08-02', interval '0291-10' year(4) to month,
                       interval '12:14:57.888888' hour to second),
                       ('I2c', 'picc8883', 38223242.333, 'r2c',
                        6839, 333, 'Rr', 7812, .436, 8.1937E16, 9.22323E2,
                       date '2003-08-03', interval '7291-09' year(4) to month,
                       interval '05:27:33.888888' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)

    stmt = """INSERT INTO receiver3 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I3a', 'pic38888', 1234567.83, '333',
                       -7291, 382, 'c2', 10, .823, 1.27839E18, 3.7289112E23,
                       date '2003-07-31', interval '4444-01' year(4) to month,
                       interval '23:09:12.666666' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = """UPDATE recevier2 SET char_3 = '4444',
                     iy_to_mo = NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4082')

    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from receiver1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select * from receiver2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select * from receiver3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)

    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """control query default TABLELOCK 'OFF';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """control query default SIMILARITY_CHECK 'OFF';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """control query default QUERY_CACHE '0';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """INSERT INTO receiver1 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I1a', 'pica8888', 1234567.83, '333',
                       -7291, 382, 'c2', 10, .823, 1.27839E18, 3.7289112E23,
                       date '2003-07-31', interval '4444-01' year(4) to month,
                       interval '23:09:12.666666' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO receiver2 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I2a', 'pica8888', -1273, 'r2a',
                       -8219, 79, 'R2', 12, .72, 2.3787E13, 4.237423E52,
                       date '2003-08-01', interval '4291-09' year(4) to month,
                       interval '02:04:59.888888' hour to second),
                      ('I2b', 'picb8882', 22273.111, 'r2b',
                       8219, 709, 'r2', 7333, .172, 5.3787E13, 9.237423E52,
                       date '2003-08-02', interval '0291-10' year(4) to month,
                       interval '12:14:57.888888' hour to second),
                       ('I2c', 'picc8883', 38223242.333, 'r2c',
                        6839, 333, 'Rr', 7812, .436, 8.1937E16, 9.22323E2,
                       date '2003-08-03', interval '7291-09' year(4) to month,
                       interval '05:27:33.888888' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)

    stmt = """INSERT INTO receiver3 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I3a', 'pic38888', 1234567.83, '333',
                       -7291, 382, 'c2', 10, .823, 1.27839E18, 3.7289112E23,
                       date '2003-07-31', interval '4444-01' year(4) to month,
                       interval '23:09:12.666666' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # Copy to expect file
    stmt = """select * from receiver1;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from receiver2;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from receiver3;"""
    output = _dci.cmdexec(stmt)

    stmt = """select * from receiver1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    
    stmt = """select * from receiver2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    
    stmt = """select * from receiver3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s3')

    stmt = """UPDATE receiver1 SET  pic_x_8 = 'PRIMKEY'
       WHERE pic_x_8 = 'PICX8';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4033')

    stmt = """UPDATE receiver1 SET char_3 = 'UPD'
       WHERE pic_x_8 = 'PICA8888';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)

    stmt = """INSERT INTO receiver1 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I1a', 'picb8888', 1234567.83, '333',
                       -7291, 382, 'c2', 20, .823, 1.27839E18, 3.7289112E23,
                       date '2003-07-31', interval '4444-01' year(4) to month,
                       interval '23:09:12.666666' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from receiver1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0) 
    
    stmt = """select * from receiver2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0) 
    
    stmt = """select * from receiver3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0) 
 
    stmt = """control query default TABLELOCK 'OFF';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """control query default SIMILARITY_CHECK 'OFF';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default QUERY_CACHE '0';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO receiver1 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I1a', 'pica8888', 1234567.83, '333',
                       -7291, 382, 'c2', 10, .823, 1.27839E18, 3.7289112E23,
                       date '2003-07-31', interval '4444-01' year(4) to month,
                       interval '23:09:12.666666' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO receiver2 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I2a', 'pica8888', -1273, 'r2a',
                       -8219, 79, 'R2', 12, .72, 2.3787E13, 4.237423E52,
                       date '2003-08-01', interval '4291-09' year(4) to month,
                       interval '02:04:59.888888' hour to second),
                      ('I2b', 'picb8882', 22273.111, 'r2b',
                       8219, 709, 'r2', 7333, .172, 5.3787E13, 9.237423E52,
                       date '2003-08-02', interval '0291-10' year(4) to month,
                       interval '12:14:57.888888' hour to second),
                       ('I2c', 'picc8883', 38223242.333, 'r2c',
                        6839, 333, 'Rr', 7812, .436, 8.1937E16, 9.22323E2,
                       date '2003-08-03', interval '7291-09' year(4) to month,
                       interval '05:27:33.888888' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)

    stmt = """INSERT INTO receiver3 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I3a', 'pic38888', 1234567.83, '333',
                       -7291, 382, 'c2', 10, .823, 1.27839E18, 3.7289112E23,
                       date '2003-07-31', interval '4444-01' year(4) to month,
                       interval '23:09:12.666666' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = """UPDATE receiver1 SET char_3 = 'UPD'
       WHERE pic_x_8 = 'PICA8888';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)

    stmt = """INSERT INTO receiver2 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsiged, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I2a', 'pic8888 ', -1273, 'r2a',
                       -8219, 79, 'R2', 12, .72, 2.3787E13, 4.237423E52,
                       date '2003-08-01', interval '4291:09' year(4) to month,
                       interval '02:04:59.888888' hour to second),
                      ('I2b', 'pic8882 ', 22273.111, 'r2b',
                       8219, 709, 'r2', 7333, .172, 5.3787E13, 9.237423E52,
                       date '2003-08-02', interval '0291-10' year(4) to month,
                       interval '12:14:57.888888' hour to second),
                       ('I2c', 'pic8883 ', 38223242.333, 'r2c',
                        6839, 333, 'Rr', 7812, .436, 8.1937E16, 9.22323E2,
                       date '2003-08-03', interval '7291-09' year(4) to month,
                       interval '05:27:33.888888' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'3044')
    
    stmt = """INSERT INTO receiver3 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('eee', 'pic     ', 1234567.83, '333',
                       -7291, 382, 'c2', 10, .823, 1.27839E18, 3.7289112E23,
                       date '0000-01-01', interval '4444-01' year(4) to month,
                       interval '23:09:12.666666' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'3045')
    
    # Copy to expect file
    stmt = """select * from receiver1;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from receiver2;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from receiver3;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from receiver1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s4')
    
    stmt = """select * from receiver2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s5')
    
    stmt = """select * from receiver3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s6')
    
    stmt = """control query default TABLELOCK reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default SIMILARITY_CHECK reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default QUERY_CACHE reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """delete from receiver1;"""
    output = _dci.cmdexec(stmt)
    stmt = """delete from receiver2;"""
    output = _dci.cmdexec(stmt)
    stmt = """delete from receiver3;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO receiver1 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I1a', 'p88888', 1234567.83, '333',
                       -7291, 382, 'c2', 10, .823, 1.27839E18, 3.7289112E23,
                       date '2003-07-31', interval '4444-01' year(4) to month,
                       interval '23:09:12.666666' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = """INSERT INTO receiver2 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I2a', 'p88888', -1273, 'r2a',
                       -8219, 79, 'R2', 12, .72, 2.3787E13, 4.237423E52,
                       date '2003-08-01', interval '4291-09' year(4) to month,
                       interval '02:04:59.888888' hour to second),
                      ('I2b', 'p88882', 22273.111, 'r2b',
                       8219, 709, 'r2', 7333, .172, 5.3787E13, 9.237423E52,
                       date '2003-08-02', interval '0291-10' year(4) to month,
                       interval '12:14:57.888888' hour to second),
                       ('I2c', 'p88883', 38223242.333, 'r2c',
                        6839, 333, 'Rr', 7812, .436, 8.1937E16, 9.22323E2,
                       date '2003-08-03', interval '7291-09' year(4) to month,
                       interval '05:27:33.888888' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)
    
    stmt = """INSERT INTO receiver3 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I3a', 'p88888', 1234567.83, '333',
                       -7291, 382, 'c2', 10, .823, 1.27839E18, 3.7289112E23,
                       date '2003-07-31', interval '4444-01' year(4) to month,
                       interval '23:09:12.666666' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default UPD_ABORT_ON_ERROR 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default TABLELOCK 'OFF';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default QUERY_CACHE_STATEMENT_PINNING 'OFF';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default QUERY_CACHE '0';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO receiver2 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I2d', 'pic88882', 22273.111, 'r2b',
                       8219, 709, 'r2', 7333, 9.172, 5.3787E13, 9.3E52,
                       date '2003-08-02', interval '0291-10' year(4) to month,
                       interval '12:14:57.888888' hour to second),
                       ('I2d', 'picx8888r', 38223242.333, 'r2c',
                        6839, 333, 'Rr', 7812, .906, 8.1937E16, 3.22323E12,
                       date '2003-08-03', interval '7291-09' year(4) to month,
                       interval '05:27:33.888888' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'8402')

    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO receiver2 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ((select char_3 from receiver1),
                       'pic28882', 21273.111, 'I2b',
                       7259, 19, 'i2', 3333, .122, 7.1287E3, 8.23E5,
                       (select y_to_d from receiver1), 
                       (select iy_to_mo from receiver1),
                       interval '12:14:57.123987' hour to second),
                       ('I22', 'picr888r', 82242.333,
                        (select var_char_3 from receiver1),
                        16839, 23, 'ir', 33812, .96, 3.4732E6, 6.83E12,
                        (select y_to_d from receiver1), 
                        interval '7291-09' year(4) to month,
                        interval '06:27:33.888888' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    stmt = """INSERT INTO receiver1 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I1a', (select pic_x_8 from receiver2), 1234567.83, 
                       '333', -7291, 382, 'c2', 72, .823, 1.27839E18, 
                       3.7289112E23, date '2003-07-31',  
                       interval '4444-01' year(4) to month,
                       interval '13:09:12.666666' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'8401')

    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """DROP VIEW view_r1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'20123')
    
    stmt = """DROP TABLE receiver1 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'20123')
    
    stmt = """INSERT INTO receiver3 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I3b', 'pic28801', 1357.16, 'bbb',
                       12721, 618, 'c3', 35, .472, 6.39E7, 2.9112E2,
                       date '2003-07-31', interval '2831-01' year(4) to month,
                       interval '02:19:27.228836' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO receiver3 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I3c', 'picC8801', 7.16, 'ccc',
                       11, 392, 'c4', 5, .0, 0, 0,
                       date '2003-12-11', interval '1234-11' year(4) to month,
                       interval '12:19:27.228836' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  Violation of constraint r3c1 
    stmt = """INSERT INTO receiver3 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I3f', 'picC8821', 6.16, 'ccc',
                       11, 392, 'c4', 5, .0, null, 0,
                       date '2003-12-11', interval '0234-11' year(4) to month,
                       interval '22:19:27.228836' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'8101')
    
    stmt = """select * from receiver1;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from receiver2;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from receiver3;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from receiver1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s7a')
    
    stmt = """select * from receiver2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s7b')
    
    stmt = """select * from receiver3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s7c')

    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """control query default UPD_ABORT_ON_ERROR 'OFF';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """UPDATE receiver3 SET medium_int = 3993
        WHERE pic_x_8 = 'P88888';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """UPDATE receiver2 SET medium_int = 2992
        WHERE pic_x_8 = 'P88883';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """INSERT INTO receiver3 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('T', 'T8801', 7.16, 'ccc',
                       11, 392, 'c4', 5, .95, 0, 0,
                       date '2003-12-11', interval '1234-11' year(4) to month,
                       interval '12:19:27.228836' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """DELETE FROM receiver2
      WHERE char_3 = 123123123123123123123123123.9 and
            pic_x_8 = 'PICX88882';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4041')
    
    stmt = """UPDATE receiver2 SET medium_int = 1991
        WHERE pic_x_8 = 'P88882';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """UPDATE receiver2 SET medium_int = 1991
        WHERE pic_x_8 = 'P88883';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """DELETE FROM receiver1
      WHERE pic_x_8 = 'PICX88888' or
            pic_decimal_2 = 99.99;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    stmt = """DELETE FROM receiver2
      WHERE pic_decimal_2 = .72 and
            float_double_p = '1.2E12' and
            pic_x_8 = upshift ('picx88882');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4041')
    
    stmt = """UPDATE receiver1 SET float_double_p = 1.2E720 
        WHERE pic_x_8 = 'PICA8888';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'3166')
    
    stmt = """UPDATE receiver1 SET medium_int = 9999
        WHERE pic_x_8 = 'P88888';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """UPDATE receiver1 SET medium_int = 9999 + 123456789E5
        WHERE pic_x_8 = 'P88888';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'8411')

    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """UPDATE receiver1 SET medium_int = 1110
        WHERE pic_x_8 = 'P88888';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """UPDATE receiver2 SET medium_int = 9999
        WHERE pic_x_8 < 'PICX88888' and float_basic > 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    
    stmt = """INSERT INTO receiver3 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I3c', 'pic38888', 567.3, '333',
                       91, 382, 'c2', 710, .0, 1.37E18, 1.7289112E23,
                       date '2003-07-31', interval '4444-01' year(4) to month,
                       interval '12:19:27.228836' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """UPDATE receiver3 SET binary_64_s = 555555555555555.333,
                     small_int   = 12283,
                     var_char_2  = 'CC',
                     y_to_d      = date '2005-03-31',
                     float_basic = 3.369E12,
                     float_double_p = 3.369E12
               WHERE char_3 = 'I3c' and
                     pic_decimal_2 = .0 and
                     ih_to_s = interval '12:19:27.228836' hour to second;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """DELETE FROM receiver3
      WHERE char_3 = 'I3e' and pic_decimal_2 = 3.99 and
            ih_to_s = ' 12:19:27.228836';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4041')

    stmt = """COMMIT WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Copy to expect file
    stmt = """select * from receiver1;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from receiver2;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from receiver3;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from receiver1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s7')
    
    stmt = """select * from receiver2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s8')
    
    stmt = """select * from receiver3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s9')

    stmt = """control query default UPD_ABORT_ON_ERROR 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """control query default QUERY_CACHE '0';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """control query default QUERY_CACHE_STATEMENT_PINNING 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """DELETE FROM receiver2
      WHERE pic_decimal_2 <> (select pic_decimal_2 from receiver3
                               where char_3 > 'AXX');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'8401')

    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """DELETE FROM receiver3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    
    stmt = """DELETE FROM receiver1
      WHERE float_double_p is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)

    stmt = """UPDATE receiver3 set float_basic = null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 0)
    
    stmt = """INSERT INTO receiver3 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I3y', 'picC8801', 7.16, 'ccc',
                       11, 392, 'c4', 5, .101, 0, 0,
                       date '2003-12-11', interval '1234-11' year(4) to month,
                       interval '10:10:20.000000' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    #  Violation of R3C3
    stmt = """INSERT INTO receiver3 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I3a', 'pic38888', 1234567.83, '333',
                       -7291, 382, 'c2', 10, .823, 1.27839E18, 3.7289112E23,
                       date '2003-07-31', null, 
                       interval ' 3:09:12.666666' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'8101')
    
    stmt = """showddl receiver1;"""
    output = _dci.cmdexec(stmt)
    stmt = """delete from receiver1;"""
    output = _dci.cmdexec(stmt)
    stmt = """delete from receiver2;"""
    output = _dci.cmdexec(stmt)
    stmt = """delete from receiver3;"""
    output = _dci.cmdexec(stmt)

    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO receiver1 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I1a', 'pic88888', 1234567.83, '333',
                       -7291, 382, 'c2', 10, .823, 1.27839E18, 3.7289112E23,
                       date '2003-07-31', interval '4444-01' year(4) to month,
                       interval '23:09:12.666666' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,1)
    
    stmt = """INSERT INTO receiver2 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I2a', 'pic88888', -1273, 'r2a',
                       -8219, 79, 'R2', 12, .72, 2.3787E13, 4.237423E52,
                       date '2003-08-01', interval '4291-09' year(4) to month,
                       interval '02:04:59.888888' hour to second),
                      ('I2b', 'pic88882', 22273.111, 'r2b',
                       8219, 709, 'r2', 7333, .172, 5.3787E13, 9.237423E52,
                       date '2003-08-02', interval '0291-10' year(4) to month,
                       interval '12:14:57.888888' hour to second),
                       ('I2c', 'pic88883', 38223242.333, 'r2c',
                        6839, 333, 'Rr', 7812, .436, 8.1937E16, 9.22323E2,
                       date '2003-08-03', interval '7291-09' year(4) to month,
                       interval '05:27:33.888888' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,3)
    
    stmt = """INSERT INTO receiver3 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I3a', 'pic88888', 7.83, '333',
                       -7291, 382, 'c2', 10, .823, 1.27839E18, 3.7289112E23,
                       date '2003-07-31', interval '4444-01' year(4) to month,
                       interval '23:09:12.666666' hour to second),
                       ('I3b', 'pic33399', 73.2, 'bbb',
                        -821, 720, 'C2', 6223, .520, 0, 0,
                       date '2103-07-31', interval '8232-05' year(4) to month,
                       interval '99:39:19.999999' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    stmt = """UPDATE receiver2 SET char_3 = 'UpU',
                     var_char_3 = '3vv',
                     medium_int = 79,
                     float_double_p = NULL
               WHERE pic_x_8 is not null and
                     pic_decimal_2 = .520 and
                     float_double_p = 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4033')
    
    stmt = """INSERT INTO receiver2 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('3cc', 'picx88882', +2273, 23.285, +29, 79,
                       .109, 81.82322872342, 24.230847392),
                      ('3bb', 'picx8888r', 173, 123.3821, 83, 23774329,
                       .43, 3.2342, 34.872);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4023')
    
    stmt = """INSERT INTO receiver2 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('www', 'wr88882', +2273, '23', +29, .79,
                       '09', 8182, .223, 1.1E11, 2.2E2,
                        date '1002-01-01', null, 
                        interval '23:09:12.666666' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'8101')
    
    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO receiver1 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I1p', 'pic8888r', 167.81, '533',
                       1, 32, 'P2', 0, .3, 8.839E1, 8.72E3,
                       date '2003-08-01', interval '8444-01' year(4) to month,
                       interval '03:29:52.123456' hour to second),
                      ('I1P', 'pic888r2', 567.13, '633',
                       7, 82, '12', 47, .275, 7.9E8, 6.89E2,
                       date '2093-07-31', interval '9446-11' year(4) to month,
                       interval '63:27:00.000000' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)

    stmt = """INSERT INTO receiver3 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I3a', 'picx88888', 1234567.83, '333',
                       -7291, 382, 'c2', 10, .823, 1.27839E18, 3.7289112E23,
                       date '2003-07-31', interval '4444-01' year(4) to month,
                       interval '23:09:12.666666' hour to second),
                       ('I3b', 'picx33399', 38273,2, 'bbb',
                        -83721, 720, 'C2', 6223, .520, 0, 0,
                       date '2103-07-31', interval '8232-05' year(4) to month,
                       interval '99:39:19.999999' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4126')

    stmt = """INSERT INTO receiver2 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('www', 'wr88882', +2273, '23', 9999898889991, .79,
                       '09', 8182, .223, 1.1E11, 2.2E2,
                        date '1002-01-01', interval '0999-02' year(4) to month,
                        interval '23:09:12.666666' hour to second); """
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'8411')

    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO receiver2 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('E2e', 'year2003', 8932, 'RIA',
                       6714, 574, 'RI', 8012, .478, 5.7E8, 8.3E5,
                       date '9993-08-21', interval '0302-11' year(4) to month,
                       interval '99:14:00.123456' hour to second),
                       ('R2R', 'year9023', 3, 'RIB',
                        76, 330, 'RJ', 5851, .228, 4.7E08, 6.93E10,
                       date '1280-02-28', interval '9999-09' year(4) to month,
                       interval '00:04:00.123456' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    stmt = """DELETE FROM receiver2
      WHERE pic_d_8 is not null and
            pic_decimal_2 = .999 and
            float_double_p = 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4001')
    
    stmt = """UPDATE receiver3 SET y_to_d = date '9191-08-08',
                     iy_to_mo = iy_to_mo + interval - '9220' year(4)
               WHERE cast(ih_to_s as varchar(16)) = ' 99:39:19.999999';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 0)
    
    stmt = """UPDATE receiver3 SET y_to_d = date '9191-08',
                     iy_to_mo = iy_to_mo + interval - '922012' year(6),
                     ih_to_s = ih_to_s - interval '99.999999' second
               WHERE cast(ih_to_s as varchar(16)) =  '99:39:19.999999' or
                     (char_3 = 'I3a' and
                     pic_decimal_2 = .823);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'3045')
    
    stmt = """INSERT INTO receiver1 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_double_p,
                       ih_to_s)
               VALUES (NULL, 'Isagain', NULL, NULL,
                       NULL, NULL, null, null, .823, 9.11111E18,
                       interval '78:00:02.999999' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """DROP TABLE receiver1 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'20123')
    
    stmt = """INSERT INTO receiver1 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_double_p,
                       ih_to_s)
               VALUES (NULL, null, NULL, NULL,
                       NULL, NULL, null, null, .823, 9.11111E18,
                       interval '78:00:02.999999' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'4122')
    
    stmt = """INSERT INTO receiver1 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUE ('I1a', 'WrongRow', 1234567.83, '333',
                       -7291, 382, 'c2', 10, .823, 1.27839E18, 3.7289112E23,
                       date '2003-07-31', interval '4444-01' year(4) to month,
                       interval '23:09:12.666666' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'15001')
    
    stmt = """UPDATE receiver3 SET y_to_d = date '9191-08',
                     iy_to_mo = iy_to_mo + interval - '9220' year(4),
                     ih_to_s = ih_to_s - interval '99.999999' second,
                     pic_x_8 = NULL
               WHERE cast(ih_to_s as varchar(16)) =  '99:39:19.999999' and
                     char_3 = 'I1a' and
                     pic_decimal_2 = .823;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'3045')
    
    stmt = """delete from receiver1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """delete from receiver2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """delete from receiver3;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """showcontrol ALL;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """INSERT INTO receiver2 (select * from receiver1
                       union all
                       select * from receiver3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 0)
    
    
    stmt = """INSERT INTO receiver2 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I2a', 'pic88888', -1273, 'r2a',
                       -8219, 79, 'R2', 12, .72, 2.3787E13, 4.237423E52,
                       date '2003-08-01', interval '4291-09' year(4) to month,
                       interval '02:04:59.888888' hour to second),
                      ('I2b', 'pic88882', 22273.111, 'r2b',
                       8219, 709, 'r2', 7333, .172, 5.3787E13, 9.237423E52,
                       date '2003-08-02', interval '0291-10' year(4) to month,
                       interval '12:14:57.888888' hour to second),
                       ('I2c', 'pic88883', 38223242.333, 'r2c',
                        6839, 333, 'Rr', 7812, .436, 8.1937E16, 9.22323E2,
                       date '2003-08-03', interval '7291-09' year(4) to month,
                        interval '05:27:33.888888' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)

    stmt = """control query default ISOLATION_LEVEL 'READ UNCOMMITTED';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """control query default ISOLATION_LEVEL_FOR_UPDATES 'READ UNCOMMITTED';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """control query default QUERY_CACHE '0';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE TABLE receiver1 (
        char_3                 char(3),
        pic_x_8                char(8) upshift not null,
        binary_64_s            numeric(18, 3) signed,
        var_char_3             varchar(3) upshift,
        small_int              smallint signed,
        decimal_3_unsigned     decimal(3, 0) unsigned,
        var_char_2             varchar(2),
        medium_int             integer unsigned,
        pic_decimal_2          decimal(3,3) not null,
        float_basic            float (4),
        float_double_p         double precision not null,
        y_to_d                 date,
        iy_to_mo               interval year(4) to month,
        ih_to_s                interval hour to second not null,
        PRIMARY KEY (pic_x_8));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'3140')
    
    stmt = """control query default ISOLATION_LEVEL 'READ COMMITTED';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """control query default ISOLATION_LEVEL_FOR_UPDATES 'READ COMMITTED';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """ALTER TABLE receiver1 ADD CONSTRAINT temp_c
      CHECK (binary_64_s is not null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '20123')
    
    stmt = """INSERT INTO receiver1 (pic_x_8, pic_decimal_2, float_double_p, ih_to_s)
               VALUES (NULL, 0.982, 1.283E12, 
                       interval '99:00.982312' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3044')

    stmt = """INSERT INTO receiver1 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I1a', 'pic88888', 1234567.83, '333',
                       -7291, 382, 'c2', 10, .823, 1.27839E18, 3.7289112E23,
                       date '2003-07-31', interval '4444-01' year(4) to month,
                       interval '23:09:12.666666' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """SELECT * FROM mytab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    stmt = """INSERT INTO receiver3 (char_3, pic_x_8, binary_64_s, var_char_3,
                       small_int, decimal_3_unsigned, var_char_2,
                       medium_int, pic_decimal_2, float_basic, float_double_p,
                       y_to_d, iy_to_mo, ih_to_s)
               VALUES ('I3a', 'pic88888', 1234567.83, '333',
                       -7291, 382, 'c2', 10, .823, 1.27839E18, 3.7289112E23,
                       date '2003-07-31', interval '4444-01' year(4) to month,
                       interval '23:09:12.666666' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = """COMMIT WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Copy to expect file;
    stmt = """showcontrol default ISOLATION_LEVEL;"""
    output = _dci.cmdexec(stmt)
    stmt = """showcontrol default QUERY_CACHE;"""
    output = _dci.cmdexec(stmt)

    stmt = """select * from receiver1;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from receiver2;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from receiver3;"""
    output = _dci.cmdexec(stmt)

    stmt = """control query default ISOLATION_LEVEL 'READ UNCOMMITTED';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """control query default ISOLATION_LEVEL_FOR_UPDATES 'READ COMMITTED';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """control query default QUERY_CACHE reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select * from receiver1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s12')
    
    stmt = """select * from receiver2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s13')
    
    stmt = """select * from receiver3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s14')
    
    # When we went to NCI, there were a few formatting issues
    # Since this test isn't focused on ShowDDL, not going to worry about it
    # #expectfile ${test_dir}/a03exp a03s15
    stmt = """showddl receiver1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """ALTER TABLE receiver1 DROP CONSTRAINT temp_c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1005')

    stmt = """delete from receiver1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output,1)
    
    stmt = """delete from receiver2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output,3)
    
    stmt = """delete from receiver3; """
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output,1)
    
    stmt = """drop index receiver1a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop index receiver1b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop index receiver1c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop index receiver1d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop index receiver1e;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """alter table receiver1 drop constraint r1c1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop index receiver2a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop index receiver2b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop index receiver2c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop index receiver2d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop index receiver2e;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """alter table receiver2 drop constraint r2c1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """alter table receiver2 drop constraint r2c2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop index receiver3a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop index receiver3b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop index receiver3c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop index receiver3d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop index receiver3e;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """alter table receiver3 drop constraint r3c1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """alter table receiver3 drop constraint r3c2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """alter table receiver3 drop constraint r3c3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

