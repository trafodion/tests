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
from ...lib import gvars
import defs

_testmgr = None
_testlist = []
_dci = None

# Statement to select names of extra-hub tables.
# Possible values of case expression must have same length (or be cast to varchar) or it won't work.
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
   
    if hpdci.tgtSQ(): 
         stmt = """prepare extrahub from
select cast(substring(left(description, position((case operator when 'FILE_SCAN_UNIQUE' then 'lock_state:' else 'scan_direct' end) in description)-2)
from position('scan_type:' in description) + 11) as varchar(100))
as "Extra Hub Tables"
from table(explain(NULL,'S'))
where operator like '%_SCAN%'
and position('project_only_cols: yes' in description) > 0;"""
         output = _dci.cmdexec(stmt)
    elif hpdci.tgtTR():
         stmt = """prepare extrahub from
select operator, description
from table(explain(NULL,'S'));"""
         output = _dci.cmdexec(stmt)
 
    # Select names of hub tables.
    # Possible values of case expression must have same length (or be cast to varchar) or it won't work.
    #prepare hub from
    #select cast(substring(left(description, position((case operator when 'FILE_SCAN_UNIQUE' then 'lock_state:' else 'scan_direct' end) in description)-2)
    #                           from position('scan_type:' in description) + 11) as varchar(100))
    #       as "Hub Tables"
    #from table(explain(NULL,'S'))
    #where operator like '%_SCAN%'
    #  and position('project_only_cols: yes' in description) = 0;

    if hpdci.tgtSQ():    
        stmt = """prepare hub from
select cast(substring(left(description, position((
case operator
when 'FILE_SCAN_UNIQUE' then 'lock_state:'
when 'INDEX_SCAN_UNIQUE' then 'lock_state:'
else 'scan_direct'
end
) in description)-2)
from position('scan_type:' in description) + 11) as varchar(100))
as "Hub Tables"
from table(explain(NULL,'S'))
where operator like '%_SCAN%'
and position('project_only_cols: yes' in description) = 0;"""
        output = _dci.cmdexec(stmt)
    elif hpdci.tgtTR():
        stmt = """prepare hub from
select operator, description 
from table(explain(NULL,'S'));"""
        output = _dci.cmdexec(stmt)
 
