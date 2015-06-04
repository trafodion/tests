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

import os
import ConfigParser

from ...lib import hpdci
from ...lib import gvars
test_dir = hpdci.my_test_dir(__name__)
work_dir = hpdci.my_work_dir(__name__)

# Set your own catalog and schema.  Change the variable names if necessary.
w_catalog = gvars.test_catalog
w_schema = hpdci.my_schema(__name__)
my_schema = w_catalog + '.' + w_schema

_target = ''
_user = ''
_pw = ''
_jdbc_classpath = ''
_hpdci_classpath = ''

def set_args():
    global _target
    global _user
    global _pw
    global _jdbc_classpath
    global _hpdci_classpath

    scriptPath = os.path.dirname(os.path.realpath(__file__))
    config = ConfigParser.ConfigParser()
    config.read(os.path.abspath(scriptPath + '../../../../config.ini'))
    try:
        _target = config.get("pytest","tcp").replace('TCP:', '', 1)
        _user = config.get("pytest","usr")
        _pw = config.get("pytest","pwd")
        _jdbc_classpath = config.get("pytest","t4jdbc_classpath")
        _hpdci_classpath = config.get("pytest","hpdci_classpath")
    except Exception:
        pass
