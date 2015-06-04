.. # @@@ START COPYRIGHT @@@
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

=======================================================================
Trafodion QA Python Test Framework with Testr and Tox and Sphinx README
=======================================================================

* Tox is used so the Python tests can run in a virtual Python environment. This allows one to use any 
  Python package for testing.  Even packages that are not part of the system Python distribution.

* Testr is a test runner which allows for better test tracking and parallel testing.

* Sphinx makes it easy to create documentation from source code. It is by far one of the most popular 
  Python documentation tool.


Running Tests
*************

* First, add the bin directory of Python 2.7 built with UCS2 support to your PATH ::

    export PATH=/<PATH_to_Python2.7_Home>/bin:$PATH

* Next, set the proxy environment variables if needed for your environment ::

    export http_proxy="http://SOME_PROXY:SOME_PORT"
    export https_proxy="$http_proxy"
    export ftp_proxy="$http_proxy"

* Next, run ``config.sh`` to configure the Framework.
  If you need help on using this command then type ``./config.sh -h``.

  **Example 1 - Configuring for Trafodion and ODBC, JDBC, & DCI**:

  Assuming that the unixODBC driver manager is installed in the default location (``/usr``) and 
  the ODBC driver is not yet configured in the ``odbc_driver`` sub-directory, the following command 
  will configure ODBC, JDBC, and DCI for Trafodion.  It will also install the ODBC driver into the 
  ``odbc_driver`` sub-directory:  ::

    ./config.sh -d <Fully_Qualified_Domain_Name_Of_Machine_OR_IP>:<Port> \
    -t /<Absolute_PATH_to>/<ODBC_driver_Filename>.tar.gz \
    -J /<Absolute_PATH_to>/<JDBC_T4_Driver_Library>.jar \
    -N /<Absolute_PATH_to>/<DCI_Library>.jar

  **Example 2 - Configuring for Trafodion with ODBC, JDBC, and DCI disabled**:

  To configure the framework for Trafodion with ODBC, JDBC, and DCI disabled do the following:

  * ``rm -rf tests/ODBC``
  * Edit ``tests/SAMPLE/test_sample.py`` and remove the section ``class SQL``
  * Then run ``config.sh`` with the followig options: ::

      ./config.sh -O -d <Fully_Qualified_Domain_Name_Of_Machine_OR_IP>:<Port>

  .. warning:: Do NOT put the <ODBC_driver_Filename>.tar.gz in the ``odbc_driver`` subdirectory. The contents of this sub-directory is
               removed every time config.sh is run with the -t option!
  
* Next run the `tox <http://tox.readthedocs.org/en/latest/>`_ command to create a Python virtual environment for
  your test and automatically kick off the tests using `testr <https://testrepository.readthedocs.org/en/latest/MANUAL.html>`_ ::

    tox -e py27 -- SAMPLE.test_sample.TestOS.test_SystemCall

  .. warning:: Make sure you do NOT source in Trafodion's sqf/sqenv.sh file. Otherwise you will encounter the following error : 

               [unixODBC][Driver Manager]Can't open lib '/<ABSOLUTE_PATH>/<TO>/<ODBC_DRIVER>_drvr64.so' : file not found




Debugging Tests outside of testr and tox (Basic)
************************************************

.. note:: Use this method to debug if you are putting print statements in your Python test files for debugging

.. warning:: Make sure you do NOT source in Trafodion's sqf/sqenv.sh file. Otherwise you will encounter the following error :

             [unixODBC][Driver Manager]Can't open lib '/<ABSOLUTE_PATH>/<TO>/<ODBC_DRIVER>_drvr64.so' : file not found

Assuming that ``config.sh`` has been run and the Python virtual environment has been set up, do the following to debug the tests

1. Activate the Python virtual environment ::

    source .tox/py27/bin/activate

2. Source in the environment variables needed ::

    source env.sh

3. Change to the ``tests`` subdirectory and run the command ::

    python <test_file_1>.py

4. Repeat Step 4 until there are no more failures.

5. When debugging is finished deactivate the Python virtual environment ::

    deactivate


Debugging Tests with testr (Basic)
**********************************

.. warning:: Make sure you do NOT source in Trafodion's sqf/sqenv.sh file. Otherwise you will encounter the following error :

             [unixODBC][Driver Manager]Can't open lib '/<ABSOLUTE_PATH>/<TO>/<ODBC_DRIVER>_drvr64.so' : file not found

Assuming that ``config.sh`` has been run and the Python virtual environment has been set up, do the following to debug the tests

1. Activate the Python virtual environment ::

    source .tox/py27/bin/activate
    
2. Source in the environment variables needed ::

    source env.sh
    
3. See what tests were failing ::

    testr failing

4. Make some fixes and rerun the failing tests ::
    
    testr run --failing 

   OR if you want to run some specific tests use the command ``tox -e py27 -- <Test_Name_as_Listed_by_testr_seperated_by_space>``

   For example, : ::

    tox -e py27 -- ODBC.test_odbc_2.SQLTest.test_FetchByColumnName ODBC.test_odbc_2.SQLTest.test_PyodbcError
    
5. Repeat Steps 3-4 until there are no more failures.

6. When debugging is finished deactivate the Python virtual environment ::

    deactivate


Debugging Tests with testr (Advanced)
*************************************

.. warning:: Make sure you do NOT source in Trafodion's sqf/sqenv.sh file. Otherwise you will encounter the following error :

             [unixODBC][Driver Manager]Can't open lib '/<ABSOLUTE_PATH>/<TO>/<ODBC_DRIVER>_drvr64.so' : file not found

Assuming that ``config.sh`` has been run and the Python virtual environment has been set up, do the following to debug the tests

