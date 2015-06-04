This test suite can be used to populate QA global tables before running any
other test suites that require these tables.  Since the user has no control
over the execution order of the test suites, this test suite is disabled by 
default.  It requires special handling if you want to use it:

(1) From sqltests/tests, remove all other files and directories except for 
    the followings:
        create_gtables
        lib
        __init__.py
(2) From sqltests/tests/create_gtables, rename the disabled .py file:
        mv test_create_gtables.py.disabled test_create_gtables.py
(3) From sqltests/tests/create_gtables/g_data, softlink the following 
    directories to the locations of your data files:
        ln -s cmureg  <location of cmureg data files>
        ln -s hpit    <location of hpit data files>
        ln -s sqldopt <location of sqldopt data files>
        ln -s sqldpop <location of sqldpop data files>
        ln -s tpcds1x <location of tpcds1x data files>
        ln -s tpch2x  <location of tpch2x data files> 
        ln -s wisc32  <location of wisc32 data files>
(4) From sqltests, run the test suite the same way you would normally run the 
    tests.

