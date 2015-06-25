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
#include <stdio.h>
#include <wchar.h>
#include "stdafx.h"
#include "RowSets.h"

/* SQ #define DEBUG_PRINT 1 */

int modes[]            = { STANDARD, STOP };
int features[]         = { STANDARD, STOP, ASYNC, HASH2 };
int operations[]       = { PREPARE_EXECUTE, EXECUTE_DIRECT, STOP };
int bindOrientations[] = { ROW, COLUMN, SINGLE, STOP };
int actions[]          = { INSERT, SELECT, UPDATE, DELETE_PARAM, STOP, INSERT_SELECT, INSERT_BULK }; // DELETE_PARAM needs to be the last action before STOP.
int tableTypes[]       = {
		REGULAR,
		SURROGATE,
		POSOFF,
		SET,
		MULTISET,
		VOLATILE,
		STOP
};
int tableFeatures[]    = {
		STANDARD,
		INDEX,
		MVS,
		AFTERTRIGGER,
		STOP,
		BEFORETRIGGER, //This feature doesn't support yet
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

/*
// Standard
TCHAR ExecSQLStr[ 16 ][ 2048 ];
// MVS
TCHAR ExecSQLStrMVS[ 7 ][ 2048 ];
// Index
TCHAR ExecSQLStrIndex[ 2 ][ 2048 ];
// RI
TCHAR ExecSQLStrRI[ 4 ][ 2048 ];
// Volatile
TCHAR ExecSQLStrVolatile[ 2 ][ 2048 ];
// Before Trigger
TCHAR ExecSQLStrBeforeTrigger[2][2048];
// After Trigger
TCHAR ExecSQLStrAfterTrigger[4][2048];
*/
// Standard
TCHAR* ExecSQLStr[ 16 ];
// MVS
TCHAR* ExecSQLStrMVS[ 7 ];
// Index
TCHAR* ExecSQLStrIndex[ 2 ];
// RI
TCHAR* ExecSQLStrRI[ 4 ];
// Volatile
TCHAR* ExecSQLStrVolatile[ 2 ];
// Before Trigger
TCHAR* ExecSQLStrBeforeTrigger[2];
// After Trigger
TCHAR* ExecSQLStrAfterTrigger[5];

TCHAR* Digit_2_Charset[11];
TCHAR* Digit_2_Ascii[11];

SQLTCHAR ignoreState[ NUMBER_OF_IGNORES ][ 10 ];
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

TCHAR *charset_filenames[] = {_T("charset_auto_generated_ascii.char"),
							 _T("charset_auto_generated_sjis.char"),
							 _T("charset_auto_generated_big5.char"),
							 _T("charset_auto_generated_gb2.char"),
							 _T("charset_auto_generated_gb1.char"),
							 _T("charset_auto_generated_ksc.char"),
							 _T("charset_auto_generated_eucjp.char"),
							 _T("charset_auto_generated_latin1.char"),
/* SQ */				 _T("charset_auto_generated_gbk.char")
						 };
TCHAR	charset_file[256];

// This concludes the test pre-defined variables. Everything below this is in regards to running the tests.
int _tmain( int argc, TCHAR* argv[] )
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

	//Initialize default values
	charset = (TCHAR*)_T("ASCII");
	_tcscpy(charset_file,charset_filenames[0]);
	uid = (TCHAR*)_T("odbcqa");
	password = (TCHAR*)_T("odbcqa");


    optarg = NULL;
    if ( argc < 9 || argc > 13)
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
				//Log output mode - simply display table's content if debug=true
#ifdef _UNIX
				if (strcasecmp(optarg,_T("debug")) == 0) debug = true;
#else
				if (_tcsicmp(optarg,_T("debug")) == 0) debug = true;
#endif
				else errflag++;
                break;
			case 'c':
				// Which default script file to pick up
				// This is not needed if -f below is specified
				charset = optarg;
				if (!_tcsicmp(charset,_T("ASCII"))) {
					_tcscpy(charset_file,charset_filenames[0]);
				}
				else if (!_tcsicmp(charset,_T("SJIS"))) {
					_tcscpy(charset_file,charset_filenames[1]);
				}
				else if (!_tcsicmp(charset,_T("BIG5"))) {
					_tcscpy(charset_file,charset_filenames[2]);
				}
				else if (!_tcsicmp(charset,_T("GB2"))) {
					_tcscpy(charset_file,charset_filenames[3]);
				}
				else if (!_tcsicmp(charset,_T("GB1"))) {
					_tcscpy(charset_file,charset_filenames[4]);
				}
				else if (!_tcsicmp(charset,_T("KSC"))) {
					_tcscpy(charset_file,charset_filenames[5]);
				}
				else if (!_tcsicmp(charset,_T("EUCJP"))) {
					_tcscpy(charset_file,charset_filenames[6]);
				}
				else if (!_tcsicmp(charset,_T("LATIN1"))) {
					_tcscpy(charset_file,charset_filenames[7]);
				}
				/* SQ */
				else if (!_tcsicmp(charset,_T("GBK"))) {
					_tcscpy(charset_file,charset_filenames[8]);
				}
				/* end of SQ */
				else {
					errflag++;
				}
				break;
            case 't':
				//The specific test number to run
                testToRun = _tstoi( optarg );
                singleTest = true;
                break;
            case 'r':
				//The test number to resume from
                if( singleTest == false )
                {
                    testToRun = _tstoi( optarg );
                    resumeTesting = true;
                }
                break;
			case 'm':
				//This is used to replace the 'local' in log's file name
				//   in helping to identify the test being run
				//   the format should be like: "UNICODE+ASCII+win32" or "UNICODE+GBK+win64", etc
				machine = optarg;
				_tprintf((TCHAR*)"Machine is: %s\n", machine);
				break;
			case 's':
				//Input secondary role for LDAP testing
				secondaryRole = optarg;
				break;
			case 'f':
				//actual path of input script file
				_tcscpy(charset_file,optarg);
				break;
            default :
                errflag++;
				break;
        }
    }

	time_t my_clock;
	my_clock = time( NULL);
    _tcsftime( logfilename, 256, _T("rowsets_%Y-%m-%d_%H.%M.%S."), localtime( &my_clock ) );
#ifdef UNICODE
	_tcscat(logfilename, _T("UNICODE."));
#else
	_tcscat(logfilename, _T("ANSI."));
#endif
	_tcscat(logfilename, charset);
	_tcscat(logfilename, _T("."));
	_tcscat(logfilename, datasource);
	_tcscat(logfilename, _T("."));
	_tcscat(logfilename, machine);
	_tcscat(logfilename, _T(".log"));

	// start for ALM log
    _tcsftime( ALM_log_file_buff, 256, _T("rowsets_%Y-%m-%d_%H.%M.%S."), localtime( &my_clock ) );
#ifdef UNICODE
	_tcscat(ALM_log_file_buff, _T("UNICODE."));
#else
	_tcscat(ALM_log_file_buff, _T("ANSI."));
#endif
	_tcscat(ALM_log_file_buff, charset);
	_tcscat(ALM_log_file_buff, _T("."));
	_tcscat(ALM_log_file_buff, datasource);
	_tcscat(ALM_log_file_buff, _T("."));
	_tcscat(ALM_log_file_buff, machine);
	_tcscat(ALM_log_file_buff, _T("_ALM.log"));
	// end for ALM log 

	if ( errflag ) 
    {
        RecordToLog( _T("Command line error.\n") );
        //RecordToLog( _T("Usage: %s -d <datasource> -u <userid> -p <password> [-o <debug> | -t <testid> | -r <test_id>]\n"), argv[0] );
        RecordToLog( _T("Usage: %s -d <datasource> -u <userid> -p <password> -c <ASCII|SJIS|BIG5|GB1|GB2|KSC|EJCJP|LATIN1> -m <OS> [-o <debug>]\n"), argv[0] );
        RecordToLog( _T("-d: data source\n") );
        RecordToLog( _T("-u: user identification\n") );
        RecordToLog( _T("-p: user password\n") );
        RecordToLog( _T("-c: character set\n") );
        RecordToLog( _T("-m: test client OS\n") );
        RecordToLog( _T("-o: turn debug mode 'ON' (optional)\n") );
        //RecordToLog( _T("-t: test id to run (optional)\n") );
        //RecordToLog( _T("-r: resume test id to start from (optional)\n") );
        return 0;
    }

#ifndef _UNIX
	TCHAR temp[256];
	FILE *scriptFD = NULL;
	errno_t err;
	if ((err  = _wfopen_s(&scriptFD, charset_file, _T("r")))  !=0 ) 
	{
		_tcscpy(temp, /* SQ _T("..\\") */_T("..\\..\\..\\src\\"));
		_tcscat(temp, charset_file);
		_tcscpy(charset_file, temp);

		if ((err  = _wfopen_s(&scriptFD, charset_file, _T("r")))  !=0) 
		{
			_tprintf(_T("Error open charset script file %s\n"), charset_file);
		    RecordToLog( _T("Error open charset script file\n") );
			return FALSE;
		}
	}
	fclose(scriptFD);
	/* SQ */ 	_tprintf(_T("Loading data from: %s\n"), charset_file);
#endif
	_tprintf(_T("Charset script file is loaded from: %s\n"), charset_file);

	setlocale(LC_ALL, "");
	//===========================================================================================================
	//Load charset data
	var_list_t *var_list;
	var_list = load_api_vars(_T("Rowsets"), charset_file);
	if (var_list == NULL) return 0;
	//print_list(var_list);

	ExecSQLStr[0] = var_mapping(_T("ExecSQLStr0"), var_list);
	ExecSQLStr[1] = var_mapping(_T("ExecSQLStr1"), var_list);
	ExecSQLStr[2] = var_mapping(_T("ExecSQLStr2"), var_list);
	ExecSQLStr[3] = var_mapping(_T("ExecSQLStr3"), var_list);
	ExecSQLStr[4] = var_mapping(_T("ExecSQLStr4"), var_list);
	ExecSQLStr[5] = var_mapping(_T("ExecSQLStr5"), var_list);
	ExecSQLStr[6] = var_mapping(_T("ExecSQLStr6"), var_list);
	ExecSQLStr[7] = var_mapping(_T("ExecSQLStr7"), var_list);
	ExecSQLStr[8] = var_mapping(_T("ExecSQLStr8"), var_list);
	ExecSQLStr[9] = var_mapping(_T("ExecSQLStr9"), var_list);
	ExecSQLStr[10] = var_mapping(_T("ExecSQLStr10"), var_list);
	ExecSQLStr[11] = var_mapping(_T("ExecSQLStr11"), var_list);
	ExecSQLStr[12] = var_mapping(_T("ExecSQLStr12"), var_list);
	ExecSQLStr[13] = var_mapping(_T("ExecSQLStr13"), var_list);
	ExecSQLStr[14] = var_mapping(_T("ExecSQLStr14"), var_list);
	ExecSQLStr[15] = var_mapping(_T("ExecSQLStr15"), var_list);

	ExecSQLStrIndex[0] = var_mapping(_T("ExecSQLStrIndex0"), var_list);
	ExecSQLStrIndex[1] = var_mapping(_T("ExecSQLStrIndex1"), var_list);

	ExecSQLStrRI[0] = var_mapping(_T("ExecSQLStrRI0"), var_list);
	ExecSQLStrRI[1] = var_mapping(_T("ExecSQLStrRI1"), var_list);
	ExecSQLStrRI[2] = var_mapping(_T("ExecSQLStrRI2"), var_list);
	ExecSQLStrRI[3] = var_mapping(_T("ExecSQLStrRI3"), var_list);

	ExecSQLStrVolatile[0] = var_mapping(_T("ExecSQLStrVolatile0"), var_list);
	ExecSQLStrVolatile[1] = var_mapping(_T("ExecSQLStrVolatile1"), var_list);

	ExecSQLStrMVS[0] = var_mapping(_T("ExecSQLStrMVS0"), var_list);
	ExecSQLStrMVS[1] = var_mapping(_T("ExecSQLStrMVS1"), var_list);
	ExecSQLStrMVS[2] = var_mapping(_T("ExecSQLStrMVS2"), var_list);
	ExecSQLStrMVS[3] = var_mapping(_T("ExecSQLStrMVS3"), var_list);
	ExecSQLStrMVS[4] = var_mapping(_T("ExecSQLStrMVS4"), var_list);
	ExecSQLStrMVS[5] = var_mapping(_T("ExecSQLStrMVS5"), var_list);
	ExecSQLStrMVS[6] = var_mapping(_T("ExecSQLStrMVS6"), var_list);

	ExecSQLStrBeforeTrigger[0] = var_mapping(_T("ExecSQLStrBeforeTrigger0"), var_list);
	ExecSQLStrBeforeTrigger[1] = var_mapping(_T("ExecSQLStrBeforeTrigger1"), var_list);

	ExecSQLStrAfterTrigger[0] = var_mapping(_T("ExecSQLStrAfterTrigger0"), var_list);
	ExecSQLStrAfterTrigger[1] = var_mapping(_T("ExecSQLStrAfterTrigger1"), var_list);
	ExecSQLStrAfterTrigger[2] = var_mapping(_T("ExecSQLStrAfterTrigger2"), var_list);
	ExecSQLStrAfterTrigger[3] = var_mapping(_T("ExecSQLStrAfterTrigger3"), var_list);
	ExecSQLStrAfterTrigger[4] = var_mapping(_T("ExecSQLStrAfterTrigger4"), var_list);

	Digit_2_Charset[0] = var_mapping(_T("Digit_2_Charset0"), var_list);
	Digit_2_Charset[1] = var_mapping(_T("Digit_2_Charset1"), var_list);
	Digit_2_Charset[2] = var_mapping(_T("Digit_2_Charset2"), var_list);
	Digit_2_Charset[3] = var_mapping(_T("Digit_2_Charset3"), var_list);
	Digit_2_Charset[4] = var_mapping(_T("Digit_2_Charset4"), var_list);
	Digit_2_Charset[5] = var_mapping(_T("Digit_2_Charset5"), var_list);
	Digit_2_Charset[6] = var_mapping(_T("Digit_2_Charset6"), var_list);
	Digit_2_Charset[7] = var_mapping(_T("Digit_2_Charset7"), var_list);
	Digit_2_Charset[8] = var_mapping(_T("Digit_2_Charset8"), var_list);
	Digit_2_Charset[9] = var_mapping(_T("Digit_2_Charset9"), var_list);
	Digit_2_Charset[10] = var_mapping(_T("Digit_2_Charset10"), var_list);

	Digit_2_Ascii[0] = var_mapping(_T("Digit_2_Ascii0"), var_list);
	Digit_2_Ascii[1] = var_mapping(_T("Digit_2_Ascii1"), var_list);
	Digit_2_Ascii[2] = var_mapping(_T("Digit_2_Ascii2"), var_list);
	Digit_2_Ascii[3] = var_mapping(_T("Digit_2_Ascii3"), var_list);
	Digit_2_Ascii[4] = var_mapping(_T("Digit_2_Ascii4"), var_list);
	Digit_2_Ascii[5] = var_mapping(_T("Digit_2_Ascii5"), var_list);
	Digit_2_Ascii[6] = var_mapping(_T("Digit_2_Ascii6"), var_list);
	Digit_2_Ascii[7] = var_mapping(_T("Digit_2_Ascii7"), var_list);
	Digit_2_Ascii[8] = var_mapping(_T("Digit_2_Ascii8"), var_list);
	Digit_2_Ascii[9] = var_mapping(_T("Digit_2_Ascii9"), var_list);
	Digit_2_Ascii[10] = var_mapping(_T("Digit_2_Ascii10"), var_list);

	String_OverFlow = var_mapping(_T("String_OverFlow"), var_list);
	//===========================================================================================================
