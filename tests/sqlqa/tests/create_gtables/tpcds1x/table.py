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

import sys
from ...lib import hpdci
import defs

_testmgr = None
_dci = None

def create_and_load(hptestmgr, prop_file, name, files, count, delim):
    global _testmgr
    global _dci
    
    _testmgr = hptestmgr

    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()

    # __name__ is the module name of this file.  It should be in *.*.*... 
    # format.  Since we know the ddl module file will be in the same
    # directory as this file, we can just replace the last part to get
    # the module name of the ddl file.
    idx = __name__.rfind('.')
    ddl_module_name = __name__[:idx] + '.' + name + '_ddl'
    ddl_module = sys.modules[ddl_module_name]
    getattr(ddl_module, '_init')(_testmgr)

    # load the data
    table = defs.my_schema + '.' + name
    for f in files:
        data_file = defs.data_dir + '/' + f
        output = _testmgr.data_loader(defs.work_dir, prop_file, table, data_file, delim)
        _dci.expect_loaded_msg(output)

    # update stats
    stmt = 'update statistics for table ' + table + ' on every column sample;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # set privilege
    stmt = 'revoke all on table ' + table + ' from PUBLIC;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = 'grant select on table ' + table + ' to PUBLIC;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # verify count
    stmt = 'select count(*) from ' + table + ';'
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, count)
