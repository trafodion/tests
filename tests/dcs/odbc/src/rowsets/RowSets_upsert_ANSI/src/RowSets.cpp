/**
  @@@ START COPYRIGHT @@@

  (C) Copyright 2015 Hewlett-Packard Development Company, L.P.

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

  @@@ END COPYRIGHT @@@
*/

// RowSets.cpp : Defines the entry point for the console application.
// This application shows the many ways to inset data via use of rowsets.
// It also demonstrates different error conditions and error handling.
// 
#include "stdafx.h"
#include "RowSets.h"

int modes[]            = { STANDARD, STOP };
int features[]         = { STANDARD, STOP, ASYNC, HASH2 };
int operations[]       = { PREPARE_EXECUTE, EXECUTE_DIRECT, STOP };
int bindOrientations[] = { ROW, COLUMN, SINGLE, STOP };
int actions[]          = { INSERT, SELECT, UPDATE, DELETE_PARAM, STOP, INSERT_SELECT, INSERT_BULK }; // DELETE_PARAM needs to be the last action before STOP.
int tableTypes[]       = {
		REGULAR,
//		SURROGATE,
//		POSOFF,
//		SET,
//		MULTISET,
//		VOLATILE,
		STOP
};
int tableFeatures[]    = {
		STANDARD,
		//INDEX,
		//MVS,
		//BEFORETRIGGER,
		//AFTERTRIGGER,
		STOP,
		RI
};
int injectionTypes[]   = {	
		NO_ERRORS,
		DUPLICATEKEY,
		UNIQUECONST,
		DUPLICATEROW,
		OVERFLOW,
		NULLVALUE,
		ERR_PER_ROW,
		FULL_ERRORS,
		DRIVER_GOOD_BAD_MULCOL,								//All error, no warning, some good rows, multiple columns
		DRIVER_GOOD_WARNING_MULCOL,							//All warning, multiple columns
		DRIVER_GOOD_BAD_WARNING_MULCOL,						//Error and warning, multiple columns
		DRIVER_ALL_BAD_MULCOL,								//All error, multiple columns
		DRIVER_ALL_WARNING_MULCOL,							//All warning, multiple columns
		DRIVER_ALL_BAD_WARNING_MULCOL,						//Error and warning, multiple columns
		SERVER_GOOD_BAD_MULCOL,								//Some good rows, some bad rows, multiple columns server error only and/or driver warning
		SERVER_ALL_BAD_MULCOL,								//All bad rows, multiple columns server error only and/or driver warning
		MIXED_DRIVERWARNING_SERVERBAD_GOOD_MULCOL,			//Some driver warning, Some server error, some good, multiple columns
		MIXED_DRIVERBAD_SERVERBAD_GOOD_MULCOL,				//Some good rows, some driver errors, some server errors, multiple columns
		MIXED_DRIVERWARNING_DRIVERBAD_SERVERBAD_GOOD_MULCOL,//Some good rows, some driver errors, some driver warnings, some server errors, multiple columns
		MIXED_DRIVERBAD_SERVERBAD_MULCOL,					//Driver errrors, server errors, no warning, no good row, multiple columns
		MIXED_DRIVERWARNING_DRIVERBAD_SERVERBAD_MULCOL,		//Driver errrors, driver warnings, server errors, no good row, multiple columns
		STOP,
		SELECTIVE,
		CANCEL
};

// number of rows to insert
int numberOfRows[] = { 10, STOP };
// rowset size
int rowsetSizes[] = { 10, STOP, 3600, STOP, 1750, 65 };
// commit rate
int commitRates[] = { 1000, STOP };

// Standard
char ExecSQLStr[ 16 ][ 2048 ];
// MVS
char ExecSQLStrMVS[ 7 ][ 2048 ];
// Index
char ExecSQLStrIndex[ 2 ][ 2048 ];
// RI
char ExecSQLStrRI[ 4 ][ 2048 ];
// Volatile
char ExecSQLStrVolatile[ 2 ][ 2048 ];
// Before Trigger
char ExecSQLStrBeforeTrigger[2][2048];
// After Trigger
char ExecSQLStrAfterTrigger[5][2048];

SQLCHAR ignoreState[ NUMBER_OF_IGNORES ][ 10 ];
SDWORD ignoreNativeError[ NUMBER_OF_IGNORES ];
int ignoreCount;

// Testing information
int  testTotal; // The number of tests to run.
int  testCount; // The number of tests run.
int  testFail;  // The number of tests that failed.
int  testPass;  // The number of tests that passed.
int  ignoredTests[ 100 ] = { STOP }; // The tests to ignore. STOP must be at the end of the array.
bool singleTest = false;    // Used with -t argument.
int  testToRun;             // Used with -t and -r argument.
bool resumeTesting = false; // Used with -r argument.
char *secondaryRole = "--";