/*
	// Now that we got through the command line arguments, lets set things up before we start testing.
    // REGULAR
    _tcscpy( ExecSQLStr[ 0 ],  _T("DROP TABLE ROWSET_TABLE CASCADE") );
    _tcscpy( ExecSQLStr[ 1 ],  _T("CREATE TABLE ROWSET_TABLE ( C01 CHAR( 20 ) CHARACTER SET ISO88591 NOT NULL, C02 CHAR( 20 ) CHARACTER SET UCS2, C03 VARCHAR( 20 ) CHARACTER SET ISO88591, C04 VARCHAR( 20 ) CHARACTER SET UCS2, C05 LONG VARCHAR( 20 ) CHARACTER SET ISO88591, C06 LONG VARCHAR( 20 ) CHARACTER SET UCS2, C07 NCHAR( 20 ), C08 NCHAR VARYING( 20 ), C09 DECIMAL (8, 0) SIGNED, C10 DECIMAL (8, 0) UNSIGNED, C11 NUMERIC (8, 0) SIGNED, C12 NUMERIC (8, 0) UNSIGNED, C13 TINYINT SIGNED, C14 TINYINT UNSIGNED, C15 SMALLINT SIGNED, C16 SMALLINT UNSIGNED, C17 INTEGER SIGNED NOT NULL, C18 INTEGER UNSIGNED, C19 LARGEINT NOT NULL NOT DROPPABLE, C20 REAL, C21 FLOAT(54), C22 DOUBLE PRECISION, C23 DATE, C24 TIME, C25 TIMESTAMP, C26 INTERVAL YEAR, C27 INTERVAL MONTH, C28 INTERVAL DAY, C29 INTERVAL HOUR, C30 INTERVAL MINUTE, C31 INTERVAL SECOND, C32 INTERVAL YEAR TO MONTH, C33 INTERVAL DAY TO HOUR, C34 INTERVAL DAY TO MINUTE, C35 INTERVAL DAY TO SECOND, C36 INTERVAL HOUR TO MINUTE, C37 INTERVAL HOUR TO SECOND, C38 INTERVAL MINUTE TO SECOND, C39 NUMERIC (19, 0) SIGNED, C40 NUMERIC (19, 0) UNSIGNED, PRIMARY KEY ( C19 ), CONSTRAINT C17C CHECK ( C17 < 50000 ) )") );
    _tcscpy( ExecSQLStr[ 2 ],  _T("INSERT INTO ROWSET_TABLE ( C01, C02, C03, C04, C05, C06, C07, C08, C09, C10, C11, C12, C13, C14, C15, C16, C17, C18, C19, C20, C21, C22, C23, C24, C25, C26, C27, C28, C29, C30, C31, C32, C33, C34, C35, C36, C37, C38, C39, C40 ) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )") );
    _tcscpy( ExecSQLStr[ 3 ],  _T("SELECT * FROM ROWSET_TABLE ORDER BY C19") );
    _tcscpy( ExecSQLStr[ 4 ],  _T("DELETE FROM ROWSET_TABLE") );
    _tcscpy( ExecSQLStr[ 5 ],  _T("DELETE FROM ROWSET_TABLE WHERE CURRENT OF TABLECURSOR") );
    _tcscpy( ExecSQLStr[ 6 ],  _T("DELETE FROM ROWSET_TABLE WHERE C01 = ? AND C03 = ? AND C05 = ? AND C06 = ? AND C07 = ? AND C08 = ?") );
    //_tcscpy( ExecSQLStr[ 7 ],  _T("UPDATE ROWSET_TABLE SET C01=?, C02=?, C03=?, C04 = ?, C05=?, C06=?, C07=?, C08 = ?, C09=?, C10=?, C11=?, C12 = ?, C13=?, C14=?, C15=?, C16 = ?, C17 = ? + 1, C18=?, C20=?, C21 = ?, C22=?, C23=?, C24=?, C25 = ?, C26=?, C27=?, C28=?, C29 = ?, C30=?, C31=?, C32=?, C33 = ?, C34 = ?, C35 = ?, C36 = ?, C37 = ?, C38 = ?, C39 = ?, C40 = ? WHERE C19 = ?") );
    _tcscpy( ExecSQLStr[ 7 ],  _T("UPDATE ROWSET_TABLE SET C01=?, C02=?, C03=?, C04 = ?, C05=?, C06=?, C07=?, C08 = ?, C09=?, C10=?, C11=?, C12 = ?, C13=?, C14=?, C15=?, C16 = ?, C17 = ?, C18=?, C20=?, C21 = ?, C22=?, C23=?, C24=?, C25 = ?, C26=?, C27=?, C28=?, C29 = ?, C30=?, C31=?, C32=?, C33 = ?, C34 = ?, C35 = ?, C36 = ?, C37 = ?, C38 = ?, C39 = ?, C40 = ? WHERE C19 = ?") );
    // No parition table.
    _tcscpy( ExecSQLStr[ 8 ],  _T("CREATE TABLE ROWSET_TABLE ( C01 CHAR( 20 ) CHARACTER SET ISO88591 NOT NULL, C02 CHAR( 20 ) CHARACTER SET UCS2, C03 VARCHAR( 20 ) CHARACTER SET ISO88591, C04 VARCHAR( 20 ) CHARACTER SET UCS2, C05 LONG VARCHAR( 20 ) CHARACTER SET ISO88591, C06 LONG VARCHAR( 20 ) CHARACTER SET UCS2, C07 NCHAR( 20 ), C08 NCHAR VARYING( 20 ), C09 DECIMAL (8, 0) SIGNED, C10 DECIMAL (8, 0) UNSIGNED, C11 NUMERIC (8, 0) SIGNED, C12 NUMERIC (8, 0) UNSIGNED, C13 TINYINT SIGNED, C14 TINYINT UNSIGNED, C15 SMALLINT SIGNED, C16 SMALLINT UNSIGNED, C17 INTEGER SIGNED NOT NULL, C18 INTEGER UNSIGNED, C19 LARGEINT NOT NULL NOT DROPPABLE, C20 REAL, C21 FLOAT(54), C22 DOUBLE PRECISION, C23 DATE, C24 TIME, C25 TIMESTAMP, C26 INTERVAL YEAR, C27 INTERVAL MONTH, C28 INTERVAL DAY, C29 INTERVAL HOUR, C30 INTERVAL MINUTE, C31 INTERVAL SECOND, C32 INTERVAL YEAR TO MONTH, C33 INTERVAL DAY TO HOUR, C34 INTERVAL DAY TO MINUTE, C35 INTERVAL DAY TO SECOND, C36 INTERVAL HOUR TO MINUTE, C37 INTERVAL HOUR TO SECOND, C38 INTERVAL MINUTE TO SECOND, C39 NUMERIC (19, 0) SIGNED, C40 NUMERIC (19, 0) UNSIGNED, PRIMARY KEY ( C19 ), CONSTRAINT C17C CHECK ( C17 < 50000 ) ) NO PARTITION ") );
    // HASH by table.
    _tcscpy( ExecSQLStr[ 9 ],  _T("CREATE TABLE ROWSET_TABLE ( C01 CHAR( 20 ) CHARACTER SET ISO88591 NOT NULL, C02 CHAR( 20 ) CHARACTER SET UCS2, C03 VARCHAR( 20 ) CHARACTER SET ISO88591, C04 VARCHAR( 20 ) CHARACTER SET UCS2, C05 LONG VARCHAR( 20 ) CHARACTER SET ISO88591, C06 LONG VARCHAR( 20 ) CHARACTER SET UCS2, C07 NCHAR( 20 ), C08 NCHAR VARYING( 20 ), C09 DECIMAL (8, 0) SIGNED, C10 DECIMAL (8, 0) UNSIGNED, C11 NUMERIC (8, 0) SIGNED, C12 NUMERIC (8, 0) UNSIGNED, C13 TINYINT SIGNED, C14 TINYINT UNSIGNED, C15 SMALLINT SIGNED, C16 SMALLINT UNSIGNED, C17 INTEGER SIGNED NOT NULL, C18 INTEGER UNSIGNED, C19 LARGEINT NOT NULL NOT DROPPABLE, C20 REAL, C21 FLOAT(54), C22 DOUBLE PRECISION, C23 DATE, C24 TIME, C25 TIMESTAMP, C26 INTERVAL YEAR, C27 INTERVAL MONTH, C28 INTERVAL DAY, C29 INTERVAL HOUR, C30 INTERVAL MINUTE, C31 INTERVAL SECOND, C32 INTERVAL YEAR TO MONTH, C33 INTERVAL DAY TO HOUR, C34 INTERVAL DAY TO MINUTE, C35 INTERVAL DAY TO SECOND, C36 INTERVAL HOUR TO MINUTE, C37 INTERVAL HOUR TO SECOND, C38 INTERVAL MINUTE TO SECOND, C39 NUMERIC (19, 0) SIGNED, C40 NUMERIC (19, 0) UNSIGNED, PRIMARY KEY ( C19 ), CONSTRAINT C17C CHECK ( C17 < 50000 ) ) HASH2 PARTITION BY ( C19 ) ") );
    // Surrogate key table.
    _tcscpy( ExecSQLStr[ 10 ], _T("CREATE TABLE ROWSET_TABLE ( C01 CHAR( 20 ) CHARACTER SET ISO88591 NOT NULL, C02 CHAR( 20 ) CHARACTER SET UCS2, C03 VARCHAR( 20 ) CHARACTER SET ISO88591, C04 VARCHAR( 20 ) CHARACTER SET UCS2, C05 LONG VARCHAR( 20 ) CHARACTER SET ISO88591, C06 LONG VARCHAR( 20 ) CHARACTER SET UCS2, C07 NCHAR( 20 ), C08 NCHAR VARYING( 20 ), C09 DECIMAL (8, 0) SIGNED, C10 DECIMAL (8, 0) UNSIGNED, C11 NUMERIC (8, 0) SIGNED, C12 NUMERIC (8, 0) UNSIGNED, C13 TINYINT SIGNED, C14 TINYINT UNSIGNED, C15 SMALLINT SIGNED, C16 SMALLINT UNSIGNED, C17 INTEGER SIGNED NOT NULL, C18 INTEGER UNSIGNED, C19 LARGEINT GENERATED BY DEFAULT AS IDENTITY NOT NULL NOT DROPPABLE, C20 REAL, C21 FLOAT(54), C22 DOUBLE PRECISION, C23 DATE, C24 TIME, C25 TIMESTAMP, C26 INTERVAL YEAR, C27 INTERVAL MONTH, C28 INTERVAL DAY, C29 INTERVAL HOUR, C30 INTERVAL MINUTE, C31 INTERVAL SECOND, C32 INTERVAL YEAR TO MONTH, C33 INTERVAL DAY TO HOUR, C34 INTERVAL DAY TO MINUTE, C35 INTERVAL DAY TO SECOND, C36 INTERVAL HOUR TO MINUTE, C37 INTERVAL HOUR TO SECOND, C39 NUMERIC (19, 0) SIGNED, C40 NUMERIC (19, 0) UNSIGNED, C38 INTERVAL MINUTE TO SECOND, PRIMARY KEY ( C19 ), CONSTRAINT C17C CHECK ( C17 < 50000 ) )") );
    // SET table
    _tcscpy( ExecSQLStr[ 11 ],  _T("CREATE SET TABLE ROWSET_TABLE ( C01 CHAR( 20 ) CHARACTER SET ISO88591 NOT NULL, C02 CHAR( 20 ) CHARACTER SET UCS2, C03 VARCHAR( 20 ) CHARACTER SET ISO88591, C04 VARCHAR( 20 ) CHARACTER SET UCS2, C05 LONG VARCHAR( 20 ) CHARACTER SET ISO88591, C06 LONG VARCHAR( 20 ) CHARACTER SET UCS2, C07 NCHAR( 20 ), C08 NCHAR VARYING( 20 ), C09 DECIMAL (8, 0) SIGNED, C10 DECIMAL (8, 0) UNSIGNED, C11 NUMERIC (8, 0) SIGNED, C12 NUMERIC (8, 0) UNSIGNED, C13 TINYINT SIGNED, C14 TINYINT UNSIGNED, C15 SMALLINT SIGNED, C16 SMALLINT UNSIGNED, C17 INTEGER SIGNED NOT NULL, C18 INTEGER UNSIGNED, C19 LARGEINT NOT NULL NOT DROPPABLE, C20 REAL, C21 FLOAT(54), C22 DOUBLE PRECISION, C23 DATE, C24 TIME, C25 TIMESTAMP, C26 INTERVAL YEAR, C27 INTERVAL MONTH, C28 INTERVAL DAY, C29 INTERVAL HOUR, C30 INTERVAL MINUTE, C31 INTERVAL SECOND, C32 INTERVAL YEAR TO MONTH, C33 INTERVAL DAY TO HOUR, C34 INTERVAL DAY TO MINUTE, C35 INTERVAL DAY TO SECOND, C36 INTERVAL HOUR TO MINUTE, C37 INTERVAL HOUR TO SECOND, C38 INTERVAL MINUTE TO SECOND, C39 NUMERIC (19, 0) SIGNED, C40 NUMERIC (19, 0) UNSIGNED, PRIMARY KEY ( C19 ), CONSTRAINT C17C CHECK ( C17 < 50000 ) )") );// NO PARTITION LOCATION $FC0300" );
    // MULTISET table
    _tcscpy( ExecSQLStr[ 12 ],  _T("CREATE MULTISET TABLE ROWSET_TABLE ( C01 CHAR( 20 ) CHARACTER SET ISO88591 NOT NULL, C02 CHAR( 20 ) CHARACTER SET UCS2, C03 VARCHAR( 20 ) CHARACTER SET ISO88591, C04 VARCHAR( 20 ) CHARACTER SET UCS2, C05 LONG VARCHAR( 20 ) CHARACTER SET ISO88591, C06 LONG VARCHAR( 20 ) CHARACTER SET UCS2, C07 NCHAR( 20 ), C08 NCHAR VARYING( 20 ), C09 DECIMAL (8, 0) SIGNED, C10 DECIMAL (8, 0) UNSIGNED, C11 NUMERIC (8, 0) SIGNED, C12 NUMERIC (8, 0) UNSIGNED, C13 TINYINT SIGNED, C14 TINYINT UNSIGNED, C15 SMALLINT SIGNED, C16 SMALLINT UNSIGNED, C17 INTEGER SIGNED NOT NULL, C18 INTEGER UNSIGNED, C19 LARGEINT NOT NULL NOT DROPPABLE, C20 REAL, C21 FLOAT(54), C22 DOUBLE PRECISION, C23 DATE, C24 TIME, C25 TIMESTAMP, C26 INTERVAL YEAR, C27 INTERVAL MONTH, C28 INTERVAL DAY, C29 INTERVAL HOUR, C30 INTERVAL MINUTE, C31 INTERVAL SECOND, C32 INTERVAL YEAR TO MONTH, C33 INTERVAL DAY TO HOUR, C34 INTERVAL DAY TO MINUTE, C35 INTERVAL DAY TO SECOND, C36 INTERVAL HOUR TO MINUTE, C37 INTERVAL HOUR TO SECOND, C38 INTERVAL MINUTE TO SECOND, C39 NUMERIC (19, 0) SIGNED, C40 NUMERIC (19, 0) UNSIGNED, PRIMARY KEY ( C19 ), CONSTRAINT C17C CHECK ( C17 < 50000 ) )") );
    // INSERT_SELECT
    _tcscpy( ExecSQLStr[ 13 ],  _T("CREATE TABLE TO_ROWSET_TABLE ( C01 CHAR( 20 ) CHARACTER SET ISO88591 NOT NULL, C02 CHAR( 20 ) CHARACTER SET UCS2, C03 VARCHAR( 20 ) CHARACTER SET ISO88591, C04 VARCHAR( 20 ) CHARACTER SET UCS2, C05 LONG VARCHAR( 20 ) CHARACTER SET ISO88591, C06 LONG VARCHAR( 20 ) CHARACTER SET UCS2, C07 NCHAR( 20 ), C08 NCHAR VARYING( 20 ), C09 DECIMAL (8, 0) SIGNED, C10 DECIMAL (8, 0) UNSIGNED, C11 NUMERIC (8, 0) SIGNED, C12 NUMERIC (8, 0) UNSIGNED, C13 TINYINT SIGNED, C14 TINYINT UNSIGNED, C15 SMALLINT SIGNED, C16 SMALLINT UNSIGNED, C17 INTEGER SIGNED NOT NULL, C18 INTEGER UNSIGNED, C19 LARGEINT NOT NULL NOT DROPPABLE, C20 REAL, C21 FLOAT(54), C22 DOUBLE PRECISION, C23 DATE, C24 TIME, C25 TIMESTAMP, C26 INTERVAL YEAR, C27 INTERVAL MONTH, C28 INTERVAL DAY, C29 INTERVAL HOUR, C30 INTERVAL MINUTE, C31 INTERVAL SECOND, C32 INTERVAL YEAR TO MONTH, C33 INTERVAL DAY TO HOUR, C34 INTERVAL DAY TO MINUTE, C35 INTERVAL DAY TO SECOND, C36 INTERVAL HOUR TO MINUTE, C37 INTERVAL HOUR TO SECOND, C38 INTERVAL MINUTE TO SECOND, C39 NUMERIC (19, 0) SIGNED, C40 NUMERIC (19, 0) UNSIGNED, PRIMARY KEY ( C19 ), CONSTRAINT C17T CHECK ( C17 < 50000 ) )") );
    _tcscpy( ExecSQLStr[ 14 ],  _T("INSERT INTO TO_ROWSET_TABLE SELECT * FROM ROWSET_TABLE WHERE C19 = ?") );
    _tcscpy( ExecSQLStr[ 15 ],  _T("DROP TABLE TO_ROWSET_TABLE CASCADE") );
	// Index
    _tcscpy( ExecSQLStrIndex[ 0 ], _T("CREATE INDEX INDEX_C01 ON ROWSET_TABLE( C19 )") );
    _tcscpy( ExecSQLStrIndex[ 1 ], _T("DROP INDEX INDEX_C01 CASCADE") );
    // RI
    _tcscpy( ExecSQLStrRI[ 0 ], _T("CONTROL QUERY DEFAULT REF_CONSTRAINT_NO_ACTION_LIKE_RESTRICT 'ON'") );
    _tcscpy( ExecSQLStrRI[ 1 ], _T("CREATE TABLE ROWSET_TABLE_2 LIKE ROWSET_TABLE") );
    _tcscpy( ExecSQLStrRI[ 2 ], _T("ALTER TABLE ROWSET_TABLE ADD CONSTRAINT CC7 FOREIGN KEY( C01 ) REFERENCES ROWSET_TABLE_2( C01)") );
    _tcscpy( ExecSQLStrRI[ 3 ], _T("DROP TABLE ROWSET_TABLE_2 CASCADE") );
    // Volatile
    _tcscpy( ExecSQLStrVolatile[ 0 ], _T("CREATE VOLATILE TABLE ROWSET_TABLE ( C01 CHAR( 20 ) CHARACTER SET ISO88591 NOT NULL, C02 CHAR( 20 ) CHARACTER SET UCS2, C03 VARCHAR( 20 ) CHARACTER SET ISO88591, C04 VARCHAR( 20 ) CHARACTER SET UCS2, C05 LONG VARCHAR( 20 ) CHARACTER SET ISO88591, C06 LONG VARCHAR( 20 ) CHARACTER SET UCS2, C07 NCHAR( 20 ), C08 NCHAR VARYING( 20 ), C09 DECIMAL (8, 0) SIGNED, C10 DECIMAL (8, 0) UNSIGNED, C11 NUMERIC (8, 0) SIGNED, C12 NUMERIC (8, 0) UNSIGNED, C13 TINYINT SIGNED, C14 TINYINT UNSIGNED, C15 SMALLINT SIGNED, C16 SMALLINT UNSIGNED, C17 INTEGER SIGNED NOT NULL, C18 INTEGER UNSIGNED, C19 LARGEINT NOT NULL NOT DROPPABLE, C20 REAL, C21 FLOAT(54), C22 DOUBLE PRECISION, C23 DATE, C24 TIME, C25 TIMESTAMP, C26 INTERVAL YEAR, C27 INTERVAL MONTH, C28 INTERVAL DAY, C29 INTERVAL HOUR, C30 INTERVAL MINUTE, C31 INTERVAL SECOND, C32 INTERVAL YEAR TO MONTH, C33 INTERVAL DAY TO HOUR, C34 INTERVAL DAY TO MINUTE, C35 INTERVAL DAY TO SECOND, C36 INTERVAL HOUR TO MINUTE, C37 INTERVAL HOUR TO SECOND, C38 INTERVAL MINUTE TO SECOND, C39 NUMERIC (19, 0) SIGNED, C40 NUMERIC (19, 0) UNSIGNED, PRIMARY KEY ( C19 ) ) ") );
    _tcscpy( ExecSQLStrVolatile[ 1 ], _T("DROP VOLATILE TABLE ROWSET_TABLE CASCADE ") );
    // MVS
    _tcscpy( ExecSQLStrMVS[ 0 ], _T("ALTER TABLE ROWSET_TABLE ATTRIBUTE ALL MVS ALLOWED") );
    _tcscpy( ExecSQLStrMVS[ 1 ], _T("CREATE TABLE ROWSET_TABLE_ALT ( C01 CHAR( 20 ) NOT NULL, C17 INTEGER SIGNED, C19 LARGEINT NOT NULL NOT DROPPABLE, PRIMARY KEY ( C19 ), CONSTRAINT C17AC CHECK ( C17 < 50000 ) )") );
    _tcscpy( ExecSQLStrMVS[ 2 ], _T("CREATE VIEW VIEW_ROWSET_TABLE AS SELECT A.C01 AS AC01, A.C17 AS AC17, A.C19 AS AC19, B.C01 AS BC01, B.C17 AS BC17, B.C19 AS BC19 FROM ROWSET_TABLE A, ROWSET_TABLE_ALT B WHERE A.C19 = B.C19;") );
    _tcscpy( ExecSQLStrMVS[ 3 ], _T("CREATE MV MVS_ROWSET_TABLE REFRESH ON STATEMENT INITIALIZE ON CREATE AS SELECT A.C01 AS AC01, A.C17 AS AC17, A.C19 AS AC19, B.C01 AS BC01, B.C17 AS BC17, B.C19 AS BC19 FROM ROWSET_TABLE A, ROWSET_TABLE_ALT B WHERE A.C19 = B.C19;") );
    _tcscpy( ExecSQLStrMVS[ 4 ], _T("DROP VIEW VIEW_ROWSET_TABLE CASCADE;") );
    _tcscpy( ExecSQLStrMVS[ 5 ], _T("DROP MV MVS_ROWSET_TABLE CASCADE;") );
    _tcscpy( ExecSQLStrMVS[ 6 ], _T("DROP TABLE ROWSET_TABLE_ALT CASCADE;") );
    // Before Trigger
    _tcscpy( ExecSQLStrBeforeTrigger[ 0 ], _T("DROP TRIGGER ROWSET_BEFORETRIGER;") );
    _tcscpy( ExecSQLStrBeforeTrigger[ 1 ], _T("CREATE TRIGGER ROWSET_BEFORETRIGER BEFORE INSERT ON ROWSET_TABLE REFERENCING NEW AS NEWROW FOR EACH ROW WHEN (NEWROW.C19 > 0 ) SET NEWROW.C39 = 987654321098765, NEWROW.C40=987654321098765;") );
    // AfterTrigger
    _tcscpy( ExecSQLStrAfterTrigger[ 0 ], _T("DROP TRIGGER ROWSET_AFTERTRIGER;") );
    _tcscpy( ExecSQLStrAfterTrigger[ 1 ], _T("DROP TABLE ROWSET_TABLE_TMP CASCADE") );
    _tcscpy( ExecSQLStrAfterTrigger[ 2 ], _T("CREATE TRIGGER ROWSET_AFTERTRIGER AFTER INSERT ON ROWSET_TABLE REFERENCING NEW AS NEWROW FOR EACH ROW WHEN ( NEWROW.C19 > 5 ) INSERT INTO ROWSET_TABLE_TMP VALUES ( NEWROW.C01,NEWROW.C17,NEWROW.C19 );") );
    _tcscpy( ExecSQLStrAfterTrigger[ 3 ], _T("CREATE TABLE ROWSET_TABLE_TMP ( C01 CHAR( 20 ) NOT NULL, C17 INTEGER SIGNED, C19 LARGEINT NOT NULL NOT DROPPABLE, PRIMARY KEY ( C19 ), CONSTRAINT C17AT CHECK ( C17 < 50000 ) )") );
*/
	//===========================================================================================================

	RecordToLog( _T(" Rowsets using DS: %s\n\t User: %s\n\t Password: %s\n"), datasource, uid, password);

    RecordToLog( _T(" > Initializing ODBC handles and connection.\n") );

	// start for ALM log
	RecordTo_ALM_Log(_T(""));
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

           RecordToLog( _T("Running test %d of %d.\n"), testCount, testTotal );
        
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

#ifdef DEBUG_PRINT /* SQ */
            PrintTestInformation( );
