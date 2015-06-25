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

// Standard
UStr* ExecSQLStr[ 16 ];
// MVS
UStr* ExecSQLStrMVS[ 7 ];
// Index
UStr* ExecSQLStrIndex[ 2 ];
// RI
UStr* ExecSQLStrRI[ 4 ];
// Volatile
UStr* ExecSQLStrVolatile[ 2 ];
// Before Trigger
UStr* ExecSQLStrBeforeTrigger[2];
// After Trigger
UStr* ExecSQLStrAfterTrigger[5];

UStr* sqlDrvInsert;
UStr* Digit_2_Charset[11];
UStr* Digit_2_Ascii[11];

UNICHAR ignoreState[ NUMBER_OF_IGNORES ][ 10*4 ];
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

char *charset_filenames[] = {"charset_auto_generated_ascii.char",
							 "charset_auto_generated_sjis.char",
							 "charset_auto_generated_big5.char",
							 "charset_auto_generated_gb2.char",
							 "charset_auto_generated_gb1.char",
							 "charset_auto_generated_ksc.char",
							 "charset_auto_generated_eucjp.char",
							 "charset_auto_generated_latin1.char",
/* SQ new */					 "charset_auto_generated_gbk.char"
						 };
char	charset_file[256];

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

	//Initialize default values
	charset = (char*)"ASCII";
	strcpy(charset_file,charset_filenames[0]);
	uid = (char*)"odbcqa";
	password = (char*)"odbcqa";

    optarg = NULL;
    if ( argc < 9 || argc > 11)
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
				if (_stricmp(optarg,"debug") == 0) debug = true;
				else errflag++;
                break;
			case 'c':
				charset = optarg;
/* SEAQUSET */			strcpy (inputLocale, charset);
				if (!_stricmp(charset,"ASCII")) {
					strcpy(charset_file,charset_filenames[0]);
				}
				else if (!_stricmp(charset,"SJIS")) {
					strcpy(charset_file,charset_filenames[1]);
				}
				else if (!_stricmp(charset,"BIG5")) {
					strcpy(charset_file,charset_filenames[2]);
				}
				else if (!_stricmp(charset,"GB2")) {
					strcpy(charset_file,charset_filenames[3]);
				}
				else if (!_stricmp(charset,"GB1")) {
					strcpy(charset_file,charset_filenames[4]);
				}
				else if (!_stricmp(charset,"KSC")) {
					strcpy(charset_file,charset_filenames[5]);
				}
				else if (!_stricmp(charset,"EUCJP")) {
					strcpy(charset_file,charset_filenames[6]);
				}
				else if (!_stricmp(charset,"LATIN1")) {
					strcpy(charset_file,charset_filenames[7]);
				}
/* SQ new */
                                else if (!_stricmp(charset,"GBK")) {
                                      	strcpy(charset_file,charset_filenames[8]);
                                }
/* end of SQ new*/

				else {
					errflag++;
				}
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

	if ( errflag ) 
    {
        RecordToLog( "Command line error.\n" );
        RecordToLog( "Usage: %s -d <datasource> -u <userid> -p <password> -c <ASCII|SJIS|BIG5|GB1|GB2|KSC|EJCJP|LATIN1> [-o <debug>]\n", argv[0] );
        RecordToLog( "-d: data source\n" );
        RecordToLog( "-u: user identification\n" );
        RecordToLog( "-p: user password\n" );
        RecordToLog( "-c: character set\n" );
        RecordToLog( "-o: turn debug mode 'ON' (optional)\n" );
        //RecordToLog( "-t: test id to run (optional)\n" );
        //RecordToLog( "-r: resume test id to start from (optional)\n" );
        return 0;
    }

	time_t my_clock;
	my_clock = time( NULL);
    strftime( logfilename, 256, "rowsets_%Y-%m-%d_%H.%M.%S.", localtime( &my_clock ) );
#ifdef UNICODE
	strcat(logfilename, "UNICODE.");
#else
	strcat(logfilename, "ANSI.");
#endif
	strcat(logfilename, charset);
	strcat(logfilename, ".");
	strcat(logfilename, datasource);
	strcat(logfilename, ".");
	strcat( logfilename, machine);
	strcat(logfilename, ".log");


	// start for ALM log
    strftime( ALM_log_file_buff, 256, "rowsets_%Y-%m-%d_%H.%M.%S.", localtime( &my_clock ) );
#ifdef UNICODE
	strcat(ALM_log_file_buff, "UNICODE.");
#else
	strcat(ALM_log_file_buff, "ANSI.");
#endif
	strcat(ALM_log_file_buff, charset);
	strcat( ALM_log_file_buff, ".");
	strcat( ALM_log_file_buff, datasource);
	strcat( ALM_log_file_buff, ".");
	strcat( ALM_log_file_buff, machine);
	strcat( ALM_log_file_buff, "_ALM.log");
	// end for ALM log 

	// Initializing ICUConverter objects
	icu_conv = new ICUConverter;

	icu_conv->err = U_ZERO_ERROR;

	icu_conv->locale = ucnv_open(inputLocale, &icu_conv->err);
	icu_conv->utf8 = ucnv_open("utf8", &icu_conv->err);

	ucnv_setFallback(icu_conv->locale, TRUE);
	ucnv_setFallback(icu_conv->utf8, TRUE);