// This concludes the test pre-defined variables. Everything below this is in regards to running the tests.
int main( int argc, char* argv[] )
{
    int   c, errflag = 0;        // Used for getOpt() only.

	// start ALM log changes
	// ALM test report will ignore counting some of tests
	int ALM_testCounter = 0;
	int ALM_testStart = 0;  // the starting test cases which grouped together.
	bool bTestCounted = false;
	// end ALM log changs

    testCount = 0;       // The number of tests run.
    testFail = 0;        // The number of tests that failed.
    testPass = 0;        // The number of tests that passed.
    ignoreCount = 0;     // The number of stored ignores. Used for error
                         // message processing. See void IgnoreMsg(), 
                         // ShouldIgnoreMsg(), and ClearIgnore().
    errorChecking = STANDARD; // Standard error checking. This is really set 
                              // in EstablishHandlesAndConnection( ).

    optarg = NULL;
    if ( argc < 7 )
        errflag++;

    while ( !errflag && ( c = getopt( argc, argv, ARGS ) ) != -1 )
    {
        switch ( c ) 
        {
            case 'd':
                datasource = optarg;
                break;
            case 'u':
                uid = optarg;
                break;
            case 'p':
                password = optarg;
                break;
            case 'o':
#ifdef _UNIX
				if (strcasecmp(optarg,"debug") == 0) debug = true;
#else
				if (_stricmp(optarg,"debug") == 0) debug = true;
#endif
				else errflag++;
                break;
            case 't':
                testToRun = atoi( optarg );
                singleTest = true;
                break;
            case 'r':
                if( singleTest == false )
                {
                    testToRun = atoi( optarg );
                    resumeTesting = true;
                }
                break;
			case 'm':
				machine = optarg;
				break;
			case 's':
				secondaryRole = optarg;
				break;
            default :
                errflag++;
        }
    }

	time_t my_clock;
	my_clock = time( NULL);
    strftime( logfilename, 256, "rowsets_%Y-%m-%d_%H.%M.%S", localtime( &my_clock ) );
	strcat( logfilename, ".");
	strcat( logfilename, datasource);
	strcat( logfilename, ".");
	strcat( logfilename, machine);
	strcat( logfilename, ".log");

	// start for ALM log
    strftime( ALM_log_file_buff, 256, "rowsets_%Y-%m-%d_%H.%M.%S", localtime( &my_clock ) );
	strcat( ALM_log_file_buff, ".");
	strcat( ALM_log_file_buff, datasource);
	strcat( ALM_log_file_buff, ".");
	strcat( ALM_log_file_buff, machine);
	strcat( ALM_log_file_buff, "_ALM.log");
	// end for ALM log 

	if ( errflag ) 
    {
        RecordToLog( "Command line error.\n" );
        RecordToLog( "Usage: %s -d <datasource> -u <userid> -p <password> -m <OS type> [-o <debug> | -t <testid> | -r <test_id>]\n", argv[0] );
        RecordToLog( "-d: data source\n" );
        RecordToLog( "-u: user identification\n" );
        RecordToLog( "-p: user password\n" );
        RecordToLog( "-m: OS tyep (ANSI+ASCII+win32/ANSI+ASCII+win64/UNICODE+GBK+win32)\n" );
		RecordToLog( "-o: turn debug mode 'ON' (optional)\n" );
        RecordToLog( "-t: test id to run (optional)\n" );
        RecordToLog( "-r: resume test id to start from (optional)\n" );
	// start for ALM log
		RecordTo_ALM_Log("Unable to initial the log file.  No tests can be executed.\n");
	// end for ALM log
        return 0;
    }

    // Now that we got through the command line arguments, lets set things up before we start testing.

    // REGULAR
    strcpy( ExecSQLStr[ 0 ],  "DROP TABLE ROWSET_TABLE CASCADE" );
    strcpy( ExecSQLStr[ 1 ],  "CREATE TABLE ROWSET_TABLE ( C01 CHAR( 20 ) CHARACTER SET ISO88591 NOT NULL, C02 CHAR( 20 ) CHARACTER SET UCS2, C03 VARCHAR( 20 ) CHARACTER SET ISO88591, C04 VARCHAR( 20 ) CHARACTER SET UCS2, C05 LONG VARCHAR( 20 ) CHARACTER SET ISO88591, C06 LONG VARCHAR( 20 ) CHARACTER SET UCS2, C07 NCHAR( 20 ), C08 NCHAR VARYING( 20 ), C09 DECIMAL (8, 0) SIGNED, C10 DECIMAL (8, 0) UNSIGNED, C11 NUMERIC (8, 0) SIGNED, C12 NUMERIC (8, 0) UNSIGNED, C13 TINYINT SIGNED, C14 TINYINT UNSIGNED, C15 SMALLINT SIGNED, C16 SMALLINT UNSIGNED, C17 INTEGER SIGNED NOT NULL, C18 INTEGER UNSIGNED, C19 LARGEINT NOT NULL NOT DROPPABLE, C20 REAL, C21 FLOAT(54), C22 DOUBLE PRECISION, C23 DATE, C24 TIME, C25 TIMESTAMP, C26 INTERVAL YEAR, C27 INTERVAL MONTH, C28 INTERVAL DAY, C29 INTERVAL HOUR, C30 INTERVAL MINUTE, C31 INTERVAL SECOND, C32 INTERVAL YEAR TO MONTH, C33 INTERVAL DAY TO HOUR, C34 INTERVAL DAY TO MINUTE, C35 INTERVAL DAY TO SECOND, C36 INTERVAL HOUR TO MINUTE, C37 INTERVAL HOUR TO SECOND, C38 INTERVAL MINUTE TO SECOND, C39 NUMERIC (19, 0) SIGNED, C40 NUMERIC (19, 0) UNSIGNED, PRIMARY KEY ( C19 ), CONSTRAINT C17C CHECK ( C17 < 50000 ) )" );
    strcpy( ExecSQLStr[ 2 ],  "UPSERT INTO ROWSET_TABLE ( C01, C02, C03, C04, C05, C06, C07, C08, C09, C10, C11, C12, C13, C14, C15, C16, C17, C18, C19, C20, C21, C22, C23, C24, C25, C26, C27, C28, C29, C30, C31, C32, C33, C34, C35, C36, C37, C38, C39, C40 ) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )" );
    strcpy( ExecSQLStr[ 3 ],  "SELECT * FROM ROWSET_TABLE ORDER BY C19" );
    strcpy( ExecSQLStr[ 4 ],  "DELETE FROM ROWSET_TABLE" );
    strcpy( ExecSQLStr[ 5 ],  "DELETE FROM ROWSET_TABLE WHERE CURRENT OF TABLECURSOR" );
    strcpy( ExecSQLStr[ 6 ],  "DELETE FROM ROWSET_TABLE WHERE C01 = ? AND C02 = ?" );
    strcpy( ExecSQLStr[ 7 ],  "UPDATE ROWSET_TABLE SET C01=?, C02=?, C03=?, C04 = ?, C05=?, C06=?, C07=?, C08 = ?, C09=?, C10=?, C11=?, C12 = ?, C13=?, C14=?, C15=?, C16 = ?, C17 = ?, C18=?, C20=?, C21 = ?, C22=?, C23=?, C24=?, C25 = ?, C26=?, C27=?, C28=?, C29 = ?, C30=?, C31=?, C32=?, C33 = ?, C34 = ?, C35 = ?, C36 = ?, C37 = ?, C38 = ?, C39 = ?, C40 = ? WHERE C19 = ?" );
    // No parition table.
    strcpy( ExecSQLStr[ 8 ],  "CREATE TABLE ROWSET_TABLE ( C01 CHAR( 20 ) CHARACTER SET ISO88591 NOT NULL, C02 CHAR( 20 ) CHARACTER SET UCS2, C03 VARCHAR( 20 ) CHARACTER SET ISO88591, C04 VARCHAR( 20 ) CHARACTER SET UCS2, C05 LONG VARCHAR( 20 ) CHARACTER SET ISO88591, C06 LONG VARCHAR( 20 ) CHARACTER SET UCS2, C07 NCHAR( 20 ), C08 NCHAR VARYING( 20 ), C09 DECIMAL (8, 0) SIGNED, C10 DECIMAL (8, 0) UNSIGNED, C11 NUMERIC (8, 0) SIGNED, C12 NUMERIC (8, 0) UNSIGNED, C13 TINYINT SIGNED, C14 TINYINT UNSIGNED, C15 SMALLINT SIGNED, C16 SMALLINT UNSIGNED, C17 INTEGER SIGNED NOT NULL, C18 INTEGER UNSIGNED, C19 LARGEINT NOT NULL NOT DROPPABLE, C20 REAL, C21 FLOAT(54), C22 DOUBLE PRECISION, C23 DATE, C24 TIME, C25 TIMESTAMP, C26 INTERVAL YEAR, C27 INTERVAL MONTH, C28 INTERVAL DAY, C29 INTERVAL HOUR, C30 INTERVAL MINUTE, C31 INTERVAL SECOND, C32 INTERVAL YEAR TO MONTH, C33 INTERVAL DAY TO HOUR, C34 INTERVAL DAY TO MINUTE, C35 INTERVAL DAY TO SECOND, C36 INTERVAL HOUR TO MINUTE, C37 INTERVAL HOUR TO SECOND, C38 INTERVAL MINUTE TO SECOND, C39 NUMERIC (19, 0) SIGNED, C40 NUMERIC (19, 0) UNSIGNED, PRIMARY KEY ( C19 ), CONSTRAINT C17C CHECK ( C17 < 50000 ) ) NO PARTITION " );
    // HASH by table.
    strcpy( ExecSQLStr[ 9 ],  "CREATE TABLE ROWSET_TABLE ( C01 CHAR( 20 ) CHARACTER SET ISO88591 NOT NULL, C02 CHAR( 20 ) CHARACTER SET UCS2, C03 VARCHAR( 20 ) CHARACTER SET ISO88591, C04 VARCHAR( 20 ) CHARACTER SET UCS2, C05 LONG VARCHAR( 20 ) CHARACTER SET ISO88591, C06 LONG VARCHAR( 20 ) CHARACTER SET UCS2, C07 NCHAR( 20 ), C08 NCHAR VARYING( 20 ), C09 DECIMAL (8, 0) SIGNED, C10 DECIMAL (8, 0) UNSIGNED, C11 NUMERIC (8, 0) SIGNED, C12 NUMERIC (8, 0) UNSIGNED, C13 TINYINT SIGNED, C14 TINYINT UNSIGNED, C15 SMALLINT SIGNED, C16 SMALLINT UNSIGNED, C17 INTEGER SIGNED NOT NULL, C18 INTEGER UNSIGNED, C19 LARGEINT NOT NULL NOT DROPPABLE, C20 REAL, C21 FLOAT(54), C22 DOUBLE PRECISION, C23 DATE, C24 TIME, C25 TIMESTAMP, C26 INTERVAL YEAR, C27 INTERVAL MONTH, C28 INTERVAL DAY, C29 INTERVAL HOUR, C30 INTERVAL MINUTE, C31 INTERVAL SECOND, C32 INTERVAL YEAR TO MONTH, C33 INTERVAL DAY TO HOUR, C34 INTERVAL DAY TO MINUTE, C35 INTERVAL DAY TO SECOND, C36 INTERVAL HOUR TO MINUTE, C37 INTERVAL HOUR TO SECOND, C38 INTERVAL MINUTE TO SECOND, C39 NUMERIC (19, 0) SIGNED, C40 NUMERIC (19, 0) UNSIGNED, PRIMARY KEY ( C19 ), CONSTRAINT C17C CHECK ( C17 < 50000 ) ) HASH2 PARTITION BY ( C19 ) " );
    // Surrogate key table.
    strcpy( ExecSQLStr[ 10 ], "CREATE TABLE ROWSET_TABLE ( C01 CHAR( 20 ) CHARACTER SET ISO88591 NOT NULL, C02 CHAR( 20 ) CHARACTER SET UCS2, C03 VARCHAR( 20 ) CHARACTER SET ISO88591, C04 VARCHAR( 20 ) CHARACTER SET UCS2, C05 LONG VARCHAR( 20 ) CHARACTER SET ISO88591, C06 LONG VARCHAR( 20 ) CHARACTER SET UCS2, C07 NCHAR( 20 ), C08 NCHAR VARYING( 20 ), C09 DECIMAL (8, 0) SIGNED, C10 DECIMAL (8, 0) UNSIGNED, C11 NUMERIC (8, 0) SIGNED, C12 NUMERIC (8, 0) UNSIGNED, C13 TINYINT SIGNED, C14 TINYINT UNSIGNED, C15 SMALLINT SIGNED, C16 SMALLINT UNSIGNED, C17 INTEGER SIGNED NOT NULL, C18 INTEGER UNSIGNED, C19 LARGEINT GENERATED BY DEFAULT AS IDENTITY NOT NULL NOT DROPPABLE, C20 REAL, C21 FLOAT(54), C22 DOUBLE PRECISION, C23 DATE, C24 TIME, C25 TIMESTAMP, C26 INTERVAL YEAR, C27 INTERVAL MONTH, C28 INTERVAL DAY, C29 INTERVAL HOUR, C30 INTERVAL MINUTE, C31 INTERVAL SECOND, C32 INTERVAL YEAR TO MONTH, C33 INTERVAL DAY TO HOUR, C34 INTERVAL DAY TO MINUTE, C35 INTERVAL DAY TO SECOND, C36 INTERVAL HOUR TO MINUTE, C37 INTERVAL HOUR TO SECOND, C39 NUMERIC (19, 0) SIGNED, C40 NUMERIC (19, 0) UNSIGNED, C38 INTERVAL MINUTE TO SECOND, PRIMARY KEY ( C19 ), CONSTRAINT C17C CHECK ( C17 < 50000 ) )" );
    // SET table
    strcpy( ExecSQLStr[ 11 ],  "CREATE SET TABLE ROWSET_TABLE ( C01 CHAR( 20 ) CHARACTER SET ISO88591 NOT NULL, C02 CHAR( 20 ) CHARACTER SET UCS2, C03 VARCHAR( 20 ) CHARACTER SET ISO88591, C04 VARCHAR( 20 ) CHARACTER SET UCS2, C05 LONG VARCHAR( 20 ) CHARACTER SET ISO88591, C06 LONG VARCHAR( 20 ) CHARACTER SET UCS2, C07 NCHAR( 20 ), C08 NCHAR VARYING( 20 ), C09 DECIMAL (8, 0) SIGNED, C10 DECIMAL (8, 0) UNSIGNED, C11 NUMERIC (8, 0) SIGNED, C12 NUMERIC (8, 0) UNSIGNED, C13 TINYINT SIGNED, C14 TINYINT UNSIGNED, C15 SMALLINT SIGNED, C16 SMALLINT UNSIGNED, C17 INTEGER SIGNED NOT NULL, C18 INTEGER UNSIGNED, C19 LARGEINT NOT NULL NOT DROPPABLE, C20 REAL, C21 FLOAT(54), C22 DOUBLE PRECISION, C23 DATE, C24 TIME, C25 TIMESTAMP, C26 INTERVAL YEAR, C27 INTERVAL MONTH, C28 INTERVAL DAY, C29 INTERVAL HOUR, C30 INTERVAL MINUTE, C31 INTERVAL SECOND, C32 INTERVAL YEAR TO MONTH, C33 INTERVAL DAY TO HOUR, C34 INTERVAL DAY TO MINUTE, C35 INTERVAL DAY TO SECOND, C36 INTERVAL HOUR TO MINUTE, C37 INTERVAL HOUR TO SECOND, C38 INTERVAL MINUTE TO SECOND, C39 NUMERIC (19, 0) SIGNED, C40 NUMERIC (19, 0) UNSIGNED, PRIMARY KEY ( C19 ), CONSTRAINT C17C CHECK ( C17 < 50000 ) )" );// NO PARTITION LOCATION $FC0300" );
    // MULTISET table
    strcpy( ExecSQLStr[ 12 ],  "CREATE MULTISET TABLE ROWSET_TABLE ( C01 CHAR( 20 ) CHARACTER SET ISO88591 NOT NULL, C02 CHAR( 20 ) CHARACTER SET UCS2, C03 VARCHAR( 20 ) CHARACTER SET ISO88591, C04 VARCHAR( 20 ) CHARACTER SET UCS2, C05 LONG VARCHAR( 20 ) CHARACTER SET ISO88591, C06 LONG VARCHAR( 20 ) CHARACTER SET UCS2, C07 NCHAR( 20 ), C08 NCHAR VARYING( 20 ), C09 DECIMAL (8, 0) SIGNED, C10 DECIMAL (8, 0) UNSIGNED, C11 NUMERIC (8, 0) SIGNED, C12 NUMERIC (8, 0) UNSIGNED, C13 TINYINT SIGNED, C14 TINYINT UNSIGNED, C15 SMALLINT SIGNED, C16 SMALLINT UNSIGNED, C17 INTEGER SIGNED NOT NULL, C18 INTEGER UNSIGNED, C19 LARGEINT NOT NULL NOT DROPPABLE, C20 REAL, C21 FLOAT(54), C22 DOUBLE PRECISION, C23 DATE, C24 TIME, C25 TIMESTAMP, C26 INTERVAL YEAR, C27 INTERVAL MONTH, C28 INTERVAL DAY, C29 INTERVAL HOUR, C30 INTERVAL MINUTE, C31 INTERVAL SECOND, C32 INTERVAL YEAR TO MONTH, C33 INTERVAL DAY TO HOUR, C34 INTERVAL DAY TO MINUTE, C35 INTERVAL DAY TO SECOND, C36 INTERVAL HOUR TO MINUTE, C37 INTERVAL HOUR TO SECOND, C38 INTERVAL MINUTE TO SECOND, C39 NUMERIC (19, 0) SIGNED, C40 NUMERIC (19, 0) UNSIGNED, PRIMARY KEY ( C19 ), CONSTRAINT C17C CHECK ( C17 < 50000 ) )" );
    // INSERT_SELECT
    strcpy( ExecSQLStr[ 13 ],  "CREATE TABLE TO_ROWSET_TABLE ( C01 CHAR( 20 ) CHARACTER SET ISO88591 NOT NULL, C02 CHAR( 20 ) CHARACTER SET UCS2, C03 VARCHAR( 20 ) CHARACTER SET ISO88591, C04 VARCHAR( 20 ) CHARACTER SET UCS2, C05 LONG VARCHAR( 20 ) CHARACTER SET ISO88591, C06 LONG VARCHAR( 20 ) CHARACTER SET UCS2, C07 NCHAR( 20 ), C08 NCHAR VARYING( 20 ), C09 DECIMAL (8, 0) SIGNED, C10 DECIMAL (8, 0) UNSIGNED, C11 NUMERIC (8, 0) SIGNED, C12 NUMERIC (8, 0) UNSIGNED, C13 TINYINT SIGNED, C14 TINYINT UNSIGNED, C15 SMALLINT SIGNED, C16 SMALLINT UNSIGNED, C17 INTEGER SIGNED NOT NULL, C18 INTEGER UNSIGNED, C19 LARGEINT NOT NULL NOT DROPPABLE, C20 REAL, C21 FLOAT(54), C22 DOUBLE PRECISION, C23 DATE, C24 TIME, C25 TIMESTAMP, C26 INTERVAL YEAR, C27 INTERVAL MONTH, C28 INTERVAL DAY, C29 INTERVAL HOUR, C30 INTERVAL MINUTE, C31 INTERVAL SECOND, C32 INTERVAL YEAR TO MONTH, C33 INTERVAL DAY TO HOUR, C34 INTERVAL DAY TO MINUTE, C35 INTERVAL DAY TO SECOND, C36 INTERVAL HOUR TO MINUTE, C37 INTERVAL HOUR TO SECOND, C38 INTERVAL MINUTE TO SECOND, C39 NUMERIC (19, 0) SIGNED, C40 NUMERIC (19, 0) UNSIGNED, PRIMARY KEY ( C19 ), CONSTRAINT C17T CHECK ( C17 < 50000 ) )" );
    strcpy( ExecSQLStr[ 14 ],  "INSERT INTO TO_ROWSET_TABLE SELECT * FROM ROWSET_TABLE WHERE C19 = ?" );
    strcpy( ExecSQLStr[ 15 ],  "DROP TABLE TO_ROWSET_TABLE CASCADE" );
	// Index
    strcpy( ExecSQLStrIndex[ 0 ], "CREATE INDEX INDEX_C01 ON ROWSET_TABLE( C19 )" );
    strcpy( ExecSQLStrIndex[ 1 ], "DROP INDEX INDEX_C01 CASCADE" );
    // RI
    strcpy( ExecSQLStrRI[ 0 ], "CONTROL QUERY DEFAULT REF_CONSTRAINT_NO_ACTION_LIKE_RESTRICT 'ON'" );
    strcpy( ExecSQLStrRI[ 1 ], "CREATE TABLE ROWSET_TABLE_2 LIKE ROWSET_TABLE" );
    strcpy( ExecSQLStrRI[ 2 ], "ALTER TABLE ROWSET_TABLE ADD CONSTRAINT CC7 FOREIGN KEY( C01 ) REFERENCES ROWSET_TABLE_2( C01)" );
    strcpy( ExecSQLStrRI[ 3 ], "DROP TABLE ROWSET_TABLE_2 CASCADE" );
    // Volatile
    strcpy( ExecSQLStrVolatile[ 0 ], "CREATE VOLATILE TABLE ROWSET_TABLE ( C01 CHAR( 20 ) CHARACTER SET ISO88591 NOT NULL, C02 CHAR( 20 ) CHARACTER SET UCS2, C03 VARCHAR( 20 ) CHARACTER SET ISO88591, C04 VARCHAR( 20 ) CHARACTER SET UCS2, C05 LONG VARCHAR( 20 ) CHARACTER SET ISO88591, C06 LONG VARCHAR( 20 ) CHARACTER SET UCS2, C07 NCHAR( 20 ), C08 NCHAR VARYING( 20 ), C09 DECIMAL (8, 0) SIGNED, C10 DECIMAL (8, 0) UNSIGNED, C11 NUMERIC (8, 0) SIGNED, C12 NUMERIC (8, 0) UNSIGNED, C13 TINYINT SIGNED, C14 TINYINT UNSIGNED, C15 SMALLINT SIGNED, C16 SMALLINT UNSIGNED, C17 INTEGER SIGNED NOT NULL, C18 INTEGER UNSIGNED, C19 LARGEINT NOT NULL NOT DROPPABLE, C20 REAL, C21 FLOAT(54), C22 DOUBLE PRECISION, C23 DATE, C24 TIME, C25 TIMESTAMP, C26 INTERVAL YEAR, C27 INTERVAL MONTH, C28 INTERVAL DAY, C29 INTERVAL HOUR, C30 INTERVAL MINUTE, C31 INTERVAL SECOND, C32 INTERVAL YEAR TO MONTH, C33 INTERVAL DAY TO HOUR, C34 INTERVAL DAY TO MINUTE, C35 INTERVAL DAY TO SECOND, C36 INTERVAL HOUR TO MINUTE, C37 INTERVAL HOUR TO SECOND, C38 INTERVAL MINUTE TO SECOND, C39 NUMERIC (19, 0) SIGNED, C40 NUMERIC (19, 0) UNSIGNED, PRIMARY KEY ( C19 ) ) " );
    strcpy( ExecSQLStrVolatile[ 1 ], "DROP VOLATILE TABLE ROWSET_TABLE CASCADE " );
    // MVS
    strcpy( ExecSQLStrMVS[ 0 ], "ALTER TABLE ROWSET_TABLE ATTRIBUTE ALL MVS ALLOWED" );
    strcpy( ExecSQLStrMVS[ 1 ], "CREATE TABLE ROWSET_TABLE_ALT ( C01 CHAR( 20 ) NOT NULL, C17 INTEGER SIGNED, C19 LARGEINT NOT NULL NOT DROPPABLE, PRIMARY KEY ( C19 ), CONSTRAINT C17AC CHECK ( C17 < 50000 ) )" );
    strcpy( ExecSQLStrMVS[ 2 ], "CREATE VIEW VIEW_ROWSET_TABLE AS SELECT A.C01 AS AC01, A.C17 AS AC17, A.C19 AS AC19, B.C01 AS BC01, B.C17 AS BC17, B.C19 AS BC19 FROM ROWSET_TABLE A, ROWSET_TABLE_ALT B WHERE A.C19 = B.C19;" );
    strcpy( ExecSQLStrMVS[ 3 ], "CREATE MV MVS_ROWSET_TABLE REFRESH ON STATEMENT INITIALIZE ON CREATE AS SELECT A.C01 AS AC01, A.C17 AS AC17, A.C19 AS AC19, B.C01 AS BC01, B.C17 AS BC17, B.C19 AS BC19 FROM ROWSET_TABLE A, ROWSET_TABLE_ALT B WHERE A.C19 = B.C19;" );
    strcpy( ExecSQLStrMVS[ 4 ], "DROP VIEW VIEW_ROWSET_TABLE CASCADE;" );
    strcpy( ExecSQLStrMVS[ 5 ], "DROP MV MVS_ROWSET_TABLE CASCADE;" );
    strcpy( ExecSQLStrMVS[ 6 ], "DROP TABLE ROWSET_TABLE_ALT CASCADE;" );
    // Before Trigger
    strcpy( ExecSQLStrBeforeTrigger[ 0 ], "DROP TRIGGER ROWSET_BEFORETRIGER;" );
    strcpy( ExecSQLStrBeforeTrigger[ 1 ], "CREATE TRIGGER ROWSET_BEFORETRIGER BEFORE INSERT ON ROWSET_TABLE REFERENCING NEW AS NEWROW FOR EACH ROW WHEN (NEWROW.C19 > 0 ) SET NEWROW.C39 = 987654321098765, NEWROW.C40=987654321098765;" );
    // AfterTrigger
    strcpy( ExecSQLStrAfterTrigger[ 0 ], "DROP TRIGGER ROWSET_AFTERTRIGER;" );
    strcpy( ExecSQLStrAfterTrigger[ 1 ], "DROP TABLE ROWSET_TABLE_TMP CASCADE" );
    strcpy( ExecSQLStrAfterTrigger[ 2 ], "CREATE TRIGGER ROWSET_AFTERTRIGER AFTER INSERT ON ROWSET_TABLE REFERENCING NEW AS NEWROW FOR EACH ROW WHEN ( NEWROW.C19 > 5 ) INSERT INTO ROWSET_TABLE_TMP VALUES ( NEWROW.C01,NEWROW.C17,NEWROW.C19 );" );
    strcpy( ExecSQLStrAfterTrigger[ 3 ], "CREATE TABLE ROWSET_TABLE_TMP ( C01 CHAR( 20 ) NOT NULL, C17 INTEGER SIGNED, C19 LARGEINT NOT NULL NOT DROPPABLE, PRIMARY KEY ( C19 ), CONSTRAINT C17AT CHECK ( C17 < 50000 ) )" );
    strcpy( ExecSQLStrAfterTrigger[ 4 ], "DELETE FROM ROWSET_TABLE_TMP" );

    RecordToLog( " > Initializing ODBC handles and connection.\n" );
	// start for ALM log
	RecordTo_ALM_Log("");
	// end for ALM log

    if( EstablishHandlesAndConnection( ) )
    {
		// Lets count how many tests are going to be run.
		// This is purely for debug and logging information.
		testTotal = 0;
		for( int loop1 = 0; tableTypes[ loop1 ] != STOP; loop1++ )
			for( int loopA = 0; tableFeatures[ loopA ] != STOP; loopA++ )
				for( int loopB = 0; modes[ loopB ] != STOP; loopB++  )
					for( int loopC = 0; features[ loopC ] != STOP; loopC++  )
						for( int loopD = 0; operations[ loopD ] != STOP; loopD++ )
							for( int loopE = 0; bindOrientations[ loopE ] != STOP; loopE++ )
								for( int loopF = 0; injectionTypes[ loopF ] != STOP; loopF++ )
									for( int loopG = 0; numberOfRows[ loopG ] != STOP; loopG++ )
										for( int loopH = 0; rowsetSizes[ loopH ] != STOP; loopH++ )
											for( int loopI = 0; commitRates[ loopI ] != STOP; loopI++ )
												for( int loopJ = 0; actions[ loopJ ] != STOP; loopJ++  )
												{
													unitTest.tableType = loop1;
													unitTest.tableFeature = loopA;
													unitTest.mode = loopB;
													unitTest.feature = loopC;
													unitTest.operation = loopD;
													unitTest.bindOrientation = loopE;
													unitTest.injectionType = loopF;
													unitTest.numberOfRows = loopG;
													unitTest.rowsetSize = loopH;
													unitTest.commitRate = loopI;
													unitTest.action = loopJ;
													if(!IgnoreTest()) testTotal++;
												 }

		// Reset unit test.
		unitTest.mode = 0;
		unitTest.feature = 0;
		unitTest.operation = 0;
		unitTest.bindOrientation = 0;
		unitTest.tableType = 0;
		unitTest.tableFeature = 0;
		unitTest.injectionType = 0;
		unitTest.numberOfRows = 0;
		unitTest.rowsetSize = 0;
		unitTest.commitRate = 0;
		unitTest.action = -1;

		// If we are to run specific test then make sure the user didn't specify didn't one out of bounds.
		//if( ( singleTest || resumeTesting ) && ( testToRun > testTotal ) )
		//{
		//    if( singleTest )
		//    {
		//        RecordToLog( " > Could not run test %d. There are only %d tests.\n", testToRun, testTotal );
		//    }
		//    else
		//    {
		//        RecordToLog( " > Could not resume testing from %d. There are only %d tests.\n", testToRun, testTotal );
		//    }
		//    return 0;
		//}

		while( NextTest( ) )
        {
			//printf("Hit enter to go next\n");
			//getchar();
			RecordToLog( "Running test %d of %d.\n", testCount, testTotal );

			// If we are to run a single test or resume testing from a point we need to 
            // adjust the count.
            if( singleTest || resumeTesting )
            {
                while( testCount != testToRun )
                {
                    NextTest( );
                }
                resumeTesting = false;
            }

			if( debug ) PrintTestInformation( );
			
			/***** ALM Log begin *****/
			ALM_TestInformation(ALM_NextTestInfo);
			if (strcmp (ALM_NextTestInfo,Heading) != 0)
			{
				if (ALM_testCounter > 0)
				{
					ALM_LogTestCaseInfo(ALM_TestCaseId, Heading, ALM_testStart, testCount-1);

					/***** ALM Log begin *****/
					ALM_Test_end = time( NULL);
					/* Log into ALM report as well */
					ALM_LogTestResultInfo(_TestCase, ALM_Test_start, ALM_Test_end);
						/***** ALM Log end *****/
				}

				ALM_testCounter++;
				bTestCounted = true;
				// SET initial results of test case, any test case failed will be tracked.
				_TestCase = PASSED;
				ALM_testStart = testCount;

				strcpy (Heading, ALM_NextTestInfo);
				ALM_Test_start = time( NULL);
				/* Log into ALM report as well */
				sprintf(ALM_TestCaseId,"Test%d",ALM_testCounter);
			}
			else
				bTestCounted = false;
			/***** ALM Log end *****/

            switch( actions[ unitTest.action ] )
            {
                case INSERT:
                    DeleteRows( );
                case INSERT_SELECT:
                case DELETE_PARAM:
                case UPDATE:
                    // Bind the C variables to the SQL columns to insert data.
                    RecordToLog( " > Binding parameters.\n" );

                    if( !BindParameters( ) )
                    {
                        RecordToLog( "....FAILED!....\n" );
						/***** ALM Log begin *****/
						_TestCase=FAILED;
						/***** ALM Log end *****/
                        testFail++;
                        break;
                    }
               
                    switch( actions[ unitTest.action ] )
                    {
                        case INSERT:
                            RecordToLog( " > Inserting rows.\n" );
                            break;
                        case DELETE_PARAM:
                            RecordToLog( " > Deleting rows.\n" );
                            break;
                        case UPDATE:
                            RecordToLog( " > Updating rows.\n" );
                            break;
                        case INSERT_SELECT:
                            RecordToLog( " > Inserting Select rows.\n" );
                            break;
                    }
                    if( !RowsetDML( ) ) 
                    {
                        RecordToLog( "....FAILED!....\n" );
						/***** ALM Log begin *****/
						_TestCase=FAILED;
						/***** ALM Log end *****/
                        testFail++;
                        break;
                    } 
                    else
                    {
                        testPass++;
                        break;
                    }
                    break;
                case INSERT_BULK:
                    // Bind the C variables to the SQL columns to insert data.
                    RecordToLog( " > Binding columns.\n" );
                    if( !BindCols( ) )
                    {
                        RecordToLog( "....FAILED!....\n" );

						/***** ALM Log begin *****/
						_TestCase=FAILED;
						/***** ALM Log end *****/

						testFail++;
                        break;
                    }
                
                    RecordToLog( " > Inserting bulk rows.\n" );

                    if( !RowsetDMLBulk( ) ) 
                    {
                        RecordToLog( "....FAILED!....\n" );
						/***** ALM Log begin *****/
						_TestCase=FAILED;
						/***** ALM Log end *****/
                        testFail++;
                        break;
                    } 
                    else
                    {
                        testPass++;
                        break;
                    }
                    break;
                case SELECT:
                    // Bind the C variables to the SQL columns to gather data.
                    RecordToLog( " > Binding columns.\n" );
                    if( !BindCols( ) )
                    {
                        RecordToLog( "....FAILED!....\n" );
						/***** ALM Log begin *****/
						_TestCase=FAILED;
						/***** ALM Log end *****/
                        testFail++;
                        break;
                    }
                    // Fetch the rows from the table.
                    RecordToLog( " > Fetching rows.\n" );
                    if( !RowsetFetch( ) ) 
                    {
                        RecordToLog( "....FAILED!....\n" );
						/***** ALM Log begin *****/
						_TestCase=FAILED;
						/***** ALM Log end *****/
                        testFail++;
                        break;
                    } 
                    else
                    {
                        testPass++;
                    }
                    break;
                default:
                    RecordToLog( " > INTERNAL ERROR: An unknown testing action has been discovered.\n" );
                    break;
            }

            if( actions[ unitTest.action ] == INSERT_SELECT )
            {
                RecordToLog( " > Cleaning up select table.\n" );
                DeleteRows( );
            }
        
            if( actions[ unitTest.action ] == DELETE_PARAM )
            {
                RecordToLog( " > Cleaning up table.\n" );
                DeleteRows( );
            }

            RecordToLog( " > Free handles.\n" );
            FreeHandles( );

            // We don't want to run any more tests for single tests.
            if( singleTest )
            {
                break;
            }
        } // NextTest

        RecordToLog( " > Releasing handles.\n" );
        DeleteHandles( );

    } // EstablishHandlesAndConnection

	// to get the last group test result log out.
	if (ALM_testCounter > 0)
	{
		ALM_LogTestCaseInfo(ALM_TestCaseId, Heading, ALM_testStart, testCount-1);

		/***** ALM Log begin *****/
		ALM_Test_end = time( NULL);
		/* Log into ALM report as well */
		ALM_LogTestResultInfo(_TestCase, ALM_Test_start, ALM_Test_end);
			/***** ALM Log end *****/
	}
	
	testCount--;
    RecordToLog( "Test count: %d\n", testCount );
    RecordToLog( "Test fail:  %d\n", testFail );
    RecordToLog( "Test pass:  %d\n", testPass );
    RecordToLog( "rowsets TEST RESULT: %s\n", ((testFail) ? "FAIL" : "PASS"));  
 
    if( timeMetrics )
        DisplayTimeMetrics( );

    return 0;
}

/* Function          : NextTest
   Calling Arguments : none
   Return Arguments  : true : Another test to run.
                       false : No more tests to run.

   Description:
   Finds the next test to run.
 */
bool NextTest( )
{
    int loop1 = unitTest.tableType;
    int loopA = unitTest.tableFeature;
    int loopB = unitTest.mode;
    int loopC = unitTest.feature;
    int loopD = unitTest.operation;
    int loopE = unitTest.bindOrientation;
    int loopF = unitTest.injectionType;
    int loopG = unitTest.numberOfRows;
    int loopH = unitTest.rowsetSize;
    int loopI = unitTest.commitRate;
    int loopJ = unitTest.action;

    if (loop1==0 && loopA==0 && loopB==0 && loopC==0 && loopD==0 && loopE==0 && loopF==0 && loopG==0 && loopH==0 && loopI==0 && loopJ==-1)
	{
		if( !IgnoreTest( ) ) {
			DropTable();
			CreateTable();
		}
	}

    testCount++;

    loopJ++;
    if( actions[ loopJ ] == STOP )
    {
        unitTest.action = 0;
        loopI++;
    }
    else
    {
        unitTest.action = loopJ;
        goto NEXT_TEST_FINISH;
    }

    if( commitRates[ loopI ] == STOP )
    {
        unitTest.commitRate = 0;
        loopH++;
    }
    else
    {
        unitTest.commitRate = loopI;
        goto NEXT_TEST_FINISH;
    }

    if( rowsetSizes[ loopH ] == STOP )
    {
        unitTest.rowsetSize = 0;
        loopG++;
    }
    else
    {
        unitTest.rowsetSize = loopH;
        goto NEXT_TEST_FINISH;
    }

    if( numberOfRows[ loopG ] == STOP )
    {
        unitTest.numberOfRows = 0;
        loopF++;
    }
    else
    {
        unitTest.numberOfRows = loopG;
        goto NEXT_TEST_FINISH;
    }
    if( injectionTypes[ loopF ] == STOP )
    {
        unitTest.injectionType = 0;
        loopE++;
    }
    else
    {
        unitTest.injectionType = loopF;
        goto NEXT_TEST_FINISH;
    }
    if( bindOrientations[ loopE ] == STOP )
    {
        unitTest.bindOrientation = 0;
        loopD++;
    }
    else
    {
        unitTest.bindOrientation = loopE;
        goto NEXT_TEST_FINISH;
    }
    if( operations[ loopD ] == STOP )
    {
        unitTest.operation = 0;
        loopC++;
    }
    else
    {
        unitTest.operation = loopD;
        goto NEXT_TEST_FINISH;
    }
    if( features[ loopC ] == STOP )
    {
        unitTest.feature = 0;
        loopB++;
    }
    else
    {
        unitTest.feature = loopC;
        goto NEXT_TEST_FINISH;
    }
    if( modes[ loopB ] == STOP )
    {
        unitTest.mode = 0;
        loopA++;
    }
    else
    {
        unitTest.mode = loopB;
        goto NEXT_TEST_FINISH;
    }
    if( tableFeatures[ loopA ] == STOP )
    {
        unitTest.tableFeature = 0;
        loop1++;
    }
    else
    {
        unitTest.tableFeature = loopA;
		if( !IgnoreTest( ) ) {
			DropTable();
			CreateTable();
		}
        goto NEXT_TEST_FINISH;
    }
    if( tableTypes[ loop1 ] == STOP )
    {
        return false;
    }
    else
    {
        unitTest.tableType = loop1;
		if( !IgnoreTest( ) ) {
			DropTable();
			CreateTable();
		}
        goto NEXT_TEST_FINISH;
    }

NEXT_TEST_FINISH:
    if( IgnoreTest( ) ) 
    {
        testCount--;
        return NextTest( );
    }
    return true;
}   

/* Function          : IgnoreTest
   Calling Arguments : none
   Return Arguments  : true : Ignore the test.
                       false : Do not ignore the test.

   Description:
   This checks to see if the program should or should not ignore the test.
 */
