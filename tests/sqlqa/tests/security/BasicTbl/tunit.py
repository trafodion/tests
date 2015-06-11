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
import setup
import cleanup
# Import you own test modules, one line for each.
from ..src_basic import basic_defs
from ..src_basic import basic_setup
from ..src_basic import basic_cleanup_general
from ..src_basic import basic_cleanup_final
from ..src_basic import tYTblDel_a
from ..src_basic import tYTblIns_a
from ..src_basic import tYTblSel_a
from ..src_basic import tYTblUpd_a
from ..src_basic import tYTblAll_a
#from ..src_basic import tYTblDel_b
#from ..src_basic import tYTblIns_b
#from ..src_basic import tYTblSel_b
#from ..src_basic import tYTblUpd_b
#from ..src_basic import tYTblAll_b

def sq_testunit(hptestmgr, testlist=[]):

    basic_defs.work_dir = defs.work_dir
    # This will be created as part of the test.  We can choose any name we like.
    # Since the schema name is unique to each test, we will just us it as part
    # of the name.
    basic_defs.TestVars.myrole1="""qi_""" + defs.w_schema + """_role1"""
    basic_defs.TestVars.myrole2="""qi_""" + defs.w_schema + """_role2"""

    cleanup._init(hptestmgr, testlist)
    setup._init(hptestmgr, testlist)

    basic_defs._init(defs.my_schema, defs.w_schema, hptestmgr)
    basic_cleanup_general._init(hptestmgr)
    basic_setup._init(hptestmgr)

    # The following set of tests should have AQR on.
    basic_defs.turn_on_aqr_all_users()

    #-- Framework A & B

    #-- The following set of tests works on objects

    basic_defs.user1_grant_all_privs_to_all = basic_defs.user1_grant_all_obj_privs_to_all_a
    basic_defs.user1_revoke_all_privs_from_all = basic_defs.user1_revoke_all_obj_privs_from_all_a
    basic_defs.def_tbl_del_query()
    hpdci.auto_execute_module_tests(tYTblDel_a, hptestmgr, testlist)
    basic_defs.def_tbl_ins_query()
    hpdci.auto_execute_module_tests(tYTblIns_a, hptestmgr, testlist)
    basic_defs.def_tbl_sel_query()
    hpdci.auto_execute_module_tests(tYTblSel_a, hptestmgr, testlist)
    basic_defs.def_tbl_upd_query()
    hpdci.auto_execute_module_tests(tYTblUpd_a, hptestmgr, testlist)
    basic_defs.def_tbl_all_query()
    hpdci.auto_execute_module_tests(tYTblAll_a, hptestmgr, testlist)

    #basic_defs.user1_grant_all_privs_to_all = basic_defs.user1_grant_all_obj_privs_to_all_b
    #basic_defs.user1_revoke_all_privs_from_all = basic_defs.user1_revoke_all_obj_privs_from_all_b
    #basic_defs.def_tbl_del_query()
    #hpdci.auto_execute_module_tests(tYTblDel_b, hptestmgr, testlist)
    #basic_defs.def_tbl_ins_query()
    #hpdci.auto_execute_module_tests(tYTblIns_b, hptestmgr, testlist)
    #basic_defs.def_tbl_sel_query()
    #hpdci.auto_execute_module_tests(tYTblSel_b, hptestmgr, testlist)
    #basic_defs.def_tbl_upd_query()
    #hpdci.auto_execute_module_tests(tYTblUpd_b, hptestmgr, testlist)
    #basic_defs.def_tbl_all_query()
    #hpdci.auto_execute_module_tests(tYTblAll_b, hptestmgr, testlist)

    basic_cleanup_general._init(hptestmgr)
    basic_cleanup_final._init(hptestmgr)
    cleanup._init(hptestmgr, testlist)