#endif /* SEAQEUST */
			
			/***** ALM Log begin *****/
			ALM_TestInformation(ALM_NextTestInfo);
			if (wcscmp (ALM_NextTestInfo,Heading) != 0)
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

				wcscpy (Heading, ALM_NextTestInfo);
				ALM_Test_start = time( NULL);
				/* Log into ALM report as well */
				swprintf(ALM_TestCaseId, 12, _T("Test%d"),ALM_testCounter);
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
                    RecordToLog( _T(" > Binding parameters.\n") );
                    if( !BindParameters( ) )
                    {
                        RecordToLog( _T("....FAILED!....\n") );

						/***** ALM Log begin *****/
						_TestCase=FAILED;
						/***** ALM Log end *****/

						testFail++;
                        break;
                    }
               
                    switch( actions[ unitTest.action ] )
                    {
                        case INSERT:
                            RecordToLog( _T(" > Inserting rows.\n") );
                            break;
                        case DELETE_PARAM:
                            RecordToLog( _T(" > Deleting rows.\n") );
                            break;
                        case UPDATE:
                            RecordToLog( _T(" > Updating rows.\n") );
                            break;
                        case INSERT_SELECT:
                            RecordToLog( _T(" > Inserting Select rows.\n") );
                            break;
                    }
                    if( !RowsetDML( ) ) 
                    {
                        RecordToLog( _T("....FAILED!....\n") );

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
                    RecordToLog( _T(" > Binding columns.\n") );
                    if( !BindCols( ) )
                    {
                        RecordToLog( _T("....FAILED!....\n") );

						/***** ALM Log begin *****/
						_TestCase=FAILED;
						/***** ALM Log end *****/

                        testFail++;
                        break;
                    }
                
                    RecordToLog( _T(" > Inserting bulk rows.\n") );

                    if( !RowsetDMLBulk( ) ) 
                    {
                        RecordToLog( _T("....FAILED!....\n") );

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
                    RecordToLog( _T(" > Binding columns.\n") );
                    if( !BindCols( ) )
                    {
                        RecordToLog( _T("....FAILED!....\n") );

						/***** ALM Log begin *****/
						_TestCase=FAILED;
						/***** ALM Log end *****/

                        testFail++;
                        break;
                    }
                    // Fetch the rows from the table.
                    RecordToLog( _T(" > Fetching rows.\n") );
                    if( !RowsetFetch( ) ) 
                    {
                        RecordToLog( _T("....FAILED!....\n") );

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
                    RecordToLog( _T(" > INTERNAL ERROR: An unknown testing action has been discovered.\n") );
            }

            if( actions[ unitTest.action ] == INSERT_SELECT )
            {
                RecordToLog( _T(" > Cleaning up select table.\n") );
                DeleteRows( );
            }
        
            if( actions[ unitTest.action ] == DELETE_PARAM )
            {
                RecordToLog( _T(" > Cleaning up table.\n") );
                DeleteRows( );
            }

            RecordToLog( _T(" > Free handles.\n") );
            FreeHandles( );

            // We don't want to run any more tests for single tests.
            if( singleTest )
            {
                break;
            }
        } // NextTest

		DropTable();

		RecordToLog( _T(" > Releasing handles.\n") );
        DeleteHandles( );

    } // EstablishHandlesAndConnection

	// ALM reporting the last sets of test cases
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
    RecordToLog( _T("Test count: %d\n"), testCount );
    RecordToLog( _T("Test fail:  %d\n"), testFail );
    RecordToLog( _T("Test pass:  %d\n"), testPass );
	/* SQ */
	if (testFail)
		RecordToLog( _T("rowsets TEST RESULT: FAIL\n"));
	else
		RecordToLog( _T("rowsets TEST RESULT: PASS\n"));
    /* end of SQ */

    if( timeMetrics )
        DisplayTimeMetrics( );

	free_list(var_list);
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

    // A after trigger cannot be created on volatile tables
	if( ( tableTypes[ unitTest.tableType ] == VOLATILE ) && ( tableFeatures[ unitTest.tableFeature ] == AFTERTRIGGER ) )
    {
        return true;
    }

    // A after trigger cannot be created on volatile tables
	if( ( tableTypes[ unitTest.tableType ] == VOLATILE ) && ( tableFeatures[ unitTest.tableFeature ] == BEFORETRIGGER ) )
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
        CheckMsgs( _T("SQLAllocHandle()"), __LINE__ );
        return false;
    }

    // Set the environment variable to ODBC version 3
    retcode = SQLSetEnvAttr( handle[ SQL_HANDLE_ENV ], SQL_ATTR_ODBC_VERSION, (SQLPOINTER)SQL_OV_ODBC3, 0 ); 
    if( retcode != SQL_SUCCESS )    
    {
        CheckMsgs( _T("SQLSetEnvAttr()"), __LINE__ );
        DeleteHandles( );
        return false;
    }

    // Allocate the connection handle off the environment handle.
    retcode = SQLAllocHandle( SQL_HANDLE_DBC, handle[ SQL_HANDLE_ENV ], &handle[ SQL_HANDLE_DBC ] ); 
    if( retcode != SQL_SUCCESS )    
    {
        CheckMsgs( _T("SQLAllocHandle()"), __LINE__ );
        DeleteHandles( );
        return false;
    }

    // The HASH2 feature requires specific connection attributes established before connecting.
    if( features[ unitTest.feature ] == HASH2 )
    {
        RecordToLog( _T(" >> Setting up SQL_MODE_LOADER.\n") );
        SQLUINTEGER mode = 1;
        SQLUINTEGER SQL_MODE_LOADER = 4001;
        retcode = SQLSetConnectAttr( handle[ SQL_HANDLE_DBC ], SQL_MODE_LOADER, (void *)mode, 0);
        if( retcode != SQL_SUCCESS )    
        {
            CheckMsgs( _T("SQLSetConnectAttr()"), __LINE__ );
            DeleteHandles( );
            return false;
        }

        RecordToLog( _T(" >> Setting up SQL_START_NODE.\n") );
        SQLUINTEGER startnode = 5;
        SQLUINTEGER SQL_START_NODE = 4000;
        retcode = SQLSetConnectAttr( handle[ SQL_HANDLE_DBC ], SQL_START_NODE, (void *) startnode, 0);
        if( retcode != SQL_SUCCESS )    
        {
            CheckMsgs( _T("SQLSetConnectAttr()"), __LINE__ );
            DeleteHandles( );
            return false;
        }

        RecordToLog( _T(" >> Setting up SQL_STREAMS_PER_SEG.\n") );
        SQLUINTEGER streams_per_node = 1;
        SQLUINTEGER SQL_STREAMS_PER_SEG = 4002;
        retcode = SQLSetConnectAttr( handle[ SQL_HANDLE_DBC ], SQL_STREAMS_PER_SEG, (void *) streams_per_node, 0 );
        if( retcode != SQL_SUCCESS )    
        {
            CheckMsgs( _T("SQLSetConnectAttr()"), __LINE__ );
            DeleteHandles( );
            return false;
        }

    }

    // Connect to the ODBC service.
    retcode = SQLConnect( handle[ SQL_HANDLE_DBC ], (SQLTCHAR*) datasource, SQL_NTS,
                          (SQLTCHAR*) uid, SQL_NTS, (SQLTCHAR*) password, SQL_NTS );
    if( retcode != SQL_SUCCESS && retcode != SQL_SUCCESS_WITH_INFO )    
    {
        CheckMsgs( _T("SQLConnect()"), __LINE__ );
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
            CheckMsgs( _T("SQLSetConnectAttr()"), __LINE__ );
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
        CheckMsgs( _T("SQLAllocHandle()"), __LINE__ );
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
            CheckMsgs( _T("SQLSetStmtAttr()"), __LINE__ );
            SQLDisconnect( handle[ SQL_HANDLE_DBC ] );
            DeleteHandles( );
            return false;
        }
    }

    // Here we need to turn for MODE_SPECIAL_1. This CQD changes the status array of
    // rowsets. We can not change this CQD as it's a read only CQD for the system.
    RecordToLog( _T(" >> Checking for MODE_SPECIAL_1=") );
    if( _tcsncmp( CheckForCQD( _T("MODE_SPECIAL_1  ") ), _T("ON"), 2 ) == 0 )
    {
        errorChecking = MODE_SPECIAL_1;
		RecordToLog( _T("ON\n") );
    }
    else
    {
        errorChecking = STANDARD;
		RecordToLog( _T("OFF\n") );
    }

    RecordToLog( _T(" >> Finished connecting to server.\n") );
    retcode = SQLFreeStmt( handle[ SQL_HANDLE_STMT ], SQL_CLOSE ); // Free and clearup the statement handle.
    if( retcode != SQL_SUCCESS )    
    {
        CheckMsgs( _T("SQLFreeStmt()"), __LINE__ );
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
            RecordToLog( _T(" >> Creating select table. \n") );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStr[ 13 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            if( retcode != SQL_SUCCESS )    
            {
                CheckMsgs( _T("SQLExecDirect()"), __LINE__ );
                DeleteHandles( );
                return false;
            }

            retcode = SQLFreeStmt( handle[ SQL_HANDLE_STMT ], SQL_CLOSE ); // Free and clearup the statement handle.
            if( retcode != SQL_SUCCESS )    
            {
                CheckMsgs( _T("SQLFreeStmt()"), __LINE__ );
                DeleteHandles( );
                return false;
            }

            return true;
    }

    switch( tableTypes[ unitTest.tableType ] )
    {
        case POSOFF:
            RecordToLog( _T(" >> Creating no partition table. \n") );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStr[ 8 ], SQL_NTS ) ) == SQL_STILL_EXECUTING ); // Create the table.
            break;
        case SURROGATE:
            RecordToLog( _T(" >> Creating surrogate key table. \n") );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStr[ 9 ], SQL_NTS ) ) == SQL_STILL_EXECUTING ); // Create the table.
            break;
        case VOLATILE:
            RecordToLog( _T(" >> Creating volatile table. \n") );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrVolatile[ 0 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            break;
        case SET:
            RecordToLog( _T(" >> Creating set table. \n") );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStr[ 11 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            break;
        case MULTISET:
            RecordToLog( _T(" >> Creating multiset table. \n") );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStr[ 12 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            break;
        case REGULAR:
        default:
            if( features[ unitTest.feature ] == HASH2 )
            {
                RecordToLog( _T(" >> Creating HASH2 table. \n") );
                while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStr[ 9 ], SQL_NTS ) ) == SQL_STILL_EXECUTING ); // Create the table.
            }
            else
            {
                RecordToLog( _T(" >> Creating standard table. \n") );
                while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStr[ 1 ], SQL_NTS ) ) == SQL_STILL_EXECUTING ); // Create the table.
            }
            break;
    }

    switch( tableFeatures[ unitTest.tableFeature ] )
    {
        case INDEX:
            RecordToLog( _T(" >> Creating index. \n") );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrIndex[ 0 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            break;
        case MVS:
            RecordToLog( _T(" >> MVS setup on standard table. \n") );
            RecordToLog( _T("   >> Allowing MVS on standard table. \n") );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrMVS[ 0 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            if( retcode != SQL_SUCCESS )    
            {
                CheckMsgs( _T("SQLExecDirect()"), __LINE__ );
                return false;
            }
            RecordToLog( _T("   >> Creating an alternative table. \n") );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrMVS[ 1 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            if( retcode != SQL_SUCCESS )    
            {
                CheckMsgs( _T("SQLExecDirect()"), __LINE__ );
                return false;
            }
            RecordToLog( _T("   >> Creating a view on standard and alternative table. \n") );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrMVS[ 2 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            if( retcode != SQL_SUCCESS )    
            {
                CheckMsgs( _T("SQLExecDirect()"), __LINE__ );
                return false;
            }
            RecordToLog( _T("   >> Creating MVS on standard and alternative table. \n") );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrMVS[ 3 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            if( retcode != SQL_SUCCESS )    
            {
                CheckMsgs( _T("SQLExecDirect()"), __LINE__ );
                return false;
            }
            break;
        case RI:
            RecordToLog( _T(" >> Initializing CQD. \n") );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrRI[ 0 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            if( retcode != SQL_SUCCESS )    
            {
                CheckMsgs( _T("SQLExecDirect()"), __LINE__ );
                return false;
            }
            RecordToLog( _T(" >> Creating LIKE table. \n") );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrRI[ 1 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            if( retcode != SQL_SUCCESS )    
            {
                CheckMsgs( _T("SQLExecDirect()"), __LINE__ );
                return false;
            }
            RecordToLog( _T(" >> Creating referential constraint. \n") );
            while ( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrRI[ 2 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            break;
        case BEFORETRIGGER:
            RecordToLog( _T(" >> Before trigger setup on standard table. \n") );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrBeforeTrigger[ 1 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            if( retcode != SQL_SUCCESS )    
            {
                CheckMsgs( _T("SQLExecDirect()"), __LINE__ );
                return false;
            }
            break;
        case AFTERTRIGGER:
            RecordToLog( _T(" >> After trigger tmp table. \n") );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrAfterTrigger[ 3 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            if( retcode != SQL_SUCCESS )    
            {
                CheckMsgs( _T("SQLExecDirect()"), __LINE__ );
                return false;
            }
            RecordToLog( _T(" >> After trigger setup on standard table.\n") );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrAfterTrigger[ 2 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            if( retcode != SQL_SUCCESS )    
            {
                CheckMsgs( _T("SQLExecDirect()"), __LINE__ );
                return false;
            }
            break;
        default:
            break;
    }

	if( ( retcode != SQL_SUCCESS ) && ( retcode != SQL_SUCCESS_WITH_INFO ) && ( !singleTest ) )    
    {
        CheckMsgs( _T("SQLExecDirect()"), __LINE__ );
        DeleteHandles( );
        return false;
    }

    if( features[ unitTest.feature ] != HASH2 && 
        retcode == SQL_SUCCESS )
    {
        RecordToLog( _T(" >> Committing transaction.\n") );
        retcode = SQLEndTran( SQL_HANDLE_DBC, handle[ SQL_HANDLE_DBC ], SQL_COMMIT ); // Commit the transaction.
        if( retcode != SQL_SUCCESS )    
        {
            CheckMsgs( _T("SQLEndTran()"), __LINE__ );
            DeleteHandles( );
            return false;
        }
    }

    retcode = SQLFreeStmt( handle[ SQL_HANDLE_STMT ], SQL_CLOSE ); // Free and clearup the statement handle.
    if( retcode != SQL_SUCCESS )    
    {
        CheckMsgs( _T("SQLFreeStmt()"), __LINE__ );
        DeleteHandles( );
        return false;
    }

    return true;
}

/* Function          : IgnoreMsg
   Calling Arguments : SQLTCHAR* : The ODBC state to ignore. 10 byte string.
                       SQWORD   : The ODBC native error to ignore.
   Return Arguments  : none

   Description:
   This function populates a data structure on what messages to ignore when a
   API call fails. This happens from time to time depending on the scenario
   the tests under takes. Example, deleting a table at the start of the test
   when no table exists.
   
 */
void IgnoreMsg( SQLTCHAR *state, SDWORD nativeError )
{
    // We only store a limited number of error messages to ignore. 
    if( ignoreCount == NUMBER_OF_IGNORES )
        return;

    // Store off the information.
    _tcsncpy( (TCHAR*)ignoreState[ ignoreCount ], (TCHAR*)state, 10 );
    ignoreNativeError[ ignoreCount ] = nativeError;
    ignoreCount++;

    return;
}

/* Function          : ShouldIgnoreMsg
   Calling Arguments : SQLTCHAR* : The ODBC state. 10 byte string.
                       SQWORD   : The ODBC native error.
   Return Arguments  : true : Ignore the error message.
                       false : Do not ignore the error message.

   Description:
   This checks to see if the program should or should not ignore the error 
   message being returned from ODBC.   
 */
bool ShouldIgnoreMsg( SQLTCHAR *state, SDWORD nativeError )
{
    for( int loop = 0; loop != ignoreCount; loop++ )
    {
        if( ( _tcscmp( (TCHAR*)ignoreState[ loop ], (TCHAR*)state ) == 0 ) &&
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
int CheckMsgs( TCHAR* sqlFunction, int lineNumber ) 
{
    SQLRETURN  retcode;       // Used to gather the return value of all ODBC API calls.
    SQLTCHAR szSqlState[ 10 ];
    SDWORD NativeError;
    SQLTCHAR szErrorMsg[ 1024 ];
    SQLTCHAR SavedErrorMsg[ 1024 ];
    int errorRepetionCount = 0;
    SWORD ErrorMsg;
    SQLSMALLINT recordNumber = -1;
    int reportedErrorMsg = NO_ERROR_FND;

    _tcscpy( (TCHAR *)SavedErrorMsg, _T("EMPTY") );

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
                            RecordToLog( _T(" >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n") );
                        }
                        if( _tcscmp( (TCHAR *)szErrorMsg, (TCHAR *)SavedErrorMsg ) != 0 )
                        {
                            RecordToLog( _T(" >>> State: %s\n"),        (TCHAR*)szSqlState );
                            RecordToLog( _T(" >>> Native Error: %d\n"), (int)NativeError );
                            RecordToLog( _T(" >>> Message: %s\n"),      (TCHAR*)szErrorMsg );
                            _tcsncpy( (TCHAR *)SavedErrorMsg, (TCHAR *)szErrorMsg, 1023 );
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
                            RecordToLog( _T(" >>> (The above error message was repeated %d times.)\n"), errorRepetionCount );
                        else if( _tcscmp( (TCHAR *)szErrorMsg, (TCHAR *)SavedErrorMsg ) != 0 )
                        {
                            RecordToLog( _T(" >>> (The above error message was repeated %d times.)\n"), errorRepetionCount );
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
        RecordToLog( _T(" >>> The error messages from above were from  %s located at %s on line %d\n"), sqlFunction, _T(__FILE__), lineNumber );
        RecordToLog( _T(" >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n") );
    }
    else if( reportedErrorMsg != IGNORE_ERROR )
    {
        RecordToLog( _T(" >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n") );
        RecordToLog( _T(" >>> WARNING NO MESSAGES RETRIEVED FROM ODBC DRIVER\n") );
        RecordToLog( _T(" >>> This was from  %s located at %s on line %d\n"), sqlFunction, _T(__FILE__), lineNumber );
        RecordToLog( _T(" >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n") );
        //exit(1);
    }

    return reportedErrorMsg;
}

void CheckMsgsNoIgnored() 
{
    SQLRETURN  retcode;
    SQLTCHAR szSqlState[ 10 ];
    SDWORD NativeError;
    SQLTCHAR szErrorMsg[ 1024 ];
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
                    RecordToLog( _T(" >>> State: %s\n"),        (TCHAR*)szSqlState );
                    RecordToLog( _T(" >>> Native Error: %d\n"), (int)NativeError );
                    RecordToLog( _T(" >>> Message: %s\n"),      (TCHAR*)szErrorMsg );

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
        CheckMsgs( _T("SQLFreeStmt()"), __LINE__ );
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

    RecordToLog( _T(" >> Cleaning up table. \n") );
    while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStr[ 4 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );//Delete all rows in table

    if( retcode != SQL_SUCCESS )    
    {
        ClearIgnore( );
        DeleteHandles( );
        return false;
    }

	if (tableFeatures[unitTest.tableFeature] == AFTERTRIGGER) {
        RecordToLog( _T(" >> Clean up temp trigger table.\n") );
	    while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrAfterTrigger[ 4 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );//Delete all rows in temp trigger table
        if( retcode != SQL_SUCCESS )    
        {
            CheckMsgs( _T("SQLExecDirect()"), __LINE__ );
            ClearIgnore( );
            DeleteHandles( );
            return false;
        }
	}

    if( features[ unitTest.feature ] != HASH2 )
    {
        RecordToLog( _T(" >> Committing transaction.\n") );
        retcode = SQLEndTran( SQL_HANDLE_DBC, handle[ SQL_HANDLE_DBC ], SQL_COMMIT ); // Commit the transaction.
        if( retcode != SQL_SUCCESS )    
        {
            CheckMsgs( _T("SQLEndTran()"), __LINE__ );
            ClearIgnore( );
            DeleteHandles( );
            return false;
        }
    }

    retcode = SQLFreeStmt( handle[ SQL_HANDLE_STMT ], SQL_CLOSE ); // Free and clearup the statement handle.
    if( retcode != SQL_SUCCESS )    
    {
        CheckMsgs( _T("SQLFreeStmt()"), __LINE__ );
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

    IgnoreMsg( (SQLTCHAR*)_T("01000"), 0 ); // Ignore the warning message connect to default DataSource.
    IgnoreMsg( (SQLTCHAR*)_T("X0104"), -1004 ); // Ignore the table does not exist.
    IgnoreMsg( (SQLTCHAR*)_T("X010V"), -1031 ); // Ignore the table can not be dropped.
    IgnoreMsg( (SQLTCHAR*)_T("X0106"), -1006 ); // Ignore the index does not exist.

    if( actions[ unitTest.action ] == INSERT_SELECT )
    {
        RecordToLog( _T(" >> Droping select table. \n") );
        while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStr[ 15 ], SQL_NTS ) ) == SQL_STILL_EXECUTING ); 
        return true;
    }

    switch( tableFeatures[ unitTest.tableFeature ] )
    {
        case INDEX:
            RecordToLog( _T(" >> Droping index. \n") );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrIndex[ 1 ], SQL_NTS ) ) == SQL_STILL_EXECUTING ); 
            break;
        case MVS:
            RecordToLog( _T(" >> Droping MVS table. \n") );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrMVS[ 4 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrMVS[ 5 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrMVS[ 6 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            break;
        case RI:
            RecordToLog( _T(" >> Droping referential constraint. \n") );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrRI[ 3 ], SQL_NTS ) ) == SQL_STILL_EXECUTING ); 
            if( retcode != SQL_SUCCESS )    
            {
                CheckMsgs( _T("SQLExecDirect()"), __LINE__ );
                ClearIgnore( );
                DeleteHandles( );
                return false;
            }
            break;
        case BEFORETRIGGER:
            RecordToLog( _T(" >> Droping before trigger. \n") );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrBeforeTrigger[ 0 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            break;
        case AFTERTRIGGER:
             RecordToLog( _T(" >> Droping after trigger. \n") );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrAfterTrigger[ 1 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrAfterTrigger[ 0 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
            break;
        default:
            break;
    }

    switch( tableTypes[ unitTest.tableType ] )
    {
		case VOLATILE:
            RecordToLog( _T(" >> Droping standard table. \n") );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStr[ 0 ], SQL_NTS ) ) == SQL_STILL_EXECUTING ); // Create the table.
            RecordToLog( _T(" >> Droping volatile table. \n") );
			while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrVolatile[ 1 ], SQL_NTS ) ) == SQL_STILL_EXECUTING ); // Create the table.
            break;
        default:
            RecordToLog( _T(" >> Droping standard table. \n") );
            while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStr[ 0 ], SQL_NTS ) ) == SQL_STILL_EXECUTING ); // Create the table.
            break;
    }

    if( retcode != SQL_SUCCESS && retcode != SQL_SUCCESS_WITH_INFO )    
    {
        if( CheckMsgs( _T("SQLExecDirect()"), __LINE__ ) != IGNORE_ERROR )
        {
            ClearIgnore( );
            DeleteHandles( );
            return false;
        }
    }

    if( features[ unitTest.feature ] != HASH2 && retcode == SQL_SUCCESS)
    {
        RecordToLog( _T(" >> Committing transaction.\n") );
        retcode = SQLEndTran( SQL_HANDLE_DBC, handle[ SQL_HANDLE_DBC ], SQL_COMMIT ); // Commit the transaction.
        if( retcode != SQL_SUCCESS )    
        {
            CheckMsgs( _T("SQLEndTran()"), __LINE__ );
            ClearIgnore( );
            DeleteHandles( );
            return false;
        }
    }

    retcode = SQLFreeStmt( handle[ SQL_HANDLE_STMT ], SQL_CLOSE ); // Free and clearup the statement handle.
    if( retcode != SQL_SUCCESS )    
    {
        CheckMsgs( _T("SQLFreeStmt()"), __LINE__ );
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
void ALM_TestInformation(TCHAR* sALM_TestInfo)
{
	wcscpy((TCHAR*)sALM_TestInfo,_T(""));
	switch( tableTypes[ unitTest.tableType ] )
	{
		case REGULAR:
			wcscat((TCHAR*)sALM_TestInfo,_T("tableType:REGULAR"));
			break;
		case POSOFF:
			wcscat((TCHAR*)sALM_TestInfo,_T("tableType:POSOFF"));
			break;
		case VOLATILE:
			wcscat((TCHAR*)sALM_TestInfo,_T("tableType:VOLATILE"));
			break;
		case SURROGATE:
			wcscat((TCHAR*)sALM_TestInfo,_T("tableType:SURROGATE"));
			break;
		case SET:
			wcscat((TCHAR*)sALM_TestInfo,_T("tableType:SET"));
			break;
		case MULTISET:
			wcscat((TCHAR*)sALM_TestInfo,_T("tableType:MULTISET"));
			break;
		default:
			wcscat((TCHAR*)sALM_TestInfo,_T("tableType:_UNKNOWN_"));
			break;
	}
	
	wcscat((TCHAR*)sALM_TestInfo,_T("+"));
    switch( tableFeatures[ unitTest.tableFeature ] )
    {
        case STANDARD:
			wcscat((TCHAR*)sALM_TestInfo,_T("tableFeature:STANDARD"));
            break;
        case INDEX:
			wcscat((TCHAR*)sALM_TestInfo,_T("tableFeature:INDEX"));
            break;
        case MVS:
			wcscat((TCHAR*)sALM_TestInfo,_T("tableFeature:MVS"));
            break;
        case RI:
			wcscat((TCHAR*)sALM_TestInfo,_T("tableFeature:RI"));
            break;
        case BEFORETRIGGER:
			wcscat((TCHAR*)sALM_TestInfo,_T("tableFeature:BEFORETRIGGER"));
            break;
        case AFTERTRIGGER:
			wcscat((TCHAR*)sALM_TestInfo,_T("tableFeature:AFTERTRIGGER"));
            break;
        default:
			wcscat((TCHAR*)sALM_TestInfo,_T("tableFeature:_UNKNOWN_"));
            break;
    }

	wcscat((TCHAR*)sALM_TestInfo,_T("+"));
    switch( modes[ unitTest.mode ] )
    {
        case STANDARD:
			wcscat((TCHAR*)sALM_TestInfo,_T("mode:STANDARD"));
            break;
        default:
			wcscat((TCHAR*)sALM_TestInfo,_T("mode:_UNKNOWN_"));
            break;
    }

    if( errorChecking == MODE_SPECIAL_1 )
    {
		wcscat((TCHAR*)sALM_TestInfo,_T("+CQD:MODE_SPECIAL_1"));
    }

	wcscat((TCHAR*)sALM_TestInfo,_T("+"));
    switch( features[ unitTest.feature ] )
    {
        case STANDARD:
			wcscat((TCHAR*)sALM_TestInfo,_T("feature:STANDARD"));
            break;
        case HASH2:
			wcscat((TCHAR*)sALM_TestInfo,_T("feature:HASH2"));
            break;
        case ASYNC:
			wcscat((TCHAR*)sALM_TestInfo,_T("feature:ASYNC"));
            break;
        default:
			wcscat((TCHAR*)sALM_TestInfo,_T("feature:_UNKNOWN_"));
            break;
    }

	wcscat((TCHAR*)sALM_TestInfo,_T("+"));
    switch( operations[ unitTest.operation ] )
    {
        case PREPARE_EXECUTE:
			wcscat((TCHAR*)sALM_TestInfo,_T("operation:PREPARE_EXECUTE"));
            break;
        case EXECUTE_DIRECT:
			wcscat((TCHAR*)sALM_TestInfo,_T("operation:EXECUTE_DIRECT"));
            break;
        default:
			wcscat((TCHAR*)sALM_TestInfo,_T("operation:_UNKNOWN_"));
            break;
    }

/*
	wcscat((TCHAR*)sALM_TestInfo,_T("+"));
    switch( actions[ unitTest.action ] )
    {
        case INSERT:
			wcscat((TCHAR*)sALM_TestInfo,"action:INSERT");
            break;
        case SELECT:
			wcscat((TCHAR*)sALM_TestInfo,"action:SELECT");
            break;
        case UPDATE:
			wcscat((TCHAR*)sALM_TestInfo,"action:UPDATE");
            break;
        case DELETE_PARAM:
			wcscat((TCHAR*)sALM_TestInfo,"action:DELETE");
            break;
        case INSERT_BULK:
			wcscat((TCHAR*)sALM_TestInfo,"action:INSERT_BULK");
            break;
        case INSERT_SELECT:
			wcscat((TCHAR*)sALM_TestInfo,"action:INSERT_SELECT");
            break;
        default:
			wcscat((TCHAR*)sALM_TestInfo,"action:_UNKNOWN_");
            break;
    }
*/

	wcscat((TCHAR*)sALM_TestInfo,_T("+"));
    switch( bindOrientations[ unitTest.bindOrientation ] )
    {
        case ROW:
			wcscat((TCHAR*)sALM_TestInfo,_T("bindOrientation:ROW"));
            break;
        case COLUMN:
			wcscat((TCHAR*)sALM_TestInfo,_T("bindOrientation:COLUMN"));
            break;
        case SINGLE:
			wcscat((TCHAR*)sALM_TestInfo,_T("bindOrientation:SINGLE"));
            break;
        default:
			wcscat((TCHAR*)sALM_TestInfo,_T("bindOrientation:_UNKNOWN_"));
            break;
    }
/*
	wcscat((TCHAR*)sALM_TestInfo,"+");
    switch( injectionTypes[ unitTest.injectionType ] )
    {
        case NO_ERRORS:
			wcscat((TCHAR*)sALM_TestInfo,"injectionType:NO_ERRORS");
            break;
        case DUPLICATEKEY:
			wcscat((TCHAR*)sALM_TestInfo,"injectionType:DUPLICATEKEY");
            break;
        case UNIQUECONST:
			wcscat((TCHAR*)sALM_TestInfo,"injectionType:UNIQUECONST");
            break;
        case SELECTIVE:
			wcscat((TCHAR*)sALM_TestInfo,"injectionType:SELECTIVE");
            break;
        case NULLVALUE:
			wcscat((TCHAR*)sALM_TestInfo,"injectionType:NULLVALUE");
            break;
        case DUPLICATEROW:
			wcscat((TCHAR*)sALM_TestInfo,"injectionType:DUPLICATEROW");
			//if (operations[ unitTest.operation ] != PREPARE_EXECUTE)
			//	(*ALM_testCounter)--;
			//bTestCounted = false;
            break;
        case OVERFLOW:
			wcscat((TCHAR*)sALM_TestInfo,"injectionType:OVERFLOW");
            break;
		case ERR_PER_ROW:
			wcscat((TCHAR*)sALM_TestInfo,"injectionType:ERR_PER_ROW");
            break;
		case ERR_PER_COL:
			wcscat((TCHAR*)sALM_TestInfo,"injectionType:ERR_PER_COL");
            break;
		case FULL_ERRORS:
			wcscat((TCHAR*)sALM_TestInfo,"injectionType:FULL_ERRORS");
            break;
		case DRIVER_GOOD_BAD_MULCOL:
			wcscat((TCHAR*)sALM_TestInfo,"injectionType:DRIVER_GOOD_BAD_MULCOL");
            break;
		case DRIVER_GOOD_WARNING_MULCOL:
			wcscat((TCHAR*)sALM_TestInfo,"injectionType:DRIVER_GOOD_WARNING_MULCOL");
            break;
		case DRIVER_GOOD_BAD_WARNING_MULCOL:
			wcscat((TCHAR*)sALM_TestInfo,"injectionType:DRIVER_GOOD_BAD_WARNING_MULCOL");
            break;
		case DRIVER_ALL_BAD_MULCOL:
			wcscat((TCHAR*)sALM_TestInfo,"injectionType:DRIVER_ALL_BAD_MULCOL");
            break;
		case DRIVER_ALL_WARNING_MULCOL:
			wcscat((TCHAR*)sALM_TestInfo,"injectionType:DRIVER_ALL_WARNING_MULCOL");
            break;
		case DRIVER_ALL_BAD_WARNING_MULCOL:
			wcscat((TCHAR*)sALM_TestInfo,"injectionType:DRIVER_ALL_BAD_WARNING_MULCOL");
            break;
		case SERVER_GOOD_BAD_MULCOL:
			wcscat((TCHAR*)sALM_TestInfo,"injectionType:SERVER_GOOD_BAD_MULCOL");
            break;
		case SERVER_ALL_BAD_MULCOL:
			wcscat((TCHAR*)sALM_TestInfo,"injectionType:SERVER_ALL_BAD_MULCOL");
            break;
		case MIXED_DRIVERWARNING_SERVERBAD_GOOD_MULCOL:
			wcscat((TCHAR*)sALM_TestInfo,"injectionType:MIXED_DRIVERWARNING_SERVERBAD_GOOD_MULCOL");
            break;
		case MIXED_DRIVERBAD_SERVERBAD_GOOD_MULCOL:
			wcscat((TCHAR*)sALM_TestInfo,"injectionType:MIXED_DRIVERBAD_SERVERBAD_GOOD_MULCOL");
            break;
		case MIXED_DRIVERWARNING_DRIVERBAD_SERVERBAD_GOOD_MULCOL:
			wcscat((TCHAR*)sALM_TestInfo,"injectionType:MIXED_DRIVERWARNING_DRIVERBAD_SERVERBAD_GOOD_MULCOL");
            break;
		case MIXED_DRIVERBAD_SERVERBAD_MULCOL:
			wcscat((TCHAR*)sALM_TestInfo,"injectionType:MIXED_DRIVERBAD_SERVERBAD_MULCOL");
            break;
		case MIXED_DRIVERWARNING_DRIVERBAD_SERVERBAD_MULCOL:
			wcscat((TCHAR*)sALM_TestInfo,"injectionType:MIXED_DRIVERWARNING_DRIVERBAD_SERVERBAD_MULCOL");
            break;
        default:
			wcscat((TCHAR*)sALM_TestInfo,"injectionType:_UNKNOWN_");
            break;
    }

	wcscat((TCHAR*)sALM_TestInfo,"+");
	sprintf(str, "numberOfRows=%d", numberOfRows[ unitTest.numberOfRows ]);
	wcscat((TCHAR*)sALM_TestInfo,str);

	wcscat((TCHAR*)sALM_TestInfo,"+");
	sprintf(str, "rowsetSize:%d", rowsetSizes[ unitTest.rowsetSize ]);
	wcscat((TCHAR*)sALM_TestInfo,str);

	wcscat((TCHAR*)sALM_TestInfo,"+");
	sprintf(str, "commitRate:%d", commitRates[ unitTest.commitRate ]);
	wcscat((TCHAR*)sALM_TestInfo,str);
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
            RecordToLog( _T("  tableType[%d]: REGULAR\n"), tableTypes[ unitTest.tableType ] );
            break;
        case POSOFF:
            RecordToLog( _T("  tableType[%d]: POSOFF\n"), tableTypes[ unitTest.tableType ] );
            break;
        case VOLATILE:
            RecordToLog( _T("  tableType[%d]: VOLATILE\n"), tableTypes[ unitTest.tableType ] );
            break;
        case SURROGATE:
            RecordToLog( _T("  tableType[%d]: SURROGATE\n"), tableTypes[ unitTest.tableType ] );
            break;
        case SET:
            RecordToLog( _T("  tableType[%d]: SET\n"), tableTypes[ unitTest.tableType ] );
            break;
        case MULTISET:
            RecordToLog( _T("  tableType[%d]: MULTISET\n"), tableTypes[ unitTest.tableType ] );
            break;
        default:
            RecordToLog( _T("  tableType[%d]: _UNKNOWN_\n"), tableTypes[ unitTest.tableType ] );
            break;
    }

    switch( tableFeatures[ unitTest.tableFeature ] )
    {
        case STANDARD:
            RecordToLog( _T("  tableFeature[%d]: STANDARD\n"), tableFeatures[ unitTest.tableFeature ] );
            break;
        case INDEX:
            RecordToLog( _T("  tableFeature[%d]: INDEX\n"), tableFeatures[ unitTest.tableFeature ] );
            break;
        case MVS:
            RecordToLog( _T("  tableFeature[%d]: MVS\n"), tableFeatures[ unitTest.tableFeature ] );
            break;
        case RI:
            RecordToLog( _T("  tableFeature[%d]: RI\n"), tableFeatures[ unitTest.tableFeature ] );
            break;
        case BEFORETRIGGER:
            RecordToLog( _T("  tableFeature[%d]: BEFORETRIGGER\n"), tableFeatures[ unitTest.tableFeature ] );
            break;
        case AFTERTRIGGER:
            RecordToLog( _T("  tableFeature[%d]: AFTERTRIGGER\n"), tableFeatures[ unitTest.tableFeature ] );
            break;
        default:
            RecordToLog( _T("  tableFeature[%d]: _UNKNOWN_\n"), tableFeatures[ unitTest.tableFeature ] );
            break;
    }

    switch( modes[ unitTest.mode ] )
    {
        case STANDARD:
            RecordToLog( _T("  mode[%d]: STANDARD\n"), modes[ unitTest.mode ] );
            break;
        default:
            RecordToLog( _T("  mode[%d]: _UNKNOWN_\n"), modes[ unitTest.mode ] );
            break;
    }

    if( errorChecking == MODE_SPECIAL_1 )
    {
        RecordToLog( _T("  CQD: MODE_SPECIAL_1 is 'ON'\n") );
    }

    switch( features[ unitTest.feature ] )
    {
        case STANDARD:
            RecordToLog( _T("  feature[%d]: STANDARD\n"), features[ unitTest.feature ] );
            break;
        case HASH2:
            RecordToLog( _T("  feature[%d]: HASH2\n"), features[ unitTest.feature ] );
            break;
        case ASYNC:
            RecordToLog( _T("  feature[%d]: ASYNC\n"), features[ unitTest.feature ] );
            break;
        default:
            RecordToLog( _T("  feature[%d]: _UNKNOWN_\n"), features[ unitTest.feature ] );
            break;
    }

    switch( operations[ unitTest.operation ] )
    {
        case PREPARE_EXECUTE:
            RecordToLog( _T("  operation[%d]: PREPARE_EXECUTE\n"), operations[ unitTest.operation ] );
            break;
        case EXECUTE_DIRECT:
            RecordToLog( _T("  operation[%d]: EXECUTE_DIRECT\n"), operations[ unitTest.operation ] );
            break;
        default:
            RecordToLog( _T("  operation[%d]: _UNKNOWN_\n"), operations[ unitTest.operation ] );
            break;
    }

    switch( actions[ unitTest.action ] )
    {
        case INSERT:
            RecordToLog( _T("  action[%d]: INSERT\n"), actions[ unitTest.action ] );
            break;
        case SELECT:
            RecordToLog( _T("  action[%d]: SELECT\n"), actions[ unitTest.action ] );
            break;
        case UPDATE:
            RecordToLog( _T("  action[%d]: UPDATE\n"), actions[ unitTest.action ] );
            break;
        case DELETE_PARAM:
            RecordToLog( _T("  action[%d]: DELETE\n"), actions[ unitTest.action ] );
            break;
        case INSERT_BULK:
            RecordToLog( _T("  action[%d]: INSERT_BULK\n"), actions[ unitTest.action ] );
            break;
        case INSERT_SELECT:
            RecordToLog( _T("  action[%d]: INSERT_SELECT\n"), actions[ unitTest.action ] );
            break;
        default:
            RecordToLog( _T("  action[%d]: _UNKNOWN_\n"), actions[ unitTest.action ] );
            break;
    }

    switch( bindOrientations[ unitTest.bindOrientation ] )
    {
        case ROW:
            RecordToLog( _T("  bindOrientation[%d]: ROW\n"), bindOrientations[ unitTest.bindOrientation ] );
            break;
        case COLUMN:
            RecordToLog( _T("  bindOrientation[%d]: COLUMN\n"), bindOrientations[ unitTest.bindOrientation ] );
            break;
        case SINGLE:
            RecordToLog( _T("  bindOrientation[%d]: SINGLE\n"), bindOrientations[ unitTest.bindOrientation ] );
            break;
        default:
            RecordToLog( _T("  bindOrientation[%d]: _UNKNOWN_\n"), bindOrientations[ unitTest.bindOrientation ] );
            break;
    }

    switch( injectionTypes[ unitTest.injectionType ] )
    {
        case NO_ERRORS:
            RecordToLog( _T("  injectionType[%d]: NO_ERRORS\n"), injectionTypes[ unitTest.injectionType ] );
            break;
        case DUPLICATEKEY:
            RecordToLog( _T("  injectionType[%d]: DUPLICATEKEY\n"), injectionTypes[ unitTest.injectionType ] );
            break;
        case UNIQUECONST:
            RecordToLog( _T("  injectionType[%d]: UNIQUECONST\n"), injectionTypes[ unitTest.injectionType ] );
            break;
        case SELECTIVE:
            RecordToLog( _T("  injectionType[%d]: SELECTIVE\n"), injectionTypes[ unitTest.injectionType ] );
            break;
        case NULLVALUE:
            RecordToLog( _T("  injectionType[%d]: NULLVALUE\n"), injectionTypes[ unitTest.injectionType ] );
            break;
        case DUPLICATEROW:
            RecordToLog( _T("  injectionType[%d]: DUPLICATEROW\n"), injectionTypes[ unitTest.injectionType ] );
            break;
        case OVERFLOW:
            RecordToLog( _T("  injectionType[%d]: OVERFLOW\n"), injectionTypes[ unitTest.injectionType ] );
            break;
		case ERR_PER_ROW:
            RecordToLog( _T("  injectionType[%d]: ERR_PER_ROW\n"), injectionTypes[ unitTest.injectionType ] );
            break;
		case ERR_PER_COL:
            RecordToLog( _T("  injectionType[%d]: ERR_PER_COL\n"), injectionTypes[ unitTest.injectionType ] );
            break;
		case FULL_ERRORS:
            RecordToLog( _T("  injectionType[%d]: FULL_ERRORS\n"), injectionTypes[ unitTest.injectionType ] );
            break;
		case DRIVER_GOOD_BAD_MULCOL:
            RecordToLog( _T("  injectionType[%d]: DRIVER_GOOD_BAD_MULCOL - Some good rows, some errors, no warning, multiple columns\n"), injectionTypes[ unitTest.injectionType ] );
            break;
		case DRIVER_GOOD_WARNING_MULCOL:
            RecordToLog( _T("  injectionType[%d]: DRIVER_GOOD_WARNING_MULCOL - Some good rows, no error, some warnings, multiple columns\n"), injectionTypes[ unitTest.injectionType ] );
            break;
		case DRIVER_GOOD_BAD_WARNING_MULCOL:
            RecordToLog( _T("  injectionType[%d]: DRIVER_GOOD_BAD_WARNING_MULCOL - Some good rows, some errors, some warnings, multiple columns\n"), injectionTypes[ unitTest.injectionType ] );
            break;
		case DRIVER_ALL_BAD_MULCOL:
            RecordToLog( _T("  injectionType[%d]: DRIVER_ALL_BAD_MULCOL - No good row, all errors, no warning, multiple columns\n"), injectionTypes[ unitTest.injectionType ] );
            break;
		case DRIVER_ALL_WARNING_MULCOL:
            RecordToLog( _T("  injectionType[%d]: DRIVER_ALL_WARNING_MULCOL - No good row, no error, all warnings, multiple columns\n"), injectionTypes[ unitTest.injectionType ] );
            break;
		case DRIVER_ALL_BAD_WARNING_MULCOL:
            RecordToLog( _T("  injectionType[%d]: DRIVER_ALL_BAD_WARNING_MULCOL - No good row, half errors and half warnings, multiple columns\n"), injectionTypes[ unitTest.injectionType ] );
            break;
		case SERVER_GOOD_BAD_MULCOL:
            RecordToLog( _T("  injectionType[%d]: SERVER_GOOD_BAD_MULCOL - Some good rows, some bad rows, multiple columns (server error only with/without driver warning)\n"), injectionTypes[ unitTest.injectionType ] );
            break;
		case SERVER_ALL_BAD_MULCOL:
            RecordToLog( _T("  injectionType[%d]: SERVER_ALL_BAD_MULCOL - No good row, all errors, multiple columns (server error only with/without driver warning)\n"), injectionTypes[ unitTest.injectionType ] );
            break;
		case MIXED_DRIVERWARNING_SERVERBAD_GOOD_MULCOL:
            RecordToLog( _T("  injectionType[%d]: MIXED_DRIVERWARNING_SERVERBAD_GOOD_MULCOL - Some good rows, some driver warnings, some server errors, multiple columns\n"), injectionTypes[ unitTest.injectionType ] );
            break;
		case MIXED_DRIVERBAD_SERVERBAD_GOOD_MULCOL:
            RecordToLog( _T("  injectionType[%d]: MIXED_DRIVERBAD_SERVERBAD_GOOD_MULCOL - Some good rows, some driver errors, some server errors, multiple columns\n"), injectionTypes[ unitTest.injectionType ] );
            break;
		case MIXED_DRIVERWARNING_DRIVERBAD_SERVERBAD_GOOD_MULCOL:
            RecordToLog( _T("  injectionType[%d]: MIXED_DRIVERWARNING_DRIVERBAD_SERVERBAD_GOOD_MULCOL - Some good rows, some driver errors, some driver warnings, some server errors, multiple columns\n"), injectionTypes[ unitTest.injectionType ] );
            break;
		case MIXED_DRIVERBAD_SERVERBAD_MULCOL:
            RecordToLog( _T("  injectionType[%d]: MIXED_DRIVERBAD_SERVERBAD_MULCOL - Driver errrors, server errors, no warning, no good row, multiple columns\n"), injectionTypes[ unitTest.injectionType ] );
            break;
		case MIXED_DRIVERWARNING_DRIVERBAD_SERVERBAD_MULCOL:
            RecordToLog( _T("  injectionType[%d]: MIXED_DRIVERWARNING_DRIVERBAD_SERVERBAD_MULCOL - Driver errrors, driver warnings, server errors, no good row, multiple columns\n"), injectionTypes[ unitTest.injectionType ] );
            break;
        default:
            RecordToLog( _T("  injectionType[%d]: _UNKNOWN_\n"), injectionTypes[ unitTest.injectionType ] );
            break;
    }
    RecordToLog( _T("  numberOfRows: %d\n"), numberOfRows[ unitTest.numberOfRows ] );
    RecordToLog( _T("  rowsetSize: %d\n"), rowsetSizes[ unitTest.rowsetSize ] );
    RecordToLog( _T("  commitRate: %d\n"), commitRates[ unitTest.commitRate ] );
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

    RecordToLog( _T(" >> Freeing the statement bind parameter buffers.\n") );
    retcode= SQLFreeStmt( handle[ SQL_HANDLE_STMT ], SQL_RESET_PARAMS );
    if( retcode != SQL_SUCCESS )    
    {    
        RecordToLog( _T(" >> SQLFreeStmt() with SQL_RESET_PARAMS attribute failed.\n") );
        CheckMsgs( _T("SQLFreeStmt()"), __LINE__ );
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
                RecordToLog( _T(" >> SQLSetStmtAttr() with SQL_ATTR_PARAM_BIND_TYPE attribute failed.\n") );
                CheckMsgs( _T("SQLSetStmtAttr()"), __LINE__ );
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
                RecordToLog( _T(" >> SQLSetStmtAttr() with SQL_ATTR_PARAM_BIND_TYPE attribute failed.\n") );
                CheckMsgs( _T("SQLSetStmtAttr()"), __LINE__ );
                FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
                return false;
            }
            break;
    }
    
    // Specify the number of elements in each parameter array.
    retcode = SQLSetStmtAttr( handle[ SQL_HANDLE_STMT ], SQL_ATTR_PARAMSET_SIZE, (void *)rowsetSizes[ unitTest.rowsetSize ], 0 );
    if( retcode != SQL_SUCCESS )    
    {
        RecordToLog( _T(" >> SQLSetStmtAttr() with SQL_ATTR_PARAMSET_SIZE attribute failed.\n") );
        CheckMsgs( _T("SQLSetStmtAttr()"), __LINE__ );
        FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
        return false;
    }

    // Specify an array in which to return the status of each set of parameters.
    retcode = SQLSetStmtAttr( handle[ SQL_HANDLE_STMT ], SQL_ATTR_PARAM_STATUS_PTR, rowsetStatusArray, 0 );
    if( retcode != SQL_SUCCESS )    
    {
        RecordToLog( _T(" >> SQLSetStmtAttr() with SQL_ATTR_PARAM_STATUS_PTR attribute failed.\n") );
        CheckMsgs( _T("SQLSetStmtAttr()"), __LINE__ );
        FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
        return false;
    }
    
    // Specify an array showing which rows to process.
    retcode = SQLSetStmtAttr( handle[ SQL_HANDLE_STMT ], SQL_ATTR_PARAM_OPERATION_PTR, rowsetOperationArray, 0 );
    if( retcode != SQL_SUCCESS )    
    {
        RecordToLog( _T(" >> SQLSetStmtAttr() with SQL_ATTR_PARAM_OPERATION_PTR attribute failed.\n") );
        CheckMsgs( _T("SQLSetStmtAttr()"), __LINE__ );
        FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
        return false;
    }

    // Specify an SQLUINTEGER value in which to return the number of sets of parameters processed.
    retcode = SQLSetStmtAttr( handle[ SQL_HANDLE_STMT ], SQL_ATTR_PARAMS_PROCESSED_PTR, &rowsProcessed, 0 );
    if( retcode != SQL_SUCCESS )    
    {
        RecordToLog( _T(" >> SQLSetStmtAttr() with SQL_ATTR_PARAMS_PROCESSED_PTR attribute failed.\n") );
        CheckMsgs( _T("SQLSetStmtAttr()"), __LINE__ );
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
                    TCHAR sqlDrvInsert[] = _T("PLANLOADTABLE ROWSET_TABLE");
                    while( ( retcode = SQLPrepare( handle[ SQL_HANDLE_STMT ], (SQLTCHAR *) sqlDrvInsert, SQL_NTS ) ) == SQL_STILL_EXECUTING );
                }
                while( ( retcode = SQLPrepare( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStr[ 2 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
                break;
            case DELETE_PARAM:
                while( ( retcode = SQLPrepare( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStr[ 6 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
                break;
            case UPDATE:
				while( ( retcode = SQLPrepare( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStr[ 7 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
                break;
            case INSERT_SELECT:
                while( ( retcode = SQLPrepare( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStr[ 14 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
                break;
            default:
                RecordToLog( _T(" >> INTERNAL ERROR: An unknown table action has been discovered.\n") );
                FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
                return false;
        }
    
        if( retcode != SQL_SUCCESS )    
        {
            if( retcode != SQL_SUCCESS_WITH_INFO )
            {
                CheckMsgs( _T("SQLPrepare()"), __LINE__ );
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
            swprintf( (TCHAR*)rowset[ rowsetPos ].dt_char_utf8, 256, _T("%s"), Digit_2_Ascii[column1Value] );
			swprintf( (TCHAR*)rowset[ rowsetPos ].dt_char_ucs, 256, _T("%s"), Digit_2_Charset[column1Value] );
            swprintf( (TCHAR*)rowset[ rowsetPos ].dt_varchar_utf8, 256, _T("%s"), Digit_2_Ascii[column1Value] );
            swprintf( (TCHAR*)rowset[ rowsetPos ].dt_varchar_ucs, 256, _T("%s"), Digit_2_Charset[column1Value] );
            swprintf( (TCHAR*)rowset[ rowsetPos ].dt_longvarchar_utf8, 256, _T("%s"), Digit_2_Ascii[column1Value] );
            swprintf( (TCHAR*)rowset[ rowsetPos ].dt_longvarchar_ucs, 256, _T("%s"), Digit_2_Charset[column1Value] );            
            swprintf( (TCHAR*)rowset[ rowsetPos ].dt_nchar, 256, _T("%s"), Digit_2_Charset[column1Value] );
            swprintf( (TCHAR*)rowset[ rowsetPos ].dt_ncharvarying, 256, _T("%s"), Digit_2_Charset[column1Value] );
            swprintf( (TCHAR*)rowset[ rowsetPos ].dt_decimal_s, 256, _T("%d"), 1 );
            swprintf( (TCHAR*)rowset[ rowsetPos ].dt_decimal_u, 256, _T("%d"), column2Value );
            swprintf( (TCHAR*)rowset[ rowsetPos ].dt_numeric_s, 256, _T("%d"), 1 );
            swprintf( (TCHAR*)rowset[ rowsetPos ].dt_numeric_u, 256, _T("%d"), 1 );
            swprintf( (TCHAR*)rowset[ rowsetPos ].dt_tinyint_s, 256, _T("%d"), 1 );
            swprintf( (TCHAR*)rowset[ rowsetPos ].dt_tinyint_u, 256, _T("%d"), 1 );
            swprintf( (TCHAR*)rowset[ rowsetPos ].dt_smallinteger_s, 256, _T("%d"), 1 );
            swprintf( (TCHAR*)rowset[ rowsetPos ].dt_smallinteger_u, 256, _T("%d"), 1 );
            swprintf( (TCHAR*)rowset[ rowsetPos ].dt_integer_s, 256, _T("%d"), column2Value );
            swprintf( (TCHAR*)rowset[ rowsetPos ].dt_integer_u, 256, _T("%d"), column1Value );            
            swprintf( (TCHAR*)rowset[ rowsetPos ].dt_largeint, 256, _T("%d"), column1Value );
            swprintf( (TCHAR*)rowset[ rowsetPos ].dt_real, 256, _T("%d"), column1Value );
            swprintf( (TCHAR*)rowset[ rowsetPos ].dt_float, 256, _T("%d"), column1Value );
            swprintf( (TCHAR*)rowset[ rowsetPos ].dt_double_precision, 256, _T("%d"), column1Value );
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
            swprintf( (TCHAR*)rowset[ rowsetPos ].dt_bignum_s, 256, _T("%s"), _T("1234567890123456789") );
            swprintf( (TCHAR*)rowset[ rowsetPos ].dt_bignum_u, 256, _T("%s"), _T("1234567890123456789") );
            break;
        case COLUMN:
            _stprintf( (TCHAR*)&dt_char_utf8[ rowsetPos * STRINGMAX ], _T("%s"), Digit_2_Ascii[column1Value] );
            _stprintf( (TCHAR*)&dt_char_ucs[ rowsetPos * STRINGMAX  ], _T("%s"), Digit_2_Charset[column1Value] );
            _stprintf( (TCHAR*)&dt_varchar_utf8[ rowsetPos * STRINGMAX  ], _T("%s"), Digit_2_Ascii[column1Value] );
            _stprintf( (TCHAR*)&dt_varchar_ucs[ rowsetPos * STRINGMAX  ], _T("%s"), Digit_2_Charset[column1Value] );
            _stprintf( (TCHAR*)&dt_longvarchar_utf8[ rowsetPos * STRINGMAX  ], _T("%s"), Digit_2_Ascii[column1Value] );
            _stprintf( (TCHAR*)&dt_longvarchar_ucs[ rowsetPos * STRINGMAX  ], _T("%s"), Digit_2_Charset[column1Value] );            
            _stprintf( (TCHAR*)&dt_nchar[ rowsetPos * STRINGMAX  ], _T("%s"), Digit_2_Charset[column1Value] );
            _stprintf( (TCHAR*)&dt_ncharvarying[ rowsetPos * STRINGMAX  ], _T("%s"), Digit_2_Charset[column1Value] );
            _stprintf( (TCHAR*)&dt_decimal_s[ rowsetPos * STRINGMAX  ], _T("%d"), 1 );
            _stprintf( (TCHAR*)&dt_decimal_u[ rowsetPos * STRINGMAX  ], _T("%d"), column2Value );
            _stprintf( (TCHAR*)&dt_numeric_s[ rowsetPos * STRINGMAX  ], _T("%d"), 1 );
            _stprintf( (TCHAR*)&dt_numeric_u[ rowsetPos * STRINGMAX  ], _T("%d"), 1 );
            _stprintf( (TCHAR*)&dt_tinyint_s[ rowsetPos * STRINGMAX  ], _T("%d"), 1 );
            _stprintf( (TCHAR*)&dt_tinyint_u[ rowsetPos * STRINGMAX  ], _T("%d"), 1 );
            _stprintf( (TCHAR*)&dt_smallinteger_s[ rowsetPos * STRINGMAX  ], _T("%d"), 1 );
            _stprintf( (TCHAR*)&dt_smallinteger_u[ rowsetPos * STRINGMAX  ], _T("%d"), 1 );
            _stprintf( (TCHAR*)&dt_integer_s[ rowsetPos * STRINGMAX  ], _T("%d"), column2Value );
            _stprintf( (TCHAR*)&dt_integer_u[ rowsetPos * STRINGMAX  ], _T("%d"), column1Value );
            _stprintf( (TCHAR*)&dt_largeint[ rowsetPos * STRINGMAX  ], _T("%d"), column1Value );
            _stprintf( (TCHAR*)&dt_real[ rowsetPos * STRINGMAX  ], _T("%d"), column1Value );
            _stprintf( (TCHAR*)&dt_float[ rowsetPos * STRINGMAX  ], _T("%d"), column1Value );
            _stprintf( (TCHAR*)&dt_double_precision[ rowsetPos * STRINGMAX  ], _T("%d"), column1Value );
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
            _stprintf( (TCHAR*)&dt_bignum_s[ rowsetPos * STRINGMAX  ], _T("%s"), _T("1234567890123456789") );
            _stprintf( (TCHAR*)&dt_bignum_u[ rowsetPos * STRINGMAX  ], _T("%s"), _T("1234567890123456789") );
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
        RecordToLog( _T("    Failing API: SQLBulkOperations()\n") );
        CheckMsgs( _T("SQLBulkOperations()"), __LINE__ );
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
                    RecordToLog( _T("INTERNAL ERROR: An unknown failure type has been discovered.\n") );
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
                    CheckMsgs( _T("SQLSetStmtAttr()"), __LINE__ );
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
            RecordToLog( _T("    Failing API: SQLBulkOperations()\n") );
            CheckMsgs( _T("SQLBulkOperations()"), __LINE__ );
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
                RecordToLog( _T("    Failing API: SQLEndTran()\n") );
                CheckMsgs( _T("SQLEndTran()"), __LINE__ );
                FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
                return false;
            }
            numIterations = 0;
        }

        // Check to make sure all the rows we inserted were processed.
        if ( (int)rowsProcessed != rs ) {
            RecordToLog(_T(" >> ERROR: The number of parameters processed does not match the number of rows prepared.\n"));
            RecordToLog(_T(" >> ERROR: Rows processed by ODBC: %d Rows prepared by client: %d at line %d\n"), (int)rowsProcessed, rs, __LINE__ );
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
                        RecordToLog(_T(" >> ERROR: Rowset status array row %d was expected to have SQL_PARAM_SUCCESS. Actual: %s at line %d.\n"), rowPos, Param_Status_Ptr( rowsetStatusArray[ rowPos ] ), __LINE__ );
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
                        RecordToLog(_T(" >> ERROR: Rowset status array row %d was expected to have SQL_PARAM_ERROR. Actual: %s at line %d.\n"), rowPos, Param_Status_Ptr( rowsetStatusArray[ rowPos ] ), __LINE__ );
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
                        RecordToLog(_T(" >> ERROR: Rowset status array row %d was expected to have SQL_PARAM_UNUSED. Actual: %s at line %d.\n"), rowPos, Param_Status_Ptr( rowsetStatusArray[ rowPos ] ), __LINE__ );
                        rc = false;
                        break;
                }
            }
        }

        // Check to make sure the row count of affected rows is correct.
        retcode = SQLRowCount( handle[ SQL_HANDLE_STMT ], &rowCount );
        if( retcode != SQL_SUCCESS )    
        {
            RecordToLog( _T("    Failing API: SQLRowCount()\n") );
            CheckMsgs( _T("SQLRowCount()"), __LINE__ );
            FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
            //return false;
        }

        if( ( errorChecking == MODE_SPECIAL_1 ) && ( (int)rowCount != ( rowsProcessed ) ) )
        {
            RecordToLog( _T(" >> ERROR: The number of good rows processed [%d] does not match the SQLRowCount() [%d] at line %d.\n"), rowsProcessed, rowCount, __LINE__);
            rc = false;
        }
        if( ( errorChecking == STANDARD ) && ( (int)rowCount != ( rowsProcessed - failureInjectionCount ) ) )
        {
            RecordToLog( _T(" >> ERROR: The number of good rows processed [%d] does not match the SQLRowCount() [%d] at line %d.\n"), ( rowsProcessed - failureInjectionCount ), rowCount, __LINE__);
            rc = false;
        }
    }

    // Commit the rest of the rows.
    if ( features[ unitTest.feature ] != HASH2 )
    {
        retcode = SQLEndTran( SQL_HANDLE_DBC, handle[ SQL_HANDLE_DBC ], SQL_COMMIT );
        if( retcode != SQL_SUCCESS )    
        {
            RecordToLog( _T("\n    Failing API: SQLEndTran()\n") );
            CheckMsgs( _T("SQLEndTran()"), __LINE__ );
            FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
            return false;
        }
    }

    FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
    /*****
    // Display time metrics
    if( ( timeMetrics ) && ( testMatrix[ testMatrixPos ].returnCode == true ) )
    {
        RecordToLog(_T(" Running time in seconds: %lf\n"), testMatrix[ testMatrixPos ].runningTime );
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

    RecordToLog( _T("    Freeing the statement bind column buffers.\n") );
    retcode= SQLFreeStmt( handle[ SQL_HANDLE_STMT ], SQL_UNBIND );
    if( retcode != SQL_SUCCESS )    
    {    
        RecordToLog( _T("SQLFreeStmt() with SQL_UNBIND attribute failed.\n") );
        CheckMsgs( _T("SQLFreeStmt()"), __LINE__ );
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
                CheckMsgs( _T("SQLSetStmtAttr()"), __LINE__ );
                FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
                return false;
            }
            break;
        // Set the SQL_ATTR_ROW_BIND_TYPE statement attribute to use column-wise binding.
        case COLUMN:
            retcode = SQLSetStmtAttr( handle[ SQL_HANDLE_STMT ], SQL_ATTR_ROW_BIND_TYPE, SQL_BIND_BY_COLUMN, 0 );
            if( retcode != SQL_SUCCESS )    
            {    
                CheckMsgs( _T("SQLSetStmtAttr()"), __LINE__ );
                FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
                return false;
            }
            break;
        default:
            RecordToLog( _T("INTERNAL ERROR: An unknown access style has been discovered at line %d.\n"), __LINE__ );
            FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
            return false;
    }
    
    // Specify the number of elements in each parameter array.
    retcode = SQLSetStmtAttr( handle[ SQL_HANDLE_STMT ], SQL_ATTR_ROW_ARRAY_SIZE, (void *)rowsetSizes[ unitTest.rowsetSize ], 0 );
    if( retcode != SQL_SUCCESS )    
    {
        CheckMsgs( _T("SQLSetStmtAttr()"), __LINE__ );
        FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
        return false;
    }

    // Specify an array in which to return the status of each set of parameters.
    retcode = SQLSetStmtAttr( handle[ SQL_HANDLE_STMT ], SQL_ATTR_ROW_STATUS_PTR, rowsetStatusArray, 0 );
    if( retcode != SQL_SUCCESS )    
    {
        CheckMsgs( _T("SQLSetStmtAttr()"), __LINE__ );
        FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
        return false;
    }

    // Specify an SQLUINTEGER value in which to return the number of sets of parameters processed.
    rowsProcessed = 0;
    retcode = SQLSetStmtAttr( handle[ SQL_HANDLE_STMT ], SQL_ATTR_ROWS_FETCHED_PTR, &rowsProcessed, 0 );
    if( retcode != SQL_SUCCESS )    
    {
        CheckMsgs( _T("SQLSetStmtAttr()"), __LINE__ );
        FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
        return false;
    }
/****
    retcode = SQLSetStmtAttr( handle[ SQL_HANDLE_STMT ], SQL_ATTR_CURSOR_TYPE, (SQLPOINTER)SQL_CURSOR_DYNAMIC, SQL_IS_UINTEGER);
    if( retcode != SQL_SUCCESS )    
    {   
        CheckMsgs( _T("SQLSetStmtAttr()"), __LINE__ );
        FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
        return false;
    }

    retcode = SQLSetStmtAttr( handle[ SQL_HANDLE_STMT ], SQL_ATTR_CONCURRENCY, (SQLPOINTER)SQL_CONCUR_LOCK, SQL_IS_UINTEGER);
    if( retcode != SQL_SUCCESS )    
    {   
        CheckMsgs( _T("SQLSetStmtAttr()"), __LINE__ );
        FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
        return false;
    }
****/

	BindColsA( bindOrientations[ unitTest.bindOrientation ] );

    // See if we want the rowsets to be processed through preapre or directly.
    if( operations[ unitTest.operation ] == PREPARE_EXECUTE )
    {
        switch( actions[ unitTest.action] )
        {
            case SELECT:
            case INSERT_BULK:
                while( ( retcode = SQLPrepare( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStr[ 3 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
                break;
            default:
                break;
        }
    
        // Check the return status from the prepared statement.
        if( retcode != SQL_SUCCESS )    
        {
            CheckMsgs( _T("SQLPrepare()"), __LINE__ );
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
	int colsize = 20;
    int value=0;
	int size_char_utf8=0, size_varchar_utf8=0;
	int size_char_charset=0, size_varchar_charset=0;
    TCHAR valueStr[STRINGMAX]; // The only values can be 0 through 60
    TCHAR ValueStrUtf8[ STRINGMAX ]; // The only values can be 0 through 60
    TCHAR valueStrSizedUtf8[ STRINGMAX ]; // This is for the static sized columns
    TCHAR valueStrCharset[ STRINGMAX ]; // The only values can be 0 through 60
    TCHAR valueStrSizedCharset[ STRINGMAX ]; // This is for the static sized columns
    TCHAR valueStrReal[STRINGMAX]; // This is for real values.

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
    _stprintf( valueStr, _T("%d"), value );
	_stprintf( valueStrReal, _T("%d.0"), value );
    _stprintf( ValueStrUtf8, _T("%s"), Digit_2_Ascii[ value ] );
    _stprintf( valueStrCharset, _T("%s"), Digit_2_Charset[ value ] );


	for (int loop = 0; loop < STRINGMAX; loop++) {
		valueStrSizedUtf8[ loop ] = ' ';
	}
	for( int loop = 0; ValueStrUtf8[loop] != '\0'; loop++ ) {
		valueStrSizedUtf8[ loop ] = ValueStrUtf8[ loop ];
		size_char_utf8++;
		size_varchar_utf8++;
	}
	size_char_utf8 += (colsize - (int)_tcslen(ValueStrUtf8));
	valueStrSizedUtf8[ size_char_utf8 ] = '\0';
	size_char_utf8 *= sizeof(TCHAR)*4;
	size_varchar_utf8 *= sizeof(TCHAR); // size_varchar_utf8 *= sizeof(TCHAR)*4;


	for (int loop = 0; loop < STRINGMAX; loop++) {
		valueStrSizedCharset[ loop ] = ' ';
	}
	for( int loop = 0; valueStrCharset[loop] != '\0'; loop++ ) {
		valueStrSizedCharset[ loop ] = valueStrCharset[ loop ];
		size_char_charset++;;
		size_varchar_charset++;
	}
	size_char_charset += (colsize - 15);
	valueStrSizedCharset[ size_char_charset ] = '\0';
	size_char_charset *= sizeof(TCHAR);
	size_varchar_charset *= sizeof(TCHAR);

	switch( bindOrientations[ unitTest.bindOrientation ] )
    {
        case ROW:
        case SINGLE:
			//Checked size of data returned
			if (rowset[ rowsetPos ].ptr_char_utf8 != size_char_utf8) {
                RecordToLog( _T("ERROR: Data type: ptr_char_utf8 Expected: %d Actual %d at line %d\n"), size_char_utf8, rowset[ rowsetPos ].ptr_char_utf8, __LINE__ );
                rc = false;			
			}
			else {
				if (debug)
					RecordToLog( _T("Data type matched: ptr_char_utf8 Expected: %d Actual %d at line %d\n"), size_char_utf8, rowset[ rowsetPos ].ptr_char_utf8, __LINE__ );
			}
			if (rowset[ rowsetPos ].ptr_char_ucs != size_char_charset) {
                RecordToLog( _T("ERROR: Data type: ptr_char_ucs Expected: %d Actual %d at line %d\n"), size_char_charset, rowset[ rowsetPos ].ptr_char_ucs, __LINE__ );
                rc = false;			
			}
			else {
				if (debug)
					RecordToLog( _T("Data type matched: ptr_char_ucs Expected: %d Actual %d at line %d\n"), size_char_charset, rowset[ rowsetPos ].ptr_char_ucs, __LINE__ );
			}
			if (rowset[ rowsetPos ].ptr_varchar_utf8 != size_varchar_utf8) {
                RecordToLog( _T("ERROR: Data type: ptr_varchar_utf8 Expected: %d Actual %d at line %d\n"), size_varchar_utf8, rowset[ rowsetPos ].ptr_varchar_utf8, __LINE__ );
                rc = false;			
			}
			else {
				if (debug)
					RecordToLog( _T("Data type matched: ptr_varchar_utf8 Expected: %d Actual %d at line %d\n"), size_varchar_utf8, rowset[ rowsetPos ].ptr_varchar_utf8, __LINE__ );
			}
			if (rowset[ rowsetPos ].ptr_varchar_ucs != size_varchar_charset) {
                RecordToLog( _T("ERROR: Data type: ptr_varchar_ucs Expected: %d Actual %d at line %d\n"), size_varchar_charset, rowset[ rowsetPos ].ptr_varchar_ucs, __LINE__ );
                rc = false;			
			}
			else {
				if (debug)
					RecordToLog( _T("Data type matched: ptr_varchar_ucs Expected: %d Actual %d at line %d\n"), size_varchar_charset, rowset[ rowsetPos ].ptr_varchar_ucs, __LINE__ );
			}
			if (rowset[ rowsetPos ].ptr_longvarchar_utf8 != size_varchar_utf8) {
                RecordToLog( _T("ERROR: Data type: ptr_longvarchar_utf8 Expected: %d Actual %d at line %d\n"), size_varchar_utf8, rowset[ rowsetPos ].ptr_longvarchar_utf8, __LINE__ );
                rc = false;			
			}
			else {
				if (debug)
					RecordToLog( _T("Data type matched: ptr_longvarchar_utf8 Expected: %d Actual %d at line %d\n"), size_varchar_utf8, rowset[ rowsetPos ].ptr_longvarchar_utf8, __LINE__ );
			}
			if (rowset[ rowsetPos ].ptr_longvarchar_ucs != size_varchar_charset) {
                RecordToLog( _T("ERROR: Data type: ptr_longvarchar_ucs Expected: %d Actual %d at line %d\n"), size_varchar_charset, rowset[ rowsetPos ].ptr_longvarchar_ucs, __LINE__ );
                rc = false;			
			}
			else {
				if (debug)
					RecordToLog( _T("Data type matched: ptr_longvarchar_ucs Expected: %d Actual %d at line %d\n"), size_varchar_charset, rowset[ rowsetPos ].ptr_longvarchar_ucs, __LINE__ );
			}
			if (rowset[ rowsetPos ].ptr_nchar != size_char_charset) {
                RecordToLog( _T("ERROR: Data type: ptr_nchar Expected: %d Actual %d at line %d\n"), size_char_charset, rowset[ rowsetPos ].ptr_nchar, __LINE__ );
                rc = false;			
			}
			else {
				if (debug)
					RecordToLog( _T("Data type matched: ptr_nchar Expected: %d Actual %d at line %d\n"), size_char_charset, rowset[ rowsetPos ].ptr_nchar, __LINE__ );
			}
			if (rowset[ rowsetPos ].ptr_ncharvarying != size_varchar_charset) {
                RecordToLog( _T("ERROR: Data type: ptr_ncharvarying Expected: %d Actual %d at line %d\n"), size_varchar_charset, rowset[ rowsetPos ].ptr_ncharvarying, __LINE__ );
                rc = false;			
			}
			else {
				if (debug)
					RecordToLog( _T("Data type matched: ptr_ncharvarying Expected: %d Actual %d at line %d\n"), size_varchar_charset, rowset[ rowsetPos ].ptr_ncharvarying, __LINE__ );
			}

			//Check value of data returned
			if( _tcsncmp( (TCHAR*)rowset[ rowsetPos ].dt_char_utf8,    valueStrSizedUtf8, _tcslen(valueStrSizedUtf8) ) != 0 )
            {
                RecordToLog( _T("ERROR: Data type: dt_char_utf8 Expected: %s Actual %s at line %d\n"), valueStrSizedUtf8, (TCHAR*)rowset[ rowsetPos ].dt_char_utf8, __LINE__ );
                rc = false;
            }
            if( _tcscmp( (TCHAR*)rowset[ rowsetPos ].dt_char_ucs,    valueStrSizedCharset ) != 0 )
            {
                RecordToLog( _T("ERROR: Data type: dt_char_ucs Expected: %s Actual %s at line %d\n"), valueStrSizedCharset, (TCHAR*)rowset[ rowsetPos ].dt_char_ucs, __LINE__ );
                rc = false;
            }
            if( _tcsncmp( (TCHAR*)rowset[ rowsetPos ].dt_varchar_utf8,      ValueStrUtf8, _tcslen(ValueStrUtf8) ) != 0 )
            {
                RecordToLog( _T("ERROR: Data type: dt_varchar_utf8 Expected: %s Actual %s at line %d\n"), ValueStrUtf8, (TCHAR*)rowset[ rowsetPos ].dt_varchar_utf8 , __LINE__);
                rc = false;
            }
            if( _tcscmp( (TCHAR*)rowset[ rowsetPos ].dt_varchar_ucs,      valueStrCharset ) != 0 )
            {
                RecordToLog( _T("ERROR: Data type: dt_varchar_ucs Expected: %s Actual %s at line %d\n"), valueStrCharset, (TCHAR*)rowset[ rowsetPos ].dt_varchar_ucs, __LINE__ );
                rc = false;
            }
            if( _tcsncmp( (TCHAR*)rowset[ rowsetPos ].dt_longvarchar_utf8,  ValueStrUtf8, _tcslen(ValueStrUtf8) ) != 0 )
            {
                RecordToLog( _T("ERROR: Data type: dt_longvarchar_utf8 Expected: %s Actual %s at line %d\n"), ValueStrUtf8, (TCHAR*)rowset[ rowsetPos ].dt_longvarchar_utf8, __LINE__ );
                rc = false;
            }
            if( _tcscmp( (TCHAR*)rowset[ rowsetPos ].dt_longvarchar_ucs,  valueStrCharset ) != 0 )            
            {
                RecordToLog( _T("ERROR: Data type: dt_longvarchar_ucs Expected: %s Actual %s at line %d\n"), valueStrCharset, (TCHAR*)rowset[ rowsetPos ].dt_longvarchar_ucs, __LINE__ );
                rc = false;
            }
            if( _tcscmp( (TCHAR*)rowset[ rowsetPos ].dt_nchar,       valueStrSizedCharset ) != 0 )
            {
                RecordToLog( _T("ERROR: Data type: dt_nchar Expected: %s Actual %s at line %d\n"), valueStrSizedCharset, (TCHAR*)rowset[ rowsetPos ].dt_nchar , __LINE__);
                rc = false;
            }
            if( _tcscmp( (TCHAR*)rowset[ rowsetPos ].dt_ncharvarying,     valueStrCharset ) != 0 )
            {
                RecordToLog( _T("ERROR: Data type: dt_ncharvarying Expected: %s Actual %s at line %d\n"), valueStrCharset, (TCHAR*)rowset[ rowsetPos ].dt_ncharvarying, __LINE__ );
                rc = false;
            }
	     if( _tcsncmp( (TCHAR*)rowset[ rowsetPos ].dt_decimal_s,        _T("1"), (int)rowset[ rowsetPos ].ptr_decimal_s ) != 0 )
            {
                RecordToLog( _T("ERROR: Data type: dt_decimal_s Expected: %s Actual %s at line %d\n"), valueStr, (TCHAR*)rowset[ rowsetPos ].dt_decimal_s , __LINE__);
                rc = false;
            }
            if( _tcsncmp( (TCHAR*)rowset[ rowsetPos ].dt_decimal_u,        valueStr, (int)rowset[ rowsetPos ].ptr_decimal_u ) != 0 )
            {
                RecordToLog( _T("ERROR: Data type: dt_decimal_u Expected: %s Actual %s at line %d\n"), valueStr, (TCHAR*)rowset[ rowsetPos ].dt_decimal_u , __LINE__);
                rc = false;
            }
            if( _tcsncmp( (TCHAR*)rowset[ rowsetPos ].dt_numeric_s,        _T("1"), (int)rowset[ rowsetPos ].ptr_numeric_s ) != 0 )
            {
                RecordToLog( _T("ERROR: Data type: dt_numeric_s Expected: %s Actual %s at line %d\n"), valueStr, (TCHAR*)rowset[ rowsetPos ].dt_numeric_s, __LINE__ );
                rc = false;
            }
            if( _tcsncmp( (TCHAR*)rowset[ rowsetPos ].dt_numeric_u,        _T("1"), (int)rowset[ rowsetPos ].ptr_numeric_u ) != 0 )
            {
                RecordToLog( _T("ERROR: Data type: dt_numeric_u Expected: %s Actual %s at line %d\n"), valueStr, (TCHAR*)rowset[ rowsetPos ].dt_numeric_u, __LINE__ );
                rc = false;
            }
            if( _tcsncmp( (TCHAR*)rowset[ rowsetPos ].dt_tinyint_s,        _T("1"), (int)rowset[ rowsetPos ].ptr_tinyint_s ) != 0 )
            {
                RecordToLog( _T("ERROR: Data type: dt_tinyint_s Expected: %s Actual %s at line %d\n"), valueStr, (TCHAR*)rowset[ rowsetPos ].dt_tinyint_s, __LINE__ );
                rc = false;
            }
            if( _tcsncmp( (TCHAR*)rowset[ rowsetPos ].dt_tinyint_u,        _T("1"), (int)rowset[ rowsetPos ].ptr_tinyint_u ) != 0 )
            {
                RecordToLog( _T("ERROR: Data type: dt_tinyint_u Expected: %s Actual %s at line %d\n"), valueStr, (TCHAR*)rowset[ rowsetPos ].dt_tinyint_u , __LINE__);
                rc = false;
            }
            if( _tcsncmp( (TCHAR*)rowset[ rowsetPos ].dt_smallinteger_s,   _T("1"), (int)rowset[ rowsetPos ].ptr_smallinteger_s ) != 0 )
            {
                RecordToLog( _T("ERROR: Data type: dt_smallinteger_s Expected: %s Actual %s at line %d\n"), valueStr, (TCHAR*)rowset[ rowsetPos ].dt_smallinteger_s , __LINE__);
                rc = false;
            }
            if( _tcsncmp( (TCHAR*)rowset[ rowsetPos ].dt_smallinteger_u,   _T("1"), (int)rowset[ rowsetPos ].ptr_smallinteger_u ) != 0 )
            {
                RecordToLog( _T("ERROR: Data type: dt_smallinteger_u Expected: %s Actual %s at line %d\n"), valueStr, (TCHAR*)rowset[ rowsetPos ].dt_smallinteger_u , __LINE__);
                rc = false;
            }
            if( _tcsncmp( (TCHAR*)rowset[ rowsetPos ].dt_integer_s,        valueStr, (int)rowset[ rowsetPos ].ptr_integer_s ) != 0 )
            {
                RecordToLog( _T("ERROR: Data type: dt_integer_s Expected: %s Actual %s at line %d\n"), valueStr, (TCHAR*)rowset[ rowsetPos ].dt_integer_s, __LINE__ );
                rc = false;
            }
            if( _tcsncmp( (TCHAR*)rowset[ rowsetPos ].dt_integer_u,        valueStr, (int)rowset[ rowsetPos ].ptr_integer_u ) != 0 )            
            {
                RecordToLog( _T("ERROR: Data type: dt_integer_u Expected: %s Actual %s at line %d\n"), valueStr, (TCHAR*)rowset[ rowsetPos ].dt_integer_u, __LINE__ );
                rc = false;
            }
            if( _tcsncmp( (TCHAR*)rowset[ rowsetPos ].dt_largeint,         valueStr, (int)rowset[ rowsetPos ].ptr_largeint ) != 0 )
            {
                RecordToLog( _T("ERROR: Data type: dt_largeint Expected: %s Actual %s at line %d\n"), valueStr, (TCHAR*)rowset[ rowsetPos ].dt_largeint, __LINE__ );
                rc = false;
            }
            if( _tcsncmp( (TCHAR*)rowset[ rowsetPos ].dt_real,         valueStrReal, (int)rowset[ rowsetPos ].ptr_real ) != 0 )
            {
                RecordToLog( _T("ERROR: Data type: dt_real Expected: %s Actual %s at line %d\n"), valueStr, (TCHAR*)rowset[ rowsetPos ].dt_real , __LINE__);
                rc = false;
            }
            if( _tcsncmp( (TCHAR*)rowset[ rowsetPos ].dt_float,        valueStrReal, (int)rowset[ rowsetPos ].ptr_float ) != 0 )
            {
                RecordToLog( _T("ERROR: Data type: dt_float Expected: %s Actual %s at line %d\n"), valueStr, (TCHAR*)rowset[ rowsetPos ].dt_float, __LINE__ );
                rc = false;
            }
            if( _tcsncmp( (TCHAR*)rowset[ rowsetPos ].dt_double_precision, valueStrReal, (int)rowset[ rowsetPos ].ptr_double_precision ) != 0 )
            {
                RecordToLog( _T("ERROR: Data type: dt_double_precision Expected: %s Actual %s at line %d\n"), valueStr, (TCHAR*)rowset[ rowsetPos ].dt_double_precision, __LINE__ );
                rc = false;
            }

			if (tableFeatures[ unitTest.tableFeature ] == BEFORETRIGGER) {
				if( _tcsncmp( (TCHAR*)rowset[ rowsetPos ].dt_bignum_s, _T("987654321098765"), (int)rowset[ rowsetPos ].ptr_bignum_s ) != 0 )
				{
					RecordToLog( _T("ERROR: Data type: dt_bignum_s Expected: %s Actual %s at line %d\n"), valueStr, (TCHAR*)rowset[ rowsetPos ].dt_bignum_s, __LINE__ );
					rc = false;
				}
				if( _tcsncmp( (TCHAR*)rowset[ rowsetPos ].dt_bignum_u, _T("987654321098765"), (int)rowset[ rowsetPos ].ptr_bignum_u ) != 0 )
				{
					RecordToLog( _T("ERROR: Data type: dt_bignum_u Expected: %s Actual %s at line %d\n"), valueStr, (TCHAR*)rowset[ rowsetPos ].dt_bignum_u, __LINE__ );
					rc = false;
				}
			}
			else
			{
				if( _tcsncmp( (TCHAR*)rowset[ rowsetPos ].dt_bignum_s, _T("1234567890123456789"), (int)rowset[ rowsetPos ].ptr_bignum_s ) != 0 )
				{
					RecordToLog( _T("ERROR: Data type: dt_bignum_s Expected: %s Actual %s at line %d\n"), valueStr, (TCHAR*)rowset[ rowsetPos ].dt_bignum_s, __LINE__ );
					rc = false;
				}
				if( _tcsncmp( (TCHAR*)rowset[ rowsetPos ].dt_bignum_u, _T("1234567890123456789"), (int)rowset[ rowsetPos ].ptr_bignum_u ) != 0 )
				{
					RecordToLog( _T("ERROR: Data type: dt_bignum_u Expected: %s Actual %s at line %d\n"), valueStr, (TCHAR*)rowset[ rowsetPos ].dt_bignum_u, __LINE__ );
					rc = false;
				}
			}

			if (errorChecking != MODE_SPECIAL_1) {
				if( rowset[ rowsetPos ].dt_date.year  != 2000 )
				{
					RecordToLog( _T("ERROR: Data type: dt_date.year Expected: %d Actual %d\n"), 
							2000, rowset[ rowsetPos ].dt_date.year );
					rc = false;
				}
				if( rowset[ rowsetPos ].dt_date.month != 1 )
				{
					RecordToLog( _T("ERROR: Data type: dt_date.month Expected: %d Actual %d\n"), 
							1, rowset[ rowsetPos ].dt_date.month );
					rc = false;
				}
				if( rowset[ rowsetPos ].dt_date.day   != 2 )
				{
					RecordToLog( _T("ERROR: Data type: dt_date.day Expected: %d Actual %d\n"), 
							2, rowset[ rowsetPos ].dt_date.day );
					rc = false;
				}
				if( rowset[ rowsetPos ].dt_time.hour   != 3 )
				{
					RecordToLog( _T("ERROR: Data type: dt_time.hour Expected: %d Actual %d\n"), 
							3, rowset[ rowsetPos ].dt_time.hour );
					rc = false;
				}
				if( rowset[ rowsetPos ].dt_time.minute != 4 )
				{
					RecordToLog( _T("ERROR: Data type: dt_time.minute Expected: %d Actual %d\n"), 
							4, rowset[ rowsetPos ].dt_time.minute );
					rc = false;
				}
				if( rowset[ rowsetPos ].dt_time.second != 5 )
				{
					RecordToLog( _T("ERROR: Data type: dt_time.second Expected: %d Actual %d\n"), 
							5, rowset[ rowsetPos ].dt_time.second );
					rc = false;
				}
				if( rowset[ rowsetPos ].dt_timestamp.year     != 2000 )
				{
					RecordToLog( _T("ERROR: Data type: dt_timestamp.year Expected: %d Actual %d\n"), 
							2000, rowset[ rowsetPos ].dt_timestamp.year );
					rc = false;
				}
				if( rowset[ rowsetPos ].dt_timestamp.month    != 1 )
				{
					RecordToLog( _T("ERROR: Data type: dt_timestamp.month Expected: %d Actual %d\n"), 
							1, rowset[ rowsetPos ].dt_timestamp.month );
					rc = false;
				}
				if( rowset[ rowsetPos ].dt_timestamp.day      != 2 )
				{
					RecordToLog( _T("ERROR: Data type: dt_timestamp.day Expected: %d Actual %d\n"), 
							2, rowset[ rowsetPos ].dt_timestamp.day );
					rc = false;
				}
				if( rowset[ rowsetPos ].dt_timestamp.hour     != 3 )
				{
					RecordToLog( _T("ERROR: Data type: dt_timestamp.hour Expected: %d Actual %d\n"), 
							3, rowset[ rowsetPos ].dt_timestamp.hour );
					rc = false;
				}
				if( rowset[ rowsetPos ].dt_timestamp.minute   != 4 )
				{
					RecordToLog( _T("ERROR: Data type: dt_timestamp.minute Expected: %d Actual %d\n"), 
							4, rowset[ rowsetPos ].dt_timestamp.minute );
					rc = false;
				}
				if( rowset[ rowsetPos ].dt_timestamp.second   != 5 )
				{
					RecordToLog( _T("ERROR: Data type: dt_timestamp.second Expected: %d Actual %d\n"), 
							5, rowset[ rowsetPos ].dt_timestamp.second );
					rc = false;
				}
				if( rowset[ rowsetPos ].dt_timestamp.fraction != 600000 )
				{
					RecordToLog( _T("ERROR: Data type: dt_timestamp.fraction Expected: %d Actual %d\n"), 
							600000, rowset[ rowsetPos ].dt_timestamp.fraction );
					rc = false;
				}
			}
            break;

        case COLUMN:
		//Checked size of data returned
		if (ptr_char_utf8[ rowsetPos ] != size_char_utf8) {
	              RecordToLog( _T("ERROR: Data type: ptr_char_utf8 Expected: %d Actual %d at line %d\n"), size_char_utf8, ptr_char_utf8[ rowsetPos ], __LINE__ );
       	         rc = false;			
		}
		else {
			if (debug)
				RecordToLog( _T("Data type matched: ptr_char_utf8 Expected: %d Actual %d at line %d\n"), size_char_utf8, ptr_char_utf8[ rowsetPos ], __LINE__ );
		}
		if (ptr_char_ucs[ rowsetPos ] != size_char_charset) {
                RecordToLog( _T("ERROR: Data type: ptr_char_ucs Expected: %d Actual %d at line %d\n"), size_char_charset, ptr_char_ucs[ rowsetPos ], __LINE__ );
                rc = false;			
		}
		else {
			if (debug)
				RecordToLog( _T("Data type matched: ptr_char_ucs Expected: %d Actual %d at line %d\n"), size_char_charset, ptr_char_ucs[ rowsetPos ], __LINE__ );
		}
		if (ptr_varchar_utf8[ rowsetPos ] != size_varchar_utf8) {
              	RecordToLog( _T("ERROR: Data type: ptr_varchar_utf8 Expected: %d Actual %d at line %d\n"), size_varchar_utf8, ptr_varchar_utf8[ rowsetPos ], __LINE__ );
              	rc = false;			
		}
		else {
			if (debug)
				RecordToLog( _T("Data type matched: ptr_varchar_utf8 Expected: %d Actual %d at line %d\n"), size_varchar_utf8, ptr_varchar_utf8[ rowsetPos ], __LINE__ );
		}
		if (ptr_varchar_ucs[ rowsetPos ] != size_varchar_charset) {
                RecordToLog( _T("ERROR: Data type: ptr_varchar_ucs Expected: %d Actual %d at line %d\n"), size_varchar_charset, ptr_varchar_ucs[ rowsetPos ], __LINE__ );
                rc = false;			
		}
		else {
			if (debug)
				RecordToLog( _T("Data type matched: ptr_varchar_ucs Expected: %d Actual %d at line %d\n"), size_varchar_charset, ptr_varchar_ucs[ rowsetPos ], __LINE__ );
		}
		if (ptr_longvarchar_utf8[ rowsetPos ] != size_varchar_utf8) {
                RecordToLog( _T("ERROR: Data type: ptr_longvarchar_utf8 Expected: %d Actual %d at line %d\n"), size_varchar_utf8, ptr_longvarchar_utf8[ rowsetPos ], __LINE__ );
                rc = false;			
		}
		else {
			if (debug)
				RecordToLog( _T("Data type matched: ptr_longvarchar_utf8 Expected: %d Actual %d at line %d\n"), size_varchar_utf8, ptr_longvarchar_utf8[ rowsetPos ], __LINE__ );
		}
		if (ptr_longvarchar_ucs[ rowsetPos ] != size_varchar_charset) {
                RecordToLog( _T("ERROR: Data type: ptr_longvarchar_ucs Expected: %d Actual %d at line %d\n"), size_varchar_charset, ptr_longvarchar_ucs[ rowsetPos ], __LINE__ );
                rc = false;			
		}
		else {
			if (debug)
				RecordToLog( _T("Data type matched: ptr_longvarchar_ucs Expected: %d Actual %d at line %d\n"), size_varchar_charset, ptr_longvarchar_ucs[ rowsetPos ], __LINE__ );
		}
		if (ptr_nchar[ rowsetPos ] != size_char_charset) {
                RecordToLog( _T("ERROR: Data type: ptr_nchar Expected: %d Actual %d at line %d\n"), size_char_charset, ptr_nchar[ rowsetPos ], __LINE__ );
                rc = false;			
		}
		else {
			if (debug)
				RecordToLog( _T("Data type matched: ptr_nchar Expected: %d Actual %d at line %d\n"), size_char_charset, ptr_nchar[ rowsetPos ], __LINE__ );
		}
		if (ptr_ncharvarying[ rowsetPos ] != size_varchar_charset) {
                RecordToLog( _T("ERROR: Data type: ptr_ncharvarying Expected: %d Actual %d at line %d\n"), size_varchar_charset, ptr_ncharvarying[ rowsetPos ], __LINE__ );
                rc = false;			
		}
		else {
			if (debug)
				RecordToLog( _T("Data type matched: ptr_ncharvarying Expected: %d Actual %d at line %d\n"), size_varchar_charset, ptr_ncharvarying[ rowsetPos ], __LINE__ );
		}

		//Check value of data returned
		if( _tcsncmp( (TCHAR*)&dt_char_utf8[ rowsetPos * STRINGMAX ], valueStrSizedUtf8, _tcslen(valueStrSizedUtf8) ) != 0 )
        {
            RecordToLog( _T("ERROR: Data type: dt_char_utf8 Expected: %s Actual %s at line %d\n"), valueStrSizedUtf8, (TCHAR*)&dt_char_utf8[ rowsetPos * STRINGMAX ], __LINE__ );
            rc = false;
        }
        if( _tcscmp( (TCHAR*)&dt_char_ucs[ rowsetPos * STRINGMAX ], valueStrSizedCharset ) != 0 )
        {
            RecordToLog( _T("ERROR: Data type: dt_char_ucs Expected: %s Actual %s at line %d\n"), valueStrSizedCharset, (TCHAR*)&dt_char_ucs[ rowsetPos * STRINGMAX ], __LINE__ );
            rc = false;
        }
        if( _tcsncmp( (TCHAR*)&dt_varchar_utf8[ rowsetPos * STRINGMAX ],      ValueStrUtf8, _tcslen(ValueStrUtf8) ) != 0 )
        {
            RecordToLog( _T("ERROR: Data type: dt_varchar_utf8 Expected: %s Actual %s at line %d\n"), ValueStrUtf8, (TCHAR*)&dt_varchar_utf8[ rowsetPos * STRINGMAX ] , __LINE__);
            rc = false;
        }
        if( _tcscmp( (TCHAR*)&dt_varchar_ucs[ rowsetPos * STRINGMAX ],      valueStrCharset ) != 0 )
        {
            RecordToLog( _T("ERROR: Data type: dt_varchar_ucs Expected: %s Actual %s at line %d\n"), valueStrCharset, (TCHAR*)&dt_varchar_ucs[ rowsetPos * STRINGMAX ], __LINE__ );
            rc = false;
        }
        if( _tcsncmp( (TCHAR*)&dt_longvarchar_utf8[ rowsetPos * STRINGMAX ],  ValueStrUtf8, _tcslen(ValueStrUtf8) ) != 0 )
        {
            RecordToLog( _T("ERROR: Data type: dt_longvarchar_utf8 Expected: %s Actual %s at line %d\n"), ValueStrUtf8, (TCHAR*)&dt_longvarchar_utf8[ rowsetPos * STRINGMAX ], __LINE__ );
            rc = false;
        }
        if( _tcscmp( (TCHAR*)&dt_longvarchar_ucs[ rowsetPos * STRINGMAX ],  valueStrCharset ) != 0 )            
        {
            RecordToLog( _T("ERROR: Data type: dt_longvarchar_ucs Expected: %s Actual %s at line %d\n"), valueStrCharset, (TCHAR*)&dt_longvarchar_ucs[ rowsetPos * STRINGMAX ], __LINE__ );
            rc = false;
        }
        if( _tcscmp( (TCHAR*)&dt_nchar[ rowsetPos * STRINGMAX ],       valueStrSizedCharset ) != 0 )
        {
            RecordToLog( _T("ERROR: Data type: dt_nchar Expected: %s Actual %s at line %d\n"), valueStrSizedCharset, (TCHAR*)&dt_nchar[ rowsetPos * STRINGMAX ] , __LINE__);
            rc = false;
        }
        if( _tcscmp( (TCHAR*)&dt_ncharvarying[ rowsetPos * STRINGMAX ],     valueStrCharset ) != 0 )
        {
            RecordToLog( _T("ERROR: Data type: dt_ncharvarying Expected: %s Actual %s at line %d\n"), valueStrCharset, (TCHAR*)&dt_ncharvarying[ rowsetPos * STRINGMAX ], __LINE__ );
            rc = false;
        }
		if( _tcsncmp( (TCHAR*)&dt_decimal_s[ rowsetPos * STRINGMAX ],        _T("1"), (int)ptr_decimal_s[ rowsetPos ] ) != 0 )
        {
            RecordToLog( _T("ERROR: Data type: dt_decimal_s Expected: %s Actual %s at line %d\n"), valueStr, (TCHAR*)&dt_decimal_s[ rowsetPos * STRINGMAX ] , __LINE__);
            rc = false;
        }
        if( _tcsncmp( (TCHAR*)&dt_decimal_u[ rowsetPos * STRINGMAX ],        valueStr, (int)ptr_decimal_u[ rowsetPos ] ) != 0 )
        {
            RecordToLog( _T("ERROR: Data type: dt_decimal_u Expected: %s Actual %s at line %d\n"), valueStr, (TCHAR*)&dt_decimal_u[ rowsetPos * STRINGMAX ] , __LINE__);
            rc = false;
        }
        if( _tcsncmp( (TCHAR*)&dt_numeric_s[ rowsetPos * STRINGMAX ],        _T("1"), (int)ptr_numeric_s[ rowsetPos ] ) != 0 )
        {
            RecordToLog( _T("ERROR: Data type: dt_numeric_s Expected: %s Actual %s at line %d\n"), valueStr, (TCHAR*)&dt_numeric_s[ rowsetPos * STRINGMAX ], __LINE__ );
            rc = false;
        }
        if( _tcsncmp( (TCHAR*)&dt_numeric_u[ rowsetPos * STRINGMAX ],        _T("1"), (int)ptr_numeric_u[ rowsetPos ] ) != 0 )
        {
            RecordToLog( _T("ERROR: Data type: dt_numeric_u Expected: %s Actual %s at line %d\n"), valueStr, (TCHAR*)&dt_numeric_u[ rowsetPos * STRINGMAX ], __LINE__ );
            rc = false;
        }
        if( _tcsncmp( (TCHAR*)&dt_tinyint_s[ rowsetPos * STRINGMAX ],        _T("1"), (int)ptr_tinyint_s[ rowsetPos ] ) != 0 )
        {
            RecordToLog( _T("ERROR: Data type: dt_tinyint_s Expected: %s Actual %s at line %d\n"), valueStr, (TCHAR*)&dt_tinyint_s[ rowsetPos * STRINGMAX ], __LINE__ );
            rc = false;
        }
        if( _tcsncmp( (TCHAR*)&dt_tinyint_u[ rowsetPos * STRINGMAX ],        _T("1"), (int)ptr_tinyint_u[ rowsetPos ] ) != 0 )
        {
            RecordToLog( _T("ERROR: Data type: dt_tinyint_u Expected: %s Actual %s at line %d\n"), valueStr, (TCHAR*)&dt_tinyint_u[ rowsetPos * STRINGMAX ] , __LINE__);
            rc = false;
        }
        if( _tcsncmp( (TCHAR*)&dt_smallinteger_s[ rowsetPos * STRINGMAX ],   _T("1"), (int)ptr_smallinteger_s[ rowsetPos ] ) != 0 )
        {
            RecordToLog( _T("ERROR: Data type: dt_smallinteger_s Expected: %s Actual %s at line %d\n"), valueStr, (TCHAR*)&dt_smallinteger_s[ rowsetPos * STRINGMAX ] , __LINE__);
            rc = false;
        }
        if( _tcsncmp( (TCHAR*)&dt_smallinteger_u[ rowsetPos * STRINGMAX ],   _T("1"), (int)ptr_smallinteger_u[ rowsetPos ] ) != 0 )
        {
            RecordToLog( _T("ERROR: Data type: dt_smallinteger_u Expected: %s Actual %s at line %d\n"), valueStr, (TCHAR*)&dt_smallinteger_u[ rowsetPos * STRINGMAX ] , __LINE__);
            rc = false;
        }
        if( _tcsncmp( (TCHAR*)&dt_integer_s[ rowsetPos * STRINGMAX ],        valueStr, (int)ptr_integer_s[ rowsetPos ] ) != 0 )
        {
            RecordToLog( _T("ERROR: Data type: dt_integer_s Expected: %s Actual %s at line %d\n"), valueStr, (TCHAR*)&dt_integer_s[ rowsetPos * STRINGMAX ], __LINE__ );
            rc = false;
        }
        if( _tcsncmp( (TCHAR*)&dt_integer_u[ rowsetPos * STRINGMAX ],        valueStr, (int)ptr_integer_u[ rowsetPos ] ) != 0 )            
        {
            RecordToLog( _T("ERROR: Data type: dt_integer_u Expected: %s Actual %s at line %d\n"), valueStr, (TCHAR*)&dt_integer_u[ rowsetPos * STRINGMAX ], __LINE__ );
            rc = false;
        }
        if( _tcsncmp( (TCHAR*)&dt_largeint[ rowsetPos * STRINGMAX ],         valueStr, (int)ptr_largeint[ rowsetPos ] ) != 0 )
        {
            RecordToLog( _T("ERROR: Data type: dt_largeint Expected: %s Actual %s at line %d\n"), valueStr, (TCHAR*)&dt_largeint[ rowsetPos * STRINGMAX ], __LINE__ );
            rc = false;
        }
        if( _tcsncmp( (TCHAR*)&dt_real[ rowsetPos * STRINGMAX ],         valueStrReal, (int)ptr_real[ rowsetPos ] ) != 0 )
        {
            RecordToLog( _T("ERROR: Data type: dt_real Expected: %s Actual %s at line %d\n"), valueStr, (TCHAR*)&dt_real[ rowsetPos * STRINGMAX ] , __LINE__);
            rc = false;
        }
        if( _tcsncmp( (TCHAR*)&dt_float[ rowsetPos * STRINGMAX ],        valueStrReal, (int)ptr_float[ rowsetPos ] ) != 0 )
        {
            RecordToLog( _T("ERROR: Data type: dt_float Expected: %s Actual %s at line %d\n"), valueStr, (TCHAR*)&dt_float[ rowsetPos * STRINGMAX ], __LINE__ );
            rc = false;
        }
        if( _tcsncmp( (TCHAR*)&dt_double_precision[ rowsetPos * STRINGMAX ], valueStrReal, (int)ptr_double_precision[ rowsetPos ] ) != 0 )
        {
            RecordToLog( _T("ERROR: Data type: dt_double_precision Expected: %s Actual %s at line %d\n"), valueStr, (TCHAR*)&dt_double_precision[ rowsetPos * STRINGMAX ], __LINE__ );
            rc = false;
        }

		if (tableFeatures[ unitTest.tableFeature ] == BEFORETRIGGER) {
			if( _tcsncmp( (TCHAR*)&dt_bignum_s[ rowsetPos * STRINGMAX ], _T("987654321098765"), (int)ptr_bignum_s[ rowsetPos ] ) != 0 )
			{
				RecordToLog( _T("ERROR: Data type: dt_bignum_s Expected: %s Actual %s at line %d\n"), valueStr, (TCHAR*)&dt_bignum_s[ rowsetPos * STRINGMAX ], __LINE__ );
				rc = false;
			}
			if( _tcsncmp( (TCHAR*)&dt_bignum_u[ rowsetPos * STRINGMAX ], _T("987654321098765"), (int)ptr_bignum_u[ rowsetPos ] ) != 0 )
			{
				RecordToLog( _T("ERROR: Data type: dt_bignum_u Expected: %s Actual %s at line %d\n"), valueStr, (TCHAR*)&dt_bignum_u[ rowsetPos * STRINGMAX ], __LINE__ );
				rc = false;
			}
		}
		else
		{
			if( _tcsncmp( (TCHAR*)&dt_bignum_s[ rowsetPos * STRINGMAX ], _T("1234567890123456789"), (int)ptr_bignum_s[ rowsetPos ] ) != 0 )
			{
				RecordToLog( _T("ERROR: Data type: dt_bignum_s Expected: %s Actual %s at line %d\n"), valueStr, (TCHAR*)&dt_bignum_s[ rowsetPos * STRINGMAX ], __LINE__ );
				rc = false;
			}
			if( _tcsncmp( (TCHAR*)&dt_bignum_u[ rowsetPos * STRINGMAX ], _T("1234567890123456789"), (int)ptr_bignum_u[ rowsetPos ] ) != 0 )
			{
				RecordToLog( _T("ERROR: Data type: dt_bignum_u Expected: %s Actual %s at line %d\n"), valueStr, (TCHAR*)&dt_bignum_u[ rowsetPos * STRINGMAX ], __LINE__ );
				rc = false;
			}
		}

		if (errorChecking != MODE_SPECIAL_1) {
			if( (int)dt_date[ rowsetPos ].year  != 2000 )
			{
				RecordToLog( _T("ERROR: Data type: dt_date.year Expected: %d Actual %d\n"), 
						2000, dt_date[ rowsetPos ].year );
				rc = false;
			}
			if( (int)dt_date[ rowsetPos ].month != 1 )
			{
				RecordToLog( _T("ERROR: Data type: dt_date.month Expected: %d Actual %d\n"), 
						1, dt_date[ rowsetPos ].month );
				rc = false;
			}
			if( (int)dt_date[ rowsetPos ].day   != 2 )
			{
				RecordToLog( _T("ERROR: Data type: dt_date.day Expected: %d Actual %d\n"), 
						2, dt_date[ rowsetPos ].day );
				rc = false;
			}
			if( (int)dt_time[ rowsetPos ].hour   != 3 )
			{
				RecordToLog( _T("ERROR: Data type: dt_time.hour Expected: %d Actual %d\n"), 
						3, dt_time[ rowsetPos ].hour );
				rc = false;
			}
			if( (int)dt_time[ rowsetPos ].minute != 4 )
			{
				RecordToLog( _T("ERROR: Data type: dt_time.minute Expected: %d Actual %d\n"), 
						4, dt_time[ rowsetPos ].minute );
				rc = false;
			}
			if( (int)dt_time[ rowsetPos ].second != 5 )
			{
				RecordToLog( _T("ERROR: Data type: dt_time.second Expected: %d Actual %d\n"), 
						5, dt_time[ rowsetPos * STRINGMAX ].second );
				rc = false;
			}
			if( (int)dt_timestamp[ rowsetPos ].year     != 2000 )
			{
				RecordToLog( _T("ERROR: Data type: dt_timestamp.year Expected: %d Actual %d\n"), 
						2000, dt_timestamp[ rowsetPos ].year );
				rc = false;
			}
			if( (int)dt_timestamp[ rowsetPos ].month    != 1 )
			{
				RecordToLog( _T("ERROR: Data type: dt_timestamp.month Expected: %d Actual %d\n"), 
						1, dt_timestamp[ rowsetPos ].month );
				rc = false;
			}
			if( (int)dt_timestamp[ rowsetPos ].day      != 2 )
			{
				RecordToLog( _T("ERROR: Data type: dt_timestamp.day Expected: %d Actual %d\n"), 
						2, dt_timestamp[ rowsetPos ].day );
				rc = false;
			}
			if( (int)dt_timestamp[ rowsetPos ].hour     != 3 )
			{
				RecordToLog( _T("ERROR: Data type: dt_timestamp.hour Expected: %d Actual %d\n"), 
						3, dt_timestamp[ rowsetPos ].hour );
				rc = false;
			}
			if( (int)dt_timestamp[ rowsetPos ].minute   != 4 )
			{
				RecordToLog( _T("ERROR: Data type: dt_timestamp.minute Expected: %d Actual %d\n"), 
						4, dt_timestamp[ rowsetPos ].minute );
				rc = false;
			}
			if( (int)dt_timestamp[ rowsetPos ].second   != 5 )
			{
				RecordToLog( _T("ERROR: Data type: dt_timestamp.second Expected: %d Actual %d\n"), 
						5, dt_timestamp[ rowsetPos ].second );
				rc = false;
			}
			if( (int)dt_timestamp[ rowsetPos ].fraction != 600000 )
			{
				RecordToLog( _T("ERROR: Data type: dt_timestamp.fraction Expected: %d Actual %d\n"), 
						600000, dt_timestamp[ rowsetPos ].fraction );
				rc = false;
			}
		}			
              break;

		default:
			RecordToLog( _T("INTERNAL ERROR: An unknown access style has been discovered at line %d.\n"), __LINE__ );
			rc = false;
			break;
    }
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
    int numberOfRowsRetrieved = 0;
    
    // Run the prepared select statement. 
    if( operations[ unitTest.operation ] == PREPARE_EXECUTE )
    {
        while( ( retcode = SQLExecute( handle[ SQL_HANDLE_STMT ] ) ) == SQL_STILL_EXECUTING );
    }
    else
    {
        while( (retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStr[ 3 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
    }
    
    if( retcode != SQL_SUCCESS )    
    {
        if( retcode != SQL_SUCCESS_WITH_INFO )
        {
            CheckMsgs( _T("SQLExecute()"), __LINE__ );
            FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
            return false;
        }
    }
    
    // Gather the data.
    while( retcode != SQL_NO_DATA ) 
    {
        //while( ( retcode = SQLFetchScroll( handle[ SQL_HANDLE_STMT ], SQL_FETCH_NEXT, 0 ) ) == SQL_STILL_EXECUTING );
        while( ( retcode = SQLFetch( handle[ SQL_HANDLE_STMT ] ) ) == SQL_STILL_EXECUTING );
        if( retcode == SQL_NO_DATA )
        {
            break;
        }
        if( retcode != SQL_SUCCESS )
        {
            CheckMsgs( _T("SQLFetch()"), __LINE__ );
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
                RecordToLog(_T(" >> ERROR: Rowset status array row %d was expected to have SQL_ROW_SUCCESS or SQL_ROW_SUCCESS_WITH_INFO. Actual: %d at line %d.\n"), rowPos, rowsetStatusArray[ rowPos ] , __LINE__); 
                rc = false;
            }
        }
    }

    if( numberOfRowsRetrieved != goodRowCount)
    {
        RecordToLog(_T(" >> ERROR: The number of rows expected (%d) does not match the number of rows retrieved (%d) at line %d.\n"), goodRowCount, numberOfRowsRetrieved, __LINE__);
        rc = false;
    }
    if( !gatheredData && (goodRowCount != 0))
    {
        RecordToLog(_T(" >> ERROR: No data was returned from SELECT statement at line %d.\n"), __LINE__ ); 
        rc = false;
    }

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
    
    for ( numberOfRowsHandled = 0; numberOfRowsHandled < numberOfRows[ unitTest.numberOfRows ]; )
    {
        failureInjectionCount = 0;
		goodRowCount = 0;
        // Assign the values in the rowsetnumberOfRows
        for( rs = 0; ( rs < rowsetSizes[ unitTest.rowsetSize ] ) && ( rs < numberOfRows[ unitTest.numberOfRows ] )&& ( numberOfRowsHandled < numberOfRows[ unitTest.numberOfRows ] ); rs++ )
        {
			unsigned int bitflag = 0;
            switch( injectionTypes[ unitTest.injectionType ] )
            {
				/***********************************************************************/
                case NO_ERRORS:
					bitflag = B_NOERRORS;
					goodRowCount++;
                    break;
				/***********************************************************************/
				/***********************************************************************/
                case DUPLICATEKEY:
                    if( ( ( rs + 1 ) % 5 ) == 0 )
                    {
                        // Inject an error.
						bitflag = B_DUPLICATEKEY;
                        //The Multiset tables is excepting duplicate keys
                        if( tableTypes[ unitTest.tableType ] == MULTISET )
                        {
							goodRowCount++;
							if ( actions[ unitTest.action ] == UPDATE )
								goodRowCount += 3;
                        }
						else
						{
							if ( actions[ unitTest.action ] == UPDATE )
								goodRowCount++;
						}
                    }
                    else
                    {
                        // Do not inject an error.
						bitflag = B_NOERRORS;
						goodRowCount++;
                    }
                   break;
				/***********************************************************************/
				/***********************************************************************/
                case UNIQUECONST:
                    if( ( ( rs + 1 ) % 5 ) == 0 )
                    {
                        // Inject an error.
						bitflag = B_CHECKCONST;
                    }
                    else
                    {
                        // Do not inject an error.
						bitflag = B_NOERRORS;
						goodRowCount++;
                    }
                    break;
				/***********************************************************************/
				/***********************************************************************/
                case DUPLICATEROW:
					if( ( ( rs + 1 ) % 5 ) == 0 )
					{
						// Inject an inclusive duplicate row.
						bitflag = B_DUPLICATEROW;
						//The Multiset tables is excepting duplicate keys
						if( tableTypes[ unitTest.tableType ] == MULTISET )
						{
							goodRowCount++;
							if ( actions[ unitTest.action ] == UPDATE )
								goodRowCount += 3;
						}
						else
						{
							if ( actions[ unitTest.action ] == UPDATE )
								goodRowCount++;
						}
					}
					else
					{
						// Do not inject an error.
						bitflag = B_NOERRORS;
						goodRowCount++;
					}
					break;
				/***********************************************************************/
				/***********************************************************************/
                case OVERFLOW:
					if( ( ( rs + 1 ) % 5 ) == 0 )
                    {
                        // Inject an error.
						bitflag = B_STRINGOVERFLOW;
						// SQ goodRowCount++;
                    }
					else {
                        // Do not inject an error.
						bitflag = B_NOERRORS;
						goodRowCount++;
					}
                    break;
				/***********************************************************************/
				/***********************************************************************/
                case NULLVALUE:
                    if( ( ( rs + 1 ) % 5 ) == 0 ) {
                        // Inject an error.
						bitflag = B_NULLVALUE;
					}
					else {
                        // Do not inject an error.
						bitflag = B_NOERRORS;
						goodRowCount++;
					}
                    break;
				/***********************************************************************/
				/***********************************************************************/
               case CANCEL:
					expectedRowsetStatusArray[rs] = SQL_PARAM_SUCCESS;
                    AssignRow( rs, numberOfRowsHandled + 1, numberOfRowsHandled + 1 );
                    break;
				/***********************************************************************/
				/***********************************************************************/
                case SELECTIVE:
                    if( ( ( rs + 1 ) % 5 ) == 0 )
                    {
                        // We exclude this row selectively to not be processed.
                        rowsetOperationArray[ rs ] = SQL_PARAM_IGNORE;
						expectedRowsetStatusArray[rs] = SQL_PARAM_ERROR;
                        failureInjectionCount++;
                    } 
                    else
                    {
                        // We make sure we reset the good rows to become processed. 
                        rowsetOperationArray[ rs ] = SQL_PARAM_PROCEED;
						expectedRowsetStatusArray[rs] = SQL_PARAM_SUCCESS;
                    }
                    AssignRow( rs, numberOfRowsHandled + 1, numberOfRowsHandled + 1 );
                    break;
				/***********************************************************************/
				/***********************************************************************/
				case ERR_PER_ROW: // Some rows will be injected, and each row has different type of error.
					switch ( rs % 10) {
						case 0: //Check constraint
							if ( tableTypes[ unitTest.tableType ] != VOLATILE )
								bitflag = B_CHECKCONST;
							else
								bitflag = B_TIMESTAMP;;
							break;
						case 1:			//String overflow
							bitflag = B_STRINGOVERFLOW;
							// SQ goodRowCount++;
							break;
						case 2:			//Duplicated key
							bitflag = B_DUPLICATEKEY;
							//The Multiset tables is excepting duplicate keys
							if( tableTypes[ unitTest.tableType ] == MULTISET )
							{
								goodRowCount++;
								/* SQ 
								if ( actions[ unitTest.action ] == UPDATE )
									goodRowCount += 5;
								* end of SQ */
							}
							else
							{
								/* SQ if ( actions[ unitTest.action ] == UPDATE ) */  if ( actions[ unitTest.action ] == UPDATE || actions[ unitTest.action ] == DELETE_PARAM || actions[ unitTest.action ] == INSERT || actions[ unitTest.action ] == SELECT)
									goodRowCount++;
							}
							break;
						case 3:			//Duplicated rows
							bitflag = B_DUPLICATEROW | B_STRINGOVERFLOW;
							//The Multiset tables is excepting duplicate rows
							/* SQ 
							if( tableTypes[ unitTest.tableType ] == MULTISET )
							{
								goodRowCount++;
								if ( actions[ unitTest.action ] == UPDATE )
									goodRowCount += 5;
							}
							else
							{
								if ( actions[ unitTest.action ] == UPDATE )
									goodRowCount++;
							}
							end of SQ */
							break;
						case 4:			//Null value
							bitflag = B_NULLVALUE;
							break;
						case 5:			//Date, Time or Timestamp can not be converted
							bitflag = B_STRINGOVERFLOW;
							// SQ goodRowCount++;
							break;
						case 6:			//Divided by zero
							bitflag = B_STRINGOVERFLOW;
							// SQ goodRowCount++;
							break;
						case 7:			//Negative value can not be converted to unsigned datatype
							bitflag = B_SIGN2UNSIGN;
							break;
						case 8:			//Numeric overflow
							bitflag = B_NUMERICOVERFLOW;
							break;
						case 9:			//Timestamp
							bitflag = B_TIMESTAMP;
							break;
					}
					break;//ERR_PER_ROW		
				/***********************************************************************/
				/***********************************************************************/
				case FULL_ERRORS: // ??? Dont know, hehehe
					switch ( rs % 10) {
						case 0:	case 1: case 4: case 6: case 8: //String overflow
							bitflag = B_STRINGOVERFLOW;
							// SQ goodRowCount++;
							break;
#if 0 /* SQ old */
						case 2:	case 3: case 5: case 7: case 9:	//Duplicated Key
							bitflag = B_DUPLICATEKEY;
							//The Multiset tables is excepting duplicate keys
							if( tableTypes[ unitTest.tableType ] == MULTISET )
							{
								goodRowCount++;
								if ( actions[ unitTest.action ] == UPDATE )
									goodRowCount += 10;
							}
							else
							{
								if ( actions[ unitTest.action ] == UPDATE )
									goodRowCount++;
							}
#endif /* end of SQ old */
/* SQ new */
						case 2: //Duplicated Key  - only this row got inserted
							bitflag = B_DUPLICATEKEY;
							//The Multiset tables is excepting duplicate keys
							if( tableTypes[ unitTest.tableType ] == MULTISET )
							{
								goodRowCount++;
								if ( actions[ unitTest.action ] == UPDATE )
									goodRowCount += 10;
							}
							else
							{
								if ( actions[ unitTest.action ] == UPDATE || actions[ unitTest.action ] == SELECT || actions[ unitTest.action ] == DELETE_PARAM || actions[ unitTest.action ] == INSERT )
									goodRowCount++;
							}
							break;
						case 3: case 5: case 7: case 9: //Duplicated Key
							bitflag = B_DUPLICATEKEY;
							//The Multiset tables is excepting duplicate keys
							if( tableTypes[ unitTest.tableType ] == MULTISET )
							{
								goodRowCount++;
								if ( actions[ unitTest.action ] == UPDATE && (rs%10)==3 )
									goodRowCount += 10;
							}
							else
							{
								if ( actions[ unitTest.action ] == UPDATE )
									goodRowCount++;
							}
							break;
					}
					break;
				/***********************************************************************/
				/***********************************************************************/
				case DRIVER_GOOD_BAD_MULCOL://Some good rows, some error, multiple columns
					switch ( rs % 10) {
						case 0: case 2: case 4: case 6: case 8:	//Nullvalue, String overflow, numeric overflow, negative value to unsigned colunm
							bitflag = B_NULLVALUE | B_STRINGOVERFLOW | B_NUMERICOVERFLOW | B_SIGN2UNSIGN;
							break;
						case 1:	case 3:	case 5:	case 7:	case 9:	//Good row		
							bitflag = B_NOERRORS;
							goodRowCount++;
							break;
					}
					break;
				/***********************************************************************/
				/***********************************************************************/
				case DRIVER_GOOD_WARNING_MULCOL://Some good rows, no error, some warning, multiple columns
					switch ( rs % 10) {
						case 0: case 2: case 4: case 6: case 8:	case 9: //String overflow (this is the only warning I know so far)
							bitflag = B_STRINGOVERFLOW;
							// SQ goodRowCount++;
							break;
						case 1:	case 3:	case 5:	case 7:	//Good row		
							bitflag = B_NOERRORS;
							goodRowCount++;
							break;
					}
					break;
				/***********************************************************************/
				/***********************************************************************/
				case DRIVER_GOOD_BAD_WARNING_MULCOL://Some good rows, some errors, some warning, multiple columns
					switch ( rs % 10) {
						case 0: case 3:	case 6:	case 9:	//String overflow	
							bitflag = B_STRINGOVERFLOW;
							// SQ goodRowCount++;
							break;
						case 2:	case 5:	case 8:	//Nullvalue, String overflow, numeric overflow, negative value to unsigned colunm
							bitflag = B_NULLVALUE | B_STRINGOVERFLOW | B_NUMERICOVERFLOW | B_SIGN2UNSIGN;
							break;
						case 1:	case 4:	case 7:		//Good rows
							bitflag = B_NOERRORS;
							goodRowCount++;
							break;
					}
					break;
				/***********************************************************************/
				/***********************************************************************/
				case DRIVER_ALL_BAD_MULCOL://No good rows, all error, no warning, multiple columns
					switch ( rs % 10) {
						case 0: case 2: case 4: case 6: case 8:	//Nullvalue, String overflow, numeric overflow, negative value to unsigned colunm
							bitflag = B_NULLVALUE | B_STRINGOVERFLOW | B_NUMERICOVERFLOW | B_SIGN2UNSIGN;
							break;
						case 1:	case 3:	case 5:	case 7:	case 9:	//Nullvalue		
							bitflag = B_NULLVALUE;
							break;
					}
					break;
				/***********************************************************************/
				/***********************************************************************/
				case DRIVER_ALL_WARNING_MULCOL://No good row, no error, all warning, multiple columns
					switch ( rs % 10) {
						// SQ: B_STRINGOVERFLOW is considered as an error since R2.5.
						case 0: case 2: case 4: case 6: case 8:	case 9: //String overflow (this is the only warning I know so far)
							bitflag = B_STRINGOVERFLOW;
							// SQ goodRowCount++;
							break;
						case 1:	case 3:	case 5:	case 7:			
							bitflag = B_STRINGOVERFLOW;
							// SEAQUSET goodRowCount++;
							break;
					}
					break;
				/***********************************************************************/
				/***********************************************************************/
				case DRIVER_ALL_BAD_WARNING_MULCOL://No good row, half error and half warning, multiple columns
					switch ( rs % 10) {
						case 0: case 2: case 4: case 6: case 8:	//Nullvalue, String overflow, numeric overflow, negative value to unsigned colunm
							bitflag = B_NULLVALUE | B_STRINGOVERFLOW | B_NUMERICOVERFLOW | B_SIGN2UNSIGN;
							break;
						case 1:	case 3:	case 5:	case 7:	case 9:	//String overflow	
							bitflag = B_STRINGOVERFLOW;
							// SQ goodRowCount++;
							break;
					}
					break;
				/***********************************************************************/
				/***********************************************************************/
				case SERVER_GOOD_BAD_MULCOL://Some good rows, some bad rows, multiple columns (server error only with/without driver warning)
					switch ( rs % 10) {
						case 0: case 3:	case 6:	case 9:	//Check constraint, negative value to unsigned colunm
							bitflag = B_CHECKCONST | B_SIGN2UNSIGN;
							break;
						case 2:	case 5:	case 8: //Duplicated Key, String overflow
							bitflag = B_DUPLICATEKEY | B_STRINGOVERFLOW;
							//The Multiset tables is excepting duplicate keys
							/* SQ
							if( tableTypes[ unitTest.tableType ] == MULTISET )
							{
								goodRowCount++;
								if ( actions[ unitTest.action ] == UPDATE )
									goodRowCount += 4;
							}
							else
							{
								if ( actions[ unitTest.action ] == UPDATE )
									goodRowCount++;
							}
							end of SQ */
							break;
						case 1:	case 4:	case 7:		//Good rows
							bitflag = B_NOERRORS;
							goodRowCount++;
							break;
					}
					break;
				/***********************************************************************/
				/***********************************************************************/
				case SERVER_ALL_BAD_MULCOL://No good row, all errors, multiple columns (server error only with/without driver warning)
					switch ( rs % 10) {
						case 0: case 1: case 4:	case 5:	case 8: case 9:	//Check constraint, String overflow
							/**
							This is an temporary hack, since there is an inconsistent error-check in SQL Update.
							EX: UPDATE TABLE ROWSET_TABLE SET C1=10 WHERE C2=20;
							1. In B_CHECKCONST violation, SQL does WHERE operation first, then checks for a violation.
								which always returns SUCCESS if there is no row in the table.
							2. In B_SIGN2UNSIGN violationm, SQL checks a violation first, and then does WHERE operation.
								In this case, a sign value is assigned in to a unsign column will return a ERROR
								even there is no row in the table
							*/
							//if (tableTypes[ unitTest.tableType ] != VOLATILE)
							//{
							//	bitflag = B_CHECKCONST | B_STRINGOVERFLOW;
							//}
							//else
							//{
								bitflag = B_SIGN2UNSIGN | B_STRINGOVERFLOW;
							//}
							break;
						case 2:	case 3:	case 6: case 7: //Duplicated Key, negative value to unsigned colunm
							bitflag = B_DUPLICATEKEY | B_SIGN2UNSIGN;
							break;
					}
					break;
				/***********************************************************************/
				/***********************************************************************/
				case MIXED_DRIVERWARNING_SERVERBAD_GOOD_MULCOL://Some good rows, some driver warnings, some server errors, multiple columns
					switch ( rs % 10) {
						case 0: // Negative value into unsigned column
							bitflag = B_SIGN2UNSIGN;
							break;
						case 3: case 6:	case 8:	//Duplicated Key, check constraint
							if (tableTypes[ unitTest.tableType ] != VOLATILE) {
								bitflag = B_DUPLICATEKEY | B_CHECKCONST;
							}
							else
								bitflag = B_DUPLICATEKEY | B_NUMERICOVERFLOW;
							break;
						case 2:	case 5:	case 7: //String overflow
							bitflag = B_STRINGOVERFLOW;
							// SQ goodRowCount++;
							break;
						case 1:	case 4:	case 9:		//Good rows
							bitflag = B_NOERRORS;
							goodRowCount++;
							break;
					}
					break;
				/***********************************************************************/
				/***********************************************************************/
				case MIXED_DRIVERBAD_SERVERBAD_GOOD_MULCOL://Some good rows, some driver errors, some server errors, multiple columns
					switch ( rs % 10) {
						case 0: case 3: case 6:	//Server error, with driver warning: check constraint, negative value to unsigned colunm
							bitflag = B_CHECKCONST | B_STRINGOVERFLOW | B_SIGN2UNSIGN;
							break;
						case 8: case 9:	//Server error, without driver warning: Duplicated Key, check constraint
							if (tableTypes[ unitTest.tableType ] != VOLATILE) {
								bitflag = B_DUPLICATEKEY | B_CHECKCONST;
							}
							else
								bitflag = B_DUPLICATEKEY | B_SIGN2UNSIGN;
							break;
						case 2:	case 5:	case 7: //Driver error: Nullvalue, String overflow, numeric overflow, negative value to unsigned colunm
							bitflag = B_NULLVALUE | B_STRINGOVERFLOW | B_NUMERICOVERFLOW | B_SIGN2UNSIGN;
							break;
						case 1:	case 4:	//Good rows
							bitflag = B_NOERRORS;
							goodRowCount++;
							break;
					}
					break;
				/***********************************************************************/
				/***********************************************************************/
				case MIXED_DRIVERWARNING_DRIVERBAD_SERVERBAD_GOOD_MULCOL://Some good rows, some driver errors, some driver warnings, some server errors, multiple columns
					switch ( rs % 10) {
						case 0: case 3: case 8:	//Server error: Check constraint, negative value to a unsigned column
							bitflag = B_CHECKCONST | B_SIGN2UNSIGN;
							break;
						case 6: case 9:	//Driver warning: String overflow
							bitflag = B_STRINGOVERFLOW;
							// SQ goodRowCount++;
							break;
						case 2:	case 5:	case 7: //Driver error: Nullvalue, String overflow, numeric overflow
							bitflag = B_NULLVALUE | B_STRINGOVERFLOW | B_NUMERICOVERFLOW;
							break;
						case 1:	case 4:	//Good rows
							bitflag = B_NOERRORS;
							goodRowCount++;
							break;
					}
					break;
				/***********************************************************************/
				/***********************************************************************/
				case MIXED_DRIVERBAD_SERVERBAD_MULCOL://Driver errrors, server errors, no warning, no good row, multiple columns
					switch ( rs % 10) {
						case 0: case 3:	case 6:	case 9:	//Server error: Check constraint
							/**
							This is an temporary hack, since there is an inconsistent error-check in SQL Update.
							EX: UPDATE TABLE ROWSET_TABLE SET C1=10 WHERE C2=20;
							1. In B_CHECKCONST violation, SQL does WHERE operation first, then checks for a violation.
								which always returns SUCCESS if there is no row in the table.
							2. In B_SIGN2UNSIGN violationm, SQL checks a violation first, and then does WHERE operation.
								In this case, a sign value is assigned in to a unsign column will return a ERROR
								even there is no row in the table
							*/
							//if (tableTypes[ unitTest.tableType ] != VOLATILE) {
							//	bitflag = B_CHECKCONST;
							//}
							//else {
								bitflag = B_SIGN2UNSIGN;
							//}
							break;
						case 1:	case 4:	case 7: //Server error with warning: Duplicated Key, String overflow, negative value to unsigned colunm
							bitflag = B_DUPLICATEKEY | B_STRINGOVERFLOW | B_SIGN2UNSIGN;
							break;
						case 2:	case 5:	case 8: //Driver error
							bitflag = B_NULLVALUE | B_STRINGOVERFLOW | B_NUMERICOVERFLOW | B_SIGN2UNSIGN;
							break;
					}
					break;
				/***********************************************************************/
				/***********************************************************************/
				case MIXED_DRIVERWARNING_DRIVERBAD_SERVERBAD_MULCOL://Driver errrors, driver warnings, server errors, no good row, multiple columns
					switch ( rs % 10) {
						case 0:	case 3:	case 6: //Driver error: Nullvalue, numeric overflow
							bitflag = B_NULLVALUE | B_NUMERICOVERFLOW;
							break;
						case 1: case 4: case 7: case 9:	//Driver warning: String overflow
							bitflag = B_STRINGOVERFLOW;
							// SQ goodRowCount++;
							break;
						case 2: case 5: case 8:	//Server error: Duplicated Key, String overflow
							bitflag = B_DUPLICATEKEY | B_STRINGOVERFLOW;
							//The Multiset tables is excepting duplicate keys
							/* SQ
							if( tableTypes[ unitTest.tableType ] == MULTISET )
							{
								goodRowCount++;
								if ( actions[ unitTest.action ] == UPDATE )
									goodRowCount += 7;
							}
							else
							{
								if ( actions[ unitTest.action ] == UPDATE )
									goodRowCount++;
							}
							end of SQ */
							break;
					}
					break;
				/***********************************************************************/
				/***********************************************************************/
				default:
                    RecordToLog( _T(" >> INTERNAL ERROR: An unknown failure type has been discovered.\n") );
                    rc = false;
                    break;
            }

			DML_A_ROW(  bitflag,
						actions[ unitTest.action ],
						tableTypes[ unitTest.tableType ],
						bindOrientations[ unitTest.bindOrientation ],
						rs,
						&failureInjectionCount,
						numberOfRowsHandled
					);

			if (debug) DisplayRowsets(bindOrientations[ unitTest.bindOrientation ], rs);

            numberOfRowsHandled++;
        }

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
			case NULLVALUE:
			case OVERFLOW:
			case ERR_PER_ROW:
			case FULL_ERRORS:
			case DRIVER_GOOD_BAD_MULCOL:								//All error, some good rows, multiple columns
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
			case MIXED_DRIVERBAD_SERVERBAD_MULCOL:					//Driver errrors, server errors, no good row, multiple columns
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
                RecordToLog( _T(" >> INTERNAL ERROR: An unknown failure type has been discovered. at line=%d\n"), __LINE__ );
                rc = false;
                break;
		}

        // We might have to readjust the rowset size we supply to the driver.
        if( rs != rowsetSizes[ unitTest.rowsetSize ] )
        {
            retcode = SQLSetStmtAttr( handle[ SQL_HANDLE_STMT ], SQL_ATTR_PARAMSET_SIZE, (void *)rs, 0 );
            if( retcode != SQL_SUCCESS )    
            {
                CheckMsgs( _T("SQLSetStmtAttr()"), __LINE__ );
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
                    while( ( rowsetRetcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStr[ 2 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
                    break;
                case DELETE_PARAM:
                    while( ( rowsetRetcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStr[ 6 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
                    break;
                case UPDATE:
					while( ( rowsetRetcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStr[ 7 ], SQL_NTS ) ) == SQL_STILL_EXECUTING );
                    break;
                default:
                    RecordToLog( _T(" >> INTERNAL ERROR: An unknown table action has been discovered.\n") );
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
			RecordToLog( _T(" >> Failing API: SQLExecute/Direct(), expected: %d, actual: %d at line= %d\n"), expectedRowsetRetcode, rowsetRetcode, __LINE__ );
			CheckMsgs( _T("SQLExecute/Direct()"), __LINE__ );
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
                RecordToLog( _T(" >> Failing API: SQLEndTran()\n") );
                CheckMsgs( _T("SQLEndTran()"), __LINE__ );
                FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
                return false;
            }
            numIterations = 0;
        }

        // Check to make sure all the rows we inserted were processed.
        if ( (int)rowsProcessed != rs ) {
            RecordToLog(_T(" >> ERROR: The number of parameters processed does not match the number of rows prepared.\n"));
            RecordToLog(_T(" >> ERROR: Rows processed by ODBC: %d Rows prepared by client: %d\n"), (int)rowsProcessed, rs );
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
	      						if (debug) RecordToLog(_T("%13d  Success\n"), i+1);
      							break;
						case SQL_PARAM_SUCCESS_WITH_INFO:
         						if (debug) RecordToLog(_T("%13d  Success With Info\n"), i+1);
								pSuccessinfo = true;
         						break;
      						case SQL_PARAM_ERROR:
        						if (debug) RecordToLog(_T("%13d  Error  <-----\n"), i+1);
								pSuccessinfo = true;
        						break;
      						case SQL_PARAM_UNUSED:
								if (debug) RecordToLog(_T("%13d  Not processed\n"), i+1);
        						break;
     						case SQL_PARAM_DIAG_UNAVAILABLE:
        						if (debug) RecordToLog(_T("%13d  Unknown\n"), i+1);
        						break;
					}
			}
			else {
				RecordToLog(_T("%13d  ERROR: Rowset status array row %d was expected to have %s. Actual: %s at line %d.\n"), i+1, i+1, Param_Status_Ptr( expectedRowsetStatusArray[ i ] ), Param_Status_Ptr( rowsetStatusArray[ i ] ), __LINE__ );
				rc = false;
			}
		}

		if ((rowsetRetcode == SQL_SUCCESS && pSuccessinfo) ||
			(rowsetRetcode == SQL_SUCCESS_WITH_INFO && !pSuccessinfo)){
       		RecordToLog(_T(" >> ERROR: All the rows in rowset status array don't match with rowset returncode= %d, at line %d.\n"), rowsetRetcode, __LINE__ );
			rc = false;
		}

        // Check to make sure the row count of affected rows is correct.
        retcode = SQLRowCount( handle[ SQL_HANDLE_STMT ], &rowCount );
        if( retcode != SQL_SUCCESS )    
        {
            RecordToLog( _T("    Failing API: SQLRowCount()\n") );
            CheckMsgs( _T("SQLRowCount()"), __LINE__ );
            FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
            return false;
        }

        if (debug) RecordToLog( _T("ExpectedRowcount=%d , ActualRowcount=%d\n"), goodRowCount, rowCount );

		if( (int)rowCount != goodRowCount)
		{
			RecordToLog( _T(" >> ERROR: The number of expected good rows processed [%d] does not match the SQLRowCount() [%d] at line %d.\n"), goodRowCount, rowCount, __LINE__);
			rc = false;
		}
    }

    // Commit the rest of the rows.
    if ( features[ unitTest.feature ] != HASH2 )
    {
        retcode = SQLEndTran( SQL_HANDLE_DBC, handle[ SQL_HANDLE_DBC ], SQL_COMMIT );
        if( retcode != SQL_SUCCESS )    
        {
            RecordToLog( _T("\n    Failing API: SQLEndTran()\n") );
            CheckMsgs( _T("SQLEndTran()"), __LINE__ );
            FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
            return false;
        }
    }

	if(rc == false)
		DisplayTable(bindOrientations[ unitTest.bindOrientation ],rs );
    FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );

    return rc;
}

/****************************************************************
** ALM_LogTestCaseInfo(char*, char*, int, int)
**
** This function will attempt to write the TestCase Info to ALM log file
****************************************************************/
void ALM_LogTestCaseInfo(TCHAR *testID, TCHAR *ALM_TestCase_Description, int nStartTest, int nEndTest)
{
	int i=0;
	TCHAR ALM_buff[1024];

	/* Note: the char string pointer ALM_TestCase_Description is coming 
	with a "\n" that we need to remove it to avoid output extra line. */
    int original_len = wcslen(ALM_TestCase_Description)+1;
    TCHAR *Description_string = (TCHAR *)malloc(original_len * sizeof(TCHAR));
    memset(Description_string,0,original_len);
    wcsncpy(Description_string,ALM_TestCase_Description,original_len);

    for(i=0; i<original_len; i++)
    {
        if(Description_string[i] == '\n')
        {
            // Move all the char following the char "c" by one to the left.
            wcsncpy(&Description_string[i],&Description_string[i+1],original_len-i);
        }
    }

	/* Log into ALM report as well */
	swprintf(ALM_buff, 1024, _T("odbc|%s+%s+%s+%s|%s|%s - (case# %d - %d)|\n"), 
		_T("rowsets"), _T("UNICODE"), _T("ASCII"), machine, testID, Description_string, nStartTest, nEndTest);
	RecordTo_ALM_Log(ALM_buff);
	free( Description_string );

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
	TCHAR	ALM_buff[1024];
	TCHAR	ALM_Datebuf[11];  /* yyyy-mm-dd */
	TCHAR	ALM_Test_startTime[11],  ALM_Test_endTime[11]; /* hh:mm:ss */

	wcsftime( ALM_Datebuf, 11, _T("%Y-%m-%d"), localtime( &tStart ) );
	wcsftime( ALM_Test_startTime, 11, _T("%H:%M:%S"), localtime( &tStart ) );
	wcsftime( ALM_Test_endTime, 11, _T("%H:%M:%S"), localtime( &tEnd ) );

	if (result==PASSED)
	{
		swprintf(ALM_buff, 1024, _T("PASS|%s|%s|%s|%.0f|\n"), 
			ALM_Datebuf, ALM_Test_startTime, ALM_Test_endTime, difftime(tEnd, tStart));
	}
	else
	{
		swprintf(ALM_buff, 1024, _T("FAIL|%s|%s|%s|%.0f|\n"), 
			ALM_Datebuf, ALM_Test_startTime, ALM_Test_endTime, difftime(tEnd, tStart));
	}

	RecordTo_ALM_Log(ALM_buff);
}