bool IgnoreTest( )
{
    for( int loop = 0; ignoredTests[ loop ] != STOP; loop++ )
    {
        if( ignoredTests[ loop ] == testCount )
        {
            return true;
        }
    }

    // HASH2 only works under Linux.
#ifndef _HASH2
    if( features[ unitTest.feature ] == HASH2 )
    {
        return true;
    }
#endif

/*
    // Async only works under Windows.
#ifndef WIN32
    if( features[ unitTest.feature ] == ASYNC )
    {
        return true;
    }
#endif
*/
    // Volatile tables can not have unique constraints
    if( ( tableTypes[ unitTest.tableType ] == VOLATILE ) && ( injectionTypes[ unitTest.injectionType ] == UNIQUECONST ) )
    {
        return true;
    }

    // A materialized view cannot be created on volatile tables
	if( ( tableTypes[ unitTest.tableType ] == VOLATILE ) && ( tableFeatures[ unitTest.tableFeature ] == MVS ) )
    {
        return true;
    }

	// Multiset tables only work with MODE_SPECIAL_1
    if( ( tableTypes[ unitTest.tableType ] == MULTISET ) && ( errorChecking == STANDARD ) )
    {
        return true;
    }

    return false;
}

/* Function          : EstablishHandlesAndConnection
   Calling Arguments : none
   Return Arguments  : true : Established a good connection and handles.
                       false: Could not establish a good connection or handles.

   Description:
   Creates the needed handles to perform all the ODBC tests. Also this also
   establishes the ODBC connection.

 */
bool EstablishHandlesAndConnection(  )
{
    SQLRETURN  retcode;       // Used to gather the return value of all ODBC API calls.
    
    //if( ( tableTypes[ unitTest.tableType ] == VOLATILE ) && ( actions[ unitTest.action ] != INSERT ) )
    //{
    //    return true;
    //}

    // Allocate the evironment handle.
    retcode = SQLAllocHandle( SQL_HANDLE_ENV, SQL_NULL_HANDLE, &handle[ SQL_HANDLE_ENV ] );
    if( retcode != SQL_SUCCESS )    
    {
        CheckMsgs( "SQLAllocHandle()", __LINE__ );
        return false;
    }

    // Set the environment variable to ODBC version 3
    retcode = SQLSetEnvAttr( handle[ SQL_HANDLE_ENV ], SQL_ATTR_ODBC_VERSION, (SQLPOINTER)SQL_OV_ODBC3, 0 ); 
    if( retcode != SQL_SUCCESS )    
    {
        CheckMsgs( "SQLSetEnvAttr()", __LINE__ );
        DeleteHandles( );
        return false;
    }

    // Allocate the connection handle off the environment handle.
    retcode = SQLAllocHandle( SQL_HANDLE_DBC, handle[ SQL_HANDLE_ENV ], &handle[ SQL_HANDLE_DBC ] ); 
    if( retcode != SQL_SUCCESS )    
    {
        CheckMsgs( "SQLAllocHandle()", __LINE__ );
        DeleteHandles( );
        return false;
    }

    // The HASH2 feature requires specific connection attributes established before connecting.
    if( features[ unitTest.feature ] == HASH2 )
    {
        RecordToLog( " >> Setting up SQL_MODE_LOADER.\n" );
        SQLUINTEGER mode = 1;
        SQLUINTEGER SQL_MODE_LOADER = 4001;
        retcode = SQLSetConnectAttr( handle[ SQL_HANDLE_DBC ], SQL_MODE_LOADER, (SQLPOINTER)mode, 0);
        if( retcode != SQL_SUCCESS )    
        {
            CheckMsgs( "SQLSetConnectAttr()", __LINE__ );
            DeleteHandles( );
            return false;
        }

        RecordToLog( " >> Setting up SQL_START_NODE.\n" );
        SQLUINTEGER startnode = 5;
        SQLUINTEGER SQL_START_NODE = 4000;
        retcode = SQLSetConnectAttr( handle[ SQL_HANDLE_DBC ], SQL_START_NODE, (void *) startnode, 0);
        if( retcode != SQL_SUCCESS )    
        {
            CheckMsgs( "SQLSetConnectAttr()", __LINE__ );
            DeleteHandles( );
            return false;
        }

        RecordToLog( " >> Setting up SQL_STREAMS_PER_SEG.\n" );
        SQLUINTEGER streams_per_node = 1;
        SQLUINTEGER SQL_STREAMS_PER_SEG = 4002;
        retcode = SQLSetConnectAttr( handle[ SQL_HANDLE_DBC ], SQL_STREAMS_PER_SEG, (void *) streams_per_node, 0 );
        if( retcode != SQL_SUCCESS )    
        {
            CheckMsgs( "SQLSetConnectAttr()", __LINE__ );
            DeleteHandles( );
            return false;
        }

    }

#ifdef _LDAP
    retcode = SQLSetConnectAttr(handle[ SQL_HANDLE_DBC ],SQL_ATTR_ROLENAME,(SQLPOINTER)secondaryRole,SQL_NTS);
    if(retcode != SQL_SUCCESS || retcode != SQL_SUCCESS_WITH_INFO) {
		CheckMsgs("Unable to set the SQL_ATTR_ROLENAME\n", __LINE__);
    }
#endif

    // Connect to the ODBC service.
    retcode = SQLConnect( handle[ SQL_HANDLE_DBC ], (SQLCHAR*) datasource, SQL_NTS,
                          (SQLCHAR*) uid, SQL_NTS, (SQLCHAR*) password, SQL_NTS );
    if( retcode != SQL_SUCCESS && retcode != SQL_SUCCESS_WITH_INFO )    
    {
        CheckMsgs( "SQLConnect()", __LINE__ );
        if( retcode != SQL_SUCCESS_WITH_INFO )
        {
            DeleteHandles( );
            return false;
        }
    }

    // Turn off autocommit.
/*****
    if( features[ unitTest.feature ] == ASYNC )
    {
        retcode = SQLSetConnectAttr( handle[ SQL_HANDLE_DBC ], SQL_ATTR_AUTOCOMMIT, (SQLPOINTER)SQL_AUTOCOMMIT_OFF, 0 );
        if( retcode != SQL_SUCCESS )    
        {
            CheckMsgs( "SQLSetConnectAttr()", __LINE__ );
            SQLDisconnect( handle[ SQL_HANDLE_DBC ] );
            DeleteHandles( );
            return false;
        }
    }
*****/

    // Allocate the SQL statement handle.
    retcode = SQLAllocHandle(SQL_HANDLE_STMT, handle[ SQL_HANDLE_DBC ], &handle[ SQL_HANDLE_STMT ] ); 
    if( retcode != SQL_SUCCESS )    
    {
        CheckMsgs( "SQLAllocHandle()", __LINE__ );
        SQLDisconnect( handle[ SQL_HANDLE_DBC ] );
        DeleteHandles( );
        return false;
    }
    
    // Turn on asynchronous operations.
    if( features[ unitTest.feature ] == ASYNC )
    {
        retcode = SQLSetStmtAttr( handle[ SQL_HANDLE_STMT ],
                                  SQL_ATTR_ASYNC_ENABLE, (SQLPOINTER)SQL_ASYNC_ENABLE_ON,
                                  sizeof( SQL_ASYNC_ENABLE_ON ) );
        if( retcode != SQL_SUCCESS ) 
        {
            CheckMsgs( "SQLSetStmtAttr()", __LINE__ );
            SQLDisconnect( handle[ SQL_HANDLE_DBC ] );
            DeleteHandles( );
            return false;
        }
    }

    // Here we need to turn for MODE_SPECIAL_1. This CQD changes the status array of
    // rowsets. We can not change this CQD as it's a read only CQD for the system.
    RecordToLog( " >> Checking for MODE_SPECIAL_1.\n" );
    if( strcmp ( CheckForCQD( "MODE_SPECIAL_1"), "ON" ) == 0 )
    {
        errorChecking = MODE_SPECIAL_1;
        RecordToLog( "  CQD: MODE_SPECIAL_1 is 'ON'\n" );
    }
    else
    {
        errorChecking = STANDARD;
    }

    RecordToLog( " >> Finished connecting to server.\n" );
    retcode = SQLFreeStmt( handle[ SQL_HANDLE_STMT ], SQL_CLOSE ); // Free and clearup the statement handle.
    if( retcode != SQL_SUCCESS )    
    {
        CheckMsgs( "SQLFreeStmt()", __LINE__ );
        DeleteHandles( );
        return false;
    }
   
    return true;
}

/* Function          : CreateTable
   Calling Arguments : none
   Return Arguments  : true : Was able to create the neccessary testing table.
                       false : Was not able to create the neccessary testing table.

   Description:
   Creates the needed table to perform the ODBC test(s).
 */
bool CreateTable( )
{
    SQLRETURN  retcode;       // Used to gather the return value of all ODBC API calls.
    retcode = SQL_SUCCESS;

    if( actions[ unitTest.action ] == INSERT_SELECT )
    {
            RecordToLog( " >> Creating select table. \n" );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStr[ 13 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            if( retcode != SQL_SUCCESS )    
            {
                CheckMsgs( "SQLExecDirect()", __LINE__ );
                DeleteHandles( );
                return false;
            }

            retcode = SQLFreeStmt( handle[ SQL_HANDLE_STMT ], SQL_CLOSE ); // Free and clearup the statement handle.
            if( retcode != SQL_SUCCESS )    
            {
                CheckMsgs( "SQLFreeStmt()", __LINE__ );
                DeleteHandles( );
                return false;
            }

            return true;
    }

    switch( tableTypes[ unitTest.tableType ] )
    {
        case POSOFF:
            RecordToLog( " >> Creating no partition table. \n" );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStr[ 8 ], SQL_NTS ) ) == SQL_STILL_EXECUTING ); // Create the table.
            break;
        case SURROGATE:
            RecordToLog( " >> Creating surrogate key table. \n" );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStr[ 9 ], SQL_NTS ) ) == SQL_STILL_EXECUTING ); // Create the table.
            break;
        case VOLATILE:
            RecordToLog( " >> Creating volatile table. \n" );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStrVolatile[ 0 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            break;
        case SET:
            RecordToLog( " >> Creating set table. \n" );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStr[ 11 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            break;
        case MULTISET:
            RecordToLog( " >> Creating multiset table. \n" );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStr[ 12 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            break;
        case REGULAR:
        default:
            if( features[ unitTest.feature ] == HASH2 )
            {
                RecordToLog( " >> Creating HASH2 table. \n" );
                while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStr[ 9 ], SQL_NTS ) ) == SQL_STILL_EXECUTING ); // Create the table.
            }
            else
            {
                RecordToLog( " >> Creating standard table. \n" );
                while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStr[ 1 ], SQL_NTS ) ) == SQL_STILL_EXECUTING ); // Create the table.
            }
            break;
    }

    switch( tableFeatures[ unitTest.tableFeature ] )
    {
        case INDEX:
            RecordToLog( " >> Creating index. \n" );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStrIndex[ 0 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            break;
        case MVS:
            RecordToLog( " >> MVS setup on standard table. \n" );
            RecordToLog( "   >> Allowing MVS on standard table. \n" );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStrMVS[ 0 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            if( retcode != SQL_SUCCESS )    
            {
                CheckMsgs( "SQLExecDirect()", __LINE__ );
                return false;
            }
            RecordToLog( "   >> Creating an alternative table. \n" );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStrMVS[ 1 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            if( retcode != SQL_SUCCESS )    
            {
                CheckMsgs( "SQLExecDirect()", __LINE__ );
                return false;
            }
            RecordToLog( "   >> Creating a view on standard and alternative table. \n" );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStrMVS[ 2 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            if( retcode != SQL_SUCCESS )    
            {
                CheckMsgs( "SQLExecDirect()", __LINE__ );
                return false;
            }
            RecordToLog( "   >> Creating MVS on standard and alternative table. \n" );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStrMVS[ 3 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            if( retcode != SQL_SUCCESS )    
            {
                CheckMsgs( "SQLExecDirect()", __LINE__ );
                return false;
            }
            break;
        case RI:
            RecordToLog( " >> Initializing CQD. \n" );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStrRI[ 0 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            if( retcode != SQL_SUCCESS )    
            {
                CheckMsgs( "SQLExecDirect()", __LINE__ );
                return false;
            }
            RecordToLog( " >> Creating LIKE table. \n" );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStrRI[ 1 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            if( retcode != SQL_SUCCESS )    
            {
                CheckMsgs( "SQLExecDirect()", __LINE__ );
                return false;
            }
            RecordToLog( " >> Creating referential constraint. \n" );
            while ( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStrRI[ 2 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            break;
        case BEFORETRIGGER:
            RecordToLog( " >> Before trigger setup on standard table. \n" );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStrBeforeTrigger[ 1 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            if( retcode != SQL_SUCCESS )    
            {
                CheckMsgs( "SQLExecDirect()", __LINE__ );
                return false;
            }
            break;
        case AFTERTRIGGER:
            RecordToLog( " >> After trigger tmp table. \n" );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStrAfterTrigger[ 3 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            if( retcode != SQL_SUCCESS )    
            {
                CheckMsgs( "SQLExecDirect()", __LINE__ );
                return false;
            }
            RecordToLog( " >> After trigger setup on standard table. \n" );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStrAfterTrigger[ 2 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            if( retcode != SQL_SUCCESS )    
            {
                CheckMsgs( "SQLExecDirect()", __LINE__ );
                return false;
            }
            break;
        default:
            break;
    }

	if( ( retcode != SQL_SUCCESS ) && ( retcode != SQL_SUCCESS_WITH_INFO ) && ( !singleTest ) )    
    {
        CheckMsgs( "SQLExecDirect()", __LINE__ );
        DeleteHandles( );
        return false;
    }

    //if( features[ unitTest.feature ] != HASH2 && 
    //    retcode == SQL_SUCCESS )
    //{
    //    RecordToLog( " >> Committing transaction.\n" );
    //    retcode = SQLEndTran( SQL_HANDLE_DBC, handle[ SQL_HANDLE_DBC ], SQL_COMMIT ); // Commit the transaction.
    //    if( retcode != SQL_SUCCESS )    
    //    {
    //        CheckMsgs( "SQLEndTran()", __LINE__ );
    //        DeleteHandles( );
    //        return false;
    //    }
    //}

    retcode = SQLFreeStmt( handle[ SQL_HANDLE_STMT ], SQL_CLOSE ); // Free and clearup the statement handle.
    if( retcode != SQL_SUCCESS )    
    {
        CheckMsgs( "SQLFreeStmt()", __LINE__ );
        DeleteHandles( );
        return false;
    }

    return true;
}

/* Function          : IgnoreMsg
   Calling Arguments : SQLCHAR* : The ODBC state to ignore. 10 byte string.
                       SQWORD   : The ODBC native error to ignore.
   Return Arguments  : none

   Description:
   This function populates a data structure on what messages to ignore when a
   API call fails. This happens from time to time depending on the scenario
   the tests under takes. Example, deleting a table at the start of the test
   when no table exists.
   
 */
void IgnoreMsg( SQLCHAR *state, SDWORD nativeError )
{
    // We only store a limited number of error messages to ignore. 
    if( ignoreCount == NUMBER_OF_IGNORES )
        return;

    // Store off the information.
    strncpy( (char*)ignoreState[ ignoreCount ], (char*)state, 10 );
    ignoreNativeError[ ignoreCount ] = nativeError;
    ignoreCount++;

    return;
}

/* Function          : ShouldIgnoreMsg
   Calling Arguments : SQLCHAR* : The ODBC state. 10 byte string.
                       SQWORD   : The ODBC native error.
   Return Arguments  : true : Ignore the error message.
                       false : Do not ignore the error message.

   Description:
   This checks to see if the program should or should not ignore the error 
   message being returned from ODBC.   
 */
bool ShouldIgnoreMsg( SQLCHAR *state, SDWORD nativeError )
{
    for( int loop = 0; loop != ignoreCount; loop++ )
    {
        if( ( strcmp( (char*)ignoreState[ loop ], (char*)state ) == 0 ) &&
            ( ignoreNativeError[ loop ] == nativeError ) )
        {
            return true;
        }
    }
    return false;
}

/* Function          : ClearIgnore
   Calling Arguments : none
   Return Arguments  : none

   Description:
   This clears out the stored ignore messages.
   
 */
void ClearIgnore( void )
{
    ignoreCount = 0;
    return;
}

/* Function          : CheckMsgs
   Calling Arguments : none
   Return Arguments  : NO_ERROR_FND: No error message was found.
                       ERROR_REPORT: Error message was reported.
                       IGNORE_ERROR: Error message was ignored.

   Description:
   After running a command you can check to see if there were any messages 
   returned from ODBC. These messages can be errors, warnings, or 
   informational. We try to prevent repeating errors as this can flood 
   logs.

   The function checks before logging the error if the error message should be 
   ignored. If all the error messages should be ignored, then return a three.

   Notes: Hopefully you can see the reason to keep the handles in a 
   structured form and not in seperate variables. The ideal case (TO-DO) is
   keep the handles in a tree-like structure passing in the lowest leaf. 
   Then reverse back up the tree to the root node. This will allow clients
   the ability to manage more complex ODBC handles in the future.
 */
int CheckMsgs( char* sqlFunction, int lineNumber ) 
{
    SQLRETURN  retcode;       // Used to gather the return value of all ODBC API calls.
    SQLCHAR szSqlState[ 10 ];
    SDWORD NativeError;
    SQLCHAR szErrorMsg[ 1024 ];
    SQLCHAR SavedErrorMsg[ 1024 ];
    int errorRepetionCount = 0;
    SWORD ErrorMsg;
    SQLSMALLINT recordNumber = -1;
    int reportedErrorMsg = NO_ERROR_FND;

    strcpy( (char *)SavedErrorMsg, "EMPTY" );

    // Loop through all the handles passed in
    for( int loop = 0; loop < 5; loop++ )
    {
        // Loop through all the possible handle types the handle can be
        for( SQLSMALLINT handleType = 1; handleType != 5; handleType++ )
        {
            if( handle[ loop ] != (SQLHANDLE)NULL ) 
            {
                while( ( retcode = SQLGetDiagRec( handleType, handle[ loop ], 
                                                  recordNumber, szSqlState, &NativeError, 
                                                  szErrorMsg, (int)sizeof( szErrorMsg ), &ErrorMsg ) ) == SQL_STILL_EXECUTING );
                while( ( retcode == SQL_SUCCESS ) || ( retcode == SQL_SUCCESS_WITH_INFO ) ) 
                {
                    szErrorMsg[ 500 ] = '\0';
                    // We do not log ignored messages, unless we have already 
                    // reported an error message. 
                    if( ( !ShouldIgnoreMsg( szSqlState, NativeError ) ) || 
                        ( reportedErrorMsg == ERROR_REPORT ) )
                    {
                        if( reportedErrorMsg == NO_ERROR_FND )
                        {
                            RecordToLog( " >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n" );
                        }
                        if( strcmp( (char *)szErrorMsg, (char *)SavedErrorMsg ) != 0 )
                        {
                            RecordToLog( " >>> State: %s\n",        (char*)szSqlState );
                            RecordToLog( " >>> Native Error: %d\n", (int)NativeError );
                            RecordToLog( " >>> Message: %s\n",      (char*)szErrorMsg );
                            strncpy( (char *)SavedErrorMsg, (char *)szErrorMsg, 1023 );
                            errorRepetionCount++;
                            reportedErrorMsg = ERROR_REPORT;
                        } 
                        else
                        {
                            errorRepetionCount++;
                        }
                    }
                    else
                    {
                        // Store off that we ignored the messages. However 
                        // only if we haven't reported an error message already.
                        if( reportedErrorMsg == NO_ERROR_FND )
                        {
                            reportedErrorMsg = IGNORE_ERROR;
                        }
                    }
                    recordNumber++; // Cycle through the records.
                    while( ( retcode = SQLGetDiagRec( handleType, handle[ loop ], 
                                                      recordNumber, szSqlState, &NativeError, 
                                                      szErrorMsg, (int)sizeof( szErrorMsg ), &ErrorMsg ) ) == SQL_STILL_EXECUTING );
                    if( errorRepetionCount > 0 )
                    {
                        if( retcode != SQL_SUCCESS )
                            RecordToLog( " >>> (The above error message was repeated %d times.)\n", errorRepetionCount );
                        else if( strcmp( (char *)szErrorMsg, (char *)SavedErrorMsg ) != 0 )
                        {
                            RecordToLog( " >>> (The above error message was repeated %d times.)\n", errorRepetionCount );
                            errorRepetionCount = -1;
                        }
                    }
                }
                recordNumber = 1;
            }
        }
    }
    if( reportedErrorMsg == ERROR_REPORT )
    {
        RecordToLog( " >>> The error messages from above were from  %s located at %s on line %d\n", sqlFunction, __FILE__, lineNumber );
        RecordToLog( " >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n" );
    }
    else if( reportedErrorMsg != IGNORE_ERROR )
    {
		reportedErrorMsg = NO_ERROR_FND;
        //RecordToLog( " >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n" );
        //RecordToLog( " >>> WARNING NO MESSAGES RETRIEVED FROM ODBC DRIVER\n" );
        //RecordToLog( " >>> This was from  %s located at %s on line %d\n", sqlFunction, __FILE__, lineNumber );
        //RecordToLog( " >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n" );
        //exit(1);
    }

    return reportedErrorMsg;
}

void CheckMsgsNoIgnored() 
{
    SQLRETURN  retcode;
    SQLCHAR szSqlState[ 10 ];
    SDWORD NativeError;
    SQLCHAR szErrorMsg[ 1024 ];
    SWORD ErrorMsg;
    SQLSMALLINT recordNumber = 1;

	// Loop through all the handles passed in
    for( int loop = 0; loop < 5; loop++ )
    {
        // Loop through all the possible handle types the handle can be
        for( SQLSMALLINT handleType = 1; handleType != 5; handleType++ )
        {
            if( handle[ loop ] != (SQLHANDLE)NULL ) 
            {
                while( ( retcode = SQLGetDiagRec( handleType, handle[ loop ], 
                                                  recordNumber, szSqlState, &NativeError, 
                                                  szErrorMsg, (int)sizeof( szErrorMsg ), &ErrorMsg ) ) == SQL_STILL_EXECUTING );
                while( ( retcode == SQL_SUCCESS ) || ( retcode == SQL_SUCCESS_WITH_INFO ) ) 
                {
                    szErrorMsg[ 500 ] = '\0';
                    RecordToLog( " >>> State: %s\n",        (char*)szSqlState );
                    RecordToLog( " >>> Native Error: %d\n", (int)NativeError );
                    RecordToLog( " >>> Message: %s\n",      (char*)szErrorMsg );

                    recordNumber++;
					while( ( retcode = SQLGetDiagRec( handleType, handle[ loop ], 
                                                      recordNumber, szSqlState, &NativeError, 
                                                      szErrorMsg, (int)sizeof( szErrorMsg ), &ErrorMsg ) ) == SQL_STILL_EXECUTING );
                }
				recordNumber = 1;
            }
        }
    }
}

bool FreeHandles( )
{
    SQLRETURN retcode;

    retcode = SQLFreeStmt( handle[ SQL_HANDLE_STMT ], SQL_CLOSE ); // Free and clearup the statement handle.
    if( retcode != SQL_SUCCESS )    
    {
        CheckMsgs( "SQLFreeStmt()", __LINE__ );
        ClearIgnore( );
        DeleteHandles( );
        return false;
    }

    return true;
}

/* Function          : DeleteHandles
   Calling Arguments : void
   Return Arguments  : void

   Description: 
   Deletes all the ODBC handles.
 */

void DeleteHandles( )
{
    SQLRETURN retcode;
    if( ( tableTypes[ unitTest.tableType ] == VOLATILE ) && ( actions[ unitTest.action ] != DELETE_PARAM ) )
    {
        return;
    }
    // Free the ODBC handles.
    if( handle[ SQL_HANDLE_STMT ] != (SQLHANDLE)NULL )
        while( ( retcode = SQLFreeHandle( SQL_HANDLE_STMT, handle[ SQL_HANDLE_STMT ] ) ) == SQL_STILL_EXECUTING ); 

    if( handle[ SQL_HANDLE_DBC ] != (SQLHANDLE)NULL ) 
    {
        while( ( retcode = SQLDisconnect( handle[ SQL_HANDLE_DBC ] ) ) == SQL_STILL_EXECUTING ); 
        while( ( retcode = SQLFreeHandle( SQL_HANDLE_DBC, handle[ SQL_HANDLE_DBC ] ) ) == SQL_STILL_EXECUTING ); 
    }

    if( handle[ SQL_HANDLE_ENV ] != (SQLHANDLE)NULL )
        while( ( retcode = SQLFreeHandle( SQL_HANDLE_ENV, handle[ SQL_HANDLE_ENV ] ) ) == SQL_STILL_EXECUTING ); 

    handle[ SQL_HANDLE_ENV ]  = (SQLHANDLE)NULL;
    handle[ SQL_HANDLE_DBC ]  = (SQLHANDLE)NULL;
    handle[ SQL_HANDLE_STMT ] = (SQLHANDLE)NULL;
}

bool DeleteRows( )
{
    SQLRETURN    retcode = SQL_SUCCESS;

    RecordToLog( " >> Cleaning up table. \n" );
    while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStr[ 4 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );//Delete all rows in table

    if( retcode != SQL_SUCCESS )    
    {
        ClearIgnore( );
        DeleteHandles( );
        return false;
    }

    //ExecSQLStrAfterTrigger

    if( tableFeatures[ unitTest.tableFeature ] == AFTERTRIGGER )
        while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStrAfterTrigger[ 4 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );//Delete all rows in rowset_tmp table

    if( features[ unitTest.feature ] != HASH2 )
    {
        RecordToLog( " >> Committing transaction.\n" );
        retcode = SQLEndTran( SQL_HANDLE_DBC, handle[ SQL_HANDLE_DBC ], SQL_COMMIT ); // Commit the transaction.
        if( retcode != SQL_SUCCESS )    
        {
            CheckMsgs( "SQLEndTran()", __LINE__ );
            ClearIgnore( );
            DeleteHandles( );
            return false;
        }
    }

    retcode = SQLFreeStmt( handle[ SQL_HANDLE_STMT ], SQL_CLOSE ); // Free and clearup the statement handle.
    if( retcode != SQL_SUCCESS )    
    {
        CheckMsgs( "SQLFreeStmt()", __LINE__ );
        ClearIgnore( );
        DeleteHandles( );
        return false;
    }
    return true;
}


/* Function          : DropTable
   Calling Arguments : none
   Return Arguments  : true : table was droped.
                       false : table was not dropped.
   Description: 
   Drops the table.
 */
bool DropTable() 
{
    SQLRETURN  retcode;       // Used to gather the return value of all ODBC API calls.

    if( singleTest )
    {
        return true;
    }

    retcode = SQL_SUCCESS;

    IgnoreMsg( (SQLCHAR*)"X0104", -1004 ); // Ignore the table does not exist.
    IgnoreMsg( (SQLCHAR*)"X010V", -1031 ); // Ignore the table can not be dropped.
    IgnoreMsg( (SQLCHAR*)"X0106", -1006 ); // Ignore the index does not exist.

    if( actions[ unitTest.action ] == INSERT_SELECT )
    {
        RecordToLog( " >> Dropping select table. \n" );
        while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStr[ 15 ], SQL_NTS ) ) == SQL_STILL_EXECUTING ); 
        return true;
    }

    switch( tableFeatures[ unitTest.tableFeature ] )
    {
        case INDEX:
            RecordToLog( " >> Dropping index. \n" );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStrIndex[ 1 ], SQL_NTS ) ) == SQL_STILL_EXECUTING ); 
            break;
        case MVS:
            RecordToLog( " >> Dropping MVS table. \n" );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStrMVS[ 4 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStrMVS[ 5 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStrMVS[ 6 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            break;
        case RI:
            RecordToLog( " >> Dropping referential constraint. \n" );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStrRI[ 3 ], SQL_NTS ) ) == SQL_STILL_EXECUTING ); 
            /*if( retcode != SQL_SUCCESS )    
            {
                CheckMsgs( "SQLExecDirect()", __LINE__ );
                ClearIgnore( );
                DeleteHandles( );
                return false;
            }*/
            break;
        case BEFORETRIGGER:
            RecordToLog( " >> Droping before trigger. \n" );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStrBeforeTrigger[ 0 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            break;
        case AFTERTRIGGER:
             RecordToLog( " >> Droping after trigger. \n" );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStrAfterTrigger[ 1 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStrAfterTrigger[ 0 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            break;
        default:
            break;
    }

    switch( tableTypes[ unitTest.tableType ] )
    {
		case VOLATILE:
            RecordToLog( " >> Droping standard table. \n" );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStr[ 0 ], SQL_NTS ) ) == SQL_STILL_EXECUTING ); // Create the table.
            RecordToLog( " >> Droping volatile table. \n" );
			while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStrVolatile[ 1 ], SQL_NTS ) ) == SQL_STILL_EXECUTING ); // Create the table.
            break;
        default:
            RecordToLog( " >> Droping standard table. \n" );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStr[ 0 ], SQL_NTS ) ) == SQL_STILL_EXECUTING ); // Create the table.
            break;
    }

    if( retcode != SQL_SUCCESS && retcode != SQL_SUCCESS_WITH_INFO )    
    {
        /*if( CheckMsgs( "SQLExecDirect()", __LINE__ ) != IGNORE_ERROR )
        {
            ClearIgnore( );
            DeleteHandles( );
            return false;
        }*/
    }

    if( features[ unitTest.feature ] != HASH2 && retcode == SQL_SUCCESS)
    {
        RecordToLog( " >> Committing transaction.\n" );
        retcode = SQLEndTran( SQL_HANDLE_DBC, handle[ SQL_HANDLE_DBC ], SQL_COMMIT ); // Commit the transaction.
        if( retcode != SQL_SUCCESS )    
        {
            CheckMsgs( "SQLEndTran()", __LINE__ );
            ClearIgnore( );
            DeleteHandles( );
            return false;
        }
    }

    retcode = SQLFreeStmt( handle[ SQL_HANDLE_STMT ], SQL_CLOSE ); // Free and clearup the statement handle.
    if( retcode != SQL_SUCCESS )    
    {
        CheckMsgs( "SQLFreeStmt()", __LINE__ );
        ClearIgnore( );
        DeleteHandles( );
        return false;
    }
    return true;
}