* Activate the Python virtual environment ::

    source .tox/py27/bin/activate

* Source in the environment variables needed ::

    source env.sh
    
* Look for last testr run number in the directory .testrepository.  Look for a file with the highest number in this directory.
  If the test has only been run once then the run number should be 0. ::

    ls -l .testrepository

* Look at the file .testrepository/$LAST_TEST_RUN_NUMBER and find the test that failed.  Then under the tags section 
  you should see something like ::
  
    tags: worker-0
    
  With this worker name we can extract the list of tests that ran in that test run on that worker. ::
  
    testr last --subunit | subunit-filter -s --xfail --with-tag=worker-0 | subunit-ls > slave-0.list
    
  Using this test list we can run that set of tests in the same order that caused the failure with : ::
  
    testr run --load-list=slave-0.list
    
* When debugging is finished deactivate the Python virtual environment ::

    deactivate
    
    
Other Useful testr Commands
***************************

* List all the tests that ran ::

    testr list-tests
    
* Run only one test : ``testr run <Test_Name_as_Listed_by_testr>``.  For example, ::

    testr run ODBC.test_odbc_2.SQLTest.test_FetchByColumnName

* Get all test results of the last test run in csv format ::

    testr last --subunit | subunit-1to2 | subunit2csv
    
* Get all test results of the last test run in pyunit format ::

    testr last --subunit | subunit-1to2 | subunit2pyunit
    
* Get all test results of the last test run in JUnit format ::

    testr last --subunit | subunit-1to2 | subunit2junitxml
    

Adding New Tests
****************

Directory Structure
-------------------

* Add any new required Python packages to the file ``test-requirements.txt``
* Make sure the file's name follows the naming format : ``test_*.py``
* If ``test_*.py`` files are created in a subdirectory under the ``tests`` directory,
  a ``__init__.py`` file must also be created in the subdirectory.  Otherwise the tests in
  that subdirectory will not be discovered and run by testr.

test_*.py Structure
-------------------

* Make sure ALL class test cases extend ``unittest.TestCase``.  For example, ::
    
    class SystemCallTests(unittest.TestCase)

* Make sure ALL unit test names start with ``test_``.  For example, ::

    def test_SystemCall(self):

General Test Documenting Advice
--------------------------------

* Write code according to `PEP 8 (the "Python Style Guide") <http://www.python.org/dev/peps/pep-0008>`_.
    * The code can be checked with one of the following ways

      **Check the whole tests directory for PEP8 compliance**: ::
      
          tox -e pep8

      **Checking a directory for PEP8 compliance**: ::

          tox -e pep8 -- tests/<SOME_DIRECTORY>

      **Checking a file for PEP8 compliance**: ::

          tox -e pep8 -- tests/<SOME_DIRECTORY>/<SOME_FILE>.py

* Use ``docstrings`` to describe modules, classes, and functions
* Do NOT use triple-quote strings to comment out code.  Use hashes instead.
* Docstrings and Block comments are NOT interchangeable.  The docstring is supposed to describe the operation of the function
  or class.  The leading comment block of a function or class is a programmer's note. ::
    
    # This is a block comment. Your notes go here
    def myFunction(x):
        """This is a docstring. Describe your function here."""
* Make sure copyright header is in every Python source file

Building Test Documents
-----------------------

Run the following tox command to automatically re-build the test documentation ::

    tox -e docs


Known Issues
************

* If the Trafodion sqf/sqenv.sh file has been sourced into your environment the ODBC tests will run into the error: ::

    [unixODBC][Driver Manager]Can't open lib '/<ABSOLUTE_PATH>/<TO>/<ODBC_DRIVER>_drvr64.so' : file not found


About this README
*****************

This README is written using `reStructuredText <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_ format.  Using this 
format, the `Sphinx <http://sphinx-doc.org/index.html>`_ tool can be used to create documentation in HTML, PDF, and other formats.


Other Resources
***************

**Python**

* `Python <https://www.python.org/>`_
* `Learning Python <http://www.learnpython.org/>`_
* `Codecademy Python Track <http://www.codecademy.com/tracks/python>`_
* `Learn Python the Hard Way <http://learnpythonthehardway.org/book/>`_

**Python ODBC Modules**

* `pyodbc <https://code.google.com/p/pyodbc/>`_
* `pypyodbc <https://code.google.com/p/pypyodbc/>`_

**Python Unittest**

* `Pytest <http://pytest.org/latest/>`_
* `Python unittest fixture syntax and flow reference <http://pythontesting.net/framework/unittest/unittest-fixtures/>`_
* `Python Style guide checker - PEP 8 <http://www.python.org/dev/peps/pep-0008>`_

**Testr**

* `Testr Manual <https://testrepository.readthedocs.org/en/latest/MANUAL.html>`_
* `Testr - OpenStack <https://wiki.openstack.org/wiki/Testr>`_
* `Python Tox <http://tox.readthedocs.org/en/latest/>`_

**reStructuredText and Sphinx**

* `Sphinx <http://sphinx-doc.org/index.html>`_
* `Sphinx reStructuredText Primer <http://sphinx-doc.org/rest.html>`_
* `Sphinx Markup Constructs <http://sphinx-doc.org/markup/index.html>`_
* `Sphinx Tutorial <http://matplotlib.org/sampledoc/>`_
* `reStructuredText Tool Support <http://stackoverflow.com/questions/2746692/restructuredtext-tool-support>`_
* `Online reStructuredText Editor <http://rst.ninjs.org/>`_
* `reStructuredText in vim <https://github.com/Rykka/riv.vim>`_
* `Online Sphinx editor <https://livesphinx.herokuapp.com/>`_