/* SQ    icu_ConTo(sqlDrvInsert->ustr,"PLANLOADTABLE ROWSET_TABLE"); */

	printf("Charset script file is loaded from: %s\n", charset_file);

	setlocale(LC_ALL, "");
	//===========================================================================================================
	//Load charset data
	var_list_t *var_list;
	var_list = load_api_vars("Rowsets", charset_file);
	if (var_list == NULL) return 0;
	//print_list(var_list);

	InitializeUStr(&ExecSQLStr[0], USTR_SELF_INIT, var_mapping("ExecSQLStr0", var_list));
	InitializeUStr(&ExecSQLStr[1], USTR_SELF_INIT, var_mapping("ExecSQLStr1", var_list));
	InitializeUStr(&ExecSQLStr[2], USTR_SELF_INIT, var_mapping("ExecSQLStr2", var_list));
	InitializeUStr(&ExecSQLStr[3], USTR_SELF_INIT, var_mapping("ExecSQLStr3", var_list));
	InitializeUStr(&ExecSQLStr[4], USTR_SELF_INIT, var_mapping("ExecSQLStr4", var_list));
	InitializeUStr(&ExecSQLStr[5], USTR_SELF_INIT, var_mapping("ExecSQLStr5", var_list));
	InitializeUStr(&ExecSQLStr[6], USTR_SELF_INIT, var_mapping("ExecSQLStr6", var_list));
	InitializeUStr(&ExecSQLStr[7], USTR_SELF_INIT, var_mapping("ExecSQLStr7", var_list));
	InitializeUStr(&ExecSQLStr[8], USTR_SELF_INIT, var_mapping("ExecSQLStr8", var_list));
	InitializeUStr(&ExecSQLStr[9], USTR_SELF_INIT, var_mapping("ExecSQLStr9", var_list));
	InitializeUStr(&ExecSQLStr[10], USTR_SELF_INIT, var_mapping("ExecSQLStr10", var_list));
	InitializeUStr(&ExecSQLStr[11], USTR_SELF_INIT, var_mapping("ExecSQLStr11", var_list));
	InitializeUStr(&ExecSQLStr[12], USTR_SELF_INIT, var_mapping("ExecSQLStr12", var_list));
	InitializeUStr(&ExecSQLStr[13], USTR_SELF_INIT, var_mapping("ExecSQLStr13", var_list));
	InitializeUStr(&ExecSQLStr[14], USTR_SELF_INIT, var_mapping("ExecSQLStr14", var_list));
	InitializeUStr(&ExecSQLStr[15], USTR_SELF_INIT, var_mapping("ExecSQLStr15", var_list));

	InitializeUStr(&ExecSQLStrIndex[0], USTR_SELF_INIT, var_mapping("ExecSQLStrIndex0", var_list));
	InitializeUStr(&ExecSQLStrIndex[1], USTR_SELF_INIT, var_mapping("ExecSQLStrIndex1", var_list));

	InitializeUStr(&ExecSQLStrRI[0], USTR_SELF_INIT, var_mapping("ExecSQLStrRI0", var_list));
	InitializeUStr(&ExecSQLStrRI[1], USTR_SELF_INIT, var_mapping("ExecSQLStrRI1", var_list));
	InitializeUStr(&ExecSQLStrRI[2], USTR_SELF_INIT, var_mapping("ExecSQLStrRI2", var_list));
	InitializeUStr(&ExecSQLStrRI[3], USTR_SELF_INIT, var_mapping("ExecSQLStrRI3", var_list));

	InitializeUStr(&ExecSQLStrVolatile[0], USTR_SELF_INIT, var_mapping("ExecSQLStrVolatile0", var_list));
	InitializeUStr(&ExecSQLStrVolatile[1], USTR_SELF_INIT, var_mapping("ExecSQLStrVolatile1", var_list));

	InitializeUStr(&ExecSQLStrMVS[0], USTR_SELF_INIT, var_mapping("ExecSQLStrMVS0", var_list));
	InitializeUStr(&ExecSQLStrMVS[1], USTR_SELF_INIT, var_mapping("ExecSQLStrMVS1", var_list));
	InitializeUStr(&ExecSQLStrMVS[2], USTR_SELF_INIT, var_mapping("ExecSQLStrMVS2", var_list));
	InitializeUStr(&ExecSQLStrMVS[3], USTR_SELF_INIT, var_mapping("ExecSQLStrMVS3", var_list));
	InitializeUStr(&ExecSQLStrMVS[4], USTR_SELF_INIT, var_mapping("ExecSQLStrMVS4", var_list));
	InitializeUStr(&ExecSQLStrMVS[5], USTR_SELF_INIT, var_mapping("ExecSQLStrMVS5", var_list));
	InitializeUStr(&ExecSQLStrMVS[6], USTR_SELF_INIT, var_mapping("ExecSQLStrMVS6", var_list));

	InitializeUStr(&ExecSQLStrBeforeTrigger[0], USTR_SELF_INIT, var_mapping("ExecSQLStrBeforeTrigger0", var_list));
	InitializeUStr(&ExecSQLStrBeforeTrigger[1], USTR_SELF_INIT, var_mapping("ExecSQLStrBeforeTrigger1", var_list));

	InitializeUStr(&ExecSQLStrAfterTrigger[0], USTR_SELF_INIT, var_mapping("ExecSQLStrAfterTrigger0", var_list));
	InitializeUStr(&ExecSQLStrAfterTrigger[1], USTR_SELF_INIT, var_mapping("ExecSQLStrAfterTrigger1", var_list));
	InitializeUStr(&ExecSQLStrAfterTrigger[2], USTR_SELF_INIT, var_mapping("ExecSQLStrAfterTrigger2", var_list));
	InitializeUStr(&ExecSQLStrAfterTrigger[3], USTR_SELF_INIT, var_mapping("ExecSQLStrAfterTrigger3", var_list));
	InitializeUStr(&ExecSQLStrAfterTrigger[4], USTR_SELF_INIT, var_mapping("ExecSQLStrAfterTrigger4", var_list));

	InitializeUStr(&Digit_2_Charset[0], USTR_SELF_INIT, var_mapping("Digit_2_Charset0", var_list));
	InitializeUStr(&Digit_2_Charset[1], USTR_SELF_INIT, var_mapping("Digit_2_Charset1", var_list));
	InitializeUStr(&Digit_2_Charset[2], USTR_SELF_INIT, var_mapping("Digit_2_Charset2", var_list));
	InitializeUStr(&Digit_2_Charset[3], USTR_SELF_INIT, var_mapping("Digit_2_Charset3", var_list));
	InitializeUStr(&Digit_2_Charset[4], USTR_SELF_INIT, var_mapping("Digit_2_Charset4", var_list));
	InitializeUStr(&Digit_2_Charset[5], USTR_SELF_INIT, var_mapping("Digit_2_Charset5", var_list));
	InitializeUStr(&Digit_2_Charset[6], USTR_SELF_INIT, var_mapping("Digit_2_Charset6", var_list));
	InitializeUStr(&Digit_2_Charset[7], USTR_SELF_INIT, var_mapping("Digit_2_Charset7", var_list));
	InitializeUStr(&Digit_2_Charset[8], USTR_SELF_INIT, var_mapping("Digit_2_Charset8", var_list));
	InitializeUStr(&Digit_2_Charset[9], USTR_SELF_INIT, var_mapping("Digit_2_Charset9", var_list));
	InitializeUStr(&Digit_2_Charset[10], USTR_SELF_INIT, var_mapping("Digit_2_Charset10", var_list));

	InitializeUStr(&Digit_2_Ascii[0], USTR_SELF_INIT, var_mapping("Digit_2_Ascii0", var_list));
	InitializeUStr(&Digit_2_Ascii[1], USTR_SELF_INIT, var_mapping("Digit_2_Ascii1", var_list));
	InitializeUStr(&Digit_2_Ascii[2], USTR_SELF_INIT, var_mapping("Digit_2_Ascii2", var_list));
	InitializeUStr(&Digit_2_Ascii[3], USTR_SELF_INIT, var_mapping("Digit_2_Ascii3", var_list));
	InitializeUStr(&Digit_2_Ascii[4], USTR_SELF_INIT, var_mapping("Digit_2_Ascii4", var_list));
	InitializeUStr(&Digit_2_Ascii[5], USTR_SELF_INIT, var_mapping("Digit_2_Ascii5", var_list));
	InitializeUStr(&Digit_2_Ascii[6], USTR_SELF_INIT, var_mapping("Digit_2_Ascii6", var_list));
	InitializeUStr(&Digit_2_Ascii[7], USTR_SELF_INIT, var_mapping("Digit_2_Ascii7", var_list));
	InitializeUStr(&Digit_2_Ascii[8], USTR_SELF_INIT, var_mapping("Digit_2_Ascii8", var_list));
	InitializeUStr(&Digit_2_Ascii[9], USTR_SELF_INIT, var_mapping("Digit_2_Ascii9", var_list));
	InitializeUStr(&Digit_2_Ascii[10], USTR_SELF_INIT, var_mapping("Digit_2_Ascii10", var_list));

	String_OverFlow = var_mapping("String_OverFlow", var_list);

	InitializeUStr(&sqlDrvInsert, 128, "PLANLOADTABLE ROWSET_TABLE");
	//===========================================================================================================

    RecordToLog( " > Initializing ODBC handles and connection.\n" );
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

			if( debug )
				PrintTestInformation( );

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

		DropTable();

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
        retcode = SQLSetConnectAttrW( handle[ SQL_HANDLE_DBC ], SQL_MODE_LOADER, (void *)mode, 0);
        if( retcode != SQL_SUCCESS )    
        {
            CheckMsgs( "SQLSetConnectAttrW()", __LINE__ );
            DeleteHandles( );
            return false;
        }

        RecordToLog( " >> Setting up SQL_START_NODE.\n" );
        SQLUINTEGER startnode = 5;
        SQLUINTEGER SQL_START_NODE = 4000;
        retcode = SQLSetConnectAttrW( handle[ SQL_HANDLE_DBC ], SQL_START_NODE, (void *) startnode, 0);
        if( retcode != SQL_SUCCESS )    
        {
            CheckMsgs( "SQLSetConnectAttrW()", __LINE__ );
            DeleteHandles( );
            return false;
        }

        RecordToLog( " >> Setting up SQL_STREAMS_PER_SEG.\n" );
        SQLUINTEGER streams_per_node = 1;
        SQLUINTEGER SQL_STREAMS_PER_SEG = 4002;
        retcode = SQLSetConnectAttrW( handle[ SQL_HANDLE_DBC ], SQL_STREAMS_PER_SEG, (void *) streams_per_node, 0 );
        if( retcode != SQL_SUCCESS )    
        {
            CheckMsgs( "SQLSetConnectAttrW()", __LINE__ );
            DeleteHandles( );
            return false;
        }

    }

    // Connect to the ODBC service.
    retcode = SQLConnectW( handle[ SQL_HANDLE_DBC ], (SQLTCHAR*) datasource, SQL_NTS,
                          (SQLTCHAR*) uid, SQL_NTS, (SQLTCHAR*) password, SQL_NTS );
    if( retcode != SQL_SUCCESS && retcode != SQL_SUCCESS_WITH_INFO )    
    {
        CheckMsgs( "SQLConnectW()", __LINE__ );
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
        retcode = SQLSetConnectAttrW( handle[ SQL_HANDLE_DBC ], SQL_ATTR_AUTOCOMMIT, (SQLPOINTER)SQL_AUTOCOMMIT_OFF, 0 );
        if( retcode != SQL_SUCCESS )    
        {
            CheckMsgs( "SQLSetConnectAttrW()", __LINE__ );
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
    if( CheckForCQD( "MODE_SPECIAL_1", "ON" ) == 0 )
    {
        errorChecking = MODE_SPECIAL_1;
    }
    else
    {
        errorChecking = STANDARD;
    }

	RecordToLog( " >> Creating the schema.\n" );
	CreateSchema();

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
            while( ( retcode = SQLExecDirectW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStr[ 13 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING );
            if( retcode != SQL_SUCCESS )    
            {
                CheckMsgs( "SQLExecDirectW()", __LINE__ );
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
            while( ( retcode = SQLExecDirectW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStr[ 8 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING ); // Create the table.
            break;
        case SURROGATE:
            RecordToLog( " >> Creating surrogate key table. \n" );
            while( ( retcode = SQLExecDirectW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStr[ 9 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING ); // Create the table.
            break;
        case VOLATILE:
            RecordToLog( " >> Creating volatile table. \n" );
            while( ( retcode = SQLExecDirectW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrVolatile[ 0 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING );
            break;
        case SET:
            RecordToLog( " >> Creating set table. \n" );
            while( ( retcode = SQLExecDirectW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStr[ 11 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING );
            break;
        case MULTISET:
            RecordToLog( " >> Creating multiset table. \n" );
            while( ( retcode = SQLExecDirectW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStr[ 12 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING );
            break;
        case REGULAR:
        default:
            if( features[ unitTest.feature ] == HASH2 )
            {
                RecordToLog( " >> Creating HASH2 table. \n" );
                while( ( retcode = SQLExecDirectW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStr[ 9 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING ); // Create the table.
            }
            else
            {
                RecordToLog( " >> Creating standard table. \n" );
                while( ( retcode = SQLExecDirectW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStr[ 1 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING ); // Create the table.
            }
            break;
    }

    switch( tableFeatures[ unitTest.tableFeature ] )
    {
        case INDEX:
            RecordToLog( " >> Creating index. \n" );
            while( ( retcode = SQLExecDirectW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrIndex[ 0 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING );
            break;
        case MVS:
            RecordToLog( " >> MVS setup on standard table. \n" );
            RecordToLog( "   >> Allowing MVS on standard table. \n" );
            while( ( retcode = SQLExecDirectW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrMVS[ 0 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING );
            if( retcode != SQL_SUCCESS )    
            {
                CheckMsgs( "SQLExecDirectW()", __LINE__ );
                return false;
            }
            RecordToLog( "   >> Creating an alternative table. \n" );
            while( ( retcode = SQLExecDirectW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrMVS[ 1 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING );
            if( retcode != SQL_SUCCESS )    
            {
                CheckMsgs( "SQLExecDirectW()", __LINE__ );
                return false;
            }
            RecordToLog( "   >> Creating a view on standard and alternative table. \n" );
            while( ( retcode = SQLExecDirectW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrMVS[ 2 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING );
            if( retcode != SQL_SUCCESS )    
            {
                CheckMsgs( "SQLExecDirectW()", __LINE__ );
                return false;
            }
            RecordToLog( "   >> Creating MVS on standard and alternative table. \n" );
            while( ( retcode = SQLExecDirectW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrMVS[ 3 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING );
            if( retcode != SQL_SUCCESS )    
            {
                CheckMsgs( "SQLExecDirectW()", __LINE__ );
                return false;
            }
            break;
        case RI:
            RecordToLog( " >> Initializing CQD. \n" );
            while( ( retcode = SQLExecDirectW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrRI[ 0 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING );
            if( retcode != SQL_SUCCESS )    
            {
                CheckMsgs( "SQLExecDirectW()", __LINE__ );
                return false;
            }
            RecordToLog( " >> Creating LIKE table. \n" );
            while( ( retcode = SQLExecDirectW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrRI[ 1 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING );
            if( retcode != SQL_SUCCESS )    
            {
                CheckMsgs( "SQLExecDirectW()", __LINE__ );
                return false;
            }
            RecordToLog( " >> Creating referential constraint. \n" );
            while ( ( retcode = SQLExecDirectW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrRI[ 2 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING );
            break;
        case BEFORETRIGGER:
            RecordToLog( " >> Before trigger setup on standard table. \n" );
            while( ( retcode = SQLExecDirectW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrBeforeTrigger[ 1 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING );
            if( retcode != SQL_SUCCESS )    
            {
                CheckMsgs( "SQLExecDirectW()", __LINE__ );
                return false;
            }
            break;
        case AFTERTRIGGER:
            RecordToLog( " >> After trigger tmp table. \n" );
            while( ( retcode = SQLExecDirectW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrAfterTrigger[ 3 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING );
            if( retcode != SQL_SUCCESS )    
            {
                CheckMsgs( "SQLExecDirectW()", __LINE__ );
                return false;
            }
            RecordToLog( " >> After trigger setup on standard table.\n" );
            while( ( retcode = SQLExecDirectW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrAfterTrigger[ 2 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING );
            if( retcode != SQL_SUCCESS )    
            {
                CheckMsgs( "SQLExecDirectW()", __LINE__ );
                return false;
            }
            break;
        default:
            break;
    }

	if( ( retcode != SQL_SUCCESS ) && ( retcode != SQL_SUCCESS_WITH_INFO ) && ( !singleTest ) )    
    {
        CheckMsgs( "SQLExecDirectW()", __LINE__ );
        DeleteHandles( );
        return false;
    }

    if( features[ unitTest.feature ] != HASH2 && 
        retcode == SQL_SUCCESS )
    {
        RecordToLog( " >> Committing transaction.\n" );
        retcode = SQLEndTran( SQL_HANDLE_DBC, handle[ SQL_HANDLE_DBC ], SQL_COMMIT ); // Commit the transaction.
        if( retcode != SQL_SUCCESS )    
        {
            CheckMsgs( "SQLEndTran()", __LINE__ );
            DeleteHandles( );
            return false;
        }
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
void IgnoreMsg( UNICHAR *state, SDWORD nativeError )
{
    // We only store a limited number of error messages to ignore. 
    if( ignoreCount == NUMBER_OF_IGNORES )
        return;

    // Store off the information.
    icu_strcpy( ignoreState[ ignoreCount ], state );
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
bool ShouldIgnoreMsg( UNICHAR *state, SDWORD nativeError )
{
    for( int loop = 0; loop != ignoreCount; loop++ )
    {
        if( ( icu_strcmp( ignoreState[ loop ], state ) == 0 ) &&
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
    SQLRETURN   retcode;       // Used to gather the return value of all ODBC API calls.
    UNICHAR     szSqlState[ 10*4 ];
    SDWORD      NativeError;
    UNICHAR     szErrorMsg[ 1024*4 ];
    UNICHAR     SavedErrorMsg[ 1024*4 ];
    int         errorRepetionCount = 0;
    SWORD       ErrorMsg;
    SQLSMALLINT recordNumber = -1;
    int         reportedErrorMsg = NO_ERROR_FND;

    icu_ConTo( SavedErrorMsg, "EMPTY" );

    // Loop through all the handles passed in
    for( int loop = 0; loop < 5; loop++ )
    {
        // Loop through all the possible handle types the handle can be
        for( SQLSMALLINT handleType = 1; handleType != 5; handleType++ )
        {
            if( handle[ loop ] != (SQLHANDLE)NULL ) 
            {
                while( ( retcode = SQLGetDiagRec( handleType, handle[ loop ], 
                                                  recordNumber, (SQLTCHAR*)szSqlState, &NativeError, 
                                                  (SQLTCHAR*)szErrorMsg, 1024*4, &ErrorMsg ) ) == SQL_STILL_EXECUTING );
                while( ( retcode == SQL_SUCCESS ) || ( retcode == SQL_SUCCESS_WITH_INFO ) ) 
                {
                    // We do not log ignored messages, unless we have already 
                    // reported an error message. 
                    if( ( !ShouldIgnoreMsg( szSqlState, NativeError ) ) || 
                        ( reportedErrorMsg == ERROR_REPORT ) )
                    {
                        if( reportedErrorMsg == NO_ERROR_FND )
                        {
                            RecordToLog( " >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n" );
                        }
                        if( icu_strcmp( szErrorMsg, SavedErrorMsg ) != 0 )
                        {
                            RecordToLog( " >>> State: %s\n",        szSqlState );
                            RecordToLog( " >>> Native Error: %d\n", NativeError );
                            RecordToLog( " >>> Message: %s\n",      szErrorMsg );
                            icu_strcpy( SavedErrorMsg, szErrorMsg );
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
                                                      recordNumber, (SQLTCHAR*)szSqlState, &NativeError, 
                                                      (SQLTCHAR*)szErrorMsg, 1024*4, &ErrorMsg ) ) == SQL_STILL_EXECUTING );
                    if( errorRepetionCount > 0 )
                    {
                        if( retcode != SQL_SUCCESS )
                            RecordToLog( " >>> (The above error message was repeated %d times.)\n", errorRepetionCount );
                        else if( icu_strcmp( szErrorMsg, SavedErrorMsg ) != 0 )
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
        RecordToLog( " >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n" );
        RecordToLog( " >>> WARNING NO MESSAGES RETRIEVED FROM ODBC DRIVER\n" );
        RecordToLog( " >>> This was from  %s located at %s on line %d\n", sqlFunction, __FILE__, lineNumber );
        RecordToLog( " >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n" );
        //exit(1);
    }

	ErrornousExit(szSqlState, NativeError);

    return reportedErrorMsg;
}

void CheckMsgsNoIgnored() 
{
    SQLRETURN  retcode;
    UNICHAR szSqlState[ 10*4 ];
    SDWORD NativeError;
    UNICHAR szErrorMsg[ 1024*4 ];
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
                                                  recordNumber, (SQLTCHAR*)szSqlState, &NativeError, 
                                                  (SQLTCHAR*)szErrorMsg, 1024*4, &ErrorMsg ) ) == SQL_STILL_EXECUTING );
                while( ( retcode == SQL_SUCCESS ) || ( retcode == SQL_SUCCESS_WITH_INFO ) ) 
                {
                    szErrorMsg[ 500 ] = '\0';
                    RecordToLog( " >>> State: %s\n",        szSqlState );
                    RecordToLog( " >>> Native Error: %d\n", (int)NativeError );
                    RecordToLog( " >>> Message: %s\n",      szErrorMsg );

                    recordNumber++;
					while( ( retcode = SQLGetDiagRec( handleType, handle[ loop ], 
                                                      recordNumber, (SQLTCHAR*)szSqlState, &NativeError, 
                                                      (SQLTCHAR*)szErrorMsg, 1024*4, &ErrorMsg ) ) == SQL_STILL_EXECUTING );
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
    while( ( retcode = SQLExecDirectW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStr[ 4 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING );//Delete all rows in table

    if( retcode != SQL_SUCCESS )    
    {
        ClearIgnore( );
        DeleteHandles( );
        return false;
    }

	if (tableFeatures[unitTest.tableFeature] == AFTERTRIGGER) {
        RecordToLog( " >> Clean up temp trigger table.\n" );
	    while( ( retcode = SQLExecDirectW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrAfterTrigger[ 4 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING );//Delete all rows in temp trigger table
        if( retcode != SQL_SUCCESS )    
        {
            CheckMsgs( "SQLExecDirectW()", __LINE__ );
            ClearIgnore( );
            DeleteHandles( );
            return false;
        }
	}

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
    UNICHAR temp[128];
    SQLRETURN  retcode;       // Used to gather the return value of all ODBC API calls.

    if( singleTest )
    {
        return true;
    }

    retcode = SQL_SUCCESS;

    IgnoreMsg( icu_ConTo(temp,"01000"), 0 ); // Ignore the warning message connect to default DataSource.
    IgnoreMsg( icu_ConTo(temp,"X0104"), -1004 ); // Ignore the table does not exist.
    IgnoreMsg( icu_ConTo(temp,"X010V"), -1031 ); // Ignore the table can not be dropped.
    IgnoreMsg( icu_ConTo(temp,"X0106"), -1006 ); // Ignore the index does not exist.

    if( actions[ unitTest.action ] == INSERT_SELECT )
    {
        RecordToLog( " >> Droping select table. \n" );
        while( ( retcode = SQLExecDirectW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStr[ 15 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING ); 
        return true;
    }

    switch( tableFeatures[ unitTest.tableFeature ] )
    {
        case INDEX:
            RecordToLog( " >> Droping index. \n" );
            while( ( retcode = SQLExecDirectW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrIndex[ 1 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING ); 
            break;
        case MVS:
            RecordToLog( " >> Droping MVS table. \n" );
            while( ( retcode = SQLExecDirectW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrMVS[ 4 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING );
            while( ( retcode = SQLExecDirectW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrMVS[ 5 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING );
            while( ( retcode = SQLExecDirectW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrMVS[ 6 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING );
            break;
        case RI:
            RecordToLog( " >> Droping referential constraint. \n" );
            while( ( retcode = SQLExecDirectW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrRI[ 3 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING ); 
            if( retcode != SQL_SUCCESS )    
            {
                CheckMsgs( "SQLExecDirectW()", __LINE__ );
                ClearIgnore( );
                DeleteHandles( );
                return false;
            }
            break;
        case BEFORETRIGGER:
            RecordToLog( " >> Droping before trigger. \n" );
            while( ( retcode = SQLExecDirectW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrBeforeTrigger[ 0 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING );
            break;
        case AFTERTRIGGER:
             RecordToLog( " >> Droping after trigger. \n" );
            while( ( retcode = SQLExecDirectW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrAfterTrigger[ 1 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING );
            while( ( retcode = SQLExecDirectW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrAfterTrigger[ 0 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING );
            break;
        default:
            break;
    }

    switch( tableTypes[ unitTest.tableType ] )
    {
		case VOLATILE:
            RecordToLog( " >> Droping standard table. \n" );
            while( ( retcode = SQLExecDirectW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStr[ 0 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING ); // Create the table.
            RecordToLog( " >> Droping volatile table. \n" );
			while( ( retcode = SQLExecDirectW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStrVolatile[ 1 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING ); // Create the table.
            break;
        default:
            RecordToLog( " >> Droping standard table. \n" );
            while( ( retcode = SQLExecDirectW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStr[ 0 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING ); // Create the table.
            break;
    }

    if( retcode != SQL_SUCCESS && retcode != SQL_SUCCESS_WITH_INFO )    
    {
        if( CheckMsgs( "SQLExecDirectW()", __LINE__ ) != IGNORE_ERROR )
        {
            ClearIgnore( );
            DeleteHandles( );
            return false;
        }
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
void ALM_TestInformation(char* sALM_TestInfo)
{
	strcpy((char *)sALM_TestInfo,"");
	switch( tableTypes[ unitTest.tableType ] )
	{
		case REGULAR:
			strcat((char *)sALM_TestInfo, "tableType:REGULAR");
			break;
		case POSOFF:
			strcat((char *)sALM_TestInfo, "tableType:POSOFF");
			break;
		case VOLATILE:
			strcat((char *)sALM_TestInfo, "tableType:VOLATILE");
			break;
		case SURROGATE:
			strcat((char *)sALM_TestInfo, "tableType:SURROGATE");
			break;
		case SET:
			strcat((char *)sALM_TestInfo, "tableType:SET");
			break;
		case MULTISET:
			strcat((char *)sALM_TestInfo, "tableType:MULTISET");
			break;
		default:
			strcat((char *)sALM_TestInfo, "tableType:_UNKNOWN_");
			break;
	}
	
	strcat((char *)sALM_TestInfo, "+");
    switch( tableFeatures[ unitTest.tableFeature ] )
    {
        case STANDARD:
			strcat((char *)sALM_TestInfo, "tableFeature:STANDARD");
            break;
        case INDEX:
			strcat((char *)sALM_TestInfo, "tableFeature:INDEX");
            break;
        case MVS:
			strcat((char *)sALM_TestInfo, "tableFeature:MVS");
            break;
        case RI:
			strcat((char *)sALM_TestInfo, "tableFeature:RI");
            break;
        case BEFORETRIGGER:
			strcat((char *)sALM_TestInfo, "tableFeature:BEFORETRIGGER");
            break;
        case AFTERTRIGGER:
			strcat((char *)sALM_TestInfo, "tableFeature:AFTERTRIGGER");
            break;
        default:
			strcat((char *)sALM_TestInfo, "tableFeature:_UNKNOWN_");
            break;
    }

	strcat((char *)sALM_TestInfo, "+");
    switch( modes[ unitTest.mode ] )
    {
        case STANDARD:
			strcat((char *)sALM_TestInfo, "mode:STANDARD");
            break;
        default:
			strcat((char *)sALM_TestInfo, "mode:_UNKNOWN_");
            break;
    }

    if( errorChecking == MODE_SPECIAL_1 )
    {
		strcat((char *)sALM_TestInfo, "+CQD:MODE_SPECIAL_1");
    }

	strcat((char *)sALM_TestInfo, "+");
    switch( features[ unitTest.feature ] )
    {
        case STANDARD:
			strcat((char *)sALM_TestInfo, "feature:STANDARD");
            break;
        case HASH2:
			strcat((char *)sALM_TestInfo, "feature:HASH2");
            break;
        case ASYNC:
			strcat((char *)sALM_TestInfo, "feature:ASYNC");
            break;
        default:
			strcat((char *)sALM_TestInfo, "feature:_UNKNOWN_");
            break;
    }

	strcat((char *)sALM_TestInfo, "+");
    switch( operations[ unitTest.operation ] )
    {
        case PREPARE_EXECUTE:
			strcat((char *)sALM_TestInfo, "operation:PREPARE_EXECUTE");
            break;
        case EXECUTE_DIRECT:
			strcat((char *)sALM_TestInfo, "operation:EXECUTE_DIRECT");
            break;
        default:
			strcat((char *)sALM_TestInfo, "operation:_UNKNOWN_");
            break;
    }

/*
	strcat((char *)sALM_TestInfo, "+");
    switch( actions[ unitTest.action ] )
    {
        case INSERT:
			strcat((char *)sALM_TestInfo,"action:INSERT");
            break;
        case SELECT:
			strcat((char *)sALM_TestInfo,"action:SELECT");
            break;
        case UPDATE:
			strcat((char *)sALM_TestInfo,"action:UPDATE");
            break;
        case DELETE_PARAM:
			strcat((char *)sALM_TestInfo,"action:DELETE");
            break;
        case INSERT_BULK:
			strcat((char *)sALM_TestInfo,"action:INSERT_BULK");
            break;
        case INSERT_SELECT:
			strcat((char *)sALM_TestInfo,"action:INSERT_SELECT");
            break;
        default:
			strcat((char *)sALM_TestInfo,"action:_UNKNOWN_");
            break;
    }
*/

	strcat((char *)sALM_TestInfo, "+");
    switch( bindOrientations[ unitTest.bindOrientation ] )
    {
        case ROW:
			strcat((char *)sALM_TestInfo, "bindOrientation:ROW");
            break;
        case COLUMN:
			strcat((char *)sALM_TestInfo, "bindOrientation:COLUMN");
            break;
        case SINGLE:
			strcat((char *)sALM_TestInfo, "bindOrientation:SINGLE");
            break;
        default:
			strcat((char *)sALM_TestInfo, "bindOrientation:_UNKNOWN_");
            break;
    }
/*
	strcat((char *)sALM_TestInfo,"+");
    switch( injectionTypes[ unitTest.injectionType ] )
    {
        case NO_ERRORS:
			strcat((char *)sALM_TestInfo,"injectionType:NO_ERRORS");
            break;
        case DUPLICATEKEY:
			strcat((char *)sALM_TestInfo,"injectionType:DUPLICATEKEY");
            break;
        case UNIQUECONST:
			strcat((char *)sALM_TestInfo,"injectionType:UNIQUECONST");
            break;
        case SELECTIVE:
			strcat((char *)sALM_TestInfo,"injectionType:SELECTIVE");
            break;
        case NULLVALUE:
			strcat((char *)sALM_TestInfo,"injectionType:NULLVALUE");
            break;
        case DUPLICATEROW:
			strcat((char *)sALM_TestInfo,"injectionType:DUPLICATEROW");
			//if (operations[ unitTest.operation ] != PREPARE_EXECUTE)
			//	(*ALM_testCounter)--;
			//bTestCounted = false;
            break;
        case OVERFLOW:
			strcat((char *)sALM_TestInfo,"injectionType:OVERFLOW");
            break;
		case ERR_PER_ROW:
			strcat((char *)sALM_TestInfo,"injectionType:ERR_PER_ROW");
            break;
		case ERR_PER_COL:
			strcat((char *)sALM_TestInfo,"injectionType:ERR_PER_COL");
            break;
		case FULL_ERRORS:
			strcat((char *)sALM_TestInfo,"injectionType:FULL_ERRORS");
            break;
		case DRIVER_GOOD_BAD_MULCOL:
			strcat((char *)sALM_TestInfo,"injectionType:DRIVER_GOOD_BAD_MULCOL");
            break;
		case DRIVER_GOOD_WARNING_MULCOL:
			strcat((char *)sALM_TestInfo,"injectionType:DRIVER_GOOD_WARNING_MULCOL");
            break;
		case DRIVER_GOOD_BAD_WARNING_MULCOL:
			strcat((char *)sALM_TestInfo,"injectionType:DRIVER_GOOD_BAD_WARNING_MULCOL");
            break;
		case DRIVER_ALL_BAD_MULCOL:
			strcat((char *)sALM_TestInfo,"injectionType:DRIVER_ALL_BAD_MULCOL");
            break;
		case DRIVER_ALL_WARNING_MULCOL:
			strcat((char *)sALM_TestInfo,"injectionType:DRIVER_ALL_WARNING_MULCOL");
            break;
		case DRIVER_ALL_BAD_WARNING_MULCOL:
			strcat((char *)sALM_TestInfo,"injectionType:DRIVER_ALL_BAD_WARNING_MULCOL");
            break;
		case SERVER_GOOD_BAD_MULCOL:
			strcat((char *)sALM_TestInfo,"injectionType:SERVER_GOOD_BAD_MULCOL");
            break;
		case SERVER_ALL_BAD_MULCOL:
			strcat((char *)sALM_TestInfo,"injectionType:SERVER_ALL_BAD_MULCOL");
            break;
		case MIXED_DRIVERWARNING_SERVERBAD_GOOD_MULCOL:
			strcat((char *)sALM_TestInfo,"injectionType:MIXED_DRIVERWARNING_SERVERBAD_GOOD_MULCOL");
            break;
		case MIXED_DRIVERBAD_SERVERBAD_GOOD_MULCOL:
			strcat((char *)sALM_TestInfo,"injectionType:MIXED_DRIVERBAD_SERVERBAD_GOOD_MULCOL");
            break;
		case MIXED_DRIVERWARNING_DRIVERBAD_SERVERBAD_GOOD_MULCOL:
			strcat((char *)sALM_TestInfo,"injectionType:MIXED_DRIVERWARNING_DRIVERBAD_SERVERBAD_GOOD_MULCOL");
            break;
		case MIXED_DRIVERBAD_SERVERBAD_MULCOL:
			strcat((char *)sALM_TestInfo,"injectionType:MIXED_DRIVERBAD_SERVERBAD_MULCOL");
            break;
		case MIXED_DRIVERWARNING_DRIVERBAD_SERVERBAD_MULCOL:
			strcat((char *)sALM_TestInfo,"injectionType:MIXED_DRIVERWARNING_DRIVERBAD_SERVERBAD_MULCOL");
            break;
        default:
			strcat((char *)sALM_TestInfo,"injectionType:_UNKNOWN_");
            break;
    }

	strcat((char *)sALM_TestInfo,"+");
	sprintf(str, "numberOfRows=%d", numberOfRows[ unitTest.numberOfRows ]);
	strcat((char *)sALM_TestInfo,str);

	strcat((char *)sALM_TestInfo,"+");
	sprintf(str, "rowsetSize:%d", rowsetSizes[ unitTest.rowsetSize ]);
	strcat((char *)sALM_TestInfo,str);

	strcat((char *)sALM_TestInfo,"+");
	sprintf(str, "commitRate:%d", commitRates[ unitTest.commitRate ]);
	strcat((char *)sALM_TestInfo,str);
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
                    while( ( retcode = SQLPrepareW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR *) sqlDrvInsert->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING );
                }
                while( ( retcode = SQLPrepareW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStr[ 2 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING );
                break;
            case DELETE_PARAM:
                while( ( retcode = SQLPrepareW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStr[ 6 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING );
                break;
            case UPDATE:
				while( ( retcode = SQLPrepareW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStr[ 7 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING );
                break;
            case INSERT_SELECT:
                while( ( retcode = SQLPrepareW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStr[ 14 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING );
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
                CheckMsgs( "SQLPrepareW()", __LINE__ );
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

void AssignRow( int rowsetPos, int column1Value, int column2Value, int type )
{
    keyarray[ rowsetPos ] = column1Value;
    switch( bindOrientations[ unitTest.bindOrientation ] )
    {
        case ROW:
        case SINGLE:
			if( type == ROWSET_PRIMARY ) {
				icu_ConTo( rowset[ rowsetPos ].dt_char_utf8, Digit_2_Ascii[column1Value]->astr );
				icu_ConTo( rowset[ rowsetPos ].dt_char_ucs, Digit_2_Charset[column1Value]->astr );
				icu_ConTo( rowset[ rowsetPos ].dt_varchar_utf8, Digit_2_Ascii[column1Value]->astr );
				icu_ConTo( rowset[ rowsetPos ].dt_varchar_ucs, Digit_2_Charset[column1Value]->astr );
				icu_ConTo( rowset[ rowsetPos ].dt_longvarchar_utf8, Digit_2_Ascii[column1Value]->astr );
				icu_ConTo( rowset[ rowsetPos ].dt_longvarchar_ucs, Digit_2_Charset[column1Value]->astr ); 
				icu_ConTo( rowset[ rowsetPos ].dt_nchar, Digit_2_Charset[column1Value]->astr );
				icu_ConTo( rowset[ rowsetPos ].dt_ncharvarying, Digit_2_Charset[column1Value]->astr );
				icu_IntToChar ( rowset[ rowsetPos ].dt_decimal_s, 1 );
				icu_IntToChar ( rowset[ rowsetPos ].dt_decimal_u, column2Value );
				icu_IntToChar ( rowset[ rowsetPos ].dt_numeric_s, 1 );
				icu_IntToChar ( rowset[ rowsetPos ].dt_numeric_u, 1 );
				icu_IntToChar ( rowset[ rowsetPos ].dt_tinyint_s, 1 );
				icu_IntToChar ( rowset[ rowsetPos ].dt_tinyint_u, 1 );
				icu_IntToChar ( rowset[ rowsetPos ].dt_smallinteger_s, 1 );
				icu_IntToChar ( rowset[ rowsetPos ].dt_smallinteger_u, 1 );
				icu_IntToChar ( rowset[ rowsetPos ].dt_integer_s, column1Value );  
				icu_IntToChar ( rowset[ rowsetPos ].dt_integer_u, column1Value );
				icu_IntToChar ( rowset[ rowsetPos ].dt_largeint, column1Value );
				icu_IntToChar ( rowset[ rowsetPos ].dt_real, column1Value, true );
				icu_IntToChar ( rowset[ rowsetPos ].dt_float, column1Value, true );
				icu_IntToChar ( rowset[ rowsetPos ].dt_double_precision, column1Value, true );
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
				icu_ConTo( rowset[ rowsetPos ].dt_bignum_s, "1234567890123456789" );
				icu_ConTo( rowset[ rowsetPos ].dt_bignum_u, "1234567890123456789" );
			}
			else {
				icu_ConTo( rowset1[ rowsetPos ].dt_char_utf8, Digit_2_Ascii[column1Value]->astr);
                rowset1[ rowsetPos ].ptr_char_utf8 = (SQLLEN) icu_strlen( rowset1[ rowsetPos ].dt_char_utf8 ) * 4;
				icu_ConTo( rowset1[ rowsetPos ].dt_char_ucs, Digit_2_Charset[column1Value]->astr );
                rowset1[ rowsetPos ].ptr_char_ucs = (SQLLEN) icu_strlen( rowset1[ rowsetPos ].dt_char_ucs );
				icu_ConTo( rowset1[ rowsetPos ].dt_varchar_utf8, Digit_2_Ascii[column1Value]->astr );
                rowset1[ rowsetPos ].ptr_varchar_utf8 = (SQLLEN) icu_strlen( rowset1[ rowsetPos ].dt_varchar_utf8 );
				icu_ConTo( rowset1[ rowsetPos ].dt_varchar_ucs, Digit_2_Charset[column1Value]->astr );
                rowset1[ rowsetPos ].ptr_varchar_ucs = (SQLLEN) icu_strlen( rowset1[ rowsetPos ].dt_varchar_ucs );
                icu_ConTo( rowset1[ rowsetPos ].dt_longvarchar_utf8, Digit_2_Ascii[column1Value]->astr );
                rowset1[ rowsetPos ].ptr_longvarchar_utf8 = (SQLLEN) icu_strlen( rowset1[ rowsetPos ].dt_longvarchar_utf8 );
				icu_ConTo( rowset1[ rowsetPos ].dt_longvarchar_ucs, Digit_2_Charset[column1Value]->astr );
                rowset1[ rowsetPos ].ptr_longvarchar_ucs = (SQLLEN) icu_strlen( rowset1[ rowsetPos ].dt_longvarchar_ucs );
				icu_ConTo( rowset1[ rowsetPos ].dt_nchar, Digit_2_Charset[column1Value]->astr );
                rowset1[ rowsetPos ].ptr_nchar = (SQLLEN) icu_strlen( rowset1[ rowsetPos ].dt_nchar );
				icu_ConTo( rowset1[ rowsetPos ].dt_ncharvarying, Digit_2_Charset[column1Value]->astr );
                rowset1[ rowsetPos ].ptr_ncharvarying = (SQLLEN) icu_strlen( rowset1[ rowsetPos ].dt_ncharvarying );
				icu_IntToChar ( rowset1[ rowsetPos ].dt_decimal_s, 1 );
				icu_IntToChar ( rowset1[ rowsetPos ].dt_decimal_u, column2Value );
				icu_IntToChar ( rowset1[ rowsetPos ].dt_numeric_s, 1 );
				icu_IntToChar ( rowset1[ rowsetPos ].dt_numeric_u, 1 );
				icu_IntToChar ( rowset1[ rowsetPos ].dt_tinyint_s, 1 );
				icu_IntToChar ( rowset1[ rowsetPos ].dt_tinyint_u, 1 );
				icu_IntToChar ( rowset1[ rowsetPos ].dt_smallinteger_s, 1 );
				icu_IntToChar ( rowset1[ rowsetPos ].dt_smallinteger_u, 1 );
				icu_IntToChar ( rowset1[ rowsetPos ].dt_integer_s, column1Value );  
				icu_IntToChar ( rowset1[ rowsetPos ].dt_integer_u, column1Value );
				icu_IntToChar ( rowset1[ rowsetPos ].dt_largeint, column1Value );
				icu_IntToChar ( rowset1[ rowsetPos ].dt_real, column1Value, true);
				icu_IntToChar ( rowset1[ rowsetPos ].dt_float, column1Value, true );
				icu_IntToChar ( rowset1[ rowsetPos ].dt_double_precision, column1Value, true );
				rowset1[ rowsetPos ].dt_date.year  = 2000;
				rowset1[ rowsetPos ].dt_date.month = 1;
				rowset1[ rowsetPos ].dt_date.day   = 2;
				rowset1[ rowsetPos ].dt_time.hour   = 3;
				rowset1[ rowsetPos ].dt_time.minute = 4;
				rowset1[ rowsetPos ].dt_time.second = 5;
				rowset1[ rowsetPos ].dt_timestamp.year     = 2000;
				rowset1[ rowsetPos ].dt_timestamp.month    = 1;
				rowset1[ rowsetPos ].dt_timestamp.day      = 2;
				rowset1[ rowsetPos ].dt_timestamp.hour     = 3;
				rowset1[ rowsetPos ].dt_timestamp.minute   = 4;
				rowset1[ rowsetPos ].dt_timestamp.second   = 5;
				rowset1[ rowsetPos ].dt_timestamp.fraction = 600000;
				rowset1[ rowsetPos ].dt_interval_year.intval.year_month.year       = 0;
				rowset1[ rowsetPos ].dt_interval_month.intval.year_month.month     = 1;
				rowset1[ rowsetPos ].dt_interval_day.intval.day_second.day         = 2;
				rowset1[ rowsetPos ].dt_interval_hour.intval.day_second.hour       = 3;
				rowset1[ rowsetPos ].dt_interval_minute.intval.day_second.minute   = 4;
				rowset1[ rowsetPos ].dt_interval_second.intval.day_second.second   = 5;
				rowset1[ rowsetPos ].dt_interval_second.intval.day_second.fraction = 6;
				rowset1[ rowsetPos ].dt_interval_year_to_month.intval.year_month.year  = 0;
				rowset1[ rowsetPos ].dt_interval_year_to_month.intval.year_month.month = 1;
				rowset1[ rowsetPos ].dt_interval_day_to_hour.intval.day_second.day  = 2;
				rowset1[ rowsetPos ].dt_interval_day_to_hour.intval.day_second.hour = 3;
				rowset1[ rowsetPos ].dt_interval_day_to_minute.intval.day_second.day    = 2;
				rowset1[ rowsetPos ].dt_interval_day_to_minute.intval.day_second.hour   = 3;
				rowset1[ rowsetPos ].dt_interval_day_to_minute.intval.day_second.minute = 4;
				rowset1[ rowsetPos ].dt_interval_day_to_second.intval.day_second.day      = 2;
				rowset1[ rowsetPos ].dt_interval_day_to_second.intval.day_second.hour     = 3;
				rowset1[ rowsetPos ].dt_interval_day_to_second.intval.day_second.minute   = 4;
				rowset1[ rowsetPos ].dt_interval_day_to_second.intval.day_second.second   = 5;
				rowset1[ rowsetPos ].dt_interval_day_to_second.intval.day_second.fraction = 6;
				rowset1[ rowsetPos ].dt_interval_hour_to_minute.intval.day_second.hour   = 3;
				rowset1[ rowsetPos ].dt_interval_hour_to_minute.intval.day_second.minute = 4;
				rowset1[ rowsetPos ].dt_interval_hour_to_second.intval.day_second.hour     = 3;
				rowset1[ rowsetPos ].dt_interval_hour_to_second.intval.day_second.minute   = 4;
				rowset1[ rowsetPos ].dt_interval_hour_to_second.intval.day_second.second   = 5;
				rowset1[ rowsetPos ].dt_interval_hour_to_second.intval.day_second.fraction = 6;
				rowset1[ rowsetPos ].dt_interval_minute_to_second.intval.day_second.minute   = 4;
				rowset1[ rowsetPos ].dt_interval_minute_to_second.intval.day_second.second   = 5;
				rowset1[ rowsetPos ].dt_interval_minute_to_second.intval.day_second.fraction = 6;
				icu_ConTo( rowset1[ rowsetPos ].dt_bignum_s, "1234567890123456789" );
				icu_ConTo( rowset1[ rowsetPos ].dt_bignum_u, "1234567890123456789" );
			}
            break;
        case COLUMN:
			if( type == ROWSET_PRIMARY ) {
				icu_ConTo( &dt_char_utf8[ rowsetPos * STRINGMAX ], Digit_2_Ascii[column1Value]->astr );
				icu_ConTo( &dt_char_ucs[ rowsetPos * STRINGMAX  ], Digit_2_Charset[column1Value]->astr );
				icu_ConTo( &dt_varchar_utf8[ rowsetPos * STRINGMAX  ], Digit_2_Ascii[column1Value]->astr );
				icu_ConTo( &dt_varchar_ucs[ rowsetPos * STRINGMAX  ],Digit_2_Charset[column1Value]->astr );
				icu_ConTo( &dt_longvarchar_utf8[ rowsetPos * STRINGMAX  ], Digit_2_Ascii[column1Value]->astr );
				icu_ConTo( &dt_longvarchar_ucs[ rowsetPos * STRINGMAX  ], Digit_2_Charset[column1Value]->astr );
				icu_ConTo( &dt_nchar[ rowsetPos * STRINGMAX  ], Digit_2_Charset[column1Value]->astr );
				icu_ConTo( &dt_ncharvarying[ rowsetPos * STRINGMAX  ], Digit_2_Charset[column1Value]->astr );
				icu_IntToChar( &dt_decimal_s[ rowsetPos * STRINGMAX  ], 1 );
				icu_IntToChar( &dt_decimal_u[ rowsetPos * STRINGMAX  ], column2Value );
				icu_IntToChar( &dt_numeric_s[ rowsetPos * STRINGMAX  ], 1 );
				icu_IntToChar( &dt_numeric_u[ rowsetPos * STRINGMAX  ], 1 );
				icu_IntToChar( &dt_tinyint_s[ rowsetPos * STRINGMAX  ], 1 );
				icu_IntToChar( &dt_tinyint_u[ rowsetPos * STRINGMAX  ], 1 );
				icu_IntToChar( &dt_smallinteger_s[ rowsetPos * STRINGMAX  ], 1 );
				icu_IntToChar( &dt_smallinteger_u[ rowsetPos * STRINGMAX  ], 1 );
				icu_IntToChar( &dt_integer_s[ rowsetPos * STRINGMAX  ], column2Value );
				icu_IntToChar( &dt_integer_u[ rowsetPos * STRINGMAX  ], column1Value );
				icu_IntToChar( &dt_largeint[ rowsetPos * STRINGMAX  ], column1Value );
				icu_IntToChar( &dt_real[ rowsetPos * STRINGMAX  ], column1Value, true );
				icu_IntToChar( &dt_float[ rowsetPos * STRINGMAX  ], column1Value, true );
				icu_IntToChar( &dt_double_precision[ rowsetPos * STRINGMAX  ], column1Value, true );
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
				icu_ConTo( &dt_bignum_s[ rowsetPos * STRINGMAX  ], "1234567890123456789" );
				icu_ConTo( &dt_bignum_u[ rowsetPos * STRINGMAX  ], "1234567890123456789" );
			} 
			else {
				icu_ConTo( &dt_char_utf8_1[ rowsetPos * STRINGMAX ], Digit_2_Ascii[column1Value]->astr );
                ptr_char_utf8_1[ rowsetPos ] = (SQLLEN) icu_strlen( &dt_char_utf8_1[ rowsetPos * STRINGMAX ] ) * 4;
				icu_ConTo( &dt_char_ucs1[ rowsetPos * STRINGMAX ], Digit_2_Charset[column1Value]->astr );
                ptr_char_ucs1[ rowsetPos ] = (SQLLEN) icu_strlen( &dt_char_ucs1[ rowsetPos * STRINGMAX ] );
				icu_ConTo( &dt_varchar_utf8_1[ rowsetPos * STRINGMAX ], Digit_2_Ascii[column1Value]->astr );
                ptr_varchar_utf8_1[ rowsetPos ] = (SQLLEN) icu_strlen( &dt_varchar_utf8_1[ rowsetPos * STRINGMAX ] );
				icu_ConTo( &dt_varchar_ucs1[ rowsetPos * STRINGMAX ],Digit_2_Charset[column1Value]->astr );
                ptr_varchar_ucs1[ rowsetPos ] = (SQLLEN) icu_strlen( &dt_varchar_ucs1[ rowsetPos * STRINGMAX ] );
				icu_ConTo( &dt_longvarchar_utf8_1[ rowsetPos * STRINGMAX ], Digit_2_Ascii[column1Value]->astr );
                ptr_longvarchar_utf8_1[ rowsetPos ] = (SQLLEN) icu_strlen( &dt_longvarchar_utf8_1[ rowsetPos * STRINGMAX ] );
				icu_ConTo( &dt_longvarchar_ucs1[ rowsetPos * STRINGMAX ], Digit_2_Charset[column1Value]->astr );
                ptr_longvarchar_ucs1[ rowsetPos ] = (SQLLEN) icu_strlen( &dt_longvarchar_ucs1[ rowsetPos * STRINGMAX ] );
				icu_ConTo( &dt_nchar1[ rowsetPos * STRINGMAX ], Digit_2_Charset[column1Value]->astr );
                ptr_nchar1[ rowsetPos ] = (SQLLEN) icu_strlen( &dt_nchar1[ rowsetPos * STRINGMAX ] );
				icu_ConTo( &dt_ncharvarying1[ rowsetPos * STRINGMAX ], Digit_2_Charset[column1Value]->astr );
                ptr_ncharvarying1[ rowsetPos ] = (SQLLEN) icu_strlen( &dt_ncharvarying1[ rowsetPos * STRINGMAX ] );
				icu_IntToChar( &dt_decimal_s1[ rowsetPos * STRINGMAX ], 1 );
				icu_IntToChar( &dt_decimal_u1[ rowsetPos * STRINGMAX ], column2Value );
				icu_IntToChar( &dt_numeric_s1[ rowsetPos * STRINGMAX ], 1 );
				icu_IntToChar( &dt_numeric_u1[ rowsetPos * STRINGMAX ], 1 );
				icu_IntToChar( &dt_tinyint_s1[ rowsetPos * STRINGMAX ], 1 );
				icu_IntToChar( &dt_tinyint_u1[ rowsetPos * STRINGMAX ], 1 );
				icu_IntToChar( &dt_smallinteger_s1[ rowsetPos * STRINGMAX ], 1 );
				icu_IntToChar( &dt_smallinteger_u1[ rowsetPos * STRINGMAX ], 1 );
				icu_IntToChar( &dt_integer_s1[ rowsetPos * STRINGMAX ], column2Value );
				icu_IntToChar( &dt_integer_u1[ rowsetPos * STRINGMAX ], column1Value );
				icu_IntToChar( &dt_largeint1[ rowsetPos * STRINGMAX ], column1Value );
				icu_IntToChar( &dt_real1[ rowsetPos * STRINGMAX ], column1Value, true );
				icu_IntToChar( &dt_float1[ rowsetPos * STRINGMAX ], column1Value, true );
				icu_IntToChar( &dt_double_precision1[ rowsetPos * STRINGMAX ], column1Value, true );
				dt_date1[ rowsetPos ].year  = 2000;
				dt_date1[ rowsetPos ].month = 1;
				dt_date1[ rowsetPos ].day   = 2;
				dt_time1[ rowsetPos ].hour   = 3;
				dt_time1[ rowsetPos ].minute = 4;
				dt_time1[ rowsetPos ].second = 5;
				dt_timestamp1[ rowsetPos ].year     = 2000;
				dt_timestamp1[ rowsetPos ].month    = 1;
				dt_timestamp1[ rowsetPos ].day      = 2;
				dt_timestamp1[ rowsetPos ].hour     = 3;
				dt_timestamp1[ rowsetPos ].minute   = 4;
				dt_timestamp1[ rowsetPos ].second   = 5;
				dt_timestamp1[ rowsetPos ].fraction = 600000;
				dt_interval_year1[ rowsetPos ].intval.year_month.year       = 0;
				dt_interval_month1[ rowsetPos ].intval.year_month.month     = 1;
				dt_interval_day1[ rowsetPos ].intval.day_second.day         = 2;
				dt_interval_hour1[ rowsetPos ].intval.day_second.hour       = 3;
				dt_interval_minute1[ rowsetPos ].intval.day_second.minute   = 4;
				dt_interval_second1[ rowsetPos ].intval.day_second.second   = 5;
				dt_interval_second1[ rowsetPos ].intval.day_second.fraction = 6;
				dt_interval_year_to_month1[ rowsetPos ].intval.year_month.year  = 0;
				dt_interval_year_to_month1[ rowsetPos ].intval.year_month.month = 1;
				dt_interval_day_to_hour1[ rowsetPos ].intval.day_second.day  = 2;
				dt_interval_day_to_hour1[ rowsetPos ].intval.day_second.hour = 3;
				dt_interval_day_to_minute1[ rowsetPos ].intval.day_second.day    = 2;
				dt_interval_day_to_minute1[ rowsetPos ].intval.day_second.hour   = 3;
				dt_interval_day_to_minute1[ rowsetPos ].intval.day_second.minute = 4;
				dt_interval_day_to_second1[ rowsetPos ].intval.day_second.day      = 2;
				dt_interval_day_to_second1[ rowsetPos ].intval.day_second.hour     = 3;
				dt_interval_day_to_second1[ rowsetPos ].intval.day_second.minute   = 4;
				dt_interval_day_to_second1[ rowsetPos ].intval.day_second.second   = 5;
				dt_interval_day_to_second1[ rowsetPos ].intval.day_second.fraction = 6;
				dt_interval_hour_to_minute1[ rowsetPos ].intval.day_second.hour   = 3;
				dt_interval_hour_to_minute1[ rowsetPos ].intval.day_second.minute = 4;
				dt_interval_hour_to_second1[ rowsetPos ].intval.day_second.hour     = 3;
				dt_interval_hour_to_second1[ rowsetPos ].intval.day_second.minute   = 4;
				dt_interval_hour_to_second1[ rowsetPos ].intval.day_second.second   = 5;
				dt_interval_hour_to_second1[ rowsetPos ].intval.day_second.fraction = 6;
				dt_interval_minute_to_second1[ rowsetPos ].intval.day_second.minute   = 4;
				dt_interval_minute_to_second1[ rowsetPos ].intval.day_second.second   = 5;
				dt_interval_minute_to_second1[ rowsetPos ].intval.day_second.fraction = 6;
				icu_ConTo( &dt_bignum_s1[ rowsetPos * STRINGMAX  ], "1234567890123456789" );
				icu_ConTo( &dt_bignum_u1[ rowsetPos * STRINGMAX  ], "1234567890123456789" );
			}
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
                    AssignRow( rs, numberOfRowsHandled + 1, numberOfRowsHandled + 1, ROWSET_PRIMARY );
                    break;
                case DUPLICATEKEY:
                    if( ( rs % 5 ) == 0 )
                    {
                        // Inject an error.
                        switch( actions[ unitTest.action] )
                        {
                            case UPDATE:
                                AssignRow( rs, numberOfRowsHandled, numberOfRowsHandled + 1, ROWSET_PRIMARY );
                                break;
                            default:
                                AssignRow( rs, 1, numberOfRowsHandled, ROWSET_PRIMARY );
                                break;
                        }
                        failureInjectionCount++;
                    }
                    else
                    {
                        // Do not inject an error.
                        AssignRow( rs, numberOfRowsHandled + 1, numberOfRowsHandled + 1, ROWSET_PRIMARY );
                    }
                    break;
                case UNIQUECONST:
                    if( ( rs % 5 ) == 0 )
                    {
                        // Inject an error.
                        switch( actions[ unitTest.action] )
                        {
                            case UPDATE:
                                AssignRow( rs, numberOfRowsHandled + 50001, numberOfRowsHandled + 1, ROWSET_PRIMARY );
                                break;
                            default:
                                AssignRow( rs, numberOfRowsHandled + 1, numberOfRowsHandled + 50001, ROWSET_PRIMARY );
                                break;
                        }
                        failureInjectionCount++;
                    }
                    else
                    {
                        // Do not inject an error.
                        AssignRow(  rs,numberOfRowsHandled+ 1,numberOfRowsHandled+ 1, ROWSET_PRIMARY );
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
                    AssignRow(  rs,numberOfRowsHandled+ 1,numberOfRowsHandled+ 1, ROWSET_PRIMARY );
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

        if( ( errorChecking == MODE_SPECIAL_1 ) && ( (int)rowCount != (int)rowsProcessed ) )
        {
            RecordToLog( " >> ERROR: The number of good rows processed [%d] does not match the SQLRowCount() [%d] at line %d.\n", rowsProcessed, rowCount, __LINE__);
            rc = false;
        }
        if( ( errorChecking == STANDARD ) && ( (int)rowCount != (int)( rowsProcessed - failureInjectionCount ) ) )
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

	BindColsA( bindOrientations[ unitTest.bindOrientation ] );

    // See if we want the rowsets to be processed through preapre or directly.
    if( operations[ unitTest.operation ] == PREPARE_EXECUTE )
    {
        switch( actions[ unitTest.action] )
        {
            case SELECT:
            case INSERT_BULK:
                while( ( retcode = SQLPrepareW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStr[ 3 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING );
                break;
            default:
                break;
        }
    
        // Check the return status from the prepared statement.
        if( retcode != SQL_SUCCESS )    
        {
            CheckMsgs( "SQLPrepareW()", __LINE__ );
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
	int i = 0;

    // First we need to figure out what the value should be.
    if( bindOrientations[ unitTest.bindOrientation ] == SINGLE )
    {
		//RecordToLog("No comparisons for SINGLE bindtype\n");
        return true;
    }

	//Now comparing between rowset[rowsetPos] and rowset1[rowpos[rowsetPos]]
    //RecordToLog("Index is at %d and value %d\n", rowsetPos, rowpos[ rowsetPos ]);

   	switch( bindOrientations[ unitTest.bindOrientation ] )
    {
        case ROW:
        case SINGLE:
			//Checked size of data returned
			rc = CheckNum( "ptr_char_utf8",          rowset1[ rowpos[ rowsetPos ] ].ptr_char_utf8,          rowset[ rowsetPos ].ptr_char_utf8,       __LINE__, rc );
            rc = CheckNum( "ptr_varchar_utf8",       rowset1[ rowpos[ rowsetPos ] ].ptr_varchar_utf8,       rowset[ rowsetPos ].ptr_varchar_utf8,    __LINE__, rc );
            rc = CheckNum( "ptr_varchar_ucs",       rowset1[ rowpos[ rowsetPos ] ].ptr_varchar_ucs,       rowset[ rowsetPos ].ptr_varchar_ucs,    __LINE__, rc );
            rc = CheckNum( "ptr_longvarchar_utf8",   rowset1[ rowpos[ rowsetPos ] ].ptr_longvarchar_utf8,   rowset[ rowsetPos ].ptr_longvarchar_utf8,__LINE__, rc );
            rc = CheckNum( "ptr_longvarchar_ucs",   rowset1[ rowpos[ rowsetPos ] ].ptr_longvarchar_ucs,   rowset[ rowsetPos ].ptr_longvarchar_ucs,__LINE__, rc );
            rc = CheckNum( "ptr_nchar",             rowset1[ rowpos[ rowsetPos ] ].ptr_nchar,             rowset[ rowsetPos ].ptr_nchar,          __LINE__, rc );
            rc = CheckNum( "ptr_ncharvarying",      rowset1[ rowpos[ rowsetPos ] ].ptr_ncharvarying,      rowset[ rowsetPos ].ptr_ncharvarying,   __LINE__, rc );

			//Check value of data returned
            rc = CheckStrN( "dt_char_utf8",           rowset1[ rowpos[ rowsetPos ] ].dt_char_utf8,           rowset[ rowsetPos ].dt_char_utf8,    icu_strlen(rowset1[ rowpos[ rowsetPos] ].dt_char_utf8),    __LINE__, rc );
            rc = CheckStr( "dt_char_ucs",           rowset1[ rowpos[ rowsetPos ] ].dt_char_ucs,           rowset[ rowsetPos ].dt_char_ucs,        __LINE__, rc );
            rc = CheckStr( "dt_varchar_utf8",        rowset1[ rowpos[ rowsetPos ] ].dt_varchar_utf8,        rowset[ rowsetPos ].dt_varchar_utf8 ,    __LINE__, rc );
            rc = CheckStr( "dt_varchar_ucs",        rowset1[ rowpos[ rowsetPos ] ].dt_varchar_ucs,        rowset[ rowsetPos ].dt_varchar_ucs,     __LINE__, rc );
            rc = CheckStr( "dt_longvarchar_utf8",    rowset1[ rowpos[ rowsetPos ] ].dt_longvarchar_utf8,    rowset[ rowsetPos ].dt_longvarchar_utf8, __LINE__, rc );
            rc = CheckStr( "dt_longvarchar_ucs",    rowset1[ rowpos[ rowsetPos ] ].dt_longvarchar_ucs,    rowset[ rowsetPos ].dt_longvarchar_ucs, __LINE__, rc );
            rc = CheckStr( "dt_nchar",              rowset1[ rowpos[ rowsetPos ] ].dt_nchar,              rowset[ rowsetPos ].dt_nchar ,          __LINE__, rc );
            rc = CheckStr( "dt_ncharvarying",       rowset1[ rowpos[ rowsetPos ] ].dt_ncharvarying,       rowset[ rowsetPos ].dt_ncharvarying,    __LINE__, rc );

            rc = CheckStrN( "dt_decimal_s",         rowset1[ rowpos[ rowsetPos ] ].dt_decimal_s,          rowset[ rowsetPos ].dt_decimal_s,       rowset[ rowsetPos ].ptr_decimal_s,          __LINE__, rc );
            rc = CheckStrN( "dt_decimal_u",         rowset1[ rowpos[ rowsetPos ] ].dt_decimal_u,          rowset[ rowsetPos ].dt_decimal_u,       rowset[ rowsetPos ].ptr_decimal_u,          __LINE__, rc );
            rc = CheckStrN( "dt_numeric_s",         rowset1[ rowpos[ rowsetPos ] ].dt_numeric_s,          rowset[ rowsetPos ].dt_numeric_s,       rowset[ rowsetPos ].ptr_numeric_s,          __LINE__, rc );
            rc = CheckStrN( "dt_numeric_u",         rowset1[ rowpos[ rowsetPos ] ].dt_numeric_u,          rowset[ rowsetPos ].dt_numeric_u,       rowset[ rowsetPos ].ptr_numeric_u,          __LINE__, rc );
            rc = CheckStrN( "dt_tinyint_s",         rowset1[ rowpos[ rowsetPos ] ].dt_tinyint_s,          rowset[ rowsetPos ].dt_tinyint_s,       rowset[ rowsetPos ].ptr_tinyint_s,          __LINE__, rc );
            rc = CheckStrN( "dt_tinyint_u",         rowset1[ rowpos[ rowsetPos ] ].dt_tinyint_u,          rowset[ rowsetPos ].dt_tinyint_u,       rowset[ rowsetPos ].ptr_tinyint_u,          __LINE__, rc );
            rc = CheckStrN( "dt_smallinteger_s",    rowset1[ rowpos[ rowsetPos ] ].dt_smallinteger_s,     rowset[ rowsetPos ].dt_smallinteger_s,  rowset[ rowsetPos ].ptr_smallinteger_s,     __LINE__, rc );
            rc = CheckStrN( "dt_smallinteger_u",    rowset1[ rowpos[ rowsetPos ] ].dt_smallinteger_u,     rowset[ rowsetPos ].dt_smallinteger_u,  rowset[ rowsetPos ].ptr_smallinteger_u,     __LINE__, rc );
            rc = CheckStrN( "dt_integer_s",         rowset1[ rowpos[ rowsetPos ] ].dt_integer_s,          rowset[ rowsetPos ].dt_integer_s,       rowset[ rowsetPos ].ptr_integer_s,          __LINE__, rc );
            rc = CheckStrN( "dt_integer_u",         rowset1[ rowpos[ rowsetPos ] ].dt_integer_u,          rowset[ rowsetPos ].dt_integer_u,       rowset[ rowsetPos ].ptr_integer_u,          __LINE__, rc );
            rc = CheckStrN( "dt_largeint",          rowset1[ rowpos[ rowsetPos ] ].dt_largeint,           rowset[ rowsetPos ].dt_largeint,        rowset[ rowsetPos ].ptr_largeint,           __LINE__, rc );
            rc = CheckStrN( "dt_real",              rowset1[ rowpos[ rowsetPos ] ].dt_real,               rowset[ rowsetPos ].dt_real,            rowset[ rowsetPos ].ptr_real,               __LINE__, rc );
            rc = CheckStrN( "dt_float",             rowset1[ rowpos[ rowsetPos ] ].dt_float,              rowset[ rowsetPos ].dt_float,           rowset[ rowsetPos ].ptr_float,              __LINE__, rc );
            rc = CheckStrN( "dt_double_precision",  rowset1[ rowpos[ rowsetPos ] ].dt_double_precision,   rowset[ rowsetPos ].dt_double_precision,rowset[ rowsetPos ].ptr_double_precision,   __LINE__, rc );

			if (tableFeatures[ unitTest.tableFeature ] == BEFORETRIGGER) {
				rc = CheckStrN( "dt_bignum_s", rowset1[ rowpos[ rowsetPos ] ].dt_bignum_s, rowset[ rowsetPos ].dt_bignum_s, rowset[ rowsetPos ].ptr_bignum_s, __LINE__, rc );
				rc = CheckStrN( "dt_bignum_u", rowset1[ rowpos[ rowsetPos ] ].dt_bignum_u, rowset[ rowsetPos ].dt_bignum_u, rowset[ rowsetPos ].ptr_bignum_u, __LINE__, rc );
			}
			else
			{
				rc = CheckStrN( "dt_bignum_s", rowset1[ rowpos[ rowsetPos ] ].dt_bignum_s, rowset[ rowsetPos ].dt_bignum_s, rowset[ rowsetPos ].ptr_bignum_s, __LINE__, rc );
				rc = CheckStrN( "dt_bignum_u", rowset1[ rowpos[ rowsetPos ] ].dt_bignum_u, rowset[ rowsetPos ].dt_bignum_u, rowset[ rowsetPos ].ptr_bignum_u, __LINE__, rc );
			}

			if (errorChecking != MODE_SPECIAL_1) {
				rc = CheckNum( "dt_date.year",          rowset1[ rowpos[ rowsetPos ] ].dt_date.year,          rowset[ rowsetPos ].dt_date.year,           __LINE__, rc );
				rc = CheckNum( "dt_date.month",         rowset1[ rowpos[ rowsetPos ] ].dt_date.month,         rowset[ rowsetPos ].dt_date.month,          __LINE__, rc );
				rc = CheckNum( "dt_date.day",           rowset1[ rowpos[ rowsetPos ] ].dt_date.day,           rowset[ rowsetPos ].dt_date.day,            __LINE__, rc );
				rc = CheckNum( "dt_time.hour",          rowset1[ rowpos[ rowsetPos ] ].dt_time.hour,          rowset[ rowsetPos ].dt_time.hour,           __LINE__, rc );
				rc = CheckNum( "dt_time.minute",        rowset1[ rowpos[ rowsetPos ] ].dt_time.minute,        rowset[ rowsetPos ].dt_time.minute,         __LINE__, rc );
				rc = CheckNum( "dt_time.second",        rowset1[ rowpos[ rowsetPos ] ].dt_time.second,        rowset[ rowsetPos ].dt_time.second,         __LINE__, rc );
				rc = CheckNum( "dt_timestamp.year",     rowset1[ rowpos[ rowsetPos ] ].dt_timestamp.year,     rowset[ rowsetPos ].dt_timestamp.year,      __LINE__, rc );
				rc = CheckNum( "dt_timestamp.month",    rowset1[ rowpos[ rowsetPos ] ].dt_timestamp.month,    rowset[ rowsetPos ].dt_timestamp.month,     __LINE__, rc );
				rc = CheckNum( "dt_timestamp.day",      rowset1[ rowpos[ rowsetPos ] ].dt_timestamp.day,      rowset[ rowsetPos ].dt_timestamp.day,       __LINE__, rc );
				rc = CheckNum( "dt_timestamp.hour",     rowset1[ rowpos[ rowsetPos ] ].dt_timestamp.hour,     rowset[ rowsetPos ].dt_timestamp.hour,      __LINE__, rc );
				rc = CheckNum( "dt_timestamp.minute",   rowset1[ rowpos[ rowsetPos ] ].dt_timestamp.minute,   rowset[ rowsetPos ].dt_timestamp.minute,    __LINE__, rc );
				rc = CheckNum( "dt_timestamp.second",   rowset1[ rowpos[ rowsetPos ] ].dt_timestamp.second,   rowset[ rowsetPos ].dt_timestamp.second,    __LINE__, rc );
				rc = CheckNum( "dt_timestamp.fraction", rowset1[ rowpos[ rowsetPos ] ].dt_timestamp.fraction, rowset[ rowsetPos ].dt_timestamp.fraction,  __LINE__, rc );
			}
            break;

        case COLUMN:
			//Checked size of data returned
			rc = CheckNum( "ptr_char_utf8",          ptr_char_utf8_1[ rowpos[ rowsetPos ] ],         ptr_char_utf8[ rowsetPos ],          __LINE__, rc );
			rc = CheckNum( "ptr_char_ucs",          ptr_char_ucs1[ rowpos[ rowsetPos ] ],         ptr_char_ucs[ rowsetPos ],          __LINE__, rc );
            rc = CheckNum( "ptr_varchar_utf8",       ptr_varchar_utf8_1[ rowpos[ rowsetPos ] ],      ptr_varchar_utf8[ rowsetPos ],       __LINE__, rc );
		    rc = CheckNum( "ptr_varchar_ucs",       ptr_varchar_ucs1[ rowpos[ rowsetPos ] ],      ptr_varchar_ucs[ rowsetPos ],       __LINE__, rc );
			rc = CheckNum( "ptr_longvarchar_utf8",   ptr_longvarchar_utf8_1[ rowpos[ rowsetPos ] ],  ptr_longvarchar_utf8[ rowsetPos ],   __LINE__, rc );
			rc = CheckNum( "ptr_longvarchar_ucs",   ptr_longvarchar_ucs1[ rowpos[ rowsetPos ] ],  ptr_longvarchar_ucs[ rowsetPos ],   __LINE__, rc );
			rc = CheckNum( "ptr_nchar",             ptr_nchar1[ rowpos[ rowsetPos ] ],            ptr_nchar[ rowsetPos ],             __LINE__, rc );
			rc = CheckNum( "ptr_ncharvarying",      ptr_ncharvarying1[ rowpos[ rowsetPos ] ],     ptr_ncharvarying[ rowsetPos ],      __LINE__, rc );

            //Check value of data returned
			rc = CheckStrN( "dt_char_utf8",           &dt_char_utf8_1[ rowpos[ rowsetPos ] * STRINGMAX ],         &dt_char_utf8[ rowsetPos * STRINGMAX ],   icu_strlen( &dt_char_utf8_1[ rowpos[ rowsetPos ] * STRINGMAX ]),      __LINE__, rc );
			rc = CheckStr( "dt_char_ucs",           &dt_char_ucs1[ rowpos[ rowsetPos ] * STRINGMAX ],         &dt_char_ucs[ rowsetPos * STRINGMAX ],          __LINE__, rc );
			rc = CheckStr( "dt_varchar_utf8",        &dt_varchar_utf8_1[ rowpos[ rowsetPos ] * STRINGMAX ],      &dt_varchar_utf8[ rowsetPos * STRINGMAX ],       __LINE__, rc );
			rc = CheckStr( "dt_varchar_ucs",        &dt_varchar_ucs1[ rowpos[ rowsetPos ] * STRINGMAX ],      &dt_varchar_ucs[ rowsetPos * STRINGMAX ],       __LINE__, rc );
			rc = CheckStr( "dt_longvarchar_utf8",    &dt_longvarchar_utf8_1[ rowpos[ rowsetPos ] * STRINGMAX ],  &dt_longvarchar_utf8[ rowsetPos * STRINGMAX ],   __LINE__, rc );
			rc = CheckStr( "dt_longvarchar_ucs",    &dt_longvarchar_ucs1[ rowpos[ rowsetPos ] * STRINGMAX ],  &dt_longvarchar_ucs[ rowsetPos * STRINGMAX ],   __LINE__, rc );
			rc = CheckStr( "dt_nchar",              &dt_nchar1[ rowpos[ rowsetPos ] * STRINGMAX ],            &dt_nchar[ rowsetPos * STRINGMAX ],             __LINE__, rc );
			rc = CheckStr( "dt_ncharvarying",       &dt_ncharvarying1[ rowpos[ rowsetPos ] * STRINGMAX ],     &dt_ncharvarying[ rowsetPos * STRINGMAX ],      __LINE__, rc );
			rc = CheckStrN( "dt_decimal_s",         &dt_decimal_s1[ rowpos[ rowsetPos ] * STRINGMAX ],        &dt_decimal_s[ rowsetPos * STRINGMAX ],         ptr_decimal_s[ rowsetPos ],         __LINE__, rc );
			rc = CheckStrN( "dt_decimal_u",         &dt_decimal_u1[ rowpos[ rowsetPos ] * STRINGMAX ],        &dt_decimal_u[ rowsetPos * STRINGMAX ],         ptr_decimal_u[ rowsetPos ],         __LINE__, rc );
			rc = CheckStrN( "dt_numeric_s",         &dt_numeric_s1[ rowpos[ rowsetPos ] * STRINGMAX ],        &dt_numeric_s[ rowsetPos * STRINGMAX ],         ptr_numeric_s[ rowsetPos ],         __LINE__, rc );
			rc = CheckStrN( "dt_numeric_u",         &dt_numeric_u1[ rowpos[ rowsetPos ] * STRINGMAX ],        &dt_numeric_u[ rowsetPos * STRINGMAX ],         ptr_numeric_u[ rowsetPos ],         __LINE__, rc );
			rc = CheckStrN( "dt_tinyint_s",         &dt_tinyint_s1[ rowpos[ rowsetPos ] * STRINGMAX ],        &dt_tinyint_s[ rowsetPos * STRINGMAX ],         ptr_tinyint_s[ rowsetPos ],         __LINE__, rc );
			rc = CheckStrN( "dt_tinyint_u",         &dt_tinyint_u1[ rowpos[ rowsetPos ] * STRINGMAX ],        &dt_tinyint_u[ rowsetPos * STRINGMAX ],         ptr_tinyint_u[ rowsetPos ],         __LINE__, rc );
			rc = CheckStrN( "dt_smallinteger_s",    &dt_smallinteger_s1[ rowpos[ rowsetPos ] * STRINGMAX ],   &dt_smallinteger_s[ rowsetPos * STRINGMAX ],    ptr_smallinteger_s[ rowsetPos ],    __LINE__, rc );
			rc = CheckStrN( "dt_smallinteger_u",    &dt_smallinteger_u1[ rowpos[ rowsetPos ] * STRINGMAX ],   &dt_smallinteger_u[ rowsetPos * STRINGMAX ],    ptr_smallinteger_u[ rowsetPos ],    __LINE__, rc );
			rc = CheckStrN( "dt_integer_s",         &dt_integer_s1[ rowpos[ rowsetPos ] * STRINGMAX ],        &dt_integer_s[ rowsetPos * STRINGMAX ],         ptr_integer_s[ rowsetPos ],         __LINE__, rc );
			rc = CheckStrN( "dt_integer_u",         &dt_integer_u1[ rowpos[ rowsetPos ] * STRINGMAX ],        &dt_integer_u[ rowsetPos * STRINGMAX ],         ptr_integer_u[ rowsetPos ],         __LINE__, rc );
			rc = CheckStrN( "dt_largeint",          &dt_largeint1[ rowpos[ rowsetPos ] * STRINGMAX ],         &dt_largeint[ rowsetPos * STRINGMAX ],          ptr_largeint[ rowsetPos ],          __LINE__, rc );
			rc = CheckStrN( "dt_real",              &dt_real1[ rowpos[ rowsetPos ] * STRINGMAX ],             &dt_real[ rowsetPos * STRINGMAX ],              ptr_real[ rowsetPos ],              __LINE__, rc );
			rc = CheckStrN( "dt_float",             &dt_float1[ rowpos[ rowsetPos ] * STRINGMAX ],            &dt_float[ rowsetPos * STRINGMAX ],             ptr_float[ rowsetPos ],             __LINE__, rc );
			rc = CheckStrN( "dt_double_precision",  &dt_double_precision1[ rowpos[ rowsetPos ] * STRINGMAX ], &dt_double_precision[ rowsetPos * STRINGMAX ],  ptr_double_precision[ rowsetPos ],  __LINE__, rc );
			
			if (tableFeatures[ unitTest.tableFeature ] == BEFORETRIGGER) {
				rc = CheckStrN( "dt_bignum_s", &dt_bignum_s1[ rowpos[ rowsetPos ] * STRINGMAX ], &dt_bignum_s[ rowsetPos * STRINGMAX ], ptr_bignum_s[ rowsetPos ], __LINE__, rc );
				rc = CheckStrN( "dt_bignum_u", &dt_bignum_u1[ rowpos[ rowsetPos ] * STRINGMAX ], &dt_bignum_u[ rowsetPos * STRINGMAX ], ptr_bignum_u[ rowsetPos ], __LINE__, rc );
			}
			else
			{
				rc = CheckStrN( "dt_bignum_s", &dt_bignum_s1[ rowpos[ rowsetPos ] * STRINGMAX ], &dt_bignum_s[ rowsetPos * STRINGMAX ], ptr_bignum_s[ rowsetPos ], __LINE__, rc );
				rc = CheckStrN( "dt_bignum_u", &dt_bignum_u1[ rowpos[ rowsetPos ] * STRINGMAX ], &dt_bignum_u[ rowsetPos * STRINGMAX ], ptr_bignum_u[ rowsetPos ], __LINE__, rc );
			}

			if (errorChecking != MODE_SPECIAL_1) {
				rc = CheckNum( "dt_date.year",          dt_date1[ rowpos[ rowsetPos ] ].year,                 dt_date[ rowsetPos ].year,               __LINE__, rc );
				rc = CheckNum( "dt_date.month",         dt_date1[ rowpos[ rowsetPos ] ].month,                dt_date[ rowsetPos ].month,              __LINE__, rc );
				rc = CheckNum( "dt_date.day",           dt_date1[ rowpos[ rowsetPos ] ].day,                  dt_date[ rowsetPos ].day,                __LINE__, rc );
				rc = CheckNum( "dt_time.hour",          dt_time1[ rowpos[ rowsetPos ] ].hour,                 dt_time[ rowsetPos ].hour,               __LINE__, rc );
				rc = CheckNum( "dt_time.minute",        dt_time1[ rowpos[ rowsetPos ] ].minute,               dt_time[ rowsetPos ].minute,             __LINE__, rc );
				rc = CheckNum( "dt_time.second",        dt_time1[ rowpos[ rowsetPos ] ].second,               dt_time[ rowsetPos ].second,             __LINE__, rc );
				rc = CheckNum( "dt_timestamp.year",     dt_timestamp1[ rowpos[ rowsetPos ] ].year,            dt_timestamp[ rowsetPos ].year,          __LINE__, rc );
				rc = CheckNum( "dt_timestamp.month",    dt_timestamp1[ rowpos[ rowsetPos ] ].month,           dt_timestamp[ rowsetPos ].month,         __LINE__, rc );
				rc = CheckNum( "dt_timestamp.day",      dt_timestamp1[ rowpos[ rowsetPos ] ].day,             dt_timestamp[ rowsetPos ].day,           __LINE__, rc );
				rc = CheckNum( "dt_timestamp.hour",     dt_timestamp1[ rowpos[ rowsetPos ] ].hour,            dt_timestamp[ rowsetPos ].hour,          __LINE__, rc );
				rc = CheckNum( "dt_timestamp.minute",   dt_timestamp1[ rowpos[ rowsetPos ] ].minute,          dt_timestamp[ rowsetPos ].minute,        __LINE__, rc );
				rc = CheckNum( "dt_timestamp.second",   dt_timestamp1[ rowpos[ rowsetPos ] ].second,          dt_timestamp[ rowsetPos ].second,        __LINE__, rc );
				rc = CheckNum( "dt_timestamp.fraction", dt_timestamp1[ rowpos[ rowsetPos ] ].fraction,        dt_timestamp[ rowsetPos ].fraction,      __LINE__, rc );
			}			
            break;

		default:
			RecordToLog( "INTERNAL ERROR: An unknown access style has been discovered at line %d.\n", __LINE__ );
			rc = false;
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
    int numberOfRowsRetrieved = 0;

	// Generating expected Rowset for comparison
	GeneratingRows( rowsetSizes[ unitTest.rowsetSize ], numberOfRows[ unitTest.numberOfRows ], 
                         injectionTypes[ unitTest.injectionType ], tableTypes[ unitTest.tableType ], 
						 INSERT, bindOrientations[ unitTest.bindOrientation ],
						 ROWSET_SECONDARY);
    
    // Run the prepared select statement. 
    if( operations[ unitTest.operation ] == PREPARE_EXECUTE )
    {
        while( ( retcode = SQLExecute( handle[ SQL_HANDLE_STMT ] ) ) == SQL_STILL_EXECUTING );
    }
    else
    {
        while( (retcode = SQLExecDirectW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStr[ 3 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING );
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
        //while( ( retcode = SQLFetchScroll( handle[ SQL_HANDLE_STMT ], SQL_FETCH_NEXT, 0 ) ) == SQL_STILL_EXECUTING );
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
        //quicksort(rowpos, keyarray, 0, rowsetSizes[unitTest.rowsetSize]-1);
        //for( int idx = 0; idx < (int)rowsetSizes[unitTest.rowsetSize]; idx++ )
        //    RecordToLog("%d -- %d \n", rowpos[idx], keyarray[idx]);
        for( int rowPos = 0; rowPos < (int)rowsProcessed; rowPos++ ) 
        {
            rowValue++;
            if ( ( rowsetStatusArray[ rowPos ] == SQL_ROW_SUCCESS ) ||
                 ( rowsetStatusArray[ rowPos ] == SQL_ROW_SUCCESS_WITH_INFO ) ) 
            {
                // TODO: INSERT LOGIC TO MAKE SURE RETURNING VALUES ARE RIGHT
				if( CompareRow( rowPos, rowValue ) == false )
                    rc = false;
		    }
            else
            {
                RecordToLog(" >> ERROR: Rowset status array row %d was expected to have SQL_ROW_SUCCESS or SQL_ROW_SUCCESS_WITH_INFO. Actual: %d at line %d.\n", rowPos, rowsetStatusArray[ rowPos ] , __LINE__); 
                rc = false;
            }
        }

        if(rc == false) {
            PrintTestInformation();
            RecordToLog("Rows processed %d\n", rowsProcessed);
            DisplayTable( bindOrientations[ unitTest.bindOrientation ],rowsetSizes[ unitTest.rowsetSize ], ROWSET_PRIMARY );
	        RecordToLog(" \n ");
	        DisplayTable( bindOrientations[ unitTest.bindOrientation ],rowsetSizes[ unitTest.rowsetSize ], ROWSET_SECONDARY );
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
    SQLLEN     rowCount;
    int        rs;
    bool       rc = true;
    time_t     startTime;
    
	rs = GeneratingRows( rowsetSizes[ unitTest.rowsetSize ], numberOfRows[ unitTest.numberOfRows ], 
                         injectionTypes[ unitTest.injectionType ], tableTypes[ unitTest.tableType ], 
						 actions[ unitTest.action ], bindOrientations[ unitTest.bindOrientation ],
						 ROWSET_PRIMARY );

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
		//case OVERFLOW:
		//	expectedRowsetRetcode = SQL_ERROR;
		//	break;
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
                while( ( rowsetRetcode = SQLExecDirectW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStr[ 2 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING );
                break;
            case DELETE_PARAM:
                while( ( rowsetRetcode = SQLExecDirectW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStr[ 6 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING );
                break;
            case UPDATE:
				while( ( rowsetRetcode = SQLExecDirectW( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)ExecSQLStr[ 7 ]->ustr, SQL_NTS ) ) == SQL_STILL_EXECUTING );
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
		if (debug) {
			RecordToLog("Parameter Set  Status\n");
			RecordToLog("-------------  -------------\n");
		}
		if (expectedRowsetStatusArray[i] == rowsetStatusArray[i]) {
			switch (expectedRowsetStatusArray[i]) {
				case SQL_PARAM_SUCCESS:
  					if(debug) RecordToLog("%13d  Success\n", i+1);
					break;
				case SQL_PARAM_SUCCESS_WITH_INFO:
 					if(debug) RecordToLog("%13d  Success With Info\n", i+1);
					pSuccessinfo = true;
 					break;
				case SQL_PARAM_ERROR:
					if(debug) RecordToLog("%13d  Error  <-----\n", i+1);
					pSuccessinfo = true;
					break;
				case SQL_PARAM_UNUSED:
					if(debug) RecordToLog("%13d  Not processed\n", i+1);
					break;
				case SQL_PARAM_DIAG_UNAVAILABLE:
					if(debug) RecordToLog("%13d  Unknown\n", i+1);
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
   		RecordToLog(" >> ERROR: All the rows in rowset status array don't match with rowset returncode= %d, at line %d.\n", rowsetRetcode, __LINE__ );
		rc = false;
	}

    // Check to make sure the row count of affected rows is correct.
    retcode = SQLRowCount( handle[ SQL_HANDLE_STMT ], &rowCount );
    if( retcode != SQL_SUCCESS )    
    {
        RecordToLog( "    Failing API: SQLRowCount()\n" );
        CheckMsgs( "SQLRowCount()", __LINE__ );
        FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );
        return false;
    }

    if (debug) RecordToLog( "ExpectedRowcount=%d , ActualRowcount=%d\n", goodRowCount, rowCount );

	if( (int)rowCount != goodRowCount)
	{
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
		DisplayTable(bindOrientations[ unitTest.bindOrientation ],rowsetSizes[ unitTest.rowsetSize ], ROWSET_PRIMARY);
    }

	FreeRowsets( bindOrientations[ unitTest.bindOrientation ] );

    return rc;
}

bool CheckStr(char* type, UNICHAR* expected, UNICHAR* actual, int line, bool rc) {
	if( icu_strcmp(expected, actual) != 0 ) {
		RecordToLog( "ERROR: Data type: %s Expected: '%s' Actual '%s' at line %d\n", type, expected, actual, line );
		return false;
    } else {
		//if(debug)
			//RecordToLog( "MATCHED: Data type: %s Expected: '%s' Actual '%s' at line %d\n", type, expected, actual, line );
        if(rc) return true;
        else return false;
    }
}

bool CheckStrN(char* type, UNICHAR* expected, UNICHAR* actual, int size, int line, bool rc) {
	if( icu_strncmp(expected, actual, size) != 0 ) {
		RecordToLog( "ERROR: Data type: %s Expected: '%s' Actual '%s' at line %d\n", type, expected, actual, line );
		return false;
    } else {
		//if(debug)
			//RecordToLog( "MATCHED: Data type: %s Expected: '%s' Actual '%s' at line %d\n", type, expected, actual, line );
        if(rc) return true;
        else return false;
    }
}

bool CheckNum(char* type, int expected, int actual, int line, bool rc) {
	if(expected != actual) {
		RecordToLog( "ERROR: Data type: %s Expected: %d Actual %d at line %d\n", type, expected, actual, line );
		return false;
	} else {
		//if(debug)
			//RecordToLog( "MATCHED: Data type: %s Expected: %d Actual %d at line %d\n", type, expected, actual, line);
        if(rc) return true;
        else return false;
	}
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
	sprintf(ALM_buff, "odbc-%s|%s+%s+%s+%s|%s|%s - (case# %d - %d)|\n", 
		machine, "rowsets", "UNICODE", "ASCII", machine, testID, Description_string, nStartTest, nEndTest);
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