/* Function          : ALM_TestInformation
   Calling Arguments : char *
   Return Arguments  : void

   Description: 
   Prints the up coming test information for ALM log file.
 */
void ALM_TestInformation(char * sALM_TestInfo)
{
	strcpy((char*)sALM_TestInfo,"");
	switch( tableTypes[ unitTest.tableType ] )
	{
		case REGULAR:
			strcat((char*)sALM_TestInfo,"tableType:REGULAR");
			break;
		case POSOFF:
			strcat((char*)sALM_TestInfo,"tableType:POSOFF");
			break;
		case VOLATILE:
			strcat((char*)sALM_TestInfo,"tableType:VOLATILE");
			break;
		case SURROGATE:
			strcat((char*)sALM_TestInfo,"tableType:SURROGATE");
			break;
		case SET:
			strcat((char*)sALM_TestInfo,"tableType:SET");
			break;
		case MULTISET:
			strcat((char*)sALM_TestInfo,"tableType:MULTISET");
			break;
		default:
			strcat((char*)sALM_TestInfo,"tableType:_UNKNOWN_");
			break;
	}
	
	strcat((char*)sALM_TestInfo,"+");
    switch( tableFeatures[ unitTest.tableFeature ] )
    {
        case STANDARD:
			strcat((char*)sALM_TestInfo,"tableFeature:STANDARD");
            break;
        case INDEX:
			strcat((char*)sALM_TestInfo,"tableFeature:INDEX");
            break;
        case MVS:
			strcat((char*)sALM_TestInfo,"tableFeature:MVS");
            break;
        case RI:
			strcat((char*)sALM_TestInfo,"tableFeature:RI");
            break;
        case BEFORETRIGGER:
			strcat((char*)sALM_TestInfo,"tableFeature:BEFORETRIGGER");
            break;
        case AFTERTRIGGER:
			strcat((char*)sALM_TestInfo,"tableFeature:AFTERTRIGGER");
            break;
        default:
			strcat((char*)sALM_TestInfo,"tableFeature:_UNKNOWN_");
            break;
    }

	strcat((char*)sALM_TestInfo,"+");
    switch( modes[ unitTest.mode ] )
    {
        case STANDARD:
			strcat((char*)sALM_TestInfo,"mode:STANDARD");
            break;
        default:
			strcat((char*)sALM_TestInfo,"mode:_UNKNOWN_");
            break;
    }

    if( errorChecking == MODE_SPECIAL_1 )
    {
		strcat((char*)sALM_TestInfo,"+CQD:MODE_SPECIAL_1");
    }

	strcat((char*)sALM_TestInfo,"+");
    switch( features[ unitTest.feature ] )
    {
        case STANDARD:
			strcat((char*)sALM_TestInfo,"feature:STANDARD");
            break;
        case HASH2:
			strcat((char*)sALM_TestInfo,"feature:HASH2");
            break;
        case ASYNC:
			strcat((char*)sALM_TestInfo,"feature:ASYNC");
            break;
        default:
			strcat((char*)sALM_TestInfo,"feature:_UNKNOWN_");
            break;
    }

	strcat((char*)sALM_TestInfo,"+");
    switch( operations[ unitTest.operation ] )
    {
        case PREPARE_EXECUTE:
			strcat((char*)sALM_TestInfo,"operation:PREPARE_EXECUTE");
            break;
        case EXECUTE_DIRECT:
			strcat((char*)sALM_TestInfo,"operation:EXECUTE_DIRECT");
            break;
        default:
			strcat((char*)sALM_TestInfo,"operation:_UNKNOWN_");
            break;
    }

/*
	strcat((char*)sALM_TestInfo,"+");
    switch( actions[ unitTest.action ] )
    {
        case INSERT:
			strcat((char*)sALM_TestInfo,"action:INSERT");
            break;
        case SELECT:
			strcat((char*)sALM_TestInfo,"action:SELECT");
            break;
        case UPDATE:
			strcat((char*)sALM_TestInfo,"action:UPDATE");
            break;
        case DELETE_PARAM:
			strcat((char*)sALM_TestInfo,"action:DELETE");
            break;
        case INSERT_BULK:
			strcat((char*)sALM_TestInfo,"action:INSERT_BULK");
            break;
        case INSERT_SELECT:
			strcat((char*)sALM_TestInfo,"action:INSERT_SELECT");
            break;
        default:
			strcat((char*)sALM_TestInfo,"action:_UNKNOWN_");
            break;
    }
*/

	strcat((char*)sALM_TestInfo,"+");
    switch( bindOrientations[ unitTest.bindOrientation ] )
    {
        case ROW:
			strcat((char*)sALM_TestInfo,"bindOrientation:ROW");
            break;
        case COLUMN:
			strcat((char*)sALM_TestInfo,"bindOrientation:COLUMN");
            break;
        case SINGLE:
			strcat((char*)sALM_TestInfo,"bindOrientation:SINGLE");
            break;
        default:
			strcat((char*)sALM_TestInfo,"bindOrientation:_UNKNOWN_");
            break;
    }
/*
	strcat((char*)sALM_TestInfo,"+");
    switch( injectionTypes[ unitTest.injectionType ] )
    {
        case NO_ERRORS:
			strcat((char*)sALM_TestInfo,"injectionType:NO_ERRORS");
            break;
        case DUPLICATEKEY:
			strcat((char*)sALM_TestInfo,"injectionType:DUPLICATEKEY");
            break;
        case UNIQUECONST:
			strcat((char*)sALM_TestInfo,"injectionType:UNIQUECONST");
            break;
        case SELECTIVE:
			strcat((char*)sALM_TestInfo,"injectionType:SELECTIVE");
            break;
        case NULLVALUE:
			strcat((char*)sALM_TestInfo,"injectionType:NULLVALUE");
            break;
        case DUPLICATEROW:
			strcat((char*)sALM_TestInfo,"injectionType:DUPLICATEROW");
			//if (operations[ unitTest.operation ] != PREPARE_EXECUTE)
			//	(*ALM_testCounter)--;
			//bTestCounted = false;
            break;
        case OVERFLOW:
			strcat((char*)sALM_TestInfo,"injectionType:OVERFLOW");
            break;
		case ERR_PER_ROW:
			strcat((char*)sALM_TestInfo,"injectionType:ERR_PER_ROW");
            break;
		case ERR_PER_COL:
			strcat((char*)sALM_TestInfo,"injectionType:ERR_PER_COL");
            break;
		case FULL_ERRORS:
			strcat((char*)sALM_TestInfo,"injectionType:FULL_ERRORS");
            break;
		case DRIVER_GOOD_BAD_MULCOL:
			strcat((char*)sALM_TestInfo,"injectionType:DRIVER_GOOD_BAD_MULCOL");
            break;
		case DRIVER_GOOD_WARNING_MULCOL:
			strcat((char*)sALM_TestInfo,"injectionType:DRIVER_GOOD_WARNING_MULCOL");
            break;
		case DRIVER_GOOD_BAD_WARNING_MULCOL:
			strcat((char*)sALM_TestInfo,"injectionType:DRIVER_GOOD_BAD_WARNING_MULCOL");
            break;
		case DRIVER_ALL_BAD_MULCOL:
			strcat((char*)sALM_TestInfo,"injectionType:DRIVER_ALL_BAD_MULCOL");
            break;
		case DRIVER_ALL_WARNING_MULCOL:
			strcat((char*)sALM_TestInfo,"injectionType:DRIVER_ALL_WARNING_MULCOL");
            break;
		case DRIVER_ALL_BAD_WARNING_MULCOL:
			strcat((char*)sALM_TestInfo,"injectionType:DRIVER_ALL_BAD_WARNING_MULCOL");
            break;
		case SERVER_GOOD_BAD_MULCOL:
			strcat((char*)sALM_TestInfo,"injectionType:SERVER_GOOD_BAD_MULCOL");
            break;
		case SERVER_ALL_BAD_MULCOL:
			strcat((char*)sALM_TestInfo,"injectionType:SERVER_ALL_BAD_MULCOL");
            break;
		case MIXED_DRIVERWARNING_SERVERBAD_GOOD_MULCOL:
			strcat((char*)sALM_TestInfo,"injectionType:MIXED_DRIVERWARNING_SERVERBAD_GOOD_MULCOL");
            break;
		case MIXED_DRIVERBAD_SERVERBAD_GOOD_MULCOL:
			strcat((char*)sALM_TestInfo,"injectionType:MIXED_DRIVERBAD_SERVERBAD_GOOD_MULCOL");
            break;
		case MIXED_DRIVERWARNING_DRIVERBAD_SERVERBAD_GOOD_MULCOL:
			strcat((char*)sALM_TestInfo,"injectionType:MIXED_DRIVERWARNING_DRIVERBAD_SERVERBAD_GOOD_MULCOL");
            break;
		case MIXED_DRIVERBAD_SERVERBAD_MULCOL:
			strcat((char*)sALM_TestInfo,"injectionType:MIXED_DRIVERBAD_SERVERBAD_MULCOL");
            break;
		case MIXED_DRIVERWARNING_DRIVERBAD_SERVERBAD_MULCOL:
			strcat((char*)sALM_TestInfo,"injectionType:MIXED_DRIVERWARNING_DRIVERBAD_SERVERBAD_MULCOL");
            break;
        default:
			strcat((char*)sALM_TestInfo,"injectionType:_UNKNOWN_");
            break;
    }

	strcat((char*)sALM_TestInfo,"+");
	sprintf(str, "numberOfRows=%d", numberOfRows[ unitTest.numberOfRows ]);
	strcat((char*)sALM_TestInfo,str);

	strcat((char*)sALM_TestInfo,"+");
	sprintf(str, "rowsetSize:%d", rowsetSizes[ unitTest.rowsetSize ]);
	strcat((char*)sALM_TestInfo,str);

	strcat((char*)sALM_TestInfo,"+");
	sprintf(str, "commitRate:%d", commitRates[ unitTest.commitRate ]);
	strcat((char*)sALM_TestInfo,str);
*/

	return;
}


/* Function          : PrintTestInformation
   Calling Arguments : none
   Return Arguments  : none

   Description: 
   Prints the test information.
 */
void PrintTestInformation(  )
{
    switch( tableTypes[ unitTest.tableType ] )
    {
        case REGULAR:
            RecordToLog( "  tableType[%d]: REGULAR\n", tableTypes[ unitTest.tableType ] );
            break;
        case POSOFF:
            RecordToLog( "  tableType[%d]: POSOFF\n", tableTypes[ unitTest.tableType ] );
            break;
        case VOLATILE:
            RecordToLog( "  tableType[%d]: VOLATILE\n", tableTypes[ unitTest.tableType ] );
            break;
        case SURROGATE:
            RecordToLog( "  tableType[%d]: SURROGATE\n", tableTypes[ unitTest.tableType ] );
            break;
        case SET:
            RecordToLog( "  tableType[%d]: SET\n", tableTypes[ unitTest.tableType ] );
            break;
        case MULTISET:
            RecordToLog( "  tableType[%d]: MULTISET\n", tableTypes[ unitTest.tableType ] );
            break;
        default:
            RecordToLog( "  tableType[%d]: _UNKNOWN_\n", tableTypes[ unitTest.tableType ] );
            break;
    }

    switch( tableFeatures[ unitTest.tableFeature ] )
    {
        case STANDARD:
            RecordToLog( "  tableFeature[%d]: STANDARD\n", tableFeatures[ unitTest.tableFeature ] );
            break;
        case INDEX:
            RecordToLog( "  tableFeature[%d]: INDEX\n", tableFeatures[ unitTest.tableFeature ] );
            break;
        case MVS:
            RecordToLog( "  tableFeature[%d]: MVS\n", tableFeatures[ unitTest.tableFeature ] );
            break;
        case RI:
            RecordToLog( "  tableFeature[%d]: RI\n", tableFeatures[ unitTest.tableFeature ] );
            break;
        case BEFORETRIGGER:
            RecordToLog( "  tableFeature[%d]: BEFORETRIGGER\n", tableFeatures[ unitTest.tableFeature ] );
            break;
        case AFTERTRIGGER:
            RecordToLog( "  tableFeature[%d]: AFTERTRIGGER\n", tableFeatures[ unitTest.tableFeature ] );
            break;
        default:
            RecordToLog( "  tableFeature[%d]: _UNKNOWN_\n", tableFeatures[ unitTest.tableFeature ] );
            break;
    }

    switch( modes[ unitTest.mode ] )
    {
        case STANDARD:
            RecordToLog( "  mode[%d]: STANDARD\n", modes[ unitTest.mode ] );
            break;
        default:
            RecordToLog( "  mode[%d]: _UNKNOWN_\n", modes[ unitTest.mode ] );
            break;
    }

    if( errorChecking == MODE_SPECIAL_1 )
    {
        //RecordToLog( "  CQD: MODE_SPECIAL_1 is 'ON'\n" );
    }

    switch( features[ unitTest.feature ] )
    {
        case STANDARD:
            RecordToLog( "  feature[%d]: STANDARD\n", features[ unitTest.feature ] );
            break;
        case HASH2:
            RecordToLog( "  feature[%d]: HASH2\n", features[ unitTest.feature ] );
            break;
        case ASYNC:
            RecordToLog( "  feature[%d]: ASYNC\n", features[ unitTest.feature ] );
            break;
        default:
            RecordToLog( "  feature[%d]: _UNKNOWN_\n", features[ unitTest.feature ] );
            break;
    }

    switch( operations[ unitTest.operation ] )
    {
        case PREPARE_EXECUTE:
            RecordToLog( "  operation[%d]: PREPARE_EXECUTE\n", operations[ unitTest.operation ] );
            break;
        case EXECUTE_DIRECT:
            RecordToLog( "  operation[%d]: EXECUTE_DIRECT\n", operations[ unitTest.operation ] );
            break;
        default:
            RecordToLog( "  operation[%d]: _UNKNOWN_\n", operations[ unitTest.operation ] );
            break;
    }

    switch( actions[ unitTest.action ] )
    {
        case INSERT:
            RecordToLog( "  action[%d]: INSERT\n", actions[ unitTest.action ] );
            break;
        case SELECT:
            RecordToLog( "  action[%d]: SELECT\n", actions[ unitTest.action ] );
            break;
        case UPDATE:
            RecordToLog( "  action[%d]: UPDATE\n", actions[ unitTest.action ] );
            break;
        case DELETE_PARAM:
            RecordToLog( "  action[%d]: DELETE\n", actions[ unitTest.action ] );
            break;
        case INSERT_BULK:
            RecordToLog( "  action[%d]: INSERT_BULK\n", actions[ unitTest.action ] );
            break;
        case INSERT_SELECT:
            RecordToLog( "  action[%d]: INSERT_SELECT\n", actions[ unitTest.action ] );
            break;
        default:
            RecordToLog( "  action[%d]: _UNKNOWN_\n", actions[ unitTest.action ] );
            break;
    }

    switch( bindOrientations[ unitTest.bindOrientation ] )
    {
        case ROW:
            RecordToLog( "  bindOrientation[%d]: ROW\n", bindOrientations[ unitTest.bindOrientation ] );
            break;
        case COLUMN:
            RecordToLog( "  bindOrientation[%d]: COLUMN\n", bindOrientations[ unitTest.bindOrientation ] );
            break;
        case SINGLE:
            RecordToLog( "  bindOrientation[%d]: SINGLE\n", bindOrientations[ unitTest.bindOrientation ] );
            break;
        default:
            RecordToLog( "  bindOrientation[%d]: _UNKNOWN_\n", bindOrientations[ unitTest.bindOrientation ] );
            break;
    }

    switch( injectionTypes[ unitTest.injectionType ] )
    {
        case NO_ERRORS:
            RecordToLog( "  injectionType[%d]: NO_ERRORS\n", injectionTypes[ unitTest.injectionType ] );
            break;
        case DUPLICATEKEY:
            RecordToLog( "  injectionType[%d]: DUPLICATEKEY\n", injectionTypes[ unitTest.injectionType ] );
            break;
        case UNIQUECONST:
            RecordToLog( "  injectionType[%d]: UNIQUECONST\n", injectionTypes[ unitTest.injectionType ] );
            break;
        case SELECTIVE:
            RecordToLog( "  injectionType[%d]: SELECTIVE\n", injectionTypes[ unitTest.injectionType ] );
            break;
        case NULLVALUE:
            RecordToLog( "  injectionType[%d]: NULLVALUE\n", injectionTypes[ unitTest.injectionType ] );
            break;
        case DUPLICATEROW:
            RecordToLog( "  injectionType[%d]: DUPLICATEROW\n", injectionTypes[ unitTest.injectionType ] );
            break;
        case OVERFLOW:
            RecordToLog( "  injectionType[%d]: OVERFLOW\n", injectionTypes[ unitTest.injectionType ] );
            break;
		case ERR_PER_ROW:
            RecordToLog( "  injectionType[%d]: ERR_PER_ROW\n", injectionTypes[ unitTest.injectionType ] );
            break;
		case ERR_PER_COL:
            RecordToLog( "  injectionType[%d]: ERR_PER_COL\n", injectionTypes[ unitTest.injectionType ] );
            break;
		case FULL_ERRORS:
            RecordToLog( "  injectionType[%d]: FULL_ERRORS\n", injectionTypes[ unitTest.injectionType ] );
            break;
		case DRIVER_GOOD_BAD_MULCOL:
            RecordToLog( "  injectionType[%d]: DRIVER_GOOD_BAD_MULCOL - Some good rows, some errors, no warning, multiple columns\n", injectionTypes[ unitTest.injectionType ] );
            break;
		case DRIVER_GOOD_WARNING_MULCOL:
            RecordToLog( "  injectionType[%d]: DRIVER_GOOD_WARNING_MULCOL - Some good rows, no error, some warnings, multiple columns\n", injectionTypes[ unitTest.injectionType ] );
            break;
		case DRIVER_GOOD_BAD_WARNING_MULCOL:
            RecordToLog( "  injectionType[%d]: DRIVER_GOOD_BAD_WARNING_MULCOL - Some good rows, some errors, some warnings, multiple columns\n", injectionTypes[ unitTest.injectionType ] );
            break;
		case DRIVER_ALL_BAD_MULCOL:
            RecordToLog( "  injectionType[%d]: DRIVER_ALL_BAD_MULCOL - No good row, all errors, no warning, multiple columns\n", injectionTypes[ unitTest.injectionType ] );
            break;
		case DRIVER_ALL_WARNING_MULCOL:
            RecordToLog( "  injectionType[%d]: DRIVER_ALL_WARNING_MULCOL - No good row, no error, all warnings, multiple columns\n", injectionTypes[ unitTest.injectionType ] );
            break;
		case DRIVER_ALL_BAD_WARNING_MULCOL:
            RecordToLog( "  injectionType[%d]: DRIVER_ALL_BAD_WARNING_MULCOL - No good row, half errors and half warnings, multiple columns\n", injectionTypes[ unitTest.injectionType ] );
            break;
		case SERVER_GOOD_BAD_MULCOL:
            RecordToLog( "  injectionType[%d]: SERVER_GOOD_BAD_MULCOL - Some good rows, some bad rows, multiple columns (server error only with/without driver warning)\n", injectionTypes[ unitTest.injectionType ] );
            break;
		case SERVER_ALL_BAD_MULCOL:
            RecordToLog( "  injectionType[%d]: SERVER_ALL_BAD_MULCOL - No good row, all errors, multiple columns (server error only with/without driver warning)\n", injectionTypes[ unitTest.injectionType ] );
            break;
		case MIXED_DRIVERWARNING_SERVERBAD_GOOD_MULCOL:
            RecordToLog( "  injectionType[%d]: MIXED_DRIVERWARNING_SERVERBAD_GOOD_MULCOL - Some good rows, some driver warnings, some server errors, multiple columns\n", injectionTypes[ unitTest.injectionType ] );
            break;
		case MIXED_DRIVERBAD_SERVERBAD_GOOD_MULCOL:
            RecordToLog( "  injectionType[%d]: MIXED_DRIVERBAD_SERVERBAD_GOOD_MULCOL - Some good rows, some driver errors, some server errors, multiple columns\n", injectionTypes[ unitTest.injectionType ] );
            break;
		case MIXED_DRIVERWARNING_DRIVERBAD_SERVERBAD_GOOD_MULCOL:
            RecordToLog( "  injectionType[%d]: MIXED_DRIVERWARNING_DRIVERBAD_SERVERBAD_GOOD_MULCOL - Some good rows, some driver errors, some driver warnings, some server errors, multiple columns\n", injectionTypes[ unitTest.injectionType ] );
            break;
		case MIXED_DRIVERBAD_SERVERBAD_MULCOL:
            RecordToLog( "  injectionType[%d]: MIXED_DRIVERBAD_SERVERBAD_MULCOL - Driver errrors, server errors, no warning, no good row, multiple columns\n", injectionTypes[ unitTest.injectionType ] );
            break;
		case MIXED_DRIVERWARNING_DRIVERBAD_SERVERBAD_MULCOL:
            RecordToLog( "  injectionType[%d]: MIXED_DRIVERWARNING_DRIVERBAD_SERVERBAD_MULCOL - Driver errrors, driver warnings, server errors, no good row, multiple columns\n", injectionTypes[ unitTest.injectionType ] );
            break;
        default:
            RecordToLog( "  injectionType[%d]: _UNKNOWN_\n", injectionTypes[ unitTest.injectionType ] );
            break;
    }
    RecordToLog( "  numberOfRows: %d\n", numberOfRows[ unitTest.numberOfRows ] );
    RecordToLog( "  rowsetSize: %d\n", rowsetSizes[ unitTest.rowsetSize ] );
    RecordToLog( "  commitRate: %d\n", commitRates[ unitTest.commitRate ] );
}
    
/* Function          : BindParameters
   Calling Arguments : none
   Return Arguments  : true : Bound parameters 
                       false : error

   Description: 
   Binds the C variables to the SQL data types inside the table.
 */
bool BindParameters(  )
{
    SQLRETURN  retcode;       // Used to gather the return value of all ODBC API calls.

    RecordToLog( " >> Freeing the statement bind parameter buffers.\n" );
    retcode= SQLFreeStmt( handle[ SQL_HANDLE_STMT ], SQL_RESET_PARAMS );
    if( retcode != SQL_SUCCESS )    
    {    
        RecordToLog( " >> SQLFreeStmt() with SQL_RESET_PARAMS attribute failed.\n" );
        CheckMsgs( "SQLFreeStmt()", __LINE__ );
    }
    
    // Allocate the space needed for the rowsets.
	AllocateRowsets( bindOrientations[ unitTest.bindOrientation ], rowsetSizes[unitTest.rowsetSize] );

	switch( bindOrientations[ unitTest.bindOrientation ] )
    {
        // Set the SQL_ATTR_PARAM_BIND_TYPE statement attribute to use row-wise binding.
        case ROW:
        case SINGLE:
            retcode = SQLSetStmtAttr( handle[ SQL_HANDLE_STMT ], SQL_ATTR_PARAM_BIND_TYPE, (void *)sizeof( table_rowset ), 0 );
            if( retcode != SQL_SUCCESS )    
            {
                RecordToLog( " >> SQLSetStmtAttr() with SQL_ATTR_PARAM_BIND_TYPE attribute failed.\n" );
                CheckMsgs( "SQLSetStmtAttr()", __LINE__ );
                FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
                return false;
            }
            break;
        // Set the SQL_ATTR_PARAM_BIND_TYPE statement attribute to use column-wise binding.
        case COLUMN:
        default:
            retcode = SQLSetStmtAttr( handle[ SQL_HANDLE_STMT ], SQL_ATTR_PARAM_BIND_TYPE, SQL_PARAM_BIND_BY_COLUMN, 0 );
            if( retcode != SQL_SUCCESS )    
            {    
                RecordToLog( " >> SQLSetStmtAttr() with SQL_ATTR_PARAM_BIND_TYPE attribute failed.\n" );
                CheckMsgs( "SQLSetStmtAttr()", __LINE__ );
                FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
                return false;
            }
            break;
    }
    
    // Specify the number of elements in each parameter array.
    retcode = SQLSetStmtAttr( handle[ SQL_HANDLE_STMT ], SQL_ATTR_PARAMSET_SIZE, (void *)rowsetSizes[ unitTest.rowsetSize ], 0 );
    if( retcode != SQL_SUCCESS )    
    {
        RecordToLog( " >> SQLSetStmtAttr() with SQL_ATTR_PARAMSET_SIZE attribute failed.\n" );
        CheckMsgs( "SQLSetStmtAttr()", __LINE__ );
        FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
        return false;
    }

    // Specify an array in which to return the status of each set of parameters.
    retcode = SQLSetStmtAttr( handle[ SQL_HANDLE_STMT ], SQL_ATTR_PARAM_STATUS_PTR, rowsetStatusArray, 0 );
    if( retcode != SQL_SUCCESS )    
    {
        RecordToLog( " >> SQLSetStmtAttr() with SQL_ATTR_PARAM_STATUS_PTR attribute failed.\n" );
        CheckMsgs( "SQLSetStmtAttr()", __LINE__ );
        FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
        return false;
    }
    
    // Specify an array showing which rows to process.
    retcode = SQLSetStmtAttr( handle[ SQL_HANDLE_STMT ], SQL_ATTR_PARAM_OPERATION_PTR, rowsetOperationArray, 0 );
    if( retcode != SQL_SUCCESS )    
    {
        RecordToLog( " >> SQLSetStmtAttr() with SQL_ATTR_PARAM_OPERATION_PTR attribute failed.\n" );
        CheckMsgs( "SQLSetStmtAttr()", __LINE__ );
        FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
        return false;
    }

    // Specify an SQLUINTEGER value in which to return the number of sets of parameters processed.
    retcode = SQLSetStmtAttr( handle[ SQL_HANDLE_STMT ], SQL_ATTR_PARAMS_PROCESSED_PTR, &rowsProcessed, 0 );
    if( retcode != SQL_SUCCESS )    
    {
        RecordToLog( " >> SQLSetStmtAttr() with SQL_ATTR_PARAMS_PROCESSED_PTR attribute failed.\n" );
        CheckMsgs( "SQLSetStmtAttr()", __LINE__ );
        FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
        return false;
    }

	BindParametersA( bindOrientations[ unitTest.bindOrientation ], actions[ unitTest.action ], injectionTypes[ unitTest.injectionType ] );

    // See if we want to run the rowsets through prepare or execute directly.
    if( operations[ unitTest.operation ] == PREPARE_EXECUTE )
    {
        // Preparing the action/DML statement we are to execute against the rowsets.
        switch( actions[ unitTest.action ] )
        {
            case INSERT:
                // The HASH2 feature requires this statement to be prepared before the insert statement.
                if( features[ unitTest.feature ] == HASH2 )
                {
                    char sqlDrvInsert[] = "PLANLOADTABLE ROWSET_TABLE";
                    while( ( retcode = SQLPrepare( handle[ SQL_HANDLE_STMT ], (SQLCHAR *) sqlDrvInsert, SQL_NTS ) ) == SQL_STILL_EXECUTING );
                }
                while( ( retcode = SQLPrepare( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStr[ 2 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
                break;
            case DELETE_PARAM:
                while( ( retcode = SQLPrepare( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStr[ 6 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
                break;
            case UPDATE:
				while( ( retcode = SQLPrepare( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStr[ 7 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
                break;
            case INSERT_SELECT:
                while( ( retcode = SQLPrepare( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStr[ 14 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
                break;
            default:
                RecordToLog( " >> INTERNAL ERROR: An unknown table action has been discovered.\n" );
                FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
                return false;
        }
    
        if( retcode != SQL_SUCCESS )    
        {
            if( retcode != SQL_SUCCESS_WITH_INFO )
            {
                CheckMsgs( "SQLPrepare()", __LINE__ );
                FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
                return false;
            }
        }
    }

    return true;
}

/* Function          : AssignRow
   Calling Arguments : int : The test matrix test we are running.
                     : int : Rowset position to insert the values.
                     : int : Column1 value.
                     : int : Column2 value.
   Return Arguments  : none.
   
   Description: 
   This is a support function of RowsetDML(). This inserts the values into
   rowset rows. This helps tighten up the code some by not having to insert 
   many of the same switch statements.
*/

void AssignRow( int rowsetPos, int column1Value, int column2Value )
{
	int size=SQL_NTS;

    switch( bindOrientations[ unitTest.bindOrientation ] )
    {
        case ROW:
        case SINGLE:
//#ifdef WIN32
            sprintf( (char*)rowset[ rowsetPos ].dt_char_iso, "%d", column1Value );
			sprintf( (char*)rowset[ rowsetPos ].dt_char_ucs, "%d", column1Value );
            sprintf( (char*)rowset[ rowsetPos ].dt_varchar_iso, "%d", column1Value );
            sprintf( (char*)rowset[ rowsetPos ].dt_varchar_ucs, "%d", column1Value );
            sprintf( (char*)rowset[ rowsetPos ].dt_longvarchar_iso, "%d", column1Value );
            sprintf( (char*)rowset[ rowsetPos ].dt_longvarchar_ucs, "%d", column1Value );            
            sprintf( (char*)rowset[ rowsetPos ].dt_nchar, "%d", column1Value );
            sprintf( (char*)rowset[ rowsetPos ].dt_ncharvarying, "%d", column1Value );
//#else
//            sprintf( (char*)rowset[ rowsetPos ].dt_char_iso, "%d", column1Value );
//
//			size = int_to_ucs2( column1Value, (char*)rowset[ rowsetPos ].dt_char_ucs);
//			rowset[ rowsetPos ].ptr_char_ucs = size;
//
//			sprintf( (char*)rowset[ rowsetPos ].dt_varchar_iso, "%d", column1Value );
//
//			size = int_to_ucs2( column1Value, (char*)rowset[ rowsetPos ].dt_varchar_ucs);
//			rowset[ rowsetPos ].ptr_varchar_ucs = size;
//
//			sprintf( (char*)rowset[ rowsetPos ].dt_longvarchar_iso, "%d", column1Value );
//
//			size = int_to_ucs2( column1Value, (char*)rowset[ rowsetPos ].dt_longvarchar_ucs);
//			rowset[ rowsetPos ].ptr_longvarchar_ucs = size;
//
//			size = int_to_ucs2( column1Value, (char*)rowset[ rowsetPos ].dt_nchar);
//			rowset[ rowsetPos ].ptr_nchar = size;
//
//			size = int_to_ucs2( column1Value, (char*)rowset[ rowsetPos ].dt_ncharvarying);
//			rowset[ rowsetPos ].ptr_ncharvarying = size;
//#endif
            sprintf( (char*)rowset[ rowsetPos ].dt_decimal_s, "%d", 1 );
            sprintf( (char*)rowset[ rowsetPos ].dt_decimal_u, "%d", column2Value );
            sprintf( (char*)rowset[ rowsetPos ].dt_numeric_s, "%d", 1 );
            sprintf( (char*)rowset[ rowsetPos ].dt_numeric_u, "%d", 1 );
            sprintf( (char*)rowset[ rowsetPos ].dt_tinyint_s, "%d", 1 );
            sprintf( (char*)rowset[ rowsetPos ].dt_tinyint_u, "%d", 1 );
            sprintf( (char*)rowset[ rowsetPos ].dt_smallinteger_s, "%d", 1 );
            sprintf( (char*)rowset[ rowsetPos ].dt_smallinteger_u, "%d", 1 );
            sprintf( (char*)rowset[ rowsetPos ].dt_integer_s, "%d", column2Value );
            sprintf( (char*)rowset[ rowsetPos ].dt_integer_u, "%d", column1Value );            
            sprintf( (char*)rowset[ rowsetPos ].dt_largeint, "%d", column1Value );
            sprintf( (char*)rowset[ rowsetPos ].dt_real, "%d", column1Value );
            sprintf( (char*)rowset[ rowsetPos ].dt_float, "%d", column1Value );
            sprintf( (char*)rowset[ rowsetPos ].dt_double_precision, "%d", column1Value );
            rowset[ rowsetPos ].dt_date.year  = 2000;
            rowset[ rowsetPos ].dt_date.month = 1;
            rowset[ rowsetPos ].dt_date.day   = 2;
            rowset[ rowsetPos ].dt_time.hour   = 3;
            rowset[ rowsetPos ].dt_time.minute = 4;
            rowset[ rowsetPos ].dt_time.second = 5;
            rowset[ rowsetPos ].dt_timestamp.year     = 2000;
            rowset[ rowsetPos ].dt_timestamp.month    = 1;
            rowset[ rowsetPos ].dt_timestamp.day      = 2;
            rowset[ rowsetPos ].dt_timestamp.hour     = 3;
            rowset[ rowsetPos ].dt_timestamp.minute   = 4;
            rowset[ rowsetPos ].dt_timestamp.second   = 5;
            rowset[ rowsetPos ].dt_timestamp.fraction = 600000;
            rowset[ rowsetPos ].dt_interval_year.intval.year_month.year       = 0;
            rowset[ rowsetPos ].dt_interval_month.intval.year_month.month     = 1;
            rowset[ rowsetPos ].dt_interval_day.intval.day_second.day         = 2;
            rowset[ rowsetPos ].dt_interval_hour.intval.day_second.hour       = 3;
            rowset[ rowsetPos ].dt_interval_minute.intval.day_second.minute   = 4;
            rowset[ rowsetPos ].dt_interval_second.intval.day_second.second   = 5;
            rowset[ rowsetPos ].dt_interval_second.intval.day_second.fraction = 6;
            rowset[ rowsetPos ].dt_interval_year_to_month.intval.year_month.year  = 0;
            rowset[ rowsetPos ].dt_interval_year_to_month.intval.year_month.month = 1;
            rowset[ rowsetPos ].dt_interval_day_to_hour.intval.day_second.day  = 2;
            rowset[ rowsetPos ].dt_interval_day_to_hour.intval.day_second.hour = 3;
            rowset[ rowsetPos ].dt_interval_day_to_minute.intval.day_second.day    = 2;
            rowset[ rowsetPos ].dt_interval_day_to_minute.intval.day_second.hour   = 3;
            rowset[ rowsetPos ].dt_interval_day_to_minute.intval.day_second.minute = 4;
            rowset[ rowsetPos ].dt_interval_day_to_second.intval.day_second.day      = 2;
            rowset[ rowsetPos ].dt_interval_day_to_second.intval.day_second.hour     = 3;
            rowset[ rowsetPos ].dt_interval_day_to_second.intval.day_second.minute   = 4;
            rowset[ rowsetPos ].dt_interval_day_to_second.intval.day_second.second   = 5;
            rowset[ rowsetPos ].dt_interval_day_to_second.intval.day_second.fraction = 6;
            rowset[ rowsetPos ].dt_interval_hour_to_minute.intval.day_second.hour   = 3;
            rowset[ rowsetPos ].dt_interval_hour_to_minute.intval.day_second.minute = 4;
            rowset[ rowsetPos ].dt_interval_hour_to_second.intval.day_second.hour     = 3;
            rowset[ rowsetPos ].dt_interval_hour_to_second.intval.day_second.minute   = 4;
            rowset[ rowsetPos ].dt_interval_hour_to_second.intval.day_second.second   = 5;
            rowset[ rowsetPos ].dt_interval_hour_to_second.intval.day_second.fraction = 6;
            rowset[ rowsetPos ].dt_interval_minute_to_second.intval.day_second.minute   = 4;
            rowset[ rowsetPos ].dt_interval_minute_to_second.intval.day_second.second   = 5;
            rowset[ rowsetPos ].dt_interval_minute_to_second.intval.day_second.fraction = 6;
            sprintf( (char*)rowset[ rowsetPos ].dt_bignum_s, "%s", "1234567890123456789" );
            sprintf( (char*)rowset[ rowsetPos ].dt_bignum_u, "%s", "1234567890123456789" );
            break;
        case COLUMN:
//#ifdef WIN32
            sprintf( (char*)&dt_char_iso[ rowsetPos * STRINGMAX ], "%d", column1Value );
            sprintf( (char*)&dt_char_ucs[ rowsetPos * STRINGMAXDBL  ], "%d", column1Value );
            sprintf( (char*)&dt_varchar_iso[ rowsetPos * STRINGMAX  ], "%d", column1Value );
            sprintf( (char*)&dt_varchar_ucs[ rowsetPos * STRINGMAXDBL  ], "%d", column1Value );
            sprintf( (char*)&dt_longvarchar_iso[ rowsetPos * STRINGMAX  ], "%d", column1Value );
            sprintf( (char*)&dt_longvarchar_ucs[ rowsetPos * STRINGMAXDBL  ], "%d", column1Value );            
            sprintf( (char*)&dt_nchar[ rowsetPos * STRINGMAXDBL  ], "%d", column1Value );
            sprintf( (char*)&dt_ncharvarying[ rowsetPos * STRINGMAXDBL  ], "%d", column1Value );
//#else
//            sprintf( (char*)&dt_char_iso[ rowsetPos * STRINGMAX ], "%d", column1Value );
//
//            size = int_to_ucs2( column1Value, (char*)&dt_char_ucs[ rowsetPos * STRINGMAXDBL  ]);
//            ptr_char_ucs[rowsetPos] = size;
//
//            sprintf( (char*)&dt_varchar_iso[ rowsetPos * STRINGMAX  ], "%d", column1Value );
//
//            size = int_to_ucs2( column1Value, (char*)&dt_varchar_ucs[ rowsetPos * STRINGMAXDBL  ]);
//            ptr_varchar_ucs[ rowsetPos ] = size;
//
//            sprintf( (char*)&dt_longvarchar_iso[ rowsetPos * STRINGMAX  ], "%d", column1Value );
//
//            size = int_to_ucs2( column1Value, (char*)&dt_longvarchar_ucs[ rowsetPos * STRINGMAXDBL  ]);
//            ptr_longvarchar_ucs[ rowsetPos ] = size;
//
//            size = int_to_ucs2( column1Value, (char*)&dt_nchar[ rowsetPos * STRINGMAXDBL  ]);
//            ptr_nchar[ rowsetPos ] = size;
//
//            size = int_to_ucs2( column1Value, (char*)&dt_ncharvarying[ rowsetPos * STRINGMAXDBL  ]);
//            ptr_ncharvarying[ rowsetPos ] = size;
//#endif
            sprintf( (char*)&dt_decimal_s[ rowsetPos * STRINGMAX  ], "%d", 1 );
            sprintf( (char*)&dt_decimal_u[ rowsetPos * STRINGMAX  ], "%d", column2Value );
            sprintf( (char*)&dt_numeric_s[ rowsetPos * STRINGMAX  ], "%d", 1 );
            sprintf( (char*)&dt_numeric_u[ rowsetPos * STRINGMAX  ], "%d", 1 );
            sprintf( (char*)&dt_tinyint_s[ rowsetPos * STRINGMAX  ], "%d", 1 );
            sprintf( (char*)&dt_tinyint_u[ rowsetPos * STRINGMAX  ], "%d", 1 );
            sprintf( (char*)&dt_smallinteger_s[ rowsetPos * STRINGMAX  ], "%d", 1 );
            sprintf( (char*)&dt_smallinteger_u[ rowsetPos * STRINGMAX  ], "%d", 1 );
            sprintf( (char*)&dt_integer_s[ rowsetPos * STRINGMAX  ], "%d", column2Value );
            sprintf( (char*)&dt_integer_u[ rowsetPos * STRINGMAX  ], "%d", column1Value );
            sprintf( (char*)&dt_largeint[ rowsetPos * STRINGMAX  ], "%d", column1Value );
            sprintf( (char*)&dt_real[ rowsetPos * STRINGMAX  ], "%d", column1Value );
            sprintf( (char*)&dt_float[ rowsetPos * STRINGMAX  ], "%d", column1Value );
            sprintf( (char*)&dt_double_precision[ rowsetPos * STRINGMAX  ], "%d", column1Value );
            dt_date[ rowsetPos ].year  = 2000;
            dt_date[ rowsetPos ].month = 1;
            dt_date[ rowsetPos ].day   = 2;
            dt_time[ rowsetPos ].hour   = 3;
            dt_time[ rowsetPos ].minute = 4;
            dt_time[ rowsetPos ].second = 5;
            dt_timestamp[ rowsetPos ].year     = 2000;
            dt_timestamp[ rowsetPos ].month    = 1;
            dt_timestamp[ rowsetPos ].day      = 2;
            dt_timestamp[ rowsetPos ].hour     = 3;
            dt_timestamp[ rowsetPos ].minute   = 4;
            dt_timestamp[ rowsetPos ].second   = 5;
            dt_timestamp[ rowsetPos ].fraction = 600000;
            dt_interval_year[ rowsetPos ].intval.year_month.year       = 0;
            dt_interval_month[ rowsetPos ].intval.year_month.month     = 1;
            dt_interval_day[ rowsetPos ].intval.day_second.day         = 2;
            dt_interval_hour[ rowsetPos ].intval.day_second.hour       = 3;
            dt_interval_minute[ rowsetPos ].intval.day_second.minute   = 4;
            dt_interval_second[ rowsetPos ].intval.day_second.second   = 5;
            dt_interval_second[ rowsetPos ].intval.day_second.fraction = 6;
            dt_interval_year_to_month[ rowsetPos ].intval.year_month.year  = 0;
            dt_interval_year_to_month[ rowsetPos ].intval.year_month.month = 1;
            dt_interval_day_to_hour[ rowsetPos ].intval.day_second.day  = 2;
            dt_interval_day_to_hour[ rowsetPos ].intval.day_second.hour = 3;
            dt_interval_day_to_minute[ rowsetPos ].intval.day_second.day    = 2;
            dt_interval_day_to_minute[ rowsetPos ].intval.day_second.hour   = 3;
            dt_interval_day_to_minute[ rowsetPos ].intval.day_second.minute = 4;
            dt_interval_day_to_second[ rowsetPos ].intval.day_second.day      = 2;
            dt_interval_day_to_second[ rowsetPos ].intval.day_second.hour     = 3;
            dt_interval_day_to_second[ rowsetPos ].intval.day_second.minute   = 4;
            dt_interval_day_to_second[ rowsetPos ].intval.day_second.second   = 5;
            dt_interval_day_to_second[ rowsetPos ].intval.day_second.fraction = 6;
            dt_interval_hour_to_minute[ rowsetPos ].intval.day_second.hour   = 3;
            dt_interval_hour_to_minute[ rowsetPos ].intval.day_second.minute = 4;
            dt_interval_hour_to_second[ rowsetPos ].intval.day_second.hour     = 3;
            dt_interval_hour_to_second[ rowsetPos ].intval.day_second.minute   = 4;
            dt_interval_hour_to_second[ rowsetPos ].intval.day_second.second   = 5;
            dt_interval_hour_to_second[ rowsetPos ].intval.day_second.fraction = 6;
            dt_interval_minute_to_second[ rowsetPos ].intval.day_second.minute   = 4;
            dt_interval_minute_to_second[ rowsetPos ].intval.day_second.second   = 5;
            dt_interval_minute_to_second[ rowsetPos ].intval.day_second.fraction = 6;
            sprintf( (char*)&dt_bignum_s[ rowsetPos * STRINGMAX  ], "%s", "1234567890123456789" );
            sprintf( (char*)&dt_bignum_u[ rowsetPos * STRINGMAX  ], "%s", "1234567890123456789" );
            break;
    }
    return;
}

/* Function          : RowsetDMLBulk
   Calling Arguments : int : The test matrix test we are running.
                       int : What rows to inject errors into.
   Return Arguments  : bool : True = pass False = fail

   Description: 
   
 */
bool RowsetDMLBulk( )
{
    SQLRETURN  retcode;       // Used to gather the return value of all ODBC API calls.
    int        numIterations = 0;
    int        numberOfRowsHandled= 0;
    SQLLEN     rowCount;
    int        rs;
    bool       rc = true;
    int        failureInjectionCount;
    time_t     startTime;
    
    while( ( retcode = SQLExecute( handle[ SQL_HANDLE_STMT ] ) ) == SQL_STILL_EXECUTING );
    if( retcode != SQL_SUCCESS )
    {
        RecordToLog( "    Failing API: SQLBulkOperations()\n" );
        CheckMsgs( "SQLBulkOperations()", __LINE__ );
        FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
        return false;
    }

    // Insert the number of rows requested.
    for (numberOfRowsHandled= 0;numberOfRowsHandled< numberOfRows[ unitTest.numberOfRows ]; )
    {
        failureInjectionCount = 0; // The number of failures we inject into a rowset.
        // Assign the values in the rowset
        for( rs = 0; rs < rowsetSizes[ unitTest.rowsetSize ]; rs++ )
        {
            switch( injectionTypes[ unitTest.injectionType ] )
            {
                case NO_ERRORS:
                case NULLVALUE:
                    AssignRow( rs, numberOfRowsHandled + 1, numberOfRowsHandled + 1 );
                    break;
                case DUPLICATEKEY:
                    if( ( rs % 5 ) == 0 )
                    {
                        // Inject an error.
                        switch( actions[ unitTest.action] )
                        {
                            case UPDATE:
                                AssignRow( rs, numberOfRowsHandled, numberOfRowsHandled + 1 );
                                break;
                            default:
                                AssignRow( rs, 1, numberOfRowsHandled );
                                break;
                        }
                        failureInjectionCount++;
                    }
                    else
                    {
                        // Do not inject an error.
                        AssignRow( rs, numberOfRowsHandled + 1, numberOfRowsHandled + 1 );
                    }
                    break;
                case UNIQUECONST:
                    if( ( rs % 5 ) == 0 )
                    {
                        // Inject an error.
                        switch( actions[ unitTest.action] )
                        {
                            case UPDATE:
                                AssignRow( rs, numberOfRowsHandled + 50001, numberOfRowsHandled + 1 );
                                break;
                            default:
                                AssignRow( rs, numberOfRowsHandled + 1, numberOfRowsHandled + 50001 );
                                break;
                        }
                        failureInjectionCount++;
                    }
                    else
                    {
                        // Do not inject an error.
                        AssignRow(  rs,numberOfRowsHandled+ 1,numberOfRowsHandled+ 1 );
                    }
                    break;
                case SELECTIVE:
                    if( ( rs % 5 ) == 0 )
                    {
                        // We exclude this row selectively to not be processed.
                        rowsetOperationArray[ rs ] = SQL_PARAM_IGNORE;
                        failureInjectionCount++;
                    } 
                    else
                    {
                        // We make sure we reset the good rows to become processed. 
                        rowsetOperationArray[ rs ] = SQL_PARAM_PROCEED;
                    }
                    AssignRow(  rs,numberOfRowsHandled+ 1,numberOfRowsHandled+ 1 );
                    break;
                default:
                    RecordToLog( "INTERNAL ERROR: An unknown failure type has been discovered.\n" );
                    rc = false;
                    break;
            }

            numberOfRowsHandled++;
            if( numberOfRowsHandled >= numberOfRows[ unitTest.numberOfRows ] )
            {
                // Readjust the number of elements in each parameter array.
                rs++;
                retcode = SQLSetStmtAttr( handle[ SQL_HANDLE_STMT ], SQL_ATTR_PARAMSET_SIZE, (void *)rs, 0 );
                if( retcode != SQL_SUCCESS )    
                {
                    CheckMsgs( "SQLSetStmtAttr()", __LINE__ );
                    FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
                    return false;
                }
                break;
            }
        }

        // Insert the rows.
        time( &startTime );
        while( ( retcode = SQLBulkOperations( handle[ SQL_HANDLE_STMT ], SQL_ADD ) ) == SQL_STILL_EXECUTING );
//        testMatrix[ testMatrixPos ].runningTime += difftime( time( NULL ), startTime );
        if( retcode != SQL_SUCCESS )
        {
            RecordToLog( "    Failing API: SQLBulkOperations()\n" );
            CheckMsgs( "SQLBulkOperations()", __LINE__ );
            FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
            return false;
        }

        // See if we need to commit the tracaction.
        if( commitRates[ unitTest.commitRate ] == numIterations  &&
            features[ unitTest.feature ] != HASH2 ) // Commit the rows at the set commit rate.
        {
            retcode = SQLEndTran( SQL_HANDLE_DBC, handle[ SQL_HANDLE_DBC ], SQL_COMMIT );
            if( retcode != SQL_SUCCESS )    
            {
                RecordToLog( "    Failing API: SQLEndTran()\n" );
                CheckMsgs( "SQLEndTran()", __LINE__ );
                FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
                return false;
            }
            numIterations = 0;
        }

        // Check to make sure all the rows we inserted were processed.
        if ( (int)rowsProcessed != rs ) {
            RecordToLog(" >> ERROR: The number of parameters processed does not match the number of rows prepared.\n");
            RecordToLog(" >> ERROR: Rows processed by ODBC: %d Rows prepared by client: %d at line %d\n", (int)rowsProcessed, rs, __LINE__ );
            rc = false;
        }

        // Check to make sure all the rows in the rowset status array map correctly to the errorMatrix.
        for( int rowPos = 0; rowPos < (int)rowsProcessed; rowPos++ )
        {
            if( ( ( injectionTypes[ unitTest.injectionType ] == NO_ERRORS ) || 
                  ( injectionTypes[ unitTest.injectionType ] == NULLVALUE ) ||
                  ( ( rowPos % 5 ) != 0 ) ) 
               || ( modes[ unitTest.mode ] == MODE_SPECIAL_1 ) )
            {
                switch( rowsetStatusArray[ rowPos ] )
                {
                    case SQL_PARAM_SUCCESS:
                        break;
                    default:
                        RecordToLog(" >> ERROR: Rowset status array row %d was expected to have SQL_PARAM_SUCCESS. Actual: %s at line %d.\n", rowPos, Param_Status_Ptr( rowsetStatusArray[ rowPos ] ), __LINE__ );
                        rc = false;
                        break;
                }
            } 
            else if ( injectionTypes[ unitTest.injectionType ] != SELECTIVE )
            {
                switch( rowsetStatusArray[ rowPos ] )
                {
                    case SQL_PARAM_ERROR:
                        break;
                    default:
                        RecordToLog(" >> ERROR: Rowset status array row %d was expected to have SQL_PARAM_ERROR. Actual: %s at line %d.\n", rowPos, Param_Status_Ptr( rowsetStatusArray[ rowPos ] ), __LINE__ );
                        rc = false;
                        break;
                }
            }
            else /* SELECTIVE test */
            {
                switch( rowsetStatusArray[ rowPos ] )
                {
                    case SQL_PARAM_UNUSED:
                        break;
                    default:
                        RecordToLog(" >> ERROR: Rowset status array row %d was expected to have SQL_PARAM_UNUSED. Actual: %s at line %d.\n", rowPos, Param_Status_Ptr( rowsetStatusArray[ rowPos ] ), __LINE__ );
                        rc = false;
                        break;
                }
            }
        }

        // Check to make sure the row count of affected rows is correct.
        retcode = SQLRowCount( handle[ SQL_HANDLE_STMT ], &rowCount );
        if( retcode != SQL_SUCCESS )    
        {
            RecordToLog( "    Failing API: SQLRowCount()\n" );
            CheckMsgs( "SQLRowCount()", __LINE__ );
            FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
            //return false;
        }

        if( ( errorChecking == MODE_SPECIAL_1 ) && ( (int)rowCount != ( rowsProcessed ) ) )
        {
            RecordToLog( " >> ERROR: The number of good rows processed [%d] does not match the SQLRowCount() [%d] at line %d.\n", rowsProcessed, rowCount, __LINE__);
            rc = false;
        }
        if( ( errorChecking == STANDARD ) && ( (int)rowCount != ( rowsProcessed - failureInjectionCount ) ) )
        {
            RecordToLog( " >> ERROR: The number of good rows processed [%d] does not match the SQLRowCount() [%d] at line %d.\n", ( rowsProcessed - failureInjectionCount ), rowCount, __LINE__);
            rc = false;
        }
    }

    // Commit the rest of the rows.
    if ( features[ unitTest.feature ] != HASH2 )
    {
        retcode = SQLEndTran( SQL_HANDLE_DBC, handle[ SQL_HANDLE_DBC ], SQL_COMMIT );
        if( retcode != SQL_SUCCESS )    
        {
            RecordToLog( "\n    Failing API: SQLEndTran()\n" );
            CheckMsgs( "SQLEndTran()", __LINE__ );
            FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
            return false;
        }
    }

    FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
    /*****
    // Display time metrics
    if( ( timeMetrics ) && ( testMatrix[ testMatrixPos ].returnCode == true ) )
    {
        RecordToLog(" Running time in seconds: %lf\n", testMatrix[ testMatrixPos ].runningTime );
    }
    *****/
    return rc;
}

/* Function          : BindCols
   Calling Arguments : int : The test matrix test we are running.
   Return Arguments  : bool : True = bound columns False = errors

   Description: 
   Binds the C variables to the SQL data types inside the table to fetch the data.
 */
bool BindCols(  )
{
    SQLRETURN  retcode;       // Used to gather the return value of all ODBC API calls.

    RecordToLog( "    Freeing the statement bind column buffers.\n" );
    retcode= SQLFreeStmt( handle[ SQL_HANDLE_STMT ], SQL_UNBIND );
    if( retcode != SQL_SUCCESS )    
    {    
        RecordToLog( "SQLFreeStmt() with SQL_UNBIND attribute failed.\n" );
        CheckMsgs( "SQLFreeStmt()", __LINE__ );
    }
  
    // Allocate the space needed for the rowsets.
	AllocateRowsets( bindOrientations[ unitTest.bindOrientation ], rowsetSizes[unitTest.rowsetSize] );
       
    switch( bindOrientations[ unitTest.bindOrientation ] )
    {
        // Set the SQL_ATTR_ROW_BIND_TYPE statement attribute to use row-wise binding.
        case ROW:
        case SINGLE:
            retcode = SQLSetStmtAttr( handle[ SQL_HANDLE_STMT ], SQL_ATTR_ROW_BIND_TYPE, (void *)sizeof( table_rowset ), 0 );
            if( retcode != SQL_SUCCESS )    
            {
                CheckMsgs( "SQLSetStmtAttr()", __LINE__ );
                FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
                return false;
            }
            break;
        // Set the SQL_ATTR_ROW_BIND_TYPE statement attribute to use column-wise binding.
        case COLUMN:
            retcode = SQLSetStmtAttr( handle[ SQL_HANDLE_STMT ], SQL_ATTR_ROW_BIND_TYPE, SQL_BIND_BY_COLUMN, 0 );
            if( retcode != SQL_SUCCESS )    
            {    
                CheckMsgs( "SQLSetStmtAttr()", __LINE__ );
                FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
                return false;
            }
            break;
        default:
            RecordToLog( "INTERNAL ERROR: An unknown access style has been discovered at line %d.\n", __LINE__ );
            FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
            return false;
    }
    
    // Specify the number of elements in each parameter array.
    retcode = SQLSetStmtAttr( handle[ SQL_HANDLE_STMT ], SQL_ATTR_ROW_ARRAY_SIZE, (void *)rowsetSizes[ unitTest.rowsetSize ], 0 );
    if( retcode != SQL_SUCCESS )    
    {
        CheckMsgs( "SQLSetStmtAttr()", __LINE__ );
        FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
        return false;
    }

    // Specify an array in which to return the status of each set of parameters.
    retcode = SQLSetStmtAttr( handle[ SQL_HANDLE_STMT ], SQL_ATTR_ROW_STATUS_PTR, rowsetStatusArray, 0 );
    if( retcode != SQL_SUCCESS )    
    {
        CheckMsgs( "SQLSetStmtAttr()", __LINE__ );
        FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
        return false;
    }

    // Specify an SQLUINTEGER value in which to return the number of sets of parameters processed.
    rowsProcessed = 0;
    retcode = SQLSetStmtAttr( handle[ SQL_HANDLE_STMT ], SQL_ATTR_ROWS_FETCHED_PTR, &rowsProcessed, 0 );
    if( retcode != SQL_SUCCESS )    
    {
        CheckMsgs( "SQLSetStmtAttr()", __LINE__ );
        FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
        return false;
    }
/****
    retcode = SQLSetStmtAttr( handle[ SQL_HANDLE_STMT ], SQL_ATTR_CURSOR_TYPE, (SQLPOINTER)SQL_CURSOR_DYNAMIC, SQL_IS_UINTEGER);
    if( retcode != SQL_SUCCESS )    
    {   
        CheckMsgs( "SQLSetStmtAttr()", __LINE__ );
        FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
        return false;
    }

    retcode = SQLSetStmtAttr( handle[ SQL_HANDLE_STMT ], SQL_ATTR_CONCURRENCY, (SQLPOINTER)SQL_CONCUR_LOCK, SQL_IS_UINTEGER);
    if( retcode != SQL_SUCCESS )    
    {   
        CheckMsgs( "SQLSetStmtAttr()", __LINE__ );
        FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
        return false;
    }
****/

	BindColsA( bindOrientations[ unitTest.bindOrientation ], testCount);

    // See if we want the rowsets to be processed through preapre or directly.
    if( operations[ unitTest.operation ] == PREPARE_EXECUTE )
    {
        switch( actions[ unitTest.action] )
        {
            case SELECT:
            case INSERT_BULK:
                while( ( retcode = SQLPrepare( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStr[ 3 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
                break;
            default:
                break;
        }
    
        // Check the return status from the prepared statement.
        if( retcode != SQL_SUCCESS )    
        {
            CheckMsgs( "SQLPrepare()", __LINE__ );
            if( retcode != SQL_SUCCESS_WITH_INFO )
            {
                FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
                return false;
            }
        }
    }

    return true;
}

/* Function          : CompareRow
   Calling Arguments : int : The test matrix test we are running.
                     : int : Rowset position of the values.
                     : int : The value for the rowset.
   Return Arguments  : bool.
   
   Description: 
   This is a support function of RowsetFetch(). Compares the values 
   retrieved from the returning data.
*/

bool CompareRow( int rowsetPos, int rowsetValue )
{
    bool rc = true;
    int value, size;
//	int sizeUCS2;
    char valueStrSized[ STRINGMAX ]; // This is for the static sized columns
    char valueStr[9]; // The only values can be 0 through 60
    char valueStrReal[9]; // This is for real values.
//	char valueStrUCS2[ STRINGMAXDBL ];
//	char valueStrSizedUCS2[ STRINGMAXDBL ];

    // First we need to figure out what the value should be.
    if( bindOrientations[ unitTest.bindOrientation ] == SINGLE )
    {
        return true;
    }
    else
    {
        //value = ( ( rowsetPos + 1 ) + ( iteration * 10 ) );
        value = rowsetValue;
    }

    // Convert this value into the return values we expect.
    sprintf( valueStr, "%d", value );
	sprintf( valueStrReal, "%d.0", value );

	for( int loop = 0; loop != STRINGMAX; loop++ ) valueStrSized[ loop ] = ' ';
    valueStrSized[ STRINGMAX - 1 ] = '\0';

	for( int loop = 0; valueStr[loop] != '\0'; loop++ ) valueStrSized[ loop ] = valueStr[ loop ];

	size = (int)strlen(valueStr);

	switch( bindOrientations[ unitTest.bindOrientation ] )
    {
        case ROW:
        case SINGLE:
			//Checked size of data returned
			if (rowset[ rowsetPos ].ptr_char_iso != 20) {
                RecordToLog( "ERROR: Data type: ptr_char_iso Expected: 20 Actual %d at line %d\n", rowset[ rowsetPos ].ptr_char_iso, __LINE__ );
                rc = false;			
			}
			if (rowset[ rowsetPos ].ptr_char_ucs != 20) {
                RecordToLog( "ERROR: Data type: ptr_char_ucs Expected: 20 Actual %d at line %d\n", rowset[ rowsetPos ].ptr_char_ucs, __LINE__ );
                rc = false;			
			}
			if (rowset[ rowsetPos ].ptr_varchar_iso != size) {
                RecordToLog( "ERROR: Data type: ptr_varchar_iso Expected: %d Actual %d at line %d\n", size, rowset[ rowsetPos ].ptr_varchar_iso, __LINE__ );
                rc = false;			
			}
			if (rowset[ rowsetPos ].ptr_varchar_ucs != size) {
                RecordToLog( "ERROR: Data type: ptr_varchar_ucs Expected: %d Actual %d at line %d\n", size, rowset[ rowsetPos ].ptr_varchar_ucs, __LINE__ );
                rc = false;			
			}
			if (rowset[ rowsetPos ].ptr_longvarchar_iso != size) {
                RecordToLog( "ERROR: Data type: ptr_longvarchar_iso Expected: %d Actual %d at line %d\n", size, rowset[ rowsetPos ].ptr_longvarchar_iso, __LINE__ );
                rc = false;			
			}
			if (rowset[ rowsetPos ].ptr_longvarchar_ucs != size) {
                RecordToLog( "ERROR: Data type: ptr_longvarchar_ucs Expected: %d Actual %d at line %d\n", size, rowset[ rowsetPos ].ptr_longvarchar_ucs, __LINE__ );
                rc = false;			
			}
			if (rowset[ rowsetPos ].ptr_nchar != 20) {
                RecordToLog( "ERROR: Data type: ptr_nchar Expected: 20 Actual %d at line %d\n", rowset[ rowsetPos ].ptr_nchar, __LINE__ );
                rc = false;			
			}
			if (rowset[ rowsetPos ].ptr_ncharvarying != size) {
                RecordToLog( "ERROR: Data type: ptr_ncharvarying Expected: %d Actual %d at line %d\n", size, rowset[ rowsetPos ].ptr_ncharvarying, __LINE__ );
                rc = false;			
			}

			//Check value of data returned
			if( strncmp( (char*)rowset[ rowsetPos ].dt_char_iso,    valueStrSized, (int)rowset[ rowsetPos ].ptr_char_iso ) != 0 )
            {
                RecordToLog( "ERROR: Data type: dt_char_iso Expected: %s Actual %s at line %d\n", valueStr, (char*)rowset[ rowsetPos ].dt_char_iso, __LINE__ );
                rc = false;
            }
            if( strncmp( (char*)rowset[ rowsetPos ].dt_char_ucs,    valueStrSized, (int)rowset[ rowsetPos ].ptr_char_ucs ) != 0 )
            {
                RecordToLog( "ERROR: Data type: dt_char_ucs Expected: %s Actual %s at line %d\n", valueStr, (char*)rowset[ rowsetPos ].dt_char_ucs, __LINE__ );
                rc = false;
            }
            if( strncmp( (char*)rowset[ rowsetPos ].dt_varchar_iso,      valueStr, (int)rowset[ rowsetPos ].ptr_varchar_iso ) != 0 )
            {
                RecordToLog( "ERROR: Data type: dt_varchar_iso Expected: %s Actual %s at line %d\n", valueStr, (char*)rowset[ rowsetPos ].dt_varchar_iso , __LINE__);
                rc = false;
            }
            if( strncmp( (char*)rowset[ rowsetPos ].dt_varchar_ucs,      valueStr, (int)rowset[ rowsetPos ].ptr_varchar_ucs ) != 0 )
            {
                RecordToLog( "ERROR: Data type: dt_varchar_ucs Expected: %s Actual %s at line %d\n", valueStr, (char*)rowset[ rowsetPos ].dt_varchar_ucs, __LINE__ );
                rc = false;
            }
            if( strncmp( (char*)rowset[ rowsetPos ].dt_longvarchar_iso,  valueStr, (int)rowset[ rowsetPos ].ptr_longvarchar_iso ) != 0 )
            {
                RecordToLog( "ERROR: Data type: dt_longvarchar_iso Expected: %s Actual %s at line %d\n", valueStr, (char*)rowset[ rowsetPos ].dt_longvarchar_iso, __LINE__ );
                rc = false;
            }
            if( strncmp( (char*)rowset[ rowsetPos ].dt_longvarchar_ucs,  valueStr, (int)rowset[ rowsetPos ].ptr_longvarchar_ucs ) != 0 )            
            {
                RecordToLog( "ERROR: Data type: dt_longvarchar_ucs Expected: %s Actual %s at line %d\n", valueStr, (char*)rowset[ rowsetPos ].dt_longvarchar_ucs, __LINE__ );
                rc = false;
            }
            if( strncmp( (char*)rowset[ rowsetPos ].dt_nchar,       valueStrSized, (int)rowset[ rowsetPos ].ptr_nchar ) != 0 )
            {
                RecordToLog( "ERROR: Data type: dt_nchar Expected: %s Actual %s at line %d \n", valueStr, (char*)rowset[ rowsetPos ].dt_nchar , __LINE__);
                rc = false;
            }
            if( strncmp( (char*)rowset[ rowsetPos ].dt_ncharvarying,     valueStr, (int)rowset[ rowsetPos ].ptr_ncharvarying ) != 0 )
            {
                RecordToLog( "ERROR: Data type: dt_ncharvarying Expected: %s Actual %s at line %d \n", valueStr, (char*)rowset[ rowsetPos ].dt_ncharvarying, __LINE__ );
                rc = false;
            }

			if( strncmp( (char*)rowset[ rowsetPos ].dt_decimal_s,        "1", (int)rowset[ rowsetPos ].ptr_decimal_s ) != 0 )
            {
                RecordToLog( "ERROR: Data type: dt_decimal_s Expected: %s Actual %s at line %d \n", valueStr, (char*)rowset[ rowsetPos ].dt_decimal_s , __LINE__);
                rc = false;
            }
            if( strncmp( (char*)rowset[ rowsetPos ].dt_decimal_u,        valueStr, (int)rowset[ rowsetPos ].ptr_decimal_u ) != 0 )
            {
                RecordToLog( "ERROR: Data type: dt_decimal_u Expected: %s Actual %s at line %d \n", valueStr, (char*)rowset[ rowsetPos ].dt_decimal_u , __LINE__);
                rc = false;
            }
            if( strncmp( (char*)rowset[ rowsetPos ].dt_numeric_s,        "1", (int)rowset[ rowsetPos ].ptr_numeric_s ) != 0 )
            {
                RecordToLog( "ERROR: Data type: dt_numeric_s Expected: %s Actual %s at line %d\n", valueStr, (char*)rowset[ rowsetPos ].dt_numeric_s, __LINE__ );
                rc = false;
            }
            if( strncmp( (char*)rowset[ rowsetPos ].dt_numeric_u,        "1", (int)rowset[ rowsetPos ].ptr_numeric_u ) != 0 )
            {
                RecordToLog( "ERROR: Data type: dt_numeric_u Expected: %s Actual %s at line %d \n", valueStr, (char*)rowset[ rowsetPos ].dt_numeric_u, __LINE__ );
                rc = false;
            }
            if( strncmp( (char*)rowset[ rowsetPos ].dt_tinyint_s,        "1", (int)rowset[ rowsetPos ].ptr_tinyint_s ) != 0 )
            {
                RecordToLog( "ERROR: Data type: dt_tinyint_s Expected: %s Actual %s at line %d \n", valueStr, (char*)rowset[ rowsetPos ].dt_tinyint_s, __LINE__ );
                rc = false;
            }
            if( strncmp( (char*)rowset[ rowsetPos ].dt_tinyint_u,        "1", (int)rowset[ rowsetPos ].ptr_tinyint_u ) != 0 )
            {
                RecordToLog( "ERROR: Data type: dt_tinyint_u Expected: %s Actual %s at line %d \n", valueStr, (char*)rowset[ rowsetPos ].dt_tinyint_u , __LINE__);
                rc = false;
            }
            if( strncmp( (char*)rowset[ rowsetPos ].dt_smallinteger_s,   "1", (int)rowset[ rowsetPos ].ptr_smallinteger_s ) != 0 )
            {
                RecordToLog( "ERROR: Data type: dt_smallinteger_s Expected: %s Actual %s at line %d \n", valueStr, (char*)rowset[ rowsetPos ].dt_smallinteger_s , __LINE__);
                rc = false;
            }
            if( strncmp( (char*)rowset[ rowsetPos ].dt_smallinteger_u,   "1", (int)rowset[ rowsetPos ].ptr_smallinteger_u ) != 0 )
            {
                RecordToLog( "ERROR: Data type: dt_smallinteger_u Expected: %s Actual %s at line %d\n", valueStr, (char*)rowset[ rowsetPos ].dt_smallinteger_u , __LINE__);
                rc = false;
            }
            if( strncmp( (char*)rowset[ rowsetPos ].dt_integer_s,        valueStr, (int)rowset[ rowsetPos ].ptr_integer_s ) != 0 )
            {
                RecordToLog( "ERROR: Data type: dt_integer_s Expected: %s Actual %s at line %d\n", valueStr, (char*)rowset[ rowsetPos ].dt_integer_s, __LINE__ );
                rc = false;
            }
            if( strncmp( (char*)rowset[ rowsetPos ].dt_integer_u,        valueStr, (int)rowset[ rowsetPos ].ptr_integer_u ) != 0 )            
            {
                RecordToLog( "ERROR: Data type: dt_integer_u Expected: %s Actual %s at line %d \n", valueStr, (char*)rowset[ rowsetPos ].dt_integer_u, __LINE__ );
                rc = false;
            }
            if( strncmp( (char*)rowset[ rowsetPos ].dt_largeint,         valueStr, (int)rowset[ rowsetPos ].ptr_largeint ) != 0 )
            {
                RecordToLog( "ERROR: Data type: dt_largeint Expected: %s Actual %s at line %d\n", valueStr, (char*)rowset[ rowsetPos ].dt_largeint, __LINE__ );
                rc = false;
            }
            if( strncmp( (char*)rowset[ rowsetPos ].dt_real,         valueStrReal, (int)rowset[ rowsetPos ].ptr_real ) != 0 )
            {
                RecordToLog( "ERROR: Data type: dt_real Expected: %s Actual %s at line %d\n", valueStr, (char*)rowset[ rowsetPos ].dt_real , __LINE__);
                rc = false;
            }
            if( strncmp( (char*)rowset[ rowsetPos ].dt_float,        valueStrReal, (int)rowset[ rowsetPos ].ptr_float ) != 0 )
            {
                RecordToLog( "ERROR: Data type: dt_float Expected: %s Actual %s at line %d\n", valueStr, (char*)rowset[ rowsetPos ].dt_float, __LINE__ );
                rc = false;
            }
            if( strncmp( (char*)rowset[ rowsetPos ].dt_double_precision, valueStrReal, (int)rowset[ rowsetPos ].ptr_double_precision ) != 0 )
            {
                RecordToLog( "ERROR: Data type: dt_double_precision Expected: %s Actual %s at line %d\n", valueStr, (char*)rowset[ rowsetPos ].dt_double_precision, __LINE__ );
                rc = false;
            }

			if (tableFeatures[ unitTest.tableFeature ] == BEFORETRIGGER) {
				if( strncmp( (char*)rowset[ rowsetPos ].dt_bignum_s, "987654321098765", (int)rowset[ rowsetPos ].ptr_bignum_s ) != 0 )
				{
					RecordToLog( "ERROR: Data type: dt_bignum_s Expected: %s Actual %s at line %d\n", valueStr, (char*)rowset[ rowsetPos ].dt_bignum_s, __LINE__ );
					rc = false;
				}
				if( strncmp( (char*)rowset[ rowsetPos ].dt_bignum_u, "987654321098765", (int)rowset[ rowsetPos ].ptr_bignum_u ) != 0 )
				{
					RecordToLog( "ERROR: Data type: dt_bignum_u Expected: %s Actual %s at line %d \n", valueStr, (char*)rowset[ rowsetPos ].dt_bignum_u, __LINE__ );
					rc = false;
				}
			}
			else
			{
				if( strncmp( (char*)rowset[ rowsetPos ].dt_bignum_s, "1234567890123456789", (int)rowset[ rowsetPos ].ptr_bignum_s ) != 0 )
				{
					RecordToLog( "ERROR: Data type: dt_bignum_s Expected: %s Actual %s at line %d\n", valueStr, (char*)rowset[ rowsetPos ].dt_bignum_s, __LINE__ );
					rc = false;
				}
				if( strncmp( (char*)rowset[ rowsetPos ].dt_bignum_u, "1234567890123456789", (int)rowset[ rowsetPos ].ptr_bignum_u ) != 0 )
				{
					RecordToLog( "ERROR: Data type: dt_bignum_u Expected: %s Actual %s at line %d \n", valueStr, (char*)rowset[ rowsetPos ].dt_bignum_u, __LINE__ );
					rc = false;
				}
			}

			if (errorChecking != MODE_SPECIAL_1) {
				if( rowset[ rowsetPos ].dt_date.year  != 2000 )
				{
					RecordToLog( "ERROR: Data type: dt_date.year Expected: %d Actual %d \n", 
							2000, rowset[ rowsetPos ].dt_date.year );
					rc = false;
				}
				if( rowset[ rowsetPos ].dt_date.month != 1 )
				{
					RecordToLog( "ERROR: Data type: dt_date.month Expected: %d Actual %d \n", 
							1, rowset[ rowsetPos ].dt_date.month );
					rc = false;
				}
				if( rowset[ rowsetPos ].dt_date.day   != 2 )
				{
					RecordToLog( "ERROR: Data type: dt_date.day Expected: %d Actual %d \n", 
							2, rowset[ rowsetPos ].dt_date.day );
					rc = false;
				}
				if( rowset[ rowsetPos ].dt_time.hour   != 3 )
				{
					RecordToLog( "ERROR: Data type: dt_time.hour Expected: %d Actual %d \n", 
							3, rowset[ rowsetPos ].dt_time.hour );
					rc = false;
				}
				if( rowset[ rowsetPos ].dt_time.minute != 4 )
				{
					RecordToLog( "ERROR: Data type: dt_time.minute Expected: %d Actual %d \n", 
							4, rowset[ rowsetPos ].dt_time.minute );
					rc = false;
				}
				if( rowset[ rowsetPos ].dt_time.second != 5 )
				{
					RecordToLog( "ERROR: Data type: dt_time.second Expected: %d Actual %d \n", 
							5, rowset[ rowsetPos ].dt_time.second );
					rc = false;
				}
				if( rowset[ rowsetPos ].dt_timestamp.year     != 2000 )
				{
					RecordToLog( "ERROR: Data type: dt_timestamp.year Expected: %d Actual %d \n", 
							2000, rowset[ rowsetPos ].dt_timestamp.year );
					rc = false;
				}
				if( rowset[ rowsetPos ].dt_timestamp.month    != 1 )
				{
					RecordToLog( "ERROR: Data type: dt_timestamp.month Expected: %d Actual %d \n", 
							1, rowset[ rowsetPos ].dt_timestamp.month );
					rc = false;
				}
				if( rowset[ rowsetPos ].dt_timestamp.day      != 2 )
				{
					RecordToLog( "ERROR: Data type: dt_timestamp.day Expected: %d Actual %d \n", 
							2, rowset[ rowsetPos ].dt_timestamp.day );
					rc = false;
				}
				if( rowset[ rowsetPos ].dt_timestamp.hour     != 3 )
				{
					RecordToLog( "ERROR: Data type: dt_timestamp.hour Expected: %d Actual %d \n", 
							3, rowset[ rowsetPos ].dt_timestamp.hour );
					rc = false;
				}
				if( rowset[ rowsetPos ].dt_timestamp.minute   != 4 )
				{
					RecordToLog( "ERROR: Data type: dt_timestamp.minute Expected: %d Actual %d \n", 
							4, rowset[ rowsetPos ].dt_timestamp.minute );
					rc = false;
				}
				if( rowset[ rowsetPos ].dt_timestamp.second   != 5 )
				{
					RecordToLog( "ERROR: Data type: dt_timestamp.second Expected: %d Actual %d \n", 
							5, rowset[ rowsetPos ].dt_timestamp.second );
					rc = false;
				}
				if( rowset[ rowsetPos ].dt_timestamp.fraction != 600000 )
				{
					RecordToLog( "ERROR: Data type: dt_timestamp.fraction Expected: %d Actual %d \n", 
							600000, rowset[ rowsetPos ].dt_timestamp.fraction );
					rc = false;
				}
			}
            break;
        case COLUMN:
/****
                 ptr_char_iso[ loop ] = SQL_NTS;
                ptr_char_ucs[ loop ] = SQL_NTS;
                ptr_varchar_iso[ loop ] = SQL_NTS;
                ptr_varchar_ucs[ loop ] = SQL_NTS;
                ptr_longvarchar_iso[ loop ] = SQL_NTS;
                ptr_longvarchar_ucs[ loop ] = SQL_NTS;
                ptr_nchar[ loop ] = SQL_NTS;
                ptr_ncharvarying[ loop ] = SQL_NTS;
                ptr_decimal_s[ loop ] = SQL_NTS;
                ptr_decimal_u[ loop ] = SQL_NTS;
                ptr_numeric_s[ loop ] = SQL_NTS;
                ptr_numeric_u[ loop ] = SQL_NTS;
                ptr_tinyint_s[ loop ] = SQL_NTS;
                ptr_tinyint_u[ loop ] = SQL_NTS;
                ptr_smallinteger_s[ loop ] = SQL_NTS;
                ptr_smallinteger_u[ loop ] = SQL_NTS;
                ptr_integer_s[ loop ] = SQL_NTS;
                ptr_integer_u[ loop ] = SQL_NTS;
                ptr_largeint[ loop ] = SQL_NTS;
                ptr_real[ loop ] = SQL_NTS;
                ptr_float[ loop ] = SQL_NTS;
                ptr_double_precision[ loop ] = SQL_NTS;
                ptr_date[ loop ] = 0;
                ptr_time[ loop ] = 0;
                ptr_timestamp[ loop ] = 0;
                ptr_interval_year[ loop ] = 0;
                ptr_interval_month[ loop ] = 0;
                ptr_interval_day[ loop ] = 0;
                ptr_interval_hour[ loop ] = 0;
                ptr_interval_minute[ loop ] = 0;
                ptr_interval_second[ loop ] = 0;
                ptr_interval_year_to_month[ loop ] = 0;
                ptr_interval_day_to_hour[ loop ] = 0;
                ptr_interval_day_to_minute[ loop ] = 0;
                ptr_interval_day_to_second[ loop ] = 0;
                ptr_interval_hour_to_minute[ loop ] = 0;
                ptr_interval_hour_to_second[ loop ] = 0;
                ptr_interval_minute_to_second[ loop ] = 0;

			sprintf( (char*)&dt_char_iso[ rowsetPos * STRINGMAX ], "%d", column1Value );
            sprintf( (char*)&dt_char_ucs[ rowsetPos * STRINGMAX  ], "%d", column1Value );
            sprintf( (char*)&dt_varchar_iso[ rowsetPos * STRINGMAX  ], "%d", column1Value );
            sprintf( (char*)&dt_varchar_ucs[ rowsetPos * STRINGMAX  ], "%d", column1Value );
            sprintf( (char*)&dt_longvarchar_iso[ rowsetPos * STRINGMAX  ], "%d", column1Value );
            sprintf( (char*)&dt_longvarchar_ucs[ rowsetPos * STRINGMAX  ], "%d", column1Value );            
            sprintf( (char*)&dt_nchar[ rowsetPos * STRINGMAX  ], "%d", column1Value );
            sprintf( (char*)&dt_ncharvarying[ rowsetPos * STRINGMAX  ], "%d", column1Value );
            sprintf( (char*)&dt_decimal_s[ rowsetPos * STRINGMAX  ], "%d", column1Value );
            sprintf( (char*)&dt_decimal_u[ rowsetPos * STRINGMAX  ], "%d", column1Value );
            sprintf( (char*)&dt_numeric_s[ rowsetPos * STRINGMAX  ], "%d", column1Value );
            sprintf( (char*)&dt_numeric_u[ rowsetPos * STRINGMAX  ], "%d", column1Value );
            sprintf( (char*)&dt_tinyint_s[ rowsetPos * STRINGMAX  ], "%d", column1Value );
            sprintf( (char*)&dt_tinyint_u[ rowsetPos * STRINGMAX  ], "%d", column1Value );
            sprintf( (char*)&dt_smallinteger_s[ rowsetPos * STRINGMAX  ], "%d", column1Value );
            sprintf( (char*)&dt_smallinteger_u[ rowsetPos * STRINGMAX  ], "%d", column1Value );
            sprintf( (char*)&dt_integer_s[ rowsetPos * STRINGMAX  ], "%d", column1Value );
            sprintf( (char*)&dt_integer_u[ rowsetPos * STRINGMAX  ], "%d", column2Value );
            sprintf( (char*)&dt_largeint[ rowsetPos * STRINGMAX  ], "%d", column1Value );
            sprintf( (char*)&dt_real[ rowsetPos * STRINGMAX  ], "%d", column1Value );
            sprintf( (char*)&dt_float[ rowsetPos * STRINGMAX  ], "%d", column1Value );
            sprintf( (char*)&dt_double_precision[ rowsetPos * STRINGMAX  ], "%d", column1Value );
            dt_date[ rowsetPos ].year  = 2000;
            dt_date[ rowsetPos ].month = 1;
            dt_date[ rowsetPos ].day   = 2;
            dt_time[ rowsetPos ].hour   = 3;
            dt_time[ rowsetPos ].minute = 4;
            dt_time[ rowsetPos ].second = 5;
            dt_timestamp[ rowsetPos ].year     = 2000;
            dt_timestamp[ rowsetPos ].month    = 1;
            dt_timestamp[ rowsetPos ].day      = 2;
            dt_timestamp[ rowsetPos ].hour     = 3;
            dt_timestamp[ rowsetPos ].minute   = 4;
            dt_timestamp[ rowsetPos ].second   = 5;
            dt_timestamp[ rowsetPos ].fraction = 600000;
            dt_date[ rowsetPos ].year  = 2003;
            dt_date[ rowsetPos ].month = 3;
            dt_date[ rowsetPos ].day   = 3;
            dt_time[ rowsetPos ].hour   = 3;
            dt_time[ rowsetPos ].minute = 3;
            dt_time[ rowsetPos ].second = 3;
            dt_timestamp[ rowsetPos ].year     = 2003;
            dt_timestamp[ rowsetPos ].month    = 3;
            dt_timestamp[ rowsetPos ].day      = 3;
            dt_timestamp[ rowsetPos ].hour     = 3;
            dt_timestamp[ rowsetPos ].minute   = 3;
            dt_timestamp[ rowsetPos ].second   = 3;
            dt_timestamp[ rowsetPos ].fraction = 300000;
            dt_interval_year[ rowsetPos ].intval.year_month.year       = 0;
            dt_interval_month[ rowsetPos ].intval.year_month.month     = 1;
            dt_interval_day[ rowsetPos ].intval.day_second.day         = 2;
            dt_interval_hour[ rowsetPos ].intval.day_second.hour       = 3;
            dt_interval_minute[ rowsetPos ].intval.day_second.minute   = 4;
            dt_interval_second[ rowsetPos ].intval.day_second.second   = 5;
            dt_interval_second[ rowsetPos ].intval.day_second.fraction = 6;
            dt_interval_year_to_month[ rowsetPos ].intval.year_month.year  = 0;
            dt_interval_year_to_month[ rowsetPos ].intval.year_month.month = 1;
            dt_interval_day_to_hour[ rowsetPos ].intval.day_second.day  = 2;
            dt_interval_day_to_hour[ rowsetPos ].intval.day_second.hour = 3;
            dt_interval_day_to_minute[ rowsetPos ].intval.day_second.day    = 2;
            dt_interval_day_to_minute[ rowsetPos ].intval.day_second.hour   = 3;
            dt_interval_day_to_minute[ rowsetPos ].intval.day_second.minute = 4;
            dt_interval_day_to_second[ rowsetPos ].intval.day_second.day      = 2;
            dt_interval_day_to_second[ rowsetPos ].intval.day_second.hour     = 3;
            dt_interval_day_to_second[ rowsetPos ].intval.day_second.minute   = 4;
            dt_interval_day_to_second[ rowsetPos ].intval.day_second.second   = 5;
            dt_interval_day_to_second[ rowsetPos ].intval.day_second.fraction = 6;
            dt_interval_hour_to_minute[ rowsetPos ].intval.day_second.hour   = 3;
            dt_interval_hour_to_minute[ rowsetPos ].intval.day_second.minute = 4;
            dt_interval_hour_to_second[ rowsetPos ].intval.day_second.hour     = 3;
            dt_interval_hour_to_second[ rowsetPos ].intval.day_second.minute   = 4;
            dt_interval_hour_to_second[ rowsetPos ].intval.day_second.second   = 5;
            dt_interval_hour_to_second[ rowsetPos ].intval.day_second.fraction = 6;
            dt_interval_minute_to_second[ rowsetPos ].intval.day_second.minute   = 4;
            dt_interval_minute_to_second[ rowsetPos ].intval.day_second.second   = 5;
            dt_interval_minute_to_second[ rowsetPos ].intval.day_second.fraction = 6;
****/
            break;
    }

    if( !rc )
        RecordToLog( ">>>>>>>>Just compared row number %d.\n", rowsetPos);
    return rc;
}


/* Function          : RowsetFetch
   Calling Arguments : int : The test matrix test we are running.
                       int : Not implemented in the function yet.
   Return Arguments  : bool : True = pass False = fail

   Description: 
   
 */
bool RowsetFetch( )
{
    SQLRETURN  retcode;       // Used to gather the return value of all ODBC API calls.
    bool rc = true;
    bool gatheredData = false;
    int rowValue = 0;
    time_t     startTime;
    int numberOfRowsRetrieved = 0;
    
    // Run the prepared select statement. 
    if( operations[ unitTest.operation ] == PREPARE_EXECUTE )
    {
        while( ( retcode = SQLExecute( handle[ SQL_HANDLE_STMT ] ) ) == SQL_STILL_EXECUTING );
    }
    else
    {
        while( (retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStr[ 3 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
    }
    
    if( retcode != SQL_SUCCESS )    
    {
        if( retcode != SQL_SUCCESS_WITH_INFO )
        {
            CheckMsgs( "SQLExecute()", __LINE__ );
            FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
            return false;
        }
    }
    
    // Gather the data.
    while( retcode != SQL_NO_DATA ) 
    {
        time( &startTime );
        while( ( retcode = SQLFetch( handle[ SQL_HANDLE_STMT ] ) ) == SQL_STILL_EXECUTING );
        if( retcode == SQL_NO_DATA )
        {
            break;
        }
        if( retcode != SQL_SUCCESS )
        {
            CheckMsgs( "SQLFetch()", __LINE__ );
            FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
            SQLFreeStmt( handle[ SQL_HANDLE_STMT ], SQL_CLOSE );
            return false;
        }

        numberOfRowsRetrieved += (int)rowsProcessed;

        gatheredData = true;
        for( int rowPos = 0; rowPos < (int)rowsProcessed; rowPos++ ) 
        {
            rowValue++;
            if ( ( rowsetStatusArray[ rowPos ] == SQL_ROW_SUCCESS ) ||
                 ( rowsetStatusArray[ rowPos ] == SQL_ROW_SUCCESS_WITH_INFO ) ) 
            {
                // TODO: INSERT LOGIC TO MAKE SURE RETURNING VALUES ARE RIGHT
                if( injectionTypes[ unitTest.injectionType ] == NO_ERRORS )
                {
                    if( !CompareRow( rowPos, rowValue ) )
                        rc = false;
                }
            }
            else
            {
                RecordToLog(" >> ERROR: Rowset status array row %d was expected to have SQL_ROW_SUCCESS or SQL_ROW_SUCCESS_WITH_INFO. Actual: %d at line %d.\n", rowPos, rowsetStatusArray[ rowPos ] , __LINE__); 
                rc = false;
            }
        }
    }

    if( numberOfRowsRetrieved != goodRowCount)
    {
        RecordToLog(" >> ERROR: The number of rows expected (%d) does not match the number of rows retrieved (%d) at line %d.\n", goodRowCount, numberOfRowsRetrieved, __LINE__);
        rc = false;
    }
    if( !gatheredData && (goodRowCount != 0))
    {
        RecordToLog(" >> ERROR: No data was returned from SELECT statement at line %d.\n", __LINE__ ); 
        rc = false;
    }

	//if( numberOfRowsRetrieved != ( numberOfRows[ unitTest.numberOfRows ] - failureInjectionCount ))
    //{
    //    RecordToLog(" >> ERROR: The number of rows retrieved (%d) does not match the number of rows expected (%d) at line %d.\n", numberOfRowsRetrieved, numberOfRows[ unitTest.numberOfRows ] - failureInjectionCount , __LINE__);
    //    rc = false;
    //}        
    //if( !gatheredData && ((numberOfRows[ unitTest.numberOfRows ] - failureInjectionCount) != 0))
    //{
    //    RecordToLog(" >> ERROR: No data was returned from SELECT statement at line %d.\n", __LINE__ ); 
    //    rc = false;
    //}

	FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
    
    return rc;
}

/* Function          : RowsetDML
   Calling Arguments : int : The test matrix test we are running.
                       int : What rows to inject errors into.
   Return Arguments  : bool : True = pass False = fail

   Description: 
   This is the inner heart of the client. This function assigns the values to the 
   rowsets and then executes the prepared SQL command. Then some in house error
   checking and repeat.
 */
bool RowsetDML( )
{
    SQLRETURN  retcode;       // Used to gather the return value of all ODBC API calls.
    SQLRETURN  rowsetRetcode, expectedRowsetRetcode;
    int        numIterations = 0;
    int        numberOfRowsHandled = 0;
    SQLLEN     rowCount;
    int        rs;
    bool       rc = true;
    time_t     startTime;

	rs = GeneratingRows( rowsetSizes[ unitTest.rowsetSize ], numberOfRows[ unitTest.numberOfRows ], 
                         injectionTypes[ unitTest.injectionType ], tableTypes[ unitTest.tableType ], 
						 actions[ unitTest.action ], bindOrientations[ unitTest.bindOrientation ] );
   
	//Assign the expected rowset returncode value
    switch( injectionTypes[ unitTest.injectionType ] )
    {
		case NO_ERRORS:
			expectedRowsetRetcode = SQL_SUCCESS;
			break;
		case DUPLICATEKEY:
			if (actions[ unitTest.action ] == INSERT && tableTypes [ unitTest.tableType ] != MULTISET)
				expectedRowsetRetcode = SQL_SUCCESS_WITH_INFO;
			else
				expectedRowsetRetcode = SQL_SUCCESS;
			break;
		case DUPLICATEROW:
			if (tableTypes [ unitTest.tableType ] == SET && errorChecking != MODE_SPECIAL_1) {
				expectedRowsetRetcode = SQL_SUCCESS;
			}
			else {
				if (actions[ unitTest.action ] == INSERT && tableTypes [ unitTest.tableType ] != MULTISET)
					expectedRowsetRetcode = SQL_SUCCESS_WITH_INFO;
				else
					expectedRowsetRetcode = SQL_SUCCESS;
			}
			break;
		case UNIQUECONST:
		case OVERFLOW:
		case NULLVALUE:
		case ERR_PER_ROW:
		case FULL_ERRORS:
		case DRIVER_GOOD_BAD_MULCOL:								//All error, no warning, some good rows, multiple columns
		case DRIVER_GOOD_WARNING_MULCOL:							//All warning, multiple columns
		case DRIVER_GOOD_BAD_WARNING_MULCOL:						//Error and warning, multiple columns
		case DRIVER_ALL_BAD_MULCOL:								//All error, multiple columns
		case DRIVER_ALL_WARNING_MULCOL:							//All warning, multiple columns
		case DRIVER_ALL_BAD_WARNING_MULCOL:						//Error and warning, multiple columns
		case SERVER_GOOD_BAD_MULCOL:								//Some good rows, some bad rows, multiple columns server error only and/or driver warning
		case SERVER_ALL_BAD_MULCOL:								//All bad rows, multiple columns server error only and/or driver warning
		case MIXED_DRIVERWARNING_SERVERBAD_GOOD_MULCOL:			//Some driver warning, Some server error, some good, multiple columns
		case MIXED_DRIVERBAD_SERVERBAD_GOOD_MULCOL:				//Some good rows, some driver errors, some server errors, multiple columns
		case MIXED_DRIVERWARNING_DRIVERBAD_SERVERBAD_GOOD_MULCOL://Some good rows, some driver errors, some driver warnings, some server errors, multiple columns
		case MIXED_DRIVERBAD_SERVERBAD_MULCOL:					//Driver errrors, server errors, no warning, no good row, multiple columns
		case MIXED_DRIVERWARNING_DRIVERBAD_SERVERBAD_MULCOL:		//Driver errrors, driver warnings, server errors, no good row, multiple columns
			if (actions[ unitTest.action ] == DELETE_PARAM)
				expectedRowsetRetcode = SQL_SUCCESS;
			else
				expectedRowsetRetcode = SQL_SUCCESS_WITH_INFO;
			break;
		case SELECTIVE:
		case CANCEL:
			break;
		default:
            RecordToLog( " >> INTERNAL ERROR: An unknown failure type has been discovered. at line=%d\n", __LINE__ );
            rc = false;
            break;
	}

    // We might have to readjust the rowset size we supply to the driver.
    if( rs != rowsetSizes[ unitTest.rowsetSize ] )
    {
        retcode = SQLSetStmtAttr( handle[ SQL_HANDLE_STMT ], SQL_ATTR_PARAMSET_SIZE, (void *)rs, 0 );
        if( retcode != SQL_SUCCESS )    
        {
            CheckMsgs( "SQLSetStmtAttr()", __LINE__ );
            FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
            return false;
        }
    }

    // Pass in the rowset over to the ODBC driver to handle.
    time( &startTime );
    if( operations[ unitTest.operation ] == PREPARE_EXECUTE )
    {
        while( ( rowsetRetcode = SQLExecute( handle[ SQL_HANDLE_STMT ] ) ) == SQL_STILL_EXECUTING );
    }
    else
    {
        switch( actions[ unitTest.action ] )
        {
            case INSERT:
                while( ( rowsetRetcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStr[ 2 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
                break;
            case DELETE_PARAM:
                while( ( rowsetRetcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStr[ 6 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
                break;
            case UPDATE:
				while( ( rowsetRetcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)ExecSQLStr[ 7 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
                break;
            default:
                RecordToLog( " >> INTERNAL ERROR: An unknown table action has been discovered.\n" );
                FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
                return false;
        }
    }

	if (rowsetRetcode != SQL_SUCCESS) {
		if (rowsetRetcode != SQL_SUCCESS_WITH_INFO || debug) 
			CheckMsgsNoIgnored();
	}

	if ( rowsetRetcode != expectedRowsetRetcode)
	{
		RecordToLog( " >> Failing API: SQLExecute/Direct(), expected: %d, actual: %d at line= %d\n", expectedRowsetRetcode, rowsetRetcode, __LINE__ );
		CheckMsgs( "SQLExecute/Direct()", __LINE__ );
		//FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
		rc = false;
		//return false;
	}

    numIterations++;

    // See if we need to commit the transaction.
    if( commitRates[ unitTest.commitRate ] == numIterations  &&
        features[ unitTest.feature ] != HASH2 ) // Commit the rows at the set commit rate.
    {
        retcode = SQLEndTran( SQL_HANDLE_DBC, handle[ SQL_HANDLE_DBC ], SQL_COMMIT );
        if( retcode != SQL_SUCCESS )    
        {
            RecordToLog( " >> Failing API: SQLEndTran()\n" );
            CheckMsgs( "SQLEndTran()", __LINE__ );
			DisplayTable(bindOrientations[ unitTest.bindOrientation ],rs);
            FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
            return false;
        }
        numIterations = 0;
    }

    // Check to make sure all the rows we inserted were processed.
    if ( (int)rowsProcessed != rs ) {
        RecordToLog(" >> ERROR: The number of parameters processed does not match the number of rows prepared.\n");
        RecordToLog(" >> ERROR: Rows processed by ODBC: %d Rows prepared by client: %d\n", (int)rowsProcessed, rs );
        rc = false;
    }

	bool pSuccessinfo = false;
	for (int i = 0; i < (int)rowsProcessed; i++) {
		//if (debug) {
		//	RecordToLog("Parameter Set  Status\n");
		//	RecordToLog("-------------  -------------\n");
		//}
		if (expectedRowsetStatusArray[i] == rowsetStatusArray[i]) {
				switch (expectedRowsetStatusArray[i]) {
					case SQL_PARAM_SUCCESS:
      						if (debug || rc==false) RecordToLog("%13d  Success\n", i+1);
  							break;
					case SQL_PARAM_SUCCESS_WITH_INFO:
     						if (debug || rc==false) RecordToLog("%13d  Success With Info\n", i+1);
							pSuccessinfo = true;
     						break;
  						case SQL_PARAM_ERROR:
    						if (debug || rc==false) RecordToLog("%13d  Error  <-----\n", i+1);
							pSuccessinfo = true;
    						break;
  						case SQL_PARAM_UNUSED:
							if (debug || rc==false) RecordToLog("%13d  Not processed\n", i+1);
    						break;
 						case SQL_PARAM_DIAG_UNAVAILABLE:
    						if (debug || rc==false) RecordToLog("%13d  Unknown\n", i+1);
    						break;
				}
		}
		else {
			RecordToLog("%13d  ERROR: Rowset status array row %d was expected to have %s. Actual: %s at line %d.\n", i+1, i+1, Param_Status_Ptr( expectedRowsetStatusArray[ i ] ), Param_Status_Ptr( rowsetStatusArray[ i ] ), __LINE__ );
			rc = false;
		}
	}

	if ((rowsetRetcode == SQL_SUCCESS && pSuccessinfo) ||
		(rowsetRetcode == SQL_SUCCESS_WITH_INFO && !pSuccessinfo)){
   		RecordToLog(" >> ERROR: All the rows in rowset status array don't macth with rowset returncode= %d, at line %d.\n", rowsetRetcode, __LINE__ );
		rc = false;
	}

    // Check to make sure the row count of affected rows is correct.
    retcode = SQLRowCount( handle[ SQL_HANDLE_STMT ], &rowCount );
    if( retcode != SQL_SUCCESS )    
    {
        RecordToLog( "    Failing API: SQLRowCount()\n" );
        CheckMsgs( "SQLRowCount()", __LINE__ );
		//DisplayTable(bindOrientations[ unitTest.bindOrientation ],rs);
        FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
        return false;
    }

	if( (int)rowCount != goodRowCount)
	{
		//RecordToLog( "ExpectedRowcount=%d , ActualRowcount=%d\n", goodRowCount, rowCount );
		RecordToLog( " >> ERROR: The number of expected good rows processed [%d] does not match the SQLRowCount() [%d] at line %d.\n", goodRowCount, rowCount, __LINE__);
		rc = false;
	}

    // Commit the rest of the rows.
    if ( features[ unitTest.feature ] != HASH2 )
    {
        retcode = SQLEndTran( SQL_HANDLE_DBC, handle[ SQL_HANDLE_DBC ], SQL_COMMIT );
        if( retcode != SQL_SUCCESS )    
        {
            RecordToLog( "\n    Failing API: SQLEndTran()\n" );
            CheckMsgs( "SQLEndTran()", __LINE__ );
            FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
            return false;
        }
    }

	if(rc == false) {
		PrintTestInformation();
		DisplayTable(bindOrientations[ unitTest.bindOrientation ],rs);
	}

	FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );

    return rc;
}



/****************************************************************
** ALM_LogTestCaseInfo(char*, char*, int, int)
**
** This function will attempt to write the TestCase Info to ALM log file
****************************************************************/
void ALM_LogTestCaseInfo(char *testID, char *ALM_TestCase_Description, int nStartTest, int nEndTest)
{
	int i=0;
	char ALM_buff[1024];

	/* Note: the char string pointer ALM_TestCase_Description is coming 
	with a "\n" that we need to remove it to avoid output extra line. */
    int original_len = (unsigned)strlen(ALM_TestCase_Description)+1;
    char *Description_string = (char *)malloc(original_len);
    memset(Description_string,0,original_len);
    strncpy(Description_string,ALM_TestCase_Description,original_len);

    for(i=0; i<original_len; i++)
    {
        if(Description_string[i] == '\n')
        {
            // Move all the char following the char "c" by one to the left.
            strncpy(&Description_string[i],&Description_string[i+1],original_len-i);
        }
    }

	/* Log into ALM report as well */
	sprintf(ALM_buff, "odbc-%s|%s+%s+%s+%s|%s|%s|\n", 
		machine, "rowsets", "ANSI", "ASCII", machine, testID, Description_string);
	RecordTo_ALM_Log(ALM_buff);

}


/****************************************************************
** ALM_LogTestResultInfo(PassFail, time_t, time_t)
**
** This function will attempt to write the TestCase Info to ALM log file
****************************************************************/
void ALM_LogTestResultInfo(PassFail result,
						   time_t tStart,
						   time_t tEnd)
{
	char	ALM_buff[1024];
	char	ALM_Datebuf[11];  /* yyyy-mm-dd */
	char	ALM_Test_startTime[11],  ALM_Test_endTime[11]; /* hh:mm:ss */

	strftime( ALM_Datebuf, 11, "%Y-%m-%d", localtime( &tStart ) );
	strftime( ALM_Test_startTime, 11, "%H:%M:%S", localtime( &tStart ) );
	strftime( ALM_Test_endTime, 11, "%H:%M:%S", localtime( &tEnd ) );

	if (result==PASSED)
	{
		sprintf(ALM_buff, "PASS|%s|%s|%s|%.0f|\n", 
			ALM_Datebuf, ALM_Test_startTime, ALM_Test_endTime, difftime(tEnd, tStart));
	}
	else
	{
		sprintf(ALM_buff, "FAIL|%s|%s|%s|%.0f|\n", 
			ALM_Datebuf, ALM_Test_startTime, ALM_Test_endTime, difftime(tEnd, tStart));
	}

	RecordTo_ALM_Log(ALM_buff);
}